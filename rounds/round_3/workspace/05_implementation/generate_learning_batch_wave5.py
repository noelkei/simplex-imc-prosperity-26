from __future__ import annotations

import pprint
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
BOT_DIR = ROUND / "bots" / "amin" / "canonical"
MANIFEST = ROUND / "workspace" / "05_implementation" / "learning_batch_wave5_manifest.md"
TEMPLATE_SOURCE = ROUND / "bots" / "amin" / "historical" / "candidate_w4_03_delta1_itm_kalman_stack.py"
SPEC_PATH = "spec_learning_batch_wave5.md"


def delta_product(
    symbol: str,
    *,
    mode: str = "reversion",
    limit: int = 200,
    working_limit: int | None = None,
    max_spread: int,
    quote_offset: int,
    edge: int,
    reversion_weight: float,
    imbalance_weight: float,
    inventory_skew: float,
    passive_size: int,
    aggressive_size: int,
    passive_only: bool = False,
    trade_threshold: float = 0.0,
    passive_step: int = 1,
    **extra,
) -> dict:
    cfg = {
        "symbol": symbol,
        "mode": mode,
        "limit": limit,
        "max_spread": max_spread,
        "quote_offset": quote_offset,
        "edge": edge,
        "reversion_weight": reversion_weight,
        "imbalance_weight": imbalance_weight,
        "inventory_skew": inventory_skew,
        "passive_size": passive_size,
        "aggressive_size": aggressive_size,
        "passive_only": passive_only,
        "trade_threshold": trade_threshold,
        "passive_step": passive_step,
        "inventory_exit_quotes": True,
    }
    if working_limit is not None:
        cfg["working_limit"] = working_limit
    cfg.update(extra)
    return cfg


def voucher_product(
    symbol: str,
    strike: int,
    *,
    limit: int = 300,
    working_limit: int | None = None,
    max_spread: int,
    entry_threshold: float,
    quote_offset: int,
    cross_pad: float,
    signal_weight: float,
    inventory_skew: float,
    passive_size: int,
    aggressive_size: int,
    anchor_alpha: float = 0.02,
    passive_only: bool = False,
    neutral_two_sided: bool = False,
    inventory_exit_quotes: bool = True,
    min_price: int = 0,
    max_price: int | None = None,
    passive_step: int = 1,
    sigma_multiplier: float = 1.0,
    **extra,
) -> dict:
    cfg = {
        "symbol": symbol,
        "strike": strike,
        "limit": limit,
        "max_spread": max_spread,
        "entry_threshold": entry_threshold,
        "quote_offset": quote_offset,
        "cross_pad": cross_pad,
        "signal_weight": signal_weight,
        "inventory_skew": inventory_skew,
        "passive_size": passive_size,
        "aggressive_size": aggressive_size,
        "anchor_alpha": anchor_alpha,
        "passive_only": passive_only,
        "neutral_two_sided": neutral_two_sided,
        "inventory_exit_quotes": inventory_exit_quotes,
        "min_price": min_price,
        "passive_step": passive_step,
        "sigma_multiplier": sigma_multiplier,
    }
    if working_limit is not None:
        cfg["working_limit"] = working_limit
    if max_price is not None:
        cfg["max_price"] = max_price
    cfg.update(extra)
    return cfg


def clone(cfg: dict, **updates) -> dict:
    out = dict(cfg)
    out.update(updates)
    return out


HYDRO_BASE = delta_product(
    "HYDROGEL_PACK",
    mode="reversion",
    max_spread=18,
    quote_offset=6,
    edge=2,
    reversion_weight=0.40,
    imbalance_weight=0.0,
    inventory_skew=5.0,
    passive_size=8,
    aggressive_size=14,
)

VEX_BASE = delta_product(
    "VELVETFRUIT_EXTRACT",
    mode="reversion",
    max_spread=6,
    quote_offset=2,
    edge=1,
    reversion_weight=0.45,
    imbalance_weight=0.0,
    inventory_skew=4.0,
    passive_size=10,
    aggressive_size=16,
)

HYDRO_KALMAN = clone(
    HYDRO_BASE,
    fair_mode="kalman",
    trade_threshold=0.20,
    kalman_process_var=2.4,
    kalman_obs_var=18.0,
)

VEX_KALMAN = clone(
    VEX_BASE,
    fair_mode="kalman",
    trade_threshold=0.15,
    kalman_process_var=1.0,
    kalman_obs_var=6.0,
)

HYDRO_KALMAN_RET = clone(
    HYDRO_KALMAN,
    trade_threshold=0.24,
    regime_abs_move_cap=10.5,
    regime_abs_slope_cap=3.0,
    regime_abs_kalman_gap_cap=11.0,
    inventory_skew=5.2,
    no_new_entry_after=90000,
    hard_flat_after=98500,
)

VEX_KALMAN_RET = clone(
    VEX_KALMAN,
    trade_threshold=0.18,
    regime_abs_move_cap=4.8,
    regime_abs_slope_cap=1.5,
    regime_abs_kalman_gap_cap=4.7,
    inventory_skew=4.2,
    no_new_entry_after=90000,
    hard_flat_after=98500,
)

HYDRO_KALMAN_LATE = clone(
    HYDRO_KALMAN,
    trade_threshold=0.24,
    regime_abs_move_cap=10.0,
    regime_abs_slope_cap=2.8,
    regime_abs_kalman_gap_cap=10.5,
    inventory_skew=5.2,
    no_new_entry_after=82000,
    hard_flat_after=96500,
    max_entries_per_symbol=6,
)

VEX_KALMAN_LATE = clone(
    VEX_KALMAN,
    trade_threshold=0.18,
    regime_abs_move_cap=4.6,
    regime_abs_slope_cap=1.35,
    regime_abs_kalman_gap_cap=4.5,
    inventory_skew=4.2,
    no_new_entry_after=82000,
    hard_flat_after=96500,
    max_entries_per_symbol=6,
)

V4000_ITM_BASE = voucher_product(
    "VEV_4000",
    4000,
    max_spread=24,
    entry_threshold=0.90,
    quote_offset=3,
    cross_pad=0.22,
    signal_weight=0.40,
    inventory_skew=0.70,
    passive_size=2,
    aggressive_size=3,
    anchor_alpha=0.015,
    working_limit=32,
    vex_move_cap=6.0,
    vex_slope_cap=1.4,
    vex_move_ema_cap=2.8,
    vex_kalman_gap_cap=4.8,
)

V4500_ITM_BASE = voucher_product(
    "VEV_4500",
    4500,
    max_spread=18,
    entry_threshold=0.82,
    quote_offset=2,
    cross_pad=0.18,
    signal_weight=0.40,
    inventory_skew=0.70,
    passive_size=2,
    aggressive_size=3,
    anchor_alpha=0.015,
    working_limit=32,
    vex_move_cap=5.8,
    vex_slope_cap=1.35,
    vex_move_ema_cap=2.8,
    vex_kalman_gap_cap=4.6,
)

