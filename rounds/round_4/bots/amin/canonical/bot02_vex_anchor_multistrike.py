"""
Bot 02: VEX Anchor + Multi-Strike Options
==========================================
Approach: Use VEX market-making as the core revenue engine, then overlay
option positions on VEV_4000 (ITM, liquid) and VEV_5300 (OTM, moderate
liquidity) using Black-Scholes fair value. Take mispriced options, quote to
capture spread. VEX serves both as profit center and as the anchor for
option fair value.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()

HYDRO = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
OPTION_SYMBOLS = ["VEV_4000", "VEV_5300"]
STRIKES = {"VEV_4000": 4000, "VEV_5300": 5300}
LIMITS = {HYDRO: 200, VEX: 200, "VEV_4000": 300, "VEV_5300": 300}
ROUND4_OPTION_DAYS_LEFT = 4.0
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
    bid_vol = depth.buy_orders.get(bid, 0)
    ask_vol = -depth.sell_orders.get(ask, 0)
    total = bid_vol + ask_vol
    if total <= 0:
        return 0.0
    return (bid_vol - ask_vol) / total


def session_progress(timestamp: int) -> float:
    return float(timestamp % TIME_SCALE) / float(TIME_SCALE)


def tte_years(timestamp: int) -> float:
    progress = session_progress(timestamp)
    days_left = max(0.5, ROUND4_OPTION_DAYS_LEFT - progress)
    return days_left / 365.0


def intrinsic_value(spot: float, strike: int) -> float:
    return max(0.0, spot - strike)


def bs_call(spot: float, strike: int, tte: float, vol: float) -> float:
    if spot <= 0 or strike <= 0 or tte <= 0 or vol <= 0:
        return intrinsic_value(spot, strike)
    sqrt_t = math.sqrt(tte)
    sig_sqrt = vol * sqrt_t
    if sig_sqrt <= 0:
        return intrinsic_value(spot, strike)
    d1 = (math.log(spot / strike) + 0.5 * vol * vol * tte) / sig_sqrt
    d2 = d1 - sig_sqrt
    return spot * NORMAL.cdf(d1) - strike * NORMAL.cdf(d2)


def implied_vol(price: float, spot: float, strike: int, tte: float) -> Optional[float]:
    iv = intrinsic_value(spot, strike)
    target = max(price, iv)
    if target <= iv + 1e-6:
        return 0.1
    if spot <= 0 or strike <= 0 or tte <= 0:
        return None
    lo, hi = 1e-4, 4.0
    for _ in range(30):
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

        # VEX market making (core)
        vex_orders = self._trade_vex(state, stored)
        if vex_orders:
            result[VEX] = vex_orders

        # Option overlay
        vex_mid = mid_price(state.order_depths.get(VEX))
        if vex_mid is not None:
            for symbol in OPTION_SYMBOLS:
                opt_orders = self._trade_option(state, stored, symbol, vex_mid)
                if opt_orders:
                    result[symbol] = opt_orders

        # Update mid cache
        mids = stored.setdefault("mids", {})
        for sym in [VEX] + OPTION_SYMBOLS:
            m = mid_price(state.order_depths.get(sym))
            if m is not None:
                mids[sym] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

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

        imb = imbalance(depth)
        position = state.position.get(VEX, 0)
        buy_cap = max(0, LIMITS[VEX] - position)
        sell_cap = max(0, LIMITS[VEX] + position)

        last_mid = stored.get("mids", {}).get(VEX)
        mom = 0.0 if last_mid is None else 0.15 * (mid - last_mid)
        inv_skew = -0.1 * position
        fair = mid + 1.2 * imb + mom + inv_skew

        clip = 12
        if abs(position) >= 120:
            clip = 4
        elif abs(position) >= 80:
            clip = 8

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

    def _trade_option(
        self, state: TradingState, stored: dict, symbol: str, vex_mid: float
    ) -> List[Order]:
        depth = state.order_depths.get(symbol)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 12:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        strike = STRIKES[symbol]
        tte = tte_years(state.timestamp)
        iv_val = intrinsic_value(vex_mid, strike)
        clean_mid = max(opt_mid, iv_val)

        # Get IV and smooth it
        iv_hist = stored.setdefault("iv_hist", {})
        hist = list(iv_hist.get(symbol, []))
        current_iv = implied_vol(clean_mid, vex_mid, strike, tte)
        if current_iv is not None and current_iv > 0:
            hist.append(current_iv)
        if len(hist) > 20:
            hist = hist[-20:]
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

        edge = 1.0 if symbol == "VEV_5300" else 0.5
        clip = 12 if symbol == "VEV_5300" else 15

        if abs(position) > 200:
            clip = max(3, clip // 3)
        elif abs(position) > 100:
            clip = max(5, clip // 2)

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
