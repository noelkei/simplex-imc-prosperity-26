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

    def _ipr_fv(self, state, od, data):
        day_start = data.get("ipr_day_start")
        mid = self._mid(od)
        if day_start is None and mid is not None:
            day_start = mid - IPR_SLOPE * state.timestamp
            data["ipr_day_start"] = day_start
        if day_start is None:
            return None
        return day_start + IPR_SLOPE * state.timestamp

    def _fv(self, product, state, od, data):
        if product == IPR:
            return self._ipr_fv(state, od, data)
        return ACO_FV

    def _trade_product(self, product, state, data):
        od = state.order_depths.get(product)
        if od is None:
            return []
        fv = self._fv(product, state, od, data)
        if fv is None:
            return []

        orders = []
        pos = state.position.get(product, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = 64
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        imbalance = self._imbalance(od)
        edge_threshold = 1.0 if product == IPR else 2.0
        soft_edge = -1.5 if product == IPR else -2.0
        order_size = 10 if product == IPR else 12

        if best_ask is not None:
            ask_edge = fv - best_ask
            if ask_edge > edge_threshold or (ask_edge > soft_edge and imbalance > 0.45):
                available = -od.sell_orders[best_ask]
                size = min(available, order_size + int(max(0, imbalance) * 10))
                virtual_pos = self._add_buy(orders, product, best_ask, size, virtual_pos, max_pos)

        if best_bid is not None:
            bid_edge = best_bid - fv
            if bid_edge > edge_threshold or (bid_edge > soft_edge and imbalance < -0.45):
                available = od.buy_orders[best_bid]
                size = min(available, order_size + int(max(0, -imbalance) * 10))
                virtual_pos = self._add_sell(orders, product, best_bid, size, virtual_pos, max_pos)

        if best_bid is not None and best_ask is not None and best_ask - best_bid >= 3:
            buy_px = best_bid + 1
            sell_px = best_ask - 1
            if imbalance > 0.20 and buy_px < fv - 0.5:
                virtual_pos = self._add_buy(orders, product, buy_px, 6, virtual_pos, max_pos)
            if imbalance < -0.20 and sell_px > fv + 0.5:
                virtual_pos = self._add_sell(orders, product, sell_px, 6, virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        for product in (IPR, ACO):
            try:
                result[product] = self._trade_product(product, state, data)
            except Exception:
                result[product] = []
        return result, 0, self._save(data)
