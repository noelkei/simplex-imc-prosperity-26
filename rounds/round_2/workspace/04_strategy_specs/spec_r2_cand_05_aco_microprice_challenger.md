# Spec: R2-CAND-05 ACO Microprice Challenger

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-05-ACO-MICROPRICE-CHALLENGER`
- Candidate priority tier: `validate-next`
- Evidence strength: `medium`
- Product scope: `ASH_COATED_OSMIUM`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 ACO limit 80.
- EDA evidence: microprice deviation is plausible but redundant with top imbalance.
- Understanding summary: microprice should be one-axis challenger, not stacked.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: one-axis challenger to C04.
- Signals used: microprice deviation from top-of-book prices and volumes.
- Alternatives considered: top imbalance C04.
- Why selected: may compact top pressure and spread information better.
- Known caveats: correlation with top imbalance about `0.959`.

## Evidence Traceability

- Linked EDA Signals: microprice deviation.
- Feature Evidence: plausible top-book pressure transformation.
- Multivariate Evidence: high redundancy with top imbalance.
- Process / Distribution Assumptions: top-book pressure predicts near move.
- Redundancy Decisions: replace top imbalance, never stack first.
- Regime Assumptions: top-book volumes are meaningful online.
- Understanding Insight: microprice is a challenger only.
- Evidence gaps or strategy assumptions: must beat C04 to remain.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade only ACO using microprice deviation | smoke test |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| microprice deviation | best bid/ask prices and volumes | usable online | direct signal challenger | microprice = `(ask * bid_vol + bid * ask_vol)/(bid_vol + ask_vol)`; deviation = microprice - mid; threshold `0.75` ticks | corr with top imbalance about `0.959` | microprice captures pressure | challenger, not stack | stay idle if depth missing | none | reject unless beats C04 net PnL or robustness |
| spread filter | best bid/ask spread | usable online | execution filter | normal spread `<= 4` | spread filter evidence | spread gates execution | keep | stay idle if invalid | none | PnL by spread |
| inventory skew | current position | usable online | risk control | clip `8`; soft band +/-40 | none | inventory risk | keep | assume 0 if missing | none | no rejections |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| top imbalance | redundant primary signal; C05 must replace C04 | combined spec explicitly tests stack after C04/C05 evidence |
| full-book depth | separate backup candidate | top-book variants fail under depth regimes |
| reversal delta | separate process candidate | later combined candidate justifies it |

## Signal / Fair Value Logic

- Signal: microprice deviation shifts fair value toward the side implied by top-book depth.
- Inputs: best bid/ask prices and volumes.
- Missing-signal behavior: stay idle.
- Process assumption that would invalidate this logic: microprice does not improve markout over simple imbalance.
- Multivariate or redundancy caveat: direct substitute for top imbalance.

## Execution Logic

- Buy behavior: buy best ask when microprice-adjusted FV exceeds ask by at least `1`.
- Sell behavior: sell best bid when bid exceeds microprice-adjusted FV by at least `1`.
- Passive/resting order behavior: skew passive quotes by deviation sign when spread permits.
- Stay-idle behavior: missing depth, weak deviation, spread invalid, or no capacity.

## Position And Risk Handling

- Position limits: ACO absolute 80.
- Aggregate buy capacity: `80 - position`.
- Aggregate sell capacity: `80 + position`.
- Inventory skew or reduction: reduce same-side orders outside +/-40.

## State And Runtime

- `traderData` use: optional diagnostics only.
- Imports: standard library only.
- Runtime risk: O(1).
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: microprice is redundant but noisier than imbalance.
- Mitigation or validation: direct head-to-head vs C04.
- Failure case: depth signs/volumes mishandled.
- Mitigation or validation: unit/smoke checks on buy/sell volume signs.

## Validation Plan

- Contract checks: standard Trader smoke.
- Order sign and limit checks: aggregate capacity by side.
- Performance/run checks: C05 vs C04 PnL, markout, fills, inventory.
- Debug signals to inspect: microprice, mid, deviation, spread, position.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_05_aco_microprice_challenger.py`
- Parameters to implement: deviation threshold `0.75`, edge threshold `1`, spread max `4`, clip `8`, soft band `40`.
- Known caveats: not approved for implementation until review outcome is recorded.
