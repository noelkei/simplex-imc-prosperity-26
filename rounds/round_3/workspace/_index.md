# Round Control Panel

## Round And Deadline

- Round: `round_3`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_3.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Wave 5 is now specified and implemented in `canonical`. Next:
run the 12-bot Wave 5 final exploitation / upside-distillation batch on the
platform, then compare clean winner protection versus distilled `>10k`
upside descendants.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Unassigned | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Unassigned | Unassigned | [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Unassigned | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | None |
| 03 Strategy | READY_FOR_REVIEW | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md), [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md), [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Review pending; Wave 5 exploitation planning has now been consumed by spec and implementation |
| 04 Spec | COMPLETED | amin | Unassigned | [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md), [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md), [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md), [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md), [`04_strategy_specs/spec_learning_batch_wave3.md`](04_strategy_specs/spec_learning_batch_wave3.md), [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md), [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | READY_FOR_REVIEW | amin | Unassigned | [`05_implementation/learning_batch_wave1_manifest.md`](05_implementation/learning_batch_wave1_manifest.md), [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md), [`05_implementation/learning_batch_wave3_manifest.md`](05_implementation/learning_batch_wave3_manifest.md), [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md), [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md) / [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Review pending; Wave 5 is implemented and waiting on platform runs |
| 06 Testing/performance | IN_PROGRESS | amin | Unassigned | [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md), [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md), [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md) / [`phase_06_testing_context.md`](phase_06_testing_context.md) | Full 94-run synthesis is done; next bottleneck is platform execution of Wave 5 |
| 07 Debugging/iteration | IN_PROGRESS | amin | Unassigned | [`06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md`](06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Wave 5 is now coded; next step is live validation and post-run pruning |

## Product Scope

- Algorithmic: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Manual only: Ornamental Bio-Pods (symbol not stated in the official round page)
- EDA shortlist for early strategy work: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Understanding-led branch split: separate `HYDROGEL_PACK`; use `VELVETFRUIT_EXTRACT` as both standalone delta-1 candidate and voucher anchor; treat `VEV_5000` to `VEV_5300` as first-wave option scope and `VEV_4000` / `VEV_4500` as second-wave structural-anchor scope
- EDA de-emphasis / exclusion: investigate `VEV_4500`, `VEV_5400`, `VEV_5500`; exclude `VEV_6000`, `VEV_6500` from active bot logic unless later evidence changes
- Live challenge brief confirmation: vouchers are issued with `TTE=7d` starting on Round 1 day 1, so the active Round 3 upload regime is confirmed `TTE=5d`
- Live logger update: `VEV_5400/5500` are reopened for learner bots; `VEV_6000/6500` still look like floor products
- Full-synthesis update: isolated `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are now live-positive; `VEV_5100` and `VEV_5200` are the strongest negative evidence; `VEV_5300` is only the least-bad active strike, not a standalone winner

## External Paper Research Status

- Status: `completed`
- Expected folder: `../research/papers_raw/`
- Raw papers present: `8`
- Input types present: `2 latex_source`, `6 pdf`
- Waiting state: `fully-processed`
- Markdown conversions present:
  - `../research/papers_md/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model.md`
  - `../research/papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md`
  - `../research/papers_md/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.md`
  - `../research/papers_md/west_2004_better_approximations_to_cumulative_normal_functions.md`
  - `../research/papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md`
  - `../research/papers_md/muravyev_2015_order_flow_and_expected_option_returns.md`
  - `../research/papers_md/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.md`
  - `../research/papers_md/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.md`
- Processed paper summaries:
  - `../research/papers_processed/choi_2022_bachelier_guide_processed.md`
  - `../research/papers_processed/bergault_2022_multi_asset_mm_processed.md`
  - `../research/papers_processed/crr_1979_simplified_approach_processed.md`
  - `../research/papers_processed/west_2004_cumulative_normal_processed.md`
  - `../research/papers_processed/muravyev_2015_option_order_flow_processed.md`
  - `../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md`
  - `../research/papers_processed/garcia_ares_2023_expiration_days_processed.md`
  - `../research/papers_processed/fengler_2005_surface_smoothing_processed.md`
- Strategy dependency: Strategy should start with a paper intake pass over the
  current processed set; no further 02b work is pending unless new papers
  arrive or Strategy identifies a new literature gap

## Active Strategies

Candidate count is ROI-driven, not fixed. Track all high-ROI active candidates
with roles, priority tiers, and implementation waves.

| Candidate ID | Role | Priority Tier | Implementation Wave | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `L-delta1` | primary | implemented | wave 5 | high | Wave 5 keeps the Kalman delta-1 base alive as both benchmark and winner scaffold | captured in `spec_learning_batch_wave5.md` | amin | Decide after live runs whether fallback delta-1 still matters once the full batch is compared |
| `L-itm` | primary | implemented | wave 5 | high | `W4-03/W4-04` made active ITM on the Kalman base the current winner family and Wave 5 now protects that axis directly | captured in `spec_learning_batch_wave5.md` | amin | Decide after live runs whether the final submission should simply be the protected winner family |
| `L-active-upside-distilled` | primary | implemented | wave 5 | medium/high | Wave 5 now contains the pruned `>10k` descendants with hard retention discipline and VEX anchoring | captured in `spec_learning_batch_wave5.md` | amin | Decide which, if any, distilled branch is finalist-grade |
| `L-toxic-strike-signals` | secondary | implemented | wave 5 | medium | Wave 5 implements toxic-strike veto / transformed-threshold use instead of forcing direct inverse inventory | captured in `spec_learning_batch_wave5.md` | amin | Decide whether toxic strikes survive only as signal inputs |
| `L-heavy-regime` | deferred | defer | post-wave 5 | low/untested | HMM/Markov-style regime logic remains intentionally deferred behind simpler online gates, trend, transformed thresholds, and Kalman | intentionally excluded from the current Wave 5 plan | amin | Decide later only if the final simple salvage wave fails cleanly |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- The full 24-bot Wave 3 batch has now been run and archived from `../bots/amin/canonical/` to `../bots/amin/historical/`.
- The full 12-bot Wave 4 finalist batch has now also been run and archived to
  `../bots/amin/historical/`.
- Current family status after the updated 94-run synthesis:
  - `L-delta1`: confirmed benchmark / fallback family.
  - `L-itm`: promoted to the current clean winner family through `W4-03/W4-04`.
  - `L-active-subsets`: no longer a normal finalist family; it now survives only as upside-distillation research.
  - `L-upper`: paused out of Wave 3.
  - `L-surface`: paused out of Wave 3.
- Wave 3 implementation focus:
  - `W3-01` to `W3-02`: delta-1 champion and simple regime gating
  - `W3-03`: `VEX + ITM` active refresh
  - `W3-04` to `W3-11`: `5300` rescue, no-trade, transformed-threshold, and trend-gate designs
  - `W3-12` to `W3-14`: tiny inverse toxic-strike diagnostics
  - `W3-15` to `W3-16`: compact Kalman tests
  - `W3-17` to `W3-19`: selective active filters and capped salvage
  - `W3-20` to `W3-22`: inverse toxic-strike sidecar tests
  - `W3-23` to `W3-24`: near-final stacked architecture challengers
- Wave 5 implementation is now written and materialized in
  `../bots/amin/canonical/`:
  - `4` clean finalist / benchmark bots,
  - `6` `>10k` upside-distillation descendants,
  - `2` toxic-strike-as-signal variants.

## Baseline / Reference Bot

- `../bots/amin/historical/candidate_c06_composite_base.py` with `../performances/amin/historical/candidate_c06_composite_base.json` remains the frozen legacy composite reference.
- `../performances/amin/historical/r3_b02_itm_residual.json` is still the best historical learner reference.
- `../bots/amin/historical/baseline_state_logger.py` with `../performances/amin/historical/baseline_state_logger.json` is the live market diagnostic reference.

## Historical / Frozen Artifacts

- All Round 3 bots that already had paired performance artifacts were moved from `canonical/` to `historical/` on `2026-04-25`.
- `../bots/amin/historical/candidate_c06_composite_base.py` remains the specific tested legacy composite reference.
- `../bots/amin/historical/candidate_c06_v01_centered_base.py`, `candidate_c06_composite_inv.py`, and `baseline_state_logger.py` were also frozen after their first live runs were analyzed.
- The full 25-bot Wave 1 learner batch is now frozen under
  `../bots/amin/historical/` with matching run artifacts under
  `../performances/amin/historical/`.
- The consolidated cross-run evidence base now lives in
  `06_testing/round_3_full_performance_synthesis.md` and the CSV artifacts
  under `06_testing/artifacts/full_synthesis/`.

## Latest Results And Best Current Candidate

- Best historical tested artifact: `../performances/amin/historical/r3_b02_itm_residual.json` with real platform PnL `1409.371`.
- Historical runner-up: `../performances/amin/historical/r3_b02_itm_anchor.json` with real platform PnL `726.893`.
- Best Wave 1 learner: `../performances/amin/historical/probe_l06_delta1_dual_independent.json` with real platform PnL `886.102`.
- Best Wave 2 run: `../performances/amin/historical/candidate_w2_01_delta1_dual_control.json` at `872.653`; `candidate_w2_04_delta1_itm_overlay.json` matched it exactly with no incremental ITM contribution.
- Best Wave 3 run and prior clean champion: `../performances/amin/historical/candidate_w3_15_delta1_kalman_control.json` at `1527.305`.
- Best Wave 4 run and current overall leader: `../performances/amin/historical/candidate_w4_03_delta1_itm_kalman_stack.json` at `1606.305`.
- Wave 4 runner-up and family confirmer: `../performances/amin/historical/candidate_w4_04_delta1_itm_kalman_strict.json` at `1604.305`.
- Best pure fallback champion remains `../performances/amin/historical/candidate_w4_01_delta1_kalman_control.json` at `1527.305`.
- Best isolated product learners: `probe_l01_hydro_reversion = +556.031`,
  `probe_l02_hydro_imbalance = +537.656`, `probe_l05_vex_imbalance = +446.387`,
  `probe_l04_vex_reversion = +309.613`.
- Wave 3 interpretation highlights:
  `W3-23` proves active `ITM` can add value on top of delta-1, `W3-17` is the
  first credible standalone selective `5300` winner, and the old `>10k` /
  `~18k` peaks now read as retention failures rather than ready-made winners.
- There is still no promoted final Round 3 submission yet, but the winner axis
  is now much narrower: `W4-03/W4-04` versus one last upside-distillation wave.
- Interpretation limit: results are non-authoritative evidence, not rules.

## Post-Run Research Memory

- [`post_run_research_memory.md`](post_run_research_memory.md)
- Key current takeaways: `activitiesLog` final-sum remains the best PnL proxy
  when `profit` is unavailable; `W3-15` is now the clean architectural
  champion; `W3-23` is the best additive `ITM` overlay path; `VEV_5300` is
  still the only active strike with positive `10k` markout and `W3-17` is the
  first credible standalone selective `5300` winner; `VEV_5000/5100/5200`
  remain final-bot closure candidates unless explicitly rerun; giant legacy
  `>10k` peaks look more like retention failures than promotable architecture;
  upper remains research-only and floor looks closeable.

## Blockers And Decisions Needed

- Phase 00 review is pending.
- Phase 01 review is pending.
- Phase 02 review is pending.
- Historical artifact analysis now exists under `06_testing/`.
- Voucher expiry framing is now confirmed by the live challenge brief: the current upload regime is `TTE=5d`, so historical `6d-8d` evidence should be treated as nearby-but-not-identical.
- Need the Wave 5 live runs to decide:
  - whether the round should simply promote `W4-03/W4-04`,
  - whether any distilled high-upside descendant can clearly beat that family,
  - and whether toxic strikes survive only as veto / anti-signal inputs.
- Exact round-end timestamp is still unknown.

## Final Submission Status

- Candidate: none yet, but `W4-03/W4-04` now define the current clean winner axis.
- File: none.
- Decision reason: none.
- Linked spec: none.
- Linked validation run: none.
- Comparability status: `unclear`
- Contract readiness status: `Wave 5 specified and implemented; waiting live validation`
- Active file verified: `yes, at compile level`
- Last validation: `py_compile` on Wave 5 generator and all 12 bots.
- Active-file verification: `platform run pending`.

## Recently Changed Artifacts

- Added Round 3 source capture: `../../../docs/prosperity_wiki_raw/14_round_3.md` on `2026-04-24`
- Added official Round 3 facts: `../../../docs/prosperity_wiki/rounds/round_3.md` on `2026-04-24`
- Updated Phase 00 ingestion artifact: `00_ingestion.md` on `2026-04-24`
- Updated ingestion context: `phase_00_ingestion_context.md` on `2026-04-24`
- Updated data inventory: `../data/README.md` on `2026-04-24`
- Added Phase 01 EDA script: `01_eda/analyze_round_3_eda.py` on `2026-04-24`
- Added Phase 01 EDA summary: `01_eda/eda_option_surface_and_microstructure.md` on `2026-04-24`
- Added Phase 01 EDA processed artifacts under `../data/processed/` on `2026-04-24`
- Updated Phase 01 EDA context: `phase_01_eda_context.md` on `2026-04-24`
- Updated Phase 02 understanding summary: `02_understanding.md` on `2026-04-24`
- Updated Phase 02 understanding context: `phase_02_understanding_context.md` on `2026-04-24`
- Updated Phase 02b external paper research artifact: `02b_external_paper_research.md` on `2026-04-24`
- Updated Phase 02b external paper research context: `phase_02b_external_paper_research_context.md` on `2026-04-24`
- Added source-first paper markdown conversion: `../research/papers_md/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model.md` on `2026-04-24`
- Added source-first paper markdown conversion: `../research/papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/muravyev_2015_order_flow_and_expected_option_returns.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.md` on `2026-04-24`
- Added PDF-first paper markdown conversion: `../research/papers_md/west_2004_better_approximations_to_cumulative_normal_functions.md` on `2026-04-24`
- Added Batch 1 processed paper summary: `../research/papers_processed/choi_2022_bachelier_guide_processed.md` on `2026-04-24`
- Added Batch 1 processed paper summary: `../research/papers_processed/muravyev_2015_option_order_flow_processed.md` on `2026-04-24`
- Added Batch 1 processed paper summary: `../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md` on `2026-04-24`
- Added Batch 2 processed paper summary: `../research/papers_processed/garcia_ares_2023_expiration_days_processed.md` on `2026-04-24`
- Added Batch 2 processed paper summary: `../research/papers_processed/fengler_2005_surface_smoothing_processed.md` on `2026-04-24`
- Added Batch 3 processed paper summary: `../research/papers_processed/bergault_2022_multi_asset_mm_processed.md` on `2026-04-24`
- Added Batch 3 processed paper summary: `../research/papers_processed/crr_1979_simplified_approach_processed.md` on `2026-04-24`
- Added Batch 3 processed paper summary: `../research/papers_processed/west_2004_cumulative_normal_processed.md` on `2026-04-24`
- Updated Phase 02b external paper research artifact: `02b_external_paper_research.md` on `2026-04-24`
- Updated Phase 02b external paper research context: `phase_02b_external_paper_research_context.md` on `2026-04-24`
- Normalized Round 3 paper pipeline metadata under `../research/papers_md/` and `../research/papers_processed/` on `2026-04-24`
- Aligned the live 02b artifact and context to the refactored paper-research workflow on `2026-04-24`
- Updated Phase 04 spec: `04_strategy_specs/spec_c06_composite_base.md` on `2026-04-24`
- Updated Phase 04 spec: `04_strategy_specs/spec_c06_composite_inv.md` on `2026-04-24`
- Updated Phase 04 spec context: `phase_04_spec_context.md` on `2026-04-24`
- Implemented Bot A: `../bots/amin/canonical/candidate_c06_composite_base.py` on `2026-04-24`
- Implemented Bot B: `../bots/amin/canonical/candidate_c06_composite_inv.py` on `2026-04-24`
- Updated Phase 05 implementation context: `phase_05_implementation_context.md` on `2026-04-24`
- Updated Phase 03 strategy candidates: `03_strategy_candidates.md` on `2026-04-24`
- Updated Phase 03 strategy context: `phase_03_strategy_context.md` on `2026-04-24`
- Corrected Phase 03 strategy traceability for centered voucher residuals and controlled variant boundaries on `2026-04-25`
- Corrected Phase 04 specs to use an online residual-anchor proxy and observed-surface guardrails on `2026-04-25`
- Moved tested canonical bot/performance pairs into `../bots/amin/historical/` and `../performances/amin/historical/` on `2026-04-25`
- Added fresh corrected base challenger: `../bots/amin/canonical/candidate_c06_v01_centered_base.py` on `2026-04-25`
- Kept `candidate_c06_composite_inv.py` as the corrected controlled inventory challenger on `2026-04-25`
- Updated Phase 03/04/05/06 contexts plus `_index.md` state sync around the frozen-base rule on `2026-04-25`
- Added diagnostic logger: `../bots/amin/canonical/baseline_state_logger.py` on `2026-04-25`
- Added historical artifact analysis: `06_testing/round_3_historical_performance_analysis.md` on `2026-04-25`
- Added post-run research memory: `post_run_research_memory.md` on `2026-04-25`
- Added canonical live-run analysis: `06_testing/round_3_canonical_run_analysis.md` on `2026-04-25`
- Added learning matrix: `03_signal_strategy_learning_matrix.md` on `2026-04-25`
- Added learning-batch spec: `04_strategy_specs/spec_learning_batch_wave1.md` on `2026-04-25`
- Added learning-batch manifest: `05_implementation/learning_batch_wave1_manifest.md` on `2026-04-25`
- Added broad active-voucher debugging note: `06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md` on `2026-04-25`
- Added 25 new canonical learner bots under `../bots/amin/canonical/` on `2026-04-25`
- Archived the three newly tested live bots and raw artifacts under `historical/` on `2026-04-25`
- Archived the full 25-bot Wave 1 learner batch under `../bots/amin/historical/` and `../performances/amin/historical/` on `2026-04-25`
- Added full-performance synthesis analyzer: `06_testing/analyze_round_3_full_performance_synthesis.py` on `2026-04-25`
- Added full-performance synthesis report: `06_testing/round_3_full_performance_synthesis.md` on `2026-04-25`
- Added consolidated synthesis artifacts under `06_testing/artifacts/full_synthesis/` on `2026-04-25`
- Added next-wave planning artifact: `03_next_wave_bot_planning.md` on `2026-04-25`
- Added Wave 2 spec: `04_strategy_specs/spec_learning_batch_wave2.md` on `2026-04-25`
- Added Wave 2 implementation generator: `05_implementation/generate_learning_batch_wave2.py` on `2026-04-25`
- Added Wave 2 implementation manifest: `05_implementation/learning_batch_wave2_manifest.md` on `2026-04-25`
- Added 19 Wave 2 canonical bots under `../bots/amin/canonical/` on `2026-04-25`
- Updated Phase 03, 04, 05, and 06 contexts for the implemented Wave 2 batch on `2026-04-25`
- Archived the full 19-bot Wave 2 batch from `../bots/amin/canonical/` to `../bots/amin/historical/` after paired platform artifacts were uploaded on `2026-04-26`
- Updated Round 3 full synthesis to `58` runs with Wave 2, `>5k` peak analysis, no-trade candidates, and markout diagnostics on `2026-04-26`
- Added new full-synthesis CSV artifacts for Wave 2, `>5k` peaks, no-trade candidates, and markouts under `06_testing/artifacts/full_synthesis/` on `2026-04-26`
- Added Wave 3 spec: `04_strategy_specs/spec_learning_batch_wave3.md` on `2026-04-26`
- Added Wave 3 implementation generator: `05_implementation/generate_learning_batch_wave3.py` on `2026-04-26`
- Added Wave 3 implementation manifest: `05_implementation/learning_batch_wave3_manifest.md` on `2026-04-26`
- Added 24 Wave 3 canonical bots under `../bots/amin/canonical/` on `2026-04-26`
- Archived the full 24-bot Wave 3 batch from `../bots/amin/canonical/` to `../bots/amin/historical/` after paired platform artifacts were uploaded on `2026-04-26`
- Updated Round 3 full synthesis to `82` runs with Wave 3, `>10k` peak analysis, simple exit counterfactuals, and a Wave 3 decision board on `2026-04-26`
- Refreshed `03_next_wave_bot_planning.md` into a winner-focused `10`-core / `12`-with-closure planning cut on `2026-04-26`
- Updated Round 3 state contexts and memory to reflect the full post-Wave-2 synthesis on `2026-04-26`
- Added Wave 4 spec: `04_strategy_specs/spec_learning_batch_wave4.md` on `2026-04-26`
- Added Wave 4 implementation generator: `05_implementation/generate_learning_batch_wave4.py` on `2026-04-26`
- Added Wave 4 implementation manifest: `05_implementation/learning_batch_wave4_manifest.md` on `2026-04-26`
- Added 12 Wave 4 canonical finalist bots under `../bots/amin/canonical/` on `2026-04-26`
- Updated planning plus Phase 03, 04, 05, 06, and 07 contexts for the active
  Wave 4 finalist batch on `2026-04-26`
- Cleaned stale `canonical` archival references in Round 3 workspace docs and removed local cache artifacts on `2026-04-25`
- Pre-created from template: `2026-04-14`
