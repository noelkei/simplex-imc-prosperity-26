# Spec: R2-CAND-09 Spread Defensive Overlay

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-09-SPREAD-DEFENSIVE-OVERLAY`
- Candidate priority tier: `validate-next`
- Evidence strength: `medium`
- Product scope: both products as overlay
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 products and limits.
- EDA evidence: spread regime promoted as execution/risk filter, not alpha.
- Understanding summary: spread should be execution/risk filter.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: execution-quality overlay.
- Signals used: per-product best-bid/best-ask spread.
- Alternatives considered: no spread gating in base candidates.
- Why selected: likely improves fill/markout quality across candidates.
- Known caveats: can over-filter and reduce profitable fills.

## Evidence Traceability

- Linked EDA Signals: spread regime.
- Feature Evidence: promoted execution/risk filter.
- Multivariate Evidence: spread/relative spread redundancy favors one spread field.
- Process / Distribution Assumptions: liquidity/execution regimes matter.
- Redundancy Decisions: use absolute spread only.
- Regime Assumptions: wide spreads have different execution quality.
- Understanding Insight: spread is filter, not standalone alpha.
- Evidence gaps or strategy assumptions: must be paired with base candidate.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement only as overlay | modify parent candidate execution, not standalone alpha | compare parent with/without overlay |
| `Trader.bid()` | Round 2 wiki | exclude | return parent value or `0` unless MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| spread regime | best bid/ask per product | usable online | execution filter / risk control | normal spread `<= 4`; defensive spread `5-6`; idle spread `> 6`; product-specific override allowed in parent spec | spread evidence | wide spreads change fill quality | keep absolute spread, drop relative spread | disable affected product if invalid | none | keep only if parent PnL/markout improves |
| size throttle | parent desired order size | usable online | risk control | normal 100%, defensive 50%, idle 0% | none | smaller size reduces adverse fills | keep | no orders if parent size unavailable | none | compare fill quality |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| alpha signal from spread alone | no standalone alpha evidence | spread-only PnL evidence appears |
| relative spread | redundant with spread | cross-product comparability requires it |
| depth regime | separate backup | spread overlay insufficient |

## Signal / Fair Value Logic

- Signal: none standalone; spread changes whether parent signals may trade and at what size.
- Inputs: spread and parent candidate desired orders.
- Missing-signal behavior: if spread invalid, block affected product orders.
- Process assumption that would invalidate this logic: spread filter reduces good fills more than bad fills.
- Multivariate or redundancy caveat: not alpha, do not count as primary signal.

## Execution Logic

- Buy behavior: allow, throttle, or block parent buy orders by spread regime.
- Sell behavior: allow, throttle, or block parent sell orders by spread regime.
- Passive/resting order behavior: parent-defined, then overlay applies size/gate.
- Stay-idle behavior: idle regime, missing spread, or no parent signal.

## Position And Risk Handling

- Position limits: inherited from parent spec.
- Aggregate buy capacity: parent capacity after spread throttle.
- Aggregate sell capacity: parent capacity after spread throttle.
- Inventory skew or reduction: parent inventory controls remain authoritative.

## State And Runtime

- `traderData` use: optional diagnostics only.
- Imports: standard library only.
- Runtime risk: O(1).
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: over-filtering reduces PnL.
- Mitigation or validation: parent vs overlay A/B.
- Failure case: spread threshold too static.
- Mitigation or validation: PnL by spread bucket.

## Validation Plan

- Contract checks: overlay must preserve parent return contract.
- Order sign and limit checks: parent order signs/capacity remain valid after throttle.
- Performance/run checks: parent vs overlay PnL, fill count, average markout.
- Debug signals to inspect: spread regime, parent size, throttled size.

## Implementation Handoff

- Target bot path: overlay variant of reviewed parent, e.g. `rounds/round_2/bots/noel/canonical/candidate_r2_cand_09_spread_defensive_overlay.py` only if paired with a parent.
- Parameters to implement: normal `<=4`, defensive `5-6`, idle `>6`, defensive size multiplier `0.5`.
- Known caveats: not a standalone bot; not approved for implementation until review outcome and parent pairing are recorded.
