"""
r4_final_06 — Tighter Edge (Half Edge Thresholds)
=====================================================
Variant of 05. Single change: all edge thresholds halved so the bot
takes liquidity more aggressively. Hypothesis: the base bot leaves
money on the table by requiring too much edge before taking.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()
VEX = "VELVETFRUIT_EXTRACT"
HYDRO = "HYDROGEL_PACK"
OTM_SYMBOLS = ["VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"]
STRIKES = {"VEV_5200": 5200, "VEV_5300": 5300, "VEV_5400": 5400, "VEV_5500": 5500}
LIMITS = {
    VEX: 200, HYDRO: 200,
    "VEV_5200": 300, "VEV_5300": 300, "VEV_5400": 300, "VEV_5500": 300,
}
# Strike-specific config
STRIKE_CONFIG = {
    "VEV_5200": {"vex_sens": 0.75, "base_clip": 14, "max_spread": 6, "edge": 0.25},
    "VEV_5300": {"vex_sens": 0.60, "base_clip": 16, "max_spread": 5, "edge": 0.25},
    "VEV_5400": {"vex_sens": 0.35, "base_clip": 20, "max_spread": 3, "edge": 0.15},
    "VEV_5500": {"vex_sens": 0.18, "base_clip": 22, "max_spread": 3, "edge": 0.10},
}
RD4_DAYS_LEFT = 4.0
TIME_SCALE = 1_000_000


def best_bid_ask(d) -> Tuple[Optional[int], Optional[int]]:
    if d is None:
        return None, None
    bid = max(d.buy_orders.keys()) if d.buy_orders else None
    ask = min(d.sell_orders.keys()) if d.sell_orders else None
    return bid, ask


def mid_price(d) -> Optional[float]:
    b, a = best_bid_ask(d)
    if b is None or a is None:
        return None
    return (b + a) / 2.0


def get_spread(d) -> Optional[int]:
    b, a = best_bid_ask(d)
    if b is None or a is None:
        return None
    return a - b


def imbalance(d) -> float:
    if d is None:
        return 0.0
    b, a = best_bid_ask(d)
    if b is None or a is None:
        return 0.0
    bv = d.buy_orders.get(b, 0)
    av = -d.sell_orders.get(a, 0)
    t = bv + av
    return (bv - av) / t if t > 0 else 0.0


def tte_years(ts: int) -> float:
    prog = float(ts % TIME_SCALE) / float(TIME_SCALE)
    return max(0.5, RD4_DAYS_LEFT - prog) / 365.0


def intrinsic(spot: float, strike: int) -> float:
    return max(0.0, spot - strike)


def bs_call(spot: float, strike: int, tte: float, vol: float) -> float:
    if spot <= 0 or strike <= 0 or tte <= 0 or vol <= 0:
        return intrinsic(spot, strike)
    st = math.sqrt(tte)
    ss = vol * st
    if ss <= 0:
        return intrinsic(spot, strike)
    d1 = (math.log(spot / strike) + 0.5 * vol ** 2 * tte) / ss
    d2 = d1 - ss
    return spot * NORMAL.cdf(d1) - strike * NORMAL.cdf(d2)


def impl_vol(price: float, spot: float, strike: int, tte: float) -> Optional[float]:
    iv = intrinsic(spot, strike)
    tgt = max(price, iv)
    if tgt <= iv + 1e-6:
        return 0.08
    if spot <= 0 or strike <= 0 or tte <= 0:
        return None
    lo, hi = 1e-4, 5.0
    for _ in range(32):
        mid = 0.5 * (lo + hi)
        if bs_call(spot, strike, tte, mid) >= tgt:
            hi = mid
        else:
            lo = mid
    return hi


class Trader:
    def run(self, state: TradingState):
        stored = {}
        if state.traderData:
            try:
                stored = json.loads(state.traderData)
            except Exception:
                stored = {}

        result: Dict[str, List[Order]] = {}
        vex_mid = mid_price(state.order_depths.get(VEX))

        # Counterparty flow analysis
        flow = self._update_flow(state, stored)

        # Cross-strike exposure management
        otm_positions = {s: state.position.get(s, 0) for s in OTM_SYMBOLS}
        total_otm_abs = sum(abs(v) for v in otm_positions.values())
        vex_abs = abs(state.position.get(VEX, 0))
        # Global scaling factor — penalize when total OTM exceeds ~600
        gf = max(0.25, 1.0 - total_otm_abs / 1200 - vex_abs / 600)

        # VEX anchor MM — always active
        vex_orders = self._trade_vex(state, stored, gf)
        if vex_orders:
            result[VEX] = vex_orders

        # HYDRO for base diversification
        hydro_orders = self._trade_hydro(state, stored)
        if hydro_orders:
            result[HYDRO] = hydro_orders

        # Full OTM basket
        if vex_mid is not None:
            for sym in OTM_SYMBOLS:
                orders = self._trade_otm(state, stored, sym, vex_mid, flow, gf)
                if orders:
                    result[sym] = orders

        # Cache mids
        mids = stored.setdefault("mids", {})
        for s in [VEX, HYDRO] + OTM_SYMBOLS:
            m = mid_price(state.order_depths.get(s))
            if m is not None:
                mids[s] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _update_flow(self, state: TradingState, stored: dict) -> dict:
        events = list(stored.get("fl", []))
        for sym in OTM_SYMBOLS:
            for trade in state.market_trades.get(sym, []):
                b = getattr(trade, "buyer", "") or ""
                s = getattr(trade, "seller", "") or ""
                q = abs(int(getattr(trade, "quantity", 0) or 0))
                ts = int(getattr(trade, "timestamp", state.timestamp) or state.timestamp)
                if b or s:
                    events.append({"b": b, "s": s, "q": q, "t": ts})
        if len(events) > 120:
            events = events[-120:]
        stored["fl"] = events

        now = state.timestamp
        recent = [e for e in events if e["t"] >= now - 6000]

        m01_q = sum(e["q"] for e in recent if e["b"] == "Mark 01")
        m14_q = sum(e["q"] for e in recent if e["b"] == "Mark 14")
        m22_q = sum(e["q"] for e in recent if e["s"] == "Mark 22")

        buy_total = m01_q + m14_q
        return {
            "bullish": buy_total > m22_q and buy_total > 0,
            "bearish": m22_q > buy_total * 1.5 and m22_q > 3,
            "m01_active": m01_q > 0,
        }

    def _trade_vex(self, state: TradingState, stored: dict, gf: float) -> List[Order]:
        depth = state.order_depths.get(VEX)
        if depth is None:
            return []
        mid = mid_price(depth)
        sprd = get_spread(depth)
        if mid is None or sprd is None or sprd > 6:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        pos = state.position.get(VEX, 0)
        bc = max(0, LIMITS[VEX] - pos)
        sc = max(0, LIMITS[VEX] + pos)
        imb = imbalance(depth)
        last = stored.get("mids", {}).get(VEX)
        mom = 0.0 if last is None else 0.15 * (mid - last)
        fair = mid + 1.2 * imb + mom - 0.12 * pos

        clip = max(3, int(12 * gf))
        if abs(pos) >= 120:
            clip = max(3, clip // 3)
        elif abs(pos) >= 80:
            clip = max(4, clip // 2)

        orders: List[Order] = []
        if bc > 0 and ask <= fair - 0.75:
            q = min(clip, bc, max(0, -depth.sell_orders.get(ask, 0)))
            if q > 0:
                orders.append(Order(VEX, ask, q))
                bc -= q
        if sc > 0 and bid >= fair + 0.75:
            q = min(clip, sc, max(0, depth.buy_orders.get(bid, 0)))
            if q > 0:
                orders.append(Order(VEX, bid, -q))
                sc -= q
        if sprd <= 4:
            if bc > 0:
                px = max(1, min(bid + 1, int(math.floor(fair - 1))))
                orders.append(Order(VEX, px, min(clip, bc)))
            if sc > 0:
                px = max(ask - 1, int(math.ceil(fair + 1)))
                orders.append(Order(VEX, px, -min(clip, sc)))
        return orders

    def _trade_hydro(self, state: TradingState, stored: dict) -> List[Order]:
        depth = state.order_depths.get(HYDRO)
        if depth is None:
            return []
        mid = mid_price(depth)
        sprd = get_spread(depth)
        if mid is None or sprd is None:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        pos = state.position.get(HYDRO, 0)
        bc = max(0, LIMITS[HYDRO] - pos)
        sc = max(0, LIMITS[HYDRO] + pos)
        fair = mid - 0.15 * pos

        clip = 8
        if abs(pos) > 140:
            clip = 3

        orders: List[Order] = []
        offset = max(3, int(sprd * 0.3))
        if bc > 0:
            px = max(1, min(bid + 1, int(math.floor(fair - offset))))
            orders.append(Order(HYDRO, px, min(clip, bc)))
        if sc > 0:
            px = max(ask - 1, int(math.ceil(fair + offset)))
            orders.append(Order(HYDRO, px, -min(clip, sc)))
        return orders

    def _trade_otm(
        self, state: TradingState, stored: dict,
        sym: str, vex_mid: float, flow: dict, gf: float
    ) -> List[Order]:
        cfg = STRIKE_CONFIG[sym]
        depth = state.order_depths.get(sym)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > cfg["max_spread"]:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        strike = STRIKES[sym]
        tte = tte_years(state.timestamp)
        iv_val = intrinsic(vex_mid, strike)
        clean = max(opt_mid, iv_val)

        # Per-strike IV smoothing
        ivh = stored.setdefault("ivh", {})
        hist = list(ivh.get(sym, []))
        cv = impl_vol(clean, vex_mid, strike, tte)
        if cv is not None and cv > 0:
            hist.append(cv)
        if len(hist) > 24:
            hist = hist[-24:]
        ivh[sym] = hist
        iv_mean = sum(hist) / len(hist) if hist else None
        if iv_mean is None:
            return []

        fair = bs_call(vex_mid, strike, tte, iv_mean)
        fair = max(fair, iv_val)

        # Responsive to VEX with strike-specific sensitivity
        last_vex = stored.get("mids", {}).get(VEX)
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        imb = imbalance(depth)
        fair += cfg["vex_sens"] * vex_move + 0.3 * imb
        fair = max(fair, iv_val, 0.0)

        pos = state.position.get(sym, 0)
        lim = LIMITS[sym]
        bc = max(0, lim - pos)
        sc = max(0, lim + pos)

        clip = max(3, int(cfg["base_clip"] * gf))
        if abs(pos) > 220:
            clip = max(3, clip // 3)
        elif abs(pos) > 140:
            clip = max(4, clip // 2)

        # Flow-based adjustments
        block_buy = False
        block_sell = False
        if flow["bearish"]:
            if pos >= 0:
                block_buy = True
            clip = max(3, clip // 2)
        elif flow["bullish"] and flow["m01_active"]:
            clip = min(clip + 3, 24)

        edge = cfg["edge"]

        orders: List[Order] = []

        # Aggressive taking — walk the book
        if bc > 0 and not block_buy and ask <= fair - edge:
            for px in sorted(depth.sell_orders.keys()):
                if px > fair - edge:
                    break
                vol = min(clip, bc, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    orders.append(Order(sym, px, vol))
                    bc -= vol
                if bc <= 0:
                    break

        if sc > 0 and not block_sell and bid >= fair + edge:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair + edge:
                    break
                vol = min(clip, sc, max(0, depth.buy_orders[px]))
                if vol > 0:
                    orders.append(Order(sym, px, -vol))
                    sc -= vol
                if sc <= 0:
                    break

        # Tight quoting
        if sprd <= cfg["max_spread"]:
            if bc > 0 and not block_buy:
                px = max(0, min(bid + 1, int(math.floor(fair))))
                orders.append(Order(sym, px, min(max(1, clip // 2), bc)))
            if sc > 0 and not block_sell:
                px = max(ask - 1, int(math.ceil(fair)))
                orders.append(Order(sym, px, -min(max(1, clip // 2), sc)))

        return orders
