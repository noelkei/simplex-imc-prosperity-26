"""
IMC Prosperity – Round 1
========================
Estrategias basadas en el EDA:

ASH_COATED_OSMIUM
  → Market-making alrededor de fair value ~10000 (sin drift).
  → Imbalance L1 (corr=0.38) skewea las cotizaciones.

INTARIAN_PEPPER_ROOT
  → Fair value determinista: base + 0.1002 * timestamp
  → Tomar liquidez agresivamente cuando precio << o >> fair value.
  → Imbalance L1 skewea tamaño de orden pasiva.
"""

from datamodel import OrderDepth, TradingState, Order
from typing import List, Dict
import json


# ── Constantes ────────────────────────────────────────────────────────────────

POSITION_LIMITS = {
    "ASH_COATED_OSMIUM":    20,
    "INTARIAN_PEPPER_ROOT": 20,
}

# INTARIAN: fair_value(t) = PEPPER_BASE + PEPPER_SLOPE * t
# Slope medido exactamente del EDA: 0.1002 / tick
# Base: mid_price en t=0 del día -2 ≈ 10000 - 0.1002 * (-2*1_000_000)
# Pero como cada día resetea el timestamp a 0, usamos día + timestamp juntos.
# La fórmula más limpia: fair(t) = mid_día_inicio + 0.1002 * t_within_day
# Como el slope es idéntico los 3 días lo que varía es el intercept por día.
# Lo estimamos en el primer tick del día con la primera observación del libro.
PEPPER_SLOPE = 0.1002          # unidades de precio por tick

# ASH: fair value estable, estimado como media del mid price histórico
ASH_FAIR_VALUE = 10_000

# Spread que ofrecemos (en unidades de precio)
ASH_SPREAD    = 4     # cotizamos fair ± 4 → 9996 / 10004  (spread real del mercado ~16)
PEPPER_SPREAD = 3     # cotizamos fair ± 3  (spread real del mercado ~13)

# Umbral de imbalance para skewing de quotes
IMBALANCE_SKEW_THRESHOLD = 0.3   # |imbalance| > 0.3 → skewamos
IMBALANCE_SKEW_TICKS     = 2     # desplazamos la cita este número de ticks

# Umbral de edge para tomar liquidez agresivamente
PEPPER_AGGRESSIVE_EDGE = 5   # si precio_mercado < fair - 5 → compramos agresivo
ASH_AGGRESSIVE_EDGE    = 6   # ídem para ASH


# ── Trader ────────────────────────────────────────────────────────────────────

