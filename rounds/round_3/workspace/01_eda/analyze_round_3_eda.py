from __future__ import annotations

import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(SCRIPT_DIR / "artifacts" / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.feature_selection import mutual_info_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler


ROOT = SCRIPT_DIR.parents[3]
RAW_DIR = ROOT / "rounds" / "round_3" / "data" / "raw"
PROCESSED_DIR = ROOT / "rounds" / "round_3" / "data" / "processed"
ARTIFACTS_DIR = ROOT / "rounds" / "round_3" / "workspace" / "01_eda" / "artifacts"

def load_prices() -> pd.DataFrame:
    frames = []
    for path in sorted(RAW_DIR.glob("prices_round_3_day_*.csv")):
        df = pd.read_csv(path, sep=";")
        df["source_file"] = path.name
        frames.append(df)

    prices = pd.concat(frames, ignore_index=True)
    prices["spread"] = prices["ask_price_1"] - prices["bid_price_1"]
    prices["rel_spread_bps"] = prices["spread"] / prices["mid_price"] * 10_000
    prices["depth_1"] = prices["bid_volume_1"].fillna(0) + prices["ask_volume_1"].fillna(0)
    denom = prices["depth_1"].replace(0, np.nan)
    prices["imbalance_1"] = (
        prices["bid_volume_1"].fillna(0) - prices["ask_volume_1"].fillna(0)
    ) / denom

    prices = prices.sort_values(["product", "day", "timestamp"]).reset_index(drop=True)
    prices["mid_delta_1"] = prices.groupby(["product", "day"])["mid_price"].diff()
    prices["future_mid_delta_5"] = (
        prices.groupby(["product", "day"])["mid_price"].shift(-5) - prices["mid_price"]
    )
    prices["future_abs_mid_delta_5"] = prices["future_mid_delta_5"].abs()
    return prices


def load_trades() -> pd.DataFrame:
    frames = []
    for path in sorted(RAW_DIR.glob("trades_round_3_day_*.csv")):
        df = pd.read_csv(path, sep=";")
        df["day"] = int(path.stem.split("_")[-1])
        df["source_file"] = path.name
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def build_option_panel(prices: pd.DataFrame) -> pd.DataFrame:
    underlying = prices.loc[
        prices["product"] == "VELVETFRUIT_EXTRACT",
        ["day", "timestamp", "mid_price", "mid_delta_1", "future_mid_delta_5"],
    ].rename(
        columns={
            "mid_price": "underlying_mid",
            "mid_delta_1": "underlying_delta_1",
            "future_mid_delta_5": "underlying_future_delta_5",
        }
    )

    options = prices.loc[prices["product"].str.startswith("VEV_")].copy()
    options["strike"] = options["product"].str.split("_").str[1].astype(int)
    options["tte_days"] = 8 - options["day"]
    options = options.merge(underlying, on=["day", "timestamp"], how="left")
    options["moneyness"] = options["underlying_mid"] - options["strike"]
    options["normalized_moneyness"] = options["moneyness"] / options["underlying_mid"]
    options["intrinsic_value"] = np.maximum(options["moneyness"], 0)
    options["extrinsic_value"] = options["mid_price"] - options["intrinsic_value"]
    options["extrinsic_dev_day"] = options["extrinsic_value"] - options.groupby(
        ["day", "product"]
    )["extrinsic_value"].transform("mean")
    options["future_extrinsic_change_5"] = (
        options.groupby(["product", "day"])["extrinsic_value"].shift(-5)
        - options["extrinsic_value"]
    )
    return options


def save_csv(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED_DIR / name
    df.to_csv(path, index=False)
    return path


def save_plot(fig: plt.Figure, name: str) -> Path:
    path = ARTIFACTS_DIR / name
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def summarize_data_quality(prices: pd.DataFrame, trades: pd.DataFrame) -> dict[str, Path]:
    quality_by_file = (
        prices.groupby(["source_file"])
        .agg(
            rows=("product", "size"),
            unique_products=("product", "nunique"),
            unique_timestamps=("timestamp", "nunique"),
            min_timestamp=("timestamp", "min"),
            max_timestamp=("timestamp", "max"),
            mid_zero_count=("mid_price", lambda s: int((s == 0).sum())),
            missing_bid_2=("bid_price_2", lambda s: int(s.isna().sum())),
            missing_ask_2=("ask_price_2", lambda s: int(s.isna().sum())),
            missing_bid_3=("bid_price_3", lambda s: int(s.isna().sum())),
            missing_ask_3=("ask_price_3", lambda s: int(s.isna().sum())),
        )
        .reset_index()
    )

    quality_by_product = (
        prices.groupby("product")
        .agg(
            rows=("product", "size"),
            days_present=("day", "nunique"),
            mean_mid=("mid_price", "mean"),
            std_mid=("mid_price", "std"),
            mean_spread=("spread", "mean"),
            median_spread=("spread", "median"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            missing_bid_2_share=("bid_price_2", lambda s: float(s.isna().mean())),
            missing_ask_2_share=("ask_price_2", lambda s: float(s.isna().mean())),
            missing_bid_3_share=("bid_price_3", lambda s: float(s.isna().mean())),
            missing_ask_3_share=("ask_price_3", lambda s: float(s.isna().mean())),
            zero_mid_count=("mid_price", lambda s: int((s == 0).sum())),
        )
        .reset_index()
    )

    trade_summary = (
        trades.groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            qty_mean=("quantity", "mean"),
            qty_median=("quantity", "median"),
            price_mean=("price", "mean"),
        )
        .reset_index()
    )

    return {
        "quality_by_file": save_csv(
            quality_by_file, "derived_round_3_data_quality_by_file.csv"
        ),
        "quality_by_product": save_csv(
            quality_by_product, "derived_round_3_data_quality_by_product.csv"
        ),
        "trade_summary": save_csv(
            trade_summary, "derived_round_3_trade_summary_by_symbol.csv"
        ),
    }


def compute_trade_alignment(prices: pd.DataFrame, trades: pd.DataFrame) -> Path:
    book = prices[
        ["day", "timestamp", "product", "bid_price_1", "ask_price_1", "mid_price"]
    ].rename(columns={"product": "symbol"})
    aligned = trades.merge(book, on=["day", "timestamp", "symbol"], how="left")
    aligned["trade_minus_mid"] = aligned["price"] - aligned["mid_price"]
    aligned["at_or_below_bid"] = (aligned["price"] <= aligned["bid_price_1"]).astype(int)
    aligned["at_or_above_ask"] = (aligned["price"] >= aligned["ask_price_1"]).astype(int)

    summary = (
        aligned.groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            avg_trade_minus_mid=("trade_minus_mid", "mean"),
            abs_trade_minus_mid=("trade_minus_mid", lambda s: s.abs().mean()),
            share_at_or_below_bid=("at_or_below_bid", "mean"),
            share_at_or_above_ask=("at_or_above_ask", "mean"),
        )
        .reset_index()
    )
    return save_csv(summary, "derived_round_3_trade_alignment_summary.csv")


def compute_surface_metrics(options: pd.DataFrame) -> dict[str, Path]:
    records = []
    for (day, timestamp), group in options.groupby(["day", "timestamp"]):
        ordered = group.sort_values("strike")
        mids = ordered["mid_price"].to_numpy()
        monotone_breaks = int((np.diff(mids) > 0).sum())
        convex_breaks = int((np.diff(mids, 2) < 0).sum()) if len(mids) >= 3 else 0
        records.append(
            {
                "day": day,
                "timestamp": timestamp,
                "monotone_ok": monotone_breaks == 0,
                "convex_ok": convex_breaks == 0,
                "monotone_breaks": monotone_breaks,
                "convex_breaks": convex_breaks,
            }
        )

    surface_checks = pd.DataFrame(records)
    surface_summary = (
        surface_checks.groupby("day")
        .agg(
            monotone_ok_rate=("monotone_ok", "mean"),
            convex_ok_rate=("convex_ok", "mean"),
            avg_monotone_breaks=("monotone_breaks", "mean"),
            avg_convex_breaks=("convex_breaks", "mean"),
        )
        .reset_index()
    )

    extrinsic_by_tte = (
        options.groupby(["tte_days", "product", "strike"])
        .agg(
            mean_mid=("mid_price", "mean"),
            mean_intrinsic=("intrinsic_value", "mean"),
            mean_extrinsic=("extrinsic_value", "mean"),
        )
        .reset_index()
        .sort_values(["tte_days", "strike"])
    )

    return {
        "surface_checks": save_csv(
            surface_checks, "derived_round_3_option_surface_checks.csv"
        ),
        "surface_summary": save_csv(
            surface_summary, "derived_round_3_option_surface_summary.csv"
        ),
        "extrinsic_by_tte": save_csv(
            extrinsic_by_tte, "derived_round_3_option_extrinsic_by_tte.csv"
        ),
    }


def compute_cross_product_metrics(
    prices: pd.DataFrame, options: pd.DataFrame
) -> dict[str, Path]:
    pivot = prices.pivot_table(index=["day", "timestamp"], columns="product", values="mid_price")
    returns = pivot.groupby(level=0).pct_change().replace([np.inf, -np.inf], np.nan)
    deltas = pivot.groupby(level=0).diff()

    with np.errstate(invalid="ignore"):
        corr_matrix = returns.corr().reset_index()
        cov_matrix = returns.cov().reset_index()
    corr_path = save_csv(corr_matrix, "derived_round_3_same_time_return_corr.csv")
    cov_path = save_csv(cov_matrix, "derived_round_3_same_time_return_covariance.csv")

    lead_lag_rows = []
    underlying = deltas["VELVETFRUIT_EXTRACT"]
    for product in [c for c in deltas.columns if c.startswith("VEV_")]:
        series = deltas[product]
        for lag in [0, 1, 2, 5, 10]:
            corr = underlying.groupby(level=0).shift(lag).corr(series)
            lead_lag_rows.append(
                {
                    "product": product,
                    "underlying_lag_steps": lag,
                    "corr_underlying_delta_to_option_delta": corr,
                }
            )
    lead_lag = pd.DataFrame(lead_lag_rows)

    product_signal_rows = []
    for product, group in prices.groupby("product"):
        series = group["mid_delta_1"]
        product_signal_rows.append(
            {
                "product": product,
                "delta_acf_1": series.autocorr(lag=1),
                "delta_acf_5": series.autocorr(lag=5),
                "zero_delta_share": float((series == 0).mean()),
                "imbalance_corr_future_delta_5": group["imbalance_1"].corr(
                    group["future_mid_delta_5"]
                ),
                "spread_corr_future_abs_delta_5": group["spread"].corr(
                    group["future_abs_mid_delta_5"]
                ),
                "mean_rel_spread_bps": group["rel_spread_bps"].mean(),
            }
        )
    product_signals = pd.DataFrame(product_signal_rows)

    option_reversion_rows = []
    for product, group in options.groupby("product"):
        option_reversion_rows.append(
            {
                "product": product,
                "extrinsic_dev_vs_future_change_5_corr": group["extrinsic_dev_day"].corr(
                    group["future_extrinsic_change_5"]
                ),
                "extrinsic_std": group["extrinsic_value"].std(),
                "mean_abs_extrinsic_dev_day": group["extrinsic_dev_day"].abs().mean(),
            }
        )
    option_reversion = pd.DataFrame(option_reversion_rows)

    return {
        "return_corr": corr_path,
        "return_cov": cov_path,
        "lead_lag": save_csv(
            lead_lag, "derived_round_3_underlying_option_lead_lag.csv"
        ),
        "product_signals": save_csv(
            product_signals, "derived_round_3_product_signal_metrics.csv"
        ),
        "option_reversion": save_csv(
            option_reversion, "derived_round_3_option_reversion_metrics.csv"
        ),
    }


def compute_model_artifacts(options: pd.DataFrame) -> dict[str, Path]:
    model_df = options.loc[
        options["product"].isin(
            ["VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"]
        ),
        ["underlying_delta_1", "imbalance_1", "extrinsic_dev_day", "spread", "future_mid_delta_5"],
    ].dropna()

    standardized = model_df.copy()
    for col in standardized.columns:
        standardized[col] = (standardized[col] - standardized[col].mean()) / standardized[col].std()

    X = standardized[["underlying_delta_1", "imbalance_1", "extrinsic_dev_day"]]
    y = standardized["future_mid_delta_5"]
    linear = LinearRegression().fit(X, y)
    linear_summary = pd.DataFrame(
        {
            "feature": X.columns,
            "standardized_coef": linear.coef_,
            "pooled_r2": [r2_score(y, linear.predict(X))] * len(X.columns),
        }
    )

    mi_scores = pd.DataFrame(
        {
            "feature": ["underlying_delta_1", "imbalance_1", "extrinsic_dev_day", "spread"],
            "mutual_information": mutual_info_regression(
                model_df[["underlying_delta_1", "imbalance_1", "extrinsic_dev_day", "spread"]],
                model_df["future_mid_delta_5"],
                random_state=0,
            ),
        }
    )

    pca_inputs = options.loc[
        ~options["product"].isin(["VEV_6000", "VEV_6500"]),
        ["mid_price", "intrinsic_value", "extrinsic_value", "moneyness", "spread", "imbalance_1"],
    ].dropna()
    feature_corr = pca_inputs.corr().reset_index()
    feature_cov = pca_inputs.cov().reset_index()
    scaled = StandardScaler().fit_transform(pca_inputs)
    pca = PCA(n_components=3, random_state=0).fit(scaled)
    pca_loadings = pd.DataFrame(
        pca.components_.T,
        index=pca_inputs.columns,
        columns=["PC1", "PC2", "PC3"],
    ).reset_index(names="feature")
    pca_explained = pd.DataFrame(
        {
            "component": ["PC1", "PC2", "PC3"],
            "explained_variance_ratio": pca.explained_variance_ratio_,
        }
    )

    return {
        "linear_summary": save_csv(
            linear_summary, "derived_round_3_pooled_option_linear_model.csv"
        ),
        "mi_scores": save_csv(
            mi_scores, "derived_round_3_option_mutual_information.csv"
        ),
        "pca_loadings": save_csv(
            pca_loadings, "derived_round_3_option_pca_loadings.csv"
        ),
        "pca_explained": save_csv(
            pca_explained, "derived_round_3_option_pca_explained_variance.csv"
        ),
        "feature_corr": save_csv(
            feature_corr, "derived_round_3_option_feature_corr.csv"
        ),
        "feature_cov": save_csv(
            feature_cov, "derived_round_3_option_feature_covariance.csv"
        ),
    }


def plot_extrinsic_surface(extrinsic_by_tte: pd.DataFrame) -> Path:
    fig, ax = plt.subplots(figsize=(8, 5))
    for tte, group in extrinsic_by_tte.groupby("tte_days"):
        ordered = group.sort_values("strike")
        ax.plot(ordered["strike"], ordered["mean_extrinsic"], marker="o", label=f"TTE {int(tte)}d")
    ax.set_title("Average Voucher Extrinsic Value By Strike And TTE")
    ax.set_xlabel("Strike")
    ax.set_ylabel("Average extrinsic value")
    ax.legend()
    return save_plot(fig, "round_3_option_extrinsic_by_tte.png")


def plot_return_corr_heatmap(prices: pd.DataFrame) -> Path:
    pivot = prices.pivot_table(index=["day", "timestamp"], columns="product", values="mid_price")
    returns = pivot.groupby(level=0).pct_change().replace([np.inf, -np.inf], np.nan)
    with np.errstate(invalid="ignore"):
        corr = returns.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Same-Time Return Correlations")
    return save_plot(fig, "round_3_return_corr_heatmap.png")


def plot_imbalance_bins(prices: pd.DataFrame) -> Path:
    selected = ["HYDROGEL_PACK", "VELVETFRUIT_EXTRACT", "VEV_5000", "VEV_5200", "VEV_5400"]
    rows = []
    for product in selected:
        group = prices.loc[prices["product"] == product, ["imbalance_1", "future_mid_delta_5"]].dropna()
        group = group.copy()
        group["imbalance_bin"] = pd.qcut(group["imbalance_1"], 10, duplicates="drop")
        summary = (
            group.groupby("imbalance_bin", observed=False)["future_mid_delta_5"]
            .mean()
            .reset_index()
        )
        summary["bin_center"] = summary["imbalance_bin"].apply(lambda x: (x.left + x.right) / 2)
        summary["product"] = product
        rows.append(summary)
    plot_df = pd.concat(rows, ignore_index=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=plot_df, x="bin_center", y="future_mid_delta_5", hue="product", marker="o", ax=ax)
    ax.set_title("Order-Book Imbalance Vs Future 5-Step Mid Delta")
    ax.set_xlabel("Imbalance bin center")
    ax.set_ylabel("Average future 5-step mid delta")
    return save_plot(fig, "round_3_imbalance_signal_bins.png")


def plot_extrinsic_reversion(options: pd.DataFrame) -> Path:
    selected = ["VEV_4000", "VEV_4500", "VEV_5000", "VEV_5100", "VEV_5200"]
    rows = []
    for product in selected:
        group = options.loc[
            options["product"] == product, ["extrinsic_dev_day", "future_extrinsic_change_5"]
        ].dropna()
        if group.empty:
            continue
        group = group.copy()
        group["dev_bin"] = pd.qcut(group["extrinsic_dev_day"], 10, duplicates="drop")
        summary = (
            group.groupby("dev_bin", observed=False)["future_extrinsic_change_5"]
            .mean()
            .reset_index()
        )
        summary["bin_center"] = summary["dev_bin"].apply(lambda x: (x.left + x.right) / 2)
        summary["product"] = product
        rows.append(summary)
    plot_df = pd.concat(rows, ignore_index=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=plot_df, x="bin_center", y="future_extrinsic_change_5", hue="product", marker="o", ax=ax)
    ax.axhline(0, color="black", linewidth=1, linestyle="--")
    ax.set_title("Voucher Extrinsic Deviation Vs Future 5-Step Extrinsic Change")
    ax.set_xlabel("Extrinsic deviation bin center")
    ax.set_ylabel("Average future 5-step extrinsic change")
    return save_plot(fig, "round_3_extrinsic_reversion_bins.png")


def plot_rel_spread_box(prices: pd.DataFrame) -> Path:
    selected = [
        "HYDROGEL_PACK",
        "VELVETFRUIT_EXTRACT",
        "VEV_4000",
        "VEV_5000",
        "VEV_5200",
        "VEV_5400",
        "VEV_6000",
    ]
    plot_df = prices.loc[prices["product"].isin(selected), ["product", "rel_spread_bps"]].copy()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=plot_df, x="product", y="rel_spread_bps", ax=ax, showfliers=False)
    ax.set_title("Relative Spread Distribution By Product")
    ax.set_xlabel("Product")
    ax.set_ylabel("Relative spread (bps)")
    ax.tick_params(axis="x", rotation=30)
    return save_plot(fig, "round_3_relative_spread_boxplot.png")


