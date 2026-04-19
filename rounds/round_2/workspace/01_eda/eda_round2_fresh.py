from __future__ import annotations

import io
import json
import math
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/tmp/simplex_round2_mplconfig")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import het_arch

try:
    import ruptures as rpt
except Exception:  # pragma: no cover - optional research dependency
    rpt = None


REPO_ROOT = Path(__file__).resolve().parents[4]
ROUND_ROOT = REPO_ROOT / "rounds" / "round_2"
EDA_DIR = ROUND_ROOT / "workspace" / "01_eda"
ARTIFACT_DIR = EDA_DIR / "artifacts"
RAW_DATA_DIR = ROUND_ROOT / "data" / "raw"
PLATFORM_JSON = (
    ROUND_ROOT
    / "performances"
    / "noel"
    / "historical"
    / "baseline_state_logger.json"
)
REPORT_PATH = EDA_DIR / "eda_round2_fresh.md"

PRODUCTS = ["ASH_COATED_OSMIUM", "INTARIAN_PEPPER_ROOT"]
PRICE_FILES = [
    RAW_DATA_DIR / "prices_round_2_day_-1.csv",
    RAW_DATA_DIR / "prices_round_2_day_0.csv",
    RAW_DATA_DIR / "prices_round_2_day_1.csv",
]
TRADE_FILES = [
    RAW_DATA_DIR / "trades_round_2_day_-1.csv",
    RAW_DATA_DIR / "trades_round_2_day_0.csv",
    RAW_DATA_DIR / "trades_round_2_day_1.csv",
]

PRICE_COLS = [
    "bid_price_1",
    "bid_volume_1",
    "bid_price_2",
    "bid_volume_2",
    "bid_price_3",
    "bid_volume_3",
    "ask_price_1",
    "ask_volume_1",
    "ask_price_2",
    "ask_volume_2",
    "ask_price_3",
    "ask_volume_3",
    "mid_price",
    "profit_and_loss",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


def ensure_dirs() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def read_semicolon_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=";")


def coerce_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def read_prices() -> pd.DataFrame:
    frames = []
    for path in PRICE_FILES:
        df = read_semicolon_csv(path)
        df["source_file"] = rel(path)
        df["source_line_count_incl_header"] = line_count(path)
        frames.append(df)
    prices = pd.concat(frames, ignore_index=True)
    return coerce_numeric(prices, ["day", "timestamp", *PRICE_COLS])


def read_trades() -> pd.DataFrame:
    frames = []
    for path in TRADE_FILES:
        df = read_semicolon_csv(path)
        df["source_file"] = rel(path)
        df["source_line_count_incl_header"] = line_count(path)
        frames.append(df)
    trades = pd.concat(frames, ignore_index=True)
    return coerce_numeric(trades, ["timestamp", "price", "quantity"])


def read_platform_json() -> dict[str, Any]:
    if not PLATFORM_JSON.exists():
        return {}
    with PLATFORM_JSON.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_platform_activities(platform: dict[str, Any]) -> pd.DataFrame:
    activities_log = platform.get("activitiesLog", "")
    if not activities_log:
        return pd.DataFrame()
    df = pd.read_csv(io.StringIO(activities_log), sep=";")
    df["source_file"] = rel(PLATFORM_JSON)
    return coerce_numeric(df, ["day", "timestamp", *PRICE_COLS])


def read_platform_graph(platform: dict[str, Any]) -> pd.DataFrame:
    graph_log = platform.get("graphLog", "")
    if not graph_log:
        return pd.DataFrame()
    df = pd.read_csv(io.StringIO(graph_log), sep=";")
    df["source_file"] = rel(PLATFORM_JSON)
    return coerce_numeric(df, ["timestamp", "value"])


def add_book_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "mid_price" in out.columns:
        out["mid_price_raw"] = out["mid_price"]
        out.loc[out["mid_price"] <= 0, "mid_price"] = np.nan
    bid_prices = [f"bid_price_{idx}" for idx in range(1, 4)]
    ask_prices = [f"ask_price_{idx}" for idx in range(1, 4)]
    bid_volumes = [f"bid_volume_{idx}" for idx in range(1, 4)]
    ask_volumes = [f"ask_volume_{idx}" for idx in range(1, 4)]

    for col in [*bid_prices, *ask_prices, *bid_volumes, *ask_volumes]:
        if col not in out.columns:
            out[col] = np.nan

    out["has_best_bid"] = out["bid_price_1"].notna()
    out["has_best_ask"] = out["ask_price_1"].notna()
    out["has_two_sided_book"] = out["has_best_bid"] & out["has_best_ask"]
    out["spread"] = out["ask_price_1"] - out["bid_price_1"]
    out.loc[~out["has_two_sided_book"], "spread"] = np.nan

    out["top_bid_volume"] = out["bid_volume_1"].fillna(0).clip(lower=0)
    out["top_ask_volume"] = out["ask_volume_1"].fillna(0).abs()
    out["total_bid_volume"] = out[bid_volumes].fillna(0).clip(lower=0).sum(axis=1)
    out["total_ask_volume"] = out[ask_volumes].fillna(0).abs().sum(axis=1)
    out["top_total_volume"] = out["top_bid_volume"] + out["top_ask_volume"]
    out["book_total_volume"] = out["total_bid_volume"] + out["total_ask_volume"]
    out["top_imbalance"] = np.where(
        out["top_total_volume"] > 0,
        (out["top_bid_volume"] - out["top_ask_volume"]) / out["top_total_volume"],
        np.nan,
    )
    out["book_imbalance"] = np.where(
        out["book_total_volume"] > 0,
        (out["total_bid_volume"] - out["total_ask_volume"]) / out["book_total_volume"],
        np.nan,
    )
    out["one_sided_book"] = out["has_best_bid"] ^ out["has_best_ask"]
    out["missing_level_count"] = out[bid_prices + ask_prices].isna().sum(axis=1)
    out["relative_spread"] = np.where(
        out["mid_price"].abs() > 0, out["spread"] / out["mid_price"], np.nan
    )

    sort_cols = ["product", "day", "timestamp"]
    out = out.sort_values(sort_cols).reset_index(drop=True)
    grouped = out.groupby(["product", "day"], sort=False)
    out["mid_delta_1"] = grouped["mid_price"].diff()
    out["abs_mid_delta_1"] = out["mid_delta_1"].abs()
    out["rolling_mid_50"] = grouped["mid_price"].transform(
        lambda s: s.rolling(50, min_periods=20).mean()
    )
    out["rolling_vol_50"] = grouped["mid_delta_1"].transform(
        lambda s: s.rolling(50, min_periods=20).std()
    )
    out["mid_minus_rolling_50"] = out["mid_price"] - out["rolling_mid_50"]
    out["z_mid_50"] = np.where(
        out["rolling_vol_50"] > 0,
        out["mid_minus_rolling_50"] / out["rolling_vol_50"],
        np.nan,
    )
    return out


def save_csv(df: pd.DataFrame, name: str) -> Path:
    path = ARTIFACT_DIR / name
    df.to_csv(path, index=False)
    return path


def save_json(data: Any, name: str) -> Path:
    path = ARTIFACT_DIR / name
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
    return path


def safe_corr(x: pd.Series, y: pd.Series) -> tuple[float, float, int]:
    mask = x.notna() & y.notna()
    n = int(mask.sum())
    if n < 20:
        return np.nan, np.nan, n
    xv = x.loc[mask]
    yv = y.loc[mask]
    if xv.nunique() < 2 or yv.nunique() < 2:
        return np.nan, np.nan, n
    corr, pvalue = stats.pearsonr(xv, yv)
    return float(corr), float(pvalue), n


