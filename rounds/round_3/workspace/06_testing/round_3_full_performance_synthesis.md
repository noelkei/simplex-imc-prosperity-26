# Round 3 Full Performance Synthesis

## Executive Verdict

This report consolidates **all current Round 3 evidence**: EDA, understanding,
legacy historical runs, corrected challenger runs, and the full 25-bot Wave 1
learning batch.

- Total platform JSON artifacts analyzed: `39`.
- Wave 1 learner JSON artifacts analyzed: `25`.
- Runs with usable `tradeHistory` execution detail from `.log`: `26`.
- Best overall tested run remains `B02-resid` / `r3_b02_itm_residual.json` at real platform PnL `1409.371`.
- Best Wave 1 learner is `L06` / `probe_l06_delta1_dual_independent.json` at `886.102`.
- No pure voucher-only Wave 1 learner finished positive.

### Bottom Line

1. **The strongest live family is now clean delta-1 microstructure**, not broad
   voucher composites.
2. **Pure voucher-only Wave 1 learners did not produce a winner**. The best
   active standalone strike (`VEV_5300`) was only near-flat, not positive.
3. **`VEV_5100` and `VEV_5200` are now the clearest toxic strikes** in live
   standalone testing.
4. **Inventory control is not dead**, but it only helped on a cleaner subset
   (`VEV_5000 + VEV_5300`), not on the broad active basket.
5. **The old “HYDRO is weak” conclusion was too pessimistic**. HYDRO failed in
   earlier composite implementations, but isolated HYDRO learners turned
   clearly positive.

## Coverage Audit

- Historical / corrected / learner evidence now spans legacy delta-1, legacy
  ITM/VEX, legacy active vouchers, corrected centered composites, Wave 1
  delta-1 probes, Wave 1 ITM probes, Wave 1 active-subset probes, Wave 1
  upper probes, and Wave 1 surface probes.
- `activitiesLog` final product sums remain the best practical PnL
  reconstruction when JSON `profit` is unavailable.
- For path analysis, this report now uses **timestamp-level PnL reconstructed
  from `activitiesLog`**, not just final-run outcomes or the coarser
  `graphLog`.
- `.log` files for the Wave 1 learners are not empty; they contain a full
  single-line JSON blob with `tradeHistory`, which is useful for fill and
  inventory diagnostics.

## Path Quality Summary

- Runs with a positive intra-run peak above `100` that still finished negative:
  `20` / `39`.
- Runs with a strong intra-run peak above `500` that still finished negative:
  `17` / `39`.
- Of those reversal runs, `13` peaked in the **second
  half** of the session before giving the gains back.

| analysis_bucket | runs | mean_final_profit | mean_path_peak | median_path_peak | mean_end_from_peak | mean_path_max_drawdown | mean_positive_time_ratio | positive_peak_negative_finish_rate | big_peak_negative_finish_rate | late_peak_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy_active_vouchers | 6 | -5614.712 | 11099.881 | 12132.826 | -16714.593 | -24780.181 | 0.349 | 0.833 | 0.833 | 0.833 |
| corrected_and_legacy_composites | 3 | -3295.201 | 6047.251 | 793.538 | -9342.452 | -12891.895 | 0.290 | 0.667 | 0.667 | 0.667 |
| legacy_delta1 | 2 | -13408.434 | 2503.750 | 2503.750 | -15912.184 | -19597.688 | 0.151 | 0.500 | 0.500 | 0.000 |
| wave1_active | 10 | -4089.567 | 1691.109 | 1786.306 | -5780.676 | -6578.888 | 0.356 | 0.700 | 0.700 | 0.700 |
| legacy_itm_vex | 2 | 1068.132 | 1465.138 | 1465.138 | -397.007 | -2886.430 | 0.837 | 0.000 | 0.000 | 0.500 |
| wave1_delta1 | 5 | 547.158 | 1055.223 | 1254.016 | -508.066 | -659.674 | 0.809 | 0.000 | 0.000 | 1.000 |
| wave1_upper | 4 | -383.811 | 490.214 | 496.305 | -874.025 | -1353.143 | 0.233 | 0.500 | 0.500 | 0.000 |
| wave1_itm | 4 | 78.383 | 259.178 | 253.771 | -180.794 | -278.867 | 0.477 | 0.750 | 0.000 | 0.250 |
| wave1_surface | 2 | -5864.667 | 25.359 | 25.359 | -5890.026 | -6311.951 | 0.009 | 0.000 | 0.000 | 0.000 |
| diagnostic | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

