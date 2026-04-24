"""
r3_b01_delta1_optiver
Optiver-style delta-1 market making for HYDROGEL_PACK + VELVETFRUIT_EXTRACT.
No vouchers. Full v3 stack ported from Round 2 best bot (338996_v3):
- Kalman filter fair-value tracking with microprice + depth-shift observation
- EMA-smoothed imbalance (alpha=0.4) reduces single-tick noise
- Dynamic take edge from rolling realized vol (adverse-selection protection)
- Imbalance-scaled take sizing (1.0-1.4x when signal agrees)
- Aggressive unwind mode at |pos| >= 150 (market-takes to reduce concentration)
- Reservation price (Avellaneda-Stoikov) + predictive quote shift
- Signal-driven passive sizing (50/20 at high confidence, 35/35 neutral)
Differentiator vs Amin's bots: no vouchers; best-in-class delta-1 execution.
"""
import json
import math
from datamodel import Order, TradingState

# ---- product config ----
PRODUCTS = {
    "HYDROGEL_PACK": {
        "limit": 200, "kq": 0.10, "kr": 12.0,
        "vol_base": 4.0, "half_spread": 2,
    },
    "VELVETFRUIT_EXTRACT": {
        "limit": 200, "kq": 0.05, "kr": 5.0,
        "vol_base": 2.0, "half_spread": 1,
    },
}

IMB_ALPHA  = 0.4   # EMA alpha for imbalance smoothing
IMB_GAIN   = 4.0   # gain: imbalance → quote shift ticks
IMB_CLIP   = 3.0   # max imbalance-driven shift
VOL_WINDOW = 10    # ticks for realized-vol estimate
UNWIND_THR = 150   # |pos| threshold for aggressive unwind
UNWIND_QTY = 12    # units per tick in unwind mode
RES_SIGMA2 = 2.0   # reservation-price risk-aversion parameter


def _clip(v, lo, hi):
    return min(max(v, lo), hi)


def microprice(od):
    if not od.buy_orders or not od.sell_orders:
        return None
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    t = bv + av
    return (bb * av + ba * bv) / t if t > 0 else (bb + ba) / 2.0


def depth_shift(od):
    """3-level book weighted average vs best-mid (capped at ±2 ticks)."""
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bids = sorted(od.buy_orders.items(), reverse=True)[:3]
    asks = sorted(od.sell_orders.items())[:3]
    bv = sum(q for _, q in bids)
    av = sum(-q for _, q in asks)
    if bv <= 0 or av <= 0:
        return 0.0
    wb = sum(p * q for p, q in bids) / bv
    wa = sum(p * (-q) for p, q in asks) / av
    bb0 = bids[0][0]
    ba0 = asks[0][0]
    return _clip((wb + wa) / 2.0 - (bb0 + ba0) / 2.0, -2.0, 2.0)


def kalman_update(sd, key, obs, q, r):
    fair = float(sd.get(key + "_f", 0.0))
    var  = float(sd.get(key + "_v", 25.0))
    if obs is None:
        var = min(var + q, 100.0)
        sd[key + "_f"] = fair
        sd[key + "_v"] = var
        return fair
    pv   = min(var + q, 100.0)
    k    = pv / (pv + r)
    fair = fair + k * (obs - fair)
    var  = (1.0 - k) * pv
    sd[key + "_f"] = fair
    sd[key + "_v"] = var
    return fair


