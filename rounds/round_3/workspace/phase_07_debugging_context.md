# Phase 07 - Debugging And Iteration Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Created a debugging note for the failed broad active-voucher challengers.
- Validated that the corrected centered composite and the inventory variant both fail on the broad active basket.
- Ran and analyzed the full 25-bot Wave 1 learner batch.
- Folded the new debugging evidence into `06_testing/round_3_full_performance_synthesis.md`.
- Folded the full 19-bot Wave 2 batch back into the synthesis, including markouts, `>5k` peak study, and no-trade candidates.
- Fed the resulting debugging conclusions into the Wave 3 design cut: explicit no-trade gates, transformed thresholds, trend gates, inverse diagnostics, and compact Kalman variants.
- The Wave 3 batch has now been run and archived; the next debugging step is to inspect which branches actually preserved peak quality and which still gave it back.
- That inspection has now been done through the later 94-run synthesis,
  including `>10k` peak salvage counterfactuals and the Wave 4 finalist
  decision board.
- Converted those debugging conclusions into a Wave 4 finalist implementation:
  pure champion, champion plus ITM, selective `5300`, distilled peak-salvage,
  and one forced inverse closure bot.
- Wave 4 has now been fully run, archived, and folded into the updated
  `94`-run synthesis and finalist decision board.
- Converted the post-Wave-4 debugging conclusions into the Wave 5 batch:
  winner protection, realistic time-window retention gates, pruned
  `>10k` descendants, and toxic-strike-as-signal variants.
- Folded the observed partial Wave 5 results back into the `101`-run synthesis and converted the debugging output into an explicit closeout artifact.

## Current Findings

- The broad `VEV_5000-5300` basket should stay paused.
- `VEV_5100` and `VEV_5200` are the clearest reject-by-default strikes.
- `VEV_5000` is weak at every tested horizon and should no longer be treated as default selective-active ballast.
- `VEV_5300` is still not a standalone winner, but it is the only active strike with positive `10k` mean trade markout.
- Clean isolated delta-1 logic is now the strongest live family.
- `W4-03` is now the best clean live result in the round, and `W4-04`
  confirms the same family almost exactly; the endgame winner axis is now
  `delta-1 + ITM` on the Kalman base.
- Upper is informative but not promotable; floor now looks closeable.
- The main new debugging clue is regime timing: several selective active runs peak early and then keep trading past the useful window.
- A second new debugging clue is that the giant `>10k` and `~18k` peaks were concentrated in legacy broad active-voucher runs and could have retained `+10k` to `+16k` more under very simple giveback logic.
- A third new clue from Wave 4 is that tiny `5300` overlays can stay alive
  only as rescue overlays, but standalone or trend-led `5300` finalists are
  not strong enough to justify another normal finalist slot.
- A fourth clue is that the inverse closure bot still did not trade the target
  leg, which pushes toxic-strike logic toward veto / anti-signal use instead
  of direct inverse inventory.
- The old `>10k` peaks still matter, but now as retention and strike-selection lessons rather than as an active Round 3 execution queue.
- Partial Wave 5 evidence reinforces that toxic strikes are more useful as veto / anti-signal context than as default inventory legs.
- The debugging output is now mature enough to be carried forward as:
  - validated lessons,
  - untested hypotheses,
  - and anti-patterns.

## Decisions Made

- The current issue is no longer “why did the broad active basket fail?” only; it is now “what parts of that failure should become future framing rules?”
- Debugging focus should move from composite rescue to branch pruning,
  selective recombination, explicit no-trade / horizon control, and deciding
  which `>10k` lessons are worth carrying into a future round.
- The next debugging target is strategic architecture, not Trader contract correctness.
- Wave 3 implemented those debugging hypotheses directly; Wave 4 resolved the
  clean winner axis; Wave 5 and the closeout now convert the remaining space
  into carry-forward principles rather than more Round 3 execution.

## Open Questions / Blockers

- No Round 3 debugging blocker remains.
- The remaining open question is only how much of this debugging read should be treated as transferable to `round_4` before new data confirms it.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_debugging/README.md`](06_debugging/README.md)
- [`06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md`](06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Consume the closeout artifact and debugging conclusions as Round 4 framing:
book-level option thinking, toxic-strike-as-signal, horizon-aware rescue, and
explicit no-trade / shutdown logic.

## Deadline Risk

Unknown.
