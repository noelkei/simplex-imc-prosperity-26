# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Human action needed:** Upload `candidate_03_combined.py` to the Prosperity platform simulator and run it. Share the results (P&L, position trace) so the agent can write a run summary and identify issues.

Bot path: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | COMPLETED | Claude | Unassigned | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | None |
| 02 Understanding | READY_FOR_REVIEW | Claude | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Awaiting human review |
| 03 Strategy | READY_FOR_REVIEW | Claude | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Awaiting shortlist approval |
| 04 Spec | COMPLETED | Claude | Bruno | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | READY_FOR_REVIEW | Claude | Bruno | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Human testing needed |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot run on platform required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategies: 3.

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift` | high | strong | IPR drifts +0.001/tick; FV = day_start + t×0.001 | approved | Claude | None — implemented |
| `candidate_02_aco_fixedfv` | high | strong | ACO mean-reverts to 10,000; fixed FV market maker | approved | Claude | None — implemented |
| `candidate_03_combined` | high | strong | Candidates 01 + 02 in one submission bot | approved | Claude | Run on platform |

## Active Implementations

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_03_combined` | base | `../bots/bruno/canonical/candidate_03_combined.py` | `spec_candidate_01_ipr_drift.md` + `spec_candidate_02_aco_fixedfv.md` | `bots/bruno/historical/TEST1_merged.py` | IPR replaced; ACO refined | awaiting first run | none yet |

## Baseline / Reference Bot

- `bots/bruno/historical/TEST1_merged.py` — previous best, archived. Not active.

## Latest Results And Best Current Candidate

- No results yet.
- Best current candidate: `candidate_03_combined` — pending first platform run.

## Blockers And Decisions Needed

| Blocker | Phase | Action Required | Owner |
| --- | --- | --- | --- |
| Bot not yet run on platform | Testing (06) | Upload bot, run simulator, share P&L + position trace | Human |

## Final Submission Status

- Candidate: `candidate_03_combined` (pending validation)
- File: `../bots/bruno/canonical/candidate_03_combined.py`
- Decision reason: only validated candidate; built on strong EDA evidence
- Linked spec: `spec_candidate_01_ipr_drift.md` + `spec_candidate_02_aco_fixedfv.md`
- Linked validation run: none yet
- Comparability status: `unclear`
- Contract readiness status: `passed` (manual review)
- Active file verified: `no`

## Recently Changed Artifacts

- Pre-created from template: `2026-04-14`
- `2026-04-15`: Ingestion, EDA, Understanding, Strategy candidates written.
- `2026-04-15`: Specs written (04 COMPLETED). Bot implemented (05 READY_FOR_REVIEW).
