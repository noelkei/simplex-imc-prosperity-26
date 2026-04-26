# Phase 06 - Testing And Performance Context

## Status

READY_FOR_REVIEW

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
- Absorbed the `7` observed Wave 5 JSON artifacts that were still in `canonical/`, normalized the malformed `W5-09` filename, and extended the synthesis from `94` to `101` runs.
- Added Wave 5 closeout outputs plus new retrospective structural diagnostics:
  - Wave 5 summary and decision board
  - moneyness-role summary
  - cross-strike context around `5100/5200/5300`
  - portfolio-exposure summary
  - late-entry / post-peak churn summary
- Added the explicit closeout artifact:
  [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)

## Current Findings

- Across all `101` current JSON artifacts, the best clean full-stack family remains the Kalman `delta-1 + ITM` line:
  - `W5-01 = W4-03 = +1606.305`
  - `W4-04 = +1604.305`
- The pure fallback benchmark improved further:
  - `W5-04 = +1672.000`
  which strengthens `delta-1` as the cleanest standalone base/control branch.
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
- Partial Wave 5 evidence closes the remaining Round 3 testing loop:
  - winner protection mostly reconfirmed the existing winner axis,
  - fallback `delta-1` improved the clean base benchmark,
  - toxic-strike veto became informationally useful,
  - upside-distillation descendants stayed research-only.

## Decisions Made

- `activitiesLog` final per-product rows remain the best practical PnL proxy when JSON `profit` is unavailable.
- Timestamp-level `activitiesLog` paths are now the preferred source for intra-run quality analysis; `graphLog` should stay as a secondary audit path only.
- The Wave 1 batch should be treated as completed validation evidence, not as a pending run queue.
- The testing bottleneck is no longer live execution; the round is now closed as retrospective evidence.
- Fast-unwind should no longer be treated as the default active-voucher rescue pattern.
- Round 3 testing output should now be consumed in four buckets only:
  - validated findings,
  - carry-forward principles,
  - untested hypotheses,
  - anti-patterns.

## Open Questions / Blockers

- No Round 3 live-run blocker remains because no further Round 3 run queue remains.
- The only remaining judgment call is how strongly to carry these findings into `round_4` before fresh evidence re-validates them.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md)
- [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)
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
- [`06_testing/artifacts/full_synthesis/full_wave5_probe_summary.csv`](06_testing/artifacts/full_synthesis/full_wave5_probe_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_wave5_decision_board.csv`](06_testing/artifacts/full_synthesis/full_wave5_decision_board.csv)
- [`06_testing/artifacts/full_synthesis/full_moneyness_role_summary.csv`](06_testing/artifacts/full_synthesis/full_moneyness_role_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_cross_strike_context.csv`](06_testing/artifacts/full_synthesis/full_cross_strike_context.csv)
- [`06_testing/artifacts/full_synthesis/full_portfolio_exposure_summary.csv`](06_testing/artifacts/full_synthesis/full_portfolio_exposure_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_late_entry_summary.csv`](06_testing/artifacts/full_synthesis/full_late_entry_summary.csv)
- [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md)
- [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md)
- [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md)
- [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Use the closeout package as Round 4 input:
read the `101`-run synthesis, the closeout retrospective, and the updated
research memory before reopening testing assumptions in the next round.

## Deadline Risk

Unknown.
