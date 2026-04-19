# Spec: R2-CAND-06 ACO Full-Book Depth Backup

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-06-ACO-FULL-BOOK-DEPTH-BACKUP`
- Candidate priority tier: `backlog`
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
- EDA evidence: full-book imbalance and depth regime are backup/context.
- Understanding summary: top imbalance first; full-book only if top-book weakens.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: depth-aware backup.
- Signals used: visible depth across available bid/ask levels.
- Alternatives considered: top imbalance C04.
- Why selected: preserves a deeper-book hypothesis for specific regimes.
- Known caveats: weaker and more complex than top-book.

## Evidence Traceability

- Linked EDA Signals: full-book imbalance, depth regime.
- Feature Evidence: EDA positive but lower priority than top-book.
- Multivariate Evidence: controlled/redundancy notes favor top imbalance first.
- Process / Distribution Assumptions: liquidity regimes can change execution quality.
- Redundancy Decisions: backup/context only.
- Regime Assumptions: depth matters most under wide or one-sided regimes.
- Understanding Insight: full-book imbalance should not be co-primary first.
- Evidence gaps or strategy assumptions: needs trigger from validation weakness.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement only if reviewed | trade ACO using depth imbalance | smoke test |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| full-book imbalance | all visible bid/sell volumes in ACO `OrderDepth` | usable online | direct signal / backup | sum all bid vols and abs sell vols; threshold `0.20`; clip `6` | weaker than top imbalance | deeper book can predict regimes | downgraded backup | disable if depth sum <= 0 | none | validate only in regimes where C04 weakens |
| depth regime | total visible depth | usable online | execution filter | low depth if total < rolling median proxy or < `20`; reduce size | regime evidence | low depth worsens fills | exploratory | neutral if unavailable | optional rolling depth count | PnL/fills by depth bucket |
| spread filter | best bid/ask spread | usable online | execution filter | allow spread `<= 5`, but reduce above `4` | spread evidence | spread gates execution | keep | stay idle if invalid | none | PnL by spread |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| top imbalance | primary candidate already covers simpler signal | C04 weakens in depth regimes |
| microprice | separate top-book challenger | C05 validates |
| trade pressure | needs logs | reliable market-trades logs exist |

## Signal / Fair Value Logic

- Signal: full-book imbalance shifts fair value toward deeper bid or ask pressure.
- Inputs: visible order depth levels.
- Missing-signal behavior: stay idle.
- Process assumption that would invalidate this logic: deeper levels add no predictive or execution value.
- Multivariate or redundancy caveat: lower priority than top imbalance.

## Execution Logic

- Buy behavior: buy when depth-adjusted FV exceeds best ask by at least `1`.
- Sell behavior: sell when best bid exceeds depth-adjusted FV by at least `1`.
- Passive/resting order behavior: quote smaller size than C04 due lower confidence.
- Stay-idle behavior: depth sum zero, missing book, spread invalid, or no capacity.

## Position And Risk Handling

- Position limits: ACO absolute 80.
- Aggregate buy capacity: `80 - position`.
- Aggregate sell capacity: `80 + position`.
- Inventory skew or reduction: clip `6`, reduce outside +/-32.

## State And Runtime

- `traderData` use: optional rolling depth diagnostic only.
- Imports: standard library only.
- Runtime risk: O(levels), bounded by visible book size.
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: depth feature adds noise and complexity.
- Mitigation or validation: compare only after C04/C09 baseline.
- Failure case: visible depth distribution differs in platform subset.
- Mitigation or validation: platform subset diagnostics.

## Validation Plan

- Contract checks: standard Trader smoke.
- Order sign and limit checks: aggregate capacity.
- Performance/run checks: conditional PnL by spread/depth regime.
- Debug signals to inspect: depth sums, full imbalance, spread, position.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_06_aco_full_book_depth_backup.py`
- Parameters to implement: imbalance threshold `0.20`, spread max `5`, clip `6`, soft band `32`, optional low-depth threshold `20`.
- Known caveats: backlog candidate; not approved for implementation until review outcome is recorded.
