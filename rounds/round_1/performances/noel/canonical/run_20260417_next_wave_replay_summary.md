# Next-Wave Immediate-Fill Replay

## Method

- This is a local sanity replay, not official Prosperity PnL.
- It models immediate fills against visible sample books only.
- Platform ranking must use JSON `profit` once platform artifacts exist.
- Baseline bar: total `10007.0`, IPR `7286.0`, ACO `2721.0` from platform-style artifact analysis.

## Ranking

| Rank | Bot | Total Replay PnL | IPR Replay PnL | ACO Replay PnL | Rejections | Errors |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `candidate_10_bot02_carry_tight_mm.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |
| 2 | `candidate_19_ipr_execution_upgrade.py` | 247628.00 | 238054.00 | 9574.00 | 0 | 0 |
| 3 | `candidate_14_aco_kalman_latent_fv.py` | 247203.00 | 238054.00 | 9149.00 | 0 | 0 |
| 4 | `candidate_23_adaptive_aco_controller.py` | 246435.00 | 238054.00 | 8381.00 | 0 | 0 |
| 5 | `candidate_18_aco_offline_policy_table.py` | 246090.00 | 238054.00 | 8036.00 | 0 | 0 |
| 6 | `candidate_21_one_sided_book_specialist.py` | 245936.00 | 238054.00 | 7882.00 | 0 | 0 |
| 7 | `candidate_22_micro_alpha_rescue.py` | 244976.00 | 238054.00 | 6922.00 | 0 | 0 |
| 8 | `candidate_15_aco_hmm_regime_mm.py` | 244829.00 | 238054.00 | 6775.00 | 0 | 0 |
| 9 | `candidate_20_dual_product_risk_scheduler.py` | 243230.00 | 238054.00 | 5176.00 | 0 | 0 |
| 10 | `candidate_16_aco_edge_quality_gate.py` | 241372.00 | 238054.00 | 3318.00 | 0 | 0 |
| 11 | `candidate_17_aco_inventory_lifecycle.py` | 240317.50 | 238054.00 | 2263.50 | 0 | 0 |

## Interpretation

- Use this ranking to catch broken or obviously weak branches.
- Do not use this PnL scale for promotion.
- Upload selected bots to Prosperity, save `.py` + `.json` + `.log`, then rerun `analyze_platform_artifacts.py`.
