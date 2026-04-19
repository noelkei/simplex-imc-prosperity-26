"""
Round 2 — Simplex v3 (Amin)
==========================================================
IPR: Buy ALL available asks unconditionally (drift +0.001/ts always
     pays back entry cost). Throttle size near limit 80. Passive
     repost at best_bid+1 for priority. Sell only on extreme
     overpricing (bid > FV + 10 AND pos > 68).

ACO: Avellaneda-Stoikov market making with:
     - Weighted microprice (w=0.5, EDA-optimal)
     - Full-book imbalance shift (corr=0.41 from EDA)
     - Reservation price with inventory penalty γ = 0.045
     - Aggressive passive quoting: penny the book (bb+1, ba-1)
     - Inventory-skewed sizes for risk management
     - Taking on clear mispricing (rare but profitable)

MAF: 9 (safe threshold for top-50% bid).
==========================================================
Allowed imports only: datamodel, json, math.
"""
from datamodel import Order, OrderDepth, TradingState
import json
import math


# ─── Product symbols ─────────────────────────────────────────────────
IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMIT = 80

# ─── IPR parameters ──────────────────────────────────────────────────
IPR_DRIFT = 0.001              # exact linear drift from EDA regression
IPR_AGGRESSIVE_LIMIT = 72      # throttle take size above this position
IPR_SELL_EDGE = 10             # sell only if bid > FV + this
IPR_SELL_POS_FLOOR = 68        # sell only if pos > this

# ─── ACO parameters (Avellaneda-Stoikov) ──────────────────────────────
ACO_MICROPRICE_W = 0.5         # microprice blend weight (EDA: 12% MAE gain)
ACO_IMBALANCE_COEFF = 2.0      # full-book imbalance → FV shift (sweep-optimal)
ACO_IMBALANCE_CLIP = 3.0       # max imbalance shift (prevents FV extreme jumps)
ACO_GAMMA = 0.030              # inventory penalty (sweep: lower = more aggressive)
ACO_EMA_ALPHA = 0.08           # slow EMA → mean-reversion lag creates taking signals
ACO_BASE_HALF_SPREAD = 3       # minimum half-spread for passive quotes
ACO_TAKE_EDGE = 0.0            # take anything cheap relative to slow FV (sweep-optimal)

# ─── Market Access Fee ────────────────────────────────────────────────
MAF_BID = 9


