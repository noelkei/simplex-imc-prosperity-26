# Phase 01 - EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Phase 00 now confirms raw Round 4 price and trade CSVs for days `1-3`.
- The round has been framed as `compatible` with `round_3`, with one material
  delta: visible counterparties in `Trade.buyer` and `Trade.seller`.
- The first EDA pass has been narrowed to counterparty-aware market structure
  and revalidation of Round 3 carry-forward assumptions.
- Implemented the reusable analysis script
  [`01_eda/analyze_round_4_eda.py`](01_eda/analyze_round_4_eda.py).
- Generated processed evidence tables under `../../data/processed/`.
- Generated Phase 01 plots and manifests under `01_eda/artifacts/`.
- Wrote the canonical EDA and the four supporting annexes.
- Extended Phase 01 with side-aware counterparty markouts, buyer-seller pair
  ecology, trade-to-book context, formal counterparty stability scoring, and
  a mini EDA on newly engineered usable features.
- Added an advanced option-pricing annex covering IV surface, Greeks,
  Black-Scholes vs Heston fit, and COS pricing, plus counterparty exposure and
  metric-availability extensions.
- Added the retrospective run-informed EDA addendum
  [`01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`](01_eda/eda_round_4_wave1_abd_retrospective_addendum.md)
  after the first meaningful Wave 1 performance batch.

## Current Findings

- `prices_*` files cover all 12 algorithmic products for days `1-3`.
- `trades_*` files expose named `Mark XX` counterparties and already show
  concentrated participant activity.
- EDA should begin from the raw trade data, not from strategy speculation.
- Counterparty specialization is real and stable enough to promote as
  contextual state, but not as standalone alpha.
- Engineered context features add more explanatory value than raw buyer/seller
  names alone: the simple model ladder moves from `R^2 = 0.0076` to `0.0101`
  with raw name buckets and to `0.0183` with engineered context.
- `VEX` remains the strongest same-time anchor for the voucher family and
  delayed-follow stays weak.
- The voucher family is linked structurally but execution-fragmented by strike,
  especially from `5200` upward.
- `Mark 22` seller flow in `5200+` is the clearest counterparty-conditioned
  danger-state pattern in the raw data.
- The short-dated voucher surface is not flat: Heston improves the aggregated
  cross-strike fit in `7/9` panels, but only moderately.
- Early Pack `A/B/D` run evidence reinforces that `VEX` is the practical base,
  that `VEV_5200` is more useful as veto than as inventory, and that direct
  `VEV_4000` inventory is still untested rather than disproven.

## Decisions Made

- Use `round_3` as a compatible carry-forward source, but revalidate its
  lessons against counterparty-aware data before promoting any strategy
  conclusion.
- Start with a targeted EDA question on whether specific counterparties show
  stable product, side, or timing behavior that changes the Round 3 framing.
- Build Phase 01 as `algorithmic-first`.
- Use one canonical EDA plus annexes rather than many peer artifacts.
- Treat `round_4` as raw-data EDA plus a focused retrospective run-informed
  addendum once meaningful Wave 1 evidence exists.
- Internal sufficiency review says `Phase 01` is adequate to open
  `Phase 02 Understanding` without more mandatory EDA work.
- Remaining Phase 01 additions are `nice to have`, not blockers:
  future run-informed EDA after testing exists, manual contract analysis once
  raw contract details are available, and any extra niche quant diagnostics
  only if a later strategy candidate specifically depends on them.

## Open Questions / Blockers

- Exact deadline remains unknown.
- Manual contract-level raw data is still missing.
- Human Phase 01 review is still pending, but no material EDA gap currently
  blocks `Phase 02`.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`00_ingestion.md`](00_ingestion.md)
- [`00_prior_round_intake.md`](00_prior_round_intake.md)
- [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
- [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
- [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
- [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
- [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- [`01_eda/eda_round_4_wave1_abd_retrospective_addendum.md`](01_eda/eda_round_4_wave1_abd_retrospective_addendum.md)
- [`01_eda/analyze_round_4_eda.py`](01_eda/analyze_round_4_eda.py)
- [`06_testing/round_4_wave1_pack_abd_partial_synthesis.md`](06_testing/round_4_wave1_pack_abd_partial_synthesis.md)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
- [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)

## Next Priority Action

EDA is now sufficient again. The next EDA-derived action is not broad new
analysis, but using the retrospective addendum to support a narrower
`Phase 03/04` reopen around retention and `5200` veto reuse.

## Deadline Risk

Medium until deadline is confirmed and Phase 01 review is complete.
