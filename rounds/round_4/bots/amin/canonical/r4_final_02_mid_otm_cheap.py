"""
r4_final_02 — Mid-OTM Cheap Options (5300 + 5400 + 5500)
==========================================================
Approach: Focus on the cheap OTM strikes where spreads are tight (1-2 ticks)
and trade counts are high (80-120/day). These options have low absolute
prices (3-53) so even small mispricings represent high % edge. Market-make
with BS fair value aggressively. Skip VEX to maximize option position capacity.
"""

import json
import math
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState

NORMAL = NormalDist()
VEX = "VELVETFRUIT_EXTRACT"
OTM_SYMBOLS = ["VEV_5300", "VEV_5400", "VEV_5500"]
STRIKES = {"VEV_5300": 5300, "VEV_5400": 5400, "VEV_5500": 5500}
LIMITS = {VEX: 200, "VEV_5300": 300, "VEV_5400": 300, "VEV_5500": 300}
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
        if vex_mid is None:
            return result, 0, json.dumps(stored, separators=(",", ":"))

        for sym in OTM_SYMBOLS:
            orders = self._trade_cheap_otm(state, stored, sym, vex_mid)
            if orders:
                result[sym] = orders

        mids = stored.setdefault("mids", {})
        m = mid_price(state.order_depths.get(VEX))
        if m is not None:
            mids[VEX] = m
        for s in OTM_SYMBOLS:
            m = mid_price(state.order_depths.get(s))
            if m is not None:
                mids[s] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

    def _trade_cheap_otm(
        self, state: TradingState, stored: dict, sym: str, vex_mid: float
    ) -> List[Order]:
        depth = state.order_depths.get(sym)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 4:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        strike = STRIKES[sym]
        tte = tte_years(state.timestamp)
        iv_val = intrinsic(vex_mid, strike)
        clean = max(opt_mid, iv_val)

        # IV smoothing per strike
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

        # For cheap options, even half a tick matters
        last_vex = stored.get("mids", {}).get(VEX)
        vex_move = 0.0 if last_vex is None else vex_mid - last_vex
        imb = imbalance(depth)

        # Sensitivity to VEX move increases for nearer strikes
        vex_sensitivity = {
            "VEV_5300": 0.7, "VEV_5400": 0.4, "VEV_5500": 0.2
        }.get(sym, 0.3)
        fair += vex_sensitivity * vex_move + 0.3 * imb
        fair = max(fair, iv_val, 0.0)

        pos = state.position.get(sym, 0)
        lim = LIMITS[sym]
        bc = max(0, lim - pos)
        sc = max(0, lim + pos)

        # Larger clips for cheap options — each unit is cheap
        clip = 20
        if abs(pos) > 240:
            clip = 5
        elif abs(pos) > 160:
            clip = 10

        # For very cheap options (price < 5), edge can be tighter
        edge = 0.3 if opt_mid < 10 else 0.5

        orders: List[Order] = []

        # Aggressive take — walk the book for cheap OTM
        if bc > 0 and ask <= fair - edge:
            for px in sorted(depth.sell_orders.keys()):
                if px > fair - edge:
                    break
                vol = min(clip, bc, max(0, -depth.sell_orders[px]))
                if vol > 0:
                    orders.append(Order(sym, px, vol))
                    bc -= vol
                if bc <= 0:
                    break

        if sc > 0 and bid >= fair + edge:
            for px in sorted(depth.buy_orders.keys(), reverse=True):
                if px < fair + edge:
                    break
                vol = min(clip, sc, max(0, depth.buy_orders[px]))
                if vol > 0:
                    orders.append(Order(sym, px, -vol))
                    sc -= vol
                if sc <= 0:
                    break

        # Tight quoting on 1-2 tick spreads
        if sprd <= 3:
            if bc > 0:
                px = min(bid + 1, int(math.floor(fair)))
                px = max(0, px)
                orders.append(Order(sym, px, min(clip, bc)))
            if sc > 0:
                px = max(ask - 1, int(math.ceil(fair)))
                orders.append(Order(sym, px, -min(clip, sc)))

        return orders
