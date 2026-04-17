from datamodel import Order, TradingState
import json


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}
IPR_SLOPE = 0.001
ACO_FV = 10000


class Trader:
    def _load(self, trader_data):
        if not trader_data:
            return {}
        try:
            loaded = json.loads(trader_data)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            return {}

    def _save(self, data):
        try:
            return json.dumps(data, separators=(",", ":"))
        except Exception:
            return "{}"

    def _best_bid(self, od):
        return max(od.buy_orders) if od and od.buy_orders else None

    def _best_ask(self, od):
        return min(od.sell_orders) if od and od.sell_orders else None

    def _mid(self, od):
        bid = self._best_bid(od)
        ask = self._best_ask(od)
        if bid is not None and ask is not None:
            return (bid + ask) / 2
        return None

    def _spread(self, od):
        bid = self._best_bid(od)
        ask = self._best_ask(od)
        if bid is not None and ask is not None:
            return ask - bid
        return None

    def _imbalance(self, od):
        bid_depth = sum(q for q in od.buy_orders.values()) if od and od.buy_orders else 0
        ask_depth = sum(-q for q in od.sell_orders.values()) if od and od.sell_orders else 0
        total = bid_depth + ask_depth
        if total <= 0:
            return 0.0
        return (bid_depth - ask_depth) / total

    def _reset_caps(self, start_pos):
        self._start_pos = start_pos
        self._buy_used = 0
        self._sell_used = 0

    def _add_buy(self, orders, product, price, qty, virtual_pos, max_pos):
        cap = max_pos - self._start_pos - self._buy_used
        order_qty = min(max(qty, 0), cap)
        if order_qty > 0:
            orders.append(Order(product, int(round(price)), int(order_qty)))
            self._buy_used += order_qty
            virtual_pos += order_qty
        return virtual_pos

    def _add_sell(self, orders, product, price, qty, virtual_pos, max_pos):
        cap = max_pos + self._start_pos - self._sell_used
        order_qty = min(max(qty, 0), cap)
        if order_qty > 0:
            orders.append(Order(product, int(round(price)), -int(order_qty)))
            self._sell_used += order_qty
            virtual_pos -= order_qty
        return virtual_pos

    def _clip(self, value, lo, hi):
        return max(lo, min(hi, value))

    def _ipr_fv(self, state, od, data):
        day_start = data.get("ipr_day_start")
        mid = self._mid(od)
        if day_start is None and mid is not None:
            day_start = mid - IPR_SLOPE * state.timestamp
            data["ipr_day_start"] = day_start
        if day_start is None:
            return None
        return day_start + IPR_SLOPE * state.timestamp

    def _trade_ipr_hybrid(self, state, data):
        od = state.order_depths.get(IPR)
        if od is None:
            return []
        fv = self._ipr_fv(state, od, data)
        mid = self._mid(od)
        if fv is None or mid is None:
            return []
        residual = mid - fv
        spread = self._spread(od)
        imbalance = self._imbalance(od)
        orders = []
        pos = state.position.get(IPR, 0)
        self._reset_caps(pos)
        virtual_pos = pos

        abnormal = abs(residual) > 9 or (spread is not None and spread > 19)
        max_pos = 45 if abnormal else 78
        target = 65 + int(self._clip((-0.4 * residual + 4.0 * imbalance), -20, 13))
        if abnormal:
            target = min(pos, 35)
        target = int(self._clip(target, 0, max_pos))

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if target > pos and best_ask is not None:
            buy_edge = fv - best_ask
            if buy_edge > -2 or imbalance > 0.35:
                virtual_pos = self._add_buy(orders, IPR, best_ask, min(18, target - pos), virtual_pos, max_pos)
        if target < pos and best_bid is not None:
            sell_edge = best_bid - fv
            if sell_edge > 2 or abnormal:
                virtual_pos = self._add_sell(orders, IPR, best_bid, min(18, pos - target), virtual_pos, max_pos)

        if best_bid is not None and best_ask is not None and not abnormal:
            skew = pos * 0.04 - imbalance * 2
            bid_px = min(best_bid + 1, int(fv - 4 - skew))
            ask_px = max(best_ask - 1, int(fv + 6 - skew))
            if bid_px < best_ask and target >= pos:
                virtual_pos = self._add_buy(orders, IPR, bid_px, 8, virtual_pos, max_pos)
            if ask_px > best_bid and virtual_pos > target + 10 and ask_px > fv + 2:
                virtual_pos = self._add_sell(orders, IPR, ask_px, 8, virtual_pos, max_pos)
        return orders

    def _aco_fv(self, od, data):
        mid = self._mid(od)
        ema = data.get("aco_ema")
        if mid is not None:
            if ema is None:
                ema = mid
            else:
                ema = 0.98 * ema + 0.02 * mid
            data["aco_ema"] = ema
            dev_count = data.get("aco_dev_count", 0)
            if abs(mid - ACO_FV) > 30:
                dev_count += 1
            else:
                dev_count = max(0, dev_count - 2)
            data["aco_dev_count"] = dev_count
        else:
            dev_count = data.get("aco_dev_count", 0)
        if ema is not None and dev_count > 20:
            return 0.65 * ACO_FV + 0.35 * ema
        return ACO_FV

    def _trade_aco_adaptive(self, state, data):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        fv = self._aco_fv(od, data)
        mid = self._mid(od)
        if mid is None:
            return []
        residual = mid - fv
        spread = self._spread(od)
        imbalance = self._imbalance(od)
        dev_count = data.get("aco_dev_count", 0)
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = 45 if dev_count > 20 else 78
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)

        score = -0.25 * residual + 5.0 * imbalance - 0.04 * pos
        if spread is not None and spread > 20:
            score *= 0.6

        if best_ask is not None:
            ask_edge = fv + score - best_ask
            if ask_edge > 1.0:
                size = 10 + int(min(12, max(0, score)))
                virtual_pos = self._add_buy(orders, ACO, best_ask, size, virtual_pos, max_pos)
            elif best_ask < fv - 8 and dev_count <= 20:
                virtual_pos = self._add_buy(orders, ACO, best_ask, 8, virtual_pos, max_pos)

        if best_bid is not None:
            bid_edge = best_bid - (fv + score)
            if bid_edge > 1.0:
                size = 10 + int(min(12, max(0, -score)))
                virtual_pos = self._add_sell(orders, ACO, best_bid, size, virtual_pos, max_pos)
            elif best_bid > fv + 8 and dev_count <= 20:
                virtual_pos = self._add_sell(orders, ACO, best_bid, 8, virtual_pos, max_pos)

        if best_bid is not None and best_ask is not None:
            skew = pos * 0.08 - imbalance * 2
            bid_px = min(best_bid + 1, int(fv - 5 - skew))
            ask_px = max(best_ask - 1, int(fv + 5 - skew))
            if bid_px < best_ask and score >= -2:
                virtual_pos = self._add_buy(orders, ACO, bid_px, 10, virtual_pos, max_pos)
            if ask_px > best_bid and score <= 2:
                virtual_pos = self._add_sell(orders, ACO, ask_px, 10, virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr_hybrid(state, data)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco_adaptive(state, data)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)
