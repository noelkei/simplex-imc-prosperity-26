"""
r3_b08_regime_composite
Strategy: Regime-aware composite (C01+C02+C03) with adaptive parameters.
Inspired by ML Finance book's regime detection and uncertainty-aware sizing.

Regime detection via rolling 20-tick VEX realized vol:
- HIGH vol (rvol > HIGH_THRESH): wider entry/exit, smaller passive sizes,
  faster sigma EMA (adapts to the new vol regime quickly)
- LOW vol (rvol < LOW_THRESH): tighter entry/exit, larger passive sizes,
  slower sigma EMA (more stable in calm markets)
- MED vol: baseline parameters (same as Amin's base)

Key differentiator vs Amin's bots:
- All parameters adapt based on detected market regime
- More aggressive in low vol (better spread capture), more cautious in high vol
- Uncertainty-aware sizing: larger positions only when regime is stable/calm
- Regime state persisted in traderData for continuity across ticks
"""
import json
import math
from datamodel import Order, TradingState


# ---- math helpers ----

def norm_cdf(x: float) -> float:
    if x < -8.0:
        return 0.0
    if x > 8.0:
        return 1.0
    a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
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
    if T <= 0 or sig <= 0:
        return max(S - K, 0.0)
    vt = sig * math.sqrt(T)
    if vt < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vt
    return (S - K) * norm_cdf(d) + vt * norm_pdf(d)


