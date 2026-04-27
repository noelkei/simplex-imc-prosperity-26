# Phase 04 - Spec Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Codex
- Reviewer: Human

## Last Updated

2026-04-27

## What Has Been Done

- Reopened `Phase 04` after Wave 2 strategy work replaced the old Wave 1 queue
  as the active direction.
- Wrote four grouped Wave 2 specs:
  - `pack_g_vex_retention_rescue`
  - `pack_h_5300_winner_style_and_veto`
  - `pack_i_light_context_overlays`
  - `pack_j_4000_activation_and_execution`
- Carried run-informed evidence from Pack `A/B/D` into the specs so the Wave 2
  implementation set is explicitly path-rescue, isolation, and coverage-gap
  driven.
- Added explicit winner-style adaptation in the new `5300` and `4000` packs:
  simple rolling-IV fair value, strike-specific quote ladder, and queue
  takeover, but without porting incompatible old-round calibration or hedge
  machinery.
- Updated `04_strategy_specs/README.md` so Wave 2 and historical Wave 1 specs
  are clearly separated.

## Current Findings

- `04` should still stay grouped by learning family, not split into `15`
  isolated one-off specs.
- The highest-ROI Wave 2 implementation start is now:
  - Pack `G` retention rescue
  - Pack `H` `5300` isolation and winner-style adaptation
  - Pack `J` honest `4000` attribution closure
- Pack `I` should stay behind those unless Wave 2 capacity is larger than the
  preferred mini-batch.
- The best direct port of the uploaded winner style is no longer a literal
  carry-forward bot; it is a controlled execution architecture inside Pack `H`
  and Pack `J`.

## Decisions Made

- Reviewed spec remains mandatory before implementation unless deadline
  deferral is explicit.
- Grouped pack specs remain acceptable as long as they preserve candidate
  differences, feature contracts, and validation checks cleanly.
- User explicitly requested implementing all `15` Wave 2 bots, so the grouped
  specs were treated as operationally approved for exploratory implementation.
- The winner-style adaptation is explicitly limited to portable structure:
  rolling-IV fair value, intrinsic floor, quote ladder, and queue takeover.

## Open Questions / Blockers

- No material blocker remains in `Phase 04`.
- Canonical Pack `C/E/F` summaries are still missing, which slightly weakens
  confidence on the full `5300` family but does not block spec writing.
- Exact deadline remains unknown, so validation discipline is now more
  important than further spec expansion.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/README.md`](04_strategy_specs/README.md)
- [`04_strategy_specs/spec_pack_g_vex_retention_rescue.md`](04_strategy_specs/spec_pack_g_vex_retention_rescue.md)
- [`04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md`](04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md)
- [`04_strategy_specs/spec_pack_i_light_context_overlays.md`](04_strategy_specs/spec_pack_i_light_context_overlays.md)
- [`04_strategy_specs/spec_pack_j_4000_activation_and_execution.md`](04_strategy_specs/spec_pack_j_4000_activation_and_execution.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)

## Next Priority Action

Monitor Wave 2 implementation consistency during `Phase 05` and hand the new
bots into `Phase 06 Testing/performance`, starting with the highest-ROI
validation order:
`r4_w2_01`, `r4_w2_08`, `r4_w2_13`, then `r4_w2_07` or `r4_w2_15`.

## Deadline Risk

Medium: the spec layer is complete, but ROI now depends on grouped validation
instead of scattered run ordering.
