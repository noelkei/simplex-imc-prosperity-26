# Round Control Panel

## Round And Deadline

- Round: `round_2`
- Fact source: `../../../docs/prosperity_wiki/rounds/round_2.md`
- Raw source: `../../../docs/prosperity_wiki_raw/13_round_2.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Review phase 00 ingestion for Round 2 facts. If approved, start targeted EDA on Round 2 sample data, Market Access Fee value, and manual Research/Scale/Speed allocation scenarios.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Human review pending |
| 01 EDA | NOT_STARTED | Unassigned | Unassigned | [`01_eda/README.md`](01_eda/README.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Select targeted EDA question after ingestion review |
| 02 Understanding | NOT_STARTED | Unassigned | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | None recorded |
| 03 Strategy | NOT_STARTED | Unassigned | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | None recorded |
| 04 Spec | NOT_STARTED | Unassigned | Unassigned | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None recorded |
| 05 Implementation | NOT_STARTED | Unassigned | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Reviewed strategy spec required; `Trader.bid()` decision belongs in spec |
| 06 Testing/performance | NOT_STARTED | Unassigned | Unassigned | [`phase_06_testing_context.md`](phase_06_testing_context.md) | Bot candidate required |
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

- None.

## Active Implementations

Maximum active implementation candidates: 2.

- None.

## Baseline / Reference Bot

- None selected for Round 2.
- Round 1 final candidates may be useful implementation context after EDA, but they are not official rules and are not yet selected as Round 2 baselines.

## Latest Results And Best Current Candidate

- No results.
- No best candidate.
- Raw Round 2 sample data is present under `../data/raw/`.
- Decision-support script: [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py).
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Human review of phase 00 ingestion.
- Exact Round 2 deadline is unknown.
- Select first targeted EDA question.
- Decide a Market Access Fee bid only after estimating incremental extra-access value and choosing a risk posture.
- Decide manual Speed allocation under rank uncertainty.

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
- Added Round 2 raw source capture: `../../../docs/prosperity_wiki_raw/13_round_2.md`
- Added Round 2 curated wiki page: `../../../docs/prosperity_wiki/rounds/round_2.md`
- Updated ingestion: [`00_ingestion.md`](00_ingestion.md)
- Updated ingestion context: [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md)
- Updated EDA context: [`phase_01_eda_context.md`](phase_01_eda_context.md)
- Updated data README: [`../data/README.md`](../data/README.md)
- Added decision-support script: [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py)
