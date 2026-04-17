import datetime as dt
import time
import logging

from optibook.synchronous_client import Exchange
from optibook.common_types import InstrumentType, OptionKind

from math import floor, ceil

from exchange import exchange 

# region setup
import sys
import subprocess

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)


install_and_import("scipy")
sys.path.append("/home/workspace/your_optiver_workspace")
# endregion

from common.black_scholes import call_value, put_value, call_delta, put_delta
from common.libs import calculate_current_time_to_date

logging.getLogger("client").setLevel("ERROR")


def round_down_to_tick(price, tick_size):
    return floor(price / tick_size) * tick_size

def round_up_to_tick(price, tick_size):
    return ceil(price / tick_size) * tick_size

def get_midpoint_value(instrument_id):
    order_book = exchange.get_last_price_book(instrument_id=instrument_id)
    if not (order_book and order_book.bids and order_book.asks):
        return None
    else:
        midpoint = (order_book.bids[0].price + order_book.asks[0].price) / 2.0
        return midpoint

def get_bid_ask_spread(instrument_id):
    order_book = exchange.get_last_price_book(instrument_id=instrument_id)
    if not (order_book and order_book.bids and order_book.asks):
        return None
    return order_book.asks[0].price - order_book.bids[0].price

def calculate_theoretical_option_value(expiry, strike, option_kind, stock_value, interest_rate, volatility):
    time_to_expiry = calculate_current_time_to_date(expiry)

    if option_kind == OptionKind.CALL:
        option_value = call_value(
            S=stock_value, K=strike, T=time_to_expiry, r=interest_rate, sigma=volatility
        )
    elif option_kind == OptionKind.PUT:
        option_value = put_value(
            S=stock_value, K=strike, T=time_to_expiry, r=interest_rate, sigma=volatility
        )

    return option_value

def calculate_option_delta(expiry_date, strike, option_kind, stock_value, interest_rate, volatility):
    time_to_expiry = calculate_current_time_to_date(expiry_date)

    if option_kind == OptionKind.CALL:
        option_delta = call_delta(
            S=stock_value, K=strike, T=time_to_expiry, r=interest_rate, sigma=volatility
        )
    elif option_kind == OptionKind.PUT:
        option_delta = put_delta(
            S=stock_value, K=strike, T=time_to_expiry, r=interest_rate, sigma=volatility
        )
    else:
        raise Exception(f"Unexpected option_kind: {option_kind}")

    return option_delta

def calculate_option_gamma(expiry_date, strike, stock_value, interest_rate, volatility):
    from scipy.stats import norm
    import math
    
    time_to_expiry = calculate_current_time_to_date(expiry_date)
    if time_to_expiry <= 0:
        return 0.0
    
    d1 = (math.log(stock_value / strike) + (interest_rate + 0.5 * volatility**2) * time_to_expiry) / (
        volatility * math.sqrt(time_to_expiry)
    )
    
    gamma = norm.pdf(d1) / (stock_value * volatility * math.sqrt(time_to_expiry))
    return gamma

def calculate_option_vega(expiry_date, strike, stock_value, interest_rate, volatility):
    from scipy.stats import norm
    import math
    
    time_to_expiry = calculate_current_time_to_date(expiry_date)
    if time_to_expiry <= 0:
        return 0.0
    
    d1 = (math.log(stock_value / strike) + (interest_rate + 0.5 * volatility**2) * time_to_expiry) / (
        volatility * math.sqrt(time_to_expiry)
    )
    
    vega = stock_value * norm.pdf(d1) * math.sqrt(time_to_expiry) / 100
    return vega

def calculate_dynamic_credit(option, stock_value, stock_spread):
    time_to_expiry = calculate_current_time_to_date(option.expiry)
    
    gamma = calculate_option_gamma(
        option.expiry, option.strike, stock_value, 0.03, 3.0
    )
    vega = calculate_option_vega(
        option.expiry, option.strike, stock_value, 0.03, 3.0
    )
    
    base_credit = 0.10
    gamma_component = abs(gamma) * 100 * 0.50
    vega_component = vega * 0.01
    
    if time_to_expiry > 0:
        dte_days = time_to_expiry * 365
        dte_factor = max(0.7, 1.0 - (dte_days / 90) * 0.3)
    else:
        dte_factor = 0.5
    
    spread_factor = 1.0
    if stock_spread and stock_spread > 0.1:
        spread_factor = 1.0 + (stock_spread - 0.1) * 2.0
    
    moneyness = stock_value / option.strike
    if 0.95 < moneyness < 1.05:
        moneyness_factor = 1.2
    else:
        moneyness_factor = 1.0
    
    credit = (base_credit + gamma_component + vega_component) * dte_factor * spread_factor * moneyness_factor
    credit = max(0.08, min(0.50, credit))
    
    return credit


