# Phase 06 Testing Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned
- Last updated: 2026-04-17

## What Has Been Done

- Added local replay script: `rounds/round_1/performances/noel/canonical/replay_five_bot_batch.py`.
- Ran all five Noel canonical bots on days -2, -1, and 0 with immediate fills against visible order books.
- Saved raw metrics: `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`.
- Saved summary: `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_summary.md`.
- Added cross-bot log/replay insight summary: `rounds/round_1/performances/noel/canonical/run_20260416_cross_bot_log_insights.md`.
- Compared Amin historical platform-style JSON/log artifacts, the misfiled Amin canonical `26-candidate_03_combined.json`, Bruno canonical code, and Noel five-bot replay evidence.
- Patched `rounds/round_1/bots/noel/historical/candidate_10_bot02_carry_tight_mm.py` so ACO passive quotes use remaining capacity instead of a fixed 24-unit size before it became the historical fallback.
- Added platform artifact analyzer: `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py`.
- Analyzed 10 platform-style JSON artifacts plus matching logs where available.
- Saved raw normalized output: `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.json`.
- Saved readable PnL/insight report: `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.md`.
- Added next-wave replay script: `rounds/round_1/performances/noel/canonical/replay_next_wave_batch.py`.
- Ran baseline `candidate_10` plus next-wave `candidate_14` through `candidate_23` through local immediate-fill replay.
- Saved next-wave raw replay metrics: `rounds/round_1/performances/noel/canonical/run_20260417_next_wave_replay_metrics.json`.
- Saved next-wave replay summary: `rounds/round_1/performances/noel/canonical/run_20260417_next_wave_replay_summary.md`.
- Added high-ROI replay script: `rounds/round_1/performances/noel/canonical/replay_high_roi_variant_batch.py`.
- Ran control `candidate_10` plus high-ROI `candidate_24`, `candidate_25`, and `candidate_26` through local immediate-fill replay.
- Saved high-ROI raw replay metrics: `rounds/round_1/performances/noel/canonical/run_20260417_high_roi_variant_replay_metrics.json`.
- Saved high-ROI replay summary: `rounds/round_1/performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`.
- Updated high-ROI replay script to include threshold refinements `candidate_27` and `candidate_28`, with archived controls loaded from `noel/historical`.
- Reran the high-ROI replay for `candidate_10`, `candidate_24`, `candidate_25`, `candidate_26`, `candidate_27`, and `candidate_28`.
- Added platform JSON/log artifacts for `candidate_27` and `candidate_28` under `rounds/round_1/performances/noel/historical/`.
- Reran `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py` after the new uploads.
- Added `rounds/round_1/workspace/06_testing/candidate_26_overfit_audit.md` to check for sample-ending, log-dependent, or platform-artifact-dependent behavior in the recommended candidate.

## Current Findings

Platform artifact findings:

