# Performance Run Summary

## Run Metadata

- Run ID: `run_20260425_1535_candidate_c06_v01_centered_base`
- Date: `2026-04-25`
- Round: `round_3`
- Member / owner: `amin`
- Candidate ID: `C06`
- Variant ID: `base-corrected`
- Decision relevance: `canonical`
- Bot path: [`../../../bots/amin/historical/candidate_c06_v01_centered_base.py`](../../../bots/amin/historical/candidate_c06_v01_centered_base.py)
- Parent bot: [`../../../bots/amin/historical/candidate_c06_composite_base.py`](../../../bots/amin/historical/candidate_c06_composite_base.py)
- Strategy spec: [`../../../workspace/04_strategy_specs/spec_c06_composite_base.md`](../../../workspace/04_strategy_specs/spec_c06_composite_base.md)
- Variant hypothesis: centered residual plus observed-surface guardrail should outperform the frozen legacy composite
- Insight being tested: corrected voucher signal translation versus the historical legacy base
- Linked signal/regime assumption: active-voucher centered residual remains monetizable on live `TTE=5d`
- Linked process hypothesis: the active voucher branch should mean-revert cleanly enough to support a broad `VEV_5000-5300` basket
- Linked multivariate relationship: VEX acts as a positive anchor while active vouchers provide the main alpha
- Linked redundancy decision: centered residual should beat the raw legacy family
- Raw artifact path: [`../historical/candidate_c06_v01_centered_base.json`](../historical/candidate_c06_v01_centered_base.json), [`../historical/candidate_c06_v01_centered_base.log`](../historical/candidate_c06_v01_centered_base.log)
- Data day / source: platform Round 3 live `TTE=5d`
- Baseline / comparison run: [`../historical/candidate_c06_composite_base.json`](../historical/candidate_c06_composite_base.json)
- Current champion: `r3_b02_itm_residual.json`
- Changed axis: corrected centered residual versus frozen legacy composite
- Exact change: raw legacy residual -> centered residual with observed-surface guardrail
- Expected effect based on EDA/understanding: cleaner active-voucher alpha and lower structural surface error
- Falsification metric: total PnL worse than the legacy base or strike-level losses still dominated by the same active bucket
- Validation check: product attribution, final positions, drawdown, comparison to legacy base

## Result Summary

- Status: `FINISHED`
- Profit / score: `-3008.203`
- Runtime issues: none observed
- Rejections or errors: none observed
- Position-limit concerns: no formal limit break; terminal `VEV_5200` inventory reached `+270`
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`
- Proxy evidence basis: platform JSON `profit`

## Run Classification

- Strategy family: `composite_centered_residual`
- Tested feature / signal: centered Bachelier residual on `VEV_5000-5300` with HYDRO/VEX sidecars
- Changed axis type: `feature toggle`
- Dedup key: `C06 + composite_centered_residual + feature toggle + centered_residual + live_round3 + real platform`
- Dedup verdict: `new`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: the run materially changes the next learner queue and weakens the broad active-voucher basket assumption
- Round adaptation audit: `passed`
- Round adaptation caveat: none
- Portability: `round-specific`
- Reroute: `one-axis variant`

## Run Diagnostics

- Product PnL split: delta1 `+599.500`, itm `0.000`, active `-3607.703`
- Final positions: `VEX +4`, `HYDRO +4`, `VEV_5000 +8`, `VEV_5100 -10`, `VEV_5200 +270`, `VEV_5300 -224`
- Own trades: unavailable in durable artifact
- Buy / sell qty: unavailable in durable artifact
- Matched qty: unavailable in durable artifact
- Avg buy / avg sell: unavailable in durable artifact
- Gross spread capture: unavailable in durable artifact
- Max drawdown: `-4154.039`
- Max abs position: `270` on `VEV_5200`
- Inventory / mark caveat: loss is overwhelmingly concentrated in live active-voucher inventory, especially `VEV_5200`
- Advanced diagnostics used, if any: product attribution + live logger comparison
- Statistical or regime confidence: enough to reject the broad active-voucher centered basket as the immediate next step

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| centered active-voucher residual | improve over frozen legacy base | failed; run lost worse than legacy | product attribution + baseline comparison | down for broad basket | split the basket by strike |
| VEX sidecar | remain positive and stabilizing | helped | product attribution | unchanged/up | keep VEX learners |
| HYDRO sidecar | add small independent PnL | essentially flat to slightly negative | product attribution | unchanged/down | isolate HYDRO before reintegration |

## Process And Multivariate Diagnostics

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| active vouchers behave as one tradable family | basket should distribute risk reasonably across `5000-5300` | contradicted; `5200` dominates the loss | strike-level attribution | contradicts | move to strike/subset learners |
| centered residual should rescue the historical active-voucher family | improved total PnL | not observed | total PnL + bucket attribution | contradicts | stop broad composite reruns |
| VEX remains a positive supporting leg | positive delta1 contribution | observed | product attribution | supports | keep VEX anchor / sidecar role |

## Comparability

- Comparable to baseline: `yes`
- Same data/source: `yes`
- Same bot/spec version basis: `no`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: corrected centered residual and observed-surface guardrail versus frozen legacy code

## Interpretation Limits

- Non-authoritative evidence: single live run
- Missing artifacts: external `.log` file is empty; durable own-trade breakdown unavailable
- Comparability caveats: same live day, but different code path and not enough runs for stability claims

## Findings

- Finding: the corrected broad active-voucher composite path should be paused in favor of isolated learners.
- Signal/regime evidence verdict: `contradicts`
- Process/multivariate evidence verdict: `contradicts`
- Verdict basis: the run loses worse than the legacy reference and concentrates losses in `VEV_5200`

## Post-Run Research

- Analysis status: `full`
- Source artifacts: `candidate_c06_v01_centered_base.json`, `round_3_canonical_run_analysis.md`
- Compared against: frozen C06 legacy base, historical best ITM learner, live logger
- Memory file change: `updated`
- ROI-gated memory action: `update`
- Memory action / file-change reason: this run materially changes strike-selection and next-bot priority

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `revise spec`
- Decision vs champion: `reject`
- Candidate class: `reject`

## Next Action

- Next: stop broad active `5000-5300` composites and move immediately to strike-isolated and subset learners.
