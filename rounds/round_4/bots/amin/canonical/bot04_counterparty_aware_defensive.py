"""
Bot 04: Counterparty-Aware Defensive VEX + HYDRO
==================================================
Approach: Market-make on VEX and HYDRO but use counterparty information from
market trades to detect toxic flow. When Mark 22 (the documented aggressive
seller in upper strikes) or concentrated aggressive selling is detected,
pull back on VEX new entries and widen quotes. HYDRO trades independently.
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

HYDRO = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
LIMITS = {HYDRO: 200, VEX: 200}
FAMILY_SYMBOLS = [
    "VEV_4000", "VEV_4500", "VEV_5000", "VEV_5100", "VEV_5200",
    "VEV_5300", "VEV_5400", "VEV_5500", "VEV_6000", "VEV_6500",
]
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


class Trader:
    def run(self, state: TradingState):
        stored = {}
        if state.traderData:
            try:
                stored = json.loads(state.traderData)
            except Exception:
                stored = {}

        # Detect toxic flow from counterparties
        toxic_state = self._detect_toxic_flow(state, stored)

        result: Dict[str, List[Order]] = {}

        # VEX with counterparty awareness
        vex_orders = self._trade_vex(state, stored, toxic_state)
        if vex_orders:
            result[VEX] = vex_orders

        # HYDRO independently (no counterparty concern)
        hydro_orders = self._trade_hydro(state, stored)
        if hydro_orders:
            result[HYDRO] = hydro_orders

        mids = stored.setdefault("mids", {})
        for sym in [VEX, HYDRO]:
            m = mid_price(state.order_depths.get(sym))
            if m is not None:
                mids[sym] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _detect_toxic_flow(self, state: TradingState, stored: dict) -> dict:
        """Analyze recent market trades for toxic counterparty activity."""
        events = list(stored.get("cp_events", []))
        for symbol, trades in state.market_trades.items():
            if symbol not in FAMILY_SYMBOLS and symbol != VEX:
                continue
            for trade in trades:
                buyer = getattr(trade, "buyer", "") or ""
                seller = getattr(trade, "seller", "") or ""
                events.append({
                    "sym": symbol,
                    "b": buyer,
                    "s": seller,
                    "ts": int(getattr(trade, "timestamp", state.timestamp) or state.timestamp),
                })
        # Keep last 80 events
        if len(events) > 80:
            events = events[-80:]
        stored["cp_events"] = events

        now = state.timestamp
        recent = [e for e in events if e["ts"] >= now - 5000]

        # Detect Mark 22 seller pressure in upper strikes
        mark22_selling = any(
            e["s"] == "Mark 22" and e["sym"] in {"VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"}
            for e in recent
        )

        # Detect concentrated aggressive flow
        sellers = {}
        for e in recent:
            s = e.get("s", "")
            if s:
                sellers[s] = sellers.get(s, 0) + 1
        total_sells = sum(sellers.values())
        concentration = max(sellers.values()) / total_sells if total_sells > 0 else 0.0

        return {
            "mark22_active": mark22_selling,
            "seller_concentration": concentration,
            "toxic": mark22_selling or concentration > 0.55,
        }

    def _trade_vex(self, state: TradingState, stored: dict, toxic: dict) -> List[Order]:
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
        inv_skew = -0.12 * position
        fair = mid + 1.2 * imb + mom + inv_skew

        clip = 12
        if abs(position) >= 120:
            clip = 4
        elif abs(position) >= 80:
            clip = 8

        # Defensive pullback when toxic
        block_new = False
        if toxic["toxic"]:
            clip = max(2, clip // 2)
            if position >= 0:
                # Don't add to longs when sellers are aggressive
                block_new = True

        orders: List[Order] = []
        if buy_cap > 0 and not block_new and ask <= fair - 2.0:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                orders.append(Order(VEX, ask, qty))
                buy_cap -= qty

        if sell_cap > 0 and bid >= fair + 2.0:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                orders.append(Order(VEX, bid, -qty))
                sell_cap -= qty

        quote_width = 1 if not toxic["toxic"] else 2
        if sprd <= 5:
            if buy_cap > 0 and not block_new:
                px = min(bid + 1, int(math.floor(fair - quote_width)))
                px = max(1, px)
                orders.append(Order(VEX, px, min(clip, buy_cap)))
            if sell_cap > 0:
                px = max(ask - 1, int(math.ceil(fair + quote_width)))
                orders.append(Order(VEX, px, -min(clip, sell_cap)))

        return orders

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

        imb = imbalance(depth)
        position = state.position.get(HYDRO, 0)
        buy_cap = max(0, LIMITS[HYDRO] - position)
        sell_cap = max(0, LIMITS[HYDRO] + position)
        inv_skew = -0.2 * position
        fair = mid + 1.5 * imb + inv_skew

        clip = 10
        if abs(position) > 150:
            clip = 3
        elif abs(position) > 100:
            clip = 6

        orders: List[Order] = []
        edge = max(2.0, sprd * 0.15)
        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                orders.append(Order(HYDRO, ask, qty))
                buy_cap -= qty
        if sell_cap > 0 and bid >= fair + edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                orders.append(Order(HYDRO, bid, -qty))
                sell_cap -= qty

        offset = max(3, int(sprd * 0.3))
        if buy_cap > 0:
            px = min(bid + 1, int(math.floor(fair - offset)))
            px = max(1, px)
            orders.append(Order(HYDRO, px, min(clip, buy_cap)))
        if sell_cap > 0:
            px = max(ask - 1, int(math.ceil(fair + offset)))
            orders.append(Order(HYDRO, px, -min(clip, sell_cap)))

        return orders
