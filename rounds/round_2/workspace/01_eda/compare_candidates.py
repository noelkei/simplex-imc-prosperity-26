#!/usr/bin/env python3
import csv
import importlib.util
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = ROOT / "rounds" / "round_2" / "data" / "raw"
CANDIDATES = {
    "hybrid_01": ROOT / "rounds" / "round_2" / "bots" / "amin" / "canonical" / "candidate_r2_amin_hybrid_01.py",
    "feeaware_kalman_02": ROOT / "rounds" / "round_2" / "bots" / "amin" / "canonical" / "candidate_r2_amin_feeaware_kalman_02.py",
}


class Order:
    def __init__(self, symbol: str, price: int, quantity: int):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity


class OrderDepth:
    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}


class TradingState:
    def __init__(self, timestamp, traderData, order_depths, position):
        self.timestamp = timestamp
        self.traderData = traderData
        self.order_depths = order_depths
        self.position = position
        self.own_trades = {}
        self.market_trades = {}
        self.observations = None
        self.listings = {}


def install_datamodel_stub():
    import sys, types
    m = types.ModuleType("datamodel")
    m.Order = Order
    m.OrderDepth = OrderDepth
    m.TradingState = TradingState
    m.UserId = str
    sys.modules["datamodel"] = m


@dataclass
class Fill:
    price: int
    qty: int


PRODUCTS = ["INTARIAN_PEPPER_ROOT", "ASH_COATED_OSMIUM"]
LIMITS = {"INTARIAN_PEPPER_ROOT": 80, "ASH_COATED_OSMIUM": 80}


def load_candidate(path: Path):
    install_datamodel_stub()
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.Trader()


def load_price_rows(day: int):
    rows = []
    with open(DATA_DIR / f"prices_round_2_day_{day}.csv") as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            rows.append(row)
    return rows


def build_ticks(rows):
    ticks = {}
    for row in rows:
        ts = int(row["timestamp"])
        p = row["product"]
        od = ticks.setdefault(ts, {}).setdefault(p, OrderDepth())
        for i in range(1, 4):
            bp = row.get(f"bid_price_{i}")
            bv = row.get(f"bid_volume_{i}")
            ap = row.get(f"ask_price_{i}")
            av = row.get(f"ask_volume_{i}")
            if bp and bv:
                od.buy_orders[int(float(bp))] = int(float(bv))
            if ap and av:
                od.sell_orders[int(float(ap))] = -int(float(av))
    return ticks


def match_orders(order_depth: OrderDepth, orders: List[Order]):
    pnl = 0.0
    pos_delta = 0
    for order in orders:
        qty = order.quantity
        if qty > 0:
            remaining = qty
            for ask in sorted(list(order_depth.sell_orders.keys())):
                if remaining <= 0 or ask > order.price:
                    break
                avail = -order_depth.sell_orders[ask]
                fill = min(avail, remaining)
                if fill > 0:
                    pnl -= fill * ask
                    pos_delta += fill
                    remaining -= fill
                    order_depth.sell_orders[ask] += fill
                    if order_depth.sell_orders[ask] == 0:
                        del order_depth.sell_orders[ask]
        elif qty < 0:
            remaining = -qty
            for bid in sorted(list(order_depth.buy_orders.keys()), reverse=True):
                if remaining <= 0 or bid < order.price:
                    break
                avail = order_depth.buy_orders[bid]
                fill = min(avail, remaining)
                if fill > 0:
                    pnl += fill * bid
                    pos_delta -= fill
                    remaining -= fill
                    order_depth.buy_orders[bid] -= fill
                    if order_depth.buy_orders[bid] == 0:
                        del order_depth.buy_orders[bid]
    return pnl, pos_delta


def mark_to_mid(pos, od: OrderDepth):
    if not od.buy_orders and not od.sell_orders:
        return 0.0
    if od.buy_orders and od.sell_orders:
        mid = (max(od.buy_orders) + min(od.sell_orders)) / 2.0
    elif od.buy_orders:
        mid = max(od.buy_orders)
    else:
        mid = min(od.sell_orders)
    return pos * mid


def run_day(candidate_name: str, candidate_path: Path, day: int):
    trader = load_candidate(candidate_path)
    rows = load_price_rows(day)
    ticks = build_ticks(rows)
    trader_data = ""
    positions = {p: 0 for p in PRODUCTS}
    cash = 0.0

    for ts in sorted(ticks):
        state = TradingState(ts, trader_data, ticks[ts], positions.copy())
        result, conversions, trader_data = trader.run(state)
        for product in PRODUCTS:
            orders = result.get(product, []) if isinstance(result, dict) else []
            cash_delta, pos_delta = match_orders(ticks[ts].get(product, OrderDepth()), orders)
            cash += cash_delta
            positions[product] += pos_delta
            if positions[product] > LIMITS[product]:
                positions[product] = LIMITS[product]
            if positions[product] < -LIMITS[product]:
                positions[product] = -LIMITS[product]

    mtm = 0.0
    last_tick = ticks[max(ticks)]
    for product in PRODUCTS:
        mtm += mark_to_mid(positions[product], last_tick.get(product, OrderDepth()))
    total = cash + mtm
    return {
        "candidate": candidate_name,
        "day": day,
        "cash": round(cash, 2),
        "mtm": round(mtm, 2),
        "total": round(total, 2),
        "positions": positions,
        "bid": getattr(trader, "bid", lambda: None)(),
    }


def main():
    all_results = []
    for name, path in CANDIDATES.items():
        for day in (-1, 0, 1):
            all_results.append(run_day(name, path, day))
    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()
