"""
C09 Optimized Composite — Round 3
=================================
Based on C06 which peaked at 17K. Key fixes:
1. Sigma = 1160 (calibrated from market, not 95)
2. Dynamic TTE that decrements through the day
3. Per-strike smile bias tracking (VEV_5000/5100 trade cheap, 5200/5300 trade rich)
4. Hard position caps (60 per voucher, 40 delta-1) with aggressive unwind
5. Robust delta-1 MM with microprice, imbalance EMA, Avellaneda-Stoikov reservation

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────────────────────────
# Normal distribution helpers
# ─────────────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────────────
# Bachelier model
# ─────────────────────────────────────────────────────────────────────

def bachelier_call(S: float, K: float, T_years: float, sigma: float) -> float:
    if T_years <= 0 or sigma <= 0:
        return max(S - K, 0.0)
    vst = sigma * math.sqrt(T_years)
    if vst < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vst
    return (S - K) * norm_cdf(d) + vst * norm_pdf(d)


def bachelier_iv(S: float, K: float, T: float, C: float) -> float:
    """Bisection implied vol solver."""
    intrinsic = max(S - K, 0.0)
    if C <= intrinsic + 0.01:
        return 0.0
    lo, hi = 10.0, 5000.0
    for _ in range(50):
        mid = (lo + hi) * 0.5
        if bachelier_call(S, K, T, mid) < C:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1.0:
            break
    return (lo + hi) * 0.5


# ─────────────────────────────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────────────────────────────

# Volatility
SIGMA_DEFAULT = 1160.0          # calibrated from historical data
SIGMA_EMA_ALPHA = 0.03          # slow EMA update for online recalibration
CALIB_STRIKES = ["VEV_5200", "VEV_5300"]  # most extrinsic, best for calibration

# TTE: live round starts at 5 days, ~10000 ticks per day
TTE_START_DAYS = 5.0
TICKS_PER_DAY = 10000

# Voucher products
VOUCHER_PRODUCTS = {
    "VEV_5000": 5000,
    "VEV_5100": 5100,
    "VEV_5200": 5200,
    "VEV_5300": 5300,
}
VOUCHER_LIMIT = 300
VOUCHER_POS_CAP = 60           # hard internal cap per strike

# Smile bias priors (from EDA: VEV_5000/5100 cheap, 5200/5300 rich vs flat vol model)
# These are the average residual = market_mid - bachelier_fair(sigma=1160)
# Positive = market trades ABOVE model. Negative = market trades BELOW model.
SMILE_BIAS_PRIOR = {
    "VEV_5000": -3.0,    # market consistently ~3 below model
    "VEV_5100": -3.2,    # market consistently ~3 below model
    "VEV_5200":  1.3,    # market consistently ~1.3 above model
    "VEV_5300":  2.8,    # market consistently ~3 above model
}
BIAS_EMA_ALPHA = 0.005         # very slow learning of smile bias

# Residual reversion (trading the deviation from smile-adjusted fair)
ENTRY_THRESHOLD = 3.5          # |deviation from adjusted fair| to enter aggressively
EXIT_THRESHOLD = 0.5           # close to fair, stop forcing
VOUCHER_TAKE_SIZE = 12         # max aggressive take per level
VOUCHER_PASSIVE_SIZE = 15      # passive quote size
VOUCHER_PASSIVE_OFFSET = 2     # ticks from fair for passive quotes
VOUCHER_MAX_SPREAD = 25        # skip if book spread > this
VOUCHER_INV_SKEW = 4.0         # inventory skew strength
VOUCHER_UNWIND_THR = 50        # start aggressive unwind at this position
VOUCHER_UNWIND_QTY = 10        # aggressive unwind size

# Delta-1 products
DELTA1_PRODUCTS = {
    "HYDROGEL_PACK": 200,
    "VELVETFRUIT_EXTRACT": 200,
}
DELTA1_POS_CAP = 40            # internal position cap
DELTA1_HALF_SPREAD = 2         # passive quote half-spread
DELTA1_TAKE_EDGE = 2           # aggressive take edge
DELTA1_INV_GAMMA = 3.0         # Avellaneda-Stoikov inventory penalty
DELTA1_PASSIVE_SIZE = 25       # passive quote size
DELTA1_TAKE_SIZE = 15          # aggressive take size per level
DELTA1_UNWIND_THR = 35         # aggressive unwind threshold
DELTA1_UNWIND_QTY = 10         # unwind size
DELTA1_IMB_ALPHA = 0.3         # imbalance EMA smoothing
DELTA1_IMB_GAIN = 2.0          # imbalance → quote shift ticks


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def microprice(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return (bb + ba) / 2.0
    return (bb * av + ba * bv) / total


def simple_mid(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def book_imbalance(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return 0.0
    return (bv - av) / total


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


def clamp_qty(qty: int, pos: int, cap: int) -> int:
    """Clamp order qty to stay within [-cap, cap] position."""
    if qty > 0:
        return max(0, min(qty, cap - pos))
    elif qty < 0:
        return min(0, max(qty, -(cap + pos)))
    return 0


# ─────────────────────────────────────────────────────────────────────
# Trader
# ─────────────────────────────────────────────────────────────────────

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # ── Load state ──
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        tick = sd.get("tick", 0) + 1
        sigma = sd.get("sigma", SIGMA_DEFAULT)
        smile_bias = sd.get("smile_bias", dict(SMILE_BIAS_PRIOR))

        # ── Dynamic TTE ──
        tte_days = max(TTE_START_DAYS - tick / TICKS_PER_DAY, 0.5)
        tte_years = tte_days / 365.0

        # ── Get VEX mid ──
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = microprice(state.order_depths["VELVETFRUIT_EXTRACT"])
            if vex_mid is None:
                vex_mid = simple_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # ══════════════════════════════════════════════════════════════
        # MODULE 1: Online vol calibration
        # ══════════════════════════════════════════════════════════════
        if vex_mid is not None:
            ivols = []
            for sym in CALIB_STRIKES:
                if sym not in state.order_depths:
                    continue
                v_mid = simple_mid(state.order_depths[sym])
                if v_mid is None or v_mid <= 0:
                    continue
                K = VOUCHER_PRODUCTS[sym]
                iv = bachelier_iv(vex_mid, K, tte_years, v_mid)
                if 200 < iv < 4000:
                    ivols.append(iv)
            if ivols:
                avg_iv = sum(ivols) / len(ivols)
                sigma = SIGMA_EMA_ALPHA * avg_iv + (1 - SIGMA_EMA_ALPHA) * sigma

        # ══════════════════════════════════════════════════════════════
        # MODULE 2: Voucher trading (Bachelier residual reversion)
        # ══════════════════════════════════════════════════════════════
        if vex_mid is not None:
            for sym, K in VOUCHER_PRODUCTS.items():
                if sym not in state.order_depths:
                    continue
                od = state.order_depths[sym]
                if not od.buy_orders or not od.sell_orders:
                    continue

                bb = max(od.buy_orders)
                ba = min(od.sell_orders)
                spread = ba - bb
                if spread > VOUCHER_MAX_SPREAD or spread < 1:
                    continue

                voucher_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)

                # Bachelier fair value
                fair = bachelier_call(vex_mid, K, tte_years, sigma)
                intrinsic = max(vex_mid - K, 0.0)
                if fair < intrinsic:
                    fair = intrinsic

                # Raw residual = market - model
                raw_residual = voucher_mid - fair

                # Update smile bias EMA
                prev_bias = smile_bias.get(sym, 0.0)
                bias = BIAS_EMA_ALPHA * raw_residual + (1 - BIAS_EMA_ALPHA) * prev_bias
                smile_bias[sym] = bias

                # Tradeable deviation = raw_residual - expected_bias
                deviation = raw_residual - bias

                # Smile-adjusted fair (what the market *should* trade at)
                adj_fair = fair + bias

                # Inventory penalty (Avellaneda-Stoikov style)
                inv_adj = -VOUCHER_INV_SKEW * (pos / VOUCHER_LIMIT)
                quote_fair = adj_fair + inv_adj

                orders = []
                bought = 0
                sold = 0

                def buy_room():
                    return max(0, VOUCHER_POS_CAP - pos - bought)

                def sell_room():
                    return max(0, VOUCHER_POS_CAP + pos - sold)

                # ── Aggressive takes on large deviations ──
                if deviation < -ENTRY_THRESHOLD:
                    # Cheap vs adjusted fair → buy
                    for ask_p in sorted(od.sell_orders.keys()):
                        if buy_room() <= 0:
                            break
                        if ask_p > quote_fair - EXIT_THRESHOLD:
                            break
                        vol = -od.sell_orders[ask_p]
                        qty = min(vol, VOUCHER_TAKE_SIZE, buy_room())
                        if qty > 0:
                            orders.append(Order(sym, ask_p, qty))
                            bought += qty

                elif deviation > ENTRY_THRESHOLD:
                    # Expensive vs adjusted fair → sell
                    for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                        if sell_room() <= 0:
                            break
                        if bid_p < quote_fair + EXIT_THRESHOLD:
                            break
                        vol = od.buy_orders[bid_p]
                        qty = min(vol, VOUCHER_TAKE_SIZE, sell_room())
                        if qty > 0:
                            orders.append(Order(sym, bid_p, -qty))
                            sold += qty

                # ── Aggressive unwind at extremes ──
                if pos >= VOUCHER_UNWIND_THR and sell_room() > 0:
                    uq = min(VOUCHER_UNWIND_QTY, sell_room())
                    if uq > 0:
                        orders.append(Order(sym, bb, -uq))
                        sold += uq
                elif pos <= -VOUCHER_UNWIND_THR and buy_room() > 0:
                    uq = min(VOUCHER_UNWIND_QTY, buy_room())
                    if uq > 0:
                        orders.append(Order(sym, ba, uq))
                        bought += uq

                # ── Passive quotes ──
                buy_px = int(round(quote_fair - VOUCHER_PASSIVE_OFFSET))
                sell_px = int(round(quote_fair + VOUCHER_PASSIVE_OFFSET))

                # Don't cross the book
                if buy_px >= ba:
                    buy_px = ba - 1
                if sell_px <= bb:
                    sell_px = bb + 1

                # Inventory-skewed sizing
                if pos > 0:
                    bsz = max(2, VOUCHER_PASSIVE_SIZE - int(pos * 0.3))
                    ssz = max(2, VOUCHER_PASSIVE_SIZE + int(pos * 0.3))
                elif pos < 0:
                    bsz = max(2, VOUCHER_PASSIVE_SIZE + int(-pos * 0.3))
                    ssz = max(2, VOUCHER_PASSIVE_SIZE - int(-pos * 0.3))
                else:
                    bsz = VOUCHER_PASSIVE_SIZE
                    ssz = VOUCHER_PASSIVE_SIZE

                bq = min(bsz, buy_room())
                sq = min(ssz, sell_room())

                if bq > 0 and buy_px > 0:
                    orders.append(Order(sym, buy_px, bq))
                if sq > 0 and sell_px > 0:
                    orders.append(Order(sym, sell_px, -sq))

                result[sym] = orders

        # ══════════════════════════════════════════════════════════════
        # MODULE 3: Delta-1 market making (Optiver-style)
        # ══════════════════════════════════════════════════════════════
        for product, limit in DELTA1_PRODUCTS.items():
            od = state.order_depths.get(product)
            if od is None or not od.buy_orders or not od.sell_orders:
                continue

            bb = max(od.buy_orders)
            ba = min(od.sell_orders)
            spread = ba - bb
            if spread < 1:
                continue

            pos = state.position.get(product, 0)

            # Fair value: microprice
            mp = microprice(od)
            fair = mp if mp is not None else (bb + ba) / 2.0

            # EMA imbalance
            imb_raw = book_imbalance(od)
            imb_key = product + "_imb"
            prev_imb = sd.get(imb_key, 0.0)
            imb = DELTA1_IMB_ALPHA * imb_raw + (1 - DELTA1_IMB_ALPHA) * prev_imb
            sd[imb_key] = imb

            # Reservation price + predictive shift
            res_px = fair - DELTA1_INV_GAMMA * (pos / limit)
            imb_shift = clamp(DELTA1_IMB_GAIN * imb, -2.0, 2.0)
            qfair = res_px + imb_shift

            buy_thr = qfair - DELTA1_TAKE_EDGE
            sell_thr = qfair + DELTA1_TAKE_EDGE

            orders = []
            bought = 0
            sold = 0

            def d1_buy_room():
                return max(0, DELTA1_POS_CAP - pos - bought)

            def d1_sell_room():
                return max(0, DELTA1_POS_CAP + pos - sold)

            # Aggressive takes
            for ask_p in sorted(od.sell_orders.keys()):
                if d1_buy_room() <= 0 or ask_p > buy_thr:
                    break
                vol = -od.sell_orders[ask_p]
                qty = min(vol, DELTA1_TAKE_SIZE, d1_buy_room())
                if qty > 0:
                    orders.append(Order(product, ask_p, qty))
                    bought += qty

            for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                if d1_sell_room() <= 0 or bid_p < sell_thr:
                    break
                vol = od.buy_orders[bid_p]
                qty = min(vol, DELTA1_TAKE_SIZE, d1_sell_room())
                if qty > 0:
                    orders.append(Order(product, bid_p, -qty))
                    sold += qty

            # Aggressive unwind
            if pos >= DELTA1_UNWIND_THR and d1_sell_room() > 0:
                uq = min(DELTA1_UNWIND_QTY, d1_sell_room())
                if uq > 0:
                    orders.append(Order(product, bb, -uq))
                    sold += uq
            elif pos <= -DELTA1_UNWIND_THR and d1_buy_room() > 0:
                uq = min(DELTA1_UNWIND_QTY, d1_buy_room())
                if uq > 0:
                    orders.append(Order(product, ba, uq))
                    bought += uq

            # Passive quotes
            half = DELTA1_HALF_SPREAD
            if abs(pos) > DELTA1_POS_CAP * 0.6:
                half += 1

            bid_px = int(round(qfair - half))
            ask_px = int(round(qfair + half))

            if bid_px >= ba:
                bid_px = ba - 1
            if ask_px <= bb:
                ask_px = bb + 1
            if bid_px >= ask_px:
                bid_px = ask_px - 1

            # Inventory-skewed sizes
            if pos > 0:
                bsz = max(2, DELTA1_PASSIVE_SIZE - int(pos * 0.5))
                ssz = max(2, DELTA1_PASSIVE_SIZE + int(pos * 0.5))
            elif pos < 0:
                bsz = max(2, DELTA1_PASSIVE_SIZE + int(-pos * 0.5))
                ssz = max(2, DELTA1_PASSIVE_SIZE - int(-pos * 0.5))
            else:
                bsz = DELTA1_PASSIVE_SIZE
                ssz = DELTA1_PASSIVE_SIZE

            bq = min(bsz, d1_buy_room())
            sq = min(ssz, d1_sell_room())

            if bq > 0:
                orders.append(Order(product, bid_px, bq))
            if sq > 0:
                orders.append(Order(product, ask_px, -sq))

            result[product] = orders

        # ══════════════════════════════════════════════════════════════
        # Persist state
        # ══════════════════════════════════════════════════════════════
        sd["tick"] = tick
        sd["sigma"] = sigma
        sd["smile_bias"] = smile_bias

        return result, conversions, json.dumps(sd)
