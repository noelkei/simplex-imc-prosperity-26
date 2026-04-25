from __future__ import annotations

import io
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[4]
ROUND = ROOT / "rounds" / "round_3"
WORKSPACE = ROUND / "workspace"
TESTING = WORKSPACE / "06_testing"
ARTIFACTS = TESTING / "artifacts" / "full_synthesis"
PERF_HIST = ROUND / "performances" / "amin" / "historical"
BOT_HIST = ROUND / "bots" / "amin" / "historical"
MANIFEST = WORKSPACE / "05_implementation" / "learning_batch_wave1_manifest.md"
REPORT = TESTING / "round_3_full_performance_synthesis.md"

ALL_PRODUCTS = [
    "HYDROGEL_PACK",
    "VELVETFRUIT_EXTRACT",
    "VEV_4000",
    "VEV_4500",
    "VEV_5000",
    "VEV_5100",
    "VEV_5200",
    "VEV_5300",
    "VEV_5400",
    "VEV_5500",
    "VEV_6000",
    "VEV_6500",
]
DELTA1_PRODUCTS = ["HYDROGEL_PACK", "VELVETFRUIT_EXTRACT"]
ITM_PRODUCTS = ["VEV_4000", "VEV_4500"]
ACTIVE_PRODUCTS = ["VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300"]
UPPER_PRODUCTS = ["VEV_5400", "VEV_5500"]
FLOOR_PRODUCTS = ["VEV_6000", "VEV_6500"]
ACTIVE_UPPER_PRODUCTS = ACTIVE_PRODUCTS + UPPER_PRODUCTS


@dataclass(frozen=True)
class RunMeta:
    short_id: str
    era: str
    candidate_family: str
    analysis_bucket: str
    hypothesis: str
    product_scope: str
    bot_path: str


MANUAL_RUN_META: dict[str, RunMeta] = {
    "baseline_state_logger": RunMeta(
        short_id="D01-logger",
        era="diagnostic",
        candidate_family="diagnostic logger",
        analysis_bucket="diagnostic",
        hypothesis="Capture the live TTE=5d book and trade environment without alpha or inventory interference.",
        product_scope="all round_3 products",
        bot_path="rounds/round_3/bots/amin/historical/baseline_state_logger.py",
    ),
    "candidate_c06_composite_base": RunMeta(
        short_id="C06-legacy",
        era="legacy",
        candidate_family="legacy composite raw residual",
        analysis_bucket="corrected_and_legacy_composites",
        hypothesis="Broad C06 composite using the pre-centered active-voucher residual family.",
        product_scope="HYDRO + VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/candidate_c06_composite_base.py",
    ),
    "candidate_c06_v01_centered_base": RunMeta(
        short_id="C06-base-v01",
        era="corrected",
        candidate_family="corrected centered composite",
        analysis_bucket="corrected_and_legacy_composites",
        hypothesis="Centered Bachelier residual plus observed-surface guardrail should fix the raw active-voucher family.",
        product_scope="HYDRO + VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/candidate_c06_v01_centered_base.py",
    ),
    "candidate_c06_composite_inv": RunMeta(
        short_id="C06-inv-v01",
        era="corrected",
        candidate_family="corrected centered composite inventory",
        analysis_bucket="corrected_and_legacy_composites",
        hypothesis="Inventory skew and imbalance confirmation should rescue the corrected active-voucher basket.",
        product_scope="HYDRO + VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/candidate_c06_composite_inv.py",
    ),
    "r3_b01_delta1_baseline": RunMeta(
        short_id="B01-base",
        era="legacy",
        candidate_family="legacy delta1 baseline",
        analysis_bucket="legacy_delta1",
        hypothesis="A plain delta-1 pair maker should monetize HYDRO and VEX microstructure.",
        product_scope="HYDRO + VEX",
        bot_path="rounds/round_3/bots/amin/historical/r3_b01_delta1_baseline.py",
    ),
    "r3_b01_delta1_optiver": RunMeta(
        short_id="B01-opt",
        era="legacy",
        candidate_family="legacy delta1 optiver",
        analysis_bucket="legacy_delta1",
        hypothesis="A more aggressive Optiver-style delta-1 execution stack should improve on the plain pair maker.",
        product_scope="HYDRO + VEX",
        bot_path="rounds/round_3/bots/amin/historical/r3_b01_delta1_optiver.py",
    ),
    "r3_b02_itm_anchor": RunMeta(
        short_id="B02-anchor",
        era="legacy",
        candidate_family="legacy itm anchor composite",
        analysis_bucket="legacy_itm_vex",
        hypothesis="ITM structural-anchor vouchers can add clean residual edge on top of the VEX anchor leg.",
        product_scope="VEX + VEV_4000-4500",
        bot_path="rounds/round_3/bots/amin/historical/r3_b02_itm_anchor.py",
    ),
    "r3_b02_itm_residual": RunMeta(
        short_id="B02-resid",
        era="legacy",
        candidate_family="legacy itm residual composite",
        analysis_bucket="legacy_itm_vex",
        hypothesis="The VEX anchor plus ITM residual branch is the cleanest voucher family available.",
        product_scope="HYDRO + VEX + VEV_4000-4500",
        bot_path="rounds/round_3/bots/amin/historical/r3_b02_itm_residual.py",
    ),
    "r3_b03_voucher_pure": RunMeta(
        short_id="B03-pure",
        era="legacy",
        candidate_family="legacy active voucher pure",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="The active voucher family can stand on its own without delta-1 support.",
        product_scope="VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/r3_b03_voucher_pure.py",
    ),
    "r3_b04_full_surface": RunMeta(
        short_id="B04-surf",
        era="legacy",
        candidate_family="legacy full surface composite",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="A broader surface-aware voucher trader plus ITM support can beat a narrower active basket.",
        product_scope="VEX + VEV_4000-5500",
        bot_path="rounds/round_3/bots/amin/historical/r3_b04_full_surface.py",
    ),
    "r3_b05_composite_advanced": RunMeta(
        short_id="B05-adv",
        era="legacy",
        candidate_family="legacy advanced composite",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="A more complex composite with stronger delta-1 execution should dominate the simpler C06 family.",
        product_scope="HYDRO + VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/r3_b05_composite_advanced.py",
    ),
    "r3_b06_tte_cautious": RunMeta(
        short_id="B06-tte",
        era="legacy",
        candidate_family="legacy tte cautious",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="TTE-aware caution should improve the active voucher residual branch near expiry.",
        product_scope="VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/r3_b06_tte_cautious.py",
    ),
    "r3_b07_delta_hedge": RunMeta(
        short_id="B07-hedge",
        era="legacy",
        candidate_family="legacy delta hedge",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="Explicit VEX hedging should stabilize the active voucher branch.",
        product_scope="VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/r3_b07_delta_hedge.py",
    ),
    "r3_b08_regime_composite": RunMeta(
        short_id="B08-regime",
        era="legacy",
        candidate_family="legacy regime composite",
        analysis_bucket="legacy_active_vouchers",
        hypothesis="Regime-aware active voucher logic should outperform a static basket.",
        product_scope="VEX + VEV_5000-5300",
        bot_path="rounds/round_3/bots/amin/historical/r3_b08_regime_composite.py",
    ),
}


