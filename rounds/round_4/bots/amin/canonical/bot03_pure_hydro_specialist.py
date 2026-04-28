"""
Bot 03: Pure HYDRO Specialist
==============================
Approach: Focus exclusively on HYDROGEL_PACK — the liquid, independent
delta-1 product with no correlation to the voucher family. Use aggressive
spread capture with adaptive inventory management. HYDRO has wider spreads
(~16) offering more edge per trade. Trade nothing else.
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

HYDRO = "HYDROGEL_PACK"
LIMIT = 200


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


class Trader:
    def run(self, state: TradingState):
        stored = {}
        if state.traderData:
            try:
                stored = json.loads(state.traderData)
            except Exception:
                stored = {}

        result: Dict[str, List[Order]] = {}
        orders = self._trade_hydro(state, stored)
        if orders:
            result[HYDRO] = orders

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_hydro(self, state: TradingState, stored: dict) -> List[Order]:
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
        buy_cap = max(0, LIMIT - position)
        sell_cap = max(0, LIMIT + position)

        # Compute total book depth
        total_bid_vol = sum(depth.buy_orders.values())
        total_ask_vol = -sum(depth.sell_orders.values())
        total = total_bid_vol + total_ask_vol
        book_imb = (total_bid_vol - total_ask_vol) / total if total > 0 else 0.0

        # EMA of mid for trend detection
        ema = stored.get("hydro_ema")
        alpha = 0.12
        if ema is None:
            ema = mid
        else:
            ema = alpha * mid + (1 - alpha) * ema
        stored["hydro_ema"] = ema

        trend = mid - ema  # positive = price rising

        # Fair value: EMA + imbalance pressure + inventory skew
        inv_skew = -0.25 * position  # stronger skew for wider product
        fair = ema + 2.0 * book_imb + 0.3 * trend + inv_skew

        # Adaptive clip size
        clip = 12
        if abs(position) > 160:
            clip = 3
        elif abs(position) > 120:
            clip = 5
        elif abs(position) > 80:
            clip = 8

        orders: List[Order] = []

        # Take liquidity when clear edge
        edge_take = max(2.0, sprd * 0.15)
        if buy_cap > 0 and ask <= fair - edge_take:
            # Walk the ask side
            for px in sorted(depth.sell_orders.keys()):
                if px > fair - edge_take:
                    break
                vol = min(clip, buy_cap, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    orders.append(Order(HYDRO, px, vol))
                    buy_cap -= vol
                    if buy_cap <= 0:
                        break

        if sell_cap > 0 and bid >= fair + edge_take:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair + edge_take:
                    break
                vol = min(clip, sell_cap, max(0, depth.buy_orders[px]))
                if vol > 0:
                    orders.append(Order(HYDRO, px, -vol))
                    sell_cap -= vol
                    if sell_cap <= 0:
                        break

        # Post quotes — the wider HYDRO spread means more room
        quote_offset = max(3, int(sprd * 0.35))
        if buy_cap > 0:
            bid_px = min(bid + 1, int(math.floor(fair - quote_offset)))
            bid_px = max(1, bid_px)
            post_qty = min(clip, buy_cap)
            if post_qty > 0:
                orders.append(Order(HYDRO, bid_px, post_qty))

        if sell_cap > 0:
            ask_px = max(ask - 1, int(math.ceil(fair + quote_offset)))
            post_qty = min(clip, sell_cap)
            if post_qty > 0:
                orders.append(Order(HYDRO, ask_px, -post_qty))

        return orders
