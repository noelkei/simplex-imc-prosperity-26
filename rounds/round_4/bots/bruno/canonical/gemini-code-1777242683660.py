"""
Bot ID: P4-Frankfurt-Hybrid
Combina la estructura modular exacta de FrankfurtHedgehogs (Prosperity 3) 
con los activos y la lógica Delta-1 de Prosperity 4 (Round 3).
"""

import json
import math
from statistics import NormalDist
from datamodel import OrderDepth, TradingState, Order

_N = NormalDist()

# --- CONFIGURACIÓN DE ACTIVOS PROSPERITY 4 ---
DELTA1_SYMBOLS = ['HYDROGEL_PACK']
OPTION_UNDERLYING_SYMBOL = 'VELVETFRUIT_EXTRACT'

# Mapeo exacto de Vouchers (Opciones) a sus Strikes
OPTIONS = {
    'VEV_4000': 4000,
    'VEV_4500': 4500,
    'VEV_5000': 5000,
    'VEV_5100': 5100,
    'VEV_5200': 5200,
    'VEV_5300': 5300,
    'VEV_5400': 5400,
    'VEV_5500': 5500,
    'VEV_6000': 6000,
    'VEV_6500': 6500
}

# Límites de posición (ajustados a Prosperity 4)
POS_LIMITS = {
    'HYDROGEL_PACK': 250,
    'VELVETFRUIT_EXTRACT': 250,
}
for opt in OPTIONS.keys():
    POS_LIMITS[opt] = 20  # Ajustar a tu límite real de vouchers

