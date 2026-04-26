# Round 3 Full Performance Synthesis

## Executive Verdict

This report now consolidates the **full current Round 3 evidence base**:
legacy runs, corrected challengers, the full 25-bot Wave 1 learner batch, the
full 19-bot Wave 2 batch, the full 24-bot Wave 3 batch, the full 12-bot Wave
4 finalist batch, and the currently available **7-run partial Wave 5 closeout
batch**.

- Total platform JSON artifacts analyzed: `101`.
- Wave 1 learner JSON artifacts analyzed: `25`.
- Wave 2 learner / control JSON artifacts analyzed: `19`.
- Wave 3 learner / winner-shaping JSON artifacts analyzed: `24`.
- Wave 4 finalist JSON artifacts analyzed: `12`.
- Wave 5 partial closeout JSON artifacts analyzed: `7`.
- Runs with usable `tradeHistory` execution detail from `.log`: `75`.
- Best overall tested run is now `W5-04` / `candidate_w5_04_delta1_kalman_fallback.json` at real platform PnL `1672.000`.
- Best Wave 2 run is `W2-04` / `candidate_w2_04_delta1_itm_overlay.json` at real platform PnL `872.653`.
- Best Wave 3 run is `W3-15` / `candidate_w3_15_delta1_kalman_control.json` at real platform PnL `1527.305`.
- Best Wave 4 run is `W4-03` / `candidate_w4_03_delta1_itm_kalman_stack.json` at real platform PnL `1606.305`.
- Best available Wave 5 run is `W5-04` / `candidate_w5_04_delta1_kalman_fallback.json` at real platform PnL `1672.000`.
- Runs with intra-run peak above `+5k`: `7`.
- Runs with intra-run peak above `+10k`: `5`.

### Bottom Line

1. **Wave 5 improved the fallback benchmark but did not reopen the architectural race**: `W5-04` is now the best pure `delta-1` control, while `W5-01` only reconfirms the already-known `W4-03` winner family rather than creating a new full-stack class.
2. **The strongest reliable full architecture remains `delta-1 + ITM` on top of the Kalman base**, with pure `delta-1` now the cleaner fallback benchmark than before.
3. **The old `>10k` and `~18k` paths still matter**, but now as a source of retention logic, strike pruning, and danger-signal framing, not as a reason to reopen the raw broad active basket.
4. **Round 3 should now be closed as a retrospective evidence source for Round 4**, not left in a pseudo-active “run one more batch” state.

## Updated Ranking Snapshot

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | delta1_total | itm_total | active_total | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W5-04 | candidate_w5_04_delta1_kalman_fallback | wave5_fallback_benchmark | 1672.000 | 2341.062 | -669.062 | 1672.000 | 0.000 | 0.000 | strong positive |
| W5-01 | candidate_w5_01_delta1_itm_final_control | wave5_winner_protection | 1606.305 | 2404.709 | -798.404 | 1527.305 | 79.000 | 0.000 | strong positive |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | wave4_itm_finalists | 1606.305 | 2404.709 | -798.404 | 1527.305 | 79.000 | 0.000 | strong positive |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | wave4_itm_finalists | 1604.305 | 2418.062 | -813.758 | 1527.305 | 77.000 | 0.000 | strong positive |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | wave4_5300_finalists | 1596.305 | 2410.062 | -813.758 | 1527.305 | 77.000 | -8.000 | strong positive |
| W3-15 | candidate_w3_15_delta1_kalman_control | wave3_delta1_controls | 1527.305 | 2341.062 | -813.758 | 1527.305 | 0.000 | 0.000 | strong positive |
| W4-01 | candidate_w4_01_delta1_kalman_control | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 1527.305 | 0.000 | 0.000 | strong positive |
| W4-02 | candidate_w4_02_delta1_kalman_retention | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 1527.305 | 0.000 | 0.000 | strong positive |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | wave4_peak_salvage | 1521.305 | 2335.062 | -813.758 | 1527.305 | 0.000 | -6.000 | strong positive |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | wave4_5300_finalists | 1511.305 | 2325.062 | -813.758 | 1527.305 | 0.000 | -16.000 | strong positive |
| W4-11 | candidate_w4_11_delta1_kalman_stress_control | wave4_delta1_finalists | 1455.767 | 2276.125 | -820.358 | 1455.767 | 0.000 | 0.000 | strong positive |
| B02-resid | r3_b02_itm_residual | legacy_itm_vex | 1409.371 | 2203.384 | -794.014 | 1211.906 | 197.464 | 0.000 | strong positive |
| W3-23 | candidate_w3_23_delta1_itm_active_combo | wave3_itm_and_stacks | 998.230 | 1286.763 | -288.533 | 919.230 | 79.000 | 0.000 | strong positive |
| W3-24 | candidate_w3_24_delta1_itm_5300_stack | wave3_itm_and_stacks | 960.925 | 1275.455 | -314.530 | 919.230 | 98.000 | -56.306 | strong positive |
| W3-01 | candidate_w3_01_delta1_dual_control | wave3_delta1_controls | 919.230 | 1223.117 | -303.887 | 919.230 | 0.000 | 0.000 | strong positive |

### Ranking Reading

- `W3-15` at `1527.305` remains the best clean architectural result in the whole round unless Wave 4 overtook it.
- `W4-01` at `1527.305` tells us whether the pure champion survived translation into finalist form.
- `W4-03` at `1606.305` and `W4-04` at `1604.305` decide whether active ITM deserves final-bot promotion on top of the stronger Kalman base.
- `W4-05/W4-06/W4-07/W4-08/W4-09/W4-12` decide whether any `5300` branch still merits a final slot or whether it stays only as a salvage research branch.

