# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Implemented a shared Wave 2 engine in
  [`../bots/noel/canonical/wave2_shared_engine.py`](../bots/noel/canonical/wave2_shared_engine.py)
  covering the full Wave 2 candidate queue.
- Implemented all `15` Wave 2 canonical bots under
  [`../bots/noel/canonical/`](../bots/noel/canonical/), covering Packs `G`
  through `J`.
- Generated the Wave 2 bots as standalone uploadable files so they do not
  depend on local sibling imports forbidden by Prosperity upload checks.
- Implemented the winner-style adapted execution architecture in Wave 2 where
  it actually fits:
  - `r4_w2_07_5300_queue_takeover_probe`
  - `r4_w2_15_4000_quote_ladder_probe`
- Ran syntax compilation across the shared engine and all `15` Wave 2 bot
  files.
- Ran import smoke and minimal `run()` contract smoke for all `15` Wave 2 bots
  using a stub `datamodel` and mock `TradingState`.

## Current Findings

- The implementation is intentionally pack-driven: one shared Wave 2 engine plus
  strategy-specific configs keeps the new wave comparable and easier to debug
  locally, while the uploadable bot files themselves remain standalone.
- The most important validation start is now:
  - `r4_w2_01_vex_late_no_new_entry`
  - `r4_w2_08_5300_with_5200_veto`
  - `r4_w2_13_4000_forced_activation`
  - then one winner-style adapted probe from `r4_w2_07` or `r4_w2_15`
- The implementation now optimizes for uploadability and comparability, but not
  yet for final submission readiness.

## Decisions Made

- Implementation count was expanded to the full `15`-bot Wave 2 queue by
  explicit user direction.
- Implementation used approved grouped specs after the user's explicit request
  to implement all Wave 2 bots.
- Shared local helper code is acceptable in this phase, but each uploadable bot
  file was emitted as standalone code.
- The main architecture split is now:
  - retention rescue on `VEX`
  - `5300` isolation and winner-style adaptation
  - light context overlays
  - honest `4000` activation and execution closure

## Open Questions / Blockers

- No material blocker prevents testing.
- Validation is now the main gate: no bot should be treated as submission-ready
  until `Phase 06` and `Phase 07` produce readable evidence.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/README.md`](04_strategy_specs/README.md)
- [`../bots/noel/canonical/`](../bots/noel/canonical/)
- [`../bots/noel/canonical/wave2_shared_engine.py`](../bots/noel/canonical/wave2_shared_engine.py)
- Linked Wave 2 spec packs:
  - [`04_strategy_specs/spec_pack_g_vex_retention_rescue.md`](04_strategy_specs/spec_pack_g_vex_retention_rescue.md)
  - [`04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md`](04_strategy_specs/spec_pack_h_5300_winner_style_and_veto.md)
  - [`04_strategy_specs/spec_pack_i_light_context_overlays.md`](04_strategy_specs/spec_pack_i_light_context_overlays.md)
  - [`04_strategy_specs/spec_pack_j_4000_activation_and_execution.md`](04_strategy_specs/spec_pack_j_4000_activation_and_execution.md)
- Uploadable candidate files:
  `r4_w2_01` through `r4_w2_15` in `../bots/noel/canonical/`

## Next Priority Action

Open `06 Testing/performance` and validate the first Wave 2 batch, starting
with:
- `r4_w2_01_vex_late_no_new_entry`
- `r4_w2_08_5300_with_5200_veto`
- `r4_w2_13_4000_forced_activation`
- then `r4_w2_07_5300_queue_takeover_probe` or
  `r4_w2_15_4000_quote_ladder_probe`

## Deadline Risk

Medium: the full `15`-bot implementation breadth was intentional by user
request, but ROI now depends on disciplined grouped validation instead of
scattered runs.
