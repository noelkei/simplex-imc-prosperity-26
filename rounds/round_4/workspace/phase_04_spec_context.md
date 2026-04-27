# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-28

## What Has Been Done

- Revised the grouped Wave 2 specs after the Wave 2 debugging incident and the
  queue refinement.
- Preserved the grouped pack structure:
  - `pack_g_vex_retention_rescue`
  - `pack_h_5300_winner_style_and_veto`
  - `pack_i_light_context_overlays`
  - `pack_j_4000_activation_and_execution`
- Rewrote pack membership so the active queue keeps six structural bots and
  replaces nine low-ROI overlays with direct entry probes and option-only
  attribution tests.

## Current Findings

- Pack `G` is no longer mostly small retention variants; it is now one retained
  rescue plus three distinct `VEX` entry probes.
- Pack `H` and Pack `J` now include cleaner option-only tests, not just
  parented hybrids.
- The winner-style adapted architecture remains concentrated in `r4_w2_07` and
  `r4_w2_15`.

## Decisions Made

- Grouped pack specs remain the correct abstraction.
- User direction is still treated as operational approval for implementation.
- The spec layer now reflects the shorter remaining runway by favoring
  distinct decision questions over incremental overlay tweaks.

## Open Questions / Blockers

- No spec blocker remains.
- Fresh reruns are required before any further queue pruning.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/spec_pack_g_vex_retention_rescue.md`](04_strategy_specs/spec_pack_g_vex_retention_rescue.md)
- [`04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md`](04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md)
- [`04_strategy_specs/spec_pack_i_light_context_overlays.md`](04_strategy_specs/spec_pack_i_light_context_overlays.md)
- [`04_strategy_specs/spec_pack_j_4000_activation_and_execution.md`](04_strategy_specs/spec_pack_j_4000_activation_and_execution.md)

## Next Priority Action

Keep `Phase 05` aligned with the refined queue and treat the active upload set
as the debugged series only. Start validation with:
`r4_w2_01`, `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`.

## Deadline Risk

Medium: the spec layer is now better targeted, but the next learning depends on
clean reruns rather than more design branching.
