import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


HYDRO = "HYDROGEL_PACK"
VEX = "VELVETFRUIT_EXTRACT"

STRIKES = {
    "VEV_4000": 4000,
    "VEV_4500": 4500,
    "VEV_5000": 5000,
    "VEV_5100": 5100,
    "VEV_5200": 5200,
    "VEV_5300": 5300,
    "VEV_5400": 5400,
    "VEV_5500": 5500,
    "VEV_6000": 6000,
    "VEV_6500": 6500,
}

FAMILY_SYMBOLS = list(STRIKES.keys())
ACTIVE_MIDDLE = {"VEV_5100", "VEV_5200", "VEV_5300", "VEV_5400", "VEV_5500"}
UPPER_SYMBOLS = {"VEV_5400", "VEV_5500"}
LIMITS = {
    HYDRO: 200,
    VEX: 200,
    **{symbol: 300 for symbol in FAMILY_SYMBOLS},
}

# Product-specific spread gates: HYDRO spreads are always >= 7 in real R4 data
DELTA1_SPREAD_GATE = {HYDRO: 20, VEX: 6}


def best_bid_ask(depth) -> Tuple[Optional[int], Optional[int]]:
    if depth is None:
        return None, None
    bid = max(depth.buy_orders.keys()) if depth.buy_orders else None
    ask = min(depth.sell_orders.keys()) if depth.sell_orders else None
    return bid, ask


def mid_price(depth) -> Optional[float]:
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return None
    return (bid + ask) / 2.0


def spread(depth) -> Optional[int]:
    bid, ask = best_bid_ask(depth)
    if bid is None or ask is None:
        return None
    return ask - bid


def top_depth(depth) -> Tuple[int, int]:
    if depth is None:
        return 0, 0
    bid, ask = best_bid_ask(depth)
    bid_size = depth.buy_orders.get(bid, 0) if bid is not None else 0
    ask_size = -depth.sell_orders.get(ask, 0) if ask is not None else 0
    return max(0, bid_size), max(0, ask_size)


def imbalance(depth) -> float:
    bid_size, ask_size = top_depth(depth)
    total = bid_size + ask_size
    if total <= 0:
        return 0.0
    return (bid_size - ask_size) / total


def clamp_int(value: float) -> int:
    if value >= 0:
        return int(value)
    return -int(-value)


def rolling_slice(items: List[dict], limit: int) -> List[dict]:
    if len(items) <= limit:
        return items
    return items[-limit:]


def classify_trade_bucket(price: int, bid: Optional[int], ask: Optional[int]) -> str:
    if bid is None or ask is None:
        return "unknown"
    if price >= ask:
        return "aggressive_buy"
    if price <= bid:
        return "aggressive_sell"
    return "inside"


@dataclass
class StrategyConfig:
    strategy_id: str
    trade_vex: bool = False
    trade_hydro: bool = False
    trade_4000: bool = False
    trade_5300: bool = False
    trade_upper_passive: bool = False
    use_mark22_veto: bool = False
    use_concentration_gate: bool = False
    use_5200_monitor: bool = False
    use_benign_flow_filter: bool = False
    use_trade_to_book_gate: bool = False
    use_family_pressure_gate: bool = False
    use_toxic_neighbor_gate: bool = False
    use_horizon_hold: bool = False
    use_surface_sanity: bool = False


