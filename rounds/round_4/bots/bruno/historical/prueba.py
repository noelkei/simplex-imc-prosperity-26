"""
Bot ID: P4-Frankfurt-Safe-Execution
Arquitectura Modular + Volatility Smile + Delta Hedging Activo + Imbalance (FIXED)
Totalmente blindado contra rechazos de órdenes del motor de Prosperity.
"""

import json
import math
from datamodel import OrderDepth, TradingState, Order

# --- CONFIGURACIÓN DE ACTIVOS PROSPERITY 4 ---
DELTA1_SYMBOLS = ['HYDROGEL_PACK']
OPTION_UNDERLYING_SYMBOL = 'VELVETFRUIT_EXTRACT'

OPTIONS = {
    'VEV_4000': 4000, 'VEV_4500': 4500, 'VEV_5000': 5000,
    'VEV_5100': 5100, 'VEV_5200': 5200, 'VEV_5300': 5300,
    'VEV_5400': 5400, 'VEV_5500': 5500, 'VEV_6000': 6000,
    'VEV_6500': 6500
}

# Volatilidad real extraída de los datos de Round 3 (Volatility Smile)
SMILE_IV = {
    4000: 1.667, 4500: 0.828, 5000: 0.572, 5100: 0.534,
    5200: 0.561, 5300: 0.527, 5400: 0.574, 5500: 0.531,
    6000: 0.843, 6500: 1.259
}

POS_LIMITS = {
    'HYDROGEL_PACK': 250,
    'VELVETFRUIT_EXTRACT': 250,
}
for opt in OPTIONS.keys():
    POS_LIMITS[opt] = 20  

# --- UTILIDADES MATEMÁTICAS NATIVAS ---
SQRT_2 = math.sqrt(2.0)

def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(float(x) / SQRT_2))

