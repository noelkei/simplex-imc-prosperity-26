"""
W3-29: Phased Delta1 + Cross-Voucher Spread
=============================================
Combines:
  1. C11-style phased risk management (aggressive→standard→unwind)
  2. HYDROGEL + VEX delta-1 MM (proven profitable)
  3. Cross-voucher spread reversion between VEV_5200/5300
     (250-400 z-score crosses/day — untested opportunity)

Phase 3 flattens everything including spread positions.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# Phase boundaries
PHASE1_END = 30000
PHASE2_END = 80000
TOTAL_TICKS = 100000
STOP_NEW = 95000

HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
V52 = "VEV_5200"
V53 = "VEV_5300"
HG_LIMIT = 200; VEX_LIMIT = 200; V_LIMIT = 300

# Spread params
SPREAD_EMA_A = 0.01
SPREAD_VOL_A = 0.02
ENTRY_Z = 1.8
EXIT_Z = 0.3


def get_phase(tick):
    if tick <= PHASE1_END:
        return {
            "hg_cap": 140, "hg_half": 2, "hg_tedge": 2, "hg_psz": 30,
            "hg_tsz": 22, "hg_gamma": 1.5, "hg_uw": 100,
            "vex_cap": 130, "vex_half": 1, "vex_tedge": 1, "vex_psz": 16,
            "vex_tsz": 14, "vex_gamma": 1.5, "vex_uw": 90,
            "sp_cap": 35, "sp_sz": 8,
        }
    elif tick <= PHASE2_END:
        return {
            "hg_cap": 100, "hg_half": 3, "hg_tedge": 3, "hg_psz": 22,
            "hg_tsz": 15, "hg_gamma": 2.5, "hg_uw": 70,
            "vex_cap": 90, "vex_half": 2, "vex_tedge": 2, "vex_psz": 12,
            "vex_tsz": 10, "vex_gamma": 2.5, "vex_uw": 60,
            "sp_cap": 25, "sp_sz": 5,
        }
    else:
        prog = (tick - PHASE2_END) / (TOTAL_TICKS - PHASE2_END)
        fade = max(0.0, 1.0 - prog * 1.3)
        return {
            "hg_cap": max(5, int(50 * fade)), "hg_half": 4, "hg_tedge": 4,
            "hg_psz": max(3, int(12 * fade)), "hg_tsz": max(3, int(8 * fade)),
            "hg_gamma": 4.0, "hg_uw": max(3, int(25 * fade)),
            "vex_cap": max(5, int(30 * fade)), "vex_half": 3, "vex_tedge": 3,
            "vex_psz": max(2, int(6 * fade)), "vex_tsz": max(2, int(5 * fade)),
            "vex_gamma": 4.0, "vex_uw": max(3, int(15 * fade)),
            "sp_cap": max(0, int(10 * fade)), "sp_sz": max(1, int(3 * fade)),
        }


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


def mm_module(sym, limit, od, pos, sd, prefix, pp, cap_k, half_k, tedge_k, psz_k, tsz_k, gamma_k, uw_k):
    cap = pp[cap_k]
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    if ba - bb < 1: return []

    micro = get_microprice(od)
    ik = prefix + "i"
    imb = 0.3 * get_imbalance(od) + 0.7 * sd.get(ik, 0.0)
    sd[ik] = imb
    qfair = micro - pp[gamma_k] * (pos / max(1, cap)) + clamp(2.0 * imb, -3, 3)

    orders = []
    b, s = 0, 0
    def br(): return max(0, min(cap, limit) - pos - b)
    def sr(): return max(0, min(cap, limit) + pos - s)

    for ap in sorted(od.sell_orders):
        if br() <= 0 or ap > qfair - pp[tedge_k]: break
        q = min(-od.sell_orders[ap], pp[tsz_k], br())
        if q > 0: orders.append(Order(sym, ap, q)); b += q
    for bp in sorted(od.buy_orders, reverse=True):
        if sr() <= 0 or bp < qfair + pp[tedge_k]: break
        q = min(od.buy_orders[bp], pp[tsz_k], sr())
        if q > 0: orders.append(Order(sym, bp, -q)); s += q

    if pos >= pp[uw_k] and sr() > 0:
        uq = min(20, sr()); orders.append(Order(sym, bb, -uq)); s += uq
    elif pos <= -pp[uw_k] and br() > 0:
        uq = min(20, br()); orders.append(Order(sym, ba, uq)); b += uq

    half = pp[half_k] + (1 if abs(pos) > cap * 0.6 else 0)
    hbp = int(round(qfair - half)); hap = int(round(qfair + half))
    if hbp >= ba: hbp = ba - 1
    if hap <= bb: hap = bb + 1
    psz = pp[psz_k]
    bsz = max(3, psz - int(pos * 0.2)) if pos > 0 else max(3, psz + int(-pos * 0.2)) if pos < 0 else psz
    ssz = max(3, psz + int(pos * 0.2)) if pos > 0 else max(3, psz - int(-pos * 0.2)) if pos < 0 else psz
    bq, sq = min(bsz, br()), min(ssz, sr())
    if bq > 0: orders.append(Order(sym, hbp, bq))
    if sq > 0: orders.append(Order(sym, hap, -sq))
    return orders


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
        pp = get_phase(tick)
        no_new = tick > STOP_NEW

        # HYDROGEL
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_pos = state.position.get(HG, 0)
            if not no_new:
                result[HG] = mm_module(HG, HG_LIMIT, hg_od, hg_pos, sd, "h", pp,
                                        "hg_cap", "hg_half", "hg_tedge", "hg_psz", "hg_tsz", "hg_gamma", "hg_uw")
            elif abs(hg_pos) > 5:
                # Phase 3 forced unwind
                hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
                o = []
                if hg_pos > 0:
                    o.append(Order(HG, hg_bb, -min(25, hg_pos, HG_LIMIT + hg_pos)))
                else:
                    o.append(Order(HG, hg_ba, min(25, -hg_pos, HG_LIMIT - hg_pos)))
                result[HG] = o

        # VEX
        vex_od = state.order_depths.get(VEX)
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_pos = state.position.get(VEX, 0)
            if not no_new:
                result[VEX] = mm_module(VEX, VEX_LIMIT, vex_od, vex_pos, sd, "v", pp,
                                         "vex_cap", "vex_half", "vex_tedge", "vex_psz", "vex_tsz", "vex_gamma", "vex_uw")
            elif abs(vex_pos) > 5:
                vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
                o = []
                if vex_pos > 0:
                    o.append(Order(VEX, vex_bb, -min(20, vex_pos, VEX_LIMIT + vex_pos)))
                else:
                    o.append(Order(VEX, vex_ba, min(20, -vex_pos, VEX_LIMIT - vex_pos)))
                result[VEX] = o

        # ══════════════════════════════════════════
        # CROSS-VOUCHER SPREAD: VEV_5200 vs VEV_5300
        # ══════════════════════════════════════════
        od52 = state.order_depths.get(V52)
        od53 = state.order_depths.get(V53)

        if (od52 and od52.buy_orders and od52.sell_orders and
                od53 and od53.buy_orders and od53.sell_orders):
            bb52, ba52 = max(od52.buy_orders), min(od52.sell_orders)
            bb53, ba53 = max(od53.buy_orders), min(od53.sell_orders)
            mid52 = (bb52 + ba52) / 2.0
            mid53 = (bb53 + ba53) / 2.0

            spread = mid52 - mid53
            sp_ema = SPREAD_EMA_A * spread + (1 - SPREAD_EMA_A) * sd.get("se", spread)
            sd["se"] = sp_ema
            sp_dev = abs(spread - sp_ema)
            sp_vol = SPREAD_VOL_A * sp_dev + (1 - SPREAD_VOL_A) * sd.get("sv", 5.0)
            sp_vol = max(sp_vol, 0.5)
            sd["sv"] = sp_vol
            z = (spread - sp_ema) / sp_vol

            pos52 = state.position.get(V52, 0)
            pos53 = state.position.get(V53, 0)
            sp_cap = pp["sp_cap"]
            sp_sz = pp["sp_sz"]

            o52, o53 = [], []

            if not no_new:
                if z > ENTRY_Z:
                    # Spread high: sell 5200, buy 5300
                    if pos52 > -sp_cap:
                        q = min(sp_sz, sp_cap + pos52, V_LIMIT + pos52)
                        if q > 0: o52.append(Order(V52, bb52, -q))
                    if pos53 < sp_cap:
                        q = min(sp_sz, sp_cap - pos53, V_LIMIT - pos53)
                        if q > 0: o53.append(Order(V53, ba53, q))
                elif z < -ENTRY_Z:
                    # Spread low: buy 5200, sell 5300
                    if pos52 < sp_cap:
                        q = min(sp_sz, sp_cap - pos52, V_LIMIT - pos52)
                        if q > 0: o52.append(Order(V52, ba52, q))
                    if pos53 > -sp_cap:
                        q = min(sp_sz, sp_cap + pos53, V_LIMIT + pos53)
                        if q > 0: o53.append(Order(V53, bb53, -q))
                elif abs(z) < EXIT_Z:
                    # Flatten
                    if pos52 > 0:
                        o52.append(Order(V52, bb52, -min(sp_sz, pos52)))
                    elif pos52 < 0:
                        o52.append(Order(V52, ba52, min(sp_sz, -pos52)))
                    if pos53 > 0:
                        o53.append(Order(V53, bb53, -min(sp_sz, pos53)))
                    elif pos53 < 0:
                        o53.append(Order(V53, ba53, min(sp_sz, -pos53)))
            else:
                # No new, flatten all
                if pos52 > 0:
                    o52.append(Order(V52, bb52, -min(20, pos52)))
                elif pos52 < 0:
                    o52.append(Order(V52, ba52, min(20, -pos52)))
                if pos53 > 0:
                    o53.append(Order(V53, bb53, -min(20, pos53)))
                elif pos53 < 0:
                    o53.append(Order(V53, ba53, min(20, -pos53)))

            if o52: result[V52] = o52
            if o53: result[V53] = o53

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
