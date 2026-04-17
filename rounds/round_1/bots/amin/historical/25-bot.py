"""
IMC Prosperity 4 - Round 1
candidate_03_combined (v5):
  - INTARIAN_PEPPER_ROOT: directional max-long (unchanged)
  - ASH_COATED_OSMIUM: fixed fair-value market maker (FV=10000)

The only change vs baseline TEST1_merged:
  ACO_HALF_SPREAD: 5 → 3

At neutral position:
  Baseline: bid=9995, ask=10005 (market bots at ~9992/10008)
  v5:       bid=9997, ask=10003 (2 ticks inside market bots on each side)

v5 beats market bots more often → more incoming orders fill us first.
For v5 to beat baseline, need >1.67x more fills at 3-tick vs 5-tick margin.

Widening skew (my_ask = FV + HS + skew) is kept:
  - Ask ALWAYS above FV+HS → never selling below fair value.
  - Safe, no crossed spread, no weird behavior at extreme positions.

No one-sided quoting (confirmed harmful: -194 P&L in v3).
"""

from datamodel import Order, OrderDepth, TradingState
from typing import List, Dict
import json

POSITION_LIMITS = {
    "ASH_COATED_OSMIUM": 80,
    "INTARIAN_PEPPER_ROOT": 80,
}

ACO_FAIR_VALUE  = 10000
ACO_HALF_SPREAD = 3    # was 5. Puts us inside market bots (~9992/10008)
ACO_SKEW_FACTOR = 3    # widening skew, unchanged from baseline


class Trader:

    def _load(self, traderData: str) -> dict:
        if not traderData:
            return {}
        try:
            return json.loads(traderData)
        except Exception:
            return {}

    def _save(self, data: dict) -> str:
        return json.dumps(data)

    def _trade_ipr(self, od, position, pos_limit):
        orders = []
        product = "INTARIAN_PEPPER_ROOT"
        capacity = pos_limit - position
        if capacity <= 0:
            return orders
        for ask_price in sorted(od.sell_orders):
            if capacity <= 0:
                break
            qty = min(-od.sell_orders[ask_price], capacity)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                capacity -= qty
        if capacity > 0 and od.buy_orders:
            best_bid = max(od.buy_orders)
            orders.append(Order(product, best_bid + 1, capacity))
        return orders

    def _trade_aco(self, od, position, pos_limit):
        orders = []
        product = "ASH_COATED_OSMIUM"
        if not od.buy_orders and not od.sell_orders:
            return orders
        fair_value = ACO_FAIR_VALUE
        skew = round((position / pos_limit) * ACO_SKEW_FACTOR)
        my_bid = fair_value - ACO_HALF_SPREAD - skew
        my_ask = fair_value + ACO_HALF_SPREAD + skew  # widening: ask always above FV
        buy_cap  = pos_limit - position
        sell_cap = pos_limit + position
        for ask_price in sorted(od.sell_orders):
            if ask_price >= fair_value:
                break
            qty = min(-od.sell_orders[ask_price], buy_cap)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                buy_cap -= qty
                position += qty
        for bid_price in sorted(od.buy_orders, reverse=True):
            if bid_price <= fair_value:
                break
            qty = min(od.buy_orders[bid_price], sell_cap)
            if qty > 0:
                orders.append(Order(product, bid_price, -qty))
                sell_cap -= qty
                position -= qty
        if buy_cap > 0:
            orders.append(Order(product, my_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))
        return orders

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result: Dict[str, List[Order]] = {}
        for product, od in state.order_depths.items():
            position  = state.position.get(product, 0)
            pos_limit = POSITION_LIMITS.get(product, 80)
            if product == "INTARIAN_PEPPER_ROOT":
                orders = self._trade_ipr(od, position, pos_limit)
            elif product == "ASH_COATED_OSMIUM":
                orders = self._trade_aco(od, position, pos_limit)
            else:
                orders = []
            result[product] = orders
        return result, 0, self._save(sd)