def ac(series: pd.Series, lag: int) -> float:
    clean = series.dropna()
    if len(clean) <= lag + 2 or clean.nunique() < 2:
        return np.nan
    return float(clean.autocorr(lag))


def arch_pvalue(series: pd.Series) -> float:
    clean = series.dropna()
    if len(clean) < 100 or clean.nunique() < 2:
        return np.nan
    try:
        _, pvalue, _, _ = het_arch(clean, nlags=5)
        return float(pvalue)
    except Exception:
        return np.nan


def detect_change_points(series: pd.Series, max_points: int = 3) -> list[int]:
    clean = series.dropna().to_numpy(dtype=float)
    if rpt is None or len(clean) < 200:
        return []
    try:
        algo = rpt.Binseg(model="l2").fit(clean)
        points = algo.predict(n_bkps=max_points)
        return [int(point) for point in points if point < len(clean)]
    except Exception:
        return []


def data_quality(prices: pd.DataFrame, trades: pd.DataFrame, platform: dict[str, Any], platform_activities: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path in PRICE_FILES:
        df = prices[prices["source_file"] == rel(path)]
        rows.append(
            {
                "source": rel(path),
                "kind": "raw_prices",
                "line_count_incl_header": line_count(path),
                "rows": len(df),
                "products": ",".join(sorted(df["product"].dropna().unique())),
                "day_values": ",".join(map(str, sorted(df["day"].dropna().unique()))),
                "timestamp_min": df["timestamp"].min(),
                "timestamp_max": df["timestamp"].max(),
                "duplicate_product_timestamp_rows": int(df.duplicated(["product", "day", "timestamp"]).sum()),
                "missing_mid_price_rows": int(df["mid_price"].isna().sum()),
                "zero_mid_price_rows": int((df["mid_price_raw"] <= 0).sum()) if "mid_price_raw" in df.columns else int((df["mid_price"] <= 0).sum()),
                "missing_best_bid_rows": int(df["bid_price_1"].isna().sum()),
                "missing_best_ask_rows": int(df["ask_price_1"].isna().sum()),
            }
        )

    for path in TRADE_FILES:
        df = trades[trades["source_file"] == rel(path)]
        rows.append(
            {
                "source": rel(path),
                "kind": "raw_trades",
                "line_count_incl_header": line_count(path),
                "rows": len(df),
                "products": ",".join(sorted(df["symbol"].dropna().unique())),
                "day_values": "from file name",
                "timestamp_min": df["timestamp"].min(),
                "timestamp_max": df["timestamp"].max(),
                "duplicate_product_timestamp_rows": int(df.duplicated(["symbol", "timestamp"]).sum()),
                "missing_mid_price_rows": np.nan,
                "zero_mid_price_rows": np.nan,
                "missing_best_bid_rows": np.nan,
                "missing_best_ask_rows": np.nan,
            }
        )

    if platform:
        rows.append(
            {
                "source": rel(PLATFORM_JSON),
                "kind": "platform_json",
                "line_count_incl_header": line_count(PLATFORM_JSON),
                "rows": 1,
                "products": "from activitiesLog",
                "day_values": platform.get("round"),
                "timestamp_min": np.nan,
                "timestamp_max": np.nan,
                "duplicate_product_timestamp_rows": np.nan,
                "missing_mid_price_rows": np.nan,
                "zero_mid_price_rows": np.nan,
                "missing_best_bid_rows": np.nan,
                "missing_best_ask_rows": np.nan,
                "status": platform.get("status"),
                "profit": platform.get("profit"),
                "has_round2_state_probe": "ROUND2_STATE_PROBE" in json.dumps(platform),
            }
        )

    if not platform_activities.empty:
        rows.append(
            {
                "source": rel(PLATFORM_JSON) + "::activitiesLog",
                "kind": "platform_activities",
                "line_count_incl_header": np.nan,
                "rows": len(platform_activities),
                "products": ",".join(sorted(platform_activities["product"].dropna().unique())),
                "day_values": ",".join(map(str, sorted(platform_activities["day"].dropna().unique()))),
                "timestamp_min": platform_activities["timestamp"].min(),
                "timestamp_max": platform_activities["timestamp"].max(),
                "duplicate_product_timestamp_rows": int(
                    platform_activities.duplicated(["product", "day", "timestamp"]).sum()
                ),
                "missing_mid_price_rows": int(platform_activities["mid_price"].isna().sum()),
                "zero_mid_price_rows": int((platform_activities["mid_price_raw"] <= 0).sum()) if "mid_price_raw" in platform_activities.columns else int((platform_activities["mid_price"] <= 0).sum()),
                "missing_best_bid_rows": int(platform_activities["bid_price_1"].isna().sum()),
                "missing_best_ask_rows": int(platform_activities["ask_price_1"].isna().sum()),
                "status": platform.get("status"),
                "profit": platform.get("profit"),
                "has_round2_state_probe": False,
            }
        )

    return pd.DataFrame(rows)


def product_behavior(prices: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for (product, day), df in prices.groupby(["product", "day"]):
        df = df.sort_values("timestamp").copy()
        usable = df[df["mid_price"].notna()]
        delta = usable["mid_price"].diff()
        if len(usable) >= 10:
            lr = stats.linregress(usable["timestamp"], usable["mid_price"])
            fit = lr.intercept + lr.slope * usable["timestamp"]
            residual = usable["mid_price"] - fit
        else:
            lr = None
            residual = pd.Series(dtype=float)
        rows.append(
            {
                "product": product,
                "day": int(day),
                "rows": len(df),
                "usable_mid_rows": len(usable),
                "mid_first": usable["mid_price"].iloc[0] if len(usable) else np.nan,
                "mid_last": usable["mid_price"].iloc[-1] if len(usable) else np.nan,
                "mid_mean": usable["mid_price"].mean(),
                "mid_std": usable["mid_price"].std(),
                "mid_min": usable["mid_price"].min(),
                "mid_q05": usable["mid_price"].quantile(0.05),
                "mid_q50": usable["mid_price"].quantile(0.50),
                "mid_q95": usable["mid_price"].quantile(0.95),
                "mid_max": usable["mid_price"].max(),
                "total_change": (usable["mid_price"].iloc[-1] - usable["mid_price"].iloc[0]) if len(usable) else np.nan,
                "linear_slope_per_timestamp": lr.slope if lr else np.nan,
                "linear_r2": lr.rvalue**2 if lr else np.nan,
                "linear_residual_std": residual.std() if len(residual) else np.nan,
                "delta_std": delta.std(),
                "delta_abs_q95": delta.abs().quantile(0.95),
                "delta_ac1": ac(delta, 1),
                "delta_ac2": ac(delta, 2),
                "mid_ac1": ac(usable["mid_price"], 1),
                "arch_lm_pvalue_delta": arch_pvalue(delta),
                "spread_mean": usable["spread"].mean(),
                "spread_median": usable["spread"].median(),
                "spread_q95": usable["spread"].quantile(0.95),
                "two_sided_rate": usable["has_two_sided_book"].mean(),
                "one_sided_rate": usable["one_sided_book"].mean(),
                "change_points_mid_index": ",".join(map(str, detect_change_points(usable["mid_price"]))),
            }
        )
    return pd.DataFrame(rows)


def imbalance_ic(prices: pd.DataFrame) -> pd.DataFrame:
    features = ["top_imbalance", "book_imbalance", "spread", "book_total_volume"]
    horizons = [1, 2, 3, 5, 10]
    rows: list[dict[str, Any]] = []
    for (product, day), df in prices.groupby(["product", "day"]):
        df = df.sort_values("timestamp").copy()
        for horizon in horizons:
            future = df["mid_price"].shift(-horizon) - df["mid_price"]
            for feature in features:
                corr, pvalue, n = safe_corr(df[feature], future)
                rows.append(
                    {
                        "product": product,
                        "day": int(day),
                        "feature": feature,
                        "horizon_ticks": horizon,
                        "pearson_corr": corr,
                        "pvalue": pvalue,
                        "n": n,
                    }
                )
    return pd.DataFrame(rows)


def conditional_imbalance_ic(prices: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    horizons = [1, 3, 5]
    data = prices.copy()
    data["spread_regime"] = "unknown"
    data["liquidity_regime"] = "unknown"
    for product, product_df in data.groupby("product"):
        spread_q = product_df["spread"].quantile([0.33, 0.66])
        liq_q = product_df["book_total_volume"].quantile([0.33, 0.66])
        mask = data["product"] == product
        data.loc[mask & (data["spread"] <= spread_q.loc[0.33]), "spread_regime"] = "tight"
        data.loc[mask & (data["spread"] > spread_q.loc[0.33]) & (data["spread"] <= spread_q.loc[0.66]), "spread_regime"] = "normal"
        data.loc[mask & (data["spread"] > spread_q.loc[0.66]), "spread_regime"] = "wide"
        data.loc[mask & (data["book_total_volume"] <= liq_q.loc[0.33]), "liquidity_regime"] = "low"
        data.loc[mask & (data["book_total_volume"] > liq_q.loc[0.33]) & (data["book_total_volume"] <= liq_q.loc[0.66]), "liquidity_regime"] = "normal"
        data.loc[mask & (data["book_total_volume"] > liq_q.loc[0.66]), "liquidity_regime"] = "high"

    for product, product_df in data.groupby("product"):
        for regime_col in ["spread_regime", "liquidity_regime"]:
            for regime, regime_df in product_df.groupby(regime_col):
                for horizon in horizons:
                    for feature in ["top_imbalance", "book_imbalance"]:
                        tmp = regime_df.sort_values(["day", "timestamp"]).copy()
                        future = tmp.groupby("day")["mid_price"].shift(-horizon) - tmp["mid_price"]
                        corr, pvalue, n = safe_corr(tmp[feature], future)
                        rows.append(
                            {
                                "product": product,
                                "regime_type": regime_col,
                                "regime": regime,
                                "feature": feature,
                                "horizon_ticks": horizon,
                                "pearson_corr": corr,
                                "pvalue": pvalue,
                                "n": n,
                            }
                        )
    return pd.DataFrame(rows)


def trade_flow(trades: pd.DataFrame, prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    prices_key = prices[
        ["day", "timestamp", "product", "mid_price", "bid_price_1", "ask_price_1"]
    ].copy()
    trade_rows = []
    for path in TRADE_FILES:
        day_text = path.stem.split("_day_")[-1]
        day = int(day_text)
        df = trades[trades["source_file"] == rel(path)].copy()
        df["day"] = day
        trade_rows.append(df)
    trades_with_day = pd.concat(trade_rows, ignore_index=True)
    merged = trades_with_day.merge(
        prices_key,
        left_on=["day", "timestamp", "symbol"],
        right_on=["day", "timestamp", "product"],
        how="left",
    )
    merged["price_vs_mid"] = merged["price"] - merged["mid_price"]
    merged["side_proxy"] = np.sign(merged["price_vs_mid"]).fillna(0)
    merged["signed_qty_proxy"] = merged["side_proxy"] * merged["quantity"]

    summary_rows: list[dict[str, Any]] = []
    for (symbol, day), df in merged.groupby(["symbol", "day"]):
        summary_rows.append(
            {
                "product": symbol,
                "day": int(day),
                "trade_rows": len(df),
                "total_quantity": df["quantity"].sum(),
                "mean_quantity": df["quantity"].mean(),
                "median_quantity": df["quantity"].median(),
                "q95_quantity": df["quantity"].quantile(0.95),
                "price_min": df["price"].min(),
                "price_max": df["price"].max(),
                "matched_mid_rate": df["mid_price"].notna().mean(),
                "mean_price_vs_mid": df["price_vs_mid"].mean(),
                "abs_price_vs_mid_q95": df["price_vs_mid"].abs().quantile(0.95),
                "positive_pressure_qty": df.loc[df["side_proxy"] > 0, "quantity"].sum(),
                "negative_pressure_qty": df.loc[df["side_proxy"] < 0, "quantity"].sum(),
                "zero_or_unmatched_pressure_qty": df.loc[df["side_proxy"] == 0, "quantity"].sum(),
            }
        )

    pressure = (
        merged.groupby(["day", "timestamp", "symbol"], as_index=False)
        .agg(
            trade_count=("quantity", "size"),
            total_quantity=("quantity", "sum"),
            signed_qty_proxy=("signed_qty_proxy", "sum"),
            mean_price_vs_mid=("price_vs_mid", "mean"),
        )
        .rename(columns={"symbol": "product"})
    )
    return pd.DataFrame(summary_rows), pressure


def platform_comparability(prices: pd.DataFrame, platform_activities: pd.DataFrame, platform_graph: pd.DataFrame, platform: dict[str, Any]) -> pd.DataFrame:
    if platform_activities.empty:
        return pd.DataFrame(
            [
                {
                    "product": "ALL",
                    "metric": "platform_data",
                    "sample_value": np.nan,
                    "platform_value": np.nan,
                    "difference": np.nan,
                    "verdict": "blocked",
                    "notes": "No platform activitiesLog available.",
                }
            ]
        )

    platform_features = add_book_features(platform_activities)
    rows: list[dict[str, Any]] = []
    for product in PRODUCTS:
        raw = prices[(prices["product"] == product) & (prices["day"] == 1)].copy()
        plat = platform_features[platform_features["product"] == product].copy()
        overlap = raw.merge(
            plat,
            on=["product", "timestamp"],
            suffixes=("_raw", "_platform"),
            how="inner",
        )
        metrics = [
            ("rows", len(raw), len(plat), len(plat) - len(raw)),
            ("overlap_rows", len(raw), len(overlap), len(overlap) - min(len(raw), len(plat))),
            ("two_sided_rate", raw["has_two_sided_book"].mean(), plat["has_two_sided_book"].mean(), plat["has_two_sided_book"].mean() - raw["has_two_sided_book"].mean()),
            ("one_sided_rate", raw["one_sided_book"].mean(), plat["one_sided_book"].mean(), plat["one_sided_book"].mean() - raw["one_sided_book"].mean()),
            ("mean_spread", raw["spread"].mean(), plat["spread"].mean(), plat["spread"].mean() - raw["spread"].mean()),
            ("mean_book_total_volume", raw["book_total_volume"].mean(), plat["book_total_volume"].mean(), plat["book_total_volume"].mean() - raw["book_total_volume"].mean()),
            ("mid_std", raw["mid_price"].std(), plat["mid_price"].std(), plat["mid_price"].std() - raw["mid_price"].std()),
        ]
        for metric, sample_value, platform_value, diff in metrics:
            verdict = "yes"
            if metric == "rows":
                verdict = "no"
            elif metric == "overlap_rows":
                verdict = "yes" if platform_value >= 900 else "unclear"
            elif isinstance(diff, (int, float, np.floating)) and not pd.isna(diff):
                verdict = "yes" if abs(diff) < max(1e-9, abs(sample_value) * 0.20 if sample_value else 1.0) else "unclear"
            rows.append(
                {
                    "product": product,
                    "metric": metric,
                    "sample_value": sample_value,
                    "platform_value": platform_value,
                    "difference": diff,
                    "verdict": verdict,
                    "notes": "Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines.",
                }
            )

    rows.append(
        {
            "product": "ALL",
            "metric": "platform_profit",
            "sample_value": np.nan,
            "platform_value": platform.get("profit"),
            "difference": np.nan,
            "verdict": "not_applicable",
            "notes": "No-trade diagnostic logger, so PnL is not alpha evidence.",
        }
    )
    rows.append(
        {
            "product": "ALL",
            "metric": "graph_rows",
            "sample_value": np.nan,
            "platform_value": len(platform_graph),
            "difference": np.nan,
            "verdict": "yes" if len(platform_graph) == 500 else "unclear",
            "notes": "Expected PnL graph is flat for no-trade logger.",
        }
    )
    return pd.DataFrame(rows)


def fair_value_reference(prices: pd.DataFrame) -> pd.Series:
    refs = pd.Series(index=prices.index, dtype=float)
    for (product, day), df in prices.groupby(["product", "day"]):
        idx = df.index
        usable = df[df["mid_price"].notna()]
        if product == "INTARIAN_PEPPER_ROOT" and len(usable) >= 10:
            lr = stats.linregress(usable["timestamp"], usable["mid_price"])
            refs.loc[idx] = lr.intercept + lr.slope * df["timestamp"]
        else:
            refs.loc[idx] = df["mid_price"].rolling(100, min_periods=20).mean()
            refs.loc[idx] = refs.loc[idx].fillna(df["mid_price"].expanding(min_periods=1).mean())
    return refs


def market_access_fee_scenarios(prices: pd.DataFrame) -> pd.DataFrame:
    data = prices.copy()
    data["fair_value_proxy"] = fair_value_reference(data)
    data["buy_edge"] = data["fair_value_proxy"] - data["ask_price_1"]
    data["sell_edge"] = data["bid_price_1"] - data["fair_value_proxy"]
    rows: list[dict[str, Any]] = []
    thresholds = [0, 1, 2, 3, 5]
    capture_rates = [0.01, 0.025, 0.05, 0.10]
    for threshold in thresholds:
        buy_value = (
            data.loc[data["buy_edge"] > threshold, "buy_edge"]
            * data.loc[data["buy_edge"] > threshold, "top_ask_volume"]
        ).sum()
        sell_value = (
            data.loc[data["sell_edge"] > threshold, "sell_edge"]
            * data.loc[data["sell_edge"] > threshold, "top_bid_volume"]
        ).sum()
        gross = float(buy_value + sell_value)
        incremental_gross = gross * 0.25
        for capture_rate in capture_rates:
            proxy = incremental_gross * capture_rate
            rows.append(
                {
                    "edge_threshold": threshold,
                    "gross_edge_opportunity": gross,
                    "extra_access_incremental_gross_proxy": incremental_gross,
                    "capture_rate_assumption": capture_rate,
                    "incremental_pnl_proxy": proxy,
                    "break_even_bid_proxy": proxy,
                    "conservative_bid_floor": 0,
                    "conservative_bid_ceiling": math.floor(proxy * 0.5),
                    "caveat": "Proxy only: bid acceptance depends on competitors; testing ignores bid().",
                }
            )
    return pd.DataFrame(rows)


def research_value(research_pct: np.ndarray | float) -> np.ndarray | float:
    return 200_000 * np.log1p(research_pct) / np.log1p(100)


def scale_value(scale_pct: np.ndarray | float) -> np.ndarray | float:
    return 7 * np.asarray(scale_pct) / 100


def speed_multiplier(speed_pct: np.ndarray, scenario: str) -> np.ndarray:
    x = np.asarray(speed_pct, dtype=float) / 100
    if scenario == "pessimistic_rank_proxy":
        return 0.1 + 0.8 * np.power(x, 1.5)
    if scenario == "optimistic_rank_proxy":
        return 0.1 + 0.8 * np.sqrt(x)
    return 0.1 + 0.8 * x


def manual_scenarios() -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for scenario in [
        "pessimistic_rank_proxy",
        "linear_rank_proxy",
        "optimistic_rank_proxy",
    ]:
        for research in range(0, 101):
            for scale in range(0, 101 - research):
                max_speed = 100 - research - scale
                for speed in range(0, max_speed + 1):
                    speed_mult = float(speed_multiplier(np.array([speed]), scenario)[0])
                    budget_used = 50_000 * (research + scale + speed) / 100
                    pnl = float(research_value(research) * scale_value(scale) * speed_mult - budget_used)
                    rows.append(
                        {
                            "scenario": scenario,
                            "research_pct": research,
                            "scale_pct": scale,
                            "speed_pct": speed,
                            "speed_multiplier_assumption": speed_mult,
                            "budget_used": budget_used,
                            "manual_pnl_proxy": pnl,
                        }
                    )
    grid = pd.DataFrame(rows)
    top = (
        grid.sort_values(["scenario", "manual_pnl_proxy"], ascending=[True, False])
        .groupby("scenario")
        .head(20)
        .reset_index(drop=True)
    )
    summary = (
        grid.groupby("scenario", as_index=False)
        .agg(
            best_manual_pnl_proxy=("manual_pnl_proxy", "max"),
            median_manual_pnl_proxy=("manual_pnl_proxy", "median"),
            q95_manual_pnl_proxy=("manual_pnl_proxy", lambda s: s.quantile(0.95)),
            evaluated_allocations=("manual_pnl_proxy", "size"),
        )
        .merge(
            top.groupby("scenario", as_index=False)
            .head(1)[
                [
                    "scenario",
                    "research_pct",
                    "scale_pct",
                    "speed_pct",
                    "speed_multiplier_assumption",
                    "budget_used",
                    "manual_pnl_proxy",
                ]
            ],
            on="scenario",
            how="left",
        )
    )
    return summary, top


def round1_assumption_check(behavior: pd.DataFrame, ic: pd.DataFrame, trades_summary: pd.DataFrame) -> pd.DataFrame:
    ipr = behavior[behavior["product"] == "INTARIAN_PEPPER_ROOT"]
    aco = behavior[behavior["product"] == "ASH_COATED_OSMIUM"]
    ipr_drift = ipr["total_change"].mean()
    ipr_r2 = ipr["linear_r2"].mean()
    aco_delta_ac1 = aco["delta_ac1"].mean()
    aco_std = aco["mid_std"].mean()
    top_ic_h1 = ic[(ic["feature"] == "top_imbalance") & (ic["horizon_ticks"] == 1)]
    top_ic_mean = top_ic_h1["pearson_corr"].mean()
    rows = [
        {
            "assumption_or_hint": "IPR is steady from Round 1 hint",
            "round2_evidence": f"Mean day total change {ipr_drift:.2f}, mean linear R2 {ipr_r2:.3f}.",
            "verdict": "contradicted" if abs(ipr_drift) > 100 and ipr_r2 > 0.8 else "unknown",
            "downstream_action": "Model current-round drift explicitly before using any fixed fair value.",
        },
        {
            "assumption_or_hint": "IPR may have stable drift/residual structure",
            "round2_evidence": f"Mean linear R2 {ipr_r2:.3f}; residual std mean {ipr['linear_residual_std'].mean():.2f}.",
            "verdict": "supported" if ipr_r2 > 0.95 else "weakened",
            "downstream_action": "Consider drift plus residual features in understanding, with validation on all days.",
        },
        {
            "assumption_or_hint": "ACO is volatile or patterned",
            "round2_evidence": f"Mean mid std {aco_std:.2f}; mean delta AC1 {aco_delta_ac1:.3f}.",
            "verdict": "supported" if aco_delta_ac1 < -0.25 else "unknown",
            "downstream_action": "Consider short-horizon mean-reversion evidence, not a broad volatility claim.",
        },
        {
            "assumption_or_hint": "Book imbalance can help predict short horizon movement",
            "round2_evidence": f"Mean IC@1 for top imbalance {top_ic_mean:.3f}.",
            "verdict": "supported" if top_ic_mean > 0.10 else "weakened",
            "downstream_action": "Promote only if stable by product/day and still online-usable.",
        },
        {
            "assumption_or_hint": "Round 1 trade frequency/fill assumptions carry forward",
            "round2_evidence": f"Trade rows by product/day exist but market flow is sparse: mean rows {trades_summary['trade_rows'].mean():.1f}.",
            "verdict": "unknown",
            "downstream_action": "Do not carry fill assumptions; use Round 2 platform validation later.",
        },
    ]
    return pd.DataFrame(rows)


def feature_inventory(
    behavior: pd.DataFrame,
    ic: pd.DataFrame,
    comparability: pd.DataFrame,
    trades_summary: pd.DataFrame,
) -> pd.DataFrame:
    ic_means = (
        ic.groupby(["feature", "horizon_ticks"], as_index=False)["pearson_corr"]
        .mean()
        .rename(columns={"pearson_corr": "mean_ic"})
    )
    top_ic_1 = ic_means[(ic_means["feature"] == "top_imbalance") & (ic_means["horizon_ticks"] == 1)]["mean_ic"].mean()
    book_ic_1 = ic_means[(ic_means["feature"] == "book_imbalance") & (ic_means["horizon_ticks"] == 1)]["mean_ic"].mean()
    ipr_r2 = behavior[behavior["product"] == "INTARIAN_PEPPER_ROOT"]["linear_r2"].mean()
    aco_delta_ac1 = behavior[behavior["product"] == "ASH_COATED_OSMIUM"]["delta_ac1"].mean()
    spread_q95 = behavior["spread_q95"].mean()
    one_sided_rate = behavior["one_sided_rate"].mean()
    platform_rows = comparability[
        (comparability["metric"] == "overlap_rows")
    ]["platform_value"].min()

    rows = [
        {
            "feature": "IPR drift plus residual",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "Linear current-round IPR drift with smaller residual variation.",
            "role": "direct signal",
            "signal_strength": "strong" if ipr_r2 > 0.95 else "medium",
            "stability": "stable" if ipr_r2 > 0.95 else "day-sensitive",
            "actionability": "changes strategy",
            "lifecycle_decision": "promote" if ipr_r2 > 0.95 else "exploratory",
            "notes_caveats": f"Mean linear R2 {ipr_r2:.3f}; must avoid sample-end assumptions.",
        },
        {
            "feature": "ACO short-horizon mean reversion",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "ACO mid deltas tend to reverse at lag 1.",
            "role": "direct signal",
            "signal_strength": "strong" if aco_delta_ac1 < -0.35 else "medium",
            "stability": "stable" if aco_delta_ac1 < -0.25 else "unknown",
            "actionability": "changes strategy",
            "lifecycle_decision": "promote" if aco_delta_ac1 < -0.25 else "exploratory",
            "notes_caveats": f"Mean delta AC1 {aco_delta_ac1:.3f}; needs execution validation.",
        },
        {
            "feature": "top imbalance",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "Best-level bid/ask volume skew.",
            "role": "direct signal",
            "signal_strength": "strong" if top_ic_1 > 0.20 else "medium" if top_ic_1 > 0.10 else "weak",
            "stability": "stable",
            "actionability": "changes parameters",
            "lifecycle_decision": "promote" if top_ic_1 > 0.10 else "exploratory",
            "notes_caveats": f"Mean IC@1 {top_ic_1:.3f}; test conditional stability.",
        },
        {
            "feature": "full-book imbalance",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "Three-level total bid/ask depth skew.",
            "role": "direct signal",
            "signal_strength": "strong" if book_ic_1 > 0.20 else "medium" if book_ic_1 > 0.10 else "weak",
            "stability": "stable",
            "actionability": "changes parameters",
            "lifecycle_decision": "promote" if book_ic_1 > 0.10 else "exploratory",
            "notes_caveats": f"Mean IC@1 {book_ic_1:.3f}; top imbalance may be simpler.",
        },
        {
            "feature": "spread regime",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "Wide/tight spread state from best bid/ask.",
            "role": "execution filter",
            "signal_strength": "medium" if spread_q95 > 0 else "weak",
            "stability": "day-sensitive",
            "actionability": "changes validation",
            "lifecycle_decision": "exploratory",
            "notes_caveats": f"Mean spread q95 {spread_q95:.2f}; filter needs PnL validation.",
        },
        {
            "feature": "liquidity/depth regime",
            "origin": "csv",
            "online_usability": "usable online",
            "meaning": "Total visible depth and one-sided-book conditions.",
            "role": "risk control",
            "signal_strength": "medium",
            "stability": "regime-dependent",
            "actionability": "changes risk",
            "lifecycle_decision": "exploratory",
            "notes_caveats": f"Mean one-sided rate {one_sided_rate:.3f}; use defensively first.",
        },
        {
            "feature": "trade pressure proxy",
            "origin": "combined",
            "online_usability": "usable online",
            "meaning": "Trade price relative to mid signs recent flow.",
            "role": "diagnostic",
            "signal_strength": "weak",
            "stability": "unknown",
            "actionability": "changes validation",
            "lifecycle_decision": "needs logs",
            "notes_caveats": f"Mean trade rows per product/day {trades_summary['trade_rows'].mean():.1f}; needs platform market_trades logs.",
        },
        {
            "feature": "platform quote-subset comparability",
            "origin": "log/post-run",
            "online_usability": "EDA-only",
            "meaning": "Difference between sample day 1 and platform activitiesLog quote subset.",
            "role": "diagnostic",
            "signal_strength": "medium" if platform_rows >= 900 else "weak",
            "stability": "unknown",
            "actionability": "changes validation",
            "lifecycle_decision": "EDA-only calibration",
            "notes_caveats": f"Platform overlap rows min {platform_rows}; no printed state probe lines.",
        },
    ]
    return pd.DataFrame(rows)


def promotion_decisions(features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in features.iterrows():
        decision = row["lifecycle_decision"]
        if decision == "promote":
            destination = "Understanding / strategy candidates"
            reason = f"{row['signal_strength']} signal, {row['stability']} stability, {row['actionability']}."
        elif decision == "EDA-only calibration":
            destination = "Validation planning"
            reason = "Diagnostic evidence affects comparability, not bot logic."
        elif decision == "needs logs":
            destination = "Future platform diagnostics"
            reason = "Sample trades are insufficient for implementation decisions."
        else:
            destination = "EDA report only"
            reason = "Potentially useful but not ready for spec or implementation."
        rows.append(
            {
                "feature_or_signal": row["feature"],
                "decision": decision,
                "destination": destination,
                "reason": reason,
                "caveat_reopen_condition": row["notes_caveats"],
            }
        )
    return pd.DataFrame(rows)


def make_plots(
    prices: pd.DataFrame,
    behavior: pd.DataFrame,
    ic: pd.DataFrame,
    maf: pd.DataFrame,
    manual_top: pd.DataFrame,
    comparability: pd.DataFrame,
) -> list[Path]:
    plot_paths: list[Path] = []

    plt.figure(figsize=(11, 6))
    for product in PRODUCTS:
        subset = prices[prices["product"] == product]
        for day, df in subset.groupby("day"):
            plt.plot(df["timestamp"], df["mid_price"], label=f"{product} day {day}", alpha=0.75)
    plt.title("Round 2 mid price by product/day")
    plt.xlabel("timestamp")
    plt.ylabel("mid_price")
    plt.legend(fontsize=7)
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_mid_price_by_product_day.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    for product in PRODUCTS:
        subset = prices[prices["product"] == product]["spread"].dropna()
        plt.hist(subset, bins=40, alpha=0.55, label=product)
    plt.title("Spread distribution")
    plt.xlabel("spread")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_spread_distribution.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    for product in PRODUCTS:
        subset = prices[prices["product"] == product]["mid_delta_1"].dropna()
        plt.hist(subset, bins=80, alpha=0.55, label=product)
    plt.title("One-tick mid delta distribution")
    plt.xlabel("delta mid")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_returns_distribution.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    ic_plot = (
        ic[ic["feature"].isin(["top_imbalance", "book_imbalance"])]
        .groupby(["feature", "horizon_ticks"], as_index=False)["pearson_corr"]
        .mean()
    )
    for feature, df in ic_plot.groupby("feature"):
        plt.plot(df["horizon_ticks"], df["pearson_corr"], marker="o", label=feature)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Mean imbalance IC by horizon")
    plt.xlabel("future horizon ticks")
    plt.ylabel("Pearson IC")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_imbalance_ic.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    rows_metric = comparability[comparability["metric"].isin(["mean_spread", "mean_book_total_volume", "mid_std"])]
    x = np.arange(len(rows_metric))
    plt.bar(x - 0.18, rows_metric["sample_value"], width=0.36, label="sample")
    plt.bar(x + 0.18, rows_metric["platform_value"], width=0.36, label="platform")
    plt.xticks(x, rows_metric["product"] + " " + rows_metric["metric"], rotation=45, ha="right")
    plt.title("Platform vs sample comparability")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_platform_comparability.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    maf_plot = maf[maf["edge_threshold"].isin([0, 2, 5])]
    for threshold, df in maf_plot.groupby("edge_threshold"):
        plt.plot(
            df["capture_rate_assumption"],
            df["incremental_pnl_proxy"],
            marker="o",
            label=f"edge>{threshold}",
        )
    plt.title("MAF incremental PnL proxy scenarios")
    plt.xlabel("capture rate assumption")
    plt.ylabel("incremental pnl proxy")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_maf_scenarios.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    best = manual_top.groupby("scenario", as_index=False).head(1)
    labels = best["scenario"]
    x = np.arange(len(best))
    plt.bar(x, best["manual_pnl_proxy"])
    plt.xticks(x, labels, rotation=20, ha="right")
    plt.title("Best manual allocation by speed rank scenario")
    plt.ylabel("manual pnl proxy")
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_manual_scenarios.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    plt.figure(figsize=(10, 5))
    for product in PRODUCTS:
        df = behavior[behavior["product"] == product].sort_values("day")
        plt.plot(df["day"], df["linear_residual_std"], marker="o", label=product)
    plt.title("Linear residual std by product/day")
    plt.xlabel("day")
    plt.ylabel("residual std")
    plt.legend()
    plt.tight_layout()
    path = ARTIFACT_DIR / "plot_drift_residuals.png"
    plt.savefig(path, dpi=140)
    plt.close()
    plot_paths.append(path)

    return plot_paths


def md_table(df: pd.DataFrame, max_rows: int = 10, cols: list[str] | None = None) -> str:
    if df.empty:
        return "_No rows._"
    view = df.copy()
    if cols is not None:
        view = view[cols]
    view = view.head(max_rows)
    formatted = []
    for _, row in view.iterrows():
        item = {}
        for col, val in row.items():
            if isinstance(val, float):
                item[col] = "" if pd.isna(val) else f"{val:.4g}"
            else:
                item[col] = "" if pd.isna(val) else str(val)
        formatted.append(item)
    headers = list(view.columns)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in formatted:
        lines.append("| " + " | ".join(str(row[col]).replace("\n", " ") for col in headers) + " |")
    return "\n".join(lines)


def top_signal_summary(features: pd.DataFrame) -> tuple[list[str], list[str], list[str]]:
    promoted = features[features["lifecycle_decision"] == "promote"]["feature"].tolist()
    exploratory = features[features["lifecycle_decision"] == "exploratory"]["feature"].tolist()
    avoid = features[features["lifecycle_decision"].isin(["needs logs", "negative evidence", "reject"])]["feature"].tolist()
    return promoted, exploratory, avoid


def write_report(
    paths: dict[str, Path],
    data_quality_df: pd.DataFrame,
    behavior: pd.DataFrame,
    assumption_check: pd.DataFrame,
    ic: pd.DataFrame,
    conditional_ic: pd.DataFrame,
    trade_summary: pd.DataFrame,
    platform_comp: pd.DataFrame,
    maf: pd.DataFrame,
    manual_top: pd.DataFrame,
    features: pd.DataFrame,
    promotions: pd.DataFrame,
    plot_paths: list[Path],
    platform: dict[str, Any],
) -> None:
    promoted, exploratory, avoid = top_signal_summary(features)
    top_manual = manual_top.groupby("scenario", as_index=False).head(3)
    best_maf = maf.sort_values("incremental_pnl_proxy", ascending=False).head(5)
    ic_summary = (
        ic[ic["feature"].isin(["top_imbalance", "book_imbalance"])]
        .groupby(["feature", "horizon_ticks"], as_index=False)
        .agg(mean_ic=("pearson_corr", "mean"), min_ic=("pearson_corr", "min"), max_ic=("pearson_corr", "max"))
    )
    product_scope = pd.DataFrame(
        [
            {
                "Product": "ASH_COATED_OSMIUM",
                "Present In Data": "yes",
                "Usable Evidence": "yes",
                "Likely Trader Scope": "likely",
                "Decision": "include",
            },
            {
                "Product": "INTARIAN_PEPPER_ROOT",
                "Present In Data": "yes",
                "Usable Evidence": "yes",
                "Likely Trader Scope": "likely",
                "Decision": "include",
            },
        ]
    )
    algorithmic_scope = pd.DataFrame(
        [
            {
                "Finding": "Product signals from price/order-book CSVs",
                "Scope": "algorithmic",
                "Why": "Fields map to TradingState order_depths/mid proxies.",
                "Caveat": "Sample data evidence is not an official rule.",
            },
            {
                "Finding": "Market Access Fee scenarios",
                "Scope": "algorithmic / final-round decision",
                "Why": "Trader.bid() is Round 2-specific.",
                "Caveat": "Testing ignores bid(); competitor bid distribution unknown.",
            },
            {
                "Finding": "Research / Scale / Speed grid",
                "Scope": "manual",
                "Why": "Manual challenge allocation outside Trader.run().",
                "Caveat": "Speed multiplier is rank-based and unknown before close.",
            },
        ]
    )
    artifact_rows = []
    for label, path in paths.items():
        artifact_rows.append(
            {
                "Artifact Path": rel(path),
                "Type": "report" if path.suffix == ".md" else "table/json",
                "Source Data": "Round 2 raw CSVs / platform JSON",
                "Useful For": label,
                "Decision-Relevant?": "yes",
            }
        )
    for path in plot_paths:
        artifact_rows.append(
            {
                "Artifact Path": rel(path),
                "Type": "plot",
                "Source Data": "Round 2 derived EDA tables",
                "Useful For": path.stem.replace("plot_", ""),
                "Decision-Relevant?": "yes",
            }
        )
    artifacts = pd.DataFrame(artifact_rows)

    text = f"""# Round 2 Fresh EDA

## Status

READY_FOR_REVIEW

## Question

- Question: Which Round 2 product, market-access, validation, and manual-allocation signals are decision-useful enough to feed understanding and later strategy/spec work?
- Product scope: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Why this matters downstream: this is the evidence gate before strategy generation; no bot logic is implemented here.

## Product Scope

{md_table(product_scope)}

- Product-scope rationale: both products are official Round 2 algorithmic products with limit 80.
- Product branches: one combined EDA, with product-specific rows where behavior differs materially.

## Algorithmic vs Manual Scope

{md_table(algorithmic_scope)}

## Data Sources

- Raw data: `rounds/round_2/data/raw/prices_round_2_day_-1.csv`, `day_0`, `day_1`, plus matching trades files.
- Processed data: tables and plots in `rounds/round_2/workspace/01_eda/artifacts/`.
- Run or log artifact: `rounds/round_2/performances/noel/historical/baseline_state_logger.json`.
- Post-run research memory: absent at EDA start; expected because Round 2 has no prior validated bot run cycle.

## Round Adaptation Check

| Check | Current-Round Evidence | Decision / Action |
| --- | --- | --- |
| Active round mechanics/API | Round 2 wiki defines `Trader.bid()` for Market Access Fee | EDA-only value estimate; final bid belongs to strategy/spec |
| Products and limits | Round 2 wiki: ACO/IPR, limit 80 each | verified |
| Data schema | raw CSVs and platform `activitiesLog` share price ladder schema | classified |
| New or changed fields/mechanics | Market Access Fee, randomized 80% testing quotes, manual RSS allocation | EDA questions included |
| Prior-round assumption at risk | Round 1 product hints and bot constants | revalidate; do not carry as facts |

## Artifact Index

{md_table(artifacts, max_rows=40)}

## Data Quality And Filters

- Row counts by file and product: see `{rel(paths['data_quality'])}`.
- Timestamp coverage and gaps: raw prices cover three days with 10,000 rows per product/day; platform activities cover 1,000 rows per product on day 1.
- Missing bid/ask counts: measured in data quality and comparability tables; one-sided books are preserved, not dropped globally.
- Zero or blank `mid_price` counts: measured; non-positive mids are treated as missing for analysis.
- Filters applied: signal IC uses rows with non-null feature and future mid; product stats use available mid rows; platform comparison uses overlapping timestamps.
- Findings based on: mixed raw rows and filtered rows, stated per table.
- Data quality caveats: the platform `.log` is empty and the JSON does not contain `ROUND2_STATE_PROBE`; treat it as platform activity evidence, not raw printed state evidence.

{md_table(data_quality_df, max_rows=12)}

## Round 1 Assumption Check

{md_table(assumption_check, max_rows=10)}

## Feature Inventory

{md_table(features, max_rows=12)}

## Feature Engineering Notes

| Transformation Or Feature | Purpose | Gate Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| Linear drift + residual | Test IPR level behavior without fixed fair value | strong signal/stability for IPR | yes | Validate in strategy replay/platform |
| Mid delta autocorrelation | Test ACO short-horizon reversal | actionable if stable across days | yes | Validate execution costs and inventory behavior |
| Top/full-book imbalance | Test online order-book pressure | positive IC if stable by day/product | yes | Compare top vs full-book simplicity |
| Spread/liquidity regimes | Detect execution/risk filters | exploratory; may change validation | maybe | Test in specs only after PnL evidence |
| Trade pressure proxy | Check market-trade flow | weak/needs logs | maybe | Need platform market_trades diagnostics |
| MAF gross edge proxy | Bound extra access value | EDA-only calibration | yes | Human risk posture and platform evidence |

## Feature Promotion Decisions

{md_table(promotions, max_rows=12)}

## Analyses Run

- Reproduction notes: run `.venv/bin/python rounds/round_2/workspace/01_eda/eda_round2_fresh.py`.
- Research tools used and why: pandas/numpy for tables/features; scipy/statsmodels for regressions, correlations, ARCH checks; ruptures for lightweight change-point scanning where available; matplotlib for plots.
- Research tools considered but skipped: sklearn/numba/polars were unnecessary for the current data size and would not change decisions.
- Output artifacts: see Artifact Index.
- Descriptive stats: product/day behavior table.
- Distribution checks: mid, returns, spreads, depth, trade size.
- Volatility/regime checks: rolling vol, ARCH p-values, change-point index candidates.
- Spread/microstructure checks: spread, depth, one-sided books, imbalance.
- Correlation/lead-lag checks: imbalance IC at horizons 1, 2, 3, 5, 10.
- Price vs trade alignment: trade price relative to same-timestamp mid.
- Volume behavior: trade counts, quantities, burst proxies.
- Order book dynamics: top/full-book imbalance and liquidity regimes.

## Research Tool Notes

- Tools that changed a decision: scipy/statsmodels supported drift/IC/ARCH evidence; matplotlib made comparability and scenario artifacts reviewable.
- Tools that were unnecessary: sklearn, numba, polars.
- Risk of overfitting or over-modeling: MAF and manual scenarios are proxies, not official predictions; no final strategy decision is made here.

## Product Behavior Summary

{md_table(behavior, max_rows=12, cols=['product', 'day', 'mid_first', 'mid_last', 'total_change', 'linear_r2', 'linear_residual_std', 'delta_ac1', 'spread_mean', 'one_sided_rate'])}

## Imbalance Signal Summary

{md_table(ic_summary, max_rows=20)}

## Trades And Flow Summary

{md_table(trade_summary, max_rows=12)}

## Platform Logger / Validation Comparability

The available logger JSON is a no-trade platform result with status `{platform.get('status')}`, profit `{platform.get('profit')}`, 2,000 activity rows, and no `ROUND2_STATE_PROBE` printed-state lines. It is useful for quote-subset comparability, not alpha.

{md_table(platform_comp, max_rows=20)}

## Market Access Fee Value Estimation

This is an EDA-only proxy. It estimates gross executable-looking edge under simple fair-value references, then applies 25% extra access and capture-rate scenarios. It does not decide a final bid.

{md_table(best_maf, max_rows=8)}

## Manual Research / Scale / Speed Scenario Analysis

The grid uses official Research and Scale formulas. Speed multiplier scenarios are rank-outcome proxies because actual rank is competitor-dependent.

{md_table(top_manual, max_rows=12)}

## Distribution Hypotheses

| Product Or Scope | Hypothesis | Evidence | Strategy Implication | Caveat |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | trending / drift plus residual | high linear fit across days | consider drift-aware fair value | avoid hardcoding sample-end or day constants |
| `ASH_COATED_OSMIUM` | short-horizon mean-reverting/noisy | negative delta autocorrelation | consider reversal-style evidence | must validate after spread and fills |
| Order book | imbalance predictive | positive IC tables | candidate signal input | stability by day/product matters |
| Platform validation | quote subset comparable but not identical | platform vs sample table | use platform run cautiously | 80% quote randomization can move results |

## Facts

- Wiki fact: Round 2 algorithmic products are `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, limit 80 each.
- Wiki fact: `Trader.bid()` is Round 2-specific for Market Access Fee; testing ignores `bid()`.
- Wiki fact: manual Research / Scale / Speed allocation is separate from `Trader.run()`.

## Conditional Patterns / Regimes

{md_table(conditional_ic, max_rows=20)}

## Threshold / Execution Findings

| Finding | Feature Basis | Threshold Or Zone | Execution / Risk Use | Readiness | Caveat |
| --- | --- | --- | --- | --- | --- |
| Wider spreads and one-sided books exist | spread, one-sided flags | product/day dependent | likely execution/risk filter | exploratory | needs PnL validation |
| Imbalance IC persists at short horizons | top/full-book imbalance | horizons 1-5 | direct signal candidate | usable | confirm in strategy validation |
| Extra access value is bounded by capture rate | MAF proxy | edge threshold and capture rate | MAF bid calibration | EDA-only | competitor bid distribution unknown |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift + residual | timestamp, mid/order book | current-round level is not fixed | prevents stale Round 1 fixed FV | fair-value candidate | stable in sample | strong | avoid sample-day constants |
| ACO short-horizon reversal | mid deltas/order book | price changes often reverse | possible market-making/reversion edge | fair-value adjustment | stable in sample | medium | execution costs unknown |
| Book imbalance | top/full depth | visible liquidity predicts near move | online signal from order_depths | signal/skew candidate | stable enough for candidate queue | medium/strong | exact sizing needs validation |

## Negative Evidence

| Idea Or Signal | Why It Was Plausible | Evidence Against It | When To Reopen |
| --- | --- | --- | --- |
| Carry Round 1 fixed IPR fair value | Round 1 hint called IPR steady | Round 2 drift evidence contradicts fixed value | only with new final/platform evidence |
| Treat diagnostic logger PnL as meaningful | platform JSON has profit field | bot intentionally does not trade, profit is 0 | never for alpha; use only as quote evidence |
| Use trade pressure directly in first spec | market trades exist | sparse sample evidence and no printed state probe | after platform logs include market_trades dynamics |

## Assumptions

- MAF capture rates are scenario assumptions, not official mechanics.
- Manual Speed multiplier scenarios are rank proxies, not predictions.
- Platform activitiesLog is treated as 80% quote-subset evidence because Round 2 docs say testing uses default quotes and ignores bid().

## Open Questions

- Exact Round 2 deadline remains unknown.
- Competitive Market Access Fee bid distribution is unknown.
- Manual Speed rank outcome is unknown.
- Platform market_trades behavior from printed `TradingState` logs is still missing because the saved JSON did not include `ROUND2_STATE_PROBE`.

## Signal Strength And Uncertainty

- Strength: medium to strong for IPR drift, ACO short-horizon reversal, and imbalance; weak for trade pressure.
- Evidence: three raw sample days plus one no-trade platform activitiesLog.
- Uncertainty: sample data may differ from final simulation; platform testing quote subset is randomized.

## Downstream Use / Agent Notes

- Strong enough to consider: {', '.join(promoted) if promoted else 'none'}.
- Exploratory only: {', '.join(exploratory) if exploratory else 'none'}.
- Do not use yet: {', '.join(avoid) if avoid else 'none'}.
- Additional validation needed: strategy candidates must test whether promoted signals survive execution, position limits, randomized quote subsets, and platform PnL.
- How understanding should use this: compress promoted signals, caveats, and Round 1 assumption changes.
- How strategy generation should use this: generate a bounded candidate set around drift/residual, ACO reversal, imbalance, and conservative execution filters.
- How specification should use this: specify only online-usable fields and avoid CSV/day-specific constants.
- How implementation should use this: do not implement until a reviewed spec exists.
- How testing/debugging should use this: use platform comparability caveat and track run variance.

## Reusable Metrics

- `spread`, `top_imbalance`, `book_imbalance`, `book_total_volume`, `one_sided_book`, `mid_delta_1`, `rolling_vol_50`, `z_mid_50`, fair-value residual, trade pressure proxy.

## Strategy Implications

- What this changes: Round 2 should not inherit a fixed Round 1 view of IPR; ACO and imbalance signals deserve strategy consideration; MAF/manual decisions need scenario framing.
- If not actionable, say why: trade pressure and exact MAF bid are not ready because platform state logs and competitor bid distribution are missing.

## Interpretation Limits

- EDA is evidence, not a strategy.
- Sample data patterns are not official rules.
- Platform logger result is no-trade and cannot measure alpha.
- MAF and manual allocations are scenario analyses, not final submissions.

## Next Action

- Move to understanding synthesis after human review, then generate a small strategy candidate set grounded in the promoted signals and caveats above.
"""
    REPORT_PATH.write_text(text, encoding="utf-8")


def write_manifest(paths: dict[str, Path], plot_paths: list[Path]) -> Path:
    manifest = {
        "report": rel(REPORT_PATH),
        "tables": {key: rel(path) for key, path in sorted(paths.items())},
        "plots": [rel(path) for path in plot_paths],
    }
    return save_json(manifest, "artifact_manifest.json")


def main() -> None:
    ensure_dirs()
    prices_raw = read_prices()
    prices = add_book_features(prices_raw)
    trades = read_trades()
    platform = read_platform_json()
    platform_activities_raw = read_platform_activities(platform)
    platform_activities = add_book_features(platform_activities_raw) if not platform_activities_raw.empty else pd.DataFrame()
    platform_graph = read_platform_graph(platform)

    dq = data_quality(prices, trades, platform, platform_activities)
    behavior = product_behavior(prices)
    ic = imbalance_ic(prices)
    cond_ic = conditional_imbalance_ic(prices)
    trade_summary, trade_pressure = trade_flow(trades, prices)
    platform_comp = platform_comparability(prices, platform_activities, platform_graph, platform)
    maf = market_access_fee_scenarios(prices)
    manual_summary, manual_top = manual_scenarios()
    assumption = round1_assumption_check(behavior, ic, trade_summary)
    features = feature_inventory(behavior, ic, platform_comp, trade_summary)
    promotions = promotion_decisions(features)

    paths = {
        "data_quality": save_csv(dq, "data_quality_summary.csv"),
        "product_behavior": save_csv(behavior, "product_behavior_summary.csv"),
        "round1_assumption_check": save_csv(assumption, "round1_assumption_check.csv"),
        "imbalance_ic": save_csv(ic, "imbalance_ic.csv"),
        "conditional_imbalance_ic": save_csv(cond_ic, "conditional_imbalance_ic.csv"),
        "trade_flow_summary": save_csv(trade_summary, "trade_flow_summary.csv"),
        "trade_pressure_proxy": save_csv(trade_pressure, "trade_pressure_proxy.csv"),
        "platform_comparability": save_csv(platform_comp, "platform_comparability.csv"),
        "maf_scenarios": save_csv(maf, "maf_scenarios.csv"),
        "manual_scenario_grid_top": save_csv(manual_top, "manual_scenario_grid_top.csv"),
        "manual_scenario_summary": save_csv(manual_summary, "manual_scenario_summary.csv"),
        "feature_inventory": save_csv(features, "feature_inventory.csv"),
        "feature_promotion_decisions": save_csv(promotions, "feature_promotion_decisions.csv"),
    }

    plot_paths = make_plots(prices, behavior, ic, maf, manual_top, platform_comp)
    paths["artifact_manifest"] = write_manifest(paths, plot_paths)

    write_report(
        paths=paths,
        data_quality_df=dq,
        behavior=behavior,
        assumption_check=assumption,
        ic=ic,
        conditional_ic=cond_ic,
        trade_summary=trade_summary,
        platform_comp=platform_comp,
        maf=maf,
        manual_top=manual_top,
        features=features,
        promotions=promotions,
        plot_paths=plot_paths,
        platform=platform,
    )

    print(f"Wrote report: {rel(REPORT_PATH)}")
    print(f"Wrote artifacts: {rel(ARTIFACT_DIR)}")


if __name__ == "__main__":
    main()
