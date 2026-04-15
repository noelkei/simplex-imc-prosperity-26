# Phase 01 - EDA Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Claude
- Reviewer: Unassigned (human sign-off recommended before spec)

## Last Updated

2026-04-15

## What Has Been Done

- Loaded all 6 CSV files (prices + trades for days -2, -1, 0) into local analysis.
- Computed per-product per-day statistics: mid price range, mean, stdev, drift.
- Verified fair value formula for INTARIAN_PEPPER_ROOT (linear drift).
- Checked mean-reversion and autocorrelation for ASH_COATED_OSMIUM.
- Analyzed spread distributions and order book depth for both products.
- Analyzed trades file for price range and typical trade size.

## Current Findings

**INTARIAN_PEPPER_ROOT:**
- NOT stable. Has a linear upward drift of +0.1 per 100 ticks (+1 per 1,000 timestamp units, +~1,000 per day).
- Fair value formula: `day_start_price + timestamp * 0.001`. Residual noise stdev ≈ 2.4 (small vs. spread of 12–14).
- Each day starts ~1,000 above the previous day.
- Market spread: 12–14 ticks (dominant). Depth: ~11–12 units first level.

**ASH_COATED_OSMIUM:**
- Mean-reverts tightly around 10,000. Max observed deviation: ±23. Stdev when both sides present: 4–5.
- High autocorrelation (lag-1: 0.79) — slow reversion, price is persistent.
- Market spread: 16 ticks (64%), 18–19 ticks (~25%).
- Confirmed stable across all 3 days. No cross-day drift.

## Decisions Made

- INTARIAN_PEPPER_ROOT fair value = `day_start + t * 0.001` (not static). This overrides wiki's "quite steady" description — the product has predictable drift, not a flat level.
- ASH_COATED_OSMIUM fair value = 10,000. "Hidden pattern" is likely that its fair value is knowable despite apparent volatility.
- Both strategies will be market-making variants, distinguished by their fair value model.

## Open Questions / Blockers

- None blocking strategy phase. Open questions are noted in `01_eda/eda_round_1.md`.
- Drift rate 0.001/tick is an estimate — implementation should allow easy parameter adjustment.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/eda_round_1.md`](01_eda/eda_round_1.md)
- Data: `rounds/round_1/data/raw/prices_round_1_day_{-2,-1,0}.csv`
- Data: `rounds/round_1/data/raw/trades_round_1_day_{-2,-1,0}.csv`

## Next Priority Action

1. **Human:** Review `01_eda/eda_round_1.md` findings and confirm or correct.
2. **Agent:** Once EDA is confirmed, write phase 02 Understanding and phase 03 Strategy candidates.

