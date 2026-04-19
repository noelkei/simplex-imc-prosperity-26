# Phase 01 - EDA Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-19

## What Has Been Done

- Raw Round 2 CSV paths are now recorded in `../data/README.md` and phase 00 ingestion.
- Added `01_eda/round_2_decision_tools.py` for manual allocation and Market Access Fee scenario tables.
- Pre-kickoff EDA outputs were found in the active EDA folder and moved to
  `01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/`.
- No reviewed active EDA analysis existed before this fresh run.
- Added a no-trade diagnostic state logger for optional platform log collection
  before fresh EDA.
- Saved no-trade platform artifact at
  `../performances/noel/historical/baseline_state_logger.json`.
- Implemented and ran fresh EDA script `01_eda/eda_round2_fresh.py`.
- Generated fresh EDA report `01_eda/eda_round2_fresh.md` and supporting
  artifacts under `01_eda/artifacts/`.
- Implemented and ran consolidated multivariate/process EDA script
  `01_eda/eda_round2_consolidated.py`.
- Rewrote `01_eda/eda_round2_fresh.md` as the single canonical EDA handoff for
  Understanding, preserving first-pass findings and adding multivariate,
  redundancy, cross-product, process/distribution, PCA, MI, clustering, and
  controlled-regression evidence.

## Current Findings

- Data is present for days `-1`, `0`, and `1`, with price and trade files for `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Round 2 has two decision tracks beyond the trading algorithm: Market Access Fee bid and manual Research/Scale/Speed allocation.
- Round 1 and Round 2 use the same algorithmic products and limits, but Round 2
  adds `Trader.bid()`, extra market-access economics, randomized testing quote
  subsets, and a different manual challenge.
- Platform logs from the diagnostic state logger are EDA evidence, not
  official rules.
- Platform JSON contains `activitiesLog`, `graphLog`, positions, status, and
  profit, but no `ROUND2_STATE_PROBE` printed-state lines.
- Consolidated EDA promotes IPR drift plus residual, ACO short-horizon mean
  reversion, and top imbalance for understanding/strategy consideration.
- Spread regime is promoted as an execution/risk filter candidate, not a
  standalone alpha signal.
- Microprice deviation is a new exploratory challenger to top imbalance.
- Full-book imbalance is useful but reclassified as backup/context unless
  validation beats top imbalance under relevant regimes.
- Liquidity/depth regimes remain exploratory; trade pressure proxy still needs
  better platform `market_trades` logs.
- Cross-product lead-lag is negative evidence for first-pass strategy.
- PCA/clustering/latent-style outputs are EDA-only calibration and must not
  enter bot logic without a reviewed online proxy.

## Decisions Made

- Treat archived pre-kickoff EDA outputs as historical/unreviewed context, not
  active evidence.
- Start Round 2 EDA fresh from official wiki facts and raw CSV data.
- Human review accepted consolidated EDA for synthesis with caveats.
- Mark EDA `COMPLETED` with review outcome `approved with caveats`.
- Do not generate strategy candidates or implement bot logic from EDA before the
  understanding/spec gates.

## Open Questions / Blockers

- Exact Round 2 deadline is still unknown.
- Market Access Fee bid remains a strategy/human risk decision; EDA only gives
  proxy scenarios.
- Manual Speed rank outcome remains unknown.
- Printed `TradingState` probe lines were not present in the saved platform
  JSON, so market-trade online diagnostics remain incomplete.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md)
- [`01_eda/eda_round2_fresh.py`](01_eda/eda_round2_fresh.py)
- [`01_eda/eda_round2_consolidated.py`](01_eda/eda_round2_consolidated.py)
- [`01_eda/artifacts/`](01_eda/artifacts/)
- [`01_eda/artifacts/expanded_feature_promotion_decisions.csv`](01_eda/artifacts/expanded_feature_promotion_decisions.csv)
- [`01_eda/artifacts/artifact_manifest_consolidated.csv`](01_eda/artifacts/artifact_manifest_consolidated.csv)
- [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py)
- [`01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/`](01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/)
- [`round_1_to_round_2_pre_eda_note.md`](round_1_to_round_2_pre_eda_note.md)
- [`../bots/noel/historical/baseline_state_logger.py`](../bots/noel/historical/baseline_state_logger.py)
- [`../performances/noel/historical/baseline_state_logger.json`](../performances/noel/historical/baseline_state_logger.json)
- [`../data/README.md`](../data/README.md)

## Next Priority Action

Review Phase 02 Understanding. If approved, generate strategy candidates from the understanding summary and consolidated EDA evidence.

## Review

- Reviewer: Human
- Review outcome: approved with caveats
- Status: COMPLETED

Caveats:

- Sample-data evidence is not an official rule.
- Final platform distribution and randomized quote subset may differ.
- MAF bid and manual RSS allocation remain separate downstream decisions.
- Trade pressure still needs better platform `market_trades` logs.

## Deadline Risk

Unknown; use fast mode if less than 24 hours remain.
