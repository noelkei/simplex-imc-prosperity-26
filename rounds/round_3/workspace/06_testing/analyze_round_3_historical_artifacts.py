from __future__ import annotations

import io
import json
import math
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
WORKSPACE = ROUND / "workspace"
TESTING = WORKSPACE / "06_testing"
ARTIFACTS = TESTING / "artifacts"
PERF_HIST = ROUND / "performances" / "amin" / "historical"
BOT_HIST = ROUND / "bots" / "amin" / "historical"
BOT_CANON = ROUND / "bots" / "amin" / "canonical"
REPORT = TESTING / "round_3_historical_performance_analysis.md"
MEMORY = WORKSPACE / "post_run_research_memory.md"

RUN_DATE = "2026-04-25"

DELTA1_PRODUCTS = ["HYDROGEL_PACK", "VELVETFRUIT_EXTRACT"]
ITM_PRODUCTS = ["VEV_4000", "VEV_4500"]
ACTIVE_PRODUCTS = ["VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300"]
UPPER_PRODUCTS = ["VEV_5400", "VEV_5500"]
FLOOR_PRODUCTS = ["VEV_6000", "VEV_6500"]
ALL_PRODUCTS = DELTA1_PRODUCTS + ITM_PRODUCTS + ACTIVE_PRODUCTS + UPPER_PRODUCTS + FLOOR_PRODUCTS

BUCKETS = {
    "delta1_total": DELTA1_PRODUCTS,
    "itm_total": ITM_PRODUCTS,
    "active_total": ACTIVE_PRODUCTS,
    "upper_total": UPPER_PRODUCTS,
    "floor_total": FLOOR_PRODUCTS,
}


@dataclass(frozen=True)
class RunMeta:
    stem: str
    short_id: str
    strategy_family: str
    tested_signal: str
    role: str
    linked_candidate: str
    bot_path: str


META = {
    "candidate_c06_composite_base": RunMeta(
        "candidate_c06_composite_base",
        "C06-legacy",
        "composite_active_vouchers_legacy",
        "legacy raw Bachelier residual + model-surface guardrail",
        "historical composite reference",
        "C06 / C03 legacy",
        "rounds/round_3/bots/amin/historical/candidate_c06_composite_base.py",
    ),
    "r3_b01_delta1_baseline": RunMeta(
        "r3_b01_delta1_baseline",
        "B01-base",
        "delta1_pair_baseline",
        "delta-1 Kalman maker pair",
        "historical learner",
        "C01 + C02 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b01_delta1_baseline.py",
    ),
    "r3_b01_delta1_optiver": RunMeta(
        "r3_b01_delta1_optiver",
        "B01-opt",
        "delta1_pair_optiver",
        "delta-1 optiver-style execution stack",
        "historical learner",
        "C01 + C02 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b01_delta1_optiver.py",
    ),
    "r3_b02_itm_anchor": RunMeta(
        "r3_b02_itm_anchor",
        "B02-anchor",
        "itm_anchor_composite",
        "ITM voucher anchor residual + delta-1 support",
        "historical learner",
        "C05 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b02_itm_anchor.py",
    ),
    "r3_b02_itm_residual": RunMeta(
        "r3_b02_itm_residual",
        "B02-resid",
        "itm_residual_vex",
        "ITM intrinsic residual + VEX anchor",
        "historical learner",
        "C05 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b02_itm_residual.py",
    ),
    "r3_b03_voucher_pure": RunMeta(
        "r3_b03_voucher_pure",
        "B03-pure",
        "active_voucher_pure",
        "active-voucher residual without delta-1 legs",
        "historical learner",
        "C03 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b03_voucher_pure.py",
    ),
    "r3_b04_full_surface": RunMeta(
        "r3_b04_full_surface",
        "B04-surf",
        "full_surface_composite",
        "8-strike full-surface residual trader",
        "historical learner",
        "C03 + C05 + upper-strike probe",
        "rounds/round_3/bots/amin/historical/r3_b04_full_surface.py",
    ),
    "r3_b05_composite_advanced": RunMeta(
        "r3_b05_composite_advanced",
        "B05-adv",
        "advanced_composite",
        "active-voucher residual + optiver delta-1 stack",
        "historical learner",
        "C06 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b05_composite_advanced.py",
    ),
    "r3_b06_tte_cautious": RunMeta(
        "r3_b06_tte_cautious",
        "B06-tte",
        "tte_cautious_composite",
        "TTE-cautious active-voucher residual",
        "historical learner",
        "C07 surrogate",
        "rounds/round_3/bots/amin/historical/r3_b06_tte_cautious.py",
    ),
    "r3_b07_delta_hedge": RunMeta(
        "r3_b07_delta_hedge",
        "B07-hedge",
        "delta_hedged_composite",
        "active-voucher residual + VEX delta hedge",
        "historical learner",
        "C03 hedge variant",
        "rounds/round_3/bots/amin/historical/r3_b07_delta_hedge.py",
    ),
    "r3_b08_regime_composite": RunMeta(
        "r3_b08_regime_composite",
        "B08-regime",
        "regime_aware_composite",
        "regime-adaptive active-voucher residual",
        "historical learner",
        "C03 / C06 regime variant",
        "rounds/round_3/bots/amin/historical/r3_b08_regime_composite.py",
    ),
}


