# Platform Artifact Analysis: Round 1

## Run Metadata

- Run ID: `run_20260417_platform_artifact_analysis`
- Date: 2026-04-17
- Round: `round_1`
- Owner: `noel`
- Raw output: `rounds/round_1/performances/noel/canonical/run_20260417_platform_artifact_analysis.json`
- Script: `rounds/round_1/performances/noel/canonical/analyze_platform_artifacts.py`
- Source artifacts: platform-style JSON/log files under `rounds/round_1/performances/` plus misfiled JSONs under `rounds/round_1/bots/`.

## PnL Methodology

Use this priority order before promoting a bot:

1. `profit` from the platform-style JSON: authoritative run-level score for that artifact.
2. Sum of the final per-product `profit_and_loss` values from `activitiesLog`: should match `profit`; use to split PnL by product.
3. Final `graphLog` value: should match total PnL when present.
4. Reconstruction from own `tradeHistory` plus final mid: useful audit, but only available when a matching log exists.
5. Local replay: sanity/ranking heuristic only; not an official PnL estimator.

## Official Ranking

| Rank | Run | Member | Bucket | Official PnL | IPR PnL | ACO PnL | Final IPR | Final ACO | Own Trades | Max DD |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_26_v3_a3b1_one_sided_exit_overlay` | noel | canonical | 10090.47 | 7286.00 | 2804.47 | 80 | 9 | 81 | 682.00 |
| 2 | `candidate_28_v1_c26_strict_one_sided` | noel | historical | 10076.31 | 7286.00 | 2790.31 | 80 | 6 | 80 | 682.00 |
| 3 | `candidate_10_bot02_carry_tight_mm` | noel | historical | 10007.00 | 7286.00 | 2721.00 | 80 | 0 | 79 | 682.00 |
| 4 | `candidate_19_ipr_execution_upgrade` | noel | historical | 10007.00 | 7286.00 | 2721.00 | 80 | 0 | 79 | 682.00 |
| 5 | `candidate_24_v1_a1b1_size_skew_refine` | noel | historical | 9951.28 | 7286.00 | 2665.28 | 80 | -1 | 78 | 682.00 |
| 6 | `candidate_25_v2_a2b1_conservative_regime_gate` | noel | historical | 9930.16 | 7286.00 | 2644.16 | 80 | 3 | 78 | 682.00 |
| 7 | `candidate_27_v1_c26_soft_flatten` | noel | historical | 9920.19 | 7286.00 | 2634.19 | 80 | 10 | 77 | 682.00 |
| 8 | `candidate_14_aco_kalman_latent_fv` | noel | historical | 9839.75 | 7286.00 | 2553.75 | 80 | 40 | 60 | 682.00 |
| 9 | `candidate_21_one_sided_book_specialist` | noel | historical | 9763.47 | 7286.00 | 2477.47 | 80 | 41 | 56 | 682.00 |
| 10 | `candidate_22_micro_alpha_rescue` | noel | historical | 9657.22 | 7286.00 | 2371.22 | 80 | 17 | 57 | 682.00 |
| 11 | `candidate_18_aco_offline_policy_table` | noel | historical | 9579.25 | 7286.00 | 2293.25 | 80 | 24 | 52 | 682.00 |
| 12 | `26-candidate_03_combined` | amin | canonical | 9432.06 | 7286.00 | 2146.06 | 80 | 46 | - | 682.00 |
| 13 | `candidate_15_aco_hmm_regime_mm` | noel | historical | 9328.53 | 7286.00 | 2042.53 | 80 | 23 | 44 | 682.00 |
| 14 | `candidate_16_aco_edge_quality_gate` | noel | historical | 9313.09 | 7286.00 | 2027.09 | 80 | 21 | 44 | 682.00 |
| 15 | `candidate_17_aco_inventory_lifecycle` | noel | historical | 9308.38 | 7286.00 | 2022.38 | 80 | 20 | 50 | 682.00 |
| 16 | `22-candidate_03_combined` | amin | historical | 8975.84 | 6836.50 | 2139.34 | 75 | 45 | - | 633.50 |
| 17 | `24-bot` | amin | historical | 8975.84 | 6836.50 | 2139.34 | 75 | 45 | 83 | 633.50 |
| 18 | `candidate_23_adaptive_aco_controller` | noel | historical | 8952.16 | 7286.00 | 1666.16 | 80 | 35 | 36 | 682.00 |
| 19 | `25-bot` | amin | historical | 8907.50 | 7286.00 | 1621.50 | 80 | 16 | 94 | 682.00 |
| 20 | `candidate_20_dual_product_risk_scheduler` | noel | historical | 8821.09 | 7286.00 | 1535.09 | 80 | 21 | 32 | 682.00 |
| 21 | `23-bot` | amin | historical | 8545.59 | 7286.00 | 1259.59 | 80 | 5 | 97 | 682.00 |
| 22 | `candidate_13_bot05_hybrid_adaptive` | noel | historical | 7642.88 | 5194.44 | 2448.44 | 66 | 2 | 122 | 314.63 |
| 23 | `candidate_12_bot04_aco_markov` | noel | historical | 4551.94 | 1862.00 | 2689.94 | 0 | 18 | 102 | 107.19 |
| 24 | `candidate_09_bot01_baseline_fv_combo` | noel | historical | 4092.72 | 1862.00 | 2230.72 | 0 | 1 | 77 | 47.16 |
| 25 | `candidate_11_bot03_micro_scalper` | noel | historical | 1542.25 | 694.59 | 847.66 | -6 | -13 | 62 | 179.73 |

## PnL Calculation Audit

| Run | Official | Activities Sum | Graph Final | Trade Rebuild | Activities Delta | Graph Delta | Trade Delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | 10090.47 | 10090.47 | 10083.06 | 10061.00 | 0.00 | -7.41 | -29.47 |
| `candidate_28_v1_c26_strict_one_sided` | 10076.31 | 10076.31 | 10068.71 | 10046.00 | 0.00 | -7.60 | -30.31 |
| `candidate_10_bot02_carry_tight_mm` | 10007.00 | 10007.00 | 9999.00 | 9975.00 | 0.00 | -8.00 | -32.00 |
| `candidate_19_ipr_execution_upgrade` | 10007.00 | 10007.00 | 9999.00 | 9975.00 | 0.00 | -8.00 | -32.00 |
| `candidate_24_v1_a1b1_size_skew_refine` | 9951.28 | 9951.28 | 9943.21 | 9919.00 | 0.00 | -8.07 | -32.28 |
| `candidate_25_v2_a2b1_conservative_regime_gate` | 9930.16 | 9930.16 | 9922.36 | 9899.00 | 0.00 | -7.80 | -31.16 |
| `candidate_27_v1_c26_soft_flatten` | 9920.19 | 9920.19 | 9912.85 | 9891.00 | 0.00 | -7.34 | -29.19 |
| `candidate_14_aco_kalman_latent_fv` | 9839.75 | 9839.75 | 9834.41 | 9819.00 | 0.00 | -5.34 | -20.75 |
| `candidate_21_one_sided_book_specialist` | 9763.47 | 9763.47 | 9758.19 | 9743.00 | 0.00 | -5.28 | -20.47 |
| `candidate_22_micro_alpha_rescue` | 9657.22 | 9657.22 | 9650.34 | 9630.00 | 0.00 | -6.88 | -27.22 |
| `candidate_18_aco_offline_policy_table` | 9579.25 | 9579.25 | 9572.84 | 9554.00 | 0.00 | -6.41 | -25.25 |
| `26-candidate_03_combined` | 9432.06 | 9432.06 | 9427.12 | - | 0.00 | -4.94 | - |
| `candidate_15_aco_hmm_regime_mm` | 9328.53 | 9328.53 | 9322.06 | 9303.00 | 0.00 | -6.47 | -25.53 |
| `candidate_16_aco_edge_quality_gate` | 9313.09 | 9313.09 | 9306.48 | 9287.00 | 0.00 | -6.61 | -26.09 |
| `candidate_17_aco_inventory_lifecycle` | 9308.38 | 9308.38 | 9301.70 | 9282.00 | 0.00 | -6.67 | -26.38 |
| `22-candidate_03_combined` | 8975.84 | 8975.84 | 8971.34 | - | 0.00 | -4.50 | - |
| `24-bot` | 8975.84 | 8975.84 | 8971.34 | 8958.50 | 0.00 | -4.50 | -17.34 |
| `candidate_23_adaptive_aco_controller` | 8952.16 | 8952.16 | 8946.47 | 8930.00 | 0.00 | -5.69 | -22.16 |
| `25-bot` | 8907.50 | 8907.50 | 8900.56 | 8880.00 | 0.00 | -6.94 | -27.50 |
| `candidate_20_dual_product_risk_scheduler` | 8821.09 | 8821.09 | 8814.48 | 8795.00 | 0.00 | -6.61 | -26.09 |
| `23-bot` | 8545.59 | 8545.59 | 8537.93 | 8515.00 | 0.00 | -7.67 | -30.59 |
| `candidate_13_bot05_hybrid_adaptive` | 7642.88 | 7642.88 | 7636.38 | 7617.00 | 0.00 | -6.49 | -25.88 |
| `candidate_12_bot04_aco_markov` | 4551.94 | 4551.94 | 4553.12 | 4557.00 | 0.00 | 1.19 | 5.06 |
| `candidate_09_bot01_baseline_fv_combo` | 4092.72 | 4092.72 | 4092.79 | 4093.00 | 0.00 | 0.07 | 0.28 |
| `candidate_11_bot03_micro_scalper` | 1542.25 | 1542.25 | 1542.00 | 1541.00 | 0.00 | -0.25 | -1.25 |

## Intra-Run Trade Signals

| Run | Product | Buy Qty | Avg Buy | Sell Qty | Avg Sell | Net Qty | Gross Spread Capture | First +75/+80 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | `ASH_COATED_OSMIUM` | 235 | 9993.45 | 226 | 10005.49 | 9 | 2721.06 | -/- |
| `candidate_28_v1_c26_strict_one_sided` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_28_v1_c26_strict_one_sided` | `ASH_COATED_OSMIUM` | 232 | 9993.42 | 226 | 10005.52 | 6 | 2734.53 | -/- |
| `candidate_10_bot02_carry_tight_mm` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_10_bot02_carry_tight_mm` | `ASH_COATED_OSMIUM` | 225 | 9993.40 | 225 | 10005.50 | 0 | 2721.00 | -/- |
| `candidate_19_ipr_execution_upgrade` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_19_ipr_execution_upgrade` | `ASH_COATED_OSMIUM` | 225 | 9993.40 | 225 | 10005.50 | 0 | 2721.00 | -/- |
| `candidate_24_v1_a1b1_size_skew_refine` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_24_v1_a1b1_size_skew_refine` | `ASH_COATED_OSMIUM` | 222 | 9993.41 | 223 | 10005.40 | -1 | 2662.60 | -/- |
| `candidate_25_v2_a2b1_conservative_regime_gate` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_25_v2_a2b1_conservative_regime_gate` | `ASH_COATED_OSMIUM` | 222 | 9993.37 | 219 | 10005.32 | 3 | 2616.12 | -/- |
| `candidate_27_v1_c26_soft_flatten` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_27_v1_c26_soft_flatten` | `ASH_COATED_OSMIUM` | 227 | 9993.41 | 217 | 10005.12 | 10 | 2541.14 | -/- |
| `candidate_14_aco_kalman_latent_fv` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_14_aco_kalman_latent_fv` | `ASH_COATED_OSMIUM` | 181 | 9992.26 | 141 | 10007.40 | 40 | 2135.39 | -/- |
| `candidate_21_one_sided_book_specialist` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_21_one_sided_book_specialist` | `ASH_COATED_OSMIUM` | 174 | 9992.16 | 133 | 10007.53 | 41 | 2044.60 | -/- |
| `candidate_22_micro_alpha_rescue` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_22_micro_alpha_rescue` | `ASH_COATED_OSMIUM` | 161 | 9992.00 | 144 | 10007.20 | 17 | 2189.00 | -/- |
| `candidate_18_aco_offline_policy_table` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_18_aco_offline_policy_table` | `ASH_COATED_OSMIUM` | 150 | 9991.73 | 126 | 10007.84 | 24 | 2029.60 | -/- |
| `26-candidate_03_combined` | `INTARIAN_PEPPER_ROOT` | - | - | - | - | - | - | log missing |
| `26-candidate_03_combined` | `ASH_COATED_OSMIUM` | - | - | - | - | - | - | log missing |
| `candidate_15_aco_hmm_regime_mm` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_15_aco_hmm_regime_mm` | `ASH_COATED_OSMIUM` | 129 | 9991.47 | 106 | 10008.29 | 23 | 1783.70 | -/- |
| `candidate_16_aco_edge_quality_gate` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_16_aco_edge_quality_gate` | `ASH_COATED_OSMIUM` | 125 | 9991.30 | 104 | 10008.49 | 21 | 1787.38 | -/- |
| `candidate_17_aco_inventory_lifecycle` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_17_aco_inventory_lifecycle` | `ASH_COATED_OSMIUM` | 144 | 9992.24 | 124 | 10006.85 | 20 | 1812.72 | -/- |
| `22-candidate_03_combined` | `INTARIAN_PEPPER_ROOT` | - | - | - | - | - | - | log missing |
| `22-candidate_03_combined` | `ASH_COATED_OSMIUM` | - | - | - | - | - | - | log missing |
| `24-bot` | `INTARIAN_PEPPER_ROOT` | 75 | 12008.75 | 0 | - | 75 | - | 200/- |
| `24-bot` | `ASH_COATED_OSMIUM` | 260 | 9995.45 | 215 | 10003.88 | 45 | 1812.42 | 87400/- |
| `candidate_23_adaptive_aco_controller` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_23_adaptive_aco_controller` | `ASH_COATED_OSMIUM` | 115 | 9991.78 | 80 | 10007.83 | 35 | 1283.39 | -/- |
| `25-bot` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `25-bot` | `ASH_COATED_OSMIUM` | 275 | 9996.92 | 259 | 10002.83 | 16 | 1528.78 | -/- |
| `candidate_20_dual_product_risk_scheduler` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `candidate_20_dual_product_risk_scheduler` | `ASH_COATED_OSMIUM` | 92 | 9990.45 | 71 | 10008.44 | 21 | 1277.36 | -/- |
| `23-bot` | `INTARIAN_PEPPER_ROOT` | 80 | 12008.83 | 0 | - | 80 | - | 200/200 |
| `23-bot` | `ASH_COATED_OSMIUM` | 280 | 9997.66 | 275 | 10002.15 | 5 | 1234.30 | -/- |
| `candidate_13_bot05_hybrid_adaptive` | `INTARIAN_PEPPER_ROOT` | 155 | 12032.70 | 89 | 12041.22 | 66 | 758.99 | -/- |
| `candidate_13_bot05_hybrid_adaptive` | `ASH_COATED_OSMIUM` | 235 | 9994.33 | 233 | 10004.77 | 2 | 2431.66 | -/- |
| `candidate_12_bot04_aco_markov` | `INTARIAN_PEPPER_ROOT` | 68 | 12045.63 | 68 | 12073.01 | 0 | 1862.00 | -/- |
| `candidate_12_bot04_aco_markov` | `ASH_COATED_OSMIUM` | 233 | 9993.72 | 215 | 10005.48 | 18 | 2527.98 | -/- |
| `candidate_09_bot01_baseline_fv_combo` | `INTARIAN_PEPPER_ROOT` | 68 | 12045.63 | 68 | 12073.01 | 0 | 1862.00 | -/- |
| `candidate_09_bot01_baseline_fv_combo` | `ASH_COATED_OSMIUM` | 142 | 9991.66 | 141 | 10007.40 | 1 | 2219.66 | -/- |
| `candidate_11_bot03_micro_scalper` | `INTARIAN_PEPPER_ROOT` | 83 | 12050.99 | 89 | 12062.09 | -6 | 921.46 | -/- |
| `candidate_11_bot03_micro_scalper` | `ASH_COATED_OSMIUM` | 81 | 9993.78 | 94 | 10004.03 | -13 | 830.59 | -/- |

## Product Lever Evidence

IPR evidence: the strongest runs make the IPR position decision simple and early.

| Run | IPR PnL | Final IPR | Buy Qty | Sell Qty | First +75/+80 | IPR Max Abs Pos |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_28_v1_c26_strict_one_sided` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_10_bot02_carry_tight_mm` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_19_ipr_execution_upgrade` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_24_v1_a1b1_size_skew_refine` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_25_v2_a2b1_conservative_regime_gate` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_27_v1_c26_soft_flatten` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_14_aco_kalman_latent_fv` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_21_one_sided_book_specialist` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_22_micro_alpha_rescue` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_18_aco_offline_policy_table` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `26-candidate_03_combined` | 7286.00 | 80 | - | - | log missing | - |
| `candidate_15_aco_hmm_regime_mm` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_16_aco_edge_quality_gate` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_17_aco_inventory_lifecycle` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `22-candidate_03_combined` | 6836.50 | 75 | - | - | log missing | - |
| `24-bot` | 6836.50 | 75 | 75 | 0 | 200/- | 75 |
| `candidate_23_adaptive_aco_controller` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `25-bot` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_20_dual_product_risk_scheduler` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `23-bot` | 7286.00 | 80 | 80 | 0 | 200/200 | 80 |
| `candidate_13_bot05_hybrid_adaptive` | 5194.44 | 66 | 155 | 89 | -/- | 69 |
| `candidate_12_bot04_aco_markov` | 1862.00 | 0 | 68 | 68 | -/- | 39 |
| `candidate_09_bot01_baseline_fv_combo` | 1862.00 | 0 | 68 | 68 | -/- | 39 |
| `candidate_11_bot03_micro_scalper` | 694.59 | -6 | 83 | 89 | -/- | 26 |

