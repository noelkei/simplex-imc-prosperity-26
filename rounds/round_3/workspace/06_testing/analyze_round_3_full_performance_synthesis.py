from __future__ import annotations

import bisect
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
WAVE1_MANIFEST = WORKSPACE / "05_implementation" / "learning_batch_wave1_manifest.md"
WAVE2_MANIFEST = WORKSPACE / "05_implementation" / "learning_batch_wave2_manifest.md"
WAVE3_MANIFEST = WORKSPACE / "05_implementation" / "learning_batch_wave3_manifest.md"
WAVE4_MANIFEST = WORKSPACE / "05_implementation" / "learning_batch_wave4_manifest.md"
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
MARKOUT_HORIZONS = [1000, 5000, 10000]


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


def nearest_value_at_or_after(path_df: pd.DataFrame, target_ts: int, value_col: str) -> float:
    timestamps = path_df["timestamp"].astype(int).tolist()
    idx = bisect.bisect_left(timestamps, target_ts)
    if idx >= len(timestamps):
        idx = len(timestamps) - 1
    return float(path_df.iloc[idx][value_col])


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
            "path_peak_over_5k": 0,
            "path_peak_over_10k": 0,
            "path_peak_over_15k": 0,
            "path_shape": "unknown",
            "path_q25": math.nan,
            "path_q50": math.nan,
            "path_q75": math.nan,
            "path_q90": math.nan,
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
        "path_peak_over_5k": int(peak > 5000),
        "path_peak_over_10k": int(peak > 10000),
        "path_peak_over_15k": int(peak > 15000),
        "path_shape": path_shape,
        "path_q25": nearest_value_at_or_after(path_df, int(final_ts * 0.25), value_col),
        "path_q50": nearest_value_at_or_after(path_df, int(final_ts * 0.50), value_col),
        "path_q75": nearest_value_at_or_after(path_df, int(final_ts * 0.75), value_col),
        "path_q90": nearest_value_at_or_after(path_df, int(final_ts * 0.90), value_col),
    }


def infer_wave1_bucket(short_id: str) -> str:
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


def infer_wave2_bucket(short_id: str) -> str:
    probe_num = int(short_id.split("-")[1])
    if probe_num in {1, 2, 4}:
        return "wave2_delta1_controls"
    if probe_num in {3}:
        return "wave2_itm_passive"
    if probe_num in {5, 6}:
        return "wave2_active_clean_retests"
    if probe_num in {7, 8, 9, 10, 11, 12, 13}:
        return "wave2_active_rescue"
    if probe_num in {14, 18}:
        return "wave2_upper_refinement"
    if probe_num in {15, 16}:
        return "wave2_toxic_rescue"
    if probe_num in {17}:
        return "wave2_active_upper_bridge"
    if probe_num in {19}:
        return "wave2_floor_probe"
    return "wave2_other"


def infer_wave3_bucket(short_id: str) -> str:
    probe_num = int(short_id.split("-")[1])
    if probe_num in {1, 2, 15}:
        return "wave3_delta1_controls"
    if probe_num in {3, 23, 24}:
        return "wave3_itm_and_stacks"
    if probe_num in {4, 5, 6, 7, 8, 9, 10, 11, 16, 17, 18, 19}:
        return "wave3_active_rescue_and_filters"
    if probe_num in {12, 13, 14}:
        return "wave3_inverse_tiny"
    if probe_num in {20, 21, 22}:
        return "wave3_inverse_sidecars"
    return "wave3_other"


def infer_wave4_bucket(short_id: str) -> str:
    probe_num = int(short_id.split("-")[1])
    if probe_num in {1, 2, 11}:
        return "wave4_delta1_finalists"
    if probe_num in {3, 4}:
        return "wave4_itm_finalists"
    if probe_num in {5, 6, 7, 12}:
        return "wave4_5300_finalists"
    if probe_num in {8, 9}:
        return "wave4_peak_salvage"
    if probe_num in {10}:
        return "wave4_inverse_closure"
    return "wave4_other"


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
    deduped: list[str] = []
    for item in scope:
        if item not in deduped:
            deduped.append(item)
    return " + ".join(deduped) if deduped else "unknown"


def load_wave1_meta() -> dict[str, RunMeta]:
    rows: dict[str, RunMeta] = {}
    pattern = re.compile(
        r"^\| `(?P<short_id>L\d+)` \| `\.\./bots/amin/canonical/(?P<filename>[^`]+)` \| (?P<family>[^|]+) \| (?P<hypothesis>[^|]+) \|$"
    )
    for line in WAVE1_MANIFEST.read_text().splitlines():
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
            analysis_bucket=infer_wave1_bucket(short_id),
            hypothesis=hypothesis,
            product_scope=infer_probe_scope(stem),
            bot_path=f"rounds/round_3/bots/amin/historical/{filename}",
        )
    return rows


def load_wave2_meta() -> dict[str, RunMeta]:
    rows: dict[str, RunMeta] = {}
    pattern = re.compile(
        r"^\| `(?P<short_id>W2-\d+)` \| `\.\./bots/amin/canonical/(?P<filename>[^`]+)` \| (?P<family>[^|]+) \| (?P<products>[^|]+) \| (?P<axes>[^|]+) \| (?P<hypothesis>[^|]+) \|$"
    )
    for line in WAVE2_MANIFEST.read_text().splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        short_id = match.group("short_id").strip()
        filename = match.group("filename").strip()
        stem = filename[:-3]
        family = match.group("family").strip()
        products = match.group("products").strip()
        hypothesis = match.group("hypothesis").strip()
        rows[stem] = RunMeta(
            short_id=short_id,
            era="wave2_probe",
            candidate_family=family,
            analysis_bucket=infer_wave2_bucket(short_id),
            hypothesis=hypothesis,
            product_scope=products,
            bot_path=f"rounds/round_3/bots/amin/historical/{filename}",
        )
    return rows


def load_wave3_meta() -> dict[str, RunMeta]:
    rows: dict[str, RunMeta] = {}
    pattern = re.compile(
        r"^\| `(?P<short_id>W3-\d+)` \| `\.\./bots/amin/canonical/(?P<filename>[^`]+)` \| (?P<family>[^|]+) \| (?P<products>[^|]+) \| (?P<axes>[^|]+) \| (?P<hypothesis>[^|]+) \|$"
    )
    for line in WAVE3_MANIFEST.read_text().splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        short_id = match.group("short_id").strip()
        filename = match.group("filename").strip()
        stem = filename[:-3]
        family = match.group("family").strip()
        products = match.group("products").strip()
        hypothesis = match.group("hypothesis").strip()
        rows[stem] = RunMeta(
            short_id=short_id,
            era="wave3_probe",
            candidate_family=family,
            analysis_bucket=infer_wave3_bucket(short_id),
            hypothesis=hypothesis,
            product_scope=products,
            bot_path=f"rounds/round_3/bots/amin/historical/{filename}",
        )
    return rows


def load_wave4_meta() -> dict[str, RunMeta]:
    rows: dict[str, RunMeta] = {}
    pattern = re.compile(
        r"^\| `(?P<short_id>W4-\d+)` \| `\.\./bots/amin/canonical/(?P<filename>[^`]+)` \| (?P<family>[^|]+) \| (?P<products>[^|]+) \| (?P<axes>[^|]+) \| (?P<hypothesis>[^|]+) \|$"
    )
    for line in WAVE4_MANIFEST.read_text().splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        short_id = match.group("short_id").strip()
        filename = match.group("filename").strip()
        stem = filename[:-3]
        family = match.group("family").strip()
        products = match.group("products").strip()
        hypothesis = match.group("hypothesis").strip()
        rows[stem] = RunMeta(
            short_id=short_id,
            era="wave4_probe",
            candidate_family=family,
            analysis_bucket=infer_wave4_bucket(short_id),
            hypothesis=hypothesis,
            product_scope=products,
            bot_path=f"rounds/round_3/bots/amin/historical/{filename}",
        )
    return rows


