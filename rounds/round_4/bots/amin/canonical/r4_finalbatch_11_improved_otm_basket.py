"""
r4_finalbatch_11 — Improved OTM Basket
=======================================
Built on top of r4_finalbatch_10. Key improvements over the base:
  1. Per-strike VEX sensitivity (0.60/0.35/0.18) instead of flat 0.70
  2. No dead zone — always quotes, uses inventory skew to lean against position
  3. Walks full book depth when taking, not just top-of-book
  4. Per-strike edge thresholds (lower for far OTM)
  5. Bigger base clips (20) with softer position scaling
  6. Wider quoting threshold (spread <= 8)
  7. Adaptive premium via EMA of observed market premium
  8. Basket-level giveback stop with higher thresholds + late position wind-down
"""

import json
import math
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

VEX = "VELVETFRUIT_EXTRACT"

# Per-strike config: vex_sens from EDA correlations, edge scaled to price magnitude
STRIKE_CFG = {
    "VEV_5300": {"strike": 5300, "premium": 6.0, "vex_sens": 0.60, "edge": 1.5, "clip": 20, "max_spread": 8},
    "VEV_5400": {"strike": 5400, "premium": 4.0, "vex_sens": 0.35, "edge": 1.0, "clip": 22, "max_spread": 7},
    "VEV_5500": {"strike": 5500, "premium": 2.5, "vex_sens": 0.18, "edge": 0.5, "clip": 25, "max_spread": 6},
}
LIMIT = 300
INV_SKEW = 0.008  # fair value shift per unit of position to lean against inventory

# Basket-level giveback stop
PEAK_GIVEBACK_FRAC = 0.40   # trigger when unrealized drops to 60% of peak
MIN_PEAK_FOR_STOP = 15.0    # only arm stop after meaningful basket peak
MAX_BASKET_DRAWDOWN = 60.0  # absolute drawdown cap

# Late session wind-down
LATE_PROGRESS = 0.80        # fraction of session after which we reduce exposure
TIME_SCALE = 1_000_000

# Premium EMA smoothing
PREMIUM_ALPHA = 0.15


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
        progress = session_progress(state.timestamp)
        late = progress >= LATE_PROGRESS

        # Basket-level giveback check
        basket_stop = self._check_basket_stop(state, store)

        for sym, cfg in STRIKE_CFG.items():
            out = self._trade_strike(
                state, store, sym, cfg, vex_mid, vex_move, late, basket_stop,
            )
            if out:
                orders[sym] = out

        self._cache(state, store, vex_mid)
        return orders, 0, json.dumps(store)

    # ------------------------------------------------------------------
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

        # --- Fair value ---
        intrinsic = max(vex_mid - cfg["strike"], 0.0)
        base_prem = cfg["premium"]

        # Adaptive premium: EMA of observed (opt_mid - intrinsic)
        prem_key = f"prem_{sym}"
        observed_prem = max(opt_mid - intrinsic, 0.0)
        ema_prem = store.get(prem_key)
        if ema_prem is None:
            ema_prem = base_prem
        ema_prem = PREMIUM_ALPHA * observed_prem + (1 - PREMIUM_ALPHA) * ema_prem
        store[prem_key] = ema_prem
        prem = 0.6 * base_prem + 0.4 * ema_prem  # blend fixed + adaptive

        fair = intrinsic + prem + cfg["vex_sens"] * vex_move + 0.4 * dimb
        # Inventory skew: shift fair against position to encourage mean-reversion
        fair -= INV_SKEW * pos

        buy_cap = max(0, LIMIT - pos)
        sell_cap = max(0, LIMIT + pos)

        clip = cfg["clip"]
        if abs(pos) >= 250:
            clip = max(4, clip // 3)
        elif abs(pos) >= 200:
            clip = max(6, clip // 2)
        elif abs(pos) >= 150:
            clip = max(8, (clip * 2) // 3)

        # Late session: only reduce, don't extend
        if late:
            if pos > 0:
                buy_cap = 0
                clip = min(clip, 12)
            elif pos < 0:
                sell_cap = 0
                clip = min(clip, 12)
            else:
                buy_cap = 0
                sell_cap = 0

        # Basket stop: only allow reducing positions
        if basket_stop:
            if pos >= 0:
                buy_cap = 0
            if pos <= 0:
                sell_cap = 0
            clip = min(clip, 15)

        edge = cfg["edge"]
        out: List[Order] = []

        # --- Take: walk the full book ---
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

        # --- Quote ---
        if spread <= cfg["max_spread"]:
            q_clip = max(1, clip // 2)
            if buy_cap > 0:
                bid_px = max(1, min(bid + 1, int(math.floor(fair - 0.5))))
                out.append(Order(sym, bid_px, min(q_clip, buy_cap)))
            if sell_cap > 0:
                ask_px = max(ask - 1, int(math.ceil(fair + 0.5)))
                out.append(Order(sym, ask_px, -min(q_clip, sell_cap)))

        return self._dedupe(out)

    # ------------------------------------------------------------------
    def _check_basket_stop(self, state: TradingState, store: dict) -> bool:
        """Basket-level giveback: track sum of per-strike unrealized mark-to-mid."""
        basket = store.setdefault("basket", {})
        total_unreal = 0.0

        for sym in STRIKE_CFG:
            pos = int(state.position.get(sym, 0))
            depth = state.order_depths.get(sym)
            opt_mid = mid_price(depth)
            if pos == 0 or opt_mid is None:
                # reset per-strike tracking
                basket.pop(sym, None)
                continue

            entry = basket.get(sym)
            if entry is None or sign(int(entry.get("dir", 0))) != sign(pos):
                basket[sym] = {"entry_mid": opt_mid, "dir": sign(pos)}
                continue

            entry_mid = float(entry["entry_mid"])
            # unrealized: positive when trade is profitable
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

    # ------------------------------------------------------------------
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