ACO evidence: this is where iteration can still move the total after IPR is locked.

| Run | ACO PnL | Final ACO | Matched Qty | Edge | Avg Buy | Avg Sell | ACO Max Abs Pos |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `candidate_26_v3_a3b1_one_sided_exit_overlay` | 2804.47 | 9 | 226 | 12.04 | 9993.45 | 10005.49 | 55 |
| `candidate_28_v1_c26_strict_one_sided` | 2790.31 | 6 | 226 | 12.10 | 9993.42 | 10005.52 | 55 |
| `candidate_10_bot02_carry_tight_mm` | 2721.00 | 0 | 225 | 12.09 | 9993.40 | 10005.50 | 60 |
| `candidate_19_ipr_execution_upgrade` | 2721.00 | 0 | 225 | 12.09 | 9993.40 | 10005.50 | 60 |
| `candidate_24_v1_a1b1_size_skew_refine` | 2665.28 | -1 | 222 | 11.99 | 9993.41 | 10005.40 | 52 |
| `candidate_25_v2_a2b1_conservative_regime_gate` | 2644.16 | 3 | 219 | 11.95 | 9993.37 | 10005.32 | 48 |
| `candidate_27_v1_c26_soft_flatten` | 2634.19 | 10 | 217 | 11.71 | 9993.41 | 10005.12 | 54 |
| `candidate_14_aco_kalman_latent_fv` | 2553.75 | 40 | 141 | 15.14 | 9992.26 | 10007.40 | 57 |
| `candidate_21_one_sided_book_specialist` | 2477.47 | 41 | 133 | 15.37 | 9992.16 | 10007.53 | 68 |
| `candidate_22_micro_alpha_rescue` | 2371.22 | 17 | 144 | 15.20 | 9992.00 | 10007.20 | 34 |
| `candidate_18_aco_offline_policy_table` | 2293.25 | 24 | 126 | 16.11 | 9991.73 | 10007.84 | 43 |
| `26-candidate_03_combined` | 2146.06 | 46 | - | - | - | - | - |
| `candidate_15_aco_hmm_regime_mm` | 2042.53 | 23 | 106 | 16.83 | 9991.47 | 10008.29 | 43 |
| `candidate_16_aco_edge_quality_gate` | 2027.09 | 21 | 104 | 17.19 | 9991.30 | 10008.49 | 34 |
| `candidate_17_aco_inventory_lifecycle` | 2022.38 | 20 | 124 | 14.62 | 9992.24 | 10006.85 | 56 |
| `22-candidate_03_combined` | 2139.34 | 45 | - | - | - | - | - |
| `24-bot` | 2139.34 | 45 | 215 | 8.43 | 9995.45 | 10003.88 | 75 |
| `candidate_23_adaptive_aco_controller` | 1666.16 | 35 | 80 | 16.04 | 9991.78 | 10007.83 | 61 |
| `25-bot` | 1621.50 | 16 | 259 | 5.90 | 9996.92 | 10002.83 | 55 |
| `candidate_20_dual_product_risk_scheduler` | 1535.09 | 21 | 71 | 17.99 | 9990.45 | 10008.44 | 46 |
| `23-bot` | 1259.59 | 5 | 275 | 4.49 | 9997.66 | 10002.15 | 60 |
| `candidate_13_bot05_hybrid_adaptive` | 2448.44 | 2 | 233 | 10.44 | 9994.33 | 10004.77 | 57 |
| `candidate_12_bot04_aco_markov` | 2689.94 | 18 | 215 | 11.76 | 9993.72 | 10005.48 | 50 |
| `candidate_09_bot01_baseline_fv_combo` | 2230.72 | 1 | 141 | 15.74 | 9991.66 | 10007.40 | 23 |
| `candidate_11_bot03_micro_scalper` | 847.66 | -13 | 81 | 10.25 | 9993.78 | 10004.03 | 41 |

