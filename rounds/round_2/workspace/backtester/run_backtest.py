"""
IMC Prosperity 4 — Round 2 Backtester
Runs all 10 r2_b* bots against price CSV data (days -1, 0, 1).

Fill model (standard Prosperity simulation):
  - Each timestamp is independent (no order carry-over between ticks).
  - Buy order at price P, qty Q: fills against asks <= P, best first.
  - Sell order at price P, qty Q: fills against bids >= P, best first.
  - Position limits (±80) are enforced; excess is clipped.
  - P&L = sum(fill_cash_flows) + final_position × final_mid_price.
    "Realised" = cash flows only; "Total" = realised + MTM.

Days are independent runs (position resets to 0 at start of each day).
"""
import csv
import importlib.util
import os
import sys
import json
import traceback
from datamodel import Order, OrderDepth, TradingState

# ─── paths ────────────────────────────────────────────────────────────────────

THIS_DIR   = os.path.dirname(os.path.abspath(__file__))
BOTS_DIR   = os.path.join(THIS_DIR, "..", "..", "bots", "bruno", "canonical")
DATA_DIR   = os.path.join(THIS_DIR, "..", "..", "..", "data", "raw")
PERF_DIR   = os.path.join(THIS_DIR, "..", "..", "performances", "bruno", "canonical")
os.makedirs(PERF_DIR, exist_ok=True)

DAYS = [-1, 0, 1]
IPR  = "INTARIAN_PEPPER_ROOT"
ACO  = "ASH_COATED_OSMIUM"
PRODUCTS = [ACO, IPR]
LIMITS = {IPR: 80, ACO: 80}


# ─── data loading ─────────────────────────────────────────────────────────────

def load_prices(day):
    """Return sorted list of (timestamp, product, OrderDepth, mid) tuples."""
    path = os.path.join(DATA_DIR, f"prices_round_2_day_{day}.csv")
    recs = {}   # timestamp -> {product -> (OrderDepth, mid)}
    with open(path, newline="") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            product = row["product"]
            if product not in PRODUCTS:
                continue
            t = int(row["timestamp"])

            def _f(k):
                v = row.get(k, "")
                return float(v) if v not in ("", None) else None

            od = OrderDepth()
            for lvl in (1, 2, 3):
                bp = _f(f"bid_price_{lvl}")
                bv = _f(f"bid_volume_{lvl}")
                ap = _f(f"ask_price_{lvl}")
                av = _f(f"ask_volume_{lvl}")
                if bp is not None and bv is not None:
                    od.buy_orders[int(bp)] = int(bv)
                if ap is not None and av is not None:
                    od.sell_orders[int(ap)] = -int(av)

            mid = _f("mid_price")
            recs.setdefault(t, {})[product] = (od, mid)

    return sorted(recs.items())   # [(t, {product: (od, mid)}), ...]


# ─── fill engine ──────────────────────────────────────────────────────────────

def fill_orders(orders, order_depths, positions, limits):
    """
    Match bot orders against the current book.
    Returns dict of {product: (cash_flow, filled_qty)} for this tick.
    Modifies positions in-place.
    """
    fills = {p: {"cash": 0.0, "qty": 0} for p in PRODUCTS}
    by_product = {}
    for o in orders:
        by_product.setdefault(o.symbol, []).append(o)

    for product, prod_orders in by_product.items():
        od   = order_depths.get(product)
        pos  = positions.get(product, 0)
        lim  = limits.get(product, 80)
        if od is None:
            continue

        asks_asc  = sorted(od.sell_orders.keys())           # ascending
        bids_desc = sorted(od.buy_orders.keys(), reverse=True)  # descending
        avail_ask = {p: -od.sell_orders[p] for p in asks_asc}   # positive qty
        avail_bid = {p:  od.buy_orders[p]  for p in bids_desc}  # positive qty

        for order in prod_orders:
            qty = order.quantity   # positive = buy, negative = sell

            if qty > 0:  # BUY
                cap = lim - pos
                qty = min(qty, cap)
                for ap in asks_asc:
                    if qty <= 0 or ap > order.price:
                        break
                    trade = min(qty, avail_ask[ap])
                    if trade <= 0:
                        continue
                    fills[product]["cash"]  -= trade * ap
                    fills[product]["qty"]   += trade
                    pos  += trade
                    qty  -= trade
                    avail_ask[ap] -= trade

            elif qty < 0:  # SELL
                qty = abs(qty)
                cap = lim + pos
                qty = min(qty, cap)
                for bp in bids_desc:
                    if qty <= 0 or bp < order.price:
                        break
                    trade = min(qty, avail_bid[bp])
                    if trade <= 0:
                        continue
                    fills[product]["cash"]  += trade * bp
                    fills[product]["qty"]   -= trade
                    pos  -= trade
                    qty  -= trade
                    avail_bid[bp] -= trade

        positions[product] = pos

    return fills


