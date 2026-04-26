"""
W3-26: EMA Crossover Delta1
=============================
HYDROGEL + VEX with fast/slow EMA crossover for directional lean on fair value.
When fast EMA > slow EMA → bullish lean (buy more aggressively, widen sell)
When fast EMA < slow EMA → bearish lean (sell more aggressively, widen buy)

This tests whether short-term momentum signals can improve MM PnL.
The ac1=-0.13 for HYDRO suggests mean-reversion, but the EMA crossover
captures regime shifts in the mid-price trend.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200
VEX_LIMIT = 200
HG_CAP = 130
VEX_CAP = 110

# EMA params
FAST_ALPHA = 0.15      # fast EMA (~7 tick effective window)
SLOW_ALPHA = 0.03      # slow EMA (~33 tick effective window)
CROSS_GAIN = 1.5       # how much to shift fair on crossover signal

# HYDRO MM
HG_HALF = 3
HG_TEDGE = 3
HG_PSZ = 24
HG_TSZ = 16
HG_GAMMA = 2.0
HG_UW_THR = 85
HG_UW_Q = 18
HG_IMB_A = 0.3
HG_IMB_G = 2.0

# VEX MM
VEX_HALF = 2
VEX_TEDGE = 2
VEX_PSZ = 14
VEX_TSZ = 12
VEX_GAMMA = 2.0


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


def _mm(sym, limit, cap, od, pos, sd, prefix,
        half, tedge, psz, tsz, gamma, uw_thr, uw_q, use_cross=True):
    """Generic MM module with EMA crossover lean."""
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    if ba - bb < 1:
        return []

    micro = get_microprice(od)

    # Fast & slow EMA
    fk = prefix + "f"
    sk = prefix + "s"
    fast = FAST_ALPHA * micro + (1 - FAST_ALPHA) * sd.get(fk, micro)
    slow = SLOW_ALPHA * micro + (1 - SLOW_ALPHA) * sd.get(sk, micro)
    sd[fk] = fast
    sd[sk] = slow

    # Crossover signal: positive = bullish, negative = bearish
    cross = fast - slow
    cross_lean = clamp(CROSS_GAIN * cross, -3.0, 3.0) if use_cross else 0.0

    # Imbalance
    imb_raw = get_imbalance(od)
    ik = prefix + "i"
    imb = 0.3 * imb_raw + 0.7 * sd.get(ik, 0.0)
    sd[ik] = imb
    imb_shift = clamp(2.0 * imb, -3.0, 3.0)

    # Reservation price
    qfair = micro - gamma * (pos / max(1, cap)) + imb_shift + cross_lean

    orders = []
    b, s = 0, 0

    def br(): return max(0, min(cap, limit) - pos - b)
    def sr(): return max(0, min(cap, limit) + pos - s)

    # Aggressive takes
    for ap in sorted(od.sell_orders):
        if br() <= 0 or ap > qfair - tedge: break
        q = min(-od.sell_orders[ap], tsz, br())
        if q > 0: orders.append(Order(sym, ap, q)); b += q

    for bp in sorted(od.buy_orders, reverse=True):
        if sr() <= 0 or bp < qfair + tedge: break
        q = min(od.buy_orders[bp], tsz, sr())
        if q > 0: orders.append(Order(sym, bp, -q)); s += q

    # Unwind
    if pos >= uw_thr and sr() > 0:
        uq = min(uw_q, sr())
        orders.append(Order(sym, bb, -uq)); s += uq
    elif pos <= -uw_thr and br() > 0:
        uq = min(uw_q, br())
        orders.append(Order(sym, ba, uq)); b += uq

    # Passive
    h = half + (1 if abs(pos) > cap * 0.6 else 0)
    # Adjust half-spread directionally: when bullish, tighter bid / wider ask
    if cross > 1.0:
        h_bid = max(1, h - 1)
        h_ask = h + 1
    elif cross < -1.0:
        h_bid = h + 1
        h_ask = max(1, h - 1)
    else:
        h_bid, h_ask = h, h

    bp_px = int(round(qfair - h_bid))
    ap_px = int(round(qfair + h_ask))
    if bp_px >= ba: bp_px = ba - 1
    if ap_px <= bb: ap_px = bb + 1

    bsz = max(3, psz - int(pos * 0.2)) if pos > 0 else max(3, psz + int(-pos * 0.2)) if pos < 0 else psz
    ssz = max(3, psz + int(pos * 0.2)) if pos > 0 else max(3, psz - int(-pos * 0.2)) if pos < 0 else psz
    bq, sq = min(bsz, br()), min(ssz, sr())
    if bq > 0: orders.append(Order(sym, bp_px, bq))
    if sq > 0: orders.append(Order(sym, ap_px, -sq))

    return orders


class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sd = {}
        if state.traderData:
            try: sd = json.loads(state.traderData)
            except: sd = {}

        # HYDROGEL
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_pos = state.position.get(HG, 0)
            result[HG] = _mm(HG, HG_LIMIT, HG_CAP, hg_od, hg_pos, sd, "h",
                             HG_HALF, HG_TEDGE, HG_PSZ, HG_TSZ, HG_GAMMA, HG_UW_THR, HG_UW_Q)

        # VEX
        vex_od = state.order_depths.get(VEX)
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_pos = state.position.get(VEX, 0)
            result[VEX] = _mm(VEX, VEX_LIMIT, VEX_CAP, vex_od, vex_pos, sd, "v",
                              VEX_HALF, VEX_TEDGE, VEX_PSZ, VEX_TSZ, VEX_GAMMA,
                              int(VEX_CAP * 0.7), 15)

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
