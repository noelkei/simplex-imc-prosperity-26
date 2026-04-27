# Run Summary: `r4_s01_vex_base_control`

## Run Metadata

- Run ID: not exposed in saved platform artifact
- Date: 2026-04-27
- Round: `round_4`
- Member / owner: `noel`
- Candidate ID: `r4_s01_vex_base_control`
- Variant ID: `base`
- Decision relevance: `canonical`
- Bot path: `rounds/round_4/bots/noel/canonical/r4_s01_vex_base_control.py`
- Parent bot: none
- Strategy spec: `rounds/round_4/workspace/04_strategy_specs/spec_pack_a_delta1_controls.md`
- Variant hypothesis: clean `VEX` delta-1 anchor should provide the Wave 1 baseline
- Insight being tested: `VEX` anchor can stand up as the least contaminated control
- Linked signal/regime assumption: `VEX_anchor_same_time`
- Linked process hypothesis: liquid delta-1 names should be the cleanest place to start
- Raw artifact path: `rounds/round_4/performances/noel/historical/r4_s01_vex_base_control.{json,log}`
- Data day / source: day `3`, real platform artifacts
- Baseline / comparison run: none
- Current champion: none before this partial review
- Changed axis: baseline control
- Exact change: `VEX` only, no voucher overlay or counterparty gate
- Expected effect based on EDA/understanding: clean control with interpretable path
- Falsification metric: no meaningful fills or severe giveback versus later overlays
- Validation check: control path quality, final inventory shape, and later comparison against Pack B and D

## Result Summary

- Status: `FINISHED`
- Profit / score: `15.046875`
- Runtime issues: none observed from saved artifacts
- Rejections or errors: none visible
- Position-limit concerns: none visible; final `VEX` position `-14` stayed inside the `200` limit
- PnL source: `real platform PnL`
- Proxy confidence: `not applicable`

## Run Classification

- Strategy family: `delta-1 VEX anchor control`
- Tested feature / signal: `VEX` same-time anchor
- Changed axis type: `baseline`
- Dedup key: `r4_s01 + delta1_control + baseline + VEX_anchor + day3 + real_platform`
- Dedup verdict: `new`
- Knowledge delta: `new`
- ROI-gated memory action: `update`
- Memory action rationale: establishes the only active control among Packs A/B/D and exposes a retention problem worth carrying forward
- Round adaptation audit: `passed`
- Portability: `likely reusable`
- Branch posture: `edge then reversal`
- Reroute: `one-axis variant`

## Run Diagnostics

- Product PnL split: `VELVETFRUIT_EXTRACT +15.046875`
- Final positions: `VELVETFRUIT_EXTRACT -14`
- Own trades: `2`
- Buy / sell qty: `0 / 14`
- Matched qty: `14`
- Avg buy / avg sell: `n/a / 5254.86`
- Gross spread capture: not reconstructed; no round trip completed
- Max drawdown: `-203.93`
- Max abs position: `14`
- Inventory / mark caveat: terminal PnL was entirely tied to an open short, not realized exits
- Peak PnL: `143.01` at `86600`
- End from peak: `-148.92`
- Giveback severity: high
- Advanced diagnostics used, if any: platform `graphLog`, `activitiesLog`, and `tradeHistory` parsing

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| `VEX` anchor edge | provide a clean active control | traded only twice, both late-session sells, then gave back most of the peak | tradeHistory plus graph path review | unchanged | keep as baseline, add retention-aware challenger |

## Comparability

- Comparable to baseline: `yes`
- Same data/source: `yes`
- Same bot/spec version basis: `yes`
- Exact `.py` / `.json` / `.log` saved together: `partial`
- Known differences: exact run ID is not exposed in the saved JSON

## Findings

- Finding: `VEX` clearly dominated the Pack A control comparison because the `HYDRO` control never traded, but this was still not a clean winner path.
- Signal/regime evidence verdict: `supports`
- Process/multivariate evidence verdict: `weakens`
- Verdict basis: the run confirms that `VEX` is the only meaningful delta-1 control in this subset, but the path was one-sided, inventory-mark-driven, and gave back most of the peak.

## Post-Run Research

- Analysis status: `lightweight`
- Source artifacts: saved `.py`, `.json`, `.log`
- Compared against: `r4_s02_hydro_base_control`, `r4_s03_vex_4000_overlay`
- Memory file change: `updated`
- ROI-gated memory action: `update`

### Failure-Driven Analysis

- Losing product / interval: late-session `VEX` short retention after the `86600` peak
- Failure class: `inventory`
- Reusable lesson: a plain `VEX` control can engage, but it needs an explicit late-session retention or no-new-entry rule

### Carry-Forward Output

- Validated carry-forward principle opened or reinforced: `VEX` should remain the primary base product over `HYDRO`
- Untested hypothesis opened: a simple late-session stop or no-new-entry rule may preserve most of the control edge
- Anti-pattern reinforced: treating open-short mark gains as robust validation

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `continue`
- Decision vs champion: `not applicable`
- Candidate class: `experimental`

## Next Action

- Next: keep `r4_s01` as the Pack A baseline, but route the next VEX-only challenger to retention control rather than more broad feature layering.
