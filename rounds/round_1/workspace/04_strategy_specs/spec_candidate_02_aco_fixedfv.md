# Strategy Spec — candidate_02_aco_fixedfv

## Review Status

- Status: COMPLETED
- Owner: Claude
- Reviewer: Bruno (shortlist approval 2026-04-15, deadline deferral recorded)
- Reviewed on: 2026-04-15

## Candidate

- Candidate ID: `candidate_02_aco_fixedfv`
- Shortlist priority: high
- Evidence strength: strong
- Product scope: `ASH_COATED_OSMIUM`
- Linked candidate file: [`../03_strategy_candidates.md`](../03_strategy_candidates.md)

## Review Decision

- `_index.md` spec status: deferred under deadline
- Approved for implementation: deferred under deadline
- Notes: historical bot `TEST1_merged.py` may contain compatible behavior, but this spec is the authoritative implementation source.
- Required changes before coding: none

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md` (limit 80)
- EDA evidence: `rounds/round_1/workspace/01_eda/eda_round_1.md` (FV=10,000, stdev 4–5, autocorr 0.79, bot spread 16)
- Understanding summary: `rounds/round_1/workspace/02_understanding.md`

## Evidence Traceability

- Linked EDA Signals: ACO fixed fair value in `01_eda/eda_round_1.md`
- Feature Evidence: mid deviation from 10,000, spread distribution, lag autocorrelation
- Regime Assumptions: live fair value remains near 10,000; reversion remains slow enough to require inventory skew
- Understanding Insight: ACO should trade from fixed FV 10,000 with inventory skew, not aggressive directional reversion
- Evidence gaps or strategy assumptions: live FV level and fill behavior still require validation

## Signal / Fair Value Logic

- Signal: `fair_value = 10000` (constant)
- Inputs: `state.order_depths["ASH_COATED_OSMIUM"]`
- Missing-signal behavior: if book is entirely empty, skip all orders for this tick

## Execution Logic

- **Aggressive:** for each ask price < `fair_value`, buy up to remaining buy capacity. For each bid price > `fair_value`, sell up to remaining sell capacity.
- **Passive:** place resting buy at `fair_value - HALF_SPREAD - skew`, resting sell at `fair_value + HALF_SPREAD + skew`.
- **Stay-idle:** if book is empty, return no orders.

## Position And Risk Handling

- Position limit: 80
- Buy capacity per tick: `80 - current_position`
- Sell capacity per tick: `80 + current_position`
- Inventory skew: `skew = round((position / 80) * SKEW_FACTOR)`. Prevents position from pinning at limit during slow reversion.

## Parameters

| Parameter | Default |
| --- | --- |
| `ACO_FAIR_VALUE` | `10000` |
| `ACO_HALF_SPREAD` | `5` |
| `ACO_SKEW_FACTOR` | `2` |

## State And Runtime

- `traderData` fields: none (stateless — FV is constant)
- Imports: `from datamodel import Order` only
- Runtime: constant-time per tick

## Expected Failure Cases

- FV wrong in live round → monitor live mid average over first 200 ticks; adjust `ACO_FAIR_VALUE` if mean deviates > 10 from 10,000.
- Position pins at ±80 → increase `ACO_SKEW_FACTOR` or reduce `ACO_HALF_SPREAD`.
- Position limit violation → prevented by buy_cap/sell_cap clamping.

## Validation Plan

- Order signs: positive qty = buy, negative = sell.
- Limit check: sum buy qty ≤ `80 - position`, sum sell qty ≤ `80 + position`.
- Performance: P&L should grow. Position should oscillate around 0.

## Implementation Handoff

- Target bot path: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py` (currently missing; restore or create before validation)
- Parameters at top of file, easily tunable.
