from __future__ import annotations

import io
import json
import math
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("MPLCONFIGDIR", "/tmp/simplex_round2_mplconfig")
os.environ.setdefault("LOKY_MAX_CPU_COUNT", "8")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.diagnostic import het_arch
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

try:
    import statsmodels.api as sm
except Exception:  # pragma: no cover - research dependency guard
    sm = None

try:
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.feature_selection import mutual_info_regression
    from sklearn.preprocessing import StandardScaler
except Exception:  # pragma: no cover - optional research dependency guard
    KMeans = None
    PCA = None
    StandardScaler = None
    mutual_info_regression = None

try:
    import ruptures as rpt
except Exception:  # pragma: no cover - optional research dependency guard
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

BASE_FEATURES = [
    "spread",
    "relative_spread",
    "top_imbalance",
    "book_imbalance",
    "microprice_deviation",
    "top_total_volume",
    "book_total_volume",
    "depth_ratio",
    "missing_level_count",
    "one_sided_book_num",
    "mid_delta_lag1",
    "mid_delta_lag2",
    "rolling_vol_50",
    "rolling_vol_200",
    "z_mid_50",
    "drift_residual_z",
    "trade_count",
    "trade_quantity",
    "trade_pressure_qty",
]

REGRESSION_FEATURES = [
    "top_imbalance",
    "book_imbalance",
    "microprice_deviation",
    "spread",
    "book_total_volume",
    "mid_delta_lag1",
    "drift_residual_z",
    "trade_pressure_qty",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def ensure_dirs() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def line_count(path: Path) -> int:
    with path.open("r", encoding="utf-8") as handle:
        return sum(1 for _ in handle)


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
        day_token = path.stem.split("_day_")[-1]
        df["day"] = int(day_token)
        df["source_file"] = rel(path)
        df["source_line_count_incl_header"] = line_count(path)
        frames.append(df)
    trades = pd.concat(frames, ignore_index=True)
    trades = trades.rename(columns={"symbol": "product"})
    return coerce_numeric(trades, ["day", "timestamp", "price", "quantity"])


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
        (out["total_bid_volume"] - out["total_ask_volume"])
        / out["book_total_volume"],
        np.nan,
    )
    out["one_sided_book"] = out["has_best_bid"] ^ out["has_best_ask"]
    out["one_sided_book_num"] = out["one_sided_book"].astype(float)
    out["missing_level_count"] = out[bid_prices + ask_prices].isna().sum(axis=1)
    out["relative_spread"] = np.where(
        out["mid_price"].abs() > 0, out["spread"] / out["mid_price"], np.nan
    )
    out["depth_ratio"] = np.where(
        out["total_ask_volume"] > 0,
        out["total_bid_volume"] / out["total_ask_volume"],
        np.nan,
    )
    out["microprice"] = np.where(
        out["top_total_volume"] > 0,
        (
            out["ask_price_1"].fillna(out["mid_price"]) * out["top_bid_volume"]
            + out["bid_price_1"].fillna(out["mid_price"]) * out["top_ask_volume"]
        )
        / out["top_total_volume"],
        np.nan,
    )
    out["microprice_deviation"] = out["microprice"] - out["mid_price"]
    return out


def add_time_features(prices: pd.DataFrame) -> pd.DataFrame:
    out = prices.sort_values(["product", "day", "timestamp"]).copy()
    grouped = out.groupby(["product", "day"], sort=False)
    out["mid_delta_1"] = grouped["mid_price"].diff()
    out["mid_delta_lag1"] = grouped["mid_delta_1"].shift(1)
    out["mid_delta_lag2"] = grouped["mid_delta_1"].shift(2)
    for horizon in [1, 2, 3, 5, 10, 20, 50]:
        out[f"future_mid_delta_{horizon}"] = grouped["mid_price"].shift(-horizon) - out[
            "mid_price"
        ]
        out[f"future_return_{horizon}"] = (
            out[f"future_mid_delta_{horizon}"] / out["mid_price"]
        )
    out["rolling_mean_50"] = grouped["mid_price"].transform(
        lambda s: s.rolling(50, min_periods=20).mean()
    )
    out["rolling_std_50"] = grouped["mid_price"].transform(
        lambda s: s.rolling(50, min_periods=20).std()
    )
    out["rolling_vol_50"] = grouped["mid_delta_1"].transform(
        lambda s: s.rolling(50, min_periods=20).std()
    )
    out["rolling_vol_200"] = grouped["mid_delta_1"].transform(
        lambda s: s.rolling(200, min_periods=50).std()
    )
    out["z_mid_50"] = (out["mid_price"] - out["rolling_mean_50"]) / out[
        "rolling_std_50"
    ]
    return add_drift_residuals(out)


def add_drift_residuals(prices: pd.DataFrame) -> pd.DataFrame:
    frames = []
    for (_, _), grp in prices.groupby(["product", "day"], sort=False):
        grp = grp.copy()
        valid = grp[["timestamp", "mid_price"]].dropna()
        if len(valid) > 5:
            slope, intercept, r_value, _p_value, _stderr = stats.linregress(
                valid["timestamp"], valid["mid_price"]
            )
            fitted = intercept + slope * grp["timestamp"]
            grp["drift_fitted_mid"] = fitted
            grp["drift_residual"] = grp["mid_price"] - fitted
            resid_std = grp["drift_residual"].std(skipna=True)
            grp["drift_residual_z"] = np.where(
                resid_std and not math.isnan(resid_std),
                grp["drift_residual"] / resid_std,
                np.nan,
            )
            grp["drift_linear_r2"] = r_value**2
            grp["drift_slope_per_timestamp"] = slope
        else:
            grp["drift_fitted_mid"] = np.nan
            grp["drift_residual"] = np.nan
            grp["drift_residual_z"] = np.nan
            grp["drift_linear_r2"] = np.nan
            grp["drift_slope_per_timestamp"] = np.nan
        frames.append(grp)
    return pd.concat(frames, ignore_index=True)


