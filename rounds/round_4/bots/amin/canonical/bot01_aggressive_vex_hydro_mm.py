"""
Bot 01: Aggressive VEX + HYDRO Market Maker
============================================
Approach: Market-make on both liquid delta-1 products (VELVETFRUIT_EXTRACT
and HYDROGEL_PACK) simultaneously. Uses imbalance-driven fair value with
inventory skew. Takes aggressively when edge is clear, posts tight quotes
otherwise. No option trading — pure delta-1 revenue.
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

HYDRO = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
LIMITS = {HYDRO: 200, VEX: 200}


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
            orders = self._trade_product(state, symbol, stored)
            if orders:
                result[symbol] = orders

        trader_data = json.dumps(stored, separators=(",", ":"))
        return result, 0, trader_data

    def _trade_product(
        self, state: TradingState, symbol: str, stored: dict
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

        # Track last mid for momentum
        last_mids = stored.setdefault("last_mids", {})
        last_mid = last_mids.get(symbol)
        momentum = 0.0
        if last_mid is not None:
            momentum = mid - last_mid
        last_mids[symbol] = mid

        # Fair value: mid + imbalance skew + micro momentum
        inv_skew = -0.15 * position  # push fair away from inventory
        fair = mid + 1.5 * imb + 0.2 * momentum + inv_skew

        # Clip sizes — reduce when inventory is large
        base_clip = 15 if symbol == VEX else 10
        if abs(position) > limit * 0.7:
            clip = max(2, base_clip // 3)
        elif abs(position) > limit * 0.4:
            clip = max(4, base_clip // 2)
        else:
            clip = base_clip

        orders: List[Order] = []

        # Aggressive taking when edge is clear
        if buy_cap > 0 and ask <= fair - 1.0:
            take_vol = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_vol > 0:
                orders.append(Order(symbol, ask, take_vol))
                buy_cap -= take_vol

        if sell_cap > 0 and bid >= fair + 1.0:
            take_vol = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_vol > 0:
                orders.append(Order(symbol, bid, -take_vol))
                sell_cap -= take_vol

        # Passive quoting — tighter than the existing spread
        max_quote_spread = 6 if symbol == VEX else 20
        if sprd <= max_quote_spread:
            if buy_cap > 0:
                bid_px = min(bid + 1, int(math.floor(fair - 1)))
                bid_px = max(1, bid_px)
                post_qty = min(clip, buy_cap)
                if post_qty > 0:
                    orders.append(Order(symbol, bid_px, post_qty))

            if sell_cap > 0:
                ask_px = max(ask - 1, int(math.ceil(fair + 1)))
                post_qty = min(clip, sell_cap)
                if post_qty > 0:
                    orders.append(Order(symbol, ask_px, -post_qty))

        return orders
