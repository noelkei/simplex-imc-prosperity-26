"""Advanced Round 1 signal research.

This script evaluates lightweight, implementable signals without using known
sample length, time-to-end, or end-of-sample liquidation assumptions.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
ROUND_DIR = ROOT / "rounds" / "round_1"
RAW_DIR = ROUND_DIR / "data" / "raw"
OUT_JSON = ROUND_DIR / "data" / "processed" / "advanced_signal_research_metrics.json"
OUT_MD = ROUND_DIR / "workspace" / "01_eda" / "eda_advanced_signal_research.md"

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
PRODUCTS = (IPR, ACO)
IPR_SLOPE = 0.001
ACO_FV = 10000.0


def to_int(value):
    if value in (None, ""):
        return None
    return int(float(value))


def to_float(value):
    if value in (None, ""):
        return None
    return float(value)


def sign(value, eps=1e-9):
    if value is None:
        return 0
    if value > eps:
        return 1
    if value < -eps:
        return -1
    return 0


def mean(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def std(values):
    values = [v for v in values if v is not None]
    if len(values) < 2:
        return None
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / (len(values) - 1))


def corr(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    xvals = [p[0] for p in pairs]
    yvals = [p[1] for p in pairs]
    mx = mean(xvals)
    my = mean(yvals)
    sx = std(xvals)
    sy = std(yvals)
    if not sx or not sy:
        return None
    return sum((x - mx) * (y - my) for x, y in pairs) / ((len(pairs) - 1) * sx * sy)


def quantile(values, q):
    values = sorted(v for v in values if v is not None)
    if not values:
        return None
    idx = (len(values) - 1) * q
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - idx) + values[hi] * (idx - lo)


def round_num(value, digits=6):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, digits)
    if isinstance(value, list):
        return [round_num(v, digits) for v in value]
    if isinstance(value, dict):
        return {k: round_num(v, digits) for k, v in value.items()}
    return value


def load_prices():
    rows = []
    by_product_day = {product: defaultdict(list) for product in PRODUCTS}
    quality = {product: {"rows": 0, "valid_mid": 0, "zero_mid": 0, "both_sided": 0, "one_sided": 0} for product in PRODUCTS}
    for path in sorted(RAW_DIR.glob("prices_round_1_day_*.csv")):
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                product = row["product"]
                if product not in PRODUCTS:
                    continue
                parsed = {
                    "day": to_int(row["day"]),
                    "timestamp": to_int(row["timestamp"]),
                    "product": product,
                    "mid": to_float(row["mid_price"]),
                    "bid": to_int(row["bid_price_1"]),
                    "ask": to_int(row["ask_price_1"]),
                    "bid_vol": to_int(row["bid_volume_1"]),
                    "ask_vol": to_int(row["ask_volume_1"]),
                    "bid2": to_int(row["bid_price_2"]),
                    "ask2": to_int(row["ask_price_2"]),
                    "bid3": to_int(row["bid_price_3"]),
                    "ask3": to_int(row["ask_price_3"]),
                    "bid_vol2": to_int(row["bid_volume_2"]),
                    "ask_vol2": to_int(row["ask_volume_2"]),
                    "bid_vol3": to_int(row["bid_volume_3"]),
                    "ask_vol3": to_int(row["ask_volume_3"]),
                }
                q = quality[product]
                q["rows"] += 1
                if parsed["mid"] not in (None, 0):
                    q["valid_mid"] += 1
                else:
                    q["zero_mid"] += 1
                has_bid = parsed["bid"] is not None
                has_ask = parsed["ask"] is not None
                if has_bid and has_ask:
                    q["both_sided"] += 1
                elif has_bid or has_ask:
                    q["one_sided"] += 1
                rows.append(parsed)
                by_product_day[product][parsed["day"]].append(parsed)

    for product in PRODUCTS:
        for day in by_product_day[product]:
            by_product_day[product][day].sort(key=lambda r: r["timestamp"])
    return rows, by_product_day, quality


def load_trades():
    trades = []
    for path in sorted(RAW_DIR.glob("trades_round_1_day_*.csv")):
        day = int(path.stem.split("_")[-1])
        with path.open(newline="") as handle:
            reader = csv.DictReader(handle, delimiter=";")
            for row in reader:
                symbol = row["symbol"]
                if symbol not in PRODUCTS:
                    continue
                trades.append(
                    {
                        "day": day,
                        "timestamp": to_int(row["timestamp"]),
                        "product": symbol,
                        "price": to_float(row["price"]),
                        "quantity": to_int(row["quantity"]) or 0,
                    }
                )
    return trades


def attach_features(by_product_day):
    for product, days in by_product_day.items():
        for day, rows in days.items():
            first_mid = next((r["mid"] for r in rows if r["mid"] not in (None, 0)), None)
            ipr_anchor = first_mid - IPR_SLOPE * rows[0]["timestamp"] if first_mid is not None else None
            residuals = []
            deltas = []
            for idx, row in enumerate(rows):
                if product == IPR:
                    fv = ipr_anchor + IPR_SLOPE * row["timestamp"] if ipr_anchor is not None else None
                else:
                    fv = ACO_FV
                row["fv"] = fv
                row["residual"] = row["mid"] - fv if row["mid"] not in (None, 0) and fv is not None else None
                bid = row["bid"]
                ask = row["ask"]
                bid_vol = row["bid_vol"] or 0
                ask_vol = row["ask_vol"] or 0
                if bid is not None and ask is not None:
                    row["spread"] = ask - bid
                    if bid_vol + ask_vol > 0:
                        row["microprice"] = (ask * bid_vol + bid * ask_vol) / (bid_vol + ask_vol)
                    else:
                        row["microprice"] = None
                else:
                    row["spread"] = None
                    row["microprice"] = None
                depth_bid = sum(v or 0 for v in (row["bid_vol"], row["bid_vol2"], row["bid_vol3"]))
                depth_ask = sum(v or 0 for v in (row["ask_vol"], row["ask_vol2"], row["ask_vol3"]))
                row["depth"] = depth_bid + depth_ask
                row["imbalance_l1"] = (bid_vol - ask_vol) / (bid_vol + ask_vol) if bid_vol + ask_vol > 0 else None
                row["imbalance_l3"] = (depth_bid - depth_ask) / (depth_bid + depth_ask) if depth_bid + depth_ask > 0 else None
                row["micro_offset"] = row["microprice"] - row["mid"] if row["microprice"] is not None and row["mid"] not in (None, 0) else None
                row["buy_edge"] = fv - ask if fv is not None and ask is not None else None
                row["sell_edge"] = bid - fv if fv is not None and bid is not None else None

                prev_res = residuals[-1] if residuals else None
                if row["residual"] is not None and prev_res is not None:
                    deltas.append(row["residual"] - prev_res)
                residuals.append(row["residual"])

                past = [r for r in residuals[:-1] if r is not None]
                for window in (50, 200):
                    sample = past[-window:]
                    m = mean(sample)
                    s = std(sample)
                    row[f"z_{window}"] = (row["residual"] - m) / s if row["residual"] is not None and m is not None and s else None
                past_deltas = deltas[-50:]
                row["vol_50"] = std(past_deltas)

            for idx, row in enumerate(rows):
                for h in (1, 5, 10):
                    if idx + h < len(rows):
                        nxt = rows[idx + h]["residual"]
                        row[f"future_delta_{h}"] = nxt - row["residual"] if nxt is not None and row["residual"] is not None else None
                        row[f"future_mid_delta_{h}"] = rows[idx + h]["mid"] - row["mid"] if rows[idx + h]["mid"] not in (None, 0) and row["mid"] not in (None, 0) else None
                    else:
                        row[f"future_delta_{h}"] = None
                        row[f"future_mid_delta_{h}"] = None


def directional_metric(rows, feature, target="future_delta_1"):
    xs = [r.get(feature) for r in rows]
    ys = [r.get(target) for r in rows]
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None and sign(x) != 0 and sign(y) != 0]
    if not pairs:
        return {"n": 0, "corr": corr(xs, ys), "sign_accuracy": None}
    acc = sum(1 for x, y in pairs if sign(x) == sign(y)) / len(pairs)
    return {"n": len(pairs), "corr": corr(xs, ys), "sign_accuracy": acc}


def reversion_metric(rows, feature, thresholds, target="future_delta_5"):
    out = {}
    for threshold in thresholds:
        selected = [r for r in rows if r.get(feature) is not None and abs(r[feature]) >= threshold and r.get(target) is not None]
        if selected:
            hits = sum(1 for r in selected if sign(r[feature]) == -sign(r[target]) and sign(r[target]) != 0)
            out[str(threshold)] = {
                "n": len(selected),
                "hit_rate": hits / len(selected),
                "mean_future_delta": mean([r[target] for r in selected]),
                "mean_abs_future_delta": mean([abs(r[target]) for r in selected]),
            }
        else:
            out[str(threshold)] = {"n": 0, "hit_rate": None, "mean_future_delta": None, "mean_abs_future_delta": None}
    return out


def taker_opportunities(rows, thresholds, horizon=5):
    out = {}
    for threshold in thresholds:
        buys = [r for r in rows if r.get("buy_edge") is not None and r["buy_edge"] >= threshold and r.get(f"future_mid_delta_{horizon}") is not None]
        sells = [r for r in rows if r.get("sell_edge") is not None and r["sell_edge"] >= threshold and r.get(f"future_mid_delta_{horizon}") is not None]
        buy_markout = [(r["mid"] + r[f"future_mid_delta_{horizon}"]) - r["ask"] for r in buys]
        sell_markout = [r["bid"] - (r["mid"] + r[f"future_mid_delta_{horizon}"]) for r in sells]
        out[str(threshold)] = {
            "buy_n": len(buys),
            "buy_mean_edge": mean([r["buy_edge"] for r in buys]),
            "buy_mean_markout_h5": mean(buy_markout),
            "sell_n": len(sells),
            "sell_mean_edge": mean([r["sell_edge"] for r in sells]),
            "sell_mean_markout_h5": mean(sell_markout),
        }
    return out


def ou_metrics(by_product_day):
    out = {}
    for product, days in by_product_day.items():
        out[product] = {}
        for day, rows in days.items():
            pairs = [(r["residual"], rows[idx + 1]["residual"]) for idx, r in enumerate(rows[:-1]) if r.get("residual") is not None and rows[idx + 1].get("residual") is not None]
            if len(pairs) < 10:
                continue
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            mx = mean(xs)
            my = mean(ys)
            denom = sum((x - mx) ** 2 for x in xs)
            phi = sum((x - mx) * (y - my) for x, y in pairs) / denom if denom else None
            half_life = -math.log(2) / math.log(phi) if phi and 0 < phi < 1 else None
            out[product][str(day)] = {"phi": phi, "half_life_obs": half_life, "residual_std": std(xs)}
    return out


def cusum_metrics(rows, thresholds):
    out = {}
    deltas = [r.get("future_delta_1") for r in rows]
    for threshold in thresholds:
        pos = 0.0
        neg = 0.0
        events = []
        for idx, d in enumerate(deltas):
            if d is None:
                continue
            pos = max(0.0, pos + d)
            neg = min(0.0, neg + d)
            if pos >= threshold:
                if rows[idx].get("future_delta_5") is not None:
                    events.append(("pos", rows[idx]["future_delta_5"]))
                pos = 0.0
            if neg <= -threshold:
                if rows[idx].get("future_delta_5") is not None:
                    events.append(("neg", rows[idx]["future_delta_5"]))
                neg = 0.0
        if events:
            reversal_hits = sum(1 for side, future in events if (side == "pos" and future < 0) or (side == "neg" and future > 0))
            out[str(threshold)] = {"n": len(events), "reversal_hit_rate_h5": reversal_hits / len(events), "mean_abs_follow_delta_h5": mean([abs(e[1]) for e in events])}
        else:
            out[str(threshold)] = {"n": 0, "reversal_hit_rate_h5": None, "mean_abs_follow_delta_h5": None}
    return out


def spread_vol_regimes(rows):
    spreads = [r.get("spread") for r in rows if r.get("spread") is not None]
    vols = [r.get("vol_50") for r in rows if r.get("vol_50") is not None]
    sq1 = quantile(spreads, 1 / 3)
    sq2 = quantile(spreads, 2 / 3)
    vq1 = quantile(vols, 1 / 3)
    vq2 = quantile(vols, 2 / 3)
    out = {"spread_thresholds": [sq1, sq2], "vol_thresholds": [vq1, vq2], "spread": {}, "vol": {}}
    for name, pred in {
        "low": lambda r: r.get("spread") is not None and r["spread"] <= sq1,
        "mid": lambda r: r.get("spread") is not None and sq1 < r["spread"] <= sq2,
        "high": lambda r: r.get("spread") is not None and r["spread"] > sq2,
    }.items():
        sel = [r for r in rows if pred(r)]
        out["spread"][name] = {
            "n": len(sel),
            "mean_abs_future_delta_5": mean([abs(r.get("future_delta_5")) for r in sel if r.get("future_delta_5") is not None]),
            "mean_buy_edge": mean([r.get("buy_edge") for r in sel]),
            "mean_sell_edge": mean([r.get("sell_edge") for r in sel]),
        }
    for name, pred in {
        "low": lambda r: r.get("vol_50") is not None and r["vol_50"] <= vq1,
        "mid": lambda r: r.get("vol_50") is not None and vq1 < r["vol_50"] <= vq2,
        "high": lambda r: r.get("vol_50") is not None and r["vol_50"] > vq2,
    }.items():
        sel = [r for r in rows if pred(r)]
        out["vol"][name] = {
            "n": len(sel),
            "mean_abs_future_delta_5": mean([abs(r.get("future_delta_5")) for r in sel if r.get("future_delta_5") is not None]),
            "mean_abs_residual": mean([abs(r.get("residual")) for r in sel]),
        }
    return out


def interaction_metrics(rows):
    out = {}
    for res_th in (5, 8, 10):
        for imb_th in (0.2, 0.4):
            name = f"res{res_th}_imb{imb_th}"
            selected = []
            for r in rows:
                residual = r.get("residual")
                imb = r.get("imbalance_l1")
                target = r.get("future_delta_5")
                if residual is None or imb is None or target is None:
                    continue
                if residual <= -res_th and imb >= imb_th:
                    selected.append((1, target))
                elif residual >= res_th and imb <= -imb_th:
                    selected.append((-1, target))
            if selected:
                hits = sum(1 for expected, target in selected if sign(target) == expected)
                out[name] = {"n": len(selected), "hit_rate": hits / len(selected), "mean_abs_future_delta_5": mean([abs(v[1]) for v in selected])}
            else:
                out[name] = {"n": 0, "hit_rate": None, "mean_abs_future_delta_5": None}
    return out


def trade_flow_metrics(by_product_day, trades):
    lookup = {}
    for product, days in by_product_day.items():
        for day, rows in days.items():
            lookup[(day, product)] = {r["timestamp"]: r for r in rows}
    buckets = defaultdict(lambda: {"signed_qty": 0, "qty": 0, "future": []})
    for trade in trades:
        row = lookup.get((trade["day"], trade["product"]), {}).get(trade["timestamp"])
        if row is None or row.get("mid") in (None, 0) or row.get("future_delta_5") is None:
            continue
        s = sign(trade["price"] - row["mid"], eps=0.25)
        buckets[trade["product"]]["signed_qty"] += s * trade["quantity"]
        buckets[trade["product"]]["qty"] += trade["quantity"]
        buckets[trade["product"]]["future"].append((s * trade["quantity"], row["future_delta_5"]))
    out = {}
    for product, item in buckets.items():
        xs = [p[0] for p in item["future"]]
        ys = [p[1] for p in item["future"]]
        pairs = [(x, y) for x, y in zip(xs, ys) if x != 0 and y is not None and sign(y) != 0]
        acc = sum(1 for x, y in pairs if sign(x) == sign(y)) / len(pairs) if pairs else None
        out[product] = {
            "trade_rows_used": len(item["future"]),
            "signed_qty": item["signed_qty"],
            "total_qty": item["qty"],
            "corr_signed_qty_vs_future_delta_5": corr(xs, ys),
            "sign_accuracy": acc,
        }
    return out


def analyze():
    rows, by_product_day, quality = load_prices()
    trades = load_trades()
    attach_features(by_product_day)
    metrics = {"data_quality": quality, "products": {}, "ou": ou_metrics(by_product_day), "trade_flow": trade_flow_metrics(by_product_day, trades)}
    for product in PRODUCTS:
        product_rows = []
        for day_rows in by_product_day[product].values():
            product_rows.extend(day_rows)
        product_rows = [r for r in product_rows if r.get("residual") is not None]
        metrics["products"][product] = {
            "microprice": directional_metric(product_rows, "micro_offset", "future_delta_1"),
            "imbalance_l1": directional_metric(product_rows, "imbalance_l1", "future_delta_1"),
            "imbalance_l3": directional_metric(product_rows, "imbalance_l3", "future_delta_1"),
            "residual_reversion": reversion_metric(product_rows, "residual", [2, 5, 8, 10], "future_delta_5"),
            "z50_reversion": reversion_metric(product_rows, "z_50", [1.0, 1.5, 2.0], "future_delta_5"),
            "z200_reversion": reversion_metric(product_rows, "z_200", [1.0, 1.5, 2.0], "future_delta_5"),
            "cusum": cusum_metrics(product_rows, [6, 10, 14]),
            "taker_opportunities": taker_opportunities(product_rows, [0, 2, 5, 8, 10], horizon=5),
            "spread_vol_regimes": spread_vol_regimes(product_rows),
            "interactions": interaction_metrics(product_rows),
        }
    return metrics


def verdicts(metrics):
    out = []
    for product in PRODUCTS:
        p = metrics["products"][product]
        out.append((product, "microprice + imbalance", "medium" if product == ACO else "weak-medium", f"micro corr {p['microprice']['corr']:.3f} / imbalance corr {p['imbalance_l1']['corr']:.3f}" if p["microprice"]["corr"] is not None and p["imbalance_l1"]["corr"] is not None else "insufficient"))
        best_z = max(p["z50_reversion"].items(), key=lambda kv: kv[1]["hit_rate"] or 0)
        out.append((product, "residual z-score", "strong" if best_z[1]["hit_rate"] and best_z[1]["hit_rate"] > 0.70 else "medium", f"best z50 threshold {best_z[0]} hit {best_z[1]['hit_rate']} n {best_z[1]['n']}"))
        ou_phi = mean([v["phi"] for v in metrics["ou"][product].values()])
        out.append((product, "OU / half-life", "medium" if ou_phi and 0 < ou_phi < 0.9 else "weak", f"mean phi {ou_phi}"))
        tf = metrics["trade_flow"].get(product, {})
        out.append((product, "trade flow pressure", "weak" if not tf.get("sign_accuracy") or tf["sign_accuracy"] < 0.58 else "medium", f"sign acc {tf.get('sign_accuracy')} n {tf.get('trade_rows_used')}"))
    return out


def write_markdown(metrics):
    lines = []
    lines.append("# EDA Advanced Signal Research")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Which lightweight high-edge directions are promising for Round 1 without using known sample length, time-to-end, or end-of-sample liquidation behavior?")
    lines.append("")
    lines.append("## Data Sources")
    lines.append("")
    lines.append("- Raw prices: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`")
    lines.append("- Raw trades: `rounds/round_1/data/raw/trades_round_1_day_{-2,-1,0}.csv`")
    lines.append("- Output metrics: `rounds/round_1/data/processed/advanced_signal_research_metrics.json`")
    lines.append("")
    lines.append("## Data Quality")
    lines.append("")
    lines.append("| Product | Rows | Valid Mid | Zero Mid | Both-Sided | One-Sided |")
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for product in PRODUCTS:
        q = metrics["data_quality"][product]
        lines.append(f"| `{product}` | {q['rows']} | {q['valid_mid']} | {q['zero_mid']} | {q['both_sided']} | {q['one_sided']} |")
    lines.append("")
    lines.append("## Signal Verdicts")
    lines.append("")
    lines.append("| Product | Direction | Verdict | Evidence Note |")
    lines.append("| --- | --- | --- | --- |")
    for product, direction, verdict, note in verdicts(metrics):
        lines.append(f"| `{product}` | {direction} | {verdict} | {note} |")
    lines.append("")
    lines.append("## Product Details")
    lines.append("")
    for product in PRODUCTS:
        p = metrics["products"][product]
        lines.append(f"### `{product}`")
        lines.append("")
        lines.append("| Check | Result | Use |")
        lines.append("| --- | --- | --- |")
        lines.append(f"| Microprice offset | corr `{round_num(p['microprice']['corr'], 4)}`, sign `{round_num(p['microprice']['sign_accuracy'], 4)}`, n `{p['microprice']['n']}` | execution overlay only |")
        lines.append(f"| L1 imbalance | corr `{round_num(p['imbalance_l1']['corr'], 4)}`, sign `{round_num(p['imbalance_l1']['sign_accuracy'], 4)}`, n `{p['imbalance_l1']['n']}` | quote skew / gate |")
        best_res = max(p["residual_reversion"].items(), key=lambda kv: kv[1]["hit_rate"] or 0)
        best_z = max(p["z50_reversion"].items(), key=lambda kv: kv[1]["hit_rate"] or 0)
        lines.append(f"| Residual reversion | best threshold `{best_res[0]}`, hit `{round_num(best_res[1]['hit_rate'], 4)}`, n `{best_res[1]['n']}` | FV mean-reversion / taker gate |")
        lines.append(f"| Rolling z-score | best z50 threshold `{best_z[0]}`, hit `{round_num(best_z[1]['hit_rate'], 4)}`, n `{best_z[1]['n']}` | normalize entries; do not use as standalone model |")
        ou_vals = metrics["ou"][product]
        half_life = mean([v["half_life_obs"] for v in ou_vals.values()])
        phi = mean([v["phi"] for v in ou_vals.values()])
        lines.append(f"| OU half-life | mean phi `{round_num(phi, 4)}`, mean half-life obs `{round_num(half_life, 4)}` | short local horizon only; beware bid-ask bounce |")
        tf = metrics["trade_flow"].get(product, {})
        lines.append(f"| Trade pressure proxy | sign `{round_num(tf.get('sign_accuracy'), 4)}`, corr `{round_num(tf.get('corr_signed_qty_vs_future_delta_5'), 4)}`, rows `{tf.get('trade_rows_used')}` | weak unless paired with book state |")
        for th, vals in p["taker_opportunities"].items():
            if th in ("5", "8"):
                lines.append(f"| Taker edge >= {th} | buy n `{vals['buy_n']}`, buy markout `{round_num(vals['buy_mean_markout_h5'], 4)}`, sell n `{vals['sell_n']}`, sell markout `{round_num(vals['sell_mean_markout_h5'], 4)}` | high-confidence sweep when capacity allows |")
        lines.append("")
    lines.append("## Downstream Use")
    lines.append("")
    lines.append("- Strong enough to use: IPR +80 carry, ACO fixed-FV two-sided market making, ACO residual/z-score gates, inventory skew, and quote-quality filtering.")
    lines.append("- Use as overlays: microprice, imbalance, one-sided-book handling, volatility/spread regimes, and CUSUM as a defensive guard.")
    lines.append("- Weak or not standalone: trade-flow proxy, PCA-only, end-of-sample liquidation, and broad HMM/controller complexity.")
    lines.append("")
    lines.append("## Caveats")
    lines.append("")
    lines.append("- All horizons are local product-observation horizons; no feature uses known sample length or time remaining.")
    lines.append("- Sample data supports strategy selection, not official rules.")
    lines.append("- Passive maker fill quality is better judged from platform logs than CSV-only replay.")
    return "\n".join(lines) + "\n"


def main():
    metrics = analyze()
    OUT_JSON.write_text(json.dumps(round_num(metrics), indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text(write_markdown(metrics))
    print(json.dumps(round_num({"products": metrics["products"], "trade_flow": metrics["trade_flow"], "ou": metrics["ou"]}), indent=2, sort_keys=True)[:8000])
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
