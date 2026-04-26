"""
Generated Round 3 Wave 2 learning bot.
Batch spec: spec_learning_batch_wave2.md
Bot ID: W2-01
Family: delta1 champion control
Hypothesis: The best clean base architecture after Wave 1 is still a compact HYDRO plus VEX delta-1 stack.
"""

import json
import math
from datamodel import Order, TradingState


CONFIG = {'bot_id': 'W2-01',
 'family': 'delta1 champion control',
 'features': ['delta1 control', 'dual branch base'],
 'filename': 'candidate_w2_01_delta1_dual_control.py',
 'hypothesis': 'The best clean base architecture after Wave 1 is still a compact HYDRO plus VEX '
               'delta-1 stack.',
 'kind': 'delta1',
 'products': [{'aggressive_size': 14,
               'edge': 2,
               'imbalance_weight': 0.0,
               'inventory_skew': 5.0,
               'limit': 200,
               'max_spread': 18,
               'mode': 'reversion',
               'passive_only': False,
               'passive_size': 8,
               'passive_step': 1,
               'quote_offset': 6,
               'reversion_weight': 0.4,
               'symbol': 'HYDROGEL_PACK',
               'trade_threshold': 0.0},
              {'aggressive_size': 16,
               'edge': 1,
               'imbalance_weight': 0.0,
               'inventory_skew': 4.0,
               'limit': 200,
               'max_spread': 6,
               'mode': 'reversion',
               'passive_only': False,
               'passive_size': 10,
               'passive_step': 1,
               'quote_offset': 2,
               'reversion_weight': 0.45,
               'symbol': 'VELVETFRUIT_EXTRACT',
               'trade_threshold': 0.0}]}

SQRT_2 = math.sqrt(2.0)
SQRT_2PI = math.sqrt(2.0 * math.pi)
DEFAULT_SIGMA = 90.0
DEFAULT_SIGMA_FLOOR = 45.0
DEFAULT_SIGMA_CAP = 180.0
DEFAULT_SIGMA_ALPHA = 0.08
DEFAULT_SIGMA_MOVE_SCALE = 14.0
DEFAULT_TTE_DAYS = 5.0


def get_best_bid(order_depth):
    if not order_depth or not order_depth.buy_orders:
        return None
    return max(order_depth.buy_orders)


def get_best_ask(order_depth):
    if not order_depth or not order_depth.sell_orders:
        return None
    return min(order_depth.sell_orders)


def get_mid(order_depth):
    best_bid = get_best_bid(order_depth)
    best_ask = get_best_ask(order_depth)
    if best_bid is None or best_ask is None:
        return None
    return (best_bid + best_ask) / 2.0


def get_spread(order_depth):
    best_bid = get_best_bid(order_depth)
    best_ask = get_best_ask(order_depth)
    if best_bid is None or best_ask is None:
        return None
    return best_ask - best_bid


def get_imbalance(order_depth):
    best_bid = get_best_bid(order_depth)
    best_ask = get_best_ask(order_depth)
    if best_bid is None or best_ask is None:
        return 0.0
    bid_vol = int(order_depth.buy_orders[best_bid])
    ask_vol = abs(int(order_depth.sell_orders[best_ask]))
    total = bid_vol + ask_vol
    if total <= 0:
        return 0.0
    return (bid_vol - ask_vol) / float(total)


