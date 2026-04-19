from __future__ import annotations

import ast
import io
import json
import math
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_2"
WORKSPACE = ROUND / "workspace"
PERF_HIST = ROUND / "performances" / "noel" / "historical"
PERF_CANON = ROUND / "performances" / "noel" / "canonical"
BOT_CANON = ROUND / "bots" / "noel" / "canonical"
ARTIFACTS = WORKSPACE / "06_testing" / "artifacts"
REPORT = WORKSPACE / "06_testing" / "round2_battery_01_analysis.md"
MEMORY = WORKSPACE / "post_run_research_memory.md"

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
RUN_DATE = "2026-04-19"


@dataclass(frozen=True)
class CandidateMeta:
    candidate_id: str
    short_id: str
    strategy_family: str
    tested_signal: str
    role: str
    spec: str
    bot_file: str


META: dict[str, CandidateMeta] = {
    "01": CandidateMeta("R2-CAND-01", "C01", "ipr_drift", "IPR drift/residual", "primary diagnostic", "spec_r2_cand_01_ipr_drift_fv_maker.md", "candidate_r2_cand_01_ipr_drift_fv_maker.py"),
    "02": CandidateMeta("R2-CAND-02", "C02", "ipr_extreme", "IPR residual extreme", "secondary diagnostic", "spec_r2_cand_02_ipr_residual_extreme_execution.md", "candidate_r2_cand_02_ipr_residual_extreme_execution.py"),
    "03": CandidateMeta("R2-CAND-03", "C03", "aco_reversal", "ACO short-horizon reversal", "primary diagnostic", "spec_r2_cand_03_aco_reversal_maker.md", "candidate_r2_cand_03_aco_reversal_maker.py"),
    "04": CandidateMeta("R2-CAND-04", "C04", "aco_imbalance", "ACO top imbalance", "primary diagnostic", "spec_r2_cand_04_aco_top_imbalance_skew.md", "candidate_r2_cand_04_aco_top_imbalance_skew.py"),
    "05": CandidateMeta("R2-CAND-05", "C05", "aco_microprice", "ACO microprice", "exploratory diagnostic", "spec_r2_cand_05_aco_microprice_challenger.md", "candidate_r2_cand_05_aco_microprice_challenger.py"),
    "06": CandidateMeta("R2-CAND-06", "C06", "aco_full_book", "ACO full-book/depth", "exploratory diagnostic", "spec_r2_cand_06_aco_full_book_depth_backup.md", "candidate_r2_cand_06_aco_full_book_depth_backup.py"),
    "07": CandidateMeta("R2-CAND-07", "C07", "combined_ipr_aco_imbalance", "IPR drift + ACO imbalance", "primary final-path", "spec_r2_cand_07_combined_ipr_aco_imbalance.md", "candidate_r2_cand_07_combined_ipr_aco_imbalance.py"),
    "08": CandidateMeta("R2-CAND-08", "C08", "combined_ipr_aco_reversal", "IPR drift + ACO reversal", "secondary final-path", "spec_r2_cand_08_combined_ipr_aco_reversal.md", "candidate_r2_cand_08_combined_ipr_aco_reversal.py"),
    "09": CandidateMeta("R2-CAND-09", "C09", "spread_defensive_overlay", "IPR drift + ACO imbalance + spread overlay", "secondary overlay", "spec_r2_cand_09_spread_defensive_overlay.md", "candidate_r2_cand_09_spread_defensive_overlay.py"),
    "10": CandidateMeta("R2-CAND-10", "C10", "maf_policy_probe", "IPR drift + ACO imbalance + bid placeholder", "mechanics probe", "spec_r2_cand_10_maf_bid_policy.md", "candidate_r2_cand_10_maf_bid_policy.py"),
}


def read_platform_json(path: Path) -> tuple[dict[str, Any], pd.DataFrame, pd.DataFrame]:
    data = json.loads(path.read_text())
    activities = pd.read_csv(io.StringIO(data["activitiesLog"]), sep=";")
    graph = pd.read_csv(io.StringIO(data["graphLog"]), sep=";")
    return data, activities, graph


def parse_candidate_key(path: Path) -> tuple[str, str]:
    match = re.search(r"candidate_r2_cand_(\d\d)_", path.name)
    if not match:
        raise ValueError(f"Cannot parse candidate id from {path}")
    cand = match.group(1)
    variant = "trial_2" if "_v2" in path.stem else "trial_1"
    return cand, variant


def bot_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "CONFIG" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


def config_signature(config: dict[str, Any]) -> str:
    normalized = {k: v for k, v in config.items() if k not in {"bot_id", "role", "log"}}
    return json.dumps(normalized, sort_keys=True)


def drawdown(series: pd.Series) -> float:
    if series.empty:
        return math.nan
    return float((series - series.cummax()).min())


def final_product_pnl(activities: pd.DataFrame) -> dict[str, float]:
    rows = activities.sort_values("timestamp").groupby("product", as_index=False).tail(1)
    return {str(row["product"]): float(row["profit_and_loss"]) for _, row in rows.iterrows()}


def product_change_counts(activities: pd.DataFrame) -> dict[str, int]:
    counts: dict[str, int] = {}
    for product, frame in activities.sort_values("timestamp").groupby("product"):
        diffs = frame["profit_and_loss"].diff().fillna(frame["profit_and_loss"])
        counts[str(product)] = int((diffs.abs() > 1e-9).sum())
    return counts


