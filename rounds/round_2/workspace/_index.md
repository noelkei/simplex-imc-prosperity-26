# Round Control Panel

## Round And Deadline

- Round: `round_2`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_2.md` (not present yet; keep NOT_STARTED)
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Phase 02 Understanding complete and READY_FOR_REVIEW. Next: Phase 03 (Strategy Candidates) — enumerate 3-5 candidate bots varying imbalance gain × Kalman tuning × quote sizing, MAF bid 2,000-2,500.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | COMPLETED | Bruno | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | None |
| 01 EDA | READY_FOR_REVIEW | Bruno | Unassigned | [`01_eda/eda_round_2.md`](01_eda/eda_round_2.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | None |
| 02 Understanding | READY_FOR_REVIEW | Bruno | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None |
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

- Pre-created from template: `2026-04-14`
- 2026-04-19: Phase 00 (Ingestion) marked COMPLETED — products, MAF, manual mechanics ingested.
- 2026-04-19: Phase 01 (EDA) marked READY_FOR_REVIEW — deep EDA with Kalman MLE, HMM, ARCH-LM, imbalance IC. Key findings: IPR +1000/day drift; imbalance IC=0.65; ACO Kalman Q=0.09, R=6.75.
- 2026-04-19: Phase 02 (Understanding) marked READY_FOR_REVIEW — synthesised per-product strategy axes; confirmed max-long IPR (~80k/day) vs market-making (~2k/day); identified imbalance gain + Kalman re-tuning as primary ACO optimisation axes; MAF bid 2,000-2,500.
