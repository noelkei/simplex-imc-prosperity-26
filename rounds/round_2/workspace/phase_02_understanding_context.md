# Phase 02 - Understanding Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Bruno (Claude session)
- Reviewer: Unassigned

## Last Updated

2026-04-19

## What Has Been Done

- Synthesised Round 2 EDA findings into per-product trading-rule consequences.
- Cross-referenced with Round 1 evidence (6 day-segments total for IPR drift; 6 for ACO anchoring).
- Quantified the directional vs market-making P&L comparison for IPR (~80,000 vs ~2,000 per day).
- Translated the deep-EDA microstructure finding (imbalance IC=+0.647) into a concrete strategy axis (skew gain).
- Re-evaluated Round 1 Kalman tuning vs Round 2 MLE: Q=0.005→0.09, R=25→6.75 (much more reactive filter).
- Ranked open questions and assigned each a priority + next-action.
- Drafted MAF bid game-theoretic recommendation (2,000-2,500 range).

Artifact: [`02_understanding.md`](02_understanding.md).

## Current Findings

- **IPR**: max-long is dominant. 6/6 day-segments confirm +1000/day drift.
- **ACO**: ~10000-anchored, 16-tick spread, **imbalance signal is the new high-value axis** (IC=0.65). Round 1 Kalman tuning is under-reactive vs MLE.
- **MAF**: bid 2,000-2,500 — top-50%-likely without burning value.
- **HMM**: ruled out (regimes too short-lived to be actionable).
- **Cross-asset**: no hedging signal (return correlation ≈ 0).

## Decisions Made

- Confirm max-long IPR as fixed strategy (do not spend candidate slots on alternatives).
- Treat imbalance gain and Kalman Q/R as the two main optimisation axes for ACO.
- Allocate 1 candidate slot to "baseline = R1 candidate_04 + bid()", and remaining slots to imbalance/Kalman variants.
- MAF bid range fixed to 2,000-2,500 across all candidates (low variance lever).

## Open Questions / Blockers

- Submission-day IPR drift uncertainty (deferred with risk).
- MAF participant median (no data; game-theoretic guess).
- Whether imbalance signal is already saturated in the live env (defer to Phase 06 testing).

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02_understanding.md`](02_understanding.md)
- [`01_eda/eda_round_2.md`](01_eda/eda_round_2.md)
- [`00_ingestion.md`](00_ingestion.md)

## Next Priority Action

Move to Phase 03 (Strategy Candidates): enumerate 3-5 candidate bots that vary along the imbalance-gain × Kalman-tuning × quote-sizing axes, with MAF bid fixed in 2,000-2,500.

## Deadline Risk

Unknown — round deadline not announced.
