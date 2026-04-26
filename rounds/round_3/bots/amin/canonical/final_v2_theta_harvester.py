"""
final_v2_theta_harvester
Jane Street short-vol thesis: IV/RV ≫ 1 → sell OTM options, collect theta between rounds.

IV (Bachelier sigma ≈ 1300-1440) implies per-tick VEX vol ≈ 2.4 ticks.
Realized VEX tick-to-tick std ≈ 0.5 ticks (from EDA std_mid / sqrt(1000)).
IV/RV ≈ 5×. Every OTM option is priced ~5× too high relative to realized moves.

Strategy:
- Aggressively SHORT VEV_5300/5400/5500: take all bids above MIN_SELL_PRICE
- Portfolio delta = short options × bachelier_delta(each) → mostly negative
- Buy VEX to delta-hedge: target net_portfolio_delta ≈ 0
- HYDROGEL: standard delta-1 MM
- VEX: delta-1 MM around the hedge target

Theta between R3→R4 per 300 short:
  VEV_5300: ~6.7/unit × 300 = 2,015
  VEV_5400: ~3.9/unit × 300 = 1,160
  VEV_5500: ~1.4/unit × 300 = 428
  → 3,600/round × 4 more rounds = 14,400 cumulative theta
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

# Theta harvest targets: aggressively short these OTM strikes
# Sell at any bid ≥ intrinsic + MIN_EXTRINSIC (ensures we're selling actual extrinsic value)
THETA_TARGETS  = {5300, 5400, 5500}
MIN_EXTRINSIC  = 1.0     # minimum extrinsic value to bother selling
SELL_DISCOUNT  = 1.0     # accept up to 1 tick below fair to fill faster
# ATM/NTM: trade both ways around fair
ATM_TARGETS    = {5000, 5100, 5200}
ENTRY_ATM      = 4.0

# Delta hedge parameters
DELTA_THRESHOLD = 10.0   # rebalance when net_delta deviates this much
VEX_LIMIT       = 200

# Delta-1 MM
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
        hp_lim = 200
        if "HYDROGEL_PACK" in state.order_depths:
            od     = state.order_depths["HYDROGEL_PACK"]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is not None and spread is not None and spread <= 10:
                pos  = state.position.get("HYDROGEL_PACK", 0)
                imb  = get_imb(od)
                fair = mid - D1_INV_SKEW * (pos / hp_lim)
                lean = round(IMB_LEAN * imb)
                orders = []
                for ask in sorted(od.sell_orders):
                    if ask < fair - D1_EDGE:
                        q = clamp(-od.sell_orders[ask], pos, hp_lim)
                        if q > 0: orders.append(Order("HYDROGEL_PACK", ask, q)); pos += q
                for bid in sorted(od.buy_orders, reverse=True):
                    if bid > fair + D1_EDGE:
                        q = clamp(-od.buy_orders[bid], pos, hp_lim)
                        if q < 0: orders.append(Order("HYDROGEL_PACK", bid, q)); pos += q
                q = clamp(D1_SIZE, pos, hp_lim)
                if q > 0: orders.append(Order("HYDROGEL_PACK", int(round(fair - D1_OFFSET + lean)), q))
                q = clamp(-D1_SIZE, pos, hp_lim)
                if q < 0: orders.append(Order("HYDROGEL_PACK", int(round(fair + D1_OFFSET + lean)), q))
                result["HYDROGEL_PACK"] = orders

        if vex_mid is None:
            return result, 0, ""

        # ---- Build option portfolio: compute current portfolio delta ----
        portfolio_option_delta = 0.0
        for K, sigma in SIGMA_TABLE.items():
            sym = f"VEV_{K}"
            pos = state.position.get(sym, 0)
            if pos != 0:
                d = bachelier_delta(vex_mid, K, TTE, sigma)
                portfolio_option_delta += pos * d

        vex_pos        = state.position.get("VELVETFRUIT_EXTRACT", 0)
        net_delta      = portfolio_option_delta + vex_pos
        target_vex_pos = -portfolio_option_delta  # delta-neutral target

        # ---- Theta harvest: aggressively short OTM vouchers ----
        for K in sorted(SIGMA_TABLE.keys()):
            sym = f"VEV_{K}"
            if sym not in state.order_depths: continue
            od     = state.order_depths[sym]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > 30: continue

            pos    = state.position.get(sym, 0)
            sigma  = SIGMA_TABLE[K]
            fair   = bachelier_call(vex_mid, K, TTE, sigma)
            fair   = max(fair, max(vex_mid - K, 0.0))
            intrinsic = max(vex_mid - K, 0.0)
            orders = []

            if K in THETA_TARGETS:
                # Aggressive short: take every bid that has meaningful extrinsic
                # We sell even slightly below fair (SELL_DISCOUNT tolerance)
                for bid in sorted(od.buy_orders, reverse=True):
                    extrinsic_at_bid = bid - intrinsic
                    if extrinsic_at_bid >= MIN_EXTRINSIC and bid >= fair - SELL_DISCOUNT:
                        q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                        if q < 0:
                            orders.append(Order(sym, bid, q))
                            pos += q

                # Always post passive ask at fair or 1 tick above to ensure we fill
                apx = max(int(round(fair)), int(math.ceil(intrinsic + MIN_EXTRINSIC)))
                q   = clamp(-V_LIMIT // 5, pos, V_LIMIT)
                if q < 0 and apx > 0:
                    orders.append(Order(sym, apx, q))

                # Passive bid at fair - 3 (we'll happily buy back if needed)
                bpx = int(round(fair - 3))
                q   = clamp(V_LIMIT // 10, pos, V_LIMIT)
                if q > 0 and bpx > 0:
                    orders.append(Order(sym, bpx, q))

            else:
                # ATM/NTM: standard two-sided MM around fair
                inv_adj  = -1.5 * (pos / V_LIMIT)
                adj_fair = fair + inv_adj
                residual = mid - fair

                if abs(residual) > ENTRY_ATM:
                    if residual < -ENTRY_ATM:
                        for ask in sorted(od.sell_orders):
                            if ask < adj_fair:
                                q = clamp(-od.sell_orders[ask], pos, V_LIMIT)
                                if q > 0: orders.append(Order(sym, ask, q)); pos += q
                    else:
                        for bid in sorted(od.buy_orders, reverse=True):
                            if bid > adj_fair:
                                q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                                if q < 0: orders.append(Order(sym, bid, q)); pos += q

                psz = V_LIMIT // 5
                q = clamp(psz, pos, V_LIMIT)
                if q > 0: orders.append(Order(sym, int(round(adj_fair - 2)), q))
                q = clamp(-psz, pos, V_LIMIT)
                if q < 0: orders.append(Order(sym, int(round(adj_fair + 2)), q))

            result[sym] = orders

        # ---- VEX: delta hedge first, MM around hedge target ----
        if vex_od is not None:
            spread = get_spread(vex_od)
            vex_orders = []
            vex_pos_tmp = vex_pos

            # Recompute after above orders (approximate: use current positions only)
            hedge_error = target_vex_pos - vex_pos

            if abs(hedge_error) > DELTA_THRESHOLD:
                # Take aggressively on VEX to rebalance
                if hedge_error > 0:
                    for ask in sorted(vex_od.sell_orders):
                        need = int(round(hedge_error))
                        q    = clamp(need, vex_pos_tmp, VEX_LIMIT)
                        if q > 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask, q))
                            vex_pos_tmp += q
                            if vex_pos_tmp >= target_vex_pos - 2:
                                break
                else:
                    for bid in sorted(vex_od.buy_orders, reverse=True):
                        need = int(round(hedge_error))
                        q    = clamp(need, vex_pos_tmp, VEX_LIMIT)
                        if q < 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid, q))
                            vex_pos_tmp += q
                            if vex_pos_tmp <= target_vex_pos + 2:
                                break

            # Standard MM around mid + inventory skew (centred on hedge target)
            vex_mid_v = get_mid(vex_od)
            if vex_mid_v is not None and (spread is None or spread <= 10):
                inv_adj  = -D1_INV_SKEW * ((vex_pos_tmp - target_vex_pos) / VEX_LIMIT)
                fair_vex = vex_mid_v + inv_adj
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
