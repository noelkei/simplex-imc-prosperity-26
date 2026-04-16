# Spec: candidate_01_ipr_drift_mm

## Review Status

- Status: READY_FOR_REVIEW
- Owner: Claude
- Reviewer: Unassigned
- Reviewed on: —

## Candidate

- Candidate ID: `candidate_01_ipr_drift_mm`
- Shortlist priority: high
- Evidence strength: strong
- Product scope: `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `../03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: not reviewed
- Approved for implementation: yes (as reference for combined)
- Reviewer decision notes: approved 2026-04-16
- Required changes before coding: none anticipated

---

## Sources

- Wiki facts: `workspace/00_ingestion.md` — position limit ±80, order sign conventions
- EDA evidence: `workspace/01_eda/eda_round_1.md` — IPR drift slope 0.001/tick, R²=0.9999, spread ~13, one-sided/zero rows
- Understanding summary: `workspace/02_understanding.md` — drifting FV model, day-start assumption
- Playbook heuristics: none

## Evidence Traceability

- Linked EDA Signals: `FV(t) = day_start + 0.001 × t`, R²=0.9999 across 3 days; residual std ≈ 2 units
- Feature Evidence: `mid_price`, `timestamp`, per-day linear fit; spread (ask1−bid1) mean=13.05 std=2.63
- Regime Assumptions: drift slope stable across days; day-start ≈ first valid mid_price of the day
- Understanding Insight: IPR price is predictably steady via linear drift — quoting a static mid-price loses ~0.001 × position per tick
- Evidence gaps: slope in live round unobserved; day-start level after day 0 unknown (assumed estimable from tick 0)

---

## Signal / Fair Value Logic

- **Signal**: Linear drift fair value per tick  
  `FV(t) = day_start + 0.001 × timestamp`  
  where `day_start` = first valid (non-zero) `mid_price` observed at runtime for that day, and `timestamp` = current `TradingState.timestamp`.
- **Inputs**: `TradingState.timestamp`, `TradingState.order_depths["INTARIAN_PEPPER_ROOT"]` (mid_price proxy), `traderData` for day_start persistence.
- **Missing-signal behavior**:
  - If `mid_price = 0` (both sides null): skip quoting this tick; do not update day_start; use last known FV.
  - If only one side present: compute mid_price as that side's price; still update FV normally.
  - If `day_start` not yet set (first tick is zero): defer to next valid tick; do not quote until day_start is established.

---

## Execution Logic

**Parameters** (visible, not hidden):

| Parameter | Value | Rationale |
| --- | --- | --- |
| `SPREAD_BUFFER` | 4 | Half-spread ~6.5; buffer of 4 ensures edge above residual noise (~2 units) |
| `ORDER_SIZE` | 20 | Conservative; position limit 80, allows 4 round trips |
| `MAX_POSITION` | 75 | Leave 5-unit buffer below hard limit of 80 |

- **Buy behavior**: If `best_ask` exists and `best_ask < FV(t) - SPREAD_BUFFER`: send buy order at `best_ask`, quantity = `min(ORDER_SIZE, MAX_POSITION - current_position)`. Skip if capacity ≤ 0.
- **Sell behavior**: If `best_bid` exists and `best_bid > FV(t) + SPREAD_BUFFER`: send sell order at `best_bid`, quantity = `min(-ORDER_SIZE, -MAX_POSITION - current_position)` (negative). Skip if capacity ≤ 0.
- **Passive/resting orders**: Not used in this spec. All orders are market-crossing limit orders placed at best counterparty price.
- **Stay-idle behavior**: If no order book side satisfies the threshold, or if position capacity is 0, emit no orders for this product this tick.

---

## Position And Risk Handling

- Position limits: ±80 (wiki-defined absolute limit)
- Aggregate buy capacity per tick: `MAX_POSITION - current_position` (never exceed 75 net long)
- Aggregate sell capacity per tick: `MAX_POSITION + current_position` (never exceed 75 net short)
- Inventory skew: not in this spec variant; handled via capacity clipping. If position approaches ±MAX_POSITION, order size naturally drops to 0.
- All submitted orders in one tick must not aggregate beyond capacity — ensure single order per side per tick.

---

## State And Runtime

- **`traderData` use**: serialize `day_start` as a float string (e.g. `"IPR_DS:10000.5"`). Parse on each call. If string is missing or malformed, treat as not yet set.
- **Imports**: `json` or simple string parsing; `datamodel.Order`, `datamodel.TradingState`.
- **Runtime risk**: `traderData` string grows if other strategies also use it — use a prefixed key pattern to avoid clobbering. Total string must stay within platform limits (assume safe at this size).

---

## Expected Failure Cases

| Failure Case | Mitigation |
| --- | --- |
| day_start never set (all tick-0 rows are zero mid_price) | Defer quoting; set day_start from first non-zero tick |
| Drift slope differs from 0.001 in live round | FV will diverge; observable as consistent adverse fills. Spec does not auto-adapt — treat as a caveat for first validation run |
| Position limit violation (orders cancelled by exchange) | Capacity clipping prevents this if implemented correctly; validate in backtest |
| One-sided book on both sides simultaneously | Handled by missing-signal behavior — skip tick |

---

## Validation Plan

- **Contract checks**: `run()` returns `(result, conversions, traderData)`; `result["INTARIAN_PEPPER_ROOT"]` is a list of `Order` objects with correct sign; `traderData` is a non-None string.
- **Order sign checks**: buy orders have positive quantity; sell orders have negative quantity.
- **Position limit checks**: no tick results in `|position| > 80`; no single tick submits aggregated buy > `80 - current_position` or sell > `80 + current_position`.
- **Performance checks**: over backtest on days −2, −1, 0 — P&L should be positive; position should not rail at ±80 for extended periods.
- **Debug signals**: log `FV(t)`, `best_bid`, `best_ask`, `current_position`, and orders placed each tick during validation.

---

## Implementation Handoff

- Target bot path: `rounds/round_1/bots/<member>/canonical/`
- Parameters to implement: `SPREAD_BUFFER=4`, `ORDER_SIZE=20`, `MAX_POSITION=75`
- Known caveats:
  - day_start must be persisted in `traderData` with a namespaced key
  - slope 0.001 is hardcoded — flag for observation in live round
  - zero mid_price rows must be filtered before updating FV or day_start
