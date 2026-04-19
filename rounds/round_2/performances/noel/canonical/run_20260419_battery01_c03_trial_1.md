# run_20260419_battery01_c03_trial_1

## Run Metadata

- Run ID: `run_20260419_battery01_c03_trial_1`
- Date: `2026-04-19`
- Round: `round_2`
- Member / owner: `noel`
- Candidate ID: `R2-CAND-03`
- Variant ID: `trial_1`
- Decision relevance: `canonical`
- Bot path: [`rounds/round_2/bots/noel/canonical/candidate_r2_cand_03_aco_reversal_maker.py`](../../../../rounds/round_2/bots/noel/canonical/candidate_r2_cand_03_aco_reversal_maker.py)
- Strategy spec: [`spec_r2_cand_03_aco_reversal_maker.md`](../../../workspace/04_strategy_specs/spec_r2_cand_03_aco_reversal_maker.md)
- Raw artifact path: [`rounds/round_2/performances/noel/historical/candidate_r2_cand_03_aco_reversal_maker.json`](../../../../rounds/round_2/performances/noel/historical/candidate_r2_cand_03_aco_reversal_maker.json)
- Data day / source: Round 2 platform test JSON, day `1`, randomized 80% quote subset
- Changed axis: `ACO short-horizon reversal`
- Expected effect based on EDA/understanding: `ACO short-horizon reversal` should improve execution or alpha if the online proxy activates.
- Falsification metric: Real platform PnL, product attribution, final position, and whether the tested product actually changes PnL.

## Result Summary

- Status: `FINISHED`
- Profit / score: `0.000`
- Runtime issues: none visible in platform JSON
- Rejections or errors: not available in JSON
- Position-limit concerns: final IPR `0`, final ACO `0`; max path position unavailable
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`
- Proxy evidence basis: platform JSON `profit`, `activitiesLog`, `graphLog`, `positions`

## Run Classification

- Strategy family: `aco_reversal`
- Tested feature / signal: `ACO short-horizon reversal`
- Changed axis type: `feature toggle / execution`
- Dedup key: `aco_reversal + ACO short-horizon reversal + platform day 1 randomized subset + real platform PnL`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: ACO module produced zero PnL and zero position; revise activation before retesting.
- Round adaptation audit: `caveat`
- Round adaptation caveat: bot/source provenance is partial because raw JSON is in `historical/`, canonical bot copy exists, and no separate stdout `.log` was found.
- Portability: `round-specific`
- Reroute: `reject current implementation`

## Run Diagnostics

Product PnL split:

| product              |   final_pnl |   final_position |   pnl_change_ticks |
|:---------------------|------------:|-----------------:|-------------------:|
| INTARIAN_PEPPER_ROOT |           0 |                0 |                  0 |
| ASH_COATED_OSMIUM    |           0 |                0 |                  0 |

- Final positions: IPR `0`, ACO `0`, XIRECS `0`
- Max drawdown from graphLog: `0.000`
- Graph min / max: `0.000` / `0.000`
- Own trades / matched qty / avg buy-sell: unavailable in JSON
- Advanced diagnostics used: platform activity product attribution, graphLog drawdown, spread-gate diagnostics in aggregate battery report
- Statistical or regime confidence: limited; platform quote subset is randomized and only C08 has a repeated trial

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| `ACO short-horizon reversal` | Improve PnL or isolate evidence | Total PnL `0.000`, IPR `0.000`, ACO `0.000` | platform product attribution | `down for current ACO implementation` | `reject current implementation` |

## Process And Multivariate Diagnostics

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| Round 2 randomized quote subset | Repeat submissions may differ | C08 trial spread and C07/C10 same-logic gap show material variance | repeated/platform comparison | supports | rerun serious candidates |
| ACO EDA signal usability | ACO modules should produce activity if online proxy works | ACO PnL and final position are zero in this run | product attribution | weakens current implementation, not necessarily EDA signal | activation probe |

## Comparability

- Comparable to baseline: `unclear`
- Same data/source: `unclear` because testing quote subset is randomized per submission
- Same bot/spec version basis: `partial`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: no separate stdout `.log`; canonical bot copy exists after state repair, raw JSON remains in historical performance folder.

## Interpretation Limits

- Non-authoritative evidence: platform test result is real PnL for this test, but randomized 80% quote subset makes single-run ranking noisy.
- Missing artifacts: per-fill own trade log, rejection log, stdout `R2_BOT_LOG`.
- Comparability caveats: do not treat tiny PnL differences as strategy superiority without reruns.

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `reject current implementation`
- Decision vs champion: `reject`
- Candidate class: `reject`

## Next Action

- Next: See aggregate battery report and Generation 2 queue.
