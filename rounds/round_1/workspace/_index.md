# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Human decision needed:** Review `03_strategy_candidates.md` and approve the shortlist:
- `candidate_01_ipr_drift` — IPR drift market maker (FV = day_start + t×0.001)
- `candidate_02_aco_fixedfv` — ACO fixed-FV market maker (FV = 10,000)
- `candidate_03_combined` — both strategies combined into one submission bot

Once approved, agent will immediately write strategy specs for candidates 01 and 02, then implement the combined bot.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | COMPLETED | Claude | Unassigned | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | None |
| 02 Understanding | READY_FOR_REVIEW | Claude | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Awaiting human review |
| 03 Strategy | READY_FOR_REVIEW | Claude | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Awaiting shortlist approval |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | Shortlist approval required |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategies: 3.

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift` | high | strong | IPR drifts +0.001/tick; FV = day_start + t×0.001; market-make inside bot spread | not reviewed | Claude | Approve shortlist |
| `candidate_02_aco_fixedfv` | high | strong | ACO mean-reverts to 10,000; FV fixed; market-make inside 16-tick bot spread | not reviewed | Claude | Approve shortlist |
| `candidate_03_combined` | high | strong | Candidates 01 + 02 in one submission bot | not reviewed | Claude | Approve shortlist |

## Active Implementations

Maximum active implementation candidates: 2.

- None.

## Baseline / Reference Bot

- None selected.

## Latest Results And Best Current Candidate

- No results.
- No best candidate.

## Blockers And Decisions Needed

| Blocker | Phase | Action Required | Owner |
| --- | --- | --- | --- |
| Shortlist approval pending | Strategy (03) | Review `03_strategy_candidates.md` and approve candidates 01, 02, 03 | Human |
| Understanding review pending | Understanding (02) | Review `02_understanding.md` and confirm or correct | Human |

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

## Recently Changed Artifacts

- Pre-created from template: `2026-04-14`
- `2026-04-15`: Phase 00 ingestion written (`READY_FOR_REVIEW`). EDA blocked on missing data.
- `2026-04-15`: Data uploaded. EDA completed (`COMPLETED`). Provisional strategy framing added.
- `2026-04-15`: Phase 02 Understanding written (`READY_FOR_REVIEW`). Phase 03 Strategy candidates written (`READY_FOR_REVIEW`). Active strategies table populated.

