# Spec: R2-CAND-07 Combined IPR + ACO Imbalance

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-07-COMBINED-IPR-ACO-IMBALANCE`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 products and 80-unit limits.
- EDA evidence: IPR drift/residual; ACO top imbalance; cross-product lead-lag weak.
- Understanding summary: product-specific first; combine only if simple.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: best first final-bot path.
- Signals used: IPR drift FV/residual; ACO top imbalance; shared spread/inventory controls.
- Alternatives considered: combined reversal C08, single-product C01/C04.
- Why selected: combines strongest independent product-specific signals without cross-product dependency.
- Known caveats: must attribute PnL by product; combined inventory/risk can hide weak module.

## Evidence Traceability

- Linked EDA Signals: IPR drift plus residual; top imbalance; spread regime.
- Feature Evidence: IPR drift R2 near `1.000`; ACO top imbalance controlled coefficient `2.31`.
- Multivariate Evidence: cross-product lead-lag rejected, so modules are independent.
- Process / Distribution Assumptions: IPR drift/residual; ACO top-book pressure.
- Redundancy Decisions: one primary edge per product; no microprice stack.
- Regime Assumptions: spread gates execution quality for both products.
- Understanding Insight: product-specific branches before combining.
- Evidence gaps or strategy assumptions: combined behavior needs attribution validation.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade IPR and ACO independent modules | smoke test both products |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift FV/residual | IPR order book, timestamp, prior IPR mids | usable online | direct fair-value module | C01 params: warmup `20`, slope alpha `0.05`, edge `1`, clip `8` | residual coefficients about `-1.41` | IPR trend plus residual mean reversion | keep | disable IPR module until warm | IPR mid/slope state | product PnL and residual markout |
| ACO top imbalance | ACO top volumes/prices | usable online | direct quote-skew module | C04 params: imbalance threshold `0.15`, skew `2.0`, clip `8` | h1 coef `2.31`, p=0 | top-book pressure predicts near move | keep over microprice | disable ACO signal if depth missing | none | ACO markout by imbalance |
| spread filter | best bid/ask spreads | usable online | execution filter | per-product spread normal max `4` | spread evidence | spread gates fills | keep one spread field | disable affected product if invalid | none | PnL/fills by spread |
| inventory controls | positions | usable online | risk control | limit 80 each; soft band +/-40 each | none | independent product risk | keep | assume 0 if missing | none | no aggregate rejection |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| cross-product lead-lag | weak evidence | platform logs show coupling |
| ACO microprice | redundant challenger to top imbalance | C05 beats C04 |
| trade pressure | needs logs | reliable market-trades logs exist |
| MAF bid | separate mechanics decision | final MAF spec approved |

## Signal / Fair Value Logic

- Signal: IPR module uses drift FV/residual; ACO module uses top imbalance FV skew.
- Inputs: product-specific order books, positions, `traderData` for IPR.
- Missing-signal behavior: disable only affected product module.
- Process assumption that would invalidate this logic: either product-specific process fails in validation.
- Multivariate or redundancy caveat: no cross-product signal; no microprice stack.

## Execution Logic

- Buy behavior: per-product buy when module FV exceeds best ask by at least `1`.
- Sell behavior: per-product sell when best bid exceeds module FV by at least `1`.
- Passive/resting order behavior: per-product passive quotes only if spread permits.
- Stay-idle behavior: missing book/signal, invalid spread, or no capacity for that product.

## Position And Risk Handling

- Position limits: 80 absolute per product.
- Aggregate buy capacity: `80 - position[product]`.
- Aggregate sell capacity: `80 + position[product]`.
- Inventory skew or reduction: independent soft band +/-40; never use one product to hedge the other.

## State And Runtime

- `traderData` use: IPR drift state; optional per-product diagnostics.
- Imports: standard library only.
- Runtime risk: O(1) per product.
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: one module carries losses hidden by the other.
- Mitigation or validation: product PnL attribution.
- Failure case: combined order flow increases inventory risk.
- Mitigation or validation: position trace and per-product capacity checks.

## Validation Plan

- Contract checks: both products appear only when books exist; `bid()` returns int.
- Order sign and limit checks: per-product aggregate capacity.
- Performance/run checks: total PnL, product PnL, module markouts, spread buckets.
- Debug signals to inspect: IPR FV/residual, ACO imbalance/FV, positions.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_07_combined_ipr_aco_imbalance.py`
- Parameters to implement: C01 IPR params plus C04 ACO params; shared spread max `4`, soft band `40`.
- Known caveats: not approved for implementation until review outcome is recorded.