def spread_diagnostics(path: Path, activities: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    df = activities.copy()
    df["spread"] = df["ask_price_1"] - df["bid_price_1"]
    for product, frame in df.groupby("product"):
        spreads = frame["spread"].dropna()
        rows.append(
            {
                "run_file": path.name,
                "product": product,
                "rows": int(len(frame)),
                "two_sided_rows": int(spreads.count()),
                "spread_min": float(spreads.min()) if not spreads.empty else np.nan,
                "spread_median": float(spreads.median()) if not spreads.empty else np.nan,
                "spread_mean": float(spreads.mean()) if not spreads.empty else np.nan,
                "spread_max": float(spreads.max()) if not spreads.empty else np.nan,
                "pct_spread_le_4": float((spreads <= 4).mean()) if not spreads.empty else np.nan,
                "pct_spread_le_6": float((spreads <= 6).mean()) if not spreads.empty else np.nan,
                "pct_spread_le_10": float((spreads <= 10).mean()) if not spreads.empty else np.nan,
                "pct_spread_le_16": float((spreads <= 16).mean()) if not spreads.empty else np.nan,
                "pct_spread_le_18": float((spreads <= 18).mean()) if not spreads.empty else np.nan,
                "pct_spread_le_21": float((spreads <= 21).mean()) if not spreads.empty else np.nan,
            }
        )
    return rows


def safe_pos(data: dict[str, Any], product: str) -> int:
    positions = {str(p["symbol"]): int(p["quantity"]) for p in data.get("positions", [])}
    return positions.get(product, 0)


def collect_metrics() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, pd.DataFrame]]:
    PERF_CANON.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    run_rows: list[dict[str, Any]] = []
    product_rows: list[dict[str, Any]] = []
    spread_rows: list[dict[str, Any]] = []
    graph_frames: dict[str, pd.DataFrame] = {}

    for json_path in sorted(PERF_HIST.glob("candidate_r2_cand_*.json")):
        cand, variant = parse_candidate_key(json_path)
        meta = META[cand]
        bot_path = BOT_CANON / meta.bot_file
        config = bot_config(bot_path)
        data, activities, graph = read_platform_json(json_path)
        final_pnl = final_product_pnl(activities)
        pnl_changes = product_change_counts(activities)
        graph["run"] = f"{meta.short_id}-{variant}"
        graph_frames[f"{meta.short_id}-{variant}"] = graph

        graph_final = float(graph["value"].iloc[-1]) if not graph.empty else np.nan
        graph_max = float(graph["value"].max()) if not graph.empty else np.nan
        graph_min = float(graph["value"].min()) if not graph.empty else np.nan
        dd = drawdown(graph["value"]) if not graph.empty else np.nan

        pnl = float(data.get("profit", np.nan))
        run_id = f"run_{RUN_DATE.replace('-', '')}_battery01_{meta.short_id.lower()}_{variant}"
        config_sig = config_signature(config) if config else ""
        run_rows.append(
            {
                "run_id": run_id,
                "candidate": meta.candidate_id,
                "short_id": meta.short_id,
                "variant": variant,
                "run_file": json_path.name,
                "status": data.get("status"),
                "profit": pnl,
                "graph_final": graph_final,
                "graph_max": graph_max,
                "graph_min": graph_min,
                "max_drawdown": dd,
                "final_ipr_pnl": final_pnl.get(IPR, 0.0),
                "final_aco_pnl": final_pnl.get(ACO, 0.0),
                "final_ipr_position": safe_pos(data, IPR),
                "final_aco_position": safe_pos(data, ACO),
                "xirecs_position": safe_pos(data, "XIRECS"),
                "ipr_pnl_change_ticks": pnl_changes.get(IPR, 0),
                "aco_pnl_change_ticks": pnl_changes.get(ACO, 0),
                "strategy_family": meta.strategy_family,
                "tested_signal": meta.tested_signal,
                "role": meta.role,
                "spec": meta.spec,
                "bot_path": str(bot_path.relative_to(ROOT)),
                "raw_json_path": str(json_path.relative_to(ROOT)),
                "bot_file_exists": bot_path.exists(),
                "config_signature": config_sig,
                "modes": ",".join(config.get("modes", [])) if config else "",
                "maf_bid": int(config.get("maf_bid", 0)) if config else 0,
            }
        )

        for product in [IPR, ACO]:
            product_rows.append(
                {
                    "run_id": run_id,
                    "candidate": meta.candidate_id,
                    "short_id": meta.short_id,
                    "variant": variant,
                    "product": product,
                    "final_pnl": final_pnl.get(product, 0.0),
                    "final_position": safe_pos(data, product),
                    "pnl_change_ticks": pnl_changes.get(product, 0),
                }
            )
        spread_rows.extend(spread_diagnostics(json_path, activities))

    runs = pd.DataFrame(run_rows).sort_values("profit", ascending=False)
    products = pd.DataFrame(product_rows)
    spreads = pd.DataFrame(spread_rows)
    return runs, products, spreads, graph_frames


def classify_run(row: pd.Series, champion_profit: float) -> tuple[str, str, str, str]:
    short_id = row["short_id"]
    profit = float(row["profit"])
    if row["final_aco_pnl"] == 0 and str(row["modes"]).startswith("aco_"):
        return "reject current implementation", "reject", "update", "ACO module produced zero PnL and zero position; revise activation before retesting."
    if short_id in {"C10", "C02", "C07"}:
        return "promote to rerun/variant", "primary" if profit >= champion_profit - 400 else "backup", "update", "High real platform PnL, but stochastic quote subsets and code-equivalent runs require reruns."
    if short_id == "C08":
        return "backup / rerun only if reversal remains interesting", "backup", "update", "Positive but volatile across two trials; useful for stochasticity evidence."
    if short_id == "C09":
        return "revise overlay", "experimental", "update", "Spread defensive overlay underperformed and likely throttled usable IPR fills."
    if short_id == "C01":
        return "rerun before rejecting", "experimental", "update lightly", "Single low result conflicts with code-equivalent IPR drift family results."
    return "research only", "experimental", "update lightly", "Decision evidence is limited."


