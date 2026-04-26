"""
C10 Delta-Hedged Options + Aggressive HYDROGEL MM
==================================================
Strategy based on deep EDA findings:
1. HYDROGEL MM is primary PnL source (spread/|ret| ratio = 4.7, mean-reverting)
2. Voucher options with portfolio-level delta hedging via VEX (Optiver ASML approach)
3. VEX used primarily as delta hedge, secondary MM with remaining capacity

Key insight: C06-C09 all failed because unhedged voucher delta (~170 VEX-equiv)
dominated PnL (5K-8K daily swings vs 100-300 spread income). Delta hedging is essential.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────────────────────────
# Math helpers
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


def bachelier_call(S: float, K: float, T: float, sig: float) -> float:
    if T <= 0.0 or sig <= 0.0:
        return max(S - K, 0.0)
    vt = sig * math.sqrt(T)
    if vt < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vt
    return (S - K) * norm_cdf(d) + vt * norm_pdf(d)


def bachelier_delta(S: float, K: float, T: float, sig: float) -> float:
    if T <= 0.0 or sig <= 0.0:
        return 1.0 if S > K else 0.0
    vt = sig * math.sqrt(T)
    if vt < 1e-12:
        return 1.0 if S > K else 0.0
    return norm_cdf((S - K) / vt)


def bachelier_iv(S: float, K: float, T: float, C: float) -> float:
    intrinsic = max(S - K, 0.0)
    if C <= intrinsic + 0.01:
        return 0.0
    lo, hi = 10.0, 5000.0
    for _ in range(40):
        mid = (lo + hi) * 0.5
        if bachelier_call(S, K, T, mid) < C:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1.0:
            break
    return (lo + hi) * 0.5


# ─────────────────────────────────────────────────────────────────────
# Order book helpers
# ─────────────────────────────────────────────────────────────────────

def get_mid(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_microprice(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return (bb + ba) / 2.0
    return (bb * av + ba * bv) / total


def get_imbalance(od) -> float:
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


# ─────────────────────────────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────────────────────────────

# Voucher config
VOUCHER_PRODUCTS = {
    "VEV_5000": 5000,
    "VEV_5100": 5100,
    "VEV_5200": 5200,
    "VEV_5300": 5300,
}
VOUCHER_LIMIT = 300

# Bachelier vol
SIGMA_DEFAULT = 1160.0
SIGMA_EMA_ALPHA = 0.03

# Smile bias priors (persistent market vs model deviation)
SMILE_BIAS = {
    "VEV_5000": -3.0,
    "VEV_5100": -3.2,
    "VEV_5200": 1.3,
    "VEV_5300": 2.8,
}
BIAS_ALPHA = 0.005

# TTE
TTE_START_DAYS = 5.0
TICKS_PER_DAY = 10000

# Voucher trading params (conservative — edge is small)
VOUCHER_POS_CAP = 20           # LOW: keep delta manageable (was 60 in C09)
VOUCHER_PASSIVE_OFFSET = 3     # wider than C09 (was 2)
VOUCHER_PASSIVE_SIZE = 8       # small (was 15)
VOUCHER_ENTRY_THR = 3.0        # tighter to catch more opportunities
VOUCHER_TAKE_SIZE = 5          # small takes
VOUCHER_INV_SKEW = 3.0         # strong inventory penalty
VOUCHER_MAX_SPREAD = 15        # skip wide spreads

# Delta hedging (Optiver-inspired)
DELTA_HEDGE_THR = 15.0         # hedge when |portfolio_delta| > this
MAX_HEDGE_TRADE = 25           # max VEX units per hedge
VEX_HEDGE_RESERVE = 120        # units reserved for hedging (of 200 limit)

# Delta-1 config
HYDROGEL_LIMIT = 200
VEX_LIMIT = 200

# HYDROGEL MM params (primary PnL source — wide spread favorable)
HG_HALF_SPREAD = 3             # 3 ticks each side (spread 15.7 avg, so this is inside)
HG_TAKE_EDGE = 3               # aggressive take when price > 3 away from fair
HG_PASSIVE_SIZE = 25           # moderate passive sizing
HG_TAKE_SIZE = 15              # aggressive take
HG_INV_GAMMA = 2.5             # stronger inventory penalty
HG_POS_CAP = 100               # internal position cap (< 200 limit)
HG_UNWIND_THR = 70             # start aggressive unwind earlier
HG_UNWIND_QTY = 15             # unwind size
HG_IMB_ALPHA = 0.3             # imbalance EMA
HG_IMB_GAIN = 2.0              # imbalance → fair shift

# VEX MM params (secondary — most capacity reserved for hedging)
VEX_MM_SIZE = 12               # small passive size
VEX_HALF_SPREAD = 2
VEX_TAKE_EDGE = 2
VEX_TAKE_SIZE = 10
VEX_INV_GAMMA = 2.5
VEX_IMB_ALPHA = 0.3
VEX_IMB_GAIN = 1.5


# ─────────────────────────────────────────────────────────────────────
# Trader
# ─────────────────────────────────────────────────────────────────────

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # ── Load persisted state ──
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        tick = sd.get("tick", 0) + 1
        sigma = sd.get("sigma", SIGMA_DEFAULT)
        smile_bias = sd.get("sb", dict(SMILE_BIAS))

        # Dynamic TTE
        tte_days = max(TTE_START_DAYS - tick / TICKS_PER_DAY, 0.5)
        tte_years = tte_days / 365.0

        # ══════════════════════════════════════════════════════════════
        # MODULE 1: HYDROGEL Market Making (Primary PnL)
        # Independent product, mean-reverting, wide spread → best MM opportunity
        # ══════════════════════════════════════════════════════════════
        hg_od = state.order_depths.get("HYDROGEL_PACK")
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb = max(hg_od.buy_orders)
            hg_ba = min(hg_od.sell_orders)
            hg_spread = hg_ba - hg_bb

            if hg_spread >= 1:
                hg_pos = state.position.get("HYDROGEL_PACK", 0)

                # Fair value: microprice + imbalance EMA
                hg_micro = get_microprice(hg_od)
                hg_imb_raw = get_imbalance(hg_od)
                hg_imb_key = "hg_imb"
                hg_imb = HG_IMB_ALPHA * hg_imb_raw + (1 - HG_IMB_ALPHA) * sd.get(hg_imb_key, 0.0)
                sd[hg_imb_key] = hg_imb

                # Avellaneda-Stoikov reservation price (use cap for stronger penalty)
                hg_fair = hg_micro - HG_INV_GAMMA * (hg_pos / HG_POS_CAP)
                hg_imb_shift = clamp(HG_IMB_GAIN * hg_imb, -3.0, 3.0)
                hg_qfair = hg_fair + hg_imb_shift

                hg_orders = []
                hg_bought = 0
                hg_sold = 0

                def hg_buy_room():
                    return max(0, min(HG_POS_CAP, HYDROGEL_LIMIT) - hg_pos - hg_bought)

                def hg_sell_room():
                    return max(0, min(HG_POS_CAP, HYDROGEL_LIMIT) + hg_pos - hg_sold)

                # Aggressive takes: buy cheap / sell expensive
                for ask_p in sorted(hg_od.sell_orders.keys()):
                    if hg_buy_room() <= 0:
                        break
                    if ask_p > hg_qfair - HG_TAKE_EDGE:
                        break
                    vol = -hg_od.sell_orders[ask_p]
                    qty = min(vol, HG_TAKE_SIZE, hg_buy_room())
                    if qty > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", ask_p, qty))
                        hg_bought += qty

                for bid_p in sorted(hg_od.buy_orders.keys(), reverse=True):
                    if hg_sell_room() <= 0:
                        break
                    if bid_p < hg_qfair + HG_TAKE_EDGE:
                        break
                    vol = hg_od.buy_orders[bid_p]
                    qty = min(vol, HG_TAKE_SIZE, hg_sell_room())
                    if qty > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", bid_p, -qty))
                        hg_sold += qty

                # Aggressive unwind at extremes
                if hg_pos >= HG_UNWIND_THR and hg_sell_room() > 0:
                    uq = min(HG_UNWIND_QTY, hg_sell_room())
                    if uq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uq))
                        hg_sold += uq
                elif hg_pos <= -HG_UNWIND_THR and hg_buy_room() > 0:
                    uq = min(HG_UNWIND_QTY, hg_buy_room())
                    if uq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uq))
                        hg_bought += uq

                # Passive quotes
                half = HG_HALF_SPREAD
                if abs(hg_pos) > HG_POS_CAP * 0.6:
                    half += 1
                hg_bid_px = int(round(hg_qfair - half))
                hg_ask_px = int(round(hg_qfair + half))

                # Don't cross the book
                if hg_bid_px >= hg_ba:
                    hg_bid_px = hg_ba - 1
                if hg_ask_px <= hg_bb:
                    hg_ask_px = hg_bb + 1

                # Inventory-skewed sizing
                if hg_pos > 0:
                    bsz = max(3, HG_PASSIVE_SIZE - int(hg_pos * 0.3))
                    ssz = max(3, HG_PASSIVE_SIZE + int(hg_pos * 0.3))
                elif hg_pos < 0:
                    bsz = max(3, HG_PASSIVE_SIZE + int(-hg_pos * 0.3))
                    ssz = max(3, HG_PASSIVE_SIZE - int(-hg_pos * 0.3))
                else:
                    bsz = HG_PASSIVE_SIZE
                    ssz = HG_PASSIVE_SIZE

                bq = min(bsz, hg_buy_room())
                sq = min(ssz, hg_sell_room())
                if bq > 0:
                    hg_orders.append(Order("HYDROGEL_PACK", hg_bid_px, bq))
                if sq > 0:
                    hg_orders.append(Order("HYDROGEL_PACK", hg_ask_px, -sq))

                result["HYDROGEL_PACK"] = hg_orders

        # ══════════════════════════════════════════════════════════════
        # Get VEX mid for options pricing
        # ══════════════════════════════════════════════════════════════
        vex_mid = None
        vex_od = state.order_depths.get("VELVETFRUIT_EXTRACT")
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_mid = get_microprice(vex_od)

        # ══════════════════════════════════════════════════════════════
        # MODULE 2: Online vol calibration
        # ══════════════════════════════════════════════════════════════
        if vex_mid is not None:
            ivols = []
            for sym in ["VEV_5200", "VEV_5300"]:
                if sym not in state.order_depths:
                    continue
                od = state.order_depths[sym]
                v_mid = get_mid(od)
                if v_mid <= 0:
                    continue
                K = VOUCHER_PRODUCTS[sym]
                iv = bachelier_iv(vex_mid, K, tte_years, v_mid)
                if 200 < iv < 4000:
                    ivols.append(iv)
            if ivols:
                avg_iv = sum(ivols) / len(ivols)
                sigma = SIGMA_EMA_ALPHA * avg_iv + (1 - SIGMA_EMA_ALPHA) * sigma

        # ══════════════════════════════════════════════════════════════
        # MODULE 3: Compute Bachelier fairs and deltas for all vouchers
        # ══════════════════════════════════════════════════════════════
        fairs = {}
        deltas = {}
        if vex_mid is not None:
            for sym, K in VOUCHER_PRODUCTS.items():
                fv = bachelier_call(vex_mid, K, tte_years, sigma)
                intrinsic = max(vex_mid - K, 0.0)
                if fv < intrinsic:
                    fv = intrinsic
                fairs[sym] = fv
                deltas[sym] = bachelier_delta(vex_mid, K, tte_years, sigma)

        # ══════════════════════════════════════════════════════════════
        # MODULE 4: Compute current portfolio delta
        # ══════════════════════════════════════════════════════════════
        vex_pos = state.position.get("VELVETFRUIT_EXTRACT", 0)
        portfolio_delta = float(vex_pos)

        for sym in VOUCHER_PRODUCTS:
            v_pos = state.position.get(sym, 0)
            if sym in deltas:
                portfolio_delta += deltas[sym] * v_pos

        # ══════════════════════════════════════════════════════════════
        # MODULE 5: Voucher options trading (smile bias + residual)
        #   Conservative positions, sized by delta headroom
        # ══════════════════════════════════════════════════════════════
        if vex_mid is not None:
            for sym, K in VOUCHER_PRODUCTS.items():
                if sym not in state.order_depths or sym not in fairs:
                    continue
                od = state.order_depths[sym]
                if not od.buy_orders or not od.sell_orders:
                    continue

                bb = max(od.buy_orders)
                ba = min(od.sell_orders)
                spread = ba - bb
                if spread > VOUCHER_MAX_SPREAD or spread < 1:
                    continue

                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)
                fair = fairs[sym]
                delta = deltas[sym]

                # Update smile bias
                raw_residual = v_mid - fair
                prev_bias = smile_bias.get(sym, 0.0)
                bias = BIAS_ALPHA * raw_residual + (1 - BIAS_ALPHA) * prev_bias
                smile_bias[sym] = bias

                # Smile-adjusted fair
                adj_fair = fair + bias

                # Tradeable deviation
                deviation = raw_residual - bias

                # Inventory penalty
                inv_adj = -VOUCHER_INV_SKEW * (pos / VOUCHER_LIMIT)
                quote_fair = adj_fair + inv_adj

                # Delta headroom: limit passive size based on portfolio delta
                abs_delta = abs(delta)
                if abs_delta > 0.01:
                    delta_headroom = max(0.0, 80.0 - abs(portfolio_delta))
                    max_by_delta = int(delta_headroom / abs_delta)
                else:
                    max_by_delta = VOUCHER_POS_CAP

                effective_cap = min(VOUCHER_POS_CAP, max_by_delta)
                if effective_cap < 2:
                    effective_cap = 2

                orders = []
                bought = 0
                sold = 0

                def v_buy_room():
                    return max(0, min(effective_cap - pos - bought,
                                      VOUCHER_LIMIT - pos - bought))

                def v_sell_room():
                    return max(0, min(effective_cap + pos - sold,
                                      VOUCHER_LIMIT + pos - sold))

                # Aggressive takes on large deviations
                if deviation < -VOUCHER_ENTRY_THR:
                    for ask_p in sorted(od.sell_orders.keys()):
                        if v_buy_room() <= 0:
                            break
                        if ask_p > quote_fair - 0.5:
                            break
                        vol = -od.sell_orders[ask_p]
                        qty = min(vol, VOUCHER_TAKE_SIZE, v_buy_room())
                        if qty > 0:
                            orders.append(Order(sym, ask_p, qty))
                            bought += qty
                            portfolio_delta += delta * qty

                elif deviation > VOUCHER_ENTRY_THR:
                    for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                        if v_sell_room() <= 0:
                            break
                        if bid_p < quote_fair + 0.5:
                            break
                        vol = od.buy_orders[bid_p]
                        qty = min(vol, VOUCHER_TAKE_SIZE, v_sell_room())
                        if qty > 0:
                            orders.append(Order(sym, bid_p, -qty))
                            sold += qty
                            portfolio_delta -= delta * qty

                # Passive quotes (small, wide)
                buy_px = int(round(quote_fair - VOUCHER_PASSIVE_OFFSET))
                sell_px = int(round(quote_fair + VOUCHER_PASSIVE_OFFSET))

                if buy_px >= ba:
                    buy_px = ba - 1
                if sell_px <= bb:
                    sell_px = bb + 1

                psz = min(VOUCHER_PASSIVE_SIZE, max(1, max_by_delta))
                # Skew toward position reducing side
                if pos > 0:
                    bsz = max(1, psz - int(pos * 0.2))
                    ssz = max(1, psz + int(pos * 0.2))
                elif pos < 0:
                    bsz = max(1, psz + int(-pos * 0.2))
                    ssz = max(1, psz - int(-pos * 0.2))
                else:
                    bsz = psz
                    ssz = psz

                bq = min(bsz, v_buy_room())
                sq = min(ssz, v_sell_room())
                if bq > 0 and buy_px > 0:
                    orders.append(Order(sym, buy_px, bq))
                if sq > 0 and sell_px > 0:
                    orders.append(Order(sym, sell_px, -sq))

                result[sym] = orders

        # ══════════════════════════════════════════════════════════════
        # MODULE 6: Delta hedging via VEX (Optiver ASML approach)
        #   When |portfolio_delta| > threshold, trade VEX aggressively
        # ══════════════════════════════════════════════════════════════
        vex_orders = []
        vex_pos_curr = state.position.get("VELVETFRUIT_EXTRACT", 0)
        vex_bought = 0
        vex_sold = 0

        def vex_buy_room():
            return max(0, VEX_LIMIT - vex_pos_curr - vex_bought)

        def vex_sell_room():
            return max(0, VEX_LIMIT + vex_pos_curr - vex_sold)

        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb = max(vex_od.buy_orders)
            vex_ba = min(vex_od.sell_orders)

            # ── Delta hedge trades ──
            if portfolio_delta > DELTA_HEDGE_THR:
                # Net long delta → sell VEX to hedge
                hedge_qty = min(int(portfolio_delta - DELTA_HEDGE_THR * 0.5 + 0.5),
                                MAX_HEDGE_TRADE)
                qty = min(hedge_qty, vex_sell_room())
                if qty > 0:
                    # Sell at best bid (aggressive, IOC-like)
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -qty))
                    vex_sold += qty

            elif portfolio_delta < -DELTA_HEDGE_THR:
                # Net short delta → buy VEX to hedge
                hedge_qty = min(int(-portfolio_delta - DELTA_HEDGE_THR * 0.5 + 0.5),
                                MAX_HEDGE_TRADE)
                qty = min(hedge_qty, vex_buy_room())
                if qty > 0:
                    # Buy at best ask (aggressive, IOC-like)
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, qty))
                    vex_bought += qty

            # ── VEX passive MM with remaining capacity ──
            vex_imb_raw = get_imbalance(vex_od)
            vex_imb_key = "vex_imb"
            vex_imb = VEX_IMB_ALPHA * vex_imb_raw + (1 - VEX_IMB_ALPHA) * sd.get(vex_imb_key, 0.0)
            sd[vex_imb_key] = vex_imb

            vex_micro = get_microprice(vex_od)
            vex_fair = vex_micro - VEX_INV_GAMMA * ((vex_pos_curr + vex_bought - vex_sold) / VEX_LIMIT)
            vex_imb_shift = clamp(VEX_IMB_GAIN * vex_imb, -2.0, 2.0)
            vex_qfair = vex_fair + vex_imb_shift

            # Remaining capacity after hedge reserve
            vex_effective = vex_pos_curr + vex_bought - vex_sold
            vex_mm_room_buy = max(0, (VEX_LIMIT - VEX_HEDGE_RESERVE) - vex_effective)
            vex_mm_room_sell = max(0, (VEX_LIMIT - VEX_HEDGE_RESERVE) + vex_effective)

            # Aggressive VEX takes
            for ask_p in sorted(vex_od.sell_orders.keys()):
                if vex_buy_room() <= 0 or vex_mm_room_buy <= 0:
                    break
                if ask_p > vex_qfair - VEX_TAKE_EDGE:
                    break
                vol = -vex_od.sell_orders[ask_p]
                qty = min(vol, VEX_TAKE_SIZE, vex_buy_room(), vex_mm_room_buy)
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask_p, qty))
                    vex_bought += qty
                    vex_mm_room_buy -= qty

            for bid_p in sorted(vex_od.buy_orders.keys(), reverse=True):
                if vex_sell_room() <= 0 or vex_mm_room_sell <= 0:
                    break
                if bid_p < vex_qfair + VEX_TAKE_EDGE:
                    break
                vol = vex_od.buy_orders[bid_p]
                qty = min(vol, VEX_TAKE_SIZE, vex_sell_room(), vex_mm_room_sell)
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid_p, -qty))
                    vex_sold += qty
                    vex_mm_room_sell -= qty

            # VEX passive quotes
            vex_bid_px = int(round(vex_qfair - VEX_HALF_SPREAD))
            vex_ask_px = int(round(vex_qfair + VEX_HALF_SPREAD))

            if vex_bid_px >= vex_ba:
                vex_bid_px = vex_ba - 1
            if vex_ask_px <= vex_bb:
                vex_ask_px = vex_bb + 1

            bq = min(VEX_MM_SIZE, vex_buy_room(), max(0, vex_mm_room_buy))
            sq = min(VEX_MM_SIZE, vex_sell_room(), max(0, vex_mm_room_sell))
            if bq > 0:
                vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bid_px, bq))
            if sq > 0:
                vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ask_px, -sq))

        if vex_orders:
            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ══════════════════════════════════════════════════════════════
        # Persist state
        # ══════════════════════════════════════════════════════════════
        sd["tick"] = tick
        sd["sigma"] = sigma
        sd["sb"] = smile_bias

        return result, conversions, json.dumps(sd)
