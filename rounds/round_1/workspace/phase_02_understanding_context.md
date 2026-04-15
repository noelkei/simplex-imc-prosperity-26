# Phase 02 - Understanding Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Unassigned (human sign-off needed before spec)

## Last Updated

2026-04-15

## What Has Been Done

- Synthesized ingestion facts + EDA evidence into `02_understanding.md`.
- Labeled all claims as fact / evidence / hypothesis.
- Built evidence synthesis table with strength and decision-impact ratings.
- Identified key assumptions and prioritized unknowns.
- Derived strategy implications for both algorithmic products and manual challenge.

## Current Findings

- IPR: predictable linear drift, FV = `day_start_price + t * 0.001`. Wiki's "quite steady" refers to the drift rate, not the price level.
- ACO: fixed FV = 10,000, slow AR(1) mean reversion. The "hidden pattern" is a knowable fair value.
- Manual: buyback floor strategy, human platform action.
- Both algorithmic products are market-makeable with evidence-backed fair value models.

## Decisions Made

- IPR requires a dynamic (drift-tracking) fair value — a static FV would be wrong immediately.
- ACO uses a static FV = 10,000 with position skew logic to manage slow reversion.
- Manual products treated as a separate human-decision track.

## Open Questions / Blockers

- None blocking strategy phase.
- Live round drift rate and FV need to be verified in first ~100 ticks.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02_understanding.md`](02_understanding.md)
- [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md)
- [`00_ingestion.md`](00_ingestion.md)

## Next Priority Action

1. **Human:** Review `02_understanding.md` and approve or correct.
2. **Agent:** Once approved, write strategy specs for `candidate_01_ipr_drift` and `candidate_02_aco_fixedfv`.

