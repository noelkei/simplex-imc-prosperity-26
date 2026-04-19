"""
Deep EDA for Round 2 (ACO + IPR) using full ML/stats stack.

Sections:
  1. Data loading & validation
  2. Descriptive statistics per product per day
  3. Mid-price time series & returns analysis
  4. Stationarity (ADF, KPSS) & trend detection
  5. Microstructure (spread, depth, imbalance)
  6. Kalman filter MLE calibration
  7. HMM regime detection (hmmlearn)
  8. Volatility clustering (Ljung-Box, ARCH LM)
  9. Signal information coefficient (imbalance, micro-trend)
 10. Cross-day stability + cross-product correlation
 11. MAF (Market Access Fee) value estimation

Outputs:
  outputs/eda_summary.json
  outputs/eda_report.md
  plots/*.png
"""
from __future__ import annotations

import json
import math
import warnings
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy import stats
from scipy.optimize import minimize
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from hmmlearn.hmm import GaussianHMM

warnings.filterwarnings("ignore")

ROOT = Path("/home/user/simplex-imc-prosperity-26/rounds/round_2")
DATA_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "workspace" / "01_eda" / "outputs"
PLOT_DIR = ROOT / "workspace" / "01_eda" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PLOT_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = ["ASH_COATED_OSMIUM", "INTARIAN_PEPPER_ROOT"]
DAYS = [-1, 0, 1]


# ---------------------------------------------------------------------------
# 1. Loading
# ---------------------------------------------------------------------------
def load_prices() -> pd.DataFrame:
    frames = []
    for d in DAYS:
        df = pd.read_csv(DATA_DIR / f"prices_round_2_day_{d}.csv", sep=";")
        df["day_file"] = d
        frames.append(df)
    px = pd.concat(frames, ignore_index=True)
    # absolute time across days for convenient plotting
    px["t_abs"] = px["day_file"] * 1_000_000 + px["timestamp"]
    # Mark dirty rows (mid=0 means both sides empty in this dataset)
    px["mid_clean"] = px["mid_price"].where(px["mid_price"] > 0)
    return px


def clean_mid_series(sub: pd.DataFrame) -> np.ndarray:
    """Return mid price array filtered to remove zero/empty rows."""
    return sub["mid_price"].where(sub["mid_price"] > 0).dropna().values


def load_trades() -> pd.DataFrame:
    frames = []
    for d in DAYS:
        df = pd.read_csv(DATA_DIR / f"trades_round_2_day_{d}.csv", sep=";")
        df["day_file"] = d
        frames.append(df)
    tr = pd.concat(frames, ignore_index=True)
    tr["t_abs"] = tr["day_file"] * 1_000_000 + tr["timestamp"]
    return tr


# ---------------------------------------------------------------------------
# 2. Descriptive stats
# ---------------------------------------------------------------------------
def describe_book(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        out[prod] = {}
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].copy()
            if sub.empty:
                continue
            mid = sub["mid_clean"].dropna()
            spread = (sub["ask_price_1"] - sub["bid_price_1"]).dropna()
            depth_bid = sub[["bid_volume_1", "bid_volume_2", "bid_volume_3"]].sum(axis=1)
            depth_ask = sub[["ask_volume_1", "ask_volume_2", "ask_volume_3"]].sum(axis=1)
            out[prod][f"day_{d}"] = {
                "n_ticks": int(len(sub)),
                "n_clean_ticks": int(len(mid)),
                "n_dirty_ticks": int(len(sub) - len(mid)),
                "mid_mean": float(mid.mean()),
                "mid_std": float(mid.std()),
                "mid_min": float(mid.min()),
                "mid_max": float(mid.max()),
                "mid_skew": float(stats.skew(mid)),
                "mid_kurt": float(stats.kurtosis(mid)),
                "spread_mean": float(spread.mean()),
                "spread_median": float(spread.median()),
                "spread_std": float(spread.std()),
                "spread_pct_one_sided": float((sub["ask_price_1"].isna() | sub["bid_price_1"].isna()).mean()),
                "n_bid_levels_avg": float(sub[["bid_price_1", "bid_price_2", "bid_price_3"]].notna().sum(axis=1).mean()),
                "n_ask_levels_avg": float(sub[["ask_price_1", "ask_price_2", "ask_price_3"]].notna().sum(axis=1).mean()),
                "depth_bid_mean": float(depth_bid.mean()),
                "depth_ask_mean": float(depth_ask.mean()),
            }
    return out