## Actionable Insights

- **ActivitiesLog gives the exact product PnL split**: The final per-product profit_and_loss rows sum to JSON profit with zero delta in every analyzed artifact. Action: Rank with JSON profit, then use the final activitiesLog rows for IPR/ACO attribution.
- **Graph/trade rebuild are audit tools, not the score**: Max absolute graph delta is 8.07; max absolute tradeHistory rebuild delta is 32.28 where logs exist. Action: Do not rank bots by local reconstruction; use it only to catch obvious logging or inventory inconsistencies.
- **IPR max-long dominates lower caps**: Runs ending at +80 IPR average 7286.0 IPR PnL; +75-cap runs average 6836.5. Action: Keep IPR target at +80 unless live evidence shows drift failure.
- **ACO is the main improvement surface after IPR carry**: Best ACO run is candidate_26_v3_a3b1_one_sided_exit_overlay with 2804.5 ACO PnL, 235 buy qty, 226 sell qty. Action: Iterate ACO quote size/skew/passive fill behavior around FV=10000; keep IPR carry stable.
- **ACO quality beats raw ACO volume**: candidate_26_v3_a3b1_one_sided_exit_overlay earns 2804.5 ACO PnL at edge 12.04; 23-bot trades more matched qty but edge is 4.49. Action: Optimize quote selection and inventory skew before increasing size blindly.
- **Model overlays are useful on ACO, harmful if they replace IPR carry**: Markov/adaptive Noel variants show ACO PnL of 2689.9/2448.4, but their IPR PnL stays below the +80 baseline. Action: Steal the ACO filters from bot 04/05 only after locking the IPR +80 base layer.
- **Current Noel canonical candidate crossed 10k on platform artifact**: candidate_10_bot02_carry_tight_mm official profit is 10007.0: IPR 7286.0, ACO 2721.0. Action: Use this artifact as the primary ranking baseline, not the local replay scale.
- **Pure microstructure underuses the dominant IPR carry**: candidate_11_bot03_micro_scalper official profit is 1542.2, with only 694.6 IPR PnL. Action: Do not promote microstructure-only bots unless they keep +80 IPR carry as a base layer.