V4000_ITM_RET = clone(
    V4000_ITM_BASE,
    working_limit=26,
    passive_size=1,
    aggressive_size=2,
    entry_threshold=1.00,
    cross_pad=0.18,
    no_new_entry_after=82000,
    hard_flat_after=96000,
    max_entries_per_symbol=3,
    giveback_activation=0.22,
    giveback_stop=0.28,
    reentry_cooldown=9000,
    vex_move_cap=5.2,
    vex_slope_cap=1.15,
    vex_move_ema_cap=2.5,
    vex_kalman_gap_cap=4.2,
)

V4500_ITM_RET = clone(
    V4500_ITM_BASE,
    working_limit=26,
    passive_size=1,
    aggressive_size=2,
    entry_threshold=0.92,
    cross_pad=0.16,
    no_new_entry_after=82000,
    hard_flat_after=96000,
    max_entries_per_symbol=3,
    giveback_activation=0.20,
    giveback_stop=0.26,
    reentry_cooldown=9000,
    vex_move_cap=5.0,
    vex_slope_cap=1.10,
    vex_move_ema_cap=2.5,
    vex_kalman_gap_cap=4.0,
)

V4000_ITM_EARLY = clone(
    V4000_ITM_BASE,
    working_limit=22,
    passive_size=1,
    aggressive_size=2,
    entry_threshold=1.03,
    cross_pad=0.16,
    no_new_entry_after=72000,
    hard_flat_after=93000,
    max_entries_per_symbol=2,
    giveback_activation=0.18,
    giveback_stop=0.24,
    reentry_cooldown=12000,
    vex_move_cap=4.8,
    vex_slope_cap=1.00,
    vex_move_ema_cap=2.3,
    vex_kalman_gap_cap=3.8,
)

V4500_ITM_EARLY = clone(
    V4500_ITM_BASE,
    working_limit=22,
    passive_size=1,
    aggressive_size=2,
    entry_threshold=0.95,
    cross_pad=0.14,
    no_new_entry_after=72000,
    hard_flat_after=93000,
    max_entries_per_symbol=2,
    giveback_activation=0.16,
    giveback_stop=0.22,
    reentry_cooldown=12000,
    vex_move_cap=4.6,
    vex_slope_cap=0.95,
    vex_move_ema_cap=2.3,
    vex_kalman_gap_cap=3.6,
)

V5000_SALVAGE = voucher_product(
    "VEV_5000",
    5000,
    max_spread=5,
    entry_threshold=0.95,
    quote_offset=1,
    cross_pad=0.18,
    signal_weight=0.74,
    inventory_skew=1.15,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.020,
    working_limit=12,
    max_hold=12000,
    no_new_entry_after=52000,
    hard_flat_after=72000,
    giveback_activation=0.22,
    giveback_stop=0.30,
    reentry_cooldown=18000,
    max_entries_per_symbol=2,
    vex_move_cap=4.6,
    vex_slope_cap=0.95,
    vex_move_ema_cap=2.1,
    vex_kalman_gap_cap=3.5,
)

V5100_SALVAGE = voucher_product(
    "VEV_5100",
    5100,
    max_spread=7,
    entry_threshold=0.82,
    quote_offset=1,
    cross_pad=0.16,
    signal_weight=0.96,
    inventory_skew=1.25,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.020,
    working_limit=18,
    max_hold=12000,
    no_new_entry_after=52000,
    hard_flat_after=72000,
    giveback_activation=0.18,
    giveback_stop=0.26,
    reentry_cooldown=16000,
    max_entries_per_symbol=2,
    vex_move_cap=4.8,
    vex_slope_cap=1.00,
    vex_move_ema_cap=2.2,
    vex_kalman_gap_cap=3.6,
)

V5300_SALVAGE = voucher_product(
    "VEV_5300",
    5300,
    max_spread=3,
    entry_threshold=0.88,
    quote_offset=1,
    cross_pad=0.18,
    signal_weight=0.96,
    inventory_skew=0.92,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.024,
    working_limit=18,
    max_hold=15000,
    no_new_entry_after=60000,
    hard_flat_after=82000,
    giveback_activation=0.20,
    giveback_stop=0.28,
    reentry_cooldown=12000,
    max_entries_per_symbol=3,
    vex_move_cap=4.8,
    vex_slope_cap=1.00,
    vex_move_ema_cap=2.2,
    vex_kalman_gap_cap=3.8,
)

V5300_SALVAGE_SLOW = clone(
    V5300_SALVAGE,
    entry_threshold=0.94,
    cross_pad=0.14,
    signal_weight=0.88,
    working_limit=16,
    no_new_entry_after=68000,
    hard_flat_after=90000,
    max_hold=18000,
    giveback_activation=0.24,
    giveback_stop=0.32,
    max_entries_per_symbol=2,
)

V5000_TINY = clone(
    V5000_SALVAGE,
    working_limit=6,
    passive_size=1,
    aggressive_size=1,
    entry_threshold=1.05,
    no_new_entry_after=50000,
    hard_flat_after=70000,
    max_entries_per_symbol=1,
)

V5100_TINY = clone(
    V5100_SALVAGE,
    working_limit=8,
    passive_size=1,
    aggressive_size=1,
    entry_threshold=0.92,
    no_new_entry_after=50000,
    hard_flat_after=70000,
    max_entries_per_symbol=1,
)

V5300_TINY = clone(
    V5300_SALVAGE,
    working_limit=8,
    passive_size=1,
    aggressive_size=1,
    entry_threshold=0.96,
    no_new_entry_after=56000,
    hard_flat_after=78000,
    max_entries_per_symbol=2,
)

V5300_SIGNAL = voucher_product(
    "VEV_5300",
    5300,
    max_spread=3,
    entry_threshold=0.86,
    quote_offset=1,
    cross_pad=0.14,
    signal_weight=0.86,
    inventory_skew=0.88,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.024,
    working_limit=14,
    max_hold=14000,
    no_new_entry_after=62000,
    hard_flat_after=86000,
    giveback_activation=0.18,
    giveback_stop=0.26,
    reentry_cooldown=12000,
    max_entries_per_symbol=2,
    vex_move_cap=4.6,
    vex_slope_cap=0.95,
    vex_move_ema_cap=2.1,
    vex_kalman_gap_cap=3.6,
    same_side_penalty_symbols=["VEV_5100", "VEV_5200"],
    opposite_side_bonus_symbols=["VEV_5100"],
    watch_same_side_penalty_weight=0.45,
    watch_opposite_side_bonus_weight=0.12,
    watch_signal_cap=1.25,
    watch_abs_centered_caps={"VEV_5200": 2.4},
    veto_opposite_symbols=["VEV_5200"],
    veto_threshold=1.8,
)

