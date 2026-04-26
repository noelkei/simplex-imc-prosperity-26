"""
W3-25: Cross-Voucher Spread Reversion
=======================================
UNTESTED OPPORTUNITY: EDA shows 250-400 z-score crosses/day between VEV_5200/5300.
This is market-neutral (long one, short other) so no directional VEX delta exposure.

Strategy:
  - Track spread: VEV_5200_mid - VEV_5300_mid
  - Maintain EMA of spread as fair value
  - When spread deviates > entry_z * sigma from EMA: trade the pair
  - Long the cheap leg, short the expensive leg
  - Max position per leg: 30 (small, market-neutral)

Also runs HYDROGEL MM for base PnL (proven profitable).

Owner: amin
"""

import json
import math
from datamodel import Order, TradingState


# ─────────────────────────────────────────────────
# HYDROGEL params
# ─────────────────────────────────────────────────
HG = "HYDROGEL_PACK"
HG_LIMIT = 200
HG_CAP = 120
HG_HALF = 3
HG_TEDGE = 3
HG_PSZ = 22
HG_TSZ = 16
HG_GAMMA = 2.0
HG_UW_THR = 80
HG_UW_Q = 18

# Cross-voucher spread params
V52 = "VEV_5200"
V53 = "VEV_5300"
V_LIMIT = 300
V_CAP = 30             # per-leg position cap
SPREAD_EMA_ALPHA = 0.01  # slow EMA for spread fair
SPREAD_VOL_ALPHA = 0.02  # EMA for spread vol
ENTRY_Z = 1.8          # z-score threshold to enter
EXIT_Z = 0.3           # z-score to close
SPREAD_SIZE = 5        # trade size per fill
SPREAD_PASSIVE = 3     # passive quote size
SPREAD_OFFSET = 2      # passive offset from edge


def get_microprice(od):
    if not od.buy_orders or not od.sell_orders: return None
    bb, ba = max(od.buy_orders), min(od.sell_orders)
    bv, av = od.buy_orders[bb], -od.sell_orders[ba]
    t = bv + av
    return (bb * av + ba * bv) / t if t > 0 else (bb + ba) / 2.0


