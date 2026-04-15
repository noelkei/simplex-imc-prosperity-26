# Phase 00 - Ingestion Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Unassigned
- Review outcome: not reviewed

## Last Updated

2026-04-16

## What Has Been Done

- Read `docs/prosperity_wiki/rounds/round_1.md` and all shared wiki fact files (trader contract, datamodel, exchange mechanics, position limits).
- Filled in `00_ingestion.md` with: algorithmic products and limits, manual products and mechanics, round-specific facts, source caveats, and actionable unknowns table.
- Initial ingestion found no raw data.
- Later data arrival recorded: 6 CSV files now exist in `rounds/round_1/data/raw/`, and EDA consumed them in `01_eda/eda_round_1.md`.

## Current Findings

- Algorithmic products: `ASH_COATED_OSMIUM` (limit 80, volatile, "hidden pattern" hinted), `INTARIAN_PEPPER_ROOT` (limit 80, stable, analogous to Tutorial `EMERALDS`).
- Manual products: `DRYLAND_FLAX` (buyback 30/unit, no fee), `EMBER_MUSHROOM` (buyback 20/unit, fee 0.10/unit).
- Manual format: Exchange Auction — single limit order submitted last; clearing price maximizes volume, ties → higher price.
- Raw price/trade data is available for days -2, -1, and 0. Data-derived claims remain EDA evidence, not official wiki facts.

## Decisions Made

- Ingestion sourced exclusively from `docs/prosperity_wiki/` — no facts inferred from bots, non-canonical, or Prosperity3 reference repo.
- Prosperity3 repo (TimoDiehm/imc-prosperity-3) reviewed for strategy patterns only; findings noted as non-authoritative heuristics for downstream strategy phase, not as official Prosperity 4 facts.

## Open Questions / Blockers

- Human review pending: approve ingestion, approve with caveats, or request corrections before marking `COMPLETED`.
- EDA-derived fair value models need human review in `01_eda/eda_round_1.md`.
- What is the round deadline? Needed to set workflow mode (standard vs. fast).

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`docs/prosperity_wiki/rounds/round_1.md`](../../../docs/prosperity_wiki/rounds/round_1.md)
- [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md)

## Next Priority Action

1. **Human:** Review `00_ingestion.md` and approve, approve with caveats, or request corrections.
2. **Agent/Human:** Keep ingestion marked `READY_FOR_REVIEW` until review outcome is recorded.

## Deadline Risk

Unknown — deadline not recorded in `_index.md`. If deadline pressure requires proceeding before review, record `deferred under deadline` explicitly.
