# Phase 00 - Ingestion Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Bruno
- Reviewer: Bruno (self-review)

## Last Updated

2026-04-18

## What Has Been Done

- Fetched Round 2 wiki content into `docs/prosperity_wiki_raw/13_round_2.md`.
- Confirmed algo product list: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, both with position limit 80 (unchanged from Round 1).
- Recorded Round 2 new mechanics: Market Access Fee (MAF) via `bid()` and Invest & Expand manual auction.
- Verified raw CSV artifacts in `rounds/round_2/data/raw/` for days -1, 0, 1 (prices + trades).
- Filled in `00_ingestion.md` with products, limits, unknowns, and caveats.

## Current Findings

- Same two algorithmic products as Round 1, same limits. Round 1 priors (IPR drift, ACO FV≈10000) are hypotheses to validate against Round 2 data, not facts to copy.
- MAF requires a `bid()` integer method on `Trader`. Top 50% strictly-above-median bids win 25% extra quotes at a one-time XIRECs cost.
- Manual auction (Invest & Expand) is disjoint from the algorithmic bot.

## Decisions Made

- Move straight to phase 01 EDA on Round 2 CSVs. Do not reuse Round 1 numerical findings as priors in the strategy until they are re-validated on Round 2 data.
- Defer MAF game-theory modeling to phase 03 strategy once we know Round 2 expected P&L.

## Open Questions / Blockers

- None blocking EDA start.
- Phase 03 must revisit MAF bid sizing once EDA/backtest give an expected Round 2 P&L.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- `docs/prosperity_wiki_raw/13_round_2.md`
- `rounds/round_2/data/raw/`

## Next Priority Action

Begin phase 01 EDA on Round 2 CSV data with Kalman filter calibration and HMM regime detection.

## Deadline Risk

Unknown round deadline; workflow stays in standard mode.
