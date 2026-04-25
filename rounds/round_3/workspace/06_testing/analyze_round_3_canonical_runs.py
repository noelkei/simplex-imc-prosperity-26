from __future__ import annotations

import io
import json
import math
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
WORKSPACE = ROUND / "workspace"
TESTING = WORKSPACE / "06_testing"
ARTIFACTS = TESTING / "artifacts" / "canonical_runs"
PERF_CANON = ROUND / "performances" / "amin" / "canonical"
PERF_HIST = ROUND / "performances" / "amin" / "historical"
REPORT = TESTING / "round_3_canonical_run_analysis.md"

RUN_DATE = "2026-04-25"

DELTA1_PRODUCTS = ["HYDROGEL_PACK", "VELVETFRUIT_EXTRACT"]
ITM_PRODUCTS = ["VEV_4000", "VEV_4500"]
ACTIVE_PRODUCTS = ["VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300"]
UPPER_PRODUCTS = ["VEV_5400", "VEV_5500"]
FLOOR_PRODUCTS = ["VEV_6000", "VEV_6500"]
ALL_PRODUCTS = DELTA1_PRODUCTS + ITM_PRODUCTS + ACTIVE_PRODUCTS + UPPER_PRODUCTS + FLOOR_PRODUCTS

RUN_META = {
    "baseline_state_logger": {
        "short_id": "D01-logger",
        "family": "diagnostic_state_probe",
        "tested_signal": "live book / spread / inventory observation",
        "bot_path": "rounds/round_3/bots/amin/historical/baseline_state_logger.py",
    },
    "candidate_c06_v01_centered_base": {
        "short_id": "C06-base-v01",
        "family": "composite_centered_residual",
        "tested_signal": "centered Bachelier residual on VEV_5000-5300 with HYDRO/VEX sidecars",
        "bot_path": "rounds/round_3/bots/amin/historical/candidate_c06_v01_centered_base.py",
    },
    "candidate_c06_composite_inv": {
        "short_id": "C06-inv-v01",
        "family": "composite_centered_residual_inventory",
        "tested_signal": "centered Bachelier residual + inventory skew + imbalance confirmation",
        "bot_path": "rounds/round_3/bots/amin/historical/candidate_c06_composite_inv.py",
    },
}


def as_float(value: object) -> float:
    if value is None:
        return math.nan
    return float(value)


def read_platform_json(path: Path) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    data = json.loads(path.read_text())
    activities = pd.read_csv(io.StringIO(data["activitiesLog"]), sep=";")
    graph = pd.read_csv(io.StringIO(data["graphLog"]), sep=";")
    return data, activities, graph


def find_run_json(stem: str) -> Path:
    canonical = PERF_CANON / f"{stem}.json"
    historical = PERF_HIST / f"{stem}.json"
    if canonical.exists():
        return canonical
    if historical.exists():
        return historical
    raise FileNotFoundError(f"Could not locate JSON for {stem}")


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


def markdown_table(df: pd.DataFrame, cols: list[str], float_fmt: str = "{:.3f}") -> str:
    view = df.loc[:, cols].copy()
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
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def historical_profit_lookup() -> pd.DataFrame:
    rows = []
    for path in sorted(PERF_HIST.glob("*.json")):
        data = json.loads(path.read_text())
        rows.append(
            {
                "file": path.name,
                "profit": as_float(data.get("profit", math.nan)),
            }
        )
    return pd.DataFrame(rows).sort_values("profit", ascending=False)


