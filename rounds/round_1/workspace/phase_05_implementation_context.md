# Phase 05 - Implementation Context

## Status

READY_FOR_REVIEW

## Owner / Reviewer

- Owner: Claude
- Reviewer: Bruno

## Last Updated

2026-04-16

## What Has Been Done

- Baseline bot `TEST1_merged.py` validated on platform: P&L 9,419 (run 190076, 1 day, no violations).
  - IPR: buy-max-long. Bought 80 units in 5 trades at t≈0. Held all day. Final pos +80.
  - ACO: fixed-FV market maker at 10,000. Final pos +44 (peaked at +65 intraday).
- Platform testing confirmed: buy-max-long for IPR outperforms drift-tracking market maker.
  - Drift gain = 80 × ~100 ticks ≈ 8,000. Drift-tracking MM would earn ~1,000–2,000 (spread-only).
  - Strategy candidates updated to reflect this correction.
- `candidate_03_combined.py` v2 written with improvements over baseline:
  - IPR: same buy-max-long logic (no change — already optimal).
  - ACO: `ACO_SKEW_FACTOR` raised 2 → 3. Baseline peaked at pos +65 (81% of limit); higher skew flattens inventory faster.
  - Removed `print()` statements and unused `_update_ema` helper.

## Current Findings

- Canonical bot: `rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`
- Baseline (TEST1_merged): P&L 9,419.
- Parameters in v2:
  - `ACO_FAIR_VALUE = 10000`, `ACO_HALF_SPREAD = 5`, `ACO_SKEW_FACTOR = 3`

## Decisions Made

- IPR drift-tracking market maker (original spec) discarded: confirmed by testing to earn less than buy-max-long.
- Buy-max-long is the correct IPR strategy for this product's drift magnitude.
- `TEST1_merged.py` in canonical/ is the validated backup.
- `candidate_03_combined.py` v2 is the target submission.

## Open Questions / Blockers

- **Human action needed:** Run `candidate_03_combined.py` on platform. Goal: beat baseline 9,419.
- Watch: does ACO end position drop below 44? Lower end position = skew improvement working.

## Linked Artifacts

- [`../bots/bruno/canonical/candidate_03_combined.py`](../bots/bruno/canonical/candidate_03_combined.py)
- [`../bots/bruno/canonical/TEST1_merged.py`](../bots/bruno/canonical/TEST1_merged.py)
- [`../performances/bruno/canonical/190076.json`](../performances/bruno/canonical/190076.json)

## Next Priority Action

1. **Human:** Upload `candidate_03_combined.py` to platform, run, share results.
2. **Agent:** Write run summary, update _index.md, start phase 07 if issues found.