def as_float(value: object) -> float:
    if value is None:
        return math.nan
    return float(value)


def markdown_table(df: pd.DataFrame, cols: list[str], float_fmt: str = "{:.3f}") -> str:
    view = df.loc[:, cols].copy()
    for col in view.columns:
        if pd.api.types.is_float_dtype(view[col]):
            view[col] = view[col].map(lambda x: "" if pd.isna(x) else float_fmt.format(float(x)))
    view = view.fillna("")
    lines = [
        "| " + " | ".join(view.columns.astype(str)) + " |",
        "| " + " | ".join(["---"] * len(view.columns)) + " |",
    ]
    for row in view.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def drawdown(series: pd.Series) -> float:
    if series.empty:
        return math.nan
    return float((series - series.cummax()).min())


def parse_embedded_csv(csv_text: str) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(csv_text), sep=";")


def summarize_path(path_df: pd.DataFrame, value_col: str) -> dict[str, object]:
    if path_df.empty:
        return {
            "path_final": math.nan,
            "path_peak": math.nan,
            "path_peak_ts": math.nan,
            "path_peak_time_frac": math.nan,
            "path_trough": math.nan,
            "path_trough_ts": math.nan,
            "path_trough_time_frac": math.nan,
            "path_max_drawdown": math.nan,
            "path_end_from_peak": math.nan,
            "path_recovery_from_trough": math.nan,
            "path_positive_time_ratio": math.nan,
            "path_nonnegative_time_ratio": math.nan,
            "path_peak_retention_ratio": math.nan,
            "path_positive_peak_negative_finish": 0,
            "path_big_peak_negative_finish": 0,
            "path_peak_after_half": 0,
            "path_shape": "unknown",
        }

    series = path_df[value_col].astype(float).reset_index(drop=True)
    timestamps = path_df["timestamp"].astype(int).reset_index(drop=True)
    final = float(series.iloc[-1])
    peak_idx = int(series.idxmax())
    trough_idx = int(series.idxmin())
    peak = float(series.iloc[peak_idx])
    trough = float(series.iloc[trough_idx])
    peak_ts = int(timestamps.iloc[peak_idx])
    trough_ts = int(timestamps.iloc[trough_idx])
    final_ts = int(timestamps.iloc[-1])
    max_drawdown = drawdown(series)
    end_from_peak = final - peak
    recovery_from_trough = final - trough
    peak_retention_ratio = final / peak if peak > 0 else math.nan
    positive_peak_negative_finish = int(peak > 100 and final < 0)
    big_peak_negative_finish = int(peak > 500 and final < 0)
    peak_after_half = int(peak_ts >= final_ts / 2) if final_ts > 0 else 0

    if final > 100 and peak > 0 and peak_retention_ratio >= 0.5:
        path_shape = "sustained_winner"
    elif final > 0 and peak > 100:
        path_shape = "winner_with_giveback"
    elif big_peak_negative_finish:
        path_shape = "edge_then_major_reversal"
    elif positive_peak_negative_finish:
        path_shape = "edge_then_reversal"
    elif peak <= 100 and final < 0:
        path_shape = "monotonic_or_no_edge_loser"
    elif abs(final) <= 25 and peak <= 100:
        path_shape = "flat_or_inconclusive"
    else:
        path_shape = "mixed_path"

    return {
        "path_final": final,
        "path_peak": peak,
        "path_peak_ts": peak_ts,
        "path_peak_time_frac": float(peak_ts / final_ts) if final_ts > 0 else math.nan,
        "path_trough": trough,
        "path_trough_ts": trough_ts,
        "path_trough_time_frac": float(trough_ts / final_ts) if final_ts > 0 else math.nan,
        "path_max_drawdown": max_drawdown,
        "path_end_from_peak": end_from_peak,
        "path_recovery_from_trough": recovery_from_trough,
        "path_positive_time_ratio": float((series > 0).mean()),
        "path_nonnegative_time_ratio": float((series >= 0).mean()),
        "path_peak_retention_ratio": peak_retention_ratio,
        "path_positive_peak_negative_finish": positive_peak_negative_finish,
        "path_big_peak_negative_finish": big_peak_negative_finish,
        "path_peak_after_half": peak_after_half,
        "path_shape": path_shape,
    }


def infer_probe_bucket(short_id: str) -> str:
    probe_num = int(short_id[1:])
    if probe_num in {1, 2, 4, 5, 6}:
        return "wave1_delta1"
    if probe_num in {7, 8, 9, 10}:
        return "wave1_itm"
    if probe_num in {12, 13, 14, 15, 16, 17, 18, 19, 20, 25}:
        return "wave1_active"
    if probe_num in {21, 22, 23, 24}:
        return "wave1_upper"
    if probe_num in {26, 27}:
        return "wave1_surface"
    return "wave1_other"


