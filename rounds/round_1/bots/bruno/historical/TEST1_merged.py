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
        order_depth: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "ASH_COATED_OSMIUM"
        fair_value = 10000
        spread = 6        # cotizamos fair_value ± 4  →  9996 / 10004
        
        # Aumenta el spread si la posición es extrema para reducir inventario
        pos_ratio = abs(position) / pos_limit  # 0..1

        bid_offset = spread + int(pos_ratio * 2)   # spread más ancho si largo
        ask_offset = spread + int(pos_ratio * 2)   # spread más ancho si corto

        # Si estamos muy largos, bajamos el bid (compramos menos agresivo)
        # Si estamos muy cortos, subimos el ask (vendemos menos agresivo)
        if position > 0:
            bid_offset += 2   # menos ganas de comprar más
        elif position < 0:
            ask_offset += 2   # menos ganas de vender más

        my_bid = fair_value - bid_offset
        my_ask = fair_value + ask_offset

        # ── Tomar liquidez si hay precios mejores que el fair value ──────────
        # Comprar si hay alguien vendiendo por debajo de fair_value
        for ask_price, ask_vol in sorted(order_depth.sell_orders.items()):
            if ask_price < fair_value:
                buy_qty = min(-ask_vol, pos_limit - position)
                if buy_qty > 0:
                    orders.append(Order(product, ask_price, buy_qty))
                    position += buy_qty

        # Vender si hay alguien comprando por encima de fair_value
        for bid_price, bid_vol in sorted(order_depth.buy_orders.items(), reverse=True):
            if bid_price > fair_value:
                sell_qty = min(bid_vol, pos_limit + position)
                if sell_qty > 0:
                    orders.append(Order(product, bid_price, -sell_qty))
                    position -= sell_qty

        # ── Poner órdenes pasivas (market making) ────────────────────────────
        buy_capacity  = pos_limit - position
        sell_capacity = pos_limit + position

        if buy_capacity > 0:
            orders.append(Order(product, my_bid, buy_capacity))

        if sell_capacity > 0:
            orders.append(Order(product, my_ask, -sell_capacity))

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