def get_mid_price(order_depth: OrderDepth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    return (best_bid + best_ask) / 2.0

def get_imbalance(order_depth: OrderDepth):
    if not order_depth.buy_orders and not order_depth.sell_orders: 
        return 0.0
    buy_vol = sum(order_depth.buy_orders.values())
    # CORRECCIÓN: Los sell_orders ya son negativos en Prosperity, forzamos valor absoluto
    sell_vol = abs(sum(order_depth.sell_orders.values())) 
    total = buy_vol + sell_vol
    return (buy_vol - sell_vol) / total if total > 0 else 0.0

# --- CLASE: TRADER DE OPCIONES ---
class OptionTrader:
    def __init__(self, state: TradingState, new_trader_data: dict):
        self.state = state
        self.new_trader_data = new_trader_data
        self.orders: dict[str, list[Order]] = {}
        self.r = 0.0
        
        # Tiempo a expiración proxy
        current_day = float(state.timestamp // 1000000)
        remaining_ticks = 1000000.0 - float(state.timestamp % 1000000)
        days_left = (3.0 - 1.0 - current_day) + (remaining_ticks / 1000000.0)
        self.T = max(days_left / 252.0, 1e-6)

        self.strategy()

    def bs_call_price(self, S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0:
            return max(0.0, S - K)
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

    def bs_delta(self, S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0:
            return 1.0 if S > K else 0.0
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        return norm_cdf(d1)

    def strategy(self):
        underlying_depth = self.state.order_depths.get(OPTION_UNDERLYING_SYMBOL)
        if not underlying_depth: return
            
        S = get_mid_price(underlying_depth)
        if S is None: return

        total_portfolio_delta = 0.0

        for option_symbol, strike in OPTIONS.items():
            if option_symbol not in self.state.order_depths:
                continue
                
            depth = self.state.order_depths[option_symbol]
            position = self.state.position.get(option_symbol, 0)
            limit = POS_LIMITS.get(option_symbol, 20)
            
            sigma = SMILE_IV.get(strike, 0.55)
            
            fair_value = self.bs_call_price(S, strike, self.T, self.r, sigma)
            delta = self.bs_delta(S, strike, self.T, self.r, sigma)
            
            total_portfolio_delta += position * delta
            
            edge = 1.5 if sigma < 0.7 else 2.5
            inventory_skew = (position / float(limit)) * edge
            
            bid_px = int(math.floor(fair_value - edge - inventory_skew))
            ask_px = int(math.ceil(fair_value + edge - inventory_skew))
            
            buy_qty = limit - position
            sell_qty = -limit - position
            
            orders = []
            
            best_ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
            best_bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
            
            # 1. Arbitraje (Sniping)
            if best_ask is not None and best_ask < fair_value - edge and buy_qty > 0:
                available_ask_vol = abs(depth.sell_orders[best_ask]) 
                take_qty = min(buy_qty, available_ask_vol)
                orders.append(Order(option_symbol, best_ask, take_qty))
                buy_qty -= take_qty
                
            if best_bid is not None and best_bid > fair_value + edge and sell_qty < 0:
                available_bid_vol = depth.buy_orders[best_bid] 
                take_qty = max(sell_qty, -available_bid_vol) 
                orders.append(Order(option_symbol, best_bid, take_qty)) 
                sell_qty -= take_qty

            # --- SPREAD CLAMPING (BLINDAJE DE SEGURIDAD) ---
            # Evitamos que nuestras órdenes pasivas crucen el libro (lo que causaba que el motor rechazara tu bot)
            if best_ask is not None:
                bid_px = min(bid_px, best_ask - 1)
            if best_bid is not None:
                ask_px = max(ask_px, best_bid + 1)

            # 2. Cotización Pasiva Segura
            if buy_qty > 0:
                orders.append(Order(option_symbol, bid_px, buy_qty))
            if sell_qty < 0:
                orders.append(Order(option_symbol, ask_px, sell_qty))
                
            self.orders[option_symbol] = orders

        # Guardar Delta neto para Delta1Trader
        self.new_trader_data['target_delta'] = total_portfolio_delta

    def get_orders(self):
        return self.orders


# --- CLASE: TRADER DELTA-1 ---
class Delta1Trader:
    def __init__(self, state: TradingState, new_trader_data: dict, symbol: str):
        self.state = state
        self.new_trader_data = new_trader_data
        self.symbol = symbol
        self.orders: dict[str, list[Order]] = {}
        self.strategy()
        
    def strategy(self):
        depth = self.state.order_depths.get(self.symbol)
        if not depth: return
            
        mid = get_mid_price(depth)
        if mid is None: return
        
        pos = self.state.position.get(self.symbol, 0)
        limit = POS_LIMITS.get(self.symbol, 250)
        
        target_pos = 0
        # Target Delta Neutral para el Subyacente
        if self.symbol == OPTION_UNDERLYING_SYMBOL:
            options_delta = self.new_trader_data.get('target_delta', 0.0)
            target_pos = -int(round(options_delta))

        # Alpha direccional con Imbalance arreglado
        imbalance = get_imbalance(depth)
        predictive_shift = imbalance * 2.5 
        fair = mid + predictive_shift
        
        skew = ((pos - target_pos) / float(limit)) * 2.5
        spread = 1.5
        
        bid_px = int(math.floor(fair - spread - skew))
        ask_px = int(math.ceil(fair + spread - skew))
        
        best_ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
        best_bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
        
        # --- SPREAD CLAMPING ---
        if best_ask is not None:
            bid_px = min(bid_px, best_ask - 1)
        if best_bid is not None:
            ask_px = max(ask_px, best_bid + 1)
            
        buy_qty = limit - pos
        sell_qty = -limit - pos
        
        orders = []
        if buy_qty > 0:
            orders.append(Order(self.symbol, bid_px, buy_qty))
        if sell_qty < 0:
            orders.append(Order(self.symbol, ask_px, sell_qty))
            
        self.orders[self.symbol] = orders

    def get_orders(self):
        return self.orders


# --- CONTROLADOR PRINCIPAL ---
class Trader:
    def run(self, state: TradingState):
        result: dict[str, list[Order]] = {}
        
        # Deserialización segura
        try:
            new_trader_data = json.loads(state.traderData) if state.traderData else {}
        except:
            new_trader_data = {}

        try:
            # 1. Opciones
            opt_trader = OptionTrader(state, new_trader_data)
            result.update(opt_trader.get_orders())
            
            # 2. Delta-1
            for symbol in DELTA1_SYMBOLS + [OPTION_UNDERLYING_SYMBOL]:
                if symbol in state.order_depths:
                    delta1_trader = Delta1Trader(state, new_trader_data, symbol)
                    if symbol not in result:
                        result.update(delta1_trader.get_orders())
                        
        except Exception as e:
            # Captura de errores vainilla sin usar dependencias externas
            print(f"ERROR: {str(e)}")
            
        trader_data_out = json.dumps(new_trader_data)
        return result, 0, trader_data_out