# Phase 05 - Implementation Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Amin / OpenClaw
- Reviewer: Unassigned

## Last Updated

2026-04-19

## What Has Been Done

- Existing Amin candidate `candidate_r2_amin_hybrid_01.py` was reviewed as current baseline implementation context.
- Added new implementation `../../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py`.
- Added fast-mode one-page spec `04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md` to preserve the implementation gate under user-requested hackathon pressure.
- Local syntax compile passed for both active Amin candidates.

## Current Findings

- New candidate keeps IPR long-drift posture while making ACO fair value adaptive via a tiny Kalman state.
- New candidate is explicitly Round-2 aware via a conservative nonzero `bid()` and logic that should benefit from extra quote visibility without depending on it.
- A lightweight local replay comparison now exists and currently favors `candidate_r2_amin_hybrid_01.py` over the new Kalman variant on all three sample days, so promotion of the new bot would be premature without further tuning.

## Decisions Made

- Maximum active implementations remains 2.
- Proceeded under deadline-deferred spec flow due to explicit user request.
- Active Amin candidates are now `candidate_r2_amin_hybrid_01.py` and `candidate_r2_amin_feeaware_kalman_02.py`.
- Placeholder Market Access Fee bid for the Kalman candidate is `12` pending scenario review.

## Open Questions / Blockers

- Need better validation than the lightweight local replay before making a final submission decision, but the first comparison currently favors the old hybrid.
- Human review of the deadline-deferred spec is still desirable before final submission.
- No evidence yet that bid `12` is the right final fee.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/README.md`](04_strategy_specs/README.md)
- [`04_strategy_specs/spec_candidate_r2_amin_hybrid_ipr_drift_aco_mm.md`](04_strategy_specs/spec_candidate_r2_amin_hybrid_ipr_drift_aco_mm.md)
- [`04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md`](04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md)
- [`../bots/amin/canonical/candidate_r2_amin_hybrid_01.py`](../bots/amin/canonical/candidate_r2_amin_hybrid_01.py)
- [`../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py`](../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py)
- [`../performances/amin/canonical/candidate_comparison_2026-04-19.json`](../performances/amin/canonical/candidate_comparison_2026-04-19.json)

## Next Priority Action

Either tune the new Kalman candidate using the replay findings or, if speed matters more, commit the new research artifacts and comparison on the current branch without promoting the new bot as best yet.

## Deadline Risk

Unknown, but likely nontrivial because work is proceeding with deadline-deferred review.
