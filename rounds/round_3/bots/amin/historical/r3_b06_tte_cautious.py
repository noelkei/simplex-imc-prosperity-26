"""
r3_b06_tte_cautious
Strategy: C07 TTE-cautious variant — VEV_5000-5300 + C01+C02 delta-1.

Garcia-Ares 2023: option returns near expiration show different dynamics.
TTE=5d is out-of-sample vs the 6d-8d historical window. This bot is calibrated
for maximum caution on the live round:
- Entry threshold = 5.0 (vs base 3.0, inv 4.0) — only the highest-conviction trades
- Exit threshold = 1.5 (wider — exit more conservatively)
- Two-speed exit: if position is open and |residual| < exit×1.5, start closing
- No aggressive takes unless |residual| > 2×entry (10.0) — very high bar
- Passive size = limit//25 (tiny — just enough to capture spread)
- Wider passive offset (4 ticks vs base 2) to avoid being inside the bid-ask
- Delta-1 stays at standard parameters (delta-1 is less risky near expiry)
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


# ---- parameters ----

SIGMA_DEFAULT = 95.0
SIGMA_ALPHA   = 0.10
TTE_YEARS     = 5 / 365.0

# Standard delta-1 parameters
DELTA1 = {
    "HYDROGEL_PACK":       200,
    "VELVETFRUIT_EXTRACT": 200,
}
MM_OFFSET      = 2
MM_EDGE        = 1
MAX_D1_SPREAD  = 8
D1_INV_SKEW    = 1.5
IMB_LEAN       = 1

# TTE-cautious voucher parameters
VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}
ENTRY_THRESH    = 5.0   # very wide — only highest conviction
EXIT_THRESH     = 1.5   # conservative exit
FORCE_EXIT_MULT = 1.5   # if |residual| < EXIT_THRESH*FORCE_EXIT_MULT and pos != 0, close
HARD_TAKE_MULT  = 2.0   # only aggressive take if |residual| > ENTRY*HARD_TAKE_MULT
MAX_V_SPREAD    = 20
V_MM_OFFSET     = 4     # wider passive offset
V_INV_SKEW      = 2.0   # stronger skew to keep inventory flat
SYMS_BY_STRIKE  = sorted(VOUCHER_PRODUCTS, key=lambda s: VOUCHER_PRODUCTS[s][0])


class Trader:

    def run(self, state: TradingState):
        data = {}
        if state.traderData:
            try:
                data = json.loads(state.traderData)
            except Exception:
                data = {}

        sigma_abs = data.get("sigma_abs", SIGMA_DEFAULT)
        result    = {}

        # ---- VEX mid ----
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # ---- sigma update ----
        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move      = abs(vex_mid - prev_vex)
            daily_vol = move * math.sqrt(1000)
            sigma_abs = SIGMA_ALPHA * daily_vol + (1.0 - SIGMA_ALPHA) * sigma_abs

        # ---- delta-1 (standard Amin-style MM) ----
        for product, limit in DELTA1.items():
            if product not in state.order_depths:
                continue
            od     = state.order_depths[product]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > MAX_D1_SPREAD:
                continue

            pos       = state.position.get(product, 0)
            imbalance = get_imbalance(od)
            inv_adj   = -D1_INV_SKEW * (pos / limit)
            fair      = mid + inv_adj
            lean      = round(IMB_LEAN * imbalance)

            orders = []
            for ask in sorted(od.sell_orders):
                if ask < fair - MM_EDGE:
                    q = clamp_qty(-od.sell_orders[ask], pos, limit)
                    if q > 0:
                        orders.append(Order(product, ask, q))
                        pos += q
            for bid in sorted(od.buy_orders, reverse=True):
                if bid > fair + MM_EDGE:
                    q = clamp_qty(-od.buy_orders[bid], pos, limit)
                    if q < 0:
                        orders.append(Order(product, bid, q))
                        pos += q

            psz = max(1, limit // 10)
            q   = clamp_qty(psz, pos, limit)
            if q > 0:
                orders.append(Order(product, int(round(fair - MM_OFFSET + lean)), q))
            q = clamp_qty(-psz, pos, limit)
            if q < 0:
                orders.append(Order(product, int(round(fair + MM_OFFSET + lean)), q))
            result[product] = orders

        # ---- TTE-cautious vouchers ----
        if vex_mid is not None:
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
                residual      = mid - fair
                inv_adj       = -V_INV_SKEW * (pos / limit)
                adj_fair      = fair + inv_adj

                orders = []
                bb     = max(od.buy_orders)
                ba     = min(od.sell_orders)

                hard_take_thr = ENTRY_THRESH * HARD_TAKE_MULT  # = 10.0

                # Only aggressive take if signal is very strong
                if abs(residual) > hard_take_thr and surface_ok:
                    if residual < -hard_take_thr:
                        for ask in sorted(od.sell_orders):
                            if ask < adj_fair - EXIT_THRESH:
                                q = clamp_qty(-od.sell_orders[ask], pos, limit)
                                if q > 0:
                                    orders.append(Order(sym, ask, q))
                                    pos += q
                    elif residual > hard_take_thr:
                        for bid in sorted(od.buy_orders, reverse=True):
                            if bid > adj_fair + EXIT_THRESH:
                                q = clamp_qty(-od.buy_orders[bid], pos, limit)
                                if q < 0:
                                    orders.append(Order(sym, bid, q))
                                    pos += q

                # Two-speed force exit: if position is open but signal is fading, close
                force_exit_zone = EXIT_THRESH * FORCE_EXIT_MULT
                if pos > 0 and residual > -force_exit_zone:
                    # Long but residual has reverted toward fair → sell to flatten
                    q = clamp_qty(-min(pos, max(1, limit // 20)), pos, limit)
                    if q < 0 and bb is not None:
                        orders.append(Order(sym, bb, q))
                        pos += q
                elif pos < 0 and residual < force_exit_zone:
                    # Short but residual has reverted → buy to flatten
                    q = clamp_qty(min(-pos, max(1, limit // 20)), pos, limit)
                    if q > 0 and ba is not None:
                        orders.append(Order(sym, ba, q))
                        pos += q

                # Tiny passive quotes (just enough to capture spread)
                psz  = max(1, limit // 25)
                bpx  = int(round(adj_fair - V_MM_OFFSET))
                apx  = int(round(adj_fair + V_MM_OFFSET))

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