CONFIGS: Dict[str, StrategyConfig] = {
    "r4_s01_vex_base_control": StrategyConfig("r4_s01_vex_base_control", trade_vex=True),
    "r4_s02_hydro_base_control": StrategyConfig("r4_s02_hydro_base_control", trade_hydro=True),
    "r4_s03_vex_4000_overlay": StrategyConfig("r4_s03_vex_4000_overlay", trade_vex=True, trade_4000=True),
    "r4_s04_vex_5300_overlay": StrategyConfig("r4_s04_vex_5300_overlay", trade_vex=True, trade_5300=True),
    "r4_s05_mark22_veto_gate": StrategyConfig("r4_s05_mark22_veto_gate", trade_vex=True, use_mark22_veto=True),
    "r4_s06_counterparty_concentration_gate": StrategyConfig("r4_s06_counterparty_concentration_gate", trade_vex=True, use_concentration_gate=True),
    "r4_s07_trade_to_book_execution_overlay": StrategyConfig("r4_s07_trade_to_book_execution_overlay", trade_vex=True, trade_4000=True, use_trade_to_book_gate=True),
    "r4_s08_family_pressure_overlay": StrategyConfig("r4_s08_family_pressure_overlay", trade_vex=True, trade_4000=True, use_family_pressure_gate=True),
    "r4_s09_5300_toxic_strike_gate": StrategyConfig("r4_s09_5300_toxic_strike_gate", trade_vex=True, trade_5300=True, use_toxic_neighbor_gate=True),
    "r4_s10_5200_signal_only_veto": StrategyConfig("r4_s10_5200_signal_only_veto", trade_vex=True, use_5200_monitor=True),
    "r4_s11_5300_horizon_hold": StrategyConfig("r4_s11_5300_horizon_hold", trade_vex=True, trade_5300=True, use_horizon_hold=True),
    "r4_s12_upper_passive_probe": StrategyConfig("r4_s12_upper_passive_probe", trade_upper_passive=True),
    "r4_s13_4000_benign_flow_overlay": StrategyConfig("r4_s13_4000_benign_flow_overlay", trade_vex=True, trade_4000=True, use_benign_flow_filter=True),
    "r4_s14_surface_sanity_filter": StrategyConfig("r4_s14_surface_sanity_filter", trade_vex=True, trade_5300=True, use_surface_sanity=True),
    "r4_s15_round3_winner_revalidation": StrategyConfig("r4_s15_round3_winner_revalidation", trade_vex=True, trade_4000=True, use_mark22_veto=True, use_trade_to_book_gate=True),
}


