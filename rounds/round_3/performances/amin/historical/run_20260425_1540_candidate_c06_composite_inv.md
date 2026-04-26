# Performance Run Summary

## Run Metadata

- Run ID: `run_20260425_1540_candidate_c06_composite_inv`
- Date: `2026-04-25`
- Round: `round_3`
- Member / owner: `amin`
- Candidate ID: `C06-inv`
- Variant ID: `inventory`
- Decision relevance: `canonical`
- Bot path: [`../../../bots/amin/historical/candidate_c06_composite_inv.py`](../../../bots/amin/historical/candidate_c06_composite_inv.py)
- Parent bot: [`../../../bots/amin/historical/candidate_c06_v01_centered_base.py`](../../../bots/amin/historical/candidate_c06_v01_centered_base.py)
- Strategy spec: [`../../../workspace/04_strategy_specs/spec_c06_composite_inv.md`](../../../workspace/04_strategy_specs/spec_c06_composite_inv.md)
- Variant hypothesis: stronger voucher inventory skew plus imbalance confirmation should rescue the active-voucher branch
- Insight being tested: whether the current problem is mostly inventory concentration rather than strike selection
- Linked signal/regime assumption: current active-voucher signal is right, but risk/execution needs stronger control
- Linked process hypothesis: the active branch fails mainly because positions grow too large, not because `5200` is the wrong strike
- Linked multivariate relationship: VEX remains positive while inventory-aware active quoting should reduce downside
- Linked redundancy decision: C04 inventory axis should be tested separately from TTE caution
- Raw artifact path: [`../historical/candidate_c06_composite_inv.json`](../historical/candidate_c06_composite_inv.json), [`../historical/candidate_c06_composite_inv.log`](../historical/candidate_c06_composite_inv.log)
- Data day / source: platform Round 3 live `TTE=5d`
- Baseline / comparison run: [`run_20260425_1535_candidate_c06_v01_centered_base.md`](run_20260425_1535_candidate_c06_v01_centered_base.md)
- Current champion: `r3_b02_itm_residual.json`
- Changed axis: inventory skew + imbalance confirmation
- Exact change: stronger active-voucher inventory penalty and confirmation filter
- Expected effect based on EDA/understanding: smaller active drawdown and smaller toxic inventories
- Falsification metric: inventory variant still loses badly or underperforms the centered base even after reducing terminal inventory
- Validation check: compare total PnL, per-strike attribution, and terminal positions against the centered base

## Result Summary

- Status: `FINISHED`
- Profit / score: `-5245.475`
- Runtime issues: none observed
- Rejections or errors: none observed
- Position-limit concerns: no formal limit break; terminal `VEV_5200` inventory still reached `+114`
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`
- Proxy evidence basis: platform JSON `profit`

## Run Classification

- Strategy family: `composite_centered_residual_inventory`
- Tested feature / signal: inventory-skewed active-voucher centered residual with imbalance confirmation
- Changed axis type: `risk`
- Dedup key: `C06-inv + composite_centered_residual_inventory + risk + inventory_overlay + live_round3 + real platform`
- Dedup verdict: `new`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: the run falsifies the current idea that stronger inventory control alone solves the active-voucher branch
- Round adaptation audit: `passed`
- Round adaptation caveat: none
- Portability: `round-specific`
- Reroute: `spec revision`

## Run Diagnostics

- Product PnL split: delta1 `+599.500`, itm `0.000`, active `-5844.975`
- Final positions: `VEX +4`, `HYDRO +4`, `VEV_5000 +4`, `VEV_5100 -22`, `VEV_5200 +114`, `VEV_5300 -70`
- Own trades: unavailable in durable artifact
- Buy / sell qty: unavailable in durable artifact
- Matched qty: unavailable in durable artifact
- Avg buy / avg sell: unavailable in durable artifact
- Gross spread capture: unavailable in durable artifact
- Max drawdown: `-5393.154`
- Max abs position: `114` on `VEV_5200`
- Inventory / mark caveat: terminal inventory is smaller than the centered base, but realized loss is much worse
- Advanced diagnostics used, if any: product attribution + direct comparison to centered base
- Statistical or regime confidence: enough to reject the current C04 overlay as the immediate next path

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| voucher inventory skew | reduce loss by reducing concentration | failed; lower terminal position but worse PnL | direct comparison vs centered base | down | keep inventory control only on cleaner subsets |
| imbalance confirmation | improve trade selection | not enough to offset active losses | total + strike attribution | down/unclear | avoid treating it as the next main axis |
| VEX sidecar | remain positive | stayed positive | product attribution | unchanged/up | keep VEX branch |

## Process And Multivariate Diagnostics

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| inventory concentration is the primary problem | lower inventory should improve PnL | contradicted; inventory was lower but PnL worse | centered-base comparison | contradicts | solve strike selection first |
| active vouchers can remain broad if risk is stronger | broad basket should survive with better skew | not observed | total PnL + per-strike attribution | contradicts | move to smaller subsets |
| VEX still helps | positive sidecar contribution | observed | product attribution | supports | keep VEX combos |

## Comparability

- Comparable to baseline: `yes`
- Same data/source: `yes`
- Same bot/spec version basis: `yes`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: only the C04 inventory/imbalance axis changed versus the centered base

## Interpretation Limits

- Non-authoritative evidence: single live run
- Missing artifacts: external `.log` file is empty; durable own-trade breakdown unavailable
- Comparability caveats: one run only, but the changed axis is clean and the result is strongly negative

## Findings

- Finding: stronger inventory control alone is not the right immediate fix for the current active-voucher branch.
- Signal/regime evidence verdict: `contradicts`
- Process/multivariate evidence verdict: `contradicts`
- Verdict basis: terminal inventory improved, but PnL deteriorated sharply and the active bucket remained the failure driver

## Post-Run Research

- Analysis status: `full`
- Source artifacts: `candidate_c06_composite_inv.json`, `round_3_canonical_run_analysis.md`
- Compared against: centered base challenger, frozen legacy base, live logger
- Memory file change: `updated`
- ROI-gated memory action: `update`
- Memory action / file-change reason: the run materially reroutes the next work from inventory-first back to strike-selection-first

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `revise spec`
- Decision vs champion: `reject`
- Candidate class: `reject`

## Next Action

- Next: keep inventory as a later subset overlay, not as the next broad active-voucher challenger.
