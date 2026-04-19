"""
Round 2 — Simplex v1
Products: INTARIAN_PEPPER_ROOT (drift capture) + ASH_COATED_OSMIUM (mean-reversion MM)
Market Access Fee bid included.
Uploadable standalone Trader file. Uses only datamodel + json (standard library).
"""
from datamodel import Order, TradingState
import json
import math

# ─── Constants ───────────────────────────────────────────────────────
IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
POSITION_LIMIT = 80

# IPR drift rate: exactly 0.001 per timestamp unit (from EDA regression)
IPR_DRIFT = 0.001

# ACO EMA smoothing factor (higher = more responsive)
ACO_EMA_ALPHA = 0.15

# How much above FV we're willing to buy IPR (we buy aggressively because drift dominates)
IPR_TAKE_MARGIN = 5

# ACO: edge needed to take liquidity (must exceed this above/below FV)
ACO_TAKE_EDGE = 1

# ACO: passive quote offset from FV
ACO_QUOTE_OFFSET = 3

# Market Access Fee bid
MAF_BID = 150


class Trader:
    """Prosperity Round 2 Trader."""

    def bid(self):
        return MAF_BID

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # ── Restore persisted state ──────────────────────────────────
        memory = {}
        if state.traderData:
            try:
                memory = json.loads(state.traderData)
            except Exception:
                memory = {}

        # ── IPR: Drift-Capture Strategy ──────────────────────────────
        if IPR in state.order_depths:
            od = state.order_depths[IPR]
            position = state.position.get(IPR, 0)
            orders = []

            best_bid = max(od.buy_orders.keys()) if od.buy_orders else None
            best_ask = min(od.sell_orders.keys()) if od.sell_orders else None

            # Estimate the day's base price on first observation
            if "ipr_base" not in memory and best_bid is not None and best_ask is not None:
                mid = (best_bid + best_ask) / 2
                memory["ipr_base"] = mid - IPR_DRIFT * state.timestamp

            ipr_base = memory.get("ipr_base", 12000)
            fair_value = ipr_base + IPR_DRIFT * state.timestamp

            # ── Buy side: get long up to POSITION_LIMIT ──
            buy_budget = POSITION_LIMIT - position  # max additional units we can buy

            if buy_budget > 0:
                remaining = buy_budget

                # 1) Take sell orders that are at or below FV + margin
                for ask_price in sorted(od.sell_orders.keys()):
                    if remaining <= 0:
                        break
                    if ask_price <= fair_value + IPR_TAKE_MARGIN:
                        available = -od.sell_orders[ask_price]  # sell volumes are negative
                        qty = min(remaining, available)
                        if qty > 0:
                            orders.append(Order(IPR, ask_price, qty))
                            remaining -= qty

                # 2) Place passive bid at FV (rounded down) for any remaining
                if remaining > 0:
                    bid_price = int(math.floor(fair_value))
                    orders.append(Order(IPR, bid_price, remaining))

            # ── Sell side: only sell if extremely above FV (capture spikes) ──
            # We generally want to stay long, so only sell on extreme overshoot
            sell_budget = POSITION_LIMIT + position  # max sell volume
            if sell_budget > 0 and position > 0:
                for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                    if bid_price > fair_value + 15:  # only sell way above FV
                        available = od.buy_orders[bid_price]
                        qty = min(sell_budget, available, position)
                        if qty > 0:
                            orders.append(Order(IPR, bid_price, -qty))
                            sell_budget -= qty

            result[IPR] = orders

        # ── ACO: Mean-Reversion Market Making ────────────────────────
        if ACO in state.order_depths:
            od = state.order_depths[ACO]
            position = state.position.get(ACO, 0)
            orders = []

            best_bid = max(od.buy_orders.keys()) if od.buy_orders else None
            best_ask = min(od.sell_orders.keys()) if od.sell_orders else None

            if best_bid is not None and best_ask is not None:
                mid = (best_bid + best_ask) / 2
            elif best_bid is not None:
                mid = best_bid
            elif best_ask is not None:
                mid = best_ask
            else:
                mid = memory.get("aco_ema", 10000)

            # Update EMA
            if "aco_ema" not in memory:
                memory["aco_ema"] = mid
            else:
                memory["aco_ema"] = ACO_EMA_ALPHA * mid + (1 - ACO_EMA_ALPHA) * memory["aco_ema"]

            fv = memory["aco_ema"]

            # Inventory skew: shift FV slightly to encourage position reduction
            # If long, lower FV to make us more eager to sell / less eager to buy
            skew = -position * 0.05
            adj_fv = fv + skew

            # ── Take liquidity ──
            buy_budget = POSITION_LIMIT - position
            sell_budget = POSITION_LIMIT + position

            # Buy: take sell orders below adjusted FV - edge
            for ask_price in sorted(od.sell_orders.keys()):
                if buy_budget <= 0:
                    break
                if ask_price < adj_fv - ACO_TAKE_EDGE:
                    available = -od.sell_orders[ask_price]
                    qty = min(buy_budget, available)
                    if qty > 0:
                        orders.append(Order(ACO, ask_price, qty))
                        buy_budget -= qty

            # Sell: take buy orders above adjusted FV + edge
            for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                if sell_budget <= 0:
                    break
                if bid_price > adj_fv + ACO_TAKE_EDGE:
                    available = od.buy_orders[bid_price]
                    qty = min(sell_budget, available)
                    if qty > 0:
                        orders.append(Order(ACO, bid_price, -qty))
                        sell_budget -= qty

            # ── Passive quotes ──
            bid_price = int(math.floor(adj_fv - ACO_QUOTE_OFFSET))
            ask_price = int(math.ceil(adj_fv + ACO_QUOTE_OFFSET))

            if buy_budget > 0:
                orders.append(Order(ACO, bid_price, buy_budget))
            if sell_budget > 0:
                orders.append(Order(ACO, ask_price, -sell_budget))

            result[ACO] = orders

        # ── Persist state ────────────────────────────────────────────
        trader_data = json.dumps(memory)
        return result, conversions, trader_data
