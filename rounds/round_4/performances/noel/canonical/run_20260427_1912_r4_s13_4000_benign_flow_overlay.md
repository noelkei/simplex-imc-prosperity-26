# Run Summary: `r4_s13_4000_benign_flow_overlay`

## Run Metadata

- Run ID: not exposed in saved platform artifact
- Date: 2026-04-27
- Round: `round_4`
- Member / owner: `noel`
- Candidate ID: `r4_s13_4000_benign_flow_overlay`
- Variant ID: `base`
- Decision relevance: `canonical`
- Bot path: `rounds/round_4/bots/noel/canonical/r4_s13_4000_benign_flow_overlay.py`
- Parent bot: `r4_s03_vex_4000_overlay`
- Strategy spec: `rounds/round_4/workspace/04_strategy_specs/spec_pack_b_round3_revalidation.md`
- Variant hypothesis: benign-flow conditioning should improve the old `4000` overlay family
- Insight being tested: counterparty-conditioned flow can rescue the ITM add-on
- Linked signal/regime assumption: benign-flow state improves `4000` overlay quality
- Raw artifact path: `rounds/round_4/performances/noel/historical/r4_s13_4000_benign_flow_overlay.{json,log}`
- Data day / source: day `3`, real platform artifacts
- Baseline / comparison run: `r4_s03_vex_4000_overlay`
- Changed axis: feature toggle
- Exact change: add benign-flow conditioning to the `VEX + 4000` family
- Expected effect based on EDA/understanding: same or better early edge with fewer bad add-ons
- Falsification metric: no `4000` engagement and worse anchor path than the base
- Validation check: linked-product activation and late-session path retention

## Result Summary

- Status: `FINISHED`
- Profit / score: `-1.515625`
- Runtime issues: none observed
- Rejections or errors: none visible
- Position-limit concerns: none visible; final `VEX` position `-16` stayed inside the `200` limit
- PnL source: `real platform PnL`

## Run Classification

- Strategy family: `conditioned 4000 overlay`
- Tested feature / signal: benign-flow conditioned ITM overlay
- Changed axis type: `feature toggle`
- Dedup key: `r4_s13 + pack_b + benign_flow_4000 + day3 + real_platform`
- Dedup verdict: `contradicts`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: the branch changed behavior, but only by worsening the `VEX` path while still never trading `4000`
- Round adaptation audit: `passed`
- Portability: `uncertain`
- Branch posture: `edge then reversal`
- Reroute: `targeted EDA`

## Run Diagnostics

- Product PnL split: `VELVETFRUIT_EXTRACT -1.515625`; `VEV_4000` unused
- Final positions: `VELVETFRUIT_EXTRACT -16`
- Own trades: `3`, all in `VELVETFRUIT_EXTRACT`
- Buy / sell qty: `0 / 16`
- Matched qty: `16`
- Avg buy / avg sell: `n/a / 5253.69`
- Peak PnL: `86.22`
- End from peak: `-111.70`
- Max drawdown: `-131.10`
- Max abs position: `16`
- Inventory / mark caveat: the final loss came from a larger unclosed `VEX` short; the advertised `4000` add-on never participated

## Findings

- Finding: benign-flow conditioning did not validate the `4000` thesis because it never produced direct `VEV_4000` inventory and instead worsened the base `VEX` path via a late extra sell.
- Signal/regime evidence verdict: `weakens`
- Process/multivariate evidence verdict: `weakens`
- Verdict basis: the branch differs from `r4_s03` only through `VEX` timing, not through any realized `4000` add-on behavior.

## Post-Run Research

- Analysis status: `lightweight`
- Source artifacts: saved `.py`, `.json`, `.log`
- Compared against: `r4_s03_vex_4000_overlay`, `r4_s10_5200_signal_only_veto`
- Memory file change: `updated`
- ROI-gated memory action: `update`

### Carry-Forward Output

- Validated carry-forward principle opened or reinforced: none
- Untested hypothesis opened: the `4000` add-on still needs a clean activation test
- Anti-pattern reinforced: layering context on top of an overlay family before confirming the overlay trades at all

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `revise spec`
- Decision vs champion: `reject`
- Candidate class: `experimental`

## Next Action

- Next: do not send another benign-flow `4000` branch until Pack B is simplified to force a genuine `VEV_4000` test or is intentionally pruned.
