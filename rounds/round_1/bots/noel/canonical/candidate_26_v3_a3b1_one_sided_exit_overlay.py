"""
IMC Prosperity 4 - Round 1
candidate_26_v3_a3b1_one_sided_exit_overlay (teammate Noel, ~10,090 P&L)

Key innovations over candidate_03 (Bruno's v5):
  1. Order book imbalance signal: micro_shift = clip(2 * imb, -2, 2)
     Shifts fair value by ±2 based on L1 bid vs ask volume ratio.
  2. Centered skew (safe with HS=5): ask = FV + 5 - inv_skew
     When long: lower ask → encourage selling. When short: higher bid → encourage buying.
     Safety: HS=5 > max_skew=3 → ask always ≥ FV+2, never below FV.
  3. One-sided book handling: special logic when only bids or only asks visible.
  4. Position-dependent aggressive take filter: if |pos| > 40 and edge < 3, skip small takes.
  5. Large asymmetric quote sizes (60-72) capped by capacity.
  6. Virtual position tracking with _add_buy/_add_sell helpers (cleaner capacity management).

Parameters: a=3 (skew factor), b=1 (possibly best_bid+1 step or second param TBD).
"""
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

    def _clip(self, value, lo, hi):
        return min(max(value, lo), hi)

    def _imbalance(self, od):
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

    def _trade_aco_one_sided(self, state):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = LIMITS[ACO]
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)

        if best_bid is not None and best_ask is None:
            visible = od.buy_orders[best_bid]
            if pos > 0 and best_bid >= ACO_FV - 2:
                virtual_pos = self._add_sell(orders, ACO, best_bid, min(visible, max(12, pos)), virtual_pos, max_pos)
            elif best_bid > ACO_FV + 5 and pos > -35:
                virtual_pos = self._add_sell(orders, ACO, best_bid, min(visible, 18), virtual_pos, max_pos)
            ask_px = max(best_bid + 1, ACO_FV + 5 - round((pos / max_pos) * 3))
            ask_size = 42 if pos > 20 else 18
            virtual_pos = self._add_sell(orders, ACO, ask_px, ask_size, virtual_pos, max_pos)
            return orders

        if best_ask is not None and best_bid is None:
            visible = -od.sell_orders[best_ask]
            if pos < 0 and best_ask <= ACO_FV + 2:
                virtual_pos = self._add_buy(orders, ACO, best_ask, min(visible, max(12, -pos)), virtual_pos, max_pos)
            elif best_ask < ACO_FV - 5 and pos < 35:
                virtual_pos = self._add_buy(orders, ACO, best_ask, min(visible, 18), virtual_pos, max_pos)
            bid_px = min(best_ask - 1, ACO_FV - 5 - round((pos / max_pos) * 3))
            bid_size = 42 if pos < -20 else 18
            virtual_pos = self._add_buy(orders, ACO, bid_px, bid_size, virtual_pos, max_pos)
            return orders

        for ask in sorted(od.sell_orders):
            if ask >= ACO_FV:
                break
            available = -od.sell_orders[ask]
            edge = ACO_FV - ask
            if pos > 40 and edge < 3:
                continue
            virtual_pos = self._add_buy(orders, ACO, ask, available, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid <= ACO_FV:
                break
            available = od.buy_orders[bid]
            edge = bid - ACO_FV
            if pos < -40 and edge < 3:
                continue
            virtual_pos = self._add_sell(orders, ACO, bid, available, virtual_pos, max_pos)

        if best_bid is not None and best_ask is not None:
            imb = self._imbalance(od)
            micro_shift = self._clip(2.0 * imb, -2.0, 2.0)
            inv_skew = round((pos / max_pos) * 3)
            quote_fair = ACO_FV + micro_shift
            bid_px = min(best_bid + 1, quote_fair - 5 - inv_skew)
            ask_px = max(best_ask - 1, quote_fair + 5 - inv_skew)
            buy_size = 72 if pos < -30 else 40 if pos > 35 else 60
            sell_size = 72 if pos > 30 else 40 if pos < -35 else 60
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
            result[ACO] = self._trade_aco_one_sided(state)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)
