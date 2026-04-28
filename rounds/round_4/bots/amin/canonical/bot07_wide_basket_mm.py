"""
Bot 07: Wide Basket Market Maker
==================================
Approach: Trade everything that has liquidity: HYDRO, VEX, VEV_4000,
VEV_5200, and VEV_5300. Use simple fair value (mid + imbalance +
inventory skew) per product. Broad coverage maximizes the number of
profitable opportunities across the entire product universe.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()

HYDRO = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"

PRODUCTS = [HYDRO, VEX, "VEV_4000", "VEV_5200", "VEV_5300"]
LIMITS = {
    HYDRO: 200, VEX: 200,
    "VEV_4000": 300, "VEV_5200": 300, "VEV_5300": 300,
}
STRIKES = {"VEV_4000": 4000, "VEV_5200": 5200, "VEV_5300": 5300}
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


def intrinsic_value(spot: float, strike: int) -> float:
    return max(0.0, spot - strike)


def bs_call(spot: float, strike: int, tte: float, vol: float) -> float:
    if spot <= 0 or strike <= 0 or tte <= 0 or vol <= 0:
        return intrinsic_value(spot, strike)
    sqrt_t = math.sqrt(tte)
    sig = vol * sqrt_t
    if sig <= 0:
        return intrinsic_value(spot, strike)
    d1 = (math.log(spot / strike) + 0.5 * vol ** 2 * tte) / sig
    d2 = d1 - sig
    return spot * NORMAL.cdf(d1) - strike * NORMAL.cdf(d2)


def implied_vol(price: float, spot: float, strike: int, tte: float) -> Optional[float]:
    iv = intrinsic_value(spot, strike)
    target = max(price, iv)
    if target <= iv + 1e-6:
        return 0.1
    if spot <= 0 or strike <= 0 or tte <= 0:
        return None
    lo, hi = 1e-4, 4.0
    for _ in range(28):
        mid = 0.5 * (lo + hi)
        p = bs_call(spot, strike, tte, mid)
        if p >= target:
            hi = mid
        else:
            lo = mid
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

        for symbol in PRODUCTS:
            if symbol in STRIKES:
                orders = self._trade_option(
                    state, stored, symbol, vex_mid
                )
            else:
                orders = self._trade_delta1(state, stored, symbol)
            if orders:
                result[symbol] = orders

        # Cache mids
        mids = stored.setdefault("mids", {})
        for sym in PRODUCTS:
            m = mid_price(state.order_depths.get(sym))
            if m is not None:
                mids[sym] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_delta1(
        self, state: TradingState, stored: dict, symbol: str
    ) -> List[Order]:
        depth = state.order_depths.get(symbol)
        if depth is None:
            return []
        mid = mid_price(depth)
        sprd = get_spread(depth)
        if mid is None or sprd is None:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        imb = imbalance(depth)
        position = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)

        last_mid = stored.get("mids", {}).get(symbol)
        mom = 0.0 if last_mid is None else 0.12 * (mid - last_mid)
        inv_skew = -0.12 * position
        fair = mid + 1.2 * imb + mom + inv_skew

        # Smaller clips per product since we trade many
        clip = 10 if symbol == VEX else 8
        if abs(position) > limit * 0.7:
            clip = max(2, clip // 3)
        elif abs(position) > limit * 0.4:
            clip = max(3, clip // 2)

        max_sprd = 6 if symbol == VEX else 22

        orders: List[Order] = []
        edge = 1.5 if symbol == VEX else max(2.0, sprd * 0.15)

        if sprd <= max_sprd:
            if buy_cap > 0 and ask <= fair - edge:
                qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
                if qty > 0:
                    orders.append(Order(symbol, ask, qty))
                    buy_cap -= qty
            if sell_cap > 0 and bid >= fair + edge:
                qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
                if qty > 0:
                    orders.append(Order(symbol, bid, -qty))
                    sell_cap -= qty

            offset = 1 if symbol == VEX else max(2, int(sprd * 0.3))
            if buy_cap > 0:
                px = min(bid + 1, int(math.floor(fair - offset)))
                px = max(1, px)
                orders.append(Order(symbol, px, min(clip, buy_cap)))
            if sell_cap > 0:
                px = max(ask - 1, int(math.ceil(fair + offset)))
                orders.append(Order(symbol, px, -min(clip, sell_cap)))

        return orders

    def _trade_option(
        self, state: TradingState, stored: dict,
        symbol: str, vex_mid: Optional[float]
    ) -> List[Order]:
        depth = state.order_depths.get(symbol)
        if depth is None or vex_mid is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 14:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        strike = STRIKES[symbol]
        tte = tte_years(state.timestamp)
        iv_val = intrinsic_value(vex_mid, strike)
        clean_mid = max(opt_mid, iv_val)

        # Smooth IV
        iv_hist = stored.setdefault("iv_hist", {})
        hist = list(iv_hist.get(symbol, []))
        curr_iv = implied_vol(clean_mid, vex_mid, strike, tte)
        if curr_iv is not None and curr_iv > 0:
            hist.append(curr_iv)
        if len(hist) > 16:
            hist = hist[-16:]
        iv_hist[symbol] = hist
        iv_mean = sum(hist) / len(hist) if hist else None
        if iv_mean is None:
            return []

        fair = bs_call(vex_mid, strike, tte, iv_mean)
        fair = max(fair, iv_val)

        position = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)

        clip = 10
        if abs(position) > 180:
            clip = 3
        elif abs(position) > 100:
            clip = 6
        edge = 0.5 if symbol == "VEV_4000" else 1.0

        orders: List[Order] = []
        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                orders.append(Order(symbol, ask, qty))
                buy_cap -= qty
        if sell_cap > 0 and bid >= fair + edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                orders.append(Order(symbol, bid, -qty))
                sell_cap -= qty

        if sprd <= 10:
            if buy_cap > 0:
                px = min(bid + 1, int(math.floor(fair)))
                px = max(1, px)
                orders.append(Order(symbol, px, min(max(1, clip // 2), buy_cap)))
            if sell_cap > 0:
                px = max(ask - 1, int(math.ceil(fair)))
                orders.append(Order(symbol, px, -min(max(1, clip // 2), sell_cap)))

        return orders
