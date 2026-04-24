# Round Control Panel

## Round And Deadline

- Round: `round_3`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_3.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Two bots implemented under `bots/amin/canonical/`. Next: run both on the platform and compare performance to select the submission candidate.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Unassigned | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Unassigned | Unassigned | [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Unassigned | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | None |
| 03 Strategy | READY_FOR_REVIEW | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Human checkpoint on composite-first vs voucher-first |
| 04 Spec | READY_FOR_REVIEW | amin | Unassigned | [`04_strategy_specs/spec_c06_composite_base.md`](04_strategy_specs/spec_c06_composite_base.md), [`04_strategy_specs/spec_c06_composite_inv.md`](04_strategy_specs/spec_c06_composite_inv.md) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | Deferred under deadline |
| 05 Implementation | IN_PROGRESS | amin | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Platform validation needed |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Product Scope

- Algorithmic: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Manual only: Ornamental Bio-Pods (symbol not stated in the official round page)
- EDA shortlist for early strategy work: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Understanding-led branch split: separate `HYDROGEL_PACK`; use `VELVETFRUIT_EXTRACT` as both standalone delta-1 candidate and voucher anchor; treat `VEV_5000` to `VEV_5300` as first-wave option scope and `VEV_4000` / `VEV_4500` as second-wave structural-anchor scope
- EDA de-emphasis / exclusion: investigate `VEV_4500`, `VEV_5400`, `VEV_5500`; exclude `VEV_6000`, `VEV_6500` from first-wave bot logic unless later evidence changes

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
| `C06` | primary | spec-first | wave 1 | strong | Full-scope composite Trader (C01+C02+C03); aggregate PnL across all products | not reviewed | Unassigned | Write spec |
| `C03` | primary | spec-first | wave 1 | strong | Bachelier residual reversion for VEV_5000-5300; strongest individual voucher candidate | not reviewed | Unassigned | Write spec (component of C06) |
| `C01` | secondary | implement-first | wave 1 | medium | Hydrogel microstructure MM; independent PnL stream | not reviewed | Unassigned | Write spec (component of C06) |
| `C02` | secondary | implement-first | wave 1 | medium/high | VEX delta-1 MM + voucher anchor; dual role | not reviewed | Unassigned | Write spec (component of C06) |
| `C04` | secondary | validate-next | wave 1 | medium/high | Bachelier residual + inventory skew variant of C03 | not reviewed | Unassigned | Write spec after C03 validates |
| `C07` | exploratory | validate-next | wave 1 | medium | TTE-5d cautious residual reversion variant of C03 | not reviewed | Unassigned | Write spec as parameter variant |
| `C05` | exploratory | backlog | wave 2 | medium/high | ITM structural-anchor residual reversion for VEV_4000/4500 | not reviewed | Unassigned | Defer spec |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `C06` | base | `../bots/amin/canonical/candidate_c06_composite_base.py` | `04_strategy_specs/spec_c06_composite_base.md` | none | none | implemented | none |
| `C06-inv` | inventory | `../bots/amin/canonical/candidate_c06_composite_inv.py` | `04_strategy_specs/spec_c06_composite_inv.md` | C06 base | inventory skew + imbalance confirm + TTE-cautious | implemented | none |

## Baseline / Reference Bot

- None selected.

## Latest Results And Best Current Candidate

- No results.
- No best candidate.

Example when active:

| Candidate ID | Run Reference | Comparability | Decision | Notes |
| --- | --- | --- | --- | --- |
| `candidate_01` | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` | unclear | continue | non-authoritative evidence; caveats recorded in run summary |

- Best current candidate: `candidate_01`, pending final validation
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Phase 00 review is pending.
- Phase 01 review is pending.
- Phase 02 review is pending.
- Exact round-end timestamp is still unknown.

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
- Pre-created from template: `2026-04-14`