V5100_KALMAN_CLUSTER = clone(
    V5100_SALVAGE,
    underlying_anchor_mode="kalman",
    same_side_penalty_symbols=["VEV_5200"],
    watch_same_side_penalty_weight=0.55,
    watch_signal_cap=1.15,
    watch_abs_centered_caps={"VEV_5200": 2.2},
    veto_opposite_symbols=["VEV_5200"],
    veto_threshold=1.7,
    buy_vex_slope_min=-0.35,
    buy_vex_slope_max=0.35,
    sell_vex_slope_min=-0.35,
    sell_vex_slope_max=0.35,
)

V5300_KALMAN_CLUSTER = clone(
    V5300_SALVAGE_SLOW,
    underlying_anchor_mode="kalman",
    same_side_penalty_symbols=["VEV_5100", "VEV_5200"],
    opposite_side_bonus_symbols=["VEV_5100"],
    watch_same_side_penalty_weight=0.40,
    watch_opposite_side_bonus_weight=0.10,
    watch_signal_cap=1.10,
    watch_abs_centered_caps={"VEV_5200": 2.2},
    veto_opposite_symbols=["VEV_5200"],
    veto_threshold=1.7,
    buy_vex_slope_min=-0.30,
    buy_vex_slope_max=0.30,
    sell_vex_slope_min=-0.30,
    sell_vex_slope_max=0.30,
)


WAVE5 = [
    {
        "bot_id": "W5-01",
        "filename": "candidate_w5_01_delta1_itm_final_control.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_KALMAN, VEX_KALMAN],
        "products": [V4000_ITM_BASE, V4500_ITM_BASE],
        "family": "wave4 winner frozen control",
        "features": ["kalman champion base", "active itm overlay", "live benchmark"],
        "hypothesis": "Freeze the exact W4-03 winner family as the live benchmark so every Wave 5 upside attempt is judged against the actual strongest clean architecture.",
    },
    {
        "bot_id": "W5-02",
        "filename": "candidate_w5_02_delta1_itm_retention_lock.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_KALMAN_RET, VEX_KALMAN_RET],
        "products": [V4000_ITM_RET, V4500_ITM_RET],
        "family": "winner retention lock",
        "features": ["champion+itm", "late lock", "cooldown", "entry cap"],
        "hypothesis": "The current winner should keep more of its path quality if the ITM overlay is gated earlier, capped in reentries, and forced into a calmer late-session posture.",
        "global_reentry_cooldown": 10000,
    },
    {
        "bot_id": "W5-03",
        "filename": "candidate_w5_03_delta1_itm_early_stop.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_KALMAN_LATE, VEX_KALMAN_LATE],
        "products": [V4000_ITM_EARLY, V4500_ITM_EARLY],
        "family": "winner early-stop retention",
        "features": ["champion+itm", "earlier no-new-entry", "fewer reentries"],
        "hypothesis": "If late churn is the remaining drag, a stricter early-stop version of the winner stack should sacrifice little core edge while reducing the worst end-of-run giveback patterns.",
        "global_reentry_cooldown": 14000,
    },
    {
        "bot_id": "W5-04",
        "filename": "candidate_w5_04_delta1_kalman_fallback.py",
        "kind": "delta1",
        "products": [HYDRO_KALMAN_RET, VEX_KALMAN_RET],
        "family": "pure delta1 fallback benchmark",
        "features": ["kalman delta1", "fallback benchmark"],
        "hypothesis": "Wave 5 still needs a pure-delta benchmark so that every upside-distillation branch is judged against both the winner stack and the cleanest conservative fallback.",
    },
    {
        "bot_id": "W5-05",
        "filename": "candidate_w5_05_vex_5000_5100_5300_distilled.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN_RET],
        "products": [V5000_SALVAGE, V5100_SALVAGE, V5300_SALVAGE],
        "family": "vex-anchored three-strike distilled salvage",
        "features": ["vex anchor", "5000/5100/5300 prune", "hard cutoff"],
        "hypothesis": "The highest-ceiling legacy branch should be retested only in a VEX-anchored, strike-pruned, retention-disciplined form without reopening 5200 or the broad basket.",
        "global_reentry_cooldown": 18000,
    },
    {
        "bot_id": "W5-06",
        "filename": "candidate_w5_06_vex_5100_5300_tte_decay.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN_RET],
        "products": [
            clone(V5100_SALVAGE, no_new_entry_after=46000, hard_flat_after=66000, max_entries_per_symbol=1),
            clone(V5300_SALVAGE_SLOW, no_new_entry_after=62000, hard_flat_after=84000, max_entries_per_symbol=2),
        ],
        "family": "vex-anchored 5100/5300 tte-style decay",
        "features": ["vex anchor", "5100/5300 only", "mid-session decay"],
        "hypothesis": "A TTE-style decay interpretation may salvage the best part of the old active cluster by letting 5100 fire early while 5300 is allowed a slightly slower linked horizon.",
        "global_reentry_cooldown": 18000,
    },
    {
        "bot_id": "W5-07",
        "filename": "candidate_w5_07_active_cluster_one_shot.py",
        "kind": "voucher",
        "products": [
            clone(V5000_TINY, reentry_cooldown=999999),
            clone(V5100_TINY, reentry_cooldown=999999),
            clone(V5300_TINY, reentry_cooldown=999999),
        ],
        "family": "pure active one-shot salvage",
        "features": ["active-only", "one-shot", "hard flatten"],
        "hypothesis": "One slot should still ask whether the old active cluster can retain meaningful upside on its own once continuation is brutally constrained to almost one-shot behavior.",
        "global_reentry_cooldown": 22000,
    },
    {
        "bot_id": "W5-08",
        "filename": "candidate_w5_08_vex_crossstrike_salvage.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN_RET],
        "products": [
            clone(
                V5100_SALVAGE,
                same_side_penalty_symbols=["VEV_5300"],
                opposite_side_bonus_symbols=["VEV_5300"],
                watch_same_side_penalty_weight=0.30,
                watch_opposite_side_bonus_weight=0.08,
                watch_signal_cap=1.05,
            ),
            clone(
                V5300_SALVAGE_SLOW,
                same_side_penalty_symbols=["VEV_5100"],
                opposite_side_bonus_symbols=["VEV_5100"],
                watch_same_side_penalty_weight=0.28,
                watch_opposite_side_bonus_weight=0.08,
                watch_signal_cap=1.05,
            ),
        ],
        "family": "cross-strike ordered salvage",
        "features": ["vex anchor", "5100/5300 pair", "relative gate"],
        "hypothesis": "The old surface intuition only deserves one more chance as a pruned 5100/5300 relative-value pair with strong timing discipline instead of a broad directional basket.",
        "global_reentry_cooldown": 16000,
    },
    {
        "bot_id": "W5-09",
        "filename": "candidate_w5_09_winner_plus_tiny_trio.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_KALMAN, VEX_KALMAN],
        "products": [V4000_ITM_RET, V4500_ITM_RET, V5000_TINY, V5100_TINY, V5300_TINY],
        "family": "winner plus tiny salvage trio",
        "features": ["winner stack", "tiny 5000/5100/5300 overlay"],
        "hypothesis": "If old upside can coexist with the winner at all, the safest place to test it is as a very small salvage trio riding on top of the proven champion-plus-ITM stack.",
        "global_reentry_cooldown": 16000,
    },
    {
        "bot_id": "W5-10",
        "filename": "candidate_w5_10_winner_plus_tiny_duo.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_KALMAN, VEX_KALMAN],
        "products": [V4000_ITM_RET, V4500_ITM_RET, V5100_TINY, V5300_TINY],
        "family": "winner plus tiny 5100/5300 duo",
        "features": ["winner stack", "tiny 5100/5300 overlay"],
        "hypothesis": "Removing 5000 may be the cleanest way to ask whether the highest legacy peak driver, 5100, can still add controlled upside when paired only with 5300 and the live winner base.",
        "global_reentry_cooldown": 16000,
    },
    {
        "bot_id": "W5-11",
        "filename": "candidate_w5_11_5300_toxic_veto.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN_RET],
        "products": [V5300_SIGNAL],
        "family": "5300 with toxic-strike veto threshold",
        "features": ["5300 only", "5100/5200 as signal", "transformed threshold"],
        "hypothesis": "Toxic strikes may still carry information even if they are bad inventory, so 5300 should be tested once with 5100 and 5200 acting as nonlinear veto and threshold shapers instead of direct legs.",
    },
    {
        "bot_id": "W5-12",
        "filename": "candidate_w5_12_kalman_regime_salvage.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN_RET],
        "products": [V5100_KALMAN_CLUSTER, V5300_KALMAN_CLUSTER],
        "family": "kalman regime salvage cluster",
        "features": ["kalman anchor", "trend gate", "toxic veto"],
        "hypothesis": "If one last active cluster deserves a smarter smoother, it is a compact 5100/5300 salvage pair with Kalman anchoring and simple trend discipline rather than another broad raw basket.",
        "underlying_anchor_mode": "kalman",
        "global_reentry_cooldown": 18000,
    },
]


