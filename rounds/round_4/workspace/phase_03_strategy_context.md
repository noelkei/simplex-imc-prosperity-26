# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Consumed the completed understanding summary, `02b` paper artifact, the
  strategy handoff note, and the key `round_3` carry-forward memory.
- Ran a compact paper intake pass over the usable `round_4` raw-derived core
  plus the most relevant `round_3` carry-forward references.
- Built a full `Phase 03` strategy artifact in
  [`03_strategy_candidates.md`](03_strategy_candidates.md).
- Produced a first implementation wave of `15` exploration bots aimed at:
  - revalidating what still works from `round_3`
  - testing the genuinely new counterparty/context layer in `round_4`
  - probing whether paper-inspired filters improve or only redescribe the tape
- Added a `Wave 1 Learning Matrix` and `Spec Grouping Recommendation` so that
  `04 Spec` can be written as grouped exploratory packs instead of `15`
  disconnected one-off designs.

## Current Findings

- `round_4` should still start from `delta-1 / VEX anchor first`, but the main
  new test axis is now `counterparty-conditioned context`, not broad new alpha.
- The first implementation wave should be exploratory by design rather than a
  tiny set of presumed winners; `15` bots is justified because they isolate
  different new hypotheses cleanly.
- The cleanest next move is to write grouped specs by learning family:
  controls, round-3 revalidation, counterparty-defensive logic, `5300`
  variants, context overlays, and low-priority closure probes.
- The highest-ROI exploration themes are:
  - clean controls
  - counterparty danger-state logic
  - trade-to-book execution overlays
  - strike-isolated `4000` / `5300` tests
  - `5200` as signal-only context
  - family-pressure context
  - upper passive and surface-sanity low-priority probes

## Decisions Made

- Strategy candidate count is ROI-driven, not fixed.
- Keep all non-duplicative high-ROI candidates and manage focus with roles,
  priority tiers, and implementation waves.
- Wave 1 is explicitly fixed to `15` exploration bots by user direction.
- The top-level nine-paper `round4_raw_derived` processed core is the primary
  paper input for Strategy; `round_3` carry-forwards remain secondary.
- `03` is considered complete for review once the candidate queue, priority
  order, carry-forward ledger, paper-intake pass, and rejected/deferred ideas
  are all recorded in `03_strategy_candidates.md`.
- `04 Spec` should be written in grouped packs rather than candidate by
  candidate to preserve comparability and reduce redundant spec work.

## Open Questions / Blockers

- No material blocker prevents `04 Spec`.
- Exact deadline remains unknown, which adds some risk to a `15`-bot first wave.
- The main remaining uncertainty is not phase readiness but how fast grouped
  specs can be written and reviewed.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`02_understanding.md`](02_understanding.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)
- [`02b_strategy_handoff.md`](02b_strategy_handoff.md)

## Next Priority Action

Open `04 Spec` and write grouped specs for the `15` Wave 1 exploration bots,
starting with `pack_a_delta1_controls`, `pack_b_round3_revalidation`, and
`pack_d_counterparty_defensive`, then continue with the remaining grouped packs
from `03_strategy_candidates.md`.

## Deadline Risk

Medium: the strategy phase is ready, but a `15`-bot exploration wave will only
pay off if `04 Spec` and later implementation stay grouped and disciplined.
