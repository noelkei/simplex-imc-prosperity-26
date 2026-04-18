# Phase 01 - EDA Context

## Status

NOT_STARTED

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-18

## What Has Been Done

- Raw Round 2 CSV paths are now recorded in `../data/README.md` and phase 00 ingestion.
- Added `01_eda/round_2_decision_tools.py` for manual allocation and Market Access Fee scenario tables.
- No EDA analysis has been run yet.

## Current Findings

- Data is present for days `-1`, `0`, and `1`, with price and trade files for `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Round 2 has two decision tracks beyond the trading algorithm: Market Access Fee bid and manual Research/Scale/Speed allocation.

## Decisions Made

- None yet.

## Open Questions / Blockers

- Phase 00 ingestion is ready for review but not approved yet.
- EDA question not selected.
- No Round 2 platform logs have been recorded yet.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py)
- [`../data/README.md`](../data/README.md)

## Next Priority Action

After ingestion review, choose one targeted EDA question. Recommended first pass: compare Round 2 sample behavior against Round 1 champion assumptions and generate manual/MAF scenario tables.

## Deadline Risk

Unknown; use fast mode if less than 24 hours remain.
