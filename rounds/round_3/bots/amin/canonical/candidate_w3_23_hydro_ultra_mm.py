"""
W3-23: HYDRO-Only Ultra-Optimized Market Maker
================================================
Pure HYDROGEL MM with optimal Avellaneda-Stoikov parameters.
HYDRO has the best MM opportunity in this market:
  - Spread = 15.7 (wide), ac1 = -0.13 (mean-reverting)
  - Half-spread / |return| ratio = 4.7 (excellent)
  - 79% of ticks move ≥1, 46% ≥2, 22% ≥3

Key optimizations vs previous bots:
  1. Layered quotes: 2 price levels for more fill probability
  2. Adaptive half-spread: wider when inventory high, tighter when flat
  3. Volatility-adjusted reservation price
  4. More aggressive inventory mean-reversion
  5. No other products — all capacity on the highest-edge product

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
LIMIT = 200
POS_CAP = 160          # use most of the limit
GAMMA = 2.5            # inventory aversion
IMB_ALPHA = 0.25
IMB_GAIN = 2.5
VOL_ALPHA = 0.05       # vol EMA smoothing


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

        od = state.order_depths.get(HG)
        if od is None or not od.buy_orders or not od.sell_orders:
            return result, conversions, json.dumps(sd, separators=(",", ":"))

        bb = max(od.buy_orders)
        ba = min(od.sell_orders)
        spread = ba - bb
        if spread < 1:
            return result, conversions, json.dumps(sd, separators=(",", ":"))

        pos = state.position.get(HG, 0)
        micro = get_microprice(od)
        mid = (bb + ba) / 2.0

        # EMA imbalance
        imb_raw = get_imbalance(od)
        imb = IMB_ALPHA * imb_raw + (1 - IMB_ALPHA) * sd.get("i", 0.0)
        sd["i"] = imb

        # Realized vol estimate (EMA of |move|)
        prev_mid = sd.get("pm", mid)
        move = abs(mid - prev_mid)
        vol = VOL_ALPHA * move + (1 - VOL_ALPHA) * sd.get("v", 3.0)
        sd["v"] = vol
        sd["pm"] = mid

        # Avellaneda-Stoikov reservation price
        # r = s - gamma * q * sigma^2
        r = micro - GAMMA * (pos / POS_CAP) * max(1.0, vol)

        # Imbalance lean
        imb_shift = clamp(IMB_GAIN * imb, -3.0, 3.0)
        qfair = r + imb_shift

        orders = []
        bought = 0
        sold = 0

        def buy_room():
            return max(0, min(POS_CAP, LIMIT) - pos - bought)

        def sell_room():
            return max(0, min(POS_CAP, LIMIT) + pos - sold)

        # ── Aggressive takes ──
        # When price deviates significantly from fair, take liquidity
        take_edge = max(2, int(vol * 0.8))  # adaptive take edge

        for ask_p in sorted(od.sell_orders):
            if buy_room() <= 0 or ask_p > qfair - take_edge:
                break
            avail = -od.sell_orders[ask_p]
            qty = min(avail, 20, buy_room())
            if qty > 0:
                orders.append(Order(HG, ask_p, qty))
                bought += qty

        for bid_p in sorted(od.buy_orders, reverse=True):
            if sell_room() <= 0 or bid_p < qfair + take_edge:
                break
            avail = od.buy_orders[bid_p]
            qty = min(avail, 20, sell_room())
            if qty > 0:
                orders.append(Order(HG, bid_p, -qty))
                sold += qty

        # ── Aggressive unwind at inventory extremes ──
        if pos > POS_CAP * 0.65 and sell_room() > 0:
            uq = min(25, sell_room())
            orders.append(Order(HG, bb, -uq))
            sold += uq
        elif pos < -POS_CAP * 0.65 and buy_room() > 0:
            uq = min(25, buy_room())
            orders.append(Order(HG, ba, uq))
            bought += uq

        # ── Layered passive quotes ──
        # Level 1: tight (capture small moves)
        # Level 2: wider (capture larger moves)
        inv_frac = abs(pos) / POS_CAP

        # Adapt half-spread to inventory: wider when loaded, tighter when flat
        half1 = 3 if inv_frac < 0.3 else 4 if inv_frac < 0.6 else 5
        half2 = half1 + 2

        # Level 1 quotes
        bid1 = int(round(qfair - half1))
        ask1 = int(round(qfair + half1))
        if bid1 >= ba: bid1 = ba - 1
        if ask1 <= bb: ask1 = bb + 1

        # Inventory-skewed sizing
        base_sz = 22
        if pos > 0:
            b1 = max(3, base_sz - int(pos * 0.25))
            s1 = max(3, base_sz + int(pos * 0.15))
        elif pos < 0:
            b1 = max(3, base_sz + int(-pos * 0.15))
            s1 = max(3, base_sz - int(-pos * 0.25))
        else:
            b1, s1 = base_sz, base_sz

        bq1 = min(b1, buy_room())
        sq1 = min(s1, sell_room())
        if bq1 > 0 and bid1 > 0:
            orders.append(Order(HG, bid1, bq1))
        if sq1 > 0 and ask1 > 0:
            orders.append(Order(HG, ask1, -sq1))

        # Level 2 quotes (smaller, wider)
        bid2 = int(round(qfair - half2))
        ask2 = int(round(qfair + half2))
        if bid2 >= ba: bid2 = ba - 1
        if ask2 <= bb: ask2 = bb + 1
        if bid2 >= bid1: bid2 = bid1 - 1
        if ask2 <= ask1: ask2 = ask1 + 1

        l2_sz = max(2, base_sz // 3)
        bq2 = min(l2_sz, buy_room())
        sq2 = min(l2_sz, sell_room())
        if bq2 > 0 and bid2 > 0 and bid2 != bid1:
            orders.append(Order(HG, bid2, bq2))
        if sq2 > 0 and ask2 > 0 and ask2 != ask1:
            orders.append(Order(HG, ask2, -sq2))

        result[HG] = orders
        return result, conversions, json.dumps(sd, separators=(",", ":"))