def sign(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def clamp_qty(qty, position, limit):
    if qty > 0:
        return max(0, min(int(qty), int(limit - position)))
    if qty < 0:
        return min(0, max(int(qty), int(-(limit + position))))
    return 0


def clamp_price(price, min_price=0, max_price=None):
    value = int(round(price))
    value = max(int(min_price), value)
    if max_price is not None:
        value = min(value, int(max_price))
    return value


def intrinsic_call(underlying_mid, strike):
    return max(float(underlying_mid) - float(strike), 0.0)


def norm_cdf(x):
    return 0.5 * (1.0 + math.erf(float(x) / SQRT_2))


def norm_pdf(x):
    return math.exp(-0.5 * float(x) * float(x)) / SQRT_2PI


def bachelier_call(underlying_mid, strike, tte_days, sigma_abs):
    if sigma_abs <= 0 or tte_days <= 0:
        return intrinsic_call(underlying_mid, strike)
    tte_years = float(tte_days) / 365.0
    vol_t = float(sigma_abs) * math.sqrt(max(tte_years, 1e-9))
    if vol_t <= 1e-9:
        return intrinsic_call(underlying_mid, strike)
    d = (float(underlying_mid) - float(strike)) / vol_t
    return max(0.0, (float(underlying_mid) - float(strike)) * norm_cdf(d) + vol_t * norm_pdf(d))


def load_data(raw):
    if not raw:
        return {}
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        return {}
    return {}


def save_data(data):
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def append_orders(result, symbol, orders):
    if not orders:
        return
    bucket = result.setdefault(symbol, [])
    bucket.extend(orders)


def take_from_asks(symbol, order_depth, position, limit, max_qty, max_price):
    orders = []
    remaining = max(0, int(max_qty))
    if remaining <= 0:
        return orders, position
    for ask in sorted(order_depth.sell_orders):
        if ask > max_price or remaining <= 0:
            break
        ask_vol = max(0, -int(order_depth.sell_orders[ask]))
        qty = clamp_qty(min(ask_vol, remaining), position, limit)
        if qty > 0:
            orders.append(Order(symbol, int(ask), int(qty)))
            position += qty
            remaining -= qty
    return orders, position


def hit_bids(symbol, order_depth, position, limit, max_qty, min_price):
    orders = []
    remaining = max(0, int(max_qty))
    if remaining <= 0:
        return orders, position
    for bid in sorted(order_depth.buy_orders, reverse=True):
        if bid < min_price or remaining <= 0:
            break
        bid_vol = max(0, int(order_depth.buy_orders[bid]))
        qty = clamp_qty(-min(bid_vol, remaining), position, limit)
        if qty < 0:
            orders.append(Order(symbol, int(bid), int(qty)))
            position += qty
            remaining -= abs(qty)
    return orders, position


def flatten_position(symbol, order_depth, position, limit):
    if position > 0:
        return hit_bids(symbol, order_depth, position, limit, abs(position), -10**9)
    if position < 0:
        return take_from_asks(symbol, order_depth, position, limit, abs(position), 10**9)
    return [], position


def passive_bid_price(fair, cfg, best_bid, best_ask):
    price = int(round(fair - cfg.get("quote_offset", 1)))
    step = int(cfg.get("passive_step", 1))
    if best_bid is not None:
        price = min(price, int(best_bid) + step)
        price = max(price, int(best_bid))
    if best_ask is not None:
        price = min(price, int(best_ask) - 1)
    return clamp_price(price, cfg.get("min_price", 0), cfg.get("max_price"))


def passive_ask_price(fair, cfg, best_bid, best_ask):
    price = int(round(fair + cfg.get("quote_offset", 1)))
    step = int(cfg.get("passive_step", 1))
    if best_ask is not None:
        price = max(price, int(best_ask) - step)
        price = min(price, int(best_ask))
    if best_bid is not None:
        price = max(price, int(best_bid) + 1)
    return clamp_price(price, cfg.get("min_price", 0), cfg.get("max_price"))


def sync_position_state(store, symbol, position, centered, timestamp):
    previous = store.get(symbol, {})
    previous_position = int(previous.get("last_position", 0))
    current = dict(previous)
    if position == 0:
        current = {"last_position": 0}
    elif previous_position == 0 or sign(previous_position) != sign(position):
        current = {
            "last_position": int(position),
            "entry_timestamp": int(timestamp),
            "entry_centered": float(centered),
        }
    else:
        current["last_position"] = int(position)
        current.setdefault("entry_timestamp", int(timestamp))
        current.setdefault("entry_centered", float(centered))
    current["last_centered"] = float(centered)
    store[symbol] = current
    return current


def should_take_profit(position, centered, position_state, cfg):
    if position == 0:
        return False
    entry_centered = float(position_state.get("entry_centered", centered))
    tp_improve = cfg.get("tp_improve")
    tp_abs_threshold = cfg.get("tp_abs_threshold")
    if position > 0:
        if tp_abs_threshold is not None and centered >= -float(tp_abs_threshold):
            return True
        if tp_improve is not None and centered - entry_centered >= float(tp_improve):
            return True
    if position < 0:
        if tp_abs_threshold is not None and centered <= float(tp_abs_threshold):
            return True
        if tp_improve is not None and entry_centered - centered >= float(tp_improve):
            return True
    return False


def should_stop_out(position, centered, position_state, cfg):
    stop_width = cfg.get("adverse_move_stop")
    if position == 0 or stop_width is None:
        return False
    entry_centered = float(position_state.get("entry_centered", centered))
    stop_width = float(stop_width)
    if position > 0 and entry_centered - centered >= stop_width:
        return True
    if position < 0 and centered - entry_centered >= stop_width:
        return True
    return False


def should_time_stop(position, timestamp, position_state, cfg):
    max_hold = cfg.get("max_hold")
    if position == 0 or max_hold is None:
        return False
    entry_timestamp = position_state.get("entry_timestamp")
    if entry_timestamp is None:
        return False
    return int(timestamp) - int(entry_timestamp) >= int(max_hold)


def should_late_flat(position, timestamp, cfg):
    hard_flat_after = cfg.get("hard_flat_after")
    if position == 0 or hard_flat_after is None:
        return False
    return int(timestamp) >= int(hard_flat_after)


def allow_new_entries(timestamp, cfg):
    no_new_entry_after = cfg.get("no_new_entry_after")
    if no_new_entry_after is None:
        return True
    return int(timestamp) < int(no_new_entry_after)


def buy_allowed_by_imbalance(imbalance, cfg):
    minimum = cfg.get("buy_imbalance_min")
    return minimum is None or imbalance >= float(minimum)


def sell_allowed_by_imbalance(imbalance, cfg):
    maximum = cfg.get("sell_imbalance_max")
    return maximum is None or imbalance <= float(maximum)


def update_sigma(data, vex_mid, config):
    voucher_meta = data.setdefault("voucher_meta", {})
    sigma_abs = float(voucher_meta.get("sigma_abs", config.get("sigma_abs_default", DEFAULT_SIGMA)))
    prev_vex_mid = voucher_meta.get("prev_vex_mid")
    sigma_floor = float(config.get("sigma_abs_floor", DEFAULT_SIGMA_FLOOR))
    sigma_cap = float(config.get("sigma_abs_cap", DEFAULT_SIGMA_CAP))
    sigma_alpha = float(config.get("sigma_alpha", DEFAULT_SIGMA_ALPHA))
    sigma_move_scale = float(config.get("sigma_move_scale", DEFAULT_SIGMA_MOVE_SCALE))
    if prev_vex_mid is not None:
        target = sigma_floor + sigma_move_scale * abs(float(vex_mid) - float(prev_vex_mid))
        target = max(sigma_floor, min(sigma_cap, target))
        sigma_abs = (1.0 - sigma_alpha) * sigma_abs + sigma_alpha * target
    voucher_meta["sigma_abs"] = sigma_abs
    voucher_meta["prev_vex_mid"] = float(vex_mid)
    return sigma_abs


def effective_limit(cfg):
    return int(cfg.get("working_limit", cfg["limit"]))


def run_delta1_products(state, result, data, products):
    last_mid = data.setdefault("delta_last_mid", {})
    for cfg in products:
        symbol = cfg["symbol"]
        order_depth = state.order_depths.get(symbol)
        if order_depth is None:
            continue
        mid = get_mid(order_depth)
        spread = get_spread(order_depth)
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        if mid is None or spread is None or best_bid is None or best_ask is None:
            continue
        if spread > cfg["max_spread"]:
            last_mid[symbol] = mid
            continue

        position = int(state.position.get(symbol, 0))
        limit = effective_limit(cfg)
        prev_mid = last_mid.get(symbol)
        imbalance = get_imbalance(order_depth)
        signal = 0.0
        if cfg["mode"] in ("reversion", "hybrid") and prev_mid is not None:
            signal += float(cfg["reversion_weight"]) * (float(prev_mid) - float(mid))
        if cfg["mode"] in ("imbalance", "hybrid"):
            signal += float(cfg["imbalance_weight"]) * imbalance

        fair = float(mid) + signal - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
        trade_threshold = float(cfg.get("trade_threshold", 0.0))
        orders = []

        if not cfg.get("passive_only", False) and abs(signal) >= trade_threshold:
            if signal > 0:
                new_orders, position = take_from_asks(
                    symbol,
                    order_depth,
                    position,
                    limit,
                    cfg.get("aggressive_size", cfg["passive_size"]),
                    fair - cfg["edge"],
                )
                orders.extend(new_orders)
            elif signal < 0:
                new_orders, position = hit_bids(
                    symbol,
                    order_depth,
                    position,
                    limit,
                    cfg.get("aggressive_size", cfg["passive_size"]),
                    fair + cfg["edge"],
                )
                orders.extend(new_orders)

        buy_qty = clamp_qty(cfg["passive_size"], position, limit)
        sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
        quote_buy = True
        quote_sell = True
        if abs(signal) >= trade_threshold:
            if signal > 0:
                quote_sell = False
            elif signal < 0:
                quote_buy = False

        if quote_buy and buy_qty > 0:
            price = passive_bid_price(fair, cfg, best_bid, best_ask)
            orders.append(Order(symbol, int(price), int(buy_qty)))
        if quote_sell and sell_qty < 0:
            price = passive_ask_price(fair, cfg, best_bid, best_ask)
            orders.append(Order(symbol, int(price), int(sell_qty)))

        append_orders(result, symbol, orders)
        last_mid[symbol] = mid


def run_voucher_products(state, result, data, config):
    sidecars = config.get("sidecar_products", [])
    if sidecars:
        run_delta1_products(state, result, data, sidecars)

    vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    sigma_abs = update_sigma(data, vex_mid, config)
    anchors = data.setdefault("voucher_anchor", {})
    position_states = data.setdefault("voucher_position_state", {})
    timestamp = int(getattr(state, "timestamp", 0))

    for cfg in config["products"]:
        symbol = cfg["symbol"]
        order_depth = state.order_depths.get(symbol)
        if order_depth is None:
            continue
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        mid = get_mid(order_depth)
        spread = get_spread(order_depth)
        if best_bid is None or best_ask is None or mid is None or spread is None:
            continue

        position = int(state.position.get(symbol, 0))
        limit = effective_limit(cfg)
        imbalance = get_imbalance(order_depth)
        sigma_multiplier = float(cfg.get("sigma_multiplier", 1.0))
        fair_model = bachelier_call(
            vex_mid,
            cfg["strike"],
            config.get("tte_days", DEFAULT_TTE_DAYS),
            sigma_abs * sigma_multiplier,
        )
        raw_residual = float(mid) - float(fair_model)
        anchor = float(anchors.get(symbol, raw_residual))
        centered = raw_residual - anchor
        fair = (
            float(fair_model)
            + anchor
            - float(cfg["signal_weight"]) * centered
            - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
        )
        position_state = sync_position_state(position_states, symbol, position, centered, timestamp)
        orders = []
        force_exit = (
            should_late_flat(position, timestamp, cfg)
            or should_time_stop(position, timestamp, position_state, cfg)
            or should_stop_out(position, centered, position_state, cfg)
            or should_take_profit(position, centered, position_state, cfg)
        )

        if force_exit:
            exit_orders, position = flatten_position(symbol, order_depth, position, limit)
            orders.extend(exit_orders)
        elif spread <= cfg["max_spread"]:
            want_buy = centered < -float(cfg["entry_threshold"])
            want_sell = centered > float(cfg["entry_threshold"])
            if want_buy and not buy_allowed_by_imbalance(imbalance, cfg):
                want_buy = False
            if want_sell and not sell_allowed_by_imbalance(imbalance, cfg):
                want_sell = False

            if allow_new_entries(timestamp, cfg) and not cfg.get("passive_only", False):
                if want_buy:
                    active_orders, position = take_from_asks(
                        symbol,
                        order_depth,
                        position,
                        limit,
                        cfg.get("aggressive_size", cfg["passive_size"]),
                        fair + cfg["cross_pad"],
                    )
                    orders.extend(active_orders)
                elif want_sell:
                    active_orders, position = hit_bids(
                        symbol,
                        order_depth,
                        position,
                        limit,
                        cfg.get("aggressive_size", cfg["passive_size"]),
                        fair - cfg["cross_pad"],
                    )
                    orders.extend(active_orders)

            buy_qty = clamp_qty(cfg["passive_size"], position, limit)
            sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
            quote_buy = False
            quote_sell = False

            if allow_new_entries(timestamp, cfg):
                if want_buy:
                    quote_buy = True
                elif want_sell:
                    quote_sell = True
                elif cfg.get("neutral_two_sided", False):
                    quote_buy = True
                    quote_sell = True

            if cfg.get("inventory_exit_quotes", True):
                if position > 0:
                    quote_sell = True
                elif position < 0:
                    quote_buy = True

            if quote_buy and buy_qty > 0:
                buy_price = passive_bid_price(fair, cfg, best_bid, best_ask)
                orders.append(Order(symbol, int(buy_price), int(buy_qty)))
            if quote_sell and sell_qty < 0:
                sell_price = passive_ask_price(fair, cfg, best_bid, best_ask)
                orders.append(Order(symbol, int(sell_price), int(sell_qty)))

        append_orders(result, symbol, orders)
        alpha = float(cfg.get("anchor_alpha", config.get("default_anchor_alpha", 0.02)))
        anchors[symbol] = (1.0 - alpha) * anchor + alpha * raw_residual


def run_floor_products(state, result, data, products):
    del data
    for cfg in products:
        symbol = cfg["symbol"]
        order_depth = state.order_depths.get(symbol)
        if order_depth is None:
            continue
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        spread = None
        if best_bid is not None and best_ask is not None:
            spread = best_ask - best_bid

        position = int(state.position.get(symbol, 0))
        limit = effective_limit(cfg)
        orders = []

        if best_ask is not None and best_ask <= int(cfg["cross_buy_at_or_below"]):
            active_orders, position = take_from_asks(symbol, order_depth, position, limit, cfg["passive_size"], best_ask)
            orders.extend(active_orders)
        if best_bid is not None and best_bid >= int(cfg["cross_sell_at_or_above"]):
            if cfg.get("allow_short", False) or position > 0:
                active_orders, position = hit_bids(symbol, order_depth, position, limit, cfg["passive_size"], best_bid)
                orders.extend(active_orders)

        if spread is not None and spread >= int(cfg.get("passive_when_spread_at_least", 1)):
            buy_qty = clamp_qty(cfg["passive_size"], position, limit)
            sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
            if buy_qty > 0:
                orders.append(Order(symbol, int(cfg["bid_price"]), int(buy_qty)))
            if sell_qty < 0 and (cfg.get("allow_short", False) or position > 0):
                orders.append(Order(symbol, int(cfg["ask_price"]), int(sell_qty)))

        append_orders(result, symbol, orders)


class Trader:
    def run(self, state: TradingState):
        result = {}
        conversions = 0
        data = load_data(state.traderData)
        kind = CONFIG["kind"]
        if kind == "delta1":
            run_delta1_products(state, result, data, CONFIG["products"])
        elif kind == "voucher":
            run_voucher_products(state, result, data, CONFIG)
        elif kind == "floor":
            run_floor_products(state, result, data, CONFIG["products"])
        return result, conversions, save_data(data)
