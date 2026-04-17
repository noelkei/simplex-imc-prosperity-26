import time
import numpy as np
import collections
from optibook.synchronous_client import Exchange
from exchange import exchange as e

# --- CONFIGURACIÓN ---
STOCK_ID = 'ASML'
MAX_POS = 32            # Límite estricto solicitado
VENTANA_HISTORIA = 50   # Cuantos ticks atrás miramos para calcular X (memoria corta)
FREQ_UPDATE = 0.2       # Velocidad del bucle

# Detectar futuros
todos = e.get_instruments()
futuros = sorted([i for i in todos if i.startswith('ASML') and i.endswith('_F')])
# print(f"🎯 Futuros detectados: {futuros}")

# Memoria deslizante para calcular X en tiempo real
# Guardamos tuplas (log_bid_spread, log_ask_spread)
historia = {f: collections.deque(maxlen=VENTANA_HISTORIA) for f in futuros}

def calcular_x_dinamica(f):
    """Calcula la X óptima basada en la memoria reciente"""
    data = historia[f]
    if len(data) < 5: return 0.0 # Necesitamos un mínimo de datos
    
    # Extraer bids y asks de la historia
    # data es una lista de ([spread_bids], [spread_asks])
    # Aplanamos las listas porque en un tick puede haber varios spreads o ninguno
    diff_bids = np.array([x for snapshot in data for x in snapshot['bids']])
    diff_asks = np.array([x for snapshot in data for x in snapshot['asks']])
    
    if len(diff_bids) == 0 or len(diff_asks) == 0: return 0.0

    # Optimización rápida
    min_search = np.min(diff_bids)
    max_search = np.max(diff_asks)
    candidatos = np.linspace(min_search, max_search, 200) # 200 puntos es suficiente para tiempo real
    
    best_x = 0
    best_score = -1
    
    for x in candidatos:
        score = min(np.sum(diff_asks < x), np.sum(diff_bids > x))
        if score > best_score:
            best_score = score
            best_x = x
            
    return best_x

# print("\n🚀 INICIANDO ESTRATEGIA TAKER (VOL MAX 20)")

def futures():
    while True:
        # 1. Obtener Spot
        book_s = e.get_last_price_book(STOCK_ID)
        if not (book_s and book_s.bids and book_s.asks): continue
        mid_spot = (book_s.bids[0].price + book_s.asks[0].price) / 2
        log_spot = np.log(mid_spot)
        
        positions = e.get_positions()
        txt_out = ""

        for f in futuros:
            book_f = e.get_last_price_book(f)
            if not book_f: continue
            
            # 2. Actualizar Historia para X
            snapshot = {'bids': [], 'asks': []}
            if book_f.bids:
                snapshot['bids'].append(np.log(book_f.bids[0].price) - log_spot)
            if book_f.asks:
                snapshot['asks'].append(np.log(book_f.asks[0].price) - log_spot)
            
            historia[f].append(snapshot)
            
            # 3. Calcular X y Fair Price
            x = calcular_x_dinamica(f)
            fair_price = mid_spot * np.exp(x)
            
            # 4. Trading Aggresivo (Taker)
            pos = positions.get(f, 0)
            
            # --- OPORTUNIDAD DE COMPRA ---
            # Si el Ask del mercado es MENOR que mi precio justo -> Está BARATO -> COMPRAR
            if book_f.asks and book_f.asks[0].price < fair_price:
                market_ask_price = book_f.asks[0].price
                market_ask_vol = book_f.asks[0].volume
                
                # Cuánto puedo comprar hasta llegar a +20
                room_to_buy = int(MAX_POS - pos)
                if room_to_buy > 0:
                    # Tomamos lo que haya, limitado por mi espacio y el volumen disponible
                    vol_to_trade = min(room_to_buy, market_ask_vol)
                    
                    if vol_to_trade > 0:
                        e.insert_order(f, price=market_ask_price, volume=vol_to_trade, side='bid', order_type='ioc')
                        # print(f"\nBUY {f}: Precio {market_ask_price} < Fair {fair_price:.2f} | Vol: {vol_to_trade}")

            # --- OPORTUNIDAD DE VENTA ---
            # Si el Bid del mercado es MAYOR que mi precio justo -> Está CARO -> VENDER
            if book_f.bids and book_f.bids[0].price > fair_price:
                market_bid_price = book_f.bids[0].price
                market_bid_vol = book_f.bids[0].volume
                
                # Cuánto puedo vender hasta llegar a -20
                # Distancia desde 'pos' hasta '-20' es: pos - (-20) = pos + 20
                room_to_sell = int(MAX_POS + pos) 
                if room_to_sell > 0:
                    vol_to_trade = min(room_to_sell, market_bid_vol)
                    
                    if vol_to_trade > 0:
                        e.insert_order(f, price=market_bid_price, volume=vol_to_trade, side='ask', order_type='ioc')
                        # print(f"SELL {f}: Precio {market_bid_price} > Fair {fair_price:.2f} | Vol: {vol_to_trade}")

            # txt_out += f"[{f.split('_')[1]} P:{pos} X:{x:.4f}] "

        # print(f"Spot: {mid_spot:.1f} | {txt_out}", end='\r')
        time.sleep(FREQ_UPDATE)

# futures()