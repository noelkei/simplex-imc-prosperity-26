from __future__ import annotations

import pprint
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
BOT_DIR = ROUND / "bots" / "amin" / "canonical"
MANIFEST = ROUND / "workspace" / "05_implementation" / "learning_batch_wave2_manifest.md"


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
    }
    if working_limit is not None:
        cfg["working_limit"] = working_limit
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
    tp_improve: float | None = None,
    tp_abs_threshold: float | None = None,
    max_hold: int | None = None,
    adverse_move_stop: float | None = None,
    no_new_entry_after: int | None = None,
    hard_flat_after: int | None = None,
    buy_imbalance_min: float | None = None,
    sell_imbalance_max: float | None = None,
    inventory_exit_quotes: bool = True,
    min_price: int = 0,
    max_price: int | None = None,
    passive_step: int = 1,
    sigma_multiplier: float = 1.0,
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
    if tp_improve is not None:
        cfg["tp_improve"] = tp_improve
    if tp_abs_threshold is not None:
        cfg["tp_abs_threshold"] = tp_abs_threshold
    if max_hold is not None:
        cfg["max_hold"] = max_hold
    if adverse_move_stop is not None:
        cfg["adverse_move_stop"] = adverse_move_stop
    if no_new_entry_after is not None:
        cfg["no_new_entry_after"] = no_new_entry_after
    if hard_flat_after is not None:
        cfg["hard_flat_after"] = hard_flat_after
    if buy_imbalance_min is not None:
        cfg["buy_imbalance_min"] = buy_imbalance_min
    if sell_imbalance_max is not None:
        cfg["sell_imbalance_max"] = sell_imbalance_max
    if max_price is not None:
        cfg["max_price"] = max_price
    return cfg


def floor_product(
    symbol: str,
    *,
    limit: int = 300,
    working_limit: int,
    passive_size: int,
    bid_price: int = 0,
    ask_price: int = 1,
    cross_buy_at_or_below: int = 0,
    cross_sell_at_or_above: int = 1,
    allow_short: bool = True,
    passive_when_spread_at_least: int = 1,
) -> dict:
    return {
        "symbol": symbol,
        "limit": limit,
        "working_limit": working_limit,
        "passive_size": passive_size,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "cross_buy_at_or_below": cross_buy_at_or_below,
        "cross_sell_at_or_above": cross_sell_at_or_above,
        "allow_short": allow_short,
        "passive_when_spread_at_least": passive_when_spread_at_least,
    }


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

