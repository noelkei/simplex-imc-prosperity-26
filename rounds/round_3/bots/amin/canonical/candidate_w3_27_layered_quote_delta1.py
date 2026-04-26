"""
W3-27: Layered Quote HYDRO + VEX
==================================
Multi-level passive quoting strategy inspired by professional market makers.
Instead of single bid/ask, places 3 levels of quotes at increasing distances:
  Level 1: tight (2 from fair), medium size — captures small mean-reverting moves
  Level 2: mid (4 from fair), medium size — captures moderate moves
  Level 3: wide (6 from fair), small size — captures large moves, high edge

This captures more of the HYDROGEL spread distribution:
  - 79% of ticks move ≥1 → Level 1 fills often
  - 46% move ≥2 → Level 2 fills 
  - 22% move ≥3 → Level 3 fills with highest edge

Also includes VEX simple MM for additional delta-1 PnL.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200
VEX_LIMIT = 200
HG_CAP = 160           # high cap to fill multiple levels
VEX_CAP = 120
HG_GAMMA = 2.5
VEX_GAMMA = 2.0

# Level configs: (offset_from_fair, base_size)
HG_LEVELS = [(2, 20), (4, 15), (6, 8)]
VEX_LEVELS = [(1, 12), (2, 8), (3, 4)]

# Takes
HG_TEDGE = 3
HG_TSZ = 18
VEX_TEDGE = 2
VEX_TSZ = 12


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


def layered_mm(sym, limit, cap, od, pos, sd, prefix, levels, tedge, tsz, gamma):
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    if ba - bb < 1:
        return []

    micro = get_microprice(od)
    # EMA imbalance
    imb_raw = get_imbalance(od)
    ik = prefix + "i"
    imb = 0.3 * imb_raw + 0.7 * sd.get(ik, 0.0)
    sd[ik] = imb

    # Reservation price
    qfair = micro - gamma * (pos / max(1, cap)) + clamp(2.0 * imb, -3, 3)

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

    # Unwind at extremes
    uw_thr = int(cap * 0.65)
    if pos >= uw_thr and sr() > 0:
        uq = min(20, sr())
        orders.append(Order(sym, bb, -uq)); s += uq
    elif pos <= -uw_thr and br() > 0:
        uq = min(20, br())
        orders.append(Order(sym, ba, uq)); b += uq

    # Layered passive quotes
    inv_frac = pos / max(1, cap)
    used_bids = set()
    used_asks = set()

    for offset, base_sz in levels:
        # Inventory-skewed sizing per level
        if pos > 0:
            bsz = max(2, int(base_sz * (1.0 - 0.4 * inv_frac)))
            ssz = max(2, int(base_sz * (1.0 + 0.3 * inv_frac)))
        elif pos < 0:
            bsz = max(2, int(base_sz * (1.0 + 0.3 * abs(inv_frac))))
            ssz = max(2, int(base_sz * (1.0 - 0.4 * abs(inv_frac))))
        else:
            bsz, ssz = base_sz, base_sz

        bid_px = int(round(qfair - offset))
        ask_px = int(round(qfair + offset))

        # Don't cross the book
        if bid_px >= ba: bid_px = ba - 1
        if ask_px <= bb: ask_px = bb + 1

        # Avoid duplicate prices
        while bid_px in used_bids and bid_px > 0:
            bid_px -= 1
        while ask_px in used_asks:
            ask_px += 1

        bq = min(bsz, br())
        sq = min(ssz, sr())

        if bq > 0 and bid_px > 0:
            orders.append(Order(sym, bid_px, bq))
            used_bids.add(bid_px)
        if sq > 0:
            orders.append(Order(sym, ask_px, -sq))
            used_asks.add(ask_px)

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
            result[HG] = layered_mm(HG, HG_LIMIT, HG_CAP, hg_od, hg_pos, sd, "h",
                                     HG_LEVELS, HG_TEDGE, HG_TSZ, HG_GAMMA)

        # VEX
        vex_od = state.order_depths.get(VEX)
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_pos = state.position.get(VEX, 0)
            result[VEX] = layered_mm(VEX, VEX_LIMIT, VEX_CAP, vex_od, vex_pos, sd, "v",
                                      VEX_LEVELS, VEX_TEDGE, VEX_TSZ, VEX_GAMMA)

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
