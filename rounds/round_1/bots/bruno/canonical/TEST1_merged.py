"""
IMC Prosperity 4 – Round 1
Estrategia adaptada: 
- ASH_COATED_OSMIUM: Market-Making dinámico basado en inventario.
- INTARIAN_PEPPER_ROOT: Estrategia direccional - Comprar hasta el límite agresivamente.
"""

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import json
import math

# ── Límites de posición (Round 1) actualizados a 80 ────────────────────────
POSITION_LIMITS = {
    "ASH_COATED_OSMIUM": 80,
    "INTARIAN_PEPPER_ROOT": 80,
}

# ASH_COATED_OSMIUM
ACO_FAIR_VALUE   = 10000   # fixed fair value
ACO_HALF_SPREAD  = 5       # ticks either side of fair value for passive quotes
ACO_SKEW_FACTOR  = 2       # max skew ticks at full position limit

class Trader:

    # ── Estado persistente entre ticks ────────────────────────────────────────
    def _load_state(self, traderData: str) -> dict:
        if not traderData:
            return {}
        try:
            return json.loads(traderData)
        except Exception:
            return {}

    def _save_state(self, state: dict) -> str:
        return json.dumps(state)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _best_bid(self, order_depth: OrderDepth):
        if order_depth.buy_orders:
            return max(order_depth.buy_orders.keys())
        return None

    def _best_ask(self, order_depth: OrderDepth):
        if order_depth.sell_orders:
            return min(order_depth.sell_orders.keys())
        return None

    def _mid_price(self, order_depth: OrderDepth):
        bb = self._best_bid(order_depth)
        ba = self._best_ask(order_depth)
        if bb is not None and ba is not None:
            return (bb + ba) / 2
        return None

    # ── ASH COATED OSMIUM: Market-Making estricto alrededor de 10000 ─────────────────
    def _trade_ash(
        self,
        od: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "ASH_COATED_OSMIUM"

        if not od.buy_orders and not od.sell_orders:
            return orders  # empty book — no signal

        fair_value = ACO_FAIR_VALUE

        # Position skew
        skew = round((position / pos_limit) * ACO_SKEW_FACTOR)

        my_bid = fair_value - ACO_HALF_SPREAD - skew
        my_ask = fair_value + ACO_HALF_SPREAD + skew

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

        # Passive market-making quotes
        if buy_cap > 0:
            orders.append(Order(product, my_bid, buy_cap))
        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── Método original conservado por si se necesita ────────────────────────
    def _update_ema(self, prev_ema: float, new_price: float, alpha: float = 0.15) -> float:
        """EMA simple. alpha bajo = más suave = más lenta."""
        return alpha * new_price + (1 - alpha) * prev_ema

    # ── INTARIAN_PEPPER_ROOT: Estrategia Direccional Agresiva (Hold Max Long) ──
    def _trade_root(
        self,
        order_depth: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "INTARIAN_PEPPER_ROOT"
        
        capacity = pos_limit - position  # how much more we can buy

        # Buy every available ask level to fill our long as fast as possible
        if capacity > 0 and order_depth.sell_orders:
            for ask_price in sorted(order_depth.sell_orders.keys()):
                if capacity <= 0:
                    break
                ask_vol = -order_depth.sell_orders[ask_price]  # sell_orders stored as negative
                qty = min(ask_vol, capacity)
                orders.append(Order(product, ask_price, qty))
                capacity -= qty

        # If still not at limit, place a resting buy just above best bid
        if capacity > 0 and order_depth.buy_orders:
            best_bid = max(order_depth.buy_orders.keys())
            orders.append(Order(product, best_bid + 1, capacity))

        return orders

    # ── Método principal ──────────────────────────────────────────────────────
    def run(self, state: TradingState):
        print("=== Timestamp:", state.timestamp, "===")
        print("Positions:", state.position)

        state_data = self._load_state(state.traderData)
        result: Dict[str, List[Order]] = {}

        for product, order_depth in state.order_depths.items():
            position = state.position.get(product, 0)
            # Usar los límites del diccionario de arriba
            pos_limit = POSITION_LIMITS.get(product, 80)

            if product == "INTARIAN_PEPPER_ROOT":
                orders = self._trade_root(order_depth, position, pos_limit)

            elif product == "ASH_COATED_OSMIUM":
                orders = self._trade_ash(order_depth, position, pos_limit)
                
            if orders:
                print(f"  {product}: {orders}")

            result[product] = orders

        traderData = self._save_state(state_data)
        conversions = 0
        return result, conversions, traderData