def infer_probe_scope(stem: str) -> str:
    scope: list[str] = []
    if "hydro" in stem:
        scope.append("HYDRO")
    if "vex" in stem:
        scope.append("VEX")
    if "delta1_dual_independent" in stem:
        scope.extend(["HYDRO", "VEX"])
    if "itm_pair" in stem:
        scope.extend(["VEV_4000", "VEV_4500"])
    strikes = re.findall(r"(4\d{3}|5\d{3}|6\d{3})", stem)
    for strike in strikes:
        scope.append(f"VEV_{strike}")
    if "surface" in stem and not strikes:
        scope.append("surface_pair")
    deduped = []
    for item in scope:
        if item not in deduped:
            deduped.append(item)
    return " + ".join(deduped) if deduped else "unknown"


def load_wave1_meta() -> dict[str, RunMeta]:
    rows: dict[str, RunMeta] = {}
    pattern = re.compile(
        r"^\| `(?P<short_id>L\d+)` \| `\.\./bots/amin/canonical/(?P<filename>[^`]+)` \| (?P<family>[^|]+) \| (?P<hypothesis>[^|]+) \|$"
    )
    for line in MANIFEST.read_text().splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        short_id = match.group("short_id").strip()
        filename = match.group("filename").strip()
        stem = filename[:-3]
        family = match.group("family").strip()
        hypothesis = match.group("hypothesis").strip()
        rows[stem] = RunMeta(
            short_id=short_id,
            era="wave1_probe",
            candidate_family=family,
            analysis_bucket=infer_probe_bucket(short_id),
            hypothesis=hypothesis,
            product_scope=infer_probe_scope(stem),
            bot_path=f"rounds/round_3/bots/amin/historical/{filename}",
        )
    return rows


def load_meta() -> dict[str, RunMeta]:
    meta = dict(MANUAL_RUN_META)
    meta.update(load_wave1_meta())
    return meta


def final_product_pnl(activities: pd.DataFrame) -> dict[str, float]:
    rows = activities.sort_values("timestamp").groupby("product", as_index=False).tail(1)
    return {str(row["product"]): float(row["profit_and_loss"]) for _, row in rows.iterrows()}


def parse_positions(data: dict) -> dict[str, int]:
    positions: dict[str, int] = {}
    for item in data.get("positions", []):
        if isinstance(item, dict):
            positions[str(item.get("symbol"))] = int(item.get("quantity", 0))
    return positions


def load_trade_metrics(stem: str) -> tuple[dict[str, object], list[dict[str, object]]]:
    log_path = PERF_HIST / f"{stem}.log"
    if not log_path.exists() or log_path.stat().st_size == 0:
        return {
            "own_trades": 0,
            "buy_qty": 0,
            "sell_qty": 0,
            "exec_symbols": "",
            "max_abs_exec_position": math.nan,
        }, []
    data = json.loads(log_path.read_text())
    trade_history = data.get("tradeHistory", [])
    own_trades = [
        trade
        for trade in trade_history
        if trade.get("buyer") == "SUBMISSION" or trade.get("seller") == "SUBMISSION"
    ]
    positions: dict[str, int] = {}
    max_abs_by_symbol: dict[str, int] = {}
    per_symbol_rows: list[dict[str, object]] = []
    for trade in own_trades:
        symbol = str(trade["symbol"])
        signed_qty = int(trade["quantity"])
        if trade.get("seller") == "SUBMISSION":
            signed_qty *= -1
        positions[symbol] = positions.get(symbol, 0) + signed_qty
        max_abs_by_symbol[symbol] = max(max_abs_by_symbol.get(symbol, 0), abs(positions[symbol]))
        per_symbol_rows.append(
            {
                "stem": stem,
                "symbol": symbol,
                "timestamp": int(trade["timestamp"]),
                "signed_qty": signed_qty,
                "price": float(trade["price"]),
            }
        )
    return (
        {
            "own_trades": len(own_trades),
            "buy_qty": int(sum(trade["quantity"] for trade in own_trades if trade.get("buyer") == "SUBMISSION")),
            "sell_qty": int(sum(trade["quantity"] for trade in own_trades if trade.get("seller") == "SUBMISSION")),
            "exec_symbols": ",".join(sorted({str(trade["symbol"]) for trade in own_trades})),
            "max_abs_exec_position": max(max_abs_by_symbol.values(), default=0),
        },
        per_symbol_rows,
    )


def learning_verdict(profit: float) -> str:
    if profit > 500:
        return "strong positive"
    if profit > 100:
        return "positive"
    if profit > -25:
        return "near flat"
    if profit > -500:
        return "mild negative"
    if profit > -2000:
        return "negative"
    return "strong negative"


