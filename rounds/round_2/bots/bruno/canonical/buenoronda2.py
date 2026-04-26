from datamodel import Order, OrderDepth, TradingState
import json

# ── Changes vs 338996 ────────────────────────────────────────────────────────
# 1. MAF bid: 9 → 1500  (9 can never win the MAF auction)
# 2. Kalman: Q=0.1,R=8.0 → Q=0.092,R=6.75  (exact R2 MLE-calibrated values)
# 3. Imbalance gain: 1.1 → 5.0, clip 2.0 → 5.0
#    IC=0.647, β≈6.85 tick/unit. Old gain captured ~16% of signal.
#    New gain captures 73%.  Uses full signal to SIZE and SHIFT passive quotes.
# 4. Take threshold capped at Kalman fair ± MAX_TAKE_ABOVE_FAIR (=0):
#    takes only fire when ask ≤ Kalman fair (signal shifts quotes, not takes).
#    Prevents over-chasing imbalance in aggressive mode.
# 5. IPR: pure max-long (remove aggressive_limit=72 cap and rich-trim).
#    IPR drifts +1000/day; every unit below +80 is unrealised profit.
# 6. ACO sizing: signal-first then inventory correction.
#    When |predictive_shift| > SIGNAL_DOM (2.5), imbalance overrides
#    the position-based size skew — avoids fighting a strong signal.
# 7. Take edge: 1.0 → 1.5  (slightly more conservative to reduce noise fills)
# ─────────────────────────────────────────────────────────────────────────────

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

ACO_FAIR_DEFAULT = 10000.0
ACO_KALMAN_Q = 0.092          # MLE-calibrated (was 0.1)
ACO_KALMAN_R = 6.75           # MLE-calibrated (was 8.0)
ACO_MICROPRICE_WEIGHT = 0.4
ACO_MICROPRICE_CLIP = 2.0
ACO_DEPTH_SHIFT_CLIP = 2.0
ACO_IMBALANCE_GAIN = 5.0        # was implicit 1.1 — captures 73% of IC signal
ACO_IMBALANCE_SHIFT_CLIP = 5.0  # was 2.0
ACO_BASE_HALF_SPREAD = 2        # keep competitive passive queue
ACO_TAKE_EDGE = 1.5             # was 1.0
# Takes are capped ±MAX_TAKE_ABOVE_FAIR ticks from Kalman fair value.
# Full imbalance signal shifts passive quotes; takes stay near Kalman fair.
ACO_MAX_TAKE_ABOVE_FAIR = 0   # takes capped at Kalman fair; imbalance shifts quotes, not takes
ACO_TARGET_POSITION = 0
ACO_RESERVATION_SIGMA2 = 2.0
MARKET_ACCESS_BID = 1500      # was 9 — now able to win auction


