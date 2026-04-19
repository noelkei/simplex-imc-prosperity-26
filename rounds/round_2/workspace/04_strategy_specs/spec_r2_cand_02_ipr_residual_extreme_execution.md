# Spec: R2-CAND-02 IPR Residual Extreme Execution

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-02-IPR-RESIDUAL-EXTREME-EXECUTION`
- Candidate priority tier: `implement-first`
- Evidence strength: `medium/high`
- Product scope: `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 IPR limit 80; shared `Trader.run()` contract.
- EDA evidence: IPR drift/residual promoted.
- Understanding summary: IPR drift formula must be online-safe.
- Post-run research memory: absent.

## Selection Trace

- Based on candidate: stricter execution variant of C01.
- Signals used: same online drift FV and residual as C01.
- Alternatives considered: C01 normal execution; fixed FV rejected.
- Why selected: gives a controlled way to reduce overtrading if C01 fills poorly.
- Known caveats: may under-trade and miss profitable smaller residuals.

## Evidence Traceability

- Linked EDA Signals: IPR drift plus residual.
- Feature Evidence: residual reversal around drift.
- Multivariate Evidence: same residual evidence as C01.
- Process / Distribution Assumptions: residual mean reversion.
- Redundancy Decisions: not a new feature stack; execution differs materially.
- Regime Assumptions: residual extremes mean revert enough to pay spread.
- Understanding Insight: avoid stale FV and test execution discipline.
- Evidence gaps or strategy assumptions: threshold values are strategy parameters.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade only IPR on stronger residual dislocations | smoke test |
| `Trader.bid()` | Round 2 wiki | exclude | return `0` unless final MAF spec overrides | integer return |
| Manual RSS | Round 2 wiki | not applicable | no bot effect | no manual inputs |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| drift FV | IPR order book, timestamp, prior mids | usable online | fair-value model | same as C01 | same as C01 | trend plus residual | keep | stay idle during warmup | last mid, slope, anchor | compare to C01 |
| residual extreme | mid minus drift FV | usable online | direct signal | entry threshold `2`; passive threshold disabled unless edge `>= 2` | residual evidence | stronger residuals revert | keep | stay idle if unavailable | same | reject if lower trade count does not improve markout |
| spread filter | best bid/ask | usable online | execution filter | require spread `<= 3` for entry | spread filter evidence | spread affects execution | keep | stay idle | none | PnL by spread |
| inventory skew | position | usable online | risk control | clip `6`; soft band +/-32 | none | inventory risk | keep | assume 0 if missing | none | no rejections |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| passive small-residual quoting | candidate tests extreme-only execution | C01 overtrades but small residuals show positive markout |
| top imbalance | product-specific IPR residual test | later evidence shows book pressure improves IPR |
| trade pressure | needs logs | market-trades logs become reliable |

## Signal / Fair Value Logic

- Signal: residual extreme from online drift FV.
- Inputs: same as C01.
- Missing-signal behavior: stay idle.
- Process assumption that would invalidate this logic: residual extremes do not mean revert after fills.
- Multivariate or redundancy caveat: differs from C01 by threshold/execution, not by new feature.

## Execution Logic

- Buy behavior: buy best ask only when ask is at least `2` below FV.
- Sell behavior: sell best bid only when bid is at least `2` above FV.
- Passive/resting order behavior: no passive weak-edge quoting.
- Stay-idle behavior: edge below threshold, spread > `3`, warmup missing, or no capacity.

## Position And Risk Handling

- Position limits: IPR absolute 80.
- Aggregate buy capacity: `80 - position`.
- Aggregate sell capacity: `80 + position`.
- Inventory skew or reduction: reduce clip outside +/-32; flatten bias near limits.

## State And Runtime

- `traderData` use: same drift state as C01.
- Imports: standard library only.
- Runtime risk: O(1).
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: too few trades.
- Mitigation or validation: compare opportunity count and missed edge vs C01.
- Failure case: high-confidence entries still adverse selected.
- Mitigation or validation: markout by residual threshold.

## Validation Plan

- Contract checks: same as C01.
- Order sign and limit checks: aggregate capacity before orders.
- Performance/run checks: PnL, trade count, average markout vs C01.
- Debug signals to inspect: residual, threshold hit, spread, position.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_02_ipr_residual_extreme_execution.py`
- Parameters to implement: C01 drift params, residual threshold `2`, spread max `3`, clip `6`, inventory soft band `32`.
- Known caveats: not approved for implementation until review outcome is recorded.