## What Wave 4 Changed

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | delta1_total | itm_total | active_total | cf_gain_vs_final_retain_75 | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | wave4_itm_finalists | 1606.305 | 2404.709 | -798.404 | 1527.305 | 79.000 | 0.000 | 185.133 | strong positive |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | wave4_itm_finalists | 1604.305 | 2418.062 | -813.758 | 1527.305 | 77.000 | 0.000 | 185.133 | strong positive |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | wave4_5300_finalists | 1596.305 | 2410.062 | -813.758 | 1527.305 | 77.000 | -8.000 | 185.133 | strong positive |
| W4-01 | candidate_w4_01_delta1_kalman_control | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 1527.305 | 0.000 | 0.000 | 227.629 | strong positive |
| W4-02 | candidate_w4_02_delta1_kalman_retention | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 1527.305 | 0.000 | 0.000 | 227.629 | strong positive |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | wave4_peak_salvage | 1521.305 | 2335.062 | -813.758 | 1527.305 | 0.000 | -6.000 | 227.629 | strong positive |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | wave4_5300_finalists | 1511.305 | 2325.062 | -813.758 | 1527.305 | 0.000 | -16.000 | 227.629 | strong positive |
| W4-11 | candidate_w4_11_delta1_kalman_stress_control | wave4_delta1_finalists | 1455.767 | 2276.125 | -820.358 | 1455.767 | 0.000 | 0.000 | 235.444 | strong positive |
| W4-10 | candidate_w4_10_5100_inverse_forced | wave4_inverse_closure | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | near flat |
| W4-08 | candidate_w4_08_5300_peak_salvage | wave4_peak_salvage | -12.000 | 0.000 | -12.000 | 0.000 | 0.000 | -12.000 | 0.000 | near flat |
| W4-05 | candidate_w4_05_5300_selective_control | wave4_5300_finalists | -91.000 | 0.000 | -91.000 | 0.000 | 0.000 | -91.000 | 0.000 | mild negative |
| W4-12 | candidate_w4_12_5300_trend_comparator | wave4_5300_finalists | -107.000 | 43.039 | -150.039 | 0.000 | 0.000 | -107.000 | 136.613 | mild negative |

### Wave 4 Reading

- Pure champion control:
  - `W3-15 = 1527.305`
  - `W4-01 = 1527.305`
  - `W4-02 = 1527.305`
  This tells us whether the best clean architecture is stable under one more implementation pass and whether a light retention gate helps or hurts.
- Champion plus ITM:
  - `W3-23 = 998.230`
  - `W4-03 = 1606.305`
  - `W4-04 = 1604.305`
  This is the cleanest test of whether ITM still adds on top of the stronger Kalman champion, not just on top of the older Wave 3 control.
- Selective `5300` finalists:
  - `W3-17 = 353.150`
  - `W4-05 = -91.000`
  - `W4-06 = 1511.305`
  - `W4-07 = 1596.305`
  - `W4-12 = -107.000`
  These decide whether `5300` survives only as a standalone selective micro-branch, as a true overlay, or not at all.
- Distilled peak-salvage attempts:
  - `W4-08 = -12.000`
  - `W4-09 = 1521.305`
  These are the first serious attempts to harvest old `>10k` logic in a pruned, shutdown-driven form.
- Inverse closure:
  - `W4-10 = 0.000`
  This is only useful if it truly traded `VEV_5100`; otherwise it should be treated as closure evidence, not as a living final branch.

## What Partial Wave 5 Changed

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | delta1_total | itm_total | active_total | cf_gain_vs_final_retain_75 | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W5-04 | candidate_w5_04_delta1_kalman_fallback | wave5_fallback_benchmark | 1672.000 | 2341.062 | -669.062 | 1672.000 | 0.000 | 0.000 | 0.000 | strong positive |
| W5-01 | candidate_w5_01_delta1_itm_final_control | wave5_winner_protection | 1606.305 | 2404.709 | -798.404 | 1527.305 | 79.000 | 0.000 | 185.133 | strong positive |
| W5-03 | candidate_w5_03_delta1_itm_early_stop | wave5_winner_protection | 615.000 | 937.418 | -322.418 | 679.000 | -64.000 | 0.000 | 69.359 | strong positive |
| W5-02 | candidate_w5_02_delta1_itm_retention_lock | wave5_winner_protection | 518.000 | 706.117 | -188.117 | 634.000 | -116.000 | 0.000 | 0.516 | strong positive |
| W5-11 | candidate_w5_11_5300_toxic_veto | wave5_toxic_signal | 476.000 | 517.992 | -41.992 | 512.000 | 0.000 | -36.000 | 0.000 | positive |
| W5-09 | candidate_w5_09_winner_plus_tiny_trio | wave5_upside_distillation | 368.902 | 603.586 | -234.684 | 449.902 | -50.000 | -31.000 | 66.730 | positive |
| W5-08 | candidate_w5_08_vex_crossstrike_salvage | wave5_upside_distillation | 358.000 | 393.994 | -35.994 | 404.000 | 0.000 | -46.000 | 0.000 | positive |

### Wave 5 Reading

- Wave 5 was only observed partially (`7/12` JSONs), but it is enough to close the round's last open strategic loop.
- `W5-01`, `W5-02`, and `W5-03` tell us whether winner protection changes anything material once the clean winner family is already known.
- `W5-04` keeps the pure fallback benchmark in the comparison set so the round still distinguishes “best clean base” from “best full stack”.
- `W5-08` and `W5-09` are the only observed upside-distillation descendants with real platform evidence in this partial batch.
- `W5-11` is the only observed toxic-strike-as-signal run and therefore the direct empirical read on whether `5100/5200` are better as veto inputs than as normal inventory legs.
- No observed Wave 5 run currently justifies reopening round execution; the partial evidence is enough to collapse the open design space into documented lessons, untested backlog, and anti-patterns.

## Wave 5 Decision Board

Promote count: `2`. Research-only count: `3`. Close count: `2`.

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | delta1_total | itm_total | active_total | final_active_position_abs | cf_gain_vs_final_retain_75 | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W5-04 | candidate_w5_04_delta1_kalman_fallback | wave5_fallback_benchmark | 1672.000 | 2341.062 | -669.062 | 1672.000 | 0.000 | 0.000 | 0 | 0.000 | promote |
| W5-01 | candidate_w5_01_delta1_itm_final_control | wave5_winner_protection | 1606.305 | 2404.709 | -798.404 | 1527.305 | 79.000 | 0.000 | 0 | 185.133 | promote |
| W5-11 | candidate_w5_11_5300_toxic_veto | wave5_toxic_signal | 476.000 | 517.992 | -41.992 | 512.000 | 0.000 | -36.000 | 0 | 0.000 | research_only |
| W5-09 | candidate_w5_09_winner_plus_tiny_trio | wave5_upside_distillation | 368.902 | 603.586 | -234.684 | 449.902 | -50.000 | -31.000 | 0 | 66.730 | research_only |
| W5-08 | candidate_w5_08_vex_crossstrike_salvage | wave5_upside_distillation | 358.000 | 393.994 | -35.994 | 404.000 | 0.000 | -46.000 | 0 | 0.000 | research_only |
| W5-03 | candidate_w5_03_delta1_itm_early_stop | wave5_winner_protection | 615.000 | 937.418 | -322.418 | 679.000 | -64.000 | 0.000 | 0 | 69.359 | close |
| W5-02 | candidate_w5_02_delta1_itm_retention_lock | wave5_winner_protection | 518.000 | 706.117 | -188.117 | 634.000 | -116.000 | 0.000 | 0 | 0.516 | close |

