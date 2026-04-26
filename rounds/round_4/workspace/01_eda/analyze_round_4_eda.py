from __future__ import annotations

import json
import os
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = SCRIPT_DIR / "artifacts"
os.environ.setdefault("MPLCONFIGDIR", str(ARTIFACTS_DIR / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression


ROOT = SCRIPT_DIR.parents[3]
RAW_DIR = ROOT / "rounds" / "round_4" / "data" / "raw"
PROCESSED_DIR = ROOT / "rounds" / "round_4" / "data" / "processed"


PRODUCT_ROLE_MAP = {
    "HYDROGEL_PACK": "delta-1 base",
    "VELVETFRUIT_EXTRACT": "anchor",
    "VEV_4000": "ITM structural",
    "VEV_4500": "ITM structural",
    "VEV_5000": "active zone",
    "VEV_5100": "active zone",
    "VEV_5200": "active zone",
    "VEV_5300": "active zone",
    "VEV_5400": "upper/passive",
    "VEV_5500": "upper/passive",
    "VEV_6000": "floor/monitor",
    "VEV_6500": "floor/monitor",
}

ACTIVE_ZONE = ["VEV_5000", "VEV_5100", "VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"]
LEAD_LAG_PAIRS = [
    ("HYDROGEL_PACK", "VELVETFRUIT_EXTRACT"),
    ("VELVETFRUIT_EXTRACT", "VEV_4000"),
    ("VELVETFRUIT_EXTRACT", "VEV_5000"),
    ("VELVETFRUIT_EXTRACT", "VEV_5100"),
    ("VELVETFRUIT_EXTRACT", "VEV_5200"),
    ("VELVETFRUIT_EXTRACT", "VEV_5300"),
    ("VELVETFRUIT_EXTRACT", "VEV_5400"),
    ("VELVETFRUIT_EXTRACT", "VEV_5500"),
    ("VEV_5000", "VEV_5300"),
    ("VEV_5100", "VEV_5300"),
    ("VEV_5200", "VEV_5300"),
    ("VEV_5300", "VEV_5400"),
]


def ensure_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def add_time_bucket(values: pd.Series) -> pd.Series:
    conditions = [
        values <= 333300,
        (values >= 333400) & (values <= 666600),
        values >= 666700,
    ]
    choices = ["early", "mid", "late"]
    return pd.Series(np.select(conditions, choices, default="other"), index=values.index)


def save_csv(df: pd.DataFrame, name: str) -> Path:
    path = PROCESSED_DIR / name
    df.to_csv(path, index=False)
    return path


def save_plot(fig: plt.Figure, name: str) -> Path:
    path = ARTIFACTS_DIR / name
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return path


def load_prices() -> pd.DataFrame:
    frames = []
    for path in sorted(RAW_DIR.glob("prices_round_4_day_*.csv")):
        df = pd.read_csv(path, sep=";")
        df["source_file"] = path.name
        frames.append(df)
    prices = pd.concat(frames, ignore_index=True)
    prices["spread"] = prices["ask_price_1"] - prices["bid_price_1"]
    prices["rel_spread_bps"] = np.where(
        prices["mid_price"] != 0,
        prices["spread"] / prices["mid_price"] * 10_000,
        np.nan,
    )
    prices["depth_1"] = prices["bid_volume_1"].fillna(0) + prices["ask_volume_1"].fillna(0)
    denom = prices["depth_1"].replace(0, np.nan)
    prices["imbalance_1"] = (
        prices["bid_volume_1"].fillna(0) - prices["ask_volume_1"].fillna(0)
    ) / denom
    prices["time_bucket"] = add_time_bucket(prices["timestamp"])
    prices["product_role"] = prices["product"].map(PRODUCT_ROLE_MAP).fillna("other")
    prices = prices.sort_values(["product", "day", "timestamp"]).reset_index(drop=True)
    prices["mid_delta_1"] = prices.groupby(["product", "day"])["mid_price"].diff()
    prices["future_mid_delta_5"] = (
        prices.groupby(["product", "day"])["mid_price"].shift(-5) - prices["mid_price"]
    )
    prices["future_mid_return_bps_5"] = np.where(
        prices["mid_price"] != 0,
        prices["future_mid_delta_5"] / prices["mid_price"] * 10_000,
        np.nan,
    )
    return prices


def load_trades() -> pd.DataFrame:
    frames = []
    for path in sorted(RAW_DIR.glob("trades_round_4_day_*.csv")):
        df = pd.read_csv(path, sep=";")
        df["day"] = int(path.stem.split("_")[-1])
        df["source_file"] = path.name
        frames.append(df)
    trades = pd.concat(frames, ignore_index=True)
    trades["quantity"] = trades["quantity"].astype(float)
    trades["price"] = trades["price"].astype(float)
    trades["notional"] = trades["price"] * trades["quantity"]
    trades["time_bucket"] = add_time_bucket(trades["timestamp"])
    trades["product_role"] = trades["symbol"].map(PRODUCT_ROLE_MAP).fillna("other")
    return trades


def summarize_data_quality(prices: pd.DataFrame, trades: pd.DataFrame) -> dict[str, Path]:
    quality_by_file = (
        prices.groupby("source_file")
        .agg(
            rows=("product", "size"),
            unique_products=("product", "nunique"),
            unique_timestamps=("timestamp", "nunique"),
            min_timestamp=("timestamp", "min"),
            max_timestamp=("timestamp", "max"),
            zero_mid_count=("mid_price", lambda s: int((s == 0).sum())),
            constant_mid_products=("product", lambda s: s.nunique()),
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
            mean_abs_imbalance_1=("imbalance_1", lambda s: float(s.abs().mean())),
            zero_mid_share=("mid_price", lambda s: float((s == 0).mean())),
            missing_bid_2_share=("bid_price_2", lambda s: float(s.isna().mean())),
            missing_ask_2_share=("ask_price_2", lambda s: float(s.isna().mean())),
            missing_bid_3_share=("bid_price_3", lambda s: float(s.isna().mean())),
            missing_ask_3_share=("ask_price_3", lambda s: float(s.isna().mean())),
        )
        .reset_index()
    )

    trade_summary_by_symbol_day = (
        trades.groupby(["day", "symbol"])
        .agg(
            trade_count=("symbol", "size"),
            trade_qty=("quantity", "sum"),
            trade_notional=("notional", "sum"),
            avg_trade_price=("price", "mean"),
        )
        .reset_index()
    )

    trade_summary_by_symbol = (
        trades.groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            trade_qty=("quantity", "sum"),
            trade_notional=("notional", "sum"),
            avg_trade_price=("price", "mean"),
        )
        .reset_index()
        .sort_values("trade_count", ascending=False)
    )

    return {
        "quality_by_file": save_csv(
            quality_by_file, "derived_round_4_data_quality_by_file.csv"
        ),
        "quality_by_product": save_csv(
            quality_by_product, "derived_round_4_data_quality_by_product.csv"
        ),
        "trade_summary_by_symbol_day": save_csv(
            trade_summary_by_symbol_day, "derived_round_4_trade_summary_by_symbol_day.csv"
        ),
        "trade_summary_by_symbol": save_csv(
            trade_summary_by_symbol, "derived_round_4_trade_summary_by_symbol.csv"
        ),
    }


def compute_trade_alignment(prices: pd.DataFrame, trades: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Path]]:
    book = prices[
        [
            "day",
            "timestamp",
            "product",
            "bid_price_1",
            "ask_price_1",
            "mid_price",
            "spread",
            "rel_spread_bps",
            "depth_1",
            "imbalance_1",
            "future_mid_delta_5",
            "future_mid_return_bps_5",
            "time_bucket",
        ]
    ].rename(columns={"product": "symbol"})
    aligned = trades.merge(book, on=["day", "timestamp", "symbol", "time_bucket"], how="left")
    aligned["trade_minus_mid"] = aligned["price"] - aligned["mid_price"]
    aligned["at_or_below_bid"] = (aligned["price"] <= aligned["bid_price_1"]).astype(int)
    aligned["at_or_above_ask"] = (aligned["price"] >= aligned["ask_price_1"]).astype(int)

    summary = (
        aligned.groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            avg_trade_minus_mid=("trade_minus_mid", "mean"),
            abs_trade_minus_mid=("trade_minus_mid", lambda s: float(s.abs().mean())),
            share_at_or_below_bid=("at_or_below_bid", "mean"),
            share_at_or_above_ask=("at_or_above_ask", "mean"),
            avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
        )
        .reset_index()
    )

    paths = {
        "trade_alignment": save_csv(summary, "derived_round_4_trade_alignment_summary.csv")
    }
    return aligned, paths


