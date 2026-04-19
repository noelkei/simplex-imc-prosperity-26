"""Round 2 Generation 2 Bruno candidate.
Spec: rounds/round_2/workspace/04_strategy_specs/spec_r2_gen2_bruno_battery.md
Uploadable standalone Trader file. Uses only datamodel/json.
"""
from datamodel import Order, TradingState
import json


IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMITS = {IPR: 80, ACO: 80}
CONFIG = {'bot_id': 'R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD', 'role': 'aco_imbalance_wide_spread', 'modes': ['aco_imbalance'], 'maf_bid': 0, 'inventory_soft': 40, 'ipr_clip': 6, 'ipr_extreme_threshold': 2.0, 'ipr_threshold': 1.0, 'ipr_slope_alpha': 0.05, 'ipr_warmup': 20, 'ipr_max_spread': 3, 'aco_clip': 6, 'aco_probe_clip': 3, 'aco_quote_clip': 8, 'aco_max_spread': 21, 'aco_full_spread': 16, 'aco_mid_spread': 18, 'aco_mid_mult': 0.65, 'aco_wide_mult': 0.35, 'aco_quote_offset': 5, 'aco_half_spread': 5, 'aco_inventory_skew': 3, 'aco_aggression': 0.58, 'aco_probe_take_edge': 5.0, 'imbalance_threshold': 0.12}