def calculate_optimal_volume(option, option_delta, total_portfolio_delta, position, position_limit):
    base_volume = 15
    position_headroom = position_limit - abs(position)
    max_safe_delta = 80
    delta_headroom = max_safe_delta - abs(total_portfolio_delta)
    
    if abs(option_delta) > 0.01:
        max_volume_by_delta = int(delta_headroom / abs(option_delta))
    else:
        max_volume_by_delta = base_volume
    
    optimal_volume = min(base_volume, position_headroom, max_volume_by_delta)
    optimal_volume = max(0, optimal_volume)
    
    return optimal_volume


def calculate_position_skew(position, position_limit=100):
    """Skew individual basado en posición"""
    normalized_position = position / position_limit
    
    if abs(position) > 80:
        intensity = 3.0
    elif abs(position) > 60:
        intensity = 2.0
    elif abs(position) > 40:
        intensity = 1.0
    else:
        intensity = 0.5
    
    skew = -normalized_position * intensity
    return skew


def update_quotes_unwind(option_id, theoretical_price, position, tick_size):
    """
    MODO UNWIND: Solo quotear en la dirección para REDUCIR posición
    Con precios muy agresivos para forzar ejecución
    """
    orders = exchange.get_outstanding_orders(instrument_id=option_id)
    for order_id in orders.keys():
        exchange.delete_order(instrument_id=option_id, order_id=order_id)
    
    # Volumen para unwind (agresivo)
    unwind_volume = min(20, abs(position))
    
    if position > 0:
        # Muy LARGO → Solo quotear ASK (vender)
        # Precio MUY BARATO para forzar venta
        aggressive_discount = 0.10  # Descuento agresivo
        ask_price = round_down_to_tick(theoretical_price - aggressive_discount, tick_size)
        
        # print(f"🔴 UNWIND: Vendiendo {option_id} @ {ask_price:.2f} (pos: +{position})")
        
        exchange.insert_order(
            instrument_id=option_id,
            price=ask_price,
            volume=unwind_volume,
            side="ask",
            order_type="limit",
        )
        
    elif position < 0:
        # Muy CORTO → Solo quotear BID (comprar)
        # Precio MUY CARO para forzar compra
        aggressive_premium = 0.10
        bid_price = round_up_to_tick(theoretical_price + aggressive_premium, tick_size)
        
        # print(f"🔴 UNWIND: Comprando {option_id} @ {bid_price:.2f} (pos: {position})")
        
        exchange.insert_order(
            instrument_id=option_id,
            price=bid_price,
            volume=unwind_volume,
            side="bid",
            order_type="limit",
        )


def update_quotes(
    option_id, option, theoretical_price, credit, volume, position_limit, tick_size, 
    total_portfolio_delta, position_skew
):
    """Quote normal con position skew"""
    orders = exchange.get_outstanding_orders(instrument_id=option_id)
    for order_id, order in orders.items():
        exchange.delete_order(instrument_id=option_id, order_id=order_id)

    skewed_price = theoretical_price + position_skew
    
    bid_price = round_down_to_tick(skewed_price - credit, tick_size)
    ask_price = round_up_to_tick(skewed_price + credit, tick_size)

    position = exchange.get_positions()[option_id]

    max_volume_to_buy = position_limit - position
    max_volume_to_sell = position_limit + position

    bid_volume = min(volume, max_volume_to_buy)
    ask_volume = min(volume, max_volume_to_sell)

    if bid_volume > 0:
        exchange.insert_order(
            instrument_id=option_id,
            price=bid_price,
            volume=bid_volume,
            side="bid",
            order_type="limit",
        )
    if ask_volume > 0:
        exchange.insert_order(
            instrument_id=option_id,
            price=ask_price,
            volume=ask_volume,
            side="ask",
            order_type="limit",
        )


def hedge_delta_position(stock_id, options, stock_value):
    positions = exchange.get_positions()
    
    total_delta = 0.0
    stock_position = positions[stock_id]
    total_delta += stock_position

    for option_id, option in options.items():
        position = positions[option_id]
        
        if position != 0:
            option_delta = calculate_option_delta(
                expiry_date=option.expiry,
                strike=option.strike,
                option_kind=option.option_kind,
                stock_value=stock_value,
                interest_rate=0.03,
                volatility=3.0
            )
            
            position_delta = option_delta * position
            total_delta += position_delta
    
    # print(f"- TOTAL PORTFOLIO DELTA: {total_delta:.2f}")
    
    hedge_threshold = 5.0
    
    if abs(total_delta) > hedge_threshold:
        hedge_volume = int(abs(total_delta))
        stock_position_after_hedge = stock_position - hedge_volume if total_delta > 0 else stock_position + hedge_volume
        
        if abs(stock_position_after_hedge) > 100:
            if total_delta > 0:
                hedge_volume = min(hedge_volume, 100 + stock_position)
            else:
                hedge_volume = min(hedge_volume, 100 - stock_position)
        
        if hedge_volume > 0:
            if total_delta > 0:
                hedge_side = "ask"
            else:
                hedge_side = "bid"
            
            stock_book = exchange.get_last_price_book(stock_id)
            
            if stock_book and stock_book.bids and stock_book.asks:
                if hedge_side == "bid":
                    hedge_price = stock_book.asks[0].price + 0.10
                else:
                    hedge_price = stock_book.bids[0].price - 0.10
                
                exchange.insert_order(
                    instrument_id=stock_id,
                    price=hedge_price,
                    volume=hedge_volume,
                    side=hedge_side,
                    order_type="ioc"
                )
                
                time.sleep(0.1)
    
    return total_delta


