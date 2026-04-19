# Spec: R2-CAND-01 IPR Drift FV Maker

## Review Status

- Status: `COMPLETED`
- Owner: Codex
- Reviewer: Human
- Reviewed on: 2026-04-19

## Candidate

- Candidate ID: `R2-CAND-01-IPR-DRIFT-FV-MAKER`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `INTARIAN_PEPPER_ROOT`
- Linked candidate file: `rounds/round_2/workspace/03_strategy_candidates.md`

## Review Decision

- `_index.md` spec status: `approved`
- Approved for implementation: `yes`
- Reviewer decision notes: Human approved implementation of all 10 specs with caveats for information and log collection.
- Required changes before coding: none; validate before treating as final submission.

## Sources

- Wiki facts: Round 2 products/limits and `Trader.run()` contract.
- EDA evidence: IPR drift plus residual in `01_eda/eda_round2_fresh.md`.
- Understanding summary: IPR needs drift-aware fair value; fixed Round 1 FV rejected.
- Post-run research memory: absent.
- Playbook heuristics: passive market making around fair value, labeled as heuristic.

## Selection Trace

- Based on candidate: highest-priority IPR isolation strategy.
- Signals used: online mid, online rolling drift estimate, residual from drift fair value.
- Alternatives considered: fixed Round 1 fair value rejected; residual-extreme execution kept as C02.
- Why selected: strongest single-product evidence and fastest IPR edge isolation.
- Known caveats: final drift may differ from sample; avoid sample-end constants.

## Evidence Traceability

- Linked EDA Signals: IPR drift plus residual.
- Feature Evidence: mean linear R2 near `1.000`; residual reversal evidence.
- Multivariate Evidence: h3/h5 residual coefficients about `-1.41`, p=0.
- Process / Distribution Assumptions: deterministic trend plus residual mean reversion.
- Redundancy Decisions: fixed FV rejected; residual feature kept.
- Regime Assumptions: drift is estimable online from recent mids.
- Understanding Insight: IPR needs drift-aware fair value.
- Evidence gaps or strategy assumptions: online drift estimate is a strategy assumption.

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run()` | wiki contract | implement | trade only `INTARIAN_PEPPER_ROOT` | import/smoke test returns `(result, 0, traderData)` |
| `Trader.bid()` | Round 2 wiki | exclude | define `bid()` returning `0` unless final MAF spec overrides | verify method exists and returns int |
| Manual RSS | Round 2 wiki | not applicable | no effect on bot | no manual inputs in code |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mid price | best bid/ask from `order_depths[IPR]` | usable online | direct input | require both sides | none | current quote midpoint proxies fair anchor | keep | stay idle if missing | none | no orders on empty/missing book |
| rolling drift FV | `timestamp`, previous IPR mids | usable online | fair-value model | warmup 20 mids; slope EWMA alpha `0.05`; cap slope update to observed quote deltas | residual regression evidence | drift persists but is estimated online | keep | during warmup quote only one-lot passive or stay idle | store last mid, EWMA slope, anchor mid/time | invalidate if platform PnL shows monotonic drift model loses by day |
| residual | mid minus drift FV | usable online | direct signal | entry edge `>= 1`; quote width base `1`; max clip `8` | residual reversal evidence | residual mean reverts | keep | disable residual orders if FV unavailable | same state as drift FV | markout by residual bucket |
| spread filter | best ask minus best bid | usable online | execution filter | allow normal mode when spread `<= 4`; reduce size above `4` | spread promoted as filter | wide spreads change fill quality | keep one spread field | stay idle if spread invalid | none | PnL/fill split by spread regime |
| inventory skew | current position | usable online | risk control | limit 80; target inventory 0; reduce buys above +40, sells below -40 | none | inventory affects risk | keep | assume 0 if missing | none | no aggregate order-cap rejection |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| fixed Round 1 IPR FV | contradicted by Round 2 drift | final data materially contradicts drift evidence |
| cross-product lead-lag | weak evidence | platform logs show coupling |
| trade pressure | needs logs | reliable `market_trades` diagnostics exist |

## Signal / Fair Value Logic

- Signal: residual = current mid minus online drift fair value.
- Inputs: best bid, best ask, timestamp, previous mids in `traderData`.
- Missing-signal behavior: stay idle until both sides and warmup are available.
- Process assumption that would invalidate this logic: drift estimate fails on platform/final day.
- Multivariate or redundancy caveat: residual should not be combined with fixed FV.

## Execution Logic

- Buy behavior: buy when best ask is below FV by at least `1`, capped by position capacity and clip `8`.
- Sell behavior: sell when best bid is above FV by at least `1`, capped by position capacity and clip `8`.
- Passive/resting order behavior: if edge is weaker, post one passive buy below FV and one passive sell above FV only when spread permits.
- Stay-idle behavior: missing book, invalid spread, warmup unavailable, or zero capacity.

## Position And Risk Handling

- Position limits: `INTARIAN_PEPPER_ROOT` absolute limit 80.
- Aggregate buy capacity: `80 - current_position`.
- Aggregate sell capacity: `80 + current_position`.
- Inventory skew or reduction: reduce same-side orders as position approaches +/-40; never exceed capacity.

## State And Runtime

- `traderData` use: JSON with last IPR mid, anchor mid/time, EWMA slope, count.
- Imports: standard library only.
- Runtime risk: O(1) per call.
- Research-only dependencies excluded from uploadable bot: `yes`.

## Expected Failure Cases

- Failure case: drift overfit causes systematic chasing.
- Mitigation or validation: product PnL and residual markout by day/subset.
- Failure case: passive quotes fill adversely.
- Mitigation or validation: fill/markout split by spread and residual bucket.

## Validation Plan

- Contract checks: `Trader`, `bid`, `run`, return tuple, string `traderData`.
- Order sign and limit checks: positive buys, negative sells, aggregate capacity.
- Performance/run checks: IPR-only PnL, position trace, residual bucket markouts.
- Debug signals to inspect: mid, FV, slope, residual, spread, position.

## Implementation Handoff

- Target bot path: `rounds/round_2/bots/noel/canonical/candidate_r2_cand_01_ipr_drift_fv_maker.py`
- Parameters to implement: warmup `20`, slope alpha `0.05`, edge threshold `1`, spread normal max `4`, max clip `8`, inventory soft band `40`.
- Known caveats: not approved for implementation until review outcome is recorded.
