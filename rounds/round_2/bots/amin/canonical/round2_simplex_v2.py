"""
Round 2 — Simplex v2 (Amin)
==========================================================
IPR: Linear-drift capture with aggressive multi-level fill.
     FV(t) = base + 0.001 * timestamp.
     Buy to limit 80 ASAP. Passive repost at FV to capture any residual mean-reversion.
     Sell only on extreme departures above FV (>12 above).

ACO: Avellaneda-Stoikov inspired market making.
     Fair value via weighted microprice (w=0.5 from EDA).
     Full-book imbalance shifts (corr 0.41 with next-mid from EDA).
     Reservation price with inventory penalty γ = σ² / (2 * limit).
     Aggressive taking when mispriced > dynamic edge.
     Passive quotes at reservation ± half_spread, penned inside book.

MAF: 9 (low bid — median is likely low given many teams bid 0).
==========================================================
Uses only: datamodel, json, math (all allowed on Prosperity).
"""
from datamodel import Order, OrderDepth, TradingState
import json
import math


# ─── Product symbols ─────────────────────────────────────────────────
IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
LIMIT = 80

# ─── IPR parameters ──────────────────────────────────────────────────
IPR_DRIFT = 0.001          # slope from regression (exact across 3 days)
IPR_TAKE_EDGE = 10         # take asks within FV + this (ask is typically FV+7, need >=8)
IPR_PASSIVE_OFFSET = 1     # passive bid at FV - this (improve fill price)
IPR_SELL_THRESHOLD = 12    # only sell if bid > FV + this

# ─── ACO parameters (Avellaneda-Stoikov + microstructure) ─────────── 
ACO_MICROPRICE_W = 0.5     # EDA-optimal blend weight for microprice
ACO_IMBALANCE_COEFF = 3.0  # shift FV by imbalance * this (from EDA: corr~0.41)
ACO_GAMMA = 0.08           # inventory risk aversion (σ²/limit based)
ACO_KAPPA = 1.5            # order arrival rate parameter
ACO_BASE_SPREAD = 4        # minimum half-spread for quotes
ACO_TAKE_EDGE = 1.5        # edge required to take liquidity aggressively
ACO_MAX_POSITION_RATIO = 0.7  # above this fraction of limit, widen quotes

# ─── Market Access Fee ────────────────────────────────────────────────
MAF_BID = 9


