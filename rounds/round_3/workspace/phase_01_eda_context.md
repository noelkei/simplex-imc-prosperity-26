# Phase 01 - EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-24 15:44:50 CEST

## What Has Been Done

- Ran a reproducible Round 3 EDA over all six raw CSVs using `analyze_round_3_eda.py`.
- Generated processed tables for data quality, trade alignment, option surface checks, cross-product metrics, feature redundancy, and explanatory models.
- Wrote the canonical EDA handoff in `01_eda/eda_option_surface_and_microstructure.md`.

## Current Findings

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` look like separate delta-1 branches; their same-time return correlation is effectively zero.
- The voucher surface is almost perfectly monotone and convex across strike, with strong same-time linkage to `VELVETFRUIT_EXTRACT` in the `VEV_5000` to `VEV_5200` region.
- `VEV_6000` and `VEV_6500` behave like constant floor instruments in sample data and should be excluded from the first implementation wave.

## Decisions Made

- Promoted option-aware features such as moneyness, intrinsic/extrinsic decomposition, extrinsic deviation, and order-book imbalance into the next phase.
- Rejected delayed underlying-follow as a primary option alpha because lagged correlations collapse after lag 0.
- Marked Phase 01 `READY_FOR_REVIEW` rather than `COMPLETED` because review is still pending.

## Open Questions / Blockers

- No blocking EDA issues remain.
- Open questions for Understanding / Strategy: TTE `6d -> 5d` extrapolation, sparse trade tape in `VEV_4500` / `VEV_5000` / `VEV_5100`, and whether the deep OTM floor persists in final-day data.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md)
- [`01_eda/analyze_round_3_eda.py`](01_eda/analyze_round_3_eda.py)
- [`../data/processed/`](../data/processed/)

## Next Priority Action

Review Phase 01 EDA, then start Phase 02 Understanding using the promoted signals, exclusions, and negative evidence from `eda_option_surface_and_microstructure.md`.

## Deadline Risk

Exact round-end timestamp is still unknown, and final Round 3 trading happens at TTE `5d` while the sample data only covers TTE `8d`, `7d`, and `6d`.
