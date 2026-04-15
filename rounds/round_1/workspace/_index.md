# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Workflow correction needed:** Review debt exists for ingestion, EDA, understanding, and strategy. Also, the intended canonical bot file is missing:

`rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`

Next useful action: restore or create the canonical bot from the approved or deadline-deferred specs, then run platform validation and write a run summary.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | READY_FOR_REVIEW | Claude | Unassigned | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Awaiting human review |
| 02 Understanding | READY_FOR_REVIEW | Claude | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Awaiting human review |
| 03 Strategy | READY_FOR_REVIEW | Claude | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Awaiting shortlist approval |
| 04 Spec | COMPLETED | Claude | Bruno | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | BLOCKED | Claude | Bruno | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Canonical bot file missing |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Canonical bot required before platform run |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

Review outcomes in use: 04 Spec has deadline deferral recorded. Phases 00-03 are not reviewed and remain `READY_FOR_REVIEW`.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision / Caveat |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | yes | yes | likely | include; drift signal review pending |
| `ASH_COATED_OSMIUM` | yes | yes | likely | include; fixed-FV signal review pending |
| `DRYLAND_FLAX` | no historical bot data | wiki/manual only | no bot scope | manual auction only |
| `EMBER_MUSHROOM` | no historical bot data | wiki/manual only | no bot scope | manual auction only |

## Active Strategies

Maximum active strategies: 3.

| Candidate ID | Priority | Evidence Strength | Linked EDA Signals | Understanding Insight | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift` | high | strong | `01_eda/eda_round_1.md` — IPR drift fair value | drifting FV, not static price | IPR drifts +0.001/tick; FV = day_start + t×0.001 | deferred under deadline | Claude | Review debt before final submission |
| `candidate_02_aco_fixedfv` | high | strong | `01_eda/eda_round_1.md` — ACO fixed fair value | fixed FV with inventory skew | ACO mean-reverts to 10,000; fixed FV market maker | deferred under deadline | Claude | Review debt before final submission |
| `candidate_03_combined` | high | strong | linked signals from candidates 01 and 02 | combined independent trader | Candidates 01 + 02 in one submission bot | deferred under deadline | Claude | Restore/create bot, then run |

## Active Implementations

- None active. Intended implementation `candidate_03_combined` is blocked because `../bots/bruno/canonical/candidate_03_combined.py` is not present.

## Baseline / Reference Bot

- `bots/bruno/historical/TEST1_merged.py` — previous best, archived. Not active.

## Historical / Non-Decision Artifacts

- `bots/bruno/historical/TEST1_merged.py` — non-authoritative historical bot; not active.
- `performances/bruno/historical/114919.json` and `.log` — historical run evidence only. The log contains position-limit rejection events, so it must not be treated as a ready candidate.

## Latest Results And Best Current Candidate

- No canonical validation results.
- Best intended candidate: `candidate_03_combined`, blocked until the canonical bot file exists.

## Blockers And Decisions Needed

| Blocker | Phase | Action Required | Owner |
| --- | --- | --- | --- |
| Ingestion review pending | Ingestion (00) | Review `00_ingestion.md` and approve, approve with caveats, or request changes | Human |
| EDA review pending | EDA (01) | Review `01_eda/eda_round_1.md` and approve, approve with caveats, or request changes | Human |
| Understanding review pending | Understanding (02) | Review `02_understanding.md`; required before final submission readiness | Human |
| Strategy shortlist approval pending | Strategy (03) | Review `03_strategy_candidates.md`; required before final submission readiness | Human |
| Canonical bot missing | Implementation (05) | Restore or create `../bots/bruno/canonical/candidate_03_combined.py` from approved or deadline-deferred specs | Agent or Human |

## Final Submission Status

- Candidate: none selected. Intended candidate `candidate_03_combined` is blocked by missing bot file and missing validation.
- File: none verified. Expected file `../bots/bruno/canonical/candidate_03_combined.py` is missing.
- Decision reason: none.
- Linked spec: `spec_candidate_01_ipr_drift.md` + `spec_candidate_02_aco_fixedfv.md`
- Linked validation run: none yet
- Comparability status: `unclear`
- Contract readiness status: `blocked - bot file missing`
- Active file verified: `no`

## Recently Changed Artifacts

- Pre-created from template: `2026-04-14`
- `2026-04-15`: Ingestion, EDA, Understanding, Strategy candidates written.
- `2026-04-15`: Specs written (04 COMPLETED under deadline deferral). Implementation context later claimed a bot existed.
- `2026-04-16`: Robustness pass corrected review states, stale data blockers, historical artifact visibility, and missing canonical bot tracking.
