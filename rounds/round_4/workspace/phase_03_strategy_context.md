# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-28

## What Has Been Done

- Reopened Wave 2 strategy after the Wave 2 debugging incident and the user
  decision to optimize for this wave plus only two more rounds before final
  selection.
- Kept the six highest-ROI structural bots:
  `r4_w2_01`, `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`.
- Replaced the other nine slots with entry-quality probes and cleaner
  option-only attribution tests.
- Updated [`03_strategy_candidates.md`](03_strategy_candidates.md) so the live
  Wave 2 queue is now more signal-seeking and less overlay-heavy.

## Current Findings

- The main remaining question is no longer just retention. It is whether we
  can find cleaner entry logic in `VEX`, `5300`, and `4000`.
- `5300` and `4000` both deserve at least one direct isolated test without the
  parent `VEX` branch contaminating attribution.
- Counterparty and family context should now be tested as entry-quality gates
  as well as vetoes.

## Decisions Made

- The active Wave 2 queue stays at `15`, but the composition is now sharper:
  fewer near-duplicate overlays, more direct signal probes.
- Pack grouping remains useful, so `Phase 04` stays grouped rather than split
  into `15` separate specs.
- The next run slice should emphasize the kept structural bots first, then the
  best new entry probes.

## Open Questions / Blockers

- No strategy blocker remains.
- The refined queue now depends on implementation consistency and fresh reruns;
  old pre-fix Wave 2 evidence remains invalid.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`04_strategy_specs/`](04_strategy_specs/)
- [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)

## Next Priority Action

Use the refined specs and implementations in `Phase 05/06`. Default rerun
order:
`r4_w2_01`, `r4_w2_05`, `r4_w2_07`, `r4_w2_08`, `r4_w2_13`, `r4_w2_15`,
then the best new entry probes `r4_w2_02`, `r4_w2_06`, and `r4_w2_14`.

## Deadline Risk

Medium: the queue is now better aligned with limited remaining rounds, but its
value depends on disciplined rerun ordering and fast pruning.
