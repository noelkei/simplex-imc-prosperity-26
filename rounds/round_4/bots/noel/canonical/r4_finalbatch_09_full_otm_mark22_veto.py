import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"
MONITOR = "VEV_5200"
STRIKES = {
    "VEV_5300": (5300, 6.0),
    "VEV_5400": (5400, 4.0),
    "VEV_5500": (5500, 2.5),
}
LIMIT = 300
RECENT_WINDOW = 4_000


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


def classify_trade_bucket(price: int, bid: Optional[int], ask: Optional[int]) -> str:
    if bid is None or ask is None:
        return "unknown"
    if price >= ask:
        return "aggressive_buy"
    if price <= bid:
        return "aggressive_sell"
    return "inside"


class Trader:
    def run(self, state: TradingState):
        store = self._load(state.traderData)
        self._update_monitor_events(state, store)

        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)

        orders: Dict[str, List[Order]] = {}
        if vex_mid is None:
            self._cache(state, store)
            return orders, 0, json.dumps(store)

        last_vex = store.get("last_vex")
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        bad_5200_recent = self._bad_monitor_recent(state, store)

        for symbol, (strike, premium) in STRIKES.items():
            out = self._trade_strike(
                state,
                symbol,
                strike,
                premium,
                vex_mid,
                vex_move,
                bad_5200_recent,
            )
            if out:
                orders[symbol] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _update_monitor_events(self, state: TradingState, store: dict) -> None:
        depth = state.order_depths.get(MONITOR)
        bid, ask = best_bid_ask(depth)
        events = list(store.get("recent_5200_events", []))
        for trade in state.market_trades.get(MONITOR, []):
            price = int(getattr(trade, "price", 0) or 0)
            events.append(
                {
                    "timestamp": int(getattr(trade, "timestamp", state.timestamp) or state.timestamp),
                    "seller": getattr(trade, "seller", "") or "",
                    "bucket": classify_trade_bucket(price, bid, ask),
                }
            )
        cutoff = state.timestamp - RECENT_WINDOW
        store["recent_5200_events"] = [event for event in events if event["timestamp"] >= cutoff]

    def _bad_monitor_recent(self, state: TradingState, store: dict) -> bool:
        cutoff = state.timestamp - RECENT_WINDOW
        for event in store.get("recent_5200_events", []):
            if event["timestamp"] < cutoff:
                continue
            if event["seller"] == "Mark 22" or event["bucket"] != "inside":
                return True
        return False

    def _trade_strike(
        self,
        state: TradingState,
        symbol: str,
        strike: int,
        premium: float,
        vex_mid: float,
        vex_move: float,
        bad_5200_recent: bool,
    ) -> List[Order]:
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

        if abs(opt_mid - fair) < 3.0:
            return []

        buy_cap = max(0, LIMIT - position)
        sell_cap = max(0, LIMIT + position)
        clip = 15
        if abs(position) >= 240:
            clip = 5
        elif abs(position) >= 180:
            clip = 8

        out: List[Order] = []
        edge = 2.0
        block_new_sells = bad_5200_recent and position <= 0

        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                out.append(Order(symbol, ask, qty))
        if sell_cap > 0 and bid >= fair + edge and not block_new_sells:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                out.append(Order(symbol, bid, -qty))

        if spread_value <= 6:
            if buy_cap > 0:
                bid_px = min(bid + 1, int(fair - 1))
                bid_px = max(1, bid_px)
                out.append(Order(symbol, bid_px, min(max(1, clip // 2), buy_cap)))
            if sell_cap > 0 and not block_new_sells:
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
