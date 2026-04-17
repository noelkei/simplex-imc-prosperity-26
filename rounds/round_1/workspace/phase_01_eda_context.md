# Phase 01 EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned for 2026-04-17 advanced signal pass; previous EDA approved with caveats 2026-04-16
- Last updated: 2026-04-17

## What Has Been Done

- Original EDA remained available in `01_eda/eda_round_1.md`.
- Added strategy expansion script: `01_eda/strategy_expansion_analysis.py`.
- Added processed metrics: `../data/processed/strategy_expansion_metrics.json`.
- Added three expansion EDA handoffs:
  - `01_eda/eda_strategy_expansion_feature_lab.md`
  - `01_eda/eda_strategy_expansion_models.md`
  - `01_eda/eda_cross_product_relationships.md`
- Added targeted advanced signal research for the 2026-04-17 per-product top-3 and 3x3 strategy pass:
  - `01_eda/advanced_signal_research.py`
  - `01_eda/eda_advanced_signal_research.md`
  - `../data/processed/advanced_signal_research_metrics.json`

## Current Findings

- Raw residual and price-scaled log residual are effectively identical for both products; log does not justify a standalone strategy.
- Microstructure features are promising: sparse best-quote edge exists, and L1 imbalance correlates with next residual delta around 0.64.
- ACO Markov residual buckets show mean reversion in under/over states; deep states are too sparse to drive aggressive logic.
- Light linear models trained on days -2/-1 and validated on day 0 show R2 around 0.40-0.50, but may capture bid-ask bounce.
- Cross-product correlations and lead-lags are near zero; no directional cross-product strategy is supported.
- Advanced signal pass supports ACO residual/z-score reversion, residual+imbalance interactions, and book-state overlays as useful; it supports IPR carry as the primary IPR edge and treats IPR short-side logic as defensive/backup only.

## Decisions Made

- Use expansion EDA to support a five-bot experimental implementation batch.
- Reject log-transform-only strategy as redundant.
- Reject directional cross-product arbitrage for now.
- Treat model/microstructure signals as candidate evidence requiring backtest validation.
- Use advanced signal evidence to rank per-product A1-A3 and B1-B3 candidates in `03_strategy_research_per_product_3x3.md`.

## Open Questions / Blockers

- Human review of the 2026-04-17 advanced signal pass is pending.

## Linked Artifacts

- `01_eda/eda_round_1.md`
- `01_eda/eda_strategy_expansion_feature_lab.md`
- `01_eda/eda_strategy_expansion_models.md`
- `01_eda/eda_cross_product_relationships.md`
- `01_eda/eda_advanced_signal_research.md`
- `../data/processed/strategy_expansion_metrics.json`
- `../data/processed/advanced_signal_research_metrics.json`

## Next Priority Action

Review the advanced signal pass together with `03_strategy_research_per_product_3x3.md`, then write specs for the selected next pairings.

## Deadline Risk

Low. The new EDA is targeted and decision-oriented; it is ready for review rather than open-ended exploration.
