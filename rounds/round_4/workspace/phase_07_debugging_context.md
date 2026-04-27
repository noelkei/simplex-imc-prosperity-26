# Phase 07 - Debugging And Iteration Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Reproduced a Wave 2 implementation issue from user-reported live runs:
  `r4_w2_01` through `r4_w2_07` showed flat PnL / no visible engagement.
- Compared the Wave 2 `VEX` base trading logic against the live Wave 1 base.
- Identified that Wave 2 replaced the inherited Wave 1 `VEX` posting behavior
  with a stricter signal-gated variant, which could leave the retention pack
  effectively inactive instead of testing only retention overlays.
- Patched `wave2_shared_engine.py` so Wave 2 `VEX` branches inherit the live
  Wave 1-style `VEX` quoting behavior and keep Wave 2 overlays on top.
- Regenerated all `15` standalone uploadable Wave 2 bot files from the patched
  shared engine.
- Added `15` suffixed uploadable copies named `*_debugged.py` so patched reruns
  can be distinguished immediately from the invalid pre-hotfix evidence.
- Re-ran syntax compilation and local `Trader.run()` smoke validation after the
  fix.
- Compared Wave 1 and active Wave 2 bots on reconstructed `day_1` snapshots
  and recorded a new debugging note:
  `06_debugging/issue_2026-04-28_wave2_passive_vs_wave1.md`.
- Applied a fill-seeking recalibration pass to the active Wave 2 option
  branches and regenerated the active upload set.

## Current Findings

- Root cause is currently classified as `implementation behavior regression`,
  not as `no edge`.
- The broken behavior was structural: the Wave 2 `VEX` core was stricter than
  intended, so the original early Wave 2 queue was not testing the intended
  parent behavior.
- After the fix, strategy was refined as well: nine low-ROI active variants
  were replaced with cleaner entry and option-only probes rather than simply
  rerunning every old overlay.
- The new dominant issue is not “no orders”; it is “orders are too passive to
  get filled compared with Wave 1 behavior”, especially in `5300` and `4000`.
- Post-patch local replay indicates that this passivity issue is materially
  reduced, but live reruns are still required for confirmation.

## Decisions Made

- Debugging issues require reproduction, expected vs observed behavior, linked spec, linked run, classification, and next action.
- Treat the user-reported flat-run batch as sufficient evidence to reopen
  debugging before further validation interpretation.

## Open Questions / Blockers

- Need re-run evidence on the patched uploadables before judging Wave 2 Pack
  `G/H` quality.
- Need the user to upload the `_debugged.py` series rather than the original
  Wave 2 filenames for the next rerun slice.
- Need to confirm whether remaining inactivity, if any, comes from `5300`
  execution logic itself or only from the previously broken `VEX` parent.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`06_debugging/README.md`](06_debugging/README.md)
- [`06_debugging/issue_2026-04-28_wave2_passive_vs_wave1.md`](06_debugging/issue_2026-04-28_wave2_passive_vs_wave1.md)
- [`phase_05_implementation_context.md`](phase_05_implementation_context.md)
- [`../bots/noel/canonical/wave2_shared_engine.py`](../bots/noel/canonical/wave2_shared_engine.py)

## Next Priority Action

Re-upload the refined `_debugged.py` Wave 2 bots and re-run at least
`r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, and `r4_w2_15` now that the
fill-seeking recalibration pass is in place.

## Deadline Risk

Medium: the issue was caught early, but any pre-fix Wave 2 run evidence for the
affected bots should be treated as invalid for strategy judgment.
