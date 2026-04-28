"""
Bot 08: ITM Option Specialist (VEV_4000 Focused)
==================================================
Approach: VEV_4000 is the most liquid option (164 trades/day) and deeply
ITM (VEX ~5240, strike 4000 => intrinsic ~1240). Its price tracks VEX
closely but with its own spread to capture. Focus aggressively on VEV_4000
market-making with BS-informed fair value, plus light VEX MM as income base.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()

VEX = "VELVETFRUIT_EXTRACT"
OPT = "VEV_4000"
STRIKE = 4000
LIMITS = {VEX: 200, OPT: 300}
ROUND4_DAYS_LEFT = 4.0
TIME_SCALE = 1_000_000


def best_bid_ask(depth) -> Tuple[Optional[int], Optional[int]]:
    if depth is None:
        return None, None
    bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
    ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
    return bid, ask


def mid_price(depth) -> Optional[float]:
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return None
    return (bid + ask) / 2.0


def get_spread(depth) -> Optional[int]:
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return None
    return ask - bid


def imbalance(depth) -> float:
    if depth is None:
        return 0.0
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return 0.0
    bv = depth.buy_orders.get(bid, 0)
    av = -depth.sell_orders.get(ask, 0)
    t = bv + av
    if t <= 0:
        return 0.0
    return (bv - av) / t


def tte_years(timestamp: int) -> float:
    progress = float(timestamp % TIME_SCALE) / float(TIME_SCALE)
    days_left = max(0.5, ROUND4_DAYS_LEFT - progress)
    return days_left / 365.0


def intrinsic_value(spot: float) -> float:
    return max(0.0, spot - STRIKE)


def bs_call(spot: float, tte: float, vol: float) -> float:
    if spot <= 0 or tte <= 0 or vol <= 0:
        return intrinsic_value(spot)
    sqrt_t = math.sqrt(tte)
    sig = vol * sqrt_t
    if sig <= 0:
        return intrinsic_value(spot)
    d1 = (math.log(spot / STRIKE) + 0.5 * vol ** 2 * tte) / sig
    d2 = d1 - sig
    return spot * NORMAL.cdf(d1) - STRIKE * NORMAL.cdf(d2)


def implied_vol(price: float, spot: float, tte: float) -> Optional[float]:
    iv = intrinsic_value(spot)
    target = max(price, iv)
    if target <= iv + 1e-6:
        return 0.1
    if spot <= 0 or tte <= 0:
        return None
    lo, hi = 1e-4, 4.0
    for _ in range(30):
        mid_val = 0.5 * (lo + hi)
        p = bs_call(spot, tte, mid_val)
        if p >= target:
            hi = mid_val
        else:
            lo = mid_val
    return hi


class Trader:
    def run(self, state: TradingState):
        stored = {}
        if state.traderData:
            try:
                stored = json.loads(state.traderData)
            except Exception:
                stored = {}

        result: Dict[str, List[Order]] = {}

        vex_mid = mid_price(state.order_depths.get(VEX))

        # Primary: VEV_4000
        if vex_mid is not None:
            opt_orders = self._trade_4000(state, stored, vex_mid)
            if opt_orders:
                result[OPT] = opt_orders

        # Secondary: VEX MM
        vex_orders = self._trade_vex(state, stored)
        if vex_orders:
            result[VEX] = vex_orders

        mids = stored.setdefault("mids", {})
        for sym in [VEX, OPT]:
            m = mid_price(state.order_depths.get(sym))
            if m is not None:
                mids[sym] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_4000(
        self, state: TradingState, stored: dict, vex_mid: float
    ) -> List[Order]:
        depth = state.order_depths.get(OPT)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 25:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        tte = tte_years(state.timestamp)
        iv = intrinsic_value(vex_mid)
        clean_mid = max(opt_mid, iv)
        imb = imbalance(depth)

        # IV tracking
        iv_hist = stored.setdefault("iv4000", [])
        curr_iv = implied_vol(clean_mid, vex_mid, tte)
        if curr_iv is not None and curr_iv > 0:
            iv_hist.append(curr_iv)
        if len(iv_hist) > 24:
            stored["iv4000"] = iv_hist[-24:]
            iv_hist = stored["iv4000"]

        iv_mean = sum(iv_hist) / len(iv_hist) if iv_hist else 0.3

        # Fair = blend of BS and heuristic (intrinsic + time premium)
        bs_fair = bs_call(vex_mid, tte, iv_mean)
        bs_fair = max(bs_fair, iv)

        # VEX move tracking for faster fair update
        last_vex = stored.get("mids", {}).get(VEX)
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex

        heuristic_fair = iv + 3.0 + 0.6 * vex_move + 0.5 * imb
        heuristic_fair = max(heuristic_fair, iv)

        fair = 0.55 * bs_fair + 0.45 * heuristic_fair
        fair = max(fair, iv)

        position = state.position.get(OPT, 0)
        limit = LIMITS[OPT]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)

        # Aggressive clips for liquid option
        clip = 20
        if abs(position) > 240:
            clip = 5
        elif abs(position) > 180:
            clip = 8
        elif abs(position) > 100:
            clip = 12

        # Inventory skew on fair
        fair -= 0.005 * position

        orders: List[Order] = []

        # Aggressive taking
        edge = 0.5
        if buy_cap > 0 and ask <= fair - edge:
            for px in sorted(depth.sell_orders.keys()):
                if px > fair - edge:
                    break
                vol = min(clip, buy_cap, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    orders.append(Order(OPT, px, vol))
                    buy_cap -= vol
                if buy_cap <= 0:
                    break

        if sell_cap > 0 and bid >= fair + edge:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair + edge:
                    break
                vol = min(clip, sell_cap, max(0, depth.buy_orders[px]))
                if vol > 0:
                    orders.append(Order(OPT, px, -vol))
                    sell_cap -= vol
                if sell_cap <= 0:
                    break

        # Tight quoting — VEV_4000 has natural spread ~20
        if sprd <= 24 and buy_cap > 0:
            px = min(bid + 1, int(math.floor(fair)))
            px = max(1, px)
            orders.append(Order(OPT, px, min(clip, buy_cap)))
        if sprd <= 24 and sell_cap > 0:
            px = max(ask - 1, int(math.ceil(fair)))
            orders.append(Order(OPT, px, -min(clip, sell_cap)))

        return orders

    def _trade_vex(self, state: TradingState, stored: dict) -> List[Order]:
        depth = state.order_depths.get(VEX)
        if depth is None:
            return []
        mid = mid_price(depth)
        sprd = get_spread(depth)
        if mid is None or sprd is None or sprd > 6:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        position = state.position.get(VEX, 0)
        buy_cap = max(0, LIMITS[VEX] - position)
        sell_cap = max(0, LIMITS[VEX] + position)
        fair = mid - 0.12 * position

        clip = 10
        if abs(position) > 140:
            clip = 3

        orders: List[Order] = []
        if buy_cap > 0 and ask <= fair - 2.0:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                orders.append(Order(VEX, ask, qty))
                buy_cap -= qty
        if sell_cap > 0 and bid >= fair + 2.0:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                orders.append(Order(VEX, bid, -qty))
                sell_cap -= qty

        if sprd <= 4:
            if buy_cap > 0:
                px = min(bid + 1, int(math.floor(fair - 1)))
                px = max(1, px)
                orders.append(Order(VEX, px, min(clip, buy_cap)))
            if sell_cap > 0:
                px = max(ask - 1, int(math.ceil(fair + 1)))
                orders.append(Order(VEX, px, -min(clip, sell_cap)))

        return orders
