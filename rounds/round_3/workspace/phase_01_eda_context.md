# Phase 01 - EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Ran a reproducible Round 3 EDA over all six raw CSVs using `analyze_round_3_eda.py`.
- Generated processed tables for data quality, trade alignment, option surface checks, cross-product metrics, feature redundancy, and explanatory models.
- Wrote the canonical EDA handoff in `01_eda/eda_option_surface_and_microstructure.md`.
- Added a retrospective EDA addendum using the `101`-run closeout artifacts so the run-derived structural findings also live in Phase 01 instead of only inside testing:
  [`01_eda/eda_round_3_retrospective_carry_forward.md`](01_eda/eda_round_3_retrospective_carry_forward.md)

## Current Findings

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` look like separate delta-1 branches; their same-time return correlation is effectively zero.
- The voucher surface is almost perfectly monotone and convex across strike, with strong same-time linkage to `VELVETFRUIT_EXTRACT` in the `VEV_5000` to `VEV_5200` region.
- `VEV_6000` and `VEV_6500` behave like constant floor instruments in sample data and should be excluded from the first implementation wave.
- The retrospective addendum strengthens the original EDA in five important ways:
  - product `role` is now an EDA-level feature, not just a strategy framing choice,
  - cross-strike context around `5300` matters materially,
  - family-level exposure is decision-relevant,
  - late-entry / post-peak churn is a real EDA axis,
  - and hold horizon is part of signal definition for active vouchers.

## Decisions Made

- Promoted option-aware features such as moneyness, intrinsic/extrinsic decomposition, extrinsic deviation, and order-book imbalance into the next phase.
- Rejected delayed underlying-follow as a primary option alpha because lagged correlations collapse after lag 0.
- Promoted retrospective run-informed EDA outputs into carry-forward framing:
  role-based grouping, cross-strike context, family exposure, late-entry timing, and horizon-aware active-voucher analysis.
- Marked Phase 01 `READY_FOR_REVIEW` rather than `COMPLETED` because review is still pending.

## Open Questions / Blockers

- No blocking EDA issues remain.
- Open questions for future-round EDA: how much of the Round 3 retrospective EDA transfers cleanly once `round_4` counterparties and new live structure enter the picture.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md)
- [`01_eda/eda_round_3_retrospective_carry_forward.md`](01_eda/eda_round_3_retrospective_carry_forward.md)
- [`01_eda/analyze_round_3_eda.py`](01_eda/analyze_round_3_eda.py)
- [`../data/processed/`](../data/processed/)
- [`../06_testing/artifacts/full_synthesis/`](../06_testing/artifacts/full_synthesis/)

## Next Priority Action

Review Phase 01 EDA, then carry both the raw-data EDA and the retrospective
EDA addendum into the first Understanding / EDA pass of `round_4`.

## Deadline Risk

Exact round-end timestamp is still unknown, and final Round 3 trading happens at TTE `5d` while the sample data only covers TTE `8d`, `7d`, and `6d`.