HYDRO_PASSIVE = delta_product(
    "HYDROGEL_PACK",
    mode="reversion",
    max_spread=24,
    quote_offset=8,
    edge=3,
    reversion_weight=0.32,
    imbalance_weight=0.0,
    inventory_skew=6.0,
    passive_size=8,
    aggressive_size=0,
    passive_only=True,
    trade_threshold=1.25,
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


WAVE2 = [
    {
        "bot_id": "W2-01",
        "filename": "candidate_w2_01_delta1_dual_control.py",
        "kind": "delta1",
        "family": "delta1 champion control",
        "products": [HYDRO_REV, VEX_REV],
        "features": ["delta1 control", "dual branch base"],
        "hypothesis": "The best clean base architecture after Wave 1 is still a compact HYDRO plus VEX delta-1 stack.",
    },
    {
        "bot_id": "W2-02",
        "filename": "candidate_w2_02_hydro_passive_wide.py",
        "kind": "delta1",
        "family": "hydro passive execution carry-forward",
        "products": [HYDRO_PASSIVE],
        "features": ["hydro execution follow-up", "passive wider-spread quoting"],
        "hypothesis": "HYDRO remains live-positive, and a more passive wider-spread posture should tell us whether execution is the remaining bottleneck.",
    },
    {
        "bot_id": "W2-03",
        "filename": "candidate_w2_03_itm_passive_pair.py",
        "kind": "voucher",
        "family": "itm passive carry-forward",
        "products": [
            voucher_product(
                "VEV_4000",
                4000,
                max_spread=24,
                entry_threshold=1.1,
                quote_offset=4,
                cross_pad=0.0,
                signal_weight=0.55,
                inventory_skew=1.2,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.015,
                passive_only=True,
                working_limit=90,
            ),
            voucher_product(
                "VEV_4500",
                4500,
                max_spread=18,
                entry_threshold=1.0,
                quote_offset=3,
                cross_pad=0.0,
                signal_weight=0.55,
                inventory_skew=1.2,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.015,
                passive_only=True,
                working_limit=90,
            ),
        ],
        "features": ["itm passive follow-up", "centered bachelier anchor"],
        "hypothesis": "ITM edge should survive as a low-damage pair when we remove crossing and let residual drift choose the side passively.",
    },
    {
        "bot_id": "W2-04",
        "filename": "candidate_w2_04_delta1_itm_overlay.py",
        "kind": "voucher",
        "sidecar_products": [HYDRO_REV, VEX_REV],
        "products": [
            voucher_product(
                "VEV_4000",
                4000,
                max_spread=24,
                entry_threshold=1.2,
                quote_offset=4,
                cross_pad=0.0,
                signal_weight=0.55,
                inventory_skew=1.0,
                passive_size=3,
                aggressive_size=0,
                anchor_alpha=0.015,
                passive_only=True,
                working_limit=70,
            ),
            voucher_product(
                "VEV_4500",
                4500,
                max_spread=18,
                entry_threshold=1.1,
                quote_offset=3,
                cross_pad=0.0,
                signal_weight=0.55,
                inventory_skew=1.0,
                passive_size=3,
                aggressive_size=0,
                anchor_alpha=0.015,
                passive_only=True,
                working_limit=70,
            ),
        ],
        "family": "delta1 plus itm overlay control",
        "features": ["delta1 base", "itm overlay"],
        "hypothesis": "The highest-quality low-risk composite now is delta-1 first with only a small passive ITM residual overlay.",
    },
    {
        "bot_id": "W2-05",
        "filename": "candidate_w2_05_5300_bachelier_selective.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.4,
                signal_weight=0.90,
                inventory_skew=1.0,
                passive_size=6,
                aggressive_size=10,
                anchor_alpha=0.025,
                working_limit=90,
            )
        ],
        "family": "selective bachelier residual retest",
        "features": ["selective 5300 retest", "clean bachelier fair"],
        "hypothesis": "VEV_5300 still deserves one clean Bachelier-centered retest after the broad basket and intrinsic-only variants were pruned.",
    },
    {
        "bot_id": "W2-06",
        "filename": "candidate_w2_06_5000_5300_bachelier_selective.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5000",
                5000,
                max_spread=8,
                entry_threshold=1.35,
                quote_offset=2,
                cross_pad=0.5,
                signal_weight=0.85,
                inventory_skew=1.0,
                passive_size=4,
                aggressive_size=6,
                anchor_alpha=0.02,
                working_limit=70,
            ),
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.4,
                signal_weight=0.90,
                inventory_skew=1.0,
                passive_size=5,
                aggressive_size=8,
                anchor_alpha=0.025,
                working_limit=90,
            ),
        ],
        "family": "selective bachelier residual subset retest",
        "features": ["5000 plus 5300 subset", "clean bachelier fair"],
        "hypothesis": "The surviving active subset should be judged fairly as 5000 plus 5300 under a centered Bachelier residual before we abandon the branch.",
    },
    {
        "bot_id": "W2-07",
        "filename": "candidate_w2_07_5300_fast_unwind.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.85,
                inventory_skew=1.2,
                passive_size=4,
                aggressive_size=8,
                anchor_alpha=0.025,
                working_limit=75,
                tp_improve=0.9,
                tp_abs_threshold=0.25,
                max_hold=15000,
                adverse_move_stop=1.8,
            )
        ],
        "family": "active path rescue",
        "features": ["5300 fast take-profit", "time-stop"],
        "hypothesis": "VEV_5300 path quality should improve if we treat it as a fast-capture trade instead of a hold-for-full-reversion trade.",
    },
    {
        "bot_id": "W2-08",
        "filename": "candidate_w2_08_5000_5300_fast_unwind.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5000",
                5000,
                max_spread=8,
                entry_threshold=1.45,
                quote_offset=2,
                cross_pad=0.45,
                signal_weight=0.82,
                inventory_skew=1.2,
                passive_size=3,
                aggressive_size=5,
                anchor_alpha=0.02,
                working_limit=55,
                tp_improve=1.1,
                tp_abs_threshold=0.35,
                max_hold=18000,
                adverse_move_stop=2.1,
            ),
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.85,
                inventory_skew=1.2,
                passive_size=4,
                aggressive_size=7,
                anchor_alpha=0.025,
                working_limit=70,
                tp_improve=0.9,
                tp_abs_threshold=0.25,
                max_hold=15000,
                adverse_move_stop=1.8,
            ),
        ],
        "family": "active subset path rescue",
        "features": ["5000 plus 5300 fast unwind", "time-stop"],
        "hypothesis": "The best active subset should look materially better if we monetize the early edge and refuse to let the run drift into late reversals.",
    },
    {
        "bot_id": "W2-09",
        "filename": "candidate_w2_09_5300_late_flatten.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.4,
                signal_weight=0.88,
                inventory_skew=1.0,
                passive_size=5,
                aggressive_size=8,
                anchor_alpha=0.025,
                working_limit=80,
                no_new_entry_after=720000,
                hard_flat_after=860000,
            )
        ],
        "family": "expiry-aware late flatten",
        "features": ["5300 no-new-entry gate", "late flatten"],
        "hypothesis": "The main 5300 problem may be session-tail toxicity rather than entry quality, so shutting the branch down late should preserve more of the path peak.",
    },
    {
        "bot_id": "W2-10",
        "filename": "candidate_w2_10_5000_5300_late_flatten.py",
        "kind": "voucher",
        "products": [
            voucher_product(
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
                working_limit=55,
                no_new_entry_after=720000,
                hard_flat_after=860000,
            ),
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.4,
                signal_weight=0.88,
                inventory_skew=1.0,
                passive_size=4,
                aggressive_size=7,
                anchor_alpha=0.025,
                working_limit=75,
                no_new_entry_after=720000,
                hard_flat_after=860000,
            ),
        ],
        "family": "expiry-aware subset late flatten",
        "features": ["5000 plus 5300 no-new-entry gate", "late flatten"],
        "hypothesis": "If the selective active subset mostly loses in the session tail, a no-new-entry cutoff plus hard flatten should retain more realized edge than the clean retest variant.",
    },
    {
        "bot_id": "W2-11",
        "filename": "candidate_w2_11_5000_5300_inventory_rescue.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5000",
                5000,
                max_spread=8,
                entry_threshold=1.45,
                quote_offset=2,
                cross_pad=0.45,
                signal_weight=0.82,
                inventory_skew=2.8,
                passive_size=3,
                aggressive_size=5,
                anchor_alpha=0.02,
                working_limit=45,
                tp_improve=1.0,
                tp_abs_threshold=0.35,
                max_hold=16000,
                adverse_move_stop=2.0,
                no_new_entry_after=760000,
                hard_flat_after=875000,
            ),
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.85,
                inventory_skew=2.6,
                passive_size=4,
                aggressive_size=7,
                anchor_alpha=0.025,
                working_limit=60,
                tp_improve=0.9,
                tp_abs_threshold=0.25,
                max_hold=15000,
                adverse_move_stop=1.8,
                no_new_entry_after=760000,
                hard_flat_after=875000,
            ),
        ],
        "family": "inventory-aware subset rescue",
        "features": ["subset inventory overlay", "fast unwind", "late flatten"],
        "hypothesis": "Inventory control only has a fair chance once the branch is pruned to 5000 plus 5300 and paired with faster exits.",
    },
    {
        "bot_id": "W2-12",
        "filename": "candidate_w2_12_vex_5300_fast_combo.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.85,
                inventory_skew=1.2,
                passive_size=4,
                aggressive_size=7,
                anchor_alpha=0.025,
                working_limit=65,
                tp_improve=0.9,
                tp_abs_threshold=0.25,
                max_hold=15000,
                adverse_move_stop=1.8,
            )
        ],
        "family": "vex plus selective active combo",
        "features": ["vex anchor leg", "5300 fast unwind"],
        "hypothesis": "The descriptive VEX plus 5300 winner from Wave 1 should become more robust if the voucher leg is explicitly run as a fast-unwind addon instead of a hold leg.",
    },
    {
        "bot_id": "W2-13",
        "filename": "candidate_w2_13_selective_imbalance_filter.py",
        "kind": "voucher",
        "products": [
            voucher_product(
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
                tp_improve=1.0,
                tp_abs_threshold=0.35,
                max_hold=17000,
                adverse_move_stop=2.0,
                buy_imbalance_min=0.05,
                sell_imbalance_max=-0.05,
            ),
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.85,
                inventory_skew=1.0,
                passive_size=4,
                aggressive_size=7,
                anchor_alpha=0.025,
                working_limit=65,
                tp_improve=0.9,
                tp_abs_threshold=0.25,
                max_hold=15000,
                adverse_move_stop=1.8,
                buy_imbalance_min=0.08,
                sell_imbalance_max=-0.08,
            ),
        ],
        "family": "selective imbalance-as-filter",
        "features": ["muravyev-style confirmation", "selective active subset"],
        "hypothesis": "The selective active subset should keep more of its path edge if we only take residual trades that are confirmed by local order-book pressure.",
    },
    {
        "bot_id": "W2-14",
        "filename": "candidate_w2_14_upper_anchored_passive.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5400",
                5400,
                max_spread=2,
                entry_threshold=0.7,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.20,
                inventory_skew=0.8,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=35,
            ),
            voucher_product(
                "VEV_5500",
                5500,
                max_spread=2,
                entry_threshold=0.45,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.15,
                inventory_skew=0.8,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=35,
            ),
        ],
        "family": "upper anchored passive refinement",
        "features": ["upper passive maker", "bachelier anchor"],
        "hypothesis": "The upper branch still deserves one clean passive anchored refinement before we decide whether it is a permanent pause or just an execution problem.",
    },
    {
        "bot_id": "W2-15",
        "filename": "candidate_w2_15_5100_tiny_rescue.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [
            voucher_product(
                "VEV_5100",
                5100,
                max_spread=6,
                entry_threshold=1.55,
                quote_offset=2,
                cross_pad=0.2,
                signal_weight=0.88,
                inventory_skew=3.0,
                passive_size=1,
                aggressive_size=2,
                anchor_alpha=0.02,
                working_limit=18,
                tp_improve=0.9,
                tp_abs_threshold=0.20,
                max_hold=8000,
                adverse_move_stop=1.2,
                no_new_entry_after=700000,
                hard_flat_after=820000,
            )
        ],
        "family": "toxic-strike controlled rescue",
        "features": ["5100 micro-risk", "fast unwind", "vex sidecar"],
        "hypothesis": "VEV_5100 only deserves one last chance as a tiny fast-unwind scalp attached to a healthier VEX anchor, not as a normal active strike.",
    },
    {
        "bot_id": "W2-16",
        "filename": "candidate_w2_16_5200_tiny_rescue.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [
            voucher_product(
                "VEV_5200",
                5200,
                max_spread=4,
                entry_threshold=1.80,
                quote_offset=1,
                cross_pad=0.2,
                signal_weight=0.92,
                inventory_skew=3.2,
                passive_size=1,
                aggressive_size=2,
                anchor_alpha=0.02,
                working_limit=16,
                tp_improve=1.0,
                tp_abs_threshold=0.20,
                max_hold=7000,
                adverse_move_stop=1.3,
                no_new_entry_after=700000,
                hard_flat_after=820000,
            )
        ],
        "family": "toxic-strike controlled rescue",
        "features": ["5200 micro-risk", "fast unwind", "vex sidecar"],
        "hypothesis": "VEV_5200 only deserves one last coverage run as a tiny anchored scalp with harsh exits, not as a normal promotion candidate.",
    },
    {
        "bot_id": "W2-17",
        "filename": "candidate_w2_17_5300_5400_5500_bridge.py",
        "kind": "voucher",
        "products": [
            voucher_product(
                "VEV_5300",
                5300,
                max_spread=3,
                entry_threshold=1.0,
                quote_offset=1,
                cross_pad=0.35,
                signal_weight=0.82,
                inventory_skew=1.2,
                passive_size=3,
                aggressive_size=6,
                anchor_alpha=0.025,
                working_limit=55,
                tp_improve=0.8,
                tp_abs_threshold=0.25,
                max_hold=14000,
                adverse_move_stop=1.7,
            ),
            voucher_product(
                "VEV_5400",
                5400,
                max_spread=2,
                entry_threshold=0.7,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.20,
                inventory_skew=0.8,
                passive_size=3,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=30,
            ),
            voucher_product(
                "VEV_5500",
                5500,
                max_spread=2,
                entry_threshold=0.45,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.15,
                inventory_skew=0.8,
                passive_size=3,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=30,
            ),
        ],
        "family": "active-upper bridge",
        "features": ["5300 path rescue", "upper passive coverage"],
        "hypothesis": "The active-to-upper transition may only monetize when 5300 carries the branch and the upper names are treated as passive anchored satellites.",
    },
    {
        "bot_id": "W2-18",
        "filename": "candidate_w2_18_vex_upper_anchored_combo.py",
        "kind": "voucher",
        "sidecar_products": [VEX_REV],
        "products": [
            voucher_product(
                "VEV_5400",
                5400,
                max_spread=2,
                entry_threshold=0.7,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.20,
                inventory_skew=0.8,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=35,
            ),
            voucher_product(
                "VEV_5500",
                5500,
                max_spread=2,
                entry_threshold=0.45,
                quote_offset=1,
                cross_pad=0.0,
                signal_weight=0.15,
                inventory_skew=0.8,
                passive_size=4,
                aggressive_size=0,
                anchor_alpha=0.02,
                passive_only=True,
                neutral_two_sided=True,
                working_limit=35,
            ),
        ],
        "family": "vex plus upper anchored combo",
        "features": ["vex sidecar", "upper passive refinement"],
        "hypothesis": "If the upper branch needs both an anchor leg and passive execution, a VEX plus upper combo should be its cleanest last test.",
    },
    {
        "bot_id": "W2-19",
        "filename": "candidate_w2_19_floor_micro_probe.py",
        "kind": "floor",
        "products": [
            floor_product("VEV_6000", working_limit=4, passive_size=1),
            floor_product("VEV_6500", working_limit=4, passive_size=1),
        ],
        "family": "floor micro probe",
        "features": ["0/1 passive quoting", "tiny floor-break scavenging"],
        "hypothesis": "The floor names are probably not directional alpha, but tiny 0/1 passive and floor-break probing is still the cleanest way to confirm whether any monetizable microstructure remains.",
    },
]


