from datamodel import Order, OrderDepth, TradingState
import json


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

ACO_FAIR_DEFAULT = 10000.0
ACO_KALMAN_Q = 0.1
ACO_KALMAN_R = 8.0
ACO_MICROPRICE_WEIGHT = 0.4
ACO_MICROPRICE_CLIP = 2.0
ACO_DEPTH_SHIFT_CLIP = 2.0
ACO_PRESSURE_TAKE_EDGE = 1.0
ACO_BASE_HALF_SPREAD = 2
ACO_IMBALANCE_SHIFT_CLIP = 2.0
ACO_MAX_SKEW = 8
ACO_TAKE_EDGE = 1.0
ACO_TARGET_POSITION = 0
ACO_RESERVATION_SIGMA2 = 2.0
IPR_RICH_TRIM_EDGE = 10
IPR_REPOST_MAX_EXTRA = 2
IPR_PRESSURE_REPOST_COEF = 3.0
MARKET_ACCESS_BID = 9


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
        visible_mid = None
        if best_bid is not None and best_ask is not None:
            visible_mid = (best_bid + best_ask) / 2.0
        elif best_bid is not None:
            visible_mid = best_bid + 7.0
        elif best_ask is not None:
            visible_mid = best_ask - 7.0
        if visible_mid is not None:
            sd["ipr_mid"] = visible_mid

        aggressive_limit = 72
        for ask in sorted(od.sell_orders):
            if self._buy_cap(limit) <= 0:
                break
            ask_qty = -od.sell_orders[ask]
            target_pos = pos + self._buy_used
            take_qty = ask_qty
            if target_pos >= aggressive_limit:
                if visible_mid is not None and ask >= visible_mid:
                    take_qty = min(take_qty, 4)
                else:
                    take_qty = min(take_qty, 8)
            self._add_buy(orders, IPR, ask, take_qty, limit)

        if best_bid is not None and self._buy_cap(limit) > 0:
            imbalance = self._imbalance(od)
            depth_shift = self._depth_price_shift(od)
            pressure_score = max(0.0, imbalance + 0.1 * depth_shift)
            repost_extra = 1 + int(round(pressure_score * IPR_PRESSURE_REPOST_COEF))
            repost_extra = min(repost_extra, IPR_REPOST_MAX_EXTRA)
            bid_px = best_bid + repost_extra
            if best_ask is not None:
                bid_px = min(bid_px, best_ask - 1)
            desired_repost = self._buy_cap(limit)
            if pos + self._buy_used >= aggressive_limit:
                desired_repost = min(desired_repost, 12)
            self._add_buy(orders, IPR, bid_px, desired_repost, limit)

        effective_pos = pos + self._buy_used - self._sell_used
        if effective_pos > 68 and best_bid is not None and visible_mid is not None and best_bid >= visible_mid + IPR_RICH_TRIM_EDGE:
            self._add_sell(orders, IPR, best_bid, min(8, effective_pos - 68), limit)

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
        imbalance_shift = self._clip(1.1 * imbalance, -ACO_IMBALANCE_SHIFT_CLIP, ACO_IMBALANCE_SHIFT_CLIP)
        if spread is not None and (spread <= 14 or spread >= 18):
            predictive_shift = 0.45 * micro_shift + 0.2 * depth_shift + imbalance_shift
        else:
            predictive_shift = 0.35 * micro_shift + 0.05 * depth_shift + 0.9 * imbalance_shift
        reservation_price = fair - (pos - ACO_TARGET_POSITION) * (ACO_RESERVATION_SIGMA2 / limit)
        quote_fair = reservation_price + predictive_shift

        dynamic_take_edge = ACO_PRESSURE_TAKE_EDGE + (1 if abs(pos) > 60 else 0)
        if spread is not None and 14 < spread < 18:
            dynamic_take_edge += 0.5
        if od.sell_orders:
            for ask in sorted(od.sell_orders):
                if self._buy_cap(limit) <= 0:
                    break
                edge = quote_fair - ask
                if edge < dynamic_take_edge:
                    break
                ask_qty = -od.sell_orders[ask]
                take_qty = min(ask_qty, 18 if edge < dynamic_take_edge + 1 else 28)
                if pos + self._buy_used > 55:
                    take_qty = min(take_qty, 10)
                self._add_buy(orders, ACO, ask, take_qty, limit)

        if od.buy_orders:
            for bid in sorted(od.buy_orders, reverse=True):
                if self._sell_cap(limit) <= 0:
                    break
                edge = bid - quote_fair
                if edge < dynamic_take_edge:
                    break
                bid_qty = od.buy_orders[bid]
                take_qty = min(bid_qty, 18 if edge < dynamic_take_edge + 1 else 28)
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

        buy_size = 40
        sell_size = 40
        if predictive_shift > 1.75:
            buy_size += 8
            sell_size -= 4
        elif predictive_shift < -1.75:
            buy_size -= 4
            sell_size += 8

        if pos < -20:
            buy_size = max(buy_size, 56)
            sell_size = min(sell_size, 18)
        elif pos > 20:
            buy_size = min(buy_size, 18)
            sell_size = max(sell_size, 56)

        if abs(pos) > 60:
            if pos > 0:
                buy_size = 8
                sell_size = 64
            else:
                buy_size = 64
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