def compute_run_metrics() -> tuple[pd.DataFrame, pd.DataFrame]:
    run_rows = []
    product_rows = []

    for stem, meta in RUN_META.items():
        json_path = find_run_json(stem)
        data, activities, graph = read_platform_json(json_path)
        positions = parse_positions(data)
        product_pnl = final_product_pnl(activities)

        row = {
            "stem": stem,
            "short_id": meta["short_id"],
            "file": json_path.name,
            "strategy_family": meta["family"],
            "tested_signal": meta["tested_signal"],
            "bot_path": meta["bot_path"],
            "profit": as_float(data.get("profit", math.nan)),
            "activities_sum": float(sum(product_pnl.values())),
            "graph_final": float(graph["value"].iloc[-1]),
            "max_drawdown": drawdown(graph["value"]),
            "graph_min": float(graph["value"].min()),
            "graph_max": float(graph["value"].max()),
            "active_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ACTIVE_PRODUCTS)),
            "delta1_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in DELTA1_PRODUCTS)),
            "itm_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ITM_PRODUCTS)),
            "upper_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in UPPER_PRODUCTS)),
            "floor_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in FLOOR_PRODUCTS)),
        }

        for symbol in ALL_PRODUCTS:
            row[f"pnl_{symbol}"] = float(product_pnl.get(symbol, 0.0))
            row[f"pos_{symbol}"] = int(positions.get(symbol, 0))
            product_rows.append(
                {
                    "stem": stem,
                    "short_id": meta["short_id"],
                    "product": symbol,
                    "profit_and_loss": float(product_pnl.get(symbol, 0.0)),
                    "final_position": int(positions.get(symbol, 0)),
                }
            )

        run_rows.append(row)

    return (
        pd.DataFrame(run_rows).sort_values("profit", ascending=False),
        pd.DataFrame(product_rows).sort_values(["stem", "profit_and_loss"]),
    )


def compute_live_market_metrics() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    logger_path = find_run_json("baseline_state_logger")
    data, activities, _ = read_platform_json(logger_path)
    del data

    numeric_cols = [
        "bid_price_1",
        "ask_price_1",
        "mid_price",
        "bid_volume_1",
        "ask_volume_1",
    ]
    for col in numeric_cols:
        activities[col] = pd.to_numeric(activities[col], errors="coerce")

    market_rows = []
    signal_rows = []

    for product, frame in activities.groupby("product"):
        frame = frame.sort_values("timestamp").copy()
        spread = frame["ask_price_1"] - frame["bid_price_1"]
        delta = frame["mid_price"].diff()
        future_delta = frame["mid_price"].shift(-1) - frame["mid_price"]
        imbalance = (
            (frame["bid_volume_1"] - frame["ask_volume_1"].abs())
            / (frame["bid_volume_1"] + frame["ask_volume_1"].abs())
        )

        market_rows.append(
            {
                "product": product,
                "spread_mean": float(spread.mean()),
                "spread_median": float(spread.median()),
                "mid_std": float(frame["mid_price"].std()),
                "mid_min": float(frame["mid_price"].min()),
                "mid_max": float(frame["mid_price"].max()),
                "unique_mids": int(frame["mid_price"].nunique()),
                "pct_spread_le_2": float((spread <= 2).mean()),
                "pct_spread_le_4": float((spread <= 4).mean()),
                "pct_spread_le_8": float((spread <= 8).mean()),
            }
        )
        signal_rows.append(
            {
                "product": product,
                "imbalance_corr_fut_delta": float(imbalance.corr(future_delta))
                if future_delta.notna().sum() > 2
                else math.nan,
                "mid_reversion_corr": float(delta.corr(future_delta))
                if future_delta.notna().sum() > 2
                else math.nan,
                "mid_delta_acf1": float(delta.autocorr(1)) if delta.notna().sum() > 2 else math.nan,
            }
        )

    vex = (
        activities[activities["product"] == "VELVETFRUIT_EXTRACT"][["timestamp", "mid_price"]]
        .rename(columns={"mid_price": "vex_mid"})
        .copy()
    )
    merged = activities.merge(vex, on="timestamp", how="left")

    option_rows = []
    for product, frame in merged[merged["product"].str.startswith("VEV_")].groupby("product"):
        strike = int(product.split("_")[1])
        intrinsic = (frame["vex_mid"] - strike).clip(lower=0)
        extrinsic = frame["mid_price"] - intrinsic
        future_delta = frame["mid_price"].shift(-1) - frame["mid_price"]
        centered = extrinsic - extrinsic.mean()
        option_rows.append(
            {
                "product": product,
                "strike": strike,
                "mid_mean": float(frame["mid_price"].mean()),
                "extrinsic_mean": float(extrinsic.mean()),
                "extrinsic_std": float(extrinsic.std()),
                "unique_mid": int(frame["mid_price"].nunique()),
                "resid_reversion_corr": float(centered.corr(future_delta))
                if future_delta.notna().sum() > 2
                else math.nan,
            }
        )

    return (
        pd.DataFrame(market_rows).sort_values("product"),
        pd.DataFrame(signal_rows).sort_values("product"),
        pd.DataFrame(option_rows).sort_values("strike"),
    )


