"""
W3-24: Delta1 + ITM + VEV_5300 Selective Stack
================================================
The "best stack" — combines all proven profitable components:
  1. HYDROGEL MM (primary PnL: +550-886 in isolation)
  2. VEX Kalman MM (delta-1 anchor)
  3. ITM 4000/4500 intrinsic residual (proven +1,409 combined)
  4. VEV_5300 sell-bias overlay (NEW: market trades ~2.8 ticks above Bachelier)

Key insight on VEV_5300:
  - EDA shows positive smile bias: market consistently overprices vs Bachelier
  - Strategy: sell VEV_5300 when overpriced vs bias-adjusted Bachelier fair
  - Tiny position cap (15 units) to limit delta exposure
  - Bachelier σ = 1160 (CORRECT — learned from C06 bug)
  - TTE = 5d start, decays dynamically

This is the flagship bot for this wave.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────
# Math
# ─────────────────────────────────────────────────

def norm_cdf(x):
    if x < -8.0: return 0.0
    if x > 8.0: return 1.0
    a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
    p = 0.3275911
    s = 1.0
    if x < 0: s = -1.0; x = -x
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * math.exp(-x * x / 2.0)
    return 0.5 * (1.0 + s * y)


def norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def bachelier_call(S, K, T, sig):
    if T <= 0 or sig <= 0: return max(S - K, 0.0)
    vt = sig * math.sqrt(T)
    if vt < 1e-12: return max(S - K, 0.0)
    d = (S - K) / vt
    return (S - K) * norm_cdf(d) + vt * norm_pdf(d)


def bachelier_delta(S, K, T, sig):
    if T <= 0 or sig <= 0: return 1.0 if S > K else 0.0
    vt = sig * math.sqrt(T)
    if vt < 1e-12: return 1.0 if S > K else 0.0
    return norm_cdf((S - K) / vt)


# ─────────────────────────────────────────────────
# Params
# ─────────────────────────────────────────────────

HG_LIMIT = 200; VEX_LIMIT = 200; ITM_LIMIT = 300; V53_LIMIT = 300
HG_CAP = 130; VEX_CAP = 120
V53_CAP = 15            # tiny: limit delta exposure

# HYDROGEL
HG_HALF = 3; HG_TEDGE = 3; HG_PSZ = 25; HG_TSZ = 18
HG_GAMMA = 2.0; HG_UW_THR = 90; HG_UW_Q = 20

# VEX
VEX_HALF = 2; VEX_TEDGE = 2; VEX_PSZ = 15; VEX_TSZ = 12
VEX_GAMMA = 2.0
KQ = 0.1; KR = 10.0

# ITM
ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}
ITM_HS = {"VEV_4000": 9, "VEV_4500": 7}
ITM_TAKE = 10; ITM_PSZ = 30; EXTR_ALPHA = 0.005

# VEV_5300 sell overlay
SIGMA = 1160.0
SIGMA_EMA = 0.03
TTE_START = 5.0
TICKS_PER_DAY = 20000
BIAS_5300 = 2.8         # market trades this much above Bachelier
BIAS_ALPHA = 0.005
V53_ENTRY = 2.0         # sell when deviation > entry
V53_SELL_SIZE = 5
V53_OFFSET = 3


def get_microprice(od):
    if not od.buy_orders or not od.sell_orders: return None
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    t = bv + av
    return (bb * av + ba * bv) / t if t > 0 else (bb + ba) / 2.0


def get_imbalance(od):
    if not od.buy_orders or not od.sell_orders: return 0.0
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    t = bv + av
    return (bv - av) / t if t > 0 else 0.0


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sd = {}
        if state.traderData:
            try: sd = json.loads(state.traderData)
            except: sd = {}

        tick = sd.get("t", 0) + 1
        sd["t"] = tick
        sigma = sd.get("sig", SIGMA)
        bias53 = sd.get("b53", BIAS_5300)

        tte_days = max(TTE_START - tick / TICKS_PER_DAY, 0.5)
        tte_years = tte_days / 365.0

        # ══════════════════════════════════════════
        # HYDROGEL MM
        # ══════════════════════════════════════════
        hg_od = state.order_depths.get("HYDROGEL_PACK")
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get("HYDROGEL_PACK", 0)
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - HG_GAMMA * (hg_pos / HG_CAP) + clamp(2.0 * hg_imb, -3, 3)

                hg_orders = []
                hg_b, hg_s = 0, 0

                def hgbr():
                    return max(0, min(HG_CAP, HG_LIMIT) - hg_pos - hg_b)
                def hgsr():
                    return max(0, min(HG_CAP, HG_LIMIT) + hg_pos - hg_s)

                for ap in sorted(hg_od.sell_orders):
                    if hgbr() <= 0 or ap > hg_qfair - HG_TEDGE: break
                    q = min(-hg_od.sell_orders[ap], HG_TSZ, hgbr())
                    if q > 0: hg_orders.append(Order("HYDROGEL_PACK", ap, q)); hg_b += q

                for bp in sorted(hg_od.buy_orders, reverse=True):
                    if hgsr() <= 0 or bp < hg_qfair + HG_TEDGE: break
                    q = min(hg_od.buy_orders[bp], HG_TSZ, hgsr())
                    if q > 0: hg_orders.append(Order("HYDROGEL_PACK", bp, -q)); hg_s += q

                if hg_pos >= HG_UW_THR and hgsr() > 0:
                    uq = min(HG_UW_Q, hgsr())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uq)); hg_s += uq
                elif hg_pos <= -HG_UW_THR and hgbr() > 0:
                    uq = min(HG_UW_Q, hgbr())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uq)); hg_b += uq

                half = HG_HALF + (1 if abs(hg_pos) > HG_CAP * 0.6 else 0)
                hbp = int(round(hg_qfair - half))
                hap = int(round(hg_qfair + half))
                if hbp >= hg_ba: hbp = hg_ba - 1
                if hap <= hg_bb: hap = hg_bb + 1
                psz = HG_PSZ
                bsz = max(3, psz - int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz + int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                ssz = max(3, psz + int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz - int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                if bq > 0: hg_orders.append(Order("HYDROGEL_PACK", hbp, bq))
                if sq > 0: hg_orders.append(Order("HYDROGEL_PACK", hap, -sq))
                result["HYDROGEL_PACK"] = hg_orders

        # ══════════════════════════════════════════
        # VEX Kalman MM
        # ══════════════════════════════════════════
        vex_od = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_fair = None

        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get("VELVETFRUIT_EXTRACT", 0)

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]
            vfv = round(vex_fair)
            adj = vex_fair - VEX_GAMMA * (vex_pos / VEX_CAP)

            vex_orders = []
            vb, vs = 0, 0
            def vbr(): return max(0, min(VEX_CAP, VEX_LIMIT) - vex_pos - vb)
            def vsr(): return max(0, min(VEX_CAP, VEX_LIMIT) + vex_pos - vs)

            if vex_ba <= vfv - VEX_TEDGE:
                q = min(-vex_od.sell_orders[vex_ba], VEX_TSZ, vbr())
                if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, q)); vb += q
            if vex_bb >= vfv + VEX_TEDGE:
                q = min(vex_od.buy_orders[vex_bb], VEX_TSZ, vsr())
                if q > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -q)); vs += q

            bp = int(round(adj - VEX_HALF)); ap = int(round(adj + VEX_HALF))
            if bp >= vex_ba: bp = vex_ba - 1
            if ap <= vex_bb: ap = vex_bb + 1
            bq, sq = min(VEX_PSZ, vbr()), min(VEX_PSZ, vsr())
            if bq > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", bp, bq))
            if sq > 0: vex_orders.append(Order("VELVETFRUIT_EXTRACT", ap, -sq))
            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ══════════════════════════════════════════
        # ITM Voucher Residual
        # ══════════════════════════════════════════
        if vex_fair is not None:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders: continue
                bb, ba = max(od.buy_orders), min(od.sell_orders)
                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)
                intrinsic = max(0.0, vex_fair - strike)
                curr_extr = max(0.0, v_mid - intrinsic)
                st = sd.setdefault(sym, {"ema": 0.01})
                ema = EXTR_ALPHA * curr_extr + (1 - EXTR_ALPHA) * st["ema"]
                st["ema"] = ema
                fair = intrinsic + ema
                half_s = ITM_HS[sym]

                orders = []
                ib, is_ = 0, 0
                if ba < fair - ITM_TAKE:
                    q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                    if q > 0: orders.append(Order(sym, ba, q)); ib += q
                if bb > fair + ITM_TAKE:
                    q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                    if q > 0: orders.append(Order(sym, bb, -q)); is_ += q

                bid_px = int(round(fair - half_s)); ask_px = int(round(fair + half_s))
                if bid_px >= ba: bid_px = ba - 1
                if ask_px <= bb: ask_px = bb + 1
                dev = curr_extr - ema
                b_sz = max(2, min(ITM_PSZ + int(5 * (-dev)), ITM_LIMIT - pos - ib))
                a_sz = max(2, min(ITM_PSZ + int(5 * dev), ITM_LIMIT + pos - is_))
                if b_sz > 0 and bid_px > 0: orders.append(Order(sym, bid_px, b_sz))
                if a_sz > 0 and ask_px > 0: orders.append(Order(sym, ask_px, -a_sz))
                result[sym] = orders

        # ══════════════════════════════════════════
        # VEV_5300 Sell-Bias Overlay
        # ══════════════════════════════════════════
        if vex_fair is not None:
            sym53 = "VEV_5300"
            od53 = state.order_depths.get(sym53)
            if od53 and od53.buy_orders and od53.sell_orders:
                bb53, ba53 = max(od53.buy_orders), min(od53.sell_orders)
                spread53 = ba53 - bb53
                if 1 <= spread53 <= 15:
                    pos53 = state.position.get(sym53, 0)
                    v53_mid = (bb53 + ba53) / 2.0

                    # Bachelier fair for 5300
                    bach53 = bachelier_call(vex_fair, 5300, tte_years, sigma)
                    intrinsic53 = max(vex_fair - 5300, 0.0)
                    if bach53 < intrinsic53:
                        bach53 = intrinsic53

                    # Track smile bias
                    raw_resid = v53_mid - bach53
                    bias53 = BIAS_ALPHA * raw_resid + (1 - BIAS_ALPHA) * bias53
                    sd["b53"] = bias53

                    adj_fair53 = bach53 + bias53
                    deviation = raw_resid - bias53

                    orders53 = []
                    # Sell when overpriced (deviation > entry threshold)
                    if deviation > V53_ENTRY and pos53 > -V53_CAP:
                        for bid_p in sorted(od53.buy_orders, reverse=True):
                            if bid_p < adj_fair53 + 0.5: break
                            avail = od53.buy_orders[bid_p]
                            q = min(avail, V53_SELL_SIZE, V53_CAP + pos53)
                            if q > 0:
                                orders53.append(Order(sym53, bid_p, -q))

                    # Buy back when underpriced (deviation < -entry)
                    if deviation < -V53_ENTRY and pos53 < V53_CAP:
                        for ask_p in sorted(od53.sell_orders):
                            if ask_p > adj_fair53 - 0.5: break
                            avail = -od53.sell_orders[ask_p]
                            q = min(avail, V53_SELL_SIZE, V53_CAP - pos53)
                            if q > 0:
                                orders53.append(Order(sym53, ask_p, q))

                    # Passive quotes with inventory skew (bias toward reducing position)
                    inv_adj = -1.5 * (pos53 / V53_LIMIT)
                    qf = adj_fair53 + inv_adj
                    bp53 = int(round(qf - V53_OFFSET))
                    ap53 = int(round(qf + V53_OFFSET))
                    if bp53 >= ba53: bp53 = ba53 - 1
                    if ap53 <= bb53: ap53 = bb53 + 1

                    bq53 = min(3, V53_CAP - pos53, V53_LIMIT - pos53) if pos53 < V53_CAP else 0
                    sq53 = min(3, V53_CAP + pos53, V53_LIMIT + pos53) if pos53 > -V53_CAP else 0
                    if bq53 > 0 and bp53 > 0:
                        orders53.append(Order(sym53, bp53, bq53))
                    if sq53 > 0 and ap53 > 0:
                        orders53.append(Order(sym53, ap53, -sq53))

                    result[sym53] = orders53

        # ── Vol calibration ──
        if vex_fair is not None:
            for cal_sym in ["VEV_5200", "VEV_5300"]:
                cod = state.order_depths.get(cal_sym)
                if cod and cod.buy_orders and cod.sell_orders:
                    cmid = (max(cod.buy_orders) + min(cod.sell_orders)) / 2.0
                    if cmid > 0:
                        K = 5200 if cal_sym == "VEV_5200" else 5300
                        intr = max(vex_fair - K, 0.0)
                        if cmid > intr + 0.01:
                            lo, hi = 10.0, 5000.0
                            for _ in range(40):
                                m = (lo + hi) * 0.5
                                if bachelier_call(vex_fair, K, tte_years, m) < cmid: lo = m
                                else: hi = m
                                if hi - lo < 1.0: break
                            iv = (lo + hi) * 0.5
                            if 200 < iv < 4000:
                                sigma = SIGMA_EMA * iv + (1 - SIGMA_EMA) * sigma
            sd["sig"] = sigma

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
