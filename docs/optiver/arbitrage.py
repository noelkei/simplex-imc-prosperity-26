import time
import logging
from optibook.synchronous_client import Exchange
from exchange import exchange

# --- CONFIGURACIÓN SIMPLE ---
STOCK_ID = "SAP"
DUAL_ID = "SAP_DUAL"
MIN_PROFIT = 0.20    
MAX_VOLUME = 25    
POSITION_LIMIT = 100     

# print(f"BOT ARBITRAJE SIMPLE")

max_vol = MAX_VOLUME

def arbitrage():
    while True:
        max_vol = MAX_VOLUME
        req_profit = MIN_PROFIT
        book_stock = exchange.get_last_price_book(STOCK_ID)
        book_dual = exchange.get_last_price_book(DUAL_ID)
        positions = exchange.get_positions()
        
        pos_stock = positions.get(STOCK_ID, 0)
        pos_dual = positions.get(DUAL_ID, 0)

        if pos_stock > 70: req_profit = 0.0
        # Verificamos que los libros tengan datos
        if not (book_stock and book_stock.bids and book_stock.asks and 
                book_dual and book_dual.bids and book_dual.asks):
            time.sleep(0.1)
            continue

        # --- OPORTUNIDAD 1: Comprar SAP, Vender DUAL ---
        # (Bid DUAL - Ask SAP)
        profit_1 = book_dual.bids[0].price - book_stock.asks[0].price

        if profit_1 >= req_profit:
            if profit_1 > 0.4: max_vol = 100
            elif profit_1 > 0.3: max_vol = 50
            max_buy_stock = POSITION_LIMIT - pos_stock
            max_sell_dual = POSITION_LIMIT + pos_dual
            volume = min(book_stock.asks[0].volume, book_dual.bids[0].volume, max_buy_stock, max_sell_dual, max_vol)
            
            if volume > 0:
                # print(f"[OPORTUNIDAD] Buy {STOCK_ID} / Sell {DUAL_ID} | Ganas: {profit_1:.2f} | Vol: {volume}")
                exchange.insert_order(STOCK_ID, price=book_stock.asks[0].price, volume=volume, side='bid', order_type='ioc')
                exchange.insert_order(DUAL_ID, price=book_dual.bids[0].price, volume=volume, side='ask', order_type='ioc')
                time.sleep(1)

        # --- OPORTUNIDAD 2: Vender SAP, Comprar DUAL ---
        # (Bid SAP - Ask DUAL)
        profit_2 = book_stock.bids[0].price - book_dual.asks[0].price

        if profit_2 >= req_profit:
            if profit_2 > 0.4: max_vol = 100
            elif profit_2 > 0.3: max_vol = 50
            max_sell_stock = POSITION_LIMIT + pos_stock
            max_buy_dual = POSITION_LIMIT - pos_dual
            volume = min(book_dual.asks[0].volume, book_stock.bids[0].volume, max_sell_stock, max_buy_dual, max_vol)
            
            if volume > 0:
                # print(f"[OPORTUNIDAD] Sell {STOCK_ID} / Buy {DUAL_ID} | Ganas: {profit_2:.2f} | Vol: {volume}")
                exchange.insert_order(DUAL_ID, price=book_dual.asks[0].price, volume=volume, side='bid', order_type='ioc')
                exchange.insert_order(STOCK_ID, price=book_stock.bids[0].price, volume=volume, side='ask', order_type='ioc')
                time.sleep(1)

        net = positions.get(STOCK_ID, 0) + positions.get(DUAL_ID, 0)
        if net == 0: continue 
        book = exchange.get_last_price_book(STOCK_ID)
        if not book: continue
        if net > 0: # Tenim de més -> Vendre
            # print(f"\n[HEDGE] SELL {STOCK_ID} {net} @ {book['bid']:.2f}")
            exchange.insert_order(STOCK_ID, price=book.bids[0].price, volume=abs(net), side='ask', order_type='ioc')
        else: # Tenim de menys -> Comprar
            # print(f"\n[HEDGE] BUY {STOCK_ID} {abs(net)} @ {book['ask']:.2f}")
            exchange.insert_order(STOCK_ID, price=book.asks[0].price, volume=abs(net), side='bid', order_type='ioc')

        time.sleep(1)