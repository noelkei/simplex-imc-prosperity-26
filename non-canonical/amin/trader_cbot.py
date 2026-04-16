from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle
import math

class Trader:

    POSITION_LIMITS = {
        "ASH_COATED_OSMIUM": 80,
        "INTARIAN_PEPPER_ROOT": 80,
    }

    def run(self, state: TradingState):
        result = {}

        # Restore persistent state
        persisted = {}
        if state.traderData and state.traderData != "":
            try:
                persisted = jsonpickle.decode(state.traderData)
            except:
                persisted = {}

        # ── INTARIAN_PEPPER_ROOT ──────────────────────────────────────────
        # Strategy: BUY to max position limit as fast as possible, then hold.
        if "INTARIAN_PEPPER_ROOT" in state.order_depths:
            orders: List[Order] = []
            od: OrderDepth = state.order_depths["INTARIAN_PEPPER_ROOT"]
            pos = state.position.get("INTARIAN_PEPPER_ROOT", 0)
            limit = self.POSITION_LIMITS["INTARIAN_PEPPER_ROOT"]
            capacity = limit - pos

            # Aggressively take ALL sell orders to fill position fast
            if capacity > 0 and od.sell_orders:
                for ask_price in sorted(od.sell_orders.keys()):
                    if capacity <= 0:
                        break
                    ask_vol = -od.sell_orders[ask_price]
                    qty = min(ask_vol, capacity)
                    orders.append(Order("INTARIAN_PEPPER_ROOT", ask_price, qty))
                    capacity -= qty

            # If still room, post aggressive resting buy above best bid
            if capacity > 0:
                if od.buy_orders:
                    best_bid = max(od.buy_orders.keys())
                    # Post at best_bid + 1 to be top of queue
                    orders.append(Order("INTARIAN_PEPPER_ROOT", best_bid + 1, capacity))
                elif od.sell_orders:
                    # No bids but asks exist - post near best ask
                    best_ask = min(od.sell_orders.keys())
                    orders.append(Order("INTARIAN_PEPPER_ROOT", best_ask - 1, capacity))

            result["INTARIAN_PEPPER_ROOT"] = orders

        if "ASH_COATED_OSMIUM" in state.order_depths:
            orders: List[Order] = []
            od: OrderDepth = state.order_depths["ASH_COATED_OSMIUM"]
            pos = state.position.get("ASH_COATED_OSMIUM", 0)
            limit = self.POSITION_LIMITS["ASH_COATED_OSMIUM"]

            # ── Step 1: Compute dynamic fair value ──
            best_bid = max(od.buy_orders.keys()) if od.buy_orders else None
            best_ask = min(od.sell_orders.keys()) if od.sell_orders else None

            ema_fair = persisted.get("osmium_ema", None)

            if best_bid is not None and best_ask is not None:
                current_mid = (best_bid + best_ask) / 2
            elif best_bid is not None:
                current_mid = best_bid + 8
            elif best_ask is not None:
                current_mid = best_ask - 8
            else:
                current_mid = ema_fair if ema_fair else 10000

            alpha = 0.1
            if ema_fair is None:
                ema_fair = current_mid
            else:
                ema_fair = alpha * current_mid + (1 - alpha) * ema_fair

            persisted["osmium_ema"] = ema_fair
            fair = round(ema_fair)

            # ── Step 2: Inventory skewing (Avellaneda-Stoikov inspired) ──
            inventory_ratio = pos / limit  # ranges from -1 to +1
            skew = -round(inventory_ratio * 3)  # up to ±3 skew

            # ── Step 3: Aggressive taking of mispriced orders ──
            buy_capacity = limit - pos
            sell_capacity = limit + pos

            # Take any asks BELOW fair value (buy cheap)
            if od.sell_orders and buy_capacity > 0:
                for ask_price in sorted(od.sell_orders.keys()):
                    if ask_price < fair and buy_capacity > 0:
                        ask_vol = -od.sell_orders[ask_price]
                        qty = min(ask_vol, buy_capacity)
                        orders.append(Order("ASH_COATED_OSMIUM", ask_price, qty))
                        buy_capacity -= qty
                    elif ask_price == fair and buy_capacity > 0 and pos < 0:
                        # At fair value, only take if we need to reduce short position
                        ask_vol = -od.sell_orders[ask_price]
                        qty = min(ask_vol, buy_capacity, abs(pos))
                        if qty > 0:
                            orders.append(Order("ASH_COATED_OSMIUM", ask_price, qty))
                            buy_capacity -= qty

            # Take any bids ABOVE fair value (sell expensive)
            if od.buy_orders and sell_capacity > 0:
                for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                    if bid_price > fair and sell_capacity > 0:
                        bid_vol = od.buy_orders[bid_price]
                        qty = min(bid_vol, sell_capacity)
                        orders.append(Order("ASH_COATED_OSMIUM", bid_price, -qty))
                        sell_capacity -= qty
                    elif bid_price == fair and sell_capacity > 0 and pos > 0:
                        # At fair value, only take if we need to reduce long position
                        bid_vol = od.buy_orders[bid_price]
                        qty = min(bid_vol, sell_capacity, pos)
                        if qty > 0:
                            orders.append(Order("ASH_COATED_OSMIUM", bid_price, -qty))
                            sell_capacity -= qty

            # ── Step 4: Passive market making with skewed quotes ──
            mm_bid_price = fair - 2 + skew
            mm_ask_price = fair + 2 + skew

            if mm_bid_price >= mm_ask_price:
                mm_bid_price = fair - 1 + skew
                mm_ask_price = fair + 1 + skew
            if mm_bid_price >= mm_ask_price:
                mm_bid_price = fair - 1
                mm_ask_price = fair + 1

            if buy_capacity > 0:
                orders.append(Order("ASH_COATED_OSMIUM", mm_bid_price, buy_capacity))
            if sell_capacity > 0:
                orders.append(Order("ASH_COATED_OSMIUM", mm_ask_price, -sell_capacity))

            result["ASH_COATED_OSMIUM"] = orders

        trader_data = jsonpickle.encode(persisted)

        return result, 0, trader_data