def load_meta() -> dict[str, RunMeta]:
    meta = dict(MANUAL_RUN_META)
    meta.update(load_wave1_meta())
    meta.update(load_wave2_meta())
    meta.update(load_wave3_meta())
    meta.update(load_wave4_meta())
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


def load_log_payload(stem: str) -> dict | None:
    log_path = PERF_HIST / f"{stem}.log"
    if not log_path.exists() or log_path.stat().st_size == 0:
        return None
    return json.loads(log_path.read_text())


def own_trades_from_payload(payload: dict | None) -> list[dict]:
    if payload is None:
        return []
    return [
        trade
        for trade in payload.get("tradeHistory", [])
        if trade.get("buyer") == "SUBMISSION" or trade.get("seller") == "SUBMISSION"
    ]


def build_mid_lookup(activities: pd.DataFrame) -> dict[str, tuple[list[int], list[float]]]:
    lookup: dict[str, tuple[list[int], list[float]]] = {}
    for product, group in activities.groupby("product"):
        group = group.sort_values("timestamp")
        lookup[str(product)] = (
            group["timestamp"].astype(int).tolist(),
            group["mid_price"].astype(float).tolist(),
        )
    return lookup


def load_trade_metrics(own_trades: list[dict]) -> tuple[dict[str, object], list[dict[str, object]]]:
    if not own_trades:
        return (
            {
                "own_trades": 0,
                "buy_qty": 0,
                "sell_qty": 0,
                "exec_symbols": "",
                "max_abs_exec_position": math.nan,
            },
            [],
        )

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


def build_markout_rows(
    stem: str,
    short_id: str,
    era: str,
    analysis_bucket: str,
    own_trades: list[dict],
    activities: pd.DataFrame,
) -> list[dict[str, object]]:
    if not own_trades:
        return []

    lookup = build_mid_lookup(activities)
    rows: list[dict[str, object]] = []
    for trade in own_trades:
        product = str(trade["symbol"])
        if product not in lookup:
            continue
        timestamps, mids = lookup[product]
        trade_ts = int(trade["timestamp"])
        qty = int(trade["quantity"])
        price = float(trade["price"])
        side = 1 if trade.get("buyer") == "SUBMISSION" else -1
        idx = bisect.bisect_left(timestamps, trade_ts)
        if idx >= len(timestamps):
            idx = len(timestamps) - 1
        current_mid = float(mids[idx])
        entry_unit = (current_mid - price) * side
        row: dict[str, object] = {
            "stem": stem,
            "short_id": short_id,
            "era": era,
            "analysis_bucket": analysis_bucket,
            "product": product,
            "timestamp": trade_ts,
            "side": side,
            "quantity": qty,
            "price": price,
            "current_mid": current_mid,
            "entry_edge_unit": entry_unit,
            "entry_edge_pnl": entry_unit * qty,
        }
        for horizon in MARKOUT_HORIZONS:
            future_idx = bisect.bisect_left(timestamps, trade_ts + horizon)
            if future_idx >= len(timestamps):
                row[f"markout_{horizon}_unit"] = math.nan
                row[f"markout_{horizon}_pnl"] = math.nan
                continue
            future_mid = float(mids[future_idx])
            unit = (future_mid - price) * side
            row[f"markout_{horizon}_unit"] = unit
            row[f"markout_{horizon}_pnl"] = unit * qty
        rows.append(row)
    return rows


def exit_value_on_absolute_giveback(
    path_df: pd.DataFrame,
    value_col: str,
    giveback_limit: float,
) -> tuple[float, int]:
    if path_df.empty:
        return math.nan, 0
    series = path_df[value_col].astype(float).reset_index(drop=True)
    timestamps = path_df["timestamp"].astype(int).reset_index(drop=True)
    peak_idx = int(series.idxmax())
    peak = float(series.iloc[peak_idx])
    if peak <= 0:
        return float(series.iloc[-1]), int(timestamps.iloc[-1])
    for idx in range(peak_idx, len(series)):
        value = float(series.iloc[idx])
        if peak - value >= giveback_limit:
            return value, int(timestamps.iloc[idx])
    return float(series.iloc[-1]), int(timestamps.iloc[-1])


def exit_value_on_peak_fraction(
    path_df: pd.DataFrame,
    value_col: str,
    fraction: float,
) -> tuple[float, int]:
    if path_df.empty:
        return math.nan, 0
    series = path_df[value_col].astype(float).reset_index(drop=True)
    timestamps = path_df["timestamp"].astype(int).reset_index(drop=True)
    peak_idx = int(series.idxmax())
    peak = float(series.iloc[peak_idx])
    if peak <= 0:
        return float(series.iloc[-1]), int(timestamps.iloc[-1])
    floor_value = peak * fraction
    for idx in range(peak_idx, len(series)):
        value = float(series.iloc[idx])
        if value <= floor_value:
            return value, int(timestamps.iloc[idx])
    return float(series.iloc[-1]), int(timestamps.iloc[-1])


def build_exit_counterfactuals(path_df: pd.DataFrame, value_col: str) -> dict[str, object]:
    if path_df.empty:
        return {
            "cf_exit_peak": math.nan,
            "cf_exit_dd_2000": math.nan,
            "cf_exit_dd_5000": math.nan,
            "cf_exit_retain_75": math.nan,
            "cf_exit_retain_60": math.nan,
            "cf_gain_vs_final_dd_2000": math.nan,
            "cf_gain_vs_final_dd_5000": math.nan,
            "cf_gain_vs_final_retain_75": math.nan,
            "cf_gain_vs_final_retain_60": math.nan,
        }
    final_value = float(path_df[value_col].iloc[-1])
    peak_value = float(path_df[value_col].max())
    dd_2000_value, _ = exit_value_on_absolute_giveback(path_df, value_col, 2000.0)
    dd_5000_value, _ = exit_value_on_absolute_giveback(path_df, value_col, 5000.0)
    retain_75_value, _ = exit_value_on_peak_fraction(path_df, value_col, 0.75)
    retain_60_value, _ = exit_value_on_peak_fraction(path_df, value_col, 0.60)
    return {
        "cf_exit_peak": peak_value,
        "cf_exit_dd_2000": dd_2000_value,
        "cf_exit_dd_5000": dd_5000_value,
        "cf_exit_retain_75": retain_75_value,
        "cf_exit_retain_60": retain_60_value,
        "cf_gain_vs_final_dd_2000": dd_2000_value - final_value,
        "cf_gain_vs_final_dd_5000": dd_5000_value - final_value,
        "cf_gain_vs_final_retain_75": retain_75_value - final_value,
        "cf_gain_vs_final_retain_60": retain_60_value - final_value,
    }


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


def build_peak_profile_rows(
    stem: str,
    short_id: str,
    analysis_bucket: str,
    activities: pd.DataFrame,
    peak_ts: int,
) -> list[dict[str, object]]:
    peak_rows = (
        activities[activities["timestamp"] == peak_ts][["product", "profit_and_loss"]]
        .rename(columns={"profit_and_loss": "pnl_at_peak"})
        .copy()
    )
    final_rows = (
        activities.sort_values("timestamp")
        .groupby("product", as_index=False)
        .tail(1)[["product", "profit_and_loss"]]
        .rename(columns={"profit_and_loss": "pnl_final"})
        .copy()
    )
    merged = peak_rows.merge(final_rows, on="product", how="outer").fillna(0.0)
    merged["giveback"] = merged["pnl_final"] - merged["pnl_at_peak"]
    rows: list[dict[str, object]] = []
    for row in merged.itertuples(index=False):
        rows.append(
            {
                "stem": stem,
                "short_id": short_id,
                "analysis_bucket": analysis_bucket,
                "peak_ts": peak_ts,
                "product": row.product,
                "pnl_at_peak": float(row.pnl_at_peak),
                "pnl_final": float(row.pnl_final),
                "giveback": float(row.giveback),
            }
        )
    return rows


