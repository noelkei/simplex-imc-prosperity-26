# Phase 00 - Ingestion Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Unassigned (human sign-off needed)

## Last Updated

2026-04-15

## What Has Been Done

- Read `docs/prosperity_wiki/rounds/round_1.md` and all shared wiki fact files (trader contract, datamodel, exchange mechanics, position limits).
- Filled in `00_ingestion.md` with: algorithmic products and limits, manual products and mechanics, round-specific facts, source caveats, and actionable unknowns table.
- Confirmed `rounds/round_1/data/raw/` is empty — only `.gitkeep` present.

## Current Findings

- Algorithmic products: `ASH_COATED_OSMIUM` (limit 80, volatile, "hidden pattern" hinted), `INTARIAN_PEPPER_ROOT` (limit 80, stable, analogous to Tutorial `EMERALDS`).
- Manual products: `DRYLAND_FLAX` (buyback 30/unit, no fee), `EMBER_MUSHROOM` (buyback 20/unit, fee 0.10/unit).
- Manual format: Exchange Auction — single limit order submitted last; clearing price maximizes volume, ties → higher price.
- No data artifacts exist yet. EDA is blocked.

## Decisions Made

- Ingestion sourced exclusively from `docs/prosperity_wiki/` — no facts inferred from bots, non-canonical, or Prosperity3 reference repo.
- Prosperity3 repo (TimoDiehm/imc-prosperity-3) reviewed for strategy patterns only; findings noted as non-authoritative heuristics for downstream strategy phase, not as official Prosperity 4 facts.

## Open Questions / Blockers

- **Critical blocker:** No raw data files in `rounds/round_1/data/raw/`. EDA cannot begin. Human must commit platform log/price files.
- Does `INTARIAN_PEPPER_ROOT` have a known or estimable fair value from the platform UI or starter data? Would allow provisional market-making spec without EDA.
- What is the round deadline? Needed to set workflow mode (standard vs. fast).
## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- - [`docs/prosperity_wiki/rounds/round_1.md`](../../../docs/prosperity_wiki/rounds/round_1.md)

## Next Priority Action

1. **Human:** Review `00_ingestion.md` and approve or correct it.
2. **Human:** Commit raw data to `rounds/round_1/data/raw/`.
3. **Agent:** Once data lands and ingestion is COMPLETED, start phase 01 EDA targeting: (a) fair value and spread stability of `INTARIAN_PEPPER_ROOT`; (b) pattern/periodicity/mean-reversion test for `ASH_COATED_OSMIUM`.

## Deadline Risk

Unknown — deadline not recorded in `_index.md`. If the round started today (2026-04-15) and lasts 72 hours, the window is tight. Fast mode should be considered if data is not available within a few hours.
