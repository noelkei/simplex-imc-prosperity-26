# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-25

## What Has Been Done

- Generated the original 7 formal strategy candidates and the later learning-first matrix.
- Converted the first challenger failures into a Wave 1 learner backlog.
- Completed the full 39-run synthesis linking EDA claims, strategy families, bots, and realized platform outcomes.
- Added `03_next_wave_bot_planning.md` to audit backlog coverage, paper coverage, new path-derived hypotheses, and the recommended next-wave queue.
- Converted that planning into `04_strategy_specs/spec_learning_batch_wave2.md`.
- The Wave 2 spec was then explicitly deadline-deferred for implementation and turned into a concrete 19-bot manifest plus canonical bot batch.

## Current Findings

- The strongest current live family is clean delta-1 microstructure on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`.
- Historical ITM/VEX winners still matter, but the ITM leg now looks more like an add-on than a standalone leader.
- The broad active voucher family is weaker than originally expected.
- `VEV_5100` and `VEV_5200` should now be treated as the strongest strike-level negative evidence.
- `VEV_5000` is weak, `VEV_5300` is the least-bad active strike, and inventory helps only on a cleaned subset.
- Upper and surface branches remain exploratory and currently non-promotable.
- Only two old backlog items remain high-ROI carry-forwards: `L03` and `L11`.
- The strongest open strategy gap is now redesigned selective active-voucher exits, not a missing product family.
- The user-directed full-universe coverage goal widened the Wave 2 batch from the earlier 12-14 recommendation to a 19-bot spec with a clear split between core and coverage bots.

## Decisions Made

- The old “wave 1 unrun” strategy posture is obsolete.
- The next strategy step should start from the synthesis report, not from the original learner-priority order.
- The next formal strategy decision most likely needs to compare:
  1. delta-1-first,
  2. delta-1 plus ITM add-on,
  3. delta-1 plus a very selective active subset such as `5000 + 5300`.
- The next-wave planning artifact recommends a smaller sharper batch (`12-14` bots) rather than another 25-bot sweep.
- The user-directed whole-universe coverage requirement ultimately resolved as a 19-bot Wave 2 implementation cut, not a theoretical future option.

## Open Questions / Blockers

- Phases 00-02 reviews still pending (non-blocking for Phase 03).
- Need a human or agent strategy decision on whether vouchers remain central or become secondary overlays.
- Need first live evidence from the implemented Wave 2 batch to decide whether vouchers remain central or become selective overlays only.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md)
- [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md)
- [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Use the first Wave 2 platform runs to decide whether the new champion family is pure delta-1, delta-1 plus ITM overlay, or delta-1 plus a much more selective active-voucher addon.

## Deadline Risk

Unknown. The bottleneck is now choosing the right direction, not generating more raw evidence.