def analyze() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    meta = load_meta()
    run_rows: list[dict[str, object]] = []
    product_rows: list[dict[str, object]] = []
    execution_rows: list[dict[str, object]] = []
    trade_rows: list[dict[str, object]] = []
    linkage_rows: list[dict[str, object]] = []
    markout_rows: list[dict[str, object]] = []
    peak_profile_rows: list[dict[str, object]] = []

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
        exit_counterfactuals = build_exit_counterfactuals(activity_path, "total_pnl")
        positions = parse_positions(data)
        product_pnl = final_product_pnl(activities)
        payload = load_log_payload(stem)
        own_trades = own_trades_from_payload(payload)
        trade_metrics, raw_trade_rows = load_trade_metrics(own_trades)
        for trade_row in raw_trade_rows:
            trade_row.update(
                {
                    "stem": stem,
                    "short_id": run_meta.short_id,
                    "analysis_bucket": run_meta.analysis_bucket,
                    "candidate_family": run_meta.candidate_family,
                }
            )
            trade_rows.append(trade_row)
        current_markouts = build_markout_rows(
            stem=stem,
            short_id=run_meta.short_id,
            era=run_meta.era,
            analysis_bucket=run_meta.analysis_bucket,
            own_trades=own_trades,
            activities=activities,
        )
        markout_rows.extend(current_markouts)
        peak_profile_rows.extend(
            build_peak_profile_rows(
                stem=stem,
                short_id=run_meta.short_id,
                analysis_bucket=run_meta.analysis_bucket,
                activities=activities,
                peak_ts=int(path_metrics["path_peak_ts"]) if not pd.isna(path_metrics["path_peak_ts"]) else 0,
            )
        )

        profit_value = as_float(data.get("profit", math.nan))
        if math.isnan(profit_value):
            profit_value = float(sum(product_pnl.values()))

        final_ts = int(activity_path["timestamp"].iloc[-1]) if not activity_path.empty else 0
        post_peak_trades = int(
            sum(int(trade["timestamp"]) > int(path_metrics["path_peak_ts"]) for trade in own_trades)
        )
        post_75_trades = int(sum(int(trade["timestamp"]) > int(final_ts * 0.75) for trade in own_trades))
        post_peak_ratio = post_peak_trades / len(own_trades) if own_trades else math.nan

        if current_markouts:
            markout_df = pd.DataFrame(current_markouts)
            run_markout_metrics = {
                "mean_entry_edge_unit": float(markout_df["entry_edge_unit"].mean()),
                "mean_markout_1000_unit": float(markout_df["markout_1000_unit"].mean()),
                "mean_markout_5000_unit": float(markout_df["markout_5000_unit"].mean()),
                "mean_markout_10000_unit": float(markout_df["markout_10000_unit"].mean()),
            }
        else:
            run_markout_metrics = {
                "mean_entry_edge_unit": math.nan,
                "mean_markout_1000_unit": math.nan,
                "mean_markout_5000_unit": math.nan,
                "mean_markout_10000_unit": math.nan,
            }

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
            "graph_max_drawdown": drawdown(graph["value"]),
            "graph_min": float(graph["value"].min()),
            "graph_max": float(graph["value"].max()),
            **path_metrics,
            **exit_counterfactuals,
            "delta1_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in DELTA1_PRODUCTS)),
            "itm_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ITM_PRODUCTS)),
            "active_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in ACTIVE_PRODUCTS)),
            "upper_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in UPPER_PRODUCTS)),
            "floor_total": float(sum(product_pnl.get(symbol, 0.0) for symbol in FLOOR_PRODUCTS)),
            "active_limit_hits": int(sum(abs(positions.get(symbol, 0)) == 300 for symbol in ACTIVE_PRODUCTS)),
            "upper_limit_hits": int(sum(abs(positions.get(symbol, 0)) == 300 for symbol in UPPER_PRODUCTS)),
            "learning_verdict": learning_verdict(profit_value),
            "post_peak_trades": post_peak_trades,
            "post_75_trades": post_75_trades,
            "post_peak_ratio": post_peak_ratio,
            "early_peak_post_trade_flag": int(
                profit_value < 0
                and float(path_metrics["path_peak"]) > 100
                and float(path_metrics["path_peak_time_frac"]) < 0.35
                and not math.isnan(post_peak_ratio)
                and post_peak_ratio > 0.6
            ),
            **trade_metrics,
            **run_markout_metrics,
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
                "path_peak_time_frac": run_row["path_peak_time_frac"],
                "path_end_from_peak": run_row["path_end_from_peak"],
                "path_positive_time_ratio": run_row["path_positive_time_ratio"],
                "path_shape": run_row["path_shape"],
                "post_peak_trades": run_row["post_peak_trades"],
                "post_75_trades": run_row["post_75_trades"],
                "post_peak_ratio": run_row["post_peak_ratio"],
                "active_limit_hits": run_row["active_limit_hits"],
                "upper_limit_hits": run_row["upper_limit_hits"],
                "final_active_position_abs": int(sum(abs(positions.get(symbol, 0)) for symbol in ACTIVE_PRODUCTS)),
                "final_upper_position_abs": int(sum(abs(positions.get(symbol, 0)) for symbol in UPPER_PRODUCTS)),
                "mean_entry_edge_unit": run_row["mean_entry_edge_unit"],
                "mean_markout_1000_unit": run_row["mean_markout_1000_unit"],
                "mean_markout_5000_unit": run_row["mean_markout_5000_unit"],
                "mean_markout_10000_unit": run_row["mean_markout_10000_unit"],
            }
        )

        run_rows.append(run_row)

    run_df = pd.DataFrame(run_rows).sort_values("profit", ascending=False)
    product_df = pd.DataFrame(product_rows)
    execution_df = pd.DataFrame(execution_rows).sort_values("profit", ascending=False)
    trade_df = pd.DataFrame(trade_rows)
    linkage_df = pd.DataFrame(linkage_rows).sort_values("profit", ascending=False)
    markout_df = pd.DataFrame(markout_rows)
    peak_profile_df = pd.DataFrame(peak_profile_rows)
    return run_df, product_df, execution_df, trade_df, linkage_df, markout_df, peak_profile_df, pd.DataFrame()


def build_family_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    return (
        run_df.groupby("analysis_bucket", as_index=False)
        .agg(
            runs=("stem", "count"),
            mean_profit=("profit", "mean"),
            median_profit=("profit", "median"),
            best_profit=("profit", "max"),
            worst_profit=("profit", "min"),
            mean_path_peak=("path_peak", "mean"),
            mean_peak_time_frac=("path_peak_time_frac", "mean"),
            mean_end_from_peak=("path_end_from_peak", "mean"),
            mean_positive_time_ratio=("path_positive_time_ratio", "mean"),
            mean_delta1=("delta1_total", "mean"),
            mean_itm=("itm_total", "mean"),
            mean_active=("active_total", "mean"),
            mean_upper=("upper_total", "mean"),
            mean_own_trades=("own_trades", "mean"),
            mean_markout_10000_unit=("mean_markout_10000_unit", "mean"),
        )
        .sort_values("mean_profit", ascending=False)
    )


