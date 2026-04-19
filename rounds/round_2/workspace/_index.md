# Round Control Panel

## Round And Deadline

- Round: `round_2`
- Expected round fact source: `../../../docs/prosperity_wiki/rounds/round_2.md` (not present yet; keep NOT_STARTED)
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Phase 03 (Strategy) complete and READY_FOR_REVIEW. 10 bots implemented. Next: Phase 06 (Testing) — backtest all 10 against R2 CSV data and compare ACO P&L vs r2_b01_baseline to identify best candidate for submission.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | COMPLETED | Bruno | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | None |
| 01 EDA | READY_FOR_REVIEW | Bruno | Unassigned | [`01_eda/eda_round_2.md`](01_eda/eda_round_2.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | None |
| 02 Understanding | READY_FOR_REVIEW | Bruno | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None |
| 03 Strategy | READY_FOR_REVIEW | Bruno | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | COMPLETED | Bruno | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | None — all 10 bots implemented |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Active Strategies

Maximum active strategies: 3 (shortlisted; 10 total implemented).

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `r2_b03_imb6` | high | strong | gain=6 captures 88% of IC=0.647 signal; cleanest single-axis test | not reviewed | Bruno | Backtest vs b01 |
| `r2_b06_take_adj` | high | medium | positive-EV take threshold at FV+1 to +4 when imb>0.7 | not reviewed | Bruno | Backtest vs b02 |
| `r2_b09_full` | high | strong | all 4 axes combined; highest expected P&L | not reviewed | Bruno | Backtest vs b01; compare ACO P&L |

## Active Implementations

Maximum active implementation candidates: 2 (10 total implemented per user request).

| Candidate ID | Variant ID | Bot Path | Parent Spec | Parent Bot | Changed Axis | Status | Latest Run |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `r2_b01_baseline` | base | `../bots/bruno/canonical/r2_b01_baseline.py` | none | c_07 | +bid() | implemented | none |
| `r2_b02_imb4` | imb4 | `../bots/bruno/canonical/r2_b02_imb4.py` | none | b01 | imb_gain=4 | implemented | none |
| `r2_b03_imb6` | imb6 | `../bots/bruno/canonical/r2_b03_imb6.py` | none | b01 | imb_gain=6 | implemented | none |
| `r2_b04_kf_mle` | kf | `../bots/bruno/canonical/r2_b04_kf_mle.py` | none | b01 | R2 Kalman | implemented | none |
| `r2_b05_kf_imb4` | kf+imb4 | `../bots/bruno/canonical/r2_b05_kf_imb4.py` | none | b04 | gain=4 | implemented | none |
| `r2_b06_take_adj` | take | `../bots/bruno/canonical/r2_b06_take_adj.py` | none | b02 | imb take thr | implemented | none |
| `r2_b07_kf_take_adj` | kf+take | `../bots/bruno/canonical/r2_b07_kf_take_adj.py` | none | b07 | R2 Kalman | implemented | none |
| `r2_b08_size_adapt` | size | `../bots/bruno/canonical/r2_b08_size_adapt.py` | none | b06 | adaptive size | implemented | none |
| `r2_b09_full` | full | `../bots/bruno/canonical/r2_b09_full.py` | none | b07+b08 | all axes | implemented | none |
| `r2_b10_maf3000` | maf3k | `../bots/bruno/canonical/r2_b10_maf3000.py` | none | b09 | MAF=3000 | implemented | none |

## Baseline / Reference Bot

- `r2_b01_baseline` — R1 c_07 + bid()=2500. IPR P&L≈7,286; ACO P&L≈2,132 per run.

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
- 2026-04-19: Phase 03 (Strategy) marked READY_FOR_REVIEW — designed 10 differentiated bots across 4 axes (imb gain 2-6, Kalman R1 vs R2 MLE, imb-adjusted take threshold, adaptive sizing). Implemented all 10. Shortlist: b03 (imb6), b06 (take_adj), b09 (full). Phase 05 marked COMPLETED (all 10 bots written).
