import json
import math
from dataclasses import dataclass
from statistics import NormalDist
from typing import Dict, List, Optional, Tuple

from datamodel import Order, TradingState


NORMAL = NormalDist()

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
LIMITS = {
    HYDRO: 200,
    VEX: 200,
    **{symbol: 300 for symbol in FAMILY_SYMBOLS},
}

TIME_SCALE = 1_000_000
ROUND4_OPTION_DAYS_LEFT = 4.0
TICKS_PER_STEP = 100


def sign(value: int) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


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


def clamp_floor(value: float) -> int:
    return int(math.floor(value))


def clamp_ceil(value: float) -> int:
    return int(math.ceil(value))


def rolling_slice(items: List[dict], limit: int) -> List[dict]:
    if len(items) <= limit:
        return items
    return items[-limit:]


def mean(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return sum(values) / len(values)


def classify_trade_bucket(price: int, bid: Optional[int], ask: Optional[int]) -> str:
    if bid is None or ask is None:
        return "unknown"
    if price >= ask:
        return "aggressive_buy"
    if price <= bid:
        return "aggressive_sell"
    return "inside"


def session_progress(timestamp: int) -> float:
    return float(timestamp % TIME_SCALE) / float(TIME_SCALE)


def tte_years(timestamp: int) -> float:
    progress = session_progress(timestamp)
    days_left = max(0.5, ROUND4_OPTION_DAYS_LEFT - progress)
    return days_left / 365.0


def intrinsic_value(spot: float, strike: int) -> float:
    return max(0.0, spot - strike)


def bs_call(spot: float, strike: int, time_to_expiry: float, volatility: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if time_to_expiry <= 0 or volatility <= 0:
        return intrinsic_value(spot, strike)
    sqrt_t = math.sqrt(time_to_expiry)
    sigma_sqrt_t = volatility * sqrt_t
    if sigma_sqrt_t <= 0:
        return intrinsic_value(spot, strike)
    d1 = (
        math.log(spot / strike) + 0.5 * volatility * volatility * time_to_expiry
    ) / sigma_sqrt_t
    d2 = d1 - sigma_sqrt_t
    return spot * NORMAL.cdf(d1) - strike * NORMAL.cdf(d2)


def bs_delta(spot: float, strike: int, time_to_expiry: float, volatility: float) -> float:
    if spot <= 0 or strike <= 0:
        return 0.0
    if time_to_expiry <= 0 or volatility <= 0:
        return 1.0 if spot > strike else 0.0
    sqrt_t = math.sqrt(time_to_expiry)
    sigma_sqrt_t = volatility * sqrt_t
    if sigma_sqrt_t <= 0:
        return 1.0 if spot > strike else 0.0
    d1 = (
        math.log(spot / strike) + 0.5 * volatility * volatility * time_to_expiry
    ) / sigma_sqrt_t
    return NORMAL.cdf(d1)


def implied_volatility(
    call_price: float,
    spot: float,
    strike: int,
    time_to_expiry: float,
    max_iterations: int = 32,
) -> Optional[float]:
    intrinsic = intrinsic_value(spot, strike)
    target = max(call_price, intrinsic)
    if target <= intrinsic + 1e-6:
        return 0.08
    if spot <= 0 or strike <= 0 or time_to_expiry <= 0:
        return None

    low = 1e-4
    high = 4.0
    for _ in range(max_iterations):
        mid = 0.5 * (low + high)
        price = bs_call(spot, strike, time_to_expiry, mid)
        if price >= target:
            high = mid
        else:
            low = mid
    return high


@dataclass
class StrategyConfig:
    strategy_id: str
    trade_vex: bool = True
    trade_4000: bool = False
    trade_5300: bool = False
    vex_mode: str = ""
    option_mode: str = ""


CONFIGS: Dict[str, StrategyConfig] = {
    "r4_w2_01_vex_late_no_new_entry": StrategyConfig(
        "r4_w2_01_vex_late_no_new_entry",
        trade_vex=True,
        vex_mode="late_no_new_entry",
    ),
    "r4_w2_02_vex_inside_book_only": StrategyConfig(
        "r4_w2_02_vex_inside_book_only",
        trade_vex=True,
        vex_mode="inside_book_only",
    ),
    "r4_w2_03_vex_micro_reversal_entry": StrategyConfig(
        "r4_w2_03_vex_micro_reversal_entry",
        trade_vex=True,
        vex_mode="micro_reversal_entry",
    ),
    "r4_w2_04_vex_depth_supported_entry": StrategyConfig(
        "r4_w2_04_vex_depth_supported_entry",
        trade_vex=True,
        vex_mode="depth_supported_entry",
    ),
    "r4_w2_05_5300_clean_value_retest": StrategyConfig(
        "r4_w2_05_5300_clean_value_retest",
        trade_vex=True,
        trade_5300=True,
        option_mode="5300_clean_value",
    ),
    "r4_w2_06_5300_direct_dislocation_only": StrategyConfig(
        "r4_w2_06_5300_direct_dislocation_only",
        trade_vex=False,
        trade_5300=True,
        option_mode="5300_direct_dislocation",
    ),
    "r4_w2_07_5300_queue_takeover_probe": StrategyConfig(
        "r4_w2_07_5300_queue_takeover_probe",
        trade_vex=True,
        trade_5300=True,
        option_mode="5300_queue_takeover",
    ),
    "r4_w2_08_5300_with_5200_veto": StrategyConfig(
        "r4_w2_08_5300_with_5200_veto",
        trade_vex=True,
        trade_5300=True,
        option_mode="5300_with_5200_veto",
    ),
    "r4_w2_09_vex_tape_clean_entry": StrategyConfig(
        "r4_w2_09_vex_tape_clean_entry",
        trade_vex=True,
        vex_mode="tape_clean_entry",
    ),
    "r4_w2_10_vex_imbalance_surge_entry": StrategyConfig(
        "r4_w2_10_vex_imbalance_surge_entry",
        trade_vex=True,
        vex_mode="imbalance_surge_entry",
    ),
    "r4_w2_11_vex_low_concentration_entry": StrategyConfig(
        "r4_w2_11_vex_low_concentration_entry",
        trade_vex=True,
        vex_mode="low_concentration_entry",
    ),
    "r4_w2_12_5300_option_only_veto": StrategyConfig(
        "r4_w2_12_5300_option_only_veto",
        trade_vex=False,
        trade_5300=True,
        option_mode="5300_option_only_veto",
    ),
    "r4_w2_13_4000_forced_activation": StrategyConfig(
        "r4_w2_13_4000_forced_activation",
        trade_vex=True,
        trade_4000=True,
        option_mode="4000_forced_activation",
    ),
    "r4_w2_14_4000_option_only_band_entry": StrategyConfig(
        "r4_w2_14_4000_option_only_band_entry",
        trade_vex=False,
        trade_4000=True,
        option_mode="4000_option_only_band",
    ),
    "r4_w2_15_4000_quote_ladder_probe": StrategyConfig(
        "r4_w2_15_4000_quote_ladder_probe",
        trade_vex=True,
        trade_4000=True,
        option_mode="4000_quote_ladder",
    ),
}


class SharedWave2Trader:
    def __init__(self, strategy_id: str):
        self.cfg = CONFIGS[strategy_id]

    def run(self, state: TradingState):
        stored = self._load_state(state.traderData)
        store = stored.get(self.cfg.strategy_id, {})
        self._update_events(state, store)

        context = self._build_context(state, store)
        self._refresh_position_state(state, store, VEX, mid_price(state.order_depths.get(VEX)))
        if self.cfg.trade_5300:
            self._refresh_position_state(state, store, "VEV_5300", mid_price(state.order_depths.get("VEV_5300")))
        if self.cfg.trade_4000:
            self._refresh_position_state(state, store, "VEV_4000", mid_price(state.order_depths.get("VEV_4000")))

        orders: Dict[str, List[Order]] = {}
        if self.cfg.trade_vex:
            vex_orders = self._trade_vex(state, store, context)
            if vex_orders:
                orders[VEX] = vex_orders
        if self.cfg.trade_5300:
            option_orders = self._trade_option(state, "VEV_5300", store, context)
            if option_orders:
                orders["VEV_5300"] = option_orders
        if self.cfg.trade_4000:
            option_orders = self._trade_option(state, "VEV_4000", store, context)
            if option_orders:
                orders["VEV_4000"] = option_orders

        self._update_mid_cache(state, store)
        stored[self.cfg.strategy_id] = store
        trader_data = json.dumps(stored, separators=(",", ":"))
        return orders, 0, trader_data

    def _load_state(self, trader_data: str) -> dict:
        if not isinstance(trader_data, str) or not trader_data:
            return {}
        try:
            loaded = json.loads(trader_data)
            return loaded if isinstance(loaded, dict) else {}
        except Exception:
            return {}

    def _update_events(self, state: TradingState, store: dict) -> None:
        events = list(store.get("events", []))
        for symbol, trades in state.market_trades.items():
            if symbol not in FAMILY_SYMBOLS and symbol != VEX:
                continue
            depth = state.order_depths.get(symbol)
            bid, ask = best_bid_ask(depth)
            for trade in trades:
                price = int(getattr(trade, "price", 0) or 0)
                events.append(
                    {
                        "symbol": symbol,
                        "buyer": getattr(trade, "buyer", "") or "",
                        "seller": getattr(trade, "seller", "") or "",
                        "price": price,
                        "qty": abs(int(getattr(trade, "quantity", 0) or 0)),
                        "timestamp": int(getattr(trade, "timestamp", state.timestamp) or state.timestamp),
                        "bucket": classify_trade_bucket(price, bid, ask),
                    }
                )
        store["events"] = rolling_slice(events, 160)

    def _build_context(self, state: TradingState, store: dict) -> dict:
        events = store.get("events", [])
        timestamp = state.timestamp
        recent_events = [event for event in events if event["timestamp"] >= timestamp - 4_000]
        family_recent = [event for event in recent_events if event["symbol"] in FAMILY_SYMBOLS]
        middle_recent = [event for event in recent_events if event["symbol"] in ACTIVE_MIDDLE]
        vex_recent = [event for event in recent_events if event["symbol"] == VEX]

        concentration_share = self._top_participant_share(family_recent)
        mark22_5200_recent = any(
            event["symbol"] == "VEV_5200"
            and event["seller"] == "Mark 22"
            for event in recent_events
        )
        bad_5200_recent = any(
            event["symbol"] == "VEV_5200"
            and (event["seller"] == "Mark 22" or event["bucket"] != "inside")
            for event in recent_events
        )
        last_vex_bucket = vex_recent[-1]["bucket"] if vex_recent else "unknown"
        last_4000_bucket = self._last_bucket_for_symbol(recent_events, "VEV_4000")

        pressure_score = sum(1 for event in middle_recent if event["bucket"] != "inside")
        if mark22_5200_recent:
            pressure_score += 2
        if concentration_share >= 0.50 and len(family_recent) >= 4:
            pressure_score += 1
        family_pressure = "high" if pressure_score >= 5 else "medium" if pressure_score >= 3 else "low"

        vex_depth = state.order_depths.get(VEX)
        vex_spread = spread(vex_depth)
        bid_depth, ask_depth = top_depth(vex_depth)
        parent_good = (
            vex_spread is not None
            and vex_spread <= 1
            and bid_depth >= 8
            and ask_depth >= 8
            and last_vex_bucket != "aggressive_sell"
        )
        benign_4000_tape = parent_good and not mark22_5200_recent and last_4000_bucket != "aggressive_sell"

        return {
            "recent_events": recent_events,
            "family_recent": family_recent,
            "mark22_5200_recent": mark22_5200_recent,
            "bad_5200_recent": bad_5200_recent,
            "last_vex_bucket": last_vex_bucket,
            "last_4000_bucket": last_4000_bucket,
            "family_pressure": family_pressure,
            "parent_good": parent_good,
            "benign_4000_tape": benign_4000_tape,
            "concentration_share": concentration_share,
        }

    def _last_bucket_for_symbol(self, events: List[dict], symbol: str) -> str:
        for event in reversed(events):
            if event["symbol"] == symbol:
                return event["bucket"]
        return "unknown"

    def _top_participant_share(self, events: List[dict]) -> float:
        counts: Dict[str, int] = {}
        total = 0
        for event in events:
            for key in ("buyer", "seller"):
                name = event.get(key, "")
                if not name:
                    continue
                counts[name] = counts.get(name, 0) + 1
                total += 1
        if total <= 0 or not counts:
            return 0.0
        return max(counts.values()) / total

    def _refresh_position_state(self, state: TradingState, store: dict, symbol: str, current_mid: Optional[float]) -> None:
        pos_states = store.setdefault("position_state", {})
        existing = dict(pos_states.get(symbol, {}))
        position = int(state.position.get(symbol, 0))
        if position == 0 or current_mid is None:
            pos_states[symbol] = {"prev_pos": position}
            return

        previous = int(existing.get("prev_pos", 0))
        previous_sign = sign(previous)
        current_sign = sign(position)
        if previous == 0 or previous_sign != current_sign:
            pos_states[symbol] = {
                "prev_pos": position,
                "entry_mid": current_mid,
                "entry_ts": state.timestamp,
                "peak_unrealized": 0.0,
            }
            return

        entry_mid = float(existing.get("entry_mid", current_mid))
        current_unrealized = (current_mid - entry_mid) * current_sign
        pos_states[symbol] = {
            "prev_pos": position,
            "entry_mid": entry_mid,
            "entry_ts": int(existing.get("entry_ts", state.timestamp)),
            "peak_unrealized": max(float(existing.get("peak_unrealized", 0.0)), current_unrealized),
        }

    def _position_stop_triggered(
        self,
        state: TradingState,
        store: dict,
        symbol: str,
        current_mid: Optional[float],
        min_peak: float,
        giveback_fraction: float,
        max_drawdown: Optional[float] = None,
        min_hold_steps: int = 0,
    ) -> bool:
        if current_mid is None:
            return False
        pos_state = store.get("position_state", {}).get(symbol, {})
        position = int(state.position.get(symbol, 0))
        if position == 0:
            return False
        entry_mid = pos_state.get("entry_mid")
        if entry_mid is None:
            return False
        current_unrealized = (current_mid - float(entry_mid)) * sign(position)
        peak = float(pos_state.get("peak_unrealized", 0.0))
        if peak < min_peak:
            return False
        entry_ts = int(pos_state.get("entry_ts", state.timestamp))
        hold_steps = int((state.timestamp - entry_ts) / TICKS_PER_STEP)
        if hold_steps < min_hold_steps:
            return False
        giveback_hit = current_unrealized <= peak * (1.0 - giveback_fraction)
        drawdown_hit = max_drawdown is not None and (peak - current_unrealized) >= max_drawdown
        return giveback_hit or drawdown_hit

    def _flatten_product(self, state: TradingState, symbol: str, max_clip: int) -> List[Order]:
        position = int(state.position.get(symbol, 0))
        if position == 0:
            return []
        depth = state.order_depths.get(symbol)
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        quantity = min(abs(position), max_clip)
        if position > 0:
            return [Order(symbol, bid, -quantity)]
        return [Order(symbol, ask, quantity)]

    def _trade_vex(self, state: TradingState, store: dict, context: dict) -> List[Order]:
        depth = state.order_depths.get(VEX)
        mid = mid_price(depth)
        spread_value = spread(depth)
        if depth is None or mid is None or spread_value is None or spread_value > 6:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        bid_depth, ask_depth = top_depth(depth)
        depth_imbalance = imbalance(depth)

        position = int(state.position.get(VEX, 0))
        limit = LIMITS[VEX]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)
        if buy_cap <= 0 and sell_cap <= 0:
            return []

        last_mid = store.get("last_mid", {}).get(VEX)
        move_term = 0.0 if last_mid is None else 0.15 * (mid - last_mid)
        fair = mid + 1.2 * depth_imbalance + move_term

        clip = 12 if not (self.cfg.trade_4000 or self.cfg.trade_5300) else 10
        if abs(position) >= 120:
            clip = min(clip, 4)
        elif abs(position) >= 80:
            clip = min(clip, 8)
        if spread_value >= 5:
            clip = min(clip, 6)

        block_new_entries = False
        cooldowns = store.setdefault("cooldowns", {})
        current_ts = state.timestamp

        if self.cfg.vex_mode == "late_no_new_entry" and session_progress(current_ts) >= 0.82:
            block_new_entries = True
        if self.cfg.vex_mode == "peak_giveback_stop":
            if self._position_stop_triggered(
                state,
                store,
                VEX,
                mid,
                min_peak=8.0,
                giveback_fraction=0.40,
                max_drawdown=22.0,
            ):
                cooldowns["vex_stop_until"] = current_ts + 1_000
                return self._flatten_product(state, VEX, max_clip=16)
            if current_ts < int(cooldowns.get("vex_stop_until", 0)):
                block_new_entries = True
        if self.cfg.vex_mode == "toxic_window_cooldown" and context["mark22_5200_recent"]:
            cooldowns["vex_toxic_until"] = current_ts + 200
        if self.cfg.vex_mode == "toxic_window_cooldown" and current_ts < int(cooldowns.get("vex_toxic_until", 0)):
            block_new_entries = True
        if self.cfg.vex_mode == "vex_plus_5200_veto" and context["bad_5200_recent"]:
            block_new_entries = True
        if self.cfg.vex_mode == "trade_to_book_light" and context["last_vex_bucket"] != "inside" and spread_value > 1:
            block_new_entries = True
        if self.cfg.vex_mode == "family_pressure_light" and context["family_pressure"] == "high":
            block_new_entries = True
        if self.cfg.vex_mode == "smaller_second_clip" and abs(position) > 0:
            clip = min(clip, 8)

        buy_signal = True
        sell_signal = True
        clean_tape = context["last_vex_bucket"] in {"inside", "unknown"}
        if self.cfg.vex_mode == "inside_book_only":
            buy_signal = spread_value <= 1 and clean_tape and fair >= mid
            sell_signal = spread_value <= 1 and clean_tape and fair <= mid
        elif self.cfg.vex_mode == "micro_reversal_entry":
            buy_signal = context["last_vex_bucket"] == "aggressive_sell" and depth_imbalance >= 0.20 and fair >= mid
            sell_signal = context["last_vex_bucket"] == "aggressive_buy" and depth_imbalance <= -0.20 and fair <= mid
        elif self.cfg.vex_mode == "depth_supported_entry":
            buy_signal = spread_value <= 2 and bid_depth >= 12 and fair >= mid
            sell_signal = spread_value <= 2 and ask_depth >= 12 and fair <= mid
        elif self.cfg.vex_mode == "tape_clean_entry":
            buy_signal = spread_value <= 1 and clean_tape and not context["bad_5200_recent"] and context["family_pressure"] == "low" and fair >= mid
            sell_signal = spread_value <= 1 and clean_tape and not context["bad_5200_recent"] and context["family_pressure"] == "low" and fair <= mid
        elif self.cfg.vex_mode == "imbalance_surge_entry":
            buy_signal = spread_value <= 2 and depth_imbalance >= 0.35
            sell_signal = spread_value <= 2 and depth_imbalance <= -0.35
        elif self.cfg.vex_mode == "low_concentration_entry":
            buy_signal = context["concentration_share"] < 0.42 and context["family_pressure"] != "high" and fair >= mid
            sell_signal = context["concentration_share"] < 0.42 and context["family_pressure"] != "high" and fair <= mid

        block_buy = block_new_entries and position >= 0
        block_sell = block_new_entries and position <= 0
        if not buy_signal:
            block_buy = True
        if not sell_signal:
            block_sell = True
        orders: List[Order] = []

        if buy_cap > 0 and not block_buy and ask <= fair - 2.0:
            take_qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_qty > 0:
                orders.append(Order(VEX, ask, take_qty))
                buy_cap -= take_qty
        if sell_cap > 0 and not block_sell and bid >= fair + 2.0:
            take_qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_qty > 0:
                orders.append(Order(VEX, bid, -take_qty))
                sell_cap -= take_qty

        if spread_value <= 4:
            if buy_cap > 0 and not block_buy:
                post_qty = min(clip, buy_cap)
                bid_px = min(bid + 1, clamp_floor(fair - 1.0))
                if post_qty > 0:
                    orders.append(Order(VEX, bid_px, post_qty))
            if sell_cap > 0 and not block_sell:
                post_qty = min(clip, sell_cap)
                ask_px = max(ask - 1, clamp_ceil(fair + 1.0))
                if post_qty > 0:
                    orders.append(Order(VEX, ask_px, -post_qty))
        return self._dedupe_orders(orders)

    def _trade_option(self, state: TradingState, symbol: str, store: dict, context: dict) -> List[Order]:
        depth = state.order_depths.get(symbol)
        vex_depth = state.order_depths.get(VEX)
        option_mid = mid_price(depth)
        vex_mid = mid_price(vex_depth)
        spread_value = spread(depth)
        if depth is None or option_mid is None or vex_mid is None or spread_value is None:
            return []
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []

        metrics = self._option_metrics(state, store, symbol, vex_mid, option_mid, depth)
        fair = metrics.get("fair")
        if fair is None:
            return []

        position = int(state.position.get(symbol, 0))
        limit = LIMITS[symbol]
        buy_cap = max(0, limit - position)
        sell_cap = max(0, limit + position)
        if buy_cap <= 0 and sell_cap <= 0:
            return []

        block_new_entries = False
        mode = self.cfg.option_mode
        if symbol == "VEV_4000":
            edge = 0.5
            max_spread = 10
            clip = 15
            band = 90
        else:
            edge = 1.0
            max_spread = 10
            clip = 12
            band = 72
        if spread_value > max_spread:
            return []
        if abs(position) >= band + 40:
            clip = min(clip, 6)
        elif abs(position) >= band:
            clip = min(clip, 8)

        if mode == "5300_horizon_hold":
            if session_progress(state.timestamp) >= 0.78:
                block_new_entries = True
            if self._position_stop_triggered(
                state,
                store,
                symbol,
                option_mid,
                min_peak=2.0,
                giveback_fraction=0.45,
                min_hold_steps=6,
            ):
                return self._flatten_product(state, symbol, max_clip=clip)
        if mode == "5300_with_5200_veto" and context["bad_5200_recent"]:
            block_new_entries = True
        if mode == "5300_option_only_veto" and context["bad_5200_recent"]:
            block_new_entries = True
        if mode == "5300_parent_gate" and not context["parent_good"]:
            block_new_entries = True
        if mode == "4000_benign_tape" and not context["benign_4000_tape"]:
            block_new_entries = True
        if mode == "4000_option_only_band" and abs(fair - option_mid) < 1.5:
            return []

        winner_style = mode in {"5300_queue_takeover", "4000_quote_ladder"}
        if winner_style:
            return self._winner_style_option_orders(
                state=state,
                symbol=symbol,
                depth=depth,
                fair=fair,
                clip=clip,
                block_new_entries=block_new_entries,
            )
        return self._simple_option_orders(
            state=state,
            symbol=symbol,
            depth=depth,
            fair=fair,
            edge=0.5 if mode == "5300_direct_dislocation" else edge,
            clip=clip,
            max_spread=max_spread,
            block_new_entries=block_new_entries,
            always_quote=(mode == "4000_forced_activation"),
            take_only=(mode == "5300_direct_dislocation"),
        )

    def _simple_option_orders(
        self,
        state: TradingState,
        symbol: str,
        depth,
        fair: float,
        edge: float,
        clip: int,
        max_spread: int,
        block_new_entries: bool,
        always_quote: bool = False,
        take_only: bool = False,
    ) -> List[Order]:
        bid, ask = best_bid_ask(depth)
        spread_value = spread(depth)
        if bid is None or ask is None or spread_value is None:
            return []
        position = int(state.position.get(symbol, 0))
        buy_cap = max(0, LIMITS[symbol] - position)
        sell_cap = max(0, LIMITS[symbol] + position)
        block_buy = block_new_entries and position >= 0
        block_sell = block_new_entries and position <= 0

        orders: List[Order] = []
        if buy_cap > 0 and not block_buy and ask <= fair - edge:
            take_qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, ask, take_qty))
                buy_cap -= take_qty
        if sell_cap > 0 and not block_sell and bid >= fair + edge:
            take_qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, bid, -take_qty))
                sell_cap -= take_qty

        should_quote = (spread_value <= max_spread - 2) and not take_only
        if should_quote or always_quote:
            if buy_cap > 0 and not block_buy:
                bid_px = min(bid + 1, clamp_floor(fair))
                bid_px = max(1, bid_px)
                post_qty = min(max(1, clip // 2), buy_cap)
                orders.append(Order(symbol, bid_px, post_qty))
            if sell_cap > 0 and not block_sell:
                ask_px = max(ask - 1, clamp_ceil(fair))
                post_qty = min(max(1, clip // 2), sell_cap)
                orders.append(Order(symbol, ask_px, -post_qty))
        return self._dedupe_orders(orders)

    def _winner_style_option_orders(
        self,
        state: TradingState,
        symbol: str,
        depth,
        fair: float,
        clip: int,
        block_new_entries: bool,
    ) -> List[Order]:
        bid, ask = best_bid_ask(depth)
        if bid is None or ask is None:
            return []
        position = int(state.position.get(symbol, 0))
        buy_cap = max(0, LIMITS[symbol] - position)
        sell_cap = max(0, LIMITS[symbol] + position)
        fair_bid = clamp_floor(fair - 1.0)
        fair_ask = clamp_ceil(fair + 1.0)
        block_buy = block_new_entries and position >= 0
        block_sell = block_new_entries and position <= 0

        orders: List[Order] = []
        sent_buys = 0
        sent_sells = 0

        if buy_cap > 0 and not block_buy and fair_bid >= ask:
            take_qty = min(clip, buy_cap, max(0, -depth.sell_orders.get(ask, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, ask, take_qty))
                buy_cap -= take_qty
                sent_buys += take_qty
        if sell_cap > 0 and not block_sell and fair_ask <= bid:
            take_qty = min(clip, sell_cap, max(0, depth.buy_orders.get(bid, 0)))
            if take_qty > 0:
                orders.append(Order(symbol, bid, -take_qty))
                sell_cap -= take_qty
                sent_sells += take_qty

        if buy_cap > 0 and not block_buy:
            post_qty = min(max(1, clip // 2), buy_cap)
            post_px = min(bid + 1, fair_bid)
            post_px = max(1, post_px)
            orders.append(Order(symbol, post_px, post_qty))
        if sell_cap > 0 and not block_sell:
            post_qty = min(max(1, clip // 2), sell_cap)
            post_px = max(ask - 1, fair_ask)
            orders.append(Order(symbol, post_px, -post_qty))
        return self._dedupe_orders(orders)

    def _option_metrics(self, state: TradingState, store: dict, symbol: str, vex_mid: float, option_mid: float, depth) -> dict:
        strike = STRIKES[symbol]
        tte = tte_years(state.timestamp)
        intrinsic = intrinsic_value(vex_mid, strike)
        clean_mid = max(option_mid, intrinsic)
        depth_imb = imbalance(depth)
        last_vex_mid = store.get("last_mid", {}).get(VEX)
        vex_move = 0.0 if last_vex_mid is None else vex_mid - last_vex_mid

        if symbol == "VEV_4000":
            heuristic_fair = intrinsic + 3.0 + 0.55 * vex_move + 0.4 * depth_imb
            heuristic_cap = 4.0
        else:
            heuristic_fair = intrinsic + 6.0 + 0.70 * vex_move + 0.5 * depth_imb
            heuristic_cap = 10.0
        heuristic_fair = max(heuristic_fair, intrinsic)

        current_iv = implied_volatility(clean_mid, vex_mid, strike, tte)
        histories = store.setdefault("iv_history", {})
        history = list(histories.get(symbol, []))
        if current_iv is not None and current_iv > 0:
            history.append(float(current_iv))
        history = rolling_slice(history, 16)
        histories[symbol] = history
        iv_mean = mean(history)
        if iv_mean is None:
            iv_mean = current_iv
        if iv_mean is None:
            return {"fair": heuristic_fair, "delta": None, "iv_mean": None, "heuristic_fair": heuristic_fair}

        bs_fair = bs_call(vex_mid, strike, tte, iv_mean)
        bs_fair = max(bs_fair, intrinsic)
        if symbol == "VEV_4000":
            fair = 0.60 * heuristic_fair + 0.40 * bs_fair
        else:
            fair = min(bs_fair, heuristic_fair + heuristic_cap)
        fair = max(fair, intrinsic)
        delta = bs_delta(vex_mid, strike, tte, iv_mean)
        return {
            "fair": fair,
            "delta": delta,
            "iv_mean": iv_mean,
            "heuristic_fair": heuristic_fair,
            "bs_fair": bs_fair,
        }

    def _update_mid_cache(self, state: TradingState, store: dict) -> None:
        last_mid = dict(store.get("last_mid", {}))
        for symbol in [VEX] + FAMILY_SYMBOLS:
            value = mid_price(state.order_depths.get(symbol))
            if value is not None:
                last_mid[symbol] = value
        store["last_mid"] = last_mid

    def _dedupe_orders(self, orders: List[Order]) -> List[Order]:
        merged: Dict[Tuple[str, int], int] = {}
        for order in orders:
            key = (order.symbol, order.price)
            merged[key] = merged.get(key, 0) + int(order.quantity)
        deduped: List[Order] = []
        for (symbol, price), quantity in merged.items():
            if quantity != 0:
                deduped.append(Order(symbol, price, quantity))
        return deduped


class Trader(SharedWave2Trader):
    def __init__(self):
        super().__init__('r4_w2_12_5300_option_only_veto')
