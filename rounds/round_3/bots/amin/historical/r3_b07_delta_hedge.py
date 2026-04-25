"""
r3_b07_delta_hedge
Strategy: Full option portfolio with Bachelier delta hedging via VEX.
Inspired by Optiver's ASML bot (asml_bot.py) — adapted to Bachelier model
and Prosperity constraints.

Bachelier delta for a call: delta = N(d), where d = (S-K) / (sigma*sqrt(T))
Portfolio delta = sum(delta_i * voucher_pos_i) + vex_pos

Hedging logic:
- After quoting all vouchers, compute portfolio delta
- If |portfolio_delta| > DELTA_HEDGE_THR:
  net_long → sell VEX aggressively (limit at best bid)
  net_short → buy VEX aggressively (limit at best ask)
- VEX position limit reserved for hedging (up to HEDGE_RESERVE units)

Credit model (ASML-inspired):
- Base credit per voucher scaled by moneyness proximity and TTE factor
- Near-ATM (|d| < 1): wider credit (more gamma risk)
- Deep ITM/OTM (|d| > 3): narrower credit (mostly intrinsic/zero)

Key differentiator vs Amin's bots:
- Explicit delta management of the whole voucher portfolio
- VEX used as delta hedge, not just as anchor for fair value
- Passive quoting sized by delta headroom (avoid building excessive delta)
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


def bachelier_delta(S: float, K: float, T: float, sig: float) -> float:
    """Bachelier call delta = N(d), where d = (S-K)/(sigma*sqrt(T))."""
    if T <= 0 or sig <= 0:
        return 1.0 if S > K else 0.0
    vt = sig * math.sqrt(T)
    if vt < 1e-12:
        return 1.0 if S > K else 0.0
    d = (S - K) / vt
    return norm_cdf(d)


def get_mid(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_spread(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return min(od.sell_orders) - max(od.buy_orders)


def clamp_qty(qty: int, pos: int, limit: int) -> int:
    if qty > 0:
        return max(0, min(qty, limit - pos))
    if qty < 0:
        return min(0, max(qty, -(limit + pos)))
    return 0


# ---- parameters ----

SIGMA_DEFAULT    = 95.0
SIGMA_ALPHA      = 0.10
TTE_YEARS        = 5 / 365.0

# HYDROGEL stays as basic MM (separate from option portfolio)
HYDROGEL_LIMIT   = 200
MM_OFFSET_D1     = 2
MM_EDGE_D1       = 1
MAX_D1_SPREAD    = 8
D1_INV_SKEW      = 1.5

# VEX: limit 200, reserve HEDGE_RESERVE units for delta hedging
VEX_LIMIT        = 200
HEDGE_RESERVE    = 100   # units reserved for delta hedging
VEX_MM_LIMIT     = VEX_LIMIT - HEDGE_RESERVE  # MM quota for VEX

DELTA_HEDGE_THR  = 15    # portfolio delta imbalance before hedging
MAX_HEDGE_TRADE  = 20    # max VEX units per hedge trade

VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}
MAX_V_SPREAD     = 20
V_INV_SKEW       = 1.5
# Portfolio-delta-based size cap: avoid accumulating too much delta
DELTA_SIZE_CAP   = 80    # max portfolio |delta| before reducing passive size

SYMS_BY_STRIKE = sorted(VOUCHER_PRODUCTS, key=lambda s: VOUCHER_PRODUCTS[s][0])


def moneyness_credit(d: float, base: float = 2.5) -> float:
    """ASML-inspired credit based on d-value.
    Near ATM (|d|<1): wider credit. Deep ITM/OTM (|d|>3): narrower.
    """
    if abs(d) < 1.0:
        return base * 1.4  # near-ATM: more gamma, wider credit
    if abs(d) < 2.0:
        return base * 1.0
    return base * 0.7


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

        # ---- HYDROGEL basic MM ----
        if "HYDROGEL_PACK" in state.order_depths:
            od     = state.order_depths["HYDROGEL_PACK"]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is not None and spread is not None and spread <= MAX_D1_SPREAD:
                pos    = state.position.get("HYDROGEL_PACK", 0)
                inv_adj = -D1_INV_SKEW * (pos / HYDROGEL_LIMIT)
                fair    = mid + inv_adj
                orders  = []
                for ask in sorted(od.sell_orders):
                    if ask < fair - MM_EDGE_D1:
                        q = clamp_qty(-od.sell_orders[ask], pos, HYDROGEL_LIMIT)
                        if q > 0:
                            orders.append(Order("HYDROGEL_PACK", ask, q))
                            pos += q
                for bid in sorted(od.buy_orders, reverse=True):
                    if bid > fair + MM_EDGE_D1:
                        q = clamp_qty(-od.buy_orders[bid], pos, HYDROGEL_LIMIT)
                        if q < 0:
                            orders.append(Order("HYDROGEL_PACK", bid, q))
                            pos += q
                psz = max(1, HYDROGEL_LIMIT // 10)
                q   = clamp_qty(psz, pos, HYDROGEL_LIMIT)
                if q > 0:
                    orders.append(Order("HYDROGEL_PACK", int(round(fair - MM_OFFSET_D1)), q))
                q = clamp_qty(-psz, pos, HYDROGEL_LIMIT)
                if q < 0:
                    orders.append(Order("HYDROGEL_PACK", int(round(fair + MM_OFFSET_D1)), q))
                result["HYDROGEL_PACK"] = orders

        if vex_mid is None:
            data["sigma_abs"] = sigma_abs
            return result, 0, json.dumps(data)

        # ---- compute Bachelier fairs and deltas ----
        fairs  = {}
        deltas = {}
        for sym, (strike, _) in VOUCHER_PRODUCTS.items():
            fv          = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
            fairs[sym]  = max(fv, max(vex_mid - strike, 0.0))
            deltas[sym] = bachelier_delta(vex_mid, strike, TTE_YEARS, sigma_abs)

        # monotonicity guardrail
        surface_ok = True
        for i in range(len(SYMS_BY_STRIKE) - 1):
            if fairs[SYMS_BY_STRIKE[i]] < fairs[SYMS_BY_STRIKE[i + 1]] - 0.5:
                surface_ok = False
                break

        # ---- compute current portfolio delta ----
        vex_pos        = state.position.get("VELVETFRUIT_EXTRACT", 0)
        portfolio_delta = float(vex_pos)  # VEX has delta=1
        for sym in VOUCHER_PRODUCTS:
            pos_sym         = state.position.get(sym, 0)
            portfolio_delta += deltas[sym] * pos_sym

        # ---- quote vouchers ----
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
            delta         = deltas[sym]

            vt  = sigma_abs * math.sqrt(TTE_YEARS)
            d_v = (vex_mid - strike) / vt if vt > 1e-12 else 0.0
            credit = moneyness_credit(d_v)

            inv_adj  = -V_INV_SKEW * (pos / limit)
            adj_fair = fair + inv_adj

            orders = []

            # Delta-headroom size: smaller when portfolio delta is large
            delta_headroom = max(0.0, DELTA_SIZE_CAP - abs(portfolio_delta))
            if abs(delta) > 0.01:
                max_vol_by_delta = int(delta_headroom / abs(delta))
            else:
                max_vol_by_delta = limit // 10
            psz = max(1, min(limit // 15, max_vol_by_delta))

            # Aggressive reversion trades (surface guardrail applies)
            if surface_ok:
                residual = mid - fair
                if residual < -credit * 1.5:
                    # significantly underpriced — buy
                    for ask in sorted(od.sell_orders):
                        if ask < adj_fair - credit * 0.5:
                            q = clamp_qty(-od.sell_orders[ask], pos, limit)
                            q = min(q, psz)
                            if q > 0:
                                orders.append(Order(sym, ask, q))
                                pos += q
                                portfolio_delta += delta * q
                elif residual > credit * 1.5:
                    # overpriced — sell
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid > adj_fair + credit * 0.5:
                            q = clamp_qty(-od.buy_orders[bid], pos, limit)
                            q = max(q, -psz)
                            if q < 0:
                                orders.append(Order(sym, bid, q))
                                pos += q
                                portfolio_delta += delta * q

            # Passive quotes
            bpx = int(round(adj_fair - credit))
            apx = int(round(adj_fair + credit))

            q = clamp_qty(psz, pos, limit)
            if q > 0 and bpx > 0:
                orders.append(Order(sym, bpx, q))
            q = clamp_qty(-psz, pos, limit)
            if q < 0 and apx > 0:
                orders.append(Order(sym, apx, q))

            result[sym] = orders

        # ---- delta hedge via VEX ----
        vex_orders = []
        vex_pos_current = state.position.get("VELVETFRUIT_EXTRACT", 0)

        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            od_vex = state.order_depths["VELVETFRUIT_EXTRACT"]
            bb_vex = max(od_vex.buy_orders)  if od_vex.buy_orders  else None
            ba_vex = min(od_vex.sell_orders) if od_vex.sell_orders else None

            vex_pos_used = vex_pos_current  # track separately

            if portfolio_delta > DELTA_HEDGE_THR:
                # Net long delta → sell VEX to hedge
                hedge_qty = min(int(portfolio_delta - DELTA_HEDGE_THR + 1), MAX_HEDGE_TRADE)
                if bb_vex is not None:
                    q = clamp_qty(-hedge_qty, vex_pos_used, VEX_LIMIT)
                    if q < 0:
                        vex_orders.append(Order("VELVETFRUIT_EXTRACT", bb_vex, q))
                        vex_pos_used += q
            elif portfolio_delta < -DELTA_HEDGE_THR:
                # Net short delta → buy VEX to hedge
                hedge_qty = min(int(-portfolio_delta - DELTA_HEDGE_THR + 1), MAX_HEDGE_TRADE)
                if ba_vex is not None:
                    q = clamp_qty(hedge_qty, vex_pos_used, VEX_LIMIT)
                    if q > 0:
                        vex_orders.append(Order("VELVETFRUIT_EXTRACT", ba_vex, q))
                        vex_pos_used += q

            # VEX passive MM within remaining capacity
            mid_vex    = get_mid(od_vex)
            spread_vex = get_spread(od_vex)
            if mid_vex is not None and spread_vex is not None and spread_vex <= MAX_D1_SPREAD:
                inv_adj_vex = -D1_INV_SKEW * (vex_pos_used / VEX_LIMIT)
                fair_vex    = mid_vex + inv_adj_vex
                psz_vex     = max(1, VEX_MM_LIMIT // 10)
                q = clamp_qty(psz_vex, vex_pos_used, VEX_LIMIT)
                if q > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex - MM_OFFSET_D1)), q))
                q = clamp_qty(-psz_vex, vex_pos_used, VEX_LIMIT)
                if q < 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex + MM_OFFSET_D1)), q))

        if vex_orders:
            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ---- persist ----
        data["sigma_abs"] = sigma_abs
        data["prev_vex"]  = vex_mid

        return result, 0, json.dumps(data)
