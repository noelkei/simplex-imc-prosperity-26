from datamodel import TradingState
import json


class Trader:
    """
    Round 3 diagnostic logger.

    This bot intentionally sends no orders. It prints a compact JSON summary of
    every TradingState so the resulting platform logs can be used for EDA,
    validation, and debugging. It is a diagnostic artifact only, never an alpha
    candidate.
    """

    def _load_counter(self, trader_data):
        if not trader_data:
            return 0
        try:
            data = json.loads(trader_data)
            if isinstance(data, dict):
                return int(data.get("call", 0))
        except Exception:
            return 0
        return 0

    def _trade_counts(self, trades_by_symbol):
        return {
            str(symbol): len(trades or [])
            for symbol, trades in (trades_by_symbol or {}).items()
        }

    def _sorted_levels(self, levels, reverse):
        return [
            {"price": int(price), "volume": int(volume)}
            for price, volume in sorted((levels or {}).items(), reverse=reverse)
        ]

    def _book_summary(self, depth):
        buy_orders = getattr(depth, "buy_orders", {}) or {}
        sell_orders = getattr(depth, "sell_orders", {}) or {}

        bids = self._sorted_levels(buy_orders, True)
        asks = self._sorted_levels(sell_orders, False)

        best_bid = bids[0]["price"] if bids else None
        best_ask = asks[0]["price"] if asks else None
        best_bid_volume = bids[0]["volume"] if bids else 0
        best_ask_volume = -asks[0]["volume"] if asks else 0

        total_bid_volume = sum(max(0, int(volume)) for volume in buy_orders.values())
        total_ask_volume = sum(abs(int(volume)) for volume in sell_orders.values())
        top_total = best_bid_volume + best_ask_volume

        summary = {
            "best_bid": best_bid,
            "best_ask": best_ask,
            "best_bid_volume": best_bid_volume,
            "best_ask_volume": best_ask_volume,
            "spread": None,
            "mid": None,
            "top_imbalance": None,
            "total_bid_volume": total_bid_volume,
            "total_ask_volume": total_ask_volume,
            "bid_levels": bids[:3],
            "ask_levels": asks[:3],
        }

        if best_bid is not None and best_ask is not None:
            summary["spread"] = best_ask - best_bid
            summary["mid"] = (best_bid + best_ask) / 2
        if top_total > 0:
            summary["top_imbalance"] = (best_bid_volume - best_ask_volume) / top_total

        return summary

    def _plain(self, value, depth=0):
        if depth > 6:
            return str(value)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(k): self._plain(v, depth + 1) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._plain(v, depth + 1) for v in value]
        attrs = getattr(value, "__dict__", None)
        if isinstance(attrs, dict):
            return {str(k): self._plain(v, depth + 1) for k, v in attrs.items()}
        return str(value)

    def _compact_trades(self, trades_by_symbol):
        compact = {}
        for symbol, trades in (trades_by_symbol or {}).items():
            rows = []
            for trade in (trades or [])[-3:]:
                rows.append(
                    {
                        "price": getattr(trade, "price", None),
                        "quantity": getattr(trade, "quantity", None),
                        "buyer": getattr(trade, "buyer", None),
                        "seller": getattr(trade, "seller", None),
                        "timestamp": getattr(trade, "timestamp", None),
                    }
                )
            compact[str(symbol)] = rows
        return compact

    def _payload(self, state, call):
        order_depths = getattr(state, "order_depths", {}) or {}
        trader_data = getattr(state, "traderData", "") or ""
        return {
            "tag": "ROUND3_STATE_PROBE",
            "version": 1,
            "call": call,
            "timestamp": getattr(state, "timestamp", None),
            "traderData_in_length": len(trader_data),
            "positions": self._plain(getattr(state, "position", {})),
            "trade_counts": {
                "own": self._trade_counts(getattr(state, "own_trades", {})),
                "market": self._trade_counts(getattr(state, "market_trades", {})),
            },
            "recent_own_trades": self._compact_trades(getattr(state, "own_trades", {})),
            "recent_market_trades": self._compact_trades(getattr(state, "market_trades", {})),
            "book_summary": {
                str(symbol): self._book_summary(depth)
                for symbol, depth in order_depths.items()
            },
            "observations": self._plain(getattr(state, "observations", None)),
        }

    def run(self, state: TradingState):
        call = self._load_counter(getattr(state, "traderData", "")) + 1
        payload = self._payload(state, call)

        try:
            print(
                "ROUND3_STATE_PROBE "
                + json.dumps(payload, separators=(",", ":"), sort_keys=True)
            )
        except Exception as exc:
            print(
                "ROUND3_STATE_PROBE_ERROR "
                + json.dumps(
                    {
                        "call": call,
                        "timestamp": getattr(state, "timestamp", None),
                        "error": str(exc),
                    },
                    separators=(",", ":"),
                    sort_keys=True,
                )
            )

        result = {
            str(symbol): []
            for symbol in (getattr(state, "order_depths", {}) or {}).keys()
        }
        conversions = 0
        traderData = json.dumps(
            {"call": call, "last_timestamp": getattr(state, "timestamp", None)},
            separators=(",", ":"),
            sort_keys=True,
        )
        return result, conversions, traderData
