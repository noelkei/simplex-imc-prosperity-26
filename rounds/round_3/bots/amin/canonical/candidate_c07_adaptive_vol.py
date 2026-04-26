"""
C07 Adaptive Vol Trader — Round 3
Strategy: Online Bachelier calibration + residual reversion + conservative delta-1 MM
Key fix over C06: sigma calibrated from market (~1160 vs 95), dynamic TTE, proper inventory mgmt
Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ---------------------------------------------------------------------------
# Normal-distribution helpers (Hart / Abramowitz-Stegun rational approx)
# ---------------------------------------------------------------------------

def norm_cdf(x: float) -> float:
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
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ---------------------------------------------------------------------------
# Bachelier (normal-model) call pricing and implied vol
# ---------------------------------------------------------------------------

def bachelier_call(S: float, K: float, T_years: float, sigma_abs: float) -> float:
    if T_years <= 0 or sigma_abs <= 0:
        return max(S - K, 0.0)
    vol_sqrt_t = sigma_abs * math.sqrt(T_years)
    if vol_sqrt_t < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vol_sqrt_t
    return (S - K) * norm_cdf(d) + vol_sqrt_t * norm_pdf(d)


def bachelier_implied_vol(S: float, K: float, T_years: float, market_price: float) -> float:
    """Bisection solver for Bachelier implied absolute volatility."""
    intrinsic = max(S - K, 0.0)
    if market_price <= intrinsic + 0.01:
        return 0.0
    lo, hi = 10.0, 5000.0
    for _ in range(60):
        mid = (lo + hi) * 0.5
        model = bachelier_call(S, K, T_years, mid)
        if model < market_price:
            lo = mid
        else:
            hi = mid
        if hi - lo < 0.5:
            break
    return (lo + hi) * 0.5


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------

# --- Voucher configuration ---
VOUCHER_STRIKES = {
    "VEV_5000": 5000,
    "VEV_5100": 5100,
    "VEV_5200": 5200,
    "VEV_5300": 5300,
    "VEV_5400": 5400,
    "VEV_5500": 5500,
}
VOUCHER_LIMIT = 300

# Strikes used for vol calibration (most extrinsic value, most informative)
CALIB_STRIKES = ["VEV_5200", "VEV_5300"]
VOL_EMA_ALPHA = 0.05
SIGMA_DEFAULT = 1160.0        # empirically calibrated from historical data

# Residual reversion parameters
RESIDUAL_EMA_ALPHA = 0.02     # slow EMA to track persistent smile bias
ENTRY_DEVIATION = 4.0         # trade only when deviation is extreme
EXIT_DEVIATION = 1.0          # stop when deviation falls below this
VOUCHER_ORDER_SIZE = 10       # smaller aggressive order size (conservative)
VOUCHER_PASSIVE_SIZE = 15     # larger passive quote size (MM focus)
VOUCHER_PASSIVE_OFFSET = 2    # offset from adjusted fair for passive quotes
VOUCHER_MAX_SPREAD = 25       # skip voucher if spread > this
VOUCHER_INV_SKEW = 5.0        # very aggressive inventory skew
VOUCHER_POS_CAP = 80          # hard per-strike position cap (<<300 limit)

# Cross-voucher spread trading (pairs)
SPREAD_PAIRS = [
    ("VEV_5000", "VEV_5100"),
    ("VEV_5100", "VEV_5200"),
    ("VEV_5200", "VEV_5300"),
]
SPREAD_EMA_ALPHA = 0.005      # slow EMA for spread mean
SPREAD_STD_EMA_ALPHA = 0.005  # slow EMA for spread std
SPREAD_Z_ENTER = 2.0          # enter spread trade when z exceeds this
SPREAD_Z_EXIT = 0.5           # exit when z reverts below this
SPREAD_ORDER_SIZE = 15        # lots per spread entry

# --- Delta-1 configuration ---
DELTA1_PRODUCTS = {
    "HYDROGEL_PACK": 200,
    "VELVETFRUIT_EXTRACT": 200,
}
DELTA1_MAX_POS = 25           # very conservative position limit
DELTA1_MM_OFFSET = 2          # passive quote offset
DELTA1_EDGE = 1               # minimum aggressive edge
DELTA1_INV_SKEW = 6.0         # extremely aggressive inventory mgmt
DELTA1_PASSIVE_SIZE = 5
DELTA1_AGGRESSIVE_SIZE = 8

# --- TTE management ---
TTE_LIVE_DAYS = 5.0           # live round starts at 5 days to expiry
TICKS_PER_DAY = 10000         # approximate ticks per trading day


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_mid(order_depth) -> float | None:
    if order_depth is None:
        return None
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders.keys())
    best_ask = min(order_depth.sell_orders.keys())
    return (best_bid + best_ask) / 2.0


def get_spread(order_depth) -> float | None:
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    return min(order_depth.sell_orders.keys()) - max(order_depth.buy_orders.keys())


def clamp_order_qty(qty: int, position: int, limit: int) -> int:
    """Clamp order quantity to respect position limit."""
    if qty > 0:
        max_buy = limit - position
        return max(0, min(qty, max_buy))
    elif qty < 0:
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

        # --- Load persisted state ---
        data = {}
        if state.traderData:
            try:
                data = json.loads(state.traderData)
            except Exception:
                data = {}

        tick_count = data.get("tick_count", 0) + 1
        sigma = data.get("sigma", SIGMA_DEFAULT)
        residual_emas = data.get("residual_emas", {})
        spread_emas = data.get("spread_emas", {})
        spread_std_emas = data.get("spread_std_emas", {})

        # --- Dynamic TTE ---
        tte_days = TTE_LIVE_DAYS - tick_count / TICKS_PER_DAY
        tte_years = max(tte_days, 0.5) / 365.0  # floor at 0.5 days

        # --- Get VEX mid (driver for all option pricing) ---
        vex_mid = get_mid(state.order_depths.get("VELVETFRUIT_EXTRACT"))

        # =================================================================
        # MODULE 1: Online vol calibration from market prices
        # =================================================================
        if vex_mid is not None:
            ivols = []
            for sym in CALIB_STRIKES:
                if sym not in state.order_depths:
                    continue
                v_mid = get_mid(state.order_depths[sym])
                if v_mid is None or v_mid <= 0:
                    continue
                K = VOUCHER_STRIKES[sym]
                iv = bachelier_implied_vol(vex_mid, K, tte_years, v_mid)
                if 100 < iv < 5000:
                    ivols.append(iv)

            if ivols:
                current_sigma = sum(ivols) / len(ivols)
                sigma = VOL_EMA_ALPHA * current_sigma + (1 - VOL_EMA_ALPHA) * sigma

        # =================================================================
        # MODULE 2: Voucher residual reversion (with correct vol)
        # =================================================================
        if vex_mid is not None:
            for sym, K in VOUCHER_STRIKES.items():
                if sym not in state.order_depths:
                    continue
                od = state.order_depths[sym]
                voucher_mid = get_mid(od)
                spread = get_spread(od)
                if voucher_mid is None or spread is None:
                    continue
                if spread > VOUCHER_MAX_SPREAD:
                    continue

                # Compute Bachelier fair value
                fair = bachelier_call(vex_mid, K, tte_years, sigma)
                intrinsic = max(vex_mid - K, 0.0)
                if fair < intrinsic:
                    fair = intrinsic

                # Raw residual
                residual = voucher_mid - fair

                # Track residual EMA (captures persistent vol smile bias)
                prev_ema = residual_emas.get(sym, residual)
                ema = RESIDUAL_EMA_ALPHA * residual + (1 - RESIDUAL_EMA_ALPHA) * prev_ema
                residual_emas[sym] = ema

                # Tradeable deviation = how far current residual is from its typical level
                deviation = residual - ema

                position = state.position.get(sym, 0)

                # Inventory-aware fair adjustment
                inv_adj = -VOUCHER_INV_SKEW * (position / VOUCHER_LIMIT)
                adj_fair = fair + ema + inv_adj  # fair + smile_bias + inventory_adj

                orders = []

                # Aggressive fills when deviation is significant
                if deviation < -ENTRY_DEVIATION:
                    # Cheaper than usual → buy
                    for ask_p in sorted(od.sell_orders.keys()):
                        if ask_p < adj_fair - EXIT_DEVIATION:
                            vol = -od.sell_orders[ask_p]
                            qty = clamp_order_qty(
                                min(vol, VOUCHER_ORDER_SIZE), position, VOUCHER_POS_CAP
                            )
                            if qty > 0:
                                orders.append(Order(sym, ask_p, qty))
                                position += qty

                elif deviation > ENTRY_DEVIATION:
                    # More expensive than usual → sell
                    for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                        if bid_p > adj_fair + EXIT_DEVIATION:
                            vol = od.buy_orders[bid_p]
                            qty = clamp_order_qty(
                                -min(vol, VOUCHER_ORDER_SIZE), position, VOUCHER_POS_CAP
                            )
                            if qty < 0:
                                orders.append(Order(sym, bid_p, qty))
                                position += qty

                # Passive resting quotes around adjusted fair
                buy_p = int(round(adj_fair - VOUCHER_PASSIVE_OFFSET))
                sell_p = int(round(adj_fair + VOUCHER_PASSIVE_OFFSET))

                bq = clamp_order_qty(VOUCHER_PASSIVE_SIZE, position, VOUCHER_POS_CAP)
                sq = clamp_order_qty(-VOUCHER_PASSIVE_SIZE, position, VOUCHER_POS_CAP)

                if bq > 0 and buy_p > 0:
                    orders.append(Order(sym, buy_p, bq))
                if sq < 0 and sell_p > 0:
                    orders.append(Order(sym, sell_p, sq))

                result[sym] = orders

        # =================================================================
        # MODULE 2b: Cross-voucher spread trading
        # =================================================================
        for sym_lo, sym_hi in SPREAD_PAIRS:
            if sym_lo not in state.order_depths or sym_hi not in state.order_depths:
                continue
            od_lo = state.order_depths[sym_lo]
            od_hi = state.order_depths[sym_hi]
            mid_lo = get_mid(od_lo)
            mid_hi = get_mid(od_hi)
            if mid_lo is None or mid_hi is None:
                continue

            pair_key = f"{sym_lo}_{sym_hi}"
            spread = mid_lo - mid_hi  # lower strike is more expensive

            # Track spread EMA and std
            prev_spread_ema = spread_emas.get(pair_key, spread)
            s_ema = SPREAD_EMA_ALPHA * spread + (1 - SPREAD_EMA_ALPHA) * prev_spread_ema
            spread_emas[pair_key] = s_ema

            prev_std_ema = spread_std_emas.get(pair_key, 3.0)
            sq_dev = (spread - s_ema) ** 2
            std_ema = SPREAD_STD_EMA_ALPHA * sq_dev + (1 - SPREAD_STD_EMA_ALPHA) * (prev_std_ema ** 2)
            std_ema = math.sqrt(max(std_ema, 0.01))
            spread_std_emas[pair_key] = std_ema

            z = (spread - s_ema) / std_ema if std_ema > 0.1 else 0.0

            pos_lo = state.position.get(sym_lo, 0)
            pos_hi = state.position.get(sym_hi, 0)

            # Spread entry: z > threshold → spread is wide → sell lo, buy hi
            if z > SPREAD_Z_ENTER:
                # Sell spread: sell sym_lo, buy sym_hi
                if pos_lo > -VOUCHER_POS_CAP and pos_hi < VOUCHER_POS_CAP:
                    best_bid_lo = max(od_lo.buy_orders.keys()) if od_lo.buy_orders else None
                    best_ask_hi = min(od_hi.sell_orders.keys()) if od_hi.sell_orders else None
                    if best_bid_lo is not None and best_ask_hi is not None:
                        qty = SPREAD_ORDER_SIZE
                        sq = clamp_order_qty(-qty, pos_lo, VOUCHER_POS_CAP)
                        bq = clamp_order_qty(qty, pos_hi, VOUCHER_POS_CAP)
                        actual_qty = min(abs(sq), bq) if sq < 0 and bq > 0 else 0
                        if actual_qty > 0:
                            if sym_lo not in result:
                                result[sym_lo] = []
                            if sym_hi not in result:
                                result[sym_hi] = []
                            result[sym_lo].append(Order(sym_lo, best_bid_lo, -actual_qty))
                            result[sym_hi].append(Order(sym_hi, best_ask_hi, actual_qty))

            elif z < -SPREAD_Z_ENTER:
                # Buy spread: buy sym_lo, sell sym_hi
                if pos_lo < VOUCHER_POS_CAP and pos_hi > -VOUCHER_POS_CAP:
                    best_ask_lo = min(od_lo.sell_orders.keys()) if od_lo.sell_orders else None
                    best_bid_hi = max(od_hi.buy_orders.keys()) if od_hi.buy_orders else None
                    if best_ask_lo is not None and best_bid_hi is not None:
                        qty = SPREAD_ORDER_SIZE
                        bq = clamp_order_qty(qty, pos_lo, VOUCHER_POS_CAP)
                        sq = clamp_order_qty(-qty, pos_hi, VOUCHER_POS_CAP)
                        actual_qty = min(bq, abs(sq)) if bq > 0 and sq < 0 else 0
                        if actual_qty > 0:
                            if sym_lo not in result:
                                result[sym_lo] = []
                            if sym_hi not in result:
                                result[sym_hi] = []
                            result[sym_lo].append(Order(sym_lo, best_ask_lo, actual_qty))
                            result[sym_hi].append(Order(sym_hi, best_bid_hi, -actual_qty))

        # =================================================================
        # MODULE 3: Conservative delta-1 market making
        # =================================================================
        for product, full_limit in DELTA1_PRODUCTS.items():
            if product not in state.order_depths:
                continue
            od = state.order_depths[product]
            mid = get_mid(od)
            if mid is None:
                continue

            position = state.position.get(product, 0)
            eff_limit = DELTA1_MAX_POS

            # Inventory-aware fair value (strong skew forces mean-reversion)
            inv_adj = -DELTA1_INV_SKEW * (position / full_limit)
            fair = mid + inv_adj

            orders = []

            # Aggressive: take mispriced liquidity
            for ask_p in sorted(od.sell_orders.keys()):
                if ask_p < fair - DELTA1_EDGE:
                    vol = -od.sell_orders[ask_p]
                    qty = clamp_order_qty(
                        min(vol, DELTA1_AGGRESSIVE_SIZE), position, eff_limit
                    )
                    if qty > 0:
                        orders.append(Order(product, ask_p, qty))
                        position += qty

            for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                if bid_p > fair + DELTA1_EDGE:
                    vol = od.buy_orders[bid_p]
                    qty = clamp_order_qty(
                        -min(vol, DELTA1_AGGRESSIVE_SIZE), position, eff_limit
                    )
                    if qty < 0:
                        orders.append(Order(product, bid_p, qty))
                        position += qty

            # Passive: resting quotes
            buy_p = int(round(fair - DELTA1_MM_OFFSET))
            sell_p = int(round(fair + DELTA1_MM_OFFSET))

            bq = clamp_order_qty(DELTA1_PASSIVE_SIZE, position, eff_limit)
            sq = clamp_order_qty(-DELTA1_PASSIVE_SIZE, position, eff_limit)

            if bq > 0:
                orders.append(Order(product, buy_p, bq))
            if sq < 0:
                orders.append(Order(product, sell_p, sq))

            result[product] = orders

        # =================================================================
        # Persist state
        # =================================================================
        data["tick_count"] = tick_count
        data["sigma"] = sigma
        data["residual_emas"] = residual_emas
        data["spread_emas"] = spread_emas
        data["spread_std_emas"] = spread_std_emas

        trader_data = json.dumps(data)
        return result, conversions, trader_data
