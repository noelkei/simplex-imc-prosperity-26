# Round Control Panel

## Round And Deadline

- Round: `round_1`
- Active round fact source: `../../../docs/prosperity_wiki/rounds/round_1.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

**Human action needed:** Upload `candidate_03_combined.py` to the Prosperity platform and run it. Compare P&L to baseline (9,419 from TEST1_merged).

Bot path: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`
Baseline: `rounds/round_1/bots/bruno/canonical/TEST1_merged.py` → P&L 9,419 (run 190076)

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Claude | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Awaiting human review |
| 01 EDA | READY_FOR_REVIEW | Claude | Unassigned | [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Awaiting human review |
| 02 Understanding | READY_FOR_REVIEW | Claude | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Awaiting human review |
| 03 Strategy | READY_FOR_REVIEW | Claude | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | IPR strategy corrected — needs review |
| 04 Spec | COMPLETED | Claude | Bruno | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | READY_FOR_REVIEW | Claude | Bruno | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Human platform run needed |
| 06 Testing/performance | IN_PROGRESS | Bruno | Claude | [`phase_06_testing_context.md`](phase_06_testing_context.md) | candidate_03_combined not yet run |
| 07 Debugging/iteration | NOT_STARTED | Unassigned | Unassigned | [`06_debugging/`](06_debugging/) / [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Run required |

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision / Caveat |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | yes | yes | yes | Buy-max-long confirmed by testing. EDA drift signal strong. |
| `ASH_COATED_OSMIUM` | yes | yes | yes | Fixed-FV market maker confirmed. FV=10,000 stable across 3 days. |
| `DRYLAND_FLAX` | no historical price CSV rows | wiki/manual only | no bot scope | Manual auction only. Bid ≤ 29. |
| `EMBER_MUSHROOM` | no historical price CSV rows | wiki/manual only | no bot scope | Manual auction only. Bid ≤ 19.80 (net of fee). |

## Active Strategies

Maximum active strategies: 3.

| Candidate ID | Priority | Evidence Strength | Short Reason | Spec Status | Owner | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_directional` | high | strong | IPR drifts +100/sim-day; hold max long captures full drift (~7,286+ in testing) | approved by testing | Claude | None — implemented in candidate_03_combined |
| `candidate_02_aco_fixedfv` | high | strong | ACO mean-reverts to 10,000; fixed-FV MM earns spread (~1,937 in testing) | approved | Claude | None — implemented in candidate_03_combined |
| `candidate_03_combined` | high | strong | IPR max-long + ACO fixed-FV MM in one bot | approved | Claude | Run on platform to beat baseline 9,419 |

## Active Implementations

| Candidate ID | Variant | Bot Path | Changed vs Baseline | Status | Latest Run |
| --- | --- | --- | --- | --- | --- |
| `candidate_03_combined` | v2 | `../bots/bruno/canonical/candidate_03_combined.py` | ACO_SKEW_FACTOR 2→3, no prints | awaiting run | none yet |

## Baseline / Reference Bot

- `bots/bruno/canonical/TEST1_merged.py` — validated P&L **9,419** (run 190076, 1 day, no violations)

## Historical / Non-Decision Artifacts

- `bots/bruno/historical/TEST1_merged.py` — archived.
- `performances/bruno/historical/114919.json/.log` — earlier run, P&L 9,223.
- `performances/bruno/canonical/190076.json/.log` — canonical baseline run, P&L 9,419.

## Latest Results And Best Current Candidate

- Baseline (TEST1_merged, run 190076): **P&L 9,419** — IPR pos +80 held all day, ACO pos +44 at end.
- Best candidate: `candidate_03_combined` v2 — same IPR, improved ACO skew. Pending run.

## Blockers And Decisions Needed

| Blocker | Phase | Action Required | Owner |
| --- | --- | --- | --- |
| candidate_03_combined not yet run | Testing (06) | Upload bot and run on platform; share results | Human |
| Strategy 03 IPR correction needs review | Strategy (03) | Review updated `03_strategy_candidates.md` (buy-max-long replaces drift-MM for IPR) | Human |

## Final Submission Status

- Candidate: `candidate_03_combined` v2 (pending validation)
- File: `../bots/bruno/canonical/candidate_03_combined.py`
- Decision reason: buy-max-long for IPR captures drift gain (~7,286); ACO fixed-FV MM captures spread (~1,937). Total baseline 9,419.
- Linked validation run: 190076 (baseline). candidate_03_combined run pending.
- Contract readiness status: `passed` (manual review)
- Active file verified: `yes`

## Recently Changed Artifacts

- `2026-04-14`: Pre-created from template.
- `2026-04-15`: Ingestion, EDA, Understanding, Strategy candidates written.
- `2026-04-15`: Specs written (04 COMPLETED under deadline deferral). Implementation context claimed bot existed.
- `2026-04-16`: Robustness pass. TEST1_merged validated (P&L 9,419, run 190076).
- `2026-04-16`: IPR strategy corrected: buy-max-long outperforms drift-tracking MM. candidate_03_combined v2 written (ACO_SKEW_FACTOR 2→3).