def build_path_family_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    return (
        run_df.groupby("analysis_bucket", as_index=False)
        .agg(
            runs=("stem", "count"),
            mean_final_profit=("profit", "mean"),
            mean_path_peak=("path_peak", "mean"),
            median_path_peak=("path_peak", "median"),
            mean_peak_time_frac=("path_peak_time_frac", "mean"),
            mean_end_from_peak=("path_end_from_peak", "mean"),
            mean_path_max_drawdown=("path_max_drawdown", "mean"),
            mean_positive_time_ratio=("path_positive_time_ratio", "mean"),
            positive_peak_negative_finish_rate=("path_positive_peak_negative_finish", "mean"),
            big_peak_negative_finish_rate=("path_big_peak_negative_finish", "mean"),
            late_peak_rate=("path_peak_after_half", "mean"),
            early_peak_post_trade_rate=("early_peak_post_trade_flag", "mean"),
        )
        .sort_values("mean_path_peak", ascending=False)
    )


def build_path_reversal_table(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_peak_ts",
        "path_peak_time_frac",
        "path_end_from_peak",
        "path_positive_time_ratio",
        "post_peak_ratio",
        "path_shape",
    ]
    return run_df[
        (run_df["path_peak"] > 100) & (run_df["profit"] < 0)
    ].sort_values(["path_end_from_peak", "path_peak"], ascending=[True, False]).loc[:, cols]


def build_high_peak_table(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_peak_ts",
        "path_peak_time_frac",
        "path_end_from_peak",
        "delta1_total",
        "active_total",
        "post_peak_ratio",
        "path_shape",
    ]
    return run_df[run_df["path_peak"] > 5000].sort_values("path_peak", ascending=False).loc[:, cols]


def build_peak_product_summary(peak_profile_df: pd.DataFrame, high_peak_stems: list[str]) -> pd.DataFrame:
    return (
        peak_profile_df[peak_profile_df["stem"].isin(high_peak_stems)]
        .groupby("product", as_index=False)
        .agg(
            runs=("stem", "nunique"),
            total_peak_pnl=("pnl_at_peak", "sum"),
            total_final_pnl=("pnl_final", "sum"),
            total_giveback=("giveback", "sum"),
            mean_giveback=("giveback", "mean"),
        )
        .sort_values("total_giveback")
    )


def build_product_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for product in ALL_PRODUCTS:
        pnl_col = f"pnl_{product}"
        nonzero = run_df[run_df[pnl_col].abs() > 1e-9]
        wave1 = run_df[(run_df["era"] == "wave1_probe") & (run_df[pnl_col].abs() > 1e-9)]
        wave2 = run_df[(run_df["era"] == "wave2_probe") & (run_df[pnl_col].abs() > 1e-9)]
        wave3 = run_df[(run_df["era"] == "wave3_probe") & (run_df[pnl_col].abs() > 1e-9)]
        wave4 = run_df[(run_df["era"] == "wave4_probe") & (run_df[pnl_col].abs() > 1e-9)]
        rows.append(
            {
                "product": product,
                "nonzero_runs": int(nonzero.shape[0]),
                "positive_runs": int((nonzero[pnl_col] > 0).sum()),
                "negative_runs": int((nonzero[pnl_col] < 0).sum()),
                "mean_pnl": float(nonzero[pnl_col].mean()) if not nonzero.empty else math.nan,
                "best_pnl": float(nonzero[pnl_col].max()) if not nonzero.empty else math.nan,
                "worst_pnl": float(nonzero[pnl_col].min()) if not nonzero.empty else math.nan,
                "wave1_nonzero_runs": int(wave1.shape[0]),
                "wave1_mean_pnl": float(wave1[pnl_col].mean()) if not wave1.empty else math.nan,
                "wave2_nonzero_runs": int(wave2.shape[0]),
                "wave2_mean_pnl": float(wave2[pnl_col].mean()) if not wave2.empty else math.nan,
                "wave3_nonzero_runs": int(wave3.shape[0]),
                "wave3_mean_pnl": float(wave3[pnl_col].mean()) if not wave3.empty else math.nan,
                "wave4_nonzero_runs": int(wave4.shape[0]),
                "wave4_mean_pnl": float(wave4[pnl_col].mean()) if not wave4.empty else math.nan,
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
        "post_peak_ratio",
        "mean_markout_10000_unit",
        "learning_verdict",
    ]
    return run_df[run_df["era"] == "wave1_probe"].sort_values("profit", ascending=False).loc[:, cols]


def build_wave2_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "delta1_total",
        "itm_total",
        "active_total",
        "upper_total",
        "path_peak",
        "path_peak_time_frac",
        "path_end_from_peak",
        "own_trades",
        "post_peak_ratio",
        "mean_markout_10000_unit",
        "exec_symbols",
        "learning_verdict",
    ]
    return run_df[run_df["era"] == "wave2_probe"].sort_values("profit", ascending=False).loc[:, cols]


def build_wave3_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "delta1_total",
        "itm_total",
        "active_total",
        "path_peak",
        "path_peak_time_frac",
        "path_end_from_peak",
        "own_trades",
        "post_peak_ratio",
        "mean_markout_10000_unit",
        "cf_gain_vs_final_dd_2000",
        "cf_gain_vs_final_retain_75",
        "learning_verdict",
    ]
    return run_df[run_df["era"] == "wave3_probe"].sort_values("profit", ascending=False).loc[:, cols]


def build_wave4_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "delta1_total",
        "itm_total",
        "active_total",
        "path_peak",
        "path_peak_time_frac",
        "path_end_from_peak",
        "own_trades",
        "post_peak_ratio",
        "mean_markout_10000_unit",
        "cf_gain_vs_final_dd_2000",
        "cf_gain_vs_final_retain_75",
        "learning_verdict",
    ]
    return run_df[run_df["era"] == "wave4_probe"].sort_values("profit", ascending=False).loc[:, cols]


def build_no_trade_table(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_peak_time_frac",
        "path_end_from_peak",
        "own_trades",
        "post_peak_trades",
        "post_peak_ratio",
        "mean_markout_10000_unit",
    ]
    return run_df[
        (run_df["early_peak_post_trade_flag"] == 1)
    ].sort_values(["path_peak", "post_peak_ratio"], ascending=[False, False]).loc[:, cols]


def build_high_peak_gt10k_table(run_df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_peak_ts",
        "path_peak_time_frac",
        "path_end_from_peak",
        "cf_exit_dd_2000",
        "cf_exit_dd_5000",
        "cf_exit_retain_75",
        "cf_gain_vs_final_dd_2000",
        "cf_gain_vs_final_retain_75",
        "delta1_total",
        "itm_total",
        "active_total",
        "path_shape",
    ]
    return run_df[run_df["path_peak"] > 10000].sort_values("path_peak", ascending=False).loc[:, cols]


def build_markout_product_summary(markout_df: pd.DataFrame) -> pd.DataFrame:
    if markout_df.empty:
        return pd.DataFrame()
    return (
        markout_df.groupby("product", as_index=False)
        .agg(
            trades=("stem", "count"),
            mean_entry_edge_unit=("entry_edge_unit", "mean"),
            mean_markout_1000_unit=("markout_1000_unit", "mean"),
            mean_markout_5000_unit=("markout_5000_unit", "mean"),
            mean_markout_10000_unit=("markout_10000_unit", "mean"),
            mean_entry_edge_pnl=("entry_edge_pnl", "mean"),
        )
        .sort_values("product")
    )


def build_markout_run_product_summary(markout_df: pd.DataFrame) -> pd.DataFrame:
    if markout_df.empty:
        return pd.DataFrame()
    return (
        markout_df.groupby(["short_id", "stem", "analysis_bucket", "product"], as_index=False)
        .agg(
            trades=("product", "count"),
            mean_entry_edge_unit=("entry_edge_unit", "mean"),
            mean_markout_1000_unit=("markout_1000_unit", "mean"),
            mean_markout_5000_unit=("markout_5000_unit", "mean"),
            mean_markout_10000_unit=("markout_10000_unit", "mean"),
        )
        .sort_values(["stem", "product"])
    )


