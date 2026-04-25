# Phase 07 - Debugging And Iteration Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-25

## What Has Been Done

- Created a debugging note for the failed broad active-voucher challengers.
- Validated that the corrected centered composite and the inventory variant both fail on the broad active basket.
- Ran and analyzed the full 25-bot Wave 1 learner batch.
- Folded the new debugging evidence into `06_testing/round_3_full_performance_synthesis.md`.

## Current Findings

- The broad `VEV_5000-5300` basket should stay paused.
- `VEV_5100` and `VEV_5200` are the clearest reject-by-default strikes.
- `VEV_5000` is weak and `VEV_5300` is only the least-bad active strike, not a standalone winner.
- Clean isolated delta-1 logic is now the strongest live family.
- ITM is currently an add-on-quality branch, not the main engine.
- Upper and surface branches are informative but not promotable in their current implementations.

## Decisions Made

- The current issue is no longer “why did the broad active basket fail?” only; it is now “what survives after branch isolation?”
- Debugging focus should move from composite rescue to branch pruning and selective recombination.
- The next debugging target is strategic architecture, not Trader contract correctness.

## Open Questions / Blockers

- Should the next design wave start from delta-1 only, or delta-1 plus a selective voucher add-on?
- Should `VEV_5000 + VEV_5300` remain in scope while `VEV_5100/5200` are removed?
- Should the upper and surface branches be paused entirely for the next cycle?

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_debugging/README.md`](06_debugging/README.md)
- [`06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md`](06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Turn the synthesis into the next strategy/spec decision. The likely path is delta-1-first with heavy voucher pruning, but that choice belongs to the next explicit strategy step.

## Deadline Risk

Unknown.
