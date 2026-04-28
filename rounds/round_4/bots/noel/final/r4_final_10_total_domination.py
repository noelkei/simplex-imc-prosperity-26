"""
r4_final_10_total_domination: Jane-Street-style total family short.

Strategy: Short EVERY VEV strike (4000 through 5500) plus VEX delta-1.
Eight option strikes at limit -300 each gives 2,400 units of short exposure
to the VEX-down thesis, plus 200 of direct VEX short.

Key insight: deep ITM calls (4000, 4500, 5000) act as delta-1 leverage
with higher position limits (300) than VEX itself (200). For ITM strikes,
market mid ~ intrinsic, so the standard fair = intrinsic + premium model
fails to trigger sells. We instead set fair = intrinsic - small_discount,
forcing the model to see them as overpriced and short aggressively.

Per-strike fair value model:
- ITM (4000, 4500, 5000): fair = intrinsic - small_discount
- ATM/borderline (5100, 5200): fair = intrinsic + tuned_premium
- OTM (5300, 5400, 5500): fair = intrinsic + tuned_premium

Theoretical max PnL at -300 each from start to final on day 3 data:
  VEV_4000: 12,750  |  VEV_4500: 12,450  |  VEV_5000: 12,150
  VEV_5100: 11,250  |  VEV_5200:  9,300  |  VEV_5300:  5,700
  VEV_5400:  2,700  |  VEV_5500:  1,050  |  VEX:      8,400
  Total: ~75,750

vs bot 09 (26k actual): adds 3 deep ITM strikes (~37k additional theoretical).
Realistic target: 40-55k.
"""
import json
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


VEX = "VELVETFRUIT_EXTRACT"

# (strike, fair_offset, base_clip, edge)
# fair_offset: added to intrinsic to get fair value
#   negative for ITM (force model to see as overpriced)
#   positive small for OTM (matches the market premium minus a bit)
STRIKE_CONFIG = {
    "VEV_4000": (4000, -2.0, 35, 2.0),
    "VEV_4500": (4500, -2.0, 35, 2.0),
    "VEV_5000": (5000, -1.0, 30, 2.0),
    "VEV_5100": (5100,  3.0, 30, 2.0),
    "VEV_5200": (5200,  8.0, 30, 2.0),
    "VEV_5300": (5300,  6.0, 30, 2.0),
    "VEV_5400": (5400,  4.0, 25, 2.0),
    "VEV_5500": (5500,  2.5, 20, 2.0),
}
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

        for symbol, (strike, fair_offset, base_clip, edge) in STRIKE_CONFIG.items():
            out = self._trade_strike(state, symbol, strike, fair_offset, base_clip, edge, vex_mid, vex_move)
            if out:
                orders[symbol] = out

        vex_orders = self._trade_vex(state, vex_mid, store)
        if vex_orders:
            orders[VEX] = vex_orders

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _trade_strike(self, state, symbol, strike, fair_offset, base_clip, edge, vex_mid, vex_move) -> List[Order]:
        depth = state.order_depths.get(symbol)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)
        if depth is None or opt_mid is None or bid is None or ask is None:
            return []
        spread_value = ask - bid
        position = int(state.position.get(symbol, 0))
        depth_imb = imbalance(depth)

        intrinsic = max(vex_mid - strike, 0.0)
        # For ITM strikes the depth_imb signal is less meaningful; use 0.3x
        imb_weight = 0.3 if fair_offset <= 0 else 0.5
        fair = intrinsic + fair_offset + 0.70 * vex_move + imb_weight * depth_imb

        buy_cap = max(0, OPT_LIMIT - position)
        sell_cap = max(0, OPT_LIMIT + position)
        clip = base_clip
        if abs(position) >= 270:
            clip = max(5, clip // 3)
        elif abs(position) >= 220:
            clip = max(8, clip // 2)

        out: List[Order] = []

        # Cross orders
        if buy_cap > 0 and ask <= fair - edge:
            qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if qty > 0:
                out.append(Order(symbol, ask, qty))
        if sell_cap > 0 and bid >= fair + edge:
            qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if qty > 0:
                out.append(Order(symbol, bid, -qty))

        # Passive quoting -- always post inside the spread when possible
        # For ITM strikes the spread is wide (e.g., VEV_4000 spread ~21),
        # so we use the strike's actual spread tolerance via fair value rather
        # than a fixed cutoff
        if buy_cap > 0:
            target_bid = int(fair - 1)
            bid_px = min(bid + 1, target_bid)
            bid_px = max(1, bid_px)
            if bid_px > bid:  # only post if improving
                qty = min(max(1, clip // 2), buy_cap)
                out.append(Order(symbol, bid_px, qty))
        if sell_cap > 0:
            target_ask = int(fair + 1)
            ask_px = max(ask - 1, target_ask)
            if ask_px < ask:  # only post if improving
                qty = min(max(1, clip // 2), sell_cap)
                out.append(Order(symbol, ask_px, -qty))

        return self._dedupe(out)

    def _trade_vex(self, state, vex_mid, store) -> List[Order]:
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
        clip = 18
        if abs(position) >= 160:
            clip = 6
        elif abs(position) >= 120:
            clip = 10

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
