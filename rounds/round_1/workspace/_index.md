# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Human review needed:** Read `01_eda/eda_round_1.md` and confirm the two key EDA findings:
1. `INTARIAN_PEPPER_ROOT` drifts linearly at +0.001/tick (NOT stable — overrides wiki "quite steady" description).
2. `ASH_COATED_OSMIUM` mean-reverts tightly around fair value 10,000 (stdev ~5, slow AR(1) reversion).

Once confirmed, agent will write phase 02 Understanding and phase 03 Strategy candidates immediately.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | COMPLETED | Claude | Unassigned | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Human review recommended |
| 02 Understanding | NOT_STARTED | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategies: 3.

- None yet — awaiting EDA review and Understanding phase.

Provisional framing (not yet formal candidates):

| Product | Direction | Basis |
| --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | Drift-tracking market maker | Linear drift confirmed by EDA; fair value = `day_start + t*0.001` |
| `ASH_COATED_OSMIUM` | Fixed-FV market maker | Mean-reverts to 10,000; slow AR(1); tight dispersion |

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
| EDA review pending | EDA (01) | Review `01_eda/eda_round_1.md` and confirm or correct findings | Human |
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

## Recently Changed Artifacts

- Pre-created from template: `2026-04-14`
- `2026-04-15`: Phase 00 ingestion written and marked `READY_FOR_REVIEW`. EDA marked `BLOCKED` (no data). Blockers table added.
- `2026-04-15`: Data uploaded (6 CSV files). EDA completed. Phase 01 marked `COMPLETED`. Provisional strategy framing added.

