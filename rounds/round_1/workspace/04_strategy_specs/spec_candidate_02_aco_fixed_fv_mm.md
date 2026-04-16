# Spec: candidate_02_aco_fixed_fv_mm

## Review Status

- Status: READY_FOR_REVIEW
- Owner: Claude
- Reviewer: Unassigned
- Reviewed on: —

## Candidate

- Candidate ID: `candidate_02_aco_fixed_fv_mm`
- Shortlist priority: high
- Evidence strength: strong
- Product scope: `ASH_COATED_OSMIUM`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: not reviewed
- Approved for implementation: yes (as reference for combined)
- Reviewer decision notes: approved 2026-04-16
- Required changes before coding: none anticipated

---

## Sources

- Wiki facts: `workspace/00_ingestion.md` — position limit ±80, order sign conventions
- EDA evidence: `workspace/01_eda/eda_round_1.md` — ACO FV ~10000 (94.4% within ±10), trade median=10000, spread ~16, zero/one-sided rows
- Understanding summary: `workspace/02_understanding.md` — fixed-FV model, hidden-pattern caveat
- Playbook heuristics: none

## Evidence Traceability

- Linked EDA Signals: ACO mid_price (excl zeros) mean=10000.20, std=5.35; 94.4% within [9990,10010]; trade price median=10000; spread mean=16.18 std=2.57
- Feature Evidence: `mid_price` (excl zeros), `ask_price_1 - bid_price_1`, trade `price`; `deviation = mid_price - 10000`
- Regime Assumptions: FV stable at 10000 across all 3 days; no hidden pattern detected in data
- Understanding Insight: Mean-reversion to 10000 is strong; inventory skew useful to stay near flat
- Evidence gaps: "hidden pattern" wiki hint unverified; FV could shift in live round

---

## Signal / Fair Value Logic

- **Signal**: Fixed fair value  
  `FV = 10000` (constant)
- **Inputs**: `TradingState.order_depths["ASH_COATED_OSMIUM"]` (best bid, best ask, mid_price proxy).
- **Missing-signal behavior**:
  - If `mid_price = 0` (both sides null): skip quoting this tick.
  - If only one side present: still quote on the available side; compute FV-based threshold from FV=10000 directly.
  - If mid_price deviates from FV by more than `FV_ALERT_THRESHOLD` (30) for `FV_ALERT_TICKS` (50) consecutive ticks: log a warning but do not change FV — treat as a caveat to observe in first validation run. (Do not hardcode a new FV without EDA evidence.)

---

## Execution Logic

**Parameters** (visible, not hidden):

| Parameter | Value | Rationale |
| --- | --- | --- |
| `FV` | 10000 | EDA-confirmed fixed fair value |
| `SPREAD_BUFFER` | 8 | Half of mean spread ~8; ensures positive edge above noise (std=5.35) |
| `ORDER_SIZE` | 20 | Conservative; allows 4 round trips within ±80 |
| `MAX_POSITION` | 75 | 5-unit buffer below hard limit |
| `SKEW_FACTOR` | 0.1 | Fraction of position used to skew quote midpoint toward flat |
| `FV_ALERT_THRESHOLD` | 30 | Sustained mid_price deviation that triggers a log warning |
| `FV_ALERT_TICKS` | 50 | Consecutive ticks above threshold to trigger warning |

- **Buy behavior**: If `best_ask` exists and `best_ask < FV - SPREAD_BUFFER + skew_offset`: send buy order at `best_ask`, quantity = `min(ORDER_SIZE, MAX_POSITION - current_position)`. Skip if capacity ≤ 0.
- **Sell behavior**: If `best_bid` exists and `best_bid > FV + SPREAD_BUFFER + skew_offset`: send sell order at `best_bid`, quantity = `min(-ORDER_SIZE, -MAX_POSITION - current_position)` (negative). Skip if capacity ≤ 0.
- **Inventory skew**: `skew_offset = -SKEW_FACTOR × current_position`. Positive position shifts both thresholds down (encourages selling); negative position shifts up (encourages buying). This keeps the bot from building a large directional inventory.
- **Passive/resting orders**: Not used. All orders are market-crossing limit orders placed at best counterparty price.
- **Stay-idle behavior**: If no side satisfies the threshold after skew adjustment, or capacity is 0, emit no orders.

---

## Position And Risk Handling

- Position limits: ±80 (wiki-defined)
- Aggregate buy capacity per tick: `MAX_POSITION - current_position`
- Aggregate sell capacity per tick: `MAX_POSITION + current_position`
- Inventory skew reduces the effective quoting range as position diverges from 0, providing a natural mean-reversion mechanism.
- Single order per side per tick; aggregate must not exceed capacity.

---

## State And Runtime

- **`traderData` use**: Persist `aco_alert_count` (int, consecutive ticks above FV_ALERT_THRESHOLD) with namespaced key (e.g. `"ACO_AC:0"`). Parse on each call; default to 0 if missing.
- **Imports**: simple string parsing; `datamodel.Order`, `datamodel.TradingState`.
- **Runtime risk**: same `traderData` namespacing concern as spec 01 — use distinct prefixes per strategy.

---

## Expected Failure Cases

| Failure Case | Mitigation |
| --- | --- |
| ACO hidden pattern activates (price moves away from 10000) | Alert counter logged; no auto-adaptation in this spec — caveat for first validation run |
| Position rails at +75 or −75 | Inventory skew reduces order size; capacity clipping stops new orders. If persistent, reduce ORDER_SIZE or increase SKEW_FACTOR in next variant |
| Exchange rejects orders (limit violation) | Capacity clipping prevents if implemented correctly; validate in backtest |
| Zero mid_price ticks | Skip quoting; do not update alert counter |

---

## Validation Plan

- **Contract checks**: `run()` returns `(result, conversions, traderData)`; `result["ASH_COATED_OSMIUM"]` contains correctly-signed `Order` objects.
- **Order sign checks**: buy = positive quantity; sell = negative quantity.
- **Position limit checks**: `|position| ≤ 80` at all ticks; no tick submits aggregate beyond capacity.
- **Performance checks**: over backtest on days −2, −1, 0 — P&L positive; position oscillates near 0 rather than railing; inventory skew measurably reduces max position vs no-skew baseline.
- **Debug signals**: log `FV`, `best_bid`, `best_ask`, `skew_offset`, `current_position`, `aco_alert_count`, and orders placed each tick.

---

## Implementation Handoff

- Target bot path: `rounds/round_1/bots/<member>/canonical/`
- Parameters to implement: `FV=10000`, `SPREAD_BUFFER=8`, `ORDER_SIZE=20`, `MAX_POSITION=75`, `SKEW_FACTOR=0.1`, `FV_ALERT_THRESHOLD=30`, `FV_ALERT_TICKS=50`
- Known caveats:
  - FV=10000 hardcoded — observe early live ticks; flag if mid_price diverges > ±30 for >50 ticks
  - Hidden pattern unresolved — do not assume it won't appear; monitor in first validation run
  - `traderData` key must not collide with IPR spec keys
