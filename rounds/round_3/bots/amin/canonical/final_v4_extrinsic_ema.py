"""
final_v4_extrinsic_ema
Extrinsic-reversion signal MM (EDA: MI=0.3358, reversion_corr=-0.70 for VEV_4000/4500).

Extrinsic value = market_mid - max(vex_mid - K, 0).
Slow EMA (α=0.02) tracks the mean extrinsic level per strike.
When extrinsic > ema + z_score × std → SELL (overpriced extrinsic, will revert).
When extrinsic < ema - z_score × std → BUY (underpriced extrinsic, will revert).

Additionally uses calibrated Bachelier fair value as a second signal:
- Only trade in the extrinsic-signal direction when it agrees with the BS residual.

Delta-1 MM: HYDROGEL + VEX, Optiver-v3 style.
Also includes ITM vouchers (VEV_4000/4500) where the reversion corr is strongest.
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


# Full sigma table including ITM (4000/4500) for extrinsic signal
SIGMA_TABLE = {
    4000: 3054, 4500: 1906,
    5000: 1243, 5100: 1280, 5200: 1412, 5300: 1442, 5400: 1255, 5500: 1330
}
TTE       = 5 / 365.0
V_LIMIT   = 300
VEX_LIMIT = 200

# EMA parameters for extrinsic tracking
EXT_ALPHA = 0.02    # slow EMA to track extrinsic mean
STD_ALPHA = 0.02    # EMA for extrinsic std
Z_ENTRY   = 1.2     # z-score to enter trade
Z_EXIT    = 0.3     # z-score to exit

# Default extrinsic std by strike (from EDA: extrinsic_std ≈ 5-7 for OTM)
DEFAULT_STD = {4000: 2.0, 4500: 5.0, 5000: 8.0, 5100: 7.5, 5200: 6.5, 5300: 6.2, 5400: 5.5, 5500: 4.5}
BS_ENTRY  = 4.0     # also require BS residual agreement beyond this

V_SIZE    = 50
V_OFFSET  = 2

D1_SIZE     = 20
D1_OFFSET   = 2
D1_EDGE     = 1
D1_INV_SKEW = 1.5
IMB_LEAN    = 1


class Trader:

    def run(self, state: TradingState):
        data = {}
        if state.traderData:
            try: data = json.loads(state.traderData)
            except: pass

        result   = {}
        ext_emas = data.get("ext_emas", {})
        ext_stds = data.get("ext_stds", {})

        vex_od  = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_mid = get_mid(vex_od) if vex_od else None

        # ---- HYDROGEL MM ----
        if "HYDROGEL_PACK" in state.order_depths:
            od = state.order_depths["HYDROGEL_PACK"]
            mid = get_mid(od); spread = get_spread(od); lim = 200
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

        # ---- VEX MM ----
        if vex_od is not None and vex_mid is not None:
            spread_vex = get_spread(vex_od)
            if spread_vex is not None and spread_vex <= 10:
                pos  = state.position.get("VELVETFRUIT_EXTRACT", 0)
                imb  = get_imb(vex_od)
                fair = vex_mid - D1_INV_SKEW * (pos / VEX_LIMIT)
                lean = round(IMB_LEAN * imb)
                orders = []
                for ask in sorted(vex_od.sell_orders):
                    if ask < fair - D1_EDGE:
                        q = clamp(-vex_od.sell_orders[ask], pos, VEX_LIMIT)
                        if q > 0: orders.append(Order("VELVETFRUIT_EXTRACT", ask, q)); pos += q
                for bid in sorted(vex_od.buy_orders, reverse=True):
                    if bid > fair + D1_EDGE:
                        q = clamp(-vex_od.buy_orders[bid], pos, VEX_LIMIT)
                        if q < 0: orders.append(Order("VELVETFRUIT_EXTRACT", bid, q)); pos += q
                q = clamp(D1_SIZE, pos, VEX_LIMIT)
                if q > 0: orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair - D1_OFFSET + lean)), q))
                q = clamp(-D1_SIZE, pos, VEX_LIMIT)
                if q < 0: orders.append(Order("VELVETFRUIT_EXTRACT", int(round(fair + D1_OFFSET + lean)), q))
                result["VELVETFRUIT_EXTRACT"] = orders

        if vex_mid is None:
            data["ext_emas"] = ext_emas
            data["ext_stds"] = ext_stds
            return result, 0, json.dumps(data)

        # ---- Extrinsic EMA signal + BS signal for each voucher ----
        for K, sigma in SIGMA_TABLE.items():
            sym = f"VEV_{K}"
            if sym not in state.order_depths: continue
            od     = state.order_depths[sym]
            mid    = get_mid(od)
            spread = get_spread(od)
            if mid is None or spread is None or spread > 30: continue

            intrinsic  = max(vex_mid - K, 0.0)
            extrinsic  = mid - intrinsic

            # Update EMA and EMA-std of extrinsic
            sk       = str(K)
            ema_ext  = ext_emas.get(sk, extrinsic)
            std_ext  = ext_stds.get(sk, DEFAULT_STD[K])
            new_ema  = EXT_ALPHA * extrinsic + (1 - EXT_ALPHA) * ema_ext
            new_std  = math.sqrt(STD_ALPHA * (extrinsic - ema_ext) ** 2 + (1 - STD_ALPHA) * std_ext ** 2)
            new_std  = max(new_std, 1.0)
            ext_emas[sk] = new_ema
            ext_stds[sk] = new_std

            z_score  = (extrinsic - ema_ext) / new_std if new_std > 0 else 0.0

            # BS signal
            bs_fair   = bachelier_call(vex_mid, K, TTE, sigma)
            bs_fair   = max(bs_fair, intrinsic)
            bs_resid  = mid - bs_fair

            pos       = state.position.get(sym, 0)
            inv_adj   = -1.5 * (pos / V_LIMIT)
            adj_fair  = bs_fair + inv_adj

            orders = []

            # Extrinsic signal: high z → sell (overpriced extrinsic)
            if z_score > Z_ENTRY and bs_resid > BS_ENTRY * 0.5:
                for bid in sorted(od.buy_orders, reverse=True):
                    if bid > adj_fair:
                        q = clamp(-od.buy_orders[bid], pos, V_LIMIT)
                        if q < 0: orders.append(Order(sym, bid, q)); pos += q

            # Extrinsic signal: low z → buy (underpriced extrinsic)
            elif z_score < -Z_ENTRY and bs_resid < -BS_ENTRY * 0.5:
                for ask in sorted(od.sell_orders):
                    if ask < adj_fair:
                        q = clamp(-od.sell_orders[ask], pos, V_LIMIT)
                        if q > 0: orders.append(Order(sym, ask, q)); pos += q

            # Soft exit when signal fades
            elif abs(z_score) < Z_EXIT and abs(pos) > 0:
                if pos > 0:
                    bb = max(od.buy_orders)
                    q  = clamp(-min(pos, V_SIZE // 2), pos, V_LIMIT)
                    if q < 0: orders.append(Order(sym, bb, q)); pos += q
                elif pos < 0:
                    ba = min(od.sell_orders)
                    q  = clamp(min(-pos, V_SIZE // 2), pos, V_LIMIT)
                    if q > 0: orders.append(Order(sym, ba, q)); pos += q

            # Passive two-sided quoting around BS fair
            bpx = int(round(adj_fair - V_OFFSET))
            apx = int(round(adj_fair + V_OFFSET))
            q = clamp(V_SIZE, pos, V_LIMIT)
            if q > 0 and bpx > 0: orders.append(Order(sym, bpx, q))
            q = clamp(-V_SIZE, pos, V_LIMIT)
            if q < 0 and apx > 0: orders.append(Order(sym, apx, q))

            result[sym] = orders

        data["ext_emas"] = ext_emas
        data["ext_stds"] = ext_stds
        return result, 0, json.dumps(data)
