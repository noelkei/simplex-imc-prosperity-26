"""
IMC Prosperity 4 - Round 1
candidate_04_kalman_imb:

Base: candidate_26_v3_a3b1_one_sided_exit_overlay (teammate, ~10,090 P&L)
Added: Kalman filter for ACO fair value (dynamic FV instead of hardcoded 10000)

WHY Kalman filter:
  ACO FV is confirmed ~10000 across 3 days (EDA), but intraday it may drift
  slightly. Hardcoding 10000 means our quotes are mis-centered on those ticks.
  The Kalman filter tracks the "true" FV dynamically, converging near 10000
  but adapting to any slow drift or structural shift.

Kalman parameters (calibrated from EDA):
  KF_Q = 0.01  — process noise: FV is very stable (~0.001/tick drift rate)
  KF_R = 4.0   — measurement noise: mid-price has ~2 tick std (variance ≈ 4)
  KF_P0 = 25   — initial uncertainty: FV is ±5 at most initially
  KF_FV0 = 10000 — initial estimate

Behavior:
  - Tick 1: K ≈ 0.86 (strong update toward first observed mid)
  - After ~10 ticks: K ≈ 0.003 (mostly ignores new observations, very stable)
  - Net effect: quoted prices shift by <0.5 ticks on average; protects against
    any intraday drift that the hardcoded bot would miss.

Everything else: identical to teammate's bot (imbalance, centered skew,
one-sided book, asymmetric quote sizes, position filters).
"""
from datamodel import Order, TradingState
import json

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

# Kalman filter constants
KF_Q   = 0.01
KF_R   = 4.0
KF_P0  = 25.0
KF_FV0 = 10000.0

ACO_HS   = 5
ACO_SKEW = 3


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

    # ── Kalman filter for ACO fair value ──────────────────────────────────────

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

    # ── IPR: directional max-long ─────────────────────────────────────────────

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

    # ── ACO: Kalman FV + imbalance + centered skew ────────────────────────────

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

        # Compute mid and update Kalman FV
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

        # ── One-sided book: only bids visible ──
        if bb is not None and ba is None:
            vis = od.buy_orders[bb]
            if pos > 0 and bb >= fv_int - 2:
                vpos = self._add_sell(orders, ACO, bb, min(vis, max(12, pos)), vpos, max_pos)
            elif bb > fv_int + ACO_HS and pos > -35:
                vpos = self._add_sell(orders, ACO, bb, min(vis, 18), vpos, max_pos)
            ask_px = max(bb + 1, fv_int + ACO_HS - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_sell(orders, ACO, ask_px, 42 if pos > 20 else 18, vpos, max_pos)
            return orders

        # ── One-sided book: only asks visible ──
        if ba is not None and bb is None:
            vis = -od.sell_orders[ba]
            if pos < 0 and ba <= fv_int + 2:
                vpos = self._add_buy(orders, ACO, ba, min(vis, max(12, -pos)), vpos, max_pos)
            elif ba < fv_int - ACO_HS and pos < 35:
                vpos = self._add_buy(orders, ACO, ba, min(vis, 18), vpos, max_pos)
            bid_px = min(ba - 1, fv_int - ACO_HS - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_buy(orders, ACO, bid_px, 42 if pos < -20 else 18, vpos, max_pos)
            return orders

        # ── Two-sided book: aggressive takes ──
        for ask in sorted(od.sell_orders):
            if ask >= fv_int:
                break
            edge = fv_int - ask
            if pos > 40 and edge < 3:
                continue
            vpos = self._add_buy(orders, ACO, ask, -od.sell_orders[ask], vpos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= fv_int:
                break
            edge = bid - fv_int
            if pos < -40 and edge < 3:
                continue
            vpos = self._add_sell(orders, ACO, bid, od.buy_orders[bid], vpos, max_pos)

        # ── Passive quotes: Kalman FV + imbalance shift + centered skew ──
        imb        = self._imbalance(od)
        micro      = self._clip(2.0 * imb, -2.0, 2.0)
        inv_skew   = round((pos / max_pos) * ACO_SKEW)
        qfair      = fv + micro

        bid_px = min(bb + 1, qfair - ACO_HS - inv_skew)
        ask_px = max(ba - 1, qfair + ACO_HS - inv_skew)

        buy_sz  = 72 if pos < -30 else 40 if pos > 35 else 60
        sell_sz = 72 if pos >  30 else 40 if pos < -35 else 60

        if bid_px < ba:
            vpos = self._add_buy(orders, ACO, bid_px, buy_sz, vpos, max_pos)
        if ask_px > bb:
            vpos = self._add_sell(orders, ACO, ask_px, sell_sz, vpos, max_pos)

        return orders

    # ── Entry point ───────────────────────────────────────────────────────────

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
