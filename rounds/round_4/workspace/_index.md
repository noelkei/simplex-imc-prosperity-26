# Round Control Panel

## Round And Deadline

- Round: `round_4`
- Expected round fact source: [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Upload the refined active `_debugged.py` Wave 2 queue and rerun the
recalibrated option branches first:
`r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`, then
`r4_w2_01`, `r4_w2_02`, `r4_w2_06`, and `r4_w2_14`. Old pre-fix or superseded
Wave 2 runs should not be treated as live strategy evidence.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Codex | Unassigned | [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Codex | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Codex | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | Operationally complete; no blocker |
| 03 Strategy | READY_FOR_REVIEW | Codex | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Review pending |
| 04 Spec | COMPLETED | Codex | Human | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | Operationally approved by explicit user request to implement Wave 2 |
| 05 Implementation | READY_FOR_REVIEW | Codex | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Wave 2 bots implemented; validation pending |
| 06 Testing/performance | IN_PROGRESS | Codex | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Canonical Pack `C`, `E`, and `F` run summaries still missing |
| 07 Debugging/iteration | IN_PROGRESS | Codex | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Need re-run evidence on patched Wave 2 uploadables |

## Product Scope

- Algorithmic: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and
  `VEV_{4000,4500,5000,5100,5200,5300,5400,5500,6000,6500}`.
- Manual-only: `AETHER_CRYSTAL`, 2 week vanilla options, 3 week vanilla
  options, chooser option, binary put option, knock-out put option.
- Key round delta: counterparty IDs are now available in trade data via
  `Trade.buyer` and `Trade.seller`.
- Prior-round compatibility: `round_3` is compatible at product/mechanics
  level, but counterparties are a new information layer that must be revalidated in EDA.

## External Paper Research Status

- Status: `operationally complete; local raw set fully processed`
- Expected folder: `../research/papers_raw/`
- Raw papers detected: `9`
- Markdown conversions: `9 usable`
- Processed paper summaries: `9 canonical raw-derived` at top level, plus
  secondary `carry_forward`, `manual_reference`, and `knowledge_draft` buckets
- Strategy dependency: none; `03 Strategy` has consumed the nine-paper core and
  the short handoff and is ready for `04 Spec`

## Active Strategies

The active strategy queue remains a `15`-bot Wave 2 set, but it is now a
refined queue: six structural keepers plus nine replacement probes that test
entry quality and direct option attribution more honestly.

| Candidate ID | Role | Learning Pack | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_w2_01_vex_late_no_new_entry` | keep | `G` | strong | cheapest retained `VEX` rescue control | approved + implemented: `spec_pack_g_vex_retention_rescue.md` | Codex | Validate first |
| `r4_w2_05_5300_clean_value_retest` | keep | `H` | medium-high | clean `5300` baseline | approved + implemented: `spec_pack_h_5300_winner_style_and_veto.md` | Codex | Validate first |
| `r4_w2_07_5300_queue_takeover_probe` | keep | `H` | medium-high | best winner-style `5300` execution probe | approved + implemented: `spec_pack_h_5300_winner_style_and_veto.md` | Codex | Validate first |
| `r4_w2_08_5300_with_5200_veto` | keep | `H` | medium-high | strongest live-family plus useful veto combo | approved + implemented: `spec_pack_h_5300_winner_style_and_veto.md` | Codex | Validate first |
| `r4_w2_13_4000_forced_activation` | keep | `J` | medium-high | closes the biggest `4000` evidence gap | approved + implemented: `spec_pack_j_4000_activation_and_execution.md` | Codex | Validate first |
| `r4_w2_15_4000_quote_ladder_probe` | keep | `J` | medium-high | best direct `4000` execution-style test | approved + implemented: `spec_pack_j_4000_activation_and_execution.md` | Codex | Validate first |
| `r4_w2_02_vex_inside_book_only` | replacement | `G` | medium-high | tests whether clean-tape `VEX` entry matters more than more retention tweaks | approved + implemented: `spec_pack_g_vex_retention_rescue.md` | Codex | Validate after first slice |
| `r4_w2_06_5300_direct_dislocation_only` | replacement | `H` | medium-high | direct `5300` without parent contamination | approved + implemented: `spec_pack_h_5300_winner_style_and_veto.md` | Codex | Validate after first slice |
| `r4_w2_14_4000_option_only_band_entry` | replacement | `J` | medium-high | direct `4000` without parent contamination | approved + implemented: `spec_pack_j_4000_activation_and_execution.md` | Codex | Validate after first slice |
| `r4_w2_03_vex_micro_reversal_entry` | replacement | `G` | medium | aggression-reversal `VEX` entry | approved + implemented: `spec_pack_g_vex_retention_rescue.md` | Codex | Validate after first slice |
| `r4_w2_09_vex_tape_clean_entry` | replacement | `I` | medium | context as clean-entry filter rather than simple veto | approved + implemented: `spec_pack_i_light_context_overlays.md` | Codex | Validate after first slice |
| `r4_w2_12_5300_option_only_veto` | replacement | `I` | medium | direct `5300` attribution plus the useful veto | approved + implemented: `spec_pack_i_light_context_overlays.md` | Codex | Validate after first slice |
| `r4_w2_04_vex_depth_supported_entry` | replacement | `G` | medium | depth-supported `VEX` entry probe | approved + implemented: `spec_pack_g_vex_retention_rescue.md` | Codex | Lower priority |
| `r4_w2_10_vex_imbalance_surge_entry` | replacement | `I` | medium | event-driven `VEX` entry | approved + implemented: `spec_pack_i_light_context_overlays.md` | Codex | Lower priority |
| `r4_w2_11_vex_low_concentration_entry` | replacement | `I` | medium-low | family-ecology regime test | approved + implemented: `spec_pack_i_light_context_overlays.md` | Codex | Lower priority |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- Active Wave 2 implementations exist under
  [`../bots/noel/canonical/`](../bots/noel/canonical/).
- Historical Wave 1 implementations and their retired support code live under
  [`../bots/noel/historical/`](../bots/noel/historical/).
- Historical superseded Wave 2 drafts also live under
  [`../bots/noel/historical/`](../bots/noel/historical/).
- Shared engines:
  - [`../bots/noel/canonical/wave2_shared_engine.py`](../bots/noel/canonical/wave2_shared_engine.py)
- Historical shared engines:
  - [`../bots/noel/historical/wave1_shared_engine.py`](../bots/noel/historical/wave1_shared_engine.py)
- Canonical Wave 2 bot files:
  `r4_w2_01_vex_late_no_new_entry_debugged`,
  `r4_w2_02_vex_inside_book_only_debugged`,
  `r4_w2_03_vex_micro_reversal_entry_debugged`,
  `r4_w2_04_vex_depth_supported_entry_debugged`,
  `r4_w2_05_5300_clean_value_retest_debugged`,
  `r4_w2_06_5300_direct_dislocation_only_debugged`,
  `r4_w2_07_5300_queue_takeover_probe_debugged`,
  `r4_w2_08_5300_with_5200_veto_debugged`,
  `r4_w2_09_vex_tape_clean_entry_debugged`,
  `r4_w2_10_vex_imbalance_surge_entry_debugged`,
  `r4_w2_11_vex_low_concentration_entry_debugged`,
  `r4_w2_12_5300_option_only_veto_debugged`,
  `r4_w2_13_4000_forced_activation_debugged`,
  `r4_w2_14_4000_option_only_band_entry_debugged`,
  `r4_w2_15_4000_quote_ladder_probe_debugged`

Example when active:

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | base | `../bots/<member>/canonical/candidate_01_short_name.py` | `04_strategy_specs/spec_candidate_01_short_name.md` | none | none | validating | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` |

## Baseline / Reference Bot

- None selected.

## Post-Run Research Memory

- [`post_run_research_memory.md`](post_run_research_memory.md)

## Latest Results And Best Current Candidate

- Canonical Pack `A/B/D` run summaries now exist under
  `../performances/noel/canonical/`.
- Partial comparative synthesis exists in
  `06_testing/round_4_wave1_pack_abd_partial_synthesis.md`.
- A/B/D partial view:
  - best live base: `r4_s01_vex_base_control`
  - strongest reusable contextual feature: `r4_s10_5200_signal_only_veto`
  - biggest unresolved gap: honest `VEV_4000` activation
  - weakest confirmed branch: `r4_s02_hydro_base_control`
- Best current strategy posture:
  - `protect / rescue`: `VEX` retention variants
  - `exploit / isolate`: `5300`
  - `reuse as overlay`: `5200` veto
  - `coverage fill`: one clean `4000` test

Example when active:

| Candidate ID | Run Reference | Comparability | Decision | Notes |
| --- | --- | --- | --- | --- |
| `candidate_01` | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` | unclear | continue | non-authoritative evidence; caveats recorded in run summary |

- Best current candidate: unresolved after the A/B/D partial only
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Need exact manual contract details from the platform or accepted source before
  manual-order analysis can start.
- Need deadline confirmation to assess fast-mode risk accurately.
- Human review is still pending for Phases `01`, `02`, `03`, `04`, and `05`.
- No material gap currently blocks the `03/04` reroute, but canonical Pack `C`,
  `E`, and `F` summaries are still missing for full round closeout and keep
  `5300` confidence below the `VEX` / `5200` conclusions.

## Final Submission Status

- Candidate: none.
- File: none.
- Decision reason: none.
- Linked spec: none.
- Linked validation run: `06_testing/round_4_wave1_pack_abd_partial_synthesis.md`
- Comparability status: `unclear`
- Contract readiness status: `not checked`
- Active file verified: `no`
- Last validation: Pack `A/B/D` partial synthesis recorded on `2026-04-27`.
- Active-file verification: not started.

Example when active:

- Candidate: `candidate_01`
- File: `../bots/<member>/canonical/submission_active.py`
- Decision reason: best validated candidate under current evidence
- Linked spec: `04_strategy_specs/spec_candidate_01_short_name.md`
- Linked validation run: `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md`
- Comparability status: `yes`
- Contract readiness status: `passed`
- Active file verified: `yes`

## Recently Changed Artifacts

- Raw source added: `../../../docs/prosperity_wiki_raw/15_round_4.md` on `2026-04-26`
- Curated wiki added: `../../../docs/prosperity_wiki/rounds/round_4.md` on `2026-04-26`
- Raw data added: `../data/raw/prices_round_4_day_{1,2,3}.csv` and `../data/raw/trades_round_4_day_{1,2,3}.csv` on `2026-04-26`
- Ingestion artifact updated: `00_ingestion.md` on `2026-04-26`
- Prior-round intake added: `00_prior_round_intake.md` on `2026-04-26`
- Ingestion context updated: `phase_00_ingestion_context.md` on `2026-04-26`
- Canonical EDA added: `01_eda/eda_round_4_counterparty_and_option_book.md` on `2026-04-26`
- EDA annexes added: `01_eda/eda_round_4_counterparty_profiles.md`, `01_eda/eda_round_4_option_book_structure.md`, `01_eda/eda_round_4_option_volatility_and_pricing.md`, and `01_eda/eda_round_4_round3_revalidation.md` on `2026-04-26`
- EDA script extended with counterparty markouts, pair ecology, stability scoring, and engineered-feature checks: `01_eda/analyze_round_4_eda.py` on `2026-04-26`
- EDA context updated: `phase_01_eda_context.md` on `2026-04-26`
- EDA outputs extended: `../data/processed/derived_round_4_counterparty_markout_by_side.csv`, `../data/processed/derived_round_4_counterparty_pair_summary.csv`, `../data/processed/derived_round_4_counterparty_stability_scores.csv`, `../data/processed/derived_round_4_engineered_feature_summary.csv`, and `../data/processed/derived_round_4_candidate_online_features.csv` on `2026-04-26`
- Advanced option/counterparty outputs added: `../data/processed/derived_round_4_option_iv_surface_summary.csv`, `../data/processed/derived_round_4_option_bs_vs_heston_fit.csv`, `../data/processed/derived_round_4_counterparty_directional_profile.csv`, and `../data/processed/derived_round_4_counterparty_credit_metric_availability.csv` on `2026-04-27`
- Understanding summary added: `02_understanding.md` on `2026-04-27`
- Understanding context updated: `phase_02_understanding_context.md` on `2026-04-27`
- External paper research artifact rewritten around the final local-paper state:
  `02b_external_paper_research.md` on `2026-04-27`
- External paper research context updated: `phase_02b_external_paper_research_context.md` on `2026-04-27`
- External paper raw set normalized and ROI-filtered against `round_3` processed papers on `2026-04-27`
- All `papers_md` conversions for the current 9-paper raw set added under `../research/papers_md/` on `2026-04-27`
- Nine canonical raw-derived processed summaries added under
  `../research/papers_processed/` on `2026-04-27`
- Processed-set audit added: `02b_processed_set_audit.md` on `2026-04-27`
- Strategy handoff added: `02b_strategy_handoff.md` on `2026-04-27`
- Strategy candidates added: `03_strategy_candidates.md` on `2026-04-27`
- Strategy context updated: `phase_03_strategy_context.md` on `2026-04-27`
- Wave 1 learning matrix and grouped-spec recommendation added to
  `03_strategy_candidates.md` on `2026-04-27`
- Grouped Wave 1 strategy specs added under `04_strategy_specs/` on
  `2026-04-27`
- Phase 04 context updated: `phase_04_spec_context.md` on `2026-04-27`
- Wave 1 canonical bots added under `../bots/noel/canonical/` on `2026-04-27`
- Wave 1 canonical bots rewritten as standalone uploadable files on
  `2026-04-27`
- Phase 05 context updated: `phase_05_implementation_context.md` on `2026-04-27`
- Noel Wave 1 raw performance artifacts added under
  `../performances/noel/historical/` on `2026-04-27`
- Canonical Pack `A/B/D` run summaries added under
  `../performances/noel/canonical/` on `2026-04-27`
- Wave 1 Pack `A/B/D` partial synthesis added:
  `06_testing/round_4_wave1_pack_abd_partial_synthesis.md` on `2026-04-27`
- Round 4 post-run memory added: `post_run_research_memory.md` on `2026-04-27`
- Retrospective EDA addendum added:
  `01_eda/eda_round_4_wave1_abd_retrospective_addendum.md` on `2026-04-27`
- Phase 01 context updated: `phase_01_eda_context.md` on `2026-04-27`
- Phase 03 context updated: `phase_03_strategy_context.md` on `2026-04-27`
- Strategy candidates rewritten around the refined Wave 2 queue on
  `2026-04-28`
- Wave 2 grouped specs added under `04_strategy_specs/` on `2026-04-27`
- Phase 04 context updated for Wave 2 spec review on `2026-04-27`
- Wave 2 shared engine and `15` standalone uploadable bots added under
  `../bots/noel/canonical/` on `2026-04-27`
- Wave 2 `_debugged.py` upload set refined and superseded drafts moved to
  `../bots/noel/historical/` on `2026-04-28`
- Phase 05 context updated for the refined Wave 2 implementation on
  `2026-04-28`
- Phase 06 context updated for the refined Wave 2 rerun slice on `2026-04-28`
- Data README updated: `../data/README.md` on `2026-04-26`
- Round README updated: `../README.md` on `2026-04-26`