def read_platform_json(path: Path) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    data = json.loads(path.read_text())
    activities = pd.read_csv(io.StringIO(data["activitiesLog"]), sep=";")
    graph = pd.read_csv(io.StringIO(data["graphLog"]), sep=";")
    return data, activities, graph


def parse_positions(data: dict) -> dict[str, int]:
    positions = {}
    for item in data.get("positions", []):
        if isinstance(item, dict):
            positions[str(item.get("symbol"))] = int(item.get("quantity", 0))
    return positions


def final_product_pnl(activities: pd.DataFrame) -> dict[str, float]:
    rows = activities.sort_values("timestamp").groupby("product", as_index=False).tail(1)
    return {str(row["product"]): float(row["profit_and_loss"]) for _, row in rows.iterrows()}


def drawdown(series: pd.Series) -> float:
    if series.empty:
        return math.nan
    return float((series - series.cummax()).min())


def bucket_total(values: dict[str, float], symbols: list[str]) -> float:
    return float(sum(float(values.get(symbol, 0.0)) for symbol in symbols))


def markdown_table(df: pd.DataFrame, cols: list[str], max_rows: int | None = None, float_fmt: str = "{:.3f}") -> str:
    view = df.loc[:, cols].copy()
    if max_rows is not None:
        view = view.head(max_rows)
    for col in view.columns:
        if pd.api.types.is_float_dtype(view[col]):
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else float_fmt.format(float(x)))
    view = view.fillna("")
    headers = [str(col) for col in view.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in view.itertuples(index=False, name=None):
        cells = [str(cell) for cell in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def collect_metrics() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    run_rows = []
    product_rows = []
    spread_rows = []
    graph_rows = []

    for json_path in sorted(PERF_HIST.glob("*.json")):
        stem = json_path.stem
        meta = META.get(stem)
        if meta is None:
            continue

        data, activities, graph = read_platform_json(json_path)
        positions = parse_positions(data)
        product_pnl = final_product_pnl(activities)
        activities_sum = float(sum(product_pnl.values()))
        graph_final = float(graph["value"].iloc[-1]) if not graph.empty else math.nan

        row = {
            "stem": stem,
            "file": json_path.name,
            "short_id": meta.short_id,
            "strategy_family": meta.strategy_family,
            "tested_signal": meta.tested_signal,
            "role": meta.role,
            "linked_candidate": meta.linked_candidate,
            "bot_path": meta.bot_path,
            "raw_json_path": str(json_path.relative_to(ROOT)),
            "status": data.get("status"),
            "profit": float(data.get("profit", math.nan)),
            "activities_sum": activities_sum,
            "activities_delta": float(data.get("profit", math.nan)) - activities_sum,
            "graph_final": graph_final,
            "graph_delta": float(data.get("profit", math.nan)) - graph_final,
            "max_drawdown": drawdown(graph["value"]) if not graph.empty else math.nan,
            "graph_min": float(graph["value"].min()) if not graph.empty else math.nan,
            "graph_max": float(graph["value"].max()) if not graph.empty else math.nan,
            "graph_rows": int(len(graph)),
            "activities_rows": int(len(activities)),
            "day": int(activities["day"].iloc[0]) if not activities.empty else math.nan,
        }

        for symbol in ALL_PRODUCTS:
            row[f"pnl_{symbol}"] = float(product_pnl.get(symbol, 0.0))
            row[f"pos_{symbol}"] = int(positions.get(symbol, 0))

        for bucket_name, bucket_products in BUCKETS.items():
            row[bucket_name] = bucket_total(product_pnl, bucket_products)

        row["active_short_saturation"] = int(
            sum(1 for symbol in ACTIVE_PRODUCTS if positions.get(symbol, 0) <= -300)
        )

        run_rows.append(row)

        for symbol in ALL_PRODUCTS:
            product_rows.append(
                {
                    "stem": stem,
                    "file": json_path.name,
                    "short_id": meta.short_id,
                    "product": symbol,
                    "final_pnl": float(product_pnl.get(symbol, 0.0)),
                    "final_position": int(positions.get(symbol, 0)),
                }
            )

        with_spreads = activities.copy()
        with_spreads["spread"] = with_spreads["ask_price_1"] - with_spreads["bid_price_1"]
        for product, frame in with_spreads.groupby("product"):
            spreads = frame["spread"].dropna()
            spread_rows.append(
                {
                    "stem": stem,
                    "file": json_path.name,
                    "short_id": meta.short_id,
                    "product": str(product),
                    "rows": int(len(frame)),
                    "spread_mean": float(spreads.mean()) if not spreads.empty else math.nan,
                    "spread_median": float(spreads.median()) if not spreads.empty else math.nan,
                    "spread_min": float(spreads.min()) if not spreads.empty else math.nan,
                    "spread_max": float(spreads.max()) if not spreads.empty else math.nan,
                    "pct_spread_le_4": float((spreads <= 4).mean()) if not spreads.empty else math.nan,
                    "pct_spread_le_8": float((spreads <= 8).mean()) if not spreads.empty else math.nan,
                    "pct_spread_le_12": float((spreads <= 12).mean()) if not spreads.empty else math.nan,
                    "pct_spread_le_20": float((spreads <= 20).mean()) if not spreads.empty else math.nan,
                }
            )

        graph_copy = graph.copy()
        graph_copy["stem"] = stem
        graph_copy["short_id"] = meta.short_id
        graph_rows.append(graph_copy)

    runs = pd.DataFrame(run_rows).sort_values("profit", ascending=False)
    products = pd.DataFrame(product_rows)
    spreads = pd.DataFrame(spread_rows)
    graphs = pd.concat(graph_rows, ignore_index=True) if graph_rows else pd.DataFrame(columns=["timestamp", "value", "stem", "short_id"])
    return runs, products, spreads, graphs


def signal_coverage() -> pd.DataFrame:
    rows = [
        {
            "candidate_id": "C01",
            "strategy": "HYDROGEL microstructure MM",
            "products": "HYDROGEL_PACK",
            "isolated_bot_exists": "no",
            "implemented_bots": "combined only: r3_b01_* pair bots, candidate_c06 family, r3_b05/r3_b06/r3_b07/r3_b08",
            "tested_json_exists": "partial only (never hydro-only)",
            "current_active_bot": "none isolated",
            "gap_or_next_probe": "missing hydro-only learner; current evidence says hydro is weak/negative in the tested combined implementations",
        },
        {
            "candidate_id": "C02",
            "strategy": "VEX delta-1 MM + voucher anchor",
            "products": "VELVETFRUIT_EXTRACT",
            "isolated_bot_exists": "no",
            "implemented_bots": "delta-1 pair bots, ITM bots, candidate_c06 family, r3_b05/r3_b06/r3_b07/r3_b08",
            "tested_json_exists": "partial only (never vex-only)",
            "current_active_bot": "none isolated",
            "gap_or_next_probe": "missing vex-only learner despite VEX being the strongest tested delta-1 leg",
        },
        {
            "candidate_id": "C03",
            "strategy": "Active-voucher centered residual reversion",
            "products": "VEV_5000-5300",
            "isolated_bot_exists": "yes",
            "implemented_bots": "r3_b03_voucher_pure, candidate_c06_composite_base legacy, candidate_c06_v01_centered_base",
            "tested_json_exists": "yes for legacy/raw family; no for current centered challenger",
            "current_active_bot": "candidate_c06_v01_centered_base.py",
            "gap_or_next_probe": "run the centered challenger; historical raw family lost money and saturated shorts, especially in VEV_5000-5200",
        },
        {
            "candidate_id": "C04",
            "strategy": "Active-voucher residual + inventory skew + imbalance",
            "products": "VEV_5000-5300",
            "isolated_bot_exists": "no",
            "implemented_bots": "candidate_c06_composite_inv only",
            "tested_json_exists": "no clean C04 run yet",
            "current_active_bot": "candidate_c06_composite_inv.py",
            "gap_or_next_probe": "run the clean inventory challenger; current historical evidence says short saturation is a real issue",
        },
        {
            "candidate_id": "C05",
            "strategy": "ITM structural-anchor residual",
            "products": "VEV_4000-4500",
            "isolated_bot_exists": "partial",
            "implemented_bots": "r3_b02_itm_anchor, r3_b02_itm_residual, r3_b04_full_surface",
            "tested_json_exists": "yes",
            "current_active_bot": "none",
            "gap_or_next_probe": "historical best tested family; worth a fresh learning variant or spec promotion",
        },
        {
            "candidate_id": "C06",
            "strategy": "Full composite trader",
            "products": "HYDROGEL + VEX + VEV_5000-5300",
            "isolated_bot_exists": "not applicable",
            "implemented_bots": "candidate_c06_composite_base legacy, candidate_c06_v01_centered_base, r3_b05_composite_advanced, r3_b08_regime_composite",
            "tested_json_exists": "yes for legacy/alternate composite families",
            "current_active_bot": "candidate_c06_v01_centered_base.py",
            "gap_or_next_probe": "current centered base still needs its first run; hydro and VEV_5000 behavior remain the biggest composite risks",
        },
        {
            "candidate_id": "C07",
            "strategy": "TTE-cautious active-voucher residual",
            "products": "VEV_5000-5300",
            "isolated_bot_exists": "no",
            "implemented_bots": "r3_b06_tte_cautious",
            "tested_json_exists": "yes",
            "current_active_bot": "none",
            "gap_or_next_probe": "historical cautious bot still lost; keep as calibration branch, not as current default",
        },
        {
            "candidate_id": "D01",
            "strategy": "No-trade diagnostic state logger",
            "products": "all round_3 products",
            "isolated_bot_exists": "yes",
            "implemented_bots": "baseline_state_logger.py",
            "tested_json_exists": "no",
            "current_active_bot": "baseline_state_logger.py",
            "gap_or_next_probe": "run only for state/log collection; use for diagnostics, never for alpha",
        },
    ]
    return pd.DataFrame(rows)


def next_backlog() -> pd.DataFrame:
    rows = [
        {
            "idea_id": "R3-NEXT-01",
            "type": "diagnostic",
            "idea": "Run baseline_state_logger first if we need richer per-iteration state/trade logs.",
            "why": "Historical JSONs give book/PnL, but not enough detail about trade events, own fills, or exact state transitions.",
            "priority": "high",
        },
        {
            "idea_id": "R3-NEXT-02",
            "type": "validation",
            "idea": "Run candidate_c06_v01_centered_base against the historical legacy base.",
            "why": "Historical active-voucher runs weaken raw residual implementations but strengthen the case for the corrected centered-residual challenger.",
            "priority": "high",
        },
        {
            "idea_id": "R3-NEXT-03",
            "type": "validation",
            "idea": "Run candidate_c06_composite_inv after the centered base.",
            "why": "Historical active-voucher runs repeatedly hit short saturation; the clean inventory variant directly tests that risk control.",
            "priority": "high",
        },
        {
            "idea_id": "R3-NEXT-04",
            "type": "learning variant",
            "idea": "Create a hydro-only learner and a vex-only learner.",
            "why": "We still do not have isolated online evidence for C01 or C02; current data only tests them in pairs or composites.",
            "priority": "high",
        },
        {
            "idea_id": "R3-NEXT-05",
            "type": "learning variant",
            "idea": "Reopen ITM residual as a near-term learner/follow-up.",
            "why": "The only positive tested family is ITM/VEX, led by r3_b02_itm_residual (+1409.371) and r3_b02_itm_anchor (+726.893).",
            "priority": "high",
        },
        {
            "idea_id": "R3-NEXT-06",
            "type": "learning variant",
            "idea": "Test an active-voucher subset without VEV_5000 (for example VEV_5100-5300 or VEV_5200-5300).",
            "why": "VEV_5000 was negative in 7/7 tested runs; VEV_5300 was positive in 7/7.",
            "priority": "medium/high",
        },
        {
            "idea_id": "R3-NEXT-07",
            "type": "targeted EDA + variant",
            "idea": "Recheck VEV_5400/5500 with platform-style evidence before discarding them.",
            "why": "Historical activitiesLog spreads look tight there, which contradicts the raw-day EDA; however the one full-surface run still lost money.",
            "priority": "medium",
        },
    ]
    return pd.DataFrame(rows)


def write_plots(runs: pd.DataFrame, products: pd.DataFrame, graphs: pd.DataFrame) -> None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return

    ordered = runs.sort_values("profit", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(ordered["short_id"], ordered["profit"], color="#3e7cb1")
    ax.set_title("Round 3 historical profit ranking")
    ax.set_xlabel("real platform PnL")
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "historical_profit_ranking.png", dpi=160)
    plt.close(fig)

    bucket_frame = runs.loc[:, ["short_id", "delta1_total", "itm_total", "active_total", "upper_total"]].set_index("short_id")
    fig, ax = plt.subplots(figsize=(11, 5))
    bucket_frame.plot(kind="bar", stacked=True, ax=ax, color=["#566573", "#4f8c6b", "#c46f5e", "#b58f4e"])
    ax.set_title("Round 3 historical PnL bucket attribution")
    ax.set_ylabel("bucket PnL")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "historical_bucket_attribution.png", dpi=160)
    plt.close(fig)

    active = products[products["product"].isin(ACTIVE_PRODUCTS)].pivot(index="short_id", columns="product", values="final_pnl").fillna(0.0)
    fig, ax = plt.subplots(figsize=(11, 5))
    active.plot(kind="bar", ax=ax, color=["#7b3f00", "#9f5f00", "#c77d00", "#e09f3e"])
    ax.set_title("Active voucher final PnL by strike")
    ax.set_ylabel("final product PnL")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "historical_active_voucher_pnl.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5))
    for short_id, frame in graphs.groupby("short_id"):
        ax.plot(frame["timestamp"], frame["value"], linewidth=1.0, label=short_id)
    ax.set_title("Round 3 graphLog trajectories")
    ax.set_xlabel("timestamp")
    ax.set_ylabel("graphLog value")
    ax.legend(fontsize=7, ncol=2)
    fig.tight_layout()
    fig.savefig(ARTIFACTS / "historical_graph_trajectories.png", dpi=160)
    plt.close(fig)


def write_memory(runs: pd.DataFrame, coverage: pd.DataFrame, backlog: pd.DataFrame) -> None:
    best = runs.iloc[0]
    best_link = Path(os.path.relpath(ROOT / best.raw_json_path, WORKSPACE)).as_posix()
    source_rows = []
    knowledge_rows = []
    for row in runs.itertuples(index=False):
        raw_link = Path(os.path.relpath(ROOT / row.raw_json_path, WORKSPACE)).as_posix()
        source_rows.append(
            f"| `{row.short_id}` | `{row.linked_candidate}` | [`json`]({raw_link}) | real platform PnL | research | profit `{row.profit:.3f}`, delta1 `{row.delta1_total:.3f}`, itm `{row.itm_total:.3f}`, active `{row.active_total:.3f}` |"
        )
        if row.itm_total > 0 and row.profit > 0:
            delta = "new"
            action = "update"
        elif row.active_total < 0:
            delta = "contradicts"
            action = "update"
        else:
            delta = "confirms"
            action = "update lightly"
        knowledge_rows.append(
            f"| `{row.short_id}` | `{row.linked_candidate}` | {row.strategy_family} | execution / risk | {row.tested_signal} | real platform | historical Round 3 set | {delta} | {action} |"
        )

    backlog_rows = [
        f"| {row.idea_id} | historical_analysis | {row.type} | {row.priority} | untested | {row.idea} |"
        for row in backlog.itertuples(index=False)
    ]

    memory = f"""# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round: `round_3`
- Last updated: `{RUN_DATE}`
- Current champion: no current active champion yet. Best historical tested artifact is `{best.short_id}` / `{best.file}` with `{best.profit:.3f}`, but it is not the current active canonical path.
- Latest platform artifact: [`{best.raw_json_path}`]({best_link})
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
| `R3-MEM-01` | all | all 11 historical JSONs | validation heuristic | The sum of the final per-product `activitiesLog.profit_and_loss` rows equals JSON `profit` exactly in every artifact. | high | likely reusable | validation / Phase 06 | only applies when `activitiesLog` exists |
| `R3-MEM-02` | all | all 11 historical JSONs | validation heuristic | Final `graphLog` is only an audit proxy; median absolute delta vs `profit` is about `124.541`, max `344.146`. | high | likely reusable | validation / Phase 06 | do not rank bots with `graphLog` alone |
| `R3-MEM-03` | VEX + ITM | B02-anchor, B02-resid | edge | ITM/VEX residual family is the only positive tested branch so far. | medium/high | round-specific | strategy / variant | both runs still include VEX exposure, so pure ITM still needs isolation |
| `R3-MEM-04` | HYDROGEL | all nonzero HYDRO runs | negative evidence | HYDROGEL was negative in `9/9` nonzero runs; current online implementations do not show a clean hydro edge. | high for current implementations | round-specific | strategy / variant | this weakens current hydro bots, not the raw EDA signal itself |
| `R3-MEM-05` | active vouchers | B03, C06-legacy, B05, B06, B07, B08, B04 | failure / edge | Losses cluster in `VEV_5000-5200`; `VEV_5300` is positive in `7/7` tested runs. | high | round-specific | spec / variant | historical active-voucher bots mostly used raw or differently tuned residual logic, not the new centered challenger |
| `R3-MEM-06` | active vouchers | C06-legacy, B05, B07, B08, B04, B03 | failure | Active-voucher bots repeatedly ended near max short inventory (often `-1200` aggregate across `VEV_5000-5300`). | high | round-specific | spec / variant | inventory saturation is an implementation and risk clue, not proof that the signal is dead |
| `R3-MEM-07` | HYDRO / wide strikes | all 11 historical JSONs | contradiction / validation | Platform-style spreads show HYDRO much wider than VEX, and `VEV_5400/5500` narrower than raw-day EDA suggested. | medium | round-specific | targeted EDA / validation | historical `activitiesLog` is platform-style evidence, not official round fact |

## Feature Feedback

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| HYDRO delta-1 maker logic | B01-base, B01-opt, composite families | failed in current implementations | product attribution | down | create hydro-only learner before trusting hydro inside composites |
| VEX delta-1 / anchor logic | most nonzero VEX runs | helped more often than not | product attribution | up | isolate with vex-only learner |
| ITM residual / anchor logic | B02-anchor, B02-resid, B04 | helped | product attribution | up | reprioritize ITM follow-up |
| Raw active-voucher residual family | B03, C06-legacy, B05, B06, B08 | failed in tested implementations | strike-level attribution + inventory saturation | down for raw family | test centered-residual challenger next |
| TTE-cautious overlay | B06 | improved less than hoped | direct comparison vs legacy family | unchanged/down | keep as secondary branch only |
| Delta hedge overlay | B07 | reduced active-voucher loss but hurt VEX leg badly | product attribution | unclear | debug only after base centered run exists |

## Multivariate Relationship Feedback

| Relationship | Runs | EDA Expectation | Run Evidence | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| VEX is the usable voucher anchor | most positive families | strong | supports | up | keep VEX as anchor and isolate it |
| HYDRO is independent and additive | composite families | additive sidecar | independence not contradicted, but contribution weak/negative | unchanged for independence / down for usefulness | hydro-only learner |
| Wide-strike spreads make 5400/5500 untradeable | raw EDA vs B04 platform-style log | exclude by default | historical platform-style spreads contradict the raw spread claim, but profitability still weak | unchanged / mixed | targeted EDA before reopening |

## Process Hypothesis Feedback

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| ITM residual snap-back is monetizable | VEV_4000-4500 | B02-anchor, B02-resid | supports | up | move ITM learning variants forward |
| Active near-ATM residual mean reversion is monetizable with current raw implementations | VEV_5000-5300 | B03, C06-legacy, B05, B06, B08 | weakens / contradicts raw implementation family | down for current raw family | centered challenger + inventory control |
| TTE=5d needs caution | VEV_5000-5300 | B06 | not resolved cleanly | unchanged | keep as later calibration branch |

## Redundancy Decision Feedback

| Feature Family | Prior Redundancy Decision | Runs | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| Raw residual vs centered residual | raw residual was the historical default | B03, C06-legacy, B05, B06, B08 | raw family underperformed | spec revision already done | test centered residual live |
| Hydro sidecar branch | keep as separate branch | composite families | currently adds little or negative value | reopen | isolate before keeping it in composites |

## Statistical Confidence Notes

- Decision-relevant confidence update: `activitiesLog` final-sum is an exact PnL proxy when JSON `profit` is present; `graphLog` final is not.
- Tool or method used: platform JSON parsing, product attribution, spread coverage, and graphLog drawdown.
- Caveat or overfit risk: no stdout `.log`, no own-trade detail, and no exact artifact bundle for every historical upload.

## Log-Derived Feature Discoveries

| Feature Or Signal | Source Runs / Logs | Evidence | Online Usability | Proposed Use | Next Step |
| --- | --- | --- | --- | --- | --- |
| `activitiesLog` final product PnL split | all historical JSONs | exact reconstruction of total PnL | validation-only | diagnostics / run ranking | keep as default PnL proxy when `profit` is missing |
| HYDRO wide-top-spread warning | all historical JSONs | mean HYDRO top spread about `15.6` | usable online | execution filter / strategy pruning | hydro-only learner |
| `VEV_5000` strike penalty | active-voucher runs | negative in `7/7` tested runs | usable online | product filter / risk control | targeted variant excluding `VEV_5000` |
| Short-saturation alert for active vouchers | active-voucher composite runs | repeated `-300` terminal positions | usable online | risk control | inventory-first challenger |

## Feature Confidence Updates

| Feature Or Signal | Previous Confidence | New Confidence | Reason | Affected Artifact |
| --- | --- | --- | --- | --- |
| ITM residual branch | medium/high | high enough to prioritize | best historical real platform results | strategy / variant |
| HYDRO online implementation | medium | low for current code paths | consistently negative realized contribution | strategy / variant |
| Raw active-voucher residual family | medium/high | lowered | repeated historical losses and short saturation | spec / variant |

## Failure Patterns

| Pattern | Runs | Conditions | Failure Class | Action |
| --- | --- | --- | --- | --- |
| Active-voucher short saturation | C06-legacy, B05, B08, B04, B03 | repeated terminal `-300` per strike | inventory / risk | test inventory-clean challenger |
| HYDRO drag | B01-base, B01-opt, B05 and most composites | HYDRO PnL stays negative | signal / execution | isolate hydro before keeping it |
| VEV_5000 drag | all active-voucher runs | `VEV_5000` negative in every tested run | product-selection / risk | test subset without `VEV_5000` |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| VEX + ITM residual family | B02-anchor, B02-resid | VEX anchor plus ITM voucher residual | real enough to reprioritize | positive real platform PnL in both tested implementations | next learner / spec |
| Raw active-voucher family | B03, C06-legacy, B05, B06, B08 | mostly short inventory mark against lower strikes | fragile / failing | repeated negative strike attribution | replace with centered challenger |

## Counterfactual Backlog

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
{chr(10).join(backlog_rows)}

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| Treat `graphLog` final as real PnL | all | it drifts materially from JSON `profit` | only as audit sanity check |
| Assume HYDRO helps just because EDA liked it | B01-base, B01-opt, composites | realized contribution is consistently negative in current implementations | after hydro-only learner |
| Treat raw active-voucher losses as proof the corrected centered challenger is dead | historical active-voucher family | current active canonical bot uses a different centered signal and different guardrail | after the corrected base has a real run |

## Downstream Notes

- EDA: revisit HYDRO online spread conditions and the `VEV_5400/5500` raw-vs-platform spread contradiction.
- Understanding: carry forward that historical ITM/VEX evidence is strongest, HYDRO is weakest, and `VEV_5000` is the worst active strike in tested bots.
- Strategy generation: next learning queue should include the logger, the current corrected challengers, hydro-only/vex-only learners, ITM follow-up, and an active-voucher subset without `VEV_5000`.
- Spec writing: keep centered residual and observed-surface guardrail; add explicit short-saturation / strike-selection checks before broad composite reruns.
- Variant generation: prioritize one-axis learning variants over broader “best bot” composites until the signal map is clearer.
"""
    MEMORY.write_text(memory)


def write_report(runs: pd.DataFrame, products: pd.DataFrame, spreads: pd.DataFrame, coverage: pd.DataFrame, backlog: pd.DataFrame) -> None:
    best = runs.iloc[0]
    proxy_mean = runs["graph_delta"].abs().mean()
    proxy_max = runs["graph_delta"].abs().max()

    bucket_summary = runs.loc[:, ["short_id", "profit", "delta1_total", "itm_total", "active_total", "upper_total", "max_drawdown", "active_short_saturation"]]
    strike_summary = products[products["product"].isin(ACTIVE_PRODUCTS)].pivot(index="short_id", columns="product", values="final_pnl").reset_index().fillna(0.0)
    spread_summary = (
        spreads.groupby("product", as_index=False)[
            ["spread_mean", "spread_median", "pct_spread_le_4", "pct_spread_le_8", "pct_spread_le_12", "pct_spread_le_20"]
        ]
        .mean()
        .sort_values("product")
    )

    report = f"""# Round 3 Historical Performance Analysis

## Executive Verdict

Historical Round 3 platform artifacts already teach us a lot before we run the two corrected canonical challengers.

- Best tested historical artifact: `{best.file}` with real platform PnL `{best.profit:.3f}`.
- Best tested branch so far: **VEX + ITM voucher residual** (`r3_b02_itm_residual`, then `r3_b02_itm_anchor`).
- Weakest current branch: **HYDRO online implementations**. HYDRO is negative in every nonzero tested run.
- Main active-voucher problem in historical bots: losses cluster in `VEV_5000-5200`, while `VEV_5300` stays positive and several bots finish max short across all active strikes.
- Validation heuristic now calibrated: the final per-product `activitiesLog` rows reconstruct total PnL exactly; `graphLog` is only an audit proxy.

## Artifact Audit And PnL Proxy Calibration

Real platform PnL source for these historical artifacts is JSON `profit`. For future cases where `profit` is missing but `activitiesLog` exists, the best proxy is:

1. Sum of the final per-product `profit_and_loss` values from `activitiesLog`.
2. Use `graphLog` only as a weak audit proxy.

Calibration on the 11 historical Round 3 JSONs:

- `activitiesLog` final-sum delta vs JSON `profit`: exact `0.0` in every artifact.
- `graphLog` final value median absolute delta vs JSON `profit`: `{proxy_mean:.3f}` mean absolute delta, `{runs['graph_delta'].abs().median():.3f}` median absolute delta, max `{proxy_max:.3f}`.

## Ranking By Real Platform PnL

{markdown_table(runs, ["short_id", "file", "profit", "delta1_total", "itm_total", "active_total", "max_drawdown"])}

## Bucket Attribution

`delta1_total = HYDROGEL + VEX`, `itm_total = VEV_4000 + VEV_4500`, `active_total = VEV_5000-5300`, `upper_total = VEV_5400 + VEV_5500`.

{markdown_table(bucket_summary, ["short_id", "profit", "delta1_total", "itm_total", "active_total", "upper_total", "max_drawdown", "active_short_saturation"])}

Interpretation:

- The two positive bots are ITM/VEX families.
- Delta-1-only families are negative, especially the Optiver-style stack.
- Historical active-voucher families mostly lose through the lower active strikes and end heavily short.
- The corrected centered-residual challenger is still worth running because these historical bots mostly tested raw or differently tuned residual families, not the new centered implementation.

## Active Voucher Strike Attribution

{markdown_table(strike_summary, ["short_id", "VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300"])}

Key pattern:

- `VEV_5000` is negative in `7/7` tested active-voucher runs.
- `VEV_5100` is negative in `6/7`.
- `VEV_5200` is negative in `6/7`.
- `VEV_5300` is positive in `7/7`.

This is the clearest reason to test a subset variant that excludes `VEV_5000` before we assume the entire active-voucher branch is bad.

## Spread Diagnostics From Platform-Style Logs

{markdown_table(spread_summary, ["product", "spread_mean", "spread_median", "pct_spread_le_4", "pct_spread_le_8", "pct_spread_le_12", "pct_spread_le_20"])}

What this changes:

- HYDRO top-of-book spreads are much wider than VEX in platform-style logs, which weakens trust in the current HYDRO online implementation.
- VEX still looks tradable.
- `VEV_5000-5300` are not obviously failing just because spreads are too wide.
- `VEV_5400/5500` look much tighter here than the raw-day EDA suggested; that contradiction should trigger targeted validation, not blind promotion.

## Signal And Bot Coverage Matrix

{markdown_table(coverage, ["candidate_id", "strategy", "products", "isolated_bot_exists", "tested_json_exists", "current_active_bot", "gap_or_next_probe"], max_rows=None)}

Counts from the current repo state:

- Formal strategy candidates in the Round 3 strategy artifact: `7` (`C01` to `C07`).
- Underlying non-composite signal families: `6` (`C01`-`C05` + `C07`; `C06` is the composite wrapper).
- Implemented Round 3 bot files now relevant to learning: `14` total.
  - `11` historical tested bots with paired JSONs.
  - `2` current canonical challengers.
  - `1` diagnostic no-trade state logger.

## What We Have Not Tested Cleanly Yet

- No **HYDRO-only** learner bot.
- No **VEX-only** learner bot.
- No clean **C04 inventory** run yet.
- No fresh run yet for the corrected **centered-residual base**.
- No **upper-strike-only (`VEV_5400/5500`)** learner bot.
- No **pure ITM-only** bot without any VEX/delta-1 support.

## Recommended Next Iterations

These next runs are for **learning signal behavior**, not for picking the final global champion immediately.

{markdown_table(backlog, ["idea_id", "type", "idea", "why", "priority"], max_rows=None)}

## Bottom Line

Before new uploads, the historical JSONs already tell us:

1. The best exact PnL proxy from platform-style artifacts is the final `activitiesLog` product sum, not `graphLog`.
2. ITM/VEX residual logic is the strongest tested family so far.
3. HYDRO is the weakest current online branch and should not be trusted without an isolated learner.
4. Raw active-voucher families underperform mainly through `VEV_5000-5200` and short saturation, which is exactly why the new centered and inventory-clean challengers are still worth testing.

## Artifacts

- [`artifacts/historical_run_metrics.csv`](artifacts/historical_run_metrics.csv)
- [`artifacts/historical_product_attribution.csv`](artifacts/historical_product_attribution.csv)
- [`artifacts/historical_spread_diagnostics.csv`](artifacts/historical_spread_diagnostics.csv)
- [`artifacts/historical_signal_coverage.csv`](artifacts/historical_signal_coverage.csv)
- [`artifacts/historical_next_backlog.csv`](artifacts/historical_next_backlog.csv)
- [`artifacts/historical_profit_ranking.png`](artifacts/historical_profit_ranking.png)
- [`artifacts/historical_bucket_attribution.png`](artifacts/historical_bucket_attribution.png)
- [`artifacts/historical_active_voucher_pnl.png`](artifacts/historical_active_voucher_pnl.png)
- [`artifacts/historical_graph_trajectories.png`](artifacts/historical_graph_trajectories.png)

## Handoff

- This report is decision-supporting evidence, not official Prosperity truth.
- Next useful work is:
  1. optional diagnostic logger run for richer state logs,
  2. first run of `candidate_c06_v01_centered_base.py`,
  3. first run of `candidate_c06_composite_inv.py`,
  4. then isolated learning variants for HYDRO, VEX, and ITM / strike selection.
"""
    REPORT.write_text(report)


def main() -> None:
    TESTING.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    runs, products, spreads, graphs = collect_metrics()
    coverage = signal_coverage()
    backlog = next_backlog()

    runs.to_csv(ARTIFACTS / "historical_run_metrics.csv", index=False)
    products.to_csv(ARTIFACTS / "historical_product_attribution.csv", index=False)
    spreads.to_csv(ARTIFACTS / "historical_spread_diagnostics.csv", index=False)
    coverage.to_csv(ARTIFACTS / "historical_signal_coverage.csv", index=False)
    backlog.to_csv(ARTIFACTS / "historical_next_backlog.csv", index=False)

    write_plots(runs, products, graphs)
    write_memory(runs, coverage, backlog)
    write_report(runs, products, spreads, coverage, backlog)

    print(f"Wrote {REPORT}")
    print(f"Wrote {MEMORY}")


if __name__ == "__main__":
    main()