class Trader:
    def bid(self):
        return int(CONFIG.get("maf_bid", 0))

    def _load(self, trader_data):
        if not trader_data:
            return {}
        try:
            loaded = json.loads(trader_data)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            return {}

    def _dump(self, memory):
        memory["bot"] = CONFIG["bot_id"]
        try:
            return json.dumps(memory, separators=(",", ":"), sort_keys=True)[:48000]
        except Exception:
            return json.dumps({"bot": CONFIG["bot_id"]}, separators=(",", ":"))

    def _position(self, state, product):
        return int((getattr(state, "position", {}) or {}).get(product, 0))

    def _best_bid(self, depth):
        buys = getattr(depth, "buy_orders", {}) or {}
        return max(buys) if buys else None

    def _best_ask(self, depth):
        sells = getattr(depth, "sell_orders", {}) or {}
        return min(sells) if sells else None

    def _clip(self, value, lo, hi):
        return min(max(value, lo), hi)

    def _book(self, state, product, allow_one_sided=False):
        depth = (getattr(state, "order_depths", {}) or {}).get(product)
        if depth is None:
            return None
        buys = getattr(depth, "buy_orders", {}) or {}
        sells = getattr(depth, "sell_orders", {}) or {}
        best_bid = max(buys) if buys else None
        best_ask = min(sells) if sells else None
        if best_bid is None and best_ask is None:
            return None
        if not allow_one_sided and (best_bid is None or best_ask is None):
            return None
        bid_vol = max(0, int(buys.get(best_bid, 0))) if best_bid is not None else 0
        ask_vol = abs(int(sells.get(best_ask, 0))) if best_ask is not None else 0
        total_bid = sum(max(0, int(v)) for v in buys.values())
        total_ask = sum(abs(int(v)) for v in sells.values())
        if best_bid is not None and best_ask is not None:
            mid = (best_bid + best_ask) / 2.0
            spread = int(best_ask - best_bid)
        elif best_bid is not None:
            mid = float(best_bid + CONFIG.get("aco_half_spread", 8))
            spread = None
        else:
            mid = float(best_ask - CONFIG.get("aco_half_spread", 8))
            spread = None
        return {
            "depth": depth,
            "buys": buys,
            "sells": sells,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "bid_vol": bid_vol,
            "ask_vol": ask_vol,
            "total_bid": int(total_bid),
            "total_ask": int(total_ask),
            "mid": mid,
            "spread": spread,
        }

    def _capacities(self, state):
        caps = {}
        for product, limit in LIMITS.items():
            pos = self._position(state, product)
            caps[product] = {"buy": max(0, limit - pos), "sell": max(0, limit + pos)}
        return caps

    def _add_order(self, orders, caps, product, price, qty):
        if qty == 0 or price is None:
            return
        price = int(round(price))
        if qty > 0:
            allowed = min(int(qty), caps[product]["buy"])
            if allowed > 0:
                orders.setdefault(product, []).append(Order(product, price, allowed))
                caps[product]["buy"] -= allowed
            return
        allowed = min(int(-qty), caps[product]["sell"])
        if allowed > 0:
            orders.setdefault(product, []).append(Order(product, price, -allowed))
            caps[product]["sell"] -= allowed

    def _spread_mult(self, product, spread):
        if spread is None:
            return 1.0
        if product == IPR:
            if CONFIG.get("ipr_continuous_spread", False):
                if spread <= CONFIG.get("ipr_full_spread", 4):
                    return 1.0
                if spread <= CONFIG.get("ipr_mid_spread", 14):
                    return float(CONFIG.get("ipr_mid_mult", 0.5))
                if spread <= CONFIG.get("ipr_max_spread", 18):
                    return float(CONFIG.get("ipr_wide_mult", 0.25))
                return 0.0
            return 1.0 if spread <= CONFIG.get("ipr_max_spread", 4) else 0.0
        if CONFIG.get("aco_continuous_spread", True):
            if spread <= CONFIG.get("aco_full_spread", 16):
                return 1.0
            if spread <= CONFIG.get("aco_mid_spread", 18):
                return float(CONFIG.get("aco_mid_mult", 0.65))
            if spread <= CONFIG.get("aco_max_spread", 21):
                return float(CONFIG.get("aco_wide_mult", 0.35))
            return 0.0
        return 1.0 if spread <= CONFIG.get("aco_max_spread", 21) else 0.0

    def _inventory_clip(self, base_clip, position, side, soft):
        if side > 0 and position > soft:
            return max(1, base_clip // 2)
        if side < 0 and position < -soft:
            return max(1, base_clip // 2)
        return base_clip

    def _top_imbalance(self, book):
        total = book["bid_vol"] + book["ask_vol"]
        if total <= 0:
            return 0.0
        return (book["bid_vol"] - book["ask_vol"]) / total

    def _full_imbalance(self, book):
        total = book["total_bid"] + book["total_ask"]
        if total <= 0:
            return 0.0
        return (book["total_bid"] - book["total_ask"]) / total

    def _smooth_aco_fair(self, memory, mid):
        fair = float(memory.get("aco_fair", mid))
        alpha = float(CONFIG.get("aco_fair_alpha", 0.05))
        fair = fair + alpha * (float(mid) - fair)
        memory["aco_fair"] = fair
        return fair

    def _trade_ipr(self, state, memory, orders, caps, extreme=False, flatten=False, spread_retune=False):
        book = self._book(state, IPR)
        if book is None:
            return
        ts = int(getattr(state, "timestamp", 0) or 0)
        last_mid = memory.get("ipr_last_mid")
        last_ts = memory.get("ipr_last_ts")
        slope = float(memory.get("ipr_slope", 0.0))
        count = int(memory.get("ipr_count", 0))
        fair = book["mid"]
        if last_mid is not None and last_ts is not None:
            dt = max(1, ts - int(last_ts))
            fair = float(last_mid) + slope * dt
            observed_slope = (book["mid"] - float(last_mid)) / dt
            alpha = float(CONFIG.get("ipr_slope_alpha", 0.05))
            slope = observed_slope if count <= 1 else slope + alpha * (observed_slope - slope)
        count += 1
        memory["ipr_last_mid"] = book["mid"]
        memory["ipr_last_ts"] = ts
        memory["ipr_slope"] = slope
        memory["ipr_count"] = count
        if count < int(CONFIG.get("ipr_warmup", 20)):
            return

        spread_mult = self._spread_mult(IPR, book["spread"])
        if spread_retune:
            spread_penalty = max(0.0, float(book["spread"] or 0) - CONFIG.get("ipr_full_spread", 4)) * float(CONFIG.get("ipr_spread_penalty", 0.08))
        else:
            spread_penalty = 0.0
        threshold_key = "ipr_extreme_threshold" if extreme else "ipr_threshold"
        threshold = float(CONFIG.get(threshold_key, 1.0)) + spread_penalty
        pos = self._position(state, IPR)
        clip = int(CONFIG.get("ipr_clip", 8) * spread_mult)
        if clip > 0:
            buy_edge = fair - book["best_ask"]
            sell_edge = book["best_bid"] - fair
            if buy_edge >= threshold:
                qty = min(book["ask_vol"], self._inventory_clip(clip, pos, 1, int(CONFIG.get("inventory_soft", 40))))
                self._add_order(orders, caps, IPR, book["best_ask"], qty)
            if sell_edge >= threshold:
                qty = min(book["bid_vol"], self._inventory_clip(clip, pos, -1, int(CONFIG.get("inventory_soft", 40))))
                self._add_order(orders, caps, IPR, book["best_bid"], -qty)

        if flatten:
            soft = int(CONFIG.get("flatten_soft", 18))
            qty = int(CONFIG.get("flatten_clip", 4))
            if pos > soft and book["best_bid"] is not None:
                self._add_order(orders, caps, IPR, book["best_bid"], -min(qty, pos - soft))
            elif pos < -soft and book["best_ask"] is not None:
                self._add_order(orders, caps, IPR, book["best_ask"], min(qty, -soft - pos))

    def _quote_inside(self, orders, caps, product, book, fair, base_clip, offset, inventory_skew=0):
        if book["best_bid"] is None or book["best_ask"] is None:
            return
        if book["best_ask"] - book["best_bid"] <= 1:
            return
        bid_px = int(round(fair - offset - inventory_skew))
        ask_px = int(round(fair + offset - inventory_skew))
        bid_px = min(book["best_ask"] - 1, max(book["best_bid"] + 1, bid_px))
        ask_px = max(book["best_bid"] + 1, min(book["best_ask"] - 1, ask_px))
        if bid_px < ask_px:
            self._add_order(orders, caps, product, bid_px, base_clip)
            self._add_order(orders, caps, product, ask_px, -base_clip)

    def _trade_aco_activation(self, state, memory, orders, caps):
        book = self._book(state, ACO)
        if book is None:
            return
        mult = self._spread_mult(ACO, book["spread"])
        clip = max(1, int(CONFIG.get("aco_probe_clip", 3) * mult))
        if clip <= 0:
            return
        fair = self._smooth_aco_fair(memory, book["mid"])
        pos = self._position(state, ACO)
        take_edge = float(CONFIG.get("aco_probe_take_edge", 5.0))
        if book["best_ask"] <= fair - take_edge:
            self._add_order(orders, caps, ACO, book["best_ask"], min(book["ask_vol"], clip))
        if book["best_bid"] >= fair + take_edge:
            self._add_order(orders, caps, ACO, book["best_bid"], -min(book["bid_vol"], clip))
        inv_skew = round((pos / LIMITS[ACO]) * CONFIG.get("aco_inventory_skew", 3))
        self._quote_inside(orders, caps, ACO, book, fair, clip, CONFIG.get("aco_quote_offset", 5), inv_skew)

    def _trade_aco_imbalance(self, state, memory, orders, caps):
        book = self._book(state, ACO)
        if book is None:
            return
        mult = self._spread_mult(ACO, book["spread"])
        clip = max(1, int(CONFIG.get("aco_clip", 5) * mult))
        if clip <= 0:
            return
        signal = self._top_imbalance(book)
        threshold = float(CONFIG.get("imbalance_threshold", 0.12))
        if abs(signal) < threshold:
            if CONFIG.get("aco_probe_fallback", False):
                self._trade_aco_activation(state, memory, orders, caps)
            return
        spread = max(1, int(book["spread"] or 1))
        step = max(1, int(round(spread * float(CONFIG.get("aco_aggression", 0.55)))))
        pos = self._position(state, ACO)
        qty = self._inventory_clip(clip, pos, 1 if signal > 0 else -1, int(CONFIG.get("inventory_soft", 40)))
        if signal > threshold:
            price = min(book["best_ask"] - 1, book["best_bid"] + step)
            self._add_order(orders, caps, ACO, price, qty)
        elif signal < -threshold:
            price = max(book["best_bid"] + 1, book["best_ask"] - step)
            self._add_order(orders, caps, ACO, price, -qty)

    def _trade_aco_reversal(self, state, memory, orders, caps):
        book = self._book(state, ACO)
        if book is None:
            return
        last_mid = memory.get("aco_last_mid")
        memory["aco_last_mid"] = book["mid"]
        if last_mid is None:
            if CONFIG.get("aco_probe_fallback", False):
                self._trade_aco_activation(state, memory, orders, caps)
            return
        delta = book["mid"] - float(last_mid)
        signal = -delta
        threshold = float(CONFIG.get("aco_reversal_threshold", 0.5))
        if abs(signal) < threshold:
            return
        mult = self._spread_mult(ACO, book["spread"])
        clip = max(1, int(CONFIG.get("aco_clip", 5) * mult))
        spread = max(1, int(book["spread"] or 1))
        step = max(1, int(round(spread * float(CONFIG.get("aco_aggression", 0.55)))))
        pos = self._position(state, ACO)
        qty = self._inventory_clip(clip, pos, 1 if signal > 0 else -1, int(CONFIG.get("inventory_soft", 40)))
        if signal > 0:
            self._add_order(orders, caps, ACO, min(book["best_ask"] - 1, book["best_bid"] + step), qty)
        else:
            self._add_order(orders, caps, ACO, max(book["best_bid"] + 1, book["best_ask"] - step), -qty)

    def _kf_update(self, memory, mid):
        fv = float(memory.get("aco_kf_fv", CONFIG.get("aco_kf_fv0", 10000.0)))
        p_var = float(memory.get("aco_kf_p", CONFIG.get("aco_kf_p0", 25.0)))
        q_var = float(CONFIG.get("aco_kf_q", 0.005))
        r_var = float(CONFIG.get("aco_kf_r", 25.0))
        pred = p_var + q_var
        gain = pred / (pred + r_var)
        fv = fv + gain * (mid - fv)
        p_var = (1.0 - gain) * pred
        memory["aco_kf_fv"] = fv
        memory["aco_kf_p"] = p_var
        return fv

    def _trade_aco_kalman(self, state, memory, orders, caps):
        book = self._book(state, ACO, allow_one_sided=True)
        if book is None:
            return
        fv = self._kf_update(memory, book["mid"])
        pos = self._position(state, ACO)
        clip = int(CONFIG.get("aco_clip", 10))
        half = int(CONFIG.get("aco_half_spread", 5))
        skew = round((pos / LIMITS[ACO]) * CONFIG.get("aco_inventory_skew", 3))
        if book["best_ask"] is not None and book["best_ask"] < fv - CONFIG.get("aco_take_edge", 1):
            self._add_order(orders, caps, ACO, book["best_ask"], min(abs(book["ask_vol"]), clip))
        if book["best_bid"] is not None and book["best_bid"] > fv + CONFIG.get("aco_take_edge", 1):
            self._add_order(orders, caps, ACO, book["best_bid"], -min(book["bid_vol"], clip))
        if book["best_bid"] is not None and book["best_ask"] is not None:
            self._quote_inside(orders, caps, ACO, book, fv, int(CONFIG.get("aco_quote_clip", 12)), half, skew)
        elif book["best_bid"] is not None:
            self._add_order(orders, caps, ACO, max(book["best_bid"] + 1, round(fv + half - skew)), -int(CONFIG.get("aco_quote_clip", 8)))
        elif book["best_ask"] is not None:
            self._add_order(orders, caps, ACO, min(book["best_ask"] - 1, round(fv - half - skew)), int(CONFIG.get("aco_quote_clip", 8)))

    def _trade_aco_noel_c26(self, state, memory, orders, caps):
        book = self._book(state, ACO, allow_one_sided=True)
        if book is None:
            return
        fv = float(CONFIG.get("aco_fixed_fv", 10000.0))
        pos = self._position(state, ACO)
        max_pos = LIMITS[ACO]
        half = int(CONFIG.get("aco_half_spread", 5))
        skew = round((pos / max_pos) * CONFIG.get("aco_inventory_skew", 3))
        if book["best_bid"] is not None and book["best_ask"] is None:
            if pos > 0 and book["best_bid"] >= fv - 2:
                self._add_order(orders, caps, ACO, book["best_bid"], -min(book["bid_vol"], max(8, pos)))
            ask_px = max(book["best_bid"] + 1, fv + half - skew)
            self._add_order(orders, caps, ACO, ask_px, -int(CONFIG.get("aco_quote_clip", 12)))
            return
        if book["best_ask"] is not None and book["best_bid"] is None:
            if pos < 0 and book["best_ask"] <= fv + 2:
                self._add_order(orders, caps, ACO, book["best_ask"], min(book["ask_vol"], max(8, -pos)))
            bid_px = min(book["best_ask"] - 1, fv - half - skew)
            self._add_order(orders, caps, ACO, bid_px, int(CONFIG.get("aco_quote_clip", 12)))
            return
        if book["best_ask"] < fv - CONFIG.get("aco_take_edge", 1):
            self._add_order(orders, caps, ACO, book["best_ask"], min(book["ask_vol"], int(CONFIG.get("aco_clip", 8))))
        if book["best_bid"] > fv + CONFIG.get("aco_take_edge", 1):
            self._add_order(orders, caps, ACO, book["best_bid"], -min(book["bid_vol"], int(CONFIG.get("aco_clip", 8))))
        imb_shift = self._clip(2.0 * self._top_imbalance(book), -2.0, 2.0)
        self._quote_inside(orders, caps, ACO, book, fv + imb_shift, int(CONFIG.get("aco_quote_clip", 12)), half, skew)

    def run(self, state: TradingState):
        memory = self._load(getattr(state, "traderData", ""))
        orders = {}
        caps = self._capacities(state)
        modes = CONFIG.get("modes", [])
        for mode in modes:
            try:
                if mode == "ipr_extreme":
                    self._trade_ipr(state, memory, orders, caps, extreme=True)
                elif mode == "ipr_drift":
                    self._trade_ipr(state, memory, orders, caps, extreme=False)
                elif mode == "ipr_extreme_flatten":
                    self._trade_ipr(state, memory, orders, caps, extreme=True, flatten=True)
                elif mode == "ipr_spread_retune":
                    self._trade_ipr(state, memory, orders, caps, extreme=True, spread_retune=True)
                elif mode == "aco_activation":
                    self._trade_aco_activation(state, memory, orders, caps)
                elif mode == "aco_imbalance":
                    self._trade_aco_imbalance(state, memory, orders, caps)
                elif mode == "aco_reversal":
                    self._trade_aco_reversal(state, memory, orders, caps)
                elif mode == "aco_kalman_r1":
                    self._trade_aco_kalman(state, memory, orders, caps)
                elif mode == "aco_noel_c26":
                    self._trade_aco_noel_c26(state, memory, orders, caps)
            except Exception:
                memory["last_error_mode"] = mode
        result = {}
        active_ipr = any(mode.startswith("ipr_") for mode in modes)
        active_aco = any(mode.startswith("aco_") for mode in modes)
        if active_ipr or IPR in orders:
            result[IPR] = orders.get(IPR, [])
        if active_aco or ACO in orders:
            result[ACO] = orders.get(ACO, [])
        return result, 0, self._dump(memory)
