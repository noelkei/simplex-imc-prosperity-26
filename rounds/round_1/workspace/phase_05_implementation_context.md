# Phase 05 - Implementation Context

## Status

BLOCKED

## Owner / Reviewer

- Owner: Claude
- Reviewer: Bruno
- Review outcome: not reviewed (artifact missing)

## Last Updated

2026-04-16

## What Has Been Done

- Specs exist for `candidate_01_ipr_drift` and `candidate_02_aco_fixedfv`.
- The workspace previously recorded `candidate_03_combined.py` as implemented, but the canonical file is not present in `rounds/round_1/bots/bruno/canonical/`.
- Implementation is therefore blocked until the canonical bot is restored or created from the approved or deadline-deferred specs.

## Current Findings

- Intended bot: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`
- Current state: file missing.
- Expected parameters from specs:
  - `IPR_DRIFT_RATE = 0.001`, `IPR_HALF_SPREAD = 4`, `IPR_SKEW_FACTOR = 2`
  - `ACO_FAIR_VALUE = 10000`, `ACO_HALF_SPREAD = 5`, `ACO_SKEW_FACTOR = 2`

## Decisions Made

- `candidate_03_combined` remains the intended implementation target, not an active runnable bot.
- `TEST1_merged.py` is archived historical — not active.

## Open Questions / Blockers

- **Blocking:** Canonical bot file is missing. Do not ask humans to run platform validation until it exists.

## Linked Artifacts

- Intended missing bot: `../bots/bruno/canonical/candidate_03_combined.py`
- [`04_strategy_specs/spec_candidate_01_ipr_drift.md`](04_strategy_specs/spec_candidate_01_ipr_drift.md)
- [`04_strategy_specs/spec_candidate_02_aco_fixedfv.md`](04_strategy_specs/spec_candidate_02_aco_fixedfv.md)

## Next Priority Action

1. **Agent/Human:** Restore or create `../bots/bruno/canonical/candidate_03_combined.py` from the linked specs.
2. **Agent:** Re-check Trader contract, order signs, aggregate position capacity, and runtime.
3. **Human:** Only after the file exists, upload bot to platform, run simulator, and share results.
