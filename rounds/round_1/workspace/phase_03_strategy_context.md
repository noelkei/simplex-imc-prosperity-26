# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Unassigned (human shortlist approval needed)

## Last Updated

2026-04-15

## What Has Been Done

- Generated 3 strategy candidates based on EDA + understanding.
- Built candidate table with evidence strength, cost, risk, and priority ratings.
- Wrote candidate detail sections (edge, execution sketch, parameters, validation checks).
- Proposed shortlist and identified human decisions needed.

## Current Findings

- `candidate_01_ipr_drift`: IPR drift market maker. FV = `day_start_price + t * 0.001`. HALF_SPREAD = 4–5 ticks.
- `candidate_02_aco_fixedfv`: ACO fixed-FV market maker. FV = 10,000. HALF_SPREAD = 5 ticks. Position skew at ±40.
- `candidate_03_combined`: both strategies in one bot. Primary submission candidate.

## Decisions Made

- Shortlist: candidates 01, 02, 03.
- Manual challenge is a human platform action. Recommended bids: DRYLAND_FLAX ≤ 29, EMBER_MUSHROOM ≤ 19.80.

## Open Questions / Blockers

- **Human decision needed:** Approve shortlist before agent writes specs.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`02_understanding.md`](02_understanding.md)

## Next Priority Action

1. **Human:** Approve shortlist in `03_strategy_candidates.md`.
2. **Agent:** Write `04_strategy_specs/spec_candidate_01_ipr_drift.md` and `04_strategy_specs/spec_candidate_02_aco_fixedfv.md`.

