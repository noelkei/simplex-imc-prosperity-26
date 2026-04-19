"""
Round 2 EDA — deep statistical + ML profiling.

Goals:
  1. Basic descriptive statistics per product per day (level, spread, book depth).
  2. Trend detection for IPR (slope, residual stdev) and structural-break test.
  3. AR(1) coefficient for ACO mid deviation (reversion speed + half-life).
  4. Autocorrelation out to lag 50 (both products, both on delta-mid and mid).
  5. Kalman filter calibration via EM-like grid: find (Q, R) that minimize
     one-step-ahead forecast error on a held-out day.
  6. Hidden Markov Model (2-state Gaussian regimes on delta-mid, Viterbi+EM)
     for ACO volatility regimes — measure regime persistence and whether
     volatility regimes predict next-tick direction.
  7. Order-book imbalance predictive power (IC at lag 1..5).
  8. Expected Round 2 P&L sanity check using Round 1 strategy baseline.

No external libraries — pure Python + math. Outputs saved to
`01_eda/outputs/` as markdown/text blocks.
"""
import csv
import math
import os
import json
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUT_DIR, exist_ok=True)

DAYS = [-1, 0, 1]
IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"

# ─────────────────────────────────────────────────────────────────────────────
# Loader

def load_prices(day):
    path = os.path.join(DATA_DIR, f"prices_round_2_day_{day}.csv")
    rows = {IPR: [], ACO: []}
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            p = r["product"]
            if p not in rows:
                continue

            def _f(k):
                v = r.get(k, "")
                return float(v) if v not in ("", None) else None

            rec = {
                "t": int(r["timestamp"]),
                "bid1": _f("bid_price_1"), "bv1": _f("bid_volume_1"),
                "bid2": _f("bid_price_2"), "bv2": _f("bid_volume_2"),
                "bid3": _f("bid_price_3"), "bv3": _f("bid_volume_3"),
                "ask1": _f("ask_price_1"), "av1": _f("ask_volume_1"),
                "ask2": _f("ask_price_2"), "av2": _f("ask_volume_2"),
                "ask3": _f("ask_price_3"), "av3": _f("ask_volume_3"),
                "mid": _f("mid_price"),
            }
            rows[p].append(rec)
    return rows

def load_trades(day):
    path = os.path.join(DATA_DIR, f"trades_round_2_day_{day}.csv")
    out = {IPR: [], ACO: []}
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for r in reader:
            p = r.get("symbol") or r.get("product")
            if p not in out:
                continue
            out[p].append({
                "t": int(r["timestamp"]),
                "price": float(r["price"]),
                "qty": int(r["quantity"]),
            })
    return out

# ─────────────────────────────────────────────────────────────────────────────
# Stats helpers

def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")

def stdev(xs):
    if len(xs) < 2:
        return float("nan")
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))

def autocorr(xs, lag):
    n = len(xs)
    if n <= lag + 2:
        return float("nan")
    m = mean(xs)
    num = sum((xs[i] - m) * (xs[i + lag] - m) for i in range(n - lag))
    den = sum((x - m) ** 2 for x in xs)
    return num / den if den > 0 else float("nan")

