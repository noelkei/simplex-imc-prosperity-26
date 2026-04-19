# Spec: R2-CAND-03 ACO Reversal Maker

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-03-ACO-REVERSAL-MAKER`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium/high`
- Product scope: `ASH_COATED_OSMIUM`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 ACO limit 80; `Trader.run()` contract.
- EDA evidence: ACO short-horizon mean reversion.
- Understanding summary: ACO reversal needs execution discipline.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: direct test of ACO process hypothesis.
- Signals used: previous mid delta from online order books.
- Alternatives considered: top imbalance C04; microprice C05.
- Why selected: mean delta AC1 around `-0.500` supports reversal framing.
- Known caveats: spread and adverse selection can erase the edge.

## Evidence Traceability

- Linked EDA Signals: ACO short-horizon reversal.
- Feature Evidence: negative delta autocorrelation.
- Multivariate Evidence: controlled/process evidence supports reversal framing.
- Process / Distribution Assumptions: short-horizon mean-reverting microstructure.
- Redundancy Decisions: separate from top imbalance; do not stack first.
- Regime Assumptions: reversal effect is tradable when spread is reasonable.
- Understanding Insight: ACO needs reversal plus execution discipline.
- Evidence gaps or strategy assumptions: fill quality must validate.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade only ACO based on reversal signal | smoke test |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mid delta | ACO best bid/ask current and previous mid | usable online | direct signal | fair adjustment `-0.5 * last_delta`; require at least 1 prior mid | ACO reversal evidence | recent move partially reverses | keep | stay idle until previous mid exists | previous ACO mid | invalidate if markout has same sign as delta |
| spread filter | best bid/ask spread | usable online | execution filter | allow entry spread `<= 4`; reduce above `4` | spread filter evidence | spread gates profitability | keep | stay idle if invalid | none | PnL by spread |
| inventory skew | current position | usable online | risk control | clip `8`; soft band +/-40 | none | inventory risk | keep | assume 0 if missing | none | no limit rejections |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| top imbalance | separate candidate C04 | C03 underperforms and C04 validates |
| microprice | redundant challenger | one-axis C05 beats top imbalance |
| trade pressure | needs logs | reliable `market_trades` evidence exists |

## Signal / Fair Value Logic

- Signal: last mid delta predicts partial reversal.
- Inputs: current mid, previous mid, spread, position.
- Missing-signal behavior: store mid and stay idle on first tick.
- Process assumption that would invalidate this logic: ACO moves persist rather than reverse.
- Multivariate or redundancy caveat: do not co-primary stack with top imbalance.

## Execution Logic

- Buy behavior: if last delta is negative and best ask is at or below reversal-adjusted FV, buy up to clip.
- Sell behavior: if last delta is positive and best bid is at or above reversal-adjusted FV, sell up to clip.
- Passive/resting order behavior: optionally post one passive quote on the reversal side when spread permits and edge is weak.
- Stay-idle behavior: no prior mid, spread too wide, edge below `1`, or no capacity.

## Position And Risk Handling

- Position limits: ACO absolute 80.
- Aggregate buy capacity: `80 - position`.
- Aggregate sell capacity: `80 + position`.
- Inventory skew or reduction: reduce clip outside +/-40; avoid adding near limits.

## State And Runtime

- `traderData` use: previous ACO mid and last delta.
- Imports: standard library only.
- Runtime risk: O(1).
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: fills occur just before continuation, not reversal.
- Mitigation or validation: markout by last-delta bucket.
- Failure case: spread capture insufficient.
- Mitigation or validation: PnL by spread regime.

## Validation Plan

- Contract checks: `Trader.run`, `bid`, return shape.
- Order sign and limit checks: ACO order signs and capacity.
- Performance/run checks: ACO-only PnL, fill markout, reversal bucket PnL.
- Debug signals to inspect: mid, last_delta, adjusted FV, spread, position.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_03_aco_reversal_maker.py`
- Parameters to implement: reversal coefficient `0.5`, edge threshold `1`, spread max `4`, clip `8`, soft band `40`.
- Known caveats: not approved for implementation until review outcome is recorded.
