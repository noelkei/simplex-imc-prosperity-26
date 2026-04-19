# Round Template Control Panel

## Round And Deadline

- Round: `ROUND_X`
- Active round fact source after copy: `../../../docs/prosperity_wiki/rounds/ROUND_X.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Start phase 00 ingestion after copying this template to `rounds/round_X/workspace/`.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | NOT_STARTED | Unassigned | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | None recorded |
| 01 EDA | NOT_STARTED | Unassigned | Unassigned | [`01_eda/README.md`](01_eda/README.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | None recorded |
| 02 Understanding | NOT_STARTED | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

Review outcomes: `not reviewed`, `approved`, `approved with caveats`, `changes requested`, or `deferred under deadline`.

Do not mark a phase `COMPLETED` while review is merely recommended, unassigned, or pending. Use `READY_FOR_REVIEW` until a review outcome is recorded.

## Product Scope

Track products as they move from ingestion and EDA into strategy and implementation.

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision / Caveat |
| --- | --- | --- | --- | --- |
| TBD | yes / no | yes / no / partial | likely / possible / no / unknown | include / defer / exclude / investigate |

## Active Strategies

Candidate count is ROI-driven, not fixed. Track all high-ROI active candidates
with roles, priority tiers, and implementation waves.

- None.

Example when active:

| Candidate ID | Role | Priority Tier | Implementation Wave | Evidence Strength | Linked EDA Signals | Understanding Insight | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | primary | spec-first | wave 1 | medium | `01_eda/eda_example.md#signal-hypotheses` | concise insight | concise rationale from understanding/EDA | not reviewed | Unassigned | Review spec |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity,
deadline risk, and distinct test axes.

- None.

Example when active:

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Insight Being Tested | Changed Axis | Expected Effect | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | base | `../bots/<member>/canonical/candidate_01_short_name.py` | `04_strategy_specs/spec_candidate_01_short_name.md` | none | linked understanding insight | none | expected effect from EDA/understanding | validating | `../performances/<member>/canonical/run_YYYYMMDD_HHMM_candidate_01.md` |

## Baseline / Reference Bot

- None selected.

## Historical / Non-Decision Artifacts

- None recorded.

Historical bots, raw logs, and superseded runs are non-authoritative. Mention them here only when they could be mistaken for active state.

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

- None recorded.

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

- Template copied: `DATE`
