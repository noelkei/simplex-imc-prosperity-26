"""
r4_final_03 — Counterparty Flow Follower OTM
==============================================
Approach: Mark 01 consistently buys OTM options, Mark 22 consistently
sells. Follow Mark 01's flow direction — when Mark 01 has been buying
recently, bias long. When Mark 22 selling intensifies, pull back.
Covers 5200-5500 range. Adds VEX MM as base income.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()
VEX = "VELVETFRUIT_EXTRACT"
OTM_SYMBOLS = ["VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"]
STRIKES = {"VEV_5200": 5200, "VEV_5300": 5300, "VEV_5400": 5400, "VEV_5500": 5500}
LIMITS = {VEX: 200, "VEV_5200": 300, "VEV_5300": 300, "VEV_5400": 300, "VEV_5500": 300}
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
    for _ in range(30):
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

        # Track counterparty flow
        flow = self._update_flow(state, stored)

        # VEX MM
        vex_orders = self._trade_vex(state, stored)
        if vex_orders:
            result[VEX] = vex_orders

        # OTM basket with flow bias
        if vex_mid is not None:
            for sym in OTM_SYMBOLS:
                orders = self._trade_otm_flow(state, stored, sym, vex_mid, flow)
                if orders:
                    result[sym] = orders

        mids = stored.setdefault("mids", {})
        for s in [VEX] + OTM_SYMBOLS:
            m = mid_price(state.order_depths.get(s))
            if m is not None:
                mids[s] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _update_flow(self, state: TradingState, stored: dict) -> dict:
        """Track Mark 01 buying / Mark 22 selling in OTM."""
        events = list(stored.get("flow_ev", []))
        for sym in OTM_SYMBOLS:
            for trade in state.market_trades.get(sym, []):
                buyer = getattr(trade, "buyer", "") or ""
                seller = getattr(trade, "seller", "") or ""
                qty = abs(int(getattr(trade, "quantity", 0) or 0))
                ts = int(getattr(trade, "timestamp", state.timestamp) or state.timestamp)
                if buyer or seller:
                    events.append({
                        "s": sym, "b": buyer, "sl": seller,
                        "q": qty, "t": ts,
                    })
        if len(events) > 100:
            events = events[-100:]
        stored["flow_ev"] = events

        now = state.timestamp
        recent = [e for e in events if e["t"] >= now - 5000]

        mark01_buying = sum(e["q"] for e in recent if e["b"] == "Mark 01")
        mark22_selling = sum(e["q"] for e in recent if e["sl"] == "Mark 22")
        mark14_buying = sum(e["q"] for e in recent if e["b"] == "Mark 14")

        # Net flow score: positive = bullish (Mark 01 buying dominates)
        total = mark01_buying + mark14_buying + mark22_selling
        if total == 0:
            flow_score = 0.0
        else:
            flow_score = (mark01_buying + mark14_buying - mark22_selling) / total

        return {
            "score": flow_score,
            "m01_active": mark01_buying > 0,
            "m22_heavy": mark22_selling > mark01_buying + mark14_buying,
        }

    def _trade_vex(self, state: TradingState, stored: dict) -> List[Order]:
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
        fair = mid + 1.2 * imb - 0.12 * pos

        clip = 10
        if abs(pos) >= 120:
            clip = 4

        orders: List[Order] = []
        if bc > 0 and ask <= fair - 2.0:
            q = min(clip, bc, max(0, -depth.sell_orders.get(ask, 0)))
            if q > 0:
                orders.append(Order(VEX, ask, q))
                bc -= q
        if sc > 0 and bid >= fair + 2.0:
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

    def _trade_otm_flow(
        self, state: TradingState, stored: dict,
        sym: str, vex_mid: float, flow: dict
    ) -> List[Order]:
        depth = state.order_depths.get(sym)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 5:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        strike = STRIKES[sym]
        tte = tte_years(state.timestamp)
        iv_val = intrinsic(vex_mid, strike)
        clean = max(opt_mid, iv_val)

        ivh = stored.setdefault("ivh", {})
        hist = list(ivh.get(sym, []))
        cv = impl_vol(clean, vex_mid, strike, tte)
        if cv is not None and cv > 0:
            hist.append(cv)
        if len(hist) > 20:
            hist = hist[-20:]
        ivh[sym] = hist
        iv_mean = sum(hist) / len(hist) if hist else None
        if iv_mean is None:
            return []

        fair = bs_call(vex_mid, strike, tte, iv_mean)
        fair = max(fair, iv_val)

        last_vex = stored.get("mids", {}).get(VEX)
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        imb = imbalance(depth)
        fair += 0.5 * vex_move + 0.3 * imb
        fair = max(fair, iv_val, 0.0)

        pos = state.position.get(sym, 0)
        lim = LIMITS[sym]
        bc = max(0, lim - pos)
        sc = max(0, lim + pos)

        clip = 16
        if abs(pos) > 220:
            clip = 4
        elif abs(pos) > 140:
            clip = 8

        # Flow-based bias
        block_buy = False
        block_sell = False
        if flow["m22_heavy"]:
            # Mark 22 heavy selling — don't go long on new entries
            if pos >= 0:
                block_buy = True
        if flow["m01_active"] and flow["score"] > 0.3:
            # Mark 01 actively buying — favor long side
            clip = min(clip + 4, 20)

        edge = 0.3 if opt_mid < 10 else 0.5

        orders: List[Order] = []
        if bc > 0 and not block_buy and ask <= fair - edge:
            q = min(clip, bc, max(0, -depth.sell_orders.get(ask, 0)))
            if q > 0:
                orders.append(Order(sym, ask, q))
                bc -= q
        if sc > 0 and not block_sell and bid >= fair + edge:
            q = min(clip, sc, max(0, depth.buy_orders.get(bid, 0)))
            if q > 0:
                orders.append(Order(sym, bid, -q))
                sc -= q

        if sprd <= 4:
            if bc > 0 and not block_buy:
                px = max(0, min(bid + 1, int(math.floor(fair))))
                orders.append(Order(sym, px, min(max(1, clip // 2), bc)))
            if sc > 0 and not block_sell:
                px = max(ask - 1, int(math.ceil(fair)))
                orders.append(Order(sym, px, -min(max(1, clip // 2), sc)))

        return orders