class Trader:
    def bid(self):
        return MAF_BID

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # ── Load state ───────────────────────────────────────────────
        mem = {}
        if state.traderData:
            try:
                mem = json.loads(state.traderData)
            except Exception:
                mem = {}

        # ── Trade IPR ────────────────────────────────────────────────
        result[IPR] = self._trade_ipr(state, mem)

        # ── Trade ACO ────────────────────────────────────────────────
        result[ACO] = self._trade_aco(state, mem)

        # ── Save state ───────────────────────────────────────────────
        return result, conversions, json.dumps(mem, separators=(",", ":"))

    # ════════════════════════════════════════════════════════════════
    # IPR: DRIFT CAPTURE
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

        # Compute fair value
        if "ipr_base" not in mem and bb is not None and ba is not None:
            mid = (bb + ba) / 2.0
            mem["ipr_base"] = mid - IPR_DRIFT * state.timestamp

        base = mem.get("ipr_base")
        if base is None:
            # Fallback: just buy everything available
            base = 12000.0
        fv = base + IPR_DRIFT * state.timestamp

        # ── BUY: aggressively fill to limit ──────────────────────────
        buy_cap = LIMIT - pos

        # 1) Take all ask levels within FV + edge
        if buy_cap > 0 and od.sell_orders:
            for ask_px in sorted(od.sell_orders):
                if buy_cap - buy_used <= 0:
                    break
                if ask_px <= fv + IPR_TAKE_EDGE:
                    ask_vol = -od.sell_orders[ask_px]
                    qty = min(buy_cap - buy_used, ask_vol)
                    if qty > 0:
                        orders.append(Order(IPR, ask_px, qty))
                        buy_used += qty

        # 2) Also take L2/L3 asks up to FV+12 if we still have room
        #    (squeeze more fills in early when position is low)
        if buy_cap - buy_used > 0 and pos + buy_used < 60 and od.sell_orders:
            for ask_px in sorted(od.sell_orders):
                if buy_cap - buy_used <= 0:
                    break
                if ask_px <= fv + 12 and ask_px > fv + IPR_TAKE_EDGE:
                    ask_vol = -od.sell_orders[ask_px]
                    qty = min(buy_cap - buy_used, ask_vol)
                    if qty > 0:
                        orders.append(Order(IPR, ask_px, qty))
                        buy_used += qty

        # 3) Passive repost: bid at FV or FV+1 to improve entry
        remaining_buy = buy_cap - buy_used
        if remaining_buy > 0:
            # Bid just above best bid for priority, but below best ask
            bid_px = int(math.floor(fv))
            if bb is not None:
                bid_px = max(bid_px, bb + 1)
            if ba is not None:
                bid_px = min(bid_px, ba - 1)
            orders.append(Order(IPR, bid_px, remaining_buy))

        # ── SELL: only on extreme residual overshoot ─────────────────
        sell_cap = LIMIT + pos
        if sell_cap > 0 and pos > 0 and od.buy_orders:
            for bid_px in sorted(od.buy_orders, reverse=True):
                if sell_cap - sell_used <= 0:
                    break
                if bid_px > fv + IPR_SELL_THRESHOLD:
                    bid_vol = od.buy_orders[bid_px]
                    qty = min(sell_cap - sell_used, bid_vol, pos - sell_used)
                    if qty > 0:
                        orders.append(Order(IPR, bid_px, -qty))
                        sell_used += qty

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

        # ── Fair value: weighted microprice + imbalance ──────────────
        raw_mid = None
        if bb is not None and ba is not None:
            raw_mid = (bb + ba) / 2.0

        micro = self._microprice(od, bb, ba)
        imb = self._full_book_imbalance(od)

        # Weighted microprice (EDA: w=0.5 gives 12% better prediction)
        if raw_mid is not None and micro is not None:
            fv_raw = raw_mid + ACO_MICROPRICE_W * (micro - raw_mid)
        elif micro is not None:
            fv_raw = micro
        elif raw_mid is not None:
            fv_raw = raw_mid
        else:
            fv_raw = mem.get("aco_fv", 10000.0)

        # Imbalance directional shift
        imb_shift = ACO_IMBALANCE_COEFF * imb

        # EMA smoothing of fair value (fast alpha for responsive tracking)
        alpha = 0.3
        prev_fv = mem.get("aco_fv", fv_raw)
        fv_smooth = alpha * fv_raw + (1.0 - alpha) * prev_fv
        mem["aco_fv"] = fv_smooth

        # ── Reservation price (Avellaneda-Stoikov) ───────────────────
        # r = s - q * γ * σ²
        # where q = position, γ = risk aversion, σ² = variance
        reservation = fv_smooth + imb_shift - pos * ACO_GAMMA

        # ── Dynamic spread (widens with inventory and volatility) ─────
        pos_ratio = abs(pos) / LIMIT
        spread_penalty = 1 if pos_ratio < ACO_MAX_POSITION_RATIO else 2
        half_spread = ACO_BASE_SPREAD + spread_penalty

        # If book is tight, narrow our spread to compete
        if bb is not None and ba is not None:
            book_spread = ba - bb
            if book_spread <= 12:
                half_spread = max(2, half_spread - 1)

        # ── TAKE: aggressive edge capture ────────────────────────────
        buy_cap = LIMIT - pos
        sell_cap = LIMIT + pos

        dynamic_edge = ACO_TAKE_EDGE
        # Be more aggressive when inventory is helping us (take more to reduce inventory)
        if pos < -20:
            dynamic_edge = max(0.5, dynamic_edge - 0.5)  # more eager to buy
        elif pos > 20:
            dynamic_edge = max(0.5, dynamic_edge - 0.5)  # more eager to sell (separate below)

        # Take cheap asks
        if od.sell_orders and buy_cap > 0:
            for ask_px in sorted(od.sell_orders):
                if buy_cap - buy_used <= 0:
                    break
                edge = reservation - ask_px
                buy_edge_needed = dynamic_edge if pos >= -20 else max(0.5, dynamic_edge - 0.5)
                if edge < buy_edge_needed:
                    break
                ask_vol = -od.sell_orders[ask_px]
                # Size: larger if edge is bigger or if reducing inventory
                take_size = ask_vol
                if pos + buy_used > 50:
                    take_size = min(take_size, 10)
                qty = min(buy_cap - buy_used, take_size)
                if qty > 0:
                    orders.append(Order(ACO, ask_px, qty))
                    buy_used += qty

        # Take expensive bids
        if od.buy_orders and sell_cap > 0:
            for bid_px in sorted(od.buy_orders, reverse=True):
                if sell_cap - sell_used <= 0:
                    break
                edge = bid_px - reservation
                sell_edge_needed = dynamic_edge if pos <= 20 else max(0.5, dynamic_edge - 0.5)
                if edge < sell_edge_needed:
                    break
                bid_vol = od.buy_orders[bid_px]
                take_size = bid_vol
                if pos - sell_used < -50:
                    take_size = min(take_size, 10)
                qty = min(sell_cap - sell_used, take_size)
                if qty > 0:
                    orders.append(Order(ACO, bid_px, -qty))
                    sell_used += qty

        # ── PASSIVE QUOTES ───────────────────────────────────────────
        bid_px = int(math.floor(reservation - half_spread))
        ask_px = int(math.ceil(reservation + half_spread))

        # Pin quotes inside the book (improve fill probability)
        if bb is not None:
            bid_px = max(bid_px, bb)      # at least match best bid
        if ba is not None:
            ask_px = min(ask_px, ba)      # at least match best ask

        # Ensure bid < ask always
        if bid_px >= ask_px:
            if bb is not None and ba is not None:
                bid_px = bb
                ask_px = ba
            else:
                mid_int = int(round(reservation))
                bid_px = mid_int - 1
                ask_px = mid_int + 1

        # Skew quote sizes based on inventory
        buy_size = 40
        sell_size = 40

        if pos > 20:
            buy_size = max(10, 40 - pos)
            sell_size = min(70, 40 + pos)
        elif pos < -20:
            buy_size = min(70, 40 - pos)
            sell_size = max(10, 40 + pos)

        # Extreme inventory: heavily skew
        if pos > 55:
            buy_size = 5
            sell_size = LIMIT
        elif pos < -55:
            buy_size = LIMIT
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
        """Volume-weighted microprice."""
        if bb is None or ba is None:
            return None
        bv = od.buy_orders.get(bb, 0)
        av = -od.sell_orders.get(ba, 0)
        total = bv + av
        if total <= 0:
            return (bb + ba) / 2.0
        return (bb * av + ba * bv) / total

    def _full_book_imbalance(self, od: OrderDepth) -> float:
        """Full-book volume imbalance (EDA shows better prediction than L1 alone)."""
        total_bid = 0
        total_ask = 0
        if od.buy_orders:
            for px, vol in od.buy_orders.items():
                total_bid += vol
        if od.sell_orders:
            for px, vol in od.sell_orders.items():
                total_ask += (-vol)
        total = total_bid + total_ask
        if total <= 0:
            return 0.0
        return (total_bid - total_ask) / total
