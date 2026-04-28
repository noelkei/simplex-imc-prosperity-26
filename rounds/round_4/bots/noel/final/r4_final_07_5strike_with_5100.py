"""
r4_final_07_5strike_with_5100: Adds VEV_5100 and VEV_5200 to the basket.

Strategy: 5 strikes (5100, 5200, 5300, 5400, 5500). VEV_5100 is slightly ITM
when VEX = 5295, with intrinsic = 195 and market mid 201.5 (premium = 6.5).
By using a smaller premium (3.0) in our fair model for ITM strikes, we
correctly identify them as overpriced and trigger sell orders.

VEV_5100 captured the largest move in the OTM/ATM band: 201.5 -> 164 = -37.5
per unit. At 300 short, max PnL = +11,250.

vs bot 06: adds VEV_5100 (+11k potential).
Target: 22-26k.
"""
import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"
# Per-strike: (strike, premium, base_clip)
# Smaller premium for ITM strikes since their time value is smaller
STRIKES = {
    "VEV_5100": (5100, 3.0, 30),
    "VEV_5200": (5200, 8.0, 30),
    "VEV_5300": (5300, 6.0, 30),
    "VEV_5400": (5400, 4.0, 25),
    "VEV_5500": (5500, 2.5, 20),
}
LIMIT = 300


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


def imbalance(depth) -> float:
    if depth is None:
        return 0.0
    bid, ask = best_bid_ask(depth)
    bid_size = depth.buy_orders.get(bid, 0) if bid is not None else 0
    ask_size = -depth.sell_orders.get(ask, 0) if ask is not None else 0
    total = bid_size + ask_size
    if total <= 0:
        return 0.0
    return (bid_size - ask_size) / total


class Trader:
    def run(self, state: TradingState):
        store = self._load(state.traderData)
        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)

        orders: Dict[str, List[Order]] = {}
        if vex_mid is None:
            self._cache(state, store)
            return orders, 0, json.dumps(store)

        last_vex = store.get("last_vex")
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex

        for symbol, (strike, premium, base_clip) in STRIKES.items():
            out = self._trade_strike(state, symbol, strike, premium, base_clip, vex_mid, vex_move)
            if out:
                orders[symbol] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _trade_strike(self, state, symbol, strike, premium, base_clip, vex_mid, vex_move) -> List[Order]:
        depth = state.order_depths.get(symbol)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)
        if depth is None or opt_mid is None or bid is None or ask is None:
            return []
        spread_value = ask - bid
        position = int(state.position.get(symbol, 0))
        depth_imb = imbalance(depth)

        intrinsic = max(vex_mid - strike, 0.0)
        fair = intrinsic + premium + 0.70 * vex_move + 0.5 * depth_imb

        buy_cap = max(0, LIMIT - position)
        sell_cap = max(0, LIMIT + position)
        clip = base_clip
        if abs(position) >= 270:
            clip = max(5, clip // 3)
        elif abs(position) >= 220:
            clip = max(8, clip // 2)

        out: List[Order] = []
        edge = 2.0
        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                out.append(Order(symbol, ask, qty))
        if sell_cap > 0 and bid >= fair + edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                out.append(Order(symbol, bid, -qty))

        if spread_value <= 8:
            if buy_cap > 0:
                bid_px = min(bid + 1, int(fair - 1))
                bid_px = max(1, bid_px)
                out.append(Order(symbol, bid_px, min(max(1, clip // 2), buy_cap)))
            if sell_cap > 0:
                ask_px = max(ask - 1, int(fair + 1))
                out.append(Order(symbol, ask_px, -min(max(1, clip // 2), sell_cap)))

        return self._dedupe(out)

    def _load(self, td) -> dict:
        if not isinstance(td, str) or not td:
            return {}
        try:
            d = json.loads(td)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}

    def _cache(self, state, store, vex_mid: Optional[float] = None) -> None:
        if vex_mid is None:
            vex_mid = mid_price(state.order_depths.get(VEX))
        if vex_mid is not None:
            store["last_vex"] = vex_mid

    def _dedupe(self, orders: List[Order]) -> List[Order]:
        merged: Dict[Tuple[str, int], int] = {}
        for o in orders:
            key = (o.symbol, o.price)
            merged[key] = merged.get(key, 0) + int(o.quantity)
        return [Order(s, p, q) for (s, p), q in merged.items() if q != 0]
