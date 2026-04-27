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
  strategy handoff note, the `round_4` post-run memory, and the Pack `A/B/D`
  synthesis.
- Reopened [`03_strategy_candidates.md`](03_strategy_candidates.md) after
  Wave 1 Pack `A/B/D` materially changed the branch map.
- Reframed Phase `03` around a Wave 2 exploratory queue of `15` bots whose
  purpose is learning efficiency, not immediate final-winner selection.
- Converted the Wave 1 lessons into a clean coverage audit:
  - `VEX` base is alive but retention-limited
  - standalone `HYDRO` is low ROI
  - `VEV_4000` is still untested online, not disproven
  - `VEV_5200` survives mainly as signal-only veto context
- Ran a compatibility gate over the uploaded winner `.py` files in
  `../research/` and classified them as architecture inspiration only, not
  current-round direct templates.

## Current Findings

- The highest-ROI Phase `03` themes are now:
  - `VEX` retention rescue
  - `5300` current-round isolation
  - `5200` veto reuse on stronger parents
  - honest `4000` attribution closure
- The uploaded winner bots are useful only at the architecture level:
  - strike-specific treatment
  - fair-value quote discipline
  - cross-then-requote probes
  - inventory-aware quote tilt
- The current candidate queue should answer five questions before the winner
  wave:
  - is `VEX` salvageable with retention controls?
  - does `5300` deserve serious exploitation now?
  - does the `5200` veto travel cleanly to stronger parents?
  - is `4000` dead or merely untested?
  - are some failures execution-limited rather than no-edge?

## Decisions Made

- Strategy candidate count remains ROI-driven, but this reopen still chooses
  `15` slots because the unresolved questions are distinct and decision-relevant.
- Wave 2 candidates are grouped into four learning packs:
  - `G` retention rescue
  - `H` `5300` isolation
  - `I` light context overlays
  - `J` honest `4000` closure
- Uploaded winner `.py` files are classified `partially compatible` and feed
  architecture ideas only; no prior-round symbols or calibration survive.
- `04 Spec` now exists for the grouped Wave 2 queue, so the next decision is
  implementation priority rather than more strategy branching.

## Open Questions / Blockers

- No material blocker prevents the `03 -> 04` handoff.
- Canonical Pack `C/E/F` summaries are still missing, so `5300` confidence is
  lower than the `VEX` and `5200` conclusions from `A/B/D`.
- Exact deadline remains unknown, which could force Pack-level pruning during
  spec or implementation.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`02_understanding.md`](02_understanding.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)
- [`02b_strategy_handoff.md`](02b_strategy_handoff.md)
- [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`](01_eda/eda_round_4_wave1_abd_retrospective_addendum.md)

## Next Priority Action

Use the implemented Wave 2 bots in `Phase 06` to prune the queue based on real
path quality. Default validation order:
`r4_w2_01`, `r4_w2_08`, `r4_w2_13`, then the winner-style adapted probes
`r4_w2_07` or `r4_w2_15`.

## Deadline Risk

Medium: the queue is much cleaner now, but ROI still depends on keeping Wave 2
grouped, one-axis, and pruned during `04/05`.