### Reading The Path Table

- `wave1_delta1` is not just positive at the close; it also has strong
  intraday quality: mean peak `1055.223` and mean
  positive-time ratio `0.809`.
- `wave1_active` is more nuanced than “always dead”: mean peak
  `1691.109`, but mean giveback from peak
  `-5780.676`. That is a **real reversal /
  unwind problem**, not just zero edge.
- `wave1_surface` is different: mean peak only `25.359`
  and almost no time spent positive. That branch looks structurally wrong in
  the current implementation, not merely badly closed out.

## Biggest Mid-Run Reversals

These runs matter because they may still contain signal even though they
finished badly.

| short_id | stem | analysis_bucket | profit | path_peak | path_peak_ts | path_end_from_peak | path_positive_time_ratio | path_shape |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B08-regime | r3_b08_regime_composite | legacy_active_vouchers | -1501.925 | 17478.214 | 59700 | -18980.139 | 0.423 | edge_then_major_reversal |
| C06-legacy | candidate_c06_composite_base | corrected_and_legacy_composites | -1631.925 | 17348.214 | 59700 | -18980.139 | 0.424 | edge_then_major_reversal |
| B04-surf | r3_b04_full_surface | legacy_active_vouchers | -2561.846 | 15838.493 | 59700 | -18400.339 | 0.405 | edge_then_major_reversal |
| B03-pure | r3_b03_voucher_pure | legacy_active_vouchers | -2261.849 | 12539.876 | 59700 | -14801.725 | 0.405 | edge_then_major_reversal |
| L19 | probe_l19_active_5000_5100_5300_residual | wave1_active | -9241.385 | 3583.584 | 59600 | -12824.969 | 0.198 | edge_then_major_reversal |
| B06-tte | r3_b06_tte_cautious | legacy_active_vouchers | -752.886 | 11725.777 | 59700 | -12478.663 | 0.426 | edge_then_major_reversal |
| B01-base | r3_b01_delta1_baseline | legacy_delta1 | -6414.711 | 5007.500 | 34100 | -11422.211 | 0.303 | edge_then_major_reversal |
| B07-hedge | r3_b07_delta_hedge | legacy_active_vouchers | -1275.997 | 9016.926 | 59600 | -10292.923 | 0.437 | edge_then_major_reversal |
| L17 | probe_l17_active_5100_5300_residual | wave1_active | -7620.939 | 1850.436 | 59600 | -9471.375 | 0.187 | edge_then_major_reversal |
| L13 | probe_l13_active_5100_residual | wave1_active | -6956.580 | 1722.176 | 59600 | -8678.756 | 0.037 | edge_then_major_reversal |
| L16 | probe_l16_active_5000_5300_residual | wave1_active | -1837.049 | 2042.844 | 23600 | -3879.893 | 0.719 | edge_then_major_reversal |
| C06-base-v01 | candidate_c06_v01_centered_base | corrected_and_legacy_composites | -3008.203 | 793.538 | 59600 | -3801.741 | 0.445 | edge_then_major_reversal |

### Reversal Reading

- Several legacy voucher/composite bots and several Wave 1 active learners made
  meaningful money mid-run before collapsing.
- `probe_l12_active_5000_residual` and `probe_l15_active_5300_residual` are
  examples of the “edge then reversal” pattern; they are not in the same
  category as `probe_l26_surface_5200_5300_relval`, which showed almost no
  positive path at all.
- This means the next design step should distinguish:
  - branches with **monetizable entry signal but broken hold / exit / sizing**
  - branches with **no evidence of usable signal**

## Overall Ranking

### Top 12 Runs By Real Platform PnL

