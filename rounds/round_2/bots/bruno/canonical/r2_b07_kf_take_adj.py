"""
IMC Prosperity 4 - Round 2
r2_b07_kf_take_adj — R2 MLE Kalman + imbalance-adjusted take threshold

HYPOTHESIS: Combining R2 reactive Kalman (K≈0.11) with imbalance-adjusted take
threshold. When the Kalman FV momentarily drifts (e.g., price moves to 10008 for
50 ticks), fv_int=10008 and qfair=10012 when imb=1 — the take threshold lifts to
min(10012, 10008+4) = 10012. We'd buy asks up to 10011 thinking FV is 10012.

This has higher variance than b06 because the reactive KF amplifies both valid
drift signals and noise. However, when drift + imbalance align, the combined
signal is very strong and should be exploited.

Parameters: KF_Q=0.092, KF_R=6.75, IMB_GAIN=4.0, IMB_CLIP=4.0,
            TAKE_IMB_ADJ=True, MAX_IMB_TAKE=4.
"""
from datamodel import Order, TradingState
import json

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

KF_Q   = 0.092
KF_R   = 6.75
KF_P0  = 25.0
KF_FV0 = 10000.0

ACO_HS   = 5
ACO_SKEW = 3
IMB_GAIN = 4.0
IMB_CLIP = 4.0

TAKE_POS_THRESH  = 60
TAKE_EDGE_THRESH = 2
MAX_IMB_TAKE     = 4

MAF_BID = 2500


class Trader:
    def _load(self, td):
        if not td:
            return {}
        try:
            d = json.loads(td)
            return d if isinstance(d, dict) else {}
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

        imb      = self._imbalance(od)
        micro    = self._clip(IMB_GAIN * imb, -IMB_CLIP, IMB_CLIP)
        qfair    = fv + micro
        inv_skew = round((pos / max_pos) * ACO_SKEW)

        take_buy_thr  = min(round(qfair), fv_int + MAX_IMB_TAKE)
        take_sell_thr = max(round(qfair), fv_int - MAX_IMB_TAKE)

        for ask in sorted(od.sell_orders):
            if ask >= take_buy_thr:
                break
            edge = take_buy_thr - ask
            if pos > TAKE_POS_THRESH and edge < TAKE_EDGE_THRESH:
                continue
            vpos = self._add_buy(orders, ACO, ask, -od.sell_orders[ask], vpos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= take_sell_thr:
                break
            edge = bid - take_sell_thr
            if pos < -TAKE_POS_THRESH and edge < TAKE_EDGE_THRESH:
                continue
            vpos = self._add_sell(orders, ACO, bid, od.buy_orders[bid], vpos, max_pos)

        bid_px  = min(bb + 1, round(qfair) - ACO_HS - inv_skew)
        ask_px  = max(ba - 1, round(qfair) + ACO_HS - inv_skew)
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

    def bid(self) -> int:
        return MAF_BID
