"""Analyze Round 1 platform JSON/log artifacts.

This script does not simulate the exchange. It normalizes platform-style JSON
and log files already present in the repository, compares PnL calculation
methods, and extracts run-level signals that can guide bot iteration.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
ROUND_DIR = ROOT / "rounds" / "round_1"
BOTS_DIR = ROUND_DIR / "bots"
PERF_DIR = ROUND_DIR / "performances"
OUT_JSON = PERF_DIR / "noel" / "canonical" / "run_20260417_platform_artifact_analysis.json"
OUT_MD = PERF_DIR / "noel" / "canonical" / "run_20260417_platform_artifact_analysis.md"

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
PRODUCTS = (IPR, ACO)
XIRECS = "XIRECS"


def read_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def to_float(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except Exception:
        return None


def to_int(value):
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except Exception:
        return None


def round_num(value, digits=6):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return round(value, digits)
    if isinstance(value, dict):
        return {k: round_num(v, digits) for k, v in value.items()}
    if isinstance(value, list):
        return [round_num(v, digits) for v in value]
    return value


def parse_semicolon_csv(text: str) -> list[dict]:
    if not text:
        return []
    return list(csv.DictReader(io.StringIO(text), delimiter=";"))


def parse_activities(text: str):
    rows = parse_semicolon_csv(text)
    by_product = {product: [] for product in PRODUCTS}
    by_timestamp: dict[int, dict[str, float]] = defaultdict(dict)
    for row in rows:
        product = row.get("product")
        if product not in PRODUCTS:
            continue
        timestamp = to_int(row.get("timestamp"))
        parsed = {
            "day": to_int(row.get("day")),
            "timestamp": timestamp,
            "product": product,
            "mid_price": to_float(row.get("mid_price")),
            "profit_and_loss": to_float(row.get("profit_and_loss")),
            "bid_price_1": to_float(row.get("bid_price_1")),
            "ask_price_1": to_float(row.get("ask_price_1")),
        }
        by_product[product].append(parsed)
        if timestamp is not None and parsed["profit_and_loss"] is not None:
            by_timestamp[timestamp][product] = parsed["profit_and_loss"]
    last_by_product = {}
    for product, product_rows in by_product.items():
        if product_rows:
            last_by_product[product] = product_rows[-1]
    pnl_curve = []
    for timestamp in sorted(by_timestamp):
        values = by_timestamp[timestamp]
        if all(product in values for product in PRODUCTS):
            pnl_curve.append({"timestamp": timestamp, "value": sum(values[p] for p in PRODUCTS)})
    return {
        "rows": rows,
        "by_product": by_product,
        "last_by_product": last_by_product,
        "pnl_curve": pnl_curve,
    }


def parse_graph(text: str):
    rows = parse_semicolon_csv(text)
    parsed = []
    for row in rows:
        timestamp = to_int(row.get("timestamp"))
        value = to_float(row.get("value"))
        if timestamp is not None and value is not None:
            parsed.append({"timestamp": timestamp, "value": value})
    return parsed


def drawdown(curve: list[dict]) -> dict:
    if not curve:
        return {"max_drawdown": None, "min_pnl": None, "max_pnl": None, "final_pnl": None}
    peak = curve[0]["value"]
    max_dd = 0.0
    min_pnl = curve[0]["value"]
    max_pnl = curve[0]["value"]
    min_time = curve[0]["timestamp"]
    max_time = curve[0]["timestamp"]
    max_dd_time = curve[0]["timestamp"]
    for point in curve:
        value = point["value"]
        if value > peak:
            peak = value
        dd = peak - value
        if dd > max_dd:
            max_dd = dd
            max_dd_time = point["timestamp"]
        if value < min_pnl:
            min_pnl = value
            min_time = point["timestamp"]
        if value > max_pnl:
            max_pnl = value
            max_time = point["timestamp"]
    return {
        "max_drawdown": max_dd,
        "max_drawdown_time": max_dd_time,
        "min_pnl": min_pnl,
        "min_pnl_time": min_time,
        "max_pnl": max_pnl,
        "max_pnl_time": max_time,
        "final_pnl": curve[-1]["value"],
    }


def positions_map(positions):
    out = {}
    if isinstance(positions, list):
        for item in positions:
            symbol = item.get("symbol")
            qty = item.get("quantity")
            if symbol is not None:
                out[symbol] = qty
    return out


def trade_stats(trades: list[dict], final_mid: dict[str, float | None]):
    stats = {}
    own_trades = []
    market_trades = []
    pos_by_product = {product: 0 for product in PRODUCTS}
    pos_curve = {product: [] for product in PRODUCTS}
    cash_by_product = {product: 0.0 for product in PRODUCTS}
    for trade in sorted(trades, key=lambda t: (t.get("timestamp", 0), t.get("symbol", ""))):
        symbol = trade.get("symbol")
        if symbol not in PRODUCTS:
            continue
        buyer = trade.get("buyer")
        seller = trade.get("seller")
        price = to_float(trade.get("price"))
        qty = to_int(trade.get("quantity")) or 0
        timestamp = to_int(trade.get("timestamp"))
        if buyer == "SUBMISSION":
            side = "buy"
            signed_qty = qty
            cash_delta = -qty * price
        elif seller == "SUBMISSION":
            side = "sell"
            signed_qty = -qty
            cash_delta = qty * price
        else:
            market_trades.append(trade)
            continue
        own_trades.append({**trade, "side": side, "signed_qty": signed_qty})
        pos_by_product[symbol] += signed_qty
        cash_by_product[symbol] += cash_delta
        pos_curve[symbol].append({"timestamp": timestamp, "position": pos_by_product[symbol]})

    for product in PRODUCTS:
        product_trades = [t for t in own_trades if t.get("symbol") == product]
        buys = [t for t in product_trades if t["side"] == "buy"]
        sells = [t for t in product_trades if t["side"] == "sell"]
        buy_qty = sum(to_int(t.get("quantity")) or 0 for t in buys)
        sell_qty = sum(to_int(t.get("quantity")) or 0 for t in sells)
        buy_notional = sum((to_float(t.get("price")) or 0) * (to_int(t.get("quantity")) or 0) for t in buys)
        sell_notional = sum((to_float(t.get("price")) or 0) * (to_int(t.get("quantity")) or 0) for t in sells)
        avg_buy = buy_notional / buy_qty if buy_qty else None
        avg_sell = sell_notional / sell_qty if sell_qty else None
        matched_qty = min(buy_qty, sell_qty)
        gross_spread_capture = (avg_sell - avg_buy) * matched_qty if avg_buy is not None and avg_sell is not None else None
        mark = final_mid.get(product)
        reconstructed_pnl = cash_by_product[product] + pos_by_product[product] * mark if mark is not None else None
        curve = pos_curve[product]
        max_abs_pos = max((abs(p["position"]) for p in curve), default=0)
        first_nonzero = next((p["timestamp"] for p in curve if p["position"] != 0), None)
        first_abs_75 = next((p["timestamp"] for p in curve if abs(p["position"]) >= 75), None)
        first_abs_80 = next((p["timestamp"] for p in curve if abs(p["position"]) >= 80), None)
        stats[product] = {
            "own_trade_count": len(product_trades),
            "buy_qty": buy_qty,
            "sell_qty": sell_qty,
            "net_qty": buy_qty - sell_qty,
            "avg_buy": avg_buy,
            "avg_sell": avg_sell,
            "matched_qty": matched_qty,
            "gross_spread_capture": gross_spread_capture,
            "cash": cash_by_product[product],
            "reconstructed_pnl": reconstructed_pnl,
            "max_abs_position_from_own_trades": max_abs_pos,
            "first_nonzero_position_ts": first_nonzero,
            "first_abs_75_ts": first_abs_75,
            "first_abs_80_ts": first_abs_80,
        }
    return {
        "own_trade_count": len(own_trades),
        "market_trade_count": len(market_trades),
        "by_product": stats,
    }


def find_artifacts():
    candidates = []
    for path in sorted(PERF_DIR.glob("**/*.json")) + sorted(BOTS_DIR.glob("**/*.json")):
        if path.name.startswith("run_"):
            continue
        data = read_json(path)
        if not isinstance(data, dict):
            continue
        if not {"profit", "activitiesLog", "positions"}.issubset(data.keys()):
            continue
        candidates.append(path)
    return candidates


def infer_member_bucket(path: Path):
    parts = path.relative_to(ROUND_DIR).parts
    if parts[0] in ("bots", "performances") and len(parts) >= 4:
        return parts[1], parts[2]
    return "unknown", "unknown"


def find_bot_path(json_path: Path, member: str, bucket: str):
    stem = json_path.stem
    direct = BOTS_DIR / member / bucket / f"{stem}.py"
    if direct.exists():
        return direct
    matches = sorted(BOTS_DIR.glob(f"**/{stem}.py"))
    return matches[0] if matches else None


def find_log_path(json_path: Path, member: str, bucket: str):
    stem = json_path.stem
    direct = PERF_DIR / member / bucket / f"{stem}.log"
    if direct.exists():
        return direct
    matches = sorted(PERF_DIR.glob(f"**/{stem}.log"))
    return matches[0] if matches else None


def file_hash(path: Path | None):
    if path is None or not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def analyze_artifact(json_path: Path):
    data = read_json(json_path)
    member, bucket = infer_member_bucket(json_path)
    bot_path = find_bot_path(json_path, member, bucket)
    log_path = find_log_path(json_path, member, bucket)
    log_data = read_json(log_path) if log_path else None
    has_trade_log = isinstance(log_data, dict)

    activities = parse_activities(data.get("activitiesLog", ""))
    graph = parse_graph(data.get("graphLog", ""))
    final_mid = {
        product: activities["last_by_product"].get(product, {}).get("mid_price")
        for product in PRODUCTS
    }
    final_product_pnl = {
        product: activities["last_by_product"].get(product, {}).get("profit_and_loss")
        for product in PRODUCTS
    }
    product_sum = sum(v for v in final_product_pnl.values() if v is not None)
    graph_final = graph[-1]["value"] if graph else None
    official_profit = to_float(data.get("profit"))
    pos = positions_map(data.get("positions"))
    trade_history = log_data.get("tradeHistory", []) if isinstance(log_data, dict) else []
    logs = log_data.get("logs", []) if isinstance(log_data, dict) else []
    log_issue_count = 0
    for item in logs:
        if item.get("sandboxLog") or item.get("lambdaLog"):
            log_issue_count += 1
    tstats = trade_stats(trade_history, final_mid)
    reconstructed_sum = sum(
        v["reconstructed_pnl"]
        for v in tstats["by_product"].values()
        if v["reconstructed_pnl"] is not None
    ) if trade_history else None

    pnl_methods = {
        "official_profit": official_profit,
        "product_pnl_sum_from_activities": product_sum,
        "graph_final": graph_final,
        "trade_reconstruction_sum": reconstructed_sum,
        "product_sum_delta_vs_official": product_sum - official_profit if official_profit is not None else None,
        "graph_delta_vs_official": graph_final - official_profit if graph_final is not None and official_profit is not None else None,
        "trade_reconstruction_delta_vs_official": reconstructed_sum - official_profit if reconstructed_sum is not None and official_profit is not None else None,
    }

    return {
        "run_key": json_path.stem,
        "member": member,
        "bucket": bucket,
        "json_path": str(json_path.relative_to(ROOT)),
        "log_path": str(log_path.relative_to(ROOT)) if log_path else None,
        "has_trade_log": has_trade_log,
        "bot_path": str(bot_path.relative_to(ROOT)) if bot_path else None,
        "bot_hash": file_hash(bot_path),
        "submission_id": log_data.get("submissionId") if isinstance(log_data, dict) else None,
        "round": data.get("round"),
        "status": data.get("status"),
        "positions": pos,
        "final_mid": final_mid,
        "final_product_pnl": final_product_pnl,
        "pnl_methods": pnl_methods,
        "drawdown": drawdown(activities["pnl_curve"]),
        "activity_rows": len(activities["rows"]),
        "graph_rows": len(graph),
        "log_issue_count": log_issue_count,
        "trade_stats": tstats,
    }


def table_row(values):
    return "| " + " | ".join(values) + " |"


def fmt(value, digits=2):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def avg(values):
    values = [v for v in values if v is not None]
    return sum(values) / len(values) if values else None


def abs_max(values):
    values = [abs(v) for v in values if v is not None]
    return max(values) if values else None


def roundtrip_edge(stats):
    avg_buy = stats.get("avg_buy")
    avg_sell = stats.get("avg_sell")
    if avg_buy is None or avg_sell is None:
        return None
    return avg_sell - avg_buy


def build_insights(runs):
    ranked = sorted(runs, key=lambda r: r["pnl_methods"]["official_profit"], reverse=True)
    best = ranked[0] if ranked else None
    insights = []

    activity_deltas = [r["pnl_methods"]["product_sum_delta_vs_official"] for r in runs]
    graph_deltas = [r["pnl_methods"]["graph_delta_vs_official"] for r in runs]
    trade_deltas = [r["pnl_methods"]["trade_reconstruction_delta_vs_official"] for r in runs]
    max_activity_delta = abs_max(activity_deltas)
    max_graph_delta = abs_max(graph_deltas)
    max_trade_delta = abs_max(trade_deltas)
    if max_activity_delta == 0:
        insights.append(
            {
                "title": "ActivitiesLog gives the exact product PnL split",
                "detail": "The final per-product profit_and_loss rows sum to JSON profit with zero delta in every analyzed artifact.",
                "action": "Rank with JSON profit, then use the final activitiesLog rows for IPR/ACO attribution.",
            }
        )
    if max_graph_delta is not None or max_trade_delta is not None:
        insights.append(
            {
                "title": "Graph/trade rebuild are audit tools, not the score",
                "detail": f"Max absolute graph delta is {max_graph_delta:.2f}; max absolute tradeHistory rebuild delta is {max_trade_delta:.2f} where logs exist.",
                "action": "Do not rank bots by local reconstruction; use it only to catch obvious logging or inventory inconsistencies.",
            }
        )

    max_long = [r for r in runs if r["positions"].get(IPR) == 80]
    cap_75 = [r for r in runs if r["positions"].get(IPR) == 75]
    if max_long and cap_75:
        avg_max_long_ipr = sum(r["final_product_pnl"][IPR] for r in max_long) / len(max_long)
        avg_75_ipr = sum(r["final_product_pnl"][IPR] for r in cap_75) / len(cap_75)
        insights.append(
            {
                "title": "IPR max-long dominates lower caps",
                "detail": f"Runs ending at +80 IPR average {avg_max_long_ipr:.1f} IPR PnL; +75-cap runs average {avg_75_ipr:.1f}.",
                "action": "Keep IPR target at +80 unless live evidence shows drift failure.",
            }
        )

    aco_sorted = sorted(runs, key=lambda r: r["final_product_pnl"][ACO], reverse=True)
    if aco_sorted:
        top = aco_sorted[0]
        top_stats = top["trade_stats"]["by_product"][ACO]
        insights.append(
            {
                "title": "ACO is the main improvement surface after IPR carry",
                "detail": f"Best ACO run is {top['run_key']} with {top['final_product_pnl'][ACO]:.1f} ACO PnL, {top_stats['buy_qty']} buy qty, {top_stats['sell_qty']} sell qty.",
                "action": "Iterate ACO quote size/skew/passive fill behavior around FV=10000; keep IPR carry stable.",
            }
        )

    logged_aco = [r for r in runs if r["has_trade_log"] and r["trade_stats"]["by_product"][ACO]["matched_qty"]]
    if logged_aco:
        highest_volume = max(logged_aco, key=lambda r: r["trade_stats"]["by_product"][ACO]["matched_qty"])
        best_logged_aco = max(logged_aco, key=lambda r: r["final_product_pnl"][ACO])
        best_edge = roundtrip_edge(best_logged_aco["trade_stats"]["by_product"][ACO])
        volume_edge = roundtrip_edge(highest_volume["trade_stats"]["by_product"][ACO])
        insights.append(
            {
                "title": "ACO quality beats raw ACO volume",
                "detail": f"{best_logged_aco['run_key']} earns {best_logged_aco['final_product_pnl'][ACO]:.1f} ACO PnL at edge {best_edge:.2f}; {highest_volume['run_key']} trades more matched qty but edge is {volume_edge:.2f}.",
                "action": "Optimize quote selection and inventory skew before increasing size blindly.",
            }
        )

    markov = next((r for r in runs if r["run_key"] == "candidate_12_bot04_aco_markov"), None)
    hybrid = next((r for r in runs if r["run_key"] == "candidate_13_bot05_hybrid_adaptive"), None)
    if markov and hybrid:
        insights.append(
            {
                "title": "Model overlays are useful on ACO, harmful if they replace IPR carry",
                "detail": f"Markov/adaptive Noel variants show ACO PnL of {markov['final_product_pnl'][ACO]:.1f}/{hybrid['final_product_pnl'][ACO]:.1f}, but their IPR PnL stays below the +80 baseline.",
                "action": "Steal the ACO filters from bot 04/05 only after locking the IPR +80 base layer.",
            }
        )

    if best:
        best_aco_pos = best["positions"].get(ACO)
        if best_aco_pos == 0:
            insights.append(
                {
                    "title": "Flat ACO inventory finished best in the current artifact set",
                    "detail": f"The top run ends ACO at {best_aco_pos} while earning {best['final_product_pnl'][ACO]:.1f} ACO PnL.",
                    "action": "Add late-session inventory skew/flattening to ACO variants, but do not sacrifice good passive fills too early.",
                }
            )

    noel10 = next((r for r in runs if r["run_key"] == "candidate_10_bot02_carry_tight_mm"), None)
    if noel10:
        insights.append(
            {
                "title": "Current Noel canonical candidate crossed 10k on platform artifact",
                "detail": f"{noel10['run_key']} official profit is {noel10['pnl_methods']['official_profit']:.1f}: IPR {noel10['final_product_pnl'][IPR]:.1f}, ACO {noel10['final_product_pnl'][ACO]:.1f}.",
                "action": "Use this artifact as the primary ranking baseline, not the local replay scale.",
            }
        )

    low_micro = next((r for r in runs if r["run_key"] == "candidate_11_bot03_micro_scalper"), None)
    if low_micro:
        insights.append(
            {
                "title": "Pure microstructure underuses the dominant IPR carry",
                "detail": f"{low_micro['run_key']} official profit is {low_micro['pnl_methods']['official_profit']:.1f}, with only {low_micro['final_product_pnl'][IPR]:.1f} IPR PnL.",
                "action": "Do not promote microstructure-only bots unless they keep +80 IPR carry as a base layer.",
            }
        )

    return insights, best


def write_markdown(runs, insights, best):
    ranked = sorted(runs, key=lambda r: r["pnl_methods"]["official_profit"], reverse=True)
    lines = []
    lines.append("# Platform Artifact Analysis: Round 1")
    lines.append("")
    lines.append("## Run Metadata")
    lines.append("")
    lines.append("- Run ID: `run_20260417_platform_artifact_analysis`")
    lines.append("- Date: 2026-04-17")
    lines.append("- Round: `round_1`")
    lines.append("- Owner: `noel`")
    lines.append("- Raw output: `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.json`")
    lines.append("- Script: `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py`")
    lines.append("- Source artifacts: platform-style JSON/log files under `rounds/round_1/performances/` plus misfiled JSONs under `rounds/round_1/bots/`.")
    lines.append("")
    lines.append("## PnL Methodology")
    lines.append("")
    lines.append("Use this priority order before promoting a bot:")
    lines.append("")
    lines.append("1. `profit` from the platform-style JSON: authoritative run-level score for that artifact.")
    lines.append("2. Sum of the final per-product `profit_and_loss` values from `activitiesLog`: should match `profit`; use to split PnL by product.")
    lines.append("3. Final `graphLog` value: should match total PnL when present.")
    lines.append("4. Reconstruction from own `tradeHistory` plus final mid: useful audit, but only available when a matching log exists.")
    lines.append("5. Local replay: sanity/ranking heuristic only; not an official PnL estimator.")
    lines.append("")
    lines.append("## Official Ranking")
    lines.append("")
    lines.append(table_row(["Rank", "Run", "Member", "Bucket", "Official PnL", "IPR PnL", "ACO PnL", "Final IPR", "Final ACO", "Own Trades", "Max DD"]))
    lines.append(table_row(["---:", "---", "---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    for idx, run in enumerate(ranked, start=1):
        ts = run["trade_stats"]
        lines.append(
            table_row(
                [
                    str(idx),
                    f"`{run['run_key']}`",
                    run["member"],
                    run["bucket"],
                    fmt(run["pnl_methods"]["official_profit"]),
                    fmt(run["final_product_pnl"][IPR]),
                    fmt(run["final_product_pnl"][ACO]),
                    fmt(run["positions"].get(IPR), 0),
                    fmt(run["positions"].get(ACO), 0),
                    fmt(ts["own_trade_count"], 0) if run["has_trade_log"] else "-",
                    fmt(run["drawdown"]["max_drawdown"]),
                ]
            )
        )
    lines.append("")
    lines.append("## PnL Calculation Audit")
    lines.append("")
    lines.append(table_row(["Run", "Official", "Activities Sum", "Graph Final", "Trade Rebuild", "Activities Delta", "Graph Delta", "Trade Delta"]))
    lines.append(table_row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    for run in ranked:
        m = run["pnl_methods"]
        lines.append(
            table_row(
                [
                    f"`{run['run_key']}`",
                    fmt(m["official_profit"]),
                    fmt(m["product_pnl_sum_from_activities"]),
                    fmt(m["graph_final"]),
                    fmt(m["trade_reconstruction_sum"]),
                    fmt(m["product_sum_delta_vs_official"]),
                    fmt(m["graph_delta_vs_official"]),
                    fmt(m["trade_reconstruction_delta_vs_official"]),
                ]
            )
        )
    lines.append("")
    lines.append("## Intra-Run Trade Signals")
    lines.append("")
    lines.append(table_row(["Run", "Product", "Buy Qty", "Avg Buy", "Sell Qty", "Avg Sell", "Net Qty", "Gross Spread Capture", "First +75/+80"]))
    lines.append(table_row(["---", "---", "---:", "---:", "---:", "---:", "---:", "---:", "---"]))
    for run in ranked:
        for product in PRODUCTS:
            if not run["has_trade_log"]:
                lines.append(
                    table_row(
                        [
                            f"`{run['run_key']}`",
                            f"`{product}`",
                            "-",
                            "-",
                            "-",
                            "-",
                            "-",
                            "-",
                            "log missing",
                        ]
                    )
                )
                continue
            s = run["trade_stats"]["by_product"][product]
            first_pos = f"{fmt(s['first_abs_75_ts'], 0)}/{fmt(s['first_abs_80_ts'], 0)}"
            lines.append(
                table_row(
                    [
                        f"`{run['run_key']}`",
                        f"`{product}`",
                        fmt(s["buy_qty"], 0),
                        fmt(s["avg_buy"]),
                        fmt(s["sell_qty"], 0),
                        fmt(s["avg_sell"]),
                        fmt(s["net_qty"], 0),
                        fmt(s["gross_spread_capture"]),
                        first_pos,
                    ]
                )
            )
    lines.append("")
    lines.append("## Product Lever Evidence")
    lines.append("")
    lines.append("IPR evidence: the strongest runs make the IPR position decision simple and early.")
    lines.append("")
    lines.append(table_row(["Run", "IPR PnL", "Final IPR", "Buy Qty", "Sell Qty", "First +75/+80", "IPR Max Abs Pos"]))
    lines.append(table_row(["---", "---:", "---:", "---:", "---:", "---", "---:"]))
    for run in ranked:
        s = run["trade_stats"]["by_product"][IPR]
        if run["has_trade_log"]:
            first_pos = f"{fmt(s['first_abs_75_ts'], 0)}/{fmt(s['first_abs_80_ts'], 0)}"
            buy_qty = fmt(s["buy_qty"], 0)
            sell_qty = fmt(s["sell_qty"], 0)
            max_abs_pos = fmt(s["max_abs_position_from_own_trades"], 0)
        else:
            first_pos = "log missing"
            buy_qty = "-"
            sell_qty = "-"
            max_abs_pos = "-"
        lines.append(
            table_row(
                [
                    f"`{run['run_key']}`",
                    fmt(run["final_product_pnl"][IPR]),
                    fmt(run["positions"].get(IPR), 0),
                    buy_qty,
                    sell_qty,
                    first_pos,
                    max_abs_pos,
                ]
            )
        )
    lines.append("")
    lines.append("ACO evidence: this is where iteration can still move the total after IPR is locked.")
    lines.append("")
    lines.append(table_row(["Run", "ACO PnL", "Final ACO", "Matched Qty", "Edge", "Avg Buy", "Avg Sell", "ACO Max Abs Pos"]))
    lines.append(table_row(["---", "---:", "---:", "---:", "---:", "---:", "---:", "---:"]))
    for run in ranked:
        s = run["trade_stats"]["by_product"][ACO]
        if run["has_trade_log"]:
            matched_qty = fmt(s["matched_qty"], 0)
            edge = fmt(roundtrip_edge(s))
            avg_buy = fmt(s["avg_buy"])
            avg_sell = fmt(s["avg_sell"])
            max_abs_pos = fmt(s["max_abs_position_from_own_trades"], 0)
        else:
            matched_qty = "-"
            edge = "-"
            avg_buy = "-"
            avg_sell = "-"
            max_abs_pos = "-"
        lines.append(
            table_row(
                [
                    f"`{run['run_key']}`",
                    fmt(run["final_product_pnl"][ACO]),
                    fmt(run["positions"].get(ACO), 0),
                    matched_qty,
                    edge,
                    avg_buy,
                    avg_sell,
                    max_abs_pos,
                ]
            )
        )
    lines.append("")
    lines.append("## Actionable Insights")
    lines.append("")
    for insight in insights:
        lines.append(f"- **{insight['title']}**: {insight['detail']} Action: {insight['action']}")
    lines.append("")
    lines.append("## Best Current Evidence")
    lines.append("")
    if best:
        lines.append(f"- Best official artifact: `{best['run_key']}` with PnL `{best['pnl_methods']['official_profit']:.2f}`.")
        lines.append(f"- Bot path: `{best['bot_path']}`.")
        lines.append(f"- Product split: IPR `{best['final_product_pnl'][IPR]:.2f}`, ACO `{best['final_product_pnl'][ACO]:.2f}`.")
    lines.append("- The next strategy loop should optimize ACO around the current max-long IPR base, because IPR carry is already near solved in these artifacts.")
    lines.append("")
    lines.append("## Promotion Gate")
    lines.append("")
    lines.append("Before a bot is promoted for another platform attempt:")
    lines.append("")
    lines.append("- Save the exact `.py`, platform `.json`, and `.log` together, or mark missing logs as a caveat.")
    lines.append("- Rank by JSON `profit`; use final `activitiesLog` product PnL to explain the score.")
    lines.append("- Require `product_pnl_sum_from_activities` delta `0.0` versus JSON `profit`; otherwise treat the artifact as suspect.")
    lines.append("- Treat `graphLog` and trade reconstruction deltas as audit tolerances, not score sources.")
    lines.append("- Compare to the current bar: total `10007.0`, IPR `7286.0`, ACO `2721.0`.")
    lines.append("- Use local replay only for sanity checks: contract errors, position limits, and obvious fill behavior.")
    lines.append("")
    lines.append("## Iteration Backlog")
    lines.append("")
    lines.append("- `candidate_10 + ACO Markov filter`: preserve +80 IPR, borrow bot 04's ACO filter only when it improves edge without lowering matched volume too much.")
    lines.append("- `candidate_10 + ACO adaptive skew`: preserve FV=10000 base, but skew quotes away from accumulating stale ACO inventory late in the run.")
    lines.append("- `candidate_10 + edge threshold sweep`: test fewer but cleaner ACO fills; target higher average roundtrip edge than Amin 23/25.")
    lines.append("- `candidate_10 + late flatten`: keep passive ACO early, then reduce inventory risk near the end; current best finishes ACO flat.")
    lines.append("- `hybrid rescue`: only keep bot 05 ideas that do not give up the IPR +80 carry layer.")
    lines.append("")
    lines.append("## Interpretation Limits")
    lines.append("")
    lines.append("- These are platform-style execution artifacts, not official round rules.")
    lines.append("- Some artifacts are historical or misfiled; path location does not change their analytical value, but promotion should reference canonical performance summaries.")
    lines.append("- Trade reconstruction matches only when the matching `.log` exists and own trades are complete; use it as audit, not primary score.")
    lines.append("")
    lines.append("## Next Action")
    lines.append("")
    if best:
        lines.append(f"- Treat `{best['run_key']}` as the current recommended platform candidate, with `candidate_10_bot02_carry_tight_mm.py` retained as the robustness baseline.")
    else:
        lines.append("- Use `candidate_10_bot02_carry_tight_mm.py` as the current >10k baseline.")
    lines.append("- Iterate ACO variants against the platform JSON methodology: target higher ACO PnL without reducing IPR max-long behavior.")
    lines.append("- Preserve every platform run as JSON/log and rerun this analyzer before promotion.")
    return "\n".join(lines) + "\n"


def main():
    artifacts = find_artifacts()
    runs = [analyze_artifact(path) for path in artifacts]
    runs = sorted(runs, key=lambda r: r["pnl_methods"]["official_profit"], reverse=True)
    insights, best = build_insights(runs)
    output = {
        "method": "Platform JSON/log artifact analysis. Official ranking uses JSON `profit`; activities and tradeHistory are audit methods.",
        "artifacts_analyzed": len(runs),
        "ranking": [
            {
                "run_key": run["run_key"],
                "official_profit": run["pnl_methods"]["official_profit"],
                "ipr_pnl": run["final_product_pnl"][IPR],
                "aco_pnl": run["final_product_pnl"][ACO],
                "json_path": run["json_path"],
                "bot_path": run["bot_path"],
            }
            for run in runs
        ],
        "insights": insights,
        "runs": runs,
    }
    OUT_JSON.write_text(json.dumps(round_num(output), indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text(write_markdown(runs, insights, best))
    print(json.dumps(output["ranking"], indent=2))
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
