# Phase 01 - EDA Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Bruno (Claude session)
- Reviewer: Unassigned

## Last Updated

2026-04-19

## What Has Been Done

- Loaded all 3 days of Round 2 data (60k price rows, ~2.4k trade rows; both products).
- Detected and cleaned `mid_price = 0` empty-book rows (~50/day total).
- Per-day descriptive stats on mid, spread, depth, level count.
- Day-over-day drift comparison (key finding: IPR ≈ +1000/day, ACO ≈ 0).
- Returns analysis: ACF, ACF², ADF, KPSS, Ljung-Box, ARCH-LM.
- Microstructure: top-of-book imbalance information coefficient (IC) at lags 1-10.
- Kalman filter MLE calibration (Q, R per day + pooled) with `scipy.optimize`.
- Hidden Markov regime detection with `hmmlearn` (K=2,3,4) using BIC for model selection.
- Cross-product correlation per day.
- MAF (Market Access Fee) marginal-value heuristic.
- Generated 6 plots saved in `01_eda/plots/`.

Artifacts:
- Script: `01_eda/scripts/eda_r2_deep.py`
- Numerical summary: `01_eda/outputs/eda_summary.json`
- Report: `01_eda/eda_round_2.md`
- Plots: `01_eda/plots/01_mid_price_3day.png`, `02_return_hist.png`, `03_acf.png`, `04_spread_hist.png`, `05_ipr_trend.png`, `06_kalman_mle.png`

## Current Findings

Top facts (full list in `01_eda/eda_round_2.md`):

- **IPR drifts +1000 XIRECs/day** — three days observed, day-over-day deltas +999.74 and +1000.19.
- **ACO is anchored at ~10000** with std ≤ 5.7 within day; near-zero day-over-day drift.
- **Order-book imbalance has IC = +0.65 vs next-tick mid change** for both products (signal dies at lag 2).
- ACF(Δmid, lag 1) = −0.50 for both products → bid-ask bounce, not a directional signal.
- Volatility clustering is real (ARCH-LM p=0; ACF(Δmid², lag 1) ≈ 0.40), but HMM regime persistence is short (~1.5 ticks) → not actionable as a discrete-state model.
- Kalman MLE (per-day & pooled): ACO Q≈0.09, R≈6.75 (steady K≈0.10); IPR Q≈0.21, R≈5.30.
  - Round 1 final used Q=0.005, R=25 — substantially under-reactive. Re-tuning required.
- Bid-ask spread: ACO=16 (constant), IPR=13/14/15 (rising +1/day).
- Cross-product return correlation ≈ 0 → no hedging signal.
- MAF marginal value estimate ≈ 2,500 XIRECs; recommended bid 2,000-2,500.

## Decisions Made

- Drop `mid=0` rows from all statistics (treat as empty-book artefacts, not real prices).
- Use **per-day Kalman calibration** (parameters are stable across days).
- **Reject HMM** for trading-decision use; document as not-actionable rather than tuning further.
- **Confirm IPR strategy = max-long** (matches Round 1 best practice, plus stronger evidence now).
- Imbalance signal will be a primary axis for ACO market-making in candidate strategies.

## Open Questions / Blockers

- Will the IPR +1000/day drift continue on submission day? (Risk: ~80,000 P&L swing if reversal.)
- What is the MAF median bid in the population? (No data; reason game-theoretically.)
- Should IPR Kalman use a 2-state filter (level + drift) instead of 1-state? (Defer to Phase 04 spec.)
- Is the imbalance signal already arbitraged away at high frequency in the live env? (Defer to Phase 06 testing.)

## Linked Artifacts

- [`_index.md`](_index.md)
- [`01_eda/README.md`](01_eda/README.md)
- [`01_eda/eda_round_2.md`](01_eda/eda_round_2.md)
- [`01_eda/scripts/eda_r2_deep.py`](01_eda/scripts/eda_r2_deep.py)
- [`01_eda/outputs/eda_summary.json`](01_eda/outputs/eda_summary.json)
- [`01_eda/plots/`](01_eda/plots/)

## Next Priority Action

Move to Phase 02 (Understanding): translate the +1000/day IPR drift, imbalance IC=0.65 signal, and recalibrated Kalman parameters into trading-rule consequences (signs, sizes, position-management implications).

## Deadline Risk

Unknown — round deadline not announced.
