# Phase 00 - Ingestion Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-24 15:22:41 CEST

## What Has Been Done

- Reviewed the Round 3 curated wiki page, raw pasted source, and shared API / trading-rule docs.
- Filled the ingestion artifact with products, limits, manual split, source caveats, mechanics delta, and actionable unknowns.
- Recorded raw data availability for six Round 3 CSV files without turning data observations into official facts.

## Current Findings

- Round 3 adds two delta-1 products plus ten strike-specific voucher symbols with a 300 limit each.
- The round page does not introduce a new round-specific `Trader` method; shared `Trader.run(state)` remains the active coding contract.
- Raw data is available for historical days 0, 1, and 2 for both price and trade files.

## Decisions Made

- Kept manual Bio-Pod mechanics separate from algorithmic implementation requirements.
- Treated the voucher-family naming ambiguity (`VELVETFRUIT_EXTRACT_VOUCHER` vs `VEV_*`) as a caveat and downstream implementation check, not as a resolved official fact.
- Set the downstream working assumption that bot symbol handling and EDA should use the concrete `VEV_*` symbols unless a later official simulator-facing source says otherwise.
- Marked Phase 00 `READY_FOR_REVIEW` rather than `COMPLETED` because review is still pending.

## Open Questions / Blockers

- No blocking ingestion issues remain.
- Open questions tracked in [`00_ingestion.md`](00_ingestion.md): voucher-family symbol mapping, manual second-bid fill rule, manual product symbol, and exact deadline timestamp.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`../../../docs/prosperity_wiki/rounds/round_3.md`](../../../docs/prosperity_wiki/rounds/round_3.md)
- [`../data/README.md`](../data/README.md)

## Next Priority Action

Review Phase 00 ingestion, then start Phase 01 EDA using the Round 3 raw CSVs to answer option-vs-underlying and schema questions.

## Deadline Risk

Exact round-end timestamp is still unknown; the official round page only states a 48-hour duration.
