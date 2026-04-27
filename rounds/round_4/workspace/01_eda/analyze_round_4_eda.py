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
from scipy.optimize import brentq, minimize, minimize_scalar
from scipy.stats import norm
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
FUTURE_HORIZONS = [1, 5, 10]
TTE_DAYS_BY_DAY = {1: 4, 2: 3, 3: 2}
TRADING_DAYS_PER_YEAR = 252.0
OPTION_PANEL_EXCLUDED_STRIKES = {6000, 6500}
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


def bs_call_price(spot: float, strike: float, tau: float, sigma: float, rate: float = 0.0) -> float:
    if tau <= 0:
        return max(spot - strike, 0.0)
    sigma = max(float(sigma), 1e-12)
    spot = max(float(spot), 1e-12)
    strike = max(float(strike), 1e-12)
    sqrt_tau = np.sqrt(tau)
    d1 = (np.log(spot / strike) + (rate + 0.5 * sigma * sigma) * tau) / (sigma * sqrt_tau)
    d2 = d1 - sigma * sqrt_tau
    return float(spot * norm.cdf(d1) - strike * np.exp(-rate * tau) * norm.cdf(d2))


def bs_implied_vol(spot: float, strike: float, tau: float, price: float, rate: float = 0.0) -> float:
    intrinsic = max(spot - strike * np.exp(-rate * tau), 0.0)
    if tau <= 0 or price <= intrinsic + 1e-9 or price >= spot:
        return np.nan

    def objective(sigma: float) -> float:
        return bs_call_price(spot, strike, tau, sigma, rate) - price

    try:
        return float(brentq(objective, 1e-6, 5.0, maxiter=200))
    except Exception:
        return np.nan


def bs_greeks(spot: float, strike: float, tau: float, sigma: float, rate: float = 0.0) -> dict[str, float]:
    if tau <= 0 or not np.isfinite(sigma) or sigma <= 0:
        intrinsic_delta = 1.0 if spot > strike else 0.0
        return {"delta": intrinsic_delta, "gamma": np.nan, "vega": np.nan, "theta": np.nan}
    sqrt_tau = np.sqrt(tau)
    d1 = (np.log(spot / strike) + (rate + 0.5 * sigma * sigma) * tau) / (sigma * sqrt_tau)
    d2 = d1 - sigma * sqrt_tau
    pdf_d1 = norm.pdf(d1)
    return {
        "delta": float(norm.cdf(d1)),
        "gamma": float(pdf_d1 / (spot * sigma * sqrt_tau)),
        "vega": float(spot * pdf_d1 * sqrt_tau),
        "theta": float(
            -(spot * pdf_d1 * sigma) / (2 * sqrt_tau) - rate * strike * np.exp(-rate * tau) * norm.cdf(d2)
        ),
    }


def heston_characteristic_function(
    u: np.ndarray,
    spot: float,
    tau: float,
    rate: float,
    kappa: float,
    theta: float,
    volvol: float,
    rho: float,
    v0: float,
) -> np.ndarray:
    x0 = np.log(max(spot, 1e-12))
    iu = 1j * u
    d = np.sqrt((rho * volvol * iu - kappa) ** 2 + volvol * volvol * (iu + u * u))
    g = (kappa - rho * volvol * iu - d) / (kappa - rho * volvol * iu + d + 1e-18)
    exp_dt = np.exp(-d * tau)
    c_term = (
        rate * iu * tau
        + (kappa * theta / (volvol * volvol))
        * ((kappa - rho * volvol * iu - d) * tau - 2.0 * np.log((1.0 - g * exp_dt) / (1.0 - g + 1e-18)))
    )
    d_term = ((kappa - rho * volvol * iu - d) / (volvol * volvol)) * ((1.0 - exp_dt) / (1.0 - g * exp_dt + 1e-18))
    return np.exp(c_term + d_term * v0 + iu * x0)


def cos_call_payoff_coefficients(a: float, b: float, n_terms: int) -> tuple[np.ndarray, np.ndarray]:
    k = np.arange(n_terms, dtype=float)
    u = k * np.pi / (b - a)
    c = 0.0
    d = max(b, 0.0)
    exp_c = np.exp(c)
    exp_d = np.exp(d)
    chi = (
        exp_d * (np.cos(u * (d - a)) + u * np.sin(u * (d - a)))
        - exp_c * (np.cos(u * (c - a)) + u * np.sin(u * (c - a)))
    ) / (1.0 + u * u)
    psi = np.zeros_like(u)
    psi[0] = d - c
    if len(u) > 1:
        psi[1:] = (np.sin(u[1:] * (d - a)) - np.sin(u[1:] * (c - a))) / u[1:]
    vk = 2.0 / (b - a) * (chi - psi)
    return u, vk


def heston_cos_call_price(
    spot: float,
    strike: float,
    tau: float,
    rate: float,
    kappa: float,
    theta: float,
    volvol: float,
    rho: float,
    v0: float,
    n_terms: int = 128,
    truncation_l: float = 10.0,
) -> float:
    if tau <= 0:
        return max(spot - strike, 0.0)
    var_proxy = max(theta, v0, 1e-8) * tau
    c1 = np.log(max(spot / strike, 1e-12)) + (rate - 0.5 * theta) * tau
    c2 = max(var_proxy, 1e-8)
    a = c1 - truncation_l * np.sqrt(c2)
    b = c1 + truncation_l * np.sqrt(c2)
    if b <= 0:
        return max(spot - strike, 0.0)
    u, vk = cos_call_payoff_coefficients(a, b, n_terms)
    cf_y = np.exp(-1j * u * np.log(max(strike, 1e-12))) * heston_characteristic_function(
        u, spot, tau, rate, kappa, theta, volvol, rho, v0
    )
    coeff = np.real(cf_y * np.exp(-1j * u * a))
    coeff[0] *= 0.5
    price = np.exp(-rate * tau) * strike * np.sum(coeff * vk)
    return float(max(price, 0.0))


def fit_bs_constant_vol(panel: pd.DataFrame, rate: float = 0.0) -> tuple[float, float]:
    if panel.empty:
        return np.nan, np.nan
    spot = float(panel["panel_spot"].iloc[0])
    tau = float(panel["tau_years"].iloc[0])
    strikes = panel["strike"].to_numpy(dtype=float)
    market = panel["panel_mid"].to_numpy(dtype=float)

    def objective(sigma: float) -> float:
        model = np.array([bs_call_price(spot, k, tau, sigma, rate) for k in strikes])
        return float(np.mean((model - market) ** 2))

    result = minimize_scalar(objective, bounds=(1e-4, 5.0), method="bounded")
    sigma = float(result.x) if result.success else np.nan
    rmse = float(np.sqrt(result.fun)) if result.success else np.nan
    return sigma, rmse