class Trader:

    def run(self, state: TradingState):
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        result = {}

        for prod, cfg in PRODUCTS.items():
            od = state.order_depths.get(prod)
            if od is None:
                continue

            lim = cfg["limit"]
            pos = state.position.get(prod, 0)
            bb  = max(od.buy_orders)  if od.buy_orders  else None
            ba  = min(od.sell_orders) if od.sell_orders else None
            if bb is None and ba is None:
                continue

            raw_mid = (bb + ba) / 2.0 if (bb and ba) else float(bb or ba)
            micro   = microprice(od)
            ds      = depth_shift(od)
            ms      = _clip((micro - raw_mid), -2.0, 2.0) if micro else 0.0

            obs  = raw_mid + 0.4 * ms + 0.2 * ds
            fair = kalman_update(sd, prod, obs, cfg["kq"], cfg["kr"])
            if fair == 0.0:
                fair = raw_mid

            # rolling realized vol
            hk   = prod + "_h"
            hist = sd.get(hk, [])
            hist.append(obs)
            if len(hist) > VOL_WINDOW:
                hist = hist[-VOL_WINDOW:]
            sd[hk] = hist
            rvol = cfg["vol_base"]
            if len(hist) >= 4:
                ch   = [hist[i + 1] - hist[i] for i in range(len(hist) - 1)]
                ms2  = sum(c * c for c in ch) / len(ch)
                rvol = math.sqrt(ms2) if ms2 > 0 else cfg["vol_base"]

            # EMA imbalance
            imb_raw = 0.0
            if bb and ba:
                bv = od.buy_orders[bb]
                av = -od.sell_orders[ba]
                t  = bv + av
                imb_raw = (bv - av) / t if t > 0 else 0.0
            ek      = prod + "_ie"
            imb_ema = IMB_ALPHA * imb_raw + (1.0 - IMB_ALPHA) * float(sd.get(ek, 0.0))
            sd[ek]  = imb_ema

            spread = (ba - bb) if (bb and ba) else None

            imb_shift = _clip(IMB_GAIN * imb_ema, -IMB_CLIP, IMB_CLIP)
            if spread and (spread <= 4 or spread >= 10):
                pred = 0.45 * ms + 0.20 * ds + imb_shift
            else:
                pred = 0.35 * ms + 0.05 * ds + 0.90 * imb_shift

            # reservation price + predictive shift
            res_px = fair - (pos * RES_SIGMA2 / lim)
            qfair  = res_px + pred

            # dynamic take edge
            vr        = rvol / cfg["vol_base"]
            va        = _clip((vr - 1.0) * 0.8, -0.5, 1.0)
            dyn_edge  = 1.5 + va + (1 if abs(pos) > 0.75 * lim else 0)
            if spread and 4 < spread < 10:
                dyn_edge += 0.5

            buy_thr  = int(round(qfair - dyn_edge))
            sell_thr = int(round(qfair + dyn_edge))

            orders = []
            bu = 0
            su = 0

            def bcap():
                return max(0, lim - pos - bu)

            def scap():
                return max(0, lim + pos - su)

            # aggressive takes (buy side)
            for ask in sorted(od.sell_orders):
                if bcap() <= 0 or ask > buy_thr:
                    break
                aq    = -od.sell_orders[ask]
                bt    = 15 if (buy_thr - ask) < 2 else 25
                bull  = max(0.0, imb_ema)
                tq    = min(aq, int(bt * (1.0 + 0.35 * bull)))
                if pos + bu > int(0.65 * lim):
                    tq = min(tq, 8)
                q = min(tq, bcap())
                if q > 0:
                    orders.append(Order(prod, ask, q))
                    bu += q

            # aggressive takes (sell side)
            for bid in sorted(od.buy_orders, reverse=True):
                if scap() <= 0 or bid < sell_thr:
                    break
                bq    = od.buy_orders[bid]
                bt    = 15 if (bid - sell_thr) < 2 else 25
                bear  = max(0.0, -imb_ema)
                tq    = min(bq, int(bt * (1.0 + 0.35 * bear)))
                if pos - su < -int(0.65 * lim):
                    tq = min(tq, 8)
                q = min(tq, scap())
                if q > 0:
                    orders.append(Order(prod, bid, -q))
                    su += q

            # aggressive unwind at extremes
            if pos >= UNWIND_THR and bb and scap() > 0:
                uq = min(UNWIND_QTY, pos - int(0.6 * lim), scap())
                if uq > 0:
                    orders.append(Order(prod, bb, -uq))
                    su += uq
            elif pos <= -UNWIND_THR and ba and bcap() > 0:
                uq = min(UNWIND_QTY, -pos - int(0.6 * lim), bcap())
                if uq > 0:
                    orders.append(Order(prod, ba, uq))
                    bu += uq

            # passive quotes
            half   = cfg["half_spread"] + (1 if abs(pos) > int(0.65 * lim) else 0)
            if abs(ms) > 1.5:
                half += 1
            bid_px = int(round(qfair - half))
            ask_px = int(round(qfair + half))
            if bb:
                bid_px = min(bid_px, bb + 1)
            if ba:
                ask_px = max(ask_px, ba - 1)
            if ba and bid_px >= ba:
                bid_px = ba - 1
            if bb and ask_px <= bb:
                ask_px = bb + 1

            # signal-driven sizing
            bsz = 35
            ssz = 35
            if pred > 3.0:
                bsz, ssz = 50, 20
            elif pred > 1.5:
                bsz, ssz = 42, 28
            elif pred < -3.0:
                bsz, ssz = 20, 50
            elif pred < -1.5:
                bsz, ssz = 28, 42

            # soft inventory correction (signal dominates)
            if pos < -20 and pred > -2.5:
                bsz = max(bsz, 50)
                ssz = min(ssz, 15)
            elif pos > 20 and pred < 2.5:
                bsz = min(bsz, 15)
                ssz = max(ssz, 50)

            # hard cap at high inventory
            if abs(pos) > int(0.8 * lim):
                if pos > 0:
                    bsz, ssz = 8, 60
                else:
                    bsz, ssz = 60, 8

            if bcap() > 0 and (ba is None or bid_px < ba):
                q = min(bsz, bcap())
                if q > 0:
                    orders.append(Order(prod, bid_px, q))
            if scap() > 0 and (bb is None or ask_px > bb):
                q = min(ssz, scap())
                if q > 0:
                    orders.append(Order(prod, ask_px, -q))

            result[prod] = orders

        return result, 0, json.dumps(sd)
