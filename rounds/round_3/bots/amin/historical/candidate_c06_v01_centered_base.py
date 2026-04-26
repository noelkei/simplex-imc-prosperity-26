"""
C06 Composite Base Trader (fresh corrected challenger) — Round 3
Spec: spec_c06_composite_base.md
Components: C01 (HYDROGEL_PACK MM) + C02 (VELVETFRUIT_EXTRACT MM) + C03 (centered Bachelier residual reversion)
Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ---------------------------------------------------------------------------
# Normal-distribution helpers (West 2004 rational approximation)
# ---------------------------------------------------------------------------

def norm_cdf(x: float) -> float:
    """Cumulative normal distribution via rational approximation."""
    if x < -8.0:
        return 0.0
    if x > 8.0:
        return 1.0
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    sign = 1.0
    if x < 0:
        sign = -1.0
        x = -x
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + sign * y)


def norm_pdf(x: float) -> float:
    """Standard normal probability density function."""
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------
# Bachelier (normal-model) call price
# ---------------------------------------------------------------------------

def bachelier_call(S: float, K: float, T_years: float, sigma_abs: float) -> float:
    """
    Bachelier model call price.
    C = (S - K) * N(d) + sigma_abs * sqrt(T) * phi(d)
    d = (S - K) / (sigma_abs * sqrt(T))
    """
    if T_years <= 0 or sigma_abs <= 0:
        return max(S - K, 0.0)
    vol_sqrt_t = sigma_abs * math.sqrt(T_years)
    if vol_sqrt_t < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vol_sqrt_t
    return (S - K) * norm_cdf(d) + vol_sqrt_t * norm_pdf(d)


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

# Delta-1 market-making
MM_OFFSET = 2
MM_EDGE = 1
IMBALANCE_LEAN = 1
MAX_DELTA1_SPREAD = 8

# Voucher residual reversion
ENTRY_THRESHOLD = 3.0
EXIT_THRESHOLD = 0.5
VOUCHER_MM_OFFSET = 2
MAX_VOUCHER_SPREAD = 20
SIGMA_ABS_DEFAULT = 95.0
TTE_DAYS = 5
TTE_YEARS = TTE_DAYS / 365.0
RESIDUAL_ANCHOR_ALPHA = 0.01
SURFACE_MONO_TOL = 1.0
SURFACE_CONVEX_TOL = 1.0

# Position / inventory
INV_SKEW_FACTOR = 1.5
VOUCHER_INV_SKEW = 1.0

# Product configuration
DELTA1_PRODUCTS = {
    "HYDROGEL_PACK": 200,
    "VELVETFRUIT_EXTRACT": 200,
}

VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}

ALL_VOUCHER_STRIKES = sorted(VOUCHER_PRODUCTS.keys())


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_mid(order_depth) -> float | None:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    return (best_bid + best_ask) / 2.0


def get_spread(order_depth) -> float | None:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    return min(order_depth.sell_orders.keys()) - max(order_depth.buy_orders.keys())


def get_imbalance(order_depth) -> float:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return 0.0
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = abs(order_depth.sell_orders[best_ask])
    total = bid_vol + ask_vol
    if total == 0:
        return 0.0
    return (bid_vol - ask_vol) / total


def clamp_order_qty(qty: int, position: int, limit: int) -> int:
    if qty > 0:
        max_buy = limit - position
        return max(0, min(qty, max_buy))
    if qty < 0:
        max_sell = limit + position
        return min(0, max(qty, -max_sell))
    return 0


def get_observed_voucher_mids(order_depths) -> dict[str, float]:
    mids = {}
    for symbol in ALL_VOUCHER_STRIKES:
        order_depth = order_depths.get(symbol)
        if order_depth is None:
            continue
        mid = get_mid(order_depth)
        if mid is not None:
            mids[symbol] = mid
    return mids


def surface_guardrail_ok(observed_mids: dict[str, float]) -> bool:
    ordered = sorted(observed_mids.items(), key=lambda item: VOUCHER_PRODUCTS[item[0]][0])
    if len(ordered) >= 2:
        for (_, left_mid), (_, right_mid) in zip(ordered, ordered[1:]):
            if left_mid + SURFACE_MONO_TOL < right_mid:
                return False
    if len(ordered) >= 3:
        mids = [mid for _, mid in ordered]
        for idx in range(len(mids) - 2):
            second_diff = mids[idx] - 2.0 * mids[idx + 1] + mids[idx + 2]
            if second_diff < -SURFACE_CONVEX_TOL:
                return False
    return True


# ---------------------------------------------------------------------------
# Trader
# ---------------------------------------------------------------------------

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        data = {}
        if state.traderData:
            try:
                data = json.loads(state.traderData)
            except Exception:
                data = {}

        sigma_abs = data.get("sigma_abs", SIGMA_ABS_DEFAULT)
        residual_anchor = data.get("voucher_residual_anchor", {})
        if not isinstance(residual_anchor, dict):
            residual_anchor = {}

        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move = abs(vex_mid - prev_vex)
            alpha = 0.1
            daily_vol = move * math.sqrt(1000)
            sigma_abs = alpha * daily_vol + (1 - alpha) * sigma_abs

        for product, limit in DELTA1_PRODUCTS.items():
            if product not in state.order_depths:
                continue
            od = state.order_depths[product]
            mid = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None:
                continue
            if spread > MAX_DELTA1_SPREAD:
                continue

            position = state.position.get(product, 0)
            imbalance = get_imbalance(od)

            orders = []
            inv_adjustment = -INV_SKEW_FACTOR * (position / limit)
            fair = mid + inv_adjustment
            lean = round(IMBALANCE_LEAN * imbalance)

            for ask_price in sorted(od.sell_orders.keys()):
                if ask_price < fair - MM_EDGE:
                    ask_vol = -od.sell_orders[ask_price]
                    buy_qty = clamp_order_qty(ask_vol, position, limit)
                    if buy_qty > 0:
                        orders.append(Order(product, ask_price, buy_qty))
                        position += buy_qty

            for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                if bid_price > fair + MM_EDGE:
                    bid_vol = od.buy_orders[bid_price]
                    sell_qty = clamp_order_qty(-bid_vol, position, limit)
                    if sell_qty < 0:
                        orders.append(Order(product, bid_price, sell_qty))
                        position += sell_qty

            buy_price = round(fair - MM_OFFSET + lean)
            sell_price = round(fair + MM_OFFSET + lean)
            passive_size = max(1, limit // 10)

            buy_qty = clamp_order_qty(passive_size, position, limit)
            sell_qty = clamp_order_qty(-passive_size, position, limit)

            if buy_qty > 0:
                orders.append(Order(product, int(buy_price), buy_qty))
            if sell_qty < 0:
                orders.append(Order(product, int(sell_price), sell_qty))

            result[product] = orders

        if vex_mid is not None:
            observed_voucher_mids = get_observed_voucher_mids(state.order_depths)
            surface_ok = surface_guardrail_ok(observed_voucher_mids)

            fairs = {}
            for symbol in ALL_VOUCHER_STRIKES:
                strike, _ = VOUCHER_PRODUCTS[symbol]
                fair_val = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
                if fair_val < 0:
                    fair_val = max(vex_mid - strike, 0.0)
                fairs[symbol] = fair_val

            for symbol in ALL_VOUCHER_STRIKES:
                if symbol not in state.order_depths:
                    continue
                od = state.order_depths[symbol]
                voucher_mid = get_mid(od)
                spread = get_spread(od)
                if voucher_mid is None or spread is None:
                    continue
                if spread > MAX_VOUCHER_SPREAD:
                    continue

                _, limit = VOUCHER_PRODUCTS[symbol]
                position = state.position.get(symbol, 0)
                fair = fairs[symbol]

                raw_residual = voucher_mid - fair
                anchor = residual_anchor.get(symbol, raw_residual)
                reference_fair = fair + anchor
                centered_residual = voucher_mid - reference_fair

                inv_adj = -VOUCHER_INV_SKEW * (position / limit)
                adjusted_fair = reference_fair + inv_adj

                orders = []

                if surface_ok and abs(centered_residual) > ENTRY_THRESHOLD:
                    if centered_residual < -ENTRY_THRESHOLD:
                        for ask_price in sorted(od.sell_orders.keys()):
                            if ask_price < adjusted_fair - EXIT_THRESHOLD:
                                ask_vol = -od.sell_orders[ask_price]
                                buy_qty = clamp_order_qty(ask_vol, position, limit)
                                if buy_qty > 0:
                                    orders.append(Order(symbol, ask_price, buy_qty))
                                    position += buy_qty

                    elif centered_residual > ENTRY_THRESHOLD:
                        for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                            if bid_price > adjusted_fair + EXIT_THRESHOLD:
                                bid_vol = od.buy_orders[bid_price]
                                sell_qty = clamp_order_qty(-bid_vol, position, limit)
                                if sell_qty < 0:
                                    orders.append(Order(symbol, bid_price, sell_qty))
                                    position += sell_qty

                passive_size = max(1, limit // 15)
                buy_price = int(round(adjusted_fair - VOUCHER_MM_OFFSET))
                sell_price = int(round(adjusted_fair + VOUCHER_MM_OFFSET))

                if surface_ok:
                    buy_qty = clamp_order_qty(passive_size, position, limit)
                    sell_qty = clamp_order_qty(-passive_size, position, limit)
                else:
                    buy_qty = 0
                    sell_qty = 0

                if buy_qty > 0 and buy_price > 0:
                    orders.append(Order(symbol, buy_price, buy_qty))
                if sell_qty < 0 and sell_price > 0:
                    orders.append(Order(symbol, sell_price, sell_qty))

                residual_anchor[symbol] = (
                    (1.0 - RESIDUAL_ANCHOR_ALPHA) * anchor
                    + RESIDUAL_ANCHOR_ALPHA * raw_residual
                )
                result[symbol] = orders

        data["sigma_abs"] = sigma_abs
        data["voucher_residual_anchor"] = residual_anchor
        if vex_mid is not None:
            data["prev_vex"] = vex_mid

        traderData = json.dumps(data)
        return result, conversions, traderData
