"""
r4_finalbatch_12 — Conservative OTM Basket
============================================
Dials back r4_finalbatch_11 to stay closer to r4_finalbatch_10:
  - Restores dead zone (reduced to 2.0 from 3.0)
  - Restores edges closer to original (2.0 / 1.5 / 1.0)
  - Removes EMA premium (was chasing noise) — fixed premiums only
  - Restores clip size to 15
  - Restores quoting spread filter to <= 6
Keeps the beneficial structural changes:
  - Per-strike VEX sensitivity (grounded in EDA correlations)
  - Full book walking (captures more when edge is real)
  - Light inventory skew (prevents one-sided accumulation)
  - Basket-level giveback stop (smarter than per-strike)
  - Late session: only block new entries after 90%, don't reduce clips
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

VEX = "VELVETFRUIT_EXTRACT"

STRIKE_CFG = {
    "VEV_5300": {"strike": 5300, "premium": 6.0, "vex_sens": 0.60, "edge": 2.0},
    "VEV_5400": {"strike": 5400, "premium": 4.0, "vex_sens": 0.35, "edge": 1.5},
    "VEV_5500": {"strike": 5500, "premium": 2.5, "vex_sens": 0.18, "edge": 1.0},
}
LIMIT = 300
CLIP = 15
DEAD_ZONE = 2.0       # skip when |opt_mid - fair| < this
INV_SKEW = 0.005      # lighter than v11 (was 0.008)

# Basket-level giveback stop (same as v10 but basket-level)
PEAK_GIVEBACK_FRAC = 0.35
MIN_PEAK_FOR_STOP = 10.0
MAX_BASKET_DRAWDOWN = 50.0

# Late session: only block new entries, don't touch clips
LATE_PROGRESS = 0.90
TIME_SCALE = 1_000_000


def best_bid_ask(depth) -> Tuple[Optional[int], Optional[int]]:
    if depth is None:
        return None, None
    bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
    ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
    return bid, ask


def mid_price(depth) -> Optional[float]:
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return None
    return (bid + ask) / 2.0


def imbalance(depth) -> float:
    if depth is None:
        return 0.0
    bid, ask = best_bid_ask(depth)
    bsz = depth.buy_orders.get(bid, 0) if bid is not None else 0
    asz = -depth.sell_orders.get(ask, 0) if ask is not None else 0
    total = bsz + asz
    if total <= 0:
        return 0.0
    return (bsz - asz) / total


def sign(v: int) -> int:
    return (v > 0) - (v < 0)


def session_progress(ts: int) -> float:
    return float(ts % TIME_SCALE) / float(TIME_SCALE)


class Trader:
    def run(self, state: TradingState):
        store = self._load(state.traderData)
        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)

        orders: Dict[str, List[Order]] = {}
        if vex_mid is None:
            self._cache(state, store)
            return orders, 0, json.dumps(store)

        last_vex = store.get("last_vex")
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        late = session_progress(state.timestamp) >= LATE_PROGRESS
        basket_stop = self._check_basket_stop(state, store)

        for sym, cfg in STRIKE_CFG.items():
            out = self._trade_strike(
                state, store, sym, cfg, vex_mid, vex_move, late, basket_stop,
            )
            if out:
                orders[sym] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    def _trade_strike(
        self, state: TradingState, store: dict, sym: str, cfg: dict,
        vex_mid: float, vex_move: float, late: bool, basket_stop: bool,
    ) -> List[Order]:
        depth = state.order_depths.get(sym)
        opt_mid = mid_price(depth)
        bid, ask = best_bid_ask(depth)
        if depth is None or opt_mid is None or bid is None or ask is None:
            return []

        spread = ask - bid
        pos = int(state.position.get(sym, 0))
        dimb = imbalance(depth)

        intrinsic = max(vex_mid - cfg["strike"], 0.0)
        fair = intrinsic + cfg["premium"] + cfg["vex_sens"] * vex_move + 0.5 * dimb
        fair -= INV_SKEW * pos

        # Dead zone: skip when no edge (restored from v10, slightly tighter)
        if abs(opt_mid - fair) < DEAD_ZONE:
            return []

        buy_cap = max(0, LIMIT - pos)
        sell_cap = max(0, LIMIT + pos)

        clip = CLIP
        if abs(pos) >= 240:
            clip = 5
        elif abs(pos) >= 180:
            clip = 8

        # Late session: block new entries, but allow reducing positions
        if late:
            if pos >= 0:
                buy_cap = 0       # don't add to long or open new long
            if pos <= 0:
                sell_cap = 0      # don't add to short or open new short

        # Basket stop: only allow reducing positions
        if basket_stop:
            if pos >= 0:
                buy_cap = 0
            if pos <= 0:
                sell_cap = 0

        edge = cfg["edge"]
        out: List[Order] = []

        # Take: walk the full book (improvement over v10)
        if buy_cap > 0:
            for px in sorted(depth.sell_orders.keys()):
                if px > fair - edge:
                    break
                vol = min(clip, buy_cap, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    out.append(Order(sym, px, vol))
                    buy_cap -= vol
                if buy_cap <= 0:
                    break

        if sell_cap > 0:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair + edge:
                    break
                vol = min(clip, sell_cap, max(0, depth.buy_orders[px]))
                if vol > 0:
                    out.append(Order(sym, px, -vol))
                    sell_cap -= vol
                if sell_cap <= 0:
                    break

        # Quote (same spread filter as v10)
        if spread <= 6:
            q_clip = max(1, clip // 2)
            if buy_cap > 0:
                bid_px = min(bid + 1, int(fair - 1))
                bid_px = max(1, bid_px)
                out.append(Order(sym, bid_px, min(q_clip, buy_cap)))
            if sell_cap > 0:
                ask_px = max(ask - 1, int(math.ceil(fair + 1)))
                out.append(Order(sym, ask_px, -min(q_clip, sell_cap)))

        return self._dedupe(out)

    def _check_basket_stop(self, state: TradingState, store: dict) -> bool:
        basket = store.setdefault("basket", {})
        total_unreal = 0.0

        for sym in STRIKE_CFG:
            pos = int(state.position.get(sym, 0))
            depth = state.order_depths.get(sym)
            opt_mid = mid_price(depth)
            if pos == 0 or opt_mid is None:
                basket.pop(sym, None)
                continue

            entry = basket.get(sym)
            if entry is None or sign(int(entry.get("dir", 0))) != sign(pos):
                basket[sym] = {"entry_mid": opt_mid, "dir": sign(pos)}
                continue

            entry_mid = float(entry["entry_mid"])
            unreal = (opt_mid - entry_mid) * sign(pos)
            total_unreal += unreal

        peak = float(basket.get("_peak", 0.0))
        peak = max(peak, total_unreal)
        basket["_peak"] = peak

        if peak < MIN_PEAK_FOR_STOP:
            return False

        giveback_hit = total_unreal <= peak * (1.0 - PEAK_GIVEBACK_FRAC)
        drawdown_hit = (peak - total_unreal) >= MAX_BASKET_DRAWDOWN
        return giveback_hit or drawdown_hit

    def _load(self, td) -> dict:
        if not isinstance(td, str) or not td:
            return {}
        try:
            d = json.loads(td)
            return d if isinstance(d, dict) else {}
        except Exception:
            return {}

    def _cache(self, state: TradingState, store: dict,
               vex_mid: Optional[float] = None) -> None:
        if vex_mid is None:
            vex_mid = mid_price(state.order_depths.get(VEX))
        if vex_mid is not None:
            store["last_vex"] = vex_mid

    def _dedupe(self, orders: List[Order]) -> List[Order]:
        merged: Dict[Tuple[str, int], int] = {}
        for o in orders:
            key = (o.symbol, o.price)
            merged[key] = merged.get(key, 0) + int(o.quantity)
        return [Order(s, p, q) for (s, p), q in merged.items() if q != 0]
