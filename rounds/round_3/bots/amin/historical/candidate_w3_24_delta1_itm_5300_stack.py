"""
Generated Round 3 Wave 3 learning bot.
Batch spec: spec_learning_batch_wave3.md
Bot ID: W3-24
Family: delta1 plus itm plus tiny 5300 stack
Hypothesis: The last meaningful exploratory architecture is a near-final stack: delta-1 core, ITM add-on, and only a microscopic tightly gated 5300 overlay.
"""

import json
import math
from datamodel import Order, TradingState


CONFIG = {'bot_id': 'W3-24',
 'family': 'delta1 plus itm plus tiny 5300 stack',
 'features': ['champion base', 'itm overlay', 'micro 5300 overlay'],
 'filename': 'candidate_w3_24_delta1_itm_5300_stack.py',
 'hypothesis': 'The last meaningful exploratory architecture is a near-final stack: delta-1 core, '
               'ITM add-on, and only a microscopic tightly gated 5300 overlay.',
 'kind': 'voucher',
 'products': [{'aggressive_size': 2,
               'anchor_alpha': 0.015,
               'cross_pad': 0.25,
               'entry_threshold': 0.95,
               'hard_flat_after': 880000,
               'inventory_exit_quotes': True,
               'inventory_skew': 0.8,
               'limit': 300,
               'max_spread': 24,
               'min_price': 0,
               'neutral_two_sided': False,
               'no_new_entry_after': 760000,
               'passive_only': False,
               'passive_size': 2,
               'passive_step': 1,
               'quote_offset': 3,
               'sigma_multiplier': 1.0,
               'signal_weight': 0.42,
               'strike': 4000,
               'symbol': 'VEV_4000',
               'working_limit': 30},
              {'aggressive_size': 2,
               'anchor_alpha': 0.015,
               'cross_pad': 0.2,
               'entry_threshold': 0.85,
               'hard_flat_after': 880000,
               'inventory_exit_quotes': True,
               'inventory_skew': 0.8,
               'limit': 300,
               'max_spread': 18,
               'min_price': 0,
               'neutral_two_sided': False,
               'no_new_entry_after': 760000,
               'passive_only': False,
               'passive_size': 2,
               'passive_step': 1,
               'quote_offset': 2,
               'sigma_multiplier': 1.0,
               'signal_weight': 0.42,
               'strike': 4500,
               'symbol': 'VEV_4500',
               'working_limit': 30},
              {'aggressive_size': 2,
               'anchor_alpha': 0.025,
               'cross_pad': 0.4,
               'entry_threshold': 1.0,
               'hard_flat_after': 620000,
               'inventory_exit_quotes': True,
               'inventory_skew': 1.0,
               'limit': 300,
               'max_spread': 3,
               'min_price': 0,
               'neutral_two_sided': False,
               'no_new_entry_after': 300000,
               'passive_only': False,
               'passive_size': 1,
               'passive_step': 1,
               'quote_offset': 1,
               'sigma_multiplier': 1.0,
               'signal_weight': 0.88,
               'strike': 5300,
               'symbol': 'VEV_5300',
               'vex_move_cap': 5.5,
               'vex_slope_cap': 1.2,
               'working_limit': 20}],
 'sidecar_products': [{'aggressive_size': 14,
                       'edge': 2,
                       'imbalance_weight': 0.0,
                       'inventory_exit_quotes': True,
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
                       'inventory_exit_quotes': True,
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
    previous = dict(store.get(symbol, {}))
    previous_position = int(previous.get("last_position", 0))
    block_until = previous.get("block_until")
    if position == 0:
        current = {"last_position": 0}
    elif previous_position == 0 or sign(previous_position) != sign(position):
        current = {
            "last_position": int(position),
            "entry_timestamp": int(timestamp),
            "entry_centered": float(centered),
            "best_improvement": 0.0,
        }
    else:
        current = previous
        current["last_position"] = int(position)
        current.setdefault("entry_timestamp", int(timestamp))
        current.setdefault("entry_centered", float(centered))
        current.setdefault("best_improvement", 0.0)
    if block_until is not None and int(block_until) > int(timestamp):
        current["block_until"] = int(block_until)
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


def update_position_progress(position, centered, position_state):
    if position == 0:
        position_state["best_improvement"] = 0.0
        return 0.0, 0.0
    entry_centered = float(position_state.get("entry_centered", centered))
    if position > 0:
        improvement = float(centered) - entry_centered
    else:
        improvement = entry_centered - float(centered)
    best_improvement = max(float(position_state.get("best_improvement", 0.0)), improvement)
    position_state["best_improvement"] = best_improvement
    return improvement, best_improvement


def should_giveback_stop(position, improvement, best_improvement, cfg):
    giveback_stop = cfg.get("giveback_stop")
    if position == 0 or giveback_stop is None:
        return False
    activation = float(cfg.get("giveback_activation", 0.0))
    if best_improvement < activation:
        return False
    return best_improvement - improvement >= float(giveback_stop)


def set_reentry_cooldown(position_state, timestamp, cfg):
    cooldown = cfg.get("reentry_cooldown")
    if cooldown is None:
        return
    position_state["block_until"] = int(timestamp) + int(cooldown)


def allow_new_entries(timestamp, cfg, position_state=None):
    regime_start_after = cfg.get("regime_start_after")
    if regime_start_after is not None and int(timestamp) < int(regime_start_after):
        return False
    no_new_entry_after = cfg.get("no_new_entry_after")
    if no_new_entry_after is not None and int(timestamp) >= int(no_new_entry_after):
        return False
    if position_state is not None:
        block_until = position_state.get("block_until")
        if block_until is not None and int(timestamp) < int(block_until):
            return False
    return True


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


def append_history(store, key, value, max_len):
    size = max(2, int(max_len))
    history = list(store.get(key, []))
    history.append(float(value))
    if len(history) > size:
        history = history[-size:]
    store[key] = history
    return history


def ema_update(previous, value, alpha):
    if previous is None:
        return float(value)
    alpha = float(alpha)
    return (1.0 - alpha) * float(previous) + alpha * float(value)


def rolling_slope(values):
    n = len(values)
    if n < 2:
        return 0.0
    mean_x = 0.5 * float(n - 1)
    mean_y = sum(float(v) for v in values) / float(n)
    denom = sum((float(i) - mean_x) ** 2 for i in range(n))
    if denom <= 0:
        return 0.0
    numer = sum((float(i) - mean_x) * (float(v) - mean_y) for i, v in enumerate(values))
    return numer / denom


def kalman_update(store, observation, process_var, obs_var):
    observation = float(observation)
    process_var = max(1e-6, float(process_var))
    obs_var = max(1e-6, float(obs_var))
    mean = float(store.get("mean", observation))
    variance = float(store.get("variance", obs_var))
    variance += process_var
    gain = variance / (variance + obs_var)
    mean = mean + gain * (observation - mean)
    variance = (1.0 - gain) * variance
    store["mean"] = mean
    store["variance"] = variance
    return mean


def update_delta_metrics(data, symbol, mid, cfg):
    delta_state = data.setdefault("delta_state", {})
    store = delta_state.setdefault(symbol, {})
    prev_mid = store.get("prev_mid")
    ema_mid = ema_update(store.get("ema_mid"), mid, cfg.get("ema_alpha", 0.25))
    history = append_history(store, "mid_history", mid, cfg.get("slope_window", 6))
    slope = rolling_slope(history)
    move = 0.0 if prev_mid is None else float(mid) - float(prev_mid)
    move_ema = ema_update(store.get("move_ema"), abs(move), cfg.get("move_alpha", 0.25))
    kalman_state = store.setdefault("kalman", {})
    kalman_mean = kalman_update(
        kalman_state,
        mid,
        cfg.get("kalman_process_var", 2.0),
        cfg.get("kalman_obs_var", 12.0),
    )
    store["prev_mid"] = float(mid)
    store["ema_mid"] = ema_mid
    store["move_ema"] = move_ema
    return {
        "prev_mid": prev_mid,
        "ema_mid": ema_mid,
        "move": move,
        "move_ema": move_ema,
        "slope": slope,
        "kalman_mean": kalman_mean,
        "kalman_gap": float(mid) - float(kalman_mean),
    }


def update_vex_metrics(data, vex_mid, vex_imbalance, config):
    voucher_meta = data.setdefault("voucher_meta", {})
    prev_mid = voucher_meta.get("prev_vex_mid")
    ema_mid = ema_update(voucher_meta.get("ema_vex_mid"), vex_mid, config.get("vex_ema_alpha", 0.25))
    history = append_history(voucher_meta, "vex_mid_history", vex_mid, config.get("vex_slope_window", 8))
    slope = rolling_slope(history)
    move = 0.0 if prev_mid is None else float(vex_mid) - float(prev_mid)
    move_ema = ema_update(voucher_meta.get("vex_move_ema"), abs(move), config.get("vex_move_alpha", 0.25))
    kalman_state = voucher_meta.setdefault("vex_kalman", {})
    kalman_mean = kalman_update(
        kalman_state,
        vex_mid,
        config.get("vex_kalman_process_var", 1.0),
        config.get("vex_kalman_obs_var", 8.0),
    )
    voucher_meta["prev_vex_mid"] = float(vex_mid)
    voucher_meta["ema_vex_mid"] = ema_mid
    voucher_meta["vex_move_ema"] = move_ema
    voucher_meta["vex_last_imbalance"] = float(vex_imbalance)
    return {
        "prev_mid": prev_mid,
        "ema_mid": ema_mid,
        "move": move,
        "move_ema": move_ema,
        "slope": slope,
        "kalman_mean": kalman_mean,
        "kalman_gap": float(vex_mid) - float(kalman_mean),
        "imbalance": float(vex_imbalance),
    }


def get_reference_mid(metrics, cfg):
    mode = cfg.get("fair_mode", "prev_mid")
    if mode == "kalman":
        return metrics["kalman_mean"]
    if mode == "ema":
        return metrics["ema_mid"]
    return metrics["prev_mid"]


def under_cap(value, cap):
    if cap is None:
        return True
    return abs(float(value)) <= float(cap)


def delta_regime_ok(metrics, spread, imbalance, cfg):
    if cfg.get("regime_max_spread") is not None and float(spread) > float(cfg["regime_max_spread"]):
        return False
    if not under_cap(metrics["move"], cfg.get("regime_abs_move_cap")):
        return False
    if not under_cap(metrics["slope"], cfg.get("regime_abs_slope_cap")):
        return False
    if not under_cap(metrics["ema_mid"] - metrics["kalman_mean"], cfg.get("regime_abs_ema_gap_cap")):
        return False
    if not under_cap(metrics["kalman_gap"], cfg.get("regime_abs_kalman_gap_cap")):
        return False
    if not under_cap(imbalance, cfg.get("regime_abs_imbalance_cap")):
        return False
    return True


def voucher_regime_ok(vex_metrics, spread, cfg, timestamp):
    regime_stop_after = cfg.get("regime_stop_after")
    if regime_stop_after is not None and int(timestamp) >= int(regime_stop_after):
        return False
    if spread > cfg["max_spread"]:
        return False
    if not under_cap(vex_metrics["move"], cfg.get("vex_move_cap")):
        return False
    if not under_cap(vex_metrics["move_ema"], cfg.get("vex_move_ema_cap")):
        return False
    if not under_cap(vex_metrics["slope"], cfg.get("vex_slope_cap")):
        return False
    if not under_cap(vex_metrics["kalman_gap"], cfg.get("vex_kalman_gap_cap")):
        return False
    if not under_cap(vex_metrics["imbalance"], cfg.get("vex_abs_imbalance_cap")):
        return False
    return True


def dynamic_entry_threshold(base, spread, vex_metrics, cfg):
    threshold = float(base)
    threshold += abs(float(vex_metrics["move"])) * float(cfg.get("vex_move_weight", 0.0))
    threshold += abs(float(vex_metrics["move_ema"])) * float(cfg.get("vex_move_ema_weight", 0.0))
    threshold += abs(float(vex_metrics["slope"])) * float(cfg.get("vex_slope_weight", 0.0))
    threshold += abs(float(vex_metrics["kalman_gap"])) * float(cfg.get("vex_kalman_gap_weight", 0.0))
    spread_ref = float(cfg.get("spread_ref", 0.0))
    threshold += max(0.0, float(spread) - spread_ref) * float(cfg.get("spread_excess_weight", 0.0))
    return threshold


def apply_trend_gate(want_buy, want_sell, vex_metrics, cfg):
    slope = float(vex_metrics["slope"])
    buy_max = cfg.get("buy_vex_slope_max")
    buy_min = cfg.get("buy_vex_slope_min")
    sell_max = cfg.get("sell_vex_slope_max")
    sell_min = cfg.get("sell_vex_slope_min")
    if want_buy and buy_max is not None and slope > float(buy_max):
        want_buy = False
    if want_buy and buy_min is not None and slope < float(buy_min):
        want_buy = False
    if want_sell and sell_max is not None and slope > float(sell_max):
        want_sell = False
    if want_sell and sell_min is not None and slope < float(sell_min):
        want_sell = False
    return want_buy, want_sell


def effective_limit(cfg):
    return int(cfg.get("working_limit", cfg["limit"]))


def run_delta1_products(state, result, data, products):
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

        metrics = update_delta_metrics(data, symbol, mid, cfg)
        if spread > cfg["max_spread"]:
            continue

        position = int(state.position.get(symbol, 0))
        limit = effective_limit(cfg)
        imbalance = get_imbalance(order_depth)
        reference_mid = get_reference_mid(metrics, cfg)
        signal = 0.0
        if cfg["mode"] in ("reversion", "hybrid") and reference_mid is not None:
            signal += float(cfg["reversion_weight"]) * (float(reference_mid) - float(mid))
        if cfg["mode"] in ("imbalance", "hybrid"):
            signal += float(cfg["imbalance_weight"]) * imbalance

        fair = float(mid) + signal - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
        trade_threshold = float(cfg.get("trade_threshold", 0.0))
        regime_ok = delta_regime_ok(metrics, spread, imbalance, cfg)
        orders = []

        if regime_ok and not cfg.get("passive_only", False) and abs(signal) >= trade_threshold:
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
        quote_buy = False
        quote_sell = False
        if regime_ok:
            quote_buy = True
            quote_sell = True
            if abs(signal) >= trade_threshold:
                if signal > 0:
                    quote_sell = False
                elif signal < 0:
                    quote_buy = False

        if cfg.get("inventory_exit_quotes", True):
            if position > 0:
                quote_sell = True
            elif position < 0:
                quote_buy = True

        if quote_buy and buy_qty > 0:
            price = passive_bid_price(fair, cfg, best_bid, best_ask)
            orders.append(Order(symbol, int(price), int(buy_qty)))
        if quote_sell and sell_qty < 0:
            price = passive_ask_price(fair, cfg, best_bid, best_ask)
            orders.append(Order(symbol, int(price), int(sell_qty)))

        append_orders(result, symbol, orders)


def run_voucher_products(state, result, data, config):
    sidecars = config.get("sidecar_products", [])
    if sidecars:
        run_delta1_products(state, result, data, sidecars)

    vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    vex_imbalance = get_imbalance(vex_depth) if vex_depth is not None else 0.0
    sigma_abs = update_sigma(data, vex_mid, config)
    vex_metrics = update_vex_metrics(data, vex_mid, vex_imbalance, config)
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
        anchor_mode = cfg.get("underlying_anchor_mode", config.get("underlying_anchor_mode", "mid"))
        underlying_mid = vex_metrics["kalman_mean"] if anchor_mode == "kalman" else vex_mid
        sigma_multiplier = float(cfg.get("sigma_multiplier", 1.0))
        fair_model = bachelier_call(
            underlying_mid,
            cfg["strike"],
            config.get("tte_days", DEFAULT_TTE_DAYS),
            sigma_abs * sigma_multiplier,
        )
        raw_residual = float(mid) - float(fair_model)
        anchor = float(anchors.get(symbol, raw_residual))
        centered = raw_residual - anchor
        direction_mode = cfg.get("direction_mode", "normal")
        direction_sign = -1.0 if direction_mode == "normal" else 1.0
        fair = (
            float(fair_model)
            + anchor
            + direction_sign * float(cfg["signal_weight"]) * centered
            - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
        )
        position_state = sync_position_state(position_states, symbol, position, centered, timestamp)
        improvement, best_improvement = update_position_progress(position, centered, position_state)
        orders = []
        giveback_exit = should_giveback_stop(position, improvement, best_improvement, cfg)
        force_exit = (
            should_late_flat(position, timestamp, cfg)
            or should_time_stop(position, timestamp, position_state, cfg)
            or should_stop_out(position, centered, position_state, cfg)
            or should_take_profit(position, centered, position_state, cfg)
            or giveback_exit
        )

        if force_exit:
            if giveback_exit or should_stop_out(position, centered, position_state, cfg):
                set_reentry_cooldown(position_state, timestamp, cfg)
            exit_orders, position = flatten_position(symbol, order_depth, position, limit)
            orders.extend(exit_orders)
        elif spread <= cfg["max_spread"]:
            entry_threshold = dynamic_entry_threshold(cfg["entry_threshold"], spread, vex_metrics, cfg)
            if direction_mode == "inverse":
                want_buy = centered > float(entry_threshold)
                want_sell = centered < -float(entry_threshold)
            else:
                want_buy = centered < -float(entry_threshold)
                want_sell = centered > float(entry_threshold)
            want_buy, want_sell = apply_trend_gate(want_buy, want_sell, vex_metrics, cfg)
            if want_buy and not buy_allowed_by_imbalance(imbalance, cfg):
                want_buy = False
            if want_sell and not sell_allowed_by_imbalance(imbalance, cfg):
                want_sell = False

            regime_ok = voucher_regime_ok(vex_metrics, spread, cfg, timestamp)
            entries_allowed = regime_ok and allow_new_entries(timestamp, cfg, position_state)

            if entries_allowed and not cfg.get("passive_only", False):
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

            if entries_allowed:
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