### Wave 5 Decision Reading

- **Promote** means “retain as final retrospective winner evidence”.
- **Research-only** means “the idea remains informative, but only as a carry-forward hypothesis or design lesson”.
- **Close** means “do not treat this branch as still active in Round 3”.

## Retrospective Structural Audit

### Moneyness Role Summary

| role | products | runs_with_activity | mean_family_pnl | best_family_pnl | worst_family_pnl |
| --- | --- | --- | --- | --- | --- |
| delta1_base | HYDROGEL_PACK,VELVETFRUIT_EXTRACT | 54 | -216.874 | 1672.000 | -22856.344 |
| itm_structural | VEV_4000,VEV_4500 | 17 | 55.807 | 318.797 | -116.000 |
| active_zone | VEV_5000,VEV_5100,VEV_5200,VEV_5300 | 55 | -2043.319 | 852.269 | -10739.712 |
| upper_execution_passive | VEV_5400,VEV_5500 | 8 | -446.345 | 1.798 | -1841.891 |
| floor_monitor | VEV_6000,VEV_6500 | 0 |  | 0.000 | 0.000 |

### Cross-Strike Context Around `5300`

| short_id | stem | analysis_bucket | profit | pnl_VEV_5100 | pnl_VEV_5200 | pnl_VEV_5300 | toxic_pair_total | path_end_from_peak | supports_5300_trade |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L27 | probe_l27_surface_5300_5400_relval | wave1_surface | -989.622 | 0.000 | 0.000 | 852.269 | 0.000 | -1040.340 | yes |
| C06-base-v01 | candidate_c06_v01_centered_base | corrected_and_legacy_composites | -3008.203 | -110.790 | -4040.363 | 497.822 | -4151.153 | -3801.741 | mixed |
| L26 | probe_l26_surface_5200_5300_relval | wave1_surface | -10739.712 | 0.000 | -11205.903 | 466.192 | -11205.903 | -10739.712 | mixed |
| C06-inv-v01 | candidate_c06_composite_inv | corrected_and_legacy_composites | -5245.475 | -218.538 | -6058.820 | 383.569 | -6277.359 | -5245.475 | mixed |
| W3-17 | candidate_w3_17_5300_imbalance_filter | wave3_active_rescue_and_filters | 353.150 | 0.000 | 0.000 | 353.150 | 0.000 | -232.770 | yes |
| L20 | probe_l20_active_5000_5300_inventory | wave1_active | -1443.986 | 0.000 | 0.000 | 182.966 | 0.000 | -3119.134 | yes |
| W3-11 | candidate_w3_11_5300_trend_gate | wave3_active_rescue_and_filters | 165.083 | 0.000 | 0.000 | 165.083 | 0.000 | -358.247 | yes |
| B03-pure | r3_b03_voucher_pure | legacy_active_vouchers | -2261.849 | -525.648 | -519.322 | 87.185 | -1044.971 | -14801.725 | mixed |
| B06-tte | r3_b06_tte_cautious | legacy_active_vouchers | -752.886 | -724.707 | -701.262 | 80.583 | -1425.969 | -12478.663 | mixed |
| B08-regime | r3_b08_regime_composite | legacy_active_vouchers | -1501.925 | -724.707 | -701.262 | 80.583 | -1425.969 | -18980.139 | mixed |
| C06-legacy | candidate_c06_composite_base | corrected_and_legacy_composites | -1631.925 | -724.707 | -701.262 | 80.583 | -1425.969 | -18980.139 | mixed |
| B04-surf | r3_b04_full_surface | legacy_active_vouchers | -2561.846 | -724.707 | -701.262 | 80.583 | -1425.969 | -18400.339 | mixed |
| B05-adv | r3_b05_composite_advanced | legacy_active_vouchers | -25333.769 | -724.707 | -701.262 | 80.583 | -1425.969 | -25333.769 | mixed |
| B07-hedge | r3_b07_delta_hedge | legacy_active_vouchers | -1275.997 | 121.293 | 383.738 | 80.583 | 505.031 | -10292.923 | yes |
| W3-05 | candidate_w3_05_5300_giveback_halt | wave3_active_rescue_and_filters | 35.000 | 0.000 | 0.000 | 35.000 | 0.000 | -97.853 | yes |

### Portfolio Exposure Summary

| analysis_bucket | runs | mean_final_active_position_abs | max_final_active_position_abs | mean_final_itm_position_abs | mean_active_limit_hits | mean_path_end_from_peak | mean_active_total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| legacy_active_vouchers | 6 | 1071.833 | 1200 | 10.333 | 2.833 | -16714.593 | -1954.628 |
| corrected_and_legacy_composites | 3 | 640.667 | 1200 | 0.000 | 1.333 | -9342.452 | -3894.701 |
| wave1_active | 10 | 282.800 | 515 | 0.000 | 0.000 | -5780.676 | -4122.813 |
| wave2_active_clean_retests | 2 | 93.500 | 97 | 0.000 | 0.000 | -1269.083 | -866.087 |
| wave3_active_rescue_and_filters | 12 | 34.167 | 65 | 0.000 | 0.000 | -801.927 | -616.208 |
| wave2_active_rescue | 7 | 22.857 | 80 | 0.000 | 0.000 | -3325.900 | -3266.591 |
| wave1_surface | 2 | 9.500 | 17 | 0.000 | 0.000 | -5890.026 | -4943.721 |
| wave3_itm_and_stacks | 3 | 6.667 | 20 | 0.000 | 0.000 | -209.431 | -18.769 |
| wave5_toxic_signal | 1 | 0.000 | 0 | 0.000 | 0.000 | -41.992 | -36.000 |
| wave5_fallback_benchmark | 1 | 0.000 | 0 | 0.000 | 0.000 | -669.062 | 0.000 |
| wave4_peak_salvage | 2 | 0.000 | 0 | 0.000 | 0.000 | -412.879 | -9.000 |
| wave3_delta1_controls | 3 | 0.000 | 0 | 0.000 | 0.000 | -503.708 | 0.000 |
| wave5_upside_distillation | 2 | 0.000 | 0 | 0.000 | 0.000 | -135.339 | -38.500 |
| wave4_inverse_closure | 1 | 0.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave4_delta1_finalists | 3 | 0.000 | 0 | 0.000 | 0.000 | -815.958 | 0.000 |
| wave4_5300_finalists | 4 | 0.000 | 0 | 0.000 | 0.000 | -467.139 | -55.500 |
| wave3_inverse_tiny | 3 | 0.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave3_inverse_sidecars | 3 | 0.000 | 0 | 0.000 | 0.000 | -15.383 | 0.000 |
| wave4_itm_finalists | 2 | 0.000 | 0 | 0.000 | 0.000 | -806.081 | 0.000 |
| wave2_toxic_rescue | 2 | 0.000 | 0 | 0.000 | 0.000 | -515.507 | -844.000 |
| wave2_upper_refinement | 2 | 0.000 | 0 | 0.000 | 0.000 | -4.461 | 0.000 |
| diagnostic | 1 | 0.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_itm_passive | 1 | 0.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_floor_probe | 1 | 0.000 | 0 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_delta1_controls | 3 | 0.000 | 0 | 0.000 | 0.000 | -393.984 | 0.000 |
| wave2_active_upper_bridge | 1 | 0.000 | 0 | 0.000 | 0.000 | -3763.202 | -3765.000 |
| wave1_upper | 4 | 0.000 | 0 | 0.000 | 0.000 | -874.025 | 0.000 |
| wave1_itm | 4 | 0.000 | 0 | 3.000 | 0.000 | -180.794 | 0.000 |
| wave1_delta1 | 5 | 0.000 | 0 | 0.000 | 0.000 | -508.066 | 0.000 |
| legacy_itm_vex | 2 | 0.000 | 0 | 12.000 | 0.000 | -397.007 | 0.000 |
| legacy_delta1 | 2 | 0.000 | 0 | 0.000 | 0.000 | -15912.184 | 0.000 |
| wave5_winner_protection | 3 | 0.000 | 0 | 0.000 | 0.000 | -436.313 | 0.000 |