def counterparty_metrics(trades: pd.DataFrame) -> dict[str, Path]:
    buyer_summary = (
        trades.groupby(["day", "buyer"])
        .agg(
            trade_count=("buyer", "size"),
            quantity=("quantity", "sum"),
            notional=("notional", "sum"),
            distinct_products=("symbol", "nunique"),
        )
        .reset_index()
        .rename(columns={"buyer": "counterparty"})
    )
    buyer_summary["side"] = "buyer"

    seller_summary = (
        trades.groupby(["day", "seller"])
        .agg(
            trade_count=("seller", "size"),
            quantity=("quantity", "sum"),
            notional=("notional", "sum"),
            distinct_products=("symbol", "nunique"),
        )
        .reset_index()
        .rename(columns={"seller": "counterparty"})
    )
    seller_summary["side"] = "seller"

    counterparty_summary = pd.concat([buyer_summary, seller_summary], ignore_index=True)

    product_mix = []
    for side_col, side_name in [("buyer", "buyer"), ("seller", "seller")]:
        grouped = (
            trades.groupby(["day", side_col, "symbol"])
            .agg(
                trade_count=("symbol", "size"),
                quantity=("quantity", "sum"),
                notional=("notional", "sum"),
            )
            .reset_index()
            .rename(columns={side_col: "counterparty"})
        )
        grouped["side"] = side_name
        product_mix.append(grouped)
    counterparty_product_mix = pd.concat(product_mix, ignore_index=True)

    time_bucket_summary = []
    for side_col, side_name in [("buyer", "buyer"), ("seller", "seller")]:
        grouped = (
            trades.groupby(["day", side_col, "time_bucket"])
            .agg(
                trade_count=("time_bucket", "size"),
                quantity=("quantity", "sum"),
                notional=("notional", "sum"),
            )
            .reset_index()
            .rename(columns={side_col: "counterparty"})
        )
        grouped["side"] = side_name
        time_bucket_summary.append(grouped)
    counterparty_time_bucket = pd.concat(time_bucket_summary, ignore_index=True)

    side_asymmetry_rows = []
    all_names = sorted(set(trades["buyer"]).union(trades["seller"]))
    for name in all_names:
        buy = trades.loc[trades["buyer"] == name]
        sell = trades.loc[trades["seller"] == name]
        total_count = len(buy) + len(sell)
        total_qty = buy["quantity"].sum() + sell["quantity"].sum()
        total_notional = buy["notional"].sum() + sell["notional"].sum()
        side_asymmetry_rows.append(
            {
                "counterparty": name,
                "buy_trade_count": len(buy),
                "sell_trade_count": len(sell),
                "buy_qty": float(buy["quantity"].sum()),
                "sell_qty": float(sell["quantity"].sum()),
                "buy_notional": float(buy["notional"].sum()),
                "sell_notional": float(sell["notional"].sum()),
                "buy_trade_share": float(len(buy) / total_count) if total_count else np.nan,
                "buy_qty_share": float(buy["quantity"].sum() / total_qty) if total_qty else np.nan,
                "buy_notional_share": float(buy["notional"].sum() / total_notional)
                if total_notional
                else np.nan,
            }
        )
    side_asymmetry = pd.DataFrame(side_asymmetry_rows).sort_values(
        "buy_trade_count", ascending=False
    )

    concentration_rows = []
    for symbol in sorted(trades["symbol"].unique()):
        symbol_df = trades.loc[trades["symbol"] == symbol]
        total_trades = len(symbol_df)
        for side_col, side_name in [("buyer", "buyer"), ("seller", "seller")]:
            counts = symbol_df[side_col].value_counts()
            shares = counts / counts.sum()
            concentration_rows.append(
                {
                    "symbol": symbol,
                    "side": side_name,
                    "trade_count": int(counts.sum()),
                    "unique_counterparties": int(counts.size),
                    "hhi": float((shares**2).sum()),
                    "top1_share": float(shares.iloc[0]) if not shares.empty else np.nan,
                    "top3_share": float(shares.iloc[:3].sum()) if not shares.empty else np.nan,
                    "dominant_counterparty": counts.index[0] if not counts.empty else None,
                }
            )
    concentration = pd.DataFrame(concentration_rows).sort_values(["symbol", "side"])

    stability_rows = []
    top_names = (
        side_asymmetry.assign(total_trade_count=side_asymmetry["buy_trade_count"] + side_asymmetry["sell_trade_count"])
        .sort_values("total_trade_count", ascending=False)["counterparty"]
        .head(8)
        .tolist()
    )
    for name in top_names:
        for day in sorted(trades["day"].unique()):
            buy = trades.loc[(trades["buyer"] == name) & (trades["day"] == day)]
            sell = trades.loc[(trades["seller"] == name) & (trades["day"] == day)]
            all_day = pd.concat([buy.assign(side="buyer"), sell.assign(side="seller")], ignore_index=True)
            dominant_product = all_day["symbol"].value_counts().index[0] if not all_day.empty else None
            dominant_side = all_day["side"].value_counts().index[0] if not all_day.empty else None
            stability_rows.append(
                {
                    "counterparty": name,
                    "day": day,
                    "total_trades": int(len(all_day)),
                    "buy_trades": int(len(buy)),
                    "sell_trades": int(len(sell)),
                    "dominant_product": dominant_product,
                    "dominant_side": dominant_side,
                    "distinct_products": int(all_day["symbol"].nunique()) if not all_day.empty else 0,
                }
            )
    stability = pd.DataFrame(stability_rows)

    return {
        "counterparty_summary": save_csv(
            counterparty_summary, "derived_round_4_counterparty_summary.csv"
        ),
        "counterparty_product_mix": save_csv(
            counterparty_product_mix, "derived_round_4_counterparty_product_mix.csv"
        ),
        "counterparty_time_bucket": save_csv(
            counterparty_time_bucket, "derived_round_4_counterparty_time_bucket.csv"
        ),
        "counterparty_side_asymmetry": save_csv(
            side_asymmetry, "derived_round_4_counterparty_side_asymmetry.csv"
        ),
        "counterparty_concentration": save_csv(
            concentration, "derived_round_4_counterparty_concentration.csv"
        ),
        "counterparty_stability": save_csv(
            stability, "derived_round_4_counterparty_stability.csv"
        ),
    }


