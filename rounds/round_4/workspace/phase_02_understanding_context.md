# Phase 02 - Understanding Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Consumed the full `round_4` Phase 01 package:
  - canonical EDA
  - counterparty profiles annex
  - option-book structure annex
  - option volatility / pricing annex
  - `round_3` revalidation annex
- Folded in the prior-round compatibility intake from `round_3`.
- Folded in the key carry-forward principles, unresolved learnings, and
  anti-patterns from the `round_3` closeout and research memory.
- Wrote a complete understanding summary in
  [`02_understanding.md`](02_understanding.md).
- Added a compact `02b` research seed set so external paper research can start
  immediately without reopening understanding.

## Current Findings

- `round_4` should still be framed as `delta-1 base + VEX anchor` first, not
  as a broad voucher-first market.
- Counterparties matter as contextual state and danger-state evidence more than
  as direct naked alpha.
- The voucher family remains structurally linked but execution-fragmented.
- `5200` and `5300` are the main unresolved strike-level questions worth
  carrying into strategy.
- The advanced pricing layer supports surface-aware framing, but not a heavy
  live Heston/COS implementation.
- Several important `round_3` unresolved questions have now been carried
  forward explicitly instead of being left implicit.
- The understanding artifact now makes explicit that most counterparty
  findings are descriptive/contextual first and only weakly predictive so far,
  with additional warnings on sample imbalance, product-selection confounds,
  and non-stationarity of visible identities.

## Decisions Made

- Treat `round_3` validated lessons, unresolved learnings, and anti-patterns as
  separate categories in `round_4` understanding.
- Promote `VEX` anchor logic, strike-role segmentation, counterparty
  concentration context, and upper/floor exclusion into strategy framing.
- Keep raw-name alpha, universal late-session toxicity, direct `5200` veto, and
  direct `5300` rescue claims below validated status until `round_4` runs
  exist.
- Leave Phase 02 at `READY_FOR_REVIEW`; do not mark it `COMPLETED` without
  explicit review.

## Open Questions / Blockers

- Human review is still pending.
- Exact deadline remains unknown.
- No `round_4` run evidence exists yet, so several strategy-relevant claims
  remain contextual rather than validated.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`00_prior_round_intake.md`](00_prior_round_intake.md)
- [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
- [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
- [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
- [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
- [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- [`02_understanding.md`](02_understanding.md)
- [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
- [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)

## Next Priority Action

Review the understanding package, then generate the default `02b` external
paper research prompt and open `03 Strategy` using the promoted carry-forward
principles, unresolved `round_3` learnings, contextual counterparty findings,
and explicit anti-patterns captured here.

## Deadline Risk

Medium until the deadline is confirmed and the first strategy wave is opened.