| short_id | stem | analysis_bucket | profit | delta1_total | itm_total | active_total | upper_total | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B02-resid | r3_b02_itm_residual | legacy_itm_vex | 1409.371 | 1211.906 | 197.464 | 0.000 | 0.000 | strong positive |
| L06 | probe_l06_delta1_dual_independent | wave1_delta1 | 886.102 | 886.102 | 0.000 | 0.000 | 0.000 | strong positive |
| B02-anchor | r3_b02_itm_anchor | legacy_itm_vex | 726.893 | 599.500 | 127.393 | 0.000 | 0.000 | strong positive |
| L01 | probe_l01_hydro_reversion | wave1_delta1 | 556.031 | 556.031 | 0.000 | 0.000 | 0.000 | strong positive |
| L02 | probe_l02_hydro_imbalance | wave1_delta1 | 537.656 | 537.656 | 0.000 | 0.000 | 0.000 | strong positive |
| L05 | probe_l05_vex_imbalance | wave1_delta1 | 446.387 | 446.387 | 0.000 | 0.000 | 0.000 | positive |
| L10 | probe_l10_itm_pair_plus_vex | wave1_itm | 326.151 | 332.461 | -6.310 | 0.000 | 0.000 | positive |
| L04 | probe_l04_vex_reversion | wave1_delta1 | 309.613 | 309.613 | 0.000 | 0.000 | 0.000 | positive |
| L25 | probe_l25_vex_plus_5300 | wave1_active | 115.857 | 332.461 | 0.000 | -216.604 | 0.000 | positive |
| D01-logger | baseline_state_logger | diagnostic | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | near flat |
| L24 | probe_l24_upper_5400_5500_passive | wave1_upper | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | near flat |
| L07 | probe_l07_itm_4000_residual | wave1_itm | -3.155 | 0.000 | -3.155 | 0.000 | 0.000 | near flat |

### Worst 10 Runs By Real Platform PnL

| short_id | stem | analysis_bucket | profit | delta1_total | itm_total | active_total | upper_total | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C06-inv-v01 | candidate_c06_composite_inv | corrected_and_legacy_composites | -5245.475 | 599.500 | 0.000 | -5844.975 | 0.000 | strong negative |
| L14 | probe_l14_active_5200_residual | wave1_active | -5900.712 | 0.000 | 0.000 | -5900.712 | 0.000 | strong negative |
| L18 | probe_l18_active_5200_5300_residual | wave1_active | -6078.315 | 0.000 | 0.000 | -6078.315 | 0.000 | strong negative |
| B01-base | r3_b01_delta1_baseline | legacy_delta1 | -6414.711 | -6414.711 | 0.000 | 0.000 | 0.000 | strong negative |
| L13 | probe_l13_active_5100_residual | wave1_active | -6956.580 | 0.000 | 0.000 | -6956.580 | 0.000 | strong negative |
| L17 | probe_l17_active_5100_5300_residual | wave1_active | -7620.939 | 0.000 | 0.000 | -7620.939 | 0.000 | strong negative |
| L19 | probe_l19_active_5000_5100_5300_residual | wave1_active | -9241.385 | 0.000 | 0.000 | -9241.385 | 0.000 | strong negative |
| L26 | probe_l26_surface_5200_5300_relval | wave1_surface | -10739.712 | 0.000 | 0.000 | -10739.712 | 0.000 | strong negative |
| B01-opt | r3_b01_delta1_optiver | legacy_delta1 | -20402.156 | -20402.156 | 0.000 | 0.000 | 0.000 | strong negative |
| B05-adv | r3_b05_composite_advanced | legacy_active_vouchers | -25333.769 | -22856.344 | 0.000 | -2477.425 | 0.000 | strong negative |

## Strategy / Bot / Performance Linkage

This table links each saved performance artifact back to the bot family and the
main hypothesis it was testing.

