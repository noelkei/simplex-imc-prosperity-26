from __future__ import annotations

import pprint
import re
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
BOT_DIR = ROUND / "bots" / "amin" / "canonical"
MANIFEST = ROUND / "workspace" / "05_implementation" / "learning_batch_wave3_manifest.md"
TEMPLATE_SOURCE = ROUND / "bots" / "amin" / "historical" / "candidate_w2_01_delta1_dual_control.py"
SPEC_PATH = "spec_learning_batch_wave3.md"


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


HYDRO_REV = delta_product(
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

VEX_REV = delta_product(
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

HYDRO_GATE = clone(
    HYDRO_REV,
    trade_threshold=0.3,
    regime_abs_move_cap=8.0,
    regime_abs_slope_cap=2.8,
    regime_abs_kalman_gap_cap=10.0,
    ema_alpha=0.22,
    slope_window=6,
)

VEX_GATE = clone(
    VEX_REV,
    trade_threshold=0.2,
    regime_abs_move_cap=4.0,
    regime_abs_slope_cap=1.4,
    regime_abs_kalman_gap_cap=4.5,
    ema_alpha=0.25,
    slope_window=8,
)

HYDRO_KALMAN = clone(
    HYDRO_REV,
    fair_mode="kalman",
    trade_threshold=0.2,
    kalman_process_var=2.4,
    kalman_obs_var=18.0,
)

VEX_KALMAN = clone(
    VEX_REV,
    fair_mode="kalman",
    trade_threshold=0.15,
    kalman_process_var=1.0,
    kalman_obs_var=6.0,
)

V4000_ACTIVE = voucher_product(
    "VEV_4000",
    4000,
    max_spread=24,
    entry_threshold=0.95,
    quote_offset=3,
    cross_pad=0.25,
    signal_weight=0.42,
    inventory_skew=0.8,
    passive_size=3,
    aggressive_size=5,
    anchor_alpha=0.015,
    working_limit=75,
    no_new_entry_after=760000,
    hard_flat_after=880000,
)

V4500_ACTIVE = voucher_product(
    "VEV_4500",
    4500,
    max_spread=18,
    entry_threshold=0.85,
    quote_offset=2,
    cross_pad=0.20,
    signal_weight=0.42,
    inventory_skew=0.8,
    passive_size=3,
    aggressive_size=5,
    anchor_alpha=0.015,
    working_limit=75,
    no_new_entry_after=760000,
    hard_flat_after=880000,
)

V5300_BASE = voucher_product(
    "VEV_5300",
    5300,
    max_spread=3,
    entry_threshold=1.0,
    quote_offset=1,
    cross_pad=0.40,
    signal_weight=0.88,
    inventory_skew=1.0,
    passive_size=5,
    aggressive_size=8,
    anchor_alpha=0.025,
    working_limit=80,
)

V5000_BASE = voucher_product(
    "VEV_5000",
    5000,
    max_spread=8,
    entry_threshold=1.45,
    quote_offset=2,
    cross_pad=0.45,
    signal_weight=0.82,
    inventory_skew=1.0,
    passive_size=3,
    aggressive_size=5,
    anchor_alpha=0.02,
    working_limit=50,
)

V5000_INV = clone(
    V5000_BASE,
    direction_mode="inverse",
    working_limit=18,
    passive_size=1,
    aggressive_size=2,
    entry_threshold=1.35,
    max_hold=12000,
    tp_improve=0.8,
    tp_abs_threshold=0.25,
    adverse_move_stop=1.1,
    no_new_entry_after=300000,
    hard_flat_after=520000,
)

V5100_INV = voucher_product(
    "VEV_5100",
    5100,
    max_spread=6,
    entry_threshold=1.60,
    quote_offset=2,
    cross_pad=0.25,
    signal_weight=0.86,
    inventory_skew=2.6,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.02,
    working_limit=18,
    direction_mode="inverse",
    max_hold=12000,
    tp_improve=0.8,
    tp_abs_threshold=0.25,
    adverse_move_stop=1.1,
    no_new_entry_after=300000,
    hard_flat_after=520000,
)

V5200_INV = voucher_product(
    "VEV_5200",
    5200,
    max_spread=4,
    entry_threshold=1.70,
    quote_offset=1,
    cross_pad=0.22,
    signal_weight=0.90,
    inventory_skew=2.8,
    passive_size=1,
    aggressive_size=2,
    anchor_alpha=0.02,
    working_limit=16,
    direction_mode="inverse",
    max_hold=10000,
    tp_improve=0.8,
    tp_abs_threshold=0.20,
    adverse_move_stop=1.0,
    no_new_entry_after=300000,
    hard_flat_after=500000,
)


WAVE3 = [
    {
        "bot_id": "W3-01",
        "filename": "candidate_w3_01_delta1_dual_control.py",
        "kind": "delta1",
        "products": [HYDRO_REV, VEX_REV],
        "family": "delta1 champion control",
        "features": ["delta1 base", "dual control"],
        "hypothesis": "The best clean base architecture after the 58-run synthesis is still the compact HYDRO plus VEX delta-1 stack.",
    },
    {
        "bot_id": "W3-02",
        "filename": "candidate_w3_02_delta1_regime_gate.py",
        "kind": "delta1",
        "products": [HYDRO_GATE, VEX_GATE],
        "family": "delta1 simple regime gate",
        "features": ["delta1 base", "simple no-trade gate"],
        "hypothesis": "Delta-1 should improve if it stays out of short bursts of unstable microstructure instead of quoting through every local regime.",
    },
    {
        "bot_id": "W3-03",
        "filename": "candidate_w3_03_vex_itm_active_refresh.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [V4000_ACTIVE, V4500_ACTIVE],
        "family": "vex plus itm active refresh",
        "features": ["vex anchor", "active itm refresh"],
        "hypothesis": "The strongest historical VEX plus ITM family should survive better if ITM is refreshed as a lightly active overlay rather than as passive dead weight.",
    },
    {
        "bot_id": "W3-04",
        "filename": "candidate_w3_04_5300_early_window.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                no_new_entry_after=280000,
                hard_flat_after=620000,
                working_limit=65,
                passive_size=4,
                aggressive_size=6,
            )
        ],
        "family": "5300 early-window rescue",
        "features": ["early no-trade", "late flatten"],
        "hypothesis": "VEV_5300 should work better if it only trades in the early useful window and refuses to reopen risk later in the session.",
    },
    {
        "bot_id": "W3-05",
        "filename": "candidate_w3_05_5300_giveback_halt.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                no_new_entry_after=420000,
                hard_flat_after=700000,
                giveback_activation=0.55,
                giveback_stop=0.70,
                reentry_cooldown=90000,
                working_limit=70,
            )
        ],
        "family": "5300 giveback halt",
        "features": ["giveback stop", "cooldown"],
        "hypothesis": "A large part of the 5300 problem is likely re-giving profits after local progress, so a giveback halt plus cooldown should preserve more path quality.",
    },
    {
        "bot_id": "W3-06",
        "filename": "candidate_w3_06_vex_5300_state_gate.py",
        "kind": "voucher",
        "sidecar_products": [VEX_GATE],
        "products": [
            clone(
                V5300_BASE,
                no_new_entry_after=360000,
                hard_flat_after=700000,
                working_limit=60,
                vex_move_cap=6.0,
                vex_slope_cap=1.5,
                vex_move_ema_cap=2.8,
                vex_kalman_gap_cap=4.5,
            )
        ],
        "family": "vex-linked 5300 regime gate",
        "features": ["vex calm-state gate", "5300 overlay"],
        "hypothesis": "Because vouchers are options linked to VEX, 5300 should only trade when the underlying is in a calm enough state for residual reversion to matter.",
    },
    {
        "bot_id": "W3-07",
        "filename": "candidate_w3_07_5300_slow_hold.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                cross_pad=0.25,
                signal_weight=0.92,
                aggressive_size=6,
                working_limit=65,
                no_new_entry_after=340000,
                hard_flat_after=760000,
                max_hold=60000,
                giveback_activation=1.0,
                giveback_stop=0.95,
            )
        ],
        "family": "5300 slower-horizon hold",
        "features": ["slower hold", "delayed unwind"],
        "hypothesis": "VEV_5300 is not a fast scalp, so it should be judged with a slower hold horizon rather than with fast-unwind assumptions.",
    },
    {
        "bot_id": "W3-08",
        "filename": "candidate_w3_08_delta1_5300_overlay.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_REV, VEX_REV],
        "products": [
            clone(
                V5300_BASE,
                working_limit=35,
                passive_size=2,
                aggressive_size=3,
                no_new_entry_after=320000,
                hard_flat_after=680000,
                vex_move_cap=5.5,
                vex_slope_cap=1.3,
            )
        ],
        "family": "delta1 plus tiny 5300 overlay",
        "features": ["champion base", "gated 5300 overlay"],
        "hypothesis": "The right near-final architecture may be pure delta-1 plus one very small, tightly gated 5300 overlay instead of a larger voucher branch.",
    },
    {
        "bot_id": "W3-09",
        "filename": "candidate_w3_09_5000_5300_capped_salvage.py",
        "kind": "voucher",
        "products": [
            clone(
                V5000_BASE,
                working_limit=18,
                passive_size=1,
                aggressive_size=2,
                no_new_entry_after=260000,
                hard_flat_after=520000,
                giveback_activation=0.40,
                giveback_stop=0.55,
            ),
            clone(
                V5300_BASE,
                working_limit=30,
                passive_size=2,
                aggressive_size=3,
                no_new_entry_after=260000,
                hard_flat_after=520000,
                giveback_activation=0.45,
                giveback_stop=0.60,
            ),
        ],
        "family": "5000 plus 5300 capped peak salvage",
        "features": ["subset salvage", "tight early cap"],
        "hypothesis": "The only remaining fair test for keeping 5000 alive is a tiny early-window salvage design that never lets the subset grow into a late-session problem.",
    },
    {
        "bot_id": "W3-10",
        "filename": "candidate_w3_10_5300_nonlinear_gate.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                working_limit=60,
                vex_move_weight=0.10,
                vex_slope_weight=0.45,
                vex_move_ema_weight=0.08,
                spread_ref=2.0,
                spread_excess_weight=0.35,
                no_new_entry_after=360000,
                hard_flat_after=700000,
            )
        ],
        "family": "5300 transformed-threshold gate",
        "features": ["dynamic threshold", "nonlinear entry filter"],
        "hypothesis": "A transformed threshold that scales with VEX agitation and local spread should keep 5300 out of the states that currently look expensive to fade.",
    },
    {
        "bot_id": "W3-11",
        "filename": "candidate_w3_11_5300_trend_gate.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                working_limit=60,
                buy_vex_slope_min=-0.25,
                sell_vex_slope_max=0.25,
                no_new_entry_after=360000,
                hard_flat_after=700000,
            )
        ],
        "family": "5300 lightweight trend gate",
        "features": ["rolling slope gate", "trend-aware entries"],
        "hypothesis": "5300 should stop fading strong VEX trend states and only take residual trades when the underlying slope is mild enough to allow mean reversion.",
    },
    {
        "bot_id": "W3-12",
        "filename": "candidate_w3_12_5000_inverse_tiny.py",
        "kind": "voucher",
        "products": [V5000_INV],
        "family": "5000 inverse diagnostic",
        "features": ["tiny inverse", "closure-quality evidence"],
        "hypothesis": "Because 5000 is negative at every tested horizon in the standard direction, a tiny inverse diagnostic is now a higher-value test than another normal residual bot.",
    },
    {
        "bot_id": "W3-13",
        "filename": "candidate_w3_13_5100_inverse_tiny.py",
        "kind": "voucher",
        "products": [V5100_INV],
        "family": "5100 inverse diagnostic",
        "features": ["tiny inverse", "closure-quality evidence"],
        "hypothesis": "5100 should now be tested as an anti-signal in tiny size, because even its small standard-direction rescues stayed negative.",
    },
    {
        "bot_id": "W3-14",
        "filename": "candidate_w3_14_5200_inverse_tiny.py",
        "kind": "voucher",
        "products": [V5200_INV],
        "family": "5200 inverse closure test",
        "features": ["tiny inverse", "hard closure test"],
        "hypothesis": "5200 only deserves one last tiny inverse closure test; if that also fails, the strike should be closed with high confidence.",
    },
    {
        "bot_id": "W3-15",
        "filename": "candidate_w3_15_delta1_kalman_control.py",
        "kind": "delta1",
        "products": [HYDRO_KALMAN, VEX_KALMAN],
        "family": "delta1 kalman control",
        "features": ["kalman fair", "dual control"],
        "hypothesis": "A simple Kalman mean may give a cleaner delta-1 reversion reference than raw previous-mid noise, especially in VEX.",
    },
    {
        "bot_id": "W3-16",
        "filename": "candidate_w3_16_5300_kalman_anchor.py",
        "kind": "voucher",
        "sidecar_products": [VEX_KALMAN],
        "products": [
            clone(
                V5300_BASE,
                working_limit=60,
                underlying_anchor_mode="kalman",
                no_new_entry_after=360000,
                hard_flat_after=720000,
                giveback_activation=0.55,
                giveback_stop=0.70,
            )
        ],
        "family": "5300 kalman anchor rescue",
        "features": ["kalman underlying anchor", "5300 rescue"],
        "hypothesis": "If raw VEX mid is too noisy as an option anchor, a Kalman-smoothed VEX reference may make the 5300 residual trade cleaner without changing the family thesis.",
    },
    {
        "bot_id": "W3-17",
        "filename": "candidate_w3_17_5300_imbalance_filter.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                working_limit=60,
                buy_imbalance_min=0.08,
                sell_imbalance_max=-0.08,
                no_new_entry_after=360000,
                hard_flat_after=700000,
            )
        ],
        "family": "5300 imbalance filter",
        "features": ["muravyev-style filter", "selective 5300"],
        "hypothesis": "5300 may keep more of its edge if it only takes residual trades that agree with local order-book pressure instead of fading every extreme equally.",
    },
    {
        "bot_id": "W3-18",
        "filename": "candidate_w3_18_5300_vex_agitation_gate.py",
        "kind": "voucher",
        "products": [
            clone(
                V5300_BASE,
                working_limit=60,
                vex_move_ema_cap=2.4,
                vex_kalman_gap_cap=4.0,
                vex_move_weight=0.05,
                no_new_entry_after=360000,
                hard_flat_after=700000,
            )
        ],
        "family": "5300 vex-agitation gate",
        "features": ["vex agitation gate", "dynamic threshold"],
        "hypothesis": "5300 may only be worth fading when VEX is not already in an agitated state, so VEX move-ema and anchor-gap should be treated as explicit no-trade conditions.",
    },
    {
        "bot_id": "W3-19",
        "filename": "candidate_w3_19_5000_5300_vex_calm_salvage.py",
        "kind": "voucher",
        "sidecar_products": [VEX_GATE],
        "products": [
            clone(
                V5000_BASE,
                working_limit=16,
                passive_size=1,
                aggressive_size=2,
                no_new_entry_after=300000,
                hard_flat_after=540000,
                vex_move_cap=5.0,
                vex_slope_cap=1.2,
            ),
            clone(
                V5300_BASE,
                working_limit=28,
                passive_size=2,
                aggressive_size=3,
                no_new_entry_after=300000,
                hard_flat_after=540000,
                vex_move_cap=5.0,
                vex_slope_cap=1.2,
            ),
        ],
        "family": "vex-calm subset salvage",
        "features": ["subset salvage", "vex calm gate"],
        "hypothesis": "If the old high-peak subset had any real residual edge, the fairest remaining way to see it is inside a tight early window and only when VEX itself is calm enough.",
    },
    {
        "bot_id": "W3-20",
        "filename": "candidate_w3_20_5000_inverse_vex_sidecar.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [clone(V5000_INV, working_limit=20, no_new_entry_after=340000, hard_flat_after=560000)],
        "family": "5000 inverse with vex sidecar",
        "features": ["inverse diagnostic", "vex anchor sidecar"],
        "hypothesis": "If 5000 is better treated as an anti-signal, the most realistic version of that test is a tiny inverse branch attached to the healthier VEX sidecar.",
    },
    {
        "bot_id": "W3-21",
        "filename": "candidate_w3_21_5100_inverse_vex_sidecar.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [clone(V5100_INV, working_limit=20, no_new_entry_after=340000, hard_flat_after=560000)],
        "family": "5100 inverse with vex sidecar",
        "features": ["inverse diagnostic", "vex anchor sidecar"],
        "hypothesis": "If 5100 only works as an anti-signal, pairing that tiny inverse branch with VEX is the cleanest practical test of whether the strike belongs in any final architecture at all.",
    },
    {
        "bot_id": "W3-22",
        "filename": "candidate_w3_22_5200_inverse_vex_sidecar.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [clone(V5200_INV, working_limit=18, no_new_entry_after=340000, hard_flat_after=540000)],
        "family": "5200 inverse with vex sidecar",
        "features": ["inverse closure", "vex anchor sidecar"],
        "hypothesis": "5200 is toxic enough that it deserves one last tiny inverse test with VEX support before we close it decisively or keep a microscopic contrarian role alive.",
    },
    {
        "bot_id": "W3-23",
        "filename": "candidate_w3_23_delta1_itm_active_combo.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_REV, VEX_REV],
        "products": [
            clone(V4000_ACTIVE, working_limit=40, passive_size=2, aggressive_size=3),
            clone(V4500_ACTIVE, working_limit=40, passive_size=2, aggressive_size=3),
        ],
        "family": "delta1 plus itm active combo",
        "features": ["champion base", "active itm refresh"],
        "hypothesis": "A cleaner version of the strongest historical family may be delta-1 first with a smaller, more active ITM overlay rather than passive ITM or voucher-heavy composites.",
    },
    {
        "bot_id": "W3-24",
        "filename": "candidate_w3_24_delta1_itm_5300_stack.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_REV, VEX_REV],
        "products": [
            clone(V4000_ACTIVE, working_limit=30, passive_size=2, aggressive_size=2),
            clone(V4500_ACTIVE, working_limit=30, passive_size=2, aggressive_size=2),
            clone(
                V5300_BASE,
                working_limit=20,
                passive_size=1,
                aggressive_size=2,
                no_new_entry_after=300000,
                hard_flat_after=620000,
                vex_move_cap=5.5,
                vex_slope_cap=1.2,
            ),
        ],
        "family": "delta1 plus itm plus tiny 5300 stack",
        "features": ["champion base", "itm overlay", "micro 5300 overlay"],
        "hypothesis": "The last meaningful exploratory architecture is a near-final stack: delta-1 core, ITM add-on, and only a microscopic tightly gated 5300 overlay.",
    },
]


