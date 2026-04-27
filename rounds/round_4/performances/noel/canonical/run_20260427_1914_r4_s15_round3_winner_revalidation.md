# Run Summary: `r4_s15_round3_winner_revalidation`

## Run Metadata

- Run ID: not exposed in saved platform artifact
- Date: 2026-04-27
- Round: `round_4`
- Member / owner: `noel`
- Candidate ID: `r4_s15_round3_winner_revalidation`
- Variant ID: `base`
- Decision relevance: `canonical`
- Bot path: `rounds/round_4/bots/noel/canonical/r4_s15_round3_winner_revalidation.py`
- Parent bot: none
- Strategy spec: `rounds/round_4/workspace/04_strategy_specs/spec_pack_b_round3_revalidation.md`
- Variant hypothesis: the old `round_3` winner family can survive under round-4 defensive context
- Insight being tested: winner protection plus new tape filters beats trusting the old stack blindly
- Linked signal/regime assumption: `VEX + 4000` winner family survives with danger filters
- Raw artifact path: `rounds/round_4/performances/noel/historical/r4_s15_round3_winner_revalidation.{json,log}`
- Data day / source: day `3`, real platform artifacts
- Baseline / comparison run: `r4_s03_vex_4000_overlay`
- Changed axis: feature bundle
- Exact change: old winner family plus `Mark 22` veto and trade-to-book gate
- Expected effect based on EDA/understanding: protect the old winner from the new tape's obvious danger states
- Falsification metric: the branch never engages at all
- Validation check: compare activation and linked-product use against simpler Pack B versions

## Result Summary

- Status: `FINISHED`
- Profit / score: `0.0`
- Runtime issues: none observed
- Rejections or errors: none visible
- Position-limit concerns: none visible
- PnL source: `real platform PnL`

## Run Classification

- Strategy family: `round3 winner revalidation`
- Tested feature / signal: old winner stack under round-4 defensive context
- Changed axis type: `feature toggle`
- Dedup key: `r4_s15 + pack_b + winner_revalidation + day3 + real_platform`
- Dedup verdict: `contradicts`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: the branch closed an expensive question cheaply by showing over-shutdown
- Round adaptation audit: `passed`
- Portability: `uncertain`
- Branch posture: `not cleanly tested`
- Reroute: `spec revision`

## Run Diagnostics

- Product PnL split: none
- Final positions: flat
- Own trades: `0`
- Buy / sell qty: `0 / 0`
- Matched qty: `0`
- Peak PnL: `0.0`
- End from peak: `0.0`
- Max drawdown: `0.0`
- Max abs position: `0`

## Findings

- Finding: the current defensive revalidation stack shut the old winner family off completely, so it did not answer whether the `VEX + 4000` architecture still has direct online value.
- Signal/regime evidence verdict: `weakens`
- Process/multivariate evidence verdict: `not tested`
- Verdict basis: a full no-trade run can only be interpreted as over-filtering under current thresholds, not as confirmation that the old winner died.

## Post-Run Research

- Analysis status: `lightweight`
- Source artifacts: saved `.py`, `.json`, `.log`
- Compared against: `r4_s03_vex_4000_overlay`, `r4_s13_4000_benign_flow_overlay`
- Memory file change: `updated`
- ROI-gated memory action: `update`

### Carry-Forward Output

- Validated carry-forward principle opened or reinforced: none
- Untested hypothesis opened: the old winner may still survive if separated from the current over-strong defensive stack
- Anti-pattern reinforced: treating "winner protection" as justification for multi-gating before the base family is even reactivated

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `revise spec`
- Decision vs champion: `rerun`
- Candidate class: `experimental`

## Next Action

- Next: if Pack B survives, re-open it as a much narrower revalidation branch with one protective axis at a time instead of the current composite gate stack.
