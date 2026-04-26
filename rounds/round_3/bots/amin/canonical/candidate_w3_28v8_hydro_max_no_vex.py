"""
W3-28v8: HYDRO Max + No VEX + Triple ITM
==========================================
Base: W3-28 (+1,168)

STRUCTURAL CHANGES:
  1. VEX completely removed — zero VEX orders. VEX leg historically adds
     noise/risk without clear PnL. By dropping it we eliminate adverse
     selection and simplify inventory.
  2. HYDRO cap raised to full limit (200). All capacity goes to the
     strongest product.
  3. Added VEV_5000 as a third ITM strike. It's deeper OTM than 4000/4500
     but still ITM enough to have residual edge.
  4. VEX Kalman still runs (needed for ITM fair pricing) but produces
     ZERO orders.
  5. V1 aggressive params + V3 endgame unwind included.

Hypothesis: VEX is a PnL drag or neutral. Dropping it and maxing HYDRO
should change position trajectory. Adding VEV_5000 diversifies ITM edge.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200; VEX_LIMIT = 200; ITM_LIMIT = 300

# ALL capacity to HYDRO
HG_CAP = 200
HG_HALF = 3
HG_PSZ = 30
HG_TSZ = 24
HG_TEDGE = 2

EXP_GAMMA = 3.0
IMB_GAIN = 2.0

KQ = 0.1; KR = 10.0

# Three ITM strikes now
ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500, "VEV_5000": 5000}
ITM_HS = {"VEV_4000": 9, "VEV_4500": 7, "VEV_5000": 6}
ITM_TAKE = 10; ITM_PSZ = 30
ITM_5000_PSZ = 20   # smaller size for the riskier strike
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

        eff_hg_cap = max(10, int(HG_CAP * fade)) if in_p3 else HG_CAP

        # ═══════════════════════════════════════
        # HYDROGEL MM — MAX CAPACITY
        # ═══════════════════════════════════════
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get(HG, 0)
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - exp_penalty(hg_pos, eff_hg_cap) + clamp(IMB_GAIN * hg_imb, -3, 3)

                hg_orders = []
                hg_b, hg_s = 0, 0
                def hgbr(): return max(0, min(eff_hg_cap, HG_LIMIT) - hg_pos - hg_b)
                def hgsr(): return max(0, min(eff_hg_cap, HG_LIMIT) + hg_pos - hg_s)

                if not no_new:
                    for ap in sorted(hg_od.sell_orders):
                        if hgbr() <= 0 or ap > hg_qfair - HG_TEDGE: break
                        q = min(-hg_od.sell_orders[ap], HG_TSZ, hgbr())
                        if q > 0: hg_orders.append(Order(HG, ap, q)); hg_b += q
                    for bp in sorted(hg_od.buy_orders, reverse=True):
                        if hgsr() <= 0 or bp < hg_qfair + HG_TEDGE: break
                        q = min(hg_od.buy_orders[bp], HG_TSZ, hgsr())
                        if q > 0: hg_orders.append(Order(HG, bp, -q)); hg_s += q

                if hg_pos > eff_hg_cap * 0.55 and hgsr() > 0:
                    uq = min(25, hgsr())
                    hg_orders.append(Order(HG, hg_bb, -uq)); hg_s += uq
                elif hg_pos < -eff_hg_cap * 0.55 and hgbr() > 0:
                    uq = min(25, hgbr())
                    hg_orders.append(Order(HG, hg_ba, uq)); hg_b += uq

                # Phase 3 forced unwind
                if in_p3 and abs(hg_pos) > 5:
                    if hg_pos > 0:
                        uw = min(30, hg_pos, HG_LIMIT + hg_pos - hg_s)
                        if uw > 0: hg_orders.append(Order(HG, hg_bb, -uw)); hg_s += uw
                    else:
                        uw = min(30, -hg_pos, HG_LIMIT - hg_pos - hg_b)
                        if uw > 0: hg_orders.append(Order(HG, hg_ba, uw)); hg_b += uw

                if not no_new:
                    half = HG_HALF + (1 if abs(hg_pos) > eff_hg_cap * 0.45 else 0)
                    hbp = int(round(hg_qfair - half))
                    hap = int(round(hg_qfair + half))
                    if hbp >= hg_ba: hbp = hg_ba - 1
                    if hap <= hg_bb: hap = hg_bb + 1
                    bsz = prop_size(HG_PSZ, hg_pos, eff_hg_cap, "buy")
                    ssz = prop_size(HG_PSZ, hg_pos, eff_hg_cap, "sell")
                    bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                    if bq > 0: hg_orders.append(Order(HG, hbp, bq))
                    if sq > 0: hg_orders.append(Order(HG, hap, -sq))
                result[HG] = hg_orders

        # ═══════════════════════════════════════
        # VEX — OBSERVATION ONLY (no orders)
        # Still run Kalman to get vex_fair for ITM pricing
        # ═══════════════════════════════════════
        vex_od = state.order_depths.get(VEX)
        vex_fair = None
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]
            # NO VEX ORDERS — intentionally skipped

        # ═══════════════════════════════════════
        # ITM Voucher Residual — 3 strikes
        # ═══════════════════════════════════════
        if vex_fair is not None:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders: continue
                bb, ba = max(od.buy_orders), min(od.sell_orders)
                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)
                intrinsic = max(0.0, vex_fair - strike)

                # Skip if not ITM enough (VEV_5000 protection)
                if intrinsic < 5 and strike >= 5000:
                    continue

                curr_extr = max(0.0, v_mid - intrinsic)
                st = sd.setdefault(sym, {"ema": 0.01})
                ema = EXTR_ALPHA * curr_extr + (1 - EXTR_ALPHA) * st["ema"]
                st["ema"] = ema
                fair = intrinsic + ema

                base_psz = ITM_5000_PSZ if strike >= 5000 else ITM_PSZ
                orders = []
                ib, is_ = 0, 0

                if not no_new:
                    take_edge = ITM_TAKE if strike < 5000 else 15  # wider edge for 5000
                    if ba < fair - take_edge:
                        q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                        if q > 0: orders.append(Order(sym, ba, q)); ib += q
                    if bb > fair + take_edge:
                        q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                        if q > 0: orders.append(Order(sym, bb, -q)); is_ += q

                    half_s = ITM_HS[sym]
                    bid_px = int(round(fair - half_s)); ask_px = int(round(fair + half_s))
                    if bid_px >= ba: bid_px = ba - 1
                    if ask_px <= bb: ask_px = bb + 1
                    dev = curr_extr - ema
                    psz = max(5, int(base_psz * fade)) if in_p3 else base_psz
                    b_sz = max(2, min(psz + int(5 * (-dev)), ITM_LIMIT - pos - ib))
                    a_sz = max(2, min(psz + int(5 * dev), ITM_LIMIT + pos - is_))
                    if b_sz > 0 and bid_px > 0: orders.append(Order(sym, bid_px, b_sz))
                    if a_sz > 0 and ask_px > 0: orders.append(Order(sym, ask_px, -a_sz))

                # Phase 3 ITM unwind
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
