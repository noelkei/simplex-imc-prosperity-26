"""
Bot 09: VEX Mean Reversion with Inventory Penalty
===================================================
Approach: VEX trades within a fairly narrow range (~5200-5280). Compute a
rolling window mean and fade moves away from it. Stronger inventory penalty
pushes the bot to mean-revert its own position too. Add HYDRO for base
income with the same mean-reversion logic.
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

        for symbol in [VEX, HYDRO]:
            orders = self._trade_mean_revert(state, stored, symbol)
            if orders:
                result[symbol] = orders

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_mean_revert(
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

        # Rolling window of recent mids
        key = f"{symbol}_window"
        window = list(stored.get(key, []))
        window.append(mid)
        window_size = 50  # ~5 seconds of history at 100ms ticks
        if len(window) > window_size:
            window = window[-window_size:]
        stored[key] = window

        # Compute rolling mean
        rolling_mean = sum(window) / len(window)

        # Deviation from mean
        deviation = mid - rolling_mean

        imb = imbalance(depth)
        position = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)

        # Fair value: rolling mean, adjusted by imbalance and inventory
        inv_penalty = -0.20 * position  # strong inventory penalty
        fair = rolling_mean + 0.8 * imb + inv_penalty

        # More aggressive when price deviates far from mean
        urgency = min(1.0, abs(deviation) / 4.0)  # 0 to 1

        clip = 12 if symbol == VEX else 9
        if abs(position) > limit * 0.7:
            clip = max(2, clip // 3)
        elif abs(position) > limit * 0.4:
            clip = max(4, clip // 2)

        # Increase clip when mean-reversion signal is strong
        if urgency > 0.6:
            clip = min(clip + 4, 18)

        orders: List[Order] = []
        max_sprd = 6 if symbol == VEX else 22

        if sprd > max_sprd:
            return []

        # Edge to take: tighter when signal is strong
        edge = max(0.5, 2.0 * (1 - urgency))

        # Aggressive taking: buy when below mean, sell when above
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

        # Passive quoting around fair
        offset = 1 if symbol == VEX else max(2, int(sprd * 0.25))
        if buy_cap > 0:
            px = min(bid + 1, int(math.floor(fair - offset)))
            px = max(1, px)
            orders.append(Order(symbol, px, min(clip, buy_cap)))
        if sell_cap > 0:
            px = max(ask - 1, int(math.ceil(fair + offset)))
            orders.append(Order(symbol, px, -min(clip, sell_cap)))

        return orders
