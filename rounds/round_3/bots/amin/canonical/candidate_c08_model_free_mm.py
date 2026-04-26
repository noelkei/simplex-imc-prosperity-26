"""
C08 Model-Free Market Maker — Round 3
====================================
Strategy: NO Bachelier model. Pure microstructure MM on ALL products.
Core: Kalman fair value + microprice + mean-reversion signal + aggressive inventory control.

Fixes over C06/C07:
- Drops Bachelier entirely (was causing systematic mispricing)
- Uses market mid as ground truth, Kalman-smoothed
- Exploits lag-1 negative autocorrelation (-0.13 to -0.21)
- Tight inventory caps: 40 on delta-1, 50 on vouchers (out of 200/300 limits)
- Avellaneda-Stoikov reservation price for inventory penalty
- Aggressive unwind mode when position builds up

Products traded: HYDROGEL_PACK, VELVETFRUIT_EXTRACT, VEV_5000-VEV_5300
Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────────────────────────
# Product configuration
# ─────────────────────────────────────────────────────────────────────

PRODUCTS = {
    # Delta-1 products
    "HYDROGEL_PACK": {
        "limit": 200,
        "pos_cap": 40,          # internal soft cap
        "half_spread": 2,       # passive quote half-spread
        "take_edge": 2,         # aggressive take threshold
        "kalman_r": 15.0,       # Kalman observation noise (higher = smoother)
        "unwind_thr": 35,       # start aggressive unwind above this
        "unwind_qty": 8,        # aggressive unwind size
    },
    "VELVETFRUIT_EXTRACT": {
        "limit": 200,
        "pos_cap": 40,
        "half_spread": 2,
        "take_edge": 2,
        "kalman_r": 8.0,
        "unwind_thr": 35,
        "unwind_qty": 8,
    },
    # Voucher products — pure MM, no model
    "VEV_5000": {
        "limit": 300,
        "pos_cap": 50,
        "half_spread": 2,
        "take_edge": 3,
        "kalman_r": 8.0,
        "unwind_thr": 40,
        "unwind_qty": 10,
    },
    "VEV_5100": {
        "limit": 300,
        "pos_cap": 50,
        "half_spread": 2,
        "take_edge": 3,
        "kalman_r": 8.0,
        "unwind_thr": 40,
        "unwind_qty": 10,
    },
    "VEV_5200": {
        "limit": 300,
        "pos_cap": 50,
        "half_spread": 3,
        "take_edge": 3,
        "kalman_r": 6.0,
        "unwind_thr": 40,
        "unwind_qty": 10,
    },
    "VEV_5300": {
        "limit": 300,
        "pos_cap": 50,
        "half_spread": 3,
        "take_edge": 3,
        "kalman_r": 5.0,        # more responsive (strongest mean reversion)
        "unwind_thr": 40,
        "unwind_qty": 10,
    },
}

# Global parameters
KALMAN_Q = 0.1                 # process noise (small = stable fair)
IMB_ALPHA = 0.35               # EMA smoothing for order imbalance
IMB_GAIN = 3.0                 # imbalance → quote shift (ticks)
IMB_CLIP = 2.0                 # max imbalance shift
RES_GAMMA = 2.5                # Avellaneda-Stoikov inventory penalty strength
PASSIVE_BASE_SIZE = 20         # base passive quote size
TAKE_SIZE = 15                 # max aggressive take per level
MAX_SPREAD = 30                # skip product if spread > this


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def microprice(od) -> float | None:
    """Volume-weighted midpoint (better fair estimate than simple mid)."""
    if not od.buy_orders or not od.sell_orders:
        return None
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return (bb + ba) / 2.0
    return (bb * av + ba * bv) / total


def simple_mid(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def book_imbalance(od) -> float:
    """Top-of-book volume imbalance in [-1, 1]."""
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return 0.0
    return (bv - av) / total


def kalman_step(sd: dict, key: str, obs: float | None, q: float, r: float) -> float:
    """Single-variable Kalman filter update. Returns filtered fair value."""
    fk = key + "_f"
    vk = key + "_v"
    fair = sd.get(fk, 0.0)
    var = sd.get(vk, 100.0)

    # Predict
    pred_var = min(var + q, 500.0)

    if obs is None:
        sd[vk] = pred_var
        return fair

    # First tick: initialize to observation
    if fair == 0.0 and var >= 100.0:
        sd[fk] = obs
        sd[vk] = r
        return obs

    # Update
    k = pred_var / (pred_var + r)
    new_fair = fair + k * (obs - fair)
    new_var = (1.0 - k) * pred_var

    sd[fk] = new_fair
    sd[vk] = new_var
    return new_fair


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


# ─────────────────────────────────────────────────────────────────────
# Trader
# ─────────────────────────────────────────────────────────────────────

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        # Load state
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        for prod, cfg in PRODUCTS.items():
            od = state.order_depths.get(prod)
            if od is None or not od.buy_orders or not od.sell_orders:
                continue

            bb = max(od.buy_orders)
            ba = min(od.sell_orders)
            spread = ba - bb

            if spread > MAX_SPREAD or spread < 1:
                continue

            pos = state.position.get(prod, 0)
            limit = cfg["limit"]
            pos_cap = cfg["pos_cap"]

            # ── Fair value: Kalman-filtered microprice ──
            mp = microprice(od)
            raw_mid = (bb + ba) / 2.0
            obs = mp if mp is not None else raw_mid
            fair = kalman_step(sd, prod, obs, KALMAN_Q, cfg["kalman_r"])
            if fair == 0.0:
                fair = raw_mid

            # ── EMA imbalance ──
            imb_raw = book_imbalance(od)
            imb_key = prod + "_imb"
            prev_imb = sd.get(imb_key, 0.0)
            imb = IMB_ALPHA * imb_raw + (1.0 - IMB_ALPHA) * prev_imb
            sd[imb_key] = imb

            # ── Reservation price (Avellaneda-Stoikov style) ──
            # Penalizes deviating from zero inventory
            res_px = fair - RES_GAMMA * (pos / limit)

            # ── Imbalance-driven predictive shift ──
            imb_shift = clamp(IMB_GAIN * imb, -IMB_CLIP, IMB_CLIP)
            qfair = res_px + imb_shift

            # ── Dynamic take edge: widen when inventory is extreme ──
            inv_fraction = abs(pos) / pos_cap if pos_cap > 0 else 0
            take_edge = cfg["take_edge"]
            if inv_fraction > 0.7:
                take_edge = max(1, take_edge - 1)  # more aggressive unwinding

            buy_threshold = qfair - take_edge
            sell_threshold = qfair + take_edge

            orders = []
            bought = 0
            sold = 0

            def buy_room():
                return max(0, pos_cap - pos - bought)

            def sell_room():
                return max(0, pos_cap + pos - sold)

            # ── Aggressive takes ──
            for ask_p in sorted(od.sell_orders.keys()):
                if buy_room() <= 0:
                    break
                if ask_p > buy_threshold:
                    break
                avail = -od.sell_orders[ask_p]
                qty = min(avail, TAKE_SIZE, buy_room())
                if qty > 0:
                    orders.append(Order(prod, ask_p, qty))
                    bought += qty

            for bid_p in sorted(od.buy_orders.keys(), reverse=True):
                if sell_room() <= 0:
                    break
                if bid_p < sell_threshold:
                    break
                avail = od.buy_orders[bid_p]
                qty = min(avail, TAKE_SIZE, sell_room())
                if qty > 0:
                    orders.append(Order(prod, bid_p, -qty))
                    sold += qty

            # ── Aggressive unwind at extreme positions ──
            if abs(pos) >= cfg["unwind_thr"]:
                if pos > 0 and sell_room() > 0:
                    uq = min(cfg["unwind_qty"], sell_room())
                    if uq > 0:
                        orders.append(Order(prod, bb, -uq))
                        sold += uq
                elif pos < 0 and buy_room() > 0:
                    uq = min(cfg["unwind_qty"], buy_room())
                    if uq > 0:
                        orders.append(Order(prod, ba, uq))
                        bought += uq

            # ── Passive quotes ──
            half = cfg["half_spread"]
            # Widen spread when inventory is building
            if inv_fraction > 0.5:
                half += 1

            bid_px = int(round(qfair - half))
            ask_px = int(round(qfair + half))

            # Don't cross the book
            if bid_px >= ba:
                bid_px = ba - 1
            if ask_px <= bb:
                ask_px = bb + 1
            if bid_px >= ask_px:
                bid_px = ask_px - 1

            # Inventory-skewed sizes: quote bigger on the side that reduces position
            if pos > 0:
                # We're long → want to sell more, buy less
                b_size = max(2, PASSIVE_BASE_SIZE - int(pos * 0.4))
                s_size = max(2, PASSIVE_BASE_SIZE + int(pos * 0.4))
            elif pos < 0:
                # We're short → want to buy more, sell less
                b_size = max(2, PASSIVE_BASE_SIZE + int(-pos * 0.4))
                s_size = max(2, PASSIVE_BASE_SIZE - int(-pos * 0.4))
            else:
                b_size = PASSIVE_BASE_SIZE
                s_size = PASSIVE_BASE_SIZE

            bq = min(b_size, buy_room())
            sq = min(s_size, sell_room())

            if bq > 0 and bid_px > 0:
                orders.append(Order(prod, bid_px, bq))
            if sq > 0 and ask_px > 0:
                orders.append(Order(prod, ask_px, -sq))

            result[prod] = orders

        # Persist
        trader_data = json.dumps(sd)
        return result, conversions, trader_data
