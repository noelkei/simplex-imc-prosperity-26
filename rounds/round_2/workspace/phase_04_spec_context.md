# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-19

## What Has Been Done

- Accepted Phase 03 Strategy as `approved with caveats`.
- Read `skills/write_strategy_spec.md`, the strategy spec template, Round 2 wiki
  facts, Trader contract, datamodel, runtime, and trading rules.
- Created specs for all 10 Round 2 strategy candidates under
  `04_strategy_specs/`.
- Human approved all 10 specs with caveats for implementation and log
  collection.
- Classified `R2-CAND-09` as overlay-only and `R2-CAND-10` as mechanics-only,
  not standalone alpha bots.

## Current Findings

- Specs are approved with caveats:
  - `spec_r2_cand_01_ipr_drift_fv_maker.md`
  - `spec_r2_cand_02_ipr_residual_extreme_execution.md`
  - `spec_r2_cand_03_aco_reversal_maker.md`
  - `spec_r2_cand_04_aco_top_imbalance_skew.md`
  - `spec_r2_cand_05_aco_microprice_challenger.md`
  - `spec_r2_cand_06_aco_full_book_depth_backup.md`
  - `spec_r2_cand_07_combined_ipr_aco_imbalance.md`
  - `spec_r2_cand_08_combined_ipr_aco_reversal.md`
  - `spec_r2_cand_09_spread_defensive_overlay.md`
  - `spec_r2_cand_10_maf_bid_policy.md`
- Highest-priority implemented specs remain `R2-CAND-07`,
  `R2-CAND-01`, `R2-CAND-04`, and `R2-CAND-03`.
- `R2-CAND-10` uses safe `bid()` placeholder `0`; final nonzero MAF posture is
  still undecided.
- Battery 01 produced a Generation 2 queue, and current Phase 04 completion now
  covers both the original 10 Battery 01 specs and the compact Gen2 spec.
- Gen2 compact spec has now been written:
  `spec_r2_gen2_bruno_battery.md`.

## Decisions Made

- Phase 04 is `COMPLETED` with review outcome `approved with caveats`.
- Bot implementation was unblocked by human approval with caveats.
- Implementation owner should be `noel` when specs are approved, matching the
  user's requested canonical path.
- User requested implementation of the 13 Gen2 bots under Bruno canonical; this
  is recorded as approval with caveats for the compact Gen2 spec.

## Open Questions / Blockers

- Exact Round 2 deadline is unknown.
- MAF final nonzero bid risk posture remains undecided; implemented C10 uses
  safe `bid()` placeholder `0`.
- Manual RSS allocation remains separate and unresolved.
- Better platform `market_trades` logs are still missing for any future
  trade-pressure feature.
- Gen2 Battery 02 performance evidence is still missing.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/README.md`](04_strategy_specs/README.md)
- [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md)
- [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md)

## Next Priority Action

Phase 04 specs are approved with caveats for Battery 01 and Gen2. Next useful
work is Gen2 Battery 02 testing, not additional spec expansion.

## Deadline Risk

Unknown. If deadline pressure becomes explicit, specs may be deferred under
deadline only with a recorded decision.
