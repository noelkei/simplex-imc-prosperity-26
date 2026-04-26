"""
W3-28v4: Reduced VEX + Higher HYDRO Focus
===========================================
Base: W3-28 (+1,168)
Changes:
  - VEX_CAP: 120 → 70 (VEX spread is narrow at 5.0 → higher adverse selection risk)
  - VEX_PSZ: 15 → 8 (smaller passive quotes)
  - VEX_TSZ: 12 → 6 (smaller takes)
  - VEX_HALF: 2 → 3 (wider quotes to safety)
  - HG_CAP: 130 → 150 (shift capacity to the better product)
  - HG_PSZ: 24 → 30 (more passive on HYDRO)

Rationale: Delta-1 probes show HYDRO (+556) consistently outperforms VEX.
VEX's tight spread (5.0) makes it vulnerable to informed traders. By reducing
VEX exposure and increasing HYDRO, we shift PnL to the stronger product.
VEX still provides the fair value anchor for ITM pricing.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


HG = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"
HG_LIMIT = 200; VEX_LIMIT = 200; ITM_LIMIT = 300

HG_CAP = 150; VEX_CAP = 70         # ← HYDRO UP, VEX DOWN
HG_HALF = 3; VEX_HALF = 3          # ← VEX wider
HG_PSZ = 30; VEX_PSZ = 8           # ← HYDRO UP, VEX DOWN
HG_TSZ = 18; VEX_TSZ = 6           # ← VEX DOWN
HG_TEDGE = 3; VEX_TEDGE = 2

EXP_GAMMA = 3.0

KQ = 0.1; KR = 10.0

ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}
ITM_HS = {"VEV_4000": 9, "VEV_4500": 7}
ITM_TAKE = 10; ITM_PSZ = 30
EXTR_ALPHA = 0.005


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


def exp_penalty(pos, cap):
    q = pos / max(1, cap)
    sign = 1.0 if q >= 0 else -1.0
    return sign * EXP_GAMMA * (math.exp(abs(q)) - 1.0) / (math.e - 1.0)


def prop_size(base, pos, cap, side):
    if side == "buy":
        room = max(0, cap - pos)
    else:
        room = max(0, cap + pos)
    frac = room / max(1, cap)
    return max(2, int(base * frac))


class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        sd = {}
        if state.traderData:
            try: sd = json.loads(state.traderData)
            except: sd = {}

        # HYDROGEL MM
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get(HG, 0)
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - exp_penalty(hg_pos, HG_CAP) + clamp(2.0 * hg_imb, -3, 3)

                hg_orders = []
                hg_b, hg_s = 0, 0
                def hgbr(): return max(0, min(HG_CAP, HG_LIMIT) - hg_pos - hg_b)
                def hgsr(): return max(0, min(HG_CAP, HG_LIMIT) + hg_pos - hg_s)

                for ap in sorted(hg_od.sell_orders):
                    if hgbr() <= 0 or ap > hg_qfair - HG_TEDGE: break
                    q = min(-hg_od.sell_orders[ap], HG_TSZ, hgbr())
                    if q > 0: hg_orders.append(Order(HG, ap, q)); hg_b += q
                for bp in sorted(hg_od.buy_orders, reverse=True):
                    if hgsr() <= 0 or bp < hg_qfair + HG_TEDGE: break
                    q = min(hg_od.buy_orders[bp], HG_TSZ, hgsr())
                    if q > 0: hg_orders.append(Order(HG, bp, -q)); hg_s += q

                if hg_pos > HG_CAP * 0.6 and hgsr() > 0:
                    uq = min(20, hgsr())
                    hg_orders.append(Order(HG, hg_bb, -uq)); hg_s += uq
                elif hg_pos < -HG_CAP * 0.6 and hgbr() > 0:
                    uq = min(20, hgbr())
                    hg_orders.append(Order(HG, hg_ba, uq)); hg_b += uq

                half = HG_HALF + (1 if abs(hg_pos) > HG_CAP * 0.5 else 0)
                hbp = int(round(hg_qfair - half))
                hap = int(round(hg_qfair + half))
                if hbp >= hg_ba: hbp = hg_ba - 1
                if hap <= hg_bb: hap = hg_bb + 1

                bsz = prop_size(HG_PSZ, hg_pos, HG_CAP, "buy")
                ssz = prop_size(HG_PSZ, hg_pos, HG_CAP, "sell")
                bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                if bq > 0: hg_orders.append(Order(HG, hbp, bq))
                if sq > 0: hg_orders.append(Order(HG, hap, -sq))
                result[HG] = hg_orders

        # VEX Kalman MM (reduced exposure)
        vex_od = state.order_depths.get(VEX)
        vex_fair = None
        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb, vex_ba = max(vex_od.buy_orders), min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get(VEX, 0)

            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]
            vfv = round(vex_fair)
            adj = vex_fair - exp_penalty(vex_pos, VEX_CAP)

            vex_orders = []
            vb, vs = 0, 0
            def vbr(): return max(0, min(VEX_CAP, VEX_LIMIT) - vex_pos - vb)
            def vsr(): return max(0, min(VEX_CAP, VEX_LIMIT) + vex_pos - vs)

            if vex_ba <= vfv - VEX_TEDGE:
                q = min(-vex_od.sell_orders[vex_ba], VEX_TSZ, vbr())
                if q > 0: vex_orders.append(Order(VEX, vex_ba, q)); vb += q
            if vex_bb >= vfv + VEX_TEDGE:
                q = min(vex_od.buy_orders[vex_bb], VEX_TSZ, vsr())
                if q > 0: vex_orders.append(Order(VEX, vex_bb, -q)); vs += q

            bp = int(round(adj - VEX_HALF)); ap = int(round(adj + VEX_HALF))
            if bp >= vex_ba: bp = vex_ba - 1
            if ap <= vex_bb: ap = vex_bb + 1

            bsz = prop_size(VEX_PSZ, vex_pos, VEX_CAP, "buy")
            ssz = prop_size(VEX_PSZ, vex_pos, VEX_CAP, "sell")
            bq, sq = min(bsz, vbr()), min(ssz, vsr())
            if bq > 0: vex_orders.append(Order(VEX, bp, bq))
            if sq > 0: vex_orders.append(Order(VEX, ap, -sq))
            result[VEX] = vex_orders

        # ITM Voucher Residual
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

                orders = []
                ib, is_ = 0, 0
                if ba < fair - ITM_TAKE:
                    q = min(-od.sell_orders[ba], ITM_LIMIT - pos)
                    if q > 0: orders.append(Order(sym, ba, q)); ib += q
                if bb > fair + ITM_TAKE:
                    q = min(od.buy_orders[bb], ITM_LIMIT + pos)
                    if q > 0: orders.append(Order(sym, bb, -q)); is_ += q

                half_s = ITM_HS[sym]
                bid_px = int(round(fair - half_s)); ask_px = int(round(fair + half_s))
                if bid_px >= ba: bid_px = ba - 1
                if ask_px <= bb: ask_px = bb + 1
                dev = curr_extr - ema
                b_sz = max(2, min(ITM_PSZ + int(5 * (-dev)), ITM_LIMIT - pos - ib))
                a_sz = max(2, min(ITM_PSZ + int(5 * dev), ITM_LIMIT + pos - is_))
                if b_sz > 0 and bid_px > 0: orders.append(Order(sym, bid_px, b_sz))
                if a_sz > 0 and ask_px > 0: orders.append(Order(sym, ask_px, -a_sz))
                result[sym] = orders

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