class Trader:
    def bid(self):
        return MARKET_ACCESS_BID

    def _load(self, trader_data: str) -> dict:
        if not trader_data:
            return {}
        try:
            data = json.loads(trader_data)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _save(self, data: dict) -> str:
        try:
            return json.dumps(data, separators=(",", ":"))
        except Exception:
            return "{}"

    def _best_bid(self, od: OrderDepth):
        return max(od.buy_orders) if od and od.buy_orders else None

    def _best_ask(self, od: OrderDepth):
        return min(od.sell_orders) if od and od.sell_orders else None

    def _clip(self, value: float, lo: float, hi: float) -> float:
        return min(max(value, lo), hi)

    def _imbalance(self, od: OrderDepth) -> float:
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is None or best_ask is None:
            return 0.0
        bid_vol = od.buy_orders.get(best_bid, 0)
        ask_vol = -od.sell_orders.get(best_ask, 0)
        total = bid_vol + ask_vol
        if total <= 0:
            return 0.0
        return (bid_vol - ask_vol) / total

    def _reset_caps(self, start_pos: int):
        self._start_pos = start_pos
        self._buy_used = 0
        self._sell_used = 0

    def _buy_cap(self, limit: int) -> int:
        return max(0, limit - self._start_pos - self._buy_used)

    def _sell_cap(self, limit: int) -> int:
        return max(0, limit + self._start_pos - self._sell_used)

    def _add_buy(self, orders, product, price, qty, limit):
        q = min(max(int(qty), 0), self._buy_cap(limit))
        if q > 0:
            orders.append(Order(product, int(round(price)), q))
            self._buy_used += q

    def _add_sell(self, orders, product, price, qty, limit):
        q = min(max(int(qty), 0), self._sell_cap(limit))
        if q > 0:
            orders.append(Order(product, int(round(price)), -q))
            self._sell_used += q

    def _kalman_update(self, state_dict: dict, obs):
        fair = float(state_dict.get("fair", ACO_FAIR_DEFAULT))
        var = float(state_dict.get("var", 25.0))
        if obs is None:
            var = min(var + ACO_KALMAN_Q, 100.0)
            state_dict["fair"] = fair
            state_dict["var"] = var
            return fair
        pred_var = min(var + ACO_KALMAN_Q, 100.0)
        k = pred_var / (pred_var + ACO_KALMAN_R)
        fair = fair + k * (obs - fair)
        var = (1.0 - k) * pred_var
        state_dict["fair"] = fair
        state_dict["var"] = var
        return fair

    def _microprice(self, od: OrderDepth):
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is None or best_ask is None:
            return None
        bid_vol = od.buy_orders.get(best_bid, 0)
        ask_vol = -od.sell_orders.get(best_ask, 0)
        total = bid_vol + ask_vol
        if total <= 0:
            return (best_bid + best_ask) / 2.0
        return (best_bid * ask_vol + best_ask * bid_vol) / total

    def _depth_price_shift(self, od: OrderDepth):
        if od is None or not od.buy_orders or not od.sell_orders:
            return 0.0
        bid_levels = sorted(od.buy_orders.items(), reverse=True)[:3]
        ask_levels = sorted(od.sell_orders.items())[:3]
        bid_vol = sum(q for _, q in bid_levels)
        ask_vol = sum(-q for _, q in ask_levels)
        if bid_vol <= 0 or ask_vol <= 0:
            return 0.0
        weighted_bid = sum(price * qty for price, qty in bid_levels) / bid_vol
        weighted_ask = sum(price * (-qty) for price, qty in ask_levels) / ask_vol
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is None or best_ask is None:
            return 0.0
        raw_mid = (best_bid + best_ask) / 2.0
        depth_mid = (weighted_bid + weighted_ask) / 2.0
        return self._clip(depth_mid - raw_mid, -ACO_DEPTH_SHIFT_CLIP, ACO_DEPTH_SHIFT_CLIP)

    def _observe_aco_mid(self, od: OrderDepth, prior_fair: float):
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is not None and best_ask is not None:
            micro = self._microprice(od)
            raw_mid = (best_bid + best_ask) / 2.0
            depth_shift = self._depth_price_shift(od)
            if micro is None:
                return raw_mid + 0.2 * depth_shift
            micro_shift = self._clip(micro - raw_mid, -ACO_MICROPRICE_CLIP, ACO_MICROPRICE_CLIP)
            spread = best_ask - best_bid
            if spread <= 14 or spread >= 18:
                return raw_mid + ACO_MICROPRICE_WEIGHT * micro_shift + 0.25 * depth_shift
            return raw_mid + 0.3 * micro_shift
        if best_bid is not None:
            return min(best_bid + 8.0, prior_fair + 6.0)
        if best_ask is not None:
            return max(best_ask - 8.0, prior_fair - 6.0)
        return None

    def _trade_ipr(self, state: TradingState, sd: dict):
        od = state.order_depths.get(IPR)
        if od is None:
            return []

        pos = state.position.get(IPR, 0)
        limit = LIMITS[IPR]
        self._reset_caps(pos)
        orders = []

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)

        # Aggressive take: buy every ask available up to position limit
        for ask in sorted(od.sell_orders):
            if self._buy_cap(limit) <= 0:
                break
            self._add_buy(orders, IPR, ask, -od.sell_orders[ask], limit)

        # Passive bid for remaining capacity
        if best_bid is not None and self._buy_cap(limit) > 0:
            bid_px = best_bid + 1
            if best_ask is not None:
                bid_px = min(bid_px, best_ask - 1)
            self._add_buy(orders, IPR, bid_px, self._buy_cap(limit), limit)

        return orders

    def _trade_aco(self, state: TradingState, sd: dict):
        od = state.order_depths.get(ACO)
        if od is None:
            return []

        pos = state.position.get(ACO, 0)
        limit = LIMITS[ACO]
        self._reset_caps(pos)
        orders = []
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)

        if best_bid is None and best_ask is None:
            return orders

        aco_state = sd.get("aco", {})
        prior_fair = float(aco_state.get("fair", ACO_FAIR_DEFAULT))
        obs = self._observe_aco_mid(od, prior_fair)
        fair = self._kalman_update(aco_state, obs)
        sd["aco"] = aco_state

        imbalance = self._imbalance(od)
        micro = self._microprice(od)
        micro_shift = 0.0
        depth_shift = self._depth_price_shift(od)
        spread = None
        if best_bid is not None and best_ask is not None:
            spread = best_ask - best_bid
        if micro is not None and best_bid is not None and best_ask is not None:
            raw_mid = (best_bid + best_ask) / 2.0
            micro_shift = self._clip(micro - raw_mid, -ACO_MICROPRICE_CLIP, ACO_MICROPRICE_CLIP)

        # Stronger imbalance: gain 5.0, clip 5.0 (was 1.1 / 2.0)
        imbalance_shift = self._clip(
            ACO_IMBALANCE_GAIN * imbalance,
            -ACO_IMBALANCE_SHIFT_CLIP,
            ACO_IMBALANCE_SHIFT_CLIP,
        )
        if spread is not None and (spread <= 14 or spread >= 18):
            predictive_shift = 0.45 * micro_shift + 0.2 * depth_shift + imbalance_shift
        else:
            predictive_shift = 0.35 * micro_shift + 0.05 * depth_shift + 0.9 * imbalance_shift

        reservation_price = fair - (pos - ACO_TARGET_POSITION) * (ACO_RESERVATION_SIGMA2 / limit)
        quote_fair = reservation_price + predictive_shift

        dynamic_take_edge = ACO_TAKE_EDGE + (1 if abs(pos) > 60 else 0)
        if spread is not None and 14 < spread < 18:
            dynamic_take_edge += 0.5

        fv_int = round(fair)
        # Take thresholds: signal-shifted but capped near Kalman fair.
        # Imbalance shifts quotes; it does not make us chase far-above-fair asks.
        buy_take_thr = min(
            int(round(quote_fair - dynamic_take_edge)),
            fv_int + ACO_MAX_TAKE_ABOVE_FAIR,
        )
        sell_take_thr = max(
            int(round(quote_fair + dynamic_take_edge)),
            fv_int - ACO_MAX_TAKE_ABOVE_FAIR,
        )

        if od.sell_orders:
            for ask in sorted(od.sell_orders):
                if self._buy_cap(limit) <= 0 or ask > buy_take_thr:
                    break
                edge = buy_take_thr - ask
                ask_qty = -od.sell_orders[ask]
                take_qty = min(ask_qty, 18 if edge < 2 else 28)
                if pos + self._buy_used > 55:
                    take_qty = min(take_qty, 10)
                self._add_buy(orders, ACO, ask, take_qty, limit)

        if od.buy_orders:
            for bid in sorted(od.buy_orders, reverse=True):
                if self._sell_cap(limit) <= 0 or bid < sell_take_thr:
                    break
                edge = bid - sell_take_thr
                bid_qty = od.buy_orders[bid]
                take_qty = min(bid_qty, 18 if edge < 2 else 28)
                if pos - self._sell_used < -55:
                    take_qty = min(take_qty, 10)
                self._add_sell(orders, ACO, bid, take_qty, limit)

        half_spread = ACO_BASE_HALF_SPREAD + (1 if abs(pos) > 65 else 0)
        if abs(micro_shift) > 1.5:
            half_spread += 1
        bid_px = int(round(quote_fair - half_spread))
        ask_px = int(round(quote_fair + half_spread))

        if best_bid is not None:
            bid_px = min(bid_px, best_bid + 1)
        if best_ask is not None:
            ask_px = max(ask_px, best_ask - 1)

        if best_ask is not None and bid_px >= best_ask:
            bid_px = best_ask - 1
        if best_bid is not None and ask_px <= best_bid:
            ask_px = best_bid + 1

        if best_bid is None and best_ask is not None:
            bid_px = min(best_ask - 1, int(round(quote_fair - half_spread)))
        if best_ask is None and best_bid is not None:
            ask_px = max(best_bid + 1, int(round(quote_fair + half_spread)))

        # Signal-first sizing, then soft inventory correction.
        # Threshold to suppress inventory override when signal is strong:
        # if |predictive_shift| > SIGNAL_DOM, don't fight the signal with
        # the inventory skew (only cap at the emergency rebalance level).
        SIGNAL_DOM = 2.5

        buy_size = 40
        sell_size = 40
        if predictive_shift > 3.5:
            buy_size = 56; sell_size = 24
        elif predictive_shift > 1.75:
            buy_size = 48; sell_size = 32
        elif predictive_shift < -3.5:
            buy_size = 24; sell_size = 56
        elif predictive_shift < -1.75:
            buy_size = 32; sell_size = 48

        # Inventory management — only when signal is not strongly opposing it
        if pos < -20 and predictive_shift > -SIGNAL_DOM:
            buy_size = max(buy_size, 56)
            sell_size = min(sell_size, 18)
        elif pos > 20 and predictive_shift < SIGNAL_DOM:
            buy_size = min(buy_size, 18)
            sell_size = max(sell_size, 56)

        # Emergency rebalance for extreme positions
        if abs(pos) > 65:
            if pos > 0:
                buy_size = 8
                sell_size = 72
            else:
                buy_size = 72
                sell_size = 8

        if self._buy_cap(limit) > 0 and (best_ask is None or bid_px < best_ask):
            self._add_buy(orders, ACO, bid_px, buy_size, limit)
        if self._sell_cap(limit) > 0 and (best_bid is None or ask_px > best_bid):
            self._add_sell(orders, ACO, ask_px, sell_size, limit)

        return orders

    def run(self, state: TradingState):
        sd = self._load(state.traderData)
        result = {}

        try:
            result[IPR] = self._trade_ipr(state, sd)
        except Exception:
            result[IPR] = []

        try:
            result[ACO] = self._trade_aco(state, sd)
        except Exception:
            result[ACO] = []

        return result, 0, self._save(sd)