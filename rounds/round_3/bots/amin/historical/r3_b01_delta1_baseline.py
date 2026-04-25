"""
r3_b01_delta1_baseline
Strategy: Kalman-filtered market maker for HYDROGEL_PACK and VELVETFRUIT_EXTRACT.
No options. Establishes the pure delta-1 baseline.
- Kalman fair value (Q=0.1, R=50 hydro / R=10 vex)
- Imbalance-weighted quote sizes (IC≈0.14 both products)
- Aggressive take when best level is ≥2 ticks mispriced vs Kalman fair
"""
from datamodel import Order, OrderDepth, TradingState
import json

LIMITS = {"HYDROGEL_PACK": 200, "VELVETFRUIT_EXTRACT": 200}
KR     = {"HYDROGEL_PACK": 50.0, "VELVETFRUIT_EXTRACT": 10.0}
KQ     = 0.1
IMB_GAIN  = 25      # size units per unit imbalance
BASE_SIZE = 40


class Trader:
    def _load(self, s):
        try: return json.loads(s) if s else {}
        except: return {}

    def _save(self, d):
        try: return json.dumps(d, separators=(",", ":"))
        except: return "{}"

    def _bb(self, od): return max(od.buy_orders)  if od.buy_orders  else None
    def _ba(self, od): return min(od.sell_orders) if od.sell_orders else None

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
        if obs is None:
            st["v"] = pv; return f
        k = pv / (pv + R)
        st["f"] = f + k * (obs - f)
        st["v"] = (1.0 - k) * pv
        return st["f"]

    def _trade(self, sym, state, sd):
        od = state.order_depths.get(sym)
        if od is None: return []
        bb, ba = self._bb(od), self._ba(od)
        if bb is None and ba is None: return []

        mid = (bb + ba) / 2.0 if bb is not None and ba is not None else float(bb or ba)
        fair  = self._kalman(sd.setdefault(sym, {}), mid, KR[sym])
        fv    = round(fair)
        imb   = self._imb(od)
        pos   = state.position.get(sym, 0)
        lim   = LIMITS[sym]
        orders, buy_used, sell_used = [], 0, 0

        # Aggressive take: buy cheap asks / sell expensive bids
        if ba is not None and ba <= fv - 2:
            q = min(-od.sell_orders[ba], lim - pos)
            if q > 0:
                orders.append(Order(sym, ba, q))
                buy_used += q
        if bb is not None and bb >= fv + 2:
            q = min(od.buy_orders[bb], lim + pos)
            if q > 0:
                orders.append(Order(sym, bb, -q))
                sell_used += q

        # Passive quotes with imbalance + inventory skew
        b_sz = int(BASE_SIZE + IMB_GAIN * imb  - pos * 0.12)
        a_sz = int(BASE_SIZE - IMB_GAIN * imb  + pos * 0.12)
        b_sz = max(2, min(b_sz, lim - pos  - buy_used))
        a_sz = max(2, min(a_sz, lim + pos  - sell_used))

        bid_px = fv - 1
        ask_px = fv + 1
        if bb is not None: bid_px = min(bid_px, bb + 1)
        if ba is not None: ask_px = max(ask_px, ba - 1)
        if bid_px >= ask_px: bid_px = ask_px - 1

        if b_sz > 0 and lim - pos - buy_used > 0:
            orders.append(Order(sym, bid_px,  b_sz))
        if a_sz > 0 and lim + pos - sell_used > 0:
            orders.append(Order(sym, ask_px, -a_sz))
        return orders

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result = {}
        for sym in ("HYDROGEL_PACK", "VELVETFRUIT_EXTRACT"):
            try:    result[sym] = self._trade(sym, state, sd)
            except: result[sym] = []
        return result, 0, self._save(sd)
