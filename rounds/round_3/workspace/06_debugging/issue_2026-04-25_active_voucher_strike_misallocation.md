# Debug Issue

## Issue Metadata

- Issue ID: `R3-ISSUE-2026-04-25-active-voucher-strike-misallocation`
- Status: `IN_PROGRESS`
- Owner: amin
- Reviewer: Unassigned
- Round: `round_3`
- Candidate ID: `C06 / C04`

## Required Links

- Strategy spec: [`../04_strategy_specs/spec_c06_composite_base.md`](../04_strategy_specs/spec_c06_composite_base.md), [`../04_strategy_specs/spec_c06_composite_inv.md`](../04_strategy_specs/spec_c06_composite_inv.md)
- Performance run or validation artifact, paired raw JSON now archived under `historical/`: [`../../performances/amin/historical/candidate_c06_v01_centered_base.json`](../../performances/amin/historical/candidate_c06_v01_centered_base.json), [`../../performances/amin/historical/candidate_c06_composite_inv.json`](../../performances/amin/historical/candidate_c06_composite_inv.json), [`../06_testing/round_3_canonical_run_analysis.md`](../06_testing/round_3_canonical_run_analysis.md)
- Bot path: [`../../bots/amin/historical/candidate_c06_v01_centered_base.py`](../../bots/amin/historical/candidate_c06_v01_centered_base.py), [`../../bots/amin/historical/candidate_c06_composite_inv.py`](../../bots/amin/historical/candidate_c06_composite_inv.py)

## Reproduction Steps

1. Review the first live challenger runs for `candidate_c06_v01_centered_base.py` and `candidate_c06_composite_inv.py`.
2. Compare total PnL, active-voucher bucket PnL, per-strike attribution, and final positions.
3. Contrast those outcomes with the live logger market metrics from `baseline_state_logger.json`.

## Expected Behavior

- Expected: the corrected centered-residual base should improve on the historical frozen composite reference or at least isolate a cleaner active-voucher branch.
- Expected: the inventory variant should reduce the active-voucher failure mode if short/long concentration was the main issue.

## Observed Behavior

- Observed: the centered base lost `-3008.203`, worse than the frozen historical C06 reference `-1631.925`.
- Observed: the inventory variant lost `-5245.475`, materially worse than the centered base.
- Observed: both runs lost overwhelmingly through `VEV_5200`.
- Observed: `VEV_5300` stayed positive in both runs and `VELVETFRUIT_EXTRACT` stayed positive.
- Observed: the inventory variant reduced the final `VEV_5200` position but still worsened PnL, which suggests the current overlay is not solving the right problem.

## Classification

Choose one or more:

- weak strategy assumption
- execution tuning issue
- data/EDA gap

## Analysis

- Finding: active vouchers cannot currently be treated as one homogeneous `VEV_5000-5300` family on the live `TTE=5d` day.
- Finding: `VEV_5200` is the clearest strike-specific failure and should move from "included by default" to "must earn its way back."
- Finding: the live logger confirms that `VEV_5400/5500` are tradable enough to test, while `VEV_6000/6500` remain frozen and should stay outside the learning batch.
- Finding: the live intrinsic/extrinsic residual check says `VEV_4000/4500` still have the cleanest reversion, `VEV_5000` is weak but usable, and `VEV_5100/5200` are weak to non-reverting on this day.

## Fix Or Recommendation

- Recommendation: stop iterating broad composite voucher bots for now.
- Recommendation: shift to isolated learners by product and strike family.
- Recommendation: prioritize ITM learners, `5300` / upper-strike learners, and active subsets that exclude `5200`.
- Recommendation: treat stronger inventory overlays as secondary until the strike-selection problem is solved.

## Validation After Fix

- Check: run isolated HYDRO and VEX learners to refresh the delta-1 map.
- Check: run ITM-only, single-strike active, upper-strike, and surface-pair learners.
- Check: only reopen broad active-voucher composites after the isolated strike map is clearer.

## Next Action

- Next: create the learning-batch strategy matrix, generate the prioritized learner bot batch, and freeze the already-tested composite bots.
