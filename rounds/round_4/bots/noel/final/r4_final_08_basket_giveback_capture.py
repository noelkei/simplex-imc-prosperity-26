"""
r4_final_08_basket_giveback_capture: 4-strike basket with peak retention rule.

Strategy: Same 4-strike basket (5200+5300+5400+5500) as bot 06, but adds a
peak giveback stop. The bot 05 saw peak PnL = 10,138 at ts=86600 but ended at
8,729 (giveback of 1,409 = 14%). By flattening when peak gives back >=25%
per strike, we capture more of the peak.

Per-strike retention: tracks unrealized PnL, flattens when current <= peak * 0.75
(after peak >= 100 to avoid early noise).

vs bot 06: same 4 strikes, captures peak before late-session reversion.
Target: 18-22k.
"""
import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"
STRIKES = {
    "VEV_5200": (5200, 8.0, 30),
    "VEV_5300": (5300, 6.0, 30),
    "VEV_5400": (5400, 4.0, 25),
    "VEV_5500": (5500, 2.5, 20),
}
LIMIT = 300

GIVEBACK_FRACTION = 0.25
MIN_PEAK_FOR_STOP = 100.0
HARD_DRAWDOWN = 800.0


def sign(value: int) -> int:
    return (value > 0) - (value < 0)


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
            out = self._trade_strike(state, store, symbol, strike, premium, base_clip, vex_mid, vex_move)
            if out:
                orders[symbol] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _trade_strike(self, state, store, symbol, strike, premium, base_clip, vex_mid, vex_move) -> List[Order]:
        depth = state.order_depths.get(symbol)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)
        if depth is None or opt_mid is None or bid is None or ask is None:
            return []
        spread_value = ask - bid
        position = int(state.position.get(symbol, 0))

        # Peak giveback tracking
        pos_state = self._refresh_position(store, symbol, position, opt_mid, state.timestamp)
        if self._stop_triggered(position, pos_state, opt_mid):
            qty = min(abs(position), 30)
            if position > 0:
                return [Order(symbol, bid, -qty)]
            return [Order(symbol, ask, qty)]

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

    def _refresh_position(self, store, symbol, position, current_mid, ts):
        states = store.setdefault("pos_state", {})
        existing = dict(states.get(symbol, {}))
        if position == 0:
            states[symbol] = {"prev_pos": 0}
            return states[symbol]
        prev = int(existing.get("prev_pos", 0))
        if prev == 0 or sign(prev) != sign(position):
            states[symbol] = {
                "prev_pos": position,
                "entry_mid": current_mid,
                "entry_ts": ts,
                "peak_unrealized": 0.0,
            }
            return states[symbol]
        entry_mid = float(existing.get("entry_mid", current_mid))
        # P&L for short: profit when mid goes down. unrealized = -(current - entry) * sign(pos) * |pos|
        # We track per-unit unrealized so threshold is consistent across position sizes:
        unrealized_per_unit = -(current_mid - entry_mid) * sign(position)
        unrealized_total = unrealized_per_unit * abs(position)
        peak = max(float(existing.get("peak_unrealized", 0.0)), unrealized_total)
        states[symbol] = {
            "prev_pos": position,
            "entry_mid": entry_mid,
            "entry_ts": int(existing.get("entry_ts", ts)),
            "peak_unrealized": peak,
        }
        return states[symbol]

    def _stop_triggered(self, position, pos_state, current_mid) -> bool:
        if position == 0:
            return False
        entry_mid = pos_state.get("entry_mid")
        if entry_mid is None:
            return False
        peak = float(pos_state.get("peak_unrealized", 0.0))
        if peak < MIN_PEAK_FOR_STOP:
            return False
        unrealized_per_unit = -(current_mid - float(entry_mid)) * sign(position)
        unrealized_total = unrealized_per_unit * abs(position)
        giveback_hit = unrealized_total <= peak * (1.0 - GIVEBACK_FRACTION)
        drawdown_hit = (peak - unrealized_total) >= HARD_DRAWDOWN
        return giveback_hit or drawdown_hit

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
