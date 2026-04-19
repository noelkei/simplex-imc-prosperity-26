# Phase 00 - Ingestion Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-19

## What Has Been Done

- Captured the pasted Round 2 Notion content as `docs/prosperity_wiki_raw/13_round_2.md`.
- Created curated Round 2 wiki facts at `docs/prosperity_wiki/rounds/round_2.md`.
- Updated this ingestion artifact with products, limits, Market Access Fee mechanics, manual challenge mechanics, data availability, caveats, and downstream unknowns.
- Updated Round 2 control and data notes so downstream work no longer inherits stale "official facts missing" blockers.
- Human direction accepted the ingestion setup and requested a clean pre-EDA
  reset before starting Round 2 work.
- Archived pre-kickoff EDA outputs as historical/unreviewed artifacts so active
  EDA can start fresh.

## Current Findings

- Algorithmic scope: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, each with position limit 80.
- Round-specific API addition: `Trader.bid()` is relevant only for Round 2 Market Access Fee bidding; testing ignores it.
- Extra market access gives 25% more order-book quotes if the bid is in the top 50%; accepted bid is subtracted from Round 2 profit.
- Manual scope: allocate `50 000` XIRECs across Research, Scale, and Speed; Speed is rank-based across players.
- Raw Round 2 CSV files are present for days `-1`, `0`, and `1`.
- `post_run_research_memory.md` is absent, which is expected before any Round 2
  bot/run cycle.

## Decisions Made

- Manual Research/Scale/Speed mechanics are documented as manual-only and separate from bot implementation.
- MAF bid selection is left as a strategy decision, not a fact.
- Ingestion is `COMPLETED` with review outcome `approved with caveats`.
- Pre-kickoff EDA outputs are treated as historical/unreviewed, not active evidence.

## Open Questions / Blockers

- Round 2 deadline is not present in the pasted source.
- MAF bid value requires scenario analysis and a human strategy decision.
- Manual Speed allocation depends on unknown competitor allocations.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`../../../docs/prosperity_wiki/rounds/round_2.md`](../../../docs/prosperity_wiki/rounds/round_2.md)
- [`../../../docs/prosperity_wiki_raw/13_round_2.md`](../../../docs/prosperity_wiki_raw/13_round_2.md)
- [`round_1_to_round_2_pre_eda_note.md`](round_1_to_round_2_pre_eda_note.md)

## Next Priority Action

Review fresh EDA and then synthesize Round 2 understanding if approved.

## Deadline Risk

Unknown deadline; if less than 24 hours remain, switch to fast mode after ingestion review.
