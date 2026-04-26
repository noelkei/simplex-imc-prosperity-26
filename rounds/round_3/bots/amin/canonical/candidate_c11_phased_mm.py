"""
C11 Phased Market Making + Delta-Hedged Options
=================================================
Key innovation: TIME-PHASED risk management

Phase 1 (tick 1-30000, ~day 1-1.5): AGGRESSIVE
  - Highest position caps, tightest quotes, most takes
  - Goal: accumulate PnL while risk is affordable

Phase 2 (tick 30001-80000, ~day 1.5-4): STANDARD
  - Moderate caps, standard quotes
  - Goal: steady income, protect early gains

Phase 3 (tick 80001-100000, ~last day): CONSERVATIVE + UNWIND
  - Caps decrease linearly to zero
  - Stop opening new positions in last 5K ticks
  - Aggressively unwind all positions
  - Goal: close near zero inventory, preserve capital

Architecture:
  - HYDROGEL MM: Primary income (spread=15.7, ac1=-0.13, half-spread/vol=4.7)
  - VEX: Delta hedge vehicle + secondary MM
  - Vouchers: Small positions, portfolio-delta-hedged
  - Avellaneda-Stoikov reservation pricing with phase-dependent gamma

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


def get_mid(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


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
# Constants
# ─────────────────────────────────────────────────────────────────────

VOUCHER_PRODUCTS = {
    "VEV_5000": 5000,
    "VEV_5100": 5100,
    "VEV_5200": 5200,
    "VEV_5300": 5300,
}
VOUCHER_LIMIT = 300
HYDROGEL_LIMIT = 200
VEX_LIMIT = 200

SIGMA_DEFAULT = 1160.0
SIGMA_EMA_ALPHA = 0.03

SMILE_BIAS = {
    "VEV_5000": -3.0,
    "VEV_5100": -3.2,
    "VEV_5200": 1.3,
    "VEV_5300": 2.8,
}
BIAS_ALPHA = 0.005

TTE_START_DAYS = 5.0
TICKS_PER_DAY = 20000  # 100K ticks / 5 days

# Phase boundaries (100K total ticks)
PHASE1_END = 30000     # End of aggressive phase (~1.5 days)
PHASE2_END = 80000     # End of standard phase (~4 days)
TOTAL_TICKS = 100000
STOP_NEW_POS = 95000   # Stop opening new positions in last 5K ticks

# IMB EMA
IMB_ALPHA = 0.3
IMB_GAIN = 2.0


# ─────────────────────────────────────────────────────────────────────
# Phase-dependent parameters
# ─────────────────────────────────────────────────────────────────────

def get_phase_params(tick):
    """Returns parameter dict based on current tick/phase."""
    if tick <= PHASE1_END:
        # PHASE 1: AGGRESSIVE — maximize PnL accumulation
        return {
            "hg_pos_cap": 120,
            "hg_half_spread": 2,
            "hg_take_edge": 2,
            "hg_passive_size": 35,
            "hg_take_size": 25,
            "hg_inv_gamma": 1.5,
            "hg_unwind_thr": 90,
            "hg_unwind_qty": 20,
            "vex_mm_size": 15,
            "vex_half_spread": 1,
            "vex_take_edge": 1,
            "vex_take_size": 15,
            "vex_inv_gamma": 1.5,
            "vex_hedge_reserve": 100,
            "v_pos_cap": 25,
            "v_passive_size": 10,
            "v_passive_offset": 2,
            "v_entry_thr": 2.5,
            "v_take_size": 8,
            "v_inv_skew": 2.5,
            "delta_hedge_thr": 20,
            "max_hedge": 30,
        }
    elif tick <= PHASE2_END:
        # PHASE 2: STANDARD — steady income, protect gains
        return {
            "hg_pos_cap": 80,
            "hg_half_spread": 3,
            "hg_take_edge": 3,
            "hg_passive_size": 25,
            "hg_take_size": 15,
            "hg_inv_gamma": 2.5,
            "hg_unwind_thr": 55,
            "hg_unwind_qty": 15,
            "vex_mm_size": 10,
            "vex_half_spread": 2,
            "vex_take_edge": 2,
            "vex_take_size": 10,
            "vex_inv_gamma": 2.5,
            "vex_hedge_reserve": 120,
            "v_pos_cap": 15,
            "v_passive_size": 6,
            "v_passive_offset": 3,
            "v_entry_thr": 3.0,
            "v_take_size": 5,
            "v_inv_skew": 3.0,
            "delta_hedge_thr": 15,
            "max_hedge": 25,
        }
    else:
        # PHASE 3: CONSERVATIVE + UNWIND — preserve capital
        # Linear reduction from tick 80001 to 100000
        progress = (tick - PHASE2_END) / (TOTAL_TICKS - PHASE2_END)  # 0 → 1
        fade = max(0.0, 1.0 - progress * 1.2)  # goes to 0 at tick ~96667

        cap_hg = max(5, int(40 * fade))
        cap_v = max(0, int(8 * fade))

        return {
            "hg_pos_cap": cap_hg,
            "hg_half_spread": 4,
            "hg_take_edge": 4,
            "hg_passive_size": max(3, int(15 * fade)),
            "hg_take_size": max(3, int(10 * fade)),
            "hg_inv_gamma": 4.0,
            "hg_unwind_thr": max(3, int(cap_hg * 0.5)),
            "hg_unwind_qty": 20,  # aggressive unwind
            "vex_mm_size": max(2, int(6 * fade)),
            "vex_half_spread": 3,
            "vex_take_edge": 3,
            "vex_take_size": max(2, int(5 * fade)),
            "vex_inv_gamma": 4.0,
            "vex_hedge_reserve": 150,
            "v_pos_cap": cap_v,
            "v_passive_size": max(1, int(3 * fade)),
            "v_passive_offset": 4,
            "v_entry_thr": 4.0,
            "v_take_size": max(1, int(3 * fade)),
            "v_inv_skew": 5.0,
            "delta_hedge_thr": 10,
            "max_hedge": 30,
        }


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

        tick = sd.get("t", 0) + 1
        sigma = sd.get("s", SIGMA_DEFAULT)
        smile_bias = sd.get("b", dict(SMILE_BIAS))

        # Dynamic TTE
        tte_days = max(TTE_START_DAYS - tick / TICKS_PER_DAY, 0.3)
        tte_years = tte_days / 365.0

        # Get phase parameters
        pp = get_phase_params(tick)

        # Check if we should stop opening new positions
        no_new_pos = tick > STOP_NEW_POS

        # ──────────────────────────────────────────────────────
        # MODULE 1: HYDROGEL Market Making
        # ──────────────────────────────────────────────────────
        hg_od = state.order_depths.get("HYDROGEL_PACK")
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb = max(hg_od.buy_orders)
            hg_ba = min(hg_od.sell_orders)
            hg_spread = hg_ba - hg_bb

            if hg_spread >= 1:
                hg_pos = state.position.get("HYDROGEL_PACK", 0)
                hg_cap = pp["hg_pos_cap"]

                # Fair value: EMA-smoothed microprice
                hg_micro = get_microprice(hg_od)
                hg_fair_key = "hf"
                prev_fair = sd.get(hg_fair_key, hg_micro)
                # EMA smooth (alpha=0.5 — responsive but not noisy)
                hg_fair_ema = 0.5 * hg_micro + 0.5 * prev_fair
                sd[hg_fair_key] = hg_fair_ema

                # EMA imbalance
                hg_imb_raw = get_imbalance(hg_od)
                hg_imb = IMB_ALPHA * hg_imb_raw + (1 - IMB_ALPHA) * sd.get("hi", 0.0)
                sd["hi"] = hg_imb

                # Avellaneda-Stoikov reservation price
                gamma = pp["hg_inv_gamma"]
                hg_res = hg_fair_ema - gamma * (hg_pos / hg_cap) if hg_cap > 0 else hg_fair_ema
                hg_imb_shift = clamp(IMB_GAIN * hg_imb, -3.0, 3.0)
                hg_qfair = hg_res + hg_imb_shift

                hg_orders = []
                hg_bought = 0
                hg_sold = 0

                def hg_buy_room():
                    return max(0, min(hg_cap, HYDROGEL_LIMIT) - hg_pos - hg_bought)

                def hg_sell_room():
                    return max(0, min(hg_cap, HYDROGEL_LIMIT) + hg_pos - hg_sold)

                # Aggressive takes
                if not no_new_pos:
                    for ask_p in sorted(hg_od.sell_orders.keys()):
                        if hg_buy_room() <= 0:
                            break
                        if ask_p > hg_qfair - pp["hg_take_edge"]:
                            break
                        vol = -hg_od.sell_orders[ask_p]
                        qty = min(vol, pp["hg_take_size"], hg_buy_room())
                        if qty > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", ask_p, qty))
                            hg_bought += qty

                    for bid_p in sorted(hg_od.buy_orders.keys(), reverse=True):
                        if hg_sell_room() <= 0:
                            break
                        if bid_p < hg_qfair + pp["hg_take_edge"]:
                            break
                        vol = hg_od.buy_orders[bid_p]
                        qty = min(vol, pp["hg_take_size"], hg_sell_room())
                        if qty > 0:
                            hg_orders.append(Order("HYDROGEL_PACK", bid_p, -qty))
                            hg_sold += qty

                # Aggressive unwind (always active, stronger in late phases)
                if hg_pos >= pp["hg_unwind_thr"]:
                    uq = min(pp["hg_unwind_qty"], HYDROGEL_LIMIT + hg_pos - hg_sold)
                    if uq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uq))
                        hg_sold += uq
                elif hg_pos <= -pp["hg_unwind_thr"]:
                    uq = min(pp["hg_unwind_qty"], HYDROGEL_LIMIT - hg_pos - hg_bought)
                    if uq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uq))
                        hg_bought += uq

                # Phase 3 extra unwind: aggressively push position toward zero
                if tick > PHASE2_END and abs(hg_pos) > 5:
                    if hg_pos > 0:
                        uw = min(15, hg_pos, HYDROGEL_LIMIT + hg_pos - hg_sold)
                        if uw > 0:
                            # Hit the best bid to ensure fill
                            hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uw))
                            hg_sold += uw
                    elif hg_pos < 0:
                        uw = min(15, -hg_pos, HYDROGEL_LIMIT - hg_pos - hg_bought)
                        if uw > 0:
                            # Lift the best ask to ensure fill
                            hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uw))
                            hg_bought += uw

                # Passive quotes
                if not no_new_pos:
                    half = pp["hg_half_spread"]
                    if abs(hg_pos) > hg_cap * 0.6:
                        half += 1

                    hg_bid_px = int(round(hg_qfair - half))
                    hg_ask_px = int(round(hg_qfair + half))

                    if hg_bid_px >= hg_ba:
                        hg_bid_px = hg_ba - 1
                    if hg_ask_px <= hg_bb:
                        hg_ask_px = hg_bb + 1

                    psz = pp["hg_passive_size"]
                    if hg_pos > 0:
                        bsz = max(3, psz - int(hg_pos * 0.3))
                        ssz = max(3, psz + int(hg_pos * 0.3))
                    elif hg_pos < 0:
                        bsz = max(3, psz + int(-hg_pos * 0.3))
                        ssz = max(3, psz - int(-hg_pos * 0.3))
                    else:
                        bsz = psz
                        ssz = psz

                    bq = min(bsz, hg_buy_room())
                    sq = min(ssz, hg_sell_room())
                    if bq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_bid_px, bq))
                    if sq > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", hg_ask_px, -sq))

                result["HYDROGEL_PACK"] = hg_orders

        # ──────────────────────────────────────────────────────
        # Get VEX mid for options pricing
        # ──────────────────────────────────────────────────────
        vex_mid = None
        vex_od = state.order_depths.get("VELVETFRUIT_EXTRACT")
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_mid = get_microprice(vex_od)

        # ──────────────────────────────────────────────────────
        # MODULE 2: Vol calibration
        # ──────────────────────────────────────────────────────
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

        # ──────────────────────────────────────────────────────
        # MODULE 3: Bachelier fairs and deltas
        # ──────────────────────────────────────────────────────
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

        # ──────────────────────────────────────────────────────
        # MODULE 4: Portfolio delta
        # ──────────────────────────────────────────────────────
        vex_pos = state.position.get("VELVETFRUIT_EXTRACT", 0)
        portfolio_delta = float(vex_pos)
        for sym in VOUCHER_PRODUCTS:
            v_pos = state.position.get(sym, 0)
            if sym in deltas:
                portfolio_delta += deltas[sym] * v_pos

        # ──────────────────────────────────────────────────────
        # MODULE 5: Voucher options trading
        # ──────────────────────────────────────────────────────
        if vex_mid is not None and pp["v_pos_cap"] > 0:
            for sym, K in VOUCHER_PRODUCTS.items():
                if sym not in state.order_depths or sym not in fairs:
                    continue
                od = state.order_depths[sym]
                if not od.buy_orders or not od.sell_orders:
                    continue

                bb = max(od.buy_orders)
                ba = min(od.sell_orders)
                spread = ba - bb
                if spread > 15 or spread < 1:
                    continue

                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)
                fair = fairs[sym]
                delta = deltas[sym]

                raw_residual = v_mid - fair
                prev_bias = smile_bias.get(sym, 0.0)
                bias = BIAS_ALPHA * raw_residual + (1 - BIAS_ALPHA) * prev_bias
                smile_bias[sym] = bias

                adj_fair = fair + bias
                deviation = raw_residual - bias
                inv_adj = -pp["v_inv_skew"] * (pos / VOUCHER_LIMIT)
                quote_fair = adj_fair + inv_adj

                # Delta headroom
                abs_delta = abs(delta)
                if abs_delta > 0.01:
                    delta_hroom = max(0.0, 60.0 - abs(portfolio_delta))
                    max_by_delta = int(delta_hroom / abs_delta)
                else:
                    max_by_delta = pp["v_pos_cap"]

                eff_cap = min(pp["v_pos_cap"], max_by_delta)
                if eff_cap < 1:
                    eff_cap = 1

                orders = []
                bought = 0
                sold = 0

                def v_buy_room():
                    return max(0, min(eff_cap - pos - bought,
                                      VOUCHER_LIMIT - pos - bought))

                def v_sell_room():
                    return max(0, min(eff_cap + pos - sold,
                                      VOUCHER_LIMIT + pos - sold))

                # Aggressive takes
                if not no_new_pos and abs(deviation) > pp["v_entry_thr"]:
                    if deviation < -pp["v_entry_thr"]:
                        for ask_p in sorted(od.sell_orders.keys()):
                            if v_buy_room() <= 0:
                                break
                            if ask_p > quote_fair - 0.5:
                                break
                            vol = -od.sell_orders[ask_p]
                            qty = min(vol, pp["v_take_size"], v_buy_room())
                            if qty > 0:
                                orders.append(Order(sym, ask_p, qty))
                                bought += qty
                                portfolio_delta += delta * qty
                    else:
                        for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                            if v_sell_room() <= 0:
                                break
                            if bid_p < quote_fair + 0.5:
                                break
                            vol = od.buy_orders[bid_p]
                            qty = min(vol, pp["v_take_size"], v_sell_room())
                            if qty > 0:
                                orders.append(Order(sym, bid_p, -qty))
                                sold += qty
                                portfolio_delta -= delta * qty

                # Phase 3 unwind vouchers
                if tick > PHASE2_END and abs(pos) > 2:
                    if pos > 0:
                        uq = min(10, pos, VOUCHER_LIMIT + pos - sold)
                        if uq > 0:
                            orders.append(Order(sym, bb, -uq))
                            sold += uq
                    elif pos < 0:
                        uq = min(10, -pos, VOUCHER_LIMIT - pos - bought)
                        if uq > 0:
                            orders.append(Order(sym, ba, uq))
                            bought += uq

                # Passive quotes (not in final phase)
                if not no_new_pos:
                    buy_px = int(round(quote_fair - pp["v_passive_offset"]))
                    sell_px = int(round(quote_fair + pp["v_passive_offset"]))
                    if buy_px >= ba:
                        buy_px = ba - 1
                    if sell_px <= bb:
                        sell_px = bb + 1

                    psz = pp["v_passive_size"]
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

        # ──────────────────────────────────────────────────────
        # MODULE 6: VEX — Delta hedge + secondary MM
        # ──────────────────────────────────────────────────────
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

            # ── Delta hedge ──
            dh_thr = pp["delta_hedge_thr"]
            if portfolio_delta > dh_thr:
                hedge_qty = min(int(portfolio_delta - dh_thr * 0.5 + 0.5),
                                pp["max_hedge"])
                qty = min(hedge_qty, vex_sell_room())
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -qty))
                    vex_sold += qty
            elif portfolio_delta < -dh_thr:
                hedge_qty = min(int(-portfolio_delta - dh_thr * 0.5 + 0.5),
                                pp["max_hedge"])
                qty = min(hedge_qty, vex_buy_room())
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, qty))
                    vex_bought += qty

            # Phase 3 VEX unwind (push VEX position toward zero too)
            if tick > PHASE2_END and abs(vex_pos_curr) > 5:
                if vex_pos_curr > 0 and vex_sell_room() > 0:
                    uw = min(15, vex_pos_curr, vex_sell_room())
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -uw))
                    vex_sold += uw
                elif vex_pos_curr < 0 and vex_buy_room() > 0:
                    uw = min(15, -vex_pos_curr, vex_buy_room())
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, uw))
                    vex_bought += uw

            # ── VEX passive MM ──
            if not no_new_pos:
                vex_imb_raw = get_imbalance(vex_od)
                vex_imb = IMB_ALPHA * vex_imb_raw + (1 - IMB_ALPHA) * sd.get("vi", 0.0)
                sd["vi"] = vex_imb

                vex_eff_pos = vex_pos_curr + vex_bought - vex_sold
                gamma_v = pp["vex_inv_gamma"]
                vex_micro = get_microprice(vex_od)
                vex_res = vex_micro - gamma_v * (vex_eff_pos / VEX_LIMIT)
                vex_imb_shift = clamp(1.5 * vex_imb, -2.0, 2.0)
                vex_qfair = vex_res + vex_imb_shift

                # VEX MM capacity (reserve for hedge)
                reserve = pp["vex_hedge_reserve"]
                vex_mm_buy = max(0, (VEX_LIMIT - reserve) - vex_eff_pos)
                vex_mm_sell = max(0, (VEX_LIMIT - reserve) + vex_eff_pos)

                # Aggressive VEX takes
                for ask_p in sorted(vex_od.sell_orders.keys()):
                    if vex_buy_room() <= 0 or vex_mm_buy <= 0:
                        break
                    if ask_p > vex_qfair - pp["vex_take_edge"]:
                        break
                    vol = -vex_od.sell_orders[ask_p]
                    qty = min(vol, pp["vex_take_size"], vex_buy_room(), vex_mm_buy)
                    if qty > 0:
                        vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask_p, qty))
                        vex_bought += qty
                        vex_mm_buy -= qty

                for bid_p in sorted(vex_od.buy_orders.keys(), reverse=True):
                    if vex_sell_room() <= 0 or vex_mm_sell <= 0:
                        break
                    if bid_p < vex_qfair + pp["vex_take_edge"]:
                        break
                    vol = vex_od.buy_orders[bid_p]
                    qty = min(vol, pp["vex_take_size"], vex_sell_room(), vex_mm_sell)
                    if qty > 0:
                        vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid_p, -qty))
                        vex_sold += qty
                        vex_mm_sell -= qty

                # VEX passive quotes
                vhalf = pp["vex_half_spread"]
                vex_bid_px = int(round(vex_qfair - vhalf))
                vex_ask_px = int(round(vex_qfair + vhalf))

                if vex_bid_px >= vex_ba:
                    vex_bid_px = vex_ba - 1
                if vex_ask_px <= vex_bb:
                    vex_ask_px = vex_bb + 1

                bq = min(pp["vex_mm_size"], vex_buy_room(), max(0, vex_mm_buy))
                sq = min(pp["vex_mm_size"], vex_sell_room(), max(0, vex_mm_sell))
                if bq > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bid_px, bq))
                if sq > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ask_px, -sq))

        if vex_orders:
            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ──────────────────────────────────────────────────────
        # Persist state (compact keys to save space)
        # ──────────────────────────────────────────────────────
        sd["t"] = tick
        sd["s"] = sigma
        sd["b"] = smile_bias

        return result, conversions, json.dumps(sd)