def aggregate_trade_features(trades: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(columns=["product", "day", "timestamp"])
    mids = prices[["product", "day", "timestamp", "mid_price"]].copy()
    aligned = trades.merge(mids, on=["product", "day", "timestamp"], how="left")
    aligned["trade_vs_mid"] = aligned["price"] - aligned["mid_price"]
    aligned["trade_pressure_sign"] = np.sign(aligned["trade_vs_mid"]).fillna(0)
    aligned["trade_pressure_qty"] = aligned["trade_pressure_sign"] * aligned["quantity"]
    agg = (
        aligned.groupby(["product", "day", "timestamp"], as_index=False)
        .agg(
            trade_count=("price", "size"),
            trade_quantity=("quantity", "sum"),
            trade_pressure_qty=("trade_pressure_qty", "sum"),
            trade_abs_vs_mid=("trade_vs_mid", lambda s: s.abs().mean()),
        )
        .copy()
    )
    return agg


def add_trade_features(prices: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    trade_features = aggregate_trade_features(trades, prices)
    out = prices.merge(trade_features, on=["product", "day", "timestamp"], how="left")
    for col in ["trade_count", "trade_quantity", "trade_pressure_qty"]:
        out[col] = out[col].fillna(0.0)
    return out


def write_csv(df: pd.DataFrame, name: str) -> Path:
    path = ARTIFACT_DIR / name
    df.to_csv(path, index=False)
    return path


def round_value(value: Any, digits: int = 4) -> Any:
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, digits)
    return value


def df_to_md(df: pd.DataFrame, max_rows: int | None = 20) -> str:
    if df is None or df.empty:
        return "_No rows._"
    view = df.copy()
    if max_rows is not None and len(view) > max_rows:
        view = view.head(max_rows)
    for col in view.columns:
        view[col] = view[col].map(lambda x: round_value(x))
    columns = list(view.columns)
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []
    for _, row in view.iterrows():
        rows.append("| " + " | ".join(str(row[col]) for col in columns) + " |")
    suffix = ""
    if max_rows is not None and len(df) > max_rows:
        suffix = f"\n\n_Showing {max_rows} of {len(df)} rows._"
    return "\n".join([header, sep, *rows]) + suffix


def numeric_feature_frame(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    available = [col for col in features if col in df.columns]
    out = df[available].replace([np.inf, -np.inf], np.nan)
    return out.dropna(how="all")


def correlation_and_covariance(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    corr_rows = []
    cov_rows = []
    top_rows = []
    for product, grp in prices.groupby("product"):
        feature_df = numeric_feature_frame(grp, BASE_FEATURES).dropna()
        if feature_df.empty:
            continue
        corr = feature_df.corr()
        cov = feature_df.cov()
        for a in corr.columns:
            for b in corr.columns:
                corr_rows.append(
                    {
                        "product": product,
                        "feature_a": a,
                        "feature_b": b,
                        "correlation": corr.loc[a, b],
                    }
                )
                cov_rows.append(
                    {
                        "product": product,
                        "feature_a": a,
                        "feature_b": b,
                        "covariance": cov.loc[a, b],
                    }
                )
        for idx, a in enumerate(corr.columns):
            for b in corr.columns[idx + 1 :]:
                top_rows.append(
                    {
                        "product": product,
                        "feature_a": a,
                        "feature_b": b,
                        "correlation": corr.loc[a, b],
                        "abs_correlation": abs(corr.loc[a, b]),
                    }
                )
    corr_df = pd.DataFrame(corr_rows)
    cov_df = pd.DataFrame(cov_rows)
    top_df = pd.DataFrame(top_rows).sort_values(
        ["abs_correlation", "product"], ascending=[False, True]
    )
    write_csv(corr_df, "multivariate_feature_correlation.csv")
    write_csv(cov_df, "multivariate_feature_covariance.csv")
    write_csv(top_df, "multivariate_top_correlations.csv")
    return corr_df, cov_df, top_df


def redundancy_analysis(top_corr: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if top_corr.empty:
        return pd.DataFrame()
    for _, row in top_corr[top_corr["abs_correlation"] >= 0.85].iterrows():
        a = row["feature_a"]
        b = row["feature_b"]
        decision = "merge_or_choose_simpler"
        if {a, b} <= {"top_imbalance", "microprice_deviation"}:
            downstream = "Prefer top_imbalance unless microprice gives controlled lift."
        elif {a, b} & {"top_total_volume", "book_total_volume"}:
            downstream = "Use one liquidity/depth proxy first; avoid both in first spec."
        elif "spread" in {a, b} and "relative_spread" in {a, b}:
            downstream = "Use absolute spread for execution unless relative spread adds cross-product comparability."
        elif "rolling_vol_50" in {a, b} or "rolling_vol_200" in {a, b}:
            downstream = "Use one rolling volatility horizon unless validation needs both."
        else:
            downstream = "Check controlled model before stacking both features."
        rows.append(
            {
                "product": row["product"],
                "feature_a": a,
                "feature_b": b,
                "correlation": row["correlation"],
                "abs_correlation": row["abs_correlation"],
                "decision": decision,
                "downstream_effect": downstream,
            }
        )
    out = pd.DataFrame(rows)
    write_csv(out, "multivariate_redundancy_analysis.csv")
    return out


def standardized_matrix(df: pd.DataFrame, features: list[str]) -> tuple[pd.DataFrame, list[str]]:
    available = [col for col in features if col in df.columns]
    mat = df[available].replace([np.inf, -np.inf], np.nan).dropna()
    usable = [
        col
        for col in mat.columns
        if mat[col].nunique(dropna=True) > 1 and mat[col].std(skipna=True) > 0
    ]
    mat = mat[usable]
    if mat.empty:
        return mat, usable
    if StandardScaler is not None:
        values = StandardScaler().fit_transform(mat.values)
    else:
        values = (mat.values - mat.values.mean(axis=0)) / mat.values.std(axis=0)
    return pd.DataFrame(values, columns=usable, index=mat.index), usable


def vif_analysis(prices: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for product, grp in prices.groupby("product"):
        mat, usable = standardized_matrix(grp, REGRESSION_FEATURES)
        if len(usable) < 2 or len(mat) < 10:
            continue
        mat_const = add_constant(mat, has_constant="add")
        for idx, col in enumerate(mat_const.columns):
            if col == "const":
                continue
            try:
                vif = variance_inflation_factor(mat_const.values, idx)
            except Exception:
                vif = np.nan
            rows.append(
                {
                    "product": product,
                    "feature": col,
                    "vif": vif,
                    "decision_note": "high redundancy" if vif and vif > 5 else "acceptable",
                }
            )
    out = pd.DataFrame(rows).sort_values(["product", "vif"], ascending=[True, False])
    write_csv(out, "multivariate_vif.csv")
    return out


def regression_analysis(prices: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for product, grp in prices.groupby("product"):
        for horizon in [1, 3, 5, 10]:
            target = f"future_mid_delta_{horizon}"
            cols = [col for col in REGRESSION_FEATURES if col in grp.columns]
            model_df = grp[[target, *cols]].replace([np.inf, -np.inf], np.nan).dropna()
            usable = [
                col
                for col in cols
                if model_df[col].nunique(dropna=True) > 1
                and model_df[col].std(skipna=True) > 0
            ]
            model_df = model_df[[target, *usable]].dropna()
            if sm is None or len(model_df) < 100 or len(usable) < 2:
                continue
            x_values = model_df[usable]
            x_std = (x_values - x_values.mean()) / x_values.std(ddof=0)
            x_std = add_constant(x_std, has_constant="add")
            y = model_df[target]
            try:
                model = sm.OLS(y, x_std).fit()
            except Exception:
                continue
            for feature in usable:
                rows.append(
                    {
                        "product": product,
                        "horizon_ticks": horizon,
                        "feature": feature,
                        "coef_standardized": model.params.get(feature, np.nan),
                        "pvalue": model.pvalues.get(feature, np.nan),
                        "tvalue": model.tvalues.get(feature, np.nan),
                        "model_r2": model.rsquared,
                        "n": int(model.nobs),
                        "controlled_for": ",".join(usable),
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(
            ["product", "horizon_ticks", "pvalue", "feature"],
            ascending=[True, True, True, True],
        )
    write_csv(out, "multivariate_regression_summary.csv")
    return out


def mutual_information(prices: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if mutual_info_regression is None:
        out = pd.DataFrame(
            [
                {
                    "product": "ALL",
                    "horizon_ticks": "",
                    "feature": "",
                    "mutual_information": np.nan,
                    "n": 0,
                    "note": "sklearn unavailable",
                }
            ]
        )
        write_csv(out, "multivariate_mutual_information.csv")
        return out
    for product, grp in prices.groupby("product"):
        for horizon in [1, 3, 5]:
            target = f"future_mid_delta_{horizon}"
            cols = [col for col in REGRESSION_FEATURES if col in grp.columns]
            model_df = grp[[target, *cols]].replace([np.inf, -np.inf], np.nan).dropna()
            usable = [
                col
                for col in cols
                if model_df[col].nunique(dropna=True) > 1
                and model_df[col].std(skipna=True) > 0
            ]
            model_df = model_df[[target, *usable]].dropna()
            if len(model_df) < 500 or len(usable) < 2:
                continue
            sample = model_df.sample(min(len(model_df), 12000), random_state=42)
            x = sample[usable]
            y = sample[target]
            try:
                mi = mutual_info_regression(x, y, random_state=42)
            except Exception:
                continue
            for feature, value in zip(usable, mi):
                rows.append(
                    {
                        "product": product,
                        "horizon_ticks": horizon,
                        "feature": feature,
                        "mutual_information": value,
                        "n": len(sample),
                        "note": "non-linear screen; use as ranking only",
                    }
                )
    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(
            ["product", "horizon_ticks", "mutual_information"],
            ascending=[True, True, False],
        )
    write_csv(out, "multivariate_mutual_information.csv")
    return out


def pca_analysis(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    explained_rows = []
    loading_rows = []
    for product, grp in prices.groupby("product"):
        mat, usable = standardized_matrix(grp, BASE_FEATURES)
        if PCA is None or len(usable) < 5 or len(mat) < 100:
            continue
        pca = PCA(n_components=min(5, len(usable)), random_state=42)
        pca.fit(mat.values)
        for idx, ratio in enumerate(pca.explained_variance_ratio_, start=1):
            explained_rows.append(
                {
                    "product": product,
                    "component": f"PC{idx}",
                    "explained_variance_ratio": ratio,
                    "cumulative_explained_variance": np.sum(
                        pca.explained_variance_ratio_[:idx]
                    ),
                }
            )
        for comp_idx, comp in enumerate(pca.components_, start=1):
            for feature, loading in zip(usable, comp):
                loading_rows.append(
                    {
                        "product": product,
                        "component": f"PC{comp_idx}",
                        "feature": feature,
                        "loading": loading,
                        "abs_loading": abs(loading),
                    }
                )
    explained = pd.DataFrame(explained_rows)
    loadings = pd.DataFrame(loading_rows)
    if not loadings.empty:
        loadings = loadings.sort_values(
            ["product", "component", "abs_loading"], ascending=[True, True, False]
        )
    write_csv(explained, "multivariate_pca_explained_variance.csv")
    write_csv(loadings, "multivariate_pca_loadings.csv")
    return explained, loadings


def cross_product_analysis(prices: pd.DataFrame) -> pd.DataFrame:
    base = prices[["day", "timestamp", "product", "mid_delta_1", "top_imbalance", "book_imbalance", "spread"]].copy()
    pivot = base.pivot_table(
        index=["day", "timestamp"],
        columns="product",
        values=["mid_delta_1", "top_imbalance", "book_imbalance", "spread"],
    )
    pivot.columns = [f"{metric}__{product}" for metric, product in pivot.columns]
    pivot = pivot.sort_index()
    rows = []
    product_a, product_b = PRODUCTS
    for metric in ["mid_delta_1", "top_imbalance", "book_imbalance", "spread"]:
        col_a = f"{metric}__{product_a}"
        col_b = f"{metric}__{product_b}"
        if col_a in pivot.columns and col_b in pivot.columns:
            valid = pivot[[col_a, col_b]].dropna()
            corr = valid[col_a].corr(valid[col_b]) if len(valid) > 2 else np.nan
            rows.append(
                {
                    "relationship": f"{metric} same-timestamp corr",
                    "product_a": product_a,
                    "product_b": product_b,
                    "lag_ticks_a_predicts_b": 0,
                    "correlation": corr,
                    "n": len(valid),
                    "decision_note": "cross-product evidence" if abs(corr) > 0.1 else "weak cross-product evidence",
                }
            )
    for lag in range(-10, 11):
        col_a = f"mid_delta_1__{product_a}"
        col_b = f"mid_delta_1__{product_b}"
        if col_a not in pivot.columns or col_b not in pivot.columns:
            continue
        shifted_a = pivot[col_a].shift(lag)
        valid = pd.DataFrame({"a": shifted_a, "b": pivot[col_b]}).dropna()
        corr = valid["a"].corr(valid["b"]) if len(valid) > 2 else np.nan
        rows.append(
            {
                "relationship": "lead_lag_mid_delta",
                "product_a": product_a,
                "product_b": product_b,
                "lag_ticks_a_predicts_b": lag,
                "correlation": corr,
                "n": len(valid),
                "decision_note": "lead-lag candidate" if abs(corr) > 0.08 else "weak lead-lag",
            }
        )
    out = pd.DataFrame(rows)
    write_csv(out, "multivariate_cross_product_relationships.csv")
    return out


def clustering_analysis(prices: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if KMeans is None or StandardScaler is None:
        out = pd.DataFrame(
            [{"product": "ALL", "cluster": "", "note": "sklearn unavailable"}]
        )
        write_csv(out, "multivariate_cluster_summary.csv")
        return out
    cluster_features = ["spread", "book_total_volume", "rolling_vol_50", "top_imbalance"]
    for product, grp in prices.groupby("product"):
        df = grp[["day", "timestamp", "future_mid_delta_1", *cluster_features]].replace(
            [np.inf, -np.inf], np.nan
        ).dropna()
        if len(df) < 1000:
            continue
        sample = df.sample(min(len(df), 15000), random_state=42)
        x = StandardScaler().fit_transform(sample[cluster_features])
        model = KMeans(n_clusters=3, n_init=10, random_state=42)
        sample = sample.copy()
        sample["cluster"] = model.fit_predict(x)
        summary = (
            sample.groupby("cluster")
            .agg(
                n=("future_mid_delta_1", "size"),
                spread_mean=("spread", "mean"),
                depth_mean=("book_total_volume", "mean"),
                rolling_vol_mean=("rolling_vol_50", "mean"),
                abs_imbalance_mean=("top_imbalance", lambda s: s.abs().mean()),
                future_delta_mean=("future_mid_delta_1", "mean"),
                future_delta_abs_mean=("future_mid_delta_1", lambda s: s.abs().mean()),
            )
            .reset_index()
        )
        summary["product"] = product
        summary["decision_note"] = np.where(
            summary["future_delta_abs_mean"]
            > summary["future_delta_abs_mean"].median() * 1.15,
            "possible defensive/execution regime",
            "descriptive liquidity group",
        )
        rows.extend(summary.to_dict("records"))
    out = pd.DataFrame(rows)
    write_csv(out, "multivariate_cluster_summary.csv")
    return out


def process_summary(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    metric_rows = []
    hypothesis_rows = []
    for product, grp in prices.groupby("product"):
        day_metrics = []
        for day, day_grp in grp.groupby("day"):
            mid = day_grp["mid_price"].dropna()
            deltas = day_grp["mid_delta_1"].dropna()
            if len(mid) < 100 or len(deltas) < 100:
                continue
            ac1 = deltas.autocorr(lag=1)
            ac2 = deltas.autocorr(lag=2)
            skew = stats.skew(deltas, nan_policy="omit")
            kurt = stats.kurtosis(deltas, fisher=False, nan_policy="omit")
            bimodality = (skew**2 + 1) / kurt if kurt and not math.isnan(kurt) else np.nan
            arch_pvalue = np.nan
            try:
                arch_pvalue = het_arch(deltas, nlags=5)[1]
            except Exception:
                pass
            change_points = "deferred_low_roi"
            row = {
                "product": product,
                "day": day,
                "mid_first": mid.iloc[0],
                "mid_last": mid.iloc[-1],
                "total_change": mid.iloc[-1] - mid.iloc[0],
                "linear_r2": day_grp["drift_linear_r2"].dropna().iloc[0]
                if day_grp["drift_linear_r2"].notna().any()
                else np.nan,
                "residual_std": day_grp["drift_residual"].std(skipna=True),
                "delta_ac1": ac1,
                "delta_ac2": ac2,
                "delta_skew": skew,
                "delta_kurtosis": kurt,
                "bimodality_coefficient": bimodality,
                "rolling_vol_50_mean": day_grp["rolling_vol_50"].mean(skipna=True),
                "rolling_vol_50_cv": day_grp["rolling_vol_50"].std(skipna=True)
                / day_grp["rolling_vol_50"].mean(skipna=True),
                "arch_pvalue": arch_pvalue,
                "change_point_candidates": change_points,
            }
            day_metrics.append(row)
            metric_rows.append(row)
        if not day_metrics:
            continue
        metrics = pd.DataFrame(day_metrics)
        mean_r2 = metrics["linear_r2"].mean()
        mean_ac1 = metrics["delta_ac1"].mean()
        mean_change = metrics["total_change"].mean()
        arch_signal = (metrics["arch_pvalue"] < 0.05).mean()
        if product == "INTARIAN_PEPPER_ROOT" and mean_r2 > 0.95:
            hypothesis = "strong deterministic trend plus residual mean-reversion/noise"
            confidence = "high"
            implication = "Use drift-aware fair value/residual features; do not use a fixed fair value."
            status = "promote"
        elif product == "ASH_COATED_OSMIUM" and mean_ac1 < -0.35:
            hypothesis = "short-horizon mean-reverting microstructure process"
            confidence = "medium/high"
            implication = "Test reversal/fair-value adjustment with spread and fill validation."
            status = "promote"
        elif mean_ac1 < -0.35:
            hypothesis = "mean-reverting residual process"
            confidence = "medium"
            implication = "Use residual/delta reversal only with product-specific calibration."
            status = "exploratory"
        else:
            hypothesis = "noisy or weakly directional process"
            confidence = "low/medium"
            implication = "Avoid strategy family conclusions without stronger signal."
            status = "exploratory"
        if arch_signal > 0:
            implication += " Volatility clustering may matter for sizing/defensive filters."
        hypothesis_rows.append(
            {
                "product_or_scope": product,
                "hypothesized_process": hypothesis,
                "evidence": (
                    f"mean linear R2={mean_r2:.3f}; mean delta AC1={mean_ac1:.3f}; "
                    f"mean day change={mean_change:.2f}; ARCH-day share={arch_signal:.2f}"
                ),
                "confidence": confidence,
                "online_observables": "mid/order_depths, timestamp, spread, rolling delta/residual",
                "downstream_implication": implication,
                "suggested_next_test": "Validate markout/PnL under reviewed spec and platform quote subset.",
                "status": status,
                "caveat": "Sample data evidence; final platform distribution can differ.",
            }
        )
    metric_df = pd.DataFrame(metric_rows)
    hypothesis_df = pd.DataFrame(hypothesis_rows)
    write_csv(metric_df, "process_distribution_metrics.csv")
    write_csv(hypothesis_df, "process_distribution_hypotheses.csv")
    return metric_df, hypothesis_df


def expanded_signal_decisions(
    regression: pd.DataFrame,
    mi: pd.DataFrame,
    redundancy: pd.DataFrame,
    cross_product: pd.DataFrame,
    cluster_summary: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        {
            "feature_or_signal": "IPR drift plus residual",
            "decision": "promote",
            "destination": "Understanding / strategy candidates",
            "reason": "Trend process is extremely stable by day; residual feature is online-computable from timestamp and current mids.",
            "multivariate_note": "Keep as product-specific fair-value basis, not as global price constant.",
            "caveat_reopen_condition": "Reopen if platform run shows final-day drift materially differs.",
        },
        {
            "feature_or_signal": "ACO short-horizon delta reversal",
            "decision": "promote",
            "destination": "Understanding / strategy candidates",
            "reason": "Negative delta autocorrelation and controlled models support reversal framing.",
            "multivariate_note": "Use with spread/depth controls; avoid stacking with redundant residual variants.",
            "caveat_reopen_condition": "Reopen if fills/markouts show adverse selection dominates.",
        },
        {
            "feature_or_signal": "top imbalance",
            "decision": "promote",
            "destination": "Understanding / strategy candidates",
            "reason": "Strong IC and direct online availability; often simpler than full-book variants.",
            "multivariate_note": "Highly related to microprice; choose one primary edge feature first.",
            "caveat_reopen_condition": "Reopen if controlled model shows microprice dominates robustly.",
        },
        {
            "feature_or_signal": "microprice deviation",
            "decision": "exploratory",
            "destination": "Understanding research memory",
            "reason": "A compact transformation of top-of-book imbalance and spread that may encode pressure plus distance.",
            "multivariate_note": "Likely redundant with top imbalance; promote only if controlled lift is clear.",
            "caveat_reopen_condition": "Promote if validation beats top imbalance alone.",
        },
        {
            "feature_or_signal": "full-book imbalance",
            "decision": "exploratory/promote as backup",
            "destination": "Understanding / backup strategy evidence",
            "reason": "Useful IC but redundancy checks suggest it can conflict with or duplicate simpler top imbalance.",
            "multivariate_note": "Use as backup or defensive context, not automatically alongside top imbalance.",
            "caveat_reopen_condition": "Promote if it outperforms top imbalance under wide/one-sided regimes.",
        },
        {
            "feature_or_signal": "spread regime",
            "decision": "promote as execution/risk filter candidate",
            "destination": "Understanding / spec validation checks",
            "reason": "Spread materially changes execution economics and appears in controlled models/regime checks.",
            "multivariate_note": "Role should be filter/sizing/risk, not primary directional signal.",
            "caveat_reopen_condition": "Reject if platform PnL improves without spread gating.",
        },
        {
            "feature_or_signal": "liquidity/depth regime",
            "decision": "exploratory",
            "destination": "Understanding research memory",
            "reason": "Depth and missing levels affect quote quality, but clustering is mostly descriptive.",
            "multivariate_note": "Use defensively first; avoid adding multiple depth features.",
            "caveat_reopen_condition": "Promote only if run diagnostics show depth predicts fills/markouts.",
        },
        {
            "feature_or_signal": "cross-product lead-lag",
            "decision": "negative evidence",
            "destination": "Negative Evidence",
            "reason": "Lead-lag correlations are weak relative to direct within-product signals.",
            "multivariate_note": "Do not build first strategy around cross-product prediction.",
            "caveat_reopen_condition": "Reopen only if platform logs show product coupling not present in sample.",
        },
        {
            "feature_or_signal": "trade pressure proxy",
            "decision": "needs logs",
            "destination": "Future platform diagnostics",
            "reason": "CSV trade alignment is sparse and platform printed state probe is missing.",
            "multivariate_note": "Useful as diagnostic hypothesis, not first spec feature.",
            "caveat_reopen_condition": "Reopen after collecting market_trades from TradingState logs.",
        },
        {
            "feature_or_signal": "PCA/cluster latent components",
            "decision": "EDA-only calibration",
            "destination": "Research memory only",
            "reason": "Helpful for redundancy/regime framing but not online bot logic.",
            "multivariate_note": "Use to simplify feature set and validation, not as direct model input.",
            "caveat_reopen_condition": "Only implement if spec defines a simple online proxy.",
        },
    ]
    out = pd.DataFrame(rows)
    write_csv(out, "expanded_feature_promotion_decisions.csv")
    return out


def plot_correlation_heatmaps(corr: pd.DataFrame) -> list[Path]:
    paths = []
    for product in PRODUCTS:
        subset = corr[corr["product"] == product]
        if subset.empty:
            continue
        matrix = subset.pivot(index="feature_a", columns="feature_b", values="correlation")
        fig, ax = plt.subplots(figsize=(10, 8))
        im = ax.imshow(matrix.values, vmin=-1, vmax=1, cmap="coolwarm")
        ax.set_xticks(range(len(matrix.columns)))
        ax.set_xticklabels(matrix.columns, rotation=90, fontsize=7)
        ax.set_yticks(range(len(matrix.index)))
        ax.set_yticklabels(matrix.index, fontsize=7)
        ax.set_title(f"{product} serious feature correlation")
        fig.colorbar(im, ax=ax, shrink=0.8)
        fig.tight_layout()
        path = ARTIFACT_DIR / f"plot_multivariate_correlation_{product}.png"
        fig.savefig(path, dpi=160)
        plt.close(fig)
        paths.append(path)
    return paths


def plot_pca(explained: pd.DataFrame) -> Path | None:
    if explained.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 5))
    for product, grp in explained.groupby("product"):
        ax.plot(
            grp["component"],
            grp["cumulative_explained_variance"],
            marker="o",
            label=product,
        )
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Cumulative explained variance")
    ax.set_title("PCA redundancy screen")
    ax.legend()
    fig.tight_layout()
    path = ARTIFACT_DIR / "plot_multivariate_pca_explained_variance.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_cross_product(cross_product: pd.DataFrame) -> Path | None:
    subset = cross_product[cross_product["relationship"] == "lead_lag_mid_delta"]
    if subset.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(
        subset["lag_ticks_a_predicts_b"],
        subset["correlation"],
        marker="o",
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Cross-product mid-delta lead-lag")
    ax.set_xlabel("Lag ticks: ACO delta shifted before IPR delta")
    ax.set_ylabel("Correlation")
    fig.tight_layout()
    path = ARTIFACT_DIR / "plot_multivariate_cross_product_lead_lag.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def plot_process(process_metrics: pd.DataFrame) -> Path | None:
    if process_metrics.empty:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for product, grp in process_metrics.groupby("product"):
        axes[0].plot(grp["day"], grp["linear_r2"], marker="o", label=product)
        axes[1].plot(grp["day"], grp["delta_ac1"], marker="o", label=product)
    axes[0].set_title("Linear drift R2 by day")
    axes[0].set_xlabel("day")
    axes[0].set_ylabel("R2")
    axes[1].set_title("Delta autocorrelation lag 1")
    axes[1].set_xlabel("day")
    axes[1].set_ylabel("AC1")
    axes[0].legend()
    axes[1].legend()
    fig.tight_layout()
    path = ARTIFACT_DIR / "plot_process_diagnostics.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def load_existing_artifact(name: str) -> pd.DataFrame:
    path = ARTIFACT_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def artifact_row(path: Path, kind: str, useful_for: str, decision: str = "yes") -> dict[str, str]:
    source_data = "Round 2 raw CSVs / platform JSON / derived EDA tables"
    if "manual" in path.name:
        source_data = "Round 2 wiki manual formula / Research-Scale-Speed scenario grid"
    elif "maf" in path.name:
        source_data = "Round 2 wiki Market Access Fee mechanics / sample-data opportunity proxy"
    return {
        "artifact_path": rel(path),
        "type": kind,
        "source_data": source_data,
        "useful_for": useful_for,
        "decision_relevant": decision,
    }


def write_manifest(new_paths: list[Path]) -> pd.DataFrame:
    rows = []
    existing_names = [
        "data_quality_summary.csv",
        "product_behavior_summary.csv",
        "round1_assumption_check.csv",
        "imbalance_ic.csv",
        "conditional_imbalance_ic.csv",
        "trade_flow_summary.csv",
        "trade_pressure_proxy.csv",
        "platform_comparability.csv",
        "maf_scenarios.csv",
        "manual_scenario_grid_top.csv",
        "manual_scenario_summary.csv",
        "feature_inventory.csv",
        "feature_promotion_decisions.csv",
    ]
    for name in existing_names:
        path = ARTIFACT_DIR / name
        if path.exists():
            rows.append(artifact_row(path, "table", path.stem))
    plot_names = [
        "plot_mid_price_by_product_day.png",
        "plot_spread_distribution.png",
        "plot_returns_distribution.png",
        "plot_imbalance_ic.png",
        "plot_platform_comparability.png",
        "plot_maf_scenarios.png",
        "plot_manual_scenarios.png",
        "plot_drift_residuals.png",
    ]
    for name in plot_names:
        path = ARTIFACT_DIR / name
        if path.exists():
            rows.append(artifact_row(path, "plot", path.stem))
    for path in new_paths:
        kind = "plot" if path.suffix.lower() == ".png" else "table"
        rows.append(artifact_row(path, kind, path.stem))
    manifest = pd.DataFrame(rows).drop_duplicates("artifact_path")
    write_csv(manifest, "artifact_manifest_consolidated.csv")
    with (ARTIFACT_DIR / "artifact_manifest_consolidated.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(rows, handle, indent=2)
    return manifest


def promote_conclusions(
    regression: pd.DataFrame,
    top_corr: pd.DataFrame,
    process_hypotheses: pd.DataFrame,
    cross_product: pd.DataFrame,
) -> list[str]:
    bullets = [
        "`INTARIAN_PEPPER_ROOT` remains a strong drift/residual product: the process layer supports drift-aware fair value, not a fixed Round 1 fair value.",
        "`ASH_COATED_OSMIUM` remains a short-horizon mean-reversion candidate: the process layer supports reversal-style strategy tests, but only with spread/fill validation.",
        "`top_imbalance` remains the cleanest order-book directional feature; `microprice_deviation` is a new exploratory challenger because it compresses top imbalance and spread.",
        "`full-book imbalance` is useful but no longer an automatic co-primary signal; redundancy and controlled checks make it a backup/context feature unless validation beats top imbalance.",
        "`spread regime` should be promoted as an execution/risk filter candidate, not a standalone alpha signal.",
        "Cross-product lead-lag evidence is weak enough to keep out of the first strategy candidate queue.",
        "PCA and clustering are useful for feature simplification/regime diagnostics only; do not implement latent components or clusters directly.",
    ]
    if not regression.empty:
        top = regression.sort_values("pvalue").head(3)
        bullets.append(
            "Controlled regression strongest rows: "
            + "; ".join(
                f"{row.product} h{int(row.horizon_ticks)} {row.feature} coef={row.coef_standardized:.3f} p={row.pvalue:.2g}"
                for row in top.itertuples()
            )
            + "."
        )
    if not cross_product.empty:
        lead = cross_product[cross_product["relationship"] == "lead_lag_mid_delta"]
        if not lead.empty:
            max_abs = lead.iloc[lead["correlation"].abs().argmax()]
            bullets.append(
                f"Max absolute cross-product mid-delta lead-lag correlation is {max_abs['correlation']:.3f} at lag {int(max_abs['lag_ticks_a_predicts_b'])}; this is not enough to drive first-pass strategy."
            )
    return bullets


def write_report(
    manifest: pd.DataFrame,
    data_quality: pd.DataFrame,
    product_behavior: pd.DataFrame,
    round1_check: pd.DataFrame,
    old_feature_inventory: pd.DataFrame,
    old_feature_decisions: pd.DataFrame,
    imbalance_ic: pd.DataFrame,
    conditional_ic: pd.DataFrame,
    trade_flow: pd.DataFrame,
    platform_comparability: pd.DataFrame,
    maf: pd.DataFrame,
    manual_top: pd.DataFrame,
    manual_summary: pd.DataFrame,
    corr: pd.DataFrame,
    cov: pd.DataFrame,
    top_corr: pd.DataFrame,
    redundancy: pd.DataFrame,
    vif: pd.DataFrame,
    regression: pd.DataFrame,
    mi: pd.DataFrame,
    pca_explained: pd.DataFrame,
    pca_loadings: pd.DataFrame,
    cross_product: pd.DataFrame,
    cluster_summary: pd.DataFrame,
    process_metrics: pd.DataFrame,
    process_hypotheses: pd.DataFrame,
    expanded_decisions: pd.DataFrame,
) -> None:
    bullets = promote_conclusions(regression, top_corr, process_hypotheses, cross_product)
    report = [
        "# Round 2 Consolidated EDA",
        "",
        "## Status",
        "",
        "`READY_FOR_REVIEW`",
        "",
        "## Question",
        "",
        "- Question: Which Round 2 product, market-access, validation, manual-allocation, multivariate, and process/distribution signals are decision-useful enough to feed Understanding and later strategy/spec work?",
        "- Product scope: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.",
        "- Why this matters downstream: this is the evidence gate before strategy generation; no bot logic is implemented here.",
        "- Consolidation note: this report supersedes the earlier fresh EDA text as the single canonical EDA handoff for Understanding. It preserves the first-pass findings and adds the new multivariate/process layer.",
        "",
        "## Executive Handoff",
        "",
        *[f"- {bullet}" for bullet in bullets],
        "",
        "## Product Scope",
        "",
        df_to_md(
            pd.DataFrame(
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
            ),
            max_rows=None,
        ),
        "",
        "- Product-scope rationale: both products are official Round 2 algorithmic products with limit 80.",
        "- Product branches: one combined EDA, with product-specific rows where behavior differs materially.",
        "",
        "## Algorithmic vs Manual Scope",
        "",
        df_to_md(
            pd.DataFrame(
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
                    {
                        "Finding": "PCA / clustering / latent-style diagnostics",
                        "Scope": "EDA-only",
                        "Why": "Useful for redundancy and regime hypotheses.",
                        "Caveat": "Do not implement components/clusters directly without an online proxy.",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Challenge Boundary / Do Not Mix",
        "",
        "Round 2 has separate decision tracks. Understanding should preserve this boundary so manual allocation conclusions never become bot features, and algorithmic market signals never become manual allocation evidence.",
        "",
        df_to_md(
            pd.DataFrame(
                [
                    {
                        "Track": "Algorithmic trading",
                        "Decision Owner": "strategy/spec/Trader",
                        "Inputs": "order books, prices, trades/logs, position limits",
                        "Outputs": "signals, execution filters, risk controls, validation checks",
                        "Must Not Use": "manual Research/Scale/Speed allocation as bot signal",
                    },
                    {
                        "Track": "Market Access Fee",
                        "Decision Owner": "strategy/spec/human risk posture",
                        "Inputs": "Round 2 bid mechanics, extra quote access proxy, competitor uncertainty",
                        "Outputs": "bid scenario evidence and later bid decision",
                        "Must Not Use": "testing PnL as final bid proof; manual Speed assumptions",
                    },
                    {
                        "Track": "Manual challenge",
                        "Decision Owner": "human/manual submission",
                        "Inputs": "official Research/Scale/Speed formula and rank scenarios",
                        "Outputs": "manual allocation candidates only",
                        "Must Not Use": "order-book signals, bot features, or Market Access Fee as manual formula inputs",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Data Sources",
        "",
        "- Raw data: `rounds/round_2/data/raw/prices_round_2_day_-1.csv`, `day_0`, `day_1`, plus matching trades files.",
        "- Processed data: tables and plots in `rounds/round_2/workspace/01_eda/artifacts/`.",
        "- Run or log artifact: `rounds/round_2/performances/noel/historical/baseline_state_logger.json`.",
        "- Post-run research memory: absent at EDA start; expected because Round 2 has no prior validated bot run cycle.",
        "",
        "## Round Adaptation Check",
        "",
        df_to_md(
            pd.DataFrame(
                [
                    {
                        "Check": "Active round mechanics/API",
                        "Current-Round Evidence": "Round 2 wiki defines Trader.bid() for Market Access Fee",
                        "Decision / Action": "EDA-only value estimate; final bid belongs to strategy/spec",
                    },
                    {
                        "Check": "Products and limits",
                        "Current-Round Evidence": "Round 2 wiki: ACO/IPR, limit 80 each",
                        "Decision / Action": "verified",
                    },
                    {
                        "Check": "Data schema",
                        "Current-Round Evidence": "raw CSVs and platform activitiesLog share price ladder schema",
                        "Decision / Action": "classified",
                    },
                    {
                        "Check": "New or changed fields/mechanics",
                        "Current-Round Evidence": "Market Access Fee, randomized 80% testing quotes, manual RSS allocation",
                        "Decision / Action": "EDA questions included",
                    },
                    {
                        "Check": "Prior-round assumption at risk",
                        "Current-Round Evidence": "Round 1 product hints and bot constants",
                        "Decision / Action": "revalidate; do not carry as facts",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Artifact Index",
        "",
        df_to_md(manifest, max_rows=80),
        "",
        "## Data Quality And Filters",
        "",
        "- Row counts by file and product: see `data_quality_summary.csv`.",
        "- Timestamp coverage and gaps: raw prices cover three days with 10,000 rows per product/day; platform activities cover 1,000 rows per product on day 1.",
        "- Missing bid/ask counts: measured in data quality and comparability tables; one-sided books are preserved, not dropped globally.",
        "- Zero or blank `mid_price` counts: measured; non-positive mids are treated as missing for analysis.",
        "- Filters applied: signal IC/regression/MI/PCA use rows with non-null feature and target; product stats use available mid rows; platform comparison uses overlapping timestamps.",
        "- Findings based on: mixed raw rows and filtered rows, stated per table.",
        "- Data quality caveats: the platform `.log` is empty and the JSON does not contain `ROUND2_STATE_PROBE`; treat it as platform activity evidence, not raw printed state evidence.",
        "",
        df_to_md(data_quality, max_rows=12),
        "",
        "## Round 1 Assumption Check",
        "",
        df_to_md(round1_check, max_rows=None),
        "",
        "## Product Behavior Summary",
        "",
        df_to_md(product_behavior, max_rows=20),
        "",
        "## Process / Distribution Hypotheses",
        "",
        "This layer is deliberately lightweight: it frames the approximate data-generating process and what downstream phases should do differently.",
        "",
        df_to_md(process_hypotheses, max_rows=None),
        "",
        "### Process Metrics",
        "",
        df_to_md(process_metrics, max_rows=20),
        "",
        "## Feature Inventory",
        "",
        "First-pass inventory from the original EDA:",
        "",
        df_to_md(old_feature_inventory, max_rows=30),
        "",
        "## Feature Promotion Decisions",
        "",
        "Expanded decisions after multivariate/process checks. This is the table Understanding should consume first.",
        "",
        df_to_md(expanded_decisions, max_rows=None),
        "",
        "Earlier first-pass promotion decisions are preserved here for provenance:",
        "",
        df_to_md(old_feature_decisions, max_rows=20),
        "",
        "## Multivariate Feature Map",
        "",
        "Run on serious engineered features only. These checks are for feature selection, redundancy, and process evidence, not for direct bot model import.",
        "",
        "### Top Pairwise Feature Correlations",
        "",
        df_to_md(top_corr.head(30), max_rows=30),
        "",
        "### Redundancy / Dimensionality Check",
        "",
        df_to_md(redundancy, max_rows=30),
        "",
        "### VIF Redundancy Screen",
        "",
        df_to_md(vif, max_rows=30),
        "",
        "### PCA Explained Variance",
        "",
        df_to_md(pca_explained, max_rows=20),
        "",
        "### PCA Loadings",
        "",
        "Top loadings are useful for understanding feature families. They are not bot features.",
        "",
        df_to_md(pca_loadings.head(30), max_rows=30),
        "",
        "## Multivariate Model Notes",
        "",
        "OLS rows use standardized predictors and future mid delta targets. They are explanatory controls, not tuned prediction models.",
        "",
        df_to_md(regression, max_rows=60),
        "",
        "## Mutual Information / Non-Linear Screen",
        "",
        "Use as a ranking hint only. It can suggest threshold or non-linear follow-up, but does not override stability/actionability gates.",
        "",
        df_to_md(mi, max_rows=40),
        "",
        "## Cross-Product Relationships",
        "",
        "Cross-product checks are expected because two products are present. The evidence is weaker than within-product signals.",
        "",
        df_to_md(cross_product, max_rows=40),
        "",
        "## Clustering / Grouping Diagnostics",
        "",
        "KMeans clusters are used only as a lightweight liquidity/regime grouping check. They are not direct strategy state.",
        "",
        df_to_md(cluster_summary, max_rows=20),
        "",
        "## Imbalance Signal Summary",
        "",
        df_to_md(imbalance_ic, max_rows=20),
        "",
        "## Conditional Patterns / Regimes",
        "",
        "This table is long in the artifact; key rows are shown here. Use the CSV for full product/day/regime coverage.",
        "",
        df_to_md(conditional_ic, max_rows=40),
        "",
        "## Trades And Flow Summary",
        "",
        df_to_md(trade_flow, max_rows=20),
        "",
        "## Platform Logger / Validation Comparability",
        "",
        "The available logger JSON is a no-trade platform result with status `FINISHED`, profit `0.0`, 2,000 activity rows, and no `ROUND2_STATE_PROBE` printed-state lines. It is useful for quote-subset comparability, not alpha.",
        "",
        df_to_md(platform_comparability, max_rows=30),
        "",
        "## Market Access Fee Value Estimation",
        "",
        "This is an EDA-only proxy. It estimates gross executable-looking edge under simple fair-value references, then applies 25% extra access and capture-rate scenarios. It does not decide a final bid.",
        "",
        df_to_md(maf, max_rows=10),
        "",
        "## Manual Research / Scale / Speed Scenario Analysis",
        "",
        "The grid uses official Research and Scale formulas. Speed multiplier scenarios are rank-outcome proxies because actual rank is competitor-dependent.",
        "",
        df_to_md(manual_top, max_rows=12),
        "",
        "Manual scenario summary:",
        "",
        df_to_md(manual_summary, max_rows=20),
        "",
        "## Signal Hypotheses",
        "",
        df_to_md(
            pd.DataFrame(
                [
                    {
                        "Signal": "IPR drift + residual",
                        "Feature Dependencies": "timestamp, mid/order book, rolling residual",
                        "What It Means": "Current-round IPR level is trending, not fixed.",
                        "Why It Matters": "Prevents stale Round 1 fixed fair value.",
                        "Strategy Use": "drift-aware fair value candidate",
                        "Stability": "stable in sample",
                        "Confidence": "strong",
                        "Limitations / Caveats": "avoid hardcoding sample-end/day constants",
                    },
                    {
                        "Signal": "ACO short-horizon reversal",
                        "Feature Dependencies": "mid deltas/order book",
                        "What It Means": "Price changes often reverse.",
                        "Why It Matters": "Possible market-making/reversion edge.",
                        "Strategy Use": "fair-value adjustment",
                        "Stability": "stable in sample",
                        "Confidence": "medium/strong",
                        "Limitations / Caveats": "execution costs and fill quality unknown",
                    },
                    {
                        "Signal": "Top imbalance",
                        "Feature Dependencies": "best bid/ask volumes",
                        "What It Means": "Visible liquidity skew predicts near move.",
                        "Why It Matters": "Online signal from order_depths.",
                        "Strategy Use": "signal/skew candidate",
                        "Stability": "stable enough for candidate queue",
                        "Confidence": "strong",
                        "Limitations / Caveats": "exact sizing needs validation",
                    },
                    {
                        "Signal": "Microprice deviation",
                        "Feature Dependencies": "best prices and volumes",
                        "What It Means": "Top-of-book pressure translated into price deviation.",
                        "Why It Matters": "May be more compact than raw imbalance.",
                        "Strategy Use": "exploratory challenger to top imbalance",
                        "Stability": "unknown after validation",
                        "Confidence": "medium/exploratory",
                        "Limitations / Caveats": "likely redundant with top imbalance",
                    },
                    {
                        "Signal": "Spread regime",
                        "Feature Dependencies": "best bid/ask spread",
                        "What It Means": "Execution economics change across rows.",
                        "Why It Matters": "Can prevent bad fills or overtrading.",
                        "Strategy Use": "execution/risk filter",
                        "Stability": "day-sensitive",
                        "Confidence": "medium",
                        "Limitations / Caveats": "not standalone alpha",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Negative Evidence",
        "",
        df_to_md(
            pd.DataFrame(
                [
                    {
                        "Idea Or Signal": "Carry Round 1 fixed IPR fair value",
                        "Why It Was Plausible": "Round 1 hint called IPR steady",
                        "Evidence Against It": "Round 2 drift/process evidence contradicts fixed value",
                        "When To Reopen": "only with new final/platform evidence",
                    },
                    {
                        "Idea Or Signal": "Use cross-product lead-lag in first strategy",
                        "Why It Was Plausible": "two products have aligned timestamps",
                        "Evidence Against It": "lead-lag correlations are weak versus direct product signals",
                        "When To Reopen": "if platform logs reveal product coupling",
                    },
                    {
                        "Idea Or Signal": "Use PCA/clusters as bot state",
                        "Why It Was Plausible": "PCA and clusters expose feature families/regimes",
                        "Evidence Against It": "offline latent components are not direct TradingState features",
                        "When To Reopen": "only if spec defines a simple online proxy",
                    },
                    {
                        "Idea Or Signal": "Treat diagnostic logger PnL as meaningful",
                        "Why It Was Plausible": "platform JSON has profit field",
                        "Evidence Against It": "bot intentionally does not trade, profit is 0",
                        "When To Reopen": "never for alpha; use only as quote evidence",
                    },
                    {
                        "Idea Or Signal": "Use trade pressure directly in first spec",
                        "Why It Was Plausible": "market trades exist",
                        "Evidence Against It": "sparse sample evidence and no printed state probe",
                        "When To Reopen": "after platform logs include market_trades dynamics",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Downstream Feature Contract Implications",
        "",
        df_to_md(
            pd.DataFrame(
                [
                    {
                        "Feature Or Relationship": "IPR drift/residual",
                        "Contract Implication": "Needs explicit online drift/reference formula and missing-data fallback.",
                        "Online Proxy Needed?": "no; timestamp/mid/order_depths are available",
                        "Validation / Invalidation Check": "markout/PnL under day/platform subset; fail if drift residual logic overfits day constants",
                        "Do Not Use Until": "reviewed strategy spec names parameters",
                    },
                    {
                        "Feature Or Relationship": "ACO delta reversal",
                        "Contract Implication": "Needs state for previous mid/delta and spread-aware execution.",
                        "Online Proxy Needed?": "no; previous mids can be stored in traderData",
                        "Validation / Invalidation Check": "post-fill markout and inventory adverse selection",
                        "Do Not Use Until": "reviewed strategy spec defines state and fallback",
                    },
                    {
                        "Feature Or Relationship": "top imbalance / microprice",
                        "Contract Implication": "Choose one primary signal first to avoid redundancy.",
                        "Online Proxy Needed?": "no",
                        "Validation / Invalidation Check": "compare top imbalance vs microprice variant one axis at a time",
                        "Do Not Use Until": "spec selects primary and backup",
                    },
                    {
                        "Feature Or Relationship": "spread/depth regimes",
                        "Contract Implication": "Use as execution/risk filter, not alpha source.",
                        "Online Proxy Needed?": "no",
                        "Validation / Invalidation Check": "PnL/fill split by spread/depth regime",
                        "Do Not Use Until": "spec states threshold or defensive behavior",
                    },
                    {
                        "Feature Or Relationship": "cross-product lead-lag",
                        "Contract Implication": "Do not implement in first strategy.",
                        "Online Proxy Needed?": "not applicable",
                        "Validation / Invalidation Check": "targeted EDA only if new evidence appears",
                        "Do Not Use Until": "new evidence contradicts current weak verdict",
                    },
                ]
            ),
            max_rows=None,
        ),
        "",
        "## Assumptions",
        "",
        "- MAF capture rates are scenario assumptions, not official mechanics.",
        "- Manual Speed multiplier scenarios are rank proxies, not predictions.",
        "- Platform activitiesLog is treated as 80% quote-subset evidence because Round 2 docs say testing uses default quotes and ignores bid().",
        "- Multivariate regressions, PCA, mutual information, and clustering are research evidence only; uploadable bots need reviewed online Feature Contracts.",
        "",
        "## Open Questions",
        "",
        "- Exact Round 2 deadline remains unknown.",
        "- Competitive Market Access Fee bid distribution is unknown.",
        "- Manual Speed rank outcome is unknown.",
        "- Platform market_trades behavior from printed `TradingState` logs is still missing because the saved JSON did not include `ROUND2_STATE_PROBE`.",
        "",
        "## Signal Strength And Uncertainty",
        "",
        "- Strong: IPR drift/residual, top imbalance.",
        "- Medium/strong: ACO short-horizon reversal.",
        "- Medium/exploratory: microprice deviation, spread regime, full-book imbalance as backup/context.",
        "- Weak/negative: cross-product lead-lag for first strategy.",
        "- Needs logs: trade pressure proxy.",
        "- Uncertainty: sample data may differ from final simulation; platform testing quote subset is randomized.",
        "",
        "## Downstream Use / Agent Notes",
        "",
        "- Strong enough to consider: IPR drift plus residual, ACO short-horizon mean reversion, top imbalance, spread regime as an execution/risk filter.",
        "- Exploratory only: microprice deviation, full-book imbalance as backup/context, liquidity/depth regime, clustering/grouping diagnostics.",
        "- Do not use yet: cross-product lead-lag, trade pressure proxy, PCA components, cluster labels, latent states.",
        "- Additional validation needed: strategy candidates must test whether promoted signals survive execution, position limits, randomized quote subsets, and platform PnL.",
        "- How understanding should use this: consume `expanded_feature_promotion_decisions.csv`, process hypotheses, and negative evidence; do not collapse everything back to four fixed signals.",
        "- Manual challenge handling: keep Research/Scale/Speed findings in a manual-only lane; they should not enter the Signal Ledger as bot features.",
        "- Market Access Fee handling: carry as an algorithmic final-round mechanics/risk decision, separate from normal `Trader.run()` signals and separate from manual allocation.",
        "- How strategy generation should use this: generate bounded candidates around drift/residual, ACO reversal, top imbalance or microprice challenger, and conservative spread/depth filters.",
        "- How specification should use this: define online fields, state, missing-signal behavior, and invalidation checks; avoid CSV/day-specific constants.",
        "- How implementation should use this: do not implement until a reviewed spec exists.",
        "- How testing/debugging should use this: validate signal markouts and PnL by product, spread/depth regime, and platform quote subset.",
        "",
        "## Reusable Metrics",
        "",
        "- `spread`, `relative_spread`, `top_imbalance`, `book_imbalance`, `microprice_deviation`, `book_total_volume`, `depth_ratio`, `one_sided_book`, `mid_delta_lag1`, `rolling_vol_50`, `z_mid_50`, `drift_residual_z`, `trade_pressure_qty`.",
        "",
        "## Strategy Implications",
        "",
        "- Round 2 should not inherit a fixed Round 1 view of IPR.",
        "- ACO and top imbalance signals deserve first strategy consideration.",
        "- Microprice is worth a controlled challenger/variant, not immediate feature stacking.",
        "- Spread/depth should be considered as execution/risk filters.",
        "- Cross-product prediction is low ROI for first-pass strategy.",
        "- MAF/manual decisions remain scenario/risk decisions, not bot signals.",
        "",
        "## Interpretation Limits",
        "",
        "- EDA is evidence, not a strategy.",
        "- Sample data patterns are not official rules.",
        "- Platform logger result is no-trade and cannot measure alpha.",
        "- MAF and manual allocations are scenario analyses, not final submissions.",
        "- Research-library outputs are not uploadable bot dependencies.",
        "",
        "## Next Action",
        "",
        "- Human review this consolidated EDA. If approved, synthesize `02_understanding.md` from this single report and the linked artifacts, then generate a small but not artificially capped strategy candidate set grounded in the promoted/exploratory/negative evidence above.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    prices = add_book_features(read_prices())
    prices = add_time_features(prices)
    trades = read_trades()
    prices = add_trade_features(prices, trades)
    platform = read_platform_json()
    platform_activities = read_platform_activities(platform)
    if not platform_activities.empty:
        platform_activities = add_book_features(platform_activities)

    corr, cov, top_corr = correlation_and_covariance(prices)
    redundancy = redundancy_analysis(top_corr)
    vif = vif_analysis(prices)
    regression = regression_analysis(prices)
    mi = mutual_information(prices)
    pca_explained, pca_loadings = pca_analysis(prices)
    cross_product = cross_product_analysis(prices)
    cluster_summary = clustering_analysis(prices)
    process_metrics, process_hypotheses = process_summary(prices)
    expanded_decisions = expanded_signal_decisions(
        regression, mi, redundancy, cross_product, cluster_summary
    )

    new_artifacts = [
        ARTIFACT_DIR / name
        for name in [
            "multivariate_feature_correlation.csv",
            "multivariate_feature_covariance.csv",
            "multivariate_top_correlations.csv",
            "multivariate_redundancy_analysis.csv",
            "multivariate_vif.csv",
            "multivariate_regression_summary.csv",
            "multivariate_mutual_information.csv",
            "multivariate_pca_explained_variance.csv",
            "multivariate_pca_loadings.csv",
            "multivariate_cross_product_relationships.csv",
            "multivariate_cluster_summary.csv",
            "process_distribution_metrics.csv",
            "process_distribution_hypotheses.csv",
            "expanded_feature_promotion_decisions.csv",
        ]
    ]
    new_artifacts.extend(plot_correlation_heatmaps(corr))
    pca_plot = plot_pca(pca_explained)
    if pca_plot:
        new_artifacts.append(pca_plot)
    cross_plot = plot_cross_product(cross_product)
    if cross_plot:
        new_artifacts.append(cross_plot)
    process_plot = plot_process(process_metrics)
    if process_plot:
        new_artifacts.append(process_plot)

    manifest = write_manifest([p for p in new_artifacts if p.exists()])

    write_report(
        manifest=manifest,
        data_quality=load_existing_artifact("data_quality_summary.csv"),
        product_behavior=load_existing_artifact("product_behavior_summary.csv"),
        round1_check=load_existing_artifact("round1_assumption_check.csv"),
        old_feature_inventory=load_existing_artifact("feature_inventory.csv"),
        old_feature_decisions=load_existing_artifact("feature_promotion_decisions.csv"),
        imbalance_ic=load_existing_artifact("imbalance_ic.csv"),
        conditional_ic=load_existing_artifact("conditional_imbalance_ic.csv"),
        trade_flow=load_existing_artifact("trade_flow_summary.csv"),
        platform_comparability=load_existing_artifact("platform_comparability.csv"),
        maf=load_existing_artifact("maf_scenarios.csv"),
        manual_top=load_existing_artifact("manual_scenario_grid_top.csv"),
        manual_summary=load_existing_artifact("manual_scenario_summary.csv"),
        corr=corr,
        cov=cov,
        top_corr=top_corr,
        redundancy=redundancy,
        vif=vif,
        regression=regression,
        mi=mi,
        pca_explained=pca_explained,
        pca_loadings=pca_loadings,
        cross_product=cross_product,
        cluster_summary=cluster_summary,
        process_metrics=process_metrics,
        process_hypotheses=process_hypotheses,
        expanded_decisions=expanded_decisions,
    )
    print(f"Wrote {rel(REPORT_PATH)}")
    print(f"Wrote {len(new_artifacts)} new multivariate/process artifacts")


if __name__ == "__main__":
    main()
