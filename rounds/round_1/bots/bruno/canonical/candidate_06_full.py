"""
IMC Prosperity 4 - Round 1
candidate_06_full:

La mejora completa del bot del compañero (candidate_26, ~10,090 P&L).
Combina TODAS las mejoras en un solo bot:

  1. BASE: candidate_26 (imbalance signal, centered skew HS=5, one-sided book,
     asymmetric quote sizes, position-dependent take filter)

  2. KALMAN FILTER para FV dinámico (en lugar de ACO_FV=10000 fijo)
     - Converge rápido a ~10000 pero se adapta a cualquier drift intraday
     - KF_Q=0.01, KF_R=4.0

  3. HMM 2 estados (CALM / VOLATILE) para HS adaptativo
     - CALM (sigma=2): HS=3, quotes grandes (72) → más fills
     - VOLATILE (sigma=5): HS=6, quotes pequeños (40) → más seguro
     - HS varía suavemente: round(3 + 3 * p_vol)

  4. EXIT OVERLAY: cuando |position| > EXIT_THRESH (60), coloca una orden
     AGRESIVA adicional para reducir el exceso de inventario:
     - Muy largo (pos > 60): venta al best_bid (cruzamos el spread)
     - Muy corto (pos < -60): compra al best_ask
     - Tamaño: 40% del exceso, mínimo 1 unidad
     Esto evita que la posición se quede bloqueada en ±80 esperando fills pasivos.

  5. IMBALANCE SUAVIZADO con EWM (alpha=0.3) para reducir ruido en el
     micro_shift, en lugar de usar el imbalance raw de cada tick.

Por qué el exit overlay importa:
  Sin él: si pos=+75, el ask pasivo está en ~FV+HS-skew. A veces no llena
  durante muchos ticks. El bot está "bloqueado" largo sin poder hacer MM.
  Con él: vendemos activamente ~6 unidades al best_bid (coste ~2 ticks cada
  una), recuperamos capacidad de compra, y podemos seguir haciendo MM.
  El coste del crossing se recupera rápido con los fills adicionales.
"""
from datamodel import Order, TradingState
import json
import math

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

# Kalman filter
KF_Q   = 0.01
KF_R   = 4.0
KF_P0  = 25.0
KF_FV0 = 10000.0

# HMM
HMM_SIGMA_CALM = 2.0
HMM_SIGMA_VOL  = 5.0
HMM_P00 = 0.97
HMM_P11 = 0.93

# Spread bounds (driven by HMM)
HS_MIN = 3
HS_MAX = 6
ACO_SKEW = 3

# Exit overlay
EXIT_THRESH = 60
EXIT_FRAC   = 0.40   # fracción del exceso a liquidar por tick