def generation2_candidates() -> pd.DataFrame:
    rows = [
        {
            "candidate_id": "R2-G2-01-IPR-EXTREME-RERUN-CHAMPION",
            "role": "primary / robustness",
            "scope": IPR,
            "parent_evidence": "C02 real platform PnL 2656.625, final IPR position 34.",
            "primary_change": "Rerun C02-style IPR extreme logic without ACO to estimate quote-subset variance.",
            "why": "C02 is essentially tied with the best run and isolates IPR cleanly.",
            "validation_plan": "Run at least 2 more platform trials; compare median, worst-case, final inventory, and drawdown.",
            "priority": "spec/implement first",
        },
        {
            "candidate_id": "R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV",
            "role": "primary / robustness",
            "scope": IPR,
            "parent_evidence": "C07 and C10 are active-logic-equivalent to IPR drift plus inactive ACO but differ by about 300 PnL; C01 differs by much more.",
            "primary_change": "Rerun the C07/C10 IPR drift family with ACO disabled for clean comparability.",
            "why": "Separates strategy edge from randomized 80% quote subset noise.",
            "validation_plan": "2-3 repeated uploads, compare to C02 under same summary metrics.",
            "priority": "spec/implement first",
        },
        {
            "candidate_id": "R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY",
            "role": "primary / risk challenger",
            "scope": IPR,
            "parent_evidence": "C02 high PnL but final IPR position 34 and large XIRECS exposure.",
            "primary_change": "Add late/soft inventory neutralization to C02 without changing residual entry logic.",
            "why": "May preserve edge while reducing final-mark fragility.",
            "validation_plan": "Head-to-head vs C02 reruns: PnL, final position, drawdown, and missed upside.",
            "priority": "wave 1 challenger",
        },
        {
            "candidate_id": "R2-G2-04-IPR-SPREAD-RETUNE",
            "role": "diagnostic / execution",
            "scope": IPR,
            "parent_evidence": "Most observed spreads are well above 4, yet IPR can still make money when rare windows appear.",
            "primary_change": "Replace hard spread gate with continuous size/price throttling at wider spreads.",
            "why": "Current hard gate may overfilter and create high variance.",
            "validation_plan": "Compare fill/activity proxy through PnL change ticks and real PnL; reject if wider spreads cause adverse selection.",
            "priority": "wave 2",
        },
        {
            "candidate_id": "R2-G2-05-ACO-ACTIVATION-PROBE",
            "role": "diagnostic",
            "scope": ACO,
            "parent_evidence": "C03-C06 all ended at 0 PnL and 0 ACO position; ACO spread <=4 never appears in platform logs.",
            "primary_change": "Create small-size ACO probe with spread gate widened to realistic ACO levels and explicit activity logging.",
            "why": "First question is whether ACO modules are inactive versus genuinely unprofitable.",
            "validation_plan": "Require nonzero ACO position/PnL-change ticks; PnL can be secondary for this probe.",
            "priority": "wave 1 diagnostic",
        },
        {
            "candidate_id": "R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD",
            "role": "secondary / alpha challenger",
            "scope": ACO,
            "parent_evidence": "EDA promoted top imbalance, but implementation blocked by spread gating.",
            "primary_change": "Retest top imbalance with realistic spread handling and conservative quote sizes.",
            "why": "The signal was never actually tested online.",
            "validation_plan": "Compare to ACO activation probe; promote only if ACO PnL improves after activity exists.",
            "priority": "wave 2 after activation probe",
        },
        {
            "candidate_id": "R2-G2-07-ACO-REVERSAL-WIDE-SPREAD",
            "role": "secondary / process challenger",
            "scope": ACO,
            "parent_evidence": "EDA suggested ACO short-horizon reversal; C03 did not activate.",
            "primary_change": "Retest reversal with realistic spread handling and minimum fill opportunities.",
            "why": "Tests process hypothesis after removing implementation throttling.",
            "validation_plan": "Head-to-head against G2-06 on ACO-only logs.",
            "priority": "wave 2",
        },
        {
            "candidate_id": "R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE",
            "role": "primary combined / diagnostic",
            "scope": f"{IPR} + {ACO}",
            "parent_evidence": "C02 high IPR evidence; ACO needs activation proof.",
            "primary_change": "Use C02-style IPR as base and add small ACO activation module.",
            "why": "Keeps a competitive IPR engine while collecting ACO evidence.",
            "validation_plan": "Product attribution must show IPR still positive and ACO no worse than small controlled loss.",
            "priority": "wave 1 combined",
        },
        {
            "candidate_id": "R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE",
            "role": "primary combined / alpha",
            "scope": f"{IPR} + {ACO}",
            "parent_evidence": "C02 high IPR; EDA top imbalance; C04 inactive due gating.",
            "primary_change": "C02-style IPR plus corrected ACO imbalance module.",
            "why": "Best current route to a true two-product champion.",
            "validation_plan": "Promote only if total PnL beats IPR-only median or ACO adds nonnegative product attribution.",
            "priority": "wave 2/3",
        },
        {
            "candidate_id": "R2-G2-10-SPREAD-OVERLAY-CONTINUOUS",
            "role": "execution overlay",
            "scope": f"{IPR} + {ACO}",
            "parent_evidence": "C09 underperformed; hard spread gates are mismatched to observed spreads.",
            "primary_change": "Convert spread overlay from binary gate to product-specific size curve.",
            "why": "Keeps risk control without shutting the bot off.",
            "validation_plan": "Apply only to current champion family; compare against no-overlay paired run.",
            "priority": "wave 3",
        },
        {
            "candidate_id": "R2-G2-11-BRUNO-R1-KALMAN-R2-PORT",
            "role": "Round 1 canonical port / controlled side bet",
            "scope": f"{IPR} + {ACO}",
            "parent_evidence": "Bruno Round 1 canonical Kalman ACO logic is mature; Round 2 uses same products but changed dynamics.",
            "primary_change": "Port Bruno Kalman ACO module into Round 2 wrapper with current IPR base, R2 limits, bid=0, and R2 logging.",
            "why": "Low-effort way to test whether R1 ACO fair-value machinery still survives R2.",
            "validation_plan": "Treat as challenger; reject if ACO attribution remains zero or worse than corrected ACO probes.",
            "priority": "wave 2 side bet",
        },
        {
            "candidate_id": "R2-G2-12-NOEL-R1-C26-R2-PORT",
            "role": "Round 1 canonical port / controlled side bet",
            "scope": f"{IPR} + {ACO}",
            "parent_evidence": "Noel Round 1 canonical one-sided exit overlay is deployable and product-compatible.",
            "primary_change": "Port Noel C26 ACO one-sided/exit overlay into Round 2 wrapper with current IPR base and R2 logging.",
            "why": "Tests an already-hardened ACO execution/risk style without letting R1 assumptions dominate.",
            "validation_plan": "Compare against Bruno port and corrected ACO imbalance; keep only if attribution is positive or risk better.",
            "priority": "wave 2 side bet",
        },
        {
            "candidate_id": "R2-G2-13-MAF-BID-SCENARIO",
            "role": "mechanics-only",
            "scope": "Market Access Fee",
            "parent_evidence": "C10 bid is 0, so MAF has not been tested; Round 2 final accepts top 50% bids only.",
            "primary_change": "Choose a bid policy from EDA scenario table after champion PnL stabilizes.",
            "why": "MAF can change final net PnL but cannot be validated exactly in normal tests.",
            "validation_plan": "Use EDA MAF scenarios plus champion robustness; do not confuse with Trader.run alpha.",
            "priority": "near-final decision",
        },
    ]
    return pd.DataFrame(rows)


