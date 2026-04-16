"""
IMC Prosperity 4 - Round 1
candidate_03_combined (v5):
  - INTARIAN_PEPPER_ROOT: directional max-long (unchanged)
  - ASH_COATED_OSMIUM: fixed fair-value market maker (FV=10000)

Evidence base:
  rounds/round_1/workspace/01_eda/eda_round_1.md
  rounds/round_1/workspace/02_understanding.md

--- What happened in v4 and why it failed ---

v4 introduced two changes: centered skew formula AND tighter spread (HS=5→2).
Result: ACO P&L dropped from ~2,133 (baseline) to ~1,214.

Root cause of v4 failure:
  Centered skew: my_ask = FV + HS - skew
  With HS=2 and SKEW=4, at position +60 (skew=3): ask = 10000+2-3 = 9999
  At position +80 (skew=4): ask = 10000+2-4 = 9998

  We were selling BELOW fair value to exit accumulated positions.
  Tight spread (HS=2) causes fast accumulation to +80, then bot is forced
  to sell at 9998-9999 to exit. Every exit loses 1-2 ticks per unit.
  Net effect: more fills but at negative exit margin → lower total P&L.

--- v5 fix: revert to widening skew, only tighten the spread ---

The widening formula (my_ask = FV + HS + skew) is safe because:
  - Ask ALWAYS stays above FV + HS at neutral, and widens further when long
  - There is never a situation where we sell below FV
  - It correctly disincentivizes further buying when long (wider spread)

The only v5 change versus baseline (TEST1_merged):
  ACO_HALF_SPREAD: 5 → 3

Spread analysis at neutral position:
  Baseline: bid=9995, ask=10005 (market bots bid ~9992, ask ~10008)
  v5:       bid=9997, ask=10003 (2 ticks inside market bots on each side)

v5 is inside the market bots more often → more incoming orders fill us first.
Per-fill profit: 3 ticks per side (vs 5 before). Fill frequency: higher.
For v5 to beat baseline, we need >1.67x more fills. Plausible given we now
beat market bots consistently when they quote at 9992-9995 / 10008.

Widening skew with HS=3, SKEW=3 at position +40 (skew=2):
  bid=9995, ask=10005 — same as baseline neutral spread. Safe.

No one-sided quoting (confirmed harmful in v3: -194 P&L).

P&L targets (test run, 1,000 iterations):
  IPR: ~7,286 (unchanged)
  ACO: ~2,800–3,500 (vs ~2,133 baseline, vs ~1,214 in failed v4)
  Total: ~10,000–10,800

Next iteration if v5 still doesn't reach 4-6k ACO:
  Need to investigate WHY other teams earn 4-6k.
  Possible explanations: different market-making logic, directional bets,
  reading market_trades flow, or they are also running IPR differently.
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
ACO_HALF_SPREAD = 3    # was 5 in baseline. 3 puts us inside market bots (~9992/10008)
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

    # ── INTARIAN_PEPPER_ROOT: directional max-long ─────────────────────────────

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
    # Widening skew: ask = FV + HS + skew (ask widens AWAY from FV when long).
    # This ensures ask is always above FV+HS — never selling below fair value.
    # Tight spread (HS=3) keeps us inside market bots for more fills.

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

        # Widening skew: both quotes widen away from FV when position is non-zero.
        # bid always below FV, ask always above FV.
        my_bid = fair_value - ACO_HALF_SPREAD - skew
        my_ask = fair_value + ACO_HALF_SPREAD + skew  # widening: +skew, not -skew

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
