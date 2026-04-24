# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-24

## What Has Been Done

- Completed paper intake pass over all 8 processed papers with explicit classifications.
- Generated 7 strategy candidates across 4 product branches (hydrogel, VEX, active vouchers, ITM vouchers) plus 2 variants and 1 composite.
- Produced prioritized candidate queue with C06 (full-scope composite) and C03 (Bachelier residual reversion) as primary spec-first candidates.
- Classified 10 rejected/deferred ideas with evidence gaps.
- Applied exploration stop rule: all viable product branches and strategy axes are covered.
- Checked round coverage (TTE=5d, integer prices, no-lib constraint, floor behavior, independent position limits).
- Built combination/compatibility matrix confirming branch independence.
- Referenced ML_finance and slides_options docs for extra context; no new candidate directions emerged beyond what EDA/Understanding/papers already support.

## Current Findings

- C03 (Bachelier Residual Reversion for VEV_5000-5300) has the strongest evidence: hybrid of data-driven residual reversion + Choi Bachelier pricing backbone.
- C06 (Full-Scope Combined Trader) is the practical implementation target since one Trader file handles all products.
- C01 (Hydrogel MM) and C02 (VEX MM) are low-cost independent PnL streams.
- C04 (inventory skew) and C07 (TTE-cautious) are the two priority validation variants addressing the round's main operational and calibration risks.
- C05 (ITM anchor) is differentiated but deferred to wave 2 due to sparse execution.

## Decisions Made

- Paper intake: Choi and West `used`, Stoikov-Saglam and Muravyev `hybrid`, Garcia-Ares/Fengler/CRR `validation`, Bergault `inspiration-only`.
- Feature budget enforced: each candidate has 1 primary + max 2 supporting features.
- Delayed underlying-follow firmly rejected as strategy signal.
- VEV_6000/6500 excluded from all waves; VEV_5400/5500 deferred.
- Full BS/IV stack rejected in favor of Bachelier simplicity.
- Bergault full matrix deferred as escalation path only.

## Open Questions / Blockers

- Human checkpoint: composite C06 first vs C03-only first?
- Human checkpoint: C04 or C07 as priority variant?
- Phases 00-02 reviews still pending (non-blocking for Phase 03).
- TTE=5d remains out-of-sample.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`02_understanding.md`](02_understanding.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)
- [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md)

## Next Priority Action

Write strategy spec for C06 (composite Trader) with C01, C02, C03 as component blocks.
Include Feature Contract and Round-Specific Mechanics Contract.
Then implement, validate, and iterate.

## Deadline Risk

Unknown. No bots exist yet; implementation should start soon.
