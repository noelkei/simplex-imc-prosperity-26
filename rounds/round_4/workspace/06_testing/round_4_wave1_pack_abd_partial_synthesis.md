# Round 4 Wave 1 Partial Synthesis: Packs A, B, D

## Status

`READY_FOR_REVIEW`

## Scope

- Round: `round_4`
- Packs covered: `A delta-1 controls`, `B round-3 revalidation`, `D counterparty defensive`
- Source runs:
  - `r4_s01`, `r4_s02`
  - `r4_s03`, `r4_s13`, `r4_s15`
  - `r4_s05`, `r4_s06`, `r4_s10`
- Why this synthesis exists: to convert the first usable Wave 1 run evidence into reusable strategy/spec decisions before a second wave is designed
- Downstream decision impacted: reopening `Phase 03 Strategy` and `Phase 04 Spec` for a smaller, more intentional mini-wave

## Quick Scoreboard

| Candidate | Pack | Profit | Own Trades | Differentiating Leg Activated? | Branch Posture | Immediate Take |
| --- | --- | ---: | ---: | --- | --- | --- |
| `r4_s01_vex_base_control` | A | `15.046875` | `2` | yes, but only `VEX` | edge then reversal | valid baseline, weak retention |
| `r4_s02_hydro_base_control` | A | `0.0` | `0` | no | no edge | standalone `HYDRO` slot is low ROI |
| `r4_s03_vex_4000_overlay` | B | `15.046875` | `2` | no `VEV_4000` trades | not cleanly tested | collapsed to `r4_s01` |
| `r4_s13_4000_benign_flow_overlay` | B | `-1.515625` | `3` | no `VEV_4000` trades | edge then reversal | context changed `VEX`, not `4000` |
| `r4_s15_round3_winner_revalidation` | B | `0.0` | `0` | no | not cleanly tested | over-filtered old winner branch |
| `r4_s05_mark22_veto_gate` | D | `0.0` | `0` | no | not cleanly tested | hard veto shut the branch off |
| `r4_s06_counterparty_concentration_gate` | D | `-1.515625` | `3` | partially | edge then reversal | concentration gate missed the bad late sell |
| `r4_s10_5200_signal_only_veto` | D | `3.9609375` | `2` | yes, as veto only | signal-only candidate | best reusable contextual feature in A/B/D |

## Lightweight Contract / Rule Check

- `python -m py_compile` passed for all eight reviewed bots.
- All eight reviewed files return `orders, 0, trader_data`.
- No reviewed bot file references manual-only products or a round-2 `bid()`
  method.
- Observed platform runs stayed inside the documented product limits:
  - `VEX` final observed positions were between `0` and `-16`
  - no direct `VEV_4000` or `VEV_5200` inventory appeared in the reviewed subset

## Cluster / Dedup Findings

- `r4_s03` produced the same platform JSON result as `r4_s01`: the advertised `4000` overlay never activated, so Pack B baseline evidence is really just Pack A baseline evidence.
- `r4_s15` and `r4_s05` both ended as full no-trade branches: different hypotheses, same practical outcome of over-shutdown.
- `r4_s06` and `r4_s13` converged to the same negative terminal result shape: both added a late extra `VEX` sell without ever validating their differentiating overlay thesis.

## Pack Conclusions

### Pack A

- `VEX` remains the only live delta-1 base worth carrying forward from this subset.
- `HYDRO` did not engage at all and should not get another standalone Wave 2 slot without new linked-product evidence.
- The `VEX` base still needs retention protection:
  - peak PnL `143.01`
  - end-from-peak `-148.92`
  - final state was an open `VEX` short, not a realized round-trip

### Pack B

- The direct `4000` overlay thesis was not actually tested online in this batch.
- None of the three Pack B bots opened direct `VEV_4000` inventory or generated `VEV_4000` PnL.
- The two richer branches either:
  - changed only late `VEX` timing and worsened the path (`r4_s13`), or
  - shut the whole family off (`r4_s15`)