# ─── bot loader ───────────────────────────────────────────────────────────────

def load_bot(bot_path):
    spec   = importlib.util.spec_from_file_location("bot_module", bot_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["datamodel"] = sys.modules.get("datamodel") or __import__("datamodel")
    spec.loader.exec_module(module)
    return module.Trader()


# ─── run one bot × one day ────────────────────────────────────────────────────

def run_day(trader, price_data):
    """
    Run a single bot over one day's price data.
    Returns per-product P&L dict and trade log.
    """
    positions  = {p: 0 for p in PRODUCTS}
    cash       = {p: 0.0 for p in PRODUCTS}
    trader_data = ""
    last_mid    = {p: None for p in PRODUCTS}

    for t, tick in price_data:
        order_depths = {}
        for product, (od, mid) in tick.items():
            order_depths[product] = od
            if mid is not None:
                last_mid[product] = mid

        state = TradingState(
            timestamp    = t,
            listings     = {},
            order_depths = order_depths,
            own_trades   = {},
            market_trades= {},
            position     = dict(positions),
            observations = {},
            traderData   = trader_data,
        )

        try:
            result = trader.run(state)
            if isinstance(result, tuple) and len(result) == 3:
                orders_map, conversions, trader_data = result
            else:
                orders_map, trader_data = result, ""
        except Exception as e:
            orders_map  = {}
            trader_data = ""

        # flatten orders
        all_orders = []
        for prod, orders in (orders_map or {}).items():
            if orders:
                all_orders.extend(orders)

        fills = fill_orders(all_orders, order_depths, positions, LIMITS)
        for product, f in fills.items():
            cash[product] += f["cash"]

    # mark-to-market final positions
    pnl = {}
    for product in PRODUCTS:
        mtm = positions[product] * (last_mid[product] or 0.0)
        pnl[product] = {
            "realised": cash[product],
            "position": positions[product],
            "mtm":      mtm,
            "total":    cash[product] + mtm,
        }
    return pnl


# ─── run all bots ─────────────────────────────────────────────────────────────

def main():
    bots = sorted(
        f for f in os.listdir(BOTS_DIR)
        if f.startswith("r2_b") and f.endswith(".py")
    )

    all_price_data = {}
    for day in DAYS:
        all_price_data[day] = load_prices(day)
    print(f"Loaded price data for days {DAYS}: "
          f"{sum(len(v) for v in all_price_data.values())} timestamps total.")

    summary = []

    for bot_file in bots:
        bot_name = bot_file[:-3]
        bot_path = os.path.join(BOTS_DIR, bot_file)

        try:
            day_results = []
            for day in DAYS:
                # Re-load bot fresh each day (resets Trader state)
                trader = load_bot(bot_path)
                pnl = run_day(trader, all_price_data[day])
                day_results.append((day, pnl))

            # Aggregate across days
            agg = {p: {"realised": 0.0, "mtm": 0.0, "total": 0.0} for p in PRODUCTS}
            for day, pnl in day_results:
                for product in PRODUCTS:
                    agg[product]["realised"] += pnl[product]["realised"]
                    agg[product]["mtm"]      += pnl[product]["mtm"]
                    agg[product]["total"]    += pnl[product]["total"]

            aco_total = agg[ACO]["total"]
            ipr_total = agg[IPR]["total"]
            grand     = aco_total + ipr_total

            row = {
                "bot":       bot_name,
                "ACO_real":  agg[ACO]["realised"],
                "ACO_mtm":   agg[ACO]["mtm"],
                "ACO_total": aco_total,
                "IPR_real":  agg[IPR]["realised"],
                "IPR_mtm":   agg[IPR]["mtm"],
                "IPR_total": ipr_total,
                "GRAND":     grand,
                "days":      day_results,
            }
            summary.append(row)

            print(f"{bot_name:30s}  ACO={aco_total:+8.0f}  IPR={ipr_total:+8.0f}  TOTAL={grand:+8.0f}")

        except Exception:
            print(f"{bot_name:30s}  ERROR: {traceback.format_exc()}")

    # ── save detailed run report ─────────────────────────────────────────────
    from datetime import datetime
    ts_str = datetime.now().strftime("%Y%m%d_%H%M")
    report_path = os.path.join(PERF_DIR, f"run_{ts_str}_all_bots.md")

    with open(report_path, "w") as f:
        f.write(f"# Backtest Report — R2 All Bots\n\n")
        f.write(f"- Run timestamp: {ts_str}\n")
        f.write(f"- Days: {DAYS}\n")
        f.write(f"- Fill model: aggressive fills only (buy ≤ ask level; sell ≥ bid level)\n\n")

        f.write("## Summary Table\n\n")
        f.write("| Bot | ACO total | IPR total | Grand total | vs b01 ACO | vs b01 total |\n")
        f.write("| --- | ---: | ---: | ---: | ---: | ---: |\n")

        b01_aco   = next((r["ACO_total"] for r in summary if r["bot"] == "r2_b01_baseline"), None)
        b01_grand = next((r["GRAND"]     for r in summary if r["bot"] == "r2_b01_baseline"), None)

        for r in summary:
            daco  = f"{r['ACO_total'] - b01_aco:+.0f}" if b01_aco is not None else "—"
            dgrand = f"{r['GRAND'] - b01_grand:+.0f}" if b01_grand is not None else "—"
            f.write(f"| `{r['bot']}` | {r['ACO_total']:+.0f} | {r['IPR_total']:+.0f} | "
                    f"{r['GRAND']:+.0f} | {daco} | {dgrand} |\n")

        f.write("\n## Per-Day Detail\n\n")
        for r in summary:
            f.write(f"### {r['bot']}\n\n")
            f.write("| Day | ACO realised | ACO MTM | ACO total | IPR realised | IPR MTM | IPR total | Day total |\n")
            f.write("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n")
            for day, pnl in r["days"]:
                day_total = pnl[ACO]["total"] + pnl[IPR]["total"]
                f.write(
                    f"| {day:+d} | {pnl[ACO]['realised']:+.0f} | {pnl[ACO]['mtm']:+.0f} | "
                    f"{pnl[ACO]['total']:+.0f} | {pnl[IPR]['realised']:+.0f} | "
                    f"{pnl[IPR]['mtm']:+.0f} | {pnl[IPR]['total']:+.0f} | {day_total:+.0f} |\n"
                )
            f.write("\n")

        f.write("## Interpretation Notes\n\n")
        f.write("- IPR P&L is **MTM-dominated**: max-long bot accumulates +80 and holds.\n")
        f.write("- ACO P&L is the differentiated axis; bots differ only in ACO strategy.\n")
        f.write("- Aggressive-fills-only model **understates** passive-quote P&L;\n"
                "  differences between bots are directionally correct.\n")
        f.write("- Treat as **non-authoritative evidence** (backtest ≠ live results).\n")

    print(f"\nReport written to: {report_path}")
    return summary, b01_aco, b01_grand


if __name__ == "__main__":
    # Add this dir to sys.path so bots can import datamodel
    sys.path.insert(0, THIS_DIR)
    main()