| short_id | stem | era | candidate_family | product_scope | profit | learning_verdict |
| --- | --- | --- | --- | --- | --- | --- |
| C06-base-v01 | candidate_c06_v01_centered_base | corrected | corrected centered composite | HYDRO + VEX + VEV_5000-5300 | -3008.203 | strong negative |
| C06-inv-v01 | candidate_c06_composite_inv | corrected | corrected centered composite inventory | HYDRO + VEX + VEV_5000-5300 | -5245.475 | strong negative |
| D01-logger | baseline_state_logger | diagnostic | diagnostic logger | all round_3 products | 0.000 | near flat |
| B02-resid | r3_b02_itm_residual | legacy | legacy itm residual composite | HYDRO + VEX + VEV_4000-4500 | 1409.371 | strong positive |
| B02-anchor | r3_b02_itm_anchor | legacy | legacy itm anchor composite | VEX + VEV_4000-4500 | 726.893 | strong positive |
| B06-tte | r3_b06_tte_cautious | legacy | legacy tte cautious | VEX + VEV_5000-5300 | -752.886 | negative |
| B07-hedge | r3_b07_delta_hedge | legacy | legacy delta hedge | VEX + VEV_5000-5300 | -1275.997 | negative |
| B08-regime | r3_b08_regime_composite | legacy | legacy regime composite | VEX + VEV_5000-5300 | -1501.925 | negative |
| C06-legacy | candidate_c06_composite_base | legacy | legacy composite raw residual | HYDRO + VEX + VEV_5000-5300 | -1631.925 | negative |
| B03-pure | r3_b03_voucher_pure | legacy | legacy active voucher pure | VEV_5000-5300 | -2261.849 | strong negative |
| B04-surf | r3_b04_full_surface | legacy | legacy full surface composite | VEX + VEV_4000-5500 | -2561.846 | strong negative |
| B01-base | r3_b01_delta1_baseline | legacy | legacy delta1 baseline | HYDRO + VEX | -6414.711 | strong negative |
| B01-opt | r3_b01_delta1_optiver | legacy | legacy delta1 optiver | HYDRO + VEX | -20402.156 | strong negative |
| B05-adv | r3_b05_composite_advanced | legacy | legacy advanced composite | HYDRO + VEX + VEV_5000-5300 | -25333.769 | strong negative |
| L06 | probe_l06_delta1_dual_independent | wave1_probe | delta1 dual combo | HYDRO + VEX | 886.102 | strong positive |
| L01 | probe_l01_hydro_reversion | wave1_probe | delta1 reversion | HYDRO | 556.031 | strong positive |
| L02 | probe_l02_hydro_imbalance | wave1_probe | delta1 imbalance | HYDRO | 537.656 | strong positive |
| L05 | probe_l05_vex_imbalance | wave1_probe | delta1 imbalance | VEX | 446.387 | positive |
| L10 | probe_l10_itm_pair_plus_vex | wave1_probe | itm residual plus vex | VEX + VEV_4000 + VEV_4500 | 326.151 | positive |
| L04 | probe_l04_vex_reversion | wave1_probe | delta1 reversion | VEX | 309.613 | positive |
| L25 | probe_l25_vex_plus_5300 | wave1_probe | vex plus active best strike | VEX + VEV_5300 | 115.857 | positive |
| L24 | probe_l24_upper_5400_5500_passive | wave1_probe | upper passive maker | VEV_5400 + VEV_5500 | 0.000 | near flat |
| L07 | probe_l07_itm_4000_residual | wave1_probe | itm residual | VEV_4000 | -3.155 | near flat |
| L08 | probe_l08_itm_4500_residual | wave1_probe | itm residual | VEV_4500 | -3.155 | near flat |
| L09 | probe_l09_itm_pair_residual | wave1_probe | itm residual pair | VEV_4000 + VEV_4500 | -6.310 | near flat |
| L15 | probe_l15_active_5300_residual | wave1_probe | active residual | VEV_5300 | -216.604 | mild negative |
| L22 | probe_l22_upper_5500_residual | wave1_probe | upper residual | VEV_5500 | -320.792 | mild negative |
| L21 | probe_l21_upper_5400_residual | wave1_probe | upper residual | VEV_5400 | -446.830 | mild negative |
| L23 | probe_l23_upper_5400_5500_residual | wave1_probe | upper residual pair | VEV_5400 + VEV_5500 | -767.622 | negative |
| L27 | probe_l27_surface_5300_5400_relval | wave1_probe | surface relative value | VEV_5300 + VEV_5400 | -989.622 | negative |
| L20 | probe_l20_active_5000_5300_inventory | wave1_probe | active residual inventory subset | VEV_5000 + VEV_5300 | -1443.986 | negative |
| L12 | probe_l12_active_5000_residual | wave1_probe | active residual | VEV_5000 | -1715.952 | negative |
| L16 | probe_l16_active_5000_5300_residual | wave1_probe | active residual subset | VEV_5000 + VEV_5300 | -1837.049 | negative |
| L14 | probe_l14_active_5200_residual | wave1_probe | active residual | VEV_5200 | -5900.712 | strong negative |
| L18 | probe_l18_active_5200_5300_residual | wave1_probe | active residual subset | VEV_5200 + VEV_5300 | -6078.315 | strong negative |
| L13 | probe_l13_active_5100_residual | wave1_probe | active residual | VEV_5100 | -6956.580 | strong negative |
| L17 | probe_l17_active_5100_5300_residual | wave1_probe | active residual subset | VEV_5100 + VEV_5300 | -7620.939 | strong negative |
| L19 | probe_l19_active_5000_5100_5300_residual | wave1_probe | active residual subset | VEV_5000 + VEV_5100 + VEV_5300 | -9241.385 | strong negative |
| L26 | probe_l26_surface_5200_5300_relval | wave1_probe | surface relative value | VEV_5200 + VEV_5300 | -10739.712 | strong negative |