# --- UTILIDADES GENERALES ---
def get_mid_price(order_depth: OrderDepth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    return (best_bid + best_ask) / 2.0


# --- CLASE EXACTA DE PROSPERITY 3 ADAPTADA ---
class OptionTrader:
    """
    Réplica exacta del OptionTrader de FrankfurtHedgehogs.
    Calcula Black-Scholes usando NormalDist y provee liquidez en las opciones.
    """
    def __init__(self, state: TradingState, prints: dict, new_trader_data: dict):
        self.state = state
        self.prints = prints
        self.new_trader_data = new_trader_data
        self.orders: dict[str, list[Order]] = {}
        
        # Parámetros del modelo de opciones
        self.r = 0.0  # Tasa libre de riesgo
        self.sigma = 0.15  # Volatilidad Implícita base (necesitarás afinarla)
        
        # Estimar el tiempo a expiración (T)
        TICKS_PER_DAY = 1000000.0
        TOTAL_DAYS = 3.0
        current_day = state.timestamp // TICKS_PER_DAY
        remaining_ticks = TICKS_PER_DAY - (state.timestamp % TICKS_PER_DAY)
        days_left = (TOTAL_DAYS - 1 - current_day) + (remaining_ticks / TICKS_PER_DAY)
        self.T = max(days_left / 252.0, 1e-6)

        self.strategy()

    def bs_call_price(self, S, K, T, r, sigma):
        """Fórmula Black-Scholes para opciones Call (como en Frankfurt)"""
        if T <= 0 or sigma <= 0 or S <= 0:
            return max(0.0, S - K)
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        call_price = S * _N.cdf(d1) - K * math.exp(-r * T) * _N.cdf(d2)
        return call_price

    def strategy(self):
        # 1. Obtener precio del subyacente
        underlying_depth = self.state.order_depths.get(OPTION_UNDERLYING_SYMBOL)
        if not underlying_depth:
            return
            
        S = get_mid_price(underlying_depth)
        if S is None:
            return

        # 2. Iterar sobre todos los Vouchers
        for option_symbol, strike in OPTIONS.items():
            if option_symbol not in self.state.order_depths:
                continue
                
            depth = self.state.order_depths[option_symbol]
            position = self.state.position.get(option_symbol, 0)
            limit = POS_LIMITS.get(option_symbol, 20)
            
            # Calcular Fair Value
            fair_value = self.bs_call_price(S, strike, self.T, self.r, self.sigma)
            
            # Margen y Skewing (Como en el OptionTrader original)
            edge = 1.5  # Spread mínimo deseado
            inventory_skew = (position / limit) * 2.0
            
            bid_px = int(math.floor(fair_value - edge - inventory_skew))
            ask_px = int(math.ceil(fair_value + edge - inventory_skew))
            
            buy_qty = limit - position
            sell_qty = -limit - position
            
            orders = []
            
            # Arbitraje (Sniping)
            best_ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
            best_bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
            
            if best_ask and best_ask < fair_value - edge and buy_qty > 0:
                take_qty = min(buy_qty, depth.sell_orders[best_ask])
                orders.append(Order(option_symbol, best_ask, take_qty))
                buy_qty -= take_qty
                
            if best_bid and best_bid > fair_value + edge and sell_qty < 0:
                take_qty = max(sell_qty, -depth.buy_orders[best_bid])
                orders.append(Order(option_symbol, best_bid, -take_qty))
                sell_qty += take_qty

            # Cotización Pasiva
            if buy_qty > 0:
                orders.append(Order(option_symbol, bid_px, buy_qty))
            if sell_qty < 0:
                orders.append(Order(option_symbol, ask_px, sell_qty))
                
            self.orders[option_symbol] = orders

    def get_orders(self):
        return self.orders


class Delta1Trader:
    """
    Tu lógica de la Ronda 3 (candidate_w5_04_delta1_kalman_fallback.py)
    encapsulada en una clase modular para mantener el estilo Frankfurt.
    """
    def __init__(self, state: TradingState, prints: dict, new_trader_data: dict, symbol: str):
        self.state = state
        self.prints = prints
        self.new_trader_data = new_trader_data
        self.symbol = symbol
        self.orders: dict[str, list[Order]] = {}
        
        self.strategy()
        
    def strategy(self):
        depth = self.state.order_depths.get(self.symbol)
        if not depth:
            return
            
        # AQUÍ VA TU LÓGICA DE KALMAN FILTER PARA HYDROGEL Y VELVETFRUIT
        # (He dejado un market maker simple como placeholder, debes insertar tu lógica)
        
        mid = get_mid_price(depth)
        if mid is None: return
        
        pos = self.state.position.get(self.symbol, 0)
        limit = POS_LIMITS.get(self.symbol, 250)
        
        bid_px = int(math.floor(mid - 1))
        ask_px = int(math.ceil(mid + 1))
        
        orders = []
        if limit - pos > 0:
            orders.append(Order(self.symbol, bid_px, limit - pos))
        if -limit - pos < 0:
            orders.append(Order(self.symbol, ask_px, -limit - pos))
            
        self.orders[self.symbol] = orders

    def get_orders(self):
        return self.orders


# --- CONTROLADOR PRINCIPAL ---
class Trader:
    def run(self, state: TradingState):
        result: dict[str, list[Order]] = {}
        new_trader_data = {}
        
        prints = {
            "GENERAL": {
                "TIMESTAMP": state.timestamp,
                "POSITIONS": state.position
            },
        }

        def export(prints):
            try: print(json.dumps(prints))
            except: pass

        # 1. Ejecutar el OptionTrader para el subyacente y los vouchers
        try:
            opt_trader = OptionTrader(state, prints, new_trader_data)
            result.update(opt_trader.get_orders())
        except Exception as e:
            pass # Añadir print(e) para debug

        # 2. Ejecutar tu lógica Delta-1 (Kalman) para el resto de productos
        for symbol in DELTA1_SYMBOLS + [OPTION_UNDERLYING_SYMBOL]:
            if symbol in state.order_depths:
                try:
                    delta1_trader = Delta1Trader(state, prints, new_trader_data, symbol)
                    
                    # Evitar sobreescribir órdenes del subyacente si OptionTrader ya hizo delta hedging
                    if symbol not in result:
                        result.update(delta1_trader.get_orders())
                except:
                    pass

        export(prints)
        
        # Serializar el nuevo estado si usaste Kalman en Delta1Trader
        trader_data_out = json.dumps(new_trader_data)
        
        return result, 0, trader_data_out