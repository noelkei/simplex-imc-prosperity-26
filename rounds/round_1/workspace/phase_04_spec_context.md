# Phase 04 Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Approved with caveats 2026-04-17 for next-wave matrix, high-ROI batch, and candidate 27/28 threshold refinements
- Last updated: 2026-04-17

## What Has Been Done

- Added `04_strategy_specs/spec_experimental_5_bot_matrix.md`.
- Added `04_strategy_specs/spec_next_wave_10_bot_matrix.md`.
- Added `04_strategy_specs/spec_high_roi_3_variant_batch.md` for `candidate_24`, `candidate_25`, and `candidate_26`.
- Added `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md` for `candidate_27` and `candidate_28`.
- Previous specs remain reference material:
  - `04_strategy_specs/spec_candidate_03_combined.md`
  - candidate 01 and candidate 02 specs.

## Current Findings

- The five-bot matrix spec defines signals, execution logic, risk handling, state/runtime, and validation checks.
- The next-wave 10-bot matrix spec defines the Kalman, HMM, edge-quality, lifecycle, policy-table, IPR execution, scheduler, one-sided, micro-overlay, and adaptive-controller implementation batch.
- Spec approval is limited to performance exploration, not final submission selection.
- The high-ROI batch spec keeps IPR +80 unchanged and tests only ACO size/skew, conservative residual-regime gating, and one-sided/book-state exits.
- The candidate 27/28 spec keeps IPR +80 unchanged and tests only ACO threshold refinements over `candidate_26`.

## Decisions Made

- Implementation may proceed for the five Noel bots.
- Implementation may proceed for the ten next-wave Noel bots.
- Implementation may proceed for the three high-ROI variants requested by the user:
  - `candidate_24_v1_a1b1_size_skew_refine`
  - `candidate_25_v2_a2b1_conservative_regime_gate`
  - `candidate_26_v3_a3b1_one_sided_exit_overlay`
- Implementation may proceed for the two threshold refinements requested by the user:
  - `candidate_27_v1_c26_soft_flatten`
  - `candidate_28_v1_c26_strict_one_sided`
- Promote only after validation.

## Open Questions / Blockers

- None for spec. Validation remains pending.

## Linked Artifacts

- `04_strategy_specs/spec_experimental_5_bot_matrix.md`
- `04_strategy_specs/spec_next_wave_10_bot_matrix.md`
- `04_strategy_specs/spec_high_roi_3_variant_batch.md`
- `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`
- `03_strategy_candidates.md`
- `phase_03_strategy_context.md`

## Next Priority Action

Run platform submissions for `candidate_27` and `candidate_28`, then compare against the existing `candidate_26` platform leader.

## Deadline Risk

Medium until validation confirms a usable candidate.
