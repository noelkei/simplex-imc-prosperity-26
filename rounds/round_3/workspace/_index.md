# Round Control Panel

## Round And Deadline

- Round: `round_3`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_3.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Consume the closed `round_3` package as input to `round_4`:
read the `101`-run synthesis, the closeout retrospective, and the updated
research memory before reopening EDA, understanding, or strategy work in the
next round. `round_3` no longer expects new platform runs.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Unassigned | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Unassigned | Unassigned | [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md), [`01_eda/eda_round_3_retrospective_carry_forward.md`](01_eda/eda_round_3_retrospective_carry_forward.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Unassigned | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | None |
| 03 Strategy | READY_FOR_REVIEW | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md), [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md), [`03_next_wave_bot_planning.md`](03_next_wave_bot_planning.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Review pending; Round 3 strategy is closed and should now be consumed as Round 4 framing |
| 04 Spec | COMPLETED | amin | Unassigned | [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md), [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md), [`04_strategy_specs/spec_learning_batch_wave1.md`](04_strategy_specs/spec_learning_batch_wave1.md), [`04_strategy_specs/spec_learning_batch_wave2.md`](04_strategy_specs/spec_learning_batch_wave2.md), [`04_strategy_specs/spec_learning_batch_wave3.md`](04_strategy_specs/spec_learning_batch_wave3.md), [`04_strategy_specs/spec_learning_batch_wave4.md`](04_strategy_specs/spec_learning_batch_wave4.md), [`04_strategy_specs/spec_learning_batch_wave5.md`](04_strategy_specs/spec_learning_batch_wave5.md) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | READY_FOR_REVIEW | amin | Unassigned | [`05_implementation/learning_batch_wave1_manifest.md`](05_implementation/learning_batch_wave1_manifest.md), [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md), [`05_implementation/learning_batch_wave3_manifest.md`](05_implementation/learning_batch_wave3_manifest.md), [`05_implementation/learning_batch_wave4_manifest.md`](05_implementation/learning_batch_wave4_manifest.md), [`05_implementation/learning_batch_wave5_manifest.md`](05_implementation/learning_batch_wave5_manifest.md) / [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Review pending; Wave 5 observed pairs were archived, unpaired bots were retired, and `canonical/` is now intentionally empty |
| 06 Testing/performance | READY_FOR_REVIEW | amin | Unassigned | [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md), [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md), [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md), [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md) / [`phase_06_testing_context.md`](phase_06_testing_context.md) | Review pending; the synthesis now covers `101` runs and closes Round 3 as retrospective evidence |
| 07 Debugging/iteration | READY_FOR_REVIEW | amin | Unassigned | [`06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md`](06_debugging/issue_2026-04-25_active_voucher_strike_misallocation.md), [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Review pending; debugging conclusions have been converted into carry-forward principles, untested hypotheses, and anti-patterns |

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
| `L-delta1` | primary | archived evidence | wave 5 closeout | high | `W5-04` closes the round as the best pure fallback benchmark and confirms delta-1 as the clean base/context branch | captured in synthesis + closeout | amin | Carry into `round_4` as base/control framing |
| `L-itm` | primary | archived evidence | wave 5 closeout | high | `W5-01` re-confirms the `W4-03/W4-04` winner family without creating a new architecture class | captured in synthesis + closeout | amin | Carry into `round_4` as preferred additive overlay framing |
| `L-active-upside-distilled` | primary | research-only | wave 5 closeout | medium/high | Observed Wave 5 descendants stay informative for upside/retention learning, but not as active Round 3 queue | captured in synthesis + closeout | amin | Re-enter only if `round_4` data supports the same mechanics |
| `L-toxic-strike-signals` | secondary | research-only | wave 5 closeout | medium/high | Toxic strikes finished the round looking more useful as veto/state information than as normal legs | captured in synthesis + closeout | amin | Carry into `round_4` EDA as a framing hypothesis |
| `L-heavy-regime` | deferred | defer | post-round_3 | low/untested | Hidden-state complexity stayed intentionally deferred behind simpler observable regime gates and shutdown logic | intentionally excluded from the closeout winner set | amin | Reconsider only if simpler gates fail with fresh evidence |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- All observed Round 3 implementations now live in `../bots/amin/historical/`.
- The `7` observed Wave 5 bot-performance pairs were archived after analysis.
- The unpaired Wave 5 bots were retired as `untested due to round close`, not promoted to historical evidence.
- `rounds/round_3/bots/amin/canonical/` is intentionally empty for this round.
- Implementation status at close:
  - `L-delta1`: confirmed benchmark / fallback family.
  - `L-itm`: preferred additive winner overlay.
  - `L-active-subsets`: research-only, not a normal finalist family.
  - `L-toxic-strike-signals`: research-only signal-role branch.
  - `L-upper` and `L-surface`: exploratory only.

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
- Best Wave 4 run and best clean full-stack family reference: `../performances/amin/historical/candidate_w4_03_delta1_itm_kalman_stack.json` at `1606.305`.
- Wave 4 runner-up and family confirmer: `../performances/amin/historical/candidate_w4_04_delta1_itm_kalman_strict.json` at `1604.305`.
- Best Wave 5 run and pure fallback champion: `../performances/amin/historical/candidate_w5_04_delta1_kalman_fallback.json` at `1672.000`.
- Best Wave 5 winner-protection confirmer: `../performances/amin/historical/candidate_w5_01_delta1_itm_final_control.json` at `1606.305`.
- Best isolated product learners: `probe_l01_hydro_reversion = +556.031`,
  `probe_l02_hydro_imbalance = +537.656`, `probe_l05_vex_imbalance = +446.387`,
  `probe_l04_vex_reversion = +309.613`.
- Closeout interpretation highlights:
  `W5-04` raises the clean fallback benchmark, `W5-01` confirms the winner
  family without creating a new one, `W5-11` supports toxic-strike veto
  framing, and the old `>10k` / `~18k` peaks now survive only as retention and
  strike-selection lessons.
- There is still no promoted final Round 3 submission artifact, because the
  round is now being closed as retrospective evidence rather than live-finalized
  from this workspace.
- Interpretation limit: results are non-authoritative evidence, not rules.

## Post-Run Research Memory

- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`06_testing/round_3_closeout_retrospective.md`](06_testing/round_3_closeout_retrospective.md)
- Key current takeaways: `activitiesLog` final-sum remains the best PnL proxy
  when `profit` is unavailable; `W5-04` is the best pure fallback benchmark;
  `W4-03/W4-04/W5-01` define the best full-stack winner family; `VEV_5300` is
  still the only active strike with positive `10k` markout but now belongs to
  special-case rescue framing only; `VEV_5000/5100/5200` are better read as
  danger-state evidence than as default legs; giant legacy `>10k` peaks look
  more like retention failures than promotable architecture.

## Blockers And Decisions Needed

- Phase 00 review is pending.
- Phase 01 review is pending.
- Phase 02 review is pending.
- Historical artifact analysis now exists under `06_testing/`.
- Voucher expiry framing is now confirmed by the live challenge brief: the current upload regime is `TTE=5d`, so historical `6d-8d` evidence should be treated as nearby-but-not-identical.
- No further Round 3 run queue remains.
- Main remaining decision is only how aggressively to carry Round 3 lessons into Round 4 without overstating them as facts of the new round.
- Exact round-end timestamp is still unknown.

## Final Submission Status

- Candidate: none finalized inside `round_3`; closeout leaves `W4-03/W4-04/W5-01` as the best full-stack family reference and `W5-04` as the best fallback benchmark.
- File: none.
- Decision reason: none.
- Linked spec: none.
- Linked validation run: none.
- Comparability status: `unclear`
- Contract readiness status: `Round 3 closed as retrospective evidence; no active canonical implementation remains`
- Active file verified: `yes, at compile level`
- Last validation: `101`-run closeout synthesis plus Wave 5 archival cleanup.
- Active-file verification: `not applicable for round_3 canonical; all observed artifacts archived`.

## Recently Changed Artifacts

- Archived the observed `7` Wave 5 bot/performance pairs into `../bots/amin/historical/` and `../performances/amin/historical/` on `2026-04-26`
- Retired the `5` unpaired Wave 5 canonical bots as `untested due to round close` on `2026-04-26`
- Archived the three legacy run-summary `.md` files from `../performances/amin/canonical/` into `../performances/amin/historical/` on `2026-04-26`
- Updated `06_testing/round_3_full_performance_synthesis.md` to the `101`-run closeout version on `2026-04-26`
- Added `06_testing/round_3_closeout_retrospective.md` on `2026-04-26`
- Refreshed `post_run_research_memory.md` for the partial Wave 5 closeout and Round 4 carry-forward framing on `2026-04-26`

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