def analyze() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    meta = load_meta()
    run_rows: list[dict[str, object]] = []
    product_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []
    exec_trade_rows: list[dict[str, object]] = []
    linkage_rows: list[dict[str, object]] = []

    for json_path in sorted(PERF_HIST.glob("*.json")):
        stem = json_path.stem
        if stem not in meta:
            raise KeyError(f"Missing run metadata for {stem}")

        run_meta = meta[stem]
        data = json.loads(json_path.read_text())
        activities = parse_embedded_csv(data["activitiesLog"])
        graph = parse_embedded_csv(data["graphLog"])
        activity_path = (
            activities.groupby("timestamp", as_index=False)["profit_and_loss"].sum()
            .rename(columns={"profit_and_loss": "total_pnl"})
            .sort_values("timestamp")
        )
        path_metrics = summarize_path(activity_path, "total_pnl")
        positions = parse_positions(data)
        product_pnl = final_product_pnl(activities)
        trade_metrics, trade_rows = load_trade_metrics(stem)
        exec_trade_rows.extend(trade_rows)

        profit_value = as_float(data.get("profit", math.nan))
        if math.isnan(profit_value):
            profit_value = float(sum(product_pnl.values()))

        run_row = {
            "stem": stem,
            "short_id": run_meta.short_id,
            "era": run_meta.era,
            "candidate_family": run_meta.candidate_family,
            "analysis_bucket": run_meta.analysis_bucket,
            "hypothesis": run_meta.hypothesis,
            "product_scope": run_meta.product_scope,
            "bot_path": run_meta.bot_path,
            "profit": profit_value,
            "activities_sum": float(sum(product_pnl.values())),
            "graph_final": float(graph["value"].iloc[-1]),
            "max_drawdown": drawdown(graph["value"]),
            "graph_min": float(graph["value"].min()),
            "graph_max": float(graph["value"].max()),
            **path_metrics,
            "delta1_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in DELTA1_PRODUCTS)),
            "itm_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ITM_PRODUCTS)),
            "active_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ACTIVE_PRODUCTS)),
            "upper_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in UPPER_PRODUCTS)),
            "floor_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in FLOOR_PRODUCTS)),
            "active_limit_hits": int(sum(abs(positions.get(symbol, 0)) == 300 for symbol in ACTIVE_PRODUCTS)),
            "upper_limit_hits": int(sum(abs(positions.get(symbol, 0)) == 300 for symbol in UPPER_PRODUCTS)),
            "learning_verdict": learning_verdict(profit_value),
            **trade_metrics,
        }

        for symbol in ALL_PRODUCTS:
            run_row[f"pnl_{symbol}"] = float(product_pnl.get(symbol, 0.0))
            run_row[f"pos_{symbol}"] = int(positions.get(symbol, 0))
            product_rows.append(
                {
                    "stem": stem,
                    "short_id": run_meta.short_id,
                    "analysis_bucket": run_meta.analysis_bucket,
                    "candidate_family": run_meta.candidate_family,
                    "product": symbol,
                    "profit_and_loss": float(product_pnl.get(symbol, 0.0)),
                    "final_position": int(positions.get(symbol, 0)),
                }
            )

        linkage_rows.append(
            {
                "short_id": run_meta.short_id,
                "stem": stem,
                "era": run_meta.era,
                "candidate_family": run_meta.candidate_family,
                "analysis_bucket": run_meta.analysis_bucket,
                "product_scope": run_meta.product_scope,
                "hypothesis": run_meta.hypothesis,
                "profit": run_row["profit"],
                "learning_verdict": run_row["learning_verdict"],
                "bot_path": run_meta.bot_path,
            }
        )

        execution_rows.append(
            {
                "stem": stem,
                "short_id": run_meta.short_id,
                "analysis_bucket": run_meta.analysis_bucket,
                "candidate_family": run_meta.candidate_family,
                "profit": run_row["profit"],
                "own_trades": trade_metrics["own_trades"],
                "buy_qty": trade_metrics["buy_qty"],
                "sell_qty": trade_metrics["sell_qty"],
                "max_abs_exec_position": trade_metrics["max_abs_exec_position"],
                "exec_symbols": trade_metrics["exec_symbols"],
                "path_peak": run_row["path_peak"],
                "path_peak_ts": run_row["path_peak_ts"],
                "path_end_from_peak": run_row["path_end_from_peak"],
                "path_positive_time_ratio": run_row["path_positive_time_ratio"],
                "path_shape": run_row["path_shape"],
                "active_limit_hits": run_row["active_limit_hits"],
                "upper_limit_hits": run_row["upper_limit_hits"],
                "final_active_position_abs": int(sum(abs(positions.get(symbol, 0)) for symbol in ACTIVE_PRODUCTS)),
                "final_upper_position_abs": int(sum(abs(positions.get(symbol, 0)) for symbol in UPPER_PRODUCTS)),
            }
        )

        run_rows.append(run_row)

    run_df = pd.DataFrame(run_rows).sort_values("profit", ascending=False)
    product_df = pd.DataFrame(product_rows)
    execution_df = pd.DataFrame(execution_rows).sort_values("profit", ascending=False)
    trade_df = pd.DataFrame(exec_trade_rows)
    linkage_df = pd.DataFrame(linkage_rows).sort_values("profit", ascending=False)
    return run_df, product_df, execution_df, trade_df, linkage_df


def build_family_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        run_df.groupby("analysis_bucket", as_index=False)
        .agg(
            runs=("stem", "count"),
            mean_profit=("profit", "mean"),
            median_profit=("profit", "median"),
            best_profit=("profit", "max"),
            worst_profit=("profit", "min"),
            mean_delta1=("delta1_total", "mean"),
            mean_itm=("itm_total", "mean"),
            mean_active=("active_total", "mean"),
            mean_upper=("upper_total", "mean"),
            mean_own_trades=("own_trades", "mean"),
        )
        .sort_values("mean_profit", ascending=False)
    )
    return summary


def build_path_family_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        run_df.groupby("analysis_bucket", as_index=False)
        .agg(
            runs=("stem", "count"),
            mean_final_profit=("profit", "mean"),
            mean_path_peak=("path_peak", "mean"),
            median_path_peak=("path_peak", "median"),
            mean_end_from_peak=("path_end_from_peak", "mean"),
            mean_path_max_drawdown=("path_max_drawdown", "mean"),
            mean_positive_time_ratio=("path_positive_time_ratio", "mean"),
            positive_peak_negative_finish_rate=("path_positive_peak_negative_finish", "mean"),
            big_peak_negative_finish_rate=("path_big_peak_negative_finish", "mean"),
            late_peak_rate=("path_peak_after_half", "mean"),
        )
        .sort_values("mean_path_peak", ascending=False)
    )
    return summary


def build_path_reversal_table(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_peak_ts",
        "path_end_from_peak",
        "path_positive_time_ratio",
        "path_shape",
    ]
    return run_df[
        (run_df["path_peak"] > 100) & (run_df["profit"] < 0)
    ].sort_values(["path_end_from_peak", "path_peak"], ascending=[True, False]).loc[:, cols]


