# Run Summary: `r4_s06_counterparty_concentration_gate`

## Run Metadata

- Run ID: not exposed in saved platform artifact
- Date: 2026-04-27
- Round: `round_4`
- Member / owner: `noel`
- Candidate ID: `r4_s06_counterparty_concentration_gate`
- Variant ID: `base`
- Decision relevance: `canonical`
- Bot path: `rounds/round_4/bots/noel/canonical/r4_s06_counterparty_concentration_gate.py`
- Parent bot: `r4_s01_vex_base_control`
- Strategy spec: `rounds/round_4/workspace/04_strategy_specs/spec_pack_d_counterparty_defensive.md`
- Variant hypothesis: concentration state should improve context quality over raw names
- Insight being tested: engineered counterparty context beats plain anchor behavior
- Linked signal/regime assumption: `counterparty_concentration_context`
- Raw artifact path: `rounds/round_4/performances/noel/historical/r4_s06_counterparty_concentration_gate.{json,log}`
- Data day / source: day `3`, real platform artifacts
- Baseline / comparison run: `r4_s10_5200_signal_only_veto`
- Changed axis: feature toggle
- Exact change: concentration gate on top of the live `VEX` branch
- Expected effect based on EDA/understanding: filter weaker states while preserving good `VEX` entries
- Falsification metric: late bad trade still occurs or total path worsens
- Validation check: compare late-session behavior and path retention against other Pack D bots

## Result Summary

- Status: `FINISHED`
- Profit / score: `-1.515625`
- Runtime issues: none observed
- Rejections or errors: none visible
- Position-limit concerns: none visible; final `VEX` position `-16` stayed inside the `200` limit
- PnL source: `real platform PnL`

## Run Classification

- Strategy family: `counterparty defensive concentration gate`
- Tested feature / signal: concentration / dominance state
- Changed axis type: `feature toggle`
- Dedup key: `r4_s06 + pack_d + concentration_gate + day3 + real_platform`
- Dedup verdict: `new`
- Knowledge delta: `contradicts`
- ROI-gated memory action: `update`
- Memory action rationale: this is the cleanest direct test showing that the concentration gate did not prevent the bad late sell
- Round adaptation audit: `passed`
- Portability: `uncertain`
- Branch posture: `edge then reversal`
- Reroute: `signal-only reuse`

## Run Diagnostics

- Product PnL split: `VELVETFRUIT_EXTRACT -1.515625`
- Final positions: `VELVETFRUIT_EXTRACT -16`
- Own trades: `3`
- Buy / sell qty: `0 / 16`
- Matched qty: `16`
- Avg buy / avg sell: `n/a / 5253.69`
- Peak PnL: `86.22`
- End from peak: `-111.70`
- Max drawdown: `-131.10`
- Max abs position: `16`
- Inventory / mark caveat: negative final result came from holding a larger open short into the close

## Feature Diagnostics

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| concentration gate | prevent weak contextual entries | failed to block the additional sell at `99400` and ended below zero | tradeHistory plus graph path review | down | use only if re-specified or discarded |

## Findings

- Finding: the concentration gate preserved the early `VEX` sells but still allowed the harmful late-session extension.
- Signal/regime evidence verdict: `weakens`
- Process/multivariate evidence verdict: `weakens`
- Verdict basis: relative to `r4_s10`, the gate failed at the exact decision point that mattered most for final retention.

## Post-Run Research

- Analysis status: `lightweight`
- Source artifacts: saved `.py`, `.json`, `.log`
- Compared against: `r4_s10_5200_signal_only_veto`
- Memory file change: `updated`
- ROI-gated memory action: `update`

### Failure-Driven Analysis

- Losing product / interval: `VEX` late sell at `99400`
- Failure class: `timing`
- Evidence: the branch matched `r4_s10` until the extra sell, then finished below zero while `r4_s10` stayed positive
- Reusable lesson: broad concentration state was not the right veto for the most harmful late-session extension

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop: `discard`
- Decision vs champion: `reject`
- Candidate class: `reject`

## Next Action

- Next: drop concentration gating as a standalone Wave 2 axis unless later EDA finds a cleaner activation definition than the current one.
