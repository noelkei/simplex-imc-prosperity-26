"""
r4_final_04 — OTM Basket + VEX Anchor Combined
=================================================
Approach: Strong VEX market-making as the anchor and primary profit engine,
plus a broad OTM basket (5200-5500) that uses VEX as the fair-value anchor
for all option pricing. The idea is that VEX revenue is reliable, and OTM
options add asymmetric upside when they are mispriced relative to VEX.
Cross-product inventory awareness: reduce OTM clips when VEX exposure
is already elevated.
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
LIMITS = {
    VEX: 200,
    "VEV_5200": 300, "VEV_5300": 300, "VEV_5400": 300, "VEV_5500": 300,
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


def bs_delta(spot: float, strike: int, tte: float, vol: float) -> float:
    if spot <= 0 or strike <= 0 or tte <= 0 or vol <= 0:
        return 1.0 if spot > strike else 0.0
    st = math.sqrt(tte)
    ss = vol * st
    if ss <= 0:
        return 1.0 if spot > strike else 0.0
    d1 = (math.log(spot / strike) + 0.5 * vol ** 2 * tte) / ss
    return NORMAL.cdf(d1)


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

        # Global exposure check for cross-product sizing
        total_otm_exposure = sum(
            abs(state.position.get(s, 0)) for s in OTM_SYMBOLS
        )
        vex_exposure = abs(state.position.get(VEX, 0))
        # Scale down when overall exposure is high
        global_factor = max(0.3, 1.0 - 0.002 * total_otm_exposure - 0.003 * vex_exposure)

        # VEX anchor — aggressive MM
        vex_orders = self._trade_vex(state, stored, global_factor)
        if vex_orders:
            result[VEX] = vex_orders

        # OTM basket
        if vex_mid is not None:
            for sym in OTM_SYMBOLS:
                orders = self._trade_otm(state, stored, sym, vex_mid, global_factor)
                if orders:
                    result[sym] = orders

        mids = stored.setdefault("mids", {})
        for s in [VEX] + OTM_SYMBOLS:
            m = mid_price(state.order_depths.get(s))
            if m is not None:
                mids[s] = m

        return result, 0, json.dumps(stored, separators=(",", ":"))

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

        clip = max(3, int(14 * gf))
        if abs(pos) >= 120:
            clip = max(3, clip // 3)
        elif abs(pos) >= 80:
            clip = max(4, clip // 2)

        orders: List[Order] = []
        if bc > 0 and ask <= fair - 1.5:
            q = min(clip, bc, max(0, -depth.sell_orders.get(ask, 0)))
            if q > 0:
                orders.append(Order(VEX, ask, q))
                bc -= q
        if sc > 0 and bid >= fair + 1.5:
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

    def _trade_otm(
        self, state: TradingState, stored: dict,
        sym: str, vex_mid: float, gf: float
    ) -> List[Order]:
        depth = state.order_depths.get(sym)
        if depth is None:
            return []
        opt_mid = mid_price(depth)
        sprd = get_spread(depth)
        if opt_mid is None or sprd is None or sprd > 6:
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
        sensitivity = {"VEV_5200": 0.7, "VEV_5300": 0.6, "VEV_5400": 0.4, "VEV_5500": 0.2}
        fair += sensitivity.get(sym, 0.3) * vex_move + 0.3 * imb
        fair = max(fair, iv_val, 0.0)

        pos = state.position.get(sym, 0)
        lim = LIMITS[sym]
        bc = max(0, lim - pos)
        sc = max(0, lim + pos)

        base_clip = 14
        clip = max(3, int(base_clip * gf))
        if abs(pos) > 200:
            clip = max(3, clip // 3)
        elif abs(pos) > 120:
            clip = max(4, clip // 2)

        edge = 0.3 if opt_mid < 10 else 0.5

        orders: List[Order] = []
        if bc > 0 and ask <= fair - edge:
            q = min(clip, bc, max(0, -depth.sell_orders.get(ask, 0)))
            if q > 0:
                orders.append(Order(sym, ask, q))
                bc -= q
        if sc > 0 and bid >= fair + edge:
            q = min(clip, sc, max(0, depth.buy_orders.get(bid, 0)))
            if q > 0:
                orders.append(Order(sym, bid, -q))
                sc -= q

        if sprd <= 4:
            if bc > 0:
                px = max(0, min(bid + 1, int(math.floor(fair))))
                orders.append(Order(sym, px, min(max(1, clip // 2), bc)))
            if sc > 0:
                px = max(ask - 1, int(math.ceil(fair)))
                orders.append(Order(sym, px, -min(max(1, clip // 2), sc)))

        return orders
