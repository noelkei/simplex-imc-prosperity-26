"""
final_v1_calibrated_mm
Fixed Bachelier with per-strike sigma table calibrated to Round 3 EDA mean mids.
Core fix: sigma_abs=95 → hardcoded per-strike sigma matching observed prices at S=5250.
Delta-1: Optiver-v3 MM on HYDROGEL + VEX with inventory skew and imbalance lean.
Vouchers: VEV_5000-5500, larger passive sizes (limit//5=60), Fengler surface check.
"""
import json
import math
from datamodel import Order, TradingState


def norm_cdf(x):
    if x < -8: return 0.0
    if x > 8: return 1.0
    a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
    sign = 1.0
    if x < 0:
        sign = -1.0; x = -x
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + sign * y)


def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def bachelier_call(S, K, T, sigma):
    if T <= 0 or sigma <= 0:
        return max(S - K, 0.0)
    vt = sigma * math.sqrt(T)
    if vt < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vt
    return (S - K) * norm_cdf(d) + vt * norm_pdf(d)


def get_mid(od):
    if not od.buy_orders or not od.sell_orders: return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_spread(od):
    if not od.buy_orders or not od.sell_orders: return None
    return min(od.sell_orders) - max(od.buy_orders)


def get_imb(od):
    if not od.buy_orders or not od.sell_orders: return 0.0
    bb = max(od.buy_orders); ba = min(od.sell_orders)
    bv = od.buy_orders[bb]; av = abs(od.sell_orders[ba])
    return (bv - av) / (bv + av) if bv + av > 0 else 0.0


def clamp(qty, pos, lim):
    if qty > 0: return max(0, min(qty, lim - pos))
    if qty < 0: return min(0, max(qty, -(lim + pos)))
    return 0


# Calibrated per-strike Bachelier absolute vol (annual) — S≈5250, T=5/365
# Calibrated via binary search to match EDA mean mids in Round 3 historical data
SIGMA_TABLE = {5000: 1243, 5100: 1280, 5200: 1412, 5300: 1442, 5400: 1255, 5500: 1330}
VOUCHERS    = {f"VEV_{k}": k for k in SIGMA_TABLE}
V_LIMIT     = 300
TTE         = 5 / 365.0

D1_PRODS    = {"HYDROGEL_PACK": 200, "VELVETFRUIT_EXTRACT": 200}
D1_OFFSET   = 2
D1_EDGE     = 1
D1_MAX_SPR  = 10
D1_INV_SKEW = 1.5
IMB_LEAN    = 1
D1_SIZE     = 20

V_OFFSET    = 2
V_SIZE      = 60        # limit // 5
V_INV_SKEW  = 1.5
ENTRY       = 5.0       # residual threshold for aggressive takes
MAX_V_SPR   = 25


class Trader:

    def run(self, state: TradingState):
        result = {}

        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # ---- delta-1 MM ----
        for prod, lim in D1_PRODS.items():
            if prod not in state.order_depths: continue
            od     = state.order_depths[prod]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > D1_MAX_SPR: continue

            pos  = state.position.get(prod, 0)
            imb  = get_imb(od)
            fair = mid - D1_INV_SKEW * (pos / lim)
            lean = round(IMB_LEAN * imb)

            orders = []
            for ask in sorted(od.sell_orders):
                if ask < fair - D1_EDGE:
                    q = clamp(-od.sell_orders[ask], pos, lim)
                    if q > 0: orders.append(Order(prod, ask, q)); pos += q
            for bid in sorted(od.buy_orders, reverse=True):
                if bid > fair + D1_EDGE:
                    q = clamp(-od.buy_orders[bid], pos, lim)
                    if q < 0: orders.append(Order(prod, bid, q)); pos += q

            q = clamp(D1_SIZE, pos, lim)
            if q > 0: orders.append(Order(prod, int(round(fair - D1_OFFSET + lean)), q))
            q = clamp(-D1_SIZE, pos, lim)
            if q < 0: orders.append(Order(prod, int(round(fair + D1_OFFSET + lean)), q))
            result[prod] = orders

        # ---- voucher MM (calibrated Bachelier) ----
        if vex_mid is None:
            return result, 0, ""

        fairs = {}
        syms  = sorted(VOUCHERS, key=lambda s: VOUCHERS[s])
        for sym in syms:
            K    = VOUCHERS[sym]
            sig  = SIGMA_TABLE[K]
            fv   = bachelier_call(vex_mid, K, TTE, sig)
            fairs[sym] = max(fv, max(vex_mid - K, 0.0))

        # Fengler monotonicity check (lower strike ≥ higher strike)
        surface_ok = all(
            fairs[syms[i]] >= fairs[syms[i + 1]] - 0.5
            for i in range(len(syms) - 1)
        )

        for sym in syms:
            if sym not in state.order_depths: continue
            od     = state.order_depths[sym]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > MAX_V_SPR: continue

            K    = VOUCHERS[sym]
            pos  = state.position.get(sym, 0)
            fair = fairs[sym]
            imb  = get_imb(od)

            inv_adj  = -V_INV_SKEW * (pos / V_LIMIT)
            adj_fair = fair + inv_adj
            residual = mid - fair

            orders = []

            # aggressive take on strong mispricing
            if surface_ok and abs(residual) > ENTRY:
                if residual < -ENTRY:
                    for ask in sorted(od.sell_orders):
                        if ask < adj_fair:
                            q = clamp(-od.sell_orders[ask], pos, V_LIMIT)
                            if q > 0: orders.append(Order(sym, ask, q)); pos += q
                else:
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid > adj_fair:
                            q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                            if q < 0: orders.append(Order(sym, bid, q)); pos += q

            # passive two-level quoting
            bpx = int(round(adj_fair - V_OFFSET))
            apx = int(round(adj_fair + V_OFFSET))
            q = clamp(V_SIZE, pos, V_LIMIT)
            if q > 0 and bpx > 0: orders.append(Order(sym, bpx, q))
            q = clamp(-V_SIZE, pos, V_LIMIT)
            if q < 0 and apx > 0: orders.append(Order(sym, apx, q))

            result[sym] = orders

        return result, 0, ""
