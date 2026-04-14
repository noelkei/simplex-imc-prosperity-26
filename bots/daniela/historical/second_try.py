from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle
import numpy as np

class Trader:

    # Position limits per product
    POSITION_LIMITS = {
        "ASH_COATED_OSMIUM": 80,
        "INTARIAN_PEPPER_ROOT": 80,
    }

    # Fair value for Osmium (mean-reverting)
    OSMIUM_FAIR = 10000

    def run(self, state: TradingState):
        result = {}
        trader_data = ""

        # ── INTARIAN_PEPPER_ROOT ──────────────────────────────────────────
        # Trending UP ~1000 XIRECS per day. Strategy: always hold max LONG.
        if "INTARIAN_PEPPER_ROOT" in state.order_depths:
            orders: List[Order] = []
            od: OrderDepth = state.order_depths["INTARIAN_PEPPER_ROOT"]
            pos = state.position.get("INTARIAN_PEPPER_ROOT", 0)
            limit = self.POSITION_LIMITS["INTARIAN_PEPPER_ROOT"]
            capacity = limit - pos  # how much more we can buy

            # Buy every available ask level to fill our long as fast as possible
            if capacity > 0 and od.sell_orders:
                for ask_price in sorted(od.sell_orders.keys()):
                    if capacity <= 0:
                        break
                    ask_vol = -od.sell_orders[ask_price]  # sell_orders stored as negative
                    qty = min(ask_vol, capacity)
                    orders.append(Order("INTARIAN_PEPPER_ROOT", ask_price, qty))
                    capacity -= qty

            # If still not at limit, place a resting buy just above best bid
            if capacity > 0 and od.buy_orders:
                best_bid = max(od.buy_orders.keys())
                orders.append(Order("INTARIAN_PEPPER_ROOT", best_bid + 1, capacity))

            result["INTARIAN_PEPPER_ROOT"] = orders

        # ── ASH_COATED_OSMIUM ────────────────────────────────────────────
        # Mean-reverting tightly around 10000. Strategy: market make + mean reversion.
        if "ASH_COATED_OSMIUM" in state.order_depths:
            orders: List[Order] = []
            od: OrderDepth = state.order_depths["ASH_COATED_OSMIUM"]
            pos = state.position.get("ASH_COATED_OSMIUM", 0)
            limit = self.POSITION_LIMITS["ASH_COATED_OSMIUM"]
            fair = self.OSMIUM_FAIR

            # --- Take liquidity: buy underpriced, sell overpriced ---
            buy_capacity = limit - pos
            sell_capacity = limit + pos  # how many we can sell/short

            if od.sell_orders and buy_capacity > 0:
                for ask_price in sorted(od.sell_orders.keys()):
                    if ask_price < fair:  # underpriced — take it
                        if buy_capacity <= 0:
                            break
                        ask_vol = -od.sell_orders[ask_price]
                        qty = min(ask_vol, buy_capacity)
                        orders.append(Order("ASH_COATED_OSMIUM", ask_price, qty))
                        buy_capacity -= qty

            if od.buy_orders and sell_capacity > 0:
                for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                    if bid_price > fair:  # overpriced — sell it
                        if sell_capacity <= 0:
                            break
                        bid_vol = od.buy_orders[bid_price]
                        qty = min(bid_vol, sell_capacity)
                        orders.append(Order("ASH_COATED_OSMIUM", bid_price, -qty))
                        sell_capacity -= qty

            # --- Passive market making around fair value ---
            # Quote bid at fair-1, ask at fair+1 with remaining capacity
            mm_buy_qty = buy_capacity
            mm_sell_qty = sell_capacity

            if mm_buy_qty > 0:
                orders.append(Order("ASH_COATED_OSMIUM", fair - 1, mm_buy_qty))
            if mm_sell_qty > 0:
                orders.append(Order("ASH_COATED_OSMIUM", fair + 1, -mm_sell_qty))

            result["ASH_COATED_OSMIUM"] = orders

        return result, 0, trader_data