def classify_wave4_next_action(row: pd.Series) -> str:
    overlay_vs_delta1 = (
        float(row["profit"]) - float(row["delta1_total"])
        if abs(float(row["delta1_total"])) > 1e-9
        else math.nan
    )
    if row["era"] != "wave4_probe":
        return ""
    if int(row["own_trades"]) == 0:
        return "not_cleanly_tested"
    if row["analysis_bucket"] == "wave4_inverse_closure" and "VEV_5100" not in str(row["exec_symbols"]):
        return "close"
    if row["analysis_bucket"] in {"wave4_delta1_finalists", "wave4_itm_finalists"} and float(row["profit"]) > 1400 and float(row["path_end_from_peak"]) > -900:
        return "promote"
    if (
        row["analysis_bucket"] in {"wave4_5300_finalists", "wave4_peak_salvage"}
        and float(row["profit"]) > 1400
        and overlay_vs_delta1 > -25
    ):
        return "rescue"
    if (
        row["analysis_bucket"] in {"wave4_5300_finalists", "wave4_peak_salvage"}
        and float(row["path_peak"]) > 500
        and float(row["cf_gain_vs_final_retain_75"]) > 150
    ):
        return "rescue"
    if float(row["profit"]) <= 0 and float(row["path_peak"]) <= 100:
        return "close"
    if float(row["profit"]) <= 0 and float(row["mean_markout_10000_unit"]) <= 0:
        return "close"
    return "hold_for_review"


def build_wave4_decision_board(run_df: pd.DataFrame) -> pd.DataFrame:
    wave4 = run_df[run_df["era"] == "wave4_probe"].copy()
    if wave4.empty:
        return pd.DataFrame()
    wave4["next_action"] = wave4.apply(classify_wave4_next_action, axis=1)
    wave4["overlay_vs_delta1"] = wave4.apply(
        lambda row: float(row["profit"]) - float(row["delta1_total"]) if abs(float(row["delta1_total"])) > 1e-9 else math.nan,
        axis=1,
    )
    order = {
        "promote": 0,
        "rescue": 1,
        "hold_for_review": 2,
        "not_cleanly_tested": 3,
        "close": 4,
    }
    wave4["next_action_order"] = wave4["next_action"].map(order).fillna(99)
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_end_from_peak",
        "delta1_total",
        "itm_total",
        "active_total",
        "overlay_vs_delta1",
        "mean_markout_10000_unit",
        "cf_gain_vs_final_retain_75",
        "own_trades",
        "exec_symbols",
        "next_action",
    ]
    return wave4.sort_values(["next_action_order", "profit"], ascending=[True, False]).loc[:, cols]


def classify_wave3_next_action(row: pd.Series) -> str:
    if row["era"] != "wave3_probe":
        return ""
    if int(row["own_trades"]) == 0:
        return "not_cleanly_tested"
    if row["analysis_bucket"] in {"wave3_inverse_tiny", "wave3_inverse_sidecars"} and abs(float(row["active_total"])) < 1e-9:
        return "not_cleanly_tested"
    if abs(float(row["delta1_total"])) > 1e-9 and float(row["profit"]) < float(row["delta1_total"]) - 25:
        return "hold_for_review"
    if float(row["profit"]) > 800 and float(row["path_end_from_peak"]) > -900:
        return "promote"
    if float(row["profit"]) > 250 and float(row["path_end_from_peak"]) > -300 and float(row["mean_markout_10000_unit"]) >= 0:
        return "promote"
    if float(row["path_peak"]) > 250 and float(row["cf_gain_vs_final_retain_75"]) > 200 and float(row["mean_markout_10000_unit"]) > 0:
        return "rescue"
    if float(row["profit"]) <= 0 and float(row["path_peak"]) <= 100:
        return "kill"
    if float(row["profit"]) <= 0 and float(row["mean_markout_10000_unit"]) <= 0:
        return "kill"
    return "hold_for_review"


def build_wave3_decision_board(run_df: pd.DataFrame) -> pd.DataFrame:
    wave3 = run_df[run_df["era"] == "wave3_probe"].copy()
    if wave3.empty:
        return pd.DataFrame()
    wave3["next_action"] = wave3.apply(classify_wave3_next_action, axis=1)
    wave3["overlay_vs_delta1"] = wave3.apply(
        lambda row: float(row["profit"]) - float(row["delta1_total"]) if abs(float(row["delta1_total"])) > 1e-9 else math.nan,
        axis=1,
    )
    order = {
        "promote": 0,
        "rescue": 1,
        "hold_for_review": 2,
        "not_cleanly_tested": 3,
        "kill": 4,
    }
    wave3["next_action_order"] = wave3["next_action"].map(order).fillna(99)
    cols = [
        "short_id",
        "stem",
        "analysis_bucket",
        "profit",
        "path_peak",
        "path_end_from_peak",
        "delta1_total",
        "itm_total",
        "active_total",
        "overlay_vs_delta1",
        "mean_markout_10000_unit",
        "cf_gain_vs_final_retain_75",
        "own_trades",
        "exec_symbols",
        "next_action",
    ]
    return wave3.sort_values(["next_action_order", "profit"], ascending=[True, False]).loc[:, cols]


