from datamodel import Order, TradingState
import json


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}
ACO_FV = 10000
MODE = "table"


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

    def _clip(self, value, lo, hi):
        return max(lo, min(hi, value))

    def _reset_caps(self, start_pos):
        self._start_pos = start_pos
        self._buy_used = 0
        self._sell_used = 0

    def _add_buy(self, orders, product, price, qty, virtual_pos, max_pos):
        cap = max_pos - self._start_pos - self._buy_used
        order_qty = min(max(int(qty), 0), cap)
        if order_qty > 0:
            orders.append(Order(product, int(round(price)), order_qty))
            self._buy_used += order_qty
            virtual_pos += order_qty
        return virtual_pos

    def _add_sell(self, orders, product, price, qty, virtual_pos, max_pos):
        cap = max_pos + self._start_pos - self._sell_used
        order_qty = min(max(int(qty), 0), cap)
        if order_qty > 0:
            orders.append(Order(product, int(round(price)), -order_qty))
            self._sell_used += order_qty
            virtual_pos -= order_qty
        return virtual_pos

    def _trade_ipr_carry(self, state, data):
        od = state.order_depths.get(IPR)
        if od is None:
            return []
        orders = []
        pos = state.position.get(IPR, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        max_pos = LIMITS[IPR]
        guarded = MODE == "ipr_exec"
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        mid = self._mid(od)

        if guarded and mid is not None:
            anchor = data.get("ipr_anchor")
            if anchor is None:
                data["ipr_anchor"] = mid - 0.001 * state.timestamp
            expected = data.get("ipr_anchor", mid) + 0.001 * state.timestamp
            if state.timestamp > 2000 and mid < expected - 18:
                max_pos = 70

        for ask in sorted(od.sell_orders):
            if virtual_pos >= max_pos:
                break
            virtual_pos = self._add_buy(orders, IPR, ask, -od.sell_orders[ask], virtual_pos, max_pos)

        if virtual_pos < max_pos and best_bid is not None:
            bid_px = best_bid + 1
            if best_ask is not None:
                bid_px = min(bid_px, best_ask - 1)
            if guarded and state.timestamp < 500 and best_ask is not None:
                bid_px = best_ask
            virtual_pos = self._add_buy(orders, IPR, bid_px, max_pos - virtual_pos, virtual_pos, max_pos)
        return orders

    def _kalman_fair(self, data, mid):
        mean = data.get("aco_k_mean", ACO_FV)
        var = data.get("aco_k_var", 25.0)
        q = 0.08 if MODE == "kalman" else 0.04
        r = 28.0
        if mid is not None:
            var += q
            gain = var / (var + r)
            mean = mean + gain * (mid - mean)
            var = (1 - gain) * var
        data["aco_k_mean"] = mean
        data["aco_k_var"] = var
        return 0.75 * ACO_FV + 0.25 * mean, abs((mid if mid is not None else mean) - mean)

    def _hmm_probs(self, data, residual):
        probs = data.get("aco_hmm", [0.25, 0.50, 0.25])
        trans = ((0.72, 0.23, 0.05), (0.16, 0.68, 0.16), (0.05, 0.23, 0.72))
        pred = [sum(probs[j] * trans[j][i] for j in range(3)) for i in range(3)]
        if residual < -7:
            emit = [0.74, 0.23, 0.03]
        elif residual > 7:
            emit = [0.03, 0.23, 0.74]
        elif residual < -3:
            emit = [0.48, 0.42, 0.10]
        elif residual > 3:
            emit = [0.10, 0.42, 0.48]
        else:
            emit = [0.12, 0.76, 0.12]
        post = [pred[i] * emit[i] for i in range(3)]
        total = sum(post) or 1.0
        post = [x / total for x in post]
        data["aco_hmm"] = post
        return post

    def _base_plan(self, state, data, od, pos):
        mid = self._mid(od)
        residual = (mid - ACO_FV) if mid is not None else 0.0
        spread = self._spread(od)
        imb = self._imbalance(od)
        fair = ACO_FV
        width = 5
        buy_cross = ACO_FV - 1
        sell_cross = ACO_FV + 1
        size = LIMITS[ACO]
        max_pos = LIMITS[ACO]
        passive_buy = True
        passive_sell = True
        flatten = False
        skew_extra = 0.0

        if MODE == "kalman":
            fair, innovation = self._kalman_fair(data, mid)
            width = 5 if innovation < 8 else 8
            buy_cross = fair - (4 if innovation < 10 else 7)
            sell_cross = fair + (4 if innovation < 10 else 7)
            skew_extra = self._clip((fair - ACO_FV) * 0.25, -2, 2)
        elif MODE == "hmm":
            under, neutral, over = self._hmm_probs(data, residual)
            state_bias = under - over
            fair = ACO_FV + 2.0 * state_bias
            width = 4 if max(under, over) > 0.58 else 7
            buy_cross = ACO_FV - (3 if under > 0.50 else 7)
            sell_cross = ACO_FV + (3 if over > 0.50 else 7)
            skew_extra = -3.0 * state_bias
        elif MODE == "edge":
            req = 6 + abs(pos) // 24
            if spread is not None and spread < 11:
                req += 2
            if state.timestamp > 80000:
                req += 1
            width = req
            buy_cross = ACO_FV - req
            sell_cross = ACO_FV + req
            size = 34
        elif MODE == "lifecycle":
            target = 45 if state.timestamp < 40000 else 25 if state.timestamp < 80000 else 0
            width = 5 if state.timestamp < 80000 else 3
            buy_cross = ACO_FV - 4
            sell_cross = ACO_FV + 4
            skew_extra = (pos - target) * 0.10
            if state.timestamp >= 80000:
                flatten = True
                passive_buy = pos < 0
                passive_sell = pos > 0
        elif MODE == "table":
            inv_bucket = 1 if pos > 45 else -1 if pos < -45 else 0
            if inv_bucket > 0:
                buy_cross = ACO_FV - 10
                sell_cross = ACO_FV + 2
                passive_buy = False
            elif inv_bucket < 0:
                buy_cross = ACO_FV - 2
                sell_cross = ACO_FV + 10
                passive_sell = False
            elif residual < -8:
                buy_cross = ACO_FV - 3
                sell_cross = ACO_FV + 8
            elif residual > 8:
                buy_cross = ACO_FV - 8
                sell_cross = ACO_FV + 3
            else:
                buy_cross = ACO_FV - 6
                sell_cross = ACO_FV + 6
            width = 6
            size = 42
        elif MODE == "scheduler":
            width = 8
            buy_cross = ACO_FV - 8
            sell_cross = ACO_FV + 8
            size = 24
            if abs(pos) > 45:
                width = 4
                passive_buy = pos < 0
                passive_sell = pos > 0
        elif MODE == "one_sided":
            width = 6
            buy_cross = ACO_FV - 5
            sell_cross = ACO_FV + 5
            size = 30
        elif MODE == "micro":
            liq_penalty = 1 if spread is not None and spread > 18 else 0
            fair = ACO_FV + self._clip(3.0 * imb, -3, 3)
            width = 5 + liq_penalty
            buy_cross = fair - 5
            sell_cross = fair + 5
            skew_extra = -2.0 * imb
            size = 36
        elif MODE == "adaptive":
            kfair, innovation = self._kalman_fair(data, mid)
            under, neutral, over = self._hmm_probs(data, residual)
            confidence = max(under, over) - neutral * 0.25
            width = 5 if innovation < 9 and confidence > 0.35 else 8
            fair = 0.85 * ACO_FV + 0.15 * kfair
            buy_cross = ACO_FV - (5 if under > 0.45 and innovation < 12 else 8)
            sell_cross = ACO_FV + (5 if over > 0.45 and innovation < 12 else 8)
            if state.timestamp > 82000 or abs(pos) > 55:
                passive_buy = pos < 10
                passive_sell = pos > -10
                width = min(width, 5)
            size = 32
        else:
            width = 5
            buy_cross = ACO_FV - 1
            sell_cross = ACO_FV + 1

        return {
            "fair": fair,
            "width": width,
            "buy_cross": buy_cross,
            "sell_cross": sell_cross,
            "size": size,
            "max_pos": max_pos,
            "passive_buy": passive_buy,
            "passive_sell": passive_sell,
            "flatten": flatten,
            "skew_extra": skew_extra,
        }

    def _trade_aco(self, state, data):
        od = state.order_depths.get(ACO)
        if od is None:
            return []
        orders = []
        pos = state.position.get(ACO, 0)
        self._reset_caps(pos)
        virtual_pos = pos
        best_bid = self._best_bid(od)
        best_ask = self._best_ask(od)
        plan = self._base_plan(state, data, od, pos)
        max_pos = plan["max_pos"]

        if MODE == "one_sided" and (best_bid is None or best_ask is None):
            if best_ask is not None and (pos < 0 or best_ask <= ACO_FV - 5):
                virtual_pos = self._add_buy(orders, ACO, best_ask, min(28, abs(pos) if pos < 0 else 18), virtual_pos, max_pos)
            if best_bid is not None and (pos > 0 or best_bid >= ACO_FV + 5):
                virtual_pos = self._add_sell(orders, ACO, best_bid, min(28, pos if pos > 0 else 18), virtual_pos, max_pos)
            if best_bid is not None and best_ask is None and pos <= 35:
                virtual_pos = self._add_sell(orders, ACO, ACO_FV + 6, 18, virtual_pos, max_pos)
            if best_ask is not None and best_bid is None and pos >= -35:
                virtual_pos = self._add_buy(orders, ACO, ACO_FV - 6, 18, virtual_pos, max_pos)
            return orders

        for ask in sorted(od.sell_orders):
            if ask > plan["buy_cross"]:
                break
            available = -od.sell_orders[ask]
            qty = min(available, plan["size"])
            if plan["flatten"] and pos >= 0:
                continue
            virtual_pos = self._add_buy(orders, ACO, ask, qty, virtual_pos, max_pos)

        for bid in sorted(od.buy_orders, reverse=True):
            if bid < plan["sell_cross"]:
                break
            available = od.buy_orders[bid]
            qty = min(available, plan["size"])
            if plan["flatten"] and pos <= 0:
                continue
            virtual_pos = self._add_sell(orders, ACO, bid, qty, virtual_pos, max_pos)

        if best_bid is not None and best_ask is not None:
            skew = round((pos / LIMITS[ACO]) * 3 + plan["skew_extra"])
            bid_px = min(best_bid + 1, plan["fair"] - plan["width"] - skew)
            ask_px = max(best_ask - 1, plan["fair"] + plan["width"] - skew)
            if plan["passive_buy"] and bid_px < best_ask:
                virtual_pos = self._add_buy(orders, ACO, bid_px, plan["size"], virtual_pos, max_pos)
            if plan["passive_sell"] and ask_px > best_bid:
                virtual_pos = self._add_sell(orders, ACO, ask_px, plan["size"], virtual_pos, max_pos)
        return orders

    def run(self, state: TradingState):
        data = self._load(state.traderData)
        result = {}
        try:
            result[IPR] = self._trade_ipr_carry(state, data)
        except Exception:
            result[IPR] = []
        try:
            result[ACO] = self._trade_aco(state, data)
        except Exception:
            result[ACO] = []
        return result, 0, self._save(data)