## Family Summary

| analysis_bucket | runs | mean_profit | median_profit | best_profit | worst_profit | mean_delta1 | mean_itm | mean_active | mean_upper | mean_own_trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| legacy_itm_vex | 2 | 1068.132 | 1068.132 | 1409.371 | 726.893 | 905.703 | 162.428 | 0.000 | 0.000 | 0.000 |
| wave1_delta1 | 5 | 547.158 | 537.656 | 886.102 | 309.613 | 547.158 | 0.000 | 0.000 | 0.000 | 30.600 |
| wave1_itm | 4 | 78.383 | -3.155 | 326.151 | -6.310 | 83.115 | -4.732 | 0.000 | 0.000 | 39.500 |
| diagnostic | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| wave1_upper | 4 | -383.811 | -383.811 | 0.000 | -767.622 | 0.000 | 0.000 | 0.000 | -383.811 | 360.500 |
| corrected_and_legacy_composites | 3 | -3295.201 | -3008.203 | -1631.925 | -5245.475 | 599.500 | 0.000 | -3894.701 | 0.000 | 243.667 |
| wave1_active | 10 | -4089.567 | -3868.880 | 115.857 | -9241.385 | 33.246 | 0.000 | -4122.813 | 0.000 | 533.500 |
| legacy_active_vouchers | 6 | -5614.712 | -1881.887 | -752.886 | -25333.769 | -3680.046 | 53.133 | -1954.628 | -33.171 | 0.000 |
| wave1_surface | 2 | -5864.667 | -5864.667 | -989.622 | -10739.712 | 0.000 | 0.000 | -4943.721 | -920.946 | 464.000 |
| legacy_delta1 | 2 | -13408.434 | -13408.434 | -6414.711 | -20402.156 | -13408.434 | 0.000 | 0.000 | 0.000 | 0.000 |

### Reading The Family Table

- `wave1_delta1` is decisively positive: mean PnL `547.158`.
- `wave1_itm` is basically flat to slightly negative on its own: mean PnL `78.383`.
- `wave1_active` is still clearly negative even after strike isolation: mean PnL `-4089.567`.
- `wave1_upper` is negative in directional residual form: mean PnL `-383.811`.
- `wave1_surface` is the weakest new experimental family after the toxic active strikes: mean PnL `-5864.667`.

## EDA / Understanding Scorecard

| Original EDA / Understanding Claim | Current Verdict From Runs | Evidence |
| --- | --- | --- |
| `HYDROGEL_PACK` should be treated as a separate branch. | validated strongly | `L01 = +556.031`, `L02 = +537.656`, `L06` also positive; hydro weakness was not a product-level death sentence. |
| `VELVETFRUIT_EXTRACT` is the natural anchor and a tradable standalone delta-1 product. | validated strongly | `L04 = +309.613`, `L05 = +446.387`, `L06 = +886.102`; VEX is also positive inside the corrected challengers and `L25`. |
| `VEV_5000-5300` is the best first-wave active option scope. | weakened / contradicted | No pure active Wave 1 learner finished positive; `L15` (`VEV_5300`) was the least bad at `-216.604`, while `VEV_5100` and `VEV_5200` were disastrous. |
| `VEV_4000/4500` should be useful but were not first-wave execution leaders. | partially validated | Pure ITM probes were near-flat (`L07`, `L08`, `L09`), not winners; the positive live result is `L10`, but that comes mostly from the VEX leg. |
| `VEV_5400/5500` are execution-sensitive and should only be reopened carefully. | validated with caution | Directional residual upper bots lost money (`L21`, `L22`, `L23`); passive upper (`L24`) produced zero trades and zero PnL. |
| `VEV_6000/6500` should stay excluded. | validated strongly | Logger still shows the floor regime, and no profitable evidence has emerged there. |
| Surface-relative features may help when absolute residual is noisy. | not validated in current implementation | `L26 = -10739.712`, `L27 = -989.622`; local surface spreads are not rescuing the voucher branch in their current form. |

