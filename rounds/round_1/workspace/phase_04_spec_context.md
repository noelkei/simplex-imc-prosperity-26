# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Claude
- Reviewer: Bruno (shortlist approval 2026-04-15, deadline deferral recorded)

## Last Updated

2026-04-15

## What Has Been Done

- Wrote `spec_candidate_01_ipr_drift.md` and `spec_candidate_02_aco_fixedfv.md`.
- Both specs cover signal, execution, position/risk, state, failure cases, validation, and parameters.
- Reviewed existing bot `TEST1_merged.py` — ACO structure reused, IPR strategy replaced.

## Current Findings

- IPR spec: FV = `ipr_start_price + timestamp * 0.001`. Day-reset detection. HALF_SPREAD=4.
- ACO spec: FV = 10000 (constant). HALF_SPREAD=5. Stateless.
- Both approved for immediate implementation under deadline deferral.

## Decisions Made

- Deadline deferral: full independent review waived. Human shortlist approval accepted as review.
- Combined into single bot `candidate_03_combined.py`.

## Linked Artifacts

- [`04_strategy_specs/spec_candidate_01_ipr_drift.md`](04_strategy_specs/spec_candidate_01_ipr_drift.md)
- [`04_strategy_specs/spec_candidate_02_aco_fixedfv.md`](04_strategy_specs/spec_candidate_02_aco_fixedfv.md)

## Next Priority Action

Run bot on platform simulator and record results.