# ---------------------------------------------------------------------------
# 3-4. Returns, stationarity, trend
# ---------------------------------------------------------------------------
def returns_and_stationarity(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        out[prod] = {}
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].sort_values("timestamp")
            mid = clean_mid_series(sub)
            if len(mid) < 100:
                continue
            ret = np.diff(mid)
            log_ret = np.diff(np.log(mid))

            # ADF / KPSS
            try:
                adf_stat, adf_p = adfuller(mid, autolag="AIC", regression="ct")[:2]
            except Exception:
                adf_stat, adf_p = float("nan"), float("nan")
            try:
                kpss_stat, kpss_p = kpss(mid, regression="ct", nlags="auto")[:2]
            except Exception:
                kpss_stat, kpss_p = float("nan"), float("nan")

            # Trend OLS - need timestamps aligned to clean mid
            sub_clean = sub[sub["mid_price"] > 0]
            X = add_constant(sub_clean["timestamp"].values)
            slope, intercept = OLS(mid, X).fit().params[::-1]
            mid_drift_per_tick = float(slope)
            # Span of the day in ticks
            day_span = float(sub_clean["timestamp"].max() - sub_clean["timestamp"].min())
            mid_drift_per_day = mid_drift_per_tick * day_span

            # ACF of returns and squared returns
            try:
                acf_ret = acf(ret, nlags=20, fft=False)[1:6].tolist()
                acf_ret2 = acf(ret ** 2, nlags=20, fft=False)[1:6].tolist()
            except Exception:
                acf_ret, acf_ret2 = [], []

            # Ljung-Box on returns and squared returns (volatility clustering)
            try:
                lb_ret = acorr_ljungbox(ret, lags=[10], return_df=True)
                lb_p_ret = float(lb_ret["lb_pvalue"].iloc[0])
            except Exception:
                lb_p_ret = float("nan")
            try:
                lb_ret2 = acorr_ljungbox(ret ** 2, lags=[10], return_df=True)
                lb_p_ret2 = float(lb_ret2["lb_pvalue"].iloc[0])
            except Exception:
                lb_p_ret2 = float("nan")

            # ARCH LM test
            try:
                arch_stat, arch_p, _, _ = het_arch(ret, nlags=10)
            except Exception:
                arch_stat, arch_p = float("nan"), float("nan")

            out[prod][f"day_{d}"] = {
                "n_returns": int(len(ret)),
                "ret_mean": float(ret.mean()),
                "ret_std": float(ret.std()),
                "ret_var": float(ret.var()),
                "ret_skew": float(stats.skew(ret)),
                "ret_kurt": float(stats.kurtosis(ret)),
                "log_ret_mean": float(log_ret.mean()),
                "log_ret_std": float(log_ret.std()),
                "adf_stat": float(adf_stat),
                "adf_p": float(adf_p),  # H0: unit root
                "kpss_stat": float(kpss_stat),
                "kpss_p": float(kpss_p),  # H0: trend-stationary
                "ols_drift_per_tick": mid_drift_per_tick,
                "ols_drift_per_day": mid_drift_per_day,
                "acf_ret_lag1to5": acf_ret,
                "acf_ret2_lag1to5": acf_ret2,
                "ljungbox_p_ret": lb_p_ret,
                "ljungbox_p_ret2": lb_p_ret2,
                "arch_lm_stat": float(arch_stat),
                "arch_lm_p": float(arch_p),
            }
    return out


