# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Bruno (human testing needed)

## Last Updated

2026-04-15

## What Has Been Done

- Implemented `candidate_03_combined.py` combining both specs.
- IPR: drift-tracking market maker. Initializes `ipr_start_price` on first tick. FV = start + t*0.001. Day-reset detection via `ipr_last_ts`. Aggressive fills + passive quotes + position skew.
- ACO: fixed-FV market maker. FV = 10000. Aggressive fills + passive quotes + position skew. Stateless.
- Replaced old IPR "buy max long" strategy with drift-tracking approach.
- Trader contract verified: `run()` returns `result, 0, traderData`. Order signs correct. Position limits enforced.

## Current Findings

- Bot: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`
- Parameters (all at top of file):
  - `IPR_DRIFT_RATE = 0.001`, `IPR_HALF_SPREAD = 4`, `IPR_SKEW_FACTOR = 2`
  - `ACO_FAIR_VALUE = 10000`, `ACO_HALF_SPREAD = 5`, `ACO_SKEW_FACTOR = 2`

## Decisions Made

- `candidate_03_combined` is the active implementation.
- `TEST1_merged.py` is archived historical — not active.

## Open Questions / Blockers

- **Human action needed:** Run bot on Prosperity platform simulator. Share P&L and position trace.

## Linked Artifacts

- [`../bots/bruno/canonical/candidate_03_combined.py`](../bots/bruno/canonical/candidate_03_combined.py)
- [`04_strategy_specs/spec_candidate_01_ipr_drift.md`](04_strategy_specs/spec_candidate_01_ipr_drift.md)
- [`04_strategy_specs/spec_candidate_02_aco_fixedfv.md`](04_strategy_specs/spec_candidate_02_aco_fixedfv.md)

## Next Priority Action

1. **Human:** Upload bot to platform, run simulator, share results.
2. **Agent:** Write run summary and identify issues.
