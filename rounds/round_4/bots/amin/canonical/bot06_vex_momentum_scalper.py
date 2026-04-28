"""
Bot 06: VEX Momentum Scalper
==============================
Approach: Track VEX micro-momentum using a fast/slow EMA crossover.
When momentum is positive and book supports it, go long aggressively.
When momentum is negative, go short. Quick inventory turnover with
strict position limits and stop-loss via drawdown. No option trading.
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

VEX = "VELVETFRUIT_EXTRACT"
HYDRO = "HYDROGEL_PACK"
LIMITS = {VEX: 200, HYDRO: 200}


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


class Trader:
    def run(self, state: TradingState):
        stored = {}
        if state.traderData:
            try:
                stored = json.loads(state.traderData)
            except Exception:
                stored = {}

        result: Dict[str, List[Order]] = {}

        # Momentum-based VEX scalping
        vex_orders = self._trade_momentum_vex(state, stored)
        if vex_orders:
            result[VEX] = vex_orders

        # Also do simple HYDRO MM for base income
        hydro_orders = self._trade_hydro_simple(state, stored)
        if hydro_orders:
            result[HYDRO] = hydro_orders

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_momentum_vex(self, state: TradingState, stored: dict) -> List[Order]:
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

        # Update EMAs
        fast_alpha = 0.25
        slow_alpha = 0.06
        fast_ema = stored.get("vex_fast_ema")
        slow_ema = stored.get("vex_slow_ema")
        if fast_ema is None:
            fast_ema = mid
            slow_ema = mid
        else:
            fast_ema = fast_alpha * mid + (1 - fast_alpha) * fast_ema
            slow_ema = slow_alpha * mid + (1 - slow_alpha) * slow_ema
        stored["vex_fast_ema"] = fast_ema
        stored["vex_slow_ema"] = slow_ema

        momentum = fast_ema - slow_ema  # positive = uptrend
        imb = imbalance(depth)

        position = state.position.get(VEX, 0)
        buy_cap = max(0, LIMITS[VEX] - position)
        sell_cap = max(0, LIMITS[VEX] + position)

        # Momentum-aligned fair value
        inv_skew = -0.15 * position
        fair = mid + 2.0 * momentum + 1.0 * imb + inv_skew

        # Strong momentum signals
        strong_up = momentum > 0.8 and imb > 0.1
        strong_down = momentum < -0.8 and imb < -0.1

        clip = 15
        if abs(position) >= 140:
            clip = 4
        elif abs(position) >= 100:
            clip = 8

        orders: List[Order] = []

        # Aggressive taking when momentum + imbalance align
        if strong_up and buy_cap > 0:
            # Take all available asks near fair
            for px in sorted(depth.sell_orders.keys()):
                if px > fair:
                    break
                vol = min(clip, buy_cap, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    orders.append(Order(VEX, px, vol))
                    buy_cap -= vol
                if buy_cap <= 0:
                    break

        if strong_down and sell_cap > 0:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair:
                    break
                vol = min(clip, sell_cap, max(0, depth.buy_orders[px]))
                if vol > 0:
                    orders.append(Order(VEX, px, -vol))
                    sell_cap -= vol
                if sell_cap <= 0:
                    break

        # Normal taking with moderate edge
        if buy_cap > 0 and ask <= fair - 1.5:
            vol = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if vol > 0:
                orders.append(Order(VEX, ask, vol))
                buy_cap -= vol
        if sell_cap > 0 and bid >= fair + 1.5:
            vol = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if vol > 0:
                orders.append(Order(VEX, bid, -vol))
                sell_cap -= vol

        # Passive quotes biased by momentum
        if sprd <= 4:
            if buy_cap > 0:
                bias = 1 if momentum > 0.3 else 0
                px = min(bid + 1 + bias, int(math.floor(fair)))
                px = max(1, px)
                orders.append(Order(VEX, px, min(clip, buy_cap)))
            if sell_cap > 0:
                bias = 1 if momentum < -0.3 else 0
                px = max(ask - 1 - bias, int(math.ceil(fair)))
                orders.append(Order(VEX, px, -min(clip, sell_cap)))

        return orders

    def _trade_hydro_simple(self, state: TradingState, stored: dict) -> List[Order]:
        depth = state.order_depths.get(HYDRO)
        if depth is None:
            return []
        mid = mid_price(depth)
        sprd = get_spread(depth)
        if mid is None or sprd is None:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        position = state.position.get(HYDRO, 0)
        buy_cap = max(0, LIMITS[HYDRO] - position)
        sell_cap = max(0, LIMITS[HYDRO] + position)
        fair = mid - 0.15 * position

        clip = 8
        if abs(position) > 120:
            clip = 3

        orders: List[Order] = []
        offset = max(3, int(sprd * 0.3))
        if buy_cap > 0:
            px = min(bid + 1, int(math.floor(fair - offset)))
            px = max(1, px)
            orders.append(Order(HYDRO, px, min(clip, buy_cap)))
        if sell_cap > 0:
            px = max(ask - 1, int(math.ceil(fair + offset)))
            orders.append(Order(HYDRO, px, -min(clip, sell_cap)))

        return orders
