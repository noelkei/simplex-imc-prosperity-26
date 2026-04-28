# Phase 06 - Testing And Performance Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Absorbed the full current `round_4` performance base into
  [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md).
- Crossed that evidence with the closed `round_3` peak and carry-forward
  package.
- Archived all prior current-round canonical performance artifacts into
  `historical/` before opening the new final upload wave.

## Current Findings

- The current live champion is `r4_final_05_full_otm_basket`.
- The best fallback families are still `5300`-centered, not `4000` or
  delta-1-first.
- The only remaining high-ROI unknowns are whether the three new retention and
  veto derivatives can protect more of the champion path.

## Decisions Made

- Final testing should be champion-first, not broad exploration.
- All old canonical performance artifacts are now evidence only, not live queue
  state.
- Missing performance for the archived dead-end bots is treated as non-ROI for
  this last pass.

## Open Questions / Blockers

- Need fresh platform reruns on the final `10`-bot pack.
- Need real platform evidence before selecting the final submission file.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`phase_05_implementation_context.md`](phase_05_implementation_context.md)

## Next Priority Action

Upload and rerun the final pack in this order:
`01`, `02`, `08`, `09`, `10`, then `03`, `04`, `05`, `06`, `07`.

## Deadline Risk

Medium: the evidence base is clean now, but submission selection still depends
on one final live ranking pass.
