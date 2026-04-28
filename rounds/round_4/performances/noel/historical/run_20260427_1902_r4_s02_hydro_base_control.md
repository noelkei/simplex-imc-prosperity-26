# Run Summary: `r4_s02_hydro_base_control`

## Run Metadata

- Run ID: not exposed in saved platform artifact
- Date: 2026-04-27
- Round: `round_4`
- Member / owner: `noel`
- Candidate ID: `r4_s02_hydro_base_control`
- Variant ID: `base`
- Decision relevance: `canonical`
- Bot path: `rounds/round_4/bots/noel/canonical/r4_s02_hydro_base_control.py`
- Parent bot: none
- Strategy spec: `rounds/round_4/workspace/04_strategy_specs/spec_pack_a_delta1_controls.md`
- Variant hypothesis: `HYDRO` could act as an independent delta-1 control
- Insight being tested: `HYDRO` deserves a standalone Wave 1 control slot
- Linked signal/regime assumption: clean independent `HYDRO` delta-1 process
- Raw artifact path: `rounds/round_4/performances/noel/historical/r4_s02_hydro_base_control.{json,log}`
- Data day / source: day `3`, real platform artifacts
- Baseline / comparison run: `r4_s01_vex_base_control`
- Changed axis: product choice
- Exact change: swap anchor product from `VEX` to `HYDRO`
- Expected effect based on EDA/understanding: a comparable control with different product process
- Falsification metric: zero engagement or no clean edge
- Validation check: trade count, path activation, and control usefulness

## Result Summary

- Status: `FINISHED`
- Profit / score: `0.0`
- Runtime issues: none observed
- Rejections or errors: none visible
- Position-limit concerns: none visible
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`

## Run Classification

- Strategy family: `delta-1 HYDRO control`
- Tested feature / signal: standalone `HYDRO` anchor
- Changed axis type: `baseline`
- Dedup key: `r4_s02 + delta1_control + product_swap + HYDRO_anchor + day3 + real_platform`
- Dedup verdict: `new`
- Knowledge delta: `new`
- ROI-gated memory action: `update`
- Memory action rationale: zero engagement closes an important branch cheaply
- Round adaptation audit: `passed`
- Portability: `uncertain`
- Branch posture: `no edge`
- Reroute: `ignore`

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
- Inventory / mark caveat: none; the bot never engaged

## Comparability

- Comparable to baseline: `yes`
- Same data/source: `yes`
- Same bot/spec version basis: `yes`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: exact run ID is not exposed in the saved JSON

## Findings

- Finding: the Pack A independent `HYDRO` control produced no trades and no evidence strong enough to justify another standalone slot.
- Signal/regime evidence verdict: `weakens`
- Process/multivariate evidence verdict: `not tested`
- Verdict basis: the branch remained inactive for the full run, so it did not validate the hoped-for independent `HYDRO` control thesis.

## Post-Run Research

- Analysis status: `lightweight`
- Source artifacts: saved `.py`, `.json`, `.log`
- Compared against: `r4_s01_vex_base_control`
- Memory file change: `updated`
- ROI-gated memory action: `update`

### Carry-Forward Output

- Validated carry-forward principle opened or reinforced: none
- Untested hypothesis opened: none worth immediate implementation
- Anti-pattern reinforced: spending Wave 2 slots on standalone `HYDRO` controls without new evidence

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `discard`
- Decision vs champion: `reject`
- Candidate class: `reject`

## Next Action

- Next: deprioritize standalone `HYDRO` control work and keep `HYDRO` out of the next mini-wave unless a later pack shows a linked-product reason to reintroduce it.
