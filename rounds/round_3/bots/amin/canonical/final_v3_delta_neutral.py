"""
final_v3_delta_neutral
Full delta-neutral portfolio manager with calibrated Bachelier model.

Every tick: compute Bachelier delta for each voucher position, sum portfolio delta,
hedge residual via VEX. Position limits respected. Option MM uses calibrated sigma.

Key improvements over r3_b07_delta_hedge:
- SIGMA_TABLE (not sigma=95) → correct delta values from tick 1
- VEX position limit = 200; accounts for hedge occupancy in passive sizing
- Aggressive hedge takes first, then passive VEX MM on residual capacity
- Wider ATM passive sizes (limit//4=75) since correct pricing means real edge
- Dynamic per-strike entry threshold: ATM tighter (4.0), OTM tighter (3.0)
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


def bachelier_delta(S, K, T, sigma):
    if T <= 0 or sigma <= 0:
        return 1.0 if S >= K else 0.0
    vt = sigma * math.sqrt(T)
    if vt < 1e-12:
        return 1.0 if S >= K else 0.0
    return norm_cdf((S - K) / vt)


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


SIGMA_TABLE = {5000: 1243, 5100: 1280, 5200: 1412, 5300: 1442, 5400: 1255, 5500: 1330}
TTE         = 5 / 365.0
V_LIMIT     = 300
VEX_LIMIT   = 200

# Per-strike entry thresholds (OTM has better signal quality)
ENTRY_BY_K  = {5000: 5.0, 5100: 5.0, 5200: 4.0, 5300: 3.5, 5400: 3.0, 5500: 3.0}
V_OFFSET    = 2
# Passive sizes: larger for OTM (more theta edge)
SIZE_BY_K   = {5000: 40, 5100: 40, 5200: 60, 5300: 75, 5400: 75, 5500: 75}
MAX_V_SPR   = 25

DELTA_HEDGE_THRESH = 5.0   # rehedge when net delta deviates by this

D1_SIZE     = 20
D1_OFFSET   = 2
D1_EDGE     = 1
D1_INV_SKEW = 1.5
IMB_LEAN    = 1


class Trader:

    def run(self, state: TradingState):
        result = {}

        vex_od  = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_mid = get_mid(vex_od) if vex_od else None

        # ---- HYDROGEL delta-1 MM ----
        if "HYDROGEL_PACK" in state.order_depths:
            od     = state.order_depths["HYDROGEL_PACK"]
            mid    = get_mid(od)
            spread = get_spread(od)
            lim    = 200
            if mid is not None and spread is not None and spread <= 10:
                pos  = state.position.get("HYDROGEL_PACK", 0)
                imb  = get_imb(od)
                fair = mid - D1_INV_SKEW * (pos / lim)
                lean = round(IMB_LEAN * imb)
                orders = []
                for ask in sorted(od.sell_orders):
                    if ask < fair - D1_EDGE:
                        q = clamp(-od.sell_orders[ask], pos, lim)
                        if q > 0: orders.append(Order("HYDROGEL_PACK", ask, q)); pos += q
                for bid in sorted(od.buy_orders, reverse=True):
                    if bid > fair + D1_EDGE:
                        q = clamp(-od.buy_orders[bid], pos, lim)
                        if q < 0: orders.append(Order("HYDROGEL_PACK", bid, q)); pos += q
                q = clamp(D1_SIZE, pos, lim)
                if q > 0: orders.append(Order("HYDROGEL_PACK", int(round(fair - D1_OFFSET + lean)), q))
                q = clamp(-D1_SIZE, pos, lim)
                if q < 0: orders.append(Order("HYDROGEL_PACK", int(round(fair + D1_OFFSET + lean)), q))
                result["HYDROGEL_PACK"] = orders

        if vex_mid is None:
            return result, 0, ""

        # ---- Compute portfolio option delta ----
        portfolio_option_delta = 0.0
        for K, sigma in SIGMA_TABLE.items():
            sym = f"VEV_{K}"
            pos = state.position.get(sym, 0)
            if pos != 0:
                d = bachelier_delta(vex_mid, K, TTE, sigma)
                portfolio_option_delta += pos * d

        vex_pos    = state.position.get("VELVETFRUIT_EXTRACT", 0)
        net_delta  = portfolio_option_delta + vex_pos
        hedge_need = -portfolio_option_delta - vex_pos  # to make net=0

        # ---- Voucher MM ----
        fairs = {}
        for K, sigma in SIGMA_TABLE.items():
            fv         = bachelier_call(vex_mid, K, TTE, sigma)
            fairs[K]   = max(fv, max(vex_mid - K, 0.0))

        # Fengler check
        ks = sorted(SIGMA_TABLE.keys())
        surface_ok = all(fairs[ks[i]] >= fairs[ks[i + 1]] - 0.5 for i in range(len(ks) - 1))

        for K in ks:
            sym = f"VEV_{K}"
            if sym not in state.order_depths: continue
            od     = state.order_depths[sym]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > MAX_V_SPR: continue

            pos      = state.position.get(sym, 0)
            fair     = fairs[K]
            sigma    = SIGMA_TABLE[K]
            delta_k  = bachelier_delta(vex_mid, K, TTE, sigma)

            inv_adj  = -1.5 * (pos / V_LIMIT)
            adj_fair = fair + inv_adj
            residual = mid - fair
            entry    = ENTRY_BY_K[K]
            size     = SIZE_BY_K[K]

            orders = []
            if surface_ok and abs(residual) > entry:
                if residual < -entry:
                    for ask in sorted(od.sell_orders):
                        if ask < adj_fair:
                            q = clamp(-od.sell_orders[ask], pos, V_LIMIT)
                            if q > 0: orders.append(Order(sym, ask, q)); pos += q
                else:
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid > adj_fair:
                            q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                            if q < 0: orders.append(Order(sym, bid, q)); pos += q

            q = clamp(size, pos, V_LIMIT)
            if q > 0: orders.append(Order(sym, int(round(adj_fair - V_OFFSET)), q))
            q = clamp(-size, pos, V_LIMIT)
            if q < 0: orders.append(Order(sym, int(round(adj_fair + V_OFFSET)), q))

            result[sym] = orders

        # ---- VEX: hedge first, then MM ----
        if vex_od is not None:
            vex_orders   = []
            vex_pos_tmp  = vex_pos
            vex_mid_val  = vex_mid
            spread_vex   = get_spread(vex_od)

            if abs(hedge_need) > DELTA_HEDGE_THRESH:
                need = int(round(hedge_need))
                if need > 0:
                    for ask in sorted(vex_od.sell_orders):
                        q = clamp(min(need, -vex_od.sell_orders[ask]), vex_pos_tmp, VEX_LIMIT)
                        if q > 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask, q))
                            vex_pos_tmp += q
                            need -= q
                            if need <= 0: break
                elif need < 0:
                    for bid in sorted(vex_od.buy_orders, reverse=True):
                        q = clamp(max(need, -vex_od.buy_orders[bid]), vex_pos_tmp, VEX_LIMIT)
                        if q < 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid, q))
                            vex_pos_tmp += q
                            need -= q
                            if need >= 0: break

            # MM on remaining capacity, centred on hedge target
            target_vex = -portfolio_option_delta
            if vex_mid_val is not None and (spread_vex is None or spread_vex <= 10):
                inv_adj  = -D1_INV_SKEW * ((vex_pos_tmp - target_vex) / VEX_LIMIT)
                fair_vex = vex_mid_val + inv_adj
                imb      = get_imb(vex_od)
                lean     = round(IMB_LEAN * imb)

                for ask in sorted(vex_od.sell_orders):
                    if ask < fair_vex - D1_EDGE:
                        q = clamp(-vex_od.sell_orders[ask], vex_pos_tmp, VEX_LIMIT)
                        if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask, q)); vex_pos_tmp += q
                for bid in sorted(vex_od.buy_orders, reverse=True):
                    if bid > fair_vex + D1_EDGE:
                        q = clamp(-vex_od.buy_orders[bid], vex_pos_tmp, VEX_LIMIT)
                        if q < 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid, q)); vex_pos_tmp += q

                q = clamp(D1_SIZE, vex_pos_tmp, VEX_LIMIT)
                if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex - D1_OFFSET + lean)), q))
                q = clamp(-D1_SIZE, vex_pos_tmp, VEX_LIMIT)
                if q < 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex + D1_OFFSET + lean)), q))

            result["VELVETFRUIT_EXTRACT"] = vex_orders

        return result, 0, ""