def build_product_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for product in ALL_PRODUCTS:
        pnl_col = f"pnl_{product}"
        nonzero = run_df[run_df[pnl_col].abs() > 1e-9]
        wave1 = run_df[(run_df["era"] == "wave1_probe") & (run_df[pnl_col].abs() > 1e-9)]
        rows.append(
            {
                "product": product,
                "nonzero_runs": int(nonzero.shape[0]),
                "positive_runs": int((nonzero[pnl_col] > 0).sum()),
                "negative_runs": int((nonzero[pnl_col] < 0).sum()),
                "mean_pnl": float(nonzero[pnl_col].mean()) if not nonzero.empty else math.nan,
                "median_pnl": float(nonzero[pnl_col].median()) if not nonzero.empty else math.nan,
                "best_pnl": float(nonzero[pnl_col].max()) if not nonzero.empty else math.nan,
                "worst_pnl": float(nonzero[pnl_col].min()) if not nonzero.empty else math.nan,
                "wave1_nonzero_runs": int(wave1.shape[0]),
                "wave1_positive_runs": int((wave1[pnl_col] > 0).sum()),
                "wave1_negative_runs": int((wave1[pnl_col] < 0).sum()),
                "wave1_mean_pnl": float(wave1[pnl_col].mean()) if not wave1.empty else math.nan,
            }
        )
    return pd.DataFrame(rows).sort_values("product")


def build_wave1_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "candidate_family",
        "product_scope",
        "profit",
        "delta1_total",
        "itm_total",
        "active_total",
        "upper_total",
        "path_peak",
        "path_end_from_peak",
        "path_shape",
        "own_trades",
        "max_abs_exec_position",
        "active_limit_hits",
        "upper_limit_hits",
        "learning_verdict",
    ]
    return run_df[run_df["era"] == "wave1_probe"].sort_values("profit", ascending=False).loc[:, cols]


