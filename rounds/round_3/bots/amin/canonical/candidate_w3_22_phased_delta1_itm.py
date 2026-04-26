"""
W3-22: Phased Delta1 + ITM Stack
=================================
W3-21 architecture with C11-style time-phased risk management.
Phase 1 (tick 1-30K): AGGRESSIVE — max PnL accumulation
Phase 2 (tick 30K-80K): STANDARD — steady income, protect gains
Phase 3 (tick 80K-100K): CONSERVATIVE + UNWIND — flatten all positions

Architecture:
  1. HYDROGEL MM: Avellaneda-Stoikov + phase-dependent params
  2. VEX Kalman MM: Fair value anchor + phase-dependent sizing
  3. ITM 4000/4500 intrinsic residual: Phase-gated entry/exit

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────
# Phase boundaries
# ─────────────────────────────────────────────────
PHASE1_END = 30000
PHASE2_END = 80000
TOTAL_TICKS = 100000
STOP_NEW = 95000

# Position limits
HG_LIMIT = 200
VEX_LIMIT = 200
ITM_LIMIT = 300
ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}

# Kalman
KQ = 0.1
KR_VEX = 10.0

# ITM params
EXTR_ALPHA = 0.005
ITM_HALF_SPREAD = {"VEV_4000": 9, "VEV_4500": 7}
TAKE_EDGE_ITM = 10


def get_phase(tick):
    if tick <= PHASE1_END:
        return {
            "hg_cap": 140, "hg_half": 2, "hg_tedge": 2, "hg_psz": 30, "hg_tsz": 22,
            "hg_gamma": 1.5, "hg_uw_thr": 100, "hg_uw_q": 25,
            "vex_cap": 140, "vex_half": 1, "vex_tedge": 1, "vex_psz": 18, "vex_tsz": 15,
            "vex_gamma": 1.5,
            "itm_psz": 35, "itm_take": 12,
        }
    elif tick <= PHASE2_END:
        return {
            "hg_cap": 100, "hg_half": 3, "hg_tedge": 3, "hg_psz": 22, "hg_tsz": 15,
            "hg_gamma": 2.5, "hg_uw_thr": 70, "hg_uw_q": 18,
            "vex_cap": 100, "vex_half": 2, "vex_tedge": 2, "vex_psz": 12, "vex_tsz": 10,
            "vex_gamma": 2.5,
            "itm_psz": 25, "itm_take": 8,
        }
    else:
        prog = (tick - PHASE2_END) / (TOTAL_TICKS - PHASE2_END)
        fade = max(0.0, 1.0 - prog * 1.3)
        return {
            "hg_cap": max(5, int(50 * fade)), "hg_half": 4, "hg_tedge": 4,
            "hg_psz": max(3, int(12 * fade)), "hg_tsz": max(3, int(8 * fade)),
            "hg_gamma": 4.0, "hg_uw_thr": max(3, int(25 * fade)), "hg_uw_q": 20,
            "vex_cap": max(5, int(30 * fade)), "vex_half": 3, "vex_tedge": 3,
            "vex_psz": max(2, int(6 * fade)), "vex_tsz": max(2, int(5 * fade)),
            "vex_gamma": 4.0,
            "itm_psz": max(2, int(10 * fade)), "itm_take": max(2, int(5 * fade)),
        }


def get_microprice(od):
    if not od.buy_orders or not od.sell_orders:
        return None
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return (bb + ba) / 2.0
    return (bb * av + ba * bv) / total


def get_imbalance(od):
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    total = bv + av
    return (bv - av) / total if total > 0 else 0.0


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        tick = sd.get("t", 0) + 1
        sd["t"] = tick
        pp = get_phase(tick)
        no_new = tick > STOP_NEW

        # ══════════════════════════════════════════
        # HYDROGEL MM
        # ══════════════════════════════════════════
        hg_od = state.order_depths.get("HYDROGEL_PACK")
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get("HYDROGEL_PACK", 0)
                hg_cap = pp["hg_cap"]
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - pp["hg_gamma"] * (hg_pos / max(1, hg_cap)) + clamp(2.0 * hg_imb, -3, 3)

                hg_orders = []
                hg_b, hg_s = 0, 0

                def hgbr():
                    return max(0, min(hg_cap, HG_LIMIT) - hg_pos - hg_b)
                def hgsr():
                    return max(0, min(hg_cap, HG_LIMIT) + hg_pos - hg_s)

                # Aggressive takes
                if not no_new:
                    for ap in sorted(hg_od.sell_orders):
                        if hgbr() <= 0 or ap > hg_qfair - pp["hg_tedge"]:
                            break
                        q = min(-hg_od.sell_orders[ap], pp["hg_tsz"], hgbr())
                        if q > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", ap, q)); hg_b += q
                    for bp in sorted(hg_od.buy_orders, reverse=True):
                        if hgsr() <= 0 or bp < hg_qfair + pp["hg_tedge"]:
                            break
                        q = min(hg_od.buy_orders[bp], pp["hg_tsz"], hgsr())
                        if q > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", bp, -q)); hg_s += q

                # Unwind
                if hg_pos >= pp["hg_uw_thr"] and hgsr() > 0:
                    uq = min(pp["hg_uw_q"], hgsr())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uq)); hg_s += uq
                elif hg_pos <= -pp["hg_uw_thr"] and hgbr() > 0:
                    uq = min(pp["hg_uw_q"], hgbr())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uq)); hg_b += uq

                # Phase 3 extra forced unwind
                if tick > PHASE2_END and abs(hg_pos) > 5:
                    if hg_pos > 0:
                        uw = min(20, hg_pos, hgsr())
                        if uw > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uw)); hg_s += uw
                    else:
                        uw = min(20, -hg_pos, hgbr())
                        if uw > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uw)); hg_b += uw

                # Passive quotes
                if not no_new:
                    half = pp["hg_half"] + (1 if abs(hg_pos) > hg_cap * 0.6 else 0)
                    hbp = int(round(hg_qfair - half))
                    hap = int(round(hg_qfair + half))
                    if hbp >= hg_ba: hbp = hg_ba - 1
                    if hap <= hg_bb: hap = hg_bb + 1
                    psz = pp["hg_psz"]
                    bsz = max(3, psz - int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz + int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                    ssz = max(3, psz + int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz - int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                    bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                    if bq > 0: hg_orders.append(Order("HYDROGEL_PACK", hbp, bq))
                    if sq > 0: hg_orders.append(Order("HYDROGEL_PACK", hap, -sq))

                result["HYDROGEL_PACK"] = hg_orders

        # ══════════════════════════════════════════
        # VEX Kalman MM
        # ══════════════════════════════════════════
        vex_od = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_fair = None

        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get("VELVETFRUIT_EXTRACT", 0)
            vex_cap = pp["vex_cap"]

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR_VEX)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]

            vfv = round(vex_fair)
            adj = vex_fair - pp["vex_gamma"] * (vex_pos / max(1, vex_cap))

            vex_orders = []
            vb, vs = 0, 0

            def vbr():
                return max(0, min(vex_cap, VEX_LIMIT) - vex_pos - vb)
            def vsr():
                return max(0, min(vex_cap, VEX_LIMIT) + vex_pos - vs)

            if not no_new:
                if vex_ba <= vfv - pp["vex_tedge"]:
                    q = min(-vex_od.sell_orders[vex_ba], pp["vex_tsz"], vbr())
                    if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, q)); vb += q
                if vex_bb >= vfv + pp["vex_tedge"]:
                    q = min(vex_od.buy_orders[vex_bb], pp["vex_tsz"], vsr())
                    if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -q)); vs += q

            # Phase 3 VEX unwind
            if tick > PHASE2_END and abs(vex_pos) > 5:
                if vex_pos > 0 and vsr() > 0:
                    uw = min(15, vex_pos, vsr())
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -uw)); vs += uw
                elif vex_pos < 0 and vbr() > 0:
                    uw = min(15, -vex_pos, vbr())
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, uw)); vb += uw

            # Passive quotes
            if not no_new:
                bp = int(round(adj - pp["vex_half"]))
                ap = int(round(adj + pp["vex_half"]))
                if bp >= vex_ba: bp = vex_ba - 1
                if ap <= vex_bb: ap = vex_bb + 1
                bq, sq = min(pp["vex_psz"], vbr()), min(pp["vex_psz"], vsr())
                if bq > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", bp, bq))
                if sq > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", ap, -sq))

            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ══════════════════════════════════════════
        # ITM Voucher Intrinsic Residual
        # ══════════════════════════════════════════
        if vex_fair is not None and not no_new:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders:
                    continue
                bb, ba = max(od.buy_orders), min(od.sell_orders)
                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)

                intrinsic = max(0.0, vex_fair - strike)
                curr_extr = max(0.0, v_mid - intrinsic)
                st = sd.setdefault(sym, {"ema": 0.01})
                ema = EXTR_ALPHA * curr_extr + (1 - EXTR_ALPHA) * st["ema"]
                st["ema"] = ema
                fair = intrinsic + ema

                orders = []
                ib, is_ = 0, 0

                # Aggressive
                if ba < fair - TAKE_EDGE_ITM:
                    q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                    if q > 0: orders.append(Order(sym, ba, q)); ib += q
                if bb > fair + TAKE_EDGE_ITM:
                    q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                    if q > 0: orders.append(Order(sym, bb, -q)); is_ += q

                # Passive
                half_s = ITM_HALF_SPREAD[sym]
                bid_px = int(round(fair - half_s))
                ask_px = int(round(fair + half_s))
                if bid_px >= ba: bid_px = ba - 1
                if ask_px <= bb: ask_px = bb + 1

                dev = curr_extr - ema
                psz = pp["itm_psz"]
                b_sz = max(2, min(psz + int(5 * (-dev)), ITM_LIMIT - pos - ib))
                a_sz = max(2, min(psz + int(5 * dev), ITM_LIMIT + pos - is_))
                if b_sz > 0 and bid_px > 0:
                    orders.append(Order(sym, bid_px, b_sz))
                if a_sz > 0 and ask_px > 0:
                    orders.append(Order(sym, ask_px, -a_sz))

                result[sym] = orders

        # Phase 3 ITM unwind
        if tick > PHASE2_END and vex_fair is not None:
            for sym in ITM_SYMS:
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders:
                    continue
                pos = state.position.get(sym, 0)
                if abs(pos) > 5:
                    bb, ba = max(od.buy_orders), min(od.sell_orders)
                    orders = result.get(sym, [])
                    if pos > 0:
                        uw = min(20, pos, ITM_LIMIT + pos)
                        if uw > 0: orders.append(Order(sym, bb, -uw))
                    else:
                        uw = min(20, -pos, ITM_LIMIT - pos)
                        if uw > 0: orders.append(Order(sym, ba, uw))
                    result[sym] = orders

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
