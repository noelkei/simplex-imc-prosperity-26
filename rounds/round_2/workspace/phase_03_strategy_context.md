# Phase 03 - Strategy Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Bruno (Claude session)
- Reviewer: Unassigned

## Last Updated

2026-04-19

## What Has Been Done

- Analysed all Round 1 bots: `TEST1_merged`, `candidate_03` through `candidate_07`, and Noel's `candidate_26_v3`.
- Parsed actual R1 performance logs (`190076.log`, `200823.log`) to extract per-product P&L:
  - IPR P&L: ~7,286 per run (max-long +80 strategy, drift=+0.001/timestamp)
  - ACO P&L: ~2,132 (190076) and ~1,939 (200823) — with R1 imbalance gain=2.0
- Identified **critical gap**: gain=2.0 captures only 29% of the IC=0.647 imbalance signal.
- Quantified IC signal magnitude: β=0.647×(3.7/0.35)=6.85 ticks/unit imbalance.
- Derived the **imbalance-adjusted take threshold** concept: positive EV for taking asks
  up to +4.8 ticks above FV when imb=0.7 (E[Δmid]=4.8, cost=3 ticks, gain=+1.8 ticks).
- Designed 10 differentiated bots covering 4 independent axes:
  1. Imbalance gain (2→6)
  2. Kalman tuning (R1 stable vs R2 MLE reactive)
  3. Imbalance-adjusted take threshold (novel mechanism)
  4. Adaptive quote sizing by imbalance direction
- Implemented all 10 bots as standalone Python files.
- Shortlisted 3 candidates: b03 (imb6), b06 (take_adj), b09 (full combined).

## Current Findings

- **Main opportunity**: Imbalance IC=0.647 vastly underexploited at gain=2. Raising to
  gain=5-6 is the single highest-value lever, backed by strong statistical evidence.
- **Novel mechanism**: Imbalance-adjusted take threshold — mathematically justified by
  positive EV calculation. First tested in b06, fully deployed in b09.
- **Kalman axis**: R2 MLE Kalman (K≈0.11 vs K≈0.014) is a secondary improvement;
  expected effect is modest unless intraday drift events occur frequently.
- **MAF**: Bid 2,500 (b01-b09) or 3,000 (b10); EV depends on actual participant median.
- **IPR**: Already optimal at max-long; no improvement axis identified.

## Decisions Made

- IPR strategy fixed: max-long identical to R1 c_07 (buy all available, queue at bb+1).
- MAF bid: 2,500 for all bots except b10 (3,000 sensitivity test).
- ACO: no one-sided book changes — R1 proven logic retained for that case.
- Implement all 10 bots immediately rather than staging (per explicit user request).
- Shortlist for formal spec: b03, b06, b09.

## Open Questions / Blockers

- Which gain level (4, 5, or 6) maximises ACO P&L in the live environment?
- Does the imbalance IC hold at 0.647 in the live environment, or has it been saturated?
- What is the actual distribution of MAF bids? Does 2,500 clear the median?

## Linked Artifacts

- [`_index.md`](_index.md)
- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- All 10 bots: `../bots/bruno/canonical/r2_b01_baseline.py` through `r2_b10_maf3000.py`

## Next Priority Action

Phase 04 (Spec): Write formal spec for the 3 shortlisted candidates (b03, b06, b09).
Then Phase 05 (Implementation): bots already implemented; select best candidate for submission.
Phase 06 (Testing): backtest all 10 against R2 CSV data and compare ACO P&L vs b01.

## Deadline Risk

Unknown — round deadline not announced. All 10 bots implemented and ready for testing.