class Trader:

    # ── Persistencia entre ticks ──────────────────────────────────────────────

    def _load(self, raw: str) -> dict:
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except Exception:
            return {}

    def _save(self, data: dict) -> str:
        return json.dumps(data)

    # ── Helpers de libro ─────────────────────────────────────────────────────

    def _best_bid(self, od: OrderDepth):
        return max(od.buy_orders) if od.buy_orders else None

    def _best_ask(self, od: OrderDepth):
        return min(od.sell_orders) if od.sell_orders else None

    def _mid(self, od: OrderDepth):
        bb, ba = self._best_bid(od), self._best_ask(od)
        if bb is not None and ba is not None:
            return (bb + ba) / 2
        return None

    def _imbalance(self, od: OrderDepth) -> float:
        """
        Order imbalance L1: (bid_vol - ask_vol) / (bid_vol + ask_vol)
        Rango: -1 (presión vendedora) a +1 (presión compradora)
        Correlación con ret+1 ~ +0.38 según EDA.
        """
        bb = self._best_bid(od)
        ba = self._best_ask(od)
        if bb is None or ba is None:
            return 0.0
        bv = od.buy_orders.get(bb, 0)
        av = abs(od.sell_orders.get(ba, 0))
        total = bv + av
        if total == 0:
            return 0.0
        return (bv - av) / total

    # ── ASH_COATED_OSMIUM: market-making estático ─────────────────────────────

    def _trade_ash(
        self,
        od: OrderDepth,
        position: int,
        limit: int,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "ASH_COATED_OSMIUM"
        fair = ASH_FAIR_VALUE

        imb = self._imbalance(od)

        # Skewing: si hay presión compradora subimos ambas cotizaciones un poco
        # (vendemos más caro, compramos más caro también → seguimos el flujo)
        skew = 0
        if imb > IMBALANCE_SKEW_THRESHOLD:
            skew = +IMBALANCE_SKEW_TICKS    # mercado quiere comprar → subimos
        elif imb < -IMBALANCE_SKEW_THRESHOLD:
            skew = -IMBALANCE_SKEW_TICKS    # mercado quiere vender → bajamos

        # Ajuste adicional por inventario: si estamos muy largos, bajamos bid
        # (somos menos agresivos comprando) y viceversa
        inv_skew = -round((position / limit) * 2)   # rango ±2

        my_bid = fair - ASH_SPREAD + skew + inv_skew
        my_ask = fair + ASH_SPREAD + skew + inv_skew

        # ── 1. Tomar liquidez si hay precios con edge claro ──────────────────
        for ask_px, ask_vol in sorted(od.sell_orders.items()):
            if ask_px < fair - ASH_AGGRESSIVE_EDGE:
                qty = min(-ask_vol, limit - position)
                if qty > 0:
                    orders.append(Order(product, ask_px, qty))
                    position += qty

        for bid_px in sorted(od.buy_orders, reverse=True):
            if bid_px > fair + ASH_AGGRESSIVE_EDGE:
                qty = min(od.buy_orders[bid_px], limit + position)
                if qty > 0:
                    orders.append(Order(product, bid_px, -qty))
                    position -= qty

        # ── 2. Órdenes pasivas (market-making) ───────────────────────────────
        buy_cap  = limit - position
        sell_cap = limit + position

        if buy_cap > 0 and my_bid > 0:
            orders.append(Order(product, my_bid, buy_cap))

        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── INTARIAN_PEPPER_ROOT: fair-value tracking ─────────────────────────────

    def _pepper_fair_value(self, timestamp: int, state_data: dict, od: OrderDepth) -> float:
        """
        Fair value = intercept_del_día + PEPPER_SLOPE * timestamp
        El intercept lo estimamos en el primer tick del día usando el mid del libro.
        """
        key = "pepper_intercept"
        if key not in state_data:
            mid = self._mid(od)
            if mid is None:
                # Si no hay libro aún, inicializamos con un valor razonable
                mid = 10_000
            # intercept = mid_observado - slope * timestamp_actual
            state_data[key] = mid - PEPPER_SLOPE * timestamp

        return state_data[key] + PEPPER_SLOPE * timestamp

    def _trade_pepper(
        self,
        od: OrderDepth,
        position: int,
        limit: int,
        timestamp: int,
        state_data: dict,
    ) -> List[Order]:
        orders: List[Order] = []
        product = "INTARIAN_PEPPER_ROOT"

        fair = self._pepper_fair_value(timestamp, state_data, od)
        imb  = self._imbalance(od)

        # Skewing por imbalance (misma lógica que ASH)
        skew = 0
        if imb > IMBALANCE_SKEW_THRESHOLD:
            skew = +IMBALANCE_SKEW_TICKS
        elif imb < -IMBALANCE_SKEW_THRESHOLD:
            skew = -IMBALANCE_SKEW_TICKS

        # Ajuste por inventario
        inv_skew = -round((position / limit) * 2)

        my_bid = round(fair) - PEPPER_SPREAD + skew + inv_skew
        my_ask = round(fair) + PEPPER_SPREAD + skew + inv_skew

        # ── 1. Tomar liquidez agresiva con edge grande ───────────────────────
        # Compramos si el ask está significativamente por debajo del fair value
        for ask_px, ask_vol in sorted(od.sell_orders.items()):
            if ask_px < fair - PEPPER_AGGRESSIVE_EDGE:
                qty = min(-ask_vol, limit - position)
                if qty > 0:
                    orders.append(Order(product, ask_px, qty))
                    position += qty

        # Vendemos si el bid está significativamente por encima del fair value
        for bid_px in sorted(od.buy_orders, reverse=True):
            if bid_px > fair + PEPPER_AGGRESSIVE_EDGE:
                qty = min(od.buy_orders[bid_px], limit + position)
                if qty > 0:
                    orders.append(Order(product, bid_px, -qty))
                    position -= qty

        # ── 2. Órdenes pasivas alrededor del fair value ──────────────────────
        buy_cap  = limit - position
        sell_cap = limit + position

        if buy_cap > 0 and my_bid > 0:
            orders.append(Order(product, my_bid, buy_cap))

        if sell_cap > 0:
            orders.append(Order(product, my_ask, -sell_cap))

        return orders

    # ── Método principal ──────────────────────────────────────────────────────

    def run(self, state: TradingState):
        state_data = self._load(state.traderData)
        result: Dict[str, List[Order]] = {}

        for product, od in state.order_depths.items():
            position = state.position.get(product, 0)
            limit    = POSITION_LIMITS.get(product, 20)

            if product == "ASH_COATED_OSMIUM":
                orders = self._trade_ash(od, position, limit)

            elif product == "INTARIAN_PEPPER_ROOT":
                orders = self._trade_pepper(od, position, limit, state.timestamp, state_data)

            else:
                orders = []

            result[product] = orders

        traderData  = self._save(state_data)
        conversions = 0
        return result, conversions, traderData