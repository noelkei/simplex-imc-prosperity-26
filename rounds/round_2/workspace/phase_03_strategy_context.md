# Phase 03 - Strategy Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-19

## What Has Been Done

- Accepted Phase 02 Understanding as `approved with caveats`.
- Replaced the old fixed strategy/bot caps with an ROI-driven candidate queue
  philosophy in system docs, skills, templates, and Round 2 state.
- Read the approved Understanding, consolidated EDA, strategy workflow,
  strategy template, and `skills/generate_strategy_candidates.md`.
- Wrote `03_strategy_candidates.md` with a strategy exploration board,
  per-product branches, compatibility matrix, candidate table, prioritized queue,
  rejected/deferred ideas, decision trace, and next action.
- Preserved challenge boundaries: algorithmic trading, MAF mechanics, and manual
  Research / Scale / Speed remain separate.

## Current Findings

- Phase 03 retains 10 differentiated candidates because they are ROI-relevant
  and test distinct hypotheses, roles, or mechanics.
- After Battery 01 validation, the active next strategy queue is the
  Generation 2 queue embedded in
  [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md).
  The original 10-candidate queue remains the historical/initial exploration
  board, not the next implementation queue.
- The 13-candidate Generation 2 queue has been implemented under Bruno
  canonical for Battery 02 testing.
- Initial highest-priority spec candidates were:
  - `R2-CAND-07-COMBINED-IPR-ACO-IMBALANCE`
  - `R2-CAND-01-IPR-DRIFT-FV-MAKER`
  - `R2-CAND-04-ACO-TOP-IMBALANCE-SKEW`
  - `R2-CAND-03-ACO-REVERSAL-MAKER`
- `R2-CAND-10-MAF-BID-POLICY` is mechanics-only and must not be treated as
  normal `Trader.run()` alpha.
- Manual RSS allocation remains manual-only and is not an algorithmic candidate.
- Trade pressure, cross-product lead-lag, PCA/clustering/latent direct logic, and
  fixed Round 1 IPR fair value remain rejected or deferred.

## Decisions Made

- Strategy candidate count is ROI-driven, not fixed.
- Implementation count will be driven by reviewed specs, differentiation,
  deadline risk, and validation capacity, not a fixed bot cap.
- No bots are created in Phase 03.
- Phase 03 status is `COMPLETED` with review outcome `approved with caveats`.
- Battery 01 can update downstream strategy/spec direction without reopening
  all of Phase 03; use the post-run analysis as a Gen2 addendum.

## Open Questions / Blockers

- Exact Round 2 deadline is still unknown.
- MAF bid risk posture remains a later spec/human decision.
- Manual RSS allocation remains a separate manual decision.
- Better platform `market_trades` logs are still missing for trade-pressure work.
- Battery 02 platform results are still missing for the implemented Gen2 queue.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02_understanding.md`](02_understanding.md)
- [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`../bots/bruno/canonical/`](../bots/bruno/canonical/)

## Next Priority Action

Phase 03 is approved with caveats. For new work, use the implemented Bruno
Gen2 queue and Battery 02 validation results.

## Deadline Risk

Unknown; use fast mode if less than 24 hours remain, but keep the ROI-driven
candidate queue as backlog unless validation capacity becomes the bottleneck.
