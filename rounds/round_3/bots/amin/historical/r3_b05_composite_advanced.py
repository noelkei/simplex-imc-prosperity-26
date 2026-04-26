"""
r3_b05_composite_advanced
C01+C02+C03 composite with Optiver-v3 delta-1 improvements.
Same product scope as Amin's candidate_c06_composite_base.py but with:
- Delta-1 leg (HYDROGEL + VEX) upgraded to Round-2-v3 level:
  Kalman fair value, EMA imbalance (alpha=0.4), microprice + depth shift,
  dynamic take edge from realized vol, imbalance-scaled sizing, unwind mode
- Voucher leg (VEV_5000-5300): faster sigma EMA (alpha=0.15 vs Amin's 0.10),
  tighter entry threshold (2.5 vs Amin's 3.0), imbalance lean on passive quotes
- Both legs share VEX Kalman fair as voucher anchor
"""
import json
import math
from datamodel import Order, TradingState


# ---- math helpers ----

def norm_cdf(x: float) -> float:
    if x < -8.0:
        return 0.0
    if x > 8.0:
        return 1.0
    a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
    sign = 1.0
    if x < 0:
        sign = -1.0
        x = -x
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + sign * y)


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bachelier_call(S: float, K: float, T: float, sig: float) -> float:
    if T <= 0 or sig <= 0:
        return max(S - K, 0.0)
    vt = sig * math.sqrt(T)
    if vt < 1e-12:
        return max(S - K, 0.0)
    d = (S - K) / vt
    return (S - K) * norm_cdf(d) + vt * norm_pdf(d)