- Correct PnL ranking method: use platform-style JSON `profit`; use final per-product `activitiesLog` `profit_and_loss` rows for IPR/ACO split.
- The final `activitiesLog` product PnL sum equals JSON `profit` with `0.0` delta in all analyzed artifacts.
- `graphLog` and tradeHistory reconstruction are close but not exact; max absolute deltas are `8.0` and `32.0`, so they are audit signals, not score sources.
- Best platform-style artifact found: `rounds/round_1/performances/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.json` with total PnL `10090.46875`, IPR PnL `7286.0`, ACO PnL `2804.46875`, final positions IPR `80` and ACO `9`.
- Closest challenger after threshold optimization: `rounds/round_1/performances/noel/historical/candidate_28_v1_c26_strict_one_sided.json` with total PnL `10076.3125`, IPR PnL `7286.0`, ACO PnL `2790.3125`, final positions IPR `80` and ACO `6`.
- `candidate_27_v1_c26_soft_flatten` underperformed with total PnL `9920.1875`, IPR PnL `7286.0`, and ACO PnL `2634.1875`; the soft-flatten threshold reduced ACO capture too much.
- Robust fallback artifact: `rounds/round_1/performances/noel/historical/candidate_10_bot02_carry_tight_mm.json` with total PnL `10007.0`, IPR PnL `7286.0`, ACO PnL `2721.0`, final positions IPR `80` and ACO `0`.
- Best non-Noel comparison: `rounds/round_1/bots/amin/canonical/26-candidate_03_combined.json` with total PnL `9432.0625`, IPR PnL `7286.0`, ACO PnL `2146.0625`, final positions IPR `80` and ACO `46`; the artifact is useful but misfiled and lacks a matching log here.
- IPR max-long is strongly supported: platform-style logs with final IPR `80` earn `7286.0` IPR PnL over the 1000-tick window, versus `6836.5` for the `75` cap.
- ACO is the main improvement surface after IPR: current best is ACO `2804.46875` from `candidate_26`; bot 04/05 ACO filters remain useful only if the +80 IPR layer remains intact.
- The stricter one-sided variant `candidate_28` validates the `candidate_26` strategy family as repeatable, but does not justify replacing the higher-PnL incumbent.
- Candidate 26 overfit/cheat audit found no use of timestamp, day, iteration count, logs, files, own trades, market trades, observations, randomization, or final-sample liquidation behavior. Remaining risk is ordinary parameter overfit, not an explicit exploit.

Noel local replay findings remain useful for sanity, not exact PnL:

| Rank | Bot | Total PnL | IPR PnL | ACO PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_10_bot02_carry_tight_mm.py` | 247628.0 | 238054.0 | 9574.0 | 0 | 0 |
| 2 | `candidate_13_bot05_hybrid_adaptive.py` | 157468.0 | 152629.0 | 4839.0 | 0 | 0 |
| 3 | `candidate_12_bot04_aco_markov.py` | 154812.0 | 146232.0 | 8580.0 | 0 | 0 |
| 4 | `candidate_09_bot01_baseline_fv_combo.py` | 152123.0 | 146232.0 | 5891.0 | 0 | 0 |
| 5 | `candidate_11_bot03_micro_scalper.py` | 41236.5 | 35757.5 | 5479.0 | 0 | 0 |

Next-wave local replay findings, also sanity only:

| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_10_bot02_carry_tight_mm.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |
| 2 | `candidate_19_ipr_execution_upgrade.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |
| 3 | `candidate_14_aco_kalman_latent_fv.py` | 247203.00 | 238054.00 | 9149.00 | 0 | 0 |
| 4 | `candidate_23_adaptive_aco_controller.py` | 246435.00 | 238054.00 | 8381.00 | 0 | 0 |
| 5 | `candidate_18_aco_offline_policy_table.py` | 246090.00 | 238054.00 | 8036.00 | 0 | 0 |
| 6 | `candidate_21_one_sided_book_specialist.py` | 245936.00 | 238054.00 | 7882.00 | 0 | 0 |
| 7 | `candidate_22_micro_alpha_rescue.py` | 244976.00 | 238054.00 | 6922.00 | 0 | 0 |
| 8 | `candidate_15_aco_hmm_regime_mm.py` | 244829.00 | 238054.00 | 6775.00 | 0 | 0 |
| 9 | `candidate_20_dual_product_risk_scheduler.py` | 243230.00 | 238054.00 | 5176.00 | 0 | 0 |
| 10 | `candidate_16_aco_edge_quality_gate.py` | 241372.00 | 238054.00 | 3318.00 | 0 | 0 |
| 11 | `candidate_17_aco_inventory_lifecycle.py` | 240317.50 | 238054.00 | 2263.50 | 0 | 0 |

Updated high-ROI local replay findings, also sanity only:

| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_27_v1_c26_soft_flatten.py` | 249079.00 | 238054.00 | 11025.00 | 0 | 0 |
| 2 | `candidate_26_v3_a3b1_one_sided_exit_overlay.py` | 248251.00 | 238054.00 | 10197.00 | 0 | 0 |
| 3 | `candidate_28_v1_c26_strict_one_sided.py` | 248105.00 | 238054.00 | 10051.00 | 0 | 0 |
| 4 | `candidate_25_v2_a2b1_conservative_regime_gate.py` | 247946.00 | 238054.00 | 9892.00 | 0 | 0 |
| 5 | `candidate_24_v1_a1b1_size_skew_refine.py` | 247631.00 | 238054.00 | 9577.00 | 0 | 0 |
| 6 | `candidate_10_bot02_carry_tight_mm.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |

## Decisions Made

- Treat platform-style JSON `profit` as the primary score for ranking and promotion.
- Treat final `activitiesLog` product PnL as the authoritative product attribution for each artifact.
- Demote local replay PnL magnitude to sanity/ranking heuristic only; it is not an official PnL estimator.
- Use `candidate_10_bot02_carry_tight_mm.py` as the current >10k baseline.
- Keep `candidate_12_bot04_aco_markov.py` and `candidate_13_bot05_hybrid_adaptive.py` as sources of ACO overlay ideas, not standalone primary candidates unless they preserve +80 IPR.
- Treat next-wave replay as a deployability/sanity ranking, not the official PnL ranking.
- If platform-run budget is limited, run `candidate_19`, `candidate_14`, `candidate_23`, `candidate_18`, and `candidate_21` first.
- For the current high-ROI batch, upload `candidate_26` first, then `candidate_25`, then `candidate_24`; compare all against the `candidate_10` platform bar.
- Current recommendation after platform results: promote `candidate_26` as canonical upload candidate, with `candidate_10` as lower-risk fallback.
- For the threshold refinement pass, platform-test `candidate_27` first and `candidate_28` second; do not promote them over `candidate_26` until platform JSON/log validates the replay signal.
- After threshold platform results, promote `candidate_26`; keep `candidate_28` as the closest backup and reject `candidate_27` for final upload.

## Open Questions / Blockers

- Platform JSON/log exists for `candidate_24`, `candidate_25`, `candidate_26`, `candidate_27`, and `candidate_28`.
- Exact code-version provenance remains a caveat for artifacts that do not embed bot hashes; save `.py`, `.json`, and `.log` together after each run.
- Need final submission decision and active-file verification.
- Immediate-fill replay does not model passive future fills, so it should not be used as the PnL scale.

## Linked Artifacts

- `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py`
- `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.json`
- `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- `rounds/round_1/performances/noel/canonical/replay_next_wave_batch.py`
- `rounds/round_1/performances/noel/canonical/run_20260417_next_wave_replay_metrics.json`
- `rounds/round_1/performances/noel/canonical/run_20260417_next_wave_replay_summary.md`
- `rounds/round_1/performances/noel/canonical/replay_high_roi_variant_batch.py`
- `rounds/round_1/performances/noel/canonical/run_20260417_high_roi_variant_replay_metrics.json`
- `rounds/round_1/performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`
- `rounds/round_1/performances/noel/canonical/replay_five_bot_batch.py`
- `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`
- `rounds/round_1/performances/noel/canonical/run_20260416_five_bot_replay_summary.md`
- `rounds/round_1/performances/noel/canonical/run_20260416_cross_bot_log_insights.md`
- `rounds/round_1/workspace/06_testing/candidate_26_overfit_audit.md`
- `phase_05_implementation_context.md`
- `04_strategy_specs/spec_experimental_5_bot_matrix.md`
- `04_strategy_specs/spec_next_wave_10_bot_matrix.md`
- `04_strategy_specs/spec_high_roi_3_variant_batch.md`
- `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`

## Next Priority Action

Verify the active upload file for `candidate_26_v3_a3b1_one_sided_exit_overlay.py`, then use it as the final Round 1 submission unless the user explicitly chooses the slightly lower-PnL `candidate_28` backup.

## Deadline Risk

Low. We have platform validation for the incumbent and both threshold refinements; the remaining risk is active-file verification and final upload handling.