NEW_SYNC_BLOCK = textwrap.dedent(
    """\
    def sync_position_state(store, symbol, position, centered, timestamp):
        previous = dict(store.get(symbol, {}))
        previous_position = int(previous.get("last_position", 0))
        block_until = previous.get("block_until")
        entries_count = int(previous.get("entries_count", 0))
        if position == 0:
            current = {
                "last_position": 0,
                "entries_count": entries_count,
            }
        elif previous_position == 0 or sign(previous_position) != sign(position):
            current = {
                "last_position": int(position),
                "entry_timestamp": int(timestamp),
                "entry_centered": float(centered),
                "best_improvement": 0.0,
                "entries_count": entries_count + 1,
            }
        else:
            current = previous
            current["last_position"] = int(position)
            current.setdefault("entry_timestamp", int(timestamp))
            current.setdefault("entry_centered", float(centered))
            current.setdefault("best_improvement", 0.0)
            current.setdefault("entries_count", entries_count)
        if block_until is not None and int(block_until) > int(timestamp):
            current["block_until"] = int(block_until)
        current["last_centered"] = float(centered)
        store[symbol] = current
        return current


    def should_take_profit(position, centered, position_state, cfg):
        if position == 0:
            return False
        entry_centered = float(position_state.get("entry_centered", centered))
        tp_improve = cfg.get("tp_improve")
        tp_abs_threshold = cfg.get("tp_abs_threshold")
        if position > 0:
            if tp_abs_threshold is not None and centered >= -float(tp_abs_threshold):
                return True
            if tp_improve is not None and centered - entry_centered >= float(tp_improve):
                return True
        if position < 0:
            if tp_abs_threshold is not None and centered <= float(tp_abs_threshold):
                return True
            if tp_improve is not None and entry_centered - centered >= float(tp_improve):
                return True
        return False


    def should_stop_out(position, centered, position_state, cfg):
        stop_width = cfg.get("adverse_move_stop")
        if position == 0 or stop_width is None:
            return False
        entry_centered = float(position_state.get("entry_centered", centered))
        stop_width = float(stop_width)
        if position > 0 and entry_centered - centered >= stop_width:
            return True
        if position < 0 and centered - entry_centered >= stop_width:
            return True
        return False


    def should_time_stop(position, timestamp, position_state, cfg):
        max_hold = cfg.get("max_hold")
        if position == 0 or max_hold is None:
            return False
        entry_timestamp = position_state.get("entry_timestamp")
        if entry_timestamp is None:
            return False
        return int(timestamp) - int(entry_timestamp) >= int(max_hold)


    def should_late_flat(position, timestamp, cfg):
        hard_flat_after = cfg.get("hard_flat_after")
        if position == 0 or hard_flat_after is None:
            return False
        return int(timestamp) >= int(hard_flat_after)


    def update_position_progress(position, centered, position_state):
        if position == 0:
            position_state["best_improvement"] = 0.0
            return 0.0, 0.0
        entry_centered = float(position_state.get("entry_centered", centered))
        if position > 0:
            improvement = float(centered) - entry_centered
        else:
            improvement = entry_centered - float(centered)
        best_improvement = max(float(position_state.get("best_improvement", 0.0)), improvement)
        position_state["best_improvement"] = best_improvement
        return improvement, best_improvement


    def should_giveback_stop(position, improvement, best_improvement, cfg):
        giveback_stop = cfg.get("giveback_stop")
        if position == 0 or giveback_stop is None:
            return False
        activation = float(cfg.get("giveback_activation", 0.0))
        if best_improvement < activation:
            return False
        return best_improvement - improvement >= float(giveback_stop)


    def set_reentry_cooldown(position_state, timestamp, cfg):
        cooldown = cfg.get("reentry_cooldown")
        if cooldown is None:
            return
        position_state["block_until"] = int(timestamp) + int(cooldown)


    def set_global_cooldown(data, timestamp, cfg):
        cooldown = cfg.get("global_reentry_cooldown")
        if cooldown is None:
            return
        data["global_block_until"] = int(timestamp) + int(cooldown)


    def allow_new_entries(timestamp, cfg, position_state=None, global_block_until=None):
        regime_start_after = cfg.get("regime_start_after")
        if regime_start_after is not None and int(timestamp) < int(regime_start_after):
            return False
        no_new_entry_after = cfg.get("no_new_entry_after")
        if no_new_entry_after is not None and int(timestamp) >= int(no_new_entry_after):
            return False
        if global_block_until is not None and int(timestamp) < int(global_block_until):
            return False
        if position_state is not None:
            block_until = position_state.get("block_until")
            if block_until is not None and int(timestamp) < int(block_until):
                return False
            max_entries = cfg.get("max_entries_per_symbol")
            if max_entries is not None and int(position_state.get("entries_count", 0)) >= int(max_entries):
                return False
        return True


    def buy_allowed_by_imbalance(imbalance, cfg):
        minimum = cfg.get("buy_imbalance_min")
        return minimum is None or imbalance >= float(minimum)


    def sell_allowed_by_imbalance(imbalance, cfg):
        maximum = cfg.get("sell_imbalance_max")
        return maximum is None or imbalance <= float(maximum)
    """
)