## Best Current Evidence

- Best official artifact: `candidate_26_v3_a3b1_one_sided_exit_overlay` with PnL `10090.47`.
- Bot path: `rounds/round_1/bots/noel/canonical/candidate_26_v3_a3b1_one_sided_exit_overlay.py`.
- Product split: IPR `7286.00`, ACO `2804.47`.
- The next strategy loop should optimize ACO around the current max-long IPR base, because IPR carry is already near solved in these artifacts.

## Promotion Gate

Before a bot is promoted for another platform attempt:

- Save the exact `.py`, platform `.json`, and `.log` together, or mark missing logs as a caveat.
- Rank by JSON `profit`; use final `activitiesLog` product PnL to explain the score.
- Require `product_pnl_sum_from_activities` delta `0.0` versus JSON `profit`; otherwise treat the artifact as suspect.
- Treat `graphLog` and trade reconstruction deltas as audit tolerances, not score sources.
- Compare to the current bar: total `10007.0`, IPR `7286.0`, ACO `2721.0`.
- Use local replay only for sanity checks: contract errors, position limits, and obvious fill behavior.

## Iteration Backlog

- `candidate_10 + ACO Markov filter`: preserve +80 IPR, borrow bot 04's ACO filter only when it improves edge without lowering matched volume too much.
- `candidate_10 + ACO adaptive skew`: preserve FV=10000 base, but skew quotes away from accumulating stale ACO inventory late in the run.
- `candidate_10 + edge threshold sweep`: test fewer but cleaner ACO fills; target higher average roundtrip edge than Amin 23/25.
- `candidate_10 + late flatten`: keep passive ACO early, then reduce inventory risk near the end; current best finishes ACO flat.
- `hybrid rescue`: only keep bot 05 ideas that do not give up the IPR +80 carry layer.

## Interpretation Limits

- These are platform-style execution artifacts, not official round rules.
- Some artifacts are historical or misfiled; path location does not change their analytical value, but promotion should reference canonical performance summaries.
- Trade reconstruction matches only when the matching `.log` exists and own trades are complete; use it as audit, not primary score.

## Next Action

- Treat `candidate_26_v3_a3b1_one_sided_exit_overlay` as the current recommended platform candidate, with `candidate_10_bot02_carry_tight_mm.py` retained as the robustness baseline.
- Iterate ACO variants against the platform JSON methodology: target higher ACO PnL without reducing IPR max-long behavior.
- Preserve every platform run as JSON/log and rerun this analyzer before promotion.