- Strategy implication: do not treat Pack B as a failed `4000` overlay thesis; treat it as a failed Pack B implementation design for clean online testing.

### Pack D

- The strongest result in the novelty layer was not a full defensive bot, but a reusable timing filter.
- `r4_s10` matched the early path of `r4_s06` and then skipped the harmful `99400` `VEX` sell.
- The saved trade tape around the divergence matters:
  - `98900`: `VEV_5200` printed with `Mark 22` on the seller side
  - `98900`: `VEV_5300` printed with `Mark 22` on the seller side
  - `99400`: `r4_s06` still sold `VEX`, while `r4_s10` did not
- Strategy implication: counterparty information looks more valuable as a signal-only veto than as a standalone defensive architecture.

## Product / Role Review

| Product Or Scope | Role Class | Interaction Class | Evidence From Runs | Downstream Implication |
| --- | --- | --- | --- | --- |
| `VELVETFRUIT_EXTRACT` | base / anchor | standalone usable | only live product across all A/B/D branches | keep central in Wave 2 |
| `HYDROGEL_PACK` | base | standalone usable but weak | zero engagement in `r4_s02` | deprioritize |
| `VEV_4000` | structural overlay | usable only with anchor | zero direct trades in all Pack B bots | reopen only with a cleaner activation design |
| `VEV_5200` | monitor | mainly veto / anti-signal | helped identify the harmful late window in `r4_s10` | reuse as context, not inventory |

## Timing / Retention Findings

| Finding | Evidence | Downstream Use |
| --- | --- | --- |
| late-session retention is the main control weakness | `r4_s01` peaked at `86600` and gave back `148.92` by the end | build a retention-aware `VEX` challenger |
| hard gates are too expensive when they fully suppress the branch | `r4_s05` and `r4_s15` produced zero trades | use lighter vetoes or cooldowns |
| toxic-family context is useful when it removes the last bad extension, not when it tries to define the whole bot | `r4_s10` skipped the `99400` sell that hurt `r4_s06` | reuse the feature as an overlay |

## Carry-Forward Implications

- Promote into strategy framing:
  - `VEX` over `HYDRO` as the primary base choice
  - `5200` / `Mark 22` as timing context, not direct alpha
  - retention control as a first-class Wave 2 axis
- Keep as EDA-only caution:
  - do not label `4000` dead; label it untested under current activation
- Needs fresh current-round validation:
  - any direct `4000` add-on
  - any hard `Mark 22` whole-bot veto

## Suggested Wave 2 Shape

- `protect winner`: one `VEX`-base or stronger family bot with late-session no-new-entry / cooldown logic
- `signal-only reuse`: one challenger that layers the `5200` veto onto the strongest live branch rather than a standalone defensive bot
- `clean coverage`: at most one simplified `4000` re-test if we can force actual `VEV_4000` activation and attribution
- `prune`: no standalone `HYDRO` control and no composite Pack B winner stack in the next mini-wave

## Linked Artifacts

- Run summaries:
  - `../../performances/noel/canonical/run_20260427_1900_r4_s01_vex_base_control.md`
  - `../../performances/noel/canonical/run_20260427_1902_r4_s02_hydro_base_control.md`
  - `../../performances/noel/canonical/run_20260427_1904_r4_s03_vex_4000_overlay.md`
  - `../../performances/noel/canonical/run_20260427_1906_r4_s05_mark22_veto_gate.md`
  - `../../performances/noel/canonical/run_20260427_1908_r4_s06_counterparty_concentration_gate.md`
  - `../../performances/noel/canonical/run_20260427_1910_r4_s10_5200_signal_only_veto.md`
  - `../../performances/noel/canonical/run_20260427_1912_r4_s13_4000_benign_flow_overlay.md`
  - `../../performances/noel/canonical/run_20260427_1914_r4_s15_round3_winner_revalidation.md`
- Post-run memory: `../post_run_research_memory.md`
- Retrospective EDA addendum: `../01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`
- Next action: reopen `Phase 03` and `Phase 04` with a small Wave 2 challenger set built around retention and `5200` veto reuse
