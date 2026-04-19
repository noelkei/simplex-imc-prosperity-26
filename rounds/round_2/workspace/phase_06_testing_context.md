# Phase 06 - Testing And Performance Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human
- Review outcome: approved with caveats by user direction to proceed with Gen2

## Last Updated

2026-04-19

## What Has Been Done

- Phase 05 created 10 canonical Noel Round 2 bots.
- User provided 11 Round 2 platform JSON artifacts for Battery 01:
  - the 10 candidate bots;
  - a second trial for `R2-CAND-08`.
- Parsed platform `profit`, `activitiesLog`, `graphLog`, and final `positions`
  with `.venv`.
- Generated aggregate analysis, CSV/PNG artifacts, 11 canonical run summaries,
  and `post_run_research_memory.md`.
- Battery 01 analysis was accepted for next-iteration planning.
- Gen2 Bruno implementation is now ready and needs a new testing pass.

## Current Findings

- All 11 candidate JSON artifacts finished with status `FINISHED`.
- Best raw single-run PnL is `R2-CAND-10` at `2659.906`, but it is only a
  provisional champion because `bid()` is `0`, C07/C10 are active-logic
  equivalent, and testing quote subsets are randomized.
- `R2-CAND-02` is effectively tied at `2656.625` and cleanly isolates the IPR
  residual-extreme hypothesis.
- All nonzero PnL in Battery 01 is attributed to `INTARIAN_PEPPER_ROOT`.
- `ASH_COATED_OSMIUM` has `0` PnL and `0` final position in every run; current
  ACO implementations should be rejected/revised, not interpreted as final
  negative evidence against ACO EDA signals.
- Post-run spread diagnostics show the current hard spread gates are too tight
  for ACO and likely over-throttle execution.
- C08 trial 1 vs trial 2 and C07/C10 code-equivalent PnL differences confirm
  material platform-test randomness.

## Decisions Made

- Final submission requires a readable validation or performance summary.
- Logs should be converted into `.md` and/or `.json` summaries for durable tracking.
- Battery 01 produces a Generation 2 queue focused on IPR robustness, ACO
  activation fixes, two controlled Round 1 ports, and MAF as a separate
  mechanics decision.

## Open Questions / Blockers

- Battery 01 analysis is approved with caveats for iteration planning.
- No separate `.log` files or persisted `R2_BOT_LOG` stdout were found; the
  available evidence is platform JSON only.
- Exact own-trade fills, rejections, and pathwise positions are unavailable.
- Final MAF bid remains untested because current `bid()` is `0` and platform
  testing ignores bid acceptance.
- Gen2 Battery 02 platform results are not collected yet.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`docs/templates/run_summary_template.md`](../../../docs/templates/run_summary_template.md)
- [`06_testing/round2_battery_01_analysis.md`](06_testing/round2_battery_01_analysis.md)
- [`06_testing/artifacts/`](06_testing/artifacts/)
- [`../performances/noel/canonical/`](../performances/noel/canonical/)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`../bots/bruno/canonical/`](../bots/bruno/canonical/)

## Next Priority Action

Upload/test the 13 Bruno Gen2 bots, collect platform JSON/logs, and create
Battery 02 run summaries.

## Deadline Risk

Unknown.
