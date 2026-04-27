"""
Bot ID: P4-Frankfurt-Pro
Arquitectura Modular + Volatility Smile + Delta Hedging Activo + Imbalance
"""

import json
import math
import traceback
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
    if not order_depth: return 0.0
    buy_vol = sum(order_depth.buy_orders.values())
    sell_vol = sum(order_depth.sell_orders.values())
    total = buy_vol + sell_vol
    return (buy_vol - sell_vol) / total if total > 0 else 0.0

# --- CLASE: TRADER DE OPCIONES ---
class OptionTrader:
    def __init__(self, state: TradingState, prints: dict, new_trader_data: dict):
        self.state = state
        self.prints = prints
        self.new_trader_data = new_trader_data
        self.orders: dict[str, list[Order]] = {}
        
        self.r = 0.0
        
        # Tiempo a expiración proxy
        current_day = state.timestamp // 1000000.0
        remaining_ticks = 1000000.0 - (state.timestamp % 1000000.0)
        days_left = (3.0 - 1 - current_day) + (remaining_ticks / 1000000.0)
        self.T = max(days_left / 252.0, 1e-6)

        self.strategy()

    def bs_call_price(self, S, K, T, r, sigma):
        if T <= 0 or sigma <= 0 or S <= 0:
            return max(0.0, S - K)
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        return S * norm_cdf(d1) - K * math.exp(-r * T) * norm_cdf(d2)

    def bs_delta(self, S, K, T, r, sigma):
        """Calcula la exposición direccional de la opción"""
        if T <= 0 or sigma <= 0 or S <= 0:
            return 1.0 if S > K else 0.0
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        return norm_cdf(d1)

    def strategy(self):
        underlying_depth = self.state.order_depths.get(OPTION_UNDERLYING_SYMBOL)
        if not underlying_depth: return
            
        S = get_mid_price(underlying_depth)
        if S is None: return

        # Calcular el Delta total del portafolio de opciones
        total_portfolio_delta = 0.0

        for option_symbol, strike in OPTIONS.items():
            if option_symbol not in self.state.order_depths:
                continue
                
            depth = self.state.order_depths[option_symbol]
            position = self.state.position.get(option_symbol, 0)
            limit = POS_LIMITS.get(option_symbol, 20)
            
            # Usar la Volatilidad Implícita correcta para ESTE strike (Smile)
            sigma = SMILE_IV.get(strike, 0.55)
            
            fair_value = self.bs_call_price(S, strike, self.T, self.r, sigma)
            delta = self.bs_delta(S, strike, self.T, self.r, sigma)
            
            total_portfolio_delta += position * delta
            
            # Spread dinámico: Opciones más volátiles necesitan mayor margen
            edge = 1.5 if sigma < 0.7 else 2.5
            inventory_skew = (position / limit) * edge
            
            bid_px = int(math.floor(fair_value - edge - inventory_skew))
            ask_px = int(math.ceil(fair_value + edge - inventory_skew))
            
            buy_qty = limit - position
            sell_qty = -limit - position
            
            orders = []
            
            best_ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
            best_bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
            
            # Arbitraje (Sniping)
            if best_ask and best_ask < fair_value - edge and buy_qty > 0:
                available_ask_vol = -depth.sell_orders[best_ask] 
                take_qty = min(buy_qty, available_ask_vol)
                orders.append(Order(option_symbol, best_ask, take_qty))
                buy_qty -= take_qty
                
            if best_bid and best_bid > fair_value + edge and sell_qty < 0:
                available_bid_vol = depth.buy_orders[best_bid] 
                take_qty = max(sell_qty, -available_bid_vol) 
                orders.append(Order(option_symbol, best_bid, take_qty)) 
                sell_qty -= take_qty

            # Cotización Pasiva
            if buy_qty > 0:
                orders.append(Order(option_symbol, bid_px, buy_qty))
            if sell_qty < 0:
                orders.append(Order(option_symbol, ask_px, sell_qty))
                
            self.orders[option_symbol] = orders

        # Enviar el Delta al trader del subyacente para que se cubra
        self.new_trader_data['target_delta'] = total_portfolio_delta


# --- CLASE: TRADER DELTA-1 ---
class Delta1Trader:
    def __init__(self, state: TradingState, prints: dict, new_trader_data: dict, symbol: str):
        self.state = state
        self.prints = prints
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
        # --- DELTA HEDGING PASIVO ---
        # Si este es el subyacente, nuestra posición objetivo es la opuesta al Delta de las opciones
        if self.symbol == OPTION_UNDERLYING_SYMBOL:
            options_delta = self.new_trader_data.get('target_delta', 0.0)
            target_pos = -int(round(options_delta))

        # --- ALPHA POR IMBALANCE ---
        # Predecimos a dónde se moverá el precio usando el libro de órdenes
        imbalance = get_imbalance(depth)
        predictive_shift = imbalance * 2.5 
        fair = mid + predictive_shift
        
        # Desplazamos nuestros precios en base a cuánto nos alejamos del Target
        skew = ((pos - target_pos) / limit) * 2.5
        
        # Spread dinámico (protección)
        spread = 1.5
        
        bid_px = int(math.floor(fair - spread - skew))
        ask_px = int(math.ceil(fair + spread - skew))
        
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
        
        try:
            new_trader_data = json.loads(state.traderData) if state.traderData else {}
        except:
            new_trader_data = {}
            
        prints = {}

        try:
            # 1. Ejecutar Options (Manda las órdenes de opciones y calcula el Delta Neto)
            opt_trader = OptionTrader(state, prints, new_trader_data)
            result.update(opt_trader.get_orders())
            
            # 2. Ejecutar Fallback Delta-1 (Usa el Delta Neto para cubrir el Velvetfruit, y opera Hydrogel)
            for symbol in DELTA1_SYMBOLS + [OPTION_UNDERLYING_SYMBOL]:
                if symbol in state.order_depths:
                    delta1_trader = Delta1Trader(state, prints, new_trader_data, symbol)
                    if symbol not in result:
                        result.update(delta1_trader.get_orders())
                        
        except Exception as e:
            print(f"CRITICAL ERROR at timestamp {state.timestamp}: {str(e)}")
            traceback.print_exc()
            
        trader_data_out = json.dumps(new_trader_data)
        return result, 0, trader_data_out