NEW_SYNC_BLOCK = textwrap.dedent(
    """\
    def sync_position_state(store, symbol, position, centered, timestamp):
        previous = dict(store.get(symbol, {}))
        previous_position = int(previous.get("last_position", 0))
        block_until = previous.get("block_until")
        if position == 0:
            current = {"last_position": 0}
        elif previous_position == 0 or sign(previous_position) != sign(position):
            current = {
                "last_position": int(position),
                "entry_timestamp": int(timestamp),
                "entry_centered": float(centered),
                "best_improvement": 0.0,
            }
        else:
            current = previous
            current["last_position"] = int(position)
            current.setdefault("entry_timestamp", int(timestamp))
            current.setdefault("entry_centered", float(centered))
            current.setdefault("best_improvement", 0.0)
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


    def allow_new_entries(timestamp, cfg, position_state=None):
        regime_start_after = cfg.get("regime_start_after")
        if regime_start_after is not None and int(timestamp) < int(regime_start_after):
            return False
        no_new_entry_after = cfg.get("no_new_entry_after")
        if no_new_entry_after is not None and int(timestamp) >= int(no_new_entry_after):
            return False
        if position_state is not None:
            block_until = position_state.get("block_until")
            if block_until is not None and int(timestamp) < int(block_until):
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
    """
)


