# Phase 05 Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned
- Last updated: 2026-04-17

## What Has Been Done

- Implemented five Noel bots; the baseline bot is now archived under `noel/historical`, while active validation focuses on canonical bot 02:
  - `rounds/round_1/bots/noel/historical/candidate_09_bot01_baseline_fv_combo.py`
  - `rounds/round_1/bots/noel/historical/candidate_10_bot02_carry_tight_mm.py`
  - `rounds/round_1/bots/noel/historical/candidate_11_bot03_micro_scalper.py`
  - `rounds/round_1/bots/noel/historical/candidate_12_bot04_aco_markov.py`
  - `rounds/round_1/bots/noel/historical/candidate_13_bot05_hybrid_adaptive.py`
- Linked implementation spec: `rounds/round_1/workspace/04_strategy_specs/spec_experimental_5_bot_matrix.md`.
- Static syntax check passed for all five bots.
- Smoke test with fake datamodel and minimal order books passed for all five bots.
- Updated `candidate_10_bot02_carry_tight_mm.py` after performance-log review so ACO passive quotes use remaining capacity instead of a fixed 24-unit size. This aligns bot 02 with the approved spec's full-capacity quote intent.
- Added next-wave deployable bot batch; in the current pulled tree these are historical comparison artifacts under `rounds/round_1/bots/noel/historical/`:
  - `candidate_14_aco_kalman_latent_fv.py`
  - `candidate_15_aco_hmm_regime_mm.py`
  - `candidate_16_aco_edge_quality_gate.py`
  - `candidate_17_aco_inventory_lifecycle.py`
  - `candidate_18_aco_offline_policy_table.py`
  - `candidate_19_ipr_execution_upgrade.py`
  - `candidate_20_dual_product_risk_scheduler.py`
  - `candidate_21_one_sided_book_specialist.py`
  - `candidate_22_micro_alpha_rescue.py`
  - `candidate_23_adaptive_aco_controller.py`
- Added submission manifest: `rounds/round_1/bots/noel/canonical/next_wave_submission_manifest.md`.
- Linked next-wave implementation spec: `rounds/round_1/workspace/04_strategy_specs/spec_next_wave_10_bot_matrix.md`.
- Added high-ROI deployable bot batch under `rounds/round_1/bots/noel/canonical/`:
  - `candidate_26_v3_a3b1_one_sided_exit_overlay.py`
- Linked high-ROI implementation spec: `rounds/round_1/workspace/04_strategy_specs/spec_high_roi_3_variant_batch.md`.
- Added threshold refinement deployable bot batch, now archived under `rounds/round_1/bots/noel/historical/` after platform testing:
  - `candidate_27_v1_c26_soft_flatten.py`
  - `candidate_28_v1_c26_strict_one_sided.py`
- Linked threshold refinement spec: `rounds/round_1/workspace/04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`.
- Updated high-ROI replay to include historical controls `candidate_10`, `candidate_24`, and `candidate_25` plus canonical `candidate_26`, `candidate_27`, and `candidate_28`.
- Platform artifacts for `candidate_27` and `candidate_28` were later stored with their bot files under `noel/historical`; `candidate_26` remains the canonical recommended file.

## Current Findings

- All bots implement `Trader.run(state)` and return `(result, 0, traderData)`.
- All bots include per-product exception isolation.
- All bots clip order sizes against product limits before placing orders.
- No unsupported imports or print logging found.
- Patched `candidate_10_bot02_carry_tight_mm.py` still passes `py_compile` and the five-bot immediate-fill replay with no errors or rejections. Replay PnL is unchanged because passive future fills are not modeled.
- All current high-ROI bots are self-contained single-file `Trader` implementations.
- Static `py_compile` passed for baseline plus `candidate_14` through `candidate_23`.
- Next-wave immediate-fill replay passed with `0` errors and `0` rejections for every bot.
- Static `py_compile` passed for `candidate_24`, `candidate_25`, and `candidate_26`.
- High-ROI immediate-fill replay passed with `0` errors and `0` rejections for the control plus all three new variants.
- Static `py_compile` passed for `candidate_26`, `candidate_27`, `candidate_28`, and the updated high-ROI replay script.
- Updated high-ROI immediate-fill replay passed with `0` errors and `0` rejections for control `candidate_10`, historical `candidate_24`/`candidate_25`, and canonical `candidate_26`/`candidate_27`/`candidate_28`.

## Decisions Made

- Use `candidate_26_v3_a3b1_one_sided_exit_overlay.py` as the recommended platform upload target after platform results; keep patched `candidate_10_bot02_carry_tight_mm.py` as the historical fallback.
- Keep `candidate_13_bot05_hybrid_adaptive.py` as a defensive fallback and `candidate_12_bot04_aco_markov.py` as an ACO-focused fallback.
- Do not select final active submission until platform-like validation exists for the patched primary candidate.
- Treat next-wave bots as platform-test candidates; do not promote from replay PnL alone.
- Prioritize platform runs for `candidate_19`, `candidate_14`, `candidate_23`, `candidate_18`, and `candidate_21` if upload time is limited.
- Prioritize current high-ROI platform uploads in this order: `candidate_26`, `candidate_25`, `candidate_24`; keep `candidate_10` as the control.
- Platform artifacts now rank `candidate_26` first; keep `candidate_10` as the lower-risk fallback.
- For the threshold refinement pass, upload `candidate_27` first and `candidate_28` second; keep `candidate_26` as incumbent until a platform JSON/log result beats it.
- After platform results for `candidate_27` and `candidate_28`, keep `candidate_26` as final recommended upload; `candidate_28` is closest backup and `candidate_27` is rejected.

## Open Questions / Blockers

- Human/code review of implementation is pending.
- Platform JSON/log performance validation exists for `candidate_24`, `candidate_25`, `candidate_26`, `candidate_27`, and `candidate_28`.
- Need final human submission decision and active-file verification before upload.

## Linked Artifacts

- `04_strategy_specs/spec_experimental_5_bot_matrix.md`
- `04_strategy_specs/spec_next_wave_10_bot_matrix.md`
- `04_strategy_specs/spec_high_roi_3_variant_batch.md`
- `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`
- `03_strategy_candidates.md`
- `rounds/round_1/bots/noel/canonical/next_wave_submission_manifest.md`
- `rounds/round_1/bots/noel/historical/candidate_09_bot01_baseline_fv_combo.py`
- `rounds/round_1/bots/noel/historical/candidate_10_bot02_carry_tight_mm.py`
- `rounds/round_1/bots/noel/historical/candidate_24_v1_a1b1_size_skew_refine.py`
- `rounds/round_1/bots/noel/historical/candidate_25_v2_a2b1_conservative_regime_gate.py`
- `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`
- `rounds/round_1/bots/noel/historical/candidate_27_v1_c26_soft_flatten.py`
- `rounds/round_1/bots/noel/historical/candidate_28_v1_c26_strict_one_sided.py`

## Next Priority Action

Verify the active upload file and use `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py` as the final recommended upload.

## Deadline Risk

Low. The incumbent and threshold refinements have platform JSON/log artifacts; the remaining risk is active-file verification.