def load_instruments_for_underlying(underlying_stock_id):
    all_instruments = exchange.get_instruments()
    stock = all_instruments[underlying_stock_id]
    options = {
        instrument_id: instrument
        for instrument_id, instrument in all_instruments.items()
        if instrument.instrument_type == InstrumentType.STOCK_OPTION
        and instrument.base_instrument_id == underlying_stock_id
    }
    return stock, options


# Load all instruments
STOCK_ID = "ASML"
stock, options = load_instruments_for_underlying(STOCK_ID)

def run_asml_bot():
    # pnl_inicio_intervalo = 0
    # pnl_inicio_intervalo = exchange.get_pnl()
    # pnl_actual = exchange.get_pnl()
    # pnl_inicio_intervalo = pnl_actual

    while True:

        stock_value = get_midpoint_value(STOCK_ID)
        if stock_value is None:
            time.sleep(0.1)
            continue

        stock_spread = get_bid_ask_spread(STOCK_ID)
        
        positions = exchange.get_positions()
        preliminary_delta = positions[STOCK_ID]
        
        for option_id, option in options.items():
            position = positions[option_id]
            if position != 0:
                option_delta = calculate_option_delta(
                    expiry_date=option.expiry,
                    strike=option.strike,
                    option_kind=option.option_kind,
                    stock_value=stock_value,
                    interest_rate=0.03,
                    volatility=3.0
                )
                preliminary_delta += option_delta * position

        skew_factor = 0.01
        global_skew = preliminary_delta * skew_factor
        
        # Update quotes
        for option_id, option in options.items():
            theoretical_value = calculate_theoretical_option_value(
                expiry=option.expiry,
                strike=option.strike,
                option_kind=option.option_kind,
                stock_value=stock_value,
                interest_rate=0.03,
                volatility=3.0,
            )
            
            option_delta = calculate_option_delta(
                expiry_date=option.expiry,
                strike=option.strike,
                option_kind=option.option_kind,
                stock_value=stock_value,
                interest_rate=0.03,
                volatility=3.0
            )

            position = positions[option_id]
            
            # CLAVE: Si posición extrema, MODO UNWIND
            if abs(position) >= 95:
                # Modo unwind agresivo
                update_quotes_unwind(
                    option_id=option_id,
                    theoretical_price=theoretical_value,
                    position=position,
                    tick_size=0.10
                )
                time.sleep(0.1)  # Más rápido en unwind
                continue
            
            # Normal quoting con skew
            dynamic_credit = calculate_dynamic_credit(option, stock_value, stock_spread)
            
            optimal_volume = calculate_optimal_volume(
                option, option_delta, preliminary_delta, position, position_limit=100
            )

            position_skew = calculate_position_skew(position, position_limit=100)
            # total_skew = global_skew + position_skew
            total_skew = 0
            price_to_quote = theoretical_value - total_skew
            extra_credit = abs(total_skew) * 0.1
        
            update_quotes(
                option_id=option_id,
                option=option,
                theoretical_price=price_to_quote,
                credit=dynamic_credit + extra_credit,
                volume=optimal_volume,
                position_limit=100,
                tick_size=0.10,
                total_portfolio_delta=preliminary_delta,
                position_skew=position_skew
            )

            time.sleep(0.5)

        total_delta = hedge_delta_position(STOCK_ID, options, stock_value)

        # print("\n" + "="*50)
        # print(f"ESTADO - {dt.datetime.now().strftime('%H:%M:%S')}")
        # print("-"*50)
        positions = exchange.get_positions()
        
        # blocked_count = 0
        # for instrument_id, pos in positions.items():
        #     if pos != 0:
        #         side = "LONG" if pos > 0 else "SHORT"
                
        #         # if abs(pos) >= 95:
        #         #     warning = " 🔴 UNWINDING!"
        #         #     blocked_count += 1
        #         # elif abs(pos) > 80:
        #         #     warning = " ⚠️  CRÍTICO"
        #         # elif abs(pos) > 60:
        #         #     warning = " ⚡ Alto"
        #         # else:
        #         #     warning = ""
                
        #         print(f"{instrument_id:25} | {side:5} | {pos:4d}")
        # print()

        # ops_count = len(exchange.poll_new_trades(STOCK_ID))
        # for option_id in options:
        #     ops_count += len(exchange.poll_new_trades(option_id))

        # pnl_actual_total = exchange.get_pnl()
        # pnl_este_bloque = pnl_actual_total - pnl_inicio_intervalo

        # print(f"\no/s: {ops_count} | DELTA: {preliminary_delta:6.2f} | PnL: {pnl_este_bloque:10.2f}")
        # print("="*50 + "\n")
        
        time.sleep(0.1)