### Late-Entry / Post-Peak Churn Summary

| analysis_bucket | runs | mean_post_peak_ratio | mean_post_peak_trades | mean_peak_time_frac | mean_end_from_peak | early_peak_flag_rate |
| --- | --- | --- | --- | --- | --- | --- |
| wave2_active_upper_bridge | 1 | 1.000 | 505.000 | 0.000 | -3763.202 | 0.000 |
| wave1_surface | 2 | 0.973 | 457.000 | 0.013 | -5890.026 | 0.000 |
| wave2_toxic_rescue | 2 | 0.968 | 204.500 | 0.056 | -515.507 | 0.000 |
| wave2_active_rescue | 7 | 0.900 | 422.571 | 0.067 | -3325.900 | 0.286 |
| corrected_and_legacy_composites | 2 | 0.732 | 280.000 | 0.298 | -4523.608 | 0.000 |
| wave2_active_clean_retests | 2 | 0.675 | 183.000 | 0.216 | -1269.083 | 1.000 |
| wave1_upper | 3 | 0.556 | 249.667 | 0.260 | -1165.366 | 0.000 |
| wave4_peak_salvage | 2 | 0.556 | 4.000 | 0.456 | -412.879 | 0.000 |
| wave3_active_rescue_and_filters | 12 | 0.528 | 138.750 | 0.350 | -801.927 | 0.250 |
| wave1_active | 10 | 0.504 | 265.700 | 0.415 | -5780.676 | 0.100 |
| wave4_5300_finalists | 4 | 0.481 | 10.250 | 0.461 | -467.139 | 0.000 |
| wave1_itm | 4 | 0.286 | 8.000 | 0.560 | -180.794 | 0.000 |
| wave2_delta1_controls | 3 | 0.264 | 4.667 | 0.789 | -393.984 | 0.000 |
| wave2_upper_refinement | 2 | 0.250 | 0.500 | 0.792 | -4.461 | 0.000 |
| wave3_itm_and_stacks | 3 | 0.183 | 21.333 | 0.778 | -209.431 | 0.000 |
| wave3_delta1_controls | 3 | 0.128 | 5.667 | 0.912 | -503.708 | 0.000 |
| wave4_delta1_finalists | 3 | 0.122 | 5.000 | 0.912 | -815.958 | 0.000 |
| wave1_delta1 | 5 | 0.071 | 2.000 | 0.940 | -508.066 | 0.000 |
| wave4_itm_finalists | 2 | 0.066 | 6.000 | 0.912 | -806.081 | 0.000 |
| wave3_inverse_sidecars | 3 | 0.000 | 0.000 | 0.979 | -15.383 | 0.000 |

### Structural Audit Reading

- `delta1_base` is the only family that stays robust across path quality, final PnL, and long-horizon markouts.
- `itm_structural` behaves much more like a controlled additive overlay than like a standalone engine.
- `active_zone` still contains the largest upside and the worst giveback at the same time, which is why it must be read as a regime-sensitive option book, not as a homogeneous asset basket.
- `VEV_5100/5200` remain more useful as cross-strike context and danger signals than as default direct trading legs.
- Post-peak churn remains concentrated in active-voucher families, which strengthens the carry-forward case for no-new-entry windows, cooldowns, and hard flatten rules.

## Path Quality Summary

- Runs with a positive intra-run peak above `100` that still finished negative:
  `30` / `101`.
- Runs with a strong intra-run peak above `500` that still finished negative:
  `17` / `101`.
- Runs that still look like strong no-trade / shutdown candidates because they peaked early and kept trading afterwards:
  `8`.

