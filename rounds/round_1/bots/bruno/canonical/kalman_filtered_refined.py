"""
IMC Prosperity 4 - Round 1
candidate_07_kf_tuned:

Base: candidate_04_kalman_imb (Kalman FV, ~10,094 P&L)
Data-driven improvements calibrated from actual CSV price data (3 days, 30k ticks).

WHY the HMM and exit overlay HURT:
  - AC(delta_mid, lag-1) ≈ 0.0 → regime has NO predictive power for the next tick.
    Widening the spread in "volatile" ticks just loses fills with no offsetting benefit.
  - Exit overlay crosses at best_bid (~9992) when our passive ask is at 10005.
    That is a 13-tick loss per unit. NOT worth the capacity recovery speed.

Data findings (EDA on 3-day CSV):
  - Mid price (two-sided ticks only): mean=10000.21, stdev=4.86 → var≈24.
  - KF_R should be ~25 (measurement noise variance), NOT 4.
    With KF_R=4 the filter overreacts to mid noise; KF_FV drifts from 10000.
    With KF_R=25, K≈0.02 at steady state → FV very stable near 10000.
  - Market bid-ask spread = 16 ticks (63% of two-sided ticks). HS=5 is
    well inside the market, which is correct — we capture inner order flow.
  - Take opportunities: 5% of ticks have ask<FV or bid>FV.
    Edge=2 takes (ask=9998) appear 397 times / 30k ticks; previously SKIPPED
    when pos>40. These are free 2-tick profit with 40+ units of remaining
    capacity — no reason to skip them.
  - Edge=3 takes similarly safe to take even up to pos≈65.

Changes vs candidate_04:
  1. KF_R = 25.0 (was 4.0) — calibrated from actual mid-price variance ≈ 24.
  2. KF_Q = 0.005 (was 0.01) — FV is very stable across all 3 days.
  3. Take filter relaxed:
       OLD: skip if |pos| > 40 and edge < 3  (skips edge=1 and edge=2)
       NEW: skip if |pos| > 60 and edge < 2  (only skips edge=1 at extreme pos)
     This captures edge=2 and edge=3 takes that are free money even at
     moderate inventory, without adding risk when position is near limit.

Everything else unchanged from candidate_04 / teammate's proven logic.
"""
from datamodel import Order, TradingState
import json

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

# Kalman filter — recalibrated from EDA (mid stdev=4.86, var≈24)
KF_Q   = 0.005
KF_R   = 25.0
KF_P0  = 25.0
KF_FV0 = 10000.0

ACO_HS   = 5
ACO_SKEW = 3

# Take filter: only skip tiny-edge takes when position is very extreme
TAKE_POS_THRESH = 60   # was 40
TAKE_EDGE_THRESH = 2   # was 3 → now we only skip edge=1, not edge=2


