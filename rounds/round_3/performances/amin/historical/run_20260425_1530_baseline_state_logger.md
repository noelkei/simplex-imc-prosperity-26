# Performance Run Summary

## Run Metadata

- Run ID: `run_20260425_1530_baseline_state_logger`
- Date: `2026-04-25`
- Round: `round_3`
- Member / owner: `amin`
- Candidate ID: `D01`
- Variant ID: `logger`
- Decision relevance: `canonical`
- Bot path: [`../../../bots/amin/historical/baseline_state_logger.py`](../../../bots/amin/historical/baseline_state_logger.py)
- Parent bot: none
- Strategy spec: [`../../../workspace/04_strategy_specs/spec_learning_batch_wave1.md`](../../../workspace/04_strategy_specs/spec_learning_batch_wave1.md)
- Variant hypothesis: capture a clean live `TTE=5d` market path without trading interference
- Insight being tested: live spread, movement, and microstructure quality by product
- Linked signal/regime assumption: `TTE=5d` live market conditions may differ materially from the historical `6d-8d` sample
- Linked process hypothesis: upper strikes may be more tradable live than raw-day EDA suggested
- Linked multivariate relationship: VEX remains the usable option anchor; HYDRO remains separate
- Linked redundancy decision: diagnostic state capture is worth one upload when logs can change the learner queue
- Raw artifact path: [`../historical/baseline_state_logger.json`](../historical/baseline_state_logger.json), [`../historical/baseline_state_logger.log`](../historical/baseline_state_logger.log)
- Data day / source: platform Round 3 live `TTE=5d`
- Baseline / comparison run: none
- Current champion: `r3_b02_itm_residual.json`
- Changed axis: diagnostic no-trade state capture
- Exact change: remove all trading and preserve only platform book / PnL path
- Expected effect based on EDA/understanding: clean live market metrics for product selection
- Falsification metric: logger shows no new actionable information beyond the historical sample
- Validation check: live spread table, live reversion / imbalance table, live residual table

## Result Summary

- Status: `FINISHED`
- Profit / score: `0.000`
- Runtime issues: none observed
- Rejections or errors: none observed
- Position-limit concerns: none
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`
- Proxy evidence basis: logger does not trade

## Run Classification

- Strategy family: `diagnostic_state_probe`
- Tested feature / signal: live book / spread / residual diagnostics
- Changed axis type: `baseline`
- Dedup key: `D01 + diagnostic_state_probe + baseline + live_book_capture + live_round3 + real platform`
- Dedup verdict: `new`
- Knowledge delta: `new`
- ROI-gated memory action: `update`
- Memory action rationale: the logger materially changed product prioritization for upper strikes and confirmed the floor regime
- Round adaptation audit: `passed`
- Round adaptation caveat: none
- Portability: `round-specific`
- Reroute: `targeted EDA`

## Run Diagnostics

- Product PnL split: all zero by construction
- Final positions: flat
- Own trades: zero
- Buy / sell qty: zero
- Matched qty: zero
- Avg buy / avg sell: not applicable
- Gross spread capture: not applicable
- Max drawdown: `0.000`
- Max abs position: `0`
- Inventory / mark caveat: not applicable
- Advanced diagnostics used, if any: live spread, imbalance, and intrinsic/extrinsic residual checks from `activitiesLog`
- Statistical or regime confidence: enough to reprioritize the next learning batch

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| live upper-strike tradability | `VEV_5400/5500` should either stay dead or reopen | reopened with movement plus tight spreads | live spread + unique-mid metrics | up | create upper-strike learners |
| floor regime | `VEV_6000/6500` may or may not break the floor | still frozen at `0.5` | live spread + unique-mid metrics | unchanged/up | keep floor family out of active trading |
| HYDRO live signal | HYDRO may still show microstructure edge despite poor historical execution | live reversion + imbalance still present | live microstructure diagnostics | unchanged for signal / down for blind trust | isolate HYDRO learners |

## Process And Multivariate Diagnostics

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| upper strikes are untradeable | little movement and no useful spread profile | contradicted by `VEV_5400/5500` live data | live spread / movement diagnostics | contradicts | reopen upper-strike learners |
| floor strikes may have broken live | any movement away from `0.5` | not observed | live spread / movement diagnostics | not tested strongly enough to reopen | keep monitoring only |
| VEX remains usable option anchor | vouchers still move with VEX live | still supported | same-time live coupling diagnostics | supports | keep VEX-centered voucher analysis |

## Comparability

- Comparable to baseline: `no`
- Same data/source: `yes`
- Same bot/spec version basis: `no`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: diagnostic no-trade artifact only

## Interpretation Limits

- Non-authoritative evidence: live platform observation only; not an alpha result
- Missing artifacts: external `.log` file is empty, but JSON `activitiesLog` is complete
- Comparability caveats: cannot rank against trading bots by PnL

## Findings

- Finding: `VEV_5400/5500` deserve isolated learners immediately; `VEV_6000/6500` still do not.
- Signal/regime evidence verdict: `supports`
- Process/multivariate evidence verdict: `supports`
- Verdict basis: live spread, movement, and residual diagnostics changed the next batch priority materially

## Post-Run Research

- Analysis status: `full`
- Source artifacts: `baseline_state_logger.json`, `round_3_canonical_run_analysis.md`
- Compared against: historical report and post-run memory
- Memory file change: `updated`
- ROI-gated memory action: `update`
- Memory action / file-change reason: live upper/floor evidence materially changed the learner queue

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `continue`
- Decision vs champion: `not applicable`
- Candidate class: `experimental`

## Next Action

- Next: use the live logger metrics to prioritize ITM, `5300`, and upper-strike learners ahead of new broad composites.
