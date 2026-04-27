# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Implemented a shared Wave 1 engine in
  [`../bots/noel/canonical/wave1_shared_engine.py`](../bots/noel/canonical/wave1_shared_engine.py)
  plus `15` canonical exploration bots matching the approved grouped specs.
- Implemented all Wave 1 bot files under
  [`../bots/noel/canonical/`](../bots/noel/canonical/), covering Packs `A`
  through `F`.
- Rewrote the `15` canonical bots as standalone uploadable files so they no
  longer depend on local path hacks or sibling-module imports forbidden by
  Prosperity upload checks.
- Ran syntax compilation across the shared engine and all `15` bot files.
- Ran import smoke and minimal `run()` contract smoke for all `15` bots using a
  stub `datamodel` and mock `TradingState`.

## Current Findings

- The implementation is intentionally pack-driven: one shared engine plus
  strategy-specific configs keeps the exploration wave comparable and easier to
  debug locally, while the uploadable bot files themselves are now standalone.
- The most important validation start remains Packs `A`, `B`, and `D`, because
  they answer the highest-ROI control, carry-forward, and counterparty
  questions first.
- The implementation currently optimizes for breadth and comparability, not for
  final submission readiness.

## Decisions Made

- Implementation count is driven by reviewed specs, validation capacity,
  deadline risk, and distinct test axes.
- Implementation requires a reviewed strategy spec.
- User direction to proceed into `Phase 05` was recorded as operational
  approval of the grouped specs for exploratory implementation.
- Shared local helper code is acceptable for candidate bots in this phase; any
  later submission candidate can inline or simplify if needed.

## Open Questions / Blockers

- No material blocker prevents testing.
- Validation is now the main gate: no bot should be treated as submission-ready
  until `Phase 06` and `Phase 07` produce readable evidence.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`04_strategy_specs/README.md`](04_strategy_specs/README.md)
- [`../bots/noel/canonical/`](../bots/noel/canonical/)
- [`../bots/noel/canonical/wave1_shared_engine.py`](../bots/noel/canonical/wave1_shared_engine.py)
- Uploadable candidate files:
  `r4_s01` through `r4_s15` in `../bots/noel/canonical/`

## Next Priority Action

Open `06 Testing/performance` and validate the first Wave 1 batch, starting
with Packs `A`, `B`, and `D`.

## Deadline Risk

Medium: the implementation breadth is intentional, but the `15`-bot wave only
stays high-ROI if testing is grouped and disciplined instead of scattered.