class SharedWave1Trader:
    def __init__(self, strategy_id: str):
        self.cfg = CONFIGS[strategy_id]

    def run(self, state: TradingState):
        stored = self._load_state(state.traderData)
        store = stored.get(self.cfg.strategy_id, {})
        self._update_events(state, store)

        orders: Dict[str, List[Order]] = {}
        context = self._build_context(state, store)

        if self.cfg.trade_vex:
            vex_orders = self._trade_delta1(state, VEX, store, context, conservative=self._is_context_heavy())
            if vex_orders:
                orders[VEX] = vex_orders
        if self.cfg.trade_hydro:
            hydro_orders = self._trade_delta1(state, HYDRO, store, context, conservative=False)
            if hydro_orders:
                orders[HYDRO] = hydro_orders
        if self.cfg.trade_4000:
            overlay_orders = self._trade_overlay(state, "VEV_4000", store, context)
            if overlay_orders:
                orders["VEV_4000"] = overlay_orders
        if self.cfg.trade_5300:
            overlay_orders = self._trade_overlay(state, "VEV_5300", store, context)
            if overlay_orders:
                orders["VEV_5300"] = overlay_orders
        if self.cfg.trade_upper_passive:
            for symbol in ("VEV_5400", "VEV_5500"):
                upper_orders = self._trade_upper_passive(state, symbol, store, context)
                if upper_orders:
                    orders[symbol] = upper_orders

        self._update_mid_cache(state, store)
        stored[self.cfg.strategy_id] = store
        trader_data = json.dumps(stored, separators=(",", ":"))
        return orders, 0, trader_data

    def _load_state(self, trader_data: str) -> dict:
        if not isinstance(trader_data, str) or not trader_data:
            return {}
        try:
            data = json.loads(trader_data)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _update_events(self, state: TradingState, store: dict) -> None:
        events = list(store.get("events", []))
        for symbol, trades in state.market_trades.items():
            if symbol not in FAMILY_SYMBOLS and symbol not in {VEX, HYDRO}:
                continue
            depth = state.order_depths.get(symbol)
            bid, ask = best_bid_ask(depth)
            for trade in trades:
                try:
                    qty = abs(int(trade.quantity))
                except Exception:
                    qty = 0
                events.append(
                    {
                        "symbol": symbol,
                        "buyer": getattr(trade, "buyer", "") or "",
                        "seller": getattr(trade, "seller", "") or "",
                        "price": int(getattr(trade, "price", 0) or 0),
                        "qty": qty,
                        "timestamp": int(getattr(trade, "timestamp", state.timestamp) or state.timestamp),
                        "bucket": classify_trade_bucket(int(getattr(trade, "price", 0) or 0), bid, ask),
                    }
                )
        store["events"] = rolling_slice(events, 120)

    def _build_context(self, state: TradingState, store: dict) -> dict:
        events = store.get("events", [])
        recent_events = events[-20:]
        family_recent = [event for event in recent_events if event["symbol"] in FAMILY_SYMBOLS]
        upper_recent = [event for event in recent_events if event["symbol"] in UPPER_SYMBOLS]
        middle_recent = [event for event in recent_events if event["symbol"] in ACTIVE_MIDDLE]

        concentration_share = self._top_participant_share(family_recent)
        mark22_seller_count = sum(
            1
            for event in middle_recent
            if event["seller"] == "Mark 22" and STRIKES.get(event["symbol"], 0) >= 5200
        )
        mark22_active = mark22_seller_count >= 2
        concentration_high = concentration_share >= 0.50 and len(family_recent) >= 3
        bad_5200 = any(
            event["symbol"] == "VEV_5200"
            and (event["seller"] == "Mark 22" or event["bucket"] != "inside")
            for event in recent_events[-8:]
        )
        last_bucket = recent_events[-1]["bucket"] if recent_events else "unknown"
        family_pressure_score = len(middle_recent)
        if mark22_active or concentration_high:
            family_pressure_score += 2
        family_pressure = "high" if family_pressure_score >= 6 else "medium" if family_pressure_score >= 3 else "low"
        upper_adverse = any(event["bucket"] != "inside" for event in upper_recent[-4:])

        return {
            "recent_events": recent_events,
            "mark22_active": mark22_active,
            "concentration_high": concentration_high,
            "bad_5200": bad_5200,
            "last_bucket": last_bucket,
            "family_pressure": family_pressure,
            "upper_adverse": upper_adverse,
        }

    def _top_participant_share(self, events: List[dict]) -> float:
        counts: Dict[str, int] = {}
        total = 0
        for event in events:
            for side in ("buyer", "seller"):
                name = event.get(side, "")
                if not name:
                    continue
                counts[name] = counts.get(name, 0) + 1
                total += 1
        if total <= 0 or not counts:
            return 0.0
        return max(counts.values()) / total

    def _is_context_heavy(self) -> bool:
        return any(
            [
                self.cfg.use_mark22_veto,
                self.cfg.use_concentration_gate,
                self.cfg.use_5200_monitor,
                self.cfg.use_benign_flow_filter,
                self.cfg.use_trade_to_book_gate,
                self.cfg.use_family_pressure_gate,
                self.cfg.use_toxic_neighbor_gate,
                self.cfg.use_horizon_hold,
                self.cfg.use_surface_sanity,
            ]
        )

    def _trade_delta1(self, state: TradingState, symbol: str, store: dict, context: dict, conservative: bool) -> List[Order]:
        depth = state.order_depths.get(symbol)
        mid = mid_price(depth)
        spread_value = spread(depth)
        if depth is None or mid is None or spread_value is None or spread_value > DELTA1_SPREAD_GATE.get(symbol, 6):
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        pos = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        imb = imbalance(depth)
        last_mid = store.get("last_mid", {}).get(symbol)
        move_term = 0.0 if last_mid is None else 0.15 * (mid - last_mid)
        fair = mid + (1.2 if symbol == VEX else 0.9) * imb + move_term

        if self.cfg.use_mark22_veto and context["mark22_active"] and symbol != VEX:
            return []
        if self.cfg.use_5200_monitor and context["bad_5200"]:
            return []
        if self.cfg.use_concentration_gate and context["concentration_high"]:
            conservative = True
        if self.cfg.use_trade_to_book_gate and context["last_bucket"] != "inside":
            conservative = True
        if self.cfg.use_family_pressure_gate and context["family_pressure"] == "high":
            conservative = True

        clip = 12 if not conservative else 7
        buy_cap = max(0, limit - pos)
        sell_cap = max(0, limit + pos)
        if abs(pos) >= 120:
            clip = min(clip, 4)
        elif abs(pos) >= 80:
            clip = min(clip, 6)
        if spread_value >= 5:
            clip = min(clip, 6)

        orders: List[Order] = []
        cross_edge = 2
        quote_width = 1

        if buy_cap > 0 and ask <= fair - cross_edge:
            take_qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, ask, take_qty))
                buy_cap -= take_qty
        if sell_cap > 0 and bid >= fair + cross_edge:
            take_qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, bid, -take_qty))
                sell_cap -= take_qty

        if buy_cap > 0 and spread_value <= 5:
            bid_px = min(bid + 1, clamp_int(fair - quote_width))
            post_qty = min(clip, buy_cap)
            if post_qty > 0:
                orders.append(Order(symbol, bid_px, post_qty))
        if sell_cap > 0 and spread_value <= 5:
            ask_px = max(ask - 1, clamp_int(fair + quote_width))
            post_qty = min(clip, sell_cap)
            if post_qty > 0:
                orders.append(Order(symbol, ask_px, -post_qty))
        return orders

    def _trade_overlay(self, state: TradingState, symbol: str, store: dict, context: dict) -> List[Order]:
        depth = state.order_depths.get(symbol)
        vex_depth = state.order_depths.get(VEX)
        vex_mid = mid_price(vex_depth)
        overlay_mid = mid_price(depth)
        spread_value = spread(depth)
        if vex_mid is None or depth is None or overlay_mid is None or spread_value is None:
            return []

        strike = STRIKES[symbol]
        pos = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - pos)
        sell_cap = max(0, limit + pos)
        last_mid = store.get("last_mid", {}).get(VEX)
        vex_move = 0.0 if last_mid is None else vex_mid - last_mid
        depth_imb = imbalance(depth)

        if symbol == "VEV_4000":
            fair = max(vex_mid - strike, 0.0) + 3.0 + 0.55 * vex_move + 0.4 * depth_imb
            max_spread = 25
            clip = 15
        else:
            fair = max(vex_mid - strike, 0.0) + 6.0 + 0.70 * vex_move + 0.5 * depth_imb
            max_spread = 10
            clip = 10
        if spread_value > max_spread:
            return []

        if self.cfg.use_mark22_veto and context["mark22_active"]:
            return []
        if self.cfg.use_benign_flow_filter and (context["mark22_active"] or context["concentration_high"]):
            return []
        if self.cfg.use_trade_to_book_gate and context["last_bucket"] != "inside":
            return []
        if self.cfg.use_family_pressure_gate and context["family_pressure"] == "high":
            return []
        if self.cfg.use_toxic_neighbor_gate and self._toxic_neighbor_active(state, context):
            return []
        if self.cfg.use_surface_sanity and self._surface_sanity_bad(state, symbol):
            return []
        if self.cfg.use_horizon_hold:
            if self._late_entry_block(state):
                return []
            if self._should_giveback_exit(state, symbol, store, fair, overlay_mid):
                return self._flatten_product(state, symbol, max_clip=clip)

        if abs(pos) >= (90 if symbol == "VEV_4000" else 60):
            clip = min(clip, 5)

        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        orders: List[Order] = []
        edge = 2
        if buy_cap > 0 and ask <= fair - edge:
            take_qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, ask, take_qty))
        if sell_cap > 0 and bid >= fair + edge:
            take_qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, bid, -take_qty))

        if spread_value <= max_spread - 2:
            if buy_cap > 0:
                bid_px = min(bid + 1, clamp_int(fair - 1))
                post_qty = min(max(1, clip // 2), buy_cap)
                orders.append(Order(symbol, bid_px, post_qty))
            if sell_cap > 0:
                ask_px = max(ask - 1, clamp_int(fair + 1))
                post_qty = min(max(1, clip // 2), sell_cap)
                orders.append(Order(symbol, ask_px, -post_qty))

        self._update_entry_state(state, symbol, store, fair, overlay_mid)
        return orders

    def _trade_upper_passive(self, state: TradingState, symbol: str, store: dict, context: dict) -> List[Order]:
        depth = state.order_depths.get(symbol)
        spread_value = spread(depth)
        if depth is None or spread_value is None or spread_value < 6 or spread_value > 12:
            return []
        if context["upper_adverse"]:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        pos = state.position.get(symbol, 0)
        limit = LIMITS[symbol]
        if abs(pos) >= 20:
            return []
        buy_cap = max(0, limit - pos)
        sell_cap = max(0, limit + pos)
        clip = min(4, buy_cap, sell_cap)
        if clip <= 0:
            return []
        orders: List[Order] = []
        orders.append(Order(symbol, bid + 1, min(clip, buy_cap)))
        orders.append(Order(symbol, ask - 1, -min(clip, sell_cap)))
        return orders

    def _toxic_neighbor_active(self, state: TradingState, context: dict) -> bool:
        if context["mark22_active"] or context["bad_5200"] or context["concentration_high"]:
            return True
        for symbol in ("VEV_5100", "VEV_5200"):
            if spread(state.order_depths.get(symbol)) and spread(state.order_depths.get(symbol)) > 10:
                return True
        return False

    def _surface_sanity_bad(self, state: TradingState, symbol: str) -> bool:
        strikes = sorted((strike, name) for name, strike in STRIKES.items())
        idx = next((i for i, (_, name) in enumerate(strikes) if name == symbol), None)
        if idx is None:
            return False
        mids = []
        current_mid = mid_price(state.order_depths.get(symbol))
        if current_mid is None:
            return False
        if idx > 0:
            mids.append(mid_price(state.order_depths.get(strikes[idx - 1][1])))
        if idx + 1 < len(strikes):
            mids.append(mid_price(state.order_depths.get(strikes[idx + 1][1])))
        mids = [value for value in mids if value is not None]
        if not mids:
            return False
        neighbor_avg = sum(mids) / len(mids)
        return abs(current_mid - neighbor_avg) > 3.0

    def _late_entry_block(self, state: TradingState) -> bool:
        return (state.timestamp % 1_000_000) >= 750_000

    def _should_giveback_exit(self, state: TradingState, symbol: str, store: dict, fair: float, current_mid: float) -> bool:
        pos = state.position.get(symbol, 0)
        if pos == 0:
            return False
        hold_state = store.setdefault("hold_state", {}).setdefault(symbol, {})
        peak = hold_state.get("peak_edge", 0.0)
        current_edge = abs(fair - current_mid)
        peak = max(peak, current_edge)
        hold_state["peak_edge"] = peak
        entry_ts = hold_state.get("entry_ts", state.timestamp)
        hold_steps = int((state.timestamp - entry_ts) / 100)
        return peak > 0 and hold_steps >= 6 and current_edge <= peak * 0.5

    def _flatten_product(self, state: TradingState, symbol: str, max_clip: int) -> List[Order]:
        pos = state.position.get(symbol, 0)
        if pos == 0:
            return []
        depth = state.order_depths.get(symbol)
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        qty = min(abs(pos), max_clip)
        if pos > 0:
            return [Order(symbol, bid, -qty)]
        return [Order(symbol, ask, qty)]

    def _update_entry_state(self, state: TradingState, symbol: str, store: dict, fair: float, current_mid: float) -> None:
        hold_state = store.setdefault("hold_state", {}).setdefault(symbol, {})
        pos = state.position.get(symbol, 0)
        if pos == 0:
            hold_state.clear()
            return
        if "entry_ts" not in hold_state:
            hold_state["entry_ts"] = state.timestamp
            hold_state["peak_edge"] = abs(fair - current_mid)
        else:
            hold_state["peak_edge"] = max(hold_state.get("peak_edge", 0.0), abs(fair - current_mid))

    def _update_mid_cache(self, state: TradingState, store: dict) -> None:
        last_mid = dict(store.get("last_mid", {}))
        for symbol in [HYDRO, VEX] + FAMILY_SYMBOLS:
            mid = mid_price(state.order_depths.get(symbol))
            if mid is not None:
                last_mid[symbol] = mid
        store["last_mid"] = last_mid