## Branch-by-Branch Analysis

### 1. Delta-1 Branch: Best Live Learning Outcome

Wave 1 changed the picture materially:

- `L01` (`HYDRO` reversion) finished at `+556.031`.
- `L02` (`HYDRO` imbalance) finished at `+537.656`.
- `L04` (`VEX` reversion) finished at `+309.613`.
- `L05` (`VEX` imbalance) finished at `+446.387`.
- `L06` (`HYDRO + VEX`) finished at `+886.102`.

Interpretation:

- The clean isolated delta-1 logic works much better than the old legacy pair
  makers.
- HYDRO is not rejected; the earlier negative evidence was mostly about
  implementation style and composite interactions.
- VEX remains useful both as a standalone edge and as the best anchor leg for
  any later voucher strategy.

### 2. ITM Branch: Low-Risk Add-On, Not Yet A Standalone Winner

Wave 1 ITM results:

- `L07` (`VEV_4000`) = `-3.155`
- `L08` (`VEV_4500`) = `-3.155`
- `L09` (`VEV_4000 + VEV_4500`) = `-6.310`
- `L10` (`VEX + VEV_4000 + VEV_4500`) = `+326.151`

Interpretation:

- Pure ITM residual trading is basically flat on the live `TTE=5d` day.
- The historical ITM/VEX winners were already mostly delta-1 driven:
  `B02-resid` had `delta1 = +1211.906` versus `itm = +197.464`;
  `B02-anchor` had `delta1 = +599.500` versus `itm = +127.393`.
- This means ITM is still useful, but more as a **low-damage optional add-on**
  than as the main alpha engine.

### 3. Active Voucher Branch: Still The Main Problem Area

Wave 1 active-only results:

- `L12` (`VEV_5000`) = `-1715.952`
- `L13` (`VEV_5100`) = `-6956.580`
- `L14` (`VEV_5200`) = `-5900.712`
- `L15` (`VEV_5300`) = `-216.604`
- `L16` (`VEV_5000 + VEV_5300`) = `-1837.049`
- `L17` (`VEV_5100 + VEV_5300`) = `-7620.939`
- `L18` (`VEV_5200 + VEV_5300`) = `-6078.315`
- `L19` (`VEV_5000 + VEV_5100 + VEV_5300`) = `-9241.385`
- `L20` (`VEV_5000 + VEV_5300` + inventory) = `-1443.986`
- `L25` (`VEX + VEV_5300`) = `+115.857`, with the VEX leg contributing `+332.461` and the `VEV_5300` leg `-216.604`.

Interpretation:

- `VEV_5100` and `VEV_5200` should now be treated as default rejects until
  very strong contradictory evidence appears.
- `VEV_5300` is still the **least-bad** active strike and looks useful in
  relative terms, but it is not a standalone positive alpha yet.
- `VEV_5000` is not good, but it is materially less toxic than `VEV_5100` /
  `VEV_5200`.
- Inventory helped once the basket was cleaned:
  `L20` beat `L16` by about `393.063`, even though the broad C06 inventory
  overlay had previously failed.

### 4. Upper Strikes: Reopened, But Not Yet Monetized

Wave 1 upper results:

- `L21` (`VEV_5400`) = `-446.830`
- `L22` (`VEV_5500`) = `-320.792`
- `L23` (`VEV_5400 + VEV_5500`) = `-767.622`
- `L24` (passive `VEV_5400 + VEV_5500`) = `0.000` with `0` own trades

Interpretation:

- The logger was right that these strikes move and have tight spreads.
- But that did **not** translate into profitable directional residual trading.
- Passive-only execution avoided loss, but also got no fills.
- The upper branch is therefore still open as a research branch, but it is
  not close to promotion.

### 5. Surface Relative Value: Useful Diagnostic, Bad Current Trader

