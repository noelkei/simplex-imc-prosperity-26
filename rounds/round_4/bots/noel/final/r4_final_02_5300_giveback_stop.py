import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"
SYMBOL = "VEV_5300"
STRIKE = 5300
LIMIT = 300

PEAK_GIVEBACK_FRACTION = 0.40
MIN_PEAK_EDGE = 10.0
MAX_DRAWDOWN = 60.0


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


def sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


class Trader:
    def run(self, state: TradingState):
        store = self._load(state.traderData)

        depth = state.order_depths.get(SYMBOL)
        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)

        orders: Dict[str, List[Order]] = {}
        if depth is None or opt_mid is None or vex_mid is None or bid is None or ask is None:
            self._cache(state, store)
            return orders, 0, json.dumps(store)

        spread_value = ask - bid
        position = int(state.position.get(SYMBOL, 0))
        last_vex = store.get("last_vex")
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        depth_imb = imbalance(depth)

        intrinsic = max(vex_mid - STRIKE, 0.0)
        fair = intrinsic + 6.0 + 0.70 * vex_move + 0.5 * depth_imb

        # Peak giveback tracking
        pos_state = self._refresh_position(store, position, opt_mid, state.timestamp)
        stop_triggered = self._stop_triggered(position, pos_state, opt_mid)

        if stop_triggered:
            qty = min(abs(position), 25)
            if position > 0:
                orders[SYMBOL] = [Order(SYMBOL, bid, -qty)]
            else:
                orders[SYMBOL] = [Order(SYMBOL, ask, qty)]
            self._cache(state, store, vex_mid)
            return orders, 0, json.dumps(store)

        buy_cap = max(0, LIMIT - position)
        sell_cap = max(0, LIMIT + position)
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

        out = self._dedupe(out)
        if out:
            orders[SYMBOL] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _refresh_position(self, store: dict, position: int, current_mid: float, ts: int) -> dict:
        states = store.setdefault("pos_state", {})
        existing = dict(states.get(SYMBOL, {}))
        if position == 0:
            states[SYMBOL] = {"prev_pos": 0}
            return states[SYMBOL]
        prev = int(existing.get("prev_pos", 0))
        if prev == 0 or sign(prev) != sign(position):
            states[SYMBOL] = {
                "prev_pos": position,
                "entry_mid": current_mid,
                "entry_ts": ts,
                "peak_unrealized": 0.0,
            }
            return states[SYMBOL]
        entry_mid = float(existing.get("entry_mid", current_mid))
        unrealized = (current_mid - entry_mid) * sign(position) * -1
        # For a short, profit when current_mid < entry_mid: unrealized = (entry_mid - current_mid)
        unrealized_short_correct = (entry_mid - current_mid) * sign(position) * -1
        # Simpler: unrealized = -(current_mid - entry_mid) * sign(position)
        unrealized = -(current_mid - entry_mid) * sign(position)
        peak = max(float(existing.get("peak_unrealized", 0.0)), unrealized)
        states[SYMBOL] = {
            "prev_pos": position,
            "entry_mid": entry_mid,
            "entry_ts": int(existing.get("entry_ts", ts)),
            "peak_unrealized": peak,
        }
        return states[SYMBOL]

    def _stop_triggered(self, position: int, pos_state: dict, current_mid: float) -> bool:
        if position == 0:
            return False
        entry_mid = pos_state.get("entry_mid")
        if entry_mid is None:
            return False
        peak = float(pos_state.get("peak_unrealized", 0.0))
        if peak < MIN_PEAK_EDGE:
            return False
        unrealized = -(current_mid - float(entry_mid)) * sign(position)
        giveback_hit = unrealized <= peak * (1.0 - PEAK_GIVEBACK_FRACTION)
        drawdown_hit = (peak - unrealized) >= MAX_DRAWDOWN
        return giveback_hit or drawdown_hit

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