| analysis_bucket | runs | mean_final_profit | mean_path_peak | median_path_peak | mean_peak_time_frac | mean_end_from_peak | mean_path_max_drawdown | mean_positive_time_ratio | positive_peak_negative_finish_rate | big_peak_negative_finish_rate | early_peak_post_trade_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy_active_vouchers | 6 | -5614.712 | 11099.881 | 12132.826 | 0.498 | -16714.593 | -24780.181 | 0.349 | 0.833 | 0.833 | 0.000 |
| corrected_and_legacy_composites | 3 | -3295.201 | 6047.251 | 793.538 | 0.398 | -9342.452 | -12891.895 | 0.290 | 0.667 | 0.667 | 0.000 |
| legacy_delta1 | 2 | -13408.434 | 2503.750 | 2503.750 | 0.171 | -15912.184 | -19597.688 | 0.151 | 0.500 | 0.500 | 0.000 |
| wave4_itm_finalists | 2 | 1605.305 | 2411.386 | 2411.386 | 0.912 | -806.081 | -1135.359 | 0.953 | 0.000 | 0.000 | 0.000 |
| wave5_fallback_benchmark | 1 | 1672.000 | 2341.062 | 2341.062 | 0.912 | -669.062 | -1055.648 | 0.899 | 0.000 | 0.000 | 0.000 |
| wave4_delta1_finalists | 3 | 1503.459 | 2319.417 | 2341.062 | 0.912 | -815.958 | -1055.757 | 0.899 | 0.000 | 0.000 | 0.000 |
| wave1_active | 10 | -4089.567 | 1691.109 | 1786.306 | 0.415 | -5780.676 | -6578.888 | 0.356 | 0.700 | 0.700 | 0.100 |
| wave3_delta1_controls | 3 | 1117.391 | 1621.099 | 1299.117 | 0.912 | -503.708 | -817.656 | 0.897 | 0.000 | 0.000 | 0.000 |
| legacy_itm_vex | 2 | 1068.132 | 1465.138 | 1465.138 | 0.671 | -397.007 | -2886.430 | 0.837 | 0.000 | 0.000 | 0.000 |
| wave5_winner_protection | 3 | 913.102 | 1349.415 | 937.418 | 0.912 | -436.313 | -769.002 | 0.769 | 0.000 | 0.000 | 0.000 |
| wave4_5300_finalists | 4 | 727.402 | 1194.541 | 1184.051 | 0.461 | -467.139 | -611.382 | 0.657 | 0.000 | 0.000 | 0.000 |
| wave4_peak_salvage | 2 | 754.652 | 1167.531 | 1167.531 | 0.456 | -412.879 | -535.020 | 0.446 | 0.000 | 0.000 | 0.000 |
| wave2_delta1_controls | 3 | 698.436 | 1092.419 | 1364.539 | 0.789 | -393.984 | -817.188 | 0.848 | 0.000 | 0.000 | 0.000 |
| wave1_delta1 | 5 | 547.158 | 1055.223 | 1254.016 | 0.940 | -508.066 | -659.674 | 0.809 | 0.000 | 0.000 | 0.000 |
| wave3_itm_and_stacks | 3 | 786.256 | 995.687 | 1275.455 | 0.778 | -209.431 | -722.945 | 0.908 | 0.000 | 0.000 | 0.000 |
| wave5_toxic_signal | 1 | 476.000 | 517.992 | 517.992 | 0.979 | -41.992 | -265.445 | 0.775 | 0.000 | 0.000 | 0.000 |
| wave5_upside_distillation | 2 | 363.451 | 498.790 | 498.790 | 0.945 | -135.339 | -310.469 | 0.529 | 0.000 | 0.000 | 0.000 |
| wave1_upper | 4 | -383.811 | 490.214 | 496.305 | 0.195 | -874.025 | -1353.143 | 0.233 | 0.500 | 0.500 | 0.000 |
| wave2_active_clean_retests | 2 | -866.087 | 402.996 | 402.996 | 0.216 | -1269.083 | -1533.740 | 0.490 | 1.000 | 0.000 | 1.000 |
| wave3_active_rescue_and_filters | 12 | -439.465 | 362.463 | 306.980 | 0.350 | -801.927 | -1015.493 | 0.598 | 0.500 | 0.000 | 0.250 |
| wave3_inverse_sidecars | 3 | 334.613 | 349.996 | 349.996 | 0.979 | -15.383 | -312.695 | 0.673 | 0.000 | 0.000 | 0.000 |
| wave1_itm | 4 | 78.383 | 259.178 | 253.771 | 0.560 | -180.794 | -278.867 | 0.477 | 0.750 | 0.000 | 0.000 |
| wave2_upper_refinement | 2 | 177.414 | 181.875 | 181.875 | 0.792 | -4.461 | -241.972 | 0.597 | 0.000 | 0.000 | 0.000 |
| wave2_active_rescue | 7 | -3216.415 | 109.485 | 0.000 | 0.067 | -3325.900 | -3411.559 | 0.171 | 0.286 | 0.000 | 0.286 |
| wave1_surface | 2 | -5864.667 | 25.359 | 25.359 | 0.013 | -5890.026 | -6311.951 | 0.009 | 0.000 | 0.000 | 0.000 |
| wave2_toxic_rescue | 2 | -492.769 | 22.738 | 22.738 | 0.056 | -515.507 | -753.636 | 0.019 | 0.000 | 0.000 | 0.000 |
| wave4_inverse_closure | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| diagnostic | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_itm_passive | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_floor_probe | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave2_active_upper_bridge | 1 | -3763.202 | 0.000 | 0.000 | 0.000 | -3763.202 | -3826.162 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave3_inverse_tiny | 3 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

### Path Reading

- `wave5_winner_protection` confirms the winner family but does not materially expand the upside ceiling.
- `wave5_fallback_benchmark` keeps the round honest about what is genuine voucher value-add versus what is simply the strong base carrying everything.
- `wave5_upside_distillation` stays valuable as a design laboratory, but not as grounds for more active Round 3 execution.
- The old `legacy_active_vouchers` bucket still owns the giant peaks, but also the giant collapses. That is now a retrospective lesson, not a live opportunity queue.

## All Round 3 Runs With Peak Above `+10k`

This section applies to **all of Round 3**, not only Wave 3.

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | cf_exit_dd_2000 | cf_exit_retain_75 | cf_gain_vs_final_dd_2000 | cf_gain_vs_final_retain_75 | delta1_total | active_total | path_shape |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B08-regime | r3_b08_regime_composite | legacy_active_vouchers | -1501.925 | 17478.214 | -18980.139 | 15203.195 | 12315.540 | 16705.120 | 13817.464 | 599.500 | -2101.425 | edge_then_major_reversal |
| C06-legacy | candidate_c06_composite_base | corrected_and_legacy_composites | -1631.925 | 17348.214 | -18980.139 | 15073.195 | 12185.540 | 16705.120 | 13817.464 | 599.500 | -2231.425 | edge_then_major_reversal |
| B04-surf | r3_b04_full_surface | legacy_active_vouchers | -2561.846 | 15838.493 | -18400.339 | 13731.161 | 11852.825 | 16293.007 | 14414.671 | 599.500 | -3281.120 | edge_then_major_reversal |
| B03-pure | r3_b03_voucher_pure | legacy_active_vouchers | -2261.849 | 12539.876 | -14801.725 | 9876.368 | 9248.416 | 12138.217 | 11510.265 | 0.000 | -2261.849 | edge_then_major_reversal |
| B06-tte | r3_b06_tte_cautious | legacy_active_vouchers | -752.886 | 11725.777 | -12478.663 | 9474.472 | 8368.391 | 10227.358 | 9121.277 | 599.500 | -1352.386 | edge_then_major_reversal |

### `>10k` Reading