def render_report(
    run_df: pd.DataFrame,
    family_df: pd.DataFrame,
    path_family_df: pd.DataFrame,
    product_df: pd.DataFrame,
    execution_df: pd.DataFrame,
    linkage_df: pd.DataFrame,
    wave1_df: pd.DataFrame,
    reversal_df: pd.DataFrame,
) -> str:
    total_runs = int(run_df.shape[0])
    wave1_runs = int((run_df["era"] == "wave1_probe").sum())
    log_runs = int((execution_df["own_trades"] > 0).sum())
    best_row = run_df.iloc[0]
    best_wave1 = wave1_df.iloc[0]
    best_voucher_only = wave1_df[
        (wave1_df["delta1_total"].abs() < 1e-9) & (wave1_df["profit"] > 0)
    ]
    best_voucher_only_text = (
        "No pure voucher-only Wave 1 learner finished positive."
        if best_voucher_only.empty
        else f"Best pure voucher-only learner: {best_voucher_only.iloc[0]['short_id']} at {best_voucher_only.iloc[0]['profit']:.3f}."
    )
    path_positive_peak_negative = int(run_df["path_positive_peak_negative_finish"].sum())
    path_big_peak_negative = int(run_df["path_big_peak_negative_finish"].sum())
    path_late_peak_negative = int(
        ((run_df["path_positive_peak_negative_finish"] == 1) & (run_df["path_peak_after_half"] == 1)).sum()
    )

    top_overall = run_df.head(12)
    worst_overall = run_df.tail(10)
    reversal_focus = reversal_df.head(12)

    delta1_live = family_df[family_df["analysis_bucket"] == "wave1_delta1"].iloc[0]
    itm_live = family_df[family_df["analysis_bucket"] == "wave1_itm"].iloc[0]
    active_live = family_df[family_df["analysis_bucket"] == "wave1_active"].iloc[0]
    upper_live = family_df[family_df["analysis_bucket"] == "wave1_upper"].iloc[0]
    surface_live = family_df[family_df["analysis_bucket"] == "wave1_surface"].iloc[0]
    delta1_path = path_family_df[path_family_df["analysis_bucket"] == "wave1_delta1"].iloc[0]
    active_path = path_family_df[path_family_df["analysis_bucket"] == "wave1_active"].iloc[0]
    surface_path = path_family_df[path_family_df["analysis_bucket"] == "wave1_surface"].iloc[0]

    key_products = product_df[
        product_df["product"].isin(
            [
                "HYDROGEL_PACK",
                "VELVETFRUIT_EXTRACT",
                "VEV_4000",
                "VEV_4500",
                "VEV_5000",
                "VEV_5100",
                "VEV_5200",
                "VEV_5300",
                "VEV_5400",
                "VEV_5500",
                "VEV_6000",
                "VEV_6500",
            ]
        )
    ]

    execution_focus = execution_df[
        execution_df["stem"].isin(
            [
                "probe_l06_delta1_dual_independent",
                "probe_l10_itm_pair_plus_vex",
                "probe_l15_active_5300_residual",
                "probe_l20_active_5000_5300_inventory",
                "probe_l24_upper_5400_5500_passive",
                "probe_l26_surface_5200_5300_relval",
            ]
        )
    ].sort_values("profit", ascending=False)

    report = f"""# Round 3 Full Performance Synthesis

## Executive Verdict

This report consolidates **all current Round 3 evidence**: EDA, understanding,
legacy historical runs, corrected challenger runs, and the full 25-bot Wave 1
learning batch.

- Total platform JSON artifacts analyzed: `{total_runs}`.
- Wave 1 learner JSON artifacts analyzed: `{wave1_runs}`.
- Runs with usable `tradeHistory` execution detail from `.log`: `{log_runs}`.
- Best overall tested run remains `{best_row['short_id']}` / `{best_row['stem']}.json` at real platform PnL `{best_row['profit']:.3f}`.
- Best Wave 1 learner is `{best_wave1['short_id']}` / `{best_wave1['stem']}.json` at `{best_wave1['profit']:.3f}`.
- {best_voucher_only_text}

### Bottom Line

1. **The strongest live family is now clean delta-1 microstructure**, not broad
   voucher composites.
2. **Pure voucher-only Wave 1 learners did not produce a winner**. The best
   active standalone strike (`VEV_5300`) was only near-flat, not positive.
3. **`VEV_5100` and `VEV_5200` are now the clearest toxic strikes** in live
   standalone testing.
4. **Inventory control is not dead**, but it only helped on a cleaner subset
   (`VEV_5000 + VEV_5300`), not on the broad active basket.
5. **The old “HYDRO is weak” conclusion was too pessimistic**. HYDRO failed in
   earlier composite implementations, but isolated HYDRO learners turned
   clearly positive.

## Coverage Audit

- Historical / corrected / learner evidence now spans legacy delta-1, legacy
  ITM/VEX, legacy active vouchers, corrected centered composites, Wave 1
  delta-1 probes, Wave 1 ITM probes, Wave 1 active-subset probes, Wave 1
  upper probes, and Wave 1 surface probes.
- `activitiesLog` final product sums remain the best practical PnL
  reconstruction when JSON `profit` is unavailable.
- For path analysis, this report now uses **timestamp-level PnL reconstructed
  from `activitiesLog`**, not just final-run outcomes or the coarser
  `graphLog`.
- `.log` files for the Wave 1 learners are not empty; they contain a full
  single-line JSON blob with `tradeHistory`, which is useful for fill and
  inventory diagnostics.

## Path Quality Summary

- Runs with a positive intra-run peak above `100` that still finished negative:
  `{path_positive_peak_negative}` / `{total_runs}`.
- Runs with a strong intra-run peak above `500` that still finished negative:
  `{path_big_peak_negative}` / `{total_runs}`.
- Of those reversal runs, `{path_late_peak_negative}` peaked in the **second
  half** of the session before giving the gains back.

{markdown_table(path_family_df, ['analysis_bucket', 'runs', 'mean_final_profit', 'mean_path_peak', 'median_path_peak', 'mean_end_from_peak', 'mean_path_max_drawdown', 'mean_positive_time_ratio', 'positive_peak_negative_finish_rate', 'big_peak_negative_finish_rate', 'late_peak_rate'])}

### Reading The Path Table

- `wave1_delta1` is not just positive at the close; it also has strong
  intraday quality: mean peak `{delta1_path['mean_path_peak']:.3f}` and mean
  positive-time ratio `{delta1_path['mean_positive_time_ratio']:.3f}`.
- `wave1_active` is more nuanced than “always dead”: mean peak
  `{active_path['mean_path_peak']:.3f}`, but mean giveback from peak
  `{active_path['mean_end_from_peak']:.3f}`. That is a **real reversal /
  unwind problem**, not just zero edge.
- `wave1_surface` is different: mean peak only `{surface_path['mean_path_peak']:.3f}`
  and almost no time spent positive. That branch looks structurally wrong in
  the current implementation, not merely badly closed out.

## Biggest Mid-Run Reversals

These runs matter because they may still contain signal even though they
finished badly.

{markdown_table(reversal_focus, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_peak_ts', 'path_end_from_peak', 'path_positive_time_ratio', 'path_shape'])}

### Reversal Reading

- Several legacy voucher/composite bots and several Wave 1 active learners made
  meaningful money mid-run before collapsing.
- `probe_l12_active_5000_residual` and `probe_l15_active_5300_residual` are
  examples of the “edge then reversal” pattern; they are not in the same
  category as `probe_l26_surface_5200_5300_relval`, which showed almost no
  positive path at all.
- This means the next design step should distinguish:
  - branches with **monetizable entry signal but broken hold / exit / sizing**
  - branches with **no evidence of usable signal**

## Overall Ranking

### Top 12 Runs By Real Platform PnL

{markdown_table(top_overall, ['short_id', 'stem', 'analysis_bucket', 'profit', 'delta1_total', 'itm_total', 'active_total', 'upper_total', 'learning_verdict'])}

### Worst 10 Runs By Real Platform PnL

{markdown_table(worst_overall, ['short_id', 'stem', 'analysis_bucket', 'profit', 'delta1_total', 'itm_total', 'active_total', 'upper_total', 'learning_verdict'])}

## Strategy / Bot / Performance Linkage

This table links each saved performance artifact back to the bot family and the
main hypothesis it was testing.

{markdown_table(linkage_df.sort_values(['era', 'profit'], ascending=[True, False]), ['short_id', 'stem', 'era', 'candidate_family', 'product_scope', 'profit', 'learning_verdict'])}

## Family Summary

{markdown_table(family_df, ['analysis_bucket', 'runs', 'mean_profit', 'median_profit', 'best_profit', 'worst_profit', 'mean_delta1', 'mean_itm', 'mean_active', 'mean_upper', 'mean_own_trades'])}

### Reading The Family Table

- `wave1_delta1` is decisively positive: mean PnL `{delta1_live['mean_profit']:.3f}`.
- `wave1_itm` is basically flat to slightly negative on its own: mean PnL `{itm_live['mean_profit']:.3f}`.
- `wave1_active` is still clearly negative even after strike isolation: mean PnL `{active_live['mean_profit']:.3f}`.
- `wave1_upper` is negative in directional residual form: mean PnL `{upper_live['mean_profit']:.3f}`.
- `wave1_surface` is the weakest new experimental family after the toxic active strikes: mean PnL `{surface_live['mean_profit']:.3f}`.

## EDA / Understanding Scorecard

| Original EDA / Understanding Claim | Current Verdict From Runs | Evidence |
| --- | --- | --- |
| `HYDROGEL_PACK` should be treated as a separate branch. | validated strongly | `L01 = +556.031`, `L02 = +537.656`, `L06` also positive; hydro weakness was not a product-level death sentence. |
| `VELVETFRUIT_EXTRACT` is the natural anchor and a tradable standalone delta-1 product. | validated strongly | `L04 = +309.613`, `L05 = +446.387`, `L06 = +886.102`; VEX is also positive inside the corrected challengers and `L25`. |
| `VEV_5000-5300` is the best first-wave active option scope. | weakened / contradicted | No pure active Wave 1 learner finished positive; `L15` (`VEV_5300`) was the least bad at `-216.604`, while `VEV_5100` and `VEV_5200` were disastrous. |
| `VEV_4000/4500` should be useful but were not first-wave execution leaders. | partially validated | Pure ITM probes were near-flat (`L07`, `L08`, `L09`), not winners; the positive live result is `L10`, but that comes mostly from the VEX leg. |
| `VEV_5400/5500` are execution-sensitive and should only be reopened carefully. | validated with caution | Directional residual upper bots lost money (`L21`, `L22`, `L23`); passive upper (`L24`) produced zero trades and zero PnL. |
| `VEV_6000/6500` should stay excluded. | validated strongly | Logger still shows the floor regime, and no profitable evidence has emerged there. |
| Surface-relative features may help when absolute residual is noisy. | not validated in current implementation | `L26 = -10739.712`, `L27 = -989.622`; local surface spreads are not rescuing the voucher branch in their current form. |

## Branch-by-Branch Analysis

### 1. Delta-1 Branch: Best Live Learning Outcome

Wave 1 changed the picture materially:

- `L01` (`HYDRO` reversion) finished at `+556.031`.
- `L02` (`HYDRO` imbalance) finished at `+537.656`.
- `L04` (`VEX` reversion) finished at `+309.613`.
- `L05` (`VEX` imbalance) finished at `+446.387`.
- `L06` (`HYDRO + VEX`) finished at `+886.102`.

Interpretation:

- The clean isolated delta-1 logic works much better than the old legacy pair
  makers.
- HYDRO is not rejected; the earlier negative evidence was mostly about
  implementation style and composite interactions.
- VEX remains useful both as a standalone edge and as the best anchor leg for
  any later voucher strategy.

### 2. ITM Branch: Low-Risk Add-On, Not Yet A Standalone Winner

Wave 1 ITM results:

- `L07` (`VEV_4000`) = `-3.155`
- `L08` (`VEV_4500`) = `-3.155`
- `L09` (`VEV_4000 + VEV_4500`) = `-6.310`
- `L10` (`VEX + VEV_4000 + VEV_4500`) = `+326.151`

Interpretation:

- Pure ITM residual trading is basically flat on the live `TTE=5d` day.
- The historical ITM/VEX winners were already mostly delta-1 driven:
  `B02-resid` had `delta1 = +1211.906` versus `itm = +197.464`;
  `B02-anchor` had `delta1 = +599.500` versus `itm = +127.393`.
- This means ITM is still useful, but more as a **low-damage optional add-on**
  than as the main alpha engine.

### 3. Active Voucher Branch: Still The Main Problem Area

Wave 1 active-only results:

- `L12` (`VEV_5000`) = `-1715.952`
- `L13` (`VEV_5100`) = `-6956.580`
- `L14` (`VEV_5200`) = `-5900.712`
- `L15` (`VEV_5300`) = `-216.604`
- `L16` (`VEV_5000 + VEV_5300`) = `-1837.049`
- `L17` (`VEV_5100 + VEV_5300`) = `-7620.939`
- `L18` (`VEV_5200 + VEV_5300`) = `-6078.315`
- `L19` (`VEV_5000 + VEV_5100 + VEV_5300`) = `-9241.385`
- `L20` (`VEV_5000 + VEV_5300` + inventory) = `-1443.986`
- `L25` (`VEX + VEV_5300`) = `+115.857`, with the VEX leg contributing `+332.461` and the `VEV_5300` leg `-216.604`.

Interpretation:

- `VEV_5100` and `VEV_5200` should now be treated as default rejects until
  very strong contradictory evidence appears.
- `VEV_5300` is still the **least-bad** active strike and looks useful in
  relative terms, but it is not a standalone positive alpha yet.
- `VEV_5000` is not good, but it is materially less toxic than `VEV_5100` /
  `VEV_5200`.
- Inventory helped once the basket was cleaned:
  `L20` beat `L16` by about `393.063`, even though the broad C06 inventory
  overlay had previously failed.

### 4. Upper Strikes: Reopened, But Not Yet Monetized

Wave 1 upper results:

- `L21` (`VEV_5400`) = `-446.830`
- `L22` (`VEV_5500`) = `-320.792`
- `L23` (`VEV_5400 + VEV_5500`) = `-767.622`
- `L24` (passive `VEV_5400 + VEV_5500`) = `0.000` with `0` own trades

Interpretation:

- The logger was right that these strikes move and have tight spreads.
- But that did **not** translate into profitable directional residual trading.
- Passive-only execution avoided loss, but also got no fills.
- The upper branch is therefore still open as a research branch, but it is
  not close to promotion.

### 5. Surface Relative Value: Useful Diagnostic, Bad Current Trader

Wave 1 surface results:

- `L26` (`VEV_5200 vs VEV_5300`) = `-10739.712`
- `L27` (`VEV_5300 vs VEV_5400`) = `-989.622`

Interpretation:

- `L26` is especially informative: final positions were small, but the PnL was
  catastrophically negative, which points to **realized adverse selection /
  signal error**, not just terminal inventory mark.
- `L27` is less bad, and the `VEV_5300` side was actually positive, but the
  `VEV_5400` side dominated the loss.
- So the current surface-pair implementation should be treated as a diagnostic
  failure mode, not as a candidate family to scale immediately.

## Product-Level Realized Summary

{markdown_table(key_products, ['product', 'nonzero_runs', 'positive_runs', 'negative_runs', 'mean_pnl', 'best_pnl', 'worst_pnl', 'wave1_nonzero_runs', 'wave1_positive_runs', 'wave1_negative_runs', 'wave1_mean_pnl'])}

### Product-Level Reading

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` now have real positive standalone
  evidence in Wave 1.
- `VEV_4000` / `VEV_4500` are low-damage, low-fill, near-flat live products.
- `VEV_5000` is weak but not hopeless.
- `VEV_5100` and `VEV_5200` are the strongest current negative evidence in the
  voucher family.
- `VEV_5300` is viable only as a relative or combo leg for now, not as a
  standalone winner.
- `VEV_5400/5500` are tradable enough to test, but not yet good enough to
  promote.

## Execution Diagnostics From `tradeHistory`

{markdown_table(execution_focus, ['short_id', 'stem', 'profit', 'own_trades', 'buy_qty', 'sell_qty', 'max_abs_exec_position', 'active_limit_hits', 'upper_limit_hits', 'final_active_position_abs', 'final_upper_position_abs', 'exec_symbols'])}

### Execution Reading

- Delta-1 winners (`L01`, `L02`, `L04`, `L05`, `L06`) achieved positive PnL
  with relatively low trade counts. That is a good sign for signal cleanliness.
- The active learners often traded **a lot** and still lost badly. This pushes
  the diagnosis toward signal quality / selection problems, not simple lack of
  fills.
- `L15` (`VEV_5300`) traded heavily and still only lost `-216.604`, which is
  why it remains the best active-strike survivor.
- `L24` confirms that the upper passive branch, in its current form, is too
  timid to get matched.

## What Worked

- Clean delta-1 microstructure on both `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`.
- VEX as a sidecar / anchor leg in mixed bots.
- Using inventory as a secondary cleaner on a reduced active subset.
- Excluding `VEV_6000/6500`; nothing in the new evidence argues for reopening them.
- Identifying that some active-voucher bots do have **mid-run edge**, even if
  they currently fail to retain it.

## What Did Not Work

- Broad active voucher baskets, even after centered-residual correction.
- `VEV_5100` and `VEV_5200` as default active strikes.
- Treating `VEV_5300` as a standalone promoted winner just because it was the
  least-bad strike inside earlier composites.
- Directional upper-strike residual trading.
- Current surface-pair implementations.
- Interpreting every negative final run as “no signal”; the path analysis now
  shows that this was too crude for several active-voucher experiments.

## What We Still Do Not Know

- Whether the best next bot should be **delta-1 only** or **delta-1 plus a very
  selective voucher add-on**.
- Whether ITM is worth keeping as a low-risk add-on once execution is tuned, or
  whether VEX alone captures most of that upside more simply.
- Whether `VEV_5000 + VEV_5300` can become viable with better anchoring,
  tighter execution, or stronger inventory discipline.
- Whether the upper branch can ever do better than zero-fill passive quoting
  without becoming structurally lossy.
- Whether the best way to rescue selective active vouchers is with **shorter
  holding periods / faster profit capture** rather than better long-horizon
  fair value estimates.

## Recommended Questions Before Wave 2 Strategy Design

These are **analysis-driven next questions**, not yet implementation orders.

1. Should the next champion family be delta-1 first, with vouchers demoted to optional add-ons?
2. Is the right voucher follow-up a `VEX + 5000/5300` style combo rather than any pure voucher basket?
3. Should `VEV_5100` and `VEV_5200` now be formally moved from “active scope” to “excluded unless rescued”?
4. Is ITM best framed as an execution-light addon rather than a main branch?
5. Does the next surface work need a different execution style entirely, or should that branch be paused?

## Artifacts

- [`artifacts/full_synthesis/full_run_metrics.csv`](artifacts/full_synthesis/full_run_metrics.csv)
- [`artifacts/full_synthesis/full_path_family_summary.csv`](artifacts/full_synthesis/full_path_family_summary.csv)
- [`artifacts/full_synthesis/full_path_reversal_candidates.csv`](artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`artifacts/full_synthesis/full_product_attribution.csv`](artifacts/full_synthesis/full_product_attribution.csv)
- [`artifacts/full_synthesis/full_family_summary.csv`](artifacts/full_synthesis/full_family_summary.csv)
- [`artifacts/full_synthesis/full_execution_metrics.csv`](artifacts/full_synthesis/full_execution_metrics.csv)
- [`artifacts/full_synthesis/full_strategy_run_mapping.csv`](artifacts/full_synthesis/full_strategy_run_mapping.csv)
- [`artifacts/full_synthesis/full_wave1_probe_summary.csv`](artifacts/full_synthesis/full_wave1_probe_summary.csv)

## Handoff

- This synthesis supersedes the earlier “waiting for Wave 1 runs” state.
- The next useful step is **not another blind run batch**. It is to redesign
  the next strategy wave using this evidence, especially the delta-1 recovery
  and the voucher-family split between survivable and toxic strikes.
"""
    return report


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    run_df, product_df, execution_df, trade_df, linkage_df = analyze()
    family_df = build_family_summary(run_df)
    path_family_df = build_path_family_summary(run_df)
    reversal_df = build_path_reversal_table(run_df)
    product_summary_df = build_product_summary(run_df)
    wave1_df = build_wave1_summary(run_df)

    run_df.to_csv(ARTIFACTS / "full_run_metrics.csv", index=False)
    path_family_df.to_csv(ARTIFACTS / "full_path_family_summary.csv", index=False)
    reversal_df.to_csv(ARTIFACTS / "full_path_reversal_candidates.csv", index=False)
    product_df.to_csv(ARTIFACTS / "full_product_attribution.csv", index=False)
    family_df.to_csv(ARTIFACTS / "full_family_summary.csv", index=False)
    execution_df.to_csv(ARTIFACTS / "full_execution_metrics.csv", index=False)
    linkage_df.to_csv(ARTIFACTS / "full_strategy_run_mapping.csv", index=False)
    wave1_df.to_csv(ARTIFACTS / "full_wave1_probe_summary.csv", index=False)
    if not trade_df.empty:
        trade_df.to_csv(ARTIFACTS / "full_own_trade_timeline.csv", index=False)

    REPORT.write_text(
        render_report(
            run_df,
            family_df,
            path_family_df,
            product_summary_df,
            execution_df,
            linkage_df,
            wave1_df,
            reversal_df,
        )
    )


if __name__ == "__main__":
    main()
