"""
r3_b03_voucher_pure
Strategy: Voucher-only Bachelier residual reversion for VEV_5000-5300.
No delta-1 products. Focused pure-play on the option alpha.

Key differentiators vs Amin's bots:
- No HYDROGEL_PACK or VELVETFRUIT_EXTRACT positions — pure option PnL
- Family exposure (Bergault 2022): aggregate normalized position across all 4
  voucher strikes feeds a shared nudge that shifts per-symbol fair values
- Multi-level passive quoting: 2 resting orders per side at different offsets
  (captures both the near-mid and wider spread)
- Slower sigma EMA (alpha=0.05 vs Amin's 0.10) — more stable fair value
- Imbalance lean on passive quotes (secondary modifier per Muravyev 2015)
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

SIGMA_DEFAULT  = 95.0
SIGMA_ALPHA    = 0.05   # slow EMA — more stable fair value
TTE_YEARS      = 5 / 365.0

ENTRY_THRESH   = 3.0    # minimum |residual| to enter aggressively
EXIT_THRESH    = 0.5    # residual close to fair → stop position building
MAX_SPREAD     = 20
INV_SKEW       = 1.5    # per-symbol inventory skew factor

# Bergault family exposure nudge
FAMILY_NUDGE   = 0.8    # how much aggregate family exposure shifts each fair

# Multi-level passive quoting
NEAR_OFFSET    = 2      # inner resting quote (tighter)
WIDE_OFFSET    = 5      # outer resting quote (captures bigger residuals)
NEAR_SIZE_FRAC = 10     # limit // NEAR_SIZE_FRAC per level
WIDE_SIZE_FRAC = 20

# Imbalance lean on passive quotes
IMB_LEAN       = 1      # ticks of lean from imbalance

VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}


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

        # ---- VEX mid (required for Bachelier fair) ----
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # ---- update sigma_abs (slow EMA for stability) ----
        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move      = abs(vex_mid - prev_vex)
            daily_vol = move * math.sqrt(1000)
            sigma_abs = SIGMA_ALPHA * daily_vol + (1.0 - SIGMA_ALPHA) * sigma_abs

        if vex_mid is None:
            data["sigma_abs"] = sigma_abs
            return result, 0, json.dumps(data)

        # ---- Bachelier fairs ----
        fairs = {}
        for sym, (strike, _) in VOUCHER_PRODUCTS.items():
            fv = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
            fairs[sym] = max(fv, max(vex_mid - strike, 0.0))

        # ---- surface monotonicity guardrail ----
        syms_sorted = sorted(VOUCHER_PRODUCTS, key=lambda s: VOUCHER_PRODUCTS[s][0])
        surface_ok = True
        for i in range(len(syms_sorted) - 1):
            if fairs[syms_sorted[i]] < fairs[syms_sorted[i + 1]] - 0.5:
                surface_ok = False
                break

        # ---- Bergault family exposure: aggregate normalized position ----
        family_exp = 0.0
        n_active   = 0
        for sym, (_, lim) in VOUCHER_PRODUCTS.items():
            if sym in state.order_depths:
                pos_sym   = state.position.get(sym, 0)
                family_exp += pos_sym / lim
                n_active   += 1
        if n_active > 0:
            family_exp /= n_active
        # nudge: if family is net long, push fairs down (makes bot more eager to sell)
        family_nudge_val = -FAMILY_NUDGE * family_exp

        # ---- per-voucher quoting ----
        for sym in syms_sorted:
            if sym not in state.order_depths:
                continue
            od     = state.order_depths[sym]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > MAX_SPREAD:
                continue

            strike, limit = VOUCHER_PRODUCTS[sym]
            pos           = state.position.get(sym, 0)
            fair          = fairs[sym] + family_nudge_val

            imbalance = get_imbalance(od)
            inv_adj   = -INV_SKEW * (pos / limit)
            adj_fair  = fair + inv_adj

            residual = mid - fair
            orders   = []
            bb       = max(od.buy_orders)
            ba       = min(od.sell_orders)

            # ---- aggressive reversion trades ----
            if abs(residual) > ENTRY_THRESH and surface_ok:
                if residual < -ENTRY_THRESH:
                    # underpriced — buy aggressively
                    for ask in sorted(od.sell_orders):
                        if ask < adj_fair - EXIT_THRESH:
                            q = clamp_qty(-od.sell_orders[ask], pos, limit)
                            if q > 0:
                                orders.append(Order(sym, ask, q))
                                pos += q
                elif residual > ENTRY_THRESH:
                    # overpriced — sell aggressively
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid > adj_fair + EXIT_THRESH:
                            q = clamp_qty(-od.buy_orders[bid], pos, limit)
                            if q < 0:
                                orders.append(Order(sym, bid, q))
                                pos += q

            # ---- multi-level passive quotes ----
            lean     = round(IMB_LEAN * imbalance)

            # inner level (near-mid, smaller size)
            near_sz  = max(1, limit // NEAR_SIZE_FRAC)
            near_bid = int(round(adj_fair - NEAR_OFFSET + lean))
            near_ask = int(round(adj_fair + NEAR_OFFSET + lean))

            q = clamp_qty(near_sz, pos, limit)
            if q > 0 and near_bid > 0:
                orders.append(Order(sym, near_bid, q))
            q = clamp_qty(-near_sz, pos, limit)
            if q < 0 and near_ask > 0:
                orders.append(Order(sym, near_ask, q))

            # outer level (wider, smaller size — captures larger residuals)
            wide_sz  = max(1, limit // WIDE_SIZE_FRAC)
            wide_bid = int(round(adj_fair - WIDE_OFFSET + lean))
            wide_ask = int(round(adj_fair + WIDE_OFFSET + lean))

            q = clamp_qty(wide_sz, pos, limit)
            if q > 0 and wide_bid > 0:
                orders.append(Order(sym, wide_bid, q))
            q = clamp_qty(-wide_sz, pos, limit)
            if q < 0 and wide_ask > 0:
                orders.append(Order(sym, wide_ask, q))

            result[sym] = orders

        # ---- persist state ----
        data["sigma_abs"] = sigma_abs
        if vex_mid is not None:
            data["prev_vex"] = vex_mid

        return result, 0, json.dumps(data)
