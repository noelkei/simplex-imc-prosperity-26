from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
BOT_DIR = ROUND / "bots" / "amin" / "canonical"
MANIFEST = ROUND / "workspace" / "05_implementation" / "learning_batch_wave1_manifest.md"


LEARNERS = [
    {
        "bot_id": "L01",
        "filename": "probe_l01_hydro_reversion.py",
        "kind": "delta1",
        "family": "delta1 reversion",
        "products": [
            {
                "symbol": "HYDROGEL_PACK",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 18,
                "offset": 6,
                "edge": 2,
                "reversion_weight": 0.45,
                "imbalance_weight": 0.0,
                "inventory_skew": 6.0,
                "passive_size": 10,
            }
        ],
        "hypothesis": "HYDRO still has a tradable reversion signal if we isolate it from composite noise.",
    },
    {
        "bot_id": "L02",
        "filename": "probe_l02_hydro_imbalance.py",
        "kind": "delta1",
        "family": "delta1 imbalance",
        "products": [
            {
                "symbol": "HYDROGEL_PACK",
                "limit": 200,
                "mode": "imbalance",
                "max_spread": 18,
                "offset": 6,
                "edge": 2,
                "reversion_weight": 0.0,
                "imbalance_weight": 5.0,
                "inventory_skew": 6.0,
                "passive_size": 10,
            }
        ],
        "hypothesis": "HYDRO may be better captured by imbalance than by pure mid reversion.",
    },
    {
        "bot_id": "L04",
        "filename": "probe_l04_vex_reversion.py",
        "kind": "delta1",
        "family": "delta1 reversion",
        "products": [
            {
                "symbol": "VELVETFRUIT_EXTRACT",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 6,
                "offset": 2,
                "edge": 1,
                "reversion_weight": 0.50,
                "imbalance_weight": 0.0,
                "inventory_skew": 4.0,
                "passive_size": 12,
            }
        ],
        "hypothesis": "VEX should remain one of the cleanest standalone learners on the live day.",
    },
    {
        "bot_id": "L05",
        "filename": "probe_l05_vex_imbalance.py",
        "kind": "delta1",
        "family": "delta1 imbalance",
        "products": [
            {
                "symbol": "VELVETFRUIT_EXTRACT",
                "limit": 200,
                "mode": "imbalance",
                "max_spread": 6,
                "offset": 2,
                "edge": 1,
                "reversion_weight": 0.0,
                "imbalance_weight": 2.5,
                "inventory_skew": 4.0,
                "passive_size": 12,
            }
        ],
        "hypothesis": "VEX imbalance may carry most of the live delta-1 edge by itself.",
    },
    {
        "bot_id": "L06",
        "filename": "probe_l06_delta1_dual_independent.py",
        "kind": "delta1",
        "family": "delta1 dual combo",
        "products": [
            {
                "symbol": "HYDROGEL_PACK",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 18,
                "offset": 6,
                "edge": 2,
                "reversion_weight": 0.40,
                "imbalance_weight": 0.0,
                "inventory_skew": 5.0,
                "passive_size": 8,
            },
            {
                "symbol": "VELVETFRUIT_EXTRACT",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 6,
                "offset": 2,
                "edge": 1,
                "reversion_weight": 0.45,
                "imbalance_weight": 0.0,
                "inventory_skew": 4.0,
                "passive_size": 10,
            },
        ],
        "hypothesis": "HYDRO and VEX should still add mostly independently when run as a clean dual delta-1 stack.",
    },
    {
        "bot_id": "L07",
        "filename": "probe_l07_itm_4000_residual.py",
        "kind": "voucher",
        "family": "itm residual",
        "products": [
            {
                "symbol": "VEV_4000",
                "strike": 4000,
                "limit": 300,
                "max_spread": 24,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 4,
                "cross_pad": 1.0,
                "signal_weight": 0.65,
                "inventory_skew": 1.5,
                "passive_size": 6,
            }
        ],
        "hypothesis": "VEV_4000 should be one of the cleanest live residual learners.",
    },
    {
        "bot_id": "L08",
        "filename": "probe_l08_itm_4500_residual.py",
        "kind": "voucher",
        "family": "itm residual",
        "products": [
            {
                "symbol": "VEV_4500",
                "strike": 4500,
                "limit": 300,
                "max_spread": 18,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 3,
                "cross_pad": 1.0,
                "signal_weight": 0.65,
                "inventory_skew": 1.5,
                "passive_size": 6,
            }
        ],
        "hypothesis": "VEV_4500 should be the second clean ITM residual learner.",
    },
    {
        "bot_id": "L09",
        "filename": "probe_l09_itm_pair_residual.py",
        "kind": "voucher",
        "family": "itm residual pair",
        "products": [
            {
                "symbol": "VEV_4000",
                "strike": 4000,
                "limit": 300,
                "max_spread": 24,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 4,
                "cross_pad": 1.0,
                "signal_weight": 0.60,
                "inventory_skew": 1.0,
                "passive_size": 5,
            },
            {
                "symbol": "VEV_4500",
                "strike": 4500,
                "limit": 300,
                "max_spread": 18,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 3,
                "cross_pad": 1.0,
                "signal_weight": 0.60,
                "inventory_skew": 1.0,
                "passive_size": 5,
            },
        ],
        "hypothesis": "The ITM edge should survive as a small pair, not just strike by strike.",
    },
    {
        "bot_id": "L10",
        "filename": "probe_l10_itm_pair_plus_vex.py",
        "kind": "voucher",
        "family": "itm residual plus vex",
        "sidecar_products": [
            {
                "symbol": "VELVETFRUIT_EXTRACT",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 6,
                "offset": 2,
                "edge": 1,
                "reversion_weight": 0.45,
                "imbalance_weight": 0.0,
                "inventory_skew": 4.0,
                "passive_size": 10,
            }
        ],
        "products": [
            {
                "symbol": "VEV_4000",
                "strike": 4000,
                "limit": 300,
                "max_spread": 24,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 4,
                "cross_pad": 1.0,
                "signal_weight": 0.60,
                "inventory_skew": 1.0,
                "passive_size": 5,
            },
            {
                "symbol": "VEV_4500",
                "strike": 4500,
                "limit": 300,
                "max_spread": 18,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 3,
                "cross_pad": 1.0,
                "signal_weight": 0.60,
                "inventory_skew": 1.0,
                "passive_size": 5,
            },
        ],
        "hypothesis": "A cleaner VEX plus ITM stack should reproduce the best historical family more faithfully.",
    },
    {
        "bot_id": "L12",
        "filename": "probe_l12_active_5000_residual.py",
        "kind": "voucher",
        "family": "active residual",
        "products": [
            {
                "symbol": "VEV_5000",
                "strike": 5000,
                "limit": 300,
                "max_spread": 8,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.5,
                "passive_size": 8,
            }
        ],
        "hypothesis": "VEV_5000 may still have some standalone residual edge despite weak composite behavior.",
    },
    {
        "bot_id": "L13",
        "filename": "probe_l13_active_5100_residual.py",
        "kind": "voucher",
        "family": "active residual",
        "products": [
            {
                "symbol": "VEV_5100",
                "strike": 5100,
                "limit": 300,
                "max_spread": 6,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.5,
                "passive_size": 8,
            }
        ],
        "hypothesis": "VEV_5100 needs isolation before we can prune or rescue it.",
    },
    {
        "bot_id": "L14",
        "filename": "probe_l14_active_5200_residual.py",
        "kind": "voucher",
        "family": "active residual",
        "products": [
            {
                "symbol": "VEV_5200",
                "strike": 5200,
                "limit": 300,
                "max_spread": 4,
                "entry_threshold": 2.0,
                "exit_threshold": 0.7,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.85,
                "inventory_skew": 2.0,
                "passive_size": 10,
            }
        ],
        "hypothesis": "VEV_5200 must be isolated to confirm whether it is a true reject or only a basket interaction problem.",
    },
    {
        "bot_id": "L15",
        "filename": "probe_l15_active_5300_residual.py",
        "kind": "voucher",
        "family": "active residual",
        "products": [
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 10,
            }
        ],
        "hypothesis": "VEV_5300 is the best active strike and deserves a direct standalone learner.",
    },
    {
        "bot_id": "L16",
        "filename": "probe_l16_active_5000_5300_residual.py",
        "kind": "voucher",
        "family": "active residual subset",
        "products": [
            {
                "symbol": "VEV_5000",
                "strike": 5000,
                "limit": 300,
                "max_spread": 8,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 6,
            },
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 8,
            },
        ],
        "hypothesis": "The cleanest active subset may be the outer pair 5000 plus 5300.",
    },
    {
        "bot_id": "L17",
        "filename": "probe_l17_active_5100_5300_residual.py",
        "kind": "voucher",
        "family": "active residual subset",
        "products": [
            {
                "symbol": "VEV_5100",
                "strike": 5100,
                "limit": 300,
                "max_spread": 6,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 6,
            },
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 8,
            },
        ],
        "hypothesis": "5100 may work only in the presence of 5300 rather than alone or in the full basket.",
    },
    {
        "bot_id": "L18",
        "filename": "probe_l18_active_5200_5300_residual.py",
        "kind": "voucher",
        "family": "active residual subset",
        "products": [
            {
                "symbol": "VEV_5200",
                "strike": 5200,
                "limit": 300,
                "max_spread": 4,
                "entry_threshold": 2.0,
                "exit_threshold": 0.7,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.80,
                "inventory_skew": 1.5,
                "passive_size": 8,
            },
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 8,
            },
        ],
        "hypothesis": "If 5200 only works next to 5300, we should see it here before restoring it more broadly.",
    },
    {
        "bot_id": "L19",
        "filename": "probe_l19_active_5000_5100_5300_residual.py",
        "kind": "voucher",
        "family": "active residual subset",
        "products": [
            {
                "symbol": "VEV_5000",
                "strike": 5000,
                "limit": 300,
                "max_spread": 8,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 6,
            },
            {
                "symbol": "VEV_5100",
                "strike": 5100,
                "limit": 300,
                "max_spread": 6,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 6,
            },
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 8,
            },
        ],
        "hypothesis": "The right active basket may simply be the current family without VEV_5200.",
    },
    {
        "bot_id": "L20",
        "filename": "probe_l20_active_5000_5300_inventory.py",
        "kind": "voucher",
        "family": "active residual inventory subset",
        "products": [
            {
                "symbol": "VEV_5000",
                "strike": 5000,
                "limit": 300,
                "max_spread": 8,
                "entry_threshold": 1.5,
                "exit_threshold": 0.5,
                "quote_offset": 2,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 4.0,
                "passive_size": 6,
            },
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 4.0,
                "passive_size": 8,
            },
        ],
        "hypothesis": "Inventory skew should only be judged after removing the known toxic middle strikes.",
    },
    {
        "bot_id": "L21",
        "filename": "probe_l21_upper_5400_residual.py",
        "kind": "voucher",
        "family": "upper residual",
        "products": [
            {
                "symbol": "VEV_5400",
                "strike": 5400,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 0.8,
                "exit_threshold": 0.3,
                "quote_offset": 1,
                "cross_pad": 0.3,
                "signal_weight": 0.75,
                "inventory_skew": 0.8,
                "passive_size": 12,
            }
        ],
        "hypothesis": "VEV_5400 now deserves a direct live learner because the logger showed movement plus tight spreads.",
    },
    {
        "bot_id": "L22",
        "filename": "probe_l22_upper_5500_residual.py",
        "kind": "voucher",
        "family": "upper residual",
        "products": [
            {
                "symbol": "VEV_5500",
                "strike": 5500,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 0.5,
                "exit_threshold": 0.2,
                "quote_offset": 1,
                "cross_pad": 0.2,
                "signal_weight": 0.75,
                "inventory_skew": 0.8,
                "passive_size": 12,
            }
        ],
        "hypothesis": "VEV_5500 is the highest-ROI reopened upper-strike probe because spreads are exceptionally tight.",
    },
    {
        "bot_id": "L23",
        "filename": "probe_l23_upper_5400_5500_residual.py",
        "kind": "voucher",
        "family": "upper residual pair",
        "products": [
            {
                "symbol": "VEV_5400",
                "strike": 5400,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 0.8,
                "exit_threshold": 0.3,
                "quote_offset": 1,
                "cross_pad": 0.3,
                "signal_weight": 0.75,
                "inventory_skew": 0.8,
                "passive_size": 10,
            },
            {
                "symbol": "VEV_5500",
                "strike": 5500,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 0.5,
                "exit_threshold": 0.2,
                "quote_offset": 1,
                "cross_pad": 0.2,
                "signal_weight": 0.75,
                "inventory_skew": 0.8,
                "passive_size": 12,
            },
        ],
        "hypothesis": "The upper branch may work better as a small pair than as a single-strike probe.",
    },
    {
        "bot_id": "L24",
        "filename": "probe_l24_upper_5400_5500_passive.py",
        "kind": "voucher",
        "family": "upper passive maker",
        "passive_only": True,
        "neutral_two_sided": True,
        "products": [
            {
                "symbol": "VEV_5400",
                "strike": 5400,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 99.0,
                "exit_threshold": 0.0,
                "quote_offset": 1,
                "cross_pad": 0.0,
                "signal_weight": 0.0,
                "inventory_skew": 0.6,
                "passive_size": 10,
            },
            {
                "symbol": "VEV_5500",
                "strike": 5500,
                "limit": 300,
                "max_spread": 2,
                "entry_threshold": 99.0,
                "exit_threshold": 0.0,
                "quote_offset": 1,
                "cross_pad": 0.0,
                "signal_weight": 0.0,
                "inventory_skew": 0.6,
                "passive_size": 12,
            },
        ],
        "hypothesis": "The upper branch may simply need passive spread capture rather than directional residual trading.",
    },
    {
        "bot_id": "L25",
        "filename": "probe_l25_vex_plus_5300.py",
        "kind": "voucher",
        "family": "vex plus active best strike",
        "sidecar_products": [
            {
                "symbol": "VELVETFRUIT_EXTRACT",
                "limit": 200,
                "mode": "reversion",
                "max_spread": 6,
                "offset": 2,
                "edge": 1,
                "reversion_weight": 0.45,
                "imbalance_weight": 0.0,
                "inventory_skew": 4.0,
                "passive_size": 10,
            }
        ],
        "products": [
            {
                "symbol": "VEV_5300",
                "strike": 5300,
                "limit": 300,
                "max_spread": 3,
                "entry_threshold": 1.2,
                "exit_threshold": 0.4,
                "quote_offset": 1,
                "cross_pad": 0.5,
                "signal_weight": 0.75,
                "inventory_skew": 1.0,
                "passive_size": 8,
            }
        ],
        "hypothesis": "A clean VEX plus 5300 combo may be the best near-term active learner.",
    },
    {
        "bot_id": "L26",
        "filename": "probe_l26_surface_5200_5300_relval.py",
        "kind": "surface_pair",
        "family": "surface relative value",
        "pairs": [
            {
                "left_symbol": "VEV_5200",
                "left_strike": 5200,
                "left_limit": 300,
                "right_symbol": "VEV_5300",
                "right_strike": 5300,
                "right_limit": 300,
                "left_max_spread": 4,
                "right_max_spread": 3,
                "threshold": 2.0,
                "size": 10,
                "anchor_alpha": 0.03,
            }
        ],
        "hypothesis": "The current active failure may be better explained by the 5200/5300 local surface relationship than by absolute residual alone.",
    },
    {
        "bot_id": "L27",
        "filename": "probe_l27_surface_5300_5400_relval.py",
        "kind": "surface_pair",
        "family": "surface relative value",
        "pairs": [
            {
                "left_symbol": "VEV_5300",
                "left_strike": 5300,
                "left_limit": 300,
                "right_symbol": "VEV_5400",
                "right_strike": 5400,
                "right_limit": 300,
                "left_max_spread": 3,
                "right_max_spread": 2,
                "threshold": 1.2,
                "size": 10,
                "anchor_alpha": 0.03,
            }
        ],
        "hypothesis": "The upper transition around 5300/5400 may be cleaner than the broader active basket.",
    },
]


TEMPLATE = '''"""
Generated Round 3 learning bot.
Batch spec: spec_learning_batch_wave1.md
Bot ID: {bot_id}
Family: {family}
Hypothesis: {hypothesis}
"""

import json
from datamodel import Order, TradingState


CONFIG = {config_json}


def get_mid(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    best_bid = max(order_depth.buy_orders)
    best_ask = min(order_depth.sell_orders)
    return (best_bid + best_ask) / 2.0


def get_spread(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return None
    return min(order_depth.sell_orders) - max(order_depth.buy_orders)


def get_imbalance(order_depth):
    if not order_depth.buy_orders or not order_depth.sell_orders:
        return 0.0
    best_bid = max(order_depth.buy_orders)
    best_ask = min(order_depth.sell_orders)
    bid_vol = order_depth.buy_orders[best_bid]
    ask_vol = abs(order_depth.sell_orders[best_ask])
    total = bid_vol + ask_vol
    if total <= 0:
        return 0.0
    return (bid_vol - ask_vol) / total


def clamp_qty(qty, position, limit):
    if qty > 0:
        return max(0, min(qty, limit - position))
    if qty < 0:
        return min(0, max(qty, -(limit + position)))
    return 0


def intrinsic_call(vex_mid, strike):
    return max(vex_mid - strike, 0.0)


def load_data(raw):
    if not raw:
        return {{}}
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            return data
    except Exception:
        return {{}}
    return {{}}


def save_data(data):
    return json.dumps(data, separators=(",", ":"), sort_keys=True)


def run_delta1_products(state, result, data, products):
    last_mid = data.setdefault("delta_last_mid", {{}})
    for cfg in products:
        symbol = cfg["symbol"]
        if symbol not in state.order_depths:
            continue
        od = state.order_depths[symbol]
        mid = get_mid(od)
        spread = get_spread(od)
        if mid is None or spread is None or spread > cfg["max_spread"]:
            continue

        position = state.position.get(symbol, 0)
        imbalance = get_imbalance(od)
        prev_mid = last_mid.get(symbol)

        signal = 0.0
        if cfg["mode"] in ("reversion", "hybrid") and prev_mid is not None:
            signal += cfg["reversion_weight"] * (prev_mid - mid)
        if cfg["mode"] in ("imbalance", "hybrid"):
            signal += cfg["imbalance_weight"] * imbalance

        fair = mid + signal - cfg["inventory_skew"] * (position / cfg["limit"])
        orders = []

        for ask in sorted(od.sell_orders):
            ask_vol = -od.sell_orders[ask]
            if ask <= fair - cfg["edge"]:
                buy_qty = clamp_qty(ask_vol, position, cfg["limit"])
                if buy_qty > 0:
                    orders.append(Order(symbol, int(ask), int(buy_qty)))
                    position += buy_qty

        for bid in sorted(od.buy_orders, reverse=True):
            bid_vol = od.buy_orders[bid]
            if bid >= fair + cfg["edge"]:
                sell_qty = clamp_qty(-bid_vol, position, cfg["limit"])
                if sell_qty < 0:
                    orders.append(Order(symbol, int(bid), int(sell_qty)))
                    position += sell_qty

        buy_qty = clamp_qty(cfg["passive_size"], position, cfg["limit"])
        sell_qty = clamp_qty(-cfg["passive_size"], position, cfg["limit"])
        buy_price = int(round(fair - cfg["offset"]))
        sell_price = int(round(fair + cfg["offset"]))

        if buy_qty > 0:
            orders.append(Order(symbol, buy_price, int(buy_qty)))
        if sell_qty < 0:
            orders.append(Order(symbol, sell_price, int(sell_qty)))

        if orders:
            result[symbol] = orders
        last_mid[symbol] = mid


def run_voucher_products(state, result, data, config):
    sidecars = config.get("sidecar_products", [])
    if sidecars:
        run_delta1_products(state, result, data, sidecars)

    vex_symbol = "VELVETFRUIT_EXTRACT"
    vex_depth = state.order_depths.get(vex_symbol)
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    anchors = data.setdefault("voucher_anchor", {{}})
    passive_only = bool(config.get("passive_only", False))
    neutral_two_sided = bool(config.get("neutral_two_sided", False))
    for cfg in config["products"]:
        symbol = cfg["symbol"]
        if symbol not in state.order_depths:
            continue
        od = state.order_depths[symbol]
        mid = get_mid(od)
        spread = get_spread(od)
        if mid is None or spread is None or spread > cfg["max_spread"]:
            continue

        position = state.position.get(symbol, 0)
        anchor_key = symbol
        base_fair = intrinsic_call(vex_mid, cfg["strike"])
        raw_residual = mid - base_fair
        prev_anchor = float(anchors.get(anchor_key, raw_residual))
        centered = raw_residual - prev_anchor
        fair = (
            base_fair
            + prev_anchor
            - cfg["signal_weight"] * centered
            - cfg["inventory_skew"] * (position / cfg["limit"])
        )

        orders = []
        if not passive_only:
            if centered < -cfg["entry_threshold"]:
                for ask in sorted(od.sell_orders):
                    ask_vol = -od.sell_orders[ask]
                    if ask <= fair + cfg["cross_pad"]:
                        buy_qty = clamp_qty(ask_vol, position, cfg["limit"])
                        if buy_qty > 0:
                            orders.append(Order(symbol, int(ask), int(buy_qty)))
                            position += buy_qty
            elif centered > cfg["entry_threshold"]:
                for bid in sorted(od.buy_orders, reverse=True):
                    bid_vol = od.buy_orders[bid]
                    if bid >= fair - cfg["cross_pad"]:
                        sell_qty = clamp_qty(-bid_vol, position, cfg["limit"])
                        if sell_qty < 0:
                            orders.append(Order(symbol, int(bid), int(sell_qty)))
                            position += sell_qty

        passive_size = cfg["passive_size"]
        buy_qty = clamp_qty(passive_size, position, cfg["limit"])
        sell_qty = clamp_qty(-passive_size, position, cfg["limit"])
        buy_price = int(round(fair - cfg["quote_offset"]))
        sell_price = int(round(fair + cfg["quote_offset"]))

        if centered < -cfg["entry_threshold"]:
            if buy_qty > 0:
                orders.append(Order(symbol, buy_price, int(buy_qty)))
        elif centered > cfg["entry_threshold"]:
            if sell_qty < 0:
                orders.append(Order(symbol, sell_price, int(sell_qty)))
        elif neutral_two_sided:
            if buy_qty > 0:
                orders.append(Order(symbol, buy_price, int(buy_qty)))
            if sell_qty < 0:
                orders.append(Order(symbol, sell_price, int(sell_qty)))

        if orders:
            result[symbol] = orders
        anchors[anchor_key] = (1.0 - 0.02) * prev_anchor + 0.02 * raw_residual


def run_surface_pairs(state, result, data, config):
    vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
    vex_mid = get_mid(vex_depth) if vex_depth is not None else None
    if vex_mid is None:
        return

    anchors = data.setdefault("surface_anchor", {{}})
    for cfg in config["pairs"]:
        left = cfg["left_symbol"]
        right = cfg["right_symbol"]
        if left not in state.order_depths or right not in state.order_depths:
            continue

        left_od = state.order_depths[left]
        right_od = state.order_depths[right]
        left_mid = get_mid(left_od)
        right_mid = get_mid(right_od)
        left_spread = get_spread(left_od)
        right_spread = get_spread(right_od)
        if (
            left_mid is None
            or right_mid is None
            or left_spread is None
            or right_spread is None
            or left_spread > cfg["left_max_spread"]
            or right_spread > cfg["right_max_spread"]
        ):
            continue

        left_pos = state.position.get(left, 0)
        right_pos = state.position.get(right, 0)
        left_extr = left_mid - intrinsic_call(vex_mid, cfg["left_strike"])
        right_extr = right_mid - intrinsic_call(vex_mid, cfg["right_strike"])
        raw_pair = left_extr - right_extr
        key = left + "__" + right
        prev_anchor = float(anchors.get(key, raw_pair))
        centered = raw_pair - prev_anchor
        orders_left = result.setdefault(left, [])
        orders_right = result.setdefault(right, [])
        size = int(cfg["size"])

        if centered > cfg["threshold"]:
            left_bid = max(left_od.buy_orders) if left_od.buy_orders else None
            right_ask = min(right_od.sell_orders) if right_od.sell_orders else None
            if left_bid is not None and right_ask is not None:
                sell_qty = clamp_qty(-size, left_pos, cfg["left_limit"])
                buy_qty = clamp_qty(size, right_pos, cfg["right_limit"])
                if sell_qty < 0:
                    orders_left.append(Order(left, int(left_bid), int(sell_qty)))
                    left_pos += sell_qty
                if buy_qty > 0:
                    orders_right.append(Order(right, int(right_ask), int(buy_qty)))
                    right_pos += buy_qty
        elif centered < -cfg["threshold"]:
            left_ask = min(left_od.sell_orders) if left_od.sell_orders else None
            right_bid = max(right_od.buy_orders) if right_od.buy_orders else None
            if left_ask is not None and right_bid is not None:
                buy_qty = clamp_qty(size, left_pos, cfg["left_limit"])
                sell_qty = clamp_qty(-size, right_pos, cfg["right_limit"])
                if buy_qty > 0:
                    orders_left.append(Order(left, int(left_ask), int(buy_qty)))
                    left_pos += buy_qty
                if sell_qty < 0:
                    orders_right.append(Order(right, int(right_bid), int(sell_qty)))
                    right_pos += sell_qty

        anchors[key] = (1.0 - cfg["anchor_alpha"]) * prev_anchor + cfg["anchor_alpha"] * raw_pair


class Trader:
    def run(self, state: TradingState):
        result = {{}}
        conversions = 0
        data = load_data(state.traderData)

        kind = CONFIG["kind"]
        if kind == "delta1":
            run_delta1_products(state, result, data, CONFIG["products"])
        elif kind == "voucher":
            run_voucher_products(state, result, data, CONFIG)
        elif kind == "surface_pair":
            run_surface_pairs(state, result, data, CONFIG)

        traderData = save_data(data)
        return result, conversions, traderData
'''


def bot_contents(config: dict) -> str:
    return TEMPLATE.format(
        bot_id=config["bot_id"],
        family=config["family"],
        hypothesis=config["hypothesis"],
        config_json=json.dumps(config, indent=4, sort_keys=True),
    )


def render_manifest(configs: list[dict]) -> str:
    lines = [
        "# Learning Batch Wave 1 Manifest",
        "",
        "Generated from `generate_learning_batch_wave1.py`.",
        "",
        "| Bot ID | File | Family | Hypothesis |",
        "| --- | --- | --- | --- |",
    ]
    for cfg in configs:
        lines.append(
            f"| `{cfg['bot_id']}` | `../bots/amin/canonical/{cfg['filename']}` | {cfg['family']} | {cfg['hypothesis']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    BOT_DIR.mkdir(parents=True, exist_ok=True)
    for config in LEARNERS:
        path = BOT_DIR / config["filename"]
        path.write_text(bot_contents(config))
    MANIFEST.write_text(render_manifest(LEARNERS))


if __name__ == "__main__":
    main()
