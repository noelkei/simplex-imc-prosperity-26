# Round Control Panel

## Round And Deadline

- Round: `round_4`
- Expected round fact source: [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Open `03 Strategy` using the completed understanding package and the
non-blocking `02b` research prompt. Treat external paper research as optional
incremental input while Batch 1 papers move from `papers_md/` to
`papers_processed/`.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Codex | Unassigned | [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Codex | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | IN_PROGRESS | Codex | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | No material blocker; Batch 1 processed summaries pending |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
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

- Status: `prompt generated; shortlist refined; raw set normalized`
- Expected folder: `../research/papers_raw/`
- Raw papers detected: `9`
- Markdown conversions: `9 usable`
- Processed paper summaries: none
- Strategy dependency: none currently; proceed now and consume processed papers incrementally when present

## Active Strategies

Candidate count is ROI-driven, not fixed. Track all high-ROI active candidates
with roles, priority tiers, and implementation waves.

- None.

Example when active:

| Candidate ID | Role | Priority Tier | Implementation Wave | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | primary | spec-first | wave 1 | medium | concise rationale from understanding/EDA | not reviewed | Unassigned | Review spec |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- None.

Example when active:

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | base | `../bots/<member>/canonical/candidate_01_short_name.py` | `04_strategy_specs/spec_candidate_01_short_name.md` | none | none | validating | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` |

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

- Need exact manual contract details from the platform or accepted source before
  manual-order analysis can start.
- Need deadline confirmation to assess fast-mode risk accurately.
- Human review is still pending for Phases `01` and `02`, but no material gap
  currently blocks `03 Strategy`.

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
- External paper research prompt added: `02b_external_paper_research.md` on `2026-04-27`
- External paper research context updated: `phase_02b_external_paper_research_context.md` on `2026-04-27`
- External paper raw set normalized and ROI-filtered against `round_3` processed papers on `2026-04-27`
- All `papers_md` conversions for the current 9-paper raw set added under `../research/papers_md/` on `2026-04-27`
- Data README updated: `../data/README.md` on `2026-04-26`
- Round README updated: `../README.md` on `2026-04-26`
