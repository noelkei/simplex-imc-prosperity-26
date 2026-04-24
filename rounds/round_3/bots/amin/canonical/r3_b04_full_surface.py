"""
r3_b04_full_surface
Strategy: Full 8-voucher surface (VEV_4000 to VEV_5500) + C01+C02 delta-1 MM.

Key differentiators vs Amin's bots:
- Trades ALL 8 active strikes (Amin only trades VEV_5000-5300)
- Fengler 2005 convexity check: call price must be convex across strikes
  (fairs[K] - 2*fairs[K+D] + fairs[K+2D] >= -1 for consecutive K triplets)
- Per-strike spread gate: ITM strikes allow wider spreads (up to 30), OTM up to 50
- Per-strike passive sizing based on moneyness proximity:
  near-ATM → larger size; deep ITM/OTM → smaller size
- VEV_6000/6500 excluded (constant-floor, zero alpha per strategy)
- ITM vouchers also use intrinsic floor: fair >= max(S-K, 0)
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
SIGMA_ALPHA   = 0.08
TTE_YEARS     = 5 / 365.0

# Delta-1 products
DELTA1 = {
    "HYDROGEL_PACK":       200,
    "VELVETFRUIT_EXTRACT": 200,
}
MM_OFFSET      = 2
MM_EDGE        = 1
MAX_D1_SPREAD  = 8
INV_SKEW       = 1.5
IMBALANCE_LEAN = 1

# All active vouchers (VEV_6000/6500 excluded per strategy)
VOUCHERS = {
    "VEV_4000": (4000, 300),
    "VEV_4500": (4500, 300),
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
    "VEV_5400": (5400, 300),
    "VEV_5500": (5500, 300),
}

ENTRY_THRESH = 3.0
EXIT_THRESH  = 0.5
V_INV_SKEW   = 1.5
V_MM_OFFSET  = 2

# Per-strike spread gates (ITM allows wider spread)
SPREAD_GATES = {
    "VEV_4000": 35, "VEV_4500": 30,
    "VEV_5000": 20, "VEV_5100": 20, "VEV_5200": 20, "VEV_5300": 25,
    "VEV_5400": 35, "VEV_5500": 50,
}

# Passive size fraction (limit // this value); near-ATM gets bigger
SIZE_FRACS = {
    "VEV_4000": 20, "VEV_4500": 15,
    "VEV_5000": 12, "VEV_5100": 10, "VEV_5200": 10, "VEV_5300": 12,
    "VEV_5400": 18, "VEV_5500": 25,
}

SYMS_BY_STRIKE = sorted(VOUCHERS, key=lambda s: VOUCHERS[s][0])


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

        # ---- update sigma_abs ----
        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move      = abs(vex_mid - prev_vex)
            daily_vol = move * math.sqrt(1000)
            sigma_abs = SIGMA_ALPHA * daily_vol + (1.0 - SIGMA_ALPHA) * sigma_abs

        # ---- delta-1 MM ----
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
            inv_adj   = -INV_SKEW * (pos / limit)
            fair      = mid + inv_adj
            lean      = round(IMBALANCE_LEAN * imbalance)

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

        # ---- full voucher surface ----
        if vex_mid is not None:
            # compute Bachelier fairs for all strikes
            fairs = {}
            for sym, (strike, _) in VOUCHERS.items():
                fv         = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
                intrinsic  = max(vex_mid - strike, 0.0)
                fairs[sym] = max(fv, intrinsic)

            # monotonicity check (standard)
            monotone_ok = True
            for i in range(len(SYMS_BY_STRIKE) - 1):
                s0, s1 = SYMS_BY_STRIKE[i], SYMS_BY_STRIKE[i + 1]
                if fairs[s0] < fairs[s1] - 0.5:
                    monotone_ok = False
                    break

            # Fengler 2005 convexity check: for triplets K, K+D, K+2D,
            # call prices must be convex (butterfly spread >= -1 ticks)
            convex_ok = True
            for i in range(len(SYMS_BY_STRIKE) - 2):
                s0, s1, s2 = SYMS_BY_STRIKE[i], SYMS_BY_STRIKE[i + 1], SYMS_BY_STRIKE[i + 2]
                butterfly  = fairs[s0] - 2.0 * fairs[s1] + fairs[s2]
                if butterfly < -1.0:
                    convex_ok = False
                    break

            surface_ok = monotone_ok and convex_ok

            # family exposure (Bergault) — aggregate normalized position
            total_norm = sum(
                state.position.get(sym, 0) / VOUCHERS[sym][1]
                for sym in VOUCHERS
                if sym in state.order_depths
            )
            n_active   = sum(1 for sym in VOUCHERS if sym in state.order_depths)
            family_exp = total_norm / n_active if n_active > 0 else 0.0

            for sym in SYMS_BY_STRIKE:
                if sym not in state.order_depths:
                    continue
                od     = state.order_depths[sym]
                mid    = get_mid(od)
                spread = get_spread(od)
                max_sp = SPREAD_GATES.get(sym, 25)
                if mid is None or spread is None or spread > max_sp:
                    continue

                strike, limit = VOUCHERS[sym]
                pos           = state.position.get(sym, 0)
                fair          = fairs[sym]
                imbalance     = get_imbalance(od)

                residual = mid - fair
                inv_adj  = -V_INV_SKEW * (pos / limit) - 0.4 * family_exp
                adj_fair = fair + inv_adj

                orders = []

                if abs(residual) > ENTRY_THRESH and surface_ok:
                    if residual < -ENTRY_THRESH:
                        for ask in sorted(od.sell_orders):
                            if ask < adj_fair - EXIT_THRESH:
                                q = clamp_qty(-od.sell_orders[ask], pos, limit)
                                if q > 0:
                                    orders.append(Order(sym, ask, q))
                                    pos += q
                    elif residual > ENTRY_THRESH:
                        for bid in sorted(od.buy_orders, reverse=True):
                            if bid > adj_fair + EXIT_THRESH:
                                q = clamp_qty(-od.buy_orders[bid], pos, limit)
                                if q < 0:
                                    orders.append(Order(sym, bid, q))
                                    pos += q

                # passive quotes (moneyness-adjusted size)
                psz  = max(1, limit // SIZE_FRACS.get(sym, 15))
                lean = round(imbalance)
                bpx  = int(round(adj_fair - V_MM_OFFSET + lean))
                apx  = int(round(adj_fair + V_MM_OFFSET + lean))

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
