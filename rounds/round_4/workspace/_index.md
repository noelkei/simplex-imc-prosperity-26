# Round Control Panel

## Round And Deadline

- Round: `round_4`
- Expected round fact source: [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Convert the uploaded Wave 1 raw performance artifacts into canonical summaries
and analyze Packs `A`, `B`, and `D` first, then expand to the remaining packs
once the control/comparison layer is clean.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Codex | Unassigned | [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Codex | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Codex | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | Operationally complete; no blocker |
| 03 Strategy | READY_FOR_REVIEW | Codex | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Review pending |
| 04 Spec | COMPLETED | Codex | Human | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | No blocker |
| 05 Implementation | READY_FOR_REVIEW | Codex | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Review pending |
| 06 Testing/performance | IN_PROGRESS | Codex | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Canonical run summaries still missing |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

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

Candidate count is ROI-driven, not fixed. `round_4` currently has a deliberate
Wave 1 of `15` exploration bots to test the new counterparty/context layer and
revalidate the best `round_3` structures under the new tape.

| Candidate ID | Role | Priority Tier | Implementation Wave | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_s15_round3_winner_revalidation` | primary | spec-first | wave 1 | strong | best carry-forward family under new filters | approved + implemented: `spec_pack_b_round3_revalidation.md` | Codex | Validate pack B |
| `r4_s01_vex_base_control` | primary | spec-first | wave 1 | strong | anchor control for all voucher overlays | approved + implemented: `spec_pack_a_delta1_controls.md` | Codex | Validate pack A |
| `r4_s02_hydro_base_control` | primary | spec-first | wave 1 | strong | independent delta-1 control | approved + implemented: `spec_pack_a_delta1_controls.md` | Codex | Validate pack A |
| `r4_s05_mark22_veto_gate` | primary | spec-first | wave 1 | medium-high | strongest direct round-4 novelty test | approved + implemented: `spec_pack_d_counterparty_defensive.md` | Codex | Validate pack D |
| `r4_s07_trade_to_book_execution_overlay` | primary | spec-first | wave 1 | medium-high | strongest execution overlay from EDA + papers | approved + implemented: `spec_pack_e_execution_and_family_context.md` | Codex | Validate pack E |
| `r4_s03_vex_4000_overlay` | secondary | spec-first | wave 1 | medium-high | direct ITM structural re-check | approved + implemented: `spec_pack_b_round3_revalidation.md` | Codex | Validate pack B |
| `r4_s04_vex_5300_overlay` | secondary | spec-first | wave 1 | medium-high | isolated `5300` re-check | approved + implemented: `spec_pack_c_5300_active_family.md` | Codex | Validate pack C |
| `r4_s06_counterparty_concentration_gate` | secondary | implement-first | wave 1 | medium-high | engineered context over raw names | approved + implemented: `spec_pack_d_counterparty_defensive.md` | Codex | Validate pack D |
| `r4_s13_4000_benign_flow_overlay` | secondary | implement-first | wave 1 | medium-high | old winner ingredient under benign flow | approved + implemented: `spec_pack_b_round3_revalidation.md` | Codex | Validate pack B |
| `r4_s09_5300_toxic_strike_gate` | secondary | implement-first | wave 1 | medium-high | `5300` gated by toxic neighbor context | approved + implemented: `spec_pack_c_5300_active_family.md` | Codex | Validate pack C |
| `r4_s11_5300_horizon_hold` | secondary | implement-first | wave 1 | medium-high | retention-focused `5300` redesign | approved + implemented: `spec_pack_c_5300_active_family.md` | Codex | Validate pack C |
| `r4_s10_5200_signal_only_veto` | exploratory | implement-first | wave 1 | medium-high | tests `5200` as signal-only monitor | approved + implemented: `spec_pack_d_counterparty_defensive.md` | Codex | Validate pack D |
| `r4_s08_family_pressure_overlay` | exploratory | validate-next | wave 1 | medium | family-state hypothesis test | approved + implemented: `spec_pack_e_execution_and_family_context.md` | Codex | Validate pack E |
| `r4_s12_upper_passive_probe` | exploratory | validate-next | wave 1 | weak-medium | closes or rescues upper branch cheaply | approved + implemented: `spec_pack_f_low_priority_probes.md` | Codex | Validate pack F |
| `r4_s14_surface_sanity_filter` | exploratory | validate-next | wave 1 | medium | tiny pricing-support filter test | approved + implemented: `spec_pack_f_low_priority_probes.md` | Codex | Validate pack F |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- Wave 1 implementations exist under [`../bots/noel/canonical/`](../bots/noel/canonical/).
- Shared engine:
  [`../bots/noel/canonical/wave1_shared_engine.py`](../bots/noel/canonical/wave1_shared_engine.py)
- Canonical bot files:
  `r4_s01`, `r4_s02`, `r4_s03`, `r4_s04`, `r4_s05`, `r4_s06`, `r4_s07`,
  `r4_s08`, `r4_s09`, `r4_s10`, `r4_s11`, `r4_s12`, `r4_s13`, `r4_s14`,
  `r4_s15`

Example when active:

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | base | `../bots/<member>/canonical/candidate_01_short_name.py` | `04_strategy_specs/spec_candidate_01_short_name.md` | none | none | validating | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` |

## Baseline / Reference Bot

- None selected.

## Latest Results And Best Current Candidate

- Raw performance `.json` artifacts uploaded for Noel Wave 1 bots under
  `../performances/noel/historical/`.
- No canonical comparative summary yet.
- No best candidate yet.

Example when active:

| Candidate ID | Run Reference | Comparability | Decision | Notes |
| --- | --- | --- | --- | --- |
| `candidate_01` | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` | unclear | continue | non-authoritative evidence; caveats recorded in run summary |

- Best current candidate: `candidate_01`, pending final validation
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Need exact manual contract details from the platform or accepted source before
  manual-order analysis can start.
- Need deadline confirmation to assess fast-mode risk accurately.
- Human review is still pending for Phases `01`, `02`, `03`, and `05`.
- No material gap currently blocks `06 Testing/performance`, but canonical run
  summaries are still missing.

## Final Submission Status

- Candidate: none.
- File: none.
- Decision reason: none.
- Linked spec: none.
- Linked validation run: none.
- Comparability status: `unclear`
- Contract readiness status: `not checked`
- Active file verified: `no`
- Last validation: none.
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
- Phase 06 context updated: `phase_06_testing_context.md` on `2026-04-27`
- Data README updated: `../data/README.md` on `2026-04-26`
- Round README updated: `../README.md` on `2026-04-26`
