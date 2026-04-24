# Round Control Panel

## Round And Deadline

- Round: `round_3`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_3.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Phase 02 Understanding is `READY_FOR_REVIEW`. The next action is to review [`02_understanding.md`](02_understanding.md), then generate the default Phase 02b external paper research prompt before Phase 03 strategy generation.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Unassigned | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Unassigned | Unassigned | [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | NOT_STARTED | Unassigned | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | Prompt generation pending |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Understanding summary and default 02b prompt generation required, unless the user explicitly skips 02b |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Product Scope

- Algorithmic: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Manual only: Ornamental Bio-Pods (symbol not stated in the official round page)
- EDA shortlist for early strategy work: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Understanding-led branch split: separate `HYDROGEL_PACK`; use `VELVETFRUIT_EXTRACT` as both standalone delta-1 candidate and voucher anchor; treat `VEV_5000` to `VEV_5300` as first-wave option scope and `VEV_4000` / `VEV_4500` as second-wave structural-anchor scope
- EDA de-emphasis / exclusion: investigate `VEV_4500`, `VEV_5400`, `VEV_5500`; exclude `VEV_6000`, `VEV_6500` from first-wave bot logic unless later evidence changes

## External Paper Research Status

- Status: `not started`
- Expected folder: `../research/papers_raw/`
- Processed paper summaries: none
- Strategy dependency: the Understanding summary now exists; generate the 02b prompt by default, then proceed and consume processed papers incrementally when present; explicit user skip is also valid

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

- Phase 00 review is pending.
- Phase 01 review is pending.
- Phase 02 review is pending.
- Default Phase 02b prompt generation is pending.
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
- Pre-created from template: `2026-04-14`
