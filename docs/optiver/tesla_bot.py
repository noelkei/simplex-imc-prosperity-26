import time
import statistics
import math
from collections import deque
from optibook.synchronous_client import Exchange
from exchange import exchange as e

INSTRUMENTO = 'TSLA'
MAX_POSICION = 100
HISTORIAL = 10
LATENCIA = 0.1

def close_positions_safely():
    # print("\n\n>>> PROTOCOLO DE CIERRE DE EMERGENCIA INICIADO <<<")
    e.delete_orders(INSTRUMENTO)
    time.sleep(0.2)
    
    intentos = 0
    while intentos < 5:
        pos = e.get_positions().get(INSTRUMENTO, 0)
        if pos == 0:
            print(">>> ÉXITO: Posición cerrada (FLAT).")
            break
            
        side = 'ask' if pos > 0 else 'bid'
        price = 1.0 if side == 'ask' else 100000.0
        print(f" -> Cerrando {abs(pos)} contratos ({side})...")
        e.insert_order(INSTRUMENTO, price=price, volume=abs(pos), side=side, order_type='ioc')
        time.sleep(0.5)
        intentos += 1
    if e.get_positions().get(INSTRUMENTO, 0) != 0:
        print("!!! ALERTA: No se pudo cerrar toda la posición. Revisar manualmente.")
    else:
        print(">>> Sistema apagado correctamente.")

def TSLA_MM():
    indice_escenario = 0
    ultimo_cambio = time.time()
    pnl_inicio_intervalo = 0

    # Inicialización

    e.delete_orders(INSTRUMENTO)
    pnl_inicio_intervalo = e.get_pnl()

    pnl_actual = e.get_pnl()
    ultimo_cambio = time.time()
    pnl_inicio_intervalo = pnl_actual

    bids_hist = deque(maxlen=HISTORIAL)
    asks_hist = deque(maxlen=HISTORIAL)
    e.delete_orders(INSTRUMENTO)

    while True:
        try:
            ahora = time.time()
            
            book = e.get_last_price_book(INSTRUMENTO)
            if not (book and book.bids and book.asks):
                continue

            bids_hist.append(book.bids[0].price)
            asks_hist.append(book.asks[0].price)

            if len(bids_hist) < HISTORIAL: # Esperar a tener al menos la mitad
                # print(f"Recalibrando... {len(bids_hist)} datos", end='\r')
                time.sleep(LATENCIA)
                continue

            # PRECIOS MERCADO (MODA).
            try:
                target_bid_price = statistics.mode(bids_hist)
                target_ask_price = statistics.mode(asks_hist)
            except:
                target_bid_price = book.bids[0].price
                target_ask_price = book.asks[0].price

            pos = e.get_positions().get(INSTRUMENTO, 0)
            

            # VOLUMEN (Usando el parámetro dinámico)
            target_bid_vol = MAX_POSICION - pos
            target_ask_vol  = MAX_POSICION + pos
            

            # GESTIÓN DE ÓRDENES
            mis_ordenes = e.get_outstanding_orders(INSTRUMENTO)
            vol_actual_bid_en_precio = 0
            vol_actual_ask_en_precio = 0
            
            for o_id, orden in mis_ordenes.items():
                if orden.side == 'bid':
                    if orden.price == target_bid_price:
                        vol_actual_bid_en_precio += orden.volume
                    else:
                        e.delete_order(INSTRUMENTO, order_id=o_id)
                elif orden.side == 'ask':
                    if orden.price == target_ask_price:
                        vol_actual_ask_en_precio += orden.volume
                    else:
                        e.delete_order(INSTRUMENTO, order_id=o_id)
            
            # PROPOSTA EVITAR RACE CONDITION
            time.sleep(0.02)

            # RELLENAR VOLUMEN
            # -- LADO BID --
            faltante_bid = target_bid_vol - vol_actual_bid_en_precio
            if faltante_bid > 0:
                e.insert_order(INSTRUMENTO, price=target_bid_price, volume=faltante_bid, side='bid', order_type='limit')

            # -- LADO ASK --
            faltante_ask = target_ask_vol - vol_actual_ask_en_precio
            if faltante_ask > 0:
                e.insert_order(INSTRUMENTO, price=target_ask_price, volume=faltante_ask, side='ask', order_type='limit')

            # Visualización PnL en tiempo real
            # pnl_actual_total = e.get_pnl()
            # pnl_este_bloque = pnl_actual_total - pnl_inicio_intervalo
            # tiempo_total = int((ahora - ultimo_cambio))
            
            # print(f"[{tiempo_total}s] | PnL Bloque: {pnl_este_bloque:.2f} | Pos: {pos}", end='\r')
            
            time.sleep(LATENCIA)

        except Exception as err:
            print(f"\nError inesperado: {err}")
            continue

# TSLA_MM()