def render_report(
    run_df: pd.DataFrame,
    family_df: pd.DataFrame,
    path_family_df: pd.DataFrame,
    product_summary_df: pd.DataFrame,
    execution_df: pd.DataFrame,
    linkage_df: pd.DataFrame,
    wave1_df: pd.DataFrame,
    wave2_df: pd.DataFrame,
    reversal_df: pd.DataFrame,
    high_peak_df: pd.DataFrame,
    high_peak_product_df: pd.DataFrame,
    no_trade_df: pd.DataFrame,
    markout_product_df: pd.DataFrame,
    markout_run_product_df: pd.DataFrame,
    wave3_df: pd.DataFrame,
    wave4_df: pd.DataFrame,
    high_peak_gt10k_df: pd.DataFrame,
    high_peak_gt10k_product_df: pd.DataFrame,
    wave3_decision_df: pd.DataFrame,
    wave4_decision_df: pd.DataFrame,
) -> str:
    def row_by_stem(stem: str) -> pd.Series:
        return run_df[run_df["stem"] == stem].iloc[0]

    total_runs = int(run_df.shape[0])
    wave1_runs = int((run_df["era"] == "wave1_probe").sum())
    wave2_runs = int((run_df["era"] == "wave2_probe").sum())
    wave3_runs = int((run_df["era"] == "wave3_probe").sum())
    wave4_runs = int((run_df["era"] == "wave4_probe").sum())
    log_runs = int((execution_df["own_trades"] > 0).sum())
    best_row = run_df.iloc[0]
    best_wave2 = wave2_df.iloc[0]
    best_wave3 = wave3_df.iloc[0]
    best_wave4 = wave4_df.iloc[0]
    high_peak_count = int(high_peak_df.shape[0])
    high_peak_gt10k_count = int(high_peak_gt10k_df.shape[0])
    no_trade_candidates = int(no_trade_df.shape[0])
    path_positive_peak_negative = int(run_df["path_positive_peak_negative_finish"].sum())
    path_big_peak_negative = int(run_df["path_big_peak_negative_finish"].sum())

    top_overall = run_df.head(15)
    wave4_top = wave4_df.head(12)
    high_peak_focus = high_peak_gt10k_product_df.head(8)
    promote_count = int((wave4_decision_df["next_action"] == "promote").sum()) if not wave4_decision_df.empty else 0
    rescue_count = int((wave4_decision_df["next_action"] == "rescue").sum()) if not wave4_decision_df.empty else 0
    close_count = int((wave4_decision_df["next_action"] == "close").sum()) if not wave4_decision_df.empty else 0
    not_tested_count = int((wave4_decision_df["next_action"] == "not_cleanly_tested").sum()) if not wave4_decision_df.empty else 0

    w3_15 = row_by_stem("candidate_w3_15_delta1_kalman_control")
    w3_17 = row_by_stem("candidate_w3_17_5300_imbalance_filter")
    w3_23 = row_by_stem("candidate_w3_23_delta1_itm_active_combo")
    w4_01 = row_by_stem("candidate_w4_01_delta1_kalman_control")
    w4_02 = row_by_stem("candidate_w4_02_delta1_kalman_retention")
    w4_03 = row_by_stem("candidate_w4_03_delta1_itm_kalman_stack")
    w4_04 = row_by_stem("candidate_w4_04_delta1_itm_kalman_strict")
    w4_05 = row_by_stem("candidate_w4_05_5300_selective_control")
    w4_06 = row_by_stem("candidate_w4_06_delta1_5300_selective_overlay")
    w4_07 = row_by_stem("candidate_w4_07_delta1_itm_5300_final_stack")
    w4_08 = row_by_stem("candidate_w4_08_5300_peak_salvage")
    w4_09 = row_by_stem("candidate_w4_09_delta1_5300_peak_overlay")
    w4_10 = row_by_stem("candidate_w4_10_5100_inverse_forced")
    w4_11 = row_by_stem("candidate_w4_11_delta1_kalman_stress_control")
    w4_12 = row_by_stem("candidate_w4_12_5300_trend_comparator")

    markout_focus = markout_run_product_df[
        markout_run_product_df["stem"].isin(
            [
                "candidate_w3_15_delta1_kalman_control",
                "candidate_w3_23_delta1_itm_active_combo",
                "candidate_w4_01_delta1_kalman_control",
                "candidate_w4_02_delta1_kalman_retention",
                "candidate_w4_03_delta1_itm_kalman_stack",
                "candidate_w4_04_delta1_itm_kalman_strict",
                "candidate_w4_05_5300_selective_control",
                "candidate_w4_06_delta1_5300_selective_overlay",
                "candidate_w4_07_delta1_itm_5300_final_stack",
                "candidate_w4_08_5300_peak_salvage",
                "candidate_w4_09_delta1_5300_peak_overlay",
                "candidate_w4_10_5100_inverse_forced",
                "candidate_w4_12_5300_trend_comparator",
                "r3_b08_regime_composite",
                "candidate_c06_composite_base",
            ]
        )
    ].sort_values(["stem", "product"])

    report = f"""# Round 3 Full Performance Synthesis

## Executive Verdict

This report now consolidates the **full current Round 3 evidence base**:
legacy runs, corrected challengers, the full 25-bot Wave 1 learner batch, the
full 19-bot Wave 2 batch, the full 24-bot Wave 3 batch, and the full 12-bot
Wave 4 finalist batch.

- Total platform JSON artifacts analyzed: `{total_runs}`.
- Wave 1 learner JSON artifacts analyzed: `{wave1_runs}`.
- Wave 2 learner / control JSON artifacts analyzed: `{wave2_runs}`.
- Wave 3 learner / winner-shaping JSON artifacts analyzed: `{wave3_runs}`.
- Wave 4 finalist JSON artifacts analyzed: `{wave4_runs}`.
- Runs with usable `tradeHistory` execution detail from `.log`: `{log_runs}`.
- Best overall tested run is now `{best_row['short_id']}` / `{best_row['stem']}.json` at real platform PnL `{best_row['profit']:.3f}`.
- Best Wave 2 run is `{best_wave2['short_id']}` / `{best_wave2['stem']}.json` at real platform PnL `{best_wave2['profit']:.3f}`.
- Best Wave 3 run is `{best_wave3['short_id']}` / `{best_wave3['stem']}.json` at real platform PnL `{best_wave3['profit']:.3f}`.
- Best Wave 4 run is `{best_wave4['short_id']}` / `{best_wave4['stem']}.json` at real platform PnL `{best_wave4['profit']:.3f}`.
- Runs with intra-run peak above `+5k`: `{high_peak_count}`.
- Runs with intra-run peak above `+10k`: `{high_peak_gt10k_count}`.

### Bottom Line

1. **Wave 4 did not produce a new giant winner**, but it did sharpen the endgame: the final race is now between the clean `delta-1` champion family and the `delta-1 + ITM` finalist stack.
2. **The strongest reliable architecture is still delta-1 first**, and the Wave 4 question became “which overlay survives on top of it cleanly?” rather than “which family wins?”
3. **The old `>10k` and `~18k` paths still matter**, but now specifically as a source of retention logic and strike-pruning lessons, not as a reason to reopen the raw broad active basket.
4. **If we want a final upside push above the current `~1.5k` champion ceiling, it has to come from a distilled salvage architecture**, not from simply rerunning the old wide active cluster.

## Updated Ranking Snapshot

{markdown_table(top_overall, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_end_from_peak', 'delta1_total', 'itm_total', 'active_total', 'learning_verdict'])}

### Ranking Reading

- `W3-15` at `{w3_15['profit']:.3f}` remains the best clean architectural result in the whole round unless Wave 4 overtook it.
- `W4-01` at `{w4_01['profit']:.3f}` tells us whether the pure champion survived translation into finalist form.
- `W4-03` at `{w4_03['profit']:.3f}` and `W4-04` at `{w4_04['profit']:.3f}` decide whether active ITM deserves final-bot promotion on top of the stronger Kalman base.
- `W4-05/W4-06/W4-07/W4-08/W4-09/W4-12` decide whether any `5300` branch still merits a final slot or whether it stays only as a salvage research branch.

## What Wave 4 Changed

{markdown_table(wave4_top, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_end_from_peak', 'delta1_total', 'itm_total', 'active_total', 'cf_gain_vs_final_retain_75', 'learning_verdict'])}

### Wave 4 Reading

- Pure champion control:
  - `W3-15 = {w3_15['profit']:.3f}`
  - `W4-01 = {w4_01['profit']:.3f}`
  - `W4-02 = {w4_02['profit']:.3f}`
  This tells us whether the best clean architecture is stable under one more implementation pass and whether a light retention gate helps or hurts.
- Champion plus ITM:
  - `W3-23 = {w3_23['profit']:.3f}`
  - `W4-03 = {w4_03['profit']:.3f}`
  - `W4-04 = {w4_04['profit']:.3f}`
  This is the cleanest test of whether ITM still adds on top of the stronger Kalman champion, not just on top of the older Wave 3 control.
- Selective `5300` finalists:
  - `W3-17 = {w3_17['profit']:.3f}`
  - `W4-05 = {w4_05['profit']:.3f}`
  - `W4-06 = {w4_06['profit']:.3f}`
  - `W4-07 = {w4_07['profit']:.3f}`
  - `W4-12 = {w4_12['profit']:.3f}`
  These decide whether `5300` survives only as a standalone selective micro-branch, as a true overlay, or not at all.
- Distilled peak-salvage attempts:
  - `W4-08 = {w4_08['profit']:.3f}`
  - `W4-09 = {w4_09['profit']:.3f}`
  These are the first serious attempts to harvest old `>10k` logic in a pruned, shutdown-driven form.
- Inverse closure:
  - `W4-10 = {w4_10['profit']:.3f}`
  This is only useful if it truly traded `VEV_5100`; otherwise it should be treated as closure evidence, not as a living final branch.

## Path Quality Summary

- Runs with a positive intra-run peak above `100` that still finished negative:
  `{path_positive_peak_negative}` / `{total_runs}`.
- Runs with a strong intra-run peak above `500` that still finished negative:
  `{path_big_peak_negative}` / `{total_runs}`.
- Runs that still look like strong no-trade / shutdown candidates because they peaked early and kept trading afterwards:
  `{no_trade_candidates}`.

{markdown_table(path_family_df, ['analysis_bucket', 'runs', 'mean_final_profit', 'mean_path_peak', 'median_path_peak', 'mean_peak_time_frac', 'mean_end_from_peak', 'mean_path_max_drawdown', 'mean_positive_time_ratio', 'positive_peak_negative_finish_rate', 'big_peak_negative_finish_rate', 'early_peak_post_trade_rate'])}

### Path Reading

- `wave3_delta1_controls` are now the healthiest family in the entire round on both final PnL and path quality.
- `wave3_itm_and_stacks` are also healthy, but their edge is clearly **base-driven plus small additive overlays**, not voucher-led.
- `wave3_active_rescue_and_filters` improved massively on the old active families, but as a group they are still negative because they continue to **give back too much** or fail to scale cleanly.
- `wave4_delta1_finalists` and `wave4_itm_finalists` are the new decision buckets: they tell us whether the endgame is pure champion or champion-plus-ITM.
- `wave4_peak_salvage` should be read as an exploitation experiment, not as broad strategy evidence: the real question is whether any of the old high-upside logic survives when heavily pruned and blindfolded against continuation mistakes.
- The old `legacy_active_vouchers` bucket still owns the giant peaks, but also the giant collapses. That is exactly why the next step should be **winner-focused exploitation plus selective salvage**, not reopening the broad basket.

## All Round 3 Runs With Peak Above `+10k`

This section applies to **all of Round 3**, not only Wave 3.

{markdown_table(high_peak_gt10k_df, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_end_from_peak', 'cf_exit_dd_2000', 'cf_exit_retain_75', 'cf_gain_vs_final_dd_2000', 'cf_gain_vs_final_retain_75', 'delta1_total', 'active_total', 'path_shape'])}

### `>10k` Reading

- All current `>10k` peak runs belong to the old legacy / broad active-voucher world. **No Wave 3 or Wave 4 bot got there**.
- Wave 4 also failed to approach those peaks, which is exactly why the next wave should explicitly target **distilled upside retention**, not only clean champion confirmation.
- That does **not** mean the upside was fake. It means the upside was being harvested in a branch that had terrible retention and product selection.
- The simple counterfactuals are huge:
  - `B08-regime`: `+16.7k` versus final under a `2k` giveback stop proxy.
  - `C06-legacy`: `+16.7k` versus final under the same proxy.
  - `B04-surf`: `+16.3k`.
  - `B03-pure`: `+12.1k`.
  - `B06-tte`: `+10.2k`.
- So the correct read is **not** “those big-peak branches are ready to promote”. The correct read is “they contained real upside, but packaged in the wrong basket, the wrong strikes, and the wrong continuation logic”.

## Which Products Created And Destroyed Those `>10k` Peaks

{markdown_table(high_peak_focus, ['product', 'runs', 'total_peak_pnl', 'total_final_pnl', 'total_giveback', 'mean_giveback'])}

### Product Reading

- The `>10k` runs were overwhelmingly created and destroyed by the active voucher cluster.
- `VEV_5100`, `VEV_5200`, and `VEV_5000` are still the biggest giveback drivers in the giant-peak set.
- `VEV_5300` also gives back heavily, but it remains materially less toxic than the other active strikes.
- `VELVETFRUIT_EXTRACT` continues to look more like a stabilizer / anchor than the main destroyer.
- The practical implication is that any last upside push should be **VEX-anchored and strike-pruned**, with continuation limits, rather than voucher-led and basket-wide.

## No-Trade / Shutdown Candidates

{markdown_table(no_trade_df, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_peak_time_frac', 'path_end_from_peak', 'own_trades', 'post_peak_trades', 'post_peak_ratio', 'mean_markout_10000_unit'])}

### No-Trade Reading

- The selective active-voucher runs still peak much earlier than they stop trading.
- The strongest current implication is that **new-entry shutdown, time-window control, and giveback discipline** remain the most valuable rescue axes for any remaining `5300` work.

## Execution Markout Evidence By Product

{markdown_table(markout_product_df, ['product', 'trades', 'mean_entry_edge_unit', 'mean_markout_1000_unit', 'mean_markout_5000_unit', 'mean_markout_10000_unit'])}

### Markout Reading

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` remain clean at every horizon.
- `VEV_4000/4500` are slightly awkward on entry but fine by `10k`, which matches the new “ITM as small overlay” thesis.
- `VEV_5300` is still the only active strike with a **positive `10k` mean markout** (`{markout_product_df.loc[markout_product_df['product'] == 'VEV_5300', 'mean_markout_10000_unit'].iloc[0]:.3f}`).
- `VEV_5000`, `VEV_5100`, and `VEV_5200` remain negative at `10k`, with `5200` worst on aggregate.
- `VEV_5400` is almost flat by `10k`, and `VEV_5500` slightly positive, but those branches are still low-ROI relative to the main decision axes.

## Focus Comparison: Champion Base, ITM Overlay, `5300`, And Inverse Branches

{markdown_table(markout_focus, ['short_id', 'stem', 'product', 'trades', 'mean_entry_edge_unit', 'mean_markout_1000_unit', 'mean_markout_5000_unit', 'mean_markout_10000_unit'])}

### Focus Reading

- `W4-01` and `W4-02` show whether the champion remains strong without leaning on any voucher branch.
- `W4-03` and `W4-04` show whether ITM still adds cleanly on the stronger Kalman base or whether the old uplift was tied to the older stack shape.
- `W4-05`, `W4-06`, `W4-07`, and `W4-12` tell us whether `5300` belongs as a standalone filtered branch, a micro-overlay, or nowhere in the final architecture.
- `W4-08` and `W4-09` should be read as the first direct answer to the user's core question: can we preserve any of the old huge upside without reopening the old self-destructive continuation pattern?
- `W4-10` is closure quality only; if it still did not trade `VEV_5100`, that branch should be considered exhausted for final-wave purposes.

## Wave 4 Decision Board

Promote count: `{promote_count}`. Rescue count: `{rescue_count}`. Close count: `{close_count}`. Not-cleanly-tested count: `{not_tested_count}`.

{markdown_table(wave4_decision_df, ['short_id', 'stem', 'analysis_bucket', 'profit', 'path_peak', 'path_end_from_peak', 'overlay_vs_delta1', 'mean_markout_10000_unit', 'cf_gain_vs_final_retain_75', 'own_trades', 'exec_symbols', 'next_action'])}

### Decision Reading

- **Promote now** means “candidate for the next near-final winner batch”.
- **Rescue** means “keep only if it is specifically an upside-distillation / retention experiment”.
- **Close** means “do not spend another normal finalist slot on it”.
- The purpose of this board is not to crown the winner yet. It is to decide which branches deserve the final exploitation wave.

## Product-Level Realized Summary

{markdown_table(product_summary_df, ['product', 'nonzero_runs', 'positive_runs', 'negative_runs', 'mean_pnl', 'best_pnl', 'worst_pnl', 'wave3_nonzero_runs', 'wave3_mean_pnl', 'wave4_nonzero_runs', 'wave4_mean_pnl'])}

## What Worked

- Clean delta-1 on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`.
- Kalman-style smoothing on top of the clean delta-1 base.
- Active ITM as a small additive overlay when attached to the base.
- Selective `5300` filtering when aggressively narrowed and tied to better state selection.
- Using the old `>10k` runs as **retention design evidence** rather than as a ready-made architecture.

## What Did Not Work

- Broad active-voucher baskets as promotable architecture.
- Treating `5000/5100/5200` as normal active-reversion strikes.
- Assuming raw huge peaks were enough evidence by themselves.
- Using inverse diagnostics as evidence when the target inverse leg did not even trade.
- Expecting Wave 4 finalist hygiene alone to recreate the old giant peaks. Cleanliness helped quality, but it also compressed upside.

## Analytical Consequence

The next step should now be a **winner-focused exploitation pass**, not another broad exploratory wave.

The next spec should answer:

1. Is the near-final base `W3-15`, `W4-01`, `W4-02`, `W4-03`, or `W4-04`?
2. Does any `5300` branch still deserve a final overlay slot after Wave 4?
3. Which pruned, VEX-anchored descendants of the old `>10k` paths deserve the last upside-distillation slots?
4. Which simple online retention rules from the `>10k` counterfactual study are worth converting into real logic without overfitting?

## Artifacts

- [`artifacts/full_synthesis/full_run_metrics.csv`](artifacts/full_synthesis/full_run_metrics.csv)
- [`artifacts/full_synthesis/full_family_summary.csv`](artifacts/full_synthesis/full_family_summary.csv)
- [`artifacts/full_synthesis/full_path_family_summary.csv`](artifacts/full_synthesis/full_path_family_summary.csv)
- [`artifacts/full_synthesis/full_path_reversal_candidates.csv`](artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`artifacts/full_synthesis/full_product_attribution.csv`](artifacts/full_synthesis/full_product_attribution.csv)
- [`artifacts/full_synthesis/full_execution_metrics.csv`](artifacts/full_synthesis/full_execution_metrics.csv)
- [`artifacts/full_synthesis/full_strategy_run_mapping.csv`](artifacts/full_synthesis/full_strategy_run_mapping.csv)
- [`artifacts/full_synthesis/full_wave1_probe_summary.csv`](artifacts/full_synthesis/full_wave1_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave2_probe_summary.csv`](artifacts/full_synthesis/full_wave2_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave3_probe_summary.csv`](artifacts/full_synthesis/full_wave3_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave4_probe_summary.csv`](artifacts/full_synthesis/full_wave4_probe_summary.csv)
- [`artifacts/full_synthesis/full_high_peak_gt5k_runs.csv`](artifacts/full_synthesis/full_high_peak_gt5k_runs.csv)
- [`artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
- [`artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv`](artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv)
- [`artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
- [`artifacts/full_synthesis/full_no_trade_candidates.csv`](artifacts/full_synthesis/full_no_trade_candidates.csv)
- [`artifacts/full_synthesis/full_trade_markout_by_product.csv`](artifacts/full_synthesis/full_trade_markout_by_product.csv)
- [`artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- [`artifacts/full_synthesis/full_wave3_decision_board.csv`](artifacts/full_synthesis/full_wave3_decision_board.csv)
- [`artifacts/full_synthesis/full_wave4_decision_board.csv`](artifacts/full_synthesis/full_wave4_decision_board.csv)
- [`artifacts/full_synthesis/full_peak_profiles.csv`](artifacts/full_synthesis/full_peak_profiles.csv)
"""
    return report


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    (
        run_df,
        product_df,
        execution_df,
        trade_df,
        linkage_df,
        markout_df,
        peak_profile_df,
        _,
    ) = analyze()

    family_df = build_family_summary(run_df)
    path_family_df = build_path_family_summary(run_df)
    reversal_df = build_path_reversal_table(run_df)
    high_peak_df = build_high_peak_table(run_df)
    high_peak_product_df = build_peak_product_summary(peak_profile_df, high_peak_df["stem"].tolist())
    high_peak_gt10k_df = build_high_peak_gt10k_table(run_df)
    high_peak_gt10k_product_df = build_peak_product_summary(peak_profile_df, high_peak_gt10k_df["stem"].tolist())
    product_summary_df = build_product_summary(run_df)
    wave1_df = build_wave1_summary(run_df)
    wave2_df = build_wave2_summary(run_df)
    wave3_df = build_wave3_summary(run_df)
    wave4_df = build_wave4_summary(run_df)
    no_trade_df = build_no_trade_table(run_df)
    markout_product_df = build_markout_product_summary(markout_df)
    markout_run_product_df = build_markout_run_product_summary(markout_df)
    wave3_decision_df = build_wave3_decision_board(run_df)
    wave4_decision_df = build_wave4_decision_board(run_df)

    run_df.to_csv(ARTIFACTS / "full_run_metrics.csv", index=False)
    family_df.to_csv(ARTIFACTS / "full_family_summary.csv", index=False)
    path_family_df.to_csv(ARTIFACTS / "full_path_family_summary.csv", index=False)
    reversal_df.to_csv(ARTIFACTS / "full_path_reversal_candidates.csv", index=False)
    product_df.to_csv(ARTIFACTS / "full_product_attribution.csv", index=False)
    execution_df.to_csv(ARTIFACTS / "full_execution_metrics.csv", index=False)
    linkage_df.to_csv(ARTIFACTS / "full_strategy_run_mapping.csv", index=False)
    wave1_df.to_csv(ARTIFACTS / "full_wave1_probe_summary.csv", index=False)
    wave2_df.to_csv(ARTIFACTS / "full_wave2_probe_summary.csv", index=False)
    wave3_df.to_csv(ARTIFACTS / "full_wave3_probe_summary.csv", index=False)
    wave4_df.to_csv(ARTIFACTS / "full_wave4_probe_summary.csv", index=False)
    high_peak_df.to_csv(ARTIFACTS / "full_high_peak_gt5k_runs.csv", index=False)
    high_peak_gt10k_df.to_csv(ARTIFACTS / "full_high_peak_gt10k_runs.csv", index=False)
    high_peak_product_df.to_csv(ARTIFACTS / "full_high_peak_gt5k_product_giveback.csv", index=False)
    high_peak_gt10k_product_df.to_csv(ARTIFACTS / "full_high_peak_gt10k_product_giveback.csv", index=False)
    no_trade_df.to_csv(ARTIFACTS / "full_no_trade_candidates.csv", index=False)
    peak_profile_df.to_csv(ARTIFACTS / "full_peak_profiles.csv", index=False)
    wave3_decision_df.to_csv(ARTIFACTS / "full_wave3_decision_board.csv", index=False)
    wave4_decision_df.to_csv(ARTIFACTS / "full_wave4_decision_board.csv", index=False)
    if not trade_df.empty:
        trade_df.to_csv(ARTIFACTS / "full_own_trade_timeline.csv", index=False)
    if not markout_df.empty:
        markout_df.to_csv(ARTIFACTS / "full_trade_markouts.csv", index=False)
        markout_product_df.to_csv(ARTIFACTS / "full_trade_markout_by_product.csv", index=False)
        markout_run_product_df.to_csv(ARTIFACTS / "full_trade_markout_by_run_product.csv", index=False)

    REPORT.write_text(
        render_report(
            run_df=run_df,
            family_df=family_df,
            path_family_df=path_family_df,
            product_summary_df=product_summary_df,
            execution_df=execution_df,
            linkage_df=linkage_df,
            wave1_df=wave1_df,
            wave2_df=wave2_df,
            reversal_df=reversal_df,
            high_peak_df=high_peak_df,
            high_peak_product_df=high_peak_product_df,
            no_trade_df=no_trade_df,
            markout_product_df=markout_product_df,
            markout_run_product_df=markout_run_product_df,
            wave3_df=wave3_df,
            wave4_df=wave4_df,
            high_peak_gt10k_df=high_peak_gt10k_df,
            high_peak_gt10k_product_df=high_peak_gt10k_product_df,
            wave3_decision_df=wave3_decision_df,
            wave4_decision_df=wave4_decision_df,
        )
    )


if __name__ == "__main__":
    main()
