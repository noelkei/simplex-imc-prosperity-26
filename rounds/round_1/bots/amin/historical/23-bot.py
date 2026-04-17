"""
IMC Prosperity 4 - Round 1
candidate_03_combined (v4):
  - INTARIAN_PEPPER_ROOT: directional max-long (unchanged)
  - ASH_COATED_OSMIUM: fixed fair-value market maker (FV=10000)

Evidence base:
  rounds/round_1/workspace/01_eda/eda_round_1.md
  rounds/round_1/workspace/02_understanding.md
  rounds/round_1/workspace/03_strategy_candidates.md

Changes vs v3 (two separate improvements to ACO):

  1. Fixed ask skew direction (v3 bug):
       OLD: my_ask = FV + HS + skew  (when long: raises ask UP — harder to sell)
       NEW: my_ask = FV + HS - skew  (when long: lowers ask DOWN — easier to sell)
     Effect: centered shift — both bid and ask shift DOWN when long, UP when short.
     The spread stays constant at 2*HS=4. This is correct inventory management:
     long position → sell more easily (lower ask), buy less eagerly (lower bid).
     Short position → buy more eagerly (higher bid), sell less eagerly (higher ask).

  2. Tighter passive spread:
       ACO_HALF_SPREAD: 5 → 2
     Old bid/ask at neutral: 9995 / 10005 (10 tick spread)
     New bid/ask at neutral: 9998 / 10002 (4 tick spread)
     Effect: our quotes beat market bots who quote at ~9992/10008. We are the
     best bid and ask in the market most of the time, so all incoming market
     flow fills us. Earns less per fill but dramatically more fills.

  3. Removed one-sided quoting:
     v3 introduced ACO_ONE_SIDED_THRESHOLD=40 which HURT performance (-194 P&L).
     With the centered skew and tight spread, inventory management is handled
     naturally: at position limits, buy_cap/sell_cap = 0 (no quote placed).

  Skew table with new formula (HS=2, SKEW_FACTOR=4):
    pos=0   : bid=9998, ask=10002  (spread 4, center at 10000)
    pos=+40 : bid=9996, ask=10000  (center at 9998 — actively selling at FV)
    pos=+80 : bid not placed (buy_cap=0), ask=9998  (2 below FV — exit fast)
    pos=-40 : bid=10000, ask=10004  (center at 10002 — actively buying at FV)
    pos=-80 : bid=10002, ask not placed (sell_cap=0)  (2 above FV — exit fast)

  Test run P&L targets:
    IPR: ~7,286  (unchanged, same directional logic)
    ACO: ~4,000–6,000  (vs ~2,000 in v3)
    Total: ~11,000–13,000  (vs baseline 9,419)
"""

from datamodel import Order, OrderDepth, TradingState
from typing import List, Dict
import json

# ── Position limits ────────────────────────────────────────────────────────────
POSITION_LIMITS = {
    "ASH_COATED_OSMIUM": 80,
    "INTARIAN_PEPPER_ROOT": 80,
}

# ── Parameters ─────────────────────────────────────────────────────────────────
ACO_FAIR_VALUE  = 10000
ACO_HALF_SPREAD = 2    # tighter: was 5. Puts us inside market bots (~9992/10008)
ACO_SKEW_FACTOR = 4    # centered shift per unit of position/limit


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

    # ── INTARIAN_PEPPER_ROOT: directional max-long ─────────────────────────────
    # EDA: price drifts +0.001/tick. Holding max long captures full drift.
    # Selling surrenders drift gain for a spread tick — bad trade in trend.

    def _trade_ipr(
        self,
        od: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
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

    # ── ASH_COATED_OSMIUM: fixed fair-value market maker ──────────────────────
    # EDA: mean-reverts around 10,000. Spread dominated by 16 ticks.
    # Centered skew: both bid and ask shift together in direction that reduces
    # inventory. Tight spread (HS=2) captures more fills than wider spread.

    def _trade_aco(
        self,
        od: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "ASH_COATED_OSMIUM"

        if not od.buy_orders and not od.sell_orders:
            return orders

        fair_value = ACO_FAIR_VALUE
        skew = round((position / pos_limit) * ACO_SKEW_FACTOR)

        # Centered shift: both quotes move DOWN when long, UP when short.
        # Spread stays constant at 2 * ACO_HALF_SPREAD = 4.
        my_bid = fair_value - ACO_HALF_SPREAD - skew
        my_ask = fair_value + ACO_HALF_SPREAD - skew  # KEY FIX: was +skew in v3

        buy_cap  = pos_limit - position
        sell_cap = pos_limit + position

        # Aggressive: take any ask strictly below fair value
        for ask_price in sorted(od.sell_orders):
            if ask_price >= fair_value:
                break
            qty = min(-od.sell_orders[ask_price], buy_cap)
            if qty > 0:
                orders.append(Order(product, ask_price, qty))
                buy_cap  -= qty
                position += qty

        # Aggressive: hit any bid strictly above fair value
        for bid_price in sorted(od.buy_orders, reverse=True):
            if bid_price <= fair_value:
                break
            qty = min(od.buy_orders[bid_price], sell_cap)
            if qty > 0:
                orders.append(Order(product, bid_price, -qty))
                sell_cap  -= qty
                position  -= qty

        # Passive resting quotes (one-sided naturally when at position limits)
        if buy_cap > 0:
            orders.append(Order(product, my_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── Main entry point ───────────────────────────────────────────────────────

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