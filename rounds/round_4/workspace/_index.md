# Round Control Panel

## Round And Deadline

- Round: `round_4`
- Expected round fact source: [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Deadline: `UNKNOWN`
- Workflow mode: late-stage winner protection and final rerun mode

## Current Next Priority Action

Upload the final `10`-bot distilled pack and rerun in this order:
`r4_finalbatch_01`, `02`, `08`, `09`, `10`, then `03`, `04`, `05`, `06`,
`07`.

## Phase Status

| Phase | Status | Owner | Reviewer | Artifact | Blocker |
| --- | --- | --- | --- | --- | --- |
| 00 Ingestion | READY_FOR_REVIEW | Codex | Unassigned | [`00_ingestion.md`](00_ingestion.md) / [`phase_00_ingestion_context.md`](phase_00_ingestion_context.md) | Review pending |
| 01 EDA | READY_FOR_REVIEW | Codex | Unassigned | [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md) / [`phase_01_eda_context.md`](phase_01_eda_context.md) | Review pending |
| 02 Understanding | READY_FOR_REVIEW | Codex | Unassigned | [`02_understanding.md`](02_understanding.md) / [`phase_02_understanding_context.md`](phase_02_understanding_context.md) | Review pending |
| 02b External Paper Research | COMPLETED | Codex | Unassigned | [`02b_external_paper_research.md`](02b_external_paper_research.md) / [`phase_02b_external_paper_research_context.md`](phase_02b_external_paper_research_context.md) | Operationally complete |
| 03 Strategy | READY_FOR_REVIEW | Codex | Unassigned | [`03_strategy_candidates.md`](03_strategy_candidates.md) / [`phase_03_strategy_context.md`](phase_03_strategy_context.md) | Final reruns still pending |
| 04 Spec | COMPLETED | Codex | Human | [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md) / [`phase_04_spec_context.md`](phase_04_spec_context.md) | None |
| 05 Implementation | READY_FOR_REVIEW | Codex | Unassigned | [`phase_05_implementation_context.md`](phase_05_implementation_context.md) | Final reruns still pending |
| 06 Testing/performance | IN_PROGRESS | Codex | Unassigned | [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md) / [`phase_06_testing_context.md`](phase_06_testing_context.md) | Need fresh platform reruns on the final pack |
| 07 Debugging/iteration | IN_PROGRESS | Codex | Unassigned | [`phase_07_debugging_context.md`](phase_07_debugging_context.md) | Need live confirmation on the three new derivatives |

## Product Scope

- Algorithmic: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and
  `VEV_{4000,4500,5000,5100,5200,5300,5400,5500,6000,6500}`
- Manual-only: `AETHER_CRYSTAL`, 2 week vanilla options, 3 week vanilla
  options, chooser option, binary put option, knock-out put option
- Active final-wave focus:
  - winner family: `VEV_5300`, `VEV_5400`, `VEV_5500`
  - fallback family: `VEX + 5300`
  - veto-only information: `VEV_5200`, especially `Mark 22` activity

## External Paper Research Status

- Status: `operationally complete; local raw set fully processed`
- Local raw papers: `9`
- Processed top-level canonical summaries: `9`
- Final-wave role: inspiration and method reference only; no new paper-driven
  architecture is being opened now

## Active Strategy Candidate Queue

| Candidate ID | Role | Evidence Strength | Short Reason |
| --- | --- | --- | --- |
| `r4_finalbatch_01_full_otm_basket_champion` | primary | high | best real `round_4` PnL |
| `r4_finalbatch_02_5300_5400_basket` | backup | high | strongest two-strike variant |
| `r4_finalbatch_03_5300_vex_combo` | backup | medium-high | only positive `VEX` sidecar among top bots |
| `r4_finalbatch_04_5300_giveback_stop` | fallback | medium-high | proven simple retention control |
| `r4_finalbatch_05_5300_pure_max` | fallback | medium-high | clean single-strike benchmark |
| `r4_finalbatch_06_vex_5300_overlay_fallback` | fallback | medium | best positive Noel hybrid |
| `r4_finalbatch_07_5300_horizon_hold_fallback` | fallback | medium | positive slower-horizon fallback |
| `r4_finalbatch_08_full_otm_late_freeze` | challenger | medium | direct no-new-entry test |
| `r4_finalbatch_09_full_otm_mark22_veto` | challenger | medium | imports `5200 / Mark 22` veto logic |
| `r4_finalbatch_10_full_otm_giveback_stop` | challenger | medium | basket-level retention test |

## Active Implementation Queue

- Final bot folder:
  [`../bots/noel/canonical/`](../bots/noel/canonical/)
- Archived old live bots:
  [`../bots/bruno/historical/`](../bots/bruno/historical/),
  [`../bots/isaac/historical/`](../bots/isaac/historical/),
  [`../bots/noel/historical/`](../bots/noel/historical/)
- Archived old live performance artifacts:
  [`../performances/bruno/historical/`](../performances/bruno/historical/),
  [`../performances/noel/historical/`](../performances/noel/historical/)

## Baseline / Reference Bot

- [`../bots/noel/canonical/r4_finalbatch_01_full_otm_basket_champion.py`](../bots/noel/canonical/r4_finalbatch_01_full_otm_basket_champion.py)

## Historical / Non-Decision Artifacts

- All previously live `round_4` bots and current-run performance artifacts have
  been moved to `historical/`.
- The old Wave 2 queue is now evidence only and should not be treated as live
  implementation state.

## Latest Results And Best Current Candidate

- Best current candidate:
  `r4_final_05_full_otm_basket = 8729.104`
- Best current family:
  `5300 + 5400 + 5500`
- Best fallback band:
  positive `5300` controls around `5.2k-5.4k`
- Cross-round warning:
  old `round_3` `>10k` / `~18k` peaks were not retained and should not be
  reopened raw
- Primary synthesis:
  [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)

## Post-Run Research Memory

- [`post_run_research_memory.md`](post_run_research_memory.md)

## Blockers And Decisions Needed

- Need deadline confirmation to assess how many final rerun cycles remain.
- Need fresh platform reruns on the final `10`-bot pack.
- Need the final live ranking before selecting the active submission file.

## Final Submission Status

- Candidate: none yet
- File: none yet
- Decision reason: waiting on final rerun ranking
- Linked spec: [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md)
- Linked validation artifact: [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)
- Comparability status: `yes` for the proven family, `pending` for the three new challengers
- Contract readiness status: `passed local compile + smoke`
- Active file verified: `no`

## Recently Changed Artifacts

- Archived all old `round_4` canonical bots into member `historical/` folders on `2026-04-28`
- Archived all old current-round canonical performance artifacts into
  `historical/` on `2026-04-28`
- Rewrote strategy queue for the last wave:
  [`03_strategy_candidates.md`](03_strategy_candidates.md) on `2026-04-28`
- Added final pack spec:
  [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md) on `2026-04-28`
- Added full round performance synthesis:
  [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md) on `2026-04-28`
- Rewrote round post-run memory:
  [`post_run_research_memory.md`](post_run_research_memory.md) on `2026-04-28`
- Added final `10`-bot upload pack under
  [`../bots/noel/canonical/`](../bots/noel/canonical/) on `2026-04-28`
