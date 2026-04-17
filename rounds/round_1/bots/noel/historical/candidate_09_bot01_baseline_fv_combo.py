from datamodel import Order, TradingState
import json


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}

IPR_SLOPE = 0.001
IPR_EDGE = 4
IPR_PASSIVE_EDGE = 6
ACO_FV = 10000
ACO_EDGE = 6
ACO_PASSIVE_EDGE = 5


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

    def _trade_ipr(self, state, data):
        od = state.order_depths.get(IPR)
        if od is None:
            return []
        fv = self._ipr_fv(state, od, data)
        if fv is None:
            return []
        orders = []
        pos = state.position.get(IPR, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = 78

        for ask in sorted(od.sell_orders):
            if ask >= fv + 2:
                break
            available = -od.sell_orders[ask]
            virtual_pos = self._add_buy(orders, IPR, ask, available, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= fv + IPR_EDGE or virtual_pos <= 0:
                break
            available = od.buy_orders[bid]
            virtual_pos = self._add_sell(orders, IPR, bid, min(available, virtual_pos), virtual_pos, max_pos)

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is not None and best_ask is not None:
            skew = pos * 0.04
            bid_px = min(best_bid + 1, int(fv - IPR_PASSIVE_EDGE - skew))
            ask_px = max(best_ask - 1, int(fv + IPR_PASSIVE_EDGE - skew))
            if bid_px < best_ask:
                virtual_pos = self._add_buy(orders, IPR, bid_px, 12, virtual_pos, max_pos)
            if ask_px > best_bid and virtual_pos > 25:
                virtual_pos = self._add_sell(orders, IPR, ask_px, 12, virtual_pos, max_pos)
        return orders

    def _trade_aco(self, state):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = 76

        for ask in sorted(od.sell_orders):
            if ask >= ACO_FV - ACO_EDGE:
                break
            available = -od.sell_orders[ask]
            virtual_pos = self._add_buy(orders, ACO, ask, available, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= ACO_FV + ACO_EDGE:
                break
            available = od.buy_orders[bid]
            virtual_pos = self._add_sell(orders, ACO, bid, available, virtual_pos, max_pos)

        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        if best_bid is not None and best_ask is not None:
            skew = pos * 0.08
            bid_px = min(best_bid + 1, int(ACO_FV - ACO_PASSIVE_EDGE - skew))
            ask_px = max(best_ask - 1, int(ACO_FV + ACO_PASSIVE_EDGE - skew))
            if bid_px < best_ask:
                virtual_pos = self._add_buy(orders, ACO, bid_px, 16, virtual_pos, max_pos)
            if ask_px > best_bid:
                virtual_pos = self._add_sell(orders, ACO, ask_px, 16, virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr(state, data)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco(state)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)