def get_mid(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_spread(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    return min(od.sell_orders) - max(od.buy_orders)


def get_imbalance(od) -> float:
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = abs(od.sell_orders[ba])
    return (bv - av) / (bv + av) if bv + av > 0 else 0.0


def clamp_qty(qty: int, pos: int, limit: int) -> int:
    if qty > 0:
        return max(0, min(qty, limit - pos))
    if qty < 0:
        return min(0, max(qty, -(limit + pos)))
    return 0


def _clip(v, lo, hi):
    return min(max(v, lo), hi)


def microprice(od) -> float | None:
    if not od.buy_orders or not od.sell_orders:
        return None
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    t = bv + av
    return (bb * av + ba * bv) / t if t > 0 else (bb + ba) / 2.0


def depth_shift(od) -> float:
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
    return _clip((wb + wa) / 2.0 - (bids[0][0] + asks[0][0]) / 2.0, -2.0, 2.0)


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


# ---- parameters ----

SIGMA_DEFAULT = 95.0
SIGMA_ALPHA   = 0.15   # faster than Amin's 0.10 — more responsive
TTE_YEARS     = 5 / 365.0
VOL_WINDOW    = 10
UNWIND_THR    = 150
UNWIND_QTY    = 12
IMB_ALPHA     = 0.4
IMB_GAIN      = 4.0
IMB_CLIP      = 3.0

DELTA1_CFG = {
    "HYDROGEL_PACK":       {"limit": 200, "kq": 0.10, "kr": 12.0, "vol_base": 4.0, "half_spread": 2},
    "VELVETFRUIT_EXTRACT": {"limit": 200, "kq": 0.05, "kr": 5.0,  "vol_base": 2.0, "half_spread": 1},
}

VOUCHER_PRODUCTS = {
    "VEV_5000": (5000, 300),
    "VEV_5100": (5100, 300),
    "VEV_5200": (5200, 300),
    "VEV_5300": (5300, 300),
}
ENTRY_THRESH   = 2.5   # tighter than Amin's 3.0
EXIT_THRESH    = 0.5
V_MM_OFFSET    = 2
MAX_V_SPREAD   = 20
V_INV_SKEW     = 1.2
IMB_LEAN_V     = 1
SYMS_BY_STRIKE = sorted(VOUCHER_PRODUCTS, key=lambda s: VOUCHER_PRODUCTS[s][0])


class Trader:

    def run(self, state: TradingState):
        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        sigma_abs = sd.get("sigma_abs", SIGMA_DEFAULT)
        result    = {}

        # ---- delta-1 (Optiver-v3 style) ----
        vex_kalman_fair = None
        for prod, cfg in DELTA1_CFG.items():
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
            obs     = raw_mid + 0.4 * ms + 0.2 * ds

            fair = kalman_update(sd, prod, obs, cfg["kq"], cfg["kr"])
            if fair == 0.0:
                fair = raw_mid

            # capture VEX Kalman fair for voucher pricing
            if prod == "VELVETFRUIT_EXTRACT":
                vex_kalman_fair = fair

            # realized vol
            hk   = prod + "_h"
            hist = sd.get(hk, [])
            hist.append(obs)
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
                bv = od.buy_orders[bb]; av = -od.sell_orders[ba]; t = bv + av
                imb_raw = (bv - av) / t if t > 0 else 0.0
            ek      = prod + "_ie"
            imb_ema = IMB_ALPHA * imb_raw + (1.0 - IMB_ALPHA) * float(sd.get(ek, 0.0))
            sd[ek]  = imb_ema

            spread = (ba - bb) if (bb and ba) else None
            imb_sh = _clip(IMB_GAIN * imb_ema, -IMB_CLIP, IMB_CLIP)
            if spread and (spread <= 4 or spread >= 10):
                pred = 0.45 * ms + 0.20 * ds + imb_sh
            else:
                pred = 0.35 * ms + 0.05 * ds + 0.90 * imb_sh

            res_px = fair - (pos * 2.0 / lim)
            qfair  = res_px + pred

            vr       = rvol / cfg["vol_base"]
            dyn_edge = 1.5 + _clip((vr - 1.0) * 0.8, -0.5, 1.0) + (1 if abs(pos) > 0.75 * lim else 0)
            buy_thr  = int(round(qfair - dyn_edge))
            sell_thr = int(round(qfair + dyn_edge))

            orders = []
            bu = 0
            su = 0

            def bcap(l=lim, p=pos): return max(0, l - p - bu)
            def scap(l=lim, p=pos): return max(0, l + p - su)

            for ask in sorted(od.sell_orders):
                if bcap() <= 0 or ask > buy_thr:
                    break
                aq   = -od.sell_orders[ask]
                bull = max(0.0, imb_ema)
                tq   = min(aq, int((15 if buy_thr - ask < 2 else 25) * (1.0 + 0.35 * bull)))
                if pos + bu > int(0.65 * lim):
                    tq = min(tq, 8)
                q = min(tq, bcap())
                if q > 0:
                    orders.append(Order(prod, ask, q))
                    bu += q

            for bid in sorted(od.buy_orders, reverse=True):
                if scap() <= 0 or bid < sell_thr:
                    break
                bq   = od.buy_orders[bid]
                bear = max(0.0, -imb_ema)
                tq   = min(bq, int((15 if bid - sell_thr < 2 else 25) * (1.0 + 0.35 * bear)))
                if pos - su < -int(0.65 * lim):
                    tq = min(tq, 8)
                q = min(tq, scap())
                if q > 0:
                    orders.append(Order(prod, bid, -q))
                    su += q

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

            half   = cfg["half_spread"] + (1 if abs(pos) > int(0.65 * lim) else 0)
            bid_px = int(round(qfair - half))
            ask_px = int(round(qfair + half))
            if bb: bid_px = min(bid_px, bb + 1)
            if ba: ask_px = max(ask_px, ba - 1)
            if ba and bid_px >= ba: bid_px = ba - 1
            if bb and ask_px <= bb: ask_px = bb + 1

            bsz = ssz = 35
            if pred > 3.0:   bsz, ssz = 50, 20
            elif pred > 1.5: bsz, ssz = 42, 28
            elif pred < -3.0: bsz, ssz = 20, 50
            elif pred < -1.5: bsz, ssz = 28, 42
            if pos < -20 and pred > -2.5: bsz = max(bsz, 50); ssz = min(ssz, 15)
            elif pos > 20 and pred < 2.5: bsz = min(bsz, 15); ssz = max(ssz, 50)
            if abs(pos) > int(0.8 * lim):
                if pos > 0: bsz, ssz = 8, 60
                else:       bsz, ssz = 60, 8

            if bcap() > 0 and (ba is None or bid_px < ba):
                q = min(bsz, bcap())
                if q > 0: orders.append(Order(prod, bid_px, q))
            if scap() > 0 and (bb is None or ask_px > bb):
                q = min(ssz, scap())
                if q > 0: orders.append(Order(prod, ask_px, -q))

            result[prod] = orders

        # ---- update sigma_abs ----
        prev_vex   = sd.get("prev_vex")
        vex_mid_od = get_mid(state.order_depths["VELVETFRUIT_EXTRACT"]) \
            if "VELVETFRUIT_EXTRACT" in state.order_depths else None
        if vex_mid_od is not None and prev_vex is not None:
            move      = abs(vex_mid_od - prev_vex)
            daily_vol = move * math.sqrt(1000)
            sigma_abs = SIGMA_ALPHA * daily_vol + (1.0 - SIGMA_ALPHA) * sigma_abs

        # ---- voucher leg ----
        # use Kalman VEX fair if available; fallback to book mid
        anchor = vex_kalman_fair if vex_kalman_fair is not None else vex_mid_od
        if anchor is not None:
            fairs = {}
            for sym, (strike, _) in VOUCHER_PRODUCTS.items():
                fv        = bachelier_call(anchor, strike, TTE_YEARS, sigma_abs)
                fairs[sym] = max(fv, max(anchor - strike, 0.0))

            # monotonicity guardrail
            surface_ok = True
            for i in range(len(SYMS_BY_STRIKE) - 1):
                if fairs[SYMS_BY_STRIKE[i]] < fairs[SYMS_BY_STRIKE[i + 1]] - 0.5:
                    surface_ok = False
                    break

            for sym in SYMS_BY_STRIKE:
                if sym not in state.order_depths:
                    continue
                od     = state.order_depths[sym]
                mid    = get_mid(od)
                spread = get_spread(od)
                if mid is None or spread is None or spread > MAX_V_SPREAD:
                    continue

                strike, limit = VOUCHER_PRODUCTS[sym]
                pos           = state.position.get(sym, 0)
                fair          = fairs[sym]
                imb           = get_imbalance(od)

                residual = mid - fair
                inv_adj  = -V_INV_SKEW * (pos / limit)
                adj_fair = fair + inv_adj

                orders = []

                if abs(residual) > ENTRY_THRESH and surface_ok:
                    if residual < -ENTRY_THRESH:
                        for ask in sorted(od.sell_orders):
                            if ask < adj_fair - EXIT_THRESH:
                                q = clamp_qty(-od.sell_orders[ask], pos, limit)
                                if q > 0:
                                    orders.append(Order(sym, ask, q))
                                    pos += q
                    elif residual > ENTRY_THRESH:
                        for bid in sorted(od.buy_orders, reverse=True):
                            if bid > adj_fair + EXIT_THRESH:
                                q = clamp_qty(-od.buy_orders[bid], pos, limit)
                                if q < 0:
                                    orders.append(Order(sym, bid, q))
                                    pos += q

                lean  = round(IMB_LEAN_V * imb)
                psz   = max(1, limit // 12)
                bpx   = int(round(adj_fair - V_MM_OFFSET + lean))
                apx   = int(round(adj_fair + V_MM_OFFSET + lean))

                q = clamp_qty(psz, pos, limit)
                if q > 0 and bpx > 0:
                    orders.append(Order(sym, bpx, q))
                q = clamp_qty(-psz, pos, limit)
                if q < 0 and apx > 0:
                    orders.append(Order(sym, apx, q))

                result[sym] = orders

        # ---- persist ----
        sd["sigma_abs"] = sigma_abs
        if vex_mid_od is not None:
            sd["prev_vex"] = vex_mid_od

        return result, 0, json.dumps(sd)
