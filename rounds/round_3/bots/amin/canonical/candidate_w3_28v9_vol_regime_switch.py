"""
W3-28v9: Volatility Regime Switch
===================================
Base: W3-28 (+1,168)

STRUCTURAL CHANGES:
  1. Tracks rolling realized volatility (EMA of |mid change|) for HYDRO.
  2. LOW-VOL regime (vol < threshold): tighter spreads (half=2), larger passive
     sizes, no aggressive takes. Pure spread capture.
  3. HIGH-VOL regime (vol >= threshold): wider spreads (half=5), aggressive takes
     at smaller edge, smaller passive sizes. Avoid getting run over.
  4. EXTREME-VOL regime (vol > 2x threshold): stop quoting passively, only take
     obvious mispricings. Full defensive mode.
  5. Regime detection is applied to all products (HYDRO adapts half-spread,
     VEX adapts take aggression, ITM adapts sizing).
  6. V3 endgame unwind included.

Hypothesis: Flat PnL at +1,168 across variants means the bot behaves the same
in aggregate. A volatility regime switch changes WHEN we trade (aggressive in
calm, defensive in storms) which should change the position trajectory.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200; VEX_LIMIT = 200; ITM_LIMIT = 300

HG_CAP = 155; VEX_CAP = 120
HG_PSZ = 28; VEX_PSZ = 15
HG_TSZ = 22; VEX_TSZ = 12
HG_TEDGE = 2; VEX_TEDGE = 2

EXP_GAMMA = 3.0

# Volatility regime thresholds (in absolute mid-change units)
VOL_ALPHA = 0.05          # EMA decay for realized vol
VOL_LOW_THRESH = 3.0      # below = low vol
VOL_HIGH_THRESH = 8.0     # above = extreme vol

# Regime-specific half-spreads for HYDRO
HG_HALF_LOW = 2           # tight in calm markets
HG_HALF_NORM = 3          # normal
HG_HALF_HIGH = 5          # wide in volatile markets

KQ = 0.1; KR = 10.0

ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}
ITM_HS = {"VEV_4000": 9, "VEV_4500": 7}
ITM_TAKE = 10; ITM_PSZ = 30
EXTR_ALPHA = 0.005

PHASE3_START = 80000
STOP_NEW = 95000
TOTAL_TICKS = 100000


def get_microprice(od):
    if not od.buy_orders or not od.sell_orders: return None
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    t = bv + av
    return (bb * av + ba * bv) / t if t > 0 else (bb + ba) / 2.0


def get_imbalance(od):
    if not od.buy_orders or not od.sell_orders: return 0.0
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    t = bv + av
    return (bv - av) / t if t > 0 else 0.0


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


def exp_penalty(pos, cap):
    q = pos / max(1, cap)
    sign = 1.0 if q >= 0 else -1.0
    return sign * EXP_GAMMA * (math.exp(abs(q)) - 1.0) / (math.e - 1.0)


def prop_size(base, pos, cap, side):
    if side == "buy":
        room = max(0, cap - pos)
    else:
        room = max(0, cap + pos)
    frac = room / max(1, cap)
    return max(2, int(base * frac))


def phase3_fade(tick):
    if tick <= PHASE3_START: return 1.0
    progress = (tick - PHASE3_START) / (TOTAL_TICKS - PHASE3_START)
    return max(0.0, 1.0 - progress * 1.2)


class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sd = {}
        if state.traderData:
            try: sd = json.loads(state.traderData)
            except: sd = {}

        tick = sd.get("t", 0) + 1
        sd["t"] = tick
        fade = phase3_fade(tick)
        no_new = tick > STOP_NEW
        in_p3 = tick > PHASE3_START

        eff_hg_cap = max(5, int(HG_CAP * fade)) if in_p3 else HG_CAP
        eff_vex_cap = max(5, int(VEX_CAP * fade)) if in_p3 else VEX_CAP

        # ═══════════════════════════════════════
        # VOLATILITY REGIME DETECTION
        # ═══════════════════════════════════════
        hg_od = state.order_depths.get(HG)
        vol_regime = "normal"
        rv = sd.get("rv", 3.0)

        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            hg_mid = (hg_bb + hg_ba) / 2.0
            prev_mid = sd.get("pm", hg_mid)
            sd["pm"] = hg_mid
            abs_change = abs(hg_mid - prev_mid)
            rv = VOL_ALPHA * abs_change + (1 - VOL_ALPHA) * rv
            sd["rv"] = rv

            if rv < VOL_LOW_THRESH:
                vol_regime = "low"
            elif rv > VOL_HIGH_THRESH:
                vol_regime = "extreme"
            else:
                vol_regime = "normal"

        # ═══════════════════════════════════════
        # HYDROGEL MM — regime-adaptive
        # ═══════════════════════════════════════
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get(HG, 0)
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - exp_penalty(hg_pos, eff_hg_cap) + clamp(2.0 * hg_imb, -3, 3)

                hg_orders = []
                hg_b, hg_s = 0, 0
                def hgbr(): return max(0, min(eff_hg_cap, HG_LIMIT) - hg_pos - hg_b)
                def hgsr(): return max(0, min(eff_hg_cap, HG_LIMIT) + hg_pos - hg_s)

                # Regime-adaptive take edge
                if vol_regime == "low":
                    take_edge = 1  # take on small edge in calm markets
                    take_sz = HG_TSZ + 5
                elif vol_regime == "extreme":
                    take_edge = 5  # only take on big edge in storms
                    take_sz = 10
                else:
                    take_edge = HG_TEDGE
                    take_sz = HG_TSZ

                if not no_new:
                    for ap in sorted(hg_od.sell_orders):
                        if hgbr() <= 0 or ap > hg_qfair - take_edge: break
                        q = min(-hg_od.sell_orders[ap], take_sz, hgbr())
                        if q > 0: hg_orders.append(Order(HG, ap, q)); hg_b += q
                    for bp in sorted(hg_od.buy_orders, reverse=True):
                        if hgsr() <= 0 or bp < hg_qfair + take_edge: break
                        q = min(hg_od.buy_orders[bp], take_sz, hgsr())
                        if q > 0: hg_orders.append(Order(HG, bp, -q)); hg_s += q

                # Unwind
                if hg_pos > eff_hg_cap * 0.6 and hgsr() > 0:
                    uq = min(20, hgsr())
                    hg_orders.append(Order(HG, hg_bb, -uq)); hg_s += uq
                elif hg_pos < -eff_hg_cap * 0.6 and hgbr() > 0:
                    uq = min(20, hgbr())
                    hg_orders.append(Order(HG, hg_ba, uq)); hg_b += uq

                # Phase 3 forced unwind
                if in_p3 and abs(hg_pos) > 5:
                    if hg_pos > 0:
                        uw = min(25, hg_pos, HG_LIMIT + hg_pos - hg_s)
                        if uw > 0: hg_orders.append(Order(HG, hg_bb, -uw)); hg_s += uw
                    else:
                        uw = min(25, -hg_pos, HG_LIMIT - hg_pos - hg_b)
                        if uw > 0: hg_orders.append(Order(HG, hg_ba, uw)); hg_b += uw

                # Regime-adaptive passive quotes
                if not no_new and vol_regime != "extreme":
                    if vol_regime == "low":
                        half = HG_HALF_LOW
                        psz_mult = 1.3  # larger size in calm
                    else:
                        half = HG_HALF_NORM
                        psz_mult = 1.0

                    half = half + (1 if abs(hg_pos) > eff_hg_cap * 0.5 else 0)
                    hbp = int(round(hg_qfair - half))
                    hap = int(round(hg_qfair + half))
                    if hbp >= hg_ba: hbp = hg_ba - 1
                    if hap <= hg_bb: hap = hg_bb + 1
                    bsz = max(2, int(prop_size(HG_PSZ, hg_pos, eff_hg_cap, "buy") * psz_mult))
                    ssz = max(2, int(prop_size(HG_PSZ, hg_pos, eff_hg_cap, "sell") * psz_mult))
                    bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                    if bq > 0: hg_orders.append(Order(HG, hbp, bq))
                    if sq > 0: hg_orders.append(Order(HG, hap, -sq))
                elif not no_new and vol_regime == "extreme":
                    # In extreme vol: wide defensive quotes only
                    half = HG_HALF_HIGH + (2 if abs(hg_pos) > eff_hg_cap * 0.4 else 0)
                    hbp = int(round(hg_qfair - half))
                    hap = int(round(hg_qfair + half))
                    if hbp >= hg_ba: hbp = hg_ba - 1
                    if hap <= hg_bb: hap = hg_bb + 1
                    bsz = prop_size(int(HG_PSZ * 0.5), hg_pos, eff_hg_cap, "buy")
                    ssz = prop_size(int(HG_PSZ * 0.5), hg_pos, eff_hg_cap, "sell")
                    bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                    if bq > 0: hg_orders.append(Order(HG, hbp, bq))
                    if sq > 0: hg_orders.append(Order(HG, hap, -sq))
                result[HG] = hg_orders

        # ═══════════════════════════════════════
        # VEX Kalman MM — regime-adaptive
        # ═══════════════════════════════════════
        vex_od = state.order_depths.get(VEX)
        vex_fair = None
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get(VEX, 0)

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]
            vfv = round(vex_fair)
            adj = vex_fair - exp_penalty(vex_pos, eff_vex_cap)

            vex_orders = []
            vb, vs = 0, 0
            def vbr(): return max(0, min(eff_vex_cap, VEX_LIMIT) - vex_pos - vb)
            def vsr(): return max(0, min(eff_vex_cap, VEX_LIMIT) + vex_pos - vs)

            # Skip VEX takes in extreme vol
            if not no_new and vol_regime != "extreme":
                if vex_ba <= vfv - VEX_TEDGE:
                    q = min(-vex_od.sell_orders[vex_ba], VEX_TSZ, vbr())
                    if q > 0: vex_orders.append(Order(VEX, vex_ba, q)); vb += q
                if vex_bb >= vfv + VEX_TEDGE:
                    q = min(vex_od.buy_orders[vex_bb], VEX_TSZ, vsr())
                    if q > 0: vex_orders.append(Order(VEX, vex_bb, -q)); vs += q

            if in_p3 and abs(vex_pos) > 5:
                if vex_pos > 0 and vsr() > 0:
                    uw = min(20, vex_pos, vsr())
                    vex_orders.append(Order(VEX, vex_bb, -uw)); vs += uw
                elif vex_pos < 0 and vbr() > 0:
                    uw = min(20, -vex_pos, vbr())
                    vex_orders.append(Order(VEX, vex_ba, uw)); vb += uw

            if not no_new:
                vex_half = 2 if vol_regime == "low" else (4 if vol_regime == "extreme" else 2)
                bp = int(round(adj - vex_half)); ap = int(round(adj + vex_half))
                if bp >= vex_ba: bp = vex_ba - 1
                if ap <= vex_bb: ap = vex_bb + 1
                vpsz = VEX_PSZ if vol_regime != "extreme" else int(VEX_PSZ * 0.6)
                bsz = prop_size(vpsz, vex_pos, eff_vex_cap, "buy")
                ssz = prop_size(vpsz, vex_pos, eff_vex_cap, "sell")
                bq, sq = min(bsz, vbr()), min(ssz, vsr())
                if bq > 0: vex_orders.append(Order(VEX, bp, bq))
                if sq > 0: vex_orders.append(Order(VEX, ap, -sq))
            result[VEX] = vex_orders

        # ═══════════════════════════════════════
        # ITM Voucher Residual — regime-adaptive sizing
        # ═══════════════════════════════════════
        if vex_fair is not None:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders: continue
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

                # In extreme vol, widen ITM take edge
                itm_tedge = ITM_TAKE if vol_regime != "extreme" else 18

                if not no_new:
                    if ba < fair - itm_tedge:
                        q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                        if q > 0: orders.append(Order(sym, ba, q)); ib += q
                    if bb > fair + itm_tedge:
                        q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                        if q > 0: orders.append(Order(sym, bb, -q)); is_ += q

                    half_s = ITM_HS[sym] + (2 if vol_regime == "extreme" else 0)
                    bid_px = int(round(fair - half_s)); ask_px = int(round(fair + half_s))
                    if bid_px >= ba: bid_px = ba - 1
                    if ask_px <= bb: ask_px = bb + 1
                    dev = curr_extr - ema
                    psz = max(5, int(ITM_PSZ * fade)) if in_p3 else ITM_PSZ
                    if vol_regime == "extreme":
                        psz = max(5, int(psz * 0.5))
                    b_sz = max(2, min(psz + int(5 * (-dev)), ITM_LIMIT - pos - ib))
                    a_sz = max(2, min(psz + int(5 * dev), ITM_LIMIT + pos - is_))
                    if b_sz > 0 and bid_px > 0: orders.append(Order(sym, bid_px, b_sz))
                    if a_sz > 0 and ask_px > 0: orders.append(Order(sym, ask_px, -a_sz))

                if in_p3 and abs(pos) > 5:
                    if pos > 0:
                        uw = min(25, pos, ITM_LIMIT + pos - is_)
                        if uw > 0: orders.append(Order(sym, bb, -uw))
                    else:
                        uw = min(25, -pos, ITM_LIMIT - pos - ib)
                        if uw > 0: orders.append(Order(sym, ba, uw))

                result[sym] = orders

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
