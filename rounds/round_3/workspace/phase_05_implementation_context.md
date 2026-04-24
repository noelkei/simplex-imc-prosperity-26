# Phase 05 - Implementation Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-24

## What Has Been Done

- Implemented Bot A: `candidate_c06_composite_base.py` (C01+C02+C03).
- Implemented Bot B: `candidate_c06_composite_inv.py` (C01+C02+C04 with inventory skew + imbalance confirmation).
- Both bots parse successfully and follow the Trader contract.
- Both placed under `rounds/round_3/bots/amin/canonical/`.

## Current Findings

- Bot A (base): simpler, entry threshold 3.0, light inventory skew 1.0, no imbalance filter on vouchers.
- Bot B (inventory variant): stronger inventory skew 3.0, imbalance confirmation filter, wider entry threshold 4.0 (TTE-cautious), family-level exposure nudge.

## Decisions Made

- Created two distinct bots for parallel testing per user request.
- Both use Bachelier fair-value backbone with hand-coded norm_cdf.
- Both trade HYDROGEL_PACK, VELVETFRUIT_EXTRACT, and VEV_5000-5300.
- VEV_4000/4500/5400/5500/6000/6500 excluded from wave 1.

## Open Questions / Blockers

- Need platform validation runs to compare the two bots.
- sigma_abs parameter may need calibration after first runs.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md)
- [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md)
- [`../bots/amin/canonical/candidate_c06_composite_base.py`](../bots/amin/canonical/candidate_c06_composite_base.py)
- [`../bots/amin/canonical/candidate_c06_composite_inv.py`](../bots/amin/canonical/candidate_c06_composite_inv.py)

## Next Priority Action

Run both bots on the platform, collect performance data, compare PnL, position utilization, and fill quality.

Implement the smallest reviewed candidate that can be validated quickly.

## Deadline Risk

Unknown.