def build_summary_metrics(
    prices: pd.DataFrame,
    trades: pd.DataFrame,
    options: pd.DataFrame,
    artifacts: dict[str, Path],
) -> Path:
    quality_by_product = pd.read_csv(PROCESSED_DIR / "derived_round_3_data_quality_by_product.csv")
    trade_alignment = pd.read_csv(PROCESSED_DIR / "derived_round_3_trade_alignment_summary.csv")
    surface_summary = pd.read_csv(PROCESSED_DIR / "derived_round_3_option_surface_summary.csv")
    product_signals = pd.read_csv(PROCESSED_DIR / "derived_round_3_product_signal_metrics.csv")
    option_reversion = pd.read_csv(PROCESSED_DIR / "derived_round_3_option_reversion_metrics.csv")
    linear_model = pd.read_csv(PROCESSED_DIR / "derived_round_3_pooled_option_linear_model.csv")
    mi_scores = pd.read_csv(PROCESSED_DIR / "derived_round_3_option_mutual_information.csv")
    pca_explained = pd.read_csv(PROCESSED_DIR / "derived_round_3_option_pca_explained_variance.csv")

    summary = {
        "raw_counts": {
            "price_rows": int(len(prices)),
            "trade_rows": int(len(trades)),
            "products_in_prices": sorted(prices["product"].unique().tolist()),
            "symbols_in_trades": sorted(trades["symbol"].unique().tolist()),
        },
        "quality_highlights": quality_by_product.to_dict(orient="records"),
        "surface_summary": surface_summary.to_dict(orient="records"),
        "trade_alignment": trade_alignment.to_dict(orient="records"),
        "product_signals": product_signals.to_dict(orient="records"),
        "option_reversion": option_reversion.to_dict(orient="records"),
        "linear_model": linear_model.to_dict(orient="records"),
        "mutual_information": mi_scores.to_dict(orient="records"),
        "pca_explained": pca_explained.to_dict(orient="records"),
        "artifact_paths": {k: str(v.relative_to(ROOT)) for k, v in artifacts.items()},
    }

    path = ARTIFACTS_DIR / "round_3_eda_summary_metrics.json"
    path.write_text(json.dumps(summary, indent=2))
    return path


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    prices = load_prices()
    trades = load_trades()
    options = build_option_panel(prices)

    artifact_paths: dict[str, Path] = {}
    artifact_paths.update(summarize_data_quality(prices, trades))
    artifact_paths["trade_alignment"] = compute_trade_alignment(prices, trades)
    artifact_paths.update(compute_surface_metrics(options))
    artifact_paths.update(compute_cross_product_metrics(prices, options))
    artifact_paths.update(compute_model_artifacts(options))

    extrinsic_by_tte = pd.read_csv(PROCESSED_DIR / "derived_round_3_option_extrinsic_by_tte.csv")
    artifact_paths["plot_extrinsic_surface"] = plot_extrinsic_surface(extrinsic_by_tte)
    artifact_paths["plot_return_corr_heatmap"] = plot_return_corr_heatmap(prices)
    artifact_paths["plot_imbalance_bins"] = plot_imbalance_bins(prices)
    artifact_paths["plot_extrinsic_reversion"] = plot_extrinsic_reversion(options)
    artifact_paths["plot_rel_spread_box"] = plot_rel_spread_box(prices)
    artifact_paths["summary_metrics_json"] = build_summary_metrics(
        prices, trades, options, artifact_paths
    )

    manifest = {name: str(path.relative_to(ROOT)) for name, path in artifact_paths.items()}
    (ARTIFACTS_DIR / "round_3_eda_artifact_manifest.json").write_text(
        json.dumps(manifest, indent=2)
    )


if __name__ == "__main__":
    main()
