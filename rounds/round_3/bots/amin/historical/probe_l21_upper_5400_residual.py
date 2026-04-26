"""
Generated Round 3 learning bot.
Batch spec: spec_learning_batch_wave1.md
Bot ID: L21
Family: upper residual
Hypothesis: VEV_5400 now deserves a direct live learner because the logger showed movement plus tight spreads.
"""

import json
from datamodel import Order, TradingState


CONFIG = {
    "bot_id": "L21",
    "family": "upper residual",
    "filename": "probe_l21_upper_5400_residual.py",
    "hypothesis": "VEV_5400 now deserves a direct live learner because the logger showed movement plus tight spreads.",
    "kind": "voucher",
    "products": [
        {
            "cross_pad": 0.3,
            "entry_threshold": 0.8,
            "exit_threshold": 0.3,
            "inventory_skew": 0.8,
            "limit": 300,
            "max_spread": 2,
            "passive_size": 12,
            "quote_offset": 1,
            "signal_weight": 0.75,
            "strike": 5400,
            "symbol": "VEV_5400"
        }
    ]
}


def get_mid(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders)
    best_ask = min(order_depth.sell_orders)
    return (best_bid + best_ask) / 2.0


def get_spread(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    return min(order_depth.sell_orders) - max(order_depth.buy_orders)


def get_imbalance(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return 0.0
    best_bid = max(order_depth.buy_orders)
    best_ask = min(order_depth.sell_orders)
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = abs(order_depth.sell_orders[best_ask])
    total = bid_vol + ask_vol
    if total <= 0:
        return 0.0
    return (bid_vol - ask_vol) / total


def clamp_qty(qty, position, limit):
    if qty > 0:
        return max(0, min(qty, limit - position))
    if qty < 0:
        return min(0, max(qty, -(limit + position)))
    return 0


def intrinsic_call(vex_mid, strike):
    return max(vex_mid - strike, 0.0)


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


def run_delta1_products(state, result, data, products):
    last_mid = data.setdefault("delta_last_mid", {})
    for cfg in products:
        symbol = cfg["symbol"]
        if symbol not in state.order_depths:
            continue
        od = state.order_depths[symbol]
        mid = get_mid(od)
        spread = get_spread(od)
        if mid is None or spread is None or spread > cfg["max_spread"]:
            continue

        position = state.position.get(symbol, 0)
        imbalance = get_imbalance(od)
        prev_mid = last_mid.get(symbol)

        signal = 0.0
        if cfg["mode"] in ("reversion", "hybrid") and prev_mid is not None:
            signal += cfg["reversion_weight"] * (prev_mid - mid)
        if cfg["mode"] in ("imbalance", "hybrid"):
            signal += cfg["imbalance_weight"] * imbalance

        fair = mid + signal - cfg["inventory_skew"] * (position / cfg["limit"])
        orders = []

        for ask in sorted(od.sell_orders):
            ask_vol = -od.sell_orders[ask]
            if ask <= fair - cfg["edge"]:
                buy_qty = clamp_qty(ask_vol, position, cfg["limit"])
                if buy_qty > 0:
                    orders.append(Order(symbol, int(ask), int(buy_qty)))
                    position += buy_qty

        for bid in sorted(od.buy_orders, reverse=True):
            bid_vol = od.buy_orders[bid]
            if bid >= fair + cfg["edge"]:
                sell_qty = clamp_qty(-bid_vol, position, cfg["limit"])
                if sell_qty < 0:
                    orders.append(Order(symbol, int(bid), int(sell_qty)))
                    position += sell_qty

        buy_qty = clamp_qty(cfg["passive_size"], position, cfg["limit"])
        sell_qty = clamp_qty(-cfg["passive_size"], position, cfg["limit"])
        buy_price = int(round(fair - cfg["offset"]))
        sell_price = int(round(fair + cfg["offset"]))

        if buy_qty > 0:
            orders.append(Order(symbol, buy_price, int(buy_qty)))
        if sell_qty < 0:
            orders.append(Order(symbol, sell_price, int(sell_qty)))

        if orders:
            result[symbol] = orders
        last_mid[symbol] = mid


def run_voucher_products(state, result, data, config):
    sidecars = config.get("sidecar_products", [])
    if sidecars:
        run_delta1_products(state, result, data, sidecars)

    vex_symbol = "VELVETFRUIT_EXTRACT"
    vex_depth = state.order_depths.get(vex_symbol)
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    anchors = data.setdefault("voucher_anchor", {})
    passive_only = bool(config.get("passive_only", False))
    neutral_two_sided = bool(config.get("neutral_two_sided", False))
    for cfg in config["products"]:
        symbol = cfg["symbol"]
        if symbol not in state.order_depths:
            continue
        od = state.order_depths[symbol]
        mid = get_mid(od)
        spread = get_spread(od)
        if mid is None or spread is None or spread > cfg["max_spread"]:
            continue

        position = state.position.get(symbol, 0)
        anchor_key = symbol
        base_fair = intrinsic_call(vex_mid, cfg["strike"])
        raw_residual = mid - base_fair
        prev_anchor = float(anchors.get(anchor_key, raw_residual))
        centered = raw_residual - prev_anchor
        fair = (
            base_fair
            + prev_anchor
            - cfg["signal_weight"] * centered
            - cfg["inventory_skew"] * (position / cfg["limit"])
        )

        orders = []
        if not passive_only:
            if centered < -cfg["entry_threshold"]:
                for ask in sorted(od.sell_orders):
                    ask_vol = -od.sell_orders[ask]
                    if ask <= fair + cfg["cross_pad"]:
                        buy_qty = clamp_qty(ask_vol, position, cfg["limit"])
                        if buy_qty > 0:
                            orders.append(Order(symbol, int(ask), int(buy_qty)))
                            position += buy_qty
            elif centered > cfg["entry_threshold"]:
                for bid in sorted(od.buy_orders, reverse=True):
                    bid_vol = od.buy_orders[bid]
                    if bid >= fair - cfg["cross_pad"]:
                        sell_qty = clamp_qty(-bid_vol, position, cfg["limit"])
                        if sell_qty < 0:
                            orders.append(Order(symbol, int(bid), int(sell_qty)))
                            position += sell_qty

        passive_size = cfg["passive_size"]
        buy_qty = clamp_qty(passive_size, position, cfg["limit"])
        sell_qty = clamp_qty(-passive_size, position, cfg["limit"])
        buy_price = int(round(fair - cfg["quote_offset"]))
        sell_price = int(round(fair + cfg["quote_offset"]))

        if centered < -cfg["entry_threshold"]:
            if buy_qty > 0:
                orders.append(Order(symbol, buy_price, int(buy_qty)))
        elif centered > cfg["entry_threshold"]:
            if sell_qty < 0:
                orders.append(Order(symbol, sell_price, int(sell_qty)))
        elif neutral_two_sided:
            if buy_qty > 0:
                orders.append(Order(symbol, buy_price, int(buy_qty)))
            if sell_qty < 0:
                orders.append(Order(symbol, sell_price, int(sell_qty)))

        if orders:
            result[symbol] = orders
        anchors[anchor_key] = (1.0 - 0.02) * prev_anchor + 0.02 * raw_residual


def run_surface_pairs(state, result, data, config):
    vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    anchors = data.setdefault("surface_anchor", {})
    for cfg in config["pairs"]:
        left = cfg["left_symbol"]
        right = cfg["right_symbol"]
        if left not in state.order_depths or right not in state.order_depths:
            continue

        left_od = state.order_depths[left]
        right_od = state.order_depths[right]
        left_mid = get_mid(left_od)
        right_mid = get_mid(right_od)
        left_spread = get_spread(left_od)
        right_spread = get_spread(right_od)
        if (
            left_mid is None
            or right_mid is None
            or left_spread is None
            or right_spread is None
            or left_spread > cfg["left_max_spread"]
            or right_spread > cfg["right_max_spread"]
        ):
            continue

        left_pos = state.position.get(left, 0)
        right_pos = state.position.get(right, 0)
        left_extr = left_mid - intrinsic_call(vex_mid, cfg["left_strike"])
        right_extr = right_mid - intrinsic_call(vex_mid, cfg["right_strike"])
        raw_pair = left_extr - right_extr
        key = left + "__" + right
        prev_anchor = float(anchors.get(key, raw_pair))
        centered = raw_pair - prev_anchor
        orders_left = result.setdefault(left, [])
        orders_right = result.setdefault(right, [])
        size = int(cfg["size"])

        if centered > cfg["threshold"]:
            left_bid = max(left_od.buy_orders) if left_od.buy_orders else None
            right_ask = min(right_od.sell_orders) if right_od.sell_orders else None
            if left_bid is not None and right_ask is not None:
                sell_qty = clamp_qty(-size, left_pos, cfg["left_limit"])
                buy_qty = clamp_qty(size, right_pos, cfg["right_limit"])
                if sell_qty < 0:
                    orders_left.append(Order(left, int(left_bid), int(sell_qty)))
                    left_pos += sell_qty
                if buy_qty > 0:
                    orders_right.append(Order(right, int(right_ask), int(buy_qty)))
                    right_pos += buy_qty
        elif centered < -cfg["threshold"]:
            left_ask = min(left_od.sell_orders) if left_od.sell_orders else None
            right_bid = max(right_od.buy_orders) if right_od.buy_orders else None
            if left_ask is not None and right_bid is not None:
                buy_qty = clamp_qty(size, left_pos, cfg["left_limit"])
                sell_qty = clamp_qty(-size, right_pos, cfg["right_limit"])
                if buy_qty > 0:
                    orders_left.append(Order(left, int(left_ask), int(buy_qty)))
                    left_pos += buy_qty
                if sell_qty < 0:
                    orders_right.append(Order(right, int(right_bid), int(sell_qty)))
                    right_pos += sell_qty

        anchors[key] = (1.0 - cfg["anchor_alpha"]) * prev_anchor + cfg["anchor_alpha"] * raw_pair


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
        elif kind == "surface_pair":
            run_surface_pairs(state, result, data, CONFIG)

        traderData = save_data(data)
        return result, conversions, traderData