NEW_STATE_BLOCK = textwrap.dedent(
    """\
    def update_sigma(data, vex_mid, config):
        voucher_meta = data.setdefault("voucher_meta", {})
        sigma_abs = float(voucher_meta.get("sigma_abs", config.get("sigma_abs_default", DEFAULT_SIGMA)))
        prev_vex_mid = voucher_meta.get("prev_vex_mid")
        sigma_floor = float(config.get("sigma_abs_floor", DEFAULT_SIGMA_FLOOR))
        sigma_cap = float(config.get("sigma_abs_cap", DEFAULT_SIGMA_CAP))
        sigma_alpha = float(config.get("sigma_alpha", DEFAULT_SIGMA_ALPHA))
        sigma_move_scale = float(config.get("sigma_move_scale", DEFAULT_SIGMA_MOVE_SCALE))
        if prev_vex_mid is not None:
            target = sigma_floor + sigma_move_scale * abs(float(vex_mid) - float(prev_vex_mid))
            target = max(sigma_floor, min(sigma_cap, target))
            sigma_abs = (1.0 - sigma_alpha) * sigma_abs + sigma_alpha * target
        voucher_meta["sigma_abs"] = sigma_abs
        voucher_meta["prev_vex_mid"] = float(vex_mid)
        return sigma_abs


    def append_history(store, key, value, max_len):
        size = max(2, int(max_len))
        history = list(store.get(key, []))
        history.append(float(value))
        if len(history) > size:
            history = history[-size:]
        store[key] = history
        return history


    def ema_update(previous, value, alpha):
        if previous is None:
            return float(value)
        alpha = float(alpha)
        return (1.0 - alpha) * float(previous) + alpha * float(value)


    def rolling_slope(values):
        n = len(values)
        if n < 2:
            return 0.0
        mean_x = 0.5 * float(n - 1)
        mean_y = sum(float(v) for v in values) / float(n)
        denom = sum((float(i) - mean_x) ** 2 for i in range(n))
        if denom <= 0:
            return 0.0
        numer = sum((float(i) - mean_x) * (float(v) - mean_y) for i, v in enumerate(values))
        return numer / denom


    def kalman_update(store, observation, process_var, obs_var):
        observation = float(observation)
        process_var = max(1e-6, float(process_var))
        obs_var = max(1e-6, float(obs_var))
        mean = float(store.get("mean", observation))
        variance = float(store.get("variance", obs_var))
        variance += process_var
        gain = variance / (variance + obs_var)
        mean = mean + gain * (observation - mean)
        variance = (1.0 - gain) * variance
        store["mean"] = mean
        store["variance"] = variance
        return mean


    def update_delta_metrics(data, symbol, mid, cfg):
        delta_state = data.setdefault("delta_state", {})
        store = delta_state.setdefault(symbol, {})
        prev_mid = store.get("prev_mid")
        ema_mid = ema_update(store.get("ema_mid"), mid, cfg.get("ema_alpha", 0.25))
        history = append_history(store, "mid_history", mid, cfg.get("slope_window", 6))
        slope = rolling_slope(history)
        move = 0.0 if prev_mid is None else float(mid) - float(prev_mid)
        move_ema = ema_update(store.get("move_ema"), abs(move), cfg.get("move_alpha", 0.25))
        kalman_state = store.setdefault("kalman", {})
        kalman_mean = kalman_update(
            kalman_state,
            mid,
            cfg.get("kalman_process_var", 2.0),
            cfg.get("kalman_obs_var", 12.0),
        )
        store["prev_mid"] = float(mid)
        store["ema_mid"] = ema_mid
        store["move_ema"] = move_ema
        return {
            "prev_mid": prev_mid,
            "ema_mid": ema_mid,
            "move": move,
            "move_ema": move_ema,
            "slope": slope,
            "kalman_mean": kalman_mean,
            "kalman_gap": float(mid) - float(kalman_mean),
        }


    def update_vex_metrics(data, vex_mid, vex_imbalance, config):
        voucher_meta = data.setdefault("voucher_meta", {})
        prev_mid = voucher_meta.get("prev_vex_mid")
        ema_mid = ema_update(voucher_meta.get("ema_vex_mid"), vex_mid, config.get("vex_ema_alpha", 0.25))
        history = append_history(voucher_meta, "vex_mid_history", vex_mid, config.get("vex_slope_window", 8))
        slope = rolling_slope(history)
        move = 0.0 if prev_mid is None else float(vex_mid) - float(prev_mid)
        move_ema = ema_update(voucher_meta.get("vex_move_ema"), abs(move), config.get("vex_move_alpha", 0.25))
        kalman_state = voucher_meta.setdefault("vex_kalman", {})
        kalman_mean = kalman_update(
            kalman_state,
            vex_mid,
            config.get("vex_kalman_process_var", 1.0),
            config.get("vex_kalman_obs_var", 8.0),
        )
        voucher_meta["prev_vex_mid"] = float(vex_mid)
        voucher_meta["ema_vex_mid"] = ema_mid
        voucher_meta["vex_move_ema"] = move_ema
        voucher_meta["vex_last_imbalance"] = float(vex_imbalance)
        return {
            "prev_mid": prev_mid,
            "ema_mid": ema_mid,
            "move": move,
            "move_ema": move_ema,
            "slope": slope,
            "kalman_mean": kalman_mean,
            "kalman_gap": float(vex_mid) - float(kalman_mean),
            "imbalance": float(vex_imbalance),
        }


    def get_reference_mid(metrics, cfg):
        mode = cfg.get("fair_mode", "prev_mid")
        if mode == "kalman":
            return metrics["kalman_mean"]
        if mode == "ema":
            return metrics["ema_mid"]
        return metrics["prev_mid"]


    def under_cap(value, cap):
        if cap is None:
            return True
        return abs(float(value)) <= float(cap)


    def delta_regime_ok(metrics, spread, imbalance, cfg):
        if cfg.get("regime_max_spread") is not None and float(spread) > float(cfg["regime_max_spread"]):
            return False
        if not under_cap(metrics["move"], cfg.get("regime_abs_move_cap")):
            return False
        if not under_cap(metrics["slope"], cfg.get("regime_abs_slope_cap")):
            return False
        if not under_cap(metrics["ema_mid"] - metrics["kalman_mean"], cfg.get("regime_abs_ema_gap_cap")):
            return False
        if not under_cap(metrics["kalman_gap"], cfg.get("regime_abs_kalman_gap_cap")):
            return False
        if not under_cap(imbalance, cfg.get("regime_abs_imbalance_cap")):
            return False
        return True


    def voucher_regime_ok(vex_metrics, spread, cfg, timestamp):
        regime_stop_after = cfg.get("regime_stop_after")
        if regime_stop_after is not None and int(timestamp) >= int(regime_stop_after):
            return False
        if spread > cfg["max_spread"]:
            return False
        if not under_cap(vex_metrics["move"], cfg.get("vex_move_cap")):
            return False
        if not under_cap(vex_metrics["move_ema"], cfg.get("vex_move_ema_cap")):
            return False
        if not under_cap(vex_metrics["slope"], cfg.get("vex_slope_cap")):
            return False
        if not under_cap(vex_metrics["kalman_gap"], cfg.get("vex_kalman_gap_cap")):
            return False
        if not under_cap(vex_metrics["imbalance"], cfg.get("vex_abs_imbalance_cap")):
            return False
        return True


    def dynamic_entry_threshold(base, spread, vex_metrics, cfg):
        threshold = float(base)
        threshold += abs(float(vex_metrics["move"])) * float(cfg.get("vex_move_weight", 0.0))
        threshold += abs(float(vex_metrics["move_ema"])) * float(cfg.get("vex_move_ema_weight", 0.0))
        threshold += abs(float(vex_metrics["slope"])) * float(cfg.get("vex_slope_weight", 0.0))
        threshold += abs(float(vex_metrics["kalman_gap"])) * float(cfg.get("vex_kalman_gap_weight", 0.0))
        spread_ref = float(cfg.get("spread_ref", 0.0))
        threshold += max(0.0, float(spread) - spread_ref) * float(cfg.get("spread_excess_weight", 0.0))
        return threshold


    def apply_trend_gate(want_buy, want_sell, vex_metrics, cfg):
        slope = float(vex_metrics["slope"])
        buy_max = cfg.get("buy_vex_slope_max")
        buy_min = cfg.get("buy_vex_slope_min")
        sell_max = cfg.get("sell_vex_slope_max")
        sell_min = cfg.get("sell_vex_slope_min")
        if want_buy and buy_max is not None and slope > float(buy_max):
            want_buy = False
        if want_buy and buy_min is not None and slope < float(buy_min):
            want_buy = False
        if want_sell and sell_max is not None and slope > float(sell_max):
            want_sell = False
        if want_sell and sell_min is not None and slope < float(sell_min):
            want_sell = False
        return want_buy, want_sell


    def effective_limit(cfg):
        return int(cfg.get("working_limit", cfg["limit"]))


    def strike_from_symbol(symbol):
        if not symbol.startswith("VEV_"):
            return None
        try:
            return int(symbol.split("_", 1)[1])
        except Exception:
            return None


    def collect_watch_symbols(config):
        watch_symbols = set()
        for cfg in config["products"]:
            for key in (
                "confirm_same_side_symbols",
                "veto_opposite_symbols",
                "same_side_penalty_symbols",
                "opposite_side_bonus_symbols",
            ):
                for symbol in cfg.get(key, []):
                    watch_symbols.add(symbol)
            for symbol in cfg.get("watch_abs_centered_caps", {}).keys():
                watch_symbols.add(symbol)
        return sorted(watch_symbols)


    def build_watch_contexts(state, data, config, vex_mid, sigma_abs):
        anchors = data.setdefault("voucher_anchor", {})
        contexts = {}
        for symbol in collect_watch_symbols(config):
            order_depth = state.order_depths.get(symbol)
            strike = strike_from_symbol(symbol)
            if order_depth is None or strike is None:
                continue
            mid = get_mid(order_depth)
            spread = get_spread(order_depth)
            if mid is None or spread is None:
                continue
            fair_model = bachelier_call(vex_mid, strike, config.get("tte_days", DEFAULT_TTE_DAYS), sigma_abs)
            raw_residual = float(mid) - float(fair_model)
            anchor = float(anchors.get(symbol, raw_residual))
            contexts[symbol] = {
                "mid": float(mid),
                "spread": float(spread),
                "imbalance": get_imbalance(order_depth),
                "raw_residual": raw_residual,
                "centered": raw_residual - anchor,
            }
            alpha = float(config.get("watch_anchor_alpha", config.get("default_anchor_alpha", 0.02)))
            anchors[symbol] = (1.0 - alpha) * anchor + alpha * raw_residual
        return contexts


    def transformed_threshold(base, side, watch_contexts, cfg):
        threshold = float(base)
        same_weight = float(cfg.get("watch_same_side_penalty_weight", 0.0))
        opposite_weight = float(cfg.get("watch_opposite_side_bonus_weight", 0.0))
        cap = float(cfg.get("watch_signal_cap", 9.0))
        for symbol in cfg.get("same_side_penalty_symbols", []):
            context = watch_contexts.get(symbol)
            if context is None:
                continue
            centered = float(context["centered"])
            if side == "buy" and centered < 0.0:
                threshold += same_weight * min(cap, abs(centered))
            if side == "sell" and centered > 0.0:
                threshold += same_weight * min(cap, abs(centered))
        for symbol in cfg.get("opposite_side_bonus_symbols", []):
            context = watch_contexts.get(symbol)
            if context is None:
                continue
            centered = float(context["centered"])
            if side == "buy" and centered > 0.0:
                threshold -= opposite_weight * min(cap, abs(centered))
            if side == "sell" and centered < 0.0:
                threshold -= opposite_weight * min(cap, abs(centered))
        return max(float(cfg.get("min_entry_threshold", 0.0)), threshold)


    def watch_state_allows(side, watch_contexts, cfg):
        confirm_threshold = float(cfg.get("confirm_threshold", 0.0))
        veto_threshold = float(cfg.get("veto_threshold", 0.0))
        for symbol, cap in cfg.get("watch_abs_centered_caps", {}).items():
            context = watch_contexts.get(symbol)
            if context is not None and abs(float(context["centered"])) > float(cap):
                return False
        confirms = cfg.get("confirm_same_side_symbols", [])
        if confirms:
            confirm_hit = False
            for symbol in confirms:
                context = watch_contexts.get(symbol)
                if context is None:
                    continue
                centered = float(context["centered"])
                if side == "buy" and centered <= -confirm_threshold:
                    confirm_hit = True
                if side == "sell" and centered >= confirm_threshold:
                    confirm_hit = True
            if not confirm_hit:
                return False
        for symbol in cfg.get("veto_opposite_symbols", []):
            context = watch_contexts.get(symbol)
            if context is None:
                continue
            centered = float(context["centered"])
            if side == "buy" and centered <= -veto_threshold:
                return False
            if side == "sell" and centered >= veto_threshold:
                return False
        return True
    """
)


