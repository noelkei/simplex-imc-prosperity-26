from datamodel import Order, TradingState
import json


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

    def _trade_aco_tight(self, state):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = LIMITS[ACO]

        for ask in sorted(od.sell_orders):
            if ask >= ACO_FV:
                break
            available = -od.sell_orders[ask]
            virtual_pos = self._add_buy(orders, ACO, ask, available, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= ACO_FV:
                break
            available = od.buy_orders[bid]
            virtual_pos = self._add_sell(orders, ACO, bid, available, virtual_pos, max_pos)

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is not None and best_ask is not None:
            skew = round((pos / max_pos) * 3)
            bid_px = min(best_bid + 1, ACO_FV - 5 - skew)
            ask_px = max(best_ask - 1, ACO_FV + 5 - skew)
            if bid_px < best_ask:
                virtual_pos = self._add_buy(orders, ACO, bid_px, max_pos, virtual_pos, max_pos)
            if ask_px > best_bid:
                virtual_pos = self._add_sell(orders, ACO, ask_px, max_pos, virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr_carry(state)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco_tight(state)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)
