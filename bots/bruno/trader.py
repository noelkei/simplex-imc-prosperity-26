"""
IMC Prosperity 4 – Tutorial Round 0
Estrategia: Market-Making para EMERALDS + Mean-Reversion para TOMATOES

Insights del análisis de datos:
- EMERALDS: fair value = 10000 (siempre). Spread = 9992/10008 → cotizamos 9996/10004
- TOMATOES: precio oscila alrededor de media dinámica (EMA). Mean-reversion.
"""

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import json
import math


# ── Límites de posición (Tutorial 0) ──────────────────────────────────────────
POSITION_LIMITS = {
    "EMERALDS": 20,
    "TOMATOES": 20,
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

    # ── EMERALDS: Market-Making estricto alrededor de 10000 ─────────────────
    def _trade_emeralds(
        self,
        order_depth: OrderDepth,
        position: int,
        pos_limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "EMERALDS"
        fair_value = 10000
        spread = 4          # cotizamos fair_value ± 4  →  9996 / 10004
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

    # ── TOMATOES: Mean-Reversion con EMA dinámica ────────────────────────────
    def _update_ema(self, prev_ema: float, new_price: float, alpha: float = 0.15) -> float:
        """EMA simple. alpha bajo = más suave = más lenta."""
        return alpha * new_price + (1 - alpha) * prev_ema

    def _trade_tomatoes(
        self,
        order_depth: OrderDepth,
        position: int,
        pos_limit: int,
        state_data: dict,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "TOMATOES"

        mid = self._mid_price(order_depth)
        if mid is None:
            return orders

        # Inicializar EMA si es el primer tick
        if "tomato_ema" not in state_data:
            state_data["tomato_ema"] = mid
        ema = self._update_ema(state_data["tomato_ema"], mid, alpha=0.12)
        state_data["tomato_ema"] = ema

        # Umbral para entrar: si el precio se aleja > threshold del EMA
        threshold = 7        # en unidades de precio
        trade_size = 10      # tamaño base de orden
        spread_offset = 2    # offset adicional para nuestras órdenes pasivas

        # Posición actual vs capacidad
        long_capacity  = pos_limit - position
        short_capacity = pos_limit + position

        best_ask = self._best_ask(order_depth)
        best_bid = self._best_bid(order_depth)

        # ── Señal de compra: precio muy por debajo de EMA ────────────────────
        if best_ask is not None and best_ask < ema - threshold and long_capacity > 0:
            qty = min(trade_size, long_capacity)
            orders.append(Order(product, best_ask, qty))
            position += qty
            long_capacity -= qty

        # ── Señal de venta: precio muy por encima de EMA ────────────────────
        if best_bid is not None and best_bid > ema + threshold and short_capacity > 0:
            qty = min(trade_size, short_capacity)
            orders.append(Order(product, best_bid, -qty))
            position -= qty
            short_capacity -= qty

        # ── Market making pasivo alrededor de la EMA ─────────────────────────
        # Solo ponemos órdenes pasivas si la posición no es extrema
        if abs(position) < pos_limit * 0.8:
            passive_bid = int(ema) - spread_offset
            passive_ask = int(ema) + spread_offset

            if long_capacity > 0:
                orders.append(Order(product, passive_bid, min(5, long_capacity)))
            if short_capacity > 0:
                orders.append(Order(product, passive_ask, -min(5, short_capacity)))

        # ── Reducción de inventario: si estamos muy desequilibrados ──────────
        pos_ratio = position / pos_limit
        if pos_ratio > 0.6 and best_bid is not None:
            # Liquidar parte de posición larga agresivamente
            reduce_qty = min(5, pos_limit + position)  # usando short_capacity
            if reduce_qty > 0:
                orders.append(Order(product, best_bid, -reduce_qty))
        elif pos_ratio < -0.6 and best_ask is not None:
            # Liquidar parte de posición corta agresivamente
            reduce_qty = min(5, pos_limit - position)
            if reduce_qty > 0:
                orders.append(Order(product, best_ask, reduce_qty))

        return orders

    # ── Método principal ──────────────────────────────────────────────────────
    def run(self, state: TradingState):
        print("=== Timestamp:", state.timestamp, "===")
        print("Positions:", state.position)

        state_data = self._load_state(state.traderData)
        result: Dict[str, List[Order]] = {}

        for product, order_depth in state.order_depths.items():
            position = state.position.get(product, 0)
            pos_limit = POSITION_LIMITS.get(product, 20)

            if product == "EMERALDS":
                orders = self._trade_emeralds(order_depth, position, pos_limit)

            elif product == "TOMATOES":
                orders = self._trade_tomatoes(order_depth, position, pos_limit, state_data)

            else:
                orders = []

            if orders:
                print(f"  {product}: {orders}")

            result[product] = orders

        traderData = self._save_state(state_data)
        conversions = 0
        return result, conversions, traderData