- All current `>10k` peak runs belong to the old legacy / broad active-voucher world. **No Wave 3, Wave 4, or observed partial Wave 5 bot got there**.
- The partial Wave 5 closeout is therefore enough to say that the round's final observed winner family is the clean one, while the giant-peak family survives only as a retrospective source of design lessons.
- That does **not** mean the upside was fake. It means the upside was being harvested in a branch that had terrible retention and product selection.
- The simple counterfactuals are huge:
  - `B08-regime`: `+16.7k` versus final under a `2k` giveback stop proxy.
  - `C06-legacy`: `+16.7k` versus final under the same proxy.
  - `B04-surf`: `+16.3k`.
  - `B03-pure`: `+12.1k`.
  - `B06-tte`: `+10.2k`.
- So the correct read is **not** “those big-peak branches are ready to promote”. The correct read is “they contained real upside, but packaged in the wrong basket, the wrong strikes, and the wrong continuation logic”.

## Which Products Created And Destroyed Those `>10k` Peaks

| product | runs | total_peak_pnl | total_final_pnl | total_giveback | mean_giveback |
| --- | --- | --- | --- | --- | --- |
| VEV_5100 | 5 | 24109.652 | -3424.477 | -27534.129 | -5506.826 |
| VEV_5000 | 5 | 17700.449 | -4888.875 | -22589.324 | -4517.865 |
| VEV_5200 | 5 | 18126.867 | -3324.369 | -21451.236 | -4290.247 |
| VEV_5300 | 5 | 13120.196 | 409.517 | -12710.680 | -2542.136 |
| VEV_5400 | 5 | 1184.014 | -54.231 | -1238.245 | -247.649 |
| VEV_5500 | 5 | 364.036 | -144.792 | -508.828 | -101.766 |
| VEV_6000 | 5 | 0.000 | 0.000 | 0.000 | 0.000 |
| VEV_6500 | 5 | 0.000 | 0.000 | 0.000 | 0.000 |

### Product Reading

- The `>10k` runs were overwhelmingly created and destroyed by the active voucher cluster.
- `VEV_5100`, `VEV_5200`, and `VEV_5000` are still the biggest giveback drivers in the giant-peak set.
- `VEV_5300` also gives back heavily, but it remains materially less toxic than the other active strikes.
- `VELVETFRUIT_EXTRACT` continues to look more like a stabilizer / anchor than the main destroyer.
- The practical implication for carry-forward work is that any future upside push should be **VEX-anchored and strike-pruned**, with continuation limits, rather than voucher-led and basket-wide.

## No-Trade / Shutdown Candidates

| short_id | stem | analysis_bucket | profit | path_peak | path_peak_time_frac | path_end_from_peak | own_trades | post_peak_trades | post_peak_ratio | mean_markout_10000_unit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L16 | probe_l16_active_5000_5300_residual | wave1_active | -1837.049 | 2042.844 | 0.236 | -3879.893 | 676 | 406 | 0.601 | 0.767 |
| W2-09 | candidate_w2_09_5300_late_flatten | wave2_active_rescue | -291.222 | 472.030 | 0.234 | -763.252 | 234 | 151 | 0.645 | 0.732 |
| W2-05 | candidate_w2_05_5300_bachelier_selective | wave2_active_clean_retests | -395.875 | 450.030 | 0.234 | -845.905 | 232 | 152 | 0.655 | 0.699 |
| W3-04 | candidate_w3_04_5300_early_window | wave3_active_rescue_and_filters | -215.243 | 408.151 | 0.234 | -623.394 | 233 | 146 | 0.627 | 0.727 |
| W2-06 | candidate_w2_06_5000_5300_bachelier_selective | wave2_active_clean_retests | -1336.299 | 355.961 | 0.198 | -1692.261 | 308 | 214 | 0.695 | 0.313 |
| W2-10 | candidate_w2_10_5000_5300_late_flatten | wave2_active_rescue | -976.913 | 294.367 | 0.234 | -1271.281 | 282 | 184 | 0.652 | 0.311 |
| W3-07 | candidate_w3_07_5300_slow_hold | wave3_active_rescue_and_filters | -2468.000 | 118.083 | 0.025 | -2586.083 | 344 | 328 | 0.953 | -0.351 |
| W3-16 | candidate_w3_16_5300_kalman_anchor | wave3_active_rescue_and_filters | -2116.539 | 101.313 | 0.025 | -2217.852 | 352 | 338 | 0.960 | -0.183 |

### No-Trade Reading

- The selective active-voucher runs still peak much earlier than they stop trading.
- The strongest current implication is that **new-entry shutdown, time-window control, and giveback discipline** remain the most valuable rescue axes for any remaining `5300` work.

## Execution Markout Evidence By Product

| product | trades | mean_entry_edge_unit | mean_markout_1000_unit | mean_markout_5000_unit | mean_markout_10000_unit |
| --- | --- | --- | --- | --- | --- |
| HYDROGEL_PACK | 277 | 6.758 | 6.671 | 6.810 | 9.954 |
| VELVETFRUIT_EXTRACT | 1023 | 1.504 | 1.579 | 1.591 | 3.311 |
| VEV_4000 | 207 | -4.007 | 0.814 | 1.763 | 1.251 |
| VEV_4500 | 207 | -3.130 | 0.684 | 1.649 | 1.090 |
| VEV_5000 | 598 | -2.509 | -1.881 | -2.286 | -2.284 |
| VEV_5100 | 498 | -2.414 | -2.489 | -3.175 | -3.502 |
| VEV_5200 | 1224 | -1.573 | -1.590 | -2.632 | -3.665 |
| VEV_5300 | 11852 | -1.148 | -1.077 | -0.456 | 0.388 |
| VEV_5400 | 949 | -0.692 | -0.497 | -0.294 | -0.015 |
| VEV_5500 | 628 | -0.551 | -0.400 | -0.400 | 0.161 |

