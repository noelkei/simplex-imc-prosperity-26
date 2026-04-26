# Phase 00 - Ingestion Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Created the curated Round 4 wiki file at
  [`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md)
  from the raw source at
  [`../../docs/prosperity_wiki_raw/15_round_4.md`](../../docs/prosperity_wiki_raw/15_round_4.md).
- Added the raw Round 4 source mirror at
  [`../../docs/prosperity_wiki_raw/15_round_4.md`](../../docs/prosperity_wiki_raw/15_round_4.md).
- Filled the phase 00 ingestion artifact with products, limits, manual/algorithmic split,
  Round Mechanics Delta, caveats, and downstream unknowns.
- Absorbed the uploaded Round 4 raw CSV files into ingestion state:
  `prices_round_4_day_{1,2,3}.csv` and `trades_round_4_day_{1,2,3}.csv`.
- Added a compact `round_3 -> round_4` compatibility framing into the ingestion artifact.
- Updated the Round 4 workspace README and control panel to reflect that
  ingestion has started and is ready for review.

## Current Findings

- Round 4 algorithmic products and limits match Round 3.
- The material round change is counterparty visibility through `Trade.buyer`
  and `Trade.seller`.
- Manual trading is separate and uses `AETHER_CRYSTAL` vanilla and exotic
  options.
- Raw price and trade files are now present for days `1-3`.
- The uploaded `trades_*` files already confirm named `Mark XX` counterparties
  in `buyer` and `seller`, so counterparty-aware EDA is now actionable.
- `round_4` is compatible with `round_3` at product/mechanics level, but the
  new counterparty field means carry-forward should be treated as
  `compatible, not auto-promoted`.

## Decisions Made

- Treat the user-provided Notion/wiki text as the accepted factual source for
  `docs/prosperity_wiki_raw/15_round_4.md`, then curate from that raw mirror
  into the operational wiki page.
- Keep phase 00 at `READY_FOR_REVIEW` rather than `COMPLETED` because review is
  still unassigned.
- Treat the uploaded raw CSVs as evidence inputs for EDA, not as official
  product facts.

## Open Questions / Blockers

- Manual contract-level details for the `AETHER_CRYSTAL` options are still
  missing from the accepted source set.
- Exact round deadline is still unknown.
- The first EDA question still needs to be selected and linked, but data
  availability is no longer the blocker.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`00_prior_round_intake.md`](00_prior_round_intake.md)
- [`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md)
- [`01_eda/README.md`](01_eda/README.md)

## Next Priority Action

Review phase 00 ingestion as the factual base, then consume the completed
Phase 01 EDA outputs before starting understanding.

## Deadline Risk

Medium until deadline is confirmed and the completed Phase 01 findings are reviewed.