# ---------------------------------------------------------------------------
# 5. Microstructure: imbalance and tick-by-tick mid changes
# ---------------------------------------------------------------------------
def microstructure(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        out[prod] = {}
        sub = px[(px["product"] == prod) & (px["mid_price"] > 0)].sort_values(["day_file", "timestamp"]).copy()
        bv1 = sub["bid_volume_1"].fillna(0).values
        av1 = sub["ask_volume_1"].fillna(0).values
        imb1 = np.where((bv1 + av1) > 0, (bv1 - av1) / (bv1 + av1), 0.0)
        sub["imb1"] = imb1
        # Mid changes
        sub["mid_diff"] = sub["mid_price"].diff()
        # IC: corr(imb1[t], mid_diff[t+1])
        valid = sub[["imb1", "mid_diff"]].dropna()
        valid["mid_diff_next"] = valid["mid_diff"].shift(-1)
        valid = valid.dropna()
        ic_imb1 = float(valid[["imb1", "mid_diff_next"]].corr().iloc[0, 1])

        # Mid changes histogram: how often abs change > 0
        nz_frac = float((sub["mid_diff"].abs() > 0).mean())
        big_move_frac = float((sub["mid_diff"].abs() > 1).mean())

        out[prod] = {
            "n_obs": int(len(sub)),
            "imb1_mean": float(np.mean(imb1)),
            "imb1_std": float(np.std(imb1)),
            "ic_imb1_to_next_mid_diff": ic_imb1,
            "frac_mid_changed": nz_frac,
            "frac_mid_change_gt1": big_move_frac,
        }
    return out


# ---------------------------------------------------------------------------
# 6. Kalman MLE calibration
# ---------------------------------------------------------------------------
def kalman_mle(mid: np.ndarray, fv0: float | None = None) -> Tuple[float, float, float]:
    """Maximize log-likelihood for Q (process), R (measurement) on local-level model."""
    if fv0 is None:
        fv0 = float(mid[0])

    def neg_ll(params):
        log_q, log_r = params
        q, r = math.exp(log_q), math.exp(log_r)
        x = fv0
        P = 25.0
        ll = 0.0
        for z in mid:
            # predict
            P_pred = P + q
            # innovation
            v = z - x
            S = P_pred + r
            ll += -0.5 * (math.log(2 * math.pi * S) + v * v / S)
            # update
            K = P_pred / S
            x = x + K * v
            P = (1 - K) * P_pred
        return -ll

    # initial guess
    res = minimize(
        neg_ll, x0=np.array([math.log(0.01), math.log(4.0)]),
        method="Nelder-Mead", options={"xatol": 1e-3, "fatol": 1e-3, "maxiter": 500}
    )
    q_hat = math.exp(res.x[0])
    r_hat = math.exp(res.x[1])
    return q_hat, r_hat, float(-res.fun)


def kalman_section(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        out[prod] = {}
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].sort_values("timestamp")
            mid = clean_mid_series(sub)
            if len(mid) < 200:
                continue
            q_hat, r_hat, ll = kalman_mle(mid)
            out[prod][f"day_{d}"] = {
                "q_mle": q_hat,
                "r_mle": r_hat,
                "log_lik": ll,
                "implied_K_steady": float((q_hat + math.sqrt(q_hat * (q_hat + 4 * r_hat))) /
                                         (2 * (q_hat + math.sqrt(q_hat * (q_hat + 4 * r_hat))) + 2 * r_hat)),
            }
        # Pooled estimate across all days (clean mid only, per day to avoid trend across days)
        sub = px[px["product"] == prod].sort_values(["day_file", "timestamp"])
        mid_all = clean_mid_series(sub)
        q_p, r_p, ll_p = kalman_mle(mid_all)
        out[prod]["pooled"] = {"q_mle": q_p, "r_mle": r_p, "log_lik": ll_p}
    return out


# ---------------------------------------------------------------------------
# 7. HMM regime detection
# ---------------------------------------------------------------------------
def hmm_section(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        # Concat per-day clean returns (avoid spurious jumps across day boundaries)
        rets = []
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].sort_values("timestamp")
            m = clean_mid_series(sub)
            if len(m) > 1:
                rets.append(np.diff(m))
        if not rets:
            continue
        ret_all = np.concatenate(rets)
        if len(ret_all) < 500:
            continue
        ret = ret_all.reshape(-1, 1)

        prod_out = {}
        for k in (2, 3, 4):
            try:
                model = GaussianHMM(n_components=k, covariance_type="full",
                                    n_iter=200, random_state=42)
                model.fit(ret)
                states = model.predict(ret)
                ll = model.score(ret)
                # Persistence: mean diagonal of transition matrix
                persistence = float(np.mean(np.diag(model.transmat_)))
                # State variances (volatility regimes)
                state_vars = sorted(float(model.covars_[i].flatten()[0]) for i in range(k))

                # Predictive power: corr(state_t, ret_{t+1})
                # Use state mean as feature
                state_means = model.means_.flatten()
                feat = state_means[states]
                if len(feat) > 1:
                    fc = feat[:-1]
                    rn = ret.flatten()[1:]
                    if fc.std() > 0:
                        ic_state = float(np.corrcoef(fc, rn)[0, 1])
                    else:
                        ic_state = 0.0
                else:
                    ic_state = 0.0

                # BIC
                n = len(ret)
                # params: k means + k vars + k*(k-1) transitions + (k-1) start
                n_params = k + k + k * (k - 1) + (k - 1)
                bic = -2 * ll + n_params * math.log(n)

                prod_out[f"k_{k}"] = {
                    "log_lik": float(ll),
                    "bic": float(bic),
                    "persistence_diag_mean": persistence,
                    "state_variances_sorted": state_vars,
                    "ic_state_to_next_ret": ic_state,
                }
            except Exception as e:
                prod_out[f"k_{k}"] = {"error": str(e)}
        out[prod] = prod_out
    return out


# ---------------------------------------------------------------------------
# 9. Signal IC at multiple lags
# ---------------------------------------------------------------------------
def signal_ic_section(px: pd.DataFrame) -> dict:
    out = {}
    for prod in PRODUCTS:
        sub = px[(px["product"] == prod) & (px["mid_price"] > 0)].sort_values(["day_file", "timestamp"]).copy()
        bv1 = sub["bid_volume_1"].fillna(0).values
        av1 = sub["ask_volume_1"].fillna(0).values
        imb1 = np.where((bv1 + av1) > 0, (bv1 - av1) / (bv1 + av1), 0.0)
        mid = sub["mid_price"].values
        ret = np.diff(mid)
        ic = {}
        for lag in (1, 2, 3, 5, 10):
            if len(ret) <= lag:
                continue
            x = imb1[:-lag]  # imb at t
            y = ret[lag - 1:]  # ret over next `lag` ticks starting at t+1
            # align lengths
            n = min(len(x), len(y))
            x, y = x[:n], y[:n]
            if x.std() > 0 and y.std() > 0:
                ic[f"lag_{lag}"] = float(np.corrcoef(x, y)[0, 1])
            else:
                ic[f"lag_{lag}"] = 0.0
        # Momentum / mean-reversion of returns
        ret_lags = {}
        for lag in (1, 2, 3, 5):
            if len(ret) > lag:
                ret_lags[f"lag_{lag}"] = float(np.corrcoef(ret[:-lag], ret[lag:])[0, 1])
        out[prod] = {"imbalance_ic": ic, "return_autocorr": ret_lags}
    return out


# ---------------------------------------------------------------------------
# 10. Cross-day stability + cross-product correlation
# ---------------------------------------------------------------------------
def cross_section(px: pd.DataFrame) -> dict:
    out: Dict = {"per_product_day_diffs": {}, "cross_product_corr": {}}
    # Stability per product
    for prod in PRODUCTS:
        means = []
        stds = []
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d) & (px["mid_price"] > 0)]
            mid = sub["mid_price"].dropna()
            means.append(float(mid.mean()))
            stds.append(float(mid.std()))
        out["per_product_day_diffs"][prod] = {
            "mid_mean_per_day": means,
            "mid_std_per_day": stds,
            "day_over_day_drift": [means[i + 1] - means[i] for i in range(len(means) - 1)],
        }
    # Cross-product return correlation per day
    for d in DAYS:
        aco = px[(px["product"] == "ASH_COATED_OSMIUM") & (px["day_file"] == d) & (px["mid_price"] > 0)].sort_values("timestamp")
        ipr = px[(px["product"] == "INTARIAN_PEPPER_ROOT") & (px["day_file"] == d) & (px["mid_price"] > 0)].sort_values("timestamp")
        merged = pd.merge(
            aco[["timestamp", "mid_price"]].rename(columns={"mid_price": "aco"}),
            ipr[["timestamp", "mid_price"]].rename(columns={"mid_price": "ipr"}),
            on="timestamp", how="inner"
        )
        if len(merged) < 50:
            continue
        merged["aco_ret"] = merged["aco"].diff()
        merged["ipr_ret"] = merged["ipr"].diff()
        m = merged.dropna()
        out["cross_product_corr"][f"day_{d}"] = {
            "n_overlap": int(len(m)),
            "level_corr": float(m[["aco", "ipr"]].corr().iloc[0, 1]),
            "return_corr": float(m[["aco_ret", "ipr_ret"]].corr().iloc[0, 1]),
        }
    return out


