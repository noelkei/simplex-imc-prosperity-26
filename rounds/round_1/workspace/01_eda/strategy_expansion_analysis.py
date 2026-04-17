"""Round 1 strategy expansion diagnostics.

This script is an EDA helper, not trading code. It reads the raw round CSVs and
writes reusable metrics for feature engineering, transformations, Markov state
models, light regressions, PCA-style feature structure, microstructure edges,
and cross-product relationships.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median


ROOT = Path(__file__).resolve().parents[4]
RAW_DIR = ROOT / "rounds" / "round_1" / "data" / "raw"
OUT_PATH = ROOT / "rounds" / "round_1" / "data" / "processed" / "strategy_expansion_metrics.json"

PRODUCTS = ("INTARIAN_PEPPER_ROOT", "ASH_COATED_OSMIUM")
IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"

LEVELS = (1, 2, 3)


def as_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def as_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(float(value))


def corr(xs: list[float], ys: list[float]) -> float | None:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    x_vals = [p[0] for p in pairs]
    y_vals = [p[1] for p in pairs]
    mx = mean(x_vals)
    my = mean(y_vals)
    sx = math.sqrt(sum((x - mx) ** 2 for x in x_vals))
    sy = math.sqrt(sum((y - my) ** 2 for y in y_vals))
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in pairs) / (sx * sy)


def stdev(values: list[float]) -> float | None:
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return None
    m = mean(vals)
    return math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))


def quantiles(values: list[float]) -> dict[str, float | None]:
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return {"min": None, "p05": None, "p25": None, "median": None, "p75": None, "p95": None, "max": None}

    def q(p: float) -> float:
        pos = p * (len(vals) - 1)
        lo = int(math.floor(pos))
        hi = int(math.ceil(pos))
        if lo == hi:
            return vals[lo]
        return vals[lo] * (hi - pos) + vals[hi] * (pos - lo)

    return {
        "min": vals[0],
        "p05": q(0.05),
        "p25": q(0.25),
        "median": q(0.50),
        "p75": q(0.75),
        "p95": q(0.95),
        "max": vals[-1],
    }


def round_value(value: object, digits: int = 6) -> object:
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, digits)
    if isinstance(value, dict):
        return {k: round_value(v, digits) for k, v in value.items()}
    if isinstance(value, list):
        return [round_value(v, digits) for v in value]
    return value


def load_prices() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW_DIR.glob("prices_round_1_day_*.csv")):
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                parsed = {
                    "source": path.name,
                    "day": as_int(row["day"]),
                    "timestamp": as_int(row["timestamp"]),
                    "product": row["product"],
                    "mid_price": as_float(row["mid_price"]),
                    "profit_and_loss": as_float(row["profit_and_loss"]),
                }
                for side in ("bid", "ask"):
                    for level in LEVELS:
                        parsed[f"{side}_price_{level}"] = as_float(row[f"{side}_price_{level}"])
                        parsed[f"{side}_volume_{level}"] = as_float(row[f"{side}_volume_{level}"])
                rows.append(parsed)
    rows.sort(key=lambda r: (r["day"], r["timestamp"], r["product"]))
    return rows


def load_trades() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW_DIR.glob("trades_round_1_day_*.csv")):
        day = int(path.stem.split("_day_")[-1])
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                rows.append(
                    {
                        "source": path.name,
                        "day": day,
                        "timestamp": as_int(row["timestamp"]),
                        "symbol": row["symbol"],
                        "price": as_float(row["price"]),
                        "quantity": as_float(row["quantity"]),
                    }
                )
    rows.sort(key=lambda r: (r["day"], r["timestamp"], r["symbol"]))
    return rows


def add_features(rows: list[dict]) -> list[dict]:
    first_mid: dict[tuple[int, str], float] = {}
    for row in rows:
        key = (row["day"], row["product"])
        mid = row["mid_price"]
        if key not in first_mid and mid not in (None, 0):
            if row["product"] == IPR:
                first_mid[key] = mid - 0.001 * row["timestamp"]
            else:
                first_mid[key] = 10000.0

    by_key: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in rows:
        product = row["product"]
        day = row["day"]
        mid = row["mid_price"]
        bid_1 = row["bid_price_1"]
        ask_1 = row["ask_price_1"]
        bid_depth = sum((row[f"bid_volume_{level}"] or 0.0) for level in LEVELS)
        ask_depth = sum(abs(row[f"ask_volume_{level}"] or 0.0) for level in LEVELS)
        l1_bid_depth = row["bid_volume_1"] or 0.0
        l1_ask_depth = abs(row["ask_volume_1"] or 0.0)
        total_depth = bid_depth + ask_depth
        l1_depth = l1_bid_depth + l1_ask_depth
        both_sides = bid_1 is not None and ask_1 is not None
        one_sided = (bid_1 is None) != (ask_1 is None)
        spread = ask_1 - bid_1 if both_sides else None
        fv = first_mid.get((day, product)) if product == IPR else 10000.0
        residual = mid - fv - (0.001 * row["timestamp"] if product == IPR else 0.0) if mid not in (None, 0) else None
        log_residual = math.log(mid) - math.log(fv + (0.001 * row["timestamp"] if product == IPR else 0.0)) if mid not in (None, 0) else None
        row.update(
            {
                "valid_mid": mid not in (None, 0),
                "both_sides": both_sides,
                "one_sided": one_sided,
                "zero_mid": mid in (None, 0),
                "spread": spread,
                "relative_spread": spread / mid if spread is not None and mid else None,
                "bid_depth": bid_depth,
                "ask_depth": ask_depth,
                "total_depth": total_depth,
                "imbalance_l1": (l1_bid_depth - l1_ask_depth) / l1_depth if l1_depth else None,
                "imbalance_l3": (bid_depth - ask_depth) / total_depth if total_depth else None,
                "fair_value": fv + (0.001 * row["timestamp"] if product == IPR and fv is not None else 0.0),
                "residual": residual,
                "log_residual": log_residual,
                "log_residual_price_scaled": log_residual * mid if log_residual is not None and mid else None,
                "buy_edge_best_ask": (fv + (0.001 * row["timestamp"] if product == IPR else 0.0)) - ask_1
                if ask_1 is not None and fv is not None
                else None,
                "sell_edge_best_bid": bid_1 - (fv + (0.001 * row["timestamp"] if product == IPR else 0.0))
                if bid_1 is not None and fv is not None
                else None,
            }
        )
        by_key[(day, product)].append(row)

    for group in by_key.values():
        group.sort(key=lambda r: r["timestamp"])
        for idx, row in enumerate(group):
            prev = group[idx - 1] if idx > 0 else None
            if prev and row["valid_mid"] and prev["valid_mid"]:
                row["mid_delta"] = row["mid_price"] - prev["mid_price"]
                row["log_return"] = math.log(row["mid_price"]) - math.log(prev["mid_price"])
                row["residual_delta"] = row["residual"] - prev["residual"]
            else:
                row["mid_delta"] = None
                row["log_return"] = None
                row["residual_delta"] = None
            for horizon in (1, 5, 10):
                fut = group[idx + horizon] if idx + horizon < len(group) else None
                if fut and row["residual"] is not None and fut["residual"] is not None:
                    row[f"future_residual_delta_{horizon}"] = fut["residual"] - row["residual"]
                    row[f"future_mid_delta_{horizon}"] = fut["mid_price"] - row["mid_price"]
                else:
                    row[f"future_residual_delta_{horizon}"] = None
                    row[f"future_mid_delta_{horizon}"] = None
    return rows


def data_quality(rows: list[dict], trades: list[dict]) -> dict:
    out = {}
    for product in PRODUCTS:
        product_rows = [r for r in rows if r["product"] == product]
        out[product] = {
            "price_rows": len(product_rows),
            "valid_mid_rows": sum(r["valid_mid"] for r in product_rows),
            "zero_mid_rows": sum(r["zero_mid"] for r in product_rows),
            "both_sides_rows": sum(r["both_sides"] for r in product_rows),
            "one_sided_rows": sum(r["one_sided"] for r in product_rows),
            "missing_bid1_rows": sum(r["bid_price_1"] is None for r in product_rows),
            "missing_ask1_rows": sum(r["ask_price_1"] is None for r in product_rows),
            "trade_rows": sum(t["symbol"] == product for t in trades),
        }
    return out


def univariate_regression(xs: list[float], ys: list[float]) -> dict:
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return {"n": len(pairs), "slope": None, "intercept": None, "r2": None}
    x_vals = [p[0] for p in pairs]
    y_vals = [p[1] for p in pairs]
    mx = mean(x_vals)
    my = mean(y_vals)
    var_x = sum((x - mx) ** 2 for x in x_vals)
    if var_x == 0:
        return {"n": len(pairs), "slope": None, "intercept": None, "r2": None}
    slope = sum((x - mx) * (y - my) for x, y in pairs) / var_x
    intercept = my - slope * mx
    preds = [intercept + slope * x for x in x_vals]
    ss_tot = sum((y - my) ** 2 for y in y_vals)
    ss_res = sum((y - p) ** 2 for y, p in zip(y_vals, preds))
    r2 = 1 - ss_res / ss_tot if ss_tot else None
    return {"n": len(pairs), "slope": slope, "intercept": intercept, "r2": r2}


def transformation_metrics(rows: list[dict]) -> dict:
    out = {}
    for product in PRODUCTS:
        product_rows = [r for r in rows if r["product"] == product and r["residual"] is not None]
        residuals = [r["residual"] for r in product_rows]
        log_scaled = [r["log_residual_price_scaled"] for r in product_rows]
        out[product] = {
            "residual_stats": {
                "mean": mean(residuals),
                "std": stdev(residuals),
                **quantiles(residuals),
            },
            "log_scaled_residual_stats": {
                "mean": mean(log_scaled),
                "std": stdev(log_scaled),
                **quantiles(log_scaled),
            },
            "raw_vs_log_scaled_corr": corr(residuals, log_scaled),
            "raw_residual_predicts_h1_delta": univariate_regression(
                residuals, [r["future_residual_delta_1"] for r in product_rows]
            ),
            "log_residual_predicts_h1_delta": univariate_regression(
                log_scaled, [r["future_residual_delta_1"] for r in product_rows]
            ),
            "raw_residual_predicts_h5_delta": univariate_regression(
                residuals, [r["future_residual_delta_5"] for r in product_rows]
            ),
            "log_residual_predicts_h5_delta": univariate_regression(
                log_scaled, [r["future_residual_delta_5"] for r in product_rows]
            ),
        }
    return out


BUCKETS = {
    IPR: [-math.inf, -6, -3, -1, 1, 3, 6, math.inf],
    ACO: [-math.inf, -20, -10, -3, 3, 10, 20, math.inf],
}
BUCKET_LABELS = ["deep_under", "under", "slight_under", "neutral", "slight_over", "over", "deep_over"]


def bucket(product: str, residual: float | None) -> str | None:
    if residual is None:
        return None
    bins = BUCKETS[product]
    for idx in range(len(bins) - 1):
        if bins[idx] <= residual < bins[idx + 1]:
            return BUCKET_LABELS[idx]
    return None


def markov_metrics(rows: list[dict]) -> dict:
    out = {}
    by_key: dict[tuple[int, str], list[dict]] = defaultdict(list)
    for row in rows:
        by_key[(row["day"], row["product"])].append(row)
    for product in PRODUCTS:
        transitions: dict[str, Counter] = {label: Counter() for label in BUCKET_LABELS}
        residual_by_bucket: dict[str, list[float]] = defaultdict(list)
        next_residual_by_bucket: dict[str, list[float]] = defaultdict(list)
        delta_by_bucket: dict[str, list[float]] = defaultdict(list)
        for day in sorted({r["day"] for r in rows}):
            group = sorted(by_key[(day, product)], key=lambda r: r["timestamp"])
            for idx, row in enumerate(group[:-1]):
                current_bucket = bucket(product, row["residual"])
                next_bucket = bucket(product, group[idx + 1]["residual"])
                if current_bucket is None or next_bucket is None:
                    continue
                transitions[current_bucket][next_bucket] += 1
                residual_by_bucket[current_bucket].append(row["residual"])
                next_residual_by_bucket[current_bucket].append(group[idx + 1]["residual"])
                delta_by_bucket[current_bucket].append(group[idx + 1]["residual"] - row["residual"])
        product_out = {}
        for label in BUCKET_LABELS:
            total = sum(transitions[label].values())
            probabilities = {
                dst: (transitions[label][dst] / total if total else 0.0) for dst in BUCKET_LABELS
            }
            product_out[label] = {
                "count": total,
                "probabilities": probabilities,
                "mode_next_bucket": max(probabilities, key=probabilities.get) if total else None,
                "mean_current_residual": mean(residual_by_bucket[label]) if residual_by_bucket[label] else None,
                "mean_next_residual": mean(next_residual_by_bucket[label]) if next_residual_by_bucket[label] else None,
                "mean_next_delta": mean(delta_by_bucket[label]) if delta_by_bucket[label] else None,
            }
        out[product] = product_out
    return out


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float] | None:
    n = len(vector)
    aug = [row[:] + [vector[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        for j in range(col, n + 1):
            aug[col][j] /= scale
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            for j in range(col, n + 1):
                aug[r][j] -= factor * aug[col][j]
    return [aug[i][n] for i in range(n)]


MODEL_FEATURES = [
    "residual",
    "log_residual_price_scaled",
    "spread",
    "imbalance_l1",
    "imbalance_l3",
    "total_depth",
    "one_sided",
]


def prepare_model_rows(rows: list[dict], product: str, horizon: int) -> tuple[list[dict], list[dict]]:
    usable = [
        r
        for r in rows
        if r["product"] == product
        and r["residual"] is not None
        and r[f"future_residual_delta_{horizon}"] is not None
    ]
    train = [r for r in usable if r["day"] in (-2, -1)]
    valid = [r for r in usable if r["day"] == 0]
    return train, valid


def fit_linear_model(train: list[dict], valid: list[dict], horizon: int) -> dict:
    if len(train) < 20 or len(valid) < 20:
        return {"train_n": len(train), "valid_n": len(valid), "r2": None}
    means = {}
    stds = {}
    for feature in MODEL_FEATURES:
        vals = [float(r[feature]) for r in train if r[feature] is not None]
        means[feature] = mean(vals) if vals else 0.0
        stds[feature] = stdev(vals) or 1.0

    def vector(row: dict) -> list[float]:
        vals = [1.0]
        for feature in MODEL_FEATURES:
            val = row[feature]
            vals.append(((float(val) if val is not None else means[feature]) - means[feature]) / stds[feature])
        return vals

    x_train = [vector(r) for r in train]
    y_train = [r[f"future_residual_delta_{horizon}"] for r in train]
    n_features = len(x_train[0])
    xtx = [[0.0 for _ in range(n_features)] for _ in range(n_features)]
    xty = [0.0 for _ in range(n_features)]
    for x_vec, y_val in zip(x_train, y_train):
        for i in range(n_features):
            xty[i] += x_vec[i] * y_val
            for j in range(n_features):
                xtx[i][j] += x_vec[i] * x_vec[j]
    for i in range(1, n_features):
        xtx[i][i] += 1e-6
    coefs = solve_linear_system(xtx, xty)
    if coefs is None:
        return {"train_n": len(train), "valid_n": len(valid), "r2": None}

    preds = []
    actuals = []
    for row in valid:
        x_vec = vector(row)
        preds.append(sum(c * x for c, x in zip(coefs, x_vec)))
        actuals.append(row[f"future_residual_delta_{horizon}"])
    y_mean = mean(actuals)
    ss_tot = sum((y - y_mean) ** 2 for y in actuals)
    ss_res = sum((y - p) ** 2 for y, p in zip(actuals, preds))
    r2 = 1 - ss_res / ss_tot if ss_tot else None
    sign_pairs = [(y, p) for y, p in zip(actuals, preds) if abs(y) > 1e-9 and abs(p) > 1e-9]
    sign_accuracy = (
        sum((y > 0) == (p > 0) for y, p in sign_pairs) / len(sign_pairs) if sign_pairs else None
    )
    return {
        "train_n": len(train),
        "valid_n": len(valid),
        "target": f"future_residual_delta_{horizon}",
        "r2_day0": r2,
        "mae_day0": mean(abs(y - p) for y, p in zip(actuals, preds)),
        "sign_accuracy_day0": sign_accuracy,
        "target_std_day0": stdev(actuals),
        "coefficients_standardized": {"intercept": coefs[0], **{f: coefs[i + 1] for i, f in enumerate(MODEL_FEATURES)}},
    }


def light_model_metrics(rows: list[dict]) -> dict:
    out = {}
    for product in PRODUCTS:
        out[product] = {}
        for horizon in (1, 5, 10):
            train, valid = prepare_model_rows(rows, product, horizon)
            out[product][f"horizon_{horizon}"] = fit_linear_model(train, valid, horizon)
    return out


def jacobi_eigen(matrix: list[list[float]], max_iter: int = 100) -> tuple[list[float], list[list[float]]]:
    n = len(matrix)
    a = [row[:] for row in matrix]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(max_iter):
        p, q = 0, 1
        max_val = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > max_val:
                    max_val = abs(a[i][j])
                    p, q = i, j
        if max_val < 1e-10:
            break
        angle = 0.5 * math.atan2(2 * a[p][q], a[q][q] - a[p][p])
        c = math.cos(angle)
        s = math.sin(angle)
        app = c * c * a[p][p] - 2 * s * c * a[p][q] + s * s * a[q][q]
        aqq = s * s * a[p][p] + 2 * s * c * a[p][q] + c * c * a[q][q]
        a[p][q] = a[q][p] = 0.0
        a[p][p] = app
        a[q][q] = aqq
        for k in range(n):
            if k not in (p, q):
                akp = c * a[k][p] - s * a[k][q]
                akq = s * a[k][p] + c * a[k][q]
                a[k][p] = a[p][k] = akp
                a[k][q] = a[q][k] = akq
        for k in range(n):
            vkp = c * v[k][p] - s * v[k][q]
            vkq = s * v[k][p] + c * v[k][q]
            v[k][p] = vkp
            v[k][q] = vkq
    eigenvalues = [a[i][i] for i in range(n)]
    eigenvectors = [[v[row][col] for row in range(n)] for col in range(n)]
    pairs = sorted(zip(eigenvalues, eigenvectors), key=lambda p: p[0], reverse=True)
    return [p[0] for p in pairs], [p[1] for p in pairs]


PCA_FEATURES = ["residual", "spread", "imbalance_l1", "imbalance_l3", "total_depth"]


def pca_metrics(rows: list[dict]) -> dict:
    out = {}
    for product in PRODUCTS:
        usable = [r for r in rows if r["product"] == product and r["residual"] is not None]
        means = {}
        stds = {}
        for feature in PCA_FEATURES:
            vals = [float(r[feature]) for r in usable if r[feature] is not None]
            means[feature] = mean(vals) if vals else 0.0
            stds[feature] = stdev(vals) or 1.0
        matrix_rows = []
        for row in usable:
            matrix_rows.append(
                [
                    ((float(row[feature]) if row[feature] is not None else means[feature]) - means[feature])
                    / stds[feature]
                    for feature in PCA_FEATURES
                ]
            )
        n = len(matrix_rows)
        cov = [[0.0 for _ in PCA_FEATURES] for _ in PCA_FEATURES]
        for vec in matrix_rows:
            for i in range(len(PCA_FEATURES)):
                for j in range(len(PCA_FEATURES)):
                    cov[i][j] += vec[i] * vec[j] / max(n - 1, 1)
        eigenvalues, eigenvectors = jacobi_eigen(cov)
        total = sum(max(v, 0.0) for v in eigenvalues)
        components = []
        for idx, (value, vector) in enumerate(zip(eigenvalues[:3], eigenvectors[:3]), start=1):
            components.append(
                {
                    "component": idx,
                    "explained_variance_ratio": value / total if total else None,
                    "weights": dict(zip(PCA_FEATURES, vector)),
                }
            )
        out[product] = {"n": n, "components": components}
    return out


def microstructure_metrics(rows: list[dict]) -> dict:
    out = {}
    thresholds = [0, 2, 5, 8, 10]
    for product in PRODUCTS:
        product_rows = [r for r in rows if r["product"] == product and r["valid_mid"]]
        buy_edges = [r["buy_edge_best_ask"] for r in product_rows if r["buy_edge_best_ask"] is not None]
        sell_edges = [r["sell_edge_best_bid"] for r in product_rows if r["sell_edge_best_bid"] is not None]
        edge_counts = {}
        for threshold in thresholds:
            edge_counts[str(threshold)] = {
                "buy_best_ask_edge_rows": sum(edge is not None and edge > threshold for edge in buy_edges),
                "sell_best_bid_edge_rows": sum(edge is not None and edge > threshold for edge in sell_edges),
                "buy_share": sum(edge is not None and edge > threshold for edge in buy_edges) / len(product_rows),
                "sell_share": sum(edge is not None and edge > threshold for edge in sell_edges) / len(product_rows),
            }
        spreads = [r["spread"] for r in product_rows if r["spread"] is not None]
        out[product] = {
            "spread_stats": {"mean": mean(spreads), "std": stdev(spreads), **quantiles(spreads)},
            "buy_edge_best_ask_stats": {"mean": mean(buy_edges), "std": stdev(buy_edges), **quantiles(buy_edges)},
            "sell_edge_best_bid_stats": {"mean": mean(sell_edges), "std": stdev(sell_edges), **quantiles(sell_edges)},
            "edge_counts_by_threshold": edge_counts,
            "imbalance_l1_predicts_h1_delta_corr": corr(
                [r["imbalance_l1"] for r in product_rows],
                [r["future_residual_delta_1"] for r in product_rows],
            ),
            "imbalance_l1_predicts_h5_delta_corr": corr(
                [r["imbalance_l1"] for r in product_rows],
                [r["future_residual_delta_5"] for r in product_rows],
            ),
        }
    return out


def cross_product_metrics(rows: list[dict]) -> dict:
    by_dt_product = {(r["day"], r["timestamp"], r["product"]): r for r in rows}
    panel = []
    for day in sorted({r["day"] for r in rows}):
        timestamps = sorted({r["timestamp"] for r in rows if r["day"] == day})
        for timestamp in timestamps:
            ipr = by_dt_product.get((day, timestamp, IPR))
            aco = by_dt_product.get((day, timestamp, ACO))
            if not ipr or not aco:
                continue
            panel.append({"day": day, "timestamp": timestamp, "ipr": ipr, "aco": aco})

    same_time = {}
    pairs = [
        ("residual", "residual"),
        ("mid_delta", "mid_delta"),
        ("spread", "spread"),
        ("imbalance_l1", "imbalance_l1"),
        ("total_depth", "total_depth"),
        ("one_sided", "one_sided"),
    ]
    for left, right in pairs:
        same_time[f"ipr_{left}__aco_{right}"] = corr(
            [p["ipr"][left] for p in panel],
            [float(p["aco"][right]) if isinstance(p["aco"][right], bool) else p["aco"][right] for p in panel],
        )

    lag_results = {}
    for feature in ("residual", "mid_delta", "spread", "imbalance_l1"):
        lag_results[feature] = {}
        for lag in (-10, -5, -2, -1, 0, 1, 2, 5, 10):
            xs = []
            ys = []
            for day in sorted({p["day"] for p in panel}):
                day_panel = [p for p in panel if p["day"] == day]
                for idx, point in enumerate(day_panel):
                    target_idx = idx + lag
                    if 0 <= target_idx < len(day_panel):
                        xs.append(point["ipr"][feature])
                        ys.append(day_panel[target_idx]["aco"][feature])
            lag_results[feature][f"ipr_t_to_aco_t_plus_{lag}"] = corr(xs, ys)

    strongest = {}
    for feature, values in lag_results.items():
        available = [(lag, val) for lag, val in values.items() if val is not None]
        strongest[feature] = max(available, key=lambda item: abs(item[1])) if available else None
    return {"panel_rows": len(panel), "same_time_correlations": same_time, "lag_correlations": lag_results, "strongest_lags": strongest}


def main() -> None:
    price_rows = add_features(load_prices())
    trade_rows = load_trades()
    metrics = {
        "source_files": sorted(path.name for path in RAW_DIR.glob("*.csv")),
        "data_quality": data_quality(price_rows, trade_rows),
        "transformations": transformation_metrics(price_rows),
        "markov": markov_metrics(price_rows),
        "light_models": light_model_metrics(price_rows),
        "pca": pca_metrics(price_rows),
        "microstructure": microstructure_metrics(price_rows),
        "cross_product": cross_product_metrics(price_rows),
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(round_value(metrics), indent=2, sort_keys=True) + "\n")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
