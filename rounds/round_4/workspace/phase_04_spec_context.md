# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-28

## What Has Been Done

- Added the final implementation-ready pack:
  [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md).
- Recorded the final queue as `7` proven bots plus `3` one-axis derivatives.
- Bound the new work to retention and veto logic only.

## Current Findings

- The spec layer no longer needs grouped Wave 2 exploration packs as the live
  abstraction.
- The final abstraction is a winner-distillation pack centered on the OTM
  family.
- `Mark 22 / 5200` only survives as a veto feature, not as a direct
  inventory thesis.

## Decisions Made

- Explicit user direction is treated as operational approval for this final
  pack.
- The raw `round_3` high-peak voucher basket is excluded from direct
  implementation.
- `4000` remains excluded from the last wave.

## Open Questions / Blockers

- No spec blocker remains.
- Validation must now decide whether any of the three new derivatives can beat
  or protect the champion.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md`](04_strategy_specs/spec_pack_k_final_otm_winner_distillation.md)
- [`06_testing/round_4_full_performance_synthesis.md`](06_testing/round_4_full_performance_synthesis.md)

## Next Priority Action

Keep `Phase 05` and `Phase 06` aligned with the final `10`-bot pack and rank
everything against `r4_finalbatch_01_full_otm_basket_champion.py`.

## Deadline Risk

Medium: the spec is stable, but the final promotion decision still depends on
live reruns.