NEW_DELTA_BLOCK = textwrap.dedent(
    """\
    def run_delta1_products(state, result, data, products):
        timestamp = int(getattr(state, "timestamp", 0))
        global_block_until = data.get("global_block_until")
        delta_position_state = data.setdefault("delta_position_state", {})
        for cfg in products:
            symbol = cfg["symbol"]
            order_depth = state.order_depths.get(symbol)
            if order_depth is None:
                continue
            mid = get_mid(order_depth)
            spread = get_spread(order_depth)
            best_bid = get_best_bid(order_depth)
            best_ask = get_best_ask(order_depth)
            if mid is None or spread is None or best_bid is None or best_ask is None:
                continue

            metrics = update_delta_metrics(data, symbol, mid, cfg)
            if spread > cfg["max_spread"]:
                continue

            position = int(state.position.get(symbol, 0))
            limit = effective_limit(cfg)
            imbalance = get_imbalance(order_depth)
            reference_mid = get_reference_mid(metrics, cfg)
            signal = 0.0
            if cfg["mode"] in ("reversion", "hybrid") and reference_mid is not None:
                signal += float(cfg["reversion_weight"]) * (float(reference_mid) - float(mid))
            if cfg["mode"] in ("imbalance", "hybrid"):
                signal += float(cfg["imbalance_weight"]) * imbalance

            fair = float(mid) + signal - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
            trade_threshold = float(cfg.get("trade_threshold", 0.0))
            regime_ok = delta_regime_ok(metrics, spread, imbalance, cfg)
            orders = []
            position_state = sync_position_state(delta_position_state, symbol, position, signal, timestamp)
            force_exit = should_late_flat(position, timestamp, cfg)
            if force_exit:
                exit_orders, position = flatten_position(symbol, order_depth, position, limit)
                orders.extend(exit_orders)
            else:
                entries_allowed = regime_ok and allow_new_entries(timestamp, cfg, position_state, global_block_until)
                if entries_allowed and not cfg.get("passive_only", False) and abs(signal) >= trade_threshold:
                    if signal > 0:
                        new_orders, position = take_from_asks(
                            symbol,
                            order_depth,
                            position,
                            limit,
                            cfg.get("aggressive_size", cfg["passive_size"]),
                            fair - cfg["edge"],
                        )
                        orders.extend(new_orders)
                    elif signal < 0:
                        new_orders, position = hit_bids(
                            symbol,
                            order_depth,
                            position,
                            limit,
                            cfg.get("aggressive_size", cfg["passive_size"]),
                            fair + cfg["edge"],
                        )
                        orders.extend(new_orders)

                buy_qty = clamp_qty(cfg["passive_size"], position, limit)
                sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
                quote_buy = False
                quote_sell = False
                if entries_allowed:
                    quote_buy = True
                    quote_sell = True
                    if abs(signal) >= trade_threshold:
                        if signal > 0:
                            quote_sell = False
                        elif signal < 0:
                            quote_buy = False

                if cfg.get("inventory_exit_quotes", True):
                    if position > 0:
                        quote_sell = True
                    elif position < 0:
                        quote_buy = True

                if quote_buy and buy_qty > 0:
                    price = passive_bid_price(fair, cfg, best_bid, best_ask)
                    orders.append(Order(symbol, int(price), int(buy_qty)))
                if quote_sell and sell_qty < 0:
                    price = passive_ask_price(fair, cfg, best_bid, best_ask)
                    orders.append(Order(symbol, int(price), int(sell_qty)))

            append_orders(result, symbol, orders)
    """
)


