from datamodel import TradingState
import json


class Trader:
    """
    Round 2 diagnostic logger.

    This bot intentionally sends no orders. Its only purpose is to print a
    compact JSON snapshot of every TradingState received from Prosperity so the
    resulting platform logs can be used as EDA input.
    """

    def bid(self):
        return 0

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

    def _plain(self, value, depth=0):
        if depth > 8:
            return str(value)
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {
                str(key): self._plain(item, depth + 1)
                for key, item in value.items()
            }
        if isinstance(value, (list, tuple)):
            return [self._plain(item, depth + 1) for item in value]
        attrs = getattr(value, "__dict__", None)
        if isinstance(attrs, dict):
            return {
                str(key): self._plain(item, depth + 1)
                for key, item in attrs.items()
            }
        return str(value)

    def _sorted_levels(self, levels, reverse):
        if not levels:
            return []
        return [
            {"price": int(price), "volume": int(volume)}
            for price, volume in sorted(levels.items(), reverse=reverse)
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
        total_top_volume = best_bid_volume + best_ask_volume
        total_book_volume = total_bid_volume + total_ask_volume

        summary = {
            "bid_levels": bids,
            "ask_levels": asks,
            "best_bid": best_bid,
            "best_ask": best_ask,
            "best_bid_volume": best_bid_volume,
            "best_ask_volume": best_ask_volume,
            "spread": None,
            "mid": None,
            "top_imbalance": None,
            "book_imbalance": None,
            "total_bid_volume": total_bid_volume,
            "total_ask_volume": total_ask_volume,
        }

        if best_bid is not None and best_ask is not None:
            summary["spread"] = best_ask - best_bid
            summary["mid"] = (best_bid + best_ask) / 2
        if total_top_volume > 0:
            summary["top_imbalance"] = (
                best_bid_volume - best_ask_volume
            ) / total_top_volume
        if total_book_volume > 0:
            summary["book_imbalance"] = (
                total_bid_volume - total_ask_volume
            ) / total_book_volume

        return summary

    def _trade_counts(self, trades_by_symbol):
        return {
            str(symbol): len(trades or [])
            for symbol, trades in (trades_by_symbol or {}).items()
        }

    def _extra_state_fields(self, state):
        attrs = getattr(state, "__dict__", {}) or {}
        known_fields = {
            "traderData",
            "timestamp",
            "listings",
            "order_depths",
            "own_trades",
            "market_trades",
            "position",
            "observations",
        }
        return {
            str(key): self._plain(value)
            for key, value in attrs.items()
            if key not in known_fields
        }

    def _build_payload(self, state, call):
        order_depths = getattr(state, "order_depths", {}) or {}
        trader_data = getattr(state, "traderData", "") or ""
        state_attrs = getattr(state, "__dict__", {}) or {}

        return {
            "tag": "ROUND2_STATE_PROBE",
            "version": 1,
            "call": call,
            "timestamp": getattr(state, "timestamp", None),
            "traderData_in": {
                "length": len(trader_data),
                "value": trader_data,
            },
            "state_fields_seen": sorted(str(key) for key in state_attrs.keys()),
            "extra_state_fields": self._extra_state_fields(state),
            "listings": self._plain(getattr(state, "listings", {})),
            "positions": self._plain(getattr(state, "position", {})),
            "order_depths": self._plain(order_depths),
            "book_summary": {
                str(symbol): self._book_summary(depth)
                for symbol, depth in order_depths.items()
            },
            "own_trades": self._plain(getattr(state, "own_trades", {})),
            "market_trades": self._plain(getattr(state, "market_trades", {})),
            "trade_counts": {
                "own": self._trade_counts(getattr(state, "own_trades", {})),
                "market": self._trade_counts(getattr(state, "market_trades", {})),
            },
            "observations": self._plain(getattr(state, "observations", None)),
        }

    def run(self, state: TradingState):
        call = self._load_counter(getattr(state, "traderData", "")) + 1
        payload = self._build_payload(state, call)

        try:
            print(
                "ROUND2_STATE_PROBE "
                + json.dumps(payload, separators=(",", ":"), sort_keys=True)
            )
        except Exception as exc:
            print(
                "ROUND2_STATE_PROBE_ERROR "
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

        order_depths = getattr(state, "order_depths", {}) or {}
        result = {str(symbol): [] for symbol in order_depths.keys()}
        conversions = 0
        traderData = json.dumps(
            {"call": call, "last_timestamp": getattr(state, "timestamp", None)},
            separators=(",", ":"),
            sort_keys=True,
        )

        return result, conversions, traderData