def write_plots(runs: pd.DataFrame, products: pd.DataFrame, spreads: pd.DataFrame, graph_frames: dict[str, pd.DataFrame]) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return

    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(11, 5))
    ordered = runs.sort_values("profit", ascending=True)
    ax.barh(ordered["short_id"] + " " + ordered["variant"].str.replace("trial_", "t"), ordered["profit"], color="#4777a8")
    ax.set_title("Battery 01 real platform profit")
    ax.set_xlabel("Profit")
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "battery_01_profit_ranking.png", dpi=160)
    plt.close(fig)

    pivot = products.pivot_table(index=["short_id", "variant"], columns="product", values="final_pnl", aggfunc="sum").fillna(0)
    pivot = pivot.loc[runs.set_index(["short_id", "variant"]).index]
    fig, ax = plt.subplots(figsize=(11, 5))
    pivot[[IPR, ACO]].plot(kind="bar", stacked=True, ax=ax, color=["#4f8c6b", "#c46f5e"])
    ax.set_title("Battery 01 product attribution")
    ax.set_ylabel("Final product PnL")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "battery_01_product_attribution.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5))
    for run, frame in graph_frames.items():
        ax.plot(frame["timestamp"], frame["value"], linewidth=1.2, label=run)
    ax.set_title("Battery 01 graphLog PnL trajectories")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("value")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "battery_01_pnl_trajectories.png", dpi=160)
    plt.close(fig)

    agg = spreads.groupby("product")[["pct_spread_le_4", "pct_spread_le_6", "pct_spread_le_16", "pct_spread_le_18", "pct_spread_le_21"]].mean()
    fig, ax = plt.subplots(figsize=(9, 4))
    agg.T.plot(kind="bar", ax=ax, color=["#4f8c6b", "#c46f5e"])
    ax.set_title("Observed top-spread gate coverage")
    ax.set_ylabel("share of two-sided rows")
    ax.tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "battery_01_spread_gate_coverage.png", dpi=160)
    plt.close(fig)


def markdown_table(df: pd.DataFrame, cols: list[str], max_rows: int | None = None, float_fmt: str = "{:.3f}") -> str:
    view = df.loc[:, cols].copy()
    if max_rows is not None:
        view = view.head(max_rows)
    for col in view.columns:
        if pd.api.types.is_float_dtype(view[col]):
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else float_fmt.format(float(x)))
    return view.to_markdown(index=False)


