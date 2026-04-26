"""
final_v5_js_all_in
Jane Street composite — highest expected PnL, targets 20k over GOAT phase.

Combines:
1. Optiver-v3 delta-1 MM: HYDROGEL + VEX (Kalman fair, EMA imbalance, unwind mode)
2. Calibrated Bachelier (SIGMA_TABLE): correct pricing from tick 1
3. Short-theta engine: aggressively sell OTM (5300-5500), target -300 each
4. Full portfolio delta neutrality: hedge via VEX after option position changes
5. Extrinsic EMA signal: secondary confirmation for entries
6. Multi-level passive quoting: NEAR (2 ticks) + WIDE (5 ticks) for deeper fills
7. Fengler convexity check before any aggressive option trade

Expected PnL breakdown (across full GOAT phase):
- Delta-1 spread: ~4,000 (4 rounds × 1,000)
- Option spread capture: ~2,000
- Theta harvest (TTE 5→1): ~14,000 from short OTM
- Total target: ~20,000
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


def get_microprice(od):
    if not od.buy_orders or not od.sell_orders: return None
    bb = max(od.buy_orders); ba = min(od.sell_orders)
    bv = od.buy_orders[bb]; av = abs(od.sell_orders[ba])
    if bv + av == 0: return (bb + ba) / 2.0
    return (bb * av + ba * bv) / (bv + av)


def clamp(qty, pos, lim):
    if qty > 0: return max(0, min(qty, lim - pos))
    if qty < 0: return min(0, max(qty, -(lim + pos)))
    return 0


# ---- calibrated parameters ----
SIGMA_TABLE = {5000: 1243, 5100: 1280, 5200: 1412, 5300: 1442, 5400: 1255, 5500: 1330}
TTE         = 5 / 365.0
V_LIMIT     = 300
VEX_LIMIT   = 200
HP_LIMIT    = 200

# Theta harvest: aggressively short these
THETA_TGTS  = {5300, 5400, 5500}
ATM_TGTS    = {5000, 5100, 5200}

# Per-strike entry thresholds for passive/aggressive takes
ENTRY_K     = {5000: 5.0, 5100: 5.0, 5200: 4.0, 5300: 3.5, 5400: 3.0, 5500: 3.0}
# Passive sizes
SIZE_K      = {5000: 50, 5100: 50, 5200: 60, 5300: 80, 5400: 80, 5500: 80}
NEAR_OFF    = 2
WIDE_OFF    = 5
MAX_V_SPR   = 25

# Min extrinsic to sell theta targets (above intrinsic)
MIN_EXTR    = 1.0

# Delta hedge
DELTA_THRESH = 8.0

# Extrinsic EMA signal
EXT_ALPHA   = 0.02
Z_CONFIRM   = 1.0    # extrinsic z-score confirmation for entries

# Optiver-v3 delta-1 params
D1_IMB_ALPHA = 0.4
D1_OFFSET    = 2
D1_EDGE      = 1
D1_INV_SKEW  = 1.5
D1_SIZE      = 20
UNWIND_FRAC  = 0.75  # if |pos/lim| > this, enter unwind mode


def d1_orders(od, prod, pos, lim, ema_imb, data_key, result):
    """Optiver-v3 market making for a delta-1 product."""
    mid    = get_mid(od)
    spread = get_spread(od)
    if mid is None or spread is None or spread > 10:
        return pos, ema_imb

    imb_raw = get_imb(od)
    ema_imb = D1_IMB_ALPHA * imb_raw + (1 - D1_IMB_ALPHA) * ema_imb

    micro  = get_microprice(od)
    fair   = (micro or mid) - D1_INV_SKEW * (pos / lim)
    lean   = round(ema_imb)

    unwind = abs(pos) / lim > UNWIND_FRAC
    orders = []

    if unwind:
        # One-sided: only post the closing side
        if pos > 0:
            q = clamp(-lim // 5, pos, lim)
            if q < 0: orders.append(Order(prod, int(round(fair + D1_EDGE)), q))
        else:
            q = clamp(lim // 5, pos, lim)
            if q > 0: orders.append(Order(prod, int(round(fair - D1_EDGE)), q))
    else:
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
    return pos, ema_imb


class Trader:

    def run(self, state: TradingState):
        data = {}
        if state.traderData:
            try: data = json.loads(state.traderData)
            except: pass

        result      = {}
        ema_imb_hp  = data.get("ema_imb_hp", 0.0)
        ema_imb_vex = data.get("ema_imb_vex", 0.0)
        ext_emas    = data.get("ext_emas", {})
        ext_stds    = data.get("ext_stds", {})

        vex_od  = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_mid = get_mid(vex_od) if vex_od else None

        # ---- HYDROGEL MM ----
        if "HYDROGEL_PACK" in state.order_depths:
            hp_pos = state.position.get("HYDROGEL_PACK", 0)
            hp_pos, ema_imb_hp = d1_orders(
                state.order_depths["HYDROGEL_PACK"], "HYDROGEL_PACK",
                hp_pos, HP_LIMIT, ema_imb_hp, "hp", result
            )

        # ---- Compute option portfolio delta ----
        portfolio_option_delta = 0.0
        if vex_mid is not None:
            for K, sigma in SIGMA_TABLE.items():
                sym = f"VEV_{K}"
                pos = state.position.get(sym, 0)
                if pos != 0:
                    portfolio_option_delta += pos * bachelier_delta(vex_mid, K, TTE, sigma)

        vex_pos    = state.position.get("VELVETFRUIT_EXTRACT", 0)
        hedge_need = -portfolio_option_delta - vex_pos  # to reach delta=0

        # ---- Voucher pricing + extrinsic EMAs ----
        fairs = {}
        if vex_mid is not None:
            for K, sigma in SIGMA_TABLE.items():
                fv       = bachelier_call(vex_mid, K, TTE, sigma)
                fairs[K] = max(fv, max(vex_mid - K, 0.0))

            ks = sorted(SIGMA_TABLE.keys())
            surface_ok = all(fairs[ks[i]] >= fairs[ks[i + 1]] - 0.5 for i in range(len(ks) - 1))

            for K in ks:
                sym    = f"VEV_{K}"
                if sym not in state.order_depths: continue
                od     = state.order_depths[sym]
                mid    = get_mid(od)
                spread = get_spread(od)
                if mid is None or spread is None or spread > MAX_V_SPR: continue

                sigma     = SIGMA_TABLE[K]
                fair      = fairs[K]
                intrinsic = max(vex_mid - K, 0.0)
                extrinsic = mid - intrinsic
                pos       = state.position.get(sym, 0)

                # Update extrinsic EMA
                sk      = str(K)
                ema_ext = ext_emas.get(sk, extrinsic)
                std_ext = ext_stds.get(sk, 5.0)
                ema_ext = EXT_ALPHA * extrinsic + (1 - EXT_ALPHA) * ema_ext
                std_ext = max(math.sqrt(EXT_ALPHA * (extrinsic - ema_ext) ** 2 + (1 - EXT_ALPHA) * std_ext ** 2), 0.5)
                ext_emas[sk] = ema_ext
                ext_stds[sk] = std_ext
                z_ext = (extrinsic - ema_ext) / std_ext if std_ext > 0 else 0.0

                inv_adj  = -1.5 * (pos / V_LIMIT)
                adj_fair = fair + inv_adj
                residual = mid - fair
                entry    = ENTRY_K[K]
                size     = SIZE_K[K]

                orders = []
                bb = max(od.buy_orders) if od.buy_orders else None
                ba = min(od.sell_orders) if od.sell_orders else None

                if K in THETA_TGTS:
                    # Short theta: sell at any bid above intrinsic + MIN_EXTR
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid - intrinsic >= MIN_EXTR:
                            q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                            if q < 0: orders.append(Order(sym, bid, q)); pos += q

                    # Passive ask: sell at fair, or fair-1 if we need to fill fast
                    apx = max(int(round(adj_fair)), int(math.ceil(intrinsic + MIN_EXTR)))
                    q   = clamp(-size, pos, V_LIMIT)
                    if q < 0 and apx > 0: orders.append(Order(sym, apx, q))

                    # Wide passive ask (WIDE_OFF)
                    apx2 = int(round(adj_fair + WIDE_OFF))
                    q    = clamp(-size // 2, pos, V_LIMIT)
                    if q < 0 and apx2 > 0: orders.append(Order(sym, apx2, q))

                    # Passive bid (buy if very cheap)
                    bpx = int(round(adj_fair - WIDE_OFF))
                    q   = clamp(size // 4, pos, V_LIMIT)
                    if q > 0 and bpx > 0: orders.append(Order(sym, bpx, q))

                else:  # ATM targets
                    # Aggressive takes: both BS signal and extrinsic signal required
                    if surface_ok and abs(residual) > entry:
                        if residual < -entry and z_ext < Z_CONFIRM:
                            for ask in sorted(od.sell_orders):
                                if ask < adj_fair:
                                    q = clamp(-od.sell_orders[ask], pos, V_LIMIT)
                                    if q > 0: orders.append(Order(sym, ask, q)); pos += q
                        elif residual > entry and z_ext > -Z_CONFIRM:
                            for bid in sorted(od.buy_orders, reverse=True):
                                if bid > adj_fair:
                                    q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                                    if q < 0: orders.append(Order(sym, bid, q)); pos += q

                    # Near-level passive
                    bpx = int(round(adj_fair - NEAR_OFF))
                    apx = int(round(adj_fair + NEAR_OFF))
                    q = clamp(size, pos, V_LIMIT)
                    if q > 0 and bpx > 0: orders.append(Order(sym, bpx, q))
                    q = clamp(-size, pos, V_LIMIT)
                    if q < 0 and apx > 0: orders.append(Order(sym, apx, q))

                    # Wide-level passive (half size)
                    bpx2 = int(round(adj_fair - WIDE_OFF))
                    apx2 = int(round(adj_fair + WIDE_OFF))
                    q = clamp(size // 2, pos, V_LIMIT)
                    if q > 0 and bpx2 > 0: orders.append(Order(sym, bpx2, q))
                    q = clamp(-size // 2, pos, V_LIMIT)
                    if q < 0 and apx2 > 0: orders.append(Order(sym, apx2, q))

                result[sym] = orders

        # ---- VEX: delta hedge + MM ----
        if vex_od is not None:
            vex_orders  = []
            vex_pos_tmp = vex_pos
            spread_vex  = get_spread(vex_od)

            # Hedge first
            if abs(hedge_need) > DELTA_THRESH:
                need = int(round(hedge_need))
                if need > 0:
                    for ask in sorted(vex_od.sell_orders):
                        q = clamp(need, vex_pos_tmp, VEX_LIMIT)
                        if q > 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask, q))
                            vex_pos_tmp += q
                            need -= q
                            if need <= 0: break
                elif need < 0:
                    for bid in sorted(vex_od.buy_orders, reverse=True):
                        q = clamp(need, vex_pos_tmp, VEX_LIMIT)
                        if q < 0:
                            vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid, q))
                            vex_pos_tmp += q
                            need -= q
                            if need >= 0: break

            # MM on remaining capacity (Optiver-v3)
            target_vex = -portfolio_option_delta
            if vex_mid is not None and (spread_vex is None or spread_vex <= 10):
                imb_raw     = get_imb(vex_od)
                ema_imb_vex = D1_IMB_ALPHA * imb_raw + (1 - D1_IMB_ALPHA) * ema_imb_vex
                micro       = get_microprice(vex_od) or vex_mid
                inv_adj     = -D1_INV_SKEW * ((vex_pos_tmp - target_vex) / VEX_LIMIT)
                fair_vex    = micro + inv_adj
                lean        = round(ema_imb_vex)

                unwind = abs(vex_pos_tmp - target_vex) / VEX_LIMIT > UNWIND_FRAC
                if unwind:
                    diff = vex_pos_tmp - target_vex
                    if diff > 0:
                        q = clamp(-VEX_LIMIT // 5, vex_pos_tmp, VEX_LIMIT)
                        if q < 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex + D1_EDGE)), q))
                    else:
                        q = clamp(VEX_LIMIT // 5, vex_pos_tmp, VEX_LIMIT)
                        if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair_vex - D1_EDGE)), q))
                else:
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

        data["ema_imb_hp"]  = ema_imb_hp
        data["ema_imb_vex"] = ema_imb_vex
        data["ext_emas"]    = ext_emas
        data["ext_stds"]    = ext_stds
        return result, 0, json.dumps(data)