Wave 1 surface results:

- `L26` (`VEV_5200 vs VEV_5300`) = `-10739.712`
- `L27` (`VEV_5300 vs VEV_5400`) = `-989.622`

Interpretation:

- `L26` is especially informative: final positions were small, but the PnL was
  catastrophically negative, which points to **realized adverse selection /
  signal error**, not just terminal inventory mark.
- `L27` is less bad, and the `VEV_5300` side was actually positive, but the
  `VEV_5400` side dominated the loss.
- So the current surface-pair implementation should be treated as a diagnostic
  failure mode, not as a candidate family to scale immediately.

## Product-Level Realized Summary

| product | nonzero_runs | positive_runs | negative_runs | mean_pnl | best_pnl | worst_pnl | wave1_nonzero_runs | wave1_positive_runs | wave1_negative_runs | wave1_mean_pnl |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HYDROGEL_PACK | 14 | 3 | 11 | -2443.376 | 556.031 | -14249.344 | 3 | 3 | 0 | 549.109 |
| VELVETFRUIT_EXTRACT | 17 | 14 | 3 | -451.722 | 1240.906 | -8913.188 | 5 | 5 | 0 | 350.677 |
| VEV_4000 | 6 | 3 | 3 | 54.477 | 159.398 | -3.155 | 3 | 0 | 3 | -3.155 |
| VEV_4500 | 6 | 3 | 3 | 49.644 | 159.398 | -3.155 | 3 | 0 | 3 | -3.155 |
| VEV_5000 | 13 | 2 | 11 | -1026.880 | 48.814 | -1935.734 | 4 | 0 | 4 | -1645.949 |
| VEV_5100 | 12 | 1 | 11 | -2176.873 | 121.293 | -7404.336 | 3 | 0 | 3 | -7255.084 |
| VEV_5200 | 12 | 1 | 11 | -3059.117 | 383.738 | -11205.903 | 3 | 0 | 3 | -7656.109 |
| VEV_5300 | 18 | 12 | 6 | 91.882 | 852.269 | -216.604 | 9 | 3 | 6 | 22.423 |
| VEV_5400 | 4 | 0 | 4 | -697.446 | -54.231 | -1841.891 | 3 | 0 | 3 | -911.850 |
| VEV_5500 | 3 | 0 | 3 | -262.125 | -144.792 | -320.792 | 2 | 0 | 2 | -320.792 |
| VEV_6000 | 0 | 0 | 0 |  |  |  | 0 | 0 | 0 |  |
| VEV_6500 | 0 | 0 | 0 |  |  |  | 0 | 0 | 0 |  |