def write_run_summaries(runs: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    champion_profit = float(runs["profit"].max()) if not runs.empty else 0.0
    summary_rows = []
    for _, row in runs.sort_values(["candidate", "variant"]).iterrows():
        decision, candidate_class, memory_action, rationale = classify_run(row, champion_profit)
        meta = META[str(row["candidate"])[-2:]]
        run_id = row["run_id"]
        prod = products[products["run_id"] == run_id]
        prod_table = markdown_table(prod, ["product", "final_pnl", "final_position", "pnl_change_ticks"])
        if row["final_aco_pnl"] == 0 and "ACO" in str(row["tested_signal"]) and row["final_ipr_pnl"] > 0:
            confidence_update = "up for IPR / down for ACO activation"
        elif row["final_aco_pnl"] == 0 and "ACO" in str(row["tested_signal"]):
            confidence_update = "down for current ACO implementation"
        elif row["profit"] > 0:
            confidence_update = "up"
        else:
            confidence_update = "unclear"
        summary_path = PERF_CANON / f"{run_id}.md"
        raw = Path(row["raw_json_path"])
        bot = Path(row["bot_path"])
        summary = f"""# {run_id}

## Run Metadata

- Run ID: `{run_id}`
- Date: `{RUN_DATE}`
- Round: `round_2`
- Member / owner: `noel`
- Candidate ID: `{row['candidate']}`
- Variant ID: `{row['variant']}`
- Decision relevance: `canonical`
- Bot path: [`{bot}`](../../../../{bot})
- Strategy spec: [`{meta.spec}`](../../../workspace/04_strategy_specs/{meta.spec})
- Raw artifact path: [`{raw}`](../../../../{raw})
- Data day / source: Round 2 platform test JSON, day `1`, randomized 80% quote subset
- Changed axis: `{row['tested_signal']}`
- Expected effect based on EDA/understanding: `{meta.tested_signal}` should improve execution or alpha if the online proxy activates.
- Falsification metric: Real platform PnL, product attribution, final position, and whether the tested product actually changes PnL.

## Result Summary

- Status: `{row['status']}`
- Profit / score: `{row['profit']:.3f}`
- Runtime issues: none visible in platform JSON
- Rejections or errors: not available in JSON
- Position-limit concerns: final IPR `{int(row['final_ipr_position'])}`, final ACO `{int(row['final_aco_position'])}`; max path position unavailable
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`
- Proxy evidence basis: platform JSON `profit`, `activitiesLog`, `graphLog`, `positions`

## Run Classification

- Strategy family: `{row['strategy_family']}`
- Tested feature / signal: `{row['tested_signal']}`
- Changed axis type: `feature toggle / execution`
- Dedup key: `{row['strategy_family']} + {row['tested_signal']} + platform day 1 randomized subset + real platform PnL`
- Knowledge delta: `{('contradicts' if candidate_class == 'reject' else 'new')}`
- ROI-gated memory action: `{memory_action}`
- Memory action rationale: {rationale}
- Round adaptation audit: `caveat`
- Round adaptation caveat: bot/source provenance is partial because raw JSON is in `historical/`, canonical bot copy exists, and no separate stdout `.log` was found.
- Portability: `round-specific`
- Reroute: `{decision}`

## Run Diagnostics

Product PnL split:

{prod_table}

- Final positions: IPR `{int(row['final_ipr_position'])}`, ACO `{int(row['final_aco_position'])}`, XIRECS `{int(row['xirecs_position'])}`
- Max drawdown from graphLog: `{row['max_drawdown']:.3f}`
- Graph min / max: `{row['graph_min']:.3f}` / `{row['graph_max']:.3f}`
- Own trades / matched qty / avg buy-sell: unavailable in JSON
- Advanced diagnostics used: platform activity product attribution, graphLog drawdown, spread-gate diagnostics in aggregate battery report
- Statistical or regime confidence: limited; platform quote subset is randomized and only C08 has a repeated trial

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| `{row['tested_signal']}` | Improve PnL or isolate evidence | Total PnL `{row['profit']:.3f}`, IPR `{row['final_ipr_pnl']:.3f}`, ACO `{row['final_aco_pnl']:.3f}` | platform product attribution | `{confidence_update}` | `{decision}` |

## Process And Multivariate Diagnostics

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| Round 2 randomized quote subset | Repeat submissions may differ | C08 trial spread and C07/C10 same-logic gap show material variance | repeated/platform comparison | supports | rerun serious candidates |
| ACO EDA signal usability | ACO modules should produce activity if online proxy works | ACO PnL and final position are zero in this run | product attribution | weakens current implementation, not necessarily EDA signal | activation probe |

## Comparability

- Comparable to baseline: `unclear`
- Same data/source: `unclear` because testing quote subset is randomized per submission
- Same bot/spec version basis: `partial`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: no separate stdout `.log`; canonical bot copy exists after state repair, raw JSON remains in historical performance folder.

## Interpretation Limits

- Non-authoritative evidence: platform test result is real PnL for this test, but randomized 80% quote subset makes single-run ranking noisy.
- Missing artifacts: per-fill own trade log, rejection log, stdout `R2_BOT_LOG`.
- Comparability caveats: do not treat tiny PnL differences as strategy superiority without reruns.

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `{decision}`
- Decision vs champion: `{('promote' if candidate_class == 'primary' else 'backup' if candidate_class == 'backup' else 'reject' if candidate_class == 'reject' else 'rerun')}`
- Candidate class: `{candidate_class}`

## Next Action

- Next: See aggregate battery report and Generation 2 queue.
"""
        summary_path.write_text(summary)
        summary_rows.append(
            {
                "run_id": run_id,
                "summary_path": str(summary_path.relative_to(ROOT)),
                "decision": decision,
                "candidate_class": candidate_class,
                "memory_action": memory_action,
            }
        )
    return pd.DataFrame(summary_rows)


def write_memory(runs: pd.DataFrame, gen2: pd.DataFrame, summary_index: pd.DataFrame) -> None:
    champion = runs.iloc[0]
    source_rows = []
    knowledge_rows = []
    for _, row in runs.iterrows():
        summary = summary_index[summary_index["run_id"] == row["run_id"]].iloc[0]
        raw_link = Path(os.path.relpath(ROOT / str(row["raw_json_path"]), WORKSPACE)).as_posix()
        summary_link = Path(os.path.relpath(ROOT / str(summary["summary_path"]), WORKSPACE)).as_posix()
        source_rows.append(
            f"| `{row['run_id']}` | `{row['candidate']}` | [`json`]({raw_link}) / [`summary`]({summary_link}) | real platform PnL | {summary['candidate_class']} | profit `{row['profit']:.3f}`, IPR `{row['final_ipr_pnl']:.3f}`, ACO `{row['final_aco_pnl']:.3f}` |"
        )
        knowledge_rows.append(
            f"| `{row['run_id']}` | `{row['candidate']}` | {row['strategy_family']} | feature/execution | {row['tested_signal']} | real platform | randomized R2 platform subset | {('contradicts' if summary['candidate_class'] == 'reject' else 'new')} | {summary['memory_action']} |"
        )

    gen2_rows = [
        f"| {r.candidate_id} | battery01 | {r.primary_change} | high | untested | {r.validation_plan} |"
        for r in gen2.itertuples(index=False)
    ]

    latest_link = Path(os.path.relpath(ROOT / str(champion["raw_json_path"]), WORKSPACE)).as_posix()
    memory = f"""# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round: `round_2`
- Last updated: `{RUN_DATE}`
- Current champion: `{champion['candidate']}` by raw single-run PnL, but treated as provisional because `{champion['short_id']}` is code-equivalent to lower/higher same-family runs and the quote subset is randomized.
- Latest platform artifact: [`{champion['raw_json_path']}`]({latest_link})
- Memory confidence: `medium`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(source_rows)}

## Run Knowledge Index

| Run | Candidate | Strategy Family | Changed Axis | Tested Feature / Signal | PnL Source | Comparable To | Knowledge Delta | Memory Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(knowledge_rows)}

## Current Reusable Insights

| Insight ID | Products | Based On Runs | Analysis Mode | Finding | Confidence | Portability | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R2-MEM-01` | IPR | C01/C02/C07/C08/C09/C10 | edge decomposition | Positive platform PnL is entirely IPR-attributed in Battery 01. | medium/high | round-specific | strategy/spec/variant | single-run rankings are noisy under randomized quote subset |
| `R2-MEM-02` | ACO | C03/C04/C05/C06 plus combined runs | failure | Current ACO modules produced zero final ACO PnL and zero ACO position. | high for current implementation | round-specific | spec/variant/debugging | this weakens implementation, not necessarily the EDA ACO signals |
| `R2-MEM-03` | both | C08 two trials, C07/C10 same active logic | confidence | Platform testing is materially non-deterministic because the quote subset changes. | high | round-specific | validation/champion choice | use repeated trials before choosing close champions |
| `R2-MEM-04` | MAF | C10 | negative evidence | MAF remains untested because current `bid()` is 0. | high | round-specific | final mechanics | testing ignores bid acceptance anyway |
| `R2-MEM-05` | both | repo state | provenance | Active bot files were expected in canonical; repaired by copying from historical to canonical, but raw JSON stayed historical and no `.log` exists. | high | not applicable | validation hygiene | future uploads should preserve exact py/json/log bundle |

## Feature Feedback

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| IPR residual extreme | C02 | helped | real platform PnL and IPR attribution | up | rerun and add inventory challenger |
| IPR drift/residual | C01/C07/C08/C09/C10 | helped but noisy | product attribution and same-family variance | unchanged/up | repeated trials before champion choice |
| ACO top imbalance | C04/C07/C09/C10 | failed to activate in current implementation | zero ACO PnL/position | down for implementation | activation probe and spread retune |
| ACO reversal | C03/C08 | failed to activate as ACO module; combined PnL came from IPR | product attribution | down for implementation | retest only after spread activation fix |
| Spread defensive overlay | C09 | likely harmful/over-throttled | lower PnL, observed spread gates | down | replace binary gate with continuous/product-specific sizing |
| MAF bid policy | C10 | not tested | `maf_bid=0` | unchanged | final scenario decision later |

## Multivariate Relationship Feedback

| Relationship | Runs | EDA Expectation | Run Evidence | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| Top-book pressure may help ACO | C04/C07/C09/C10 | promote/exploratory | not actually tested due zero ACO attribution | unchanged for EDA, down for implementation | targeted ACO activation run |
| Cross-product lead-lag weak | all | do not use first-pass | no bot used cross-product lead-lag | unchanged | keep rejected |

## Process Hypothesis Feedback

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| IPR drift/residual is exploitable | IPR | positive IPR runs | supports, but needs repeated trials | up | keep IPR as base engine |
| ACO mean reversion/pressure is exploitable | ACO | C03-C06 | not tested because current modules did not activate | unchanged/down for current specs | rewrite activation before judging |
| Testing quote subset is stochastic | both | C08 two trials, C07/C10 | supports | up | rerun top candidates and avoid overfitting single PnL |

## Redundancy Decision Feedback

| Feature Family | Prior Redundancy Decision | Runs | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| ACO pressure variants | keep challengers separate | C04/C05/C06 | none activated | reopen implementation/spec, not EDA | retest after spread fix |
| Combined C07/C10 | unclear | C07/C10 | active logic effectively same with different PnL | mark as stochastic duplicate | use one family with repeated trials |

## Statistical Confidence Notes

- Decision-relevant confidence update: C08 fell from `1669.594` to `837.500` across two trials, showing material test-subset variance.
- Tool or method used: platform JSON parsing with product attribution, graphLog drawdown, spread gate coverage.
- Caveat or overfit risk: no own-trades/fill logs, no same-subset paired tests, exact platform quote subset unknown.

## Log-Derived Feature Discoveries

| Feature Or Signal | Source Runs / Logs | Evidence | Online Usability | Proposed Use | Next Step |
| --- | --- | --- | --- | --- | --- |
| Product-specific spread gate | all Battery 01 JSONs | ACO spread <=4 was effectively unavailable; current gates shut down ACO | usable online | execution filter / size curve | spec variant |
| Stochastic robustness score | C08/C07/C10 | repeated/same-family divergence | validation-only | champion selection | rerun top candidates |

## Feature Confidence Updates

| Feature Or Signal | Previous Confidence | New Confidence | Reason | Affected Artifact |
| --- | --- | --- | --- | --- |
| IPR residual extreme | medium/high | high enough to rerun | near-best real platform PnL | Gen2 strategy/spec |
| ACO current implementations | medium | rejected current implementation | zero product attribution | Gen2 strategy/spec |
| Spread hard gate <=4 | medium | rejected for ACO, questionable for IPR | spread diagnostics | Gen2 spec |

## Failure Patterns

| Pattern | Runs | Conditions | Failure Class | Action |
| --- | --- | --- | --- | --- |
| ACO shutdown | C03-C06 and combined ACO modules | top spread usually much wider than configured gate | execution | widen/replace spread gate and add activation probe |
| Single-run over-ranking | C08 trials, C07/C10 | randomized 80% quote subset | evidence gap | require repeated trials for champions |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| IPR residual/drift family | C02/C07/C10 | IPR product PnL | real but stochastic | real platform profit and final IPR attribution | base engine for Gen2 |
| ACO pressure/reversal | C03-C06 | no observed ACO activity | unclear | zero final ACO PnL/position | activation diagnostics first |

## Counterfactual Backlog

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(gen2_rows)}

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| Treat C10 as a MAF-tested bot | C10 | `bid()` is 0 and testing ignores accepted bids | final MAF scenario decision |
| Use current ACO bots unchanged | C03-C06 | zero ACO activity/PnL | after spread/activation spec rewrite |
| Choose champion from one PnL point | all | randomized quote subset causes high variance | repeated trials or deadline deferral |

## Downstream Notes

- EDA: targeted post-run EDA should focus on spread gates and activation, not broad rediscovery.
- Understanding: carry IPR stronger, ACO implementation weaker, ACO EDA not fully invalidated.
- Strategy generation: Gen2 should include IPR reruns, ACO activation fixes, two controlled Round 1 ports, and MAF as separate mechanics.
- Spec writing: every ACO spec must define product-specific spread handling and an activation falsification check.
- Variant generation: no broad parameter fishing; change one axis per bot unless the bot is explicitly combined.
"""
    MEMORY.write_text(memory)


def write_report(
    runs: pd.DataFrame,
    products: pd.DataFrame,
    spreads: pd.DataFrame,
    code_equiv: pd.DataFrame,
    gen2: pd.DataFrame,
    summary_index: pd.DataFrame,
) -> None:
    champion = runs.iloc[0]
    c08 = runs[runs["short_id"] == "C08"].sort_values("variant")
    c08_note = "Only one C08 trial available."
    if len(c08) >= 2:
        vals = c08["profit"].to_numpy()
        c08_note = f"C08 had two trials: `{vals[0]:.3f}` and `{vals[1]:.3f}` profit, a range of `{(vals.max() - vals.min()):.3f}`."
    spread_summary = spreads.groupby("product")[["spread_min", "spread_median", "spread_mean", "spread_max", "pct_spread_le_4", "pct_spread_le_6", "pct_spread_le_18"]].mean().reset_index()

    report = f"""# Round 2 Battery 01 Post-Run Analysis

## Executive Verdict

Battery 01 produced useful evidence, but it did **not** yet produce a clean final submission decision.

- Best raw single-run PnL: `{champion['candidate']}` / `{champion['short_id']}` with `{champion['profit']:.3f}`.
- Practical champion status: **provisional only**. C10's `bid()` is `0`, C07/C10 are effectively the same active trading logic except metadata, and Round 2 testing randomizes the 80% quote subset.
- Main positive evidence: IPR is carrying all realized PnL in this battery.
- Main failure evidence: ACO was not actually tested as alpha because every ACO module ended with `0` ACO PnL and `0` ACO position.
- Main implementation lesson: hard spread gates around `4` are mismatched to observed Round 2 top spreads, especially ACO.
- Main validation lesson: do not choose a champion from one platform result. {c08_note}

## Sources And Provenance

- Raw platform JSONs: [`rounds/round_2/performances/noel/historical`](../../performances/noel/historical)
- Canonical bot sources repaired/copied to: [`rounds/round_2/bots/noel/canonical`](../../bots/noel/canonical)
- Run summaries: [`rounds/round_2/performances/noel/canonical`](../../performances/noel/canonical)
- Post-run memory: [`post_run_research_memory.md`](../post_run_research_memory.md)
- No separate `.log` files or persisted `R2_BOT_LOG` stdout were found. Diagnostics therefore use platform `profit`, `activitiesLog`, `graphLog`, and final `positions`.

## Ranking By Real Platform PnL

{markdown_table(runs, ["short_id", "variant", "candidate", "profit", "final_ipr_pnl", "final_aco_pnl", "final_ipr_position", "final_aco_position", "max_drawdown"])}

Decision caveat: C10 beats C02 by only `{abs(float(runs.iloc[0]['profit']) - float(runs.iloc[1]['profit'])):.3f}` PnL, which is not meaningful under the observed randomized-subset variance.

## Product Attribution

{markdown_table(products.pivot_table(index=["short_id", "variant"], columns="product", values="final_pnl", aggfunc="sum").reset_index().fillna(0), ["short_id", "variant", IPR, ACO])}

Interpretation:

- IPR generated all nonzero PnL.
- ACO generated exactly `0` final PnL in all runs, including ACO-only and combined bots.
- Combined bot scores should currently be read as IPR-family scores, not two-product evidence.

## Spread-Gate Diagnostics

Average platform spread coverage across Battery 01:

{markdown_table(spread_summary, ["product", "spread_min", "spread_median", "spread_mean", "spread_max", "pct_spread_le_4", "pct_spread_le_6", "pct_spread_le_18"])}

Why this matters:

- Current non-overlay bots require `spread <= 4` before trading.
- C09 overlay allows some activity up to `spread <= 6`.
- ACO's observed top spread is almost never compatible with those gates; ACO-only C03-C06 therefore likely failed by inactivity/over-throttling.
- IPR had rare narrow-spread windows and produced PnL, but the hard gate likely increases variance and may skip useful wider-spread opportunities.

## Code Equivalence And Non-Determinism

{markdown_table(code_equiv, ["signature_group", "short_ids", "modes", "profits"], max_rows=20)}

Key read:

- C07 and C10 have the same active trading configuration except bot metadata and role; C10 is not a meaningful MAF result because `maf_bid = 0`.
- The C07/C10 PnL gap and C08 two-trial gap show that upload-to-upload randomness is decision-relevant.
- Repeated trials are mandatory for the next champion decision unless deadline pressure forces a caveated choice.

## Hypothesis Verdicts

| Hypothesis | Battery 01 Evidence | Verdict | Next Action |
| --- | --- | --- | --- |
| IPR drift/residual can make money | Multiple positive real PnL runs, all PnL attributed to IPR | supported | rerun C02 and IPR drift family; add inventory challenger |
| IPR extreme residual is better than base drift | C02 nearly tied for top raw PnL | promising, not proven | repeat C02 and compare median/worst-case |
| ACO top imbalance is usable online | C04/C07/C09/C10 show zero ACO attribution | not tested due implementation gating | ACO activation probe first |
| ACO reversal is usable online | C03 zero; C08 positive PnL came from IPR | not tested due implementation gating | retest after spread fix |
| Spread defensive overlay helps | C09 lower PnL and likely over-throttling | weakened | replace binary gate with continuous sizing |
| MAF bid policy helps | C10 bid is 0; testing ignores final bid acceptance | not tested | final scenario decision only |
| Round 2 test is deterministic | C08 trials diverge materially | contradicted | repeated trials / robust ranking |

## Per-Run Decision Index

{markdown_table(summary_index.merge(runs[["run_id", "candidate", "short_id", "variant", "profit"]], on="run_id"), ["short_id", "variant", "profit", "decision", "candidate_class", "memory_action", "summary_path"])}

## Generation 2 Candidate Queue

This queue mixes PnL candidates and diagnostic candidates deliberately. The goal is to learn fast while keeping a competitive IPR base alive.

{markdown_table(gen2, ["candidate_id", "role", "scope", "primary_change", "priority"], max_rows=None)}

## Generation 2 Priority Plan

Spec/implement first:

1. `R2-G2-01-IPR-EXTREME-RERUN-CHAMPION`
2. `R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV`
3. `R2-G2-05-ACO-ACTIVATION-PROBE`
4. `R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE`

Implement next if first wave confirms:

1. `R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY`
2. `R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD`
3. `R2-G2-07-ACO-REVERSAL-WIDE-SPREAD`
4. `R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE`

Side bets, controlled so they do not dominate:

1. `R2-G2-11-BRUNO-R1-KALMAN-R2-PORT`
2. `R2-G2-12-NOEL-R1-C26-R2-PORT`

Near-final mechanics:

1. `R2-G2-13-MAF-BID-SCENARIO`

## What Not To Do Yet

- Do not treat C10 as a proven MAF bot.
- Do not abandon ACO EDA signals purely because current ACO implementations produced zero PnL; first fix activation.
- Do not keep the current `spread <= 4` ACO gate.
- Do not pick C10 over C02 from the `3.281` PnL difference.
- Do not stack ACO imbalance, reversal, microprice, and full-book together until at least one ACO module has nonzero platform attribution.
- Do not let Round 1 ports dominate the work; use them as two controlled challengers.

## Artifacts

- [`battery_01_run_metrics.csv`](artifacts/battery_01_run_metrics.csv)
- [`battery_01_product_attribution.csv`](artifacts/battery_01_product_attribution.csv)
- [`battery_01_spread_gate_diagnostics.csv`](artifacts/battery_01_spread_gate_diagnostics.csv)
- [`battery_01_code_equivalence.csv`](artifacts/battery_01_code_equivalence.csv)
- [`battery_01_generation2_candidates.csv`](artifacts/battery_01_generation2_candidates.csv)
- [`battery_01_profit_ranking.png`](artifacts/battery_01_profit_ranking.png)
- [`battery_01_product_attribution.png`](artifacts/battery_01_product_attribution.png)
- [`battery_01_pnl_trajectories.png`](artifacts/battery_01_pnl_trajectories.png)
- [`battery_01_spread_gate_coverage.png`](artifacts/battery_01_spread_gate_coverage.png)

## Handoff

- Phase 06 should be reviewed with caveats.
- Next useful work is not broad EDA; it is targeted Gen2 spec/implementation around IPR robustness and ACO activation.
- Strategy/spec must reopen the ACO contracts before judging ACO alpha.
- Validation must run repeated trials for any close champion candidate.
"""
    REPORT.write_text(report)


def main() -> None:
    runs, products, spreads, graph_frames = collect_metrics()

    sig_groups = []
    for sig, frame in runs.groupby("config_signature"):
        sig_groups.append(
            {
                "signature_group": len(sig_groups) + 1,
                "short_ids": ", ".join(frame.sort_values("short_id")["short_id"] + "-" + frame.sort_values("short_id")["variant"]),
                "modes": "; ".join(sorted(set(frame["modes"]))),
                "profits": ", ".join(f"{p:.3f}" for p in frame.sort_values("short_id")["profit"]),
                "signature": sig,
            }
        )
    code_equiv = pd.DataFrame(sig_groups)
    gen2 = generation2_candidates()
    write_plots(runs, products, spreads, graph_frames)

    runs.to_csv(ARTIFACTS / "battery_01_run_metrics.csv", index=False)
    products.to_csv(ARTIFACTS / "battery_01_product_attribution.csv", index=False)
    spreads.to_csv(ARTIFACTS / "battery_01_spread_gate_diagnostics.csv", index=False)
    code_equiv.to_csv(ARTIFACTS / "battery_01_code_equivalence.csv", index=False)
    gen2.to_csv(ARTIFACTS / "battery_01_generation2_candidates.csv", index=False)

    summary_index = write_run_summaries(runs, products)
    summary_index.to_csv(ARTIFACTS / "battery_01_run_summary_index.csv", index=False)
    write_memory(runs, gen2, summary_index)
    write_report(runs, products, spreads, code_equiv, gen2, summary_index)

    print(f"Wrote {REPORT}")
    print(f"Wrote {MEMORY}")
    print(f"Wrote {len(summary_index)} run summaries under {PERF_CANON}")


if __name__ == "__main__":
    main()
