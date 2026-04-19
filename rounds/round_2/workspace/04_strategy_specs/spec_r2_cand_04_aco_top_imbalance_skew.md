# Spec: R2-CAND-04 ACO Top Imbalance Skew

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-04-ACO-TOP-IMBALANCE-SKEW`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `ASH_COATED_OSMIUM`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 ACO limit 80; order signs and `Trader.run()` contract.
- EDA evidence: top imbalance promoted as strongest order-book signal.
- Understanding summary: top-book pressure is first order-book feature family.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: strongest controlled ACO order-book candidate.
- Signals used: best bid volume, best ask volume, spread, position.
- Alternatives considered: microprice C05, full-book C06, reversal C03.
- Why selected: h1 standardized coefficient `2.31`, p=0, controlled R2 `0.162`.
- Known caveats: sizing and fill quality need validation; microprice is redundant challenger.

## Evidence Traceability

- Linked EDA Signals: top imbalance.
- Feature Evidence: strongest order-book signal in Understanding.
- Multivariate Evidence: ACO future mid delta vs top imbalance h1 coef `2.31`, p=0.
- Process / Distribution Assumptions: top-book pressure predicts near move.
- Redundancy Decisions: keep top imbalance over microprice first.
- Regime Assumptions: signal works best when visible top depth is meaningful.
- Understanding Insight: use one primary pressure feature.
- Evidence gaps or strategy assumptions: live sizing coefficient must validate.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade only ACO based on top imbalance | smoke test |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| top imbalance | best bid volume, best ask volume | usable online | direct signal / quote skew | imbalance = `(bid_vol - ask_vol)/(bid_vol + ask_vol)`; threshold `0.15`; FV skew coefficient `2.0` ticks | h1 coef `2.31`, p=0 | top pressure predicts near mid move | keep over microprice first | disable signal if either side missing or depth sum <= 0 | none | compare PnL/markout vs no-imbalance |
| spread filter | best bid/ask spread | usable online | execution filter | normal spread `<= 4`; reduce size above `4` | spread filter evidence | spread gates execution | keep one spread field | stay idle if invalid | none | PnL by spread |
| inventory skew | current position | usable online | risk control | clip `8`; soft band +/-40 | none | inventory risk | keep | assume 0 if missing | none | no limit rejections |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| microprice deviation | redundant with top imbalance | one-axis C05 beats C04 |
| full-book imbalance | lower priority / backup | top-book fails in wide or one-sided regimes |
| reversal delta | separate process candidate | combined evidence justifies later variant |

## Signal / Fair Value Logic

- Signal: top imbalance shifts fair value upward when bid depth dominates and downward when ask depth dominates.
- Inputs: best bid/ask prices and volumes, spread, position.
- Missing-signal behavior: stay idle or quote neutral without imbalance.
- Process assumption that would invalidate this logic: visible top depth does not predict next markout.
- Multivariate or redundancy caveat: do not stack with microprice in first implementation.

## Execution Logic

- Buy behavior: buy best ask when imbalance-adjusted FV exceeds ask by at least `1`.
- Sell behavior: sell best bid when bid exceeds imbalance-adjusted FV by at least `1`.
- Passive/resting order behavior: skew resting quotes toward pressure side when spread permits.
- Stay-idle behavior: missing side, depth sum zero, spread invalid, weak imbalance, or no capacity.

## Position And Risk Handling

- Position limits: ACO absolute 80.
- Aggregate buy capacity: `80 - position`.
- Aggregate sell capacity: `80 + position`.
- Inventory skew or reduction: reduce same-side skew outside +/-40.

## State And Runtime

- `traderData` use: optional diagnostics only; no state required.
- Imports: standard library only.
- Runtime risk: O(1).
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: imbalance reflects stale visible depth.
- Mitigation or validation: markout by imbalance bucket.
- Failure case: over-skewing accumulates inventory.
- Mitigation or validation: inventory/PnL attribution.

## Validation Plan

- Contract checks: return shape, `bid()`, no unsupported imports.
- Order sign and limit checks: aggregate capacity by side.
- Performance/run checks: ACO PnL vs C03, markout by imbalance quantile.
- Debug signals to inspect: imbalance, FV skew, spread, position, fills.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_04_aco_top_imbalance_skew.py`
- Parameters to implement: imbalance threshold `0.15`, skew coefficient `2.0`, edge threshold `1`, spread max `4`, clip `8`, soft band `40`.
- Known caveats: not approved for implementation until review outcome is recorded.