### Markout Reading

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` remain clean at every horizon.
- `VEV_4000/4500` are slightly awkward on entry but fine by `10k`, which matches the new “ITM as small overlay” thesis.
- `VEV_5300` is still the only active strike with a **positive `10k` mean markout** (`0.388`).
- `VEV_5000`, `VEV_5100`, and `VEV_5200` remain negative at `10k`, with `5200` worst on aggregate.
- `VEV_5400` is almost flat by `10k`, and `VEV_5500` slightly positive, but those branches are still low-ROI relative to the main decision axes.

## Focus Comparison: Champion Base, ITM Overlay, `5300`, And Inverse Branches

| short_id | stem | product | trades | mean_entry_edge_unit | mean_markout_1000_unit | mean_markout_5000_unit | mean_markout_10000_unit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| W3-15 | candidate_w3_15_delta1_kalman_control | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W3-15 | candidate_w3_15_delta1_kalman_control | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W3-23 | candidate_w3_23_delta1_itm_active_combo | HYDROGEL_PACK | 14 | 7.000 | 7.143 | 7.577 | 10.500 |
| W3-23 | candidate_w3_23_delta1_itm_active_combo | VELVETFRUIT_EXTRACT | 31 | 1.500 | 1.694 | 1.603 | 2.815 |
| W3-23 | candidate_w3_23_delta1_itm_active_combo | VEV_4000 | 25 | -2.920 | 1.460 | 2.167 | 1.521 |
| W3-23 | candidate_w3_23_delta1_itm_active_combo | VEV_4500 | 25 | -2.320 | 1.140 | 1.938 | 1.271 |
| W4-01 | candidate_w4_01_delta1_kalman_control | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-01 | candidate_w4_01_delta1_kalman_control | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-02 | candidate_w4_02_delta1_kalman_retention | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-02 | candidate_w4_02_delta1_kalman_retention | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | VEV_4000 | 25 | -2.920 | 1.460 | 2.167 | 1.521 |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | VEV_4500 | 25 | -2.320 | 1.140 | 1.938 | 1.271 |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | VEV_4000 | 23 | -4.000 | 0.848 | 1.935 | 1.391 |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | VEV_4500 | 23 | -3.130 | 0.717 | 1.804 | 1.196 |
| W4-05 | candidate_w4_05_5300_selective_control | VEV_5300 | 15 | -1.067 | -0.167 | -1.133 | -0.600 |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | VEV_5300 | 5 | -1.100 | -1.100 | -1.800 | -1.900 |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | VEV_4000 | 23 | -4.000 | 0.848 | 1.935 | 1.391 |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | VEV_4500 | 23 | -3.130 | 0.717 | 1.804 | 1.196 |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | VEV_5300 | 5 | -1.100 | -1.100 | -1.800 | -1.900 |
| W4-08 | candidate_w4_08_5300_peak_salvage | VEV_5300 | 3 | -1.000 | -2.000 | 1.000 | -1.667 |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | HYDROGEL_PACK | 14 | 7.000 | 6.857 | 6.038 | 9.417 |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | VELVETFRUIT_EXTRACT | 28 | 1.607 | 1.714 | 2.038 | 4.560 |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | VEV_5300 | 3 | -1.000 | -2.000 | 1.000 | -1.667 |
| W4-12 | candidate_w4_12_5300_trend_comparator | VEV_5300 | 21 | -1.119 | -0.310 | -0.167 | -1.048 |

### Focus Reading

- `W4-01` and `W4-02` show whether the champion remains strong without leaning on any voucher branch.
- `W4-03` and `W4-04` show whether ITM still adds cleanly on the stronger Kalman base or whether the old uplift was tied to the older stack shape.
- `W4-05`, `W4-06`, `W4-07`, and `W4-12` tell us whether `5300` belongs as a standalone filtered branch, a micro-overlay, or nowhere in the final architecture.
- `W4-08` and `W4-09` should be read as the first direct answer to the user's core question: can we preserve any of the old huge upside without reopening the old self-destructive continuation pattern?
- `W4-10` is closure quality only; if it still did not trade `VEV_5100`, that branch should be considered exhausted for final-wave purposes.

## Wave 4 Decision Board

Promote count: `5`. Rescue count: `3`. Close count: `3`. Not-cleanly-tested count: `1`.

| short_id | stem | analysis_bucket | profit | path_peak | path_end_from_peak | overlay_vs_delta1 | mean_markout_10000_unit | cf_gain_vs_final_retain_75 | own_trades | exec_symbols | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W4-03 | candidate_w4_03_delta1_itm_kalman_stack | wave4_itm_finalists | 1606.305 | 2404.709 | -798.404 | 79.000 | 3.459 | 185.133 | 92 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT,VEV_4000,VEV_4500 | promote |
| W4-04 | candidate_w4_04_delta1_itm_kalman_strict | wave4_itm_finalists | 1604.305 | 2418.062 | -813.758 | 77.000 | 3.452 | 185.133 | 88 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT,VEV_4000,VEV_4500 | promote |
| W4-01 | candidate_w4_01_delta1_kalman_control | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 0.000 | 6.135 | 227.629 | 42 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT | promote |
| W4-02 | candidate_w4_02_delta1_kalman_retention | wave4_delta1_finalists | 1527.305 | 2341.062 | -813.758 | 0.000 | 6.135 | 227.629 | 42 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT | promote |
| W4-11 | candidate_w4_11_delta1_kalman_stress_control | wave4_delta1_finalists | 1455.767 | 2276.125 | -820.358 | 0.000 | 6.676 | 235.444 | 39 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT | promote |
| W4-07 | candidate_w4_07_delta1_itm_5300_final_stack | wave4_5300_finalists | 1596.305 | 2410.062 | -813.758 | 69.000 | 3.148 | 185.133 | 93 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT,VEV_4000,VEV_4500,VEV_5300 | rescue |
| W4-09 | candidate_w4_09_delta1_5300_peak_overlay | wave4_peak_salvage | 1521.305 | 2335.062 | -813.758 | -6.000 | 5.550 | 227.629 | 45 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT,VEV_5300 | rescue |
| W4-06 | candidate_w4_06_delta1_5300_selective_overlay | wave4_5300_finalists | 1511.305 | 2325.062 | -813.758 | -16.000 | 5.179 | 227.629 | 47 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT,VEV_5300 | rescue |
| W4-10 | candidate_w4_10_5100_inverse_forced | wave4_inverse_closure | 0.000 | 0.000 | 0.000 |  |  | 0.000 | 0 |  | not_cleanly_tested |
| W4-08 | candidate_w4_08_5300_peak_salvage | wave4_peak_salvage | -12.000 | 0.000 | -12.000 |  | -1.667 | 0.000 | 3 | VEV_5300 | close |
| W4-05 | candidate_w4_05_5300_selective_control | wave4_5300_finalists | -91.000 | 0.000 | -91.000 |  | -0.600 | 0.000 | 15 | VEV_5300 | close |
| W4-12 | candidate_w4_12_5300_trend_comparator | wave4_5300_finalists | -107.000 | 43.039 | -150.039 |  | -1.048 | 136.613 | 21 | VEV_5300 | close |

### Decision Reading

- **Promote now** means “candidate for the next near-final winner batch”.
- **Rescue** means “keep only if it is specifically an upside-distillation / retention experiment”.
- **Close** means “do not spend another normal finalist slot on it”.
- The purpose of this board is not to crown the winner yet. It is to decide which branches deserve the final exploitation wave.

## Product-Level Realized Summary

| product | nonzero_runs | positive_runs | negative_runs | mean_pnl | best_pnl | worst_pnl | wave3_nonzero_runs | wave3_mean_pnl | wave4_nonzero_runs | wave4_mean_pnl |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HYDROGEL_PACK | 36 | 25 | 11 | -491.480 | 1160.000 | -14249.344 | 6 | 650.723 | 8 | 994.844 |
| VELVETFRUIT_EXTRACT | 51 | 48 | 3 | 117.296 | 1240.906 | -8913.188 | 13 | 365.051 | 8 | 523.519 |
| VEV_4000 | 16 | 10 | 6 | 32.554 | 159.398 | -68.000 | 3 | 48.667 | 3 | 43.333 |
| VEV_4500 | 16 | 10 | 6 | 26.741 | 159.398 | -48.000 | 3 | 32.000 | 3 | 34.333 |
| VEV_5000 | 21 | 2 | 19 | -857.100 | 48.814 | -1935.734 | 2 | -295.610 | 0 |  |
| VEV_5100 | 15 | 1 | 14 | -1780.831 | 121.293 | -7404.336 | 0 |  | 0 |  |
| VEV_5200 | 13 | 1 | 12 | -2911.031 | 383.738 | -11205.903 | 0 |  | 0 |  |
| VEV_5300 | 50 | 15 | 35 | -596.551 | 852.269 | -5019.000 | 13 | -527.660 | 6 | -40.000 |
| VEV_5400 | 7 | 3 | 4 | -397.770 | 1.798 | -1841.891 | 0 |  | 0 |  |
| VEV_5500 | 3 | 0 | 3 | -262.125 | -144.792 | -320.792 | 0 |  | 0 |  |
| VEV_6000 | 0 | 0 | 0 |  |  |  | 0 |  | 0 |  |
| VEV_6500 | 0 | 0 | 0 |  |  |  | 0 |  | 0 |  |

## What Worked

- Clean delta-1 on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`.
- Kalman-style smoothing on top of the clean delta-1 base.
- Active ITM as a small additive overlay when attached to the base.
- Selective `5300` filtering when aggressively narrowed and tied to better state selection.
- Using the old `>10k` runs as **retention design evidence** rather than as a ready-made architecture.