def option_book_metrics(prices: pd.DataFrame, trades: pd.DataFrame) -> dict[str, Path]:
    option_prices = prices.loc[prices["product"].str.startswith("VEV_")].copy()
    option_prices["strike"] = option_prices["product"].str.split("_").str[1].astype(int)

    option_trade_summary = (
        trades.loc[trades["symbol"].str.startswith("VEV_")]
        .groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            trade_qty=("quantity", "sum"),
            trade_notional=("notional", "sum"),
        )
        .reset_index()
        .rename(columns={"symbol": "product"})
    )

    option_quote_summary = (
        option_prices.groupby("product")
        .agg(
            strike=("strike", "first"),
            quote_rows=("product", "size"),
            mean_mid=("mid_price", "mean"),
            std_mid=("mid_price", "std"),
            mean_spread=("spread", "mean"),
            median_spread=("spread", "median"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            mean_abs_imbalance_1=("imbalance_1", lambda s: float(s.abs().mean())),
            zero_mid_share=("mid_price", lambda s: float((s == 0).mean())),
        )
        .reset_index()
    )

    option_book_summary = option_quote_summary.merge(
        option_trade_summary, on="product", how="left"
    ).fillna({"trade_count": 0, "trade_qty": 0, "trade_notional": 0})
    option_book_summary["product_role"] = option_book_summary["product"].map(PRODUCT_ROLE_MAP)

    local_cross_strike = []
    pivot = option_prices.pivot_table(
        index=["day", "timestamp"], columns="product", values="mid_price"
    )
    returns = pivot.groupby(level=0).pct_change()
    for left, right in zip(ACTIVE_ZONE[:-1], ACTIVE_ZONE[1:]):
        pair = returns[[left, right]].dropna()
        corr = pair[left].corr(pair[right]) if not pair.empty else np.nan
        spread_gap = (
            option_book_summary.set_index("product").loc[right, "mean_rel_spread_bps"]
            - option_book_summary.set_index("product").loc[left, "mean_rel_spread_bps"]
        )
        trade_count_gap = (
            option_book_summary.set_index("product").loc[right, "trade_count"]
            - option_book_summary.set_index("product").loc[left, "trade_count"]
        )
        local_cross_strike.append(
            {
                "left_product": left,
                "right_product": right,
                "same_time_return_corr": corr,
                "right_minus_left_rel_spread_bps": spread_gap,
                "right_minus_left_trade_count": trade_count_gap,
            }
        )
    local_cross_strike_df = pd.DataFrame(local_cross_strike)

    family_liquidity = (
        prices.groupby(["product_role", "time_bucket"])
        .agg(
            rows=("product", "size"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            mean_abs_mid_delta_1=("mid_delta_1", lambda s: float(s.abs().mean())),
        )
        .reset_index()
    )

    return {
        "option_book_summary": save_csv(
            option_book_summary, "derived_round_4_option_book_summary.csv"
        ),
        "local_cross_strike": save_csv(
            local_cross_strike_df, "derived_round_4_local_cross_strike_context.csv"
        ),
        "family_liquidity": save_csv(
            family_liquidity, "derived_round_4_family_liquidity_by_time_bucket.csv"
        ),
    }


def cross_product_metrics(prices: pd.DataFrame) -> dict[str, Path]:
    pivot = prices.pivot_table(index=["day", "timestamp"], columns="product", values="mid_price")
    returns = pivot.groupby(level=0).pct_change().replace([np.inf, -np.inf], np.nan)

    corr_matrix = returns.corr().reset_index()
    cov_matrix = returns.cov().reset_index()

    lead_lag_rows = []
    for left, right in LEAD_LAG_PAIRS:
        for lag in [0, 1, 2, 5, 10]:
            aligned = pd.concat(
                [
                    returns[left],
                    returns.groupby(level=0)[right].shift(-lag),
                ],
                axis=1,
                keys=["left_ret", "right_ret"],
            ).dropna()
            corr = aligned["left_ret"].corr(aligned["right_ret"]) if not aligned.empty else np.nan
            lead_lag_rows.append(
                {
                    "left_product": left,
                    "right_product": right,
                    "lag_steps": lag,
                    "corr": corr,
                    "sample_size": int(len(aligned)),
                }
            )
    lead_lag = pd.DataFrame(lead_lag_rows)

    return {
        "corr_matrix": save_csv(corr_matrix, "derived_round_4_same_time_return_corr.csv"),
        "cov_matrix": save_csv(cov_matrix, "derived_round_4_same_time_return_covariance.csv"),
        "lead_lag": save_csv(lead_lag, "derived_round_4_lead_lag_summary.csv"),
    }


def feature_and_regime_metrics(prices: pd.DataFrame, trade_aligned: pd.DataFrame) -> dict[str, Path]:
    feature_cols = ["rel_spread_bps", "imbalance_1", "depth_1", "quantity", "future_mid_return_bps_5"]
    feature_frame = (
        trade_aligned[feature_cols]
        .replace([np.inf, -np.inf], np.nan)
        .dropna()
    )
    corr_path = save_csv(
        feature_frame.corr().reset_index(),
        "derived_round_4_trade_feature_corr.csv",
    )
    cov_path = save_csv(
        feature_frame.cov().reset_index(),
        "derived_round_4_trade_feature_covariance.csv",
    )

    model_df = trade_aligned[
        [
            "symbol",
            "time_bucket",
            "buyer",
            "seller",
            "rel_spread_bps",
            "imbalance_1",
            "depth_1",
            "quantity",
            "future_mid_return_bps_5",
        ]
    ].replace([np.inf, -np.inf], np.nan)
    model_df = model_df.dropna()

    top_buyers = model_df["buyer"].value_counts().head(5).index.tolist()
    top_sellers = model_df["seller"].value_counts().head(5).index.tolist()
    model_df["buyer_bucket"] = np.where(model_df["buyer"].isin(top_buyers), model_df["buyer"], "OTHER_BUYER")
    model_df["seller_bucket"] = np.where(model_df["seller"].isin(top_sellers), model_df["seller"], "OTHER_SELLER")

    X = pd.get_dummies(
        model_df[
            [
                "symbol",
                "time_bucket",
                "buyer_bucket",
                "seller_bucket",
                "rel_spread_bps",
                "imbalance_1",
                "depth_1",
                "quantity",
            ]
        ],
        columns=["symbol", "time_bucket", "buyer_bucket", "seller_bucket"],
        drop_first=False,
    )
    y = model_df["future_mid_return_bps_5"]
    model = LinearRegression()
    model.fit(X, y)
    r2 = model.score(X, y)
    coeffs = pd.DataFrame({"feature": X.columns, "coefficient": model.coef_})
    coeffs["abs_coefficient"] = coeffs["coefficient"].abs()
    coeffs = coeffs.sort_values("abs_coefficient", ascending=False)
    coeffs["r2"] = r2
    regression_path = save_csv(
        coeffs, "derived_round_4_counterparty_controlled_regression.csv"
    )

    product_regime = (
        prices.groupby(["product", "time_bucket"])
        .agg(
            rows=("product", "size"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            mean_abs_mid_delta_1=("mid_delta_1", lambda s: float(s.abs().mean())),
        )
        .reset_index()
    )
    product_regime["product_role"] = product_regime["product"].map(PRODUCT_ROLE_MAP)

    counterparty_conditioned = (
        trade_aligned.assign(
            buyer_bucket=np.where(
                trade_aligned["buyer"].isin(top_buyers), trade_aligned["buyer"], "OTHER_BUYER"
            ),
            seller_bucket=np.where(
                trade_aligned["seller"].isin(top_sellers), trade_aligned["seller"], "OTHER_SELLER"
            ),
        )
        .groupby(["symbol", "buyer_bucket", "seller_bucket"])
        .agg(
            trade_count=("symbol", "size"),
            avg_rel_spread_bps=("rel_spread_bps", "mean"),
            avg_imbalance_1=("imbalance_1", "mean"),
            avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
        )
        .reset_index()
    )

    family_conditioned = (
        prices.groupby(["product_role", "time_bucket"])
        .agg(
            rows=("product", "size"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            mean_abs_imbalance_1=("imbalance_1", lambda s: float(s.abs().mean())),
            mean_abs_mid_delta_1=("mid_delta_1", lambda s: float(s.abs().mean())),
        )
        .reset_index()
    )

    return {
        "trade_feature_corr": corr_path,
        "trade_feature_covariance": cov_path,
        "counterparty_regression": regression_path,
        "product_regime": save_csv(
            product_regime, "derived_round_4_product_regime_summary.csv"
        ),
        "counterparty_conditioned": save_csv(
            counterparty_conditioned,
            "derived_round_4_counterparty_conditioned_summary.csv",
        ),
        "family_conditioned": save_csv(
            family_conditioned, "derived_round_4_family_conditioned_regime_summary.csv"
        ),
    }


def build_plots(
    prices: pd.DataFrame,
    trades: pd.DataFrame,
    counterparty_product_mix: Path,
    corr_matrix_path: Path,
) -> dict[str, Path]:
    plot_paths: dict[str, Path] = {}

    mix = pd.read_csv(counterparty_product_mix)
    mix = mix[mix["side"] == "buyer"].copy()
    top_buyers = (
        mix.groupby("counterparty")["trade_count"].sum().sort_values(ascending=False).head(5).index
    )
    mix = mix[mix["counterparty"].isin(top_buyers)]
    heat = mix.pivot_table(
        index="counterparty", columns="symbol", values="trade_count", aggfunc="sum", fill_value=0
    )
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heat, cmap="Blues", ax=ax)
    ax.set_title("Round 4 buyer-side product mix by top counterparties")
    plot_paths["counterparty_product_mix_heatmap"] = save_plot(
        fig, "round_4_counterparty_product_mix_heatmap.png"
    )

    corr = pd.read_csv(corr_matrix_path).rename(columns={"product": "product"})
    corr = corr.set_index(corr.columns[0])
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Round 4 same-time return correlations")
    plot_paths["return_corr_heatmap"] = save_plot(fig, "round_4_return_corr_heatmap.png")

    product_order = list(PRODUCT_ROLE_MAP.keys())
    fig, ax = plt.subplots(figsize=(11, 4))
    sns.boxplot(
        data=prices,
        x="product",
        y="rel_spread_bps",
        order=product_order,
        ax=ax,
    )
    ax.set_yscale("symlog")
    ax.set_title("Round 4 relative spread by product")
    ax.tick_params(axis="x", rotation=45)
    plot_paths["relative_spread_boxplot"] = save_plot(
        fig, "round_4_relative_spread_boxplot.png"
    )

    top_names = trades["buyer"].value_counts().head(4).index.tolist()
    timing = (
        trades.loc[trades["buyer"].isin(top_names)]
        .groupby(["buyer", "time_bucket"])
        .size()
        .reset_index(name="trade_count")
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=timing, x="buyer", y="trade_count", hue="time_bucket", ax=ax)
    ax.set_title("Top buyers by time bucket")
    ax.tick_params(axis="x", rotation=25)
    plot_paths["top_buyer_timing"] = save_plot(fig, "round_4_top_buyer_timing.png")

    return plot_paths


def write_manifest(paths: dict[str, Path], summary: dict) -> None:
    manifest = {
        "processed_outputs": {k: str(v.relative_to(ROOT)) for k, v in paths.items()},
        "summary_metrics": summary,
    }
    manifest_path = ARTIFACTS_DIR / "round_4_eda_artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True))

    summary_path = ARTIFACTS_DIR / "round_4_eda_summary_metrics.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True))


def build_summary_metrics(
    prices: pd.DataFrame,
    trades: pd.DataFrame,
    counterparty_concentration_path: Path,
    option_book_summary_path: Path,
    regression_path: Path,
) -> dict:
    concentration = pd.read_csv(counterparty_concentration_path)
    option_book = pd.read_csv(option_book_summary_path)
    regression = pd.read_csv(regression_path)

    top_buyers = trades["buyer"].value_counts().head(6).to_dict()
    top_sellers = trades["seller"].value_counts().head(6).to_dict()

    summary = {
        "price_rows_total": int(len(prices)),
        "trade_rows_total": int(len(trades)),
        "products_present": sorted(prices["product"].unique().tolist()),
        "trade_symbols_present": sorted(trades["symbol"].unique().tolist()),
        "top_buyers": top_buyers,
        "top_sellers": top_sellers,
        "dominant_symbol_by_trade_count": (
            trades["symbol"].value_counts().head(8).to_dict()
        ),
        "concentration_top1_share_by_symbol_side": concentration[
            ["symbol", "side", "top1_share", "dominant_counterparty"]
        ].to_dict(orient="records"),
        "option_book_trade_counts": option_book.set_index("product")["trade_count"].to_dict(),
        "option_book_rel_spread_bps": option_book.set_index("product")[
            "mean_rel_spread_bps"
        ].round(4).to_dict(),
        "controlled_regression_r2": float(regression["r2"].iloc[0]) if not regression.empty else None,
        "top_regression_coefficients": regression.head(12)[["feature", "coefficient"]].to_dict(
            orient="records"
        ),
    }
    return summary


def main() -> None:
    ensure_dirs()
    prices = load_prices()
    trades = load_trades()

    output_paths: dict[str, Path] = {}
    output_paths.update(summarize_data_quality(prices, trades))
    trade_aligned, trade_alignment_paths = compute_trade_alignment(prices, trades)
    output_paths.update(trade_alignment_paths)
    counterparty_paths = counterparty_metrics(trades)
    output_paths.update(counterparty_paths)
    option_paths = option_book_metrics(prices, trades)
    output_paths.update(option_paths)
    cross_paths = cross_product_metrics(prices)
    output_paths.update(cross_paths)
    feature_paths = feature_and_regime_metrics(prices, trade_aligned)
    output_paths.update(feature_paths)
    plot_paths = build_plots(
        prices,
        trades,
        counterparty_paths["counterparty_product_mix"],
        cross_paths["corr_matrix"],
    )
    output_paths.update(plot_paths)

    summary = build_summary_metrics(
        prices,
        trades,
        counterparty_paths["counterparty_concentration"],
        option_paths["option_book_summary"],
        feature_paths["counterparty_regression"],
    )
    write_manifest(output_paths, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
