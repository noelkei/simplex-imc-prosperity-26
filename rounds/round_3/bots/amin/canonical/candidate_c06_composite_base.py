"""
C06 Composite Base Trader — Round 3
Spec: spec_c06_composite_base.md
Components: C01 (HYDROGEL_PACK MM) + C02 (VELVETFRUIT_EXTRACT MM) + C03 (Bachelier Residual Reversion)
Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ---------------------------------------------------------------------------
# Normal-distribution helpers (West 2004 rational approximation)
# ---------------------------------------------------------------------------

def norm_cdf(x: float) -> float:
    """Cumulative normal distribution via Abramowitz & Stegun 26.2.17 style rational approx."""
    if x < -8.0:
        return 0.0
    if x > 8.0:
        return 1.0
    # Hart approximation constants
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
MM_OFFSET = 2               # quote offset from fair for passive orders
MM_EDGE = 1                 # minimum edge to take aggressive fills
IMBALANCE_LEAN = 1          # how much to lean quotes based on imbalance (ticks)
MAX_DELTA1_SPREAD = 8       # skip product if spread > this

# Voucher residual reversion
ENTRY_THRESHOLD = 3.0       # minimum |residual| to enter
EXIT_THRESHOLD = 0.5        # residual close enough to fair to stop
VOUCHER_MM_OFFSET = 2       # passive quote offset for vouchers
MAX_VOUCHER_SPREAD = 20     # max acceptable voucher spread
SIGMA_ABS_DEFAULT = 95.0    # initial absolute volatility estimate for Bachelier
TTE_DAYS = 5                # live round time-to-expiry in days
TTE_YEARS = TTE_DAYS / 365.0

# Position / inventory
INV_SKEW_FACTOR = 1.5       # how much to skew quotes based on inventory (delta-1)
VOUCHER_INV_SKEW = 1.0      # light inventory skew for vouchers

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
    """Return mid price or None if book is missing a side."""
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
    """Top-of-book volume imbalance in [-1, 1]."""
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
    """Clamp order quantity to respect position limit."""
    if qty > 0:  # buy
        max_buy = limit - position
        return max(0, min(qty, max_buy))
    elif qty < 0:  # sell
        max_sell = limit + position
        return min(0, max(qty, -max_sell))
    return 0


# ---------------------------------------------------------------------------
# Trader
# ---------------------------------------------------------------------------

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # Load persisted state
        data = {}
        if state.traderData:
            try:
                data = json.loads(state.traderData)
            except Exception:
                data = {}

        sigma_abs = data.get("sigma_abs", SIGMA_ABS_DEFAULT)

        # ---- Get VEX mid for voucher pricing ----
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # Update sigma_abs from VEX price moves
        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move = abs(vex_mid - prev_vex)
            # Exponential moving average of absolute moves, annualized
            alpha = 0.1
            daily_vol = move * math.sqrt(1000)  # rough scaling: ~1000 ticks per day
            sigma_abs = alpha * daily_vol + (1 - alpha) * sigma_abs

        # ---- Delta-1 products ----
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
            best_bid = max(od.buy_orders.keys())
            best_ask = min(od.sell_orders.keys())

            # Inventory-aware fair value
            inv_adjustment = -INV_SKEW_FACTOR * (position / limit)
            fair = mid + inv_adjustment

            # Imbalance lean
            lean = round(IMBALANCE_LEAN * imbalance)

            # Aggressive: take liquidity when edge is clear
            # Buy against asks below fair
            for ask_price in sorted(od.sell_orders.keys()):
                if ask_price < fair - MM_EDGE:
                    ask_vol = -od.sell_orders[ask_price]  # positive
                    buy_qty = clamp_order_qty(ask_vol, position, limit)
                    if buy_qty > 0:
                        orders.append(Order(product, ask_price, buy_qty))
                        position += buy_qty

            # Sell against bids above fair
            for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                if bid_price > fair + MM_EDGE:
                    bid_vol = od.buy_orders[bid_price]
                    sell_qty = clamp_order_qty(-bid_vol, position, limit)
                    if sell_qty < 0:
                        orders.append(Order(product, bid_price, sell_qty))
                        position += sell_qty

            # Passive: place resting orders
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

        # ---- Voucher products (Bachelier residual reversion) ----
        if vex_mid is not None:
            # Compute Bachelier fairs for surface guardrail
            fairs = {}
            for symbol in ALL_VOUCHER_STRIKES:
                strike, _ = VOUCHER_PRODUCTS[symbol]
                fair_val = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
                if fair_val < 0:
                    fair_val = max(vex_mid - strike, 0.0)
                fairs[symbol] = fair_val

            # Surface monotonicity check: fair should decrease with strike
            sorted_symbols = sorted(fairs.keys(), key=lambda s: VOUCHER_PRODUCTS[s][0])
            surface_ok = True
            for i in range(len(sorted_symbols) - 1):
                if fairs[sorted_symbols[i]] < fairs[sorted_symbols[i + 1]] - 0.5:
                    surface_ok = False
                    break

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

                strike, limit = VOUCHER_PRODUCTS[symbol]
                position = state.position.get(symbol, 0)
                fair = fairs[symbol]

                # Residual
                residual = voucher_mid - fair

                # Light inventory skew
                inv_adj = -VOUCHER_INV_SKEW * (position / limit)
                adjusted_fair = fair + inv_adj

                orders = []
                best_bid = max(od.buy_orders.keys())
                best_ask = min(od.sell_orders.keys())

                if abs(residual) > ENTRY_THRESHOLD and surface_ok:
                    if residual < -ENTRY_THRESHOLD:
                        # Underpriced: buy
                        for ask_price in sorted(od.sell_orders.keys()):
                            if ask_price < adjusted_fair - EXIT_THRESHOLD:
                                ask_vol = -od.sell_orders[ask_price]
                                buy_qty = clamp_order_qty(ask_vol, position, limit)
                                if buy_qty > 0:
                                    orders.append(Order(symbol, ask_price, buy_qty))
                                    position += buy_qty

                    elif residual > ENTRY_THRESHOLD:
                        # Overpriced: sell
                        for bid_price in sorted(od.buy_orders.keys(), reverse=True):
                            if bid_price > adjusted_fair + EXIT_THRESHOLD:
                                bid_vol = od.buy_orders[bid_price]
                                sell_qty = clamp_order_qty(-bid_vol, position, limit)
                                if sell_qty < 0:
                                    orders.append(Order(symbol, bid_price, sell_qty))
                                    position += sell_qty

                # Passive quotes around adjusted fair
                passive_size = max(1, limit // 15)
                buy_price = int(round(adjusted_fair - VOUCHER_MM_OFFSET))
                sell_price = int(round(adjusted_fair + VOUCHER_MM_OFFSET))

                buy_qty = clamp_order_qty(passive_size, position, limit)
                sell_qty = clamp_order_qty(-passive_size, position, limit)

                if buy_qty > 0 and buy_price > 0:
                    orders.append(Order(symbol, buy_price, buy_qty))
                if sell_qty < 0 and sell_price > 0:
                    orders.append(Order(symbol, sell_price, sell_qty))

                result[symbol] = orders

        # ---- Persist state ----
        data["sigma_abs"] = sigma_abs
        if vex_mid is not None:
            data["prev_vex"] = vex_mid

        traderData = json.dumps(data)
        return result, conversions, traderData
