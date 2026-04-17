from datamodel import Order, TradingState
import json
import math


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}
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
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is None or best_ask is None:
            return None
        return (best_bid + best_ask) / 2.0

    def _clip(self, value, lo, hi):
        return min(max(value, lo), hi)

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

    def _trade_ipr_carry(self, state):
        od = state.order_depths.get(IPR)
        if od is None:
            return []
        orders = []
        virtual_pos = state.position.get(IPR, 0)
        self._reset_caps(virtual_pos)
        max_pos = LIMITS[IPR]

        for ask in sorted(od.sell_orders):
            if virtual_pos >= max_pos:
                break
            available = -od.sell_orders[ask]
            virtual_pos = self._add_buy(orders, IPR, ask, available, virtual_pos, max_pos)

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if virtual_pos < max_pos and best_bid is not None:
            bid_px = best_bid + 1
            if best_ask is not None:
                bid_px = min(bid_px, best_ask - 1)
            virtual_pos = self._add_buy(orders, IPR, bid_px, max_pos - virtual_pos, virtual_pos, max_pos)
        return orders

    def _aco_state(self, data, mid):
        if mid is None:
            return ACO_FV, 0.0, 0.0, 0.0
        fair = float(data.get("aco_kfair", ACO_FV))
        var = float(data.get("aco_var", 28.6))
        innovation = mid - fair
        fair += 0.08 * innovation
        fair = self._clip(fair, ACO_FV - 3.0, ACO_FV + 3.0)
        residual = mid - ACO_FV
        var = 0.96 * var + 0.04 * residual * residual
        std = math.sqrt(max(var, 9.0))
        z = residual / std
        data["aco_kfair"] = round(fair, 4)
        data["aco_var"] = round(var, 4)
        return fair, innovation, residual, z

    def _required_buy_edge(self, pos, innovation, residual, z):
        req = 1
        if residual > 6 or z > 1.25:
            req += 2
        if innovation > 8:
            req += 1
        if pos > 40:
            req += 2
        elif pos > 20:
            req += 1
        if residual < -8 and z < -1.25:
            req = max(1, req - 2)
        return req

    def _required_sell_edge(self, pos, innovation, residual, z):
        req = 1
        if residual < -6 or z < -1.25:
            req += 2
        if innovation < -8:
            req += 1
        if pos < -40:
            req += 2
        elif pos < -20:
            req += 1
        if residual > 8 and z > 1.25:
            req = max(1, req - 2)
        return req

    def _trade_aco_regime_gate(self, state, data):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = LIMITS[ACO]
        mid = self._mid(od)
        fair, innovation, residual, z = self._aco_state(data, mid)

        buy_req = self._required_buy_edge(pos, innovation, residual, z)
        sell_req = self._required_sell_edge(pos, innovation, residual, z)

        for ask in sorted(od.sell_orders):
            if ask >= ACO_FV:
                break
            edge = ACO_FV - ask
            if edge < buy_req:
                continue
            available = -od.sell_orders[ask]
            qty = available if buy_req <= 2 else min(available, 34)
            virtual_pos = self._add_buy(orders, ACO, ask, qty, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= ACO_FV:
                break
            edge = bid - ACO_FV
            if edge < sell_req:
                continue
            available = od.buy_orders[bid]
            qty = available if sell_req <= 2 else min(available, 34)
            virtual_pos = self._add_sell(orders, ACO, bid, qty, virtual_pos, max_pos)

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is not None and best_ask is not None:
            bid_width = 5
            ask_width = 5
            if residual < -6:
                bid_width = 4
                ask_width = 7
            elif residual > 6:
                bid_width = 7
                ask_width = 4
            if abs(innovation) > 10:
                bid_width += 1
                ask_width += 1
            if pos > 40:
                bid_width += 2
                ask_width = max(3, ask_width - 1)
            elif pos < -40:
                ask_width += 2
                bid_width = max(3, bid_width - 1)

            quote_fair = ACO_FV + self._clip((fair - ACO_FV) * 0.3, -1.0, 1.0)
            inv_skew = round((pos / max_pos) * 3)
            bid_px = min(best_bid + 1, quote_fair - bid_width - inv_skew)
            ask_px = max(best_ask - 1, quote_fair + ask_width - inv_skew)
            buy_size = 72 if pos < -25 else 44 if pos > 35 else 60
            sell_size = 72 if pos > 25 else 44 if pos < -35 else 60
            if bid_px < best_ask:
                virtual_pos = self._add_buy(orders, ACO, bid_px, buy_size, virtual_pos, max_pos)
            if ask_px > best_bid:
                virtual_pos = self._add_sell(orders, ACO, ask_px, sell_size, virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr_carry(state)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco_regime_gate(state, data)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)

