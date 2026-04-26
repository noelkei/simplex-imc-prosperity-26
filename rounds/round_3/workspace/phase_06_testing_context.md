# Phase 06 - Testing And Performance Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-26

## What Has Been Done

- Parsed the 11 historical Round 3 platform JSON artifacts under `../performances/amin/historical/`.
- Created `06_testing/round_3_historical_performance_analysis.md`.
- Parsed the first corrected challenger trio: logger, centered base, and inventory variant.
- Created `06_testing/round_3_canonical_run_analysis.md`.
- Parsed the full 25-bot Wave 1 learner batch after the user uploaded all paired platform artifacts.
- Created `06_testing/round_3_full_performance_synthesis.md` plus CSV artifacts under `06_testing/artifacts/full_synthesis/`.
- Confirmed that the tested Wave 1 bots and their raw artifacts now live under `historical/`.
- Confirmed that the full 19-bot Wave 2 batch now also has paired artifacts and its bots have been archived from `canonical/` to `historical/`.
- Extended the full synthesis from `39` to `58` total runs so it now includes the entire Wave 2 batch.
- Added global `>5k` peak analysis, no-trade candidate extraction, and trade-markout diagnostics from `.log` plus `activitiesLog`.
- Fed that synthesis back into a new Wave 3 spec and a 24-bot implementation batch now waiting in `../bots/amin/canonical/`.
- Confirmed that the full 24-bot Wave 3 batch now also has paired artifacts and its bots have been archived from `canonical/` to `historical/`.
- Extended the synthesis from `58` to `82` total runs, adding Wave 3, `>10k` peak analysis, simple-exit counterfactuals, a Wave 3 decision board, and base-vs-overlay synergy checks.
- Fed that synthesis into a new Wave 4 finalist spec and a 12-bot active batch
  now waiting in `../bots/amin/canonical/`.
- Confirmed that the full 12-bot Wave 4 finalist batch now also has paired
  artifacts and its bots have been archived from `canonical/` to
  `historical/`.
- Extended the synthesis from `82` to `94` total runs, adding Wave 4,
  finalist-board classification, product-level `>10k` giveback decomposition,
  and a direct comparison between pure champion, champion+ITM, and tiny
  salvage overlays.
- Fed that synthesis into the concrete Wave 5 spec and a 12-bot active batch
  now waiting in `../bots/amin/canonical/`.

## Current Findings

- Across all `94` current JSON artifacts, the strongest clean live family is
  now the Wave 4 Kalman `delta-1 + ITM` finalist stack:
  - `W4-03 = +1606.305`
  - `W4-04 = +1604.305`
- The pure champion remained fully stable:
  - `W4-01 = W4-02 = W3-15 = +1527.305`
  so the delta-1 core is confirmed, but the main incremental edge now comes
  from the ITM overlay rather than from a new pure-base tweak.
- `VEV_5300` remains the only active strike with positive aggregate `10k`
  mean trade markout, but Wave 4 clarifies that this is no longer enough to
  justify normal finalist slots:
  - standalone `5300` finalists stayed negative or flat,
  - tiny `5300` overlays survived only as slightly subtractive add-ons to the
    strong base.
- `VEV_5000`, `VEV_5100`, and `VEV_5200` remain the dominant giveback drivers
  in the giant-peak runs; `5200` remains the strongest reject-by-default
  trading strike.
- Global `>10k` peak analysis still shows only `5` such runs in all of Round 3,
  all from the old legacy broad active-voucher world; no Wave 4 finalist got
  close to that scale.
- The simple-exit counterfactuals still show that the old `>10k` runs were not
  fake upside: a crude `2k` giveback stop would have salvaged roughly `+10k`
  to `+16k` in several cases, which means the next batch should target
  **retention-aware upside distillation**, not more broad exploration.
- The inverse closure run remains unresolved rather than positive:
  `W4-10` did not trade `VEV_5100`, so direct inverse trading is currently a
  lower-ROI slot than using toxic strikes as filters or vetoes.
- Wave 5 now attacks the remaining questions directly:
  - protect the live winner family with realistic timestamp-scale retention
    gates,
  - distill the old `>10k` ceiling through pruned `VEX`-anchored descendants,
  - and test toxic strikes mainly as signal inputs instead of normal legs.

## Decisions Made

- `activitiesLog` final per-product rows remain the best practical PnL proxy when JSON `profit` is unavailable.
- Timestamp-level `activitiesLog` paths are now the preferred source for intra-run quality analysis; `graphLog` should stay as a secondary audit path only.
- The Wave 1 batch should be treated as completed validation evidence, not as a pending run queue.
- The redesign/spec step for Wave 3 is now also complete and fully synthesized;
  the testing bottleneck is no longer interpretation of exploratory waves, but
  turning the now `94`-run evidence base into a final exploitation cut.
- Fast-unwind should no longer be treated as the default active-voucher rescue pattern.
- The next testing pass should explicitly separate:
  - clean finalist protection (`W4-03/W4-04/W4-01/W4-11` class),
  - `>10k` upside-distillation descendants,
  - and toxic-strike-as-signal variants.

## Open Questions / Blockers

- Need the Wave 5 live runs.
- Need the next run batch to decide whether any distilled upside branch can
  materially beat the clean `W4-03/W4-04` finalists without collapsing.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md)
- [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/artifacts/full_synthesis/full_run_metrics.csv`](06_testing/artifacts/full_synthesis/full_run_metrics.csv)
- [`06_testing/artifacts/full_synthesis/full_path_family_summary.csv`](06_testing/artifacts/full_synthesis/full_path_family_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv`](06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`06_testing/artifacts/full_synthesis/full_wave2_probe_summary.csv`](06_testing/artifacts/full_synthesis/full_wave2_probe_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_wave3_probe_summary.csv`](06_testing/artifacts/full_synthesis/full_wave3_probe_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv`](06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt5k_runs.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt5k_runs.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
- [`06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv`](06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv)
- [`06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
- [`06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- [`06_testing/artifacts/full_synthesis/full_wave3_decision_board.csv`](06_testing/artifacts/full_synthesis/full_wave3_decision_board.csv)
- [`06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv`](06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Run the Wave 5 batch on the platform, then compare:
- protected winner family,
- pure fallback,
- and distilled `>10k` descendants.

## Deadline Risk

Unknown.