# ---------------------------------------------------------------------------
# 11. MAF value heuristic
# ---------------------------------------------------------------------------
def maf_estimate(desc: dict) -> dict:
    """Estimate marginal value of 100% market access vs 80% baseline.

    Heuristic: extra 20% of order book quotes => proportional ~25% extra fill rate
    on top of the 80% baseline. Round 1 baseline P&L ~10,094 was achieved at 80%.
    """
    base = 10_094  # candidate_04 baseline
    # Two products contribute roughly equally on neutral days; trend in IPR could amplify
    extra_fill_rate = 0.25
    nominal = base * extra_fill_rate
    return {
        "round1_baseline_pnl": base,
        "estimated_extra_value_at_full_access": nominal,
        "rationale": "Extra access = +25% fills on top of 80% baseline; value ~25% of baseline.",
        "recommended_bid_range": [1500, 3000],
    }


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------
def make_plots(px: pd.DataFrame, returns_st: dict, kal: dict):
    # 1. Mid price over 3 days for both products (clean)
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
    for ax, prod in zip(axes, PRODUCTS):
        sub = px[(px["product"] == prod) & (px["mid_price"] > 0)].sort_values(["day_file", "timestamp"])
        ax.plot(sub["t_abs"].values, sub["mid_price"].values, lw=0.6)
        ax.set_title(f"{prod} mid_price (3 days, cleaned)")
        ax.set_ylabel("mid_price")
        for d in DAYS[1:]:
            ax.axvline(d * 1_000_000, color="red", ls="--", alpha=0.4)
    axes[-1].set_xlabel("absolute timestamp (day*1e6 + t)")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "01_mid_price_3day.png", dpi=110)
    plt.close(fig)

    # 2. Return histogram per product (clean, capped to ±20)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, prod in zip(axes, PRODUCTS):
        rets = []
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].sort_values("timestamp")
            m = clean_mid_series(sub)
            if len(m) > 1:
                rets.append(np.diff(m))
        ret = np.concatenate(rets)
        ret_cap = ret[np.abs(ret) <= 20]
        ax.hist(ret_cap, bins=60, alpha=0.7)
        ax.set_title(f"{prod} mid-diff (clean, |Δ|≤20)")
        ax.set_xlabel("mid_diff")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "02_return_hist.png", dpi=110)
    plt.close(fig)

    # 3. ACF of returns (clean per-day concat)
    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    for i, prod in enumerate(PRODUCTS):
        rets = []
        for d in DAYS:
            sub = px[(px["product"] == prod) & (px["day_file"] == d)].sort_values("timestamp")
            m = clean_mid_series(sub)
            if len(m) > 1:
                rets.append(np.diff(m))
        ret = np.concatenate(rets)
        try:
            acf_vals = acf(ret, nlags=30, fft=False)
            acf_sq = acf(ret ** 2, nlags=30, fft=False)
            axes[i, 0].bar(range(len(acf_vals)), acf_vals)
            axes[i, 0].set_title(f"{prod} ACF(returns)")
            axes[i, 0].axhline(1.96 / math.sqrt(len(ret)), color="red", ls="--", alpha=0.5)
            axes[i, 0].axhline(-1.96 / math.sqrt(len(ret)), color="red", ls="--", alpha=0.5)
            axes[i, 1].bar(range(len(acf_sq)), acf_sq)
            axes[i, 1].set_title(f"{prod} ACF(returns²) - vol clustering")
        except Exception:
            pass
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "03_acf.png", dpi=110)
    plt.close(fig)

    # 4. Spread distribution
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, prod in zip(axes, PRODUCTS):
        sub = px[px["product"] == prod]
        sp = (sub["ask_price_1"] - sub["bid_price_1"]).dropna()
        ax.hist(sp, bins=30, alpha=0.7)
        ax.set_title(f"{prod} bid-ask spread")
        ax.set_xlabel("spread")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "04_spread_hist.png", dpi=110)
    plt.close(fig)

    # 5. IPR trend overlay (linear fit per day + global)
    fig, ax = plt.subplots(1, 1, figsize=(14, 5))
    sub = px[(px["product"] == "INTARIAN_PEPPER_ROOT") & (px["mid_price"] > 0)].sort_values(["day_file", "timestamp"])
    ax.plot(sub["t_abs"].values, sub["mid_price"].values, lw=0.4, alpha=0.7, label="mid")
    # Per-day linear fits
    for d in DAYS:
        s = sub[sub["day_file"] == d]
        if len(s) > 10:
            ts = s["timestamp"].values
            mid = s["mid_price"].values
            slope, intercept = np.polyfit(ts, mid, 1)
            t_abs = s["t_abs"].values
            ax.plot(t_abs, intercept + slope * ts, color="red", lw=1.5, alpha=0.8)
    ax.set_title("INTARIAN_PEPPER_ROOT mid + per-day OLS trend")
    ax.set_ylabel("mid_price")
    ax.set_xlabel("absolute timestamp")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "05_ipr_trend.png", dpi=110)
    plt.close(fig)

    # 6. Kalman MLE Q,R per product per day (bar plot)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    for ax, prod in zip(axes, PRODUCTS):
        days_keys = [k for k in kal.get(prod, {}).keys() if k.startswith("day_")]
        qs = [kal[prod][k]["q_mle"] for k in days_keys]
        rs = [kal[prod][k]["r_mle"] for k in days_keys]
        x = np.arange(len(days_keys))
        ax2 = ax.twinx()
        ax.bar(x - 0.2, qs, width=0.4, color="C0", label="Q")
        ax2.bar(x + 0.2, rs, width=0.4, color="C1", label="R")
        ax.set_xticks(x)
        ax.set_xticklabels(days_keys, rotation=20)
        ax.set_title(f"{prod} Kalman MLE Q (blue), R (orange)")
        ax.set_yscale("log")
        ax2.set_yscale("log")
    fig.tight_layout()
    fig.savefig(PLOT_DIR / "06_kalman_mle.png", dpi=110)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Loading data...")
    px = load_prices()
    tr = load_trades()
    print(f"  prices rows: {len(px)}; trades rows: {len(tr)}")

    print("[1] Descriptive stats...")
    desc = describe_book(px)

    print("[2] Returns + stationarity...")
    rs = returns_and_stationarity(px)

    print("[3] Microstructure...")
    micro = microstructure(px)

    print("[4] Kalman MLE...")
    kal = kalman_section(px)

    print("[5] HMM (this may take a minute)...")
    hmm = hmm_section(px)

    print("[6] Signal IC...")
    sig = signal_ic_section(px)

    print("[7] Cross-day / cross-product...")
    cross = cross_section(px)

    print("[8] MAF estimate...")
    maf = maf_estimate(desc)

    print("[9] Plots...")
    make_plots(px, rs, kal)

    summary = {
        "descriptive": desc,
        "returns_stationarity": rs,
        "microstructure": micro,
        "kalman_mle": kal,
        "hmm": hmm,
        "signal_ic": sig,
        "cross": cross,
        "maf": maf,
    }
    OUT_DIR.joinpath("eda_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"Wrote {OUT_DIR / 'eda_summary.json'}")
    print(f"Plots in {PLOT_DIR}")


if __name__ == "__main__":
    main()
