# Strategy Spec — candidate_01_ipr_drift

## Review Status

- Status: COMPLETED
- Owner: Claude
- Reviewer: Bruno (shortlist approval 2026-04-15, deadline deferral recorded)
- Reviewed on: 2026-04-15

## Candidate

- Candidate ID: `candidate_01_ipr_drift`
- Shortlist priority: high
- Evidence strength: strong
- Product scope: `INTARIAN_PEPPER_ROOT`
- Linked candidate file: [`../03_strategy_candidates.md`](../03_strategy_candidates.md)

## Review Decision

- `_index.md` spec status: deferred under deadline
- Approved for implementation: deferred under deadline
- Required changes before coding: none

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md` (limit 80)
- EDA evidence: `rounds/round_1/workspace/01_eda/eda_round_1.md` (drift +0.001/tick, residual stdev 2.36, bot spread 12–14)
- Understanding summary: `rounds/round_1/workspace/02_understanding.md`

## Evidence Traceability

- Linked EDA Signals: IPR drift fair value in `01_eda/eda_round_1.md`
- Feature Evidence: timestamp, first usable mid, drift rate, residual to drift fair value, top-of-book spread
- Regime Assumptions: live drift rate remains close to historical sample; first usable mid is a valid day-start proxy
- Understanding Insight: IPR should trade from a drifting fair value, not a static price
- Evidence gaps or strategy assumptions: live slope/start price still require validation

## Signal / Fair Value Logic

- Signal: `fair_value(t) = day_start_price + timestamp * DRIFT_RATE`
- Inputs: `state.timestamp`, `day_start_price` (first observed mid price of the day, stored in `traderData`)
- Day reset detection: if `timestamp < last_timestamp`, clear `day_start_price` and re-initialize
- Missing-signal behavior: if `day_start_price` not yet set and no mid price available, skip all orders for this tick

## Execution Logic

- **Aggressive:** for each ask price < `fair_value`, buy up to remaining buy capacity. For each bid price > `fair_value`, sell up to remaining sell capacity.
- **Passive:** place resting buy at `round(fair_value) - HALF_SPREAD - skew`, resting sell at `round(fair_value) + HALF_SPREAD + skew`. Quantities = remaining buy/sell capacity.
- **Stay-idle:** if `day_start_price` not initialized, return no orders.

## Position And Risk Handling

- Position limit: 80
- Buy capacity per tick: `80 - current_position`
- Sell capacity per tick: `80 + current_position`
- Inventory skew: `skew = round((position / 80) * SKEW_FACTOR)`. Positive position → raise both quotes. Negative → lower both.

## Parameters

| Parameter | Default |
| --- | --- |
| `IPR_DRIFT_RATE` | `0.001` |
| `IPR_HALF_SPREAD` | `4` |
| `IPR_SKEW_FACTOR` | `2` |

## State And Runtime

- `traderData` fields: `ipr_start_price` (float), `ipr_last_ts` (int)
- Imports: `from datamodel import Order, OrderDepth, TradingState` only
- Runtime: constant-time per tick

## Expected Failure Cases

- Drift rate wrong → FV diverges from market. Monitor first 100 ticks; adjust `IPR_DRIFT_RATE` if mid deviates > 20 ticks from formula.
- Stale start price across day boundary → fixed by day-reset detection via `ipr_last_ts`.
- Position limit violation → prevented by buy_cap/sell_cap clamping.

## Validation Plan

- Order signs: positive qty = buy, negative = sell.
- Limit check: sum buy qty ≤ `80 - position`, sum sell qty ≤ `80 + position`.
- Performance: P&L should grow linearly. Flat → check FV formula. Negative → check sign convention.

## Implementation Handoff

- Target bot path: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py` (currently missing; restore or create before validation)
- Parameters at top of file, easily tunable.
