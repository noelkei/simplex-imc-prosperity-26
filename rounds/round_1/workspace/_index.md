# Round 1 Control Panel

## Round And Deadline

- Round: `round_1`
- Fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Promote `candidate_26_v3_a3b1_one_sided_exit_overlay.py` as the recommended final upload; `candidate_28_v1_c26_strict_one_sided.py` is the closest backup, and `candidate_27_v1_c26_soft_flatten.py` is rejected by platform PnL.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | COMPLETED | Claude | Approved 2026-04-16 | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | None recorded |
| 01 EDA | READY_FOR_REVIEW | Codex | Unassigned for advanced pass; prior EDA approved with caveats 2026-04-16 | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) + expansion EDA + [`01_eda/eda_advanced_signal_research.md`](01_eda/eda_advanced_signal_research.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Human review pending for advanced pass |
| 02 Understanding | COMPLETED | Claude | Approved 2026-04-16 | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | COMPLETED | Codex | User approved with caveats 2026-04-17 | [`03_strategy_candidates.md`](03_strategy_candidates.md) + [`03_strategy_next_wave_branches.md`](03_strategy_next_wave_branches.md) + [`03_strategy_research_per_product_3x3.md`](03_strategy_research_per_product_3x3.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | COMPLETED | Codex | Approved with caveats 2026-04-17 | [`04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`](04_strategy_specs/spec_candidate_27_28_threshold_refinements.md) + [`04_strategy_specs/spec_high_roi_3_variant_batch.md`](04_strategy_specs/spec_high_roi_3_variant_batch.md) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | READY_FOR_REVIEW | Codex | Unassigned | [`next_wave_submission_manifest.md`](../bots/noel/canonical/next_wave_submission_manifest.md) / [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Static checks, replay, and platform validation passed for current finalists; active-file verification still needed |
| 06 Testing/performance | READY_FOR_REVIEW | Codex | Unassigned | [`run_20260417_platform_artifact_analysis.md`](../performances/noel/canonical/run_20260417_platform_artifact_analysis.md) + [`run_20260417_high_roi_variant_replay_summary.md`](../performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md) / [`phase_06_testing_context.md`](phase_06_testing_context.md) | Final selection recorded; active-file verification still needed |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/README.md`](06_debugging/README.md) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategy families: 3.

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `A1+B1_clean_control` | high | strong | prior champion: fixed-FV ACO balanced maker plus +80 IPR carry, platform PnL `10007.0` | approved with caveats via existing candidate 10 spec | Codex | Keep as robust fallback |
| `A2+B1_residual_regime_aco` | high | medium-strong | highest-upside next challenger: ACO Markov/Kalman/z-score gates without weakening +80 IPR | approved with caveats | Codex | Platform-test `candidate_25` |
| `A3+B1_book_state_execution` | high | strong | best current platform artifact: `candidate_26`, total `10090.47`, same IPR `7286.0`, ACO `2804.47`; `candidate_28` confirms the family but does not beat it | approved with caveats | Codex | Promote `candidate_26`; keep `candidate_28` as backup |

## Next-Wave Strategy Backlog

Next-wave branches were implemented and are retained as historical comparison artifacts; the current upload set is the tighter high-ROI batch below.

| Branch | Theme | Why It Matters | Status |
| --- | --- | --- | --- |
| `candidate_14` | ACO latent FV | tests whether a Kalman filter improves trust in FV=10000 | implemented |
| `candidate_15` | ACO hidden regimes | tests the hidden-pattern hypothesis without abandoning fixed FV | implemented |
| `candidate_16` | ACO fill quality | logs show quality beats raw volume | implemented |
| `candidate_17` | ACO inventory lifecycle | best artifact finishes ACO flat | implemented |
| `candidate_18` | ACO offline policy table | interpretable state-action branch | implemented |
| `candidate_19` | IPR execution upgrade | tests guarded/frontloaded +80 carry | implemented |
| `candidate_20` | dual-product scheduler | protects total score from ACO drag | implemented |
| `candidate_21` | one-sided book specialist | turns one-sided books into exits/provision | implemented |
| `candidate_22` | micro alpha rescue | uses microstructure only as overlay | implemented |
| `candidate_23` | adaptive controller | combines filters conservatively | implemented |

## Experimental Implementation Batch

Five bots were implemented for performance testing. `bot_01` is now an archived baseline reference under `../bots/noel/historical/`; active validation is focused on canonical `bot_02`.

| Bot ID | Candidate ID | Bot Path | IPR Strategy | ACO Strategy | Status |
| --- | --- | --- | --- | --- | --- |
| `bot_01` | `candidate_09_baseline_fv_combo` | `../bots/noel/historical/candidate_09_bot01_baseline_fv_combo.py` | drift FV MM | fixed FV MM | validated local replay before archive; baseline reference |
| `bot_02` | `candidate_10_carry_tight_mm` | `../bots/noel/historical/candidate_10_bot02_carry_tight_mm.py` | max-long carry | tight aggressive MM | prior >10k baseline; fallback/reference |
| `bot_03` | `candidate_11_microstructure_scalper` | `../bots/noel/historical/candidate_11_bot03_micro_scalper.py` | microstructure scalper | microstructure scalper | historical; too weak without IPR carry |
| `bot_04` | `candidate_12_aco_markov_overlay` | `../bots/noel/historical/candidate_12_bot04_aco_markov.py` | drift FV MM | Markov-regime MM | historical; mine for ACO filters |
| `bot_05` | `candidate_13_hybrid_adaptive_model` | `../bots/noel/historical/candidate_13_bot05_hybrid_adaptive.py` | hybrid score/defensive | adaptive FV + score | historical; mine for adaptive ACO/skew ideas |

## Active Implementations

Maximum active implementation candidates: 2.

| Candidate ID | Variant ID | Bot Path | Parent Spec | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | `v3` | `../bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py` | `04_strategy_specs/spec_high_roi_3_variant_batch.md` | ACO one-sided/book-state overlay over IPR +80 | recommended final upload | `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md` |
| `candidate_28_v1_c26_strict_one_sided` | `v1` | `../bots/noel/historical/candidate_28_v1_c26_strict_one_sided.py` | `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md` | ACO stricter one-sided threshold overlay over `candidate_26` | closest backup, not promoted | `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md` |

## High-ROI Implementation Batch

| Candidate ID | File | Role | Local Sanity |
| --- | --- | --- | --- |
| `candidate_10` | `../bots/noel/historical/candidate_10_bot02_carry_tight_mm.py` | control / prior >10k baseline | replay clean |
| `candidate_24` | `../bots/noel/historical/candidate_24_v1_a1b1_size_skew_refine.py` | A1+B1 size/skew refinement | replay clean |
| `candidate_25` | `../bots/noel/historical/candidate_25_v2_a2b1_conservative_regime_gate.py` | A2+B1 conservative regime gate | replay clean |
| `candidate_26` | `../bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py` | A3+B1 one-sided/book-state overlay; current platform leader | replay clean |
| `candidate_27` | `../bots/noel/historical/candidate_27_v1_c26_soft_flatten.py` | C26 threshold refinement: earlier soft ACO flatten | replay clean; platform rejected |
| `candidate_28` | `../bots/noel/historical/candidate_28_v1_c26_strict_one_sided.py` | C26 threshold refinement: stricter one-sided overlay | replay clean; close platform backup |

## Historical / Non-Decision Artifacts

- `../bots/bruno/canonical/new_bot.py` exists, but is not the selected active implementation.
- `../bots/amin/canonical/26-candidate_03_combined.py` exists, but is not the selected active implementation.
- Do not treat round-local bot or performance artifacts as official rules.

## Baseline / Reference Bot

- Baseline strategy: `candidate_09_baseline_fv_combo`.
- Baseline file: `../bots/noel/historical/candidate_09_bot01_baseline_fv_combo.py`.
- Current leader: `candidate_26_v3_a3b1_one_sided_exit_overlay`.

## Latest Results And Best Current Candidate

- Platform artifact analyzer: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`.
- Raw analyzer output: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.json`.
- Next-wave strategy branches: `03_strategy_next_wave_branches.md`.
- Per-product top-3 and 3x3 research pass: `03_strategy_research_per_product_3x3.md`.
- Advanced signal research: `01_eda/eda_advanced_signal_research.md`.
- High-ROI three-variant spec: `04_strategy_specs/spec_high_roi_3_variant_batch.md`.
- Threshold refinement spec: `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`.
- High-ROI submission manifest: `../bots/noel/canonical/next_wave_submission_manifest.md`.
- High-ROI replay: `../performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`.
- Next-wave spec: `04_strategy_specs/spec_next_wave_10_bot_matrix.md`.
- Next-wave bot manifest: `../bots/noel/canonical/next_wave_submission_manifest.md`.
- Next-wave local replay: `../performances/noel/canonical/run_20260417_next_wave_replay_summary.md`.
- Latest comparable local replay: `../performances/noel/canonical/run_20260416_five_bot_replay_summary.md`.
- Raw metrics: `../performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`.
- Cross-bot log insight summary: `../performances/noel/canonical/run_20260416_cross_bot_log_insights.md`.
- PnL methodology: rank by platform-style JSON `profit`; use final `activitiesLog` per-product `profit_and_loss` for IPR/ACO split; use `graphLog`, `tradeHistory`, and local replay only as audit/sanity signals.
- Best platform-style artifact found: `../performances/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.json` with total PnL `10090.46875`, IPR PnL `7286.0`, ACO PnL `2804.46875`, final positions IPR `80`, ACO `9`.
- Robust fallback artifact: `../performances/noel/historical/candidate_10_bot02_carry_tight_mm.json` with total PnL `10007.0`, IPR PnL `7286.0`, ACO PnL `2721.0`, final positions IPR `80`, ACO `0`.
- Best non-Noel comparison: `../bots/amin/canonical/26-candidate_03_combined.json` with total PnL `9432.0625`, but it is stored outside the expected performance folder and has no matching log in this tree.
- Best current candidate: `candidate_26_v3_a3b1_one_sided_exit_overlay`; it improves ACO to `2804.47` without reducing +80 IPR behavior.
- Threshold platform check: `candidate_28_v1_c26_strict_one_sided` scored `10076.3125` total with ACO `2790.3125`, close but below `candidate_26`; `candidate_27_v1_c26_soft_flatten` scored `9920.1875` and is not a promotion candidate.
- Recommended next research pairings: A2+B1 for high-upside ACO residual-regime over IPR carry, and A3+B1 for ACO book-state/short-side execution over IPR carry.
- High-ROI replay sanity ranking after threshold refinements: `candidate_27` first, `candidate_26` second, `candidate_28` third, `candidate_25` fourth, `candidate_24` fifth, control `candidate_10` sixth; all have `0` rejections and `0` errors.
- Best next-wave local sanity candidates: `candidate_19` ties baseline in local replay, `candidate_14` is the best non-control branch, followed by `candidate_23`, `candidate_18`, and `candidate_21`.
- Interpretation limit: EDA/model results are non-authoritative evidence, not rules.

## Blockers And Decisions Needed

- Need final human upload action and active-file verification. Recommended upload is `candidate_26`; closest backup is `candidate_28`; robust fallback is `candidate_10`.
- Existing JSON/log artifacts do not embed bot hashes; exact code-version provenance remains an artifact caveat unless the platform run and `.py` are saved together immediately.
- Need active-file verification before final upload.

## Final Submission Status

- Candidate: `candidate_26_v3_a3b1_one_sided_exit_overlay` is the recommended canonical upload candidate; `candidate_10_carry_tight_mm` remains the lower-risk fallback.
- File: `../bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py` as current recommended leader; not active submission yet.
- Decision reason: best platform-style artifact PnL (`10090.46875`), exact `activitiesLog` product split, unchanged IPR `7286.0`, improved ACO `2804.46875`, and no log/profit audit issue in the matching canonical artifact. New challengers did not beat it: `candidate_28` scored `10076.3125`, `candidate_27` scored `9920.1875`.
- Linked spec: `04_strategy_specs/spec_high_roi_3_variant_batch.md`; `candidate_27`/`candidate_28` threshold challengers are linked from `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`.
- Linked validation run: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`, `../performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`, and `../performances/noel/canonical/run_20260416_cross_bot_log_insights.md`
- Overfit/cheat audit: `06_testing/candidate_26_overfit_audit.md`
- Comparability status: `yes within platform-style artifacts; exact code-version coupling is inferred when artifacts lack hashes`
- Contract readiness status: `static checks and local replay passed; platform artifact present for candidate_26`
- Active file verified: `no`
- Last validation: platform artifact analysis rerun with `candidate_27` and `candidate_28` artifacts, 2026-04-17.
- Active-file verification: not started.

## Recently Changed Artifacts

- Reopened strategy expansion: `2026-04-16`
- Added `01_eda/strategy_expansion_analysis.py`
- Added `01_eda/eda_strategy_expansion_feature_lab.md`
- Added `01_eda/eda_strategy_expansion_models.md`
- Added `01_eda/eda_cross_product_relationships.md`
- Added processed metrics: `../data/processed/strategy_expansion_metrics.json`
- Updated `03_strategy_candidates.md`
- Added `03_strategy_next_wave_branches.md`
- Added `01_eda/advanced_signal_research.py`
- Added `01_eda/eda_advanced_signal_research.md`
- Added processed metrics: `../data/processed/advanced_signal_research_metrics.json`
- Added `03_strategy_research_per_product_3x3.md`
- Added `04_strategy_specs/spec_high_roi_3_variant_batch.md`
- Added `04_strategy_specs/spec_candidate_27_28_threshold_refinements.md`
- Added `../bots/noel/historical/candidate_24_v1_a1b1_size_skew_refine.py`
- Added `../bots/noel/historical/candidate_25_v2_a2b1_conservative_regime_gate.py`
- Added `../bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`
- Added `../bots/noel/historical/candidate_27_v1_c26_soft_flatten.py`
- Added `../bots/noel/historical/candidate_28_v1_c26_strict_one_sided.py`
- Stored `candidate_27` and `candidate_28` platform `.json`/`.log` artifacts under `../performances/noel/historical/`.
- Reran `../performances/noel/canonical/analyze_platform_artifacts.py`; `candidate_26` remains the recommended final upload.
- Added `06_testing/candidate_26_overfit_audit.md`.
- Updated `../bots/noel/canonical/next_wave_submission_manifest.md` with current upload set.
- Added `../performances/noel/canonical/replay_high_roi_variant_batch.py`
- Updated `../performances/noel/canonical/run_20260417_high_roi_variant_replay_metrics.json`
- Updated `../performances/noel/canonical/run_20260417_high_roi_variant_replay_summary.md`
- Updated `phase_03_strategy_context.md` for the 2026-04-17 next-wave expansion.
- Added `04_strategy_specs/spec_experimental_5_bot_matrix.md`
- Added `04_strategy_specs/spec_next_wave_10_bot_matrix.md`
- Added five Noel bot implementations; current active file is under `../bots/noel/canonical/`, archived references are under `../bots/noel/historical/`
- Added ten next-wave Noel bots; current pulled tree stores them as historical artifacts, with the active control under `../bots/noel/canonical/`
- Added `../bots/noel/canonical/next_wave_submission_manifest.md`
- Added `../performances/noel/canonical/replay_five_bot_batch.py`
- Added `../performances/noel/canonical/run_20260416_five_bot_replay_metrics.json`
- Added `../performances/noel/canonical/run_20260416_five_bot_replay_summary.md`
- Added `../performances/noel/canonical/run_20260416_cross_bot_log_insights.md`
- Added `../performances/noel/canonical/analyze_platform_artifacts.py`
- Added `../performances/noel/canonical/run_20260417_platform_artifact_analysis.json`
- Added `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- Added `../performances/noel/canonical/replay_next_wave_batch.py`
- Added `../performances/noel/canonical/run_20260417_next_wave_replay_metrics.json`
- Added `../performances/noel/canonical/run_20260417_next_wave_replay_summary.md`
- Updated `phase_06_testing_context.md` with the JSON/log PnL methodology.
- Patched `../bots/noel/historical/candidate_10_bot02_carry_tight_mm.py` to use full-capacity ACO passive quotes before it became the historical fallback.
- Noted `bot_01` baseline path as `../bots/noel/historical/candidate_09_bot01_baseline_fv_combo.py`.
