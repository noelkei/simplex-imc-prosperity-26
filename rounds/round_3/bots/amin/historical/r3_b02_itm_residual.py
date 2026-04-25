"""
r3_b02_itm_residual
Strategy: VEX market making + VEV_4000/VEV_4500 intrinsic-residual arb.
Deep ITM vouchers have extrinsic ≈ 0; fair ≈ max(0, vex_mid - strike).
EDA: extrinsic reversion corr = -0.70 for both ITM strikes → strong mean-reversion signal.
- Buy VEV when ask < intrinsic_fair - threshold
- Sell VEV when bid > intrinsic_fair + threshold
- Passive quotes around fair value for spread capture
- VEX Kalman MM provides anchor price and delta-1 P&L
"""
from datamodel import Order, OrderDepth, TradingState
import json

LIMITS = {"VELVETFRUIT_EXTRACT": 200, "VEV_4000": 300, "VEV_4500": 300}
VEX     = "VELVETFRUIT_EXTRACT"
ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}

# Extrinsic baseline at TTE=5d (extrapolated from EDA: 8d→7d→6d)
EXTR_INIT = {"VEV_4000": 0.01, "VEV_4500": 0.01}
EXTR_ALPHA = 0.005   # very slow EMA; ITM extrinsic is near-zero and stable
TAKE_EDGE  = 10      # ticks from intrinsic fair to fire aggressive take (half typical spread)
HALF_SPREAD = {"VEV_4000": 9, "VEV_4500": 7}  # passive quote half-spread
BASE_OPT_SIZE = 30   # passive quote size
KQ = 0.1; KR_VEX = 10.0


class Trader:
    def _load(self, s):
        try: return json.loads(s) if s else {}
        except: return {}
    def _save(self, d):
        try: return json.dumps(d, separators=(",", ":"))
        except: return "{}"
    def _bb(self, od): return max(od.buy_orders)  if od.buy_orders  else None
    def _ba(self, od): return min(od.sell_orders) if od.sell_orders else None
    def _mid(self, od):
        bb, ba = self._bb(od), self._ba(od)
        return (bb + ba) / 2.0 if bb is not None and ba is not None else float(bb or ba or 0)
    def _imb(self, od):
        bb, ba = self._bb(od), self._ba(od)
        if bb is None or ba is None: return 0.0
        bv, av = od.buy_orders[bb], -od.sell_orders[ba]
        t = bv + av
        return (bv - av) / t if t > 0 else 0.0
    def _kalman(self, st, obs, R):
        f = st.get("f", obs if obs is not None else 0.0)
        v = st.get("v", 200.0)
        pv = min(v + KQ, 500.0)
        if obs is None: st["v"] = pv; return f
        k = pv / (pv + R)
        st["f"] = f + k * (obs - f); st["v"] = (1 - k) * pv
        return st["f"]

    def _trade_vex(self, state, sd):
        od = state.order_depths.get(VEX)
        if od is None: return [], None
        bb, ba = self._bb(od), self._ba(od)
        if bb is None and ba is None: return [], None
        mid  = self._mid(od)
        fair = self._kalman(sd.setdefault(VEX, {}), mid, KR_VEX)
        fv   = round(fair)
        pos  = state.position.get(VEX, 0)
        lim  = LIMITS[VEX]
        imb  = self._imb(od)
        orders, bu, su = [], 0, 0

        if ba is not None and ba <= fv - 2:
            q = min(-od.sell_orders[ba], lim - pos)
            if q > 0: orders.append(Order(VEX, ba, q)); bu += q
        if bb is not None and bb >= fv + 2:
            q = min(od.buy_orders[bb], lim + pos)
            if q > 0: orders.append(Order(VEX, bb, -q)); su += q

        b_sz = max(2, min(int(40 + 20 * imb - pos * 0.1), lim - pos - bu))
        a_sz = max(2, min(int(40 - 20 * imb + pos * 0.1), lim + pos - su))
        bid_px = fv - 1
        ask_px = fv + 1
        if bb is not None: bid_px = min(bid_px, bb + 1)
        if ba is not None: ask_px = max(ask_px, ba - 1)
        if bid_px >= ask_px: bid_px = ask_px - 1
        if b_sz > 0 and lim - pos - bu > 0: orders.append(Order(VEX, bid_px,  b_sz))
        if a_sz > 0 and lim + pos - su > 0: orders.append(Order(VEX, ask_px, -a_sz))
        return orders, fair

    def _trade_itm(self, sym, vex_fair, state, sd):
        if vex_fair is None: return []
        od = state.order_depths.get(sym)
        if od is None: return []
        bb, ba = self._bb(od), self._ba(od)
        if bb is None and ba is None: return []

        strike     = ITM_SYMS[sym]
        intrinsic  = max(0.0, vex_fair - strike)
        vev_mid    = self._mid(od)
        curr_extr  = max(0.0, vev_mid - intrinsic)

        st = sd.setdefault(sym, {"ema": EXTR_INIT[sym]})
        ema = st["ema"] = EXTR_ALPHA * curr_extr + (1 - EXTR_ALPHA) * st["ema"]
        fair   = intrinsic + ema
        half_s = HALF_SPREAD[sym]
        pos    = state.position.get(sym, 0)
        lim    = LIMITS[sym]
        orders, bu, su = [], 0, 0

        # Aggressive take: buy if ask is cheap vs intrinsic+ema
        if ba is not None and ba < fair - TAKE_EDGE:
            q = min(-od.sell_orders[ba], lim - pos)
            if q > 0: orders.append(Order(sym, ba, q)); bu += q

        # Aggressive take: sell if bid is rich vs intrinsic+ema
        if bb is not None and bb > fair + TAKE_EDGE:
            q = min(od.buy_orders[bb], lim + pos)
            if q > 0: orders.append(Order(sym, bb, -q)); su += q

        # Passive quotes
        bid_px = round(fair - half_s)
        ask_px = round(fair + half_s)
        if bb is not None: bid_px = min(bid_px, bb + 1)
        if ba is not None: ask_px = max(ask_px, ba - 1)
        if bid_px >= ask_px: bid_px = ask_px - 1

        # Residual lean: cheap → bias buy, expensive → bias sell
        dev = curr_extr - ema
        b_sz = max(2, min(BASE_OPT_SIZE + int(5 * (-dev)), lim - pos - bu))
        a_sz = max(2, min(BASE_OPT_SIZE + int(5 *   dev ), lim + pos - su))
        if b_sz > 0 and lim - pos - bu > 0: orders.append(Order(sym, bid_px,  b_sz))
        if a_sz > 0 and lim + pos - su > 0: orders.append(Order(sym, ask_px, -a_sz))
        return orders

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result = {}
        try:
            vex_orders, vex_fair = self._trade_vex(state, sd)
            result[VEX] = vex_orders
        except:
            result[VEX] = []; vex_fair = None
        for sym in ITM_SYMS:
            try:    result[sym] = self._trade_itm(sym, vex_fair, state, sd)
            except: result[sym] = []
        return result, 0, self._save(sd)