class Trader:
    def bid(self):
        return MAF_BID

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        mem = {}
        if state.traderData:
            try:
                mem = json.loads(state.traderData)
            except Exception:
                mem = {}

        result[IPR] = self._trade_ipr(state, mem)
        result[ACO] = self._trade_aco(state, mem)

        return result, conversions, json.dumps(mem, separators=(",", ":"))

    # ════════════════════════════════════════════════════════════════
    # IPR: DRIFT CAPTURE — buy everything, hold forever
    # ════════════════════════════════════════════════════════════════
    def _trade_ipr(self, state: TradingState, mem: dict) -> list:
        od = state.order_depths.get(IPR)
        if od is None:
            return []

        pos = state.position.get(IPR, 0)
        orders = []
        buy_used = 0
        sell_used = 0

        bb = max(od.buy_orders) if od.buy_orders else None
        ba = min(od.sell_orders) if od.sell_orders else None

        # Fair value from drift model
        if "ipr_base" not in mem and bb is not None and ba is not None:
            mid = (bb + ba) / 2.0
            mem["ipr_base"] = mid - IPR_DRIFT * state.timestamp

        base = mem.get("ipr_base")
        if base is not None:
            fv = base + IPR_DRIFT * state.timestamp
        elif bb is not None and ba is not None:
            fv = (bb + ba) / 2.0
        else:
            fv = 12000.0

        mid_est = (bb + ba) / 2.0 if bb is not None and ba is not None else fv

        # ── BUY: Take ALL asks unconditionally ───────────────────────
        # Drift profit >>> any entry cost above FV.
        # At pos >= 72, throttle size to avoid overpaying near limit.
        buy_cap = LIMIT - pos
        if buy_cap > 0 and od.sell_orders:
            for ask_px in sorted(od.sell_orders):
                remaining = buy_cap - buy_used
                if remaining <= 0:
                    break
                ask_vol = -od.sell_orders[ask_px]
                qty = ask_vol
                # Throttle near limit to reduce overpay
                if pos + buy_used >= IPR_AGGRESSIVE_LIMIT:
                    if ask_px >= mid_est:
                        qty = min(qty, 4)
                    else:
                        qty = min(qty, 8)
                qty = min(qty, remaining)
                if qty > 0:
                    orders.append(Order(IPR, ask_px, qty))
                    buy_used += qty

        # ── Passive repost: penny the best bid for fill priority ─────
        remaining_buy = buy_cap - buy_used
        if remaining_buy > 0:
            if bb is not None:
                bid_px = bb + 1
                if ba is not None:
                    bid_px = min(bid_px, ba - 1)
            elif ba is not None:
                bid_px = ba - 2
            else:
                bid_px = int(math.floor(fv))
            # Throttle passive size near limit
            if pos + buy_used >= IPR_AGGRESSIVE_LIMIT:
                remaining_buy = min(remaining_buy, 12)
            orders.append(Order(IPR, bid_px, remaining_buy))

        # ── SELL: only extreme richness above FV ─────────────────────
        sell_cap = LIMIT + pos
        if sell_cap > 0 and pos > IPR_SELL_POS_FLOOR and od.buy_orders:
            for bid_px in sorted(od.buy_orders, reverse=True):
                if sell_cap - sell_used <= 0:
                    break
                if bid_px > fv + IPR_SELL_EDGE:
                    bid_vol = od.buy_orders[bid_px]
                    max_sell = min(8, pos - sell_used - IPR_SELL_POS_FLOOR)
                    qty = min(sell_cap - sell_used, bid_vol, max_sell)
                    if qty > 0:
                        orders.append(Order(IPR, bid_px, -qty))
                        sell_used += qty
                else:
                    break  # bids are sorted descending; stop early

        return orders

    # ════════════════════════════════════════════════════════════════
    # ACO: AVELLANEDA-STOIKOV MARKET MAKING
    # ════════════════════════════════════════════════════════════════
    def _trade_aco(self, state: TradingState, mem: dict) -> list:
        od = state.order_depths.get(ACO)
        if od is None:
            return []

        pos = state.position.get(ACO, 0)
        orders = []
        buy_used = 0
        sell_used = 0

        bb = max(od.buy_orders) if od.buy_orders else None
        ba = min(od.sell_orders) if od.sell_orders else None
        if bb is None and ba is None:
            return orders

        # ── Fair value: weighted microprice + EMA ────────────────────
        raw_mid = (bb + ba) / 2.0 if bb is not None and ba is not None else None
        micro = self._microprice(od, bb, ba)

        if raw_mid is not None and micro is not None:
            fv_obs = raw_mid + ACO_MICROPRICE_W * (micro - raw_mid)
        elif micro is not None:
            fv_obs = micro
        elif raw_mid is not None:
            fv_obs = raw_mid
        else:
            fv_obs = mem.get("aco_fv", 10000.0)

        # EMA smoothing
        prev_fv = mem.get("aco_fv", fv_obs)
        fv = ACO_EMA_ALPHA * fv_obs + (1.0 - ACO_EMA_ALPHA) * prev_fv
        mem["aco_fv"] = fv

        # ── Imbalance shift ──────────────────────────────────────────
        imb = self._full_book_imbalance(od)
        imb_shift = ACO_IMBALANCE_COEFF * imb
        if imb_shift > ACO_IMBALANCE_CLIP:
            imb_shift = ACO_IMBALANCE_CLIP
        elif imb_shift < -ACO_IMBALANCE_CLIP:
            imb_shift = -ACO_IMBALANCE_CLIP

        # ── Reservation price (Avellaneda-Stoikov) ───────────────────
        reservation = fv + imb_shift - pos * ACO_GAMMA

        # ── TAKE: aggressive when clear edge exists ──────────────────
        buy_cap = LIMIT - pos
        sell_cap = LIMIT + pos

        # Inventory-aware edge: easier to take when reducing position
        buy_edge = ACO_TAKE_EDGE - (0.3 if pos < -20 else 0.0)
        sell_edge = ACO_TAKE_EDGE - (0.3 if pos > 20 else 0.0)

        if od.sell_orders and buy_cap > 0:
            for ask_px in sorted(od.sell_orders):
                if buy_cap - buy_used <= 0:
                    break
                edge = reservation - ask_px
                if edge < buy_edge:
                    break
                ask_vol = -od.sell_orders[ask_px]
                qty = min(buy_cap - buy_used, ask_vol, 20)
                if pos + buy_used > 55:
                    qty = min(qty, 10)
                if qty > 0:
                    orders.append(Order(ACO, ask_px, qty))
                    buy_used += qty

        if od.buy_orders and sell_cap > 0:
            for bid_px in sorted(od.buy_orders, reverse=True):
                if sell_cap - sell_used <= 0:
                    break
                edge = bid_px - reservation
                if edge < sell_edge:
                    break
                bid_vol = od.buy_orders[bid_px]
                qty = min(sell_cap - sell_used, bid_vol, 20)
                if pos - sell_used < -55:
                    qty = min(qty, 10)
                if qty > 0:
                    orders.append(Order(ACO, bid_px, -qty))
                    sell_used += qty

        # ── PASSIVE QUOTES: penny the book ───────────────────────────
        # Dynamic half spread: tighter when book is tight, wider at extreme positions
        half_spread = ACO_BASE_HALF_SPREAD
        if abs(pos) > 60:
            half_spread += 1

        bid_px = int(math.floor(reservation - half_spread))
        ask_px = int(math.ceil(reservation + half_spread))

        # Penny inside the book for fill priority
        if bb is not None:
            bid_px = max(bid_px, bb + 1)
        if ba is not None:
            ask_px = min(ask_px, ba - 1)

        # Safety: bid must be below ask
        if bid_px >= ask_px:
            if bb is not None and ba is not None:
                bid_px = bb
                ask_px = ba
            else:
                mid_int = int(round(reservation))
                bid_px = mid_int - 1
                ask_px = mid_int + 1

        # Final safety: don't cross the book
        if ba is not None and bid_px >= ba:
            bid_px = ba - 1
        if bb is not None and ask_px <= bb:
            ask_px = bb + 1

        # ── Inventory-skewed quote sizes ─────────────────────────────
        buy_size = 40
        sell_size = 40

        if pos > 20:
            buy_size = max(10, 40 - pos)
            sell_size = min(70, 40 + pos)
        elif pos < -20:
            buy_size = min(70, 40 - pos)
            sell_size = max(10, 40 + pos)

        # Extreme inventory: heavily skew to unwind
        if pos > 55:
            buy_size = 5
            sell_size = 70
        elif pos < -55:
            buy_size = 70
            sell_size = 5

        remaining_buy = buy_cap - buy_used
        remaining_sell = sell_cap - sell_used

        if remaining_buy > 0:
            q = min(remaining_buy, buy_size)
            if q > 0 and (ba is None or bid_px < ba):
                orders.append(Order(ACO, bid_px, q))

        if remaining_sell > 0:
            q = min(remaining_sell, sell_size)
            if q > 0 and (bb is None or ask_px > bb):
                orders.append(Order(ACO, ask_px, -q))

        return orders

    # ── Helpers ──────────────────────────────────────────────────────

    def _microprice(self, od: OrderDepth, bb, ba) -> float:
        """Volume-weighted microprice (L1)."""
        if bb is None or ba is None:
            return None
        bv = od.buy_orders.get(bb, 0)
        av = -od.sell_orders.get(ba, 0)
        total = bv + av
        if total <= 0:
            return (bb + ba) / 2.0
        return (bb * av + ba * bv) / total

    def _full_book_imbalance(self, od: OrderDepth) -> float:
        """Full-book volume imbalance [-1, +1]. Positive = buy pressure."""
        total_bid = sum(od.buy_orders.values()) if od.buy_orders else 0
        total_ask = sum(-v for v in od.sell_orders.values()) if od.sell_orders else 0
        total = total_bid + total_ask
        if total <= 0:
            return 0.0
        return (total_bid - total_ask) / total
