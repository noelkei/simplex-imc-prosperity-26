"""
r3_b02_itm_anchor
Strategy: C05 — deep-ITM voucher anchor (VEV_4000 + VEV_4500) + C01+C02 delta-1 MM.

EDA evidence: VEV_4000/4500 extrinsic reversion corr = -0.70 (strongest signal in dataset).
At TTE=5d with VEX≈5250, these strikes are 750-1250 pts in-the-money. Bachelier time
value is tiny (<0.5), so price ≈ intrinsic value = max(S-K, 0). Any deviation from this
floor is a mean-reversion trade.

Key differentiators vs Amin's bots:
- Trades VEV_4000 and VEV_4500 (Amin's bots skip these entirely)
- Entry threshold = 2.0 (tighter — ITM signal is cleaner)
- Intrinsic hard floor: never buy above max(S-K,0) + threshold
- Spread tolerance = 30 (wider, ITM spread is larger)
- Larger passive size (limit//8) to capture the higher-probability reversion
"""
import json
import math
from datamodel import Order, TradingState


# ---- helpers ----

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
TTE_YEARS     = 5 / 365.0

DELTA1 = {
    "HYDROGEL_PACK":       200,
    "VELVETFRUIT_EXTRACT": 200,
}
MM_OFFSET      = 2
MM_EDGE        = 1
MAX_D1_SPREAD  = 8
INV_SKEW       = 1.5
IMBALANCE_LEAN = 1

ITM_VOUCHERS = {
    "VEV_4000": (4000, 300),
    "VEV_4500": (4500, 300),
}
ITM_ENTRY       = 2.0   # tight — high-corr signal
ITM_EXIT        = 0.5
ITM_MM_OFFSET   = 3     # wider passive offset for large spread
MAX_ITM_SPREAD  = 30    # ITM spreads can be wider
ITM_INV_SKEW    = 2.0   # strong skew to flatten ITM exposure
SIGMA_ALPHA     = 0.05  # slow EMA — ITM fair is stable


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

        # ---- get VEX mid ----
        vex_mid = None
        if "VELVETFRUIT_EXTRACT" in state.order_depths:
            vex_mid = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"])

        # ---- update sigma_abs from VEX moves ----
        prev_vex = data.get("prev_vex")
        if vex_mid is not None and prev_vex is not None:
            move       = abs(vex_mid - prev_vex)
            daily_vol  = move * math.sqrt(1000)
            sigma_abs  = SIGMA_ALPHA * daily_vol + (1.0 - SIGMA_ALPHA) * sigma_abs

        # ---- delta-1 market making ----
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
            bb     = max(od.buy_orders)
            ba     = min(od.sell_orders)

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

            psz     = max(1, limit // 10)
            buy_px  = round(fair - MM_OFFSET + lean)
            sell_px = round(fair + MM_OFFSET + lean)

            q = clamp_qty(psz, pos, limit)
            if q > 0:
                orders.append(Order(product, int(buy_px), q))
            q = clamp_qty(-psz, pos, limit)
            if q < 0:
                orders.append(Order(product, int(sell_px), q))

            result[product] = orders

        # ---- ITM voucher reversion (VEV_4000 + VEV_4500) ----
        if vex_mid is not None:
            for symbol, (strike, limit) in ITM_VOUCHERS.items():
                if symbol not in state.order_depths:
                    continue
                od     = state.order_depths[symbol]
                mid    = get_mid(od)
                spread = get_spread(od)
                if mid is None or spread is None or spread > MAX_ITM_SPREAD:
                    continue

                pos = state.position.get(symbol, 0)

                # Bachelier fair with intrinsic hard floor
                fair_bachelier = bachelier_call(vex_mid, strike, TTE_YEARS, sigma_abs)
                intrinsic      = max(vex_mid - strike, 0.0)
                fair           = max(fair_bachelier, intrinsic)

                residual = mid - fair
                inv_adj  = -ITM_INV_SKEW * (pos / limit)
                adj_fair = fair + inv_adj

                orders = []
                bb     = max(od.buy_orders)
                ba     = min(od.sell_orders)

                # Aggressive reversion trades
                if residual < -ITM_ENTRY:
                    # underpriced — buy
                    for ask in sorted(od.sell_orders):
                        if ask < adj_fair - ITM_EXIT:
                            q = clamp_qty(-od.sell_orders[ask], pos, limit)
                            if q > 0:
                                orders.append(Order(symbol, ask, q))
                                pos += q
                elif residual > ITM_ENTRY:
                    # overpriced — sell
                    for bid in sorted(od.buy_orders, reverse=True):
                        if bid > adj_fair + ITM_EXIT:
                            q = clamp_qty(-od.buy_orders[bid], pos, limit)
                            if q < 0:
                                orders.append(Order(symbol, bid, q))
                                pos += q

                # Passive quotes (large size — high confidence)
                psz     = max(1, limit // 8)
                buy_px  = int(round(adj_fair - ITM_MM_OFFSET))
                sell_px = int(round(adj_fair + ITM_MM_OFFSET))

                q = clamp_qty(psz, pos, limit)
                if q > 0 and buy_px > 0:
                    orders.append(Order(symbol, buy_px, q))
                q = clamp_qty(-psz, pos, limit)
                if q < 0 and sell_px > 0:
                    orders.append(Order(symbol, sell_px, q))

                result[symbol] = orders

        # ---- persist state ----
        data["sigma_abs"] = sigma_abs
        if vex_mid is not None:
            data["prev_vex"] = vex_mid

        return result, 0, json.dumps(data)