def render_report(
    run_metrics: pd.DataFrame,
    product_metrics: pd.DataFrame,
    market_metrics: pd.DataFrame,
    signal_metrics: pd.DataFrame,
    option_metrics: pd.DataFrame,
    historical_rank: pd.DataFrame,
) -> str:
    best_hist = historical_rank.iloc[0]
    hist_base = historical_rank[historical_rank["file"] == "candidate_c06_composite_base.json"].iloc[0]

    centered = run_metrics[run_metrics["stem"] == "candidate_c06_v01_centered_base"].iloc[0]
    inv = run_metrics[run_metrics["stem"] == "candidate_c06_composite_inv"].iloc[0]

    centered_products = product_metrics[product_metrics["stem"] == "candidate_c06_v01_centered_base"]
    inv_products = product_metrics[product_metrics["stem"] == "candidate_c06_composite_inv"]

    return f"""# Round 3 Canonical Run Analysis

## Executive Verdict

The first two corrected challengers did **not** beat the historical reference.

- `candidate_c06_v01_centered_base.json` finished at `{centered['profit']:.3f}`.
- `candidate_c06_composite_inv.json` finished at `{inv['profit']:.3f}`.
- Historical frozen C06 legacy reference remains better at `{hist_base['profit']:.3f}`.
- Historical best overall learner still remains `{best_hist['file']}` at `{best_hist['profit']:.3f}`.

The main failure mode is now much clearer than before:

- both corrected challengers lose almost entirely through the active voucher bucket,
- `VEV_5200` is the dominant losing strike in both runs,
- `VEV_5300` stays positive,
- `VEX` stays positive,
- inventory skew did **not** rescue the active-voucher branch on this live run.

## Current Canonical Run Ranking

{markdown_table(run_metrics, ['short_id', 'file', 'profit', 'delta1_total', 'itm_total', 'active_total', 'max_drawdown'])}

## Product Attribution

### Centered Base

{markdown_table(centered_products, ['product', 'profit_and_loss', 'final_position'])}

### Inventory Variant

{markdown_table(inv_products, ['product', 'profit_and_loss', 'final_position'])}

## Immediate Run Findings

- The centered base ended with `VEV_5200 = +270` and `VEV_5300 = -224`; the loss profile suggests the signal is over-allocating into `VEV_5200`.
- The inventory variant reduced the terminal `VEV_5200` position to `+114`, but still lost more money than the base, so the current C04 overlay looks like an execution/risk penalty rather than a rescue.
- Neither corrected run generated meaningful PnL in ITM or upper strikes because those products were not part of the active logic.
- The logger run confirms the market data itself is usable and reconstructs a full live-day book path with zero trading interference.

## Live-Day Market Metrics From The State Logger

The logger is useful because it gives us a clean live Round 3 book sample under confirmed `TTE=5d`.

{markdown_table(market_metrics, ['product', 'spread_mean', 'spread_median', 'mid_std', 'unique_mids', 'pct_spread_le_2', 'pct_spread_le_4', 'pct_spread_le_8'])}

What changes from this live view:

- `VEV_6000` and `VEV_6500` are still completely frozen at `0.5`.
- `VEV_5400` and especially `VEV_5500` are active enough to justify learning bots.
- `HYDROGEL_PACK` still has wide spreads, so any HYDRO bot must be execution-sensitive.
- `VELVETFRUIT_EXTRACT` remains the cleanest live delta-1 product.

## Live-Day Microstructure Signal Check

{markdown_table(signal_metrics, ['product', 'imbalance_corr_fut_delta', 'mid_reversion_corr', 'mid_delta_acf1'])}

Interpretation:

- HYDRO and VEX both still show live reversion plus useful top-of-book imbalance.
- ITM vouchers (`VEV_4000`, `VEV_4500`) have stronger live reversion than the active strikes.
- `VEV_5300`, `VEV_5400`, and `VEV_5500` look more promising than `VEV_5100`/`VEV_5200`.

## Live-Day Voucher Residual Check

Using a simple intrinsic anchor against live `VELVETFRUIT_EXTRACT` mids:

{markdown_table(option_metrics, ['product', 'strike', 'extrinsic_mean', 'extrinsic_std', 'resid_reversion_corr', 'unique_mid'])}

Interpretation:

- The strongest live residual reversion remains in `VEV_4000` / `VEV_4500`.
- `VEV_5000` is weak but still directionally mean-reverting.
- `VEV_5100` and `VEV_5200` are weak to non-reverting on this live day.
- `VEV_5300` is still tradable but less clean than the ITM branch.
- `VEV_5400` / `VEV_5500` are now real candidates for targeted probes, not just monitoring.

## Decision-Relevant Takeaways

1. The active-voucher batch should stop treating `VEV_5000-5300` as one homogeneous family.
2. `VEV_5200` is now the main do-not-trust strike until an isolated learner proves otherwise.
3. `VEV_4000` / `VEV_4500` should move up sharply in the learner queue.
4. `VEV_5400` / `VEV_5500` deserve their own live probes because the logger confirms movement plus tight spreads.
5. `HYDRO` still needs an isolated learner; the live signal exists, but the historical execution has been poor.

## Recommended Bot Families After These Runs

- Isolated HYDRO learners: signal exists, execution still unproven.
- Isolated VEX learners: positive leg, clean microstructure, strong anchor role.
- ITM residual learners: strongest live and historical signal family.
- Active-voucher subset learners: especially `5000`, `5300`, and pair/subset variants that exclude `5200`.
- Upper-strike learners: `5400`, `5500`, and `5400/5500` passive or residual variants.
- Surface relative-value learners: especially `5200/5300` and `5300/5400`.

## Artifacts

- [`artifacts/canonical_runs/canonical_run_metrics.csv`](artifacts/canonical_runs/canonical_run_metrics.csv)
- [`artifacts/canonical_runs/canonical_product_attribution.csv`](artifacts/canonical_runs/canonical_product_attribution.csv)
- [`artifacts/canonical_runs/live_market_metrics.csv`](artifacts/canonical_runs/live_market_metrics.csv)
- [`artifacts/canonical_runs/live_signal_metrics.csv`](artifacts/canonical_runs/live_signal_metrics.csv)
- [`artifacts/canonical_runs/live_option_residual_metrics.csv`](artifacts/canonical_runs/live_option_residual_metrics.csv)
"""


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    run_metrics, product_metrics = compute_run_metrics()
    market_metrics, signal_metrics, option_metrics = compute_live_market_metrics()
    historical_rank = historical_profit_lookup()

    run_metrics.to_csv(ARTIFACTS / "canonical_run_metrics.csv", index=False)
    product_metrics.to_csv(ARTIFACTS / "canonical_product_attribution.csv", index=False)
    market_metrics.to_csv(ARTIFACTS / "live_market_metrics.csv", index=False)
    signal_metrics.to_csv(ARTIFACTS / "live_signal_metrics.csv", index=False)
    option_metrics.to_csv(ARTIFACTS / "live_option_residual_metrics.csv", index=False)

    REPORT.write_text(
        render_report(
            run_metrics=run_metrics,
            product_metrics=product_metrics,
            market_metrics=market_metrics,
            signal_metrics=signal_metrics,
            option_metrics=option_metrics,
            historical_rank=historical_rank,
        )
    )


if __name__ == "__main__":
    main()