NEW_VOUCHER_BLOCK = textwrap.dedent(
    """\
    def run_voucher_products(state, result, data, config):
        sidecars = config.get("sidecar_products", [])
        if sidecars:
            run_delta1_products(state, result, data, sidecars)

        vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_mid = get_mid(vex_depth) if vex_depth is not None else None
        if vex_mid is None:
            return

        vex_imbalance = get_imbalance(vex_depth) if vex_depth is not None else 0.0
        sigma_abs = update_sigma(data, vex_mid, config)
        vex_metrics = update_vex_metrics(data, vex_mid, vex_imbalance, config)
        watch_contexts = build_watch_contexts(state, data, config, vex_mid, sigma_abs)
        anchors = data.setdefault("voucher_anchor", {})
        position_states = data.setdefault("voucher_position_state", {})
        timestamp = int(getattr(state, "timestamp", 0))
        global_block_until = data.get("global_block_until")

        for cfg in config["products"]:
            symbol = cfg["symbol"]
            order_depth = state.order_depths.get(symbol)
            if order_depth is None:
                continue
            best_bid = get_best_bid(order_depth)
            best_ask = get_best_ask(order_depth)
            mid = get_mid(order_depth)
            spread = get_spread(order_depth)
            if best_bid is None or best_ask is None or mid is None or spread is None:
                continue

            position = int(state.position.get(symbol, 0))
            limit = effective_limit(cfg)
            imbalance = get_imbalance(order_depth)
            anchor_mode = cfg.get("underlying_anchor_mode", config.get("underlying_anchor_mode", "mid"))
            underlying_mid = vex_metrics["kalman_mean"] if anchor_mode == "kalman" else vex_mid
            sigma_multiplier = float(cfg.get("sigma_multiplier", 1.0))
            fair_model = bachelier_call(
                underlying_mid,
                cfg["strike"],
                config.get("tte_days", DEFAULT_TTE_DAYS),
                sigma_abs * sigma_multiplier,
            )
            raw_residual = float(mid) - float(fair_model)
            anchor = float(anchors.get(symbol, raw_residual))
            centered = raw_residual - anchor
            direction_mode = cfg.get("direction_mode", "normal")
            direction_sign = -1.0 if direction_mode == "normal" else 1.0
            fair = (
                float(fair_model)
                + anchor
                + direction_sign * float(cfg["signal_weight"]) * centered
                - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
            )
            position_state = sync_position_state(position_states, symbol, position, centered, timestamp)
            improvement, best_improvement = update_position_progress(position, centered, position_state)
            orders = []
            giveback_exit = should_giveback_stop(position, improvement, best_improvement, cfg)
            stop_exit = should_stop_out(position, centered, position_state, cfg)
            force_exit = (
                should_late_flat(position, timestamp, cfg)
                or should_time_stop(position, timestamp, position_state, cfg)
                or stop_exit
                or should_take_profit(position, centered, position_state, cfg)
                or giveback_exit
            )

            if force_exit:
                if giveback_exit or stop_exit:
                    set_reentry_cooldown(position_state, timestamp, cfg)
                    set_global_cooldown(data, timestamp, config)
                exit_orders, position = flatten_position(symbol, order_depth, position, limit)
                orders.extend(exit_orders)
            elif spread <= cfg["max_spread"]:
                base_threshold = dynamic_entry_threshold(cfg["entry_threshold"], spread, vex_metrics, cfg)
                buy_threshold = transformed_threshold(base_threshold, "buy", watch_contexts, cfg)
                sell_threshold = transformed_threshold(base_threshold, "sell", watch_contexts, cfg)
                if direction_mode == "inverse":
                    want_buy = centered > float(buy_threshold)
                    want_sell = centered < -float(sell_threshold)
                else:
                    want_buy = centered < -float(buy_threshold)
                    want_sell = centered > float(sell_threshold)
                want_buy, want_sell = apply_trend_gate(want_buy, want_sell, vex_metrics, cfg)
                if want_buy and not buy_allowed_by_imbalance(imbalance, cfg):
                    want_buy = False
                if want_sell and not sell_allowed_by_imbalance(imbalance, cfg):
                    want_sell = False
                if want_buy and not watch_state_allows("buy", watch_contexts, cfg):
                    want_buy = False
                if want_sell and not watch_state_allows("sell", watch_contexts, cfg):
                    want_sell = False

                regime_ok = voucher_regime_ok(vex_metrics, spread, cfg, timestamp)
                entries_allowed = regime_ok and allow_new_entries(timestamp, cfg, position_state, global_block_until)

                if entries_allowed and not cfg.get("passive_only", False):
                    if want_buy:
                        active_orders, position = take_from_asks(
                            symbol,
                            order_depth,
                            position,
                            limit,
                            cfg.get("aggressive_size", cfg["passive_size"]),
                            fair + cfg["cross_pad"],
                        )
                        orders.extend(active_orders)
                    elif want_sell:
                        active_orders, position = hit_bids(
                            symbol,
                            order_depth,
                            position,
                            limit,
                            cfg.get("aggressive_size", cfg["passive_size"]),
                            fair - cfg["cross_pad"],
                        )
                        orders.extend(active_orders)

                buy_qty = clamp_qty(cfg["passive_size"], position, limit)
                sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
                quote_buy = False
                quote_sell = False

                if entries_allowed:
                    if want_buy:
                        quote_buy = True
                    elif want_sell:
                        quote_sell = True
                    elif cfg.get("neutral_two_sided", False):
                        quote_buy = True
                        quote_sell = True

                if cfg.get("inventory_exit_quotes", True):
                    if position > 0:
                        quote_sell = True
                    elif position < 0:
                        quote_buy = True

                if quote_buy and buy_qty > 0:
                    buy_price = passive_bid_price(fair, cfg, best_bid, best_ask)
                    orders.append(Order(symbol, int(buy_price), int(buy_qty)))
                if quote_sell and sell_qty < 0:
                    sell_price = passive_ask_price(fair, cfg, best_bid, best_ask)
                    orders.append(Order(symbol, int(sell_price), int(sell_qty)))

            append_orders(result, symbol, orders)
            alpha = float(cfg.get("anchor_alpha", config.get("default_anchor_alpha", 0.02)))
            anchors[symbol] = (1.0 - alpha) * anchor + alpha * raw_residual
    """
)