def fit_heston_panel(panel: pd.DataFrame, rate: float = 0.0) -> dict[str, float]:
    if len(panel) < 4:
        return {
            "success": 0,
            "v0": np.nan,
            "kappa": np.nan,
            "theta": np.nan,
            "volvol": np.nan,
            "rho": np.nan,
            "rmse": np.nan,
        }
    spot = float(panel["panel_spot"].iloc[0])
    tau = float(panel["tau_years"].iloc[0])
    strikes = panel["strike"].to_numpy(dtype=float)
    market = panel["panel_mid"].to_numpy(dtype=float)
    bs_seed = panel["bs_iv"].dropna().median()
    base_var = max(float(bs_seed) ** 2 if pd.notna(bs_seed) else 0.04, 1e-4)

    def objective(params: np.ndarray) -> float:
        v0, kappa, theta, volvol, rho = params
        try:
            model = np.array(
                [
                    heston_cos_call_price(spot, k, tau, rate, kappa, theta, volvol, rho, v0)
                    for k in strikes
                ]
            )
            if not np.all(np.isfinite(model)):
                return 1e9
            return float(np.mean((model - market) ** 2))
        except Exception:
            return 1e9

    result = minimize(
        objective,
        x0=np.array([base_var, 2.0, base_var, max(np.sqrt(base_var), 0.2), -0.5]),
        bounds=[(1e-6, 4.0), (0.1, 20.0), (1e-6, 4.0), (0.05, 5.0), (-0.99, 0.99)],
        method="L-BFGS-B",
        options={"maxiter": 120},
    )
    params = result.x if result.success else [np.nan] * 5
    return {
        "success": int(bool(result.success)),
        "v0": float(params[0]),
        "kappa": float(params[1]),
        "theta": float(params[2]),
        "volvol": float(params[3]),
        "rho": float(params[4]),
        "rmse": float(np.sqrt(result.fun)) if result.success else np.nan,
    }


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
    for horizon in FUTURE_HORIZONS:
        prices[f"future_mid_delta_{horizon}"] = (
            prices.groupby(["product", "day"])["mid_price"].shift(-horizon) - prices["mid_price"]
        )
        prices[f"future_mid_return_bps_{horizon}"] = np.where(
            prices["mid_price"] != 0,
            prices[f"future_mid_delta_{horizon}"] / prices["mid_price"] * 10_000,
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
            "time_bucket",
            *[f"future_mid_delta_{h}" for h in FUTURE_HORIZONS],
            *[f"future_mid_return_bps_{h}" for h in FUTURE_HORIZONS],
        ]
    ].rename(columns={"product": "symbol"})
    aligned = trades.merge(book, on=["day", "timestamp", "symbol", "time_bucket"], how="left")
    aligned["trade_minus_mid"] = aligned["price"] - aligned["mid_price"]
    aligned["at_or_below_bid"] = (aligned["price"] <= aligned["bid_price_1"]).astype(int)
    aligned["at_or_above_ask"] = (aligned["price"] >= aligned["ask_price_1"]).astype(int)
    aligned["trade_location_bucket"] = np.select(
        [
            aligned["price"] <= aligned["bid_price_1"],
            aligned["price"] >= aligned["ask_price_1"],
        ],
        ["at_or_below_bid", "at_or_above_ask"],
        default="inside_spread",
    )
    for horizon in FUTURE_HORIZONS:
        aligned[f"buyer_alpha_bps_{horizon}"] = aligned[f"future_mid_return_bps_{horizon}"]
        aligned[f"seller_alpha_bps_{horizon}"] = -aligned[f"future_mid_return_bps_{horizon}"]

    summary = (
        aligned.groupby("symbol")
        .agg(
            trade_count=("symbol", "size"),
            avg_trade_minus_mid=("trade_minus_mid", "mean"),
            abs_trade_minus_mid=("trade_minus_mid", lambda s: float(s.abs().mean())),
            share_at_or_below_bid=("at_or_below_bid", "mean"),
            share_at_or_above_ask=("at_or_above_ask", "mean"),
            avg_future_mid_return_bps_1=("future_mid_return_bps_1", "mean"),
            avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
            avg_future_mid_return_bps_10=("future_mid_return_bps_10", "mean"),
        )
        .reset_index()
    )

    side_markout_frames = []
    by_symbol_frames = []
    for side_name, counterparty_col, alpha_prefix in [
        ("buyer", "buyer", "buyer_alpha_bps"),
        ("seller", "seller", "seller_alpha_bps"),
    ]:
        side_summary = (
            aligned.groupby(counterparty_col)
            .agg(
                trade_count=("symbol", "size"),
                quantity=("quantity", "sum"),
                notional=("notional", "sum"),
                distinct_symbols=("symbol", "nunique"),
                avg_rel_spread_bps=("rel_spread_bps", "mean"),
                avg_depth_1=("depth_1", "mean"),
                avg_imbalance_1=("imbalance_1", "mean"),
                avg_trade_minus_mid=("trade_minus_mid", "mean"),
                share_at_or_below_bid=("at_or_below_bid", "mean"),
                share_at_or_above_ask=("at_or_above_ask", "mean"),
                inside_spread_share=("trade_location_bucket", lambda s: float((s == "inside_spread").mean())),
                avg_future_mid_return_bps_1=("future_mid_return_bps_1", "mean"),
                avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
                avg_future_mid_return_bps_10=("future_mid_return_bps_10", "mean"),
                avg_side_alpha_bps_1=(f"{alpha_prefix}_1", "mean"),
                avg_side_alpha_bps_5=(f"{alpha_prefix}_5", "mean"),
                avg_side_alpha_bps_10=(f"{alpha_prefix}_10", "mean"),
            )
            .reset_index()
            .rename(columns={counterparty_col: "counterparty"})
        )
        side_summary["side"] = side_name
        side_markout_frames.append(side_summary)

        by_symbol = (
            aligned.groupby([counterparty_col, "symbol"])
            .agg(
                trade_count=("symbol", "size"),
                quantity=("quantity", "sum"),
                avg_rel_spread_bps=("rel_spread_bps", "mean"),
                avg_depth_1=("depth_1", "mean"),
                avg_imbalance_1=("imbalance_1", "mean"),
                avg_trade_minus_mid=("trade_minus_mid", "mean"),
                share_at_or_below_bid=("at_or_below_bid", "mean"),
                share_at_or_above_ask=("at_or_above_ask", "mean"),
                avg_side_alpha_bps_1=(f"{alpha_prefix}_1", "mean"),
                avg_side_alpha_bps_5=(f"{alpha_prefix}_5", "mean"),
                avg_side_alpha_bps_10=(f"{alpha_prefix}_10", "mean"),
            )
            .reset_index()
            .rename(columns={counterparty_col: "counterparty"})
        )
        by_symbol["side"] = side_name
        by_symbol_frames.append(by_symbol)

    counterparty_markout = pd.concat(side_markout_frames, ignore_index=True).sort_values(
        ["trade_count", "counterparty"], ascending=[False, True]
    )
    counterparty_markout_by_symbol_side = pd.concat(
        by_symbol_frames, ignore_index=True
    ).sort_values(["trade_count", "counterparty", "symbol"], ascending=[False, True, True])

    pair_summary = (
        aligned.groupby(["buyer", "seller"])
        .agg(
            trade_count=("symbol", "size"),
            quantity=("quantity", "sum"),
            notional=("notional", "sum"),
            distinct_symbols=("symbol", "nunique"),
            dominant_symbol=("symbol", lambda s: s.value_counts().index[0]),
            avg_rel_spread_bps=("rel_spread_bps", "mean"),
            avg_future_mid_return_bps_1=("future_mid_return_bps_1", "mean"),
            avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
            avg_future_mid_return_bps_10=("future_mid_return_bps_10", "mean"),
        )
        .reset_index()
        .sort_values(["trade_count", "notional"], ascending=[False, False])
    )

    paths = {
        "trade_alignment": save_csv(summary, "derived_round_4_trade_alignment_summary.csv"),
        "counterparty_markout": save_csv(
            counterparty_markout, "derived_round_4_counterparty_markout_by_side.csv"
        ),
        "counterparty_markout_by_symbol_side": save_csv(
            counterparty_markout_by_symbol_side,
            "derived_round_4_counterparty_markout_by_symbol_side.csv",
        ),
        "counterparty_pair_summary": save_csv(
            pair_summary, "derived_round_4_counterparty_pair_summary.csv"
        ),
        "counterparty_book_context": save_csv(
            counterparty_markout_by_symbol_side,
            "derived_round_4_counterparty_book_context.csv",
        ),
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
    for name in all_names:
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

    stability_score_rows = []
    for name in all_names:
        side_row = side_asymmetry.loc[side_asymmetry["counterparty"] == name].iloc[0]
        day_rows = stability.loc[stability["counterparty"] == name]
        active_day_rows = day_rows.loc[day_rows["total_trades"] > 0]
        buy = trades.loc[trades["buyer"] == name]
        sell = trades.loc[trades["seller"] == name]
        all_trades = pd.concat([buy.assign(side="buyer"), sell.assign(side="seller")], ignore_index=True)
        product_counts = all_trades["symbol"].value_counts()
        product_shares = product_counts / product_counts.sum() if not product_counts.empty else pd.Series(dtype=float)
        total_trade_count = int(side_row["buy_trade_count"] + side_row["sell_trade_count"])
        days_present = int(active_day_rows["day"].nunique())
        dominant_product = product_counts.index[0] if not product_counts.empty else None
        dominant_product_share = float(product_shares.iloc[0]) if not product_shares.empty else np.nan
        product_hhi = float((product_shares**2).sum()) if not product_shares.empty else np.nan
        global_dominant_side = (
            "buyer" if side_row["buy_trade_count"] >= side_row["sell_trade_count"] else "seller"
        )
        dominant_product_consistency = (
            float((active_day_rows["dominant_product"] == dominant_product).mean())
            if dominant_product is not None and not active_day_rows.empty
            else np.nan
        )
        dominant_side_consistency = (
            float((active_day_rows["dominant_side"] == global_dominant_side).mean())
            if not active_day_rows.empty
            else np.nan
        )
        buy_trade_share_std = (
            float(
                active_day_rows.apply(
                    lambda row: row["buy_trades"] / row["total_trades"] if row["total_trades"] else np.nan,
                    axis=1,
                ).std(ddof=0)
            )
            if not active_day_rows.empty
            else np.nan
        )

        if total_trade_count < 25 or days_present < 2:
            stability_class = "small sample"
        elif dominant_product_share >= 0.75 and all_trades["symbol"].nunique() <= 2:
            stability_class = "stable specialist"
        elif (
            dominant_product_consistency >= 2 / 3
            and dominant_side_consistency >= 2 / 3
            and all_trades["symbol"].nunique() >= 3
        ):
            stability_class = "stable broad"
        else:
            stability_class = "mixed / rotating"

        stability_score_rows.append(
            {
                "counterparty": name,
                "total_trade_count": total_trade_count,
                "days_present": days_present,
                "global_dominant_product": dominant_product,
                "global_dominant_side": global_dominant_side,
                "dominant_product_share": dominant_product_share,
                "dominant_product_consistency": dominant_product_consistency,
                "dominant_side_consistency": dominant_side_consistency,
                "distinct_products_total": int(all_trades["symbol"].nunique()) if not all_trades.empty else 0,
                "buy_trade_share_mean": float(side_row["buy_trade_share"]) if pd.notna(side_row["buy_trade_share"]) else np.nan,
                "buy_trade_share_std": buy_trade_share_std,
                "product_concentration_hhi": product_hhi,
                "stability_class": stability_class,
            }
        )
    stability_scores = pd.DataFrame(stability_score_rows).sort_values(
        ["total_trade_count", "counterparty"], ascending=[False, True]
    )

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
        "counterparty_stability_scores": save_csv(
            stability_scores, "derived_round_4_counterparty_stability_scores.csv"
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


def advanced_option_metrics(prices: pd.DataFrame, trades: pd.DataFrame) -> dict[str, Path]:
    vex = prices.loc[prices["product"] == "VELVETFRUIT_EXTRACT", ["day", "timestamp", "mid_price"]].rename(
        columns={"mid_price": "underlying_mid"}
    )
    option_quotes = prices.loc[prices["product"].str.startswith("VEV_")].copy()
    option_quotes["strike"] = option_quotes["product"].str.split("_").str[1].astype(int)
    option_quotes = option_quotes.merge(vex, on=["day", "timestamp"], how="left")
    option_quotes["tte_days"] = option_quotes["day"].map(TTE_DAYS_BY_DAY)
    option_quotes["tau_years"] = option_quotes["tte_days"] / TRADING_DAYS_PER_YEAR
    option_quotes["intrinsic_value"] = (option_quotes["underlying_mid"] - option_quotes["strike"]).clip(lower=0.0)
    option_quotes["extrinsic_value"] = option_quotes["mid_price"] - option_quotes["intrinsic_value"]
    option_quotes["moneyness"] = option_quotes["underlying_mid"] / option_quotes["strike"]

    trade_activity = (
        trades.loc[trades["symbol"].str.startswith("VEV_")]
        .groupby(["day", "time_bucket", "symbol"])
        .agg(trade_count=("symbol", "size"), trade_notional=("notional", "sum"))
        .reset_index()
        .rename(columns={"symbol": "product"})
    )

    option_panel = (
        option_quotes.groupby(["day", "time_bucket", "product", "strike"])
        .agg(
            panel_mid=("mid_price", "median"),
            panel_spot=("underlying_mid", "median"),
            mean_spread=("spread", "mean"),
            mean_rel_spread_bps=("rel_spread_bps", "mean"),
            mean_depth_1=("depth_1", "mean"),
            mean_imbalance_1=("imbalance_1", "mean"),
            intrinsic_value=("intrinsic_value", "median"),
            extrinsic_value=("extrinsic_value", "median"),
            moneyness=("moneyness", "median"),
            tau_years=("tau_years", "median"),
            tte_days=("tte_days", "median"),
        )
        .reset_index()
        .merge(trade_activity, on=["day", "time_bucket", "product"], how="left")
        .fillna({"trade_count": 0, "trade_notional": 0.0})
    )

    option_panel["bs_iv"] = option_panel.apply(
        lambda row: bs_implied_vol(
            row["panel_spot"], row["strike"], row["tau_years"], row["panel_mid"], 0.0
        ),
        axis=1,
    )
    option_panel["bs_iv_valid"] = option_panel["bs_iv"].notna().astype(int)
    greek_rows = option_panel.apply(
        lambda row: bs_greeks(row["panel_spot"], row["strike"], row["tau_years"], row["bs_iv"], 0.0),
        axis=1,
    )
    greek_df = pd.DataFrame(list(greek_rows))
    option_panel = pd.concat([option_panel, greek_df], axis=1)

    iv_surface_summary = (
        option_panel.groupby(["day", "product", "strike"])
        .agg(
            median_bs_iv=("bs_iv", "median"),
            mean_bs_iv=("bs_iv", "mean"),
            bs_iv_valid_share=("bs_iv_valid", "mean"),
            median_delta=("delta", "median"),
            median_gamma=("gamma", "median"),
            median_vega=("vega", "median"),
            median_theta=("theta", "median"),
            median_extrinsic_value=("extrinsic_value", "median"),
            total_trade_count=("trade_count", "sum"),
        )
        .reset_index()
    )

    smile_rows = []
    fit_rows = []
    residual_rows = []
    fit_input = option_panel.loc[~option_panel["strike"].isin(OPTION_PANEL_EXCLUDED_STRIKES)].copy()
    for (day, time_bucket), panel in fit_input.groupby(["day", "time_bucket"]):
        panel = panel.loc[(panel["panel_mid"] > 0) & panel["panel_spot"].notna()].copy()
        if panel.empty:
            continue
        panel = panel.sort_values("strike")
        valid_iv = panel.loc[panel["bs_iv"].notna()].copy()
        if len(valid_iv) >= 3:
            x = np.log(valid_iv["strike"] / valid_iv["panel_spot"])
            y = valid_iv["bs_iv"]
            coeff = np.polyfit(x, y, deg=2)
            smile_rows.append(
                {
                    "day": day,
                    "time_bucket": time_bucket,
                    "tte_days": float(panel["tte_days"].iloc[0]),
                    "smile_quad_a": float(coeff[0]),
                    "smile_linear_b": float(coeff[1]),
                    "smile_level_c": float(coeff[2]),
                    "valid_strikes": int(len(valid_iv)),
                }
            )

        bs_sigma, bs_rmse = fit_bs_constant_vol(panel)
        heston_fit = fit_heston_panel(panel)
        fit_rows.append(
            {
                "day": day,
                "time_bucket": time_bucket,
                "tte_days": float(panel["tte_days"].iloc[0]),
                "panel_spot": float(panel["panel_spot"].iloc[0]),
                "strike_count": int(len(panel)),
                "bs_constant_sigma": bs_sigma,
                "bs_rmse": bs_rmse,
                "heston_success": heston_fit["success"],
                "heston_v0": heston_fit["v0"],
                "heston_kappa": heston_fit["kappa"],
                "heston_theta": heston_fit["theta"],
                "heston_volvol": heston_fit["volvol"],
                "heston_rho": heston_fit["rho"],
                "heston_rmse": heston_fit["rmse"],
                "rmse_improvement_heston_vs_bs": bs_rmse - heston_fit["rmse"]
                if pd.notna(bs_rmse) and pd.notna(heston_fit["rmse"])
                else np.nan,
            }
        )

        for _, row in panel.iterrows():
            bs_price = bs_call_price(row["panel_spot"], row["strike"], row["tau_years"], bs_sigma, 0.0) if pd.notna(bs_sigma) else np.nan
            heston_price = (
                heston_cos_call_price(
                    row["panel_spot"],
                    row["strike"],
                    row["tau_years"],
                    0.0,
                    heston_fit["kappa"],
                    heston_fit["theta"],
                    heston_fit["volvol"],
                    heston_fit["rho"],
                    heston_fit["v0"],
                )
                if heston_fit["success"]
                else np.nan
            )
            residual_rows.append(
                {
                    "day": day,
                    "time_bucket": time_bucket,
                    "product": row["product"],
                    "strike": row["strike"],
                    "panel_mid": row["panel_mid"],
                    "panel_spot": row["panel_spot"],
                    "tau_years": row["tau_years"],
                    "bs_price": bs_price,
                    "heston_price": heston_price,
                    "bs_residual": row["panel_mid"] - bs_price if pd.notna(bs_price) else np.nan,
                    "heston_residual": row["panel_mid"] - heston_price if pd.notna(heston_price) else np.nan,
                }
            )

    smile_summary = pd.DataFrame(smile_rows)
    model_fit = pd.DataFrame(fit_rows)
    model_residuals = pd.DataFrame(residual_rows)

    availability = pd.DataFrame(
        [
            {
                "metric": "implied_volatility_surface",
                "status": "implemented",
                "scope": "algorithmic VEV family",
                "reason_or_method": "BS implied vol per day/time_bucket/strike panel using call-like voucher assumption",
            },
            {
                "metric": "heston_vs_black_scholes",
                "status": "implemented",
                "scope": "algorithmic VEV family",
                "reason_or_method": "constant-vol BS fit compared to Heston COS calibration on aggregated panels",
            },
            {
                "metric": "cos_pricing_under_heston",
                "status": "implemented",
                "scope": "algorithmic VEV family",
                "reason_or_method": "Fourier-cosine pricing engine used for panel calibration and residual comparison",
            },
            {
                "metric": "greeks",
                "status": "implemented",
                "scope": "algorithmic VEV family",
                "reason_or_method": "BS Greeks computed from panel implied vols",
            },
            {
                "metric": "put_call_parity",
                "status": "not available",
                "scope": "algorithmic challenge",
                "reason_or_method": "no paired put series exists in the uploaded algorithmic data",
            },
            {
                "metric": "volume_open_interest_relation",
                "status": "partially available",
                "scope": "algorithmic challenge",
                "reason_or_method": "trade volume exists, official open interest does not; no honest OI metric can be derived from current files",
            },
        ]
    )

    volume_by_strike = (
        option_panel.groupby(["day", "product", "strike"])
        .agg(
            total_trade_count=("trade_count", "sum"),
            total_trade_notional=("trade_notional", "sum"),
            median_panel_mid=("panel_mid", "median"),
            median_bs_iv=("bs_iv", "median"),
        )
        .reset_index()
    )

    return {
        "option_panel": save_csv(option_panel, "derived_round_4_option_panel_metrics.csv"),
        "iv_surface_summary": save_csv(
            iv_surface_summary, "derived_round_4_option_iv_surface_summary.csv"
        ),
        "smile_summary": save_csv(
            smile_summary, "derived_round_4_option_smile_summary.csv"
        ),
        "model_fit": save_csv(
            model_fit, "derived_round_4_option_bs_vs_heston_fit.csv"
        ),
        "model_residuals": save_csv(
            model_residuals, "derived_round_4_option_model_residuals.csv"
        ),
        "volume_by_strike": save_csv(
            volume_by_strike, "derived_round_4_option_volume_by_strike.csv"
        ),
        "availability": save_csv(
            availability, "derived_round_4_option_metric_availability.csv"
        ),
    }


def advanced_counterparty_metrics(
    trades: pd.DataFrame,
    counterparty_stability_scores_path: Path,
    counterparty_markout_path: Path,
) -> dict[str, Path]:
    stability_scores = pd.read_csv(counterparty_stability_scores_path)
    markout = pd.read_csv(counterparty_markout_path)

    directional_rows = []
    all_names = sorted(set(trades["buyer"]).union(trades["seller"]))
    for name in all_names:
        for symbol in sorted(trades["symbol"].unique()):
            buy = trades.loc[(trades["buyer"] == name) & (trades["symbol"] == symbol)]
            sell = trades.loc[(trades["seller"] == name) & (trades["symbol"] == symbol)]
            trade_count = len(buy) + len(sell)
            if trade_count == 0:
                continue
            net_qty = float(buy["quantity"].sum() - sell["quantity"].sum())
            net_notional = float(buy["notional"].sum() - sell["notional"].sum())
            buy_share = float(len(buy) / trade_count)
            if buy_share >= 0.7:
                leaning = "directional buyer"
            elif buy_share <= 0.3:
                leaning = "directional seller"
            else:
                leaning = "balanced"
            directional_rows.append(
                {
                    "counterparty": name,
                    "symbol": symbol,
                    "product_role": PRODUCT_ROLE_MAP.get(symbol, "other"),
                    "trade_count": trade_count,
                    "buy_trade_count": int(len(buy)),
                    "sell_trade_count": int(len(sell)),
                    "buy_share": buy_share,
                    "net_qty": net_qty,
                    "net_notional": net_notional,
                    "directional_leaning": leaning,
                }
            )
    directional_profile = pd.DataFrame(directional_rows).sort_values(
        ["trade_count", "counterparty", "symbol"], ascending=[False, True, True]
    )

    family_exposure = (
        directional_profile.groupby(["counterparty", "product_role"])
        .agg(
            trade_count=("trade_count", "sum"),
            buy_trade_count=("buy_trade_count", "sum"),
            sell_trade_count=("sell_trade_count", "sum"),
            net_qty=("net_qty", "sum"),
            net_notional=("net_notional", "sum"),
        )
        .reset_index()
    )

    side_alpha = (
        markout[["counterparty", "side", "avg_side_alpha_bps_5", "trade_count"]]
        .rename(columns={"trade_count": "markout_trade_count"})
    )
    stress_proxy = stability_scores.merge(
        side_alpha.groupby("counterparty")
        .agg(
            avg_abs_side_alpha_bps_5=("avg_side_alpha_bps_5", lambda s: float(s.abs().mean())),
            max_side_alpha_bps_5=("avg_side_alpha_bps_5", "max"),
            min_side_alpha_bps_5=("avg_side_alpha_bps_5", "min"),
        )
        .reset_index(),
        on="counterparty",
        how="left",
    )
    stress_proxy["one_sidedness_score"] = (stress_proxy["buy_trade_share_mean"] - 0.5).abs() * 2.0
    stress_proxy["proxy_concentration_stress"] = (
        stress_proxy["product_concentration_hhi"].fillna(0.0) * 0.4
        + stress_proxy["one_sidedness_score"].fillna(0.0) * 0.3
        + (stress_proxy["avg_abs_side_alpha_bps_5"].fillna(0.0).clip(upper=50.0) / 50.0) * 0.3
    )

    credit_availability = pd.DataFrame(
        [
            {
                "metric": "historical_default_probability",
                "status": "not available",
                "reason": "no defaults, balance-sheet data, or survival outcomes exist in current files",
            },
            {
                "metric": "implied_default_probability",
                "status": "not available",
                "reason": "no credit spreads, CDS, or financing curves exist in current files",
            },
            {
                "metric": "true_cva",
                "status": "not available",
                "reason": "no OTC exposure profile, recovery assumption, or credit term structure exists in current files",
            },
            {
                "metric": "credit_style_proxy",
                "status": "implemented_as_proxy_only",
                "reason": "stress proxy is based on market-structure concentration and adverse flow, not on real credit risk",
            },
        ]
    )

    return {
        "directional_profile": save_csv(
            directional_profile, "derived_round_4_counterparty_directional_profile.csv"
        ),
        "family_exposure": save_csv(
            family_exposure, "derived_round_4_counterparty_family_exposure_proxy.csv"
        ),
        "stress_proxy": save_csv(
            stress_proxy, "derived_round_4_counterparty_credit_proxy.csv"
        ),
        "credit_availability": save_csv(
            credit_availability, "derived_round_4_counterparty_credit_metric_availability.csv"
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


def feature_and_regime_metrics(
    prices: pd.DataFrame,
    trade_aligned: pd.DataFrame,
    counterparty_concentration_path: Path,
    counterparty_stability_scores_path: Path,
) -> dict[str, Path]:
    concentration = pd.read_csv(counterparty_concentration_path)
    stability_scores = pd.read_csv(counterparty_stability_scores_path)

    dominant_map = concentration.set_index(["symbol", "side"])["dominant_counterparty"].to_dict()
    top1_share_map = concentration.set_index(["symbol", "side"])["top1_share"].to_dict()
    stability_class_map = stability_scores.set_index("counterparty")["stability_class"].to_dict()
    product_share_map = stability_scores.set_index("counterparty")["dominant_product_share"].to_dict()

    feature_ready = trade_aligned.copy()
    feature_ready["buyer_stability_class"] = feature_ready["buyer"].map(stability_class_map).fillna("small sample")
    feature_ready["seller_stability_class"] = feature_ready["seller"].map(stability_class_map).fillna("small sample")
    feature_ready["buyer_dominant_product_share"] = feature_ready["buyer"].map(product_share_map)
    feature_ready["seller_dominant_product_share"] = feature_ready["seller"].map(product_share_map)
    feature_ready["buyer_is_symbol_dominant"] = (
        feature_ready.apply(
            lambda row: int(dominant_map.get((row["symbol"], "buyer")) == row["buyer"]),
            axis=1,
        )
    )
    feature_ready["seller_is_symbol_dominant"] = (
        feature_ready.apply(
            lambda row: int(dominant_map.get((row["symbol"], "seller")) == row["seller"]),
            axis=1,
        )
    )
    feature_ready["symbol_buyer_top1_share"] = feature_ready["symbol"].map(
        lambda symbol: top1_share_map.get((symbol, "buyer"))
    )
    feature_ready["symbol_seller_top1_share"] = feature_ready["symbol"].map(
        lambda symbol: top1_share_map.get((symbol, "seller"))
    )
    pair_counts = feature_ready.groupby(["buyer", "seller"]).size().rename("pair_trade_count_total").reset_index()
    feature_ready = feature_ready.merge(pair_counts, on=["buyer", "seller"], how="left")
    feature_ready["pair_is_recurrent"] = (feature_ready["pair_trade_count_total"] >= 25).astype(int)

    feature_cols = [
        "rel_spread_bps",
        "imbalance_1",
        "depth_1",
        "quantity",
        "future_mid_return_bps_1",
        "future_mid_return_bps_5",
        "future_mid_return_bps_10",
        "buyer_is_symbol_dominant",
        "seller_is_symbol_dominant",
        "buyer_dominant_product_share",
        "seller_dominant_product_share",
        "symbol_buyer_top1_share",
        "symbol_seller_top1_share",
        "pair_trade_count_total",
        "pair_is_recurrent",
    ]
    feature_frame = feature_ready[feature_cols].replace([np.inf, -np.inf], np.nan).dropna()
    corr_path = save_csv(
        feature_frame.corr().reset_index(),
        "derived_round_4_trade_feature_corr.csv",
    )
    cov_path = save_csv(
        feature_frame.cov().reset_index(),
        "derived_round_4_trade_feature_covariance.csv",
    )

    model_df = feature_ready[
        [
            "symbol",
            "time_bucket",
            "buyer",
            "seller",
            "buyer_stability_class",
            "seller_stability_class",
            "trade_location_bucket",
            "rel_spread_bps",
            "imbalance_1",
            "depth_1",
            "quantity",
            "buyer_is_symbol_dominant",
            "seller_is_symbol_dominant",
            "pair_trade_count_total",
            "pair_is_recurrent",
            "symbol_buyer_top1_share",
            "symbol_seller_top1_share",
            "future_mid_return_bps_5",
        ]
    ].replace([np.inf, -np.inf], np.nan)
    model_df = model_df.dropna()

    top_buyers = model_df["buyer"].value_counts().head(5).index.tolist()
    top_sellers = model_df["seller"].value_counts().head(5).index.tolist()
    model_df["buyer_bucket"] = np.where(model_df["buyer"].isin(top_buyers), model_df["buyer"], "OTHER_BUYER")
    model_df["seller_bucket"] = np.where(model_df["seller"].isin(top_sellers), model_df["seller"], "OTHER_SELLER")

    y = model_df["future_mid_return_bps_5"]
    baseline_X = pd.get_dummies(
        model_df[
            [
                "symbol",
                "time_bucket",
                "rel_spread_bps",
                "imbalance_1",
                "depth_1",
                "quantity",
            ]
        ],
        columns=["symbol", "time_bucket"],
        drop_first=False,
    )
    counterparty_X = pd.get_dummies(
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
    engineered_X = pd.get_dummies(
        model_df[
            [
                "symbol",
                "time_bucket",
                "buyer_stability_class",
                "seller_stability_class",
                "trade_location_bucket",
                "rel_spread_bps",
                "imbalance_1",
                "depth_1",
                "quantity",
                "buyer_is_symbol_dominant",
                "seller_is_symbol_dominant",
                "pair_trade_count_total",
                "pair_is_recurrent",
                "symbol_buyer_top1_share",
                "symbol_seller_top1_share",
            ]
        ],
        columns=[
            "symbol",
            "time_bucket",
            "buyer_stability_class",
            "seller_stability_class",
            "trade_location_bucket",
        ],
        drop_first=False,
    )
    baseline_model = LinearRegression().fit(baseline_X, y)
    counterparty_model = LinearRegression().fit(counterparty_X, y)
    engineered_model = LinearRegression().fit(engineered_X, y)
    baseline_r2 = baseline_model.score(baseline_X, y)
    counterparty_r2 = counterparty_model.score(counterparty_X, y)
    engineered_r2 = engineered_model.score(engineered_X, y)

    coeffs = pd.DataFrame({"feature": engineered_X.columns, "coefficient": engineered_model.coef_})
    coeffs["abs_coefficient"] = coeffs["coefficient"].abs()
    coeffs = coeffs.sort_values("abs_coefficient", ascending=False)
    coeffs["r2"] = engineered_r2
    regression_path = save_csv(
        coeffs, "derived_round_4_counterparty_controlled_regression.csv"
    )
    model_comparison = pd.DataFrame(
        [
            {
                "model_name": "baseline_microstructure",
                "target": "future_mid_return_bps_5",
                "r2": baseline_r2,
                "incremental_vs_baseline": 0.0,
                "notes": "symbol + time bucket + spread + imbalance + depth + quantity",
            },
            {
                "model_name": "counterparty_bucket_context",
                "target": "future_mid_return_bps_5",
                "r2": counterparty_r2,
                "incremental_vs_baseline": counterparty_r2 - baseline_r2,
                "notes": "adds top buyer/seller identity buckets",
            },
            {
                "model_name": "engineered_context_features",
                "target": "future_mid_return_bps_5",
                "r2": engineered_r2,
                "incremental_vs_baseline": engineered_r2 - baseline_r2,
                "notes": "adds stability class, symbol dominance, pair recurrence, and trade location",
            },
        ]
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
        feature_ready.assign(
            buyer_bucket=np.where(
                feature_ready["buyer"].isin(top_buyers), feature_ready["buyer"], "OTHER_BUYER"
            ),
            seller_bucket=np.where(
                feature_ready["seller"].isin(top_sellers), feature_ready["seller"], "OTHER_SELLER"
            ),
        )
        .groupby(["symbol", "buyer_bucket", "seller_bucket"])
        .agg(
            trade_count=("symbol", "size"),
            avg_rel_spread_bps=("rel_spread_bps", "mean"),
            avg_imbalance_1=("imbalance_1", "mean"),
            avg_future_mid_return_bps_1=("future_mid_return_bps_1", "mean"),
            avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
            avg_future_mid_return_bps_10=("future_mid_return_bps_10", "mean"),
        )
        .reset_index()
    )

    engineered_feature_summary = []
    for feature_name, column_name, role, online_usable in [
        ("buyer_stability_class", "buyer_stability_class", "counterparty role", "yes"),
        ("seller_stability_class", "seller_stability_class", "counterparty role", "yes"),
        ("buyer_is_symbol_dominant", "buyer_is_symbol_dominant", "counterparty-symbol dominance", "yes"),
        ("seller_is_symbol_dominant", "seller_is_symbol_dominant", "counterparty-symbol dominance", "yes"),
        ("pair_is_recurrent", "pair_is_recurrent", "pair recurrence", "yes with historical memory"),
        ("trade_location_bucket", "trade_location_bucket", "trade-to-book context", "yes"),
    ]:
        grouped = (
            feature_ready.groupby(column_name)
            .agg(
                sample_size=("symbol", "size"),
                avg_future_mid_return_bps_1=("future_mid_return_bps_1", "mean"),
                avg_future_mid_return_bps_5=("future_mid_return_bps_5", "mean"),
                avg_future_mid_return_bps_10=("future_mid_return_bps_10", "mean"),
                avg_rel_spread_bps=("rel_spread_bps", "mean"),
                avg_depth_1=("depth_1", "mean"),
            )
            .reset_index()
            .rename(columns={column_name: "feature_level"})
        )
        grouped["feature_name"] = feature_name
        grouped["feature_role"] = role
        grouped["online_usable"] = online_usable
        engineered_feature_summary.append(grouped)
    engineered_feature_summary_df = pd.concat(engineered_feature_summary, ignore_index=True)

    online_feature_table = pd.DataFrame(
        [
            {
                "feature_name": "buyer_stability_class",
                "origin": "counterparty stability scores",
                "online_usability": "yes",
                "role": "context / regime",
                "signal_strength": "medium",
                "stability": "medium-high",
                "actionability": "filter candidate",
                "lifecycle_decision": "promote to understanding",
                "notes": "captures specialist vs broad vs rotating buyer ecology",
            },
            {
                "feature_name": "seller_stability_class",
                "origin": "counterparty stability scores",
                "online_usability": "yes",
                "role": "context / regime",
                "signal_strength": "medium",
                "stability": "medium-high",
                "actionability": "filter candidate",
                "lifecycle_decision": "promote to understanding",
                "notes": "especially relevant in concentrated voucher strikes",
            },
            {
                "feature_name": "buyer_is_symbol_dominant",
                "origin": "symbol-side concentration map",
                "online_usability": "yes",
                "role": "dominance flag",
                "signal_strength": "medium",
                "stability": "high in upper/floor",
                "actionability": "feature-engineering candidate",
                "lifecycle_decision": "promote cautiously",
                "notes": "useful when one buyer structurally dominates a strike",
            },
            {
                "feature_name": "seller_is_symbol_dominant",
                "origin": "symbol-side concentration map",
                "online_usability": "yes",
                "role": "dominance flag",
                "signal_strength": "medium",
                "stability": "high in upper/floor",
                "actionability": "feature-engineering candidate",
                "lifecycle_decision": "promote cautiously",
                "notes": "especially relevant for `Mark 22`-dominated seller flows",
            },
            {
                "feature_name": "pair_is_recurrent",
                "origin": "buyer-seller pair recurrence",
                "online_usability": "yes with historical memory",
                "role": "interaction context",
                "signal_strength": "weak-to-medium",
                "stability": "unclear",
                "actionability": "exploratory",
                "lifecycle_decision": "keep exploratory",
                "notes": "interesting for pair ecology, but sample is still only three days",
            },
            {
                "feature_name": "trade_location_bucket",
                "origin": "trade-to-book alignment",
                "online_usability": "yes",
                "role": "microstructure context",
                "signal_strength": "medium",
                "stability": "high",
                "actionability": "feature-engineering candidate",
                "lifecycle_decision": "promote",
                "notes": "connects counterparty events to whether prints hit bid/ask or occur inside spread",
            },
        ]
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
        "feature_model_comparison": save_csv(
            model_comparison, "derived_round_4_feature_model_comparison.csv"
        ),
        "product_regime": save_csv(
            product_regime, "derived_round_4_product_regime_summary.csv"
        ),
        "counterparty_conditioned": save_csv(
            counterparty_conditioned,
            "derived_round_4_counterparty_conditioned_summary.csv",
        ),
        "engineered_feature_summary": save_csv(
            engineered_feature_summary_df,
            "derived_round_4_engineered_feature_summary.csv",
        ),
        "candidate_online_features": save_csv(
            online_feature_table,
            "derived_round_4_candidate_online_features.csv",
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
    counterparty_markout_path: Path,
    option_iv_surface_path: Path,
    option_model_fit_path: Path,
    option_model_residuals_path: Path,
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

    markout = pd.read_csv(counterparty_markout_path)
    markout = markout.loc[markout["trade_count"] >= 40].copy()
    markout["label"] = markout["counterparty"] + " (" + markout["side"] + ")"
    markout = markout.sort_values("avg_side_alpha_bps_5", ascending=False).head(12)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=markout, x="avg_side_alpha_bps_5", y="label", hue="side", dodge=False, ax=ax)
    ax.set_title("Top counterparty-side 5-step markouts")
    ax.set_xlabel("Average 5-step side-aligned alpha (bps)")
    ax.set_ylabel("")
    plot_paths["counterparty_markout_bar"] = save_plot(
        fig, "round_4_counterparty_markout_bar.png"
    )

    iv_surface = pd.read_csv(option_iv_surface_path)
    iv_surface = iv_surface.loc[iv_surface["median_bs_iv"].notna()].copy()
    if not iv_surface.empty:
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(
            data=iv_surface,
            x="strike",
            y="median_bs_iv",
            hue="day",
            style="day",
            markers=True,
            dashes=False,
            ax=ax,
        )
        ax.set_title("Round 4 implied volatility smile by day")
        ax.set_ylabel("Median BS implied vol")
        plot_paths["iv_smile_by_day"] = save_plot(fig, "round_4_iv_smile_by_day.png")

    fit = pd.read_csv(option_model_fit_path)
    residuals = pd.read_csv(option_model_residuals_path)
    if not fit.empty and not residuals.empty:
        best_panel = fit.sort_values("rmse_improvement_heston_vs_bs", ascending=False).head(1)
        if not best_panel.empty:
            day = int(best_panel["day"].iloc[0])
            time_bucket = best_panel["time_bucket"].iloc[0]
            panel_resid = residuals.loc[
                (residuals["day"] == day) & (residuals["time_bucket"] == time_bucket)
            ].copy()
            panel_resid = panel_resid.sort_values("strike")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(panel_resid["strike"], panel_resid["panel_mid"], marker="o", label="market")
            ax.plot(panel_resid["strike"], panel_resid["bs_price"], marker="o", label="BS constant vol")
            ax.plot(panel_resid["strike"], panel_resid["heston_price"], marker="o", label="Heston COS")
            ax.set_title(f"Round 4 model fit comparison: day {day}, {time_bucket}")
            ax.set_ylabel("Option mid price")
            ax.legend()
            plot_paths["option_model_fit_comparison"] = save_plot(
                fig, "round_4_option_model_fit_comparison.png"
            )

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
    counterparty_markout_path: Path,
    counterparty_stability_scores_path: Path,
    feature_model_comparison_path: Path,
    option_model_fit_path: Path,
    option_metric_availability_path: Path,
    counterparty_credit_availability_path: Path,
) -> dict:
    concentration = pd.read_csv(counterparty_concentration_path)
    option_book = pd.read_csv(option_book_summary_path)
    regression = pd.read_csv(regression_path)
    markout = pd.read_csv(counterparty_markout_path)
    stability_scores = pd.read_csv(counterparty_stability_scores_path)
    model_comparison = pd.read_csv(feature_model_comparison_path)
    option_model_fit = pd.read_csv(option_model_fit_path)
    option_metric_availability = pd.read_csv(option_metric_availability_path)
    counterparty_credit_availability = pd.read_csv(counterparty_credit_availability_path)

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
        "feature_model_comparison": model_comparison.to_dict(orient="records"),
        "option_model_fit_summary": option_model_fit[
            [
                "day",
                "time_bucket",
                "bs_rmse",
                "heston_rmse",
                "rmse_improvement_heston_vs_bs",
                "heston_success",
            ]
        ].to_dict(orient="records"),
        "option_metric_availability": option_metric_availability.to_dict(orient="records"),
        "counterparty_credit_metric_availability": counterparty_credit_availability.to_dict(
            orient="records"
        ),
        "top_counterparty_side_markouts_5": markout.sort_values(
            "avg_side_alpha_bps_5", ascending=False
        )
        .head(10)[["counterparty", "side", "trade_count", "avg_side_alpha_bps_5"]]
        .to_dict(orient="records"),
        "stability_class_counts": stability_scores["stability_class"].value_counts().to_dict(),
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
    advanced_option_paths = advanced_option_metrics(prices, trades)
    output_paths.update(advanced_option_paths)
    advanced_counterparty_paths = advanced_counterparty_metrics(
        trades,
        counterparty_paths["counterparty_stability_scores"],
        trade_alignment_paths["counterparty_markout"],
    )
    output_paths.update(advanced_counterparty_paths)
    cross_paths = cross_product_metrics(prices)
    output_paths.update(cross_paths)
    feature_paths = feature_and_regime_metrics(
        prices,
        trade_aligned,
        counterparty_paths["counterparty_concentration"],
        counterparty_paths["counterparty_stability_scores"],
    )
    output_paths.update(feature_paths)
    plot_paths = build_plots(
        prices,
        trades,
        counterparty_paths["counterparty_product_mix"],
        cross_paths["corr_matrix"],
        trade_alignment_paths["counterparty_markout"],
        advanced_option_paths["iv_surface_summary"],
        advanced_option_paths["model_fit"],
        advanced_option_paths["model_residuals"],
    )
    output_paths.update(plot_paths)

    summary = build_summary_metrics(
        prices,
        trades,
        counterparty_paths["counterparty_concentration"],
        option_paths["option_book_summary"],
        feature_paths["counterparty_regression"],
        trade_alignment_paths["counterparty_markout"],
        counterparty_paths["counterparty_stability_scores"],
        feature_paths["feature_model_comparison"],
        advanced_option_paths["model_fit"],
        advanced_option_paths["availability"],
        advanced_counterparty_paths["credit_availability"],
    )
    write_manifest(output_paths, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
