"""
IMC Prosperity 4 - Round 1
candidate_03_combined (v2):
  - INTARIAN_PEPPER_ROOT: directional max-long (captures +1000/day drift)
  - ASH_COATED_OSMIUM: fixed fair-value market maker (FV=10000)

Evidence base:
  rounds/round_1/workspace/01_eda/eda_round_1.md
  rounds/round_1/workspace/04_strategy_specs/spec_candidate_01_ipr_drift.md
  rounds/round_1/workspace/04_strategy_specs/spec_candidate_02_aco_fixedfv.md

Baseline performance (TEST1_merged, same IPR logic):
  rounds/round_1/performances/bruno/canonical/190076.json
  Total P&L: 9,419  |  IPR final pos: +80  |  ACO final pos: +44

Changes vs TEST1_merged:
  - ACO_SKEW_FACTOR: 2 -> 3  (reduce inventory swings: baseline peaked at +65/-36)
  - Removed print() statements (slow execution, pollute logs)
  - Removed unused _update_ema helper
"""

from datamodel import Order, OrderDepth, TradingState
from typing import List, Dict
import json

POSITION_LIMITS = {
    "ASH_COATED_OSMIUM": 80,
    "INTARIAN_PEPPER_ROOT": 80,
}

ACO_FAIR_VALUE  = 10000
ACO_HALF_SPREAD = 5
ACO_SKEW_FACTOR = 3    # raised from 2; flattens inventory faster


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
        my_ask = fair_value + ACO_HALF_SPREAD + skew
        buy_cap  = pos_limit - position
        sell_cap = pos_limit + position
        for ask_price in sorted(od.sell_orders):
            if ask_price >= fair_value:
                break
            qty = min(-od.sell_orders[ask_price], buy_cap)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                buy_cap  -= qty
                position += qty
        for bid_price in sorted(od.buy_orders, reverse=True):
            if bid_price <= fair_value:
                break
            qty = min(od.buy_orders[bid_price], sell_cap)
            if qty > 0:
                orders.append(Order(product, bid_price, -qty))
                sell_cap  -= qty
                position  -= qty
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