def get_mid(od):
    if not od.buy_orders or not od.sell_orders: return None
    return (max(od.buy_orders) + min(od.sell_orders)) / 2.0


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

        # ══════════════════════════════════════════
        # HYDROGEL MM (base PnL)
        # ══════════════════════════════════════════
        hg_od = state.order_depths.get(HG)
        if hg_od and hg_od.buy_orders and hg_od.sell_orders:
            hg_bb, hg_ba = max(hg_od.buy_orders), min(hg_od.sell_orders)
            if hg_ba - hg_bb >= 1:
                hg_pos = state.position.get(HG, 0)
                hg_micro = get_microprice(hg_od)
                hg_imb = 0.3 * get_imbalance(hg_od) + 0.7 * sd.get("hi", 0.0)
                sd["hi"] = hg_imb
                hg_qfair = hg_micro - HG_GAMMA * (hg_pos / HG_CAP) + clamp(2.0 * hg_imb, -3, 3)

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

                if hg_pos >= HG_UW_THR and hgsr() > 0:
                    uq = min(HG_UW_Q, hgsr())
                    hg_orders.append(Order(HG, hg_bb, -uq)); hg_s += uq
                elif hg_pos <= -HG_UW_THR and hgbr() > 0:
                    uq = min(HG_UW_Q, hgbr())
                    hg_orders.append(Order(HG, hg_ba, uq)); hg_b += uq

                half = HG_HALF + (1 if abs(hg_pos) > HG_CAP * 0.6 else 0)
                hbp = int(round(hg_qfair - half)); hap = int(round(hg_qfair + half))
                if hbp >= hg_ba: hbp = hg_ba - 1
                if hap <= hg_bb: hap = hg_bb + 1
                bsz = max(3, HG_PSZ - int(hg_pos * 0.2)) if hg_pos > 0 else max(3, HG_PSZ + int(-hg_pos * 0.2)) if hg_pos < 0 else HG_PSZ
                ssz = max(3, HG_PSZ + int(hg_pos * 0.2)) if hg_pos > 0 else max(3, HG_PSZ - int(-hg_pos * 0.2)) if hg_pos < 0 else HG_PSZ
                bq, sq = min(bsz, hgbr()), min(ssz, hgsr())
                if bq > 0: hg_orders.append(Order(HG, hbp, bq))
                if sq > 0: hg_orders.append(Order(HG, hap, -sq))
                result[HG] = hg_orders

        # ══════════════════════════════════════════
        # CROSS-VOUCHER SPREAD: VEV_5200 vs VEV_5300
        # ══════════════════════════════════════════
        od52 = state.order_depths.get(V52)
        od53 = state.order_depths.get(V53)

        if (od52 and od52.buy_orders and od52.sell_orders and
                od53 and od53.buy_orders and od53.sell_orders):

            bb52, ba52 = max(od52.buy_orders), min(od52.sell_orders)
            bb53, ba53 = max(od53.buy_orders), min(od53.sell_orders)
            mid52 = (bb52 + ba52) / 2.0
            mid53 = (bb53 + ba53) / 2.0

            # Spread = VEV_5200 - VEV_5300 (should be positive as 5200 is deeper ITM)
            spread = mid52 - mid53

            # EMA fair spread
            sp_ema = sd.get("se", spread)
            sp_ema = SPREAD_EMA_ALPHA * spread + (1 - SPREAD_EMA_ALPHA) * sp_ema
            sd["se"] = sp_ema

            # EMA spread vol
            sp_dev = abs(spread - sp_ema)
            sp_vol = sd.get("sv", 5.0)
            sp_vol = SPREAD_VOL_ALPHA * sp_dev + (1 - SPREAD_VOL_ALPHA) * sp_vol
            sp_vol = max(sp_vol, 0.5)  # floor
            sd["sv"] = sp_vol

            # Z-score
            z = (spread - sp_ema) / sp_vol

            pos52 = state.position.get(V52, 0)
            pos53 = state.position.get(V53, 0)

            orders52 = []
            orders53 = []

            # Spread is HIGH (VEV_5200 expensive vs VEV_5300) → sell 5200, buy 5300
            if z > ENTRY_Z:
                # Sell VEV_5200
                if pos52 > -V_CAP:
                    q52 = min(SPREAD_SIZE, V_CAP + pos52, V_LIMIT + pos52)
                    if q52 > 0:
                        orders52.append(Order(V52, bb52, -q52))
                # Buy VEV_5300
                if pos53 < V_CAP:
                    q53 = min(SPREAD_SIZE, V_CAP - pos53, V_LIMIT - pos53)
                    if q53 > 0:
                        orders53.append(Order(V53, ba53, q53))

            # Spread is LOW (VEV_5200 cheap vs VEV_5300) → buy 5200, sell 5300
            elif z < -ENTRY_Z:
                # Buy VEV_5200
                if pos52 < V_CAP:
                    q52 = min(SPREAD_SIZE, V_CAP - pos52, V_LIMIT - pos52)
                    if q52 > 0:
                        orders52.append(Order(V52, ba52, q52))
                # Sell VEV_5300
                if pos53 > -V_CAP:
                    q53 = min(SPREAD_SIZE, V_CAP + pos53, V_LIMIT + pos53)
                    if q53 > 0:
                        orders53.append(Order(V53, bb53, -q53))

            # Exit: flatten when spread normalizes
            elif abs(z) < EXIT_Z:
                # Flatten VEV_5200
                if pos52 > 0:
                    q = min(SPREAD_SIZE, pos52)
                    orders52.append(Order(V52, bb52, -q))
                elif pos52 < 0:
                    q = min(SPREAD_SIZE, -pos52)
                    orders52.append(Order(V52, ba52, q))
                # Flatten VEV_5300
                if pos53 > 0:
                    q = min(SPREAD_SIZE, pos53)
                    orders53.append(Order(V53, bb53, -q))
                elif pos53 < 0:
                    q = min(SPREAD_SIZE, -pos53)
                    orders53.append(Order(V53, ba53, q))

            if orders52:
                result[V52] = orders52
            if orders53:
                result[V53] = orders53

        td = json.dumps(sd, separators=(",", ":"))
        return result, conversions, td
