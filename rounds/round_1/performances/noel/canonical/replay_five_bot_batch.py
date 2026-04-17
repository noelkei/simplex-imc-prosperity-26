"""Simple local replay for Round 1 Noel bot batch.

This is a validation helper, not an official Prosperity simulator. It counts
only immediate fills against visible book levels in the sample CSVs. Resting
orders that could be hit later by bots are not modeled.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import sys
import types
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
RAW_DIR = ROOT / "rounds" / "round_1" / "data" / "raw"
BOT_DIR = ROOT / "rounds" / "round_1" / "bots" / "noel" / "canonical"
OUT_JSON = ROOT / "rounds" / "round_1" / "performances" / "noel" / "canonical" / "run_20260416_five_bot_replay_metrics.json"

IPR = "INTARIAN_PEPPER_ROOT"
ACO = "ASH_COATED_OSMIUM"
PRODUCTS = (IPR, ACO)
LIMITS = {IPR: 80, ACO: 80}


class Order:
    def __init__(self, symbol: str, price: int, quantity: int):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"Order({self.symbol}, {self.price}, {self.quantity})"


class OrderDepth:
    def __init__(self):
        self.buy_orders: dict[int, int] = {}
        self.sell_orders: dict[int, int] = {}


class TradingState:
    def __init__(self, traderData, timestamp, order_depths, position):
        self.traderData = traderData
        self.timestamp = timestamp
        self.listings = {}
        self.order_depths = order_depths
        self.own_trades = {}
        self.market_trades = {}
        self.position = position
        self.observations = None


def install_fake_datamodel() -> None:
    module = types.ModuleType("datamodel")
    module.Order = Order
    module.OrderDepth = OrderDepth
    module.TradingState = TradingState
    sys.modules["datamodel"] = module


def parse_int(value: str | None):
    if value is None or value == "":
        return None
    return int(float(value))


def parse_float(value: str | None):
    if value is None or value == "":
        return None
    return float(value)


def load_day(day: int):
    path = RAW_DIR / f"prices_round_1_day_{day}.csv"
    by_timestamp: dict[int, dict[str, dict]] = defaultdict(dict)
    final_mid = {product: None for product in PRODUCTS}
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        for row in reader:
            product = row["product"]
            timestamp = parse_int(row["timestamp"])
            od = OrderDepth()
            for level in (1, 2, 3):
                bid_price = parse_int(row[f"bid_price_{level}"])
                bid_volume = parse_int(row[f"bid_volume_{level}"])
                ask_price = parse_int(row[f"ask_price_{level}"])
                ask_volume = parse_int(row[f"ask_volume_{level}"])
                if bid_price is not None and bid_volume is not None:
                    od.buy_orders[bid_price] = bid_volume
                if ask_price is not None and ask_volume is not None:
                    od.sell_orders[ask_price] = -abs(ask_volume)
            mid = parse_float(row["mid_price"])
            if mid not in (None, 0):
                final_mid[product] = mid
            by_timestamp[timestamp][product] = {"depth": od, "mid": mid}
    return by_timestamp, final_mid


def load_bot(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.Trader()


def match_orders(product: str, orders: list[Order], od: OrderDepth, position: int):
    buy_qty = sum(order.quantity for order in orders if order.quantity > 0)
    sell_qty = sum(-order.quantity for order in orders if order.quantity < 0)
    if buy_qty > LIMITS[product] - position or sell_qty > LIMITS[product] + position:
        return {
            "cash": 0.0,
            "position_delta": 0,
            "fills": 0,
            "filled_qty": 0,
            "rejected": 1,
        }

    buy_book = dict(od.buy_orders)
    sell_book = dict(od.sell_orders)
    cash = 0.0
    position_delta = 0
    fills = 0
    filled_qty = 0

    for order in orders:
        remaining = abs(order.quantity)
        if order.quantity > 0:
            for price in sorted(list(sell_book)):
                if remaining <= 0 or price > order.price:
                    break
                available = -sell_book[price]
                qty = min(remaining, available)
                if qty <= 0:
                    continue
                cash -= qty * price
                position_delta += qty
                filled_qty += qty
                fills += 1
                remaining -= qty
                sell_book[price] += qty
                if sell_book[price] == 0:
                    del sell_book[price]
        elif order.quantity < 0:
            for price in sorted(list(buy_book), reverse=True):
                if remaining <= 0 or price < order.price:
                    break
                available = buy_book[price]
                qty = min(remaining, available)
                if qty <= 0:
                    continue
                cash += qty * price
                position_delta -= qty
                filled_qty += qty
                fills += 1
                remaining -= qty
                buy_book[price] -= qty
                if buy_book[price] == 0:
                    del buy_book[price]

    return {
        "cash": cash,
        "position_delta": position_delta,
        "fills": fills,
        "filled_qty": filled_qty,
        "rejected": 0,
    }


def run_bot_day(bot_path: Path, day: int):
    trader = load_bot(bot_path)
    by_timestamp, final_mid = load_day(day)
    position = {product: 0 for product in PRODUCTS}
    cash = {product: 0.0 for product in PRODUCTS}
    max_abs_pos = {product: 0 for product in PRODUCTS}
    order_count = {product: 0 for product in PRODUCTS}
    fill_count = {product: 0 for product in PRODUCTS}
    filled_qty = {product: 0 for product in PRODUCTS}
    rejections = {product: 0 for product in PRODUCTS}
    errors = 0
    trader_data = ""

    for timestamp in sorted(by_timestamp):
        order_depths = {product: by_timestamp[timestamp][product]["depth"] for product in PRODUCTS if product in by_timestamp[timestamp]}
        state = TradingState(trader_data, timestamp, order_depths, dict(position))
        try:
            result, conversions, trader_data = trader.run(state)
        except Exception:
            errors += 1
            result = {}
            trader_data = trader_data if isinstance(trader_data, str) else ""
        if not isinstance(result, dict):
            errors += 1
            result = {}
        if not isinstance(trader_data, str):
            trader_data = ""
        for product in PRODUCTS:
            orders = result.get(product, [])
            if not isinstance(orders, list):
                errors += 1
                continue
            order_count[product] += len(orders)
            od = order_depths.get(product)
            if od is None:
                continue
            matched = match_orders(product, orders, od, position[product])
            cash[product] += matched["cash"]
            position[product] += matched["position_delta"]
            fill_count[product] += matched["fills"]
            filled_qty[product] += matched["filled_qty"]
            rejections[product] += matched["rejected"]
            max_abs_pos[product] = max(max_abs_pos[product], abs(position[product]))

    pnl_by_product = {}
    for product in PRODUCTS:
        mark = final_mid[product] if final_mid[product] is not None else 0.0
        pnl_by_product[product] = cash[product] + position[product] * mark
    return {
        "day": day,
        "total_pnl": sum(pnl_by_product.values()),
        "pnl_by_product": pnl_by_product,
        "final_position": dict(position),
        "max_abs_position": max_abs_pos,
        "order_count": order_count,
        "fill_count": fill_count,
        "filled_qty": filled_qty,
        "rejections": rejections,
        "errors": errors,
        "final_trader_data_len": len(trader_data),
    }


def main() -> None:
    install_fake_datamodel()
    bot_paths = sorted(path for path in BOT_DIR.glob("candidate_*.py"))
    results = {}
    for bot_path in bot_paths:
        day_results = [run_bot_day(bot_path, day) for day in (-2, -1, 0)]
        totals = {
            "total_pnl": sum(day["total_pnl"] for day in day_results),
            "pnl_by_product": {
                product: sum(day["pnl_by_product"][product] for day in day_results)
                for product in PRODUCTS
            },
            "max_abs_position": {
                product: max(day["max_abs_position"][product] for day in day_results)
                for product in PRODUCTS
            },
            "order_count": {
                product: sum(day["order_count"][product] for day in day_results)
                for product in PRODUCTS
            },
            "fill_count": {
                product: sum(day["fill_count"][product] for day in day_results)
                for product in PRODUCTS
            },
            "filled_qty": {
                product: sum(day["filled_qty"][product] for day in day_results)
                for product in PRODUCTS
            },
            "rejections": {
                product: sum(day["rejections"][product] for day in day_results)
                for product in PRODUCTS
            },
            "errors": sum(day["errors"] for day in day_results),
        }
        results[bot_path.name] = {"days": day_results, "totals": totals}

    ordered = sorted(results.items(), key=lambda item: item[1]["totals"]["total_pnl"], reverse=True)
    output = {
        "method": "Immediate-fill replay against visible sample order books; passive future fills are not modeled.",
        "days": [-2, -1, 0],
        "ranking": [
            {"bot": name, "total_pnl": metrics["totals"]["total_pnl"]}
            for name, metrics in ordered
        ],
        "results": results,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output["ranking"], indent=2))
    print(f"Wrote {OUT_JSON}")


if __name__ == "__main__":
    main()
