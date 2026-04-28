# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Closed the old Wave 2 queue as the live strategy surface.
- Crossed all `round_4` performance artifacts with `round_3` carry-forward
  evidence before selecting the last upload wave.
- Rewrote [`03_strategy_candidates.md`](03_strategy_candidates.md) around a
  distilled `10`-bot queue.

## Current Findings

- The strongest `round_4` real-PnL family is the focused OTM basket:
  `5300 + 5400 + 5500`.
- `5300` alone remains the strongest positive fallback family.
- The only `round_3` lessons worth importing now are retention and toxic-veto
  controls, not the raw broad voucher basket.

## Decisions Made

- All prior live `canonical/` bots were archived before creating the new final
  queue.
- The final queue uses `7` proven performers and `3` one-axis derivatives.
- `4000`, flat Wave 2 probes, and raw delta-1 reopens are out of the final
  upload wave.

## Open Questions / Blockers

- No strategy blocker remains.
- Final strategy ranking now depends only on fresh live reruns of the new
  `10`-bot pack.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Use the final distilled queue in `Phase 04/05/06`, starting with:
`01`, `02`, `08`, `09`, `10`, then the remaining proven backups.

## Deadline Risk

Medium: strategy selection is now narrow and evidence-based, but final ranking
still requires live reruns.
