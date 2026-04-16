"""
IMC Prosperity 4 — Round 1
candidate_03_combined (v3)

Strategy synthesis:
  - IPR: directional max-long (Bruno's proven approach)
    Buy everything, hold at +80. Captures +1000/day drift.
    P&L evidence: 12,099.5 on day 0 from new_bot.py logs.
  - ACO: fixed FV=10000 market maker with tight spread + aggressive inventory skew
    Sweep mispriced levels, post full resting orders.
    HALF_SPREAD=5, SKEW_FACTOR=3 (proven in Bruno's new_bot.py).
    P&L evidence: 10,003.0 on day 0 from new_bot.py logs.

Improvements over new_bot.py baseline (22,102.5 total P&L):
  - try/except isolation per product (spec requirement)
  - ACO FV deviation tracking via traderData (spec's alert counter)
  - Cleaner capacity math using pos_limit consistently

Evidence base:
  rounds/round_1/workspace/01_eda/eda_round_1.md
  rounds/round_1/workspace/04_strategy_specs/spec_candidate_03_combined.md
  rounds/round_1/bots/bruno/canonical/new_bot.py (baseline)
  rounds/round_1/bots/bruno/canonical/new_bot_logs.log (1000-tick log)
"""

from datamodel import Order, OrderDepth, TradingState
import json

# ── Position limits (wiki fact) ──────────────────────────────────
POSITION_LIMITS = {
    "INTARIAN_PEPPER_ROOT": 80,
    "ASH_COATED_OSMIUM": 80,
}

# ── ACO parameters (tuned from Bruno's proven baseline) ──────────
ACO_FAIR_VALUE  = 10000
ACO_HALF_SPREAD = 5
ACO_SKEW_FACTOR = 3

# ── ACO FV monitoring (from spec, for debugging) ─────────────────
ACO_FV_ALERT_THRESHOLD = 30   # mid deviates >30 from FV
ACO_FV_ALERT_TICKS     = 50   # consecutive ticks to flag


class Trader:

    # ── traderData persistence ────────────────────────────────────
    def _load(self, trader_data: str) -> dict:
        if not trader_data:
            return {}
        try:
            return json.loads(trader_data)
        except Exception:
            return {}

    def _save(self, data: dict) -> str:
        return json.dumps(data)

    # ── IPR: directional max-long ─────────────────────────────────
    def _trade_ipr(self, od: OrderDepth, position: int, pos_limit: int):
        orders = []
        product = "INTARIAN_PEPPER_ROOT"
        capacity = pos_limit - position
        if capacity <= 0:
            return orders

        # Sweep all asks — buy everything available
        for ask_price in sorted(od.sell_orders):
            if capacity <= 0:
                break
            ask_vol = -od.sell_orders[ask_price]  # sell_orders values are negative
            qty = min(ask_vol, capacity)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                capacity -= qty

        # Post remaining capacity as bid at best_bid + 1
        if capacity > 0 and od.buy_orders:
            best_bid = max(od.buy_orders)
            orders.append(Order(product, best_bid + 1, capacity))

        return orders

    # ── ACO: FV=10000 market maker with sweep + resting orders ────
    def _trade_aco(self, od: OrderDepth, position: int, pos_limit: int,
                   sd: dict):
        orders = []
        product = "ASH_COATED_OSMIUM"

        if not od.buy_orders and not od.sell_orders:
            return orders

        fair_value = ACO_FAIR_VALUE

        # FV deviation tracking
        mid = None
        if od.buy_orders and od.sell_orders:
            best_bid = max(od.buy_orders)
            best_ask = min(od.sell_orders)
            mid = (best_bid + best_ask) / 2

        alert_count = sd.get("aco_alert", 0)
        if mid is not None and abs(mid - fair_value) > ACO_FV_ALERT_THRESHOLD:
            alert_count += 1
        else:
            alert_count = 0
        sd["aco_alert"] = alert_count

        # Inventory skew: shift quotes to flatten position
        skew = round((position / pos_limit) * ACO_SKEW_FACTOR)
        my_bid = fair_value - ACO_HALF_SPREAD - skew
        my_ask = fair_value + ACO_HALF_SPREAD + skew

        buy_cap = pos_limit - position
        sell_cap = pos_limit + position

        # Sweep asks below fair value (immediate profit)
        for ask_price in sorted(od.sell_orders):
            if ask_price >= fair_value:
                break
            if buy_cap <= 0:
                break
            ask_vol = -od.sell_orders[ask_price]
            qty = min(ask_vol, buy_cap)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                buy_cap -= qty

        # Sweep bids above fair value (immediate profit)
        for bid_price in sorted(od.buy_orders, reverse=True):
            if bid_price <= fair_value:
                break
            if sell_cap <= 0:
                break
            bid_vol = od.buy_orders[bid_price]
            qty = min(bid_vol, sell_cap)
            if qty > 0:
                orders.append(Order(product, bid_price, -qty))
                sell_cap -= qty

        # Post resting orders at skewed quotes with remaining capacity
        if buy_cap > 0:
            orders.append(Order(product, my_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── Main entry ────────────────────────────────────────────────
    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result = {}

        for product in state.order_depths:
            od = state.order_depths[product]
            position = state.position.get(product, 0)
            pos_limit = POSITION_LIMITS.get(product, 80)

            if product == "INTARIAN_PEPPER_ROOT":
                try:
                    result[product] = self._trade_ipr(od, position, pos_limit)
                except Exception:
                    result[product] = []

            elif product == "ASH_COATED_OSMIUM":
                try:
                    result[product] = self._trade_aco(od, position, pos_limit, sd)
                except Exception:
                    result[product] = []

            else:
                result[product] = []

        return result, 0, self._save(sd)
