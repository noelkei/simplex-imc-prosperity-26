# Round Control Panel

## Round And Deadline

- Round: `round_2`
- Fact source: `../../../docs/prosperity_wiki/rounds/round_2.md`
- Raw source: `../../../docs/prosperity_wiki_raw/13_round_2.md`
- Deadline: `UNKNOWN`
- Workflow mode: standard until less than 24 hours remain, then fast mode

## Current Next Priority Action

Upload/test the 13 Bruno Generation 2 bots, collect platform JSON/logs, and
create Battery 02 run summaries.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | COMPLETED | Codex | Human | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Approved with caveats: deadline unknown |
| 01 EDA | COMPLETED | Codex | Human | [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Approved with caveats |
| 02 Understanding | COMPLETED | Codex | Human | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Approved with caveats |
| 03 Strategy | COMPLETED | Codex | Human | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Approved with caveats |
| 04 Spec | COMPLETED | Codex | Human | [`04_strategy_specs/`](04_strategy_specs/) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | Approved with caveats, including Gen2 compact spec |
| 05 Implementation | READY_FOR_REVIEW | Codex | Human | [`../bots/bruno/canonical/`](../bots/bruno/canonical/) / [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Gen2 implementation ready to test; human review optional before upload |
| 06 Testing/performance | COMPLETED | Codex | Human | [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md) / [`phase_06_testing_context.md`](phase_06_testing_context.md) | Battery 01 approved with caveats; Battery 02 not run |
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

Candidate count is ROI-driven, not fixed. Active candidates are managed by
role, priority tier, and implementation wave.

Battery 01 supersedes the initial testing queue for next work. The original
10 candidates remain documented, implemented, and summarized, but Generation 2
is now the active strategy queue.

| Candidate ID | Role | Priority Tier | Implementation Wave | Evidence Strength | Short Reason | Spec Status | Decision Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `R2-G2-01-IPR-EXTREME-RERUN-CHAMPION` | primary / robustness | spec-first | wave 1 | high | C02 nearly ties best raw PnL and isolates IPR extreme residual | approved / implemented | Upload/test |
| `R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV` | primary / robustness | spec-first | wave 1 | high | C07/C10 same active logic but different PnL; estimate subset variance | approved / implemented | Upload/test |
| `R2-G2-05-ACO-ACTIVATION-PROBE` | diagnostic | spec-first | wave 1 | high for implementation gap | ACO current bots produced zero PnL/position; first prove activation | approved / implemented | Upload/test |
| `R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE` | primary combined / diagnostic | spec-first | wave 1 | high | keep strong IPR base while testing corrected ACO activity | approved / implemented | Upload/test |
| `R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY` | primary / risk challenger | wave 2 | wave 2 | medium/high | reduce C02 final-inventory fragility | approved / implemented | Upload/test |
| `R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD` | secondary / alpha challenger | wave 2 | wave 2 | medium | EDA signal not truly tested because implementation gated off ACO | approved / implemented | Upload/test |
| `R2-G2-07-ACO-REVERSAL-WIDE-SPREAD` | secondary / process challenger | wave 2 | wave 2 | medium | retest ACO reversal after spread/activation fix | approved / implemented | Upload/test |
| `R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE` | primary combined / alpha | wave 2/3 | wave 2/3 | medium/high | likely true two-product champion path if ACO wakes up | approved / implemented | Upload/test |
| `R2-G2-10-SPREAD-OVERLAY-CONTINUOUS` | execution overlay | wave 3 | wave 3 | medium | replace harmful hard spread gate with continuous sizing | approved / implemented | Upload/test |
| `R2-G2-11-BRUNO-R1-KALMAN-R2-PORT` | Round 1 port / controlled side bet | side bet | wave 2 | medium | test Bruno mature ACO Kalman module under R2 wrapper | approved / implemented | Upload/test |
| `R2-G2-12-NOEL-R1-C26-R2-PORT` | Round 1 port / controlled side bet | side bet | wave 2 | medium | test Noel R1 one-sided/exit overlay under R2 wrapper | approved / implemented | Upload/test |
| `R2-G2-13-MAF-BID-SCENARIO` | mechanics-only | final mechanics | near final | medium | C10 did not test MAF because bid is zero | approved / implemented | Upload/test; do not final-submit without MAF review |

## Active Implementations

Implementation count is driven by reviewed specs, validation capacity, deadline
risk, and distinct test axes.

| Candidate ID | Bot Path | Parent Spec | Status | Latest Run |
| --- | --- | --- | --- | --- |
| `R2-G2-01` | [`../bots/bruno/canonical/candidate_r2_g2_01_ipr_extreme_rerun_champion.py`](../bots/bruno/canonical/candidate_r2_g2_01_ipr_extreme_rerun_champion.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-02` | [`../bots/bruno/canonical/candidate_r2_g2_02_ipr_drift_rerun_code_equiv.py`](../bots/bruno/canonical/candidate_r2_g2_02_ipr_drift_rerun_code_equiv.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-03` | [`../bots/bruno/canonical/candidate_r2_g2_03_ipr_extreme_flatter_inventory.py`](../bots/bruno/canonical/candidate_r2_g2_03_ipr_extreme_flatter_inventory.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-04` | [`../bots/bruno/canonical/candidate_r2_g2_04_ipr_spread_retune.py`](../bots/bruno/canonical/candidate_r2_g2_04_ipr_spread_retune.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-05` | [`../bots/bruno/canonical/candidate_r2_g2_05_aco_activation_probe.py`](../bots/bruno/canonical/candidate_r2_g2_05_aco_activation_probe.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-06` | [`../bots/bruno/canonical/candidate_r2_g2_06_aco_imbalance_wide_spread.py`](../bots/bruno/canonical/candidate_r2_g2_06_aco_imbalance_wide_spread.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-07` | [`../bots/bruno/canonical/candidate_r2_g2_07_aco_reversal_wide_spread.py`](../bots/bruno/canonical/candidate_r2_g2_07_aco_reversal_wide_spread.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-08` | [`../bots/bruno/canonical/candidate_r2_g2_08_combined_ipr_extreme_aco_probe.py`](../bots/bruno/canonical/candidate_r2_g2_08_combined_ipr_extreme_aco_probe.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-09` | [`../bots/bruno/canonical/candidate_r2_g2_09_combined_ipr_extreme_aco_imbalance.py`](../bots/bruno/canonical/candidate_r2_g2_09_combined_ipr_extreme_aco_imbalance.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-10` | [`../bots/bruno/canonical/candidate_r2_g2_10_spread_overlay_continuous.py`](../bots/bruno/canonical/candidate_r2_g2_10_spread_overlay_continuous.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-11` | [`../bots/bruno/canonical/candidate_r2_g2_11_bruno_r1_kalman_r2_port.py`](../bots/bruno/canonical/candidate_r2_g2_11_bruno_r1_kalman_r2_port.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-12` | [`../bots/bruno/canonical/candidate_r2_g2_12_noel_r1_c26_r2_port.py`](../bots/bruno/canonical/candidate_r2_g2_12_noel_r1_c26_r2_port.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready | none |
| `R2-G2-13` | [`../bots/bruno/canonical/candidate_r2_g2_13_maf_bid_scenario.py`](../bots/bruno/canonical/candidate_r2_g2_13_maf_bid_scenario.py) | [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md) | implemented / upload-ready; `bid() == 75` | none |

## Baseline / Reference Bot

- Diagnostic no-trade state logger used for log collection: [`../bots/noel/historical/baseline_state_logger.py`](../bots/noel/historical/baseline_state_logger.py).
- Purpose: upload once to Prosperity to collect `TradingState` logs for EDA; not an alpha candidate and not a final submission candidate.
- Round 1 final candidates may be useful implementation context after EDA, but they are not official rules and are not yet selected as Round 2 baselines.

## Latest Results And Best Current Candidate

- Battery 01 platform analysis is ready for review:
  [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md).
- Best raw single-run PnL: `R2-CAND-10` at `2659.906`, but champion status is
  provisional because `bid()` is `0`, C07/C10 are active-logic equivalent, and
  Round 2 platform testing randomizes the 80% quote subset.
- Near-tie primary challenger: `R2-CAND-02` at `2656.625`, with cleaner IPR
  residual-extreme attribution.
- Product attribution: all nonzero Battery 01 PnL came from
  `INTARIAN_PEPPER_ROOT`; `ASH_COATED_OSMIUM` PnL and final position were `0`
  in every run.
- Main post-run lesson: current ACO modules were over-throttled by hard spread
  gates and need activation/spec repair before judging ACO alpha.
- C08 had two trials (`1669.594` and `837.500`), confirming material
  platform-test variance.
- Run summaries are under [`../performances/noel/canonical/`](../performances/noel/canonical/).
- Post-run memory is now active:
  [`post_run_research_memory.md`](post_run_research_memory.md).
- Bruno Gen2 13-bot upload queue is implemented under
  [`../bots/bruno/canonical/`](../bots/bruno/canonical/).
- Bruno Gen2 implementation spec:
  [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md).
- Gen2 readiness checks passed: `py_compile` for all 13 and
  `GEN2_SMOKE_OK 13 bots`.
- Raw Round 2 sample data is present under `../data/raw/`.
- Diagnostic platform result is saved at [`../performances/noel/historical/baseline_state_logger.json`](../performances/noel/historical/baseline_state_logger.json); it is no-trade quote evidence, not alpha evidence.
- Consolidated EDA report for Understanding handoff: [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md).
- Consolidated EDA artifacts: [`01_eda/artifacts/`](01_eda/artifacts/), including multivariate/process tables and plots.
- Promoted EDA signals: IPR drift plus residual, ACO short-horizon mean reversion, top imbalance.
- Promoted execution/risk filter candidate: spread regime.
- Exploratory EDA signals: microprice deviation, full-book imbalance as backup/context, liquidity/depth regime.
- Negative evidence: cross-product lead-lag is too weak for first-pass strategy; PCA/clustering/latent components are EDA-only calibration, not bot logic.
- Not ready: trade pressure proxy needs better platform `market_trades` logs.
- Decision-support script: [`01_eda/round_2_decision_tools.py`](01_eda/round_2_decision_tools.py).
- Fresh EDA script: [`01_eda/eda_round2_fresh.py`](01_eda/eda_round2_fresh.py).
- Consolidated EDA script: [`01_eda/eda_round2_consolidated.py`](01_eda/eda_round2_consolidated.py).
- Understanding summary approved with caveats: [`02_understanding.md`](02_understanding.md).
- Understanding carries algorithmic Signal Ledger, MAF mechanics/risk evidence, manual-only RSS scenarios, multivariate/process evidence, and negative evidence for strategy.
- Initial strategy candidate queue: [`03_strategy_candidates.md`](03_strategy_candidates.md).
- Phase 03 retained 10 ROI-relevant Battery 01 candidates; the active next
  queue is now Generation 2 from the Phase 06 analysis.
- Phase 04 specs approved with caveats under [`04_strategy_specs/`](04_strategy_specs/).
- Implemented and validated 10 Noel canonical Round 2 bots under
  [`../bots/noel/canonical/`](../bots/noel/canonical/); active next queue is
  Generation 2, not another rerun of the same unchanged ACO bots.
- Implemented 13 Bruno Generation 2 bots under
  [`../bots/bruno/canonical/`](../bots/bruno/canonical/); all need Battery 02
  platform validation.
- Implementation smoke checks passed: `py_compile` and minimal fake-state
  `SMOKE_OK 10 bots`.
- Pre-kickoff EDA outputs are archived as historical/unreviewed under [`01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/`](01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/).
- Interpretation limit: results are non-authoritative evidence, not rules

## Blockers And Decisions Needed

- Exact Round 2 deadline is unknown.
- Upload/test the 13 Bruno Gen2 bots and save platform JSON/logs.
- Do not choose final champion from one PnL point; rerun close IPR-family
  candidates if time allows.
- Current ACO implementations should not be reused unchanged; ACO needs an
  activation/spread-gate fix first.
- Decide a Market Access Fee bid only after estimating incremental extra-access value and choosing a risk posture.
- Decide manual Speed allocation under rank uncertainty.
- Platform JSONs did not include separate stdout logs or persisted `R2_BOT_LOG`
  lines; future own-trade/fill diagnostics may need a different capture path.

## Final Submission Status

- Candidate: none.
- File: none.
- Decision reason: none.
- Linked spec: none.
- Linked validation run: [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md)
- Comparability status: `unclear` due randomized 80% testing quote subset.
- Contract readiness status: `passed smoke / validation caveats`
- Active file verified: `no`
- Last validation: Battery 01 platform JSON analysis, `2026-04-19`.
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
- Completed ingestion with human approval/caveats: `2026-04-19`
- Archived pre-kickoff EDA outputs: [`01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/`](01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/)
- Added Round 1 to Round 2 pre-EDA note: [`round_1_to_round_2_pre_eda_note.md`](round_1_to_round_2_pre_eda_note.md)
- Added diagnostic no-trade state logger: [`../bots/noel/historical/baseline_state_logger.py`](../bots/noel/historical/baseline_state_logger.py)
- Added no-trade platform artifact: [`../performances/noel/historical/baseline_state_logger.json`](../performances/noel/historical/baseline_state_logger.json)
- Added fresh EDA script: [`01_eda/eda_round2_fresh.py`](01_eda/eda_round2_fresh.py)
- Added fresh EDA report: [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md)
- Added fresh EDA artifacts: [`01_eda/artifacts/`](01_eda/artifacts/)
- Added consolidated multivariate/process EDA script: [`01_eda/eda_round2_consolidated.py`](01_eda/eda_round2_consolidated.py)
- Rewrote canonical EDA handoff as a single consolidated report with multivariate/process evidence: [`01_eda/eda_round2_fresh.md`](01_eda/eda_round2_fresh.md)
- Completed EDA with review outcome approved with caveats: [`phase_01_eda_context.md`](phase_01_eda_context.md)
- Added Round 2 understanding summary: [`02_understanding.md`](02_understanding.md)
- Updated understanding context: [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- Completed Understanding with review outcome approved with caveats: [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- Added ROI-driven Round 2 strategy candidate queue: [`03_strategy_candidates.md`](03_strategy_candidates.md)
- Updated strategy context: [`phase_03_strategy_context.md`](phase_03_strategy_context.md)
- Completed Strategy with review outcome approved with caveats: [`phase_03_strategy_context.md`](phase_03_strategy_context.md)
- Added Phase 04 specs for all 10 Round 2 candidates: [`04_strategy_specs/`](04_strategy_specs/)
- Updated spec context: [`phase_04_spec_context.md`](phase_04_spec_context.md)
- Completed specs with review outcome approved with caveats: [`phase_04_spec_context.md`](phase_04_spec_context.md)
- Implemented 10 canonical Noel Round 2 bots: [`../bots/noel/canonical/`](../bots/noel/canonical/)
- Updated implementation context: [`phase_05_implementation_context.md`](phase_05_implementation_context.md)
- Updated testing context for the 10-bot validation queue: [`phase_06_testing_context.md`](phase_06_testing_context.md)
- Copied Round 2 candidate bot files into canonical path after detecting path
  drift: [`../bots/noel/canonical/`](../bots/noel/canonical/)
- Added Battery 01 analysis script:
  [`06_testing/analyze_battery_01.py`](06_testing/analyze_battery_01.py)
- Added Battery 01 post-run report:
  [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md)
- Added Battery 01 artifacts: [`06_testing/artifacts/`](06_testing/artifacts/)
- Added 11 canonical run summaries:
  [`../performances/noel/canonical/`](../performances/noel/canonical/)
- Added post-run research memory:
  [`post_run_research_memory.md`](post_run_research_memory.md)
- Added compact Gen2 Bruno spec:
  [`04_strategy_specs/spec_r2_gen2_bruno_battery.md`](04_strategy_specs/spec_r2_gen2_bruno_battery.md)
- Added Bruno Gen2 bot generator:
  [`05_implementation/generate_bruno_gen2_bots.py`](05_implementation/generate_bruno_gen2_bots.py)
- Added 13 Bruno canonical Gen2 bots:
  [`../bots/bruno/canonical/`](../bots/bruno/canonical/)
- Updated Phase 04/05/06 contexts for Gen2 implementation and Battery 02 next
  testing action.