def get_mid(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_spread(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return min(od.sell_orders) - max(od.buy_orders)


def get_imbalance(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = abs(od.sell_orders[ba])
    return (bv - av) / (bv + av) if bv + av > 0 else 0.0


def clamp_qty(qty: int, pos: int, limit: int) -> int:
    if qty > 0:
        return max(0, min(qty, limit - pos))
    if qty < 0:
        return min(0, max(qty, -(limit + pos)))
    return 0


# ---- regime thresholds ----

VOL_WINDOW   = 20    # ticks for regime detection
VEX_VOL_BASE = 2.0   # baseline VEX mid-price tick-to-tick std dev
HIGH_THRESH  = 1.6   # HIGH vol if rvol > HIGH_THRESH * base
LOW_THRESH   = 0.6   # LOW vol if rvol < LOW_THRESH * base

# Regime-specific parameters (tuples: LOW, MED, HIGH)
ENTRY_BY_REGIME  = {"LOW": 2.0, "MED": 3.0, "HIGH": 5.0}
EXIT_BY_REGIME   = {"LOW": 0.3, "MED": 0.5, "HIGH": 1.2}
SIGMA_ALPHA_REG  = {"LOW": 0.05, "MED": 0.10, "HIGH": 0.18}
V_MM_OFFSET_REG  = {"LOW": 1,    "MED": 2,    "HIGH": 4}
V_SIZE_FRAC_REG  = {"LOW": 8,    "MED": 15,   "HIGH": 25}
V_INV_SKEW_REG   = {"LOW": 1.0,  "MED": 1.5,  "HIGH": 2.5}

# Baseline delta-1 parameters (mostly stable across regimes)
DELTA1 = {
    "HYDROGEL_PACK":       200,
    "VELVETFRUIT_EXTRACT": 200,
}
D1_MM_OFFSET   = 2
D1_MM_EDGE     = 1
MAX_D1_SPREAD  = 8
D1_INV_SKEW    = 1.5
IMB_LEAN       = 1

# Delta-1 spread gate loosens in high vol (liquidity may be thinner)
D1_SPREAD_REG  = {"LOW": 6, "MED": 8, "HIGH": 12}

VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}
MAX_V_SPREAD   = 20
TTE_YEARS      = 5 / 365.0

SYMS_BY_STRIKE = sorted(VOUCHER_PRODUCTS, key=lambda s: VOUCHER_PRODUCTS[s][0])


class Trader:

    def run(self, state: TradingState):
        data = {}
        if state.traderData:
            try:
                data = json.loads(state.traderData)
            except Exception:
                data = {}

        sigma_abs = data.get("sigma_abs", 95.0)
        result    = {}

        # ---- VEX mid + regime detection ----
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # rolling VEX mid history for regime detection
        vex_hist = data.get("vex_hist", [])
        if vex_mid is not None:
            vex_hist.append(vex_mid)
            if len(vex_hist) > VOL_WINDOW:
                vex_hist = vex_hist[-VOL_WINDOW:]
        data["vex_hist"] = vex_hist

        # compute rolling realized vol from VEX ticks
        regime = "MED"
        rvol   = VEX_VOL_BASE
        if len(vex_hist) >= 5:
            changes = [vex_hist[i + 1] - vex_hist[i] for i in range(len(vex_hist) - 1)]
            ms2     = sum(c * c for c in changes) / len(changes)
            rvol    = math.sqrt(ms2) if ms2 > 0 else VEX_VOL_BASE
            if rvol > HIGH_THRESH * VEX_VOL_BASE:
                regime = "HIGH"
            elif rvol < LOW_THRESH * VEX_VOL_BASE:
                regime = "LOW"

        data["regime"] = regime

        # ---- sigma update with regime-adaptive alpha ----
        sigma_alpha = SIGMA_ALPHA_REG[regime]
        prev_vex    = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move      = abs(vex_mid - prev_vex)
            daily_vol = move * math.sqrt(1000)
            sigma_abs = sigma_alpha * daily_vol + (1.0 - sigma_alpha) * sigma_abs

        # ---- delta-1 market making ----
        max_d1_spread = D1_SPREAD_REG[regime]
        for product, limit in DELTA1.items():
            if product not in state.order_depths:
                continue
            od     = state.order_depths[product]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > max_d1_spread:
                continue

            pos       = state.position.get(product, 0)
            imbalance = get_imbalance(od)
            inv_adj   = -D1_INV_SKEW * (pos / limit)
            fair      = mid + inv_adj
            lean      = round(IMB_LEAN * imbalance)

            orders = []
            for ask in sorted(od.sell_orders):
                if ask < fair - D1_MM_EDGE:
                    q = clamp_qty(-od.sell_orders[ask], pos, limit)
                    if q > 0:
                        orders.append(Order(product, ask, q))
                        pos += q
            for bid in sorted(od.buy_orders, reverse=True):
                if bid > fair + D1_MM_EDGE:
                    q = clamp_qty(-od.buy_orders[bid], pos, limit)
                    if q < 0:
                        orders.append(Order(product, bid, q))
                        pos += q

            # size scales up in LOW vol, down in HIGH vol
            size_mult = {"LOW": 1.3, "MED": 1.0, "HIGH": 0.7}[regime]
            psz = max(1, int(limit // 10 * size_mult))
            q   = clamp_qty(psz, pos, limit)
            if q > 0:
                orders.append(Order(product, int(round(fair - D1_MM_OFFSET + lean)), q))
            q = clamp_qty(-psz, pos, limit)
            if q < 0:
                orders.append(Order(product, int(round(fair + D1_MM_OFFSET + lean)), q))
            result[product] = orders

        # ---- regime-adaptive voucher quoting ----
        if vex_mid is not None:
            entry   = ENTRY_BY_REGIME[regime]
            ex_thr  = EXIT_BY_REGIME[regime]
            v_off   = V_MM_OFFSET_REG[regime]
            v_sfrac = V_SIZE_FRAC_REG[regime]
            v_iskew = V_INV_SKEW_REG[regime]

            fairs = {}
            for sym, (strike, _) in VOUCHER_PRODUCTS.items():
                fv        = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
                fairs[sym] = max(fv, max(vex_mid - strike, 0.0))

            surface_ok = True
            for i in range(len(SYMS_BY_STRIKE) - 1):
                if fairs[SYMS_BY_STRIKE[i]] < fairs[SYMS_BY_STRIKE[i + 1]] - 0.5:
                    surface_ok = False
                    break

            for sym in SYMS_BY_STRIKE:
                if sym not in state.order_depths:
                    continue
                od     = state.order_depths[sym]
                mid    = get_mid(od)
                spread = get_spread(od)
                if mid is None or spread is None or spread > MAX_V_SPREAD:
                    continue

                strike, limit = VOUCHER_PRODUCTS[sym]
                pos           = state.position.get(sym, 0)
                fair          = fairs[sym]
                imb           = get_imbalance(od)

                residual = mid - fair
                inv_adj  = -v_iskew * (pos / limit)
                adj_fair = fair + inv_adj

                orders = []

                if abs(residual) > entry and surface_ok:
                    if residual < -entry:
                        for ask in sorted(od.sell_orders):
                            if ask < adj_fair - ex_thr:
                                q = clamp_qty(-od.sell_orders[ask], pos, limit)
                                if q > 0:
                                    orders.append(Order(sym, ask, q))
                                    pos += q
                    elif residual > entry:
                        for bid in sorted(od.buy_orders, reverse=True):
                            if bid > adj_fair + ex_thr:
                                q = clamp_qty(-od.buy_orders[bid], pos, limit)
                                if q < 0:
                                    orders.append(Order(sym, bid, q))
                                    pos += q

                lean = round(imb)
                psz  = max(1, limit // v_sfrac)
                bpx  = int(round(adj_fair - v_off + lean))
                apx  = int(round(adj_fair + v_off + lean))

                q = clamp_qty(psz, pos, limit)
                if q > 0 and bpx > 0:
                    orders.append(Order(sym, bpx, q))
                q = clamp_qty(-psz, pos, limit)
                if q < 0 and apx > 0:
                    orders.append(Order(sym, apx, q))

                result[sym] = orders

        # ---- persist ----
        data["sigma_abs"] = sigma_abs
        if vex_mid is not None:
            data["prev_vex"] = vex_mid

        return result, 0, json.dumps(data)
