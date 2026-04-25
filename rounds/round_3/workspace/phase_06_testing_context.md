# Phase 06 - Testing And Performance Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: amin
- Reviewer: Unassigned

## Last Updated

2026-04-25

## What Has Been Done

- Parsed the 11 historical Round 3 platform JSON artifacts under `../performances/amin/historical/`.
- Created `06_testing/round_3_historical_performance_analysis.md`.
- Parsed the first corrected challenger trio: logger, centered base, and inventory variant.
- Created `06_testing/round_3_canonical_run_analysis.md`.
- Parsed the full 25-bot Wave 1 learner batch after the user uploaded all paired platform artifacts.
- Created `06_testing/round_3_full_performance_synthesis.md` plus CSV artifacts under `06_testing/artifacts/full_synthesis/`.
- Confirmed that the tested Wave 1 bots and their raw artifacts now live under `historical/`.

## Current Findings

- Across all 39 current JSON artifacts, the strongest live family is now clean isolated delta-1 microstructure, not broad voucher composites.
- Pure ITM learners are near-flat on the live `TTE=5d` day; historical ITM/VEX winners appear to be mostly VEX-driven.
- No pure voucher-only Wave 1 learner finished positive.
- `VEV_5100` and `VEV_5200` are the clearest toxic active strikes.
- `VEV_5000` is weak, `VEV_5300` is the least-bad active strike, and inventory control helps only on the cleaner `5000 + 5300` subset.
- Directional upper-strike residual learners are negative; passive upper quoting currently produces zero fills.
- Surface-pair learners are negative, with `L26` pointing to realized adverse selection rather than just terminal inventory mark.
- New path analysis shows that many negative-final runs are not equivalent: `20/39` runs peaked above `+100` and still finished negative, and `17/39` peaked above `+500` before reversing.
- The active-voucher family often looks like `edge then reversal`, while the current surface family looks more like `no edge / wrong implementation` from the start.

## Decisions Made

- `activitiesLog` final per-product rows remain the best practical PnL proxy when JSON `profit` is unavailable.
- Timestamp-level `activitiesLog` paths are now the preferred source for intra-run quality analysis; `graphLog` should stay as a secondary audit path only.
- The Wave 1 batch should be treated as completed validation evidence, not as a pending run queue.
- The redesign/spec step is now complete: the full 19-bot Wave 2 batch has been implemented and is ready for platform validation.

## Open Questions / Blockers

- Need the first Wave 2 runs to decide whether the next champion family should be delta-1-first or delta-1 plus a selective voucher overlay.
- Need the first Wave 2 runs to decide whether ITM stays as an add-on only.
- Need the first Wave 2 runs to decide whether faster profit capture / unwind really rescues the surviving active-voucher subset.
- Need the first Wave 2 runs to decide whether the upper and floor coverage bots close those families or justify keeping them alive.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_testing/round_3_historical_performance_analysis.md`](06_testing/round_3_historical_performance_analysis.md)
- [`06_testing/round_3_canonical_run_analysis.md`](06_testing/round_3_canonical_run_analysis.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/artifacts/full_synthesis/full_run_metrics.csv`](06_testing/artifacts/full_synthesis/full_run_metrics.csv)
- [`06_testing/artifacts/full_synthesis/full_path_family_summary.csv`](06_testing/artifacts/full_synthesis/full_path_family_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv`](06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`05_implementation/learning_batch_wave2_manifest.md`](05_implementation/learning_batch_wave2_manifest.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Collect the first Wave 2 platform artifacts. The testing bottleneck has moved from design to validation: we now need live runs to rank the 14 core bots, classify the 5 coverage bots, and compare final PnL with path retention.

## Deadline Risk

Unknown.
