# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Kept the six highest-ROI Wave 2 bots active:
  `r4_w2_01`, `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`.
- Replaced the other nine active slots with new entry-quality and option-only
  attribution probes.
- Updated the shared Wave 2 engine in
  [`../bots/noel/canonical/wave2_shared_engine.py`](../bots/noel/canonical/wave2_shared_engine.py)
  to support the refined queue.
- Applied a fill-seeking recalibration pass to the active option branches after
  debugging showed they were materially more passive than the useful Wave 1
  bots.
- Regenerated the full active upload set in `canonical/` as standalone
  `*_debugged.py` files.
- Moved superseded Wave 1 bots and superseded Wave 2 draft files into
  [`../bots/noel/historical/`](../bots/noel/historical/).
- Re-ran local compilation and `Trader.run()` smoke checks on the active
  upload set.

## Current Findings

- `canonical/` now represents only the live queue we actually want to upload.
- `historical/` now holds:
  - Wave 1 bots with existing performance history
  - retired pre-fix or superseded Wave 2 variants
- The refined queue is materially more signal-seeking than the prior version:
  less overlap in retention overlays, more direct entry and option-only tests.
- Local replay now shows materially more option crossing activity in the active
  `5300` and `4000` branches after the recalibration.

## Decisions Made

- The active upload set is the debugged series only.
- The old Wave 2 filenames without `_debugged.py` are no longer part of the
  live queue.
- Strategy IDs were refined in-place where needed so the implementation can
  preserve the 15-slot wave while changing the actual questions being tested.

## Open Questions / Blockers

- No implementation blocker remains.
- Fresh platform reruns are still required before pruning further.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/`](04_strategy_specs/)
- [`../bots/noel/canonical/`](../bots/noel/canonical/)
- [`../bots/noel/historical/`](../bots/noel/historical/)

## Next Priority Action

Hand the refined upload set into `Phase 06` in this order:
`r4_w2_01`, `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`,
then `r4_w2_02`, `r4_w2_06`, and `r4_w2_14`.

## Deadline Risk

Medium: the implementation layer is cleaner now, but the remaining ROI depends
on fast reruns and disciplined pruning.