# EWM imbalance smoothing
IMB_ALPHA = 0.3


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

    def _raw_imbalance(self, od):
        bb = self._best_bid(od)
        ba = self._best_ask(od)
        if bb is None or ba is None:
            return 0.0
        bv  = od.buy_orders.get(bb, 0)
        av  = -od.sell_orders.get(ba, 0)
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

    # ── Kalman filter ─────────────────────────────────────────────────────────

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

    # ── HMM forward update ────────────────────────────────────────────────────

    def _gauss(self, x, sigma):
        return math.exp(-0.5 * (x / sigma) ** 2)

    def _hmm_update(self, sd, delta_mid):
        p_vol  = sd.get("hmm_pv", 0.5)
        p_calm = 1.0 - p_vol

        pp_calm = p_calm * HMM_P00 + p_vol * (1.0 - HMM_P11)
        pp_vol  = p_calm * (1.0 - HMM_P00) + p_vol * HMM_P11

        obs    = abs(delta_mid)
        e_calm = self._gauss(obs, HMM_SIGMA_CALM)
        e_vol  = self._gauss(obs, HMM_SIGMA_VOL)

        new_calm = pp_calm * e_calm
        new_vol  = pp_vol  * e_vol
        total = new_calm + new_vol
        if total > 1e-15:
            new_calm /= total
            new_vol  /= total
        else:
            new_calm, new_vol = 0.5, 0.5

        sd["hmm_pv"] = new_vol
        return new_vol

    # ── EWM imbalance ─────────────────────────────────────────────────────────

    def _smooth_imbalance(self, sd, od):
        raw = self._raw_imbalance(od)
        prev = sd.get("ewm_imb", 0.0)
        smoothed = IMB_ALPHA * raw + (1.0 - IMB_ALPHA) * prev
        sd["ewm_imb"] = smoothed
        return smoothed

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

    # ── ACO: todo combinado ───────────────────────────────────────────────────

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

        # Mid price
        if bb is not None and ba is not None:
            mid = (bb + ba) / 2.0
        elif bb is not None:
            mid = bb + HS_MIN
        elif ba is not None:
            mid = ba - HS_MIN
        else:
            return []

        # 1. Kalman FV
        fv     = self._kf_update(sd, mid)
        fv_int = round(fv)

        # 2. HMM regime → HS adaptativo
        prev_mid = sd.get("prev_mid", mid)
        sd["prev_mid"] = mid
        p_vol = self._hmm_update(sd, mid - prev_mid)
        hs      = round(HS_MIN + (HS_MAX - HS_MIN) * p_vol)  # 3→6
        buy_sz  = round(72 - 32 * p_vol)                      # 72→40
        sell_sz = buy_sz

        # 3. EWM imbalance suavizado
        imb   = self._smooth_imbalance(sd, od)
        micro = self._clip(2.0 * imb, -2.0, 2.0)

        # ── One-sided book: solo bids ──
        if bb is not None and ba is None:
            vis = od.buy_orders[bb]
            if pos > 0 and bb >= fv_int - 2:
                vpos = self._add_sell(orders, ACO, bb, min(vis, max(12, pos)), vpos, max_pos)
            elif bb > fv_int + hs and pos > -35:
                vpos = self._add_sell(orders, ACO, bb, min(vis, 18), vpos, max_pos)
            ask_px = max(bb + 1, fv_int + hs - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_sell(orders, ACO, ask_px, 42 if pos > 20 else 18, vpos, max_pos)
            return orders

        # ── One-sided book: solo asks ──
        if ba is not None and bb is None:
            vis = -od.sell_orders[ba]
            if pos < 0 and ba <= fv_int + 2:
                vpos = self._add_buy(orders, ACO, ba, min(vis, max(12, -pos)), vpos, max_pos)
            elif ba < fv_int - hs and pos < 35:
                vpos = self._add_buy(orders, ACO, ba, min(vis, 18), vpos, max_pos)
            bid_px = min(ba - 1, fv_int - hs - round((pos / max_pos) * ACO_SKEW))
            vpos = self._add_buy(orders, ACO, bid_px, 42 if pos < -20 else 18, vpos, max_pos)
            return orders

        # ── Two-sided: takes agresivos ──
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

        # 4. EXIT OVERLAY: reducción agresiva de inventario extremo
        sell_cap_remaining = max_pos + self._start_pos - self._sell_used
        buy_cap_remaining  = max_pos - self._start_pos - self._buy_used

        if vpos > EXIT_THRESH and bb is not None and sell_cap_remaining > 0:
            excess   = vpos - EXIT_THRESH
            exit_qty = max(1, round(excess * EXIT_FRAC))
            exit_qty = min(exit_qty, sell_cap_remaining)
            orders.append(Order(ACO, bb, -exit_qty))
            self._sell_used      += exit_qty
            sell_cap_remaining   -= exit_qty
            vpos                 -= exit_qty

        elif vpos < -EXIT_THRESH and ba is not None and buy_cap_remaining > 0:
            excess   = -vpos - EXIT_THRESH
            exit_qty = max(1, round(excess * EXIT_FRAC))
            exit_qty = min(exit_qty, buy_cap_remaining)
            orders.append(Order(ACO, ba, exit_qty))
            self._buy_used      += exit_qty
            buy_cap_remaining   -= exit_qty
            vpos                += exit_qty

        # 5. Quotes pasivos con Kalman FV + imbalance suavizado + HS adaptativo
        inv_skew = round((pos / max_pos) * ACO_SKEW)
        qfair    = fv + micro

        bid_px = min(bb + 1, qfair - hs - inv_skew)
        ask_px = max(ba - 1, qfair + hs - inv_skew)

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
