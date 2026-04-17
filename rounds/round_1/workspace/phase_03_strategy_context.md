# Phase 03 Strategy Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: user approved with caveats for 2026-04-17 per-product top-3/3x3 direction by requesting the three high-ROI variants for platform testing
- Last updated: 2026-04-17

## What Has Been Done

- Reopened Phase 03 after the user requested conceptually orthogonal strategy exploration.
- Updated `03_strategy_candidates.md` with per-product strategy banks and a five-bot experiment matrix.
- Added 8 strategy families across FV baseline, directional carry, microstructure, Markov, light linear scoring, defensive overlay, and cross-product checks.
- User approved implementing five different bots for performance testing.
- Reopened Phase 03 after platform JSON/log analysis showed `candidate_10_carry_tight_mm` as the >10k baseline and ACO as the main improvement surface.
- Added `03_strategy_next_wave_branches.md` with 10 next-wave families and 3 branches each, including Kalman, HMM, edge-quality, inventory lifecycle, offline policy table, one-sided-book, and adaptive-controller approaches.
- User selected all 10 next-wave families for implementation.
- Added `03_strategy_research_per_product_3x3.md`, a per-product top-3 strategy research pass with a 3x3 ACO/IPR combination matrix and explicit short-side analysis.
- User narrowed implementation to exactly three high-ROI variants: A1+B1 size/skew refinement, A2+B1 conservative regime gate, and A3+B1 one-sided exit overlay.

## Current Findings

- Product strategies should run concurrently in one bot, but current EDA does not support directional cross-product trading.
- The five-bot matrix covers baseline FV, aggressive carry, microstructure scalping, ACO Markov, and adaptive hybrid approaches.
- Cross-product arbitrage is rejected/deferred because current correlations are near zero.
- Latest platform/log evidence says IPR +80 should be treated as the base layer for the next wave.
- ACO strategy quality, inventory lifecycle, and hidden-regime filtering are the highest-upside unexplored spaces.
- Pure microstructure is not a standalone candidate anymore; it should be used only as an execution overlay.
- The 2026-04-17 research pass ranks A1+B1 as the best/safest control, A2+B1 as the highest-upside next pair, and A3+B1 as the best viable short-side/execution pair.
- IPR short-side strategies are not supported as primary by current platform artifacts; ACO short-side execution remains central.

## Decisions Made

- Implementation batch:
  1. `candidate_09_baseline_fv_combo`
  2. `candidate_10_carry_tight_mm`
  3. `candidate_11_microstructure_scalper`
  4. `candidate_12_aco_markov_overlay`
  5. `candidate_13_hybrid_adaptive_model`
- Promote only best 1-2 bots after comparable validation.
- For the next wave, keep `candidate_10` as the baseline and explore ACO modules around it rather than replacing the whole bot.
- User selected all 10 families for implementation; no strategy-selection blocker remains.
- Recommended next strategy specs are A2+B1 and A3+B1, with A1+B1 as the control and minimum bar.
- The chosen implementation batch is `candidate_24`, `candidate_25`, and `candidate_26`.

## Open Questions / Blockers

- Platform JSON/log evidence is still needed before promoting any implemented next-wave bot.

## Linked Artifacts

- `03_strategy_candidates.md`
- `03_strategy_next_wave_branches.md`
- `03_strategy_research_per_product_3x3.md`
- `01_eda/eda_strategy_expansion_feature_lab.md`
- `01_eda/eda_strategy_expansion_models.md`
- `01_eda/eda_cross_product_relationships.md`
- `01_eda/eda_advanced_signal_research.md`
- `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- `04_strategy_specs/spec_experimental_5_bot_matrix.md`

## Next Priority Action

Run `candidate_26`, `candidate_25`, and `candidate_24` on Prosperity and compare against the `10007.0` platform bar.

## Deadline Risk

Medium-low. Strategy direction is narrowed; promotion now depends on platform JSON/log validation.