### Product-Level Reading

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` now have real positive standalone
  evidence in Wave 1.
- `VEV_4000` / `VEV_4500` are low-damage, low-fill, near-flat live products.
- `VEV_5000` is weak but not hopeless.
- `VEV_5100` and `VEV_5200` are the strongest current negative evidence in the
  voucher family.
- `VEV_5300` is viable only as a relative or combo leg for now, not as a
  standalone winner.
- `VEV_5400/5500` are tradable enough to test, but not yet good enough to
  promote.

## Execution Diagnostics From `tradeHistory`

| short_id | stem | profit | own_trades | buy_qty | sell_qty | max_abs_exec_position | active_limit_hits | upper_limit_hits | final_active_position_abs | final_upper_position_abs | exec_symbols |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L06 | probe_l06_delta1_dual_independent | 886.102 | 49 | 112 | 137 | 24.000 | 0 | 0 | 0 | 0 | HYDROGEL_PACK,VELVETFRUIT_EXTRACT |
| L10 | probe_l10_itm_pair_plus_vex | 326.151 | 74 | 162 | 173 | 24.000 | 0 | 0 | 0 | 0 | VELVETFRUIT_EXTRACT,VEV_4000,VEV_4500 |
| L24 | probe_l24_upper_5400_5500_passive | 0.000 | 0 | 0 | 0 | 0.000 | 0 | 0 | 0 | 0 |  |
| L15 | probe_l15_active_5300_residual | -216.604 | 631 | 2716 | 2431 | 300.000 | 0 | 0 | 285 | 0 | VEV_5300 |
| L20 | probe_l20_active_5000_5300_inventory | -1443.986 | 614 | 2631 | 2460 | 300.000 | 0 | 0 | 259 | 0 | VEV_5000,VEV_5300 |
| L26 | probe_l26_surface_5200_5300_relval | -10739.712 | 670 | 3159 | 3154 | 300.000 | 0 | 0 | 17 | 0 | VEV_5200,VEV_5300 |

### Execution Reading

- Delta-1 winners (`L01`, `L02`, `L04`, `L05`, `L06`) achieved positive PnL
  with relatively low trade counts. That is a good sign for signal cleanliness.
- The active learners often traded **a lot** and still lost badly. This pushes
  the diagnosis toward signal quality / selection problems, not simple lack of
  fills.
- `L15` (`VEV_5300`) traded heavily and still only lost `-216.604`, which is
  why it remains the best active-strike survivor.
- `L24` confirms that the upper passive branch, in its current form, is too
  timid to get matched.

## What Worked

- Clean delta-1 microstructure on both `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`.
- VEX as a sidecar / anchor leg in mixed bots.
- Using inventory as a secondary cleaner on a reduced active subset.
- Excluding `VEV_6000/6500`; nothing in the new evidence argues for reopening them.
- Identifying that some active-voucher bots do have **mid-run edge**, even if
  they currently fail to retain it.

## What Did Not Work

- Broad active voucher baskets, even after centered-residual correction.
- `VEV_5100` and `VEV_5200` as default active strikes.
- Treating `VEV_5300` as a standalone promoted winner just because it was the
  least-bad strike inside earlier composites.
- Directional upper-strike residual trading.
- Current surface-pair implementations.
- Interpreting every negative final run as “no signal”; the path analysis now
  shows that this was too crude for several active-voucher experiments.

## What We Still Do Not Know

- Whether the best next bot should be **delta-1 only** or **delta-1 plus a very
  selective voucher add-on**.
- Whether ITM is worth keeping as a low-risk add-on once execution is tuned, or
  whether VEX alone captures most of that upside more simply.
- Whether `VEV_5000 + VEV_5300` can become viable with better anchoring,
  tighter execution, or stronger inventory discipline.
- Whether the upper branch can ever do better than zero-fill passive quoting
  without becoming structurally lossy.
- Whether the best way to rescue selective active vouchers is with **shorter
  holding periods / faster profit capture** rather than better long-horizon
  fair value estimates.

## Recommended Questions Before Wave 2 Strategy Design

These are **analysis-driven next questions**, not yet implementation orders.

1. Should the next champion family be delta-1 first, with vouchers demoted to optional add-ons?
2. Is the right voucher follow-up a `VEX + 5000/5300` style combo rather than any pure voucher basket?
3. Should `VEV_5100` and `VEV_5200` now be formally moved from “active scope” to “excluded unless rescued”?
4. Is ITM best framed as an execution-light addon rather than a main branch?
5. Does the next surface work need a different execution style entirely, or should that branch be paused?

## Artifacts

- [`artifacts/full_synthesis/full_run_metrics.csv`](artifacts/full_synthesis/full_run_metrics.csv)
- [`artifacts/full_synthesis/full_path_family_summary.csv`](artifacts/full_synthesis/full_path_family_summary.csv)
- [`artifacts/full_synthesis/full_path_reversal_candidates.csv`](artifacts/full_synthesis/full_path_reversal_candidates.csv)
- [`artifacts/full_synthesis/full_product_attribution.csv`](artifacts/full_synthesis/full_product_attribution.csv)
- [`artifacts/full_synthesis/full_family_summary.csv`](artifacts/full_synthesis/full_family_summary.csv)
- [`artifacts/full_synthesis/full_execution_metrics.csv`](artifacts/full_synthesis/full_execution_metrics.csv)
- [`artifacts/full_synthesis/full_strategy_run_mapping.csv`](artifacts/full_synthesis/full_strategy_run_mapping.csv)
- [`artifacts/full_synthesis/full_wave1_probe_summary.csv`](artifacts/full_synthesis/full_wave1_probe_summary.csv)

## Handoff

- This synthesis supersedes the earlier “waiting for Wave 1 runs” state.
- The next useful step is **not another blind run batch**. It is to redesign
  the next strategy wave using this evidence, especially the delta-1 recovery
  and the voucher-family split between survivable and toxic strikes.
