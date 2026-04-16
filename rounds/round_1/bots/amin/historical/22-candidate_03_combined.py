"""
IMC Prosperity 4 - Round 1
candidate_03_combined (v3 - synthesized)

Strategy synthesis:
  Sources consulted:
    - rounds/round_1/workspace/04_strategy_specs/spec_candidate_01_ipr_drift_mm.md
    - rounds/round_1/workspace/04_strategy_specs/spec_candidate_02_aco_fixed_fv_mm.md
    - rounds/round_1/workspace/04_strategy_specs/spec_candidate_03_combined.md
    - rounds/round_1/bots/bruno/canonical/new_bot.py  (baseline P&L 9,419)
    - rounds/round_1/workspace/01_eda/eda_round_1.md

  IPR — directional max-long (from bruno/new_bot.py, confirmed by EDA):
    Drift = +1000/day (+0.001/tick).  With pos_limit=80, holding +80 captures
    ~80,000 units of drift per day, far exceeding what spread-based market-making
    could achieve.  Strategy: sweep all available asks, then post a passive bid
    one above best_bid to fill remaining capacity.

  ACO — dual market-maker with inventory skew (synthesized):
    FV = 10000 (EDA-confirmed: 94.4% of non-zero mid_price within +-10 of 10000;
    trade median = 10000).
    Layer 1 (aggressive): take liquidity crossing FV — buy anything below FV,
      sell anything above FV.  Skew adjusts effective FV via position-weighted
      offset to encourage mean-reversion of inventory.
    Layer 2 (passive): post limit bid at (FV - HALF_SPREAD - skew) and ask at
      (FV + HALF_SPREAD + skew) to collect spread when no aggressive fill available.
    SKEW_FACTOR=3 (tuned in bruno baseline; reduces inventory swings vs =2).
    ACO_HALF_SPREAD=5 (tighter than spec_02's buffer=8; consistent with bruno
    baseline which already showed positive P&L with this value).

  Failure isolation: each sub-strategy is wrapped in try/except; one crash does
  not prevent the other from returning orders.

  traderData: JSON dict with namespaced keys — no collision risk.
    "IPR_DS": float | None  — day-start price for IPR (not used in directional
              approach but kept for observability/future use)
    "ACO_AC": int           — consecutive ticks where ACO mid_price deviated > threshold

Position limits (wiki-confirmed):
  ASH_COATED_OSMIUM:    +-80
  INTARIAN_PEPPER_ROOT: +-80

Contract:
  run(state) -> (result, conversions, traderData)
  result maps product -> List[Order]
  conversions = 0 (no conversion mechanic in Round 1)
"""

from datamodel import Order, OrderDepth, TradingState
from typing import List, Dict
import json

# ── Constants ───────────────────────────────────────────────────────────────

POSITION_LIMITS: Dict[str, int] = {
    "ASH_COATED_OSMIUM": 80,
    "INTARIAN_PEPPER_ROOT": 80,
}

# IPR — directional max-long
IPR_MAX_POSITION = 75          # 5-unit buffer below hard limit

# ACO — dual market-maker
ACO_FAIR_VALUE      = 10000
ACO_HALF_SPREAD     = 5        # half of mean spread ~16 rounded tight; proven in baseline
ACO_SKEW_FACTOR     = 3        # position-weighted skew; tuned by bruno (raised from 2)
ACO_MAX_POSITION    = 75       # 5-unit buffer below hard limit
ACO_ALERT_THRESHOLD = 30       # deviation from FV that triggers a warning counter
ACO_ALERT_TICKS     = 50       # consecutive ticks above threshold for warning


# ── Trader ──────────────────────────────────────────────────────────────────

