# Phase 07 - Debugging And Iteration Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Converted the old Wave 2 passivity / comparability problem into archived
  evidence.
- Distilled the reusable debugging output into three final one-axis variants on
  top of the current champion family:
  - `late_freeze`
  - `Mark22_veto`
  - `giveback_stop`
- Removed the need to debug the old mixed live queue further by archiving it.

## Current Findings

- The main remaining debugging question is no longer “why didn’t this bot
  trade?”.
- The only live debugging question is whether the champion family can retain
  more of its peak without killing the core edge.
- `Mark 22 / 5200` now has a bounded role: veto of fresh extension, not broad
  architectural gating.

## Decisions Made

- Do not reopen broad Wave 2 debugging.
- Do not reopen the old `round_3` toxic basket as a debugging branch.
- Keep debugging tightly attached to the three new derivatives only.

## Open Questions / Blockers

- Need live reruns to confirm whether any of the three new derivatives is a
  real retention improvement.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md)
- [`phase_05_implementation_context.md`](phase_05_implementation_context.md)

## Next Priority Action

Treat the first rerun slice as a debugging and validation slice for
`01`, `02`, `08`, `09`, and `10`.

## Deadline Risk

Medium: the debugging surface is now small and intentional, but the winner
protection thesis still needs live confirmation.
