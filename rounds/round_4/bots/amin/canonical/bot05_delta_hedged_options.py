"""
Bot 05: Delta-Hedged Option Portfolio
=======================================
Approach: Identify mispriced options via Black-Scholes, accumulate option
positions, and hedge delta exposure through VEX. Focus on VEV_4000 (most
liquid option) and VEV_5300. The goal is to capture option mispricing while
staying roughly delta-neutral via VEX offsetting.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()

VEX = "VELVETFRUIT_EXTRACT"
STRIKES = {"VEV_4000": 4000, "VEV_5300": 5300}
LIMITS = {VEX: 200, "VEV_4000": 300, "VEV_5300": 300}
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
    sig_sqrt = vol * sqrt_t
    if sig_sqrt <= 0:
        return intrinsic_value(spot, strike)
    d1 = (math.log(spot / strike) + 0.5 * vol ** 2 * tte) / sig_sqrt
    d2 = d1 - sig_sqrt
    return spot * NORMAL.cdf(d1) - strike * NORMAL.cdf(d2)


def bs_delta(spot: float, strike: int, tte: float, vol: float) -> float:
    if spot <= 0 or strike <= 0 or tte <= 0 or vol <= 0:
        return 1.0 if spot > strike else 0.0
    sqrt_t = math.sqrt(tte)
    sig_sqrt = vol * sqrt_t
    if sig_sqrt <= 0:
        return 1.0 if spot > strike else 0.0
    d1 = (math.log(spot / strike) + 0.5 * vol ** 2 * tte) / sig_sqrt
    return NORMAL.cdf(d1)


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

        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)
        if vex_mid is None:
            return result, 0, json.dumps(stored, separators=(",", ":"))

        tte = tte_years(state.timestamp)

        # Trade options to capture mispricing
        total_delta_exposure = 0.0
        for symbol, strike in STRIKES.items():
            opt_orders, delta_added = self._trade_option(
                state, stored, symbol, strike, vex_mid, tte
            )
            if opt_orders:
                result[symbol] = opt_orders
            # Track total delta from option positions
            opt_pos = state.position.get(symbol, 0)
            opt_delta = bs_delta(vex_mid, strike, tte, self._get_smooth_iv(stored, symbol))
            total_delta_exposure += opt_pos * opt_delta

        # Hedge delta through VEX
        vex_orders = self._hedge_vex(state, stored, vex_mid, total_delta_exposure)
        if vex_orders:
            result[VEX] = vex_orders

        # Update mid cache
        mids = stored.setdefault("mids", {})
        for sym in [VEX] + list(STRIKES.keys()):
            m = mid_price(state.order_depths.get(sym))
            if m is not None:
                mids[sym] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _get_smooth_iv(self, stored: dict, symbol: str) -> float:
        hist = stored.get("iv_hist", {}).get(symbol, [])
        if not hist:
            return 0.5
        return sum(hist) / len(hist)

    def _trade_option(
        self, state: TradingState, stored: dict,
        symbol: str, strike: int, vex_mid: float, tte: float
    ) -> Tuple[List[Order], float]:
        depth = state.order_depths.get(symbol)
        if depth is None:
            return [], 0.0
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 14:
            return [], 0.0
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return [], 0.0

        iv_val = intrinsic_value(vex_mid, strike)
        clean_mid = max(opt_mid, iv_val)

        # Smooth IV
        iv_hist = stored.setdefault("iv_hist", {})
        hist = list(iv_hist.get(symbol, []))
        current_iv = implied_vol(clean_mid, vex_mid, strike, tte)
        if current_iv is not None and current_iv > 0:
            hist.append(current_iv)
        if len(hist) > 20:
            hist = hist[-20:]
        iv_hist[symbol] = hist
        iv_mean = sum(hist) / len(hist) if hist else 0.5

        fair = bs_call(vex_mid, strike, tte, iv_mean)
        fair = max(fair, iv_val)

        position = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)

        # Larger clips for option trading
        clip = 18 if symbol == "VEV_4000" else 14
        if abs(position) > 200:
            clip = max(4, clip // 3)
        elif abs(position) > 120:
            clip = max(6, clip // 2)

        edge = 0.5 if symbol == "VEV_4000" else 1.0

        orders: List[Order] = []
        delta_added = 0.0

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

        return orders, delta_added

    def _hedge_vex(
        self, state: TradingState, stored: dict,
        vex_mid: float, option_delta: float
    ) -> List[Order]:
        """Use VEX to offset delta from options. Also do light MM."""
        depth = state.order_depths.get(VEX)
        if depth is None:
            return []
        sprd = get_spread(depth)
        if sprd is None or sprd > 6:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        position = state.position.get(VEX, 0)
        buy_cap = max(0, LIMITS[VEX] - position)
        sell_cap = max(0, LIMITS[VEX] + position)

        # Target VEX position = negative of option delta exposure
        # (if we're long calls, we want short VEX to hedge)
        target_vex = -int(round(option_delta * 0.5))  # partial hedge
        target_vex = max(-LIMITS[VEX], min(LIMITS[VEX], target_vex))

        delta_to_trade = target_vex - position

        orders: List[Order] = []

        # Hedge component
        if delta_to_trade > 5 and buy_cap > 0:
            qty = min(delta_to_trade, buy_cap, 15)
            orders.append(Order(VEX, ask, qty))
        elif delta_to_trade < -5 and sell_cap > 0:
            qty = min(-delta_to_trade, sell_cap, 15)
            orders.append(Order(VEX, bid, -qty))

        # Light MM on VEX for additional revenue
        last_mid = stored.get("mids", {}).get(VEX)
        mom = 0.0 if last_mid is None else 0.1 * (vex_mid - last_mid)
        fair = vex_mid + mom - 0.08 * position

        clip = 8
        if sprd <= 4:
            if buy_cap > 3:
                px = min(bid + 1, int(math.floor(fair - 1)))
                px = max(1, px)
                orders.append(Order(VEX, px, min(clip, buy_cap)))
            if sell_cap > 3:
                px = max(ask - 1, int(math.ceil(fair + 1)))
                orders.append(Order(VEX, px, -min(clip, sell_cap)))

        return orders
