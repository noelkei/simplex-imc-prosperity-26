# Round Control Panel

## Round And Deadline

- Round: `round_2`
- Fact source: `../../../docs/prosperity_wiki/rounds/round_2.md`
- Raw source: `../../../docs/prosperity_wiki_raw/13_round_2.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Tune or de-risk the new fee-aware Kalman variant using the initial comparison results, or commit the new artifacts on the current branch while keeping the existing hybrid as the better-performing sample-data candidate for now.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Human review pending |
| 01 EDA | NOT_STARTED | Unassigned | Unassigned | [`01_eda/README.md`](01_eda/README.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Select targeted EDA question after ingestion review |
| 02 Understanding | NOT_STARTED | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | IN_PROGRESS | Amin / OpenClaw | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Understanding artifact still sparse |
| 04 Spec | IN_PROGRESS | Amin / OpenClaw | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | Human review still needed; one spec deadline-deferred |
| 05 Implementation | IN_PROGRESS | Amin / OpenClaw | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Validation still needed before promotion |
| 06 Testing/performance | NOT_STARTED | Amin / OpenClaw | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Compare active candidates |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Issue/run required |

## Product Scope

Algorithmic products:

| Product | Symbol | Position Limit |
| --- | --- | ---: |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` | 80 |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` | 80 |

Round-specific algorithmic decision:

- Market Access Fee via `Trader.bid()` for final Round 2 only; accepted top-50% bids pay the bid and receive 25% more order-book quotes.

Manual decision:

- Allocate `50 000` XIRECs across Research, Scale, and Speed. Speed multiplier is rank-based across players.

## Active Strategies

Maximum active strategies: 3.

- `r2_amin_hybrid_01`: fixed-FV hybrid candidate already implemented.
- `r2_amin_feeaware_kalman_02`: new adaptive fee-aware Kalman candidate implemented.
- `r2_amin_feeaware_microprice_03`: new adaptive fee-aware microprice candidate implemented.

## Active Implementations

Maximum active implementation candidates: 2.

- `rounds/round_2/bots/amin/canonical/candidate_r2_amin_hybrid_01.py`
- `rounds/round_2/bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py`
- `rounds/round_2/bots/amin/canonical/candidate_r2_amin_feeaware_microprice_03.py`

## Baseline / Reference Bot

- None selected for Round 2.
- Round 1 final candidates may be useful implementation context after EDA, but they are not official rules and are not yet selected as Round 2 baselines.

## Latest Results And Best Current Candidate

- Lightweight local replay comparison now exists in `../performances/amin/canonical/candidate_comparison_2026-04-19.json`.
- In the latest tuned comparison, `r2_amin_feeaware_kalman_02` is nearly tied with `r2_amin_hybrid_01` on average and wins day 0, but still trails slightly overall in the lightweight replay harness.
- Follow-up fast replay work introduced `r2_amin_feeaware_microprice_03`, a sibling branch that shifts ACO toward microprice pressure while preserving the Kalman backbone; in the local stub it edges `_02` across the three sample days, but platform validation is still required.
- Best current candidate on available sample-data evidence: slight edge to `r2_amin_hybrid_01`, but the gap is now very small.
- Raw Round 2 sample data is present under `../data/raw/`.
- Decision-support script: [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py).
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Human review of phase 00 ingestion still pending formally.
- Exact Round 2 deadline is unknown.
- Need validation comparison between fixed-FV and fee-aware Kalman candidates.
- Market Access Fee bid remains a scenario decision; current Kalman candidate uses conservative placeholder `12`.
- Decide manual Speed allocation under rank uncertainty.

## Final Submission Status

- Candidate: `r2_amin_hybrid_01` is still slightly favored on current sample-data evidence, but no final submission decision is locked.
- File: `../bots/amin/canonical/candidate_r2_amin_hybrid_01.py`
- Decision reason: latest lightweight replay still gives the hybrid a tiny average edge, though the tuned fee-aware Kalman variant is now competitive.
- Linked spec: `04_strategy_specs/spec_candidate_r2_amin_hybrid_ipr_drift_aco_mm.md`, `04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md`
- Linked validation run: `../performances/amin/canonical/candidate_comparison_2026-04-19.json`
- Comparability status: `partial`
- Contract readiness status: `partial, compile checked and lightweight replay only`
- Active file verified: `no`
- Last validation: local syntax compile plus lightweight replay comparison.
- Active-file verification: not started.

## Recently Changed Artifacts

- Pre-created from template: `2026-04-14`
- Added Round 2 raw source capture: `../../../docs/prosperity_wiki_raw/13_round_2.md`
- Added Round 2 curated wiki page: `../../../docs/prosperity_wiki/rounds/round_2.md`
- Updated ingestion: [`00_ingestion.md`](00_ingestion.md)
- Updated ingestion context: [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md)
- Updated EDA context: [`phase_01_eda_context.md`](phase_01_eda_context.md)
- Updated data README: [`../data/README.md`](../data/README.md)
- Added decision-support script: [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py)
- Updated strategy candidates: [`03_strategy_candidates.md`](03_strategy_candidates.md)
- Added spec: [`04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md`](04_strategy_specs/spec_candidate_r2_amin_feeaware_kalman_02.md)
- Added bot: [`../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py`](../bots/amin/canonical/candidate_r2_amin_feeaware_kalman_02.py)
- Added comparison runner: [`01_eda/compare_candidates.py`](01_eda/compare_candidates.py)
- Added comparison results: [`../performances/amin/canonical/candidate_comparison_2026-04-19.json`](../performances/amin/canonical/candidate_comparison_2026-04-19.json)
