"""
W3-21: Delta1 + ITM Stack
=========================
Hybrid of the two best-performing architectures:
- r3_b02_itm_residual (+1,409): VEX Kalman MM + ITM 4000/4500 intrinsic-residual arb
- w2_01 delta1_dual_control (+873): Compact HYDRO + VEX delta-1 stack

Architecture:
  1. HYDROGEL MM: Avellaneda-Stoikov reservation price, microprice + imbalance EMA
     - Primary PnL source (spread=15.7, ac1=-0.13, excellent MM)
  2. VEX Kalman MM: Kalman-filtered fair value with tight quotes
     - Delta-1 PnL + provides VEX fair for ITM pricing
  3. ITM 4000/4500 intrinsic residual: Buy cheap / sell rich vs intrinsic fair
     - Proven +1,409 in isolation; extrinsic ≈ 0 so fair ≈ max(0, vex - strike)

Key insight: Delta-1 legs are consistently +550-886, ITM residual adds +500-700 on top.
Combined should yield +1,200-1,500.

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────
# Parameters
# ─────────────────────────────────────────────────

# HYDROGEL MM (primary PnL)
HG_LIMIT = 200
HG_POS_CAP = 130
HG_HALF_SPREAD = 3
HG_TAKE_EDGE = 3
HG_PASSIVE_SIZE = 25
HG_TAKE_SIZE = 18
HG_INV_GAMMA = 2.0
HG_UNWIND_THR = 90
HG_UNWIND_QTY = 20
HG_IMB_ALPHA = 0.3
HG_IMB_GAIN = 2.0

# VEX Kalman MM
VEX_LIMIT = 200
VEX_POS_CAP = 120
VEX_HALF_SPREAD = 2
VEX_TAKE_EDGE = 2
VEX_PASSIVE_SIZE = 15
VEX_TAKE_SIZE = 12
VEX_INV_GAMMA = 2.0
KQ = 0.1
KR_VEX = 10.0

# ITM Vouchers
ITM_SYMS = {"VEV_4000": 4000, "VEV_4500": 4500}
ITM_LIMIT = 300
EXTR_ALPHA = 0.005
TAKE_EDGE_ITM = 10
ITM_HALF_SPREAD = {"VEV_4000": 9, "VEV_4500": 7}
ITM_PASSIVE_SIZE = 30


# ─────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────

def get_microprice(od):
    if not od.buy_orders or not od.sell_orders:
        return None
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return (bb + ba) / 2.0
    return (bb * av + ba * bv) / total


def get_mid(od):
    if not od.buy_orders or not od.sell_orders:
        return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


def get_imbalance(od):
    if not od.buy_orders or not od.sell_orders:
        return 0.0
    bb = max(od.buy_orders)
    ba = min(od.sell_orders)
    bv = od.buy_orders[bb]
    av = -od.sell_orders[ba]
    total = bv + av
    if total <= 0:
        return 0.0
    return (bv - av) / total


def clamp(v, lo, hi):
    return min(max(v, lo), hi)


# ─────────────────────────────────────────────────
# Trader
# ─────────────────────────────────────────────────

class Trader:

    def run(self, state: TradingState):
        result = {}
        conversions = 0

        sd = {}
        if state.traderData:
            try:
                sd = json.loads(state.traderData)
            except Exception:
                sd = {}

        # ══════════════════════════════════════════════════
        # MODULE 1: HYDROGEL Market Making
        # ══════════════════════════════════════════════════
        hg_od = state.order_depths.get("HYDROGEL_PACK")
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb = max(hg_od.buy_orders)
            hg_ba = min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get("HYDROGEL_PACK", 0)
                hg_micro = get_microprice(hg_od)

                # EMA imbalance
                hg_imb_raw = get_imbalance(hg_od)
                hg_imb = HG_IMB_ALPHA * hg_imb_raw + (1 - HG_IMB_ALPHA) * sd.get("hi", 0.0)
                sd["hi"] = hg_imb

                # Avellaneda-Stoikov reservation price
                hg_res = hg_micro - HG_INV_GAMMA * (hg_pos / HG_POS_CAP)
                hg_imb_shift = clamp(HG_IMB_GAIN * hg_imb, -3.0, 3.0)
                hg_qfair = hg_res + hg_imb_shift

                hg_orders = []
                hg_bought = 0
                hg_sold = 0

                def hg_buy():
                    return max(0, min(HG_POS_CAP, HG_LIMIT) - hg_pos - hg_bought)

                def hg_sell():
                    return max(0, min(HG_POS_CAP, HG_LIMIT) + hg_pos - hg_sold)

                # Aggressive takes
                for ask_p in sorted(hg_od.sell_orders):
                    if hg_buy() <= 0 or ask_p > hg_qfair - HG_TAKE_EDGE:
                        break
                    vol = -hg_od.sell_orders[ask_p]
                    qty = min(vol, HG_TAKE_SIZE, hg_buy())
                    if qty > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", ask_p, qty))
                        hg_bought += qty

                for bid_p in sorted(hg_od.buy_orders, reverse=True):
                    if hg_sell() <= 0 or bid_p < hg_qfair + HG_TAKE_EDGE:
                        break
                    vol = hg_od.buy_orders[bid_p]
                    qty = min(vol, HG_TAKE_SIZE, hg_sell())
                    if qty > 0:
                        hg_orders.append(Order("HYDROGEL_PACK", bid_p, -qty))
                        hg_sold += qty

                # Inventory unwind at extremes
                if hg_pos >= HG_UNWIND_THR and hg_sell() > 0:
                    uq = min(HG_UNWIND_QTY, hg_sell())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_bb, -uq))
                    hg_sold += uq
                elif hg_pos <= -HG_UNWIND_THR and hg_buy() > 0:
                    uq = min(HG_UNWIND_QTY, hg_buy())
                    hg_orders.append(Order("HYDROGEL_PACK", hg_ba, uq))
                    hg_bought += uq

                # Passive quotes with inventory skew
                half = HG_HALF_SPREAD
                if abs(hg_pos) > HG_POS_CAP * 0.6:
                    half += 1

                hg_bid_px = int(round(hg_qfair - half))
                hg_ask_px = int(round(hg_qfair + half))
                if hg_bid_px >= hg_ba:
                    hg_bid_px = hg_ba - 1
                if hg_ask_px <= hg_bb:
                    hg_ask_px = hg_bb + 1

                # Inventory-skewed sizes
                if hg_pos > 0:
                    b_sz = max(3, HG_PASSIVE_SIZE - int(hg_pos * 0.2))
                    s_sz = max(3, HG_PASSIVE_SIZE + int(hg_pos * 0.2))
                elif hg_pos < 0:
                    b_sz = max(3, HG_PASSIVE_SIZE + int(-hg_pos * 0.2))
                    s_sz = max(3, HG_PASSIVE_SIZE - int(-hg_pos * 0.2))
                else:
                    b_sz, s_sz = HG_PASSIVE_SIZE, HG_PASSIVE_SIZE

                bq = min(b_sz, hg_buy())
                sq = min(s_sz, hg_sell())
                if bq > 0:
                    hg_orders.append(Order("HYDROGEL_PACK", hg_bid_px, bq))
                if sq > 0:
                    hg_orders.append(Order("HYDROGEL_PACK", hg_ask_px, -sq))

                result["HYDROGEL_PACK"] = hg_orders

        # ══════════════════════════════════════════════════
        # MODULE 2: VEX Kalman Market Making
        # ══════════════════════════════════════════════════
        vex_od = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_fair = None

        if vex_od and vex_od.buy_orders and vex_od.sell_orders:
            vex_bb = max(vex_od.buy_orders)
            vex_ba = min(vex_od.sell_orders)
            vex_mid = (vex_bb + vex_ba) / 2.0
            vex_pos = state.position.get("VELVETFRUIT_EXTRACT", 0)

            # Kalman filter for VEX fair
            kst = sd.setdefault("vk", {"f": vex_mid, "v": 200.0})
            pv = min(kst["v"] + KQ, 500.0)
            k = pv / (pv + KR_VEX)
            kst["f"] = kst["f"] + k * (vex_mid - kst["f"])
            kst["v"] = (1 - k) * pv
            vex_fair = kst["f"]

            vfv = round(vex_fair)
            vex_imb = get_imbalance(vex_od)

            vex_orders = []
            vex_bought = 0
            vex_sold = 0

            def vex_buy():
                return max(0, min(VEX_POS_CAP, VEX_LIMIT) - vex_pos - vex_bought)

            def vex_sell():
                return max(0, min(VEX_POS_CAP, VEX_LIMIT) + vex_pos - vex_sold)

            # Aggressive takes
            if vex_ba <= vfv - VEX_TAKE_EDGE:
                qty = min(-vex_od.sell_orders[vex_ba], VEX_TAKE_SIZE, vex_buy())
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_ba, qty))
                    vex_bought += qty
            if vex_bb >= vfv + VEX_TAKE_EDGE:
                qty = min(vex_od.buy_orders[vex_bb], VEX_TAKE_SIZE, vex_sell())
                if qty > 0:
                    vex_orders.append(Order("VELVETFRUIT_EXTRACT", vex_bb, -qty))
                    vex_sold += qty

            # Passive quotes with inventory + imbalance lean
            inv_lean = -VEX_INV_GAMMA * (vex_pos / VEX_POS_CAP)
            adj_fair = vex_fair + inv_lean

            bid_px = int(round(adj_fair - VEX_HALF_SPREAD))
            ask_px = int(round(adj_fair + VEX_HALF_SPREAD))

            # Size adjustment
            b_sz = max(2, int(VEX_PASSIVE_SIZE + 10 * vex_imb - vex_pos * 0.08))
            a_sz = max(2, int(VEX_PASSIVE_SIZE - 10 * vex_imb + vex_pos * 0.08))

            if bid_px >= vex_ba:
                bid_px = vex_ba - 1
            if ask_px <= vex_bb:
                ask_px = vex_bb + 1

            bq = min(b_sz, vex_buy())
            sq = min(a_sz, vex_sell())
            if bq > 0:
                vex_orders.append(Order("VELVETFRUIT_EXTRACT", bid_px, bq))
            if sq > 0:
                vex_orders.append(Order("VELVETFRUIT_EXTRACT", ask_px, -sq))

            result["VELVETFRUIT_EXTRACT"] = vex_orders

        # ══════════════════════════════════════════════════
        # MODULE 3: ITM Voucher Intrinsic Residual
        # ══════════════════════════════════════════════════
        if vex_fair is not None:
            for sym, strike in ITM_SYMS.items():
                od = state.order_depths.get(sym)
                if od is None or not od.buy_orders or not od.sell_orders:
                    continue

                bb = max(od.buy_orders)
                ba = min(od.sell_orders)
                v_mid = (bb + ba) / 2.0
                pos = state.position.get(sym, 0)

                intrinsic = max(0.0, vex_fair - strike)
                curr_extr = max(0.0, v_mid - intrinsic)

                # Slow EMA of extrinsic (near zero for deep ITM)
                st = sd.setdefault(sym, {"ema": 0.01})
                ema = EXTR_ALPHA * curr_extr + (1 - EXTR_ALPHA) * st["ema"]
                st["ema"] = ema

                fair = intrinsic + ema
                half_s = ITM_HALF_SPREAD[sym]

                orders = []
                bought = 0
                sold = 0

                def itm_buy():
                    return max(0, ITM_LIMIT - pos - bought)

                def itm_sell():
                    return max(0, ITM_LIMIT + pos - sold)

                # Aggressive takes: buy when ask is well below fair
                if ba < fair - TAKE_EDGE_ITM:
                    qty = min(-od.sell_orders[ba], itm_buy())
                    if qty > 0:
                        orders.append(Order(sym, ba, qty))
                        bought += qty

                # Aggressive takes: sell when bid is well above fair
                if bb > fair + TAKE_EDGE_ITM:
                    qty = min(od.buy_orders[bb], itm_sell())
                    if qty > 0:
                        orders.append(Order(sym, bb, -qty))
                        sold += qty

                # Passive quotes
                bid_px = int(round(fair - half_s))
                ask_px = int(round(fair + half_s))
                if bid_px >= ba:
                    bid_px = ba - 1
                if ask_px <= bb:
                    ask_px = bb + 1

                # Residual lean (cheap → buy more, expensive → sell more)
                dev = curr_extr - ema
                b_sz = max(2, min(ITM_PASSIVE_SIZE + int(5 * (-dev)), itm_buy()))
                a_sz = max(2, min(ITM_PASSIVE_SIZE + int(5 * dev), itm_sell()))

                if b_sz > 0 and bid_px > 0:
                    orders.append(Order(sym, bid_px, b_sz))
                if a_sz > 0 and ask_px > 0:
                    orders.append(Order(sym, ask_px, -a_sz))

                result[sym] = orders

        # ── Save state ──
        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