NEW_DELTA_BLOCK = textwrap.dedent(
    """\
    def run_delta1_products(state, result, data, products):
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

            if regime_ok and not cfg.get("passive_only", False) and abs(signal) >= trade_threshold:
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
            if regime_ok:
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
        anchors = data.setdefault("voucher_anchor", {})
        position_states = data.setdefault("voucher_position_state", {})
        timestamp = int(getattr(state, "timestamp", 0))

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
            force_exit = (
                should_late_flat(position, timestamp, cfg)
                or should_time_stop(position, timestamp, position_state, cfg)
                or should_stop_out(position, centered, position_state, cfg)
                or should_take_profit(position, centered, position_state, cfg)
                or giveback_exit
            )

            if force_exit:
                if giveback_exit or should_stop_out(position, centered, position_state, cfg):
                    set_reentry_cooldown(position_state, timestamp, cfg)
                exit_orders, position = flatten_position(symbol, order_depth, position, limit)
                orders.extend(exit_orders)
            elif spread <= cfg["max_spread"]:
                entry_threshold = dynamic_entry_threshold(cfg["entry_threshold"], spread, vex_metrics, cfg)
                if direction_mode == "inverse":
                    want_buy = centered > float(entry_threshold)
                    want_sell = centered < -float(entry_threshold)
                else:
                    want_buy = centered < -float(entry_threshold)
                    want_sell = centered > float(entry_threshold)
                want_buy, want_sell = apply_trend_gate(want_buy, want_sell, vex_metrics, cfg)
                if want_buy and not buy_allowed_by_imbalance(imbalance, cfg):
                    want_buy = False
                if want_sell and not sell_allowed_by_imbalance(imbalance, cfg):
                    want_sell = False

                regime_ok = voucher_regime_ok(vex_metrics, spread, cfg, timestamp)
                entries_allowed = regime_ok and allow_new_entries(timestamp, cfg, position_state)

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
        Generated Round 3 Wave 3 learning bot.
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
        "# Learning Batch Wave 3 Manifest",
        "",
        "Generated from `generate_learning_batch_wave3.py`.",
        "",
        f"- Spec: [`../04_strategy_specs/{SPEC_PATH}`](../04_strategy_specs/{SPEC_PATH})",
        "- Owner: `amin`",
        f"- Batch size: `{len(configs)}`",
        "- Intent: `last exploratory / architecture narrowing / regime and inverse closure`",
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
    for config in WAVE3:
        path = BOT_DIR / config["filename"]
        path.write_text(bot_contents(config))
    MANIFEST.write_text(render_manifest(WAVE3))


if __name__ == "__main__":
    main()
