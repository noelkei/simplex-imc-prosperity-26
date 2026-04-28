import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"
SYMBOL = "VEV_5300"
STRIKE = 5300
OPT_LIMIT = 300
VEX_LIMIT = 200


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

        # Primary: VEV_5300 short
        opt_orders = self._trade_5300(state, vex_mid, vex_move)
        if opt_orders:
            orders[SYMBOL] = opt_orders

        # Secondary: VEX delta-1 carry
        vex_orders = self._trade_vex(state, vex_mid, store)
        if vex_orders:
            orders[VEX] = vex_orders

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _trade_5300(self, state: TradingState, vex_mid: float, vex_move: float) -> List[Order]:
        depth = state.order_depths.get(SYMBOL)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)
        if depth is None or opt_mid is None or bid is None or ask is None:
            return []
        spread_value = ask - bid
        position = int(state.position.get(SYMBOL, 0))
        depth_imb = imbalance(depth)

        intrinsic = max(vex_mid - STRIKE, 0.0)
        fair = intrinsic + 6.0 + 0.70 * vex_move + 0.5 * depth_imb

        buy_cap = max(0, OPT_LIMIT - position)
        sell_cap = max(0, OPT_LIMIT + position)
        clip = 22
        if abs(position) >= 240:
            clip = 8
        elif abs(position) >= 180:
            clip = 12

        out: List[Order] = []
        edge = 2.0
        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                out.append(Order(SYMBOL, ask, qty))
        if sell_cap > 0 and bid >= fair + edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                out.append(Order(SYMBOL, bid, -qty))

        if spread_value <= 8:
            if buy_cap > 0:
                bid_px = min(bid + 1, int(fair - 1))
                bid_px = max(1, bid_px)
                out.append(Order(SYMBOL, bid_px, min(max(1, clip // 2), buy_cap)))
            if sell_cap > 0:
                ask_px = max(ask - 1, int(fair + 1))
                out.append(Order(SYMBOL, ask_px, -min(max(1, clip // 2), sell_cap)))

        return self._dedupe(out)

    def _trade_vex(self, state: TradingState, vex_mid: float, store: dict) -> List[Order]:
        depth = state.order_depths.get(VEX)
        bid, ask = best_bid_ask(depth)
        if depth is None or bid is None or ask is None:
            return []
        spread_value = ask - bid
        if spread_value > 6:
            return []
        position = int(state.position.get(VEX, 0))
        last_vex = store.get("last_vex")
        move_term = 0.0 if last_vex is None else 0.15 * (vex_mid - last_vex)
        fair = vex_mid + 1.2 * imbalance(depth) + move_term

        buy_cap = max(0, VEX_LIMIT - position)
        sell_cap = max(0, VEX_LIMIT + position)
        clip = 12
        if abs(position) >= 120:
            clip = 4
        elif abs(position) >= 80:
            clip = 6

        out: List[Order] = []
        cross_edge = 2
        if buy_cap > 0 and ask <= fair - cross_edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                out.append(Order(VEX, ask, qty))
        if sell_cap > 0 and bid >= fair + cross_edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                out.append(Order(VEX, bid, -qty))

        if spread_value <= 5:
            if buy_cap > 0:
                bid_px = min(bid + 1, int(fair - 1))
                out.append(Order(VEX, bid_px, min(clip, buy_cap)))
            if sell_cap > 0:
                ask_px = max(ask - 1, int(fair + 1))
                out.append(Order(VEX, ask_px, -min(clip, sell_cap)))

        return self._dedupe(out)

    def _load(self, td) -> dict:
        if not isinstance(td, str) or not td:
            return {}
        try:
            d = json.loads(td)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}

    def _cache(self, state: TradingState, store: dict, vex_mid: Optional[float] = None) -> None:
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
