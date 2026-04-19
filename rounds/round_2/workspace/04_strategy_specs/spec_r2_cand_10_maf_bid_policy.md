# Spec: R2-CAND-10 Market Access Fee Bid Policy

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-10-MAF-BID-POLICY`
- Candidate priority tier: `spec-first`
- Evidence strength: `medium`
- Product scope: Round 2 final mechanics only
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 Market Access Fee via `Trader.bid()`.
- EDA evidence: `maf_scenarios.csv` opportunity proxy.
- Understanding summary: MAF is separate mechanics/risk decision, not `Trader.run()` alpha.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: required final-round mechanics decision.
- Signals used: MAF scenario table and risk posture.
- Alternatives considered: no bid, low bid, base bid, aggressive bid.
- Why selected: extra 25% quote access may increase opportunity set.
- Known caveats: competitor bid distribution unknown; testing ignores `bid()`.

## Evidence Traceability

- Linked EDA Signals: MAF scenario table.
- Feature Evidence: incremental proxy about `78-786` at threshold 0 depending capture rate.
- Multivariate Evidence: not applicable.
- Process / Distribution Assumptions: extra visible quotes may increase executable opportunities.
- Redundancy Decisions: not a normal feature; do not mix into Signal Ledger.
- Regime Assumptions: final access changes visible order book, not matching rules.
- Understanding Insight: final bid belongs in reviewed spec/human risk decision.
- Evidence gaps or strategy assumptions: accepted bid distribution is unknown.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.bid()` | Round 2 wiki | blocked pending risk posture | define final one-time bid only after review | method returns integer |
| `Trader.run()` | wiki contract | not standalone | pair with final champion bot; no alpha changes | champion validation remains separate |
| Testing ignores `bid()` | Round 2 wiki | record caveat | do not interpret test PnL as bid-inclusive | run summary caveat |
| Manual RSS | Round 2 wiki | not applicable | no effect on MAF | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MAF bid | static reviewed integer | Round 2 final only | round-specific mechanic | default pending review: `0`; candidate risk scenarios: low/base/aggressive | none | extra quotes may add opportunity | separate mechanics-only | if no review, return `0` | none | final decision audit; cannot validate in normal tests |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| MAF as alpha signal | fee affects access, not normal signal logic | official docs change |
| manual RSS | separate challenge | official docs merge mechanics |
| exact PnL bid optimizer | competitor bids unknown | reliable competitor distribution exists |

## Signal / Fair Value Logic

- Signal: none. This spec only controls `Trader.bid()`.
- Inputs: reviewed static bid amount.
- Missing-signal behavior: if no explicit risk posture is reviewed, return `0`.
- Process assumption that would invalidate this logic: MAF value proxy is negative or too uncertain.
- Multivariate or redundancy caveat: none.

## Execution Logic

- Buy behavior: inherited from paired champion; no change here.
- Sell behavior: inherited from paired champion; no change here.
- Passive/resting order behavior: inherited from paired champion.
- Stay-idle behavior: not applicable.

## Position And Risk Handling

- Position limits: inherited from paired champion.
- Aggregate buy capacity: inherited from paired champion.
- Aggregate sell capacity: inherited from paired champion.
- Inventory skew or reduction: inherited from paired champion.
- Fee risk: accepted bid subtracts directly from Round 2 profits; rejected bid pays nothing.

## State And Runtime

- `traderData` use: none.
- Imports: none required.
- Runtime risk: none.
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: overpay for access.
- Mitigation or validation: choose conservative/base/aggressive posture explicitly.
- Failure case: bid rejected and no extra access.
- Mitigation or validation: final summary records acceptance uncertainty.

## Validation Plan

- Contract checks: `bid()` exists and returns integer.
- Order sign and limit checks: not applicable to bid itself.
- Performance/run checks: normal testing ignores bid; record caveat.
- Debug signals to inspect: final chosen bid and rationale.

## Implementation Handoff

- Target bot path: not standalone. Apply reviewed `bid()` policy to the final champion bot in `rounds/round_2/bots/noel/canonical/`.
- Parameters to implement: default `0` until risk posture is reviewed; low/base/aggressive bid values must be selected by human review.
- Known caveats: mechanics-only and not approved for implementation until review outcome is recorded.
