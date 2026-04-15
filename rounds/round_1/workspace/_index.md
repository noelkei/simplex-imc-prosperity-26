# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Human action needed:** Commit raw price/order-book data files to `rounds/round_1/data/raw/` so EDA can begin. Once data lands, start phase 01 EDA targeting: (1) `INTARIAN_PEPPER_ROOT` fair value stability; (2) `ASH_COATED_OSMIUM` pattern/periodicity test.
 
Phase 00 ingestion artifact is `READY_FOR_REVIEW` — human sign-off needed before marking `COMPLETED`.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- || 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | BLOCKED | Unassigned | Unassigned | [`01_eda/README.md`](01_eda/README.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | No data in `rounds/round_1/data/raw/` |
| 02 Understanding | NOT_STARTED | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategies: 3.

- None.

Example when active:

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate_01` | high | medium | concise rationale from understanding/EDA | not reviewed | Unassigned | Review spec |

## Active Implementations

Maximum active implementation candidates: 2.

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

| Blocker | Phase | Action Required | Owner |
| --- | --- | --- | --- |
| No raw data in `rounds/round_1/data/raw/` | EDA (01) | Commit price/order-book log files from the platform | Human |
| Ingestion review pending | Ingestion (00) | Review `00_ingestion.md` and mark COMPLETED or add corrections | Human |

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

- Pre-created from template: `2026-04-14`
- `2026-04-15`: Phase 00 ingestion written and marked `READY_FOR_REVIEW`. EDA marked `BLOCKED` (no data). Blockers table added.
