# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Claude
- Reviewer: Bruno (shortlist approval 2026-04-15, deadline deferral recorded)
- Review outcome: deferred under deadline

## Last Updated

2026-04-16

## What Has Been Done

- Wrote `spec_candidate_01_ipr_drift.md` and `spec_candidate_02_aco_fixedfv.md`.
- Both specs cover signal, execution, position/risk, state, failure cases, validation, and parameters.
- Inspected historical bot `TEST1_merged.py` as non-authoritative implementation context; linked specs remain the authoritative implementation source.

## Current Findings

- IPR spec: FV = `ipr_start_price + timestamp * 0.001`. Day-reset detection. HALF_SPREAD=4.
- ACO spec: FV = 10000 (constant). HALF_SPREAD=5. Stateless.
- Both specs are implementation-eligible under recorded deadline deferral.

## Decisions Made

- Deadline deferral: full independent review waived. Human shortlist approval accepted as review.
- Intended combined bot: `candidate_03_combined.py`.
- Robustness pass found the canonical bot file is missing, so implementation tracking is blocked until it is restored or created.

## Linked Artifacts

- [`04_strategy_specs/spec_candidate_01_ipr_drift.md`](04_strategy_specs/spec_candidate_01_ipr_drift.md)
- [`04_strategy_specs/spec_candidate_02_aco_fixedfv.md`](04_strategy_specs/spec_candidate_02_aco_fixedfv.md)

## Next Priority Action

Restore or create the missing canonical bot from the linked specs, then run platform simulator and record results.