class Trader:
    def _load(self, td):
        if not td:
            return {}
        try:
            loaded = json.loads(td)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            return {}

    def _save(self, d):
        try:
            return json.dumps(d, separators=(",", ":"))
        except Exception:
            return "{}"

    def _best_bid(self, od):
        return max(od.buy_orders) if od and od.buy_orders else None

    def _best_ask(self, od):
        return min(od.sell_orders) if od and od.sell_orders else None

    def _clip(self, v, lo, hi):
        return min(max(v, lo), hi)

    def _imbalance(self, od):
        bb = self._best_bid(od)
        ba = self._best_ask(od)
        if bb is None or ba is None:
            return 0.0
        bv = od.buy_orders.get(bb, 0)
        av = -od.sell_orders.get(ba, 0)
        tot = bv + av
        return (bv - av) / tot if tot > 0 else 0.0

    def _reset_caps(self, pos):
        self._start_pos = pos
        self._buy_used  = 0
        self._sell_used = 0

    def _add_buy(self, orders, product, price, qty, vpos, max_pos):
        cap = max_pos - self._start_pos - self._buy_used
        q = min(max(qty, 0), cap)
        if q > 0:
            orders.append(Order(product, int(round(price)), int(q)))
            self._buy_used += q
            vpos += q
        return vpos

    def _add_sell(self, orders, product, price, qty, vpos, max_pos):
        cap = max_pos + self._start_pos - self._sell_used
        q = min(max(qty, 0), cap)
        if q > 0:
            orders.append(Order(product, int(round(price)), -int(q)))
            self._sell_used += q
            vpos -= q
        return vpos

    def _kf_update(self, sd, mid):
        fv = sd.get("kf_fv", KF_FV0)
        P  = sd.get("kf_P",  KF_P0)
        P_pred = P + KF_Q
        K      = P_pred / (P_pred + KF_R)
        fv_new = fv + K * (mid - fv)
        P_new  = (1.0 - K) * P_pred
        sd["kf_fv"] = fv_new
        sd["kf_P"]  = P_new
        return fv_new

    def _trade_ipr(self, state):
        od = state.order_depths.get(IPR)
        if od is None:
            return []
        orders = []
        vpos = state.position.get(IPR, 0)
        self._reset_caps(vpos)
        max_pos = LIMITS[IPR]

        for ask in sorted(od.sell_orders):
            if vpos >= max_pos:
                break
            vpos = self._add_buy(orders, IPR, ask, -od.sell_orders[ask], vpos, max_pos)

        bb = self._best_bid(od)
        ba = self._best_ask(od)
        if vpos < max_pos and bb is not None:
            bid_px = min(bb + 1, ba - 1) if ba is not None else bb + 1
            vpos = self._add_buy(orders, IPR, bid_px, max_pos - vpos, vpos, max_pos)
        return orders

    def _trade_aco(self, state, sd):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        vpos    = pos
        max_pos = LIMITS[ACO]
        bb = self._best_bid(od)
        ba = self._best_ask(od)

        if bb is not None and ba is not None:
            mid = (bb + ba) / 2.0
        elif bb is not None:
            mid = bb + ACO_HS
        elif ba is not None:
            mid = ba - ACO_HS
        else:
            return []

        fv     = self._kf_update(sd, mid)
        fv_int = round(fv)

        if bb is not None and ba is None:
            vis = od.buy_orders[bb]
            if pos > 0 and bb >= fv_int - 2:
                vpos = self._add_sell(orders, ACO, bb, min(vis, max(12, pos)), vpos, max_pos)
            elif bb > fv_int + ACO_HS and pos > -35:
                vpos = self._add_sell(orders, ACO, bb, min(vis, 18), vpos, max_pos)
            ask_px = max(bb + 1, fv_int + ACO_HS - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_sell(orders, ACO, ask_px, 42 if pos > 20 else 18, vpos, max_pos)
            return orders

        if ba is not None and bb is None:
            vis = -od.sell_orders[ba]
            if pos < 0 and ba <= fv_int + 2:
                vpos = self._add_buy(orders, ACO, ba, min(vis, max(12, -pos)), vpos, max_pos)
            elif ba < fv_int - ACO_HS and pos < 35:
                vpos = self._add_buy(orders, ACO, ba, min(vis, 18), vpos, max_pos)
            bid_px = min(ba - 1, fv_int - ACO_HS - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_buy(orders, ACO, bid_px, 42 if pos < -20 else 18, vpos, max_pos)
            return orders

        for ask in sorted(od.sell_orders):
            if ask >= fv_int:
                break
            edge = fv_int - ask
            if pos > TAKE_POS_THRESH and edge < TAKE_EDGE_THRESH:
                continue
            vpos = self._add_buy(orders, ACO, ask, -od.sell_orders[ask], vpos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= fv_int:
                break
            edge = bid - fv_int
            if pos < -TAKE_POS_THRESH and edge < TAKE_EDGE_THRESH:
                continue
            vpos = self._add_sell(orders, ACO, bid, od.buy_orders[bid], vpos, max_pos)

        imb      = self._imbalance(od)
        micro    = self._clip(2.0 * imb, -2.0, 2.0)
        inv_skew = round((pos / max_pos) * ACO_SKEW)
        qfair    = fv + micro

        bid_px = min(bb + 1, qfair - ACO_HS - inv_skew)
        ask_px = max(ba - 1, qfair + ACO_HS - inv_skew)

        buy_sz  = 72 if pos < -30 else 40 if pos > 35 else 60
        sell_sz = 72 if pos >  30 else 40 if pos < -35 else 60

        if bid_px < ba:
            vpos = self._add_buy(orders, ACO, bid_px, buy_sz, vpos, max_pos)
        if ask_px > bb:
            vpos = self._add_sell(orders, ACO, ask_px, sell_sz, vpos, max_pos)

        return orders

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr(state)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco(state, sd)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(sd)
