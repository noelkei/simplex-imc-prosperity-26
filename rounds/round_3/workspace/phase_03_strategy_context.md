# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Generated the original 7 formal strategy candidates and the later learning-first matrix.
- Converted the first challenger failures into a Wave 1 learner backlog.
- Completed the original 39-run synthesis linking EDA claims, strategy families, bots, and realized platform outcomes, later extended that evidence base to the full 58-run post-Wave-2 synthesis, and now extended it again to the 82-run post-Wave-3 synthesis.
- Added `03_next_wave_bot_planning.md` first as a pre-Wave-2 queue builder and then refreshed it into a full post-Wave-2 next-wave planning artifact with VEX-linked voucher handling, inverse-diagnostic policy, complexity ladder, and an `11`-core / `14`-with-diagnostics recommended cut.
- Expanded that planning into the user-directed final exploratory Wave 3 cut: `24` bots covering delta-1 exploitation, VEX-linked `5300` rescue, transformed thresholds, lightweight trend gates, tiny inverse diagnostics, and two Kalman tests.
- Converted that planning into `04_strategy_specs/spec_learning_batch_wave2.md`.
- The Wave 2 spec was then explicitly deadline-deferred for implementation and turned into a concrete 19-bot manifest plus canonical bot batch.
- Wave 2 has now been fully run, archived, and folded into the evolving synthesis history.
- Wave 3 has now also been fully run, archived, and folded into the updated 82-run synthesis.
- Refreshed `03_next_wave_bot_planning.md` into a winner-focused post-Wave-3 planning artifact that recommends a `10`-bot core wave or `12` bots if closure-quality diagnostics are still wanted.
- Converted that planning into the concrete Wave 4 finalist cut: a 12-bot
  batch that keeps the pure champion family, ports the ITM overlay thesis onto
  the champion base, keeps only tightly bounded `5300` overlays/salvage, and
  spends one slot on forced inverse closure.
- Wave 4 has now been fully run, folded into the `94`-run synthesis, and
  archived from `canonical/` to `historical/`.
- Refreshed `03_next_wave_bot_planning.md` again into a post-Wave-4
  exploitation plan: keep the current clean finalists, but spend the next wave
  mainly on `>10k` upside-distillation descendants with strong retention
  controls.
- Consumed that planning into the concrete Wave 5 cut: `12` bots split across
  winner protection, pure fallback, pruned `>10k` descendants, and
  toxic-strike-as-signal variants.

## Current Findings

- The strongest current full-stack family is now `W4-03/W4-04/W5-01`, while
  the strongest pure fallback benchmark is `W5-04 = 1672.000`.
- The best clean architecture remains `delta-1 + ITM` on the Kalman base, not pure `delta-1` alone, even though pure `delta-1` closes the round as the best standalone control.
- Wave 4 also resolved a second question: `5300` is still usable only as a
  tiny rescue / overlay candidate, not as a normal finalist family.
- The broad active voucher family remains weaker than originally expected, but
  the giant `>10k` and `~18k` peaks still show there is real upside in the
  old active regime if it can be heavily distilled and properly retained.
- `VEV_5100`, `VEV_5000`, and `VEV_5200` remain the dominant giveback drivers
  in the giant-peak runs; `VEV_5300` remains less toxic but still not good
  enough as a standalone endgame branch.
- The strongest open strategy gap is now very specific:
  - preserve the new clean winner,
  - then attack the upside ceiling by building descendants of `B08/C06/B04/B03/B06`
    with strike pruning, `VEX` anchoring, transformed thresholds, and strict
    retention logic.
- That Wave 5 recommendation was implemented, partially observed, and is now
  absorbed into the closeout. The next uncertainty is no longer which Round 3
  bots to build, but which strategy principles deserve to transfer into
  `round_4`.

## Decisions Made

- The old “wave 1 unrun” strategy posture is obsolete.
- The next strategy step should start from the `94`-run synthesis, not from the
  original learner-priority order.
- The next formal strategy decision should compare:
  1. `W4-03/W4-04` class clean finalists,
  2. conservative fallback finalists (`W4-01/W4-11` class),
  3. and a last wave of `>10k` upside-distillation descendants.
- Direct inverse trading is now lower priority than using toxic strikes as
  filters / vetoes / transformed-threshold inputs.
- Simple observable regime gates, transformed thresholds, lightweight trend
  gates, and Kalman smoothing remain preferred over HMM / hidden-state
  complexity.

## Open Questions / Blockers

- Phases 00-02 reviews still pending (non-blocking for Phase 03).
- No strategy-design blocker remains before coding.
- No external blocker remains before the next strategy pass.
- No strategy-design blocker remains before live execution.
- No Round 3 strategy blocker remains. The open issue is only how strongly to
  carry these conclusions into `round_4`.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Round 3 strategy work is done. The next step is to consume the closeout
package in `round_4` and reuse it as framing, not to open another Round 3
strategy batch.

## Deadline Risk

Unknown. The bottleneck is now choosing the right direction, not generating more raw evidence.
