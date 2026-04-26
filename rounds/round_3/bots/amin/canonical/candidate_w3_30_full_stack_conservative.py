"""
W3-30: Full Stack Conservative
================================
Everything that works, assembled conservatively with tight limits and
aggressive end-of-game unwind. The kitchen-sink bot.

Components:
  1. HYDROGEL MM (primary PnL, cap=100 conservative)
  2. VEX Kalman MM (secondary PnL, cap=80)
  3. ITM 4000/4500 intrinsic residual (passive, small size)
  4. VEV_5300 sell-bias overlay (tiny, cap=10)
  5. Portfolio delta monitoring (no active hedging, just position caps)
  6. Phased risk: 3 phases (aggressive/standard/unwind)

Key design: every component has been individually validated as profitable
or at worst flat. Combined with conservative caps to prevent any single
component from dominating PnL.

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


# ─────────────────────────────────────────────────
# Params
# ─────────────────────────────────────────────────
HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200; VEX_LIMIT = 200; ITM_LIMIT = 300; V_LIMIT = 300

ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}
ITM_HS = {"VEV_4000": 9, "VEV_4500": 7}
EXTR_ALPHA = 0.005

SIGMA = 1160.0; SIGMA_EMA = 0.03
TTE_START = 5.0; TICKS_PER_DAY = 20000
BIAS_5300_INIT = 2.8; BIAS_ALPHA = 0.005

PHASE1_END = 30000; PHASE2_END = 80000
TOTAL = 100000; STOP_NEW = 95000

KQ = 0.1; KR = 10.0


def get_phase(tick):
    if tick <= PHASE1_END:
        return {
            "hg_cap": 120, "hg_half": 2, "hg_te": 2, "hg_ps": 28, "hg_ts": 20, "hg_g": 1.5, "hg_uw": 90,
            "vex_cap": 100, "vex_half": 1, "vex_te": 1, "vex_ps": 15, "vex_ts": 12, "vex_g": 1.5,
            "itm_ps": 30, "v53_cap": 12, "v53_sz": 4,
        }
    elif tick <= PHASE2_END:
        return {
            "hg_cap": 80, "hg_half": 3, "hg_te": 3, "hg_ps": 20, "hg_ts": 14, "hg_g": 2.5, "hg_uw": 55,
            "vex_cap": 80, "vex_half": 2, "vex_te": 2, "vex_ps": 10, "vex_ts": 8, "vex_g": 2.5,
            "itm_ps": 22, "v53_cap": 8, "v53_sz": 3,
        }
    else:
        prog = (tick - PHASE2_END) / (TOTAL - PHASE2_END)
        f = max(0.0, 1.0 - prog * 1.3)
        return {
            "hg_cap": max(5, int(40*f)), "hg_half": 4, "hg_te": 4, "hg_ps": max(3, int(10*f)),
            "hg_ts": max(3, int(7*f)), "hg_g": 4.0, "hg_uw": max(3, int(20*f)),
            "vex_cap": max(5, int(25*f)), "vex_half": 3, "vex_te": 3, "vex_ps": max(2, int(5*f)),
            "vex_ts": max(2, int(4*f)), "vex_g": 4.0,
            "itm_ps": max(2, int(8*f)), "v53_cap": 0, "v53_sz": 0,
        }


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
        pp = get_phase(tick)
        no_new = tick > STOP_NEW
        sigma = sd.get("sig", SIGMA)
        bias53 = sd.get("b53", BIAS_5300_INIT)
        tte_d = max(TTE_START - tick / TICKS_PER_DAY, 0.5)
        tte_y = tte_d / 365.0

        # ══════════════════════════════════════════
        # 1. HYDROGEL MM
        # ══════════════════════════════════════════
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get(HG, 0)
                hg_cap = pp["hg_cap"]
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qf = hg_micro - pp["hg_g"] * (hg_pos / max(1, hg_cap)) + clamp(2.0 * hg_imb, -3, 3)

                ho = []; hb, hs = 0, 0
                def hgbr(): return max(0, min(hg_cap, HG_LIMIT) - hg_pos - hb)
                def hgsr(): return max(0, min(hg_cap, HG_LIMIT) + hg_pos - hs)

                if not no_new:
                    for ap in sorted(hg_od.sell_orders):
                        if hgbr() <= 0 or ap > hg_qf - pp["hg_te"]: break
                        q = min(-hg_od.sell_orders[ap], pp["hg_ts"], hgbr())
                        if q > 0: ho.append(Order(HG, ap, q)); hb += q
                    for bp in sorted(hg_od.buy_orders, reverse=True):
                        if hgsr() <= 0 or bp < hg_qf + pp["hg_te"]: break
                        q = min(hg_od.buy_orders[bp], pp["hg_ts"], hgsr())
                        if q > 0: ho.append(Order(HG, bp, -q)); hs += q

                if hg_pos >= pp["hg_uw"] and hgsr() > 0:
                    uq = min(20, hgsr()); ho.append(Order(HG, hg_bb, -uq)); hs += uq
                elif hg_pos <= -pp["hg_uw"] and hgbr() > 0:
                    uq = min(20, hgbr()); ho.append(Order(HG, hg_ba, uq)); hb += uq

                # Phase 3 forced unwind
                if tick > PHASE2_END and abs(hg_pos) > 5:
                    if hg_pos > 0 and hgsr() > 0:
                        uw = min(25, hg_pos, hgsr()); ho.append(Order(HG, hg_bb, -uw)); hs += uw
                    elif hg_pos < 0 and hgbr() > 0:
                        uw = min(25, -hg_pos, hgbr()); ho.append(Order(HG, hg_ba, uw)); hb += uw

                if not no_new:
                    half = pp["hg_half"] + (1 if abs(hg_pos) > hg_cap * 0.6 else 0)
                    hbp = int(round(hg_qf - half)); hap = int(round(hg_qf + half))
                    if hbp >= hg_ba: hbp = hg_ba - 1
                    if hap <= hg_bb: hap = hg_bb + 1
                    psz = pp["hg_ps"]
                    bsz = max(3, psz - int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz + int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                    ssz = max(3, psz + int(hg_pos * 0.2)) if hg_pos > 0 else max(3, psz - int(-hg_pos * 0.2)) if hg_pos < 0 else psz
                    bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                    if bq > 0: ho.append(Order(HG, hbp, bq))
                    if sq > 0: ho.append(Order(HG, hap, -sq))

                result[HG] = ho

        # ══════════════════════════════════════════
        # 2. VEX Kalman MM
        # ══════════════════════════════════════════
        vex_od = state.order_depths.get(VEX)
        vex_fair = None
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get(VEX, 0)
            vex_cap = pp["vex_cap"]

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR)
            kst["f"] += k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]
            vfv = round(vex_fair)
            adj = vex_fair - pp["vex_g"] * (vex_pos / max(1, vex_cap))

            vo = []; vb, vs = 0, 0
            def vbr(): return max(0, min(vex_cap, VEX_LIMIT) - vex_pos - vb)
            def vsr(): return max(0, min(vex_cap, VEX_LIMIT) + vex_pos - vs)

            if not no_new:
                if vex_ba <= vfv - pp["vex_te"]:
                    q = min(-vex_od.sell_orders[vex_ba], pp["vex_ts"], vbr())
                    if q > 0: vo.append(Order(VEX, vex_ba, q)); vb += q
                if vex_bb >= vfv + pp["vex_te"]:
                    q = min(vex_od.buy_orders[vex_bb], pp["vex_ts"], vsr())
                    if q > 0: vo.append(Order(VEX, vex_bb, -q)); vs += q

            # Phase 3 VEX unwind
            if tick > PHASE2_END and abs(vex_pos) > 5:
                if vex_pos > 0 and vsr() > 0:
                    uw = min(20, vex_pos, vsr()); vo.append(Order(VEX, vex_bb, -uw)); vs += uw
                elif vex_pos < 0 and vbr() > 0:
                    uw = min(20, -vex_pos, vbr()); vo.append(Order(VEX, vex_ba, uw)); vb += uw

            if not no_new:
                bp = int(round(adj - pp["vex_half"])); ap = int(round(adj + pp["vex_half"]))
                if bp >= vex_ba: bp = vex_ba - 1
                if ap <= vex_bb: ap = vex_bb + 1
                bq, sq = min(pp["vex_ps"], vbr()), min(pp["vex_ps"], vsr())
                if bq > 0: vo.append(Order(VEX, bp, bq))
                if sq > 0: vo.append(Order(VEX, ap, -sq))
            result[VEX] = vo

        # ══════════════════════════════════════════
        # 3. ITM Voucher Residual
        # ══════════════════════════════════════════
        if vex_fair is not None:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders: continue
                bb, ba = max(od.buy_orders), min(od.sell_orders)
                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)
                intr = max(0.0, vex_fair - strike)
                extr = max(0.0, v_mid - intr)
                st = sd.setdefault(sym, {"ema": 0.01})
                ema = EXTR_ALPHA * extr + (1 - EXTR_ALPHA) * st["ema"]
                st["ema"] = ema
                fair = intr + ema

                oo = []; ib, is_ = 0, 0

                if not no_new:
                    if ba < fair - 10:
                        q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                        if q > 0: oo.append(Order(sym, ba, q)); ib += q
                    if bb > fair + 10:
                        q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                        if q > 0: oo.append(Order(sym, bb, -q)); is_ += q

                    hs = ITM_HS[sym]
                    bid_px = int(round(fair - hs)); ask_px = int(round(fair + hs))
                    if bid_px >= ba: bid_px = ba - 1
                    if ask_px <= bb: ask_px = bb + 1
                    dev = extr - ema
                    psz = pp["itm_ps"]
                    bsz = max(2, min(psz + int(5*(-dev)), ITM_LIMIT - pos - ib))
                    asz = max(2, min(psz + int(5*dev), ITM_LIMIT + pos - is_))
                    if bsz > 0 and bid_px > 0: oo.append(Order(sym, bid_px, bsz))
                    if asz > 0 and ask_px > 0: oo.append(Order(sym, ask_px, -asz))

                # Phase 3 ITM unwind
                if tick > PHASE2_END and abs(pos) > 5:
                    if pos > 0:
                        uw = min(25, pos, ITM_LIMIT + pos)
                        if uw > 0: oo.append(Order(sym, bb, -uw))
                    else:
                        uw = min(25, -pos, ITM_LIMIT - pos)
                        if uw > 0: oo.append(Order(sym, ba, uw))

                result[sym] = oo

        # ══════════════════════════════════════════
        # 4. VEV_5300 Sell-Bias Overlay
        # ══════════════════════════════════════════
        if vex_fair is not None and pp["v53_cap"] > 0 and not no_new:
            od53 = state.order_depths.get("VEV_5300")
            if od53 and od53.buy_orders and od53.sell_orders:
                bb53, ba53 = max(od53.buy_orders), min(od53.sell_orders)
                if 1 <= ba53 - bb53 <= 15:
                    pos53 = state.position.get("VEV_5300", 0)
                    mid53 = (bb53 + ba53) / 2.0
                    bach = bachelier_call(vex_fair, 5300, tte_y, sigma)
                    intr53 = max(vex_fair - 5300, 0.0)
                    if bach < intr53: bach = intr53

                    raw_r = mid53 - bach
                    bias53 = BIAS_ALPHA * raw_r + (1 - BIAS_ALPHA) * bias53
                    sd["b53"] = bias53
                    adj_f = bach + bias53
                    dev = raw_r - bias53

                    oo53 = []
                    cap53 = pp["v53_cap"]
                    sz53 = pp["v53_sz"]

                    if dev > 2.0 and pos53 > -cap53:
                        for bp in sorted(od53.buy_orders, reverse=True):
                            if bp < adj_f + 0.5: break
                            q = min(od53.buy_orders[bp], sz53, cap53 + pos53)
                            if q > 0: oo53.append(Order("VEV_5300", bp, -q))

                    if dev < -2.0 and pos53 < cap53:
                        for ap in sorted(od53.sell_orders):
                            if ap > adj_f - 0.5: break
                            q = min(-od53.sell_orders[ap], sz53, cap53 - pos53)
                            if q > 0: oo53.append(Order("VEV_5300", ap, q))

                    # Small passive
                    inv_adj = -1.5 * (pos53 / V_LIMIT)
                    qf53 = adj_f + inv_adj
                    bp53 = int(round(qf53 - 3)); ap53 = int(round(qf53 + 3))
                    if bp53 >= ba53: bp53 = ba53 - 1
                    if ap53 <= bb53: ap53 = bb53 + 1
                    bq53 = min(2, cap53 - pos53) if pos53 < cap53 else 0
                    sq53 = min(2, cap53 + pos53) if pos53 > -cap53 else 0
                    if bq53 > 0 and bp53 > 0: oo53.append(Order("VEV_5300", bp53, bq53))
                    if sq53 > 0 and ap53 > 0: oo53.append(Order("VEV_5300", ap53, -sq53))

                    result["VEV_5300"] = oo53

        # Phase 3 VEV_5300 unwind
        if tick > PHASE2_END:
            od53 = state.order_depths.get("VEV_5300")
            pos53 = state.position.get("VEV_5300", 0)
            if od53 and od53.buy_orders and od53.sell_orders and abs(pos53) > 2:
                bb53, ba53 = max(od53.buy_orders), min(od53.sell_orders)
                oo53 = result.get("VEV_5300", [])
                if pos53 > 0:
                    oo53.append(Order("VEV_5300", bb53, -min(10, pos53)))
                else:
                    oo53.append(Order("VEV_5300", ba53, min(10, -pos53)))
                result["VEV_5300"] = oo53

        # Vol calibration
        if vex_fair is not None:
            for cs in ["VEV_5200", "VEV_5300"]:
                cod = state.order_depths.get(cs)
                if cod and cod.buy_orders and cod.sell_orders:
                    cmid = (max(cod.buy_orders) + min(cod.sell_orders)) / 2.0
                    if cmid > 0:
                        K = 5200 if cs == "VEV_5200" else 5300
                        intr = max(vex_fair - K, 0.0)
                        if cmid > intr + 0.01:
                            lo, hi = 10.0, 5000.0
                            for _ in range(40):
                                m = (lo + hi) * 0.5
                                if bachelier_call(vex_fair, K, tte_y, m) < cmid: lo = m
                                else: hi = m
                                if hi - lo < 1.0: break
                            iv = (lo + hi) * 0.5
                            if 200 < iv < 4000:
                                sigma = SIGMA_EMA * iv + (1 - SIGMA_EMA) * sigma
            sd["sig"] = sigma

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