## What Did Not Work

- Broad active-voucher baskets as promotable architecture.
- Treating `5000/5100/5200` as normal active-reversion strikes.
- Assuming raw huge peaks were enough evidence by themselves.
- Using inverse diagnostics as evidence when the target inverse leg did not even trade.
- Expecting Wave 4 finalist hygiene alone to recreate the old giant peaks. Cleanliness helped quality, but it also compressed upside.

## Closeout Consequence

Round 3 no longer needs another exploitation pass. The next step is to consume this evidence as a closeout package.

The carry-forward questions for Round 4 are now:

1. Which parts of the clean winner family are genuine universal structure versus Round 3-specific fit?
2. Which active-voucher lessons are validated enough to become Round 4 framing rules?
3. Which untested hypotheses from the partial Wave 5 / closeout backlog deserve re-entry only after Round 4 data confirms the same product mechanics?
4. How should counterparty-aware Round 4 EDA incorporate the now-documented distinction between clean base, additive ITM, toxic strikes, and retention-sensitive active logic?

## Artifacts

- [`artifacts/full_synthesis/full_run_metrics.csv`](artifacts/full_synthesis/full_run_metrics.csv)
- [`artifacts/full_synthesis/full_family_summary.csv`](artifacts/full_synthesis/full_family_summary.csv)
- [`artifacts/full_synthesis/full_path_family_summary.csv`](artifacts/full_synthesis/full_path_family_summary.csv)
- [`artifacts/full_synthesis/full_path_reversal_candidates.csv`](artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`artifacts/full_synthesis/full_product_attribution.csv`](artifacts/full_synthesis/full_product_attribution.csv)
- [`artifacts/full_synthesis/full_execution_metrics.csv`](artifacts/full_synthesis/full_execution_metrics.csv)
- [`artifacts/full_synthesis/full_strategy_run_mapping.csv`](artifacts/full_synthesis/full_strategy_run_mapping.csv)
- [`artifacts/full_synthesis/full_wave1_probe_summary.csv`](artifacts/full_synthesis/full_wave1_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave2_probe_summary.csv`](artifacts/full_synthesis/full_wave2_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave3_probe_summary.csv`](artifacts/full_synthesis/full_wave3_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave4_probe_summary.csv`](artifacts/full_synthesis/full_wave4_probe_summary.csv)
- [`artifacts/full_synthesis/full_wave5_probe_summary.csv`](artifacts/full_synthesis/full_wave5_probe_summary.csv)
- [`artifacts/full_synthesis/full_high_peak_gt5k_runs.csv`](artifacts/full_synthesis/full_high_peak_gt5k_runs.csv)
- [`artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
- [`artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv`](artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv)
- [`artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
- [`artifacts/full_synthesis/full_no_trade_candidates.csv`](artifacts/full_synthesis/full_no_trade_candidates.csv)
- [`artifacts/full_synthesis/full_trade_markout_by_product.csv`](artifacts/full_synthesis/full_trade_markout_by_product.csv)
- [`artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- [`artifacts/full_synthesis/full_wave3_decision_board.csv`](artifacts/full_synthesis/full_wave3_decision_board.csv)
- [`artifacts/full_synthesis/full_wave4_decision_board.csv`](artifacts/full_synthesis/full_wave4_decision_board.csv)
- [`artifacts/full_synthesis/full_wave5_decision_board.csv`](artifacts/full_synthesis/full_wave5_decision_board.csv)
- [`artifacts/full_synthesis/full_moneyness_role_summary.csv`](artifacts/full_synthesis/full_moneyness_role_summary.csv)
- [`artifacts/full_synthesis/full_cross_strike_context.csv`](artifacts/full_synthesis/full_cross_strike_context.csv)
- [`artifacts/full_synthesis/full_portfolio_exposure_summary.csv`](artifacts/full_synthesis/full_portfolio_exposure_summary.csv)
- [`artifacts/full_synthesis/full_late_entry_summary.csv`](artifacts/full_synthesis/full_late_entry_summary.csv)
- [`artifacts/full_synthesis/full_peak_profiles.csv`](artifacts/full_synthesis/full_peak_profiles.csv)