TEMPLATE = textwrap.dedent(
    """\
    \"\"\"
    Generated Round 3 Wave 2 learning bot.
    Batch spec: spec_learning_batch_wave2.md
    Bot ID: __BOT_ID__
    Family: __FAMILY__
    Hypothesis: __HYPOTHESIS__
    \"\"\"

    import json
    import math
    from datamodel import Order, TradingState


    CONFIG = __CONFIG__

    SQRT_2 = math.sqrt(2.0)
    SQRT_2PI = math.sqrt(2.0 * math.pi)
    DEFAULT_SIGMA = 90.0
    DEFAULT_SIGMA_FLOOR = 45.0
    DEFAULT_SIGMA_CAP = 180.0
    DEFAULT_SIGMA_ALPHA = 0.08
    DEFAULT_SIGMA_MOVE_SCALE = 14.0
    DEFAULT_TTE_DAYS = 5.0


    def get_best_bid(order_depth):
        if not order_depth or not order_depth.buy_orders:
            return None
        return max(order_depth.buy_orders)


    def get_best_ask(order_depth):
        if not order_depth or not order_depth.sell_orders:
            return None
        return min(order_depth.sell_orders)


    def get_mid(order_depth):
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        if best_bid is None or best_ask is None:
            return None
        return (best_bid + best_ask) / 2.0


    def get_spread(order_depth):
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        if best_bid is None or best_ask is None:
            return None
        return best_ask - best_bid


    def get_imbalance(order_depth):
        best_bid = get_best_bid(order_depth)
        best_ask = get_best_ask(order_depth)
        if best_bid is None or best_ask is None:
            return 0.0
        bid_vol = int(order_depth.buy_orders[best_bid])
        ask_vol = abs(int(order_depth.sell_orders[best_ask]))
        total = bid_vol + ask_vol
        if total <= 0:
            return 0.0
        return (bid_vol - ask_vol) / float(total)


    def sign(value):
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0


    def clamp_qty(qty, position, limit):
        if qty > 0:
            return max(0, min(int(qty), int(limit - position)))
        if qty < 0:
            return min(0, max(int(qty), int(-(limit + position))))
        return 0


    def clamp_price(price, min_price=0, max_price=None):
        value = int(round(price))
        value = max(int(min_price), value)
        if max_price is not None:
            value = min(value, int(max_price))
        return value


    def intrinsic_call(underlying_mid, strike):
        return max(float(underlying_mid) - float(strike), 0.0)


    def norm_cdf(x):
        return 0.5 * (1.0 + math.erf(float(x) / SQRT_2))


    def norm_pdf(x):
        return math.exp(-0.5 * float(x) * float(x)) / SQRT_2PI


    def bachelier_call(underlying_mid, strike, tte_days, sigma_abs):
        if sigma_abs <= 0 or tte_days <= 0:
            return intrinsic_call(underlying_mid, strike)
        tte_years = float(tte_days) / 365.0
        vol_t = float(sigma_abs) * math.sqrt(max(tte_years, 1e-9))
        if vol_t <= 1e-9:
            return intrinsic_call(underlying_mid, strike)
        d = (float(underlying_mid) - float(strike)) / vol_t
        return max(0.0, (float(underlying_mid) - float(strike)) * norm_cdf(d) + vol_t * norm_pdf(d))


    def load_data(raw):
        if not raw:
            return {}
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                return data
        except Exception:
            return {}
        return {}


    def save_data(data):
        return json.dumps(data, separators=(",", ":"), sort_keys=True)


    def append_orders(result, symbol, orders):
        if not orders:
            return
        bucket = result.setdefault(symbol, [])
        bucket.extend(orders)


    def take_from_asks(symbol, order_depth, position, limit, max_qty, max_price):
        orders = []
        remaining = max(0, int(max_qty))
        if remaining <= 0:
            return orders, position
        for ask in sorted(order_depth.sell_orders):
            if ask > max_price or remaining <= 0:
                break
            ask_vol = max(0, -int(order_depth.sell_orders[ask]))
            qty = clamp_qty(min(ask_vol, remaining), position, limit)
            if qty > 0:
                orders.append(Order(symbol, int(ask), int(qty)))
                position += qty
                remaining -= qty
        return orders, position


    def hit_bids(symbol, order_depth, position, limit, max_qty, min_price):
        orders = []
        remaining = max(0, int(max_qty))
        if remaining <= 0:
            return orders, position
        for bid in sorted(order_depth.buy_orders, reverse=True):
            if bid < min_price or remaining <= 0:
                break
            bid_vol = max(0, int(order_depth.buy_orders[bid]))
            qty = clamp_qty(-min(bid_vol, remaining), position, limit)
            if qty < 0:
                orders.append(Order(symbol, int(bid), int(qty)))
                position += qty
                remaining -= abs(qty)
        return orders, position


    def flatten_position(symbol, order_depth, position, limit):
        if position > 0:
            return hit_bids(symbol, order_depth, position, limit, abs(position), -10**9)
        if position < 0:
            return take_from_asks(symbol, order_depth, position, limit, abs(position), 10**9)
        return [], position


    def passive_bid_price(fair, cfg, best_bid, best_ask):
        price = int(round(fair - cfg.get("quote_offset", 1)))
        step = int(cfg.get("passive_step", 1))
        if best_bid is not None:
            price = min(price, int(best_bid) + step)
            price = max(price, int(best_bid))
        if best_ask is not None:
            price = min(price, int(best_ask) - 1)
        return clamp_price(price, cfg.get("min_price", 0), cfg.get("max_price"))


    def passive_ask_price(fair, cfg, best_bid, best_ask):
        price = int(round(fair + cfg.get("quote_offset", 1)))
        step = int(cfg.get("passive_step", 1))
        if best_ask is not None:
            price = max(price, int(best_ask) - step)
            price = min(price, int(best_ask))
        if best_bid is not None:
            price = max(price, int(best_bid) + 1)
        return clamp_price(price, cfg.get("min_price", 0), cfg.get("max_price"))


    def sync_position_state(store, symbol, position, centered, timestamp):
        previous = store.get(symbol, {})
        previous_position = int(previous.get("last_position", 0))
        current = dict(previous)
        if position == 0:
            current = {"last_position": 0}
        elif previous_position == 0 or sign(previous_position) != sign(position):
            current = {
                "last_position": int(position),
                "entry_timestamp": int(timestamp),
                "entry_centered": float(centered),
            }
        else:
            current["last_position"] = int(position)
            current.setdefault("entry_timestamp", int(timestamp))
            current.setdefault("entry_centered", float(centered))
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


    def allow_new_entries(timestamp, cfg):
        no_new_entry_after = cfg.get("no_new_entry_after")
        if no_new_entry_after is None:
            return True
        return int(timestamp) < int(no_new_entry_after)


    def buy_allowed_by_imbalance(imbalance, cfg):
        minimum = cfg.get("buy_imbalance_min")
        return minimum is None or imbalance >= float(minimum)


    def sell_allowed_by_imbalance(imbalance, cfg):
        maximum = cfg.get("sell_imbalance_max")
        return maximum is None or imbalance <= float(maximum)


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


    def effective_limit(cfg):
        return int(cfg.get("working_limit", cfg["limit"]))


    def run_delta1_products(state, result, data, products):
        last_mid = data.setdefault("delta_last_mid", {})
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
            if spread > cfg["max_spread"]:
                last_mid[symbol] = mid
                continue

            position = int(state.position.get(symbol, 0))
            limit = effective_limit(cfg)
            prev_mid = last_mid.get(symbol)
            imbalance = get_imbalance(order_depth)
            signal = 0.0
            if cfg["mode"] in ("reversion", "hybrid") and prev_mid is not None:
                signal += float(cfg["reversion_weight"]) * (float(prev_mid) - float(mid))
            if cfg["mode"] in ("imbalance", "hybrid"):
                signal += float(cfg["imbalance_weight"]) * imbalance

            fair = float(mid) + signal - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
            trade_threshold = float(cfg.get("trade_threshold", 0.0))
            orders = []

            if not cfg.get("passive_only", False) and abs(signal) >= trade_threshold:
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
            quote_buy = True
            quote_sell = True
            if abs(signal) >= trade_threshold:
                if signal > 0:
                    quote_sell = False
                elif signal < 0:
                    quote_buy = False

            if quote_buy and buy_qty > 0:
                price = passive_bid_price(fair, cfg, best_bid, best_ask)
                orders.append(Order(symbol, int(price), int(buy_qty)))
            if quote_sell and sell_qty < 0:
                price = passive_ask_price(fair, cfg, best_bid, best_ask)
                orders.append(Order(symbol, int(price), int(sell_qty)))

            append_orders(result, symbol, orders)
            last_mid[symbol] = mid


    def run_voucher_products(state, result, data, config):
        sidecars = config.get("sidecar_products", [])
        if sidecars:
            run_delta1_products(state, result, data, sidecars)

        vex_depth = state.order_depths.get("VELVETFRUIT_EXTRACT")
        vex_mid = get_mid(vex_depth) if vex_depth is not None else None
        if vex_mid is None:
            return

        sigma_abs = update_sigma(data, vex_mid, config)
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
            sigma_multiplier = float(cfg.get("sigma_multiplier", 1.0))
            fair_model = bachelier_call(
                vex_mid,
                cfg["strike"],
                config.get("tte_days", DEFAULT_TTE_DAYS),
                sigma_abs * sigma_multiplier,
            )
            raw_residual = float(mid) - float(fair_model)
            anchor = float(anchors.get(symbol, raw_residual))
            centered = raw_residual - anchor
            fair = (
                float(fair_model)
                + anchor
                - float(cfg["signal_weight"]) * centered
                - float(cfg["inventory_skew"]) * (position / float(max(1, limit)))
            )
            position_state = sync_position_state(position_states, symbol, position, centered, timestamp)
            orders = []
            force_exit = (
                should_late_flat(position, timestamp, cfg)
                or should_time_stop(position, timestamp, position_state, cfg)
                or should_stop_out(position, centered, position_state, cfg)
                or should_take_profit(position, centered, position_state, cfg)
            )

            if force_exit:
                exit_orders, position = flatten_position(symbol, order_depth, position, limit)
                orders.extend(exit_orders)
            elif spread <= cfg["max_spread"]:
                want_buy = centered < -float(cfg["entry_threshold"])
                want_sell = centered > float(cfg["entry_threshold"])
                if want_buy and not buy_allowed_by_imbalance(imbalance, cfg):
                    want_buy = False
                if want_sell and not sell_allowed_by_imbalance(imbalance, cfg):
                    want_sell = False

                if allow_new_entries(timestamp, cfg) and not cfg.get("passive_only", False):
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

                if allow_new_entries(timestamp, cfg):
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


    def run_floor_products(state, result, data, products):
        del data
        for cfg in products:
            symbol = cfg["symbol"]
            order_depth = state.order_depths.get(symbol)
            if order_depth is None:
                continue
            best_bid = get_best_bid(order_depth)
            best_ask = get_best_ask(order_depth)
            spread = None
            if best_bid is not None and best_ask is not None:
                spread = best_ask - best_bid

            position = int(state.position.get(symbol, 0))
            limit = effective_limit(cfg)
            orders = []

            if best_ask is not None and best_ask <= int(cfg["cross_buy_at_or_below"]):
                active_orders, position = take_from_asks(symbol, order_depth, position, limit, cfg["passive_size"], best_ask)
                orders.extend(active_orders)
            if best_bid is not None and best_bid >= int(cfg["cross_sell_at_or_above"]):
                if cfg.get("allow_short", False) or position > 0:
                    active_orders, position = hit_bids(symbol, order_depth, position, limit, cfg["passive_size"], best_bid)
                    orders.extend(active_orders)

            if spread is not None and spread >= int(cfg.get("passive_when_spread_at_least", 1)):
                buy_qty = clamp_qty(cfg["passive_size"], position, limit)
                sell_qty = clamp_qty(-cfg["passive_size"], position, limit)
                if buy_qty > 0:
                    orders.append(Order(symbol, int(cfg["bid_price"]), int(buy_qty)))
                if sell_qty < 0 and (cfg.get("allow_short", False) or position > 0):
                    orders.append(Order(symbol, int(cfg["ask_price"]), int(sell_qty)))

            append_orders(result, symbol, orders)


    class Trader:
        def run(self, state: TradingState):
            result = {}
            conversions = 0
            data = load_data(state.traderData)
            kind = CONFIG["kind"]
            if kind == "delta1":
                run_delta1_products(state, result, data, CONFIG["products"])
            elif kind == "voucher":
                run_voucher_products(state, result, data, CONFIG)
            elif kind == "floor":
                run_floor_products(state, result, data, CONFIG["products"])
            return result, conversions, save_data(data)
    """
)


def render_config(config: dict) -> str:
    return pprint.pformat(config, sort_dicts=True, width=100)


def bot_contents(config: dict) -> str:
    return (
        TEMPLATE.replace("__BOT_ID__", config["bot_id"])
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
        "# Learning Batch Wave 2 Manifest",
        "",
        "Generated from `generate_learning_batch_wave2.py`.",
        "",
        "- Spec: [`../04_strategy_specs/spec_learning_batch_wave2.md`](../04_strategy_specs/spec_learning_batch_wave2.md)",
        "- Owner: `amin`",
        "- Batch size: `19`",
        "- Intent: `learning / architecture selection / controlled whole-universe coverage`",
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
    for config in WAVE2:
        path = BOT_DIR / config["filename"]
        path.write_text(bot_contents(config))
    MANIFEST.write_text(render_manifest(WAVE2))


if __name__ == "__main__":
    main()