class Trader:

    # ── State helpers ────────────────────────────────────────────────────────

    def _load(self, traderData: str) -> dict:
        if not traderData:
            return {}
        try:
            return json.loads(traderData)
        except Exception:
            return {}

    def _save(self, data: dict) -> str:
        return json.dumps(data, separators=(",", ":"))

    # ── IPR sub-strategy ─────────────────────────────────────────────────────

    def _trade_ipr(
        self,
        od: OrderDepth,
        position: int,
        pos_limit: int,
        sd: dict,
    ) -> List[Order]:
        """
        Directional max-long: sweep all available asks then post a passive bid
        for remaining capacity.  Captures +1000/day drift.
        """
        orders: List[Order] = []
        product = "INTARIAN_PEPPER_ROOT"

        # Capacity check
        capacity = min(IPR_MAX_POSITION, pos_limit) - position
        if capacity <= 0:
            return orders

        # Layer 1: take all available asks
        for ask_price in sorted(od.sell_orders):
            if capacity <= 0:
                break
            vol = min(-od.sell_orders[ask_price], capacity)
            if vol > 0:
                orders.append(Order(product, ask_price, vol))
                capacity -= vol

        # Layer 2: passive bid one tick above best bid to fill remaining
        if capacity > 0 and od.buy_orders:
            best_bid = max(od.buy_orders)
            orders.append(Order(product, best_bid + 1, capacity))

        return orders

    # ── ACO sub-strategy ─────────────────────────────────────────────────────

    def _trade_aco(
        self,
        od: OrderDepth,
        position: int,
        pos_limit: int,
        sd: dict,
        timestamp: int,
    ) -> List[Order]:
        """
        Dual market-maker around FV=10000 with inventory skew.
        Layer 1 (aggressive): take liquidity crossing FV.
        Layer 2 (passive): post limit orders at FV +- HALF_SPREAD after skew.
        """
        orders: List[Order] = []
        product = "ASH_COATED_OSMIUM"

        if not od.buy_orders and not od.sell_orders:
            return orders

        # Derive mid_price for alert counter (best effort)
        mid = 0
        if od.buy_orders and od.sell_orders:
            mid = (max(od.buy_orders) + min(od.sell_orders)) / 2
        elif od.buy_orders:
            mid = max(od.buy_orders)
        elif od.sell_orders:
            mid = min(od.sell_orders)

        # ACO alert counter (observability — does not change FV)
        aco_ac = int(sd.get("ACO_AC", 0))
        if mid > 0 and abs(mid - ACO_FAIR_VALUE) > ACO_ALERT_THRESHOLD:
            aco_ac += 1
        else:
            aco_ac = 0
        sd["ACO_AC"] = aco_ac
        # (Log would go here in a debug run; omitted for clean production output)

        # Inventory skew: positive pos -> push quotes down (encourage selling)
        skew = round((position / pos_limit) * ACO_SKEW_FACTOR)
        my_bid = ACO_FAIR_VALUE - ACO_HALF_SPREAD - skew
        my_ask = ACO_FAIR_VALUE + ACO_HALF_SPREAD + skew

        buy_cap  = min(ACO_MAX_POSITION, pos_limit) - position
        sell_cap = min(ACO_MAX_POSITION, pos_limit) + position
        cur_pos  = position  # local copy for intra-tick capacity tracking

        # Layer 1a: take asks below FV (aggressive buy)
        for ask_price in sorted(od.sell_orders):
            if ask_price >= ACO_FAIR_VALUE:
                break
            if buy_cap <= 0:
                break
            vol = min(-od.sell_orders[ask_price], buy_cap)
            if vol > 0:
                orders.append(Order(product, ask_price, vol))
                buy_cap -= vol
                cur_pos += vol

        # Layer 1b: take bids above FV (aggressive sell)
        for bid_price in sorted(od.buy_orders, reverse=True):
            if bid_price <= ACO_FAIR_VALUE:
                break
            if sell_cap <= 0:
                break
            vol = min(od.buy_orders[bid_price], sell_cap)
            if vol > 0:
                orders.append(Order(product, bid_price, -vol))
                sell_cap -= vol
                cur_pos  -= vol

        # Layer 2: passive limit orders for remaining capacity
        if buy_cap > 0:
            orders.append(Order(product, my_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── Main entry point ─────────────────────────────────────────────────────

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result: Dict[str, List[Order]] = {}

        for product, od in state.order_depths.items():
            position  = state.position.get(product, 0)
            pos_limit = POSITION_LIMITS.get(product, 80)
            orders: List[Order] = []

            try:
                if product == "INTARIAN_PEPPER_ROOT":
                    orders = self._trade_ipr(od, position, pos_limit, sd)
                elif product == "ASH_COATED_OSMIUM":
                    orders = self._trade_aco(
                        od, position, pos_limit, sd, state.timestamp
                    )
            except Exception:
                # Failure isolation: one sub-strategy crash must not stop the other.
                orders = []

            result[product] = orders

        return result, 0, self._save(sd)