def replace_block(source: str, start_marker: str, end_marker: str, replacement: str) -> str:
    start = source.index(start_marker)
    end = source.index(end_marker, start)
    return source[:start] + replacement + "\n\n" + source[end:]


def render_config(config: dict) -> str:
    return pprint.pformat(config, sort_dicts=True, width=100)


def build_template() -> str:
    source = TEMPLATE_SOURCE.read_text()
    header = textwrap.dedent(
        f"""\
        \"\"\"
        Generated Round 3 Wave 5 exploitation / upside-distillation bot.
        Batch spec: {SPEC_PATH}
        Bot ID: __BOT_ID__
        Family: __FAMILY__
        Hypothesis: __HYPOTHESIS__
        \"\"\"

        """
    )
    source = re.sub(r'^""".*?"""\n\n', header, source, count=1, flags=re.S)
    source = re.sub(r"CONFIG = .*?\n\nSQRT_2 =", "CONFIG = __CONFIG__\n\nSQRT_2 =", source, count=1, flags=re.S)
    source = replace_block(source, "def sync_position_state", "def update_sigma", NEW_SYNC_BLOCK)
    source = replace_block(source, "def update_sigma", "def run_delta1_products", NEW_STATE_BLOCK)
    source = replace_block(source, "def run_delta1_products", "def run_voucher_products", NEW_DELTA_BLOCK)
    source = replace_block(source, "def run_voucher_products", "def run_floor_products", NEW_VOUCHER_BLOCK)
    return source


BASE_TEMPLATE = build_template()


def bot_contents(config: dict) -> str:
    return (
        BASE_TEMPLATE.replace("__BOT_ID__", config["bot_id"])
        .replace("__FAMILY__", config["family"])
        .replace("__HYPOTHESIS__", config["hypothesis"])
        .replace("__CONFIG__", render_config(config))
    )


def describe_products(config: dict) -> str:
    symbols = []
    for sidecar in config.get("sidecar_products", []):
        symbols.append(sidecar["symbol"])
    for product in config.get("products", []):
        symbols.append(product["symbol"])
    return ", ".join(symbols)


def render_manifest(configs: list[dict]) -> str:
    lines = [
        "# Finalist Batch Wave 5 Manifest",
        "",
        "Generated from `generate_learning_batch_wave5.py`.",
        "",
        f"- Spec: [`../04_strategy_specs/{SPEC_PATH}`](../04_strategy_specs/{SPEC_PATH})",
        "- Owner: `amin`",
        f"- Batch size: `{len(configs)}`",
        "- Intent: `winner-protection / upside-distillation / final submission narrowing`",
        "",
        "| Bot ID | File | Family | Products | Key Axes | Hypothesis |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for cfg in configs:
        lines.append(
            "| `{bot_id}` | `../bots/amin/canonical/{filename}` | {family} | {products} | {features} | {hypothesis} |".format(
                bot_id=cfg["bot_id"],
                filename=cfg["filename"],
                family=cfg["family"],
                products=describe_products(cfg),
                features=", ".join(cfg.get("features", [])),
                hypothesis=cfg["hypothesis"],
            )
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    BOT_DIR.mkdir(parents=True, exist_ok=True)
    for config in WAVE5:
        path = BOT_DIR / config["filename"]
        path.write_text(bot_contents(config))
    MANIFEST.write_text(render_manifest(WAVE5))


if __name__ == "__main__":
    main()