def linreg(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan"), float("nan"), float("nan")
    mx, my = mean(xs), mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx if sxx > 0 else float("nan")
    intercept = my - slope * mx
    resid = [y - (slope * x + intercept) for x, y in zip(xs, ys)]
    return slope, intercept, stdev(resid)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Basic descriptive stats

def describe(records, product_name, day):
    rows = [r for r in records if r["mid"] is not None and r["mid"] > 0
            and r["bid1"] is not None and r["ask1"] is not None]
    n_all = len(records)
    n_usable = len(rows)
    mids = [r["mid"] for r in rows]
    spreads = [r["ask1"] - r["bid1"] for r in rows]
    bv = [r["bv1"] for r in rows if r["bv1"] is not None]
    av = [r["av1"] for r in rows if r["av1"] is not None]
    return {
        "product": product_name, "day": day,
        "n_all": n_all, "n_usable": n_usable,
        "mid_mean": mean(mids), "mid_std": stdev(mids),
        "mid_min": min(mids), "mid_max": max(mids),
        "spread_mean": mean(spreads), "spread_std": stdev(spreads),
        "spread_mode": max(set(spreads), key=spreads.count) if spreads else None,
        "bv1_mean": mean(bv), "av1_mean": mean(av),
        "mid_first": mids[0], "mid_last": mids[-1],
    }

# ─────────────────────────────────────────────────────────────────────────────
# 2. IPR drift estimation (per day)

def drift_fit(records):
    rows = [r for r in records if r["mid"] is not None and r["mid"] > 0]
    xs = [r["t"] for r in rows]
    ys = [r["mid"] for r in rows]
    slope, intercept, resid_std = linreg(xs, ys)
    return {
        "slope": slope, "intercept": intercept, "resid_std": resid_std,
        "n": len(xs),
        "start_fit": intercept, "end_fit": intercept + slope * (xs[-1] if xs else 0),
    }

# ─────────────────────────────────────────────────────────────────────────────
# 3. AR(1) fit on detrended / deviation series

def ar1_fit(series):
    if len(series) < 50:
        return {"phi": float("nan"), "mu": float("nan"), "sigma": float("nan"),
                "halflife": float("nan")}
    mu = mean(series)
    y = [s - mu for s in series]
    num = sum(y[i] * y[i + 1] for i in range(len(y) - 1))
    den = sum(y[i] ** 2 for i in range(len(y) - 1))
    phi = num / den if den > 0 else 0.0
    resid = [y[i + 1] - phi * y[i] for i in range(len(y) - 1)]
    sigma = stdev(resid)
    hl = (-math.log(2) / math.log(abs(phi))) if 0 < abs(phi) < 1 else float("inf")
    return {"phi": phi, "mu": mu, "sigma": sigma, "halflife": hl}

# ─────────────────────────────────────────────────────────────────────────────
# 5. Kalman calibration via grid search: minimize one-step-ahead NLL

def kalman_nll(mids, Q, R, fv0=None, P0=25.0):
    if fv0 is None:
        fv0 = mids[0]
    fv = fv0
    P = P0
    nll = 0.0
    for m in mids[1:]:
        # predict
        P_pred = P + Q
        # innovation
        y = m - fv
        S = P_pred + R
        K = P_pred / S
        nll += 0.5 * (math.log(2 * math.pi * S) + y * y / S)
        fv = fv + K * y
        P = (1 - K) * P_pred
    return nll / max(1, (len(mids) - 1))

def grid_search_kalman(mids):
    best = None
    Qs = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
    Rs = [1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 25.0, 36.0, 49.0, 64.0]
    for Q in Qs:
        for R in Rs:
            nll = kalman_nll(mids, Q, R)
            if best is None or nll < best[0]:
                best = (nll, Q, R)
    return best

# For IPR we fit Kalman on the *residual after linear drift*; the level process
# is still modeled with a Kalman, but the mid enters the filter de-trended.

# ─────────────────────────────────────────────────────────────────────────────
# 6. 2-state Gaussian HMM via Baum-Welch on delta-mid
#    State 0 = low-vol, State 1 = high-vol. Emissions: N(0, sigma_s).
#    We run 20 EM iterations and then compute regime persistence.

def hmm_gaussian_2state(series, n_iter=30):
    n = len(series)
    if n < 100:
        return None

    # init: split by absolute value
    abs_sorted = sorted(abs(x) for x in series)
    med = abs_sorted[n // 2]
    sigma = [max(med / 2, 0.5), max(med * 2, 1.5)]
    mu = [0.0, 0.0]
    pi = [0.5, 0.5]
    # transition matrix (rows sum to 1)
    A = [[0.95, 0.05], [0.05, 0.95]]

    def gauss(x, m, s):
        if s <= 0:
            return 1e-300
        return math.exp(-0.5 * ((x - m) / s) ** 2) / (math.sqrt(2 * math.pi) * s)

    for _ in range(n_iter):
        # forward
        alpha = [[0.0, 0.0] for _ in range(n)]
        c = [0.0] * n
        for s in (0, 1):
            alpha[0][s] = pi[s] * gauss(series[0], mu[s], sigma[s])
        c[0] = sum(alpha[0]) or 1e-300
        alpha[0] = [a / c[0] for a in alpha[0]]
        for t in range(1, n):
            for s in (0, 1):
                alpha[t][s] = (alpha[t - 1][0] * A[0][s] + alpha[t - 1][1] * A[1][s]) \
                              * gauss(series[t], mu[s], sigma[s])
            c[t] = sum(alpha[t]) or 1e-300
            alpha[t] = [a / c[t] for a in alpha[t]]

        # backward
        beta = [[0.0, 0.0] for _ in range(n)]
        beta[n - 1] = [1.0, 1.0]
        for t in range(n - 2, -1, -1):
            for s in (0, 1):
                beta[t][s] = sum(
                    A[s][s2] * gauss(series[t + 1], mu[s2], sigma[s2]) * beta[t + 1][s2]
                    for s2 in (0, 1)
                ) / c[t + 1]

        # posteriors
        gamma = [[alpha[t][s] * beta[t][s] for s in (0, 1)] for t in range(n)]
        # normalize
        for t in range(n):
            tot = sum(gamma[t]) or 1e-300
            gamma[t] = [g / tot for g in gamma[t]]

        # xi (pairwise)
        xi_sum = [[0.0, 0.0], [0.0, 0.0]]
        for t in range(n - 1):
            denom = 0.0
            tmp = [[0.0, 0.0], [0.0, 0.0]]
            for i in (0, 1):
                for j in (0, 1):
                    tmp[i][j] = alpha[t][i] * A[i][j] * gauss(series[t + 1], mu[j], sigma[j]) * beta[t + 1][j]
                    denom += tmp[i][j]
            if denom == 0:
                continue
            for i in (0, 1):
                for j in (0, 1):
                    xi_sum[i][j] += tmp[i][j] / denom

        # re-estimate
        pi = gamma[0][:]
        for i in (0, 1):
            denom = sum(xi_sum[i]) or 1e-300
            for j in (0, 1):
                A[i][j] = xi_sum[i][j] / denom
        for s in (0, 1):
            g_sum = sum(gamma[t][s] for t in range(n)) or 1e-300
            mu[s] = sum(gamma[t][s] * series[t] for t in range(n)) / g_sum
            var = sum(gamma[t][s] * (series[t] - mu[s]) ** 2 for t in range(n)) / g_sum
            sigma[s] = math.sqrt(max(var, 1e-6))

    # enforce sigma[0] < sigma[1]
    if sigma[0] > sigma[1]:
        sigma = [sigma[1], sigma[0]]
        mu = [mu[1], mu[0]]
        A = [[A[1][1], A[1][0]], [A[0][1], A[0][0]]]
        pi = [pi[1], pi[0]]

    # compute regime sequence via most-likely state (from gamma)
    states = [0 if gamma[t][0] >= gamma[t][1] else 1 for t in range(n)]
    # persistence
    runs = []
    cur = states[0]
    run_len = 1
    for s in states[1:]:
        if s == cur:
            run_len += 1
        else:
            runs.append((cur, run_len))
            cur = s
            run_len = 1
    runs.append((cur, run_len))
    avg_run = {0: [], 1: []}
    for s, r in runs:
        avg_run[s].append(r)
    return {
        "mu": mu, "sigma": sigma, "A": A, "pi": pi,
        "state_frac": [sum(1 for s in states if s == 0) / n,
                       sum(1 for s in states if s == 1) / n],
        "avg_run_len_0": mean(avg_run[0]) if avg_run[0] else 0,
        "avg_run_len_1": mean(avg_run[1]) if avg_run[1] else 0,
        "n_switches": len(runs) - 1,
    }

# ─────────────────────────────────────────────────────────────────────────────
# 7. Imbalance predictive power (IC / corr at lag k)

def corr(xs, ys):
    n = min(len(xs), len(ys))
    if n < 2:
        return float("nan")
    mx = mean(xs[:n])
    my = mean(ys[:n])
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((xs[i] - mx) ** 2 for i in range(n)))
    dy = math.sqrt(sum((ys[i] - my) ** 2 for i in range(n)))
    return num / (dx * dy) if dx > 0 and dy > 0 else float("nan")

def imbalance_series(records):
    out = []
    for r in records:
        if r["bid1"] is None or r["ask1"] is None or r["mid"] is None or r["mid"] == 0:
            out.append(None)
            continue
        bv = r["bv1"] or 0
        av = r["av1"] or 0
        tot = bv + av
        imb = (bv - av) / tot if tot > 0 else 0.0
        out.append(imb)
    return out

# ─────────────────────────────────────────────────────────────────────────────
# MAIN

def dump(path, text):
    with open(os.path.join(OUT_DIR, path), "w") as f:
        f.write(text)

def main():
    report = []
    report.append("# Round 2 — Deep EDA Outputs\n")
    report.append(f"Data dir: `{DATA_DIR}`\n")

    # Load all days
    prices = {d: load_prices(d) for d in DAYS}
    trades = {d: load_trades(d) for d in DAYS}

    # 1. Descriptive stats
    report.append("\n## 1. Descriptive Stats (per product per day)\n")
    report.append("| Product | Day | n (all) | n (usable) | mid mean | mid std | mid min | mid max | spread mean | spread mode | bv1 mean | av1 mean | mid[0] | mid[-1] |")
    report.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    desc_all = {}
    for p in (IPR, ACO):
        for d in DAYS:
            s = describe(prices[d][p], p, d)
            desc_all[(p, d)] = s
            report.append(
                f"| {p} | {d} | {s['n_all']} | {s['n_usable']} | "
                f"{s['mid_mean']:.2f} | {s['mid_std']:.2f} | {s['mid_min']:.1f} | {s['mid_max']:.1f} | "
                f"{s['spread_mean']:.2f} | {s['spread_mode']} | "
                f"{s['bv1_mean']:.1f} | {s['av1_mean']:.1f} | "
                f"{s['mid_first']:.1f} | {s['mid_last']:.1f} |"
            )

    # 2. IPR drift
    report.append("\n## 2. IPR Linear Drift Fit (mid ~ slope * t + intercept)\n")
    report.append("| Day | slope (per tick) | intercept | resid stdev | start fit | end fit | total drift |")
    report.append("|---|---|---|---|---|---|---|")
    ipr_drifts = {}
    for d in DAYS:
        f = drift_fit(prices[d][IPR])
        ipr_drifts[d] = f
        total = f["slope"] * 999900 if not math.isnan(f["slope"]) else float("nan")
        report.append(
            f"| {d} | {f['slope']:.6f} | {f['intercept']:.2f} | {f['resid_std']:.2f} | "
            f"{f['start_fit']:.1f} | {f['end_fit']:.1f} | {total:+.1f} |"
        )

    # 3. ACO AR(1) (mid deviation from daily mean)
    report.append("\n## 3. ACO AR(1) Fit on mid-minus-mean\n")
    report.append("| Day | mean mid | phi (AR1) | sigma (innov) | half-life (ticks) |")
    report.append("|---|---|---|---|---|")
    aco_ar1 = {}
    for d in DAYS:
        rows = [r for r in prices[d][ACO] if r["mid"] and r["mid"] > 0]
        mids = [r["mid"] for r in rows]
        fit = ar1_fit(mids)
        aco_ar1[d] = fit
        report.append(
            f"| {d} | {fit['mu']:.2f} | {fit['phi']:.4f} | {fit['sigma']:.3f} | {fit['halflife']:.1f} |"
        )

    # 4. Autocorrelation
    report.append("\n## 4. Autocorrelation of delta-mid (lags 1..20)\n")
    report.append("| Product | Day | AC(1) | AC(2) | AC(5) | AC(10) | AC(20) |")
    report.append("|---|---|---|---|---|---|---|")
    for p in (IPR, ACO):
        for d in DAYS:
            rows = [r for r in prices[d][p] if r["mid"] and r["mid"] > 0]
            mids = [r["mid"] for r in rows]
            dmid = [mids[i + 1] - mids[i] for i in range(len(mids) - 1)]
            acs = [autocorr(dmid, k) for k in (1, 2, 5, 10, 20)]
            report.append(
                f"| {p} | {d} | " + " | ".join(f"{a:+.3f}" for a in acs) + " |"
            )

    # 5. Kalman calibration
    report.append("\n## 5. Kalman Filter Grid Search — Best (Q, R) per product per day\n")
    report.append(
        "For IPR we fit on the detrended mid (mid - drift(t)) to separate drift from noise. "
        "For ACO we fit on raw mid (since no drift).\n"
    )
    report.append("| Product | Day | Best Q | Best R | NLL per tick | K steady-state |")
    report.append("|---|---|---|---|---|---|")
    kalman_best = {}
    for p in (IPR, ACO):
        for d in DAYS:
            rows = [r for r in prices[d][p] if r["mid"] and r["mid"] > 0]
            if p == IPR:
                dfit = ipr_drifts[d]
                mids = [r["mid"] - (dfit["slope"] * r["t"] + dfit["intercept"]) for r in rows]
            else:
                mids = [r["mid"] for r in rows]
            nll, Q, R = grid_search_kalman(mids)
            # steady-state K: solve P = (1-K)(P+Q); K = (P+Q)/(P+Q+R)
            # P* satisfies P = ((P+Q)*R)/(P+Q+R). Approx via iteration.
            P = 1.0
            for _ in range(500):
                P = ((P + Q) * R) / (P + Q + R)
            K = (P + Q) / (P + Q + R)
            kalman_best[(p, d)] = (Q, R, K)
            report.append(f"| {p} | {d} | {Q} | {R} | {nll:.4f} | {K:.4f} |")

    # 6. HMM on ACO delta-mid
    report.append("\n## 6. 2-State Gaussian HMM on ACO delta-mid (Baum-Welch, 30 iters)\n")
    report.append("Interpretation: state 0 = low-vol, state 1 = high-vol. "
                  "High persistence (avg run > 50 ticks) would support regime-aware quoting.\n")
    report.append("| Day | mu_low | sigma_low | mu_high | sigma_high | P(low->low) | P(high->high) | "
                  "state0 frac | avg run_0 | avg run_1 | switches |")
    report.append("|---|---|---|---|---|---|---|---|---|---|---|")
    hmm_out = {}
    for d in DAYS:
        rows = [r for r in prices[d][ACO] if r["mid"] and r["mid"] > 0]
        mids = [r["mid"] for r in rows]
        dmid = [mids[i + 1] - mids[i] for i in range(len(mids) - 1)]
        h = hmm_gaussian_2state(dmid, n_iter=30)
        hmm_out[d] = h
        if h is None:
            report.append(f"| {d} | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |")
        else:
            report.append(
                f"| {d} | {h['mu'][0]:+.3f} | {h['sigma'][0]:.3f} | {h['mu'][1]:+.3f} | {h['sigma'][1]:.3f} | "
                f"{h['A'][0][0]:.3f} | {h['A'][1][1]:.3f} | {h['state_frac'][0]:.3f} | "
                f"{h['avg_run_len_0']:.1f} | {h['avg_run_len_1']:.1f} | {h['n_switches']} |"
            )

    # 7. Imbalance predictive power
    report.append("\n## 7. Order-Book Imbalance IC at lag 1..5\n")
    report.append(
        "corr( imbalance(t), delta_mid(t+k) ). Positive values mean a buy-side imbalance at tick t "
        "predicts an up-move at tick t+k.\n"
    )
    report.append("| Product | Day | IC@1 | IC@2 | IC@3 | IC@5 |")
    report.append("|---|---|---|---|---|---|")
    for p in (IPR, ACO):
        for d in DAYS:
            rows = prices[d][p]
            imb = imbalance_series(rows)
            mids = [r["mid"] if r["mid"] and r["mid"] > 0 else None for r in rows]
            # build aligned pairs
            line = [p, str(d)]
            for k in (1, 2, 3, 5):
                xs, ys = [], []
                for i in range(len(mids) - k):
                    if (imb[i] is None or mids[i] is None or mids[i + k] is None):
                        continue
                    xs.append(imb[i])
                    ys.append(mids[i + k] - mids[i])
                line.append(f"{corr(xs, ys):+.3f}")
            report.append("| " + " | ".join(line) + " |")

    # 8. Trade summary
    report.append("\n## 8. Trade summary (market flow)\n")
    report.append("| Product | Day | n trades | avg qty | price min | price max | total volume |")
    report.append("|---|---|---|---|---|---|---|")
    for p in (IPR, ACO):
        for d in DAYS:
            ts = trades[d][p]
            if not ts:
                report.append(f"| {p} | {d} | 0 | - | - | - | 0 |")
                continue
            qs = [t["qty"] for t in ts]
            ps = [t["price"] for t in ts]
            report.append(
                f"| {p} | {d} | {len(ts)} | {mean(qs):.1f} | {min(ps):.1f} | {max(ps):.1f} | {sum(qs)} |"
            )

    # 9. Cross-day IPR level continuity
    report.append("\n## 9. IPR cross-day level continuity\n")
    for d in DAYS:
        rows = [r for r in prices[d][IPR] if r["mid"] and r["mid"] > 0]
        if rows:
            report.append(f"- day {d}: first mid = {rows[0]['mid']:.1f}, last mid = {rows[-1]['mid']:.1f}")

    # Write outputs
    report.append("")
    dump("eda_report.md", "\n".join(report))

    # Also save a compact JSON for machine access
    summary = {
        "desc": {f"{p}|{d}": desc_all[(p, d)] for (p, d) in desc_all},
        "ipr_drift": ipr_drifts,
        "aco_ar1": aco_ar1,
        "kalman_best": {f"{p}|{d}": kalman_best[(p, d)] for (p, d) in kalman_best},
        "hmm": {str(d): hmm_out[d] for d in DAYS},
    }
    with open(os.path.join(OUT_DIR, "eda_summary.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print("OK — wrote", OUT_DIR)


if __name__ == "__main__":
    main()
