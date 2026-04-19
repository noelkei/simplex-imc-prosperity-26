# Spec: R2-CAND-08 Combined IPR + ACO Reversal

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-08-COMBINED-IPR-ACO-REVERSAL`
- Candidate priority tier: `implement-first`
- Evidence strength: `high for IPR, medium/high for ACO`
- Product scope: `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 products and limits.
- EDA evidence: IPR drift/residual; ACO reversal.
- Understanding summary: compare ACO process vs top-book pressure.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: controlled final-bot challenger to C07.
- Signals used: IPR drift FV/residual; ACO previous-mid-delta reversal.
- Alternatives considered: C07 with top imbalance.
- Why selected: same IPR module, alternate ACO hypothesis.
- Known caveats: ACO reversal may be more execution-sensitive than imbalance.

## Evidence Traceability

- Linked EDA Signals: IPR drift plus residual; ACO reversal; spread regime.
- Feature Evidence: IPR strong; ACO delta AC1 about `-0.500`.
- Multivariate Evidence: no cross-product dependency.
- Process / Distribution Assumptions: IPR trend/residual; ACO mean reversion.
- Redundancy Decisions: use ACO reversal instead of top imbalance.
- Regime Assumptions: spread gates ACO reversal profitability.
- Understanding Insight: ACO reversal plus execution discipline.
- Evidence gaps or strategy assumptions: reversal execution needs fill validation.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade IPR and ACO independent modules | smoke test both products |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift FV/residual | IPR order book, timestamp, prior mids | usable online | direct FV module | same as C01 | residual evidence | IPR trend/residual | keep | disable IPR until warm | IPR state | product PnL/markout |
| ACO reversal | ACO current and previous mid | usable online | direct FV module | coefficient `0.5`, edge `1`, clip `8` | reversal evidence | ACO mean reversion | keep instead of imbalance | disable ACO until previous mid | previous ACO mid | compare to C07/C04 |
| spread filter | per-product spread | usable online | execution filter | spread max `4` | spread evidence | spread gates execution | keep | disable affected product | none | PnL by spread |
| inventory controls | positions | usable online | risk control | limit 80, soft band +/-40 | none | independent product risk | keep | assume 0 if missing | none | no aggregate rejection |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| ACO top imbalance | C08 tests reversal instead | C07/C04 outperform reversal |
| microprice | not part of reversal hypothesis | C05 validates |
| MAF bid | separate mechanics decision | final MAF spec approved |

## Signal / Fair Value Logic

- Signal: IPR drift residual plus ACO reversal-adjusted FV.
- Inputs: product order books, previous mids, positions.
- Missing-signal behavior: disable affected module.
- Process assumption that would invalidate this logic: ACO moves continue rather than reverse.
- Multivariate or redundancy caveat: no cross-product alpha.

## Execution Logic

- Buy behavior: per module, buy if adjusted FV exceeds best ask by at least `1`.
- Sell behavior: per module, sell if best bid exceeds adjusted FV by at least `1`.
- Passive/resting order behavior: conservative passive quotes only when spread permits.
- Stay-idle behavior: missing signal/book, invalid spread, or no capacity.

## Position And Risk Handling

- Position limits: 80 absolute per product.
- Aggregate buy capacity: `80 - position[product]`.
- Aggregate sell capacity: `80 + position[product]`.
- Inventory skew or reduction: independent soft band +/-40.

## State And Runtime

- `traderData` use: IPR drift state and previous ACO mid.
- Imports: standard library only.
- Runtime risk: O(1) per product.
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: ACO reversal adverse selection dominates.
- Mitigation or validation: direct comparison vs C07/C04.
- Failure case: mixed module results hide weakness.
- Mitigation or validation: product attribution.

## Validation Plan

- Contract checks: standard Trader smoke.
- Order sign and limit checks: per-product capacity.
- Performance/run checks: total/product PnL, ACO reversal buckets, comparison with C07.
- Debug signals to inspect: IPR residual, ACO last_delta, adjusted FVs, positions.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_08_combined_ipr_aco_reversal.py`
- Parameters to implement: C01 IPR params plus C03 ACO params.
- Known caveats: not approved for implementation until review outcome is recorded.
