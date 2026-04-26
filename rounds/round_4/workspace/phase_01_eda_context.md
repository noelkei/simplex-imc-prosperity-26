# Phase 01 - EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Phase 00 now confirms raw Round 4 price and trade CSVs for days `1-3`.
- The round has been framed as `compatible` with `round_3`, with one material
  delta: visible counterparties in `Trade.buyer` and `Trade.seller`.
- The first EDA pass has been narrowed to counterparty-aware market structure
  and revalidation of Round 3 carry-forward assumptions.
- Implemented the reusable analysis script
  [`01_eda/analyze_round_4_eda.py`](01_eda/analyze_round_4_eda.py).
- Generated processed evidence tables under `../../data/processed/`.
- Generated Phase 01 plots and manifests under `01_eda/artifacts/`.
- Wrote the canonical EDA and the three supporting annexes.

## Current Findings

- `prices_*` files cover all 12 algorithmic products for days `1-3`.
- `trades_*` files expose named `Mark XX` counterparties and already show
  concentrated participant activity.
- EDA should begin from the raw trade data, not from strategy speculation.
- Counterparty specialization is real and stable enough to promote as
  contextual state, but not as standalone alpha.
- `VEX` remains the strongest same-time anchor for the voucher family and
  delayed-follow stays weak.
- The voucher family is linked structurally but execution-fragmented by strike,
  especially from `5200` upward.

## Decisions Made

- Use `round_3` as a compatible carry-forward source, but revalidate its
  lessons against counterparty-aware data before promoting any strategy
  conclusion.
- Start with a targeted EDA question on whether specific counterparties show
  stable product, side, or timing behavior that changes the Round 3 framing.
- Build Phase 01 as `algorithmic-first`.
- Use one canonical EDA plus annexes rather than many peer artifacts.
- Treat `round_4` as raw-data EDA only for now; no Round 4 retrospective
  run-informed addendum is needed yet.

## Open Questions / Blockers

- Exact deadline remains unknown.
- Manual contract-level raw data is still missing.
- Phase 01 review is still pending.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`00_prior_round_intake.md`](00_prior_round_intake.md)
- [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
- [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
- [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
- [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- [`01_eda/analyze_round_4_eda.py`](01_eda/analyze_round_4_eda.py)
- [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
- [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)

## Next Priority Action

Review Phase 01, then use the canonical EDA and annexes to write
`02_understanding.md` with explicit separation between supported
carry-forward principles, contextual counterparty findings, and still-untested
Round 4 hypotheses.

## Deadline Risk

Medium until deadline is confirmed and Phase 01 review is complete.
