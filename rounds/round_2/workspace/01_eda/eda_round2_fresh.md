# Round 2 Consolidated EDA

## Status

`COMPLETED`

Review outcome: `approved with caveats`.

Caveats: sample-data evidence is not an official rule; final platform distribution and randomized quote subset may differ; MAF bid and manual RSS allocation remain separate downstream decisions; trade pressure still needs better platform `market_trades` logs.

## Question

- Question: Which Round 2 product, market-access, validation, manual-allocation, multivariate, and process/distribution signals are decision-useful enough to feed Understanding and later strategy/spec work?
- Product scope: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Why this matters downstream: this is the evidence gate before strategy generation; no bot logic is implemented here.
- Consolidation note: this report supersedes the earlier fresh EDA text as the single canonical EDA handoff for Understanding. It preserves the first-pass findings and adds the new multivariate/process layer.

## Executive Handoff

- `INTARIAN_PEPPER_ROOT` remains a strong drift/residual product: the process layer supports drift-aware fair value, not a fixed Round 1 fair value.
- `ASH_COATED_OSMIUM` remains a short-horizon mean-reversion candidate: the process layer supports reversal-style strategy tests, but only with spread/fill validation.
- `top_imbalance` remains the cleanest order-book directional feature; `microprice_deviation` is a new exploratory challenger because it compresses top imbalance and spread.
- `full-book imbalance` is useful but no longer an automatic co-primary signal; redundancy and controlled checks make it a backup/context feature unless validation beats top imbalance.
- `spread regime` should be promoted as an execution/risk filter candidate, not a standalone alpha signal.
- Cross-product lead-lag evidence is weak enough to keep out of the first strategy candidate queue.
- PCA and clustering are useful for feature simplification/regime diagnostics only; do not implement latent components or clusters directly.
- Controlled regression strongest rows: ASH_COATED_OSMIUM h1 top_imbalance coef=2.313 p=0; INTARIAN_PEPPER_ROOT h5 drift_residual_z coef=-1.418 p=0; INTARIAN_PEPPER_ROOT h3 drift_residual_z coef=-1.411 p=0.
- Max absolute cross-product mid-delta lead-lag correlation is -0.016 at lag 8; this is not enough to drive first-pass strategy.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | yes | yes | likely | include |
| INTARIAN_PEPPER_ROOT | yes | yes | likely | include |

- Product-scope rationale: both products are official Round 2 algorithmic products with limit 80.
- Product branches: one combined EDA, with product-specific rows where behavior differs materially.

## Algorithmic vs Manual Scope

| Finding | Scope | Why | Caveat |
| --- | --- | --- | --- |
| Product signals from price/order-book CSVs | algorithmic | Fields map to TradingState order_depths/mid proxies. | Sample data evidence is not an official rule. |
| Market Access Fee scenarios | algorithmic / final-round decision | Trader.bid() is Round 2-specific. | Testing ignores bid(); competitor bid distribution unknown. |
| Research / Scale / Speed grid | manual | Manual challenge allocation outside Trader.run(). | Speed multiplier is rank-based and unknown before close. |
| PCA / clustering / latent-style diagnostics | EDA-only | Useful for redundancy and regime hypotheses. | Do not implement components/clusters directly without an online proxy. |

## Challenge Boundary / Do Not Mix

Round 2 has separate decision tracks. Understanding should preserve this boundary so manual allocation conclusions never become bot features, and algorithmic market signals never become manual allocation evidence.

| Track | Decision Owner | Inputs | Outputs | Must Not Use |
| --- | --- | --- | --- | --- |
| Algorithmic trading | strategy/spec/Trader | order books, prices, trades/logs, position limits | signals, execution filters, risk controls, validation checks | manual Research/Scale/Speed allocation as bot signal |
| Market Access Fee | strategy/spec/human risk posture | Round 2 bid mechanics, extra quote access proxy, competitor uncertainty | bid scenario evidence and later bid decision | testing PnL as final bid proof; manual Speed assumptions |
| Manual challenge | human/manual submission | official Research/Scale/Speed formula and rank scenarios | manual allocation candidates only | order-book signals, bot features, or Market Access Fee as manual formula inputs |

## Data Sources

- Raw data: `rounds/round_2/data/raw/prices_round_2_day_-1.csv`, `day_0`, `day_1`, plus matching trades files.
- Processed data: tables and plots in `rounds/round_2/workspace/01_eda/artifacts/`.
- Run or log artifact: `rounds/round_2/performances/noel/historical/baseline_state_logger.json`.
- Post-run research memory: absent at EDA start; expected because Round 2 has no prior validated bot run cycle.

## Round Adaptation Check

| Check | Current-Round Evidence | Decision / Action |
| --- | --- | --- |
| Active round mechanics/API | Round 2 wiki defines Trader.bid() for Market Access Fee | EDA-only value estimate; final bid belongs to strategy/spec |
| Products and limits | Round 2 wiki: ACO/IPR, limit 80 each | verified |
| Data schema | raw CSVs and platform activitiesLog share price ladder schema | classified |
| New or changed fields/mechanics | Market Access Fee, randomized 80% testing quotes, manual RSS allocation | EDA questions included |
| Prior-round assumption at risk | Round 1 product hints and bot constants | revalidate; do not carry as facts |

## Artifact Index

| artifact_path | type | source_data | useful_for | decision_relevant |
| --- | --- | --- | --- | --- |
| rounds/round_2/workspace/01_eda/artifacts/data_quality_summary.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | data_quality_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/product_behavior_summary.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | product_behavior_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/round1_assumption_check.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | round1_assumption_check | yes |
| rounds/round_2/workspace/01_eda/artifacts/imbalance_ic.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | imbalance_ic | yes |
| rounds/round_2/workspace/01_eda/artifacts/conditional_imbalance_ic.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | conditional_imbalance_ic | yes |
| rounds/round_2/workspace/01_eda/artifacts/trade_flow_summary.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | trade_flow_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/trade_pressure_proxy.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | trade_pressure_proxy | yes |
| rounds/round_2/workspace/01_eda/artifacts/platform_comparability.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | platform_comparability | yes |
| rounds/round_2/workspace/01_eda/artifacts/maf_scenarios.csv | table | Round 2 wiki Market Access Fee mechanics / sample-data opportunity proxy | maf_scenarios | yes |
| rounds/round_2/workspace/01_eda/artifacts/manual_scenario_grid_top.csv | table | Round 2 wiki manual formula / Research-Scale-Speed scenario grid | manual_scenario_grid_top | yes |
| rounds/round_2/workspace/01_eda/artifacts/manual_scenario_summary.csv | table | Round 2 wiki manual formula / Research-Scale-Speed scenario grid | manual_scenario_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/feature_inventory.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | feature_inventory | yes |
| rounds/round_2/workspace/01_eda/artifacts/feature_promotion_decisions.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | feature_promotion_decisions | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_mid_price_by_product_day.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_mid_price_by_product_day | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_spread_distribution.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_spread_distribution | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_returns_distribution.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_returns_distribution | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_imbalance_ic.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_imbalance_ic | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_platform_comparability.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_platform_comparability | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_maf_scenarios.png | plot | Round 2 wiki Market Access Fee mechanics / sample-data opportunity proxy | plot_maf_scenarios | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_manual_scenarios.png | plot | Round 2 wiki manual formula / Research-Scale-Speed scenario grid | plot_manual_scenarios | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_drift_residuals.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_drift_residuals | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_feature_correlation.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_feature_correlation | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_feature_covariance.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_feature_covariance | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_top_correlations.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_top_correlations | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_redundancy_analysis.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_redundancy_analysis | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_vif.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_vif | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_regression_summary.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_regression_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_mutual_information.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_mutual_information | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_pca_explained_variance.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_pca_explained_variance | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_pca_loadings.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_pca_loadings | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_cross_product_relationships.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_cross_product_relationships | yes |
| rounds/round_2/workspace/01_eda/artifacts/multivariate_cluster_summary.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | multivariate_cluster_summary | yes |
| rounds/round_2/workspace/01_eda/artifacts/process_distribution_metrics.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | process_distribution_metrics | yes |
| rounds/round_2/workspace/01_eda/artifacts/process_distribution_hypotheses.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | process_distribution_hypotheses | yes |
| rounds/round_2/workspace/01_eda/artifacts/expanded_feature_promotion_decisions.csv | table | Round 2 raw CSVs / platform JSON / derived EDA tables | expanded_feature_promotion_decisions | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_multivariate_correlation_ASH_COATED_OSMIUM.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_multivariate_correlation_ASH_COATED_OSMIUM | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_multivariate_correlation_INTARIAN_PEPPER_ROOT.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_multivariate_correlation_INTARIAN_PEPPER_ROOT | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_multivariate_pca_explained_variance.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_multivariate_pca_explained_variance | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_multivariate_cross_product_lead_lag.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_multivariate_cross_product_lead_lag | yes |
| rounds/round_2/workspace/01_eda/artifacts/plot_process_diagnostics.png | plot | Round 2 raw CSVs / platform JSON / derived EDA tables | plot_process_diagnostics | yes |

## Data Quality And Filters

- Row counts by file and product: see `data_quality_summary.csv`.
- Timestamp coverage and gaps: raw prices cover three days with 10,000 rows per product/day; platform activities cover 1,000 rows per product on day 1.
- Missing bid/ask counts: measured in data quality and comparability tables; one-sided books are preserved, not dropped globally.
- Zero or blank `mid_price` counts: measured; non-positive mids are treated as missing for analysis.
- Filters applied: signal IC/regression/MI/PCA use rows with non-null feature and target; product stats use available mid rows; platform comparison uses overlapping timestamps.
- Findings based on: mixed raw rows and filtered rows, stated per table.
- Data quality caveats: the platform `.log` is empty and the JSON does not contain `ROUND2_STATE_PROBE`; treat it as platform activity evidence, not raw printed state evidence.

| source | kind | line_count_incl_header | rows | products | day_values | timestamp_min | timestamp_max | duplicate_product_timestamp_rows | missing_mid_price_rows | zero_mid_price_rows | missing_best_bid_rows | missing_best_ask_rows | status | profit | has_round2_state_probe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rounds/round_2/data/raw/prices_round_2_day_-1.csv | raw_prices | 20001.0 | 20000 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | -1 | 0.0 | 999900.0 | 0.0 | 28.0 | 28.0 | 759.0 | 786.0 |  |  |  |
| rounds/round_2/data/raw/prices_round_2_day_0.csv | raw_prices | 20001.0 | 20000 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | 0 | 0.0 | 999900.0 | 0.0 | 34.0 | 34.0 | 795.0 | 752.0 |  |  |  |
| rounds/round_2/data/raw/prices_round_2_day_1.csv | raw_prices | 20001.0 | 20000 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | 1 | 0.0 | 999900.0 | 0.0 | 38.0 | 38.0 | 776.0 | 800.0 |  |  |  |
| rounds/round_2/data/raw/trades_round_2_day_-1.csv | raw_trades | 791.0 | 790 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | from file name | 0.0 | 997000.0 | 7.0 |  |  |  |  |  |  |  |
| rounds/round_2/data/raw/trades_round_2_day_0.csv | raw_trades | 804.0 | 803 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | from file name | 0.0 | 995200.0 | 6.0 |  |  |  |  |  |  |  |
| rounds/round_2/data/raw/trades_round_2_day_1.csv | raw_trades | 799.0 | 798 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | from file name | 0.0 | 997200.0 | 10.0 |  |  |  |  |  |  |  |
| rounds/round_2/performances/noel/historical/baseline_state_logger.json | platform_json | 1.0 | 1 | from activitiesLog | 2 |  |  |  |  |  |  |  | FINISHED | 0.0 | False |
| rounds/round_2/performances/noel/historical/baseline_state_logger.json::activitiesLog | platform_activities |  | 2000 | ASH_COATED_OSMIUM,INTARIAN_PEPPER_ROOT | 1 | 0.0 | 99900.0 | 0.0 | 2.0 | 2.0 | 83.0 | 83.0 | FINISHED | 0.0 | False |

## Round 1 Assumption Check

| assumption_or_hint | round2_evidence | verdict | downstream_action |
| --- | --- | --- | --- |
| IPR is steady from Round 1 hint | Mean day total change 999.67, mean linear R2 1.000. | contradicted | Model current-round drift explicitly before using any fixed fair value. |
| IPR may have stable drift/residual structure | Mean linear R2 1.000; residual std mean 2.37. | supported | Consider drift plus residual features in understanding, with validation on all days. |
| ACO is volatile or patterned | Mean mid std 5.05; mean delta AC1 -0.501. | supported | Consider short-horizon mean-reversion evidence, not a broad volatility claim. |
| Book imbalance can help predict short horizon movement | Mean IC@1 for top imbalance 0.648. | supported | Promote only if stable by product/day and still online-usable. |
| Round 1 trade frequency/fill assumptions carry forward | Trade rows by product/day exist but market flow is sparse: mean rows 398.5. | unknown | Do not carry fill assumptions; use Round 2 platform validation later. |

## Product Behavior Summary

| product | day | rows | usable_mid_rows | mid_first | mid_last | mid_mean | mid_std | mid_min | mid_q05 | mid_q50 | mid_q95 | mid_max | total_change | linear_slope_per_timestamp | linear_r2 | linear_residual_std | delta_std | delta_abs_q95 | delta_ac1 | delta_ac2 | mid_ac1 | arch_lm_pvalue_delta | spread_mean | spread_median | spread_q95 | two_sided_rate | one_sided_rate | change_points_mid_index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | -1 | 10000 | 9985 | 9991.0 | 10002.0 | 10000.8251 | 4.4669 | 9981.0 | 9993.0 | 10001.0 | 10008.0 | 10020.0 | 11.0 | -0.0 | 0.0012 | 4.4643 | 3.6953 | 8.5 | -0.5063 | 0.0189 | 0.6578 | 0.0 | 16.224 | 16.0 | 19.0 | 0.9251 | 0.0749 | 6350,7200,8595 |
| ASH_COATED_OSMIUM | 0 | 10000 | 9984 | 10003.0 | 10008.0 | 10001.6074 | 5.6596 | 9979.0 | 9991.5 | 10002.0 | 10011.0 | 10023.0 | 5.0 | 0.0 | 0.0064 | 5.6414 | 3.6858 | 9.0 | -0.5064 | 0.0141 | 0.7879 | 0.0 | 16.2495 | 16.0 | 19.0 | 0.9272 | 0.0728 | 6515,7490,9055 |
| ASH_COATED_OSMIUM | 1 | 10000 | 9978 | 10008.0 | 9993.0 | 10000.2054 | 5.0187 | 9980.0 | 9992.0 | 10000.0 | 10008.5 | 10019.0 | -15.0 | -0.0 | 0.1679 | 4.578 | 3.6853 | 8.5 | -0.4905 | -0.005 | 0.7303 | 0.0 | 16.2289 | 16.0 | 19.0 | 0.9234 | 0.0766 | 2200,4510,9615 |
| INTARIAN_PEPPER_ROOT | -1 | 10000 | 9987 | 11001.5 | 11999.5 | 11500.1244 | 288.6535 | 10998.0 | 11050.0 | 11500.0 | 11950.0 | 12001.5 | 998.0 | 0.001 | 0.9999 | 2.1946 | 3.1079 | 6.5 | -0.4979 | -0.0074 | 0.9999 | 0.0 | 13.0667 | 13.0 | 16.0 | 0.9258 | 0.0742 | 2480,4980,7480 |
| INTARIAN_PEPPER_ROOT | 0 | 10000 | 9982 | 11998.5 | 13000.0 | 12499.866 | 288.6096 | 11996.0 | 12050.0 | 12500.0 | 12950.0 | 13008.0 | 1001.5 | 0.001 | 0.9999 | 2.3642 | 3.3162 | 7.0 | -0.4889 | -0.0138 | 0.9999 | 0.0 | 14.121 | 14.0 | 17.0 | 0.9247 | 0.0753 | 2500,4990,7510 |
| INTARIAN_PEPPER_ROOT | 1 | 10000 | 9984 | 13000.0 | 13999.5 | 13500.0573 | 288.7464 | 12995.0 | 13050.0 | 13500.5 | 13950.5 | 14003.0 | 999.5 | 0.001 | 0.9999 | 2.5428 | 3.5781 | 7.5 | -0.5084 | 0.0312 | 0.9999 | 0.0 | 15.177 | 15.0 | 19.0 | 0.9263 | 0.0737 | 2475,4985,7490 |

## Process / Distribution Hypotheses

This layer is deliberately lightweight: it frames the approximate data-generating process and what downstream phases should do differently.

| product_or_scope | hypothesized_process | evidence | confidence | online_observables | downstream_implication | suggested_next_test | status | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | short-horizon mean-reverting microstructure process | mean linear R2=0.059; mean delta AC1=-0.500; mean day change=0.33; ARCH-day share=1.00 | medium/high | mid/order_depths, timestamp, spread, rolling delta/residual | Test reversal/fair-value adjustment with spread and fill validation. Volatility clustering may matter for sizing/defensive filters. | Validate markout/PnL under reviewed spec and platform quote subset. | promote | Sample data evidence; final platform distribution can differ. |
| INTARIAN_PEPPER_ROOT | strong deterministic trend plus residual mean-reversion/noise | mean linear R2=1.000; mean delta AC1=-0.498; mean day change=999.67; ARCH-day share=1.00 | high | mid/order_depths, timestamp, spread, rolling delta/residual | Use drift-aware fair value/residual features; do not use a fixed fair value. Volatility clustering may matter for sizing/defensive filters. | Validate markout/PnL under reviewed spec and platform quote subset. | promote | Sample data evidence; final platform distribution can differ. |

### Process Metrics

| product | day | mid_first | mid_last | total_change | linear_r2 | residual_std | delta_ac1 | delta_ac2 | delta_skew | delta_kurtosis | bimodality_coefficient | rolling_vol_50_mean | rolling_vol_50_cv | arch_pvalue | change_point_candidates |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | -1 | 9991.0 | 10002.0 | 11.0 | 0.0012 | 4.4643 | -0.5064 | 0.018 | 0.0476 | 6.1852 | 0.162 | 3.6514 | 0.2199 | 0.0 | deferred_low_roi |
| ASH_COATED_OSMIUM | 0 | 10003.0 | 10008.0 | 5.0 | 0.0064 | 5.6414 | -0.5058 | 0.0152 | -0.017 | 6.2582 | 0.1598 | 3.6223 | 0.2391 | 0.0 | deferred_low_roi |
| ASH_COATED_OSMIUM | 1 | 10008.0 | 9993.0 | -15.0 | 0.1679 | 4.578 | -0.4878 | -0.0056 | 0.0075 | 6.027 | 0.1659 | 3.6379 | 0.2096 | 0.0 | deferred_low_roi |
| INTARIAN_PEPPER_ROOT | -1 | 11001.5 | 11999.5 | 998.0 | 0.9999 | 2.1946 | -0.4976 | -0.0073 | 0.0545 | 5.982 | 0.1677 | 3.0695 | 0.2174 | 0.0 | deferred_low_roi |
| INTARIAN_PEPPER_ROOT | 0 | 11998.5 | 13000.0 | 1001.5 | 0.9999 | 2.3642 | -0.4889 | -0.0132 | -0.0113 | 5.8275 | 0.1716 | 3.2729 | 0.2134 | 0.0 | deferred_low_roi |
| INTARIAN_PEPPER_ROOT | 1 | 13000.0 | 13999.5 | 999.5 | 0.9999 | 2.5428 | -0.507 | 0.0284 | -0.0163 | 6.0012 | 0.1667 | 3.5322 | 0.2216 | 0.0 | deferred_low_roi |

## Feature Inventory

First-pass inventory from the original EDA:

| feature | origin | online_usability | meaning | role | signal_strength | stability | actionability | lifecycle_decision | notes_caveats |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift plus residual | csv | usable online | Linear current-round IPR drift with smaller residual variation. | direct signal | strong | stable | changes strategy | promote | Mean linear R2 1.000; must avoid sample-end assumptions. |
| ACO short-horizon mean reversion | csv | usable online | ACO mid deltas tend to reverse at lag 1. | direct signal | strong | stable | changes strategy | promote | Mean delta AC1 -0.501; needs execution validation. |
| top imbalance | csv | usable online | Best-level bid/ask volume skew. | direct signal | strong | stable | changes parameters | promote | Mean IC@1 0.648; test conditional stability. |
| full-book imbalance | csv | usable online | Three-level total bid/ask depth skew. | direct signal | strong | stable | changes parameters | promote | Mean IC@1 0.390; top imbalance may be simpler. |
| spread regime | csv | usable online | Wide/tight spread state from best bid/ask. | execution filter | medium | day-sensitive | changes validation | exploratory | Mean spread q95 18.17; filter needs PnL validation. |
| liquidity/depth regime | csv | usable online | Total visible depth and one-sided-book conditions. | risk control | medium | regime-dependent | changes risk | exploratory | Mean one-sided rate 0.075; use defensively first. |
| trade pressure proxy | combined | usable online | Trade price relative to mid signs recent flow. | diagnostic | weak | unknown | changes validation | needs logs | Mean trade rows per product/day 398.5; needs platform market_trades logs. |
| platform quote-subset comparability | log/post-run | EDA-only | Difference between sample day 1 and platform activitiesLog quote subset. | diagnostic | medium | unknown | changes validation | EDA-only calibration | Platform overlap rows min 1000.0; no printed state probe lines. |

## Feature Promotion Decisions

Expanded decisions after multivariate/process checks. This is the table Understanding should consume first.

| feature_or_signal | decision | destination | reason | multivariate_note | caveat_reopen_condition |
| --- | --- | --- | --- | --- | --- |
| IPR drift plus residual | promote | Understanding / strategy candidates | Trend process is extremely stable by day; residual feature is online-computable from timestamp and current mids. | Keep as product-specific fair-value basis, not as global price constant. | Reopen if platform run shows final-day drift materially differs. |
| ACO short-horizon delta reversal | promote | Understanding / strategy candidates | Negative delta autocorrelation and controlled models support reversal framing. | Use with spread/depth controls; avoid stacking with redundant residual variants. | Reopen if fills/markouts show adverse selection dominates. |
| top imbalance | promote | Understanding / strategy candidates | Strong IC and direct online availability; often simpler than full-book variants. | Highly related to microprice; choose one primary edge feature first. | Reopen if controlled model shows microprice dominates robustly. |
| microprice deviation | exploratory | Understanding research memory | A compact transformation of top-of-book imbalance and spread that may encode pressure plus distance. | Likely redundant with top imbalance; promote only if controlled lift is clear. | Promote if validation beats top imbalance alone. |
| full-book imbalance | exploratory/promote as backup | Understanding / backup strategy evidence | Useful IC but redundancy checks suggest it can conflict with or duplicate simpler top imbalance. | Use as backup or defensive context, not automatically alongside top imbalance. | Promote if it outperforms top imbalance under wide/one-sided regimes. |
| spread regime | promote as execution/risk filter candidate | Understanding / spec validation checks | Spread materially changes execution economics and appears in controlled models/regime checks. | Role should be filter/sizing/risk, not primary directional signal. | Reject if platform PnL improves without spread gating. |
| liquidity/depth regime | exploratory | Understanding research memory | Depth and missing levels affect quote quality, but clustering is mostly descriptive. | Use defensively first; avoid adding multiple depth features. | Promote only if run diagnostics show depth predicts fills/markouts. |
| cross-product lead-lag | negative evidence | Negative Evidence | Lead-lag correlations are weak relative to direct within-product signals. | Do not build first strategy around cross-product prediction. | Reopen only if platform logs show product coupling not present in sample. |
| trade pressure proxy | needs logs | Future platform diagnostics | CSV trade alignment is sparse and platform printed state probe is missing. | Useful as diagnostic hypothesis, not first spec feature. | Reopen after collecting market_trades from TradingState logs. |
| PCA/cluster latent components | EDA-only calibration | Research memory only | Helpful for redundancy/regime framing but not online bot logic. | Use to simplify feature set and validation, not as direct model input. | Only implement if spec defines a simple online proxy. |

Earlier first-pass promotion decisions are preserved here for provenance:

| feature_or_signal | decision | destination | reason | caveat_reopen_condition |
| --- | --- | --- | --- | --- |
| IPR drift plus residual | promote | Understanding / strategy candidates | strong signal, stable stability, changes strategy. | Mean linear R2 1.000; must avoid sample-end assumptions. |
| ACO short-horizon mean reversion | promote | Understanding / strategy candidates | strong signal, stable stability, changes strategy. | Mean delta AC1 -0.501; needs execution validation. |
| top imbalance | promote | Understanding / strategy candidates | strong signal, stable stability, changes parameters. | Mean IC@1 0.648; test conditional stability. |
| full-book imbalance | promote | Understanding / strategy candidates | strong signal, stable stability, changes parameters. | Mean IC@1 0.390; top imbalance may be simpler. |
| spread regime | exploratory | EDA report only | Potentially useful but not ready for spec or implementation. | Mean spread q95 18.17; filter needs PnL validation. |
| liquidity/depth regime | exploratory | EDA report only | Potentially useful but not ready for spec or implementation. | Mean one-sided rate 0.075; use defensively first. |
| trade pressure proxy | needs logs | Future platform diagnostics | Sample trades are insufficient for implementation decisions. | Mean trade rows per product/day 398.5; needs platform market_trades logs. |
| platform quote-subset comparability | EDA-only calibration | Validation planning | Diagnostic evidence affects comparability, not bot logic. | Platform overlap rows min 1000.0; no printed state probe lines. |

## Multivariate Feature Map

Run on serious engineered features only. These checks are for feature selection, redundancy, and process evidence, not for direct bot model import.

### Top Pairwise Feature Correlations

| product | feature_a | feature_b | correlation | abs_correlation |
| --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | spread | relative_spread | 1.0 | 1.0 |
| ASH_COATED_OSMIUM | top_imbalance | microprice_deviation | 0.9587 | 0.9587 |
| INTARIAN_PEPPER_ROOT | top_imbalance | microprice_deviation | 0.9575 | 0.9575 |
| INTARIAN_PEPPER_ROOT | trade_count | trade_quantity | 0.9549 | 0.9549 |
| INTARIAN_PEPPER_ROOT | spread | relative_spread | 0.9338 | 0.9338 |
| INTARIAN_PEPPER_ROOT | book_imbalance | depth_ratio | 0.9176 | 0.9176 |
| ASH_COATED_OSMIUM | trade_count | trade_quantity | 0.9164 | 0.9164 |
| INTARIAN_PEPPER_ROOT | z_mid_50 | drift_residual_z | 0.9144 | 0.9144 |
| ASH_COATED_OSMIUM | book_imbalance | depth_ratio | 0.8818 | 0.8818 |
| ASH_COATED_OSMIUM | book_total_volume | missing_level_count | -0.8058 | 0.8058 |
| INTARIAN_PEPPER_ROOT | top_imbalance | drift_residual_z | -0.8049 | 0.8049 |
| INTARIAN_PEPPER_ROOT | book_total_volume | missing_level_count | -0.8044 | 0.8044 |
| INTARIAN_PEPPER_ROOT | top_imbalance | z_mid_50 | -0.7426 | 0.7426 |
| ASH_COATED_OSMIUM | relative_spread | top_total_volume | 0.6899 | 0.6899 |
| ASH_COATED_OSMIUM | spread | top_total_volume | 0.6899 | 0.6899 |
| INTARIAN_PEPPER_ROOT | relative_spread | top_total_volume | 0.6579 | 0.6579 |
| INTARIAN_PEPPER_ROOT | microprice_deviation | drift_residual_z | -0.6553 | 0.6553 |
| INTARIAN_PEPPER_ROOT | spread | top_total_volume | 0.6214 | 0.6214 |
| INTARIAN_PEPPER_ROOT | microprice_deviation | z_mid_50 | -0.6095 | 0.6095 |
| ASH_COATED_OSMIUM | top_imbalance | z_mid_50 | -0.5956 | 0.5956 |
| ASH_COATED_OSMIUM | top_total_volume | missing_level_count | 0.593 | 0.593 |
| ASH_COATED_OSMIUM | relative_spread | missing_level_count | 0.583 | 0.583 |
| ASH_COATED_OSMIUM | spread | missing_level_count | 0.583 | 0.583 |
| INTARIAN_PEPPER_ROOT | relative_spread | missing_level_count | 0.5815 | 0.5815 |
| INTARIAN_PEPPER_ROOT | rolling_vol_50 | rolling_vol_200 | 0.5662 | 0.5662 |
| INTARIAN_PEPPER_ROOT | spread | missing_level_count | 0.5467 | 0.5467 |
| INTARIAN_PEPPER_ROOT | top_total_volume | missing_level_count | 0.5462 | 0.5462 |
| ASH_COATED_OSMIUM | microprice_deviation | z_mid_50 | -0.5155 | 0.5155 |
| ASH_COATED_OSMIUM | mid_delta_lag1 | mid_delta_lag2 | -0.5058 | 0.5058 |
| INTARIAN_PEPPER_ROOT | mid_delta_lag1 | mid_delta_lag2 | -0.4998 | 0.4998 |

### Redundancy / Dimensionality Check

| product | feature_a | feature_b | correlation | abs_correlation | decision | downstream_effect |
| --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | spread | relative_spread | 1.0 | 1.0 | merge_or_choose_simpler | Use absolute spread for execution unless relative spread adds cross-product comparability. |
| ASH_COATED_OSMIUM | top_imbalance | microprice_deviation | 0.9587 | 0.9587 | merge_or_choose_simpler | Prefer top_imbalance unless microprice gives controlled lift. |
| INTARIAN_PEPPER_ROOT | top_imbalance | microprice_deviation | 0.9575 | 0.9575 | merge_or_choose_simpler | Prefer top_imbalance unless microprice gives controlled lift. |
| INTARIAN_PEPPER_ROOT | trade_count | trade_quantity | 0.9549 | 0.9549 | merge_or_choose_simpler | Check controlled model before stacking both features. |
| INTARIAN_PEPPER_ROOT | spread | relative_spread | 0.9338 | 0.9338 | merge_or_choose_simpler | Use absolute spread for execution unless relative spread adds cross-product comparability. |
| INTARIAN_PEPPER_ROOT | book_imbalance | depth_ratio | 0.9176 | 0.9176 | merge_or_choose_simpler | Check controlled model before stacking both features. |
| ASH_COATED_OSMIUM | trade_count | trade_quantity | 0.9164 | 0.9164 | merge_or_choose_simpler | Check controlled model before stacking both features. |
| INTARIAN_PEPPER_ROOT | z_mid_50 | drift_residual_z | 0.9144 | 0.9144 | merge_or_choose_simpler | Check controlled model before stacking both features. |
| ASH_COATED_OSMIUM | book_imbalance | depth_ratio | 0.8818 | 0.8818 | merge_or_choose_simpler | Check controlled model before stacking both features. |

### VIF Redundancy Screen

| product | feature | vif | decision_note |
| --- | --- | --- | --- |
| ASH_COATED_OSMIUM | top_imbalance | 12.9808 | high redundancy |
| ASH_COATED_OSMIUM | microprice_deviation | 12.758 | high redundancy |
| ASH_COATED_OSMIUM | drift_residual_z | 1.0841 | acceptable |
| ASH_COATED_OSMIUM | spread | 1.0533 | acceptable |
| ASH_COATED_OSMIUM | book_total_volume | 1.037 | acceptable |
| ASH_COATED_OSMIUM | book_imbalance | 1.0261 | acceptable |
| ASH_COATED_OSMIUM | trade_pressure_qty | 1.0003 | acceptable |
| ASH_COATED_OSMIUM | mid_delta_lag1 | 1.0002 | acceptable |
| INTARIAN_PEPPER_ROOT | top_imbalance | 35.9092 | high redundancy |
| INTARIAN_PEPPER_ROOT | microprice_deviation | 22.3092 | high redundancy |
| INTARIAN_PEPPER_ROOT | drift_residual_z | 5.3701 | high redundancy |
| INTARIAN_PEPPER_ROOT | trade_pressure_qty | 1.0787 | acceptable |
| INTARIAN_PEPPER_ROOT | spread | 1.0515 | acceptable |
| INTARIAN_PEPPER_ROOT | book_total_volume | 1.0469 | acceptable |
| INTARIAN_PEPPER_ROOT | book_imbalance | 1.0368 | acceptable |
| INTARIAN_PEPPER_ROOT | mid_delta_lag1 | 1.0004 | acceptable |

### PCA Explained Variance

| product | component | explained_variance_ratio | cumulative_explained_variance |
| --- | --- | --- | --- |
| ASH_COATED_OSMIUM | PC1 | 0.182 | 0.182 |
| ASH_COATED_OSMIUM | PC2 | 0.1454 | 0.3274 |
| ASH_COATED_OSMIUM | PC3 | 0.1067 | 0.4341 |
| ASH_COATED_OSMIUM | PC4 | 0.1038 | 0.5379 |
| ASH_COATED_OSMIUM | PC5 | 0.0836 | 0.6216 |
| INTARIAN_PEPPER_ROOT | PC1 | 0.1938 | 0.1938 |
| INTARIAN_PEPPER_ROOT | PC2 | 0.1815 | 0.3753 |
| INTARIAN_PEPPER_ROOT | PC3 | 0.1057 | 0.481 |
| INTARIAN_PEPPER_ROOT | PC4 | 0.1038 | 0.5848 |
| INTARIAN_PEPPER_ROOT | PC5 | 0.0898 | 0.6747 |

### PCA Loadings

Top loadings are useful for understanding feature families. They are not bot features.

| product | component | feature | loading | abs_loading |
| --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | PC1 | spread | 0.4986 | 0.4986 |
| ASH_COATED_OSMIUM | PC1 | relative_spread | 0.4985 | 0.4985 |
| ASH_COATED_OSMIUM | PC1 | missing_level_count | 0.4674 | 0.4674 |
| ASH_COATED_OSMIUM | PC1 | top_total_volume | 0.4364 | 0.4364 |
| ASH_COATED_OSMIUM | PC1 | book_total_volume | -0.27 | 0.27 |
| ASH_COATED_OSMIUM | PC1 | z_mid_50 | 0.0861 | 0.0861 |
| ASH_COATED_OSMIUM | PC1 | top_imbalance | -0.0743 | 0.0743 |
| ASH_COATED_OSMIUM | PC1 | microprice_deviation | -0.0584 | 0.0584 |
| ASH_COATED_OSMIUM | PC1 | drift_residual_z | 0.05 | 0.05 |
| ASH_COATED_OSMIUM | PC1 | depth_ratio | 0.0319 | 0.0319 |
| ASH_COATED_OSMIUM | PC1 | book_imbalance | 0.0283 | 0.0283 |
| ASH_COATED_OSMIUM | PC1 | rolling_vol_200 | -0.0114 | 0.0114 |
| ASH_COATED_OSMIUM | PC1 | rolling_vol_50 | -0.011 | 0.011 |
| ASH_COATED_OSMIUM | PC1 | trade_pressure_qty | -0.0108 | 0.0108 |
| ASH_COATED_OSMIUM | PC1 | trade_quantity | 0.0053 | 0.0053 |
| ASH_COATED_OSMIUM | PC1 | mid_delta_lag2 | 0.0053 | 0.0053 |
| ASH_COATED_OSMIUM | PC1 | mid_delta_lag1 | 0.0043 | 0.0043 |
| ASH_COATED_OSMIUM | PC1 | trade_count | 0.001 | 0.001 |
| ASH_COATED_OSMIUM | PC2 | top_imbalance | 0.5585 | 0.5585 |
| ASH_COATED_OSMIUM | PC2 | microprice_deviation | 0.5449 | 0.5449 |
| ASH_COATED_OSMIUM | PC2 | z_mid_50 | -0.449 | 0.449 |
| ASH_COATED_OSMIUM | PC2 | drift_residual_z | -0.2623 | 0.2623 |
| ASH_COATED_OSMIUM | PC2 | book_imbalance | -0.2432 | 0.2432 |
| ASH_COATED_OSMIUM | PC2 | depth_ratio | -0.2023 | 0.2023 |
| ASH_COATED_OSMIUM | PC2 | top_total_volume | 0.0843 | 0.0843 |
| ASH_COATED_OSMIUM | PC2 | missing_level_count | 0.0702 | 0.0702 |
| ASH_COATED_OSMIUM | PC2 | relative_spread | 0.0602 | 0.0602 |
| ASH_COATED_OSMIUM | PC2 | spread | 0.0596 | 0.0596 |
| ASH_COATED_OSMIUM | PC2 | book_total_volume | -0.0336 | 0.0336 |
| ASH_COATED_OSMIUM | PC2 | mid_delta_lag1 | -0.0125 | 0.0125 |

## Multivariate Model Notes

OLS rows use standardized predictors and future mid delta targets. They are explanatory controls, not tuned prediction models.

| product | horizon_ticks | feature | coef_standardized | pvalue | tvalue | model_r2 | n | controlled_for |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | 1 | top_imbalance | 2.3132 | 0.0 | 39.7814 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | microprice_deviation | -1.2921 | 0.0 | -22.4143 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | drift_residual_z | -0.0944 | 0.0 | -5.6194 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | spread | -0.065 | 0.0001 | -3.9221 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | book_imbalance | -0.0353 | 0.0309 | -2.1587 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | trade_pressure_qty | -0.0292 | 0.0706 | -1.8079 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | book_total_volume | 0.0198 | 0.2275 | 1.2069 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 1 | mid_delta_lag1 | 0.0115 | 0.4761 | 0.7126 | 0.1618 | 27551 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | top_imbalance | 2.4506 | 0.0 | 41.5904 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | microprice_deviation | -1.4231 | 0.0 | -24.3632 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | drift_residual_z | -0.1151 | 0.0 | -6.7607 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | book_imbalance | -0.0588 | 0.0004 | -3.5513 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | spread | -0.0589 | 0.0004 | -3.5095 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | trade_pressure_qty | -0.0319 | 0.0512 | -1.9499 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | book_total_volume | 0.0234 | 0.1602 | 1.4045 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 3 | mid_delta_lag1 | 0.0154 | 0.3449 | 0.9445 | 0.166 | 27546 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | top_imbalance | 2.4456 | 0.0 | 40.9927 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | microprice_deviation | -1.4259 | 0.0 | -24.1082 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | drift_residual_z | -0.1556 | 0.0 | -9.0231 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | spread | -0.0352 | 0.0385 | -2.0697 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | book_imbalance | -0.0337 | 0.0444 | -2.0102 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | mid_delta_lag1 | -0.0235 | 0.1558 | -1.4194 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | trade_pressure_qty | 0.0232 | 0.1618 | 1.3991 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 5 | book_total_volume | 0.0036 | 0.8331 | 0.2107 | 0.1631 | 27540 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | top_imbalance | 2.3217 | 0.0 | 37.9319 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | microprice_deviation | -1.3313 | 0.0 | -21.94 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | drift_residual_z | -0.1996 | 0.0 | -11.28 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | book_imbalance | -0.0415 | 0.016 | -2.4088 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | spread | -0.0408 | 0.0193 | -2.34 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | mid_delta_lag1 | -0.0127 | 0.4561 | -0.7453 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | trade_pressure_qty | -0.0061 | 0.7208 | -0.3574 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| ASH_COATED_OSMIUM | 10 | book_total_volume | -0.0024 | 0.8887 | -0.14 | 0.1517 | 27529 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | drift_residual_z | -1.2481 | 0.0 | -37.7544 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | top_imbalance | 0.1511 | 0.0771 | 1.7679 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | trade_pressure_qty | -0.0255 | 0.0851 | -1.7221 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | microprice_deviation | -0.0976 | 0.1474 | -1.4489 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | mid_delta_lag1 | 0.0182 | 0.2015 | 1.2772 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | book_total_volume | 0.0136 | 0.3522 | 0.9304 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | spread | 0.0039 | 0.7915 | 0.2644 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 1 | book_imbalance | -0.0023 | 0.8747 | -0.1577 | 0.2317 | 27587 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | drift_residual_z | -1.4107 | 0.0 | -42.7269 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | microprice_deviation | 0.1984 | 0.0032 | 2.9493 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | top_imbalance | -0.2372 | 0.0055 | -2.7794 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | mid_delta_lag1 | 0.0205 | 0.1506 | 1.4375 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | trade_pressure_qty | -0.0109 | 0.4604 | -0.7382 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | book_imbalance | 0.0085 | 0.5556 | 0.5894 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | book_total_volume | 0.0071 | 0.6264 | 0.4868 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 3 | spread | -0.0013 | 0.9302 | -0.0876 | 0.2449 | 27581 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | drift_residual_z | -1.4182 | 0.0 | -42.7965 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | book_total_volume | -0.0233 | 0.1104 | -1.5964 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | top_imbalance | -0.1244 | 0.1464 | -1.4525 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | microprice_deviation | 0.075 | 0.2663 | 1.1116 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | trade_pressure_qty | -0.0152 | 0.3067 | -1.0222 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | spread | 0.0067 | 0.6465 | 0.4586 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | mid_delta_lag1 | -0.0059 | 0.6782 | -0.415 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 5 | book_imbalance | 0.001 | 0.9444 | 0.0697 | 0.2483 | 27572 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 10 | drift_residual_z | -1.1946 | 0.0 | -36.0905 | 0.2322 | 27557 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 10 | top_imbalance | 0.2572 | 0.0026 | 3.0062 | 0.2322 | 27557 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 10 | microprice_deviation | -0.1665 | 0.0135 | -2.4695 | 0.2322 | 27557 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |
| INTARIAN_PEPPER_ROOT | 10 | book_imbalance | -0.0279 | 0.0549 | -1.9197 | 0.2322 | 27557 | top_imbalance,book_imbalance,microprice_deviation,spread,book_total_volume,mid_delta_lag1,drift_residual_z,trade_pressure_qty |

_Showing 60 of 64 rows._

## Mutual Information / Non-Linear Screen

Use as a ranking hint only. It can suggest threshold or non-linear follow-up, but does not override stability/actionability gates.

| product | horizon_ticks | feature | mutual_information | n | note |
| --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | 1 | spread | 0.4114 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | microprice_deviation | 0.395 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | top_imbalance | 0.3391 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | book_imbalance | 0.2781 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | drift_residual_z | 0.0845 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | book_total_volume | 0.066 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | trade_pressure_qty | 0.004 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 1 | mid_delta_lag1 | 0.0038 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | microprice_deviation | 0.3748 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | spread | 0.3737 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | top_imbalance | 0.2862 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | book_imbalance | 0.2454 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | drift_residual_z | 0.1162 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | book_total_volume | 0.0547 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | mid_delta_lag1 | 0.0022 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 3 | trade_pressure_qty | 0.0 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | spread | 0.3067 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | microprice_deviation | 0.3025 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | top_imbalance | 0.2566 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | book_imbalance | 0.1969 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | drift_residual_z | 0.1127 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | book_total_volume | 0.0536 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | trade_pressure_qty | 0.0025 | 12000 | non-linear screen; use as ranking only |
| ASH_COATED_OSMIUM | 5 | mid_delta_lag1 | 0.0 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | drift_residual_z | 0.7764 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | microprice_deviation | 0.3716 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | top_imbalance | 0.3366 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | spread | 0.2983 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | book_imbalance | 0.2894 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | book_total_volume | 0.0492 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | mid_delta_lag1 | 0.013 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 1 | trade_pressure_qty | 0.0053 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | drift_residual_z | 1.0108 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | microprice_deviation | 0.3709 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | top_imbalance | 0.3349 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | book_imbalance | 0.3014 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | spread | 0.2835 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | book_total_volume | 0.0609 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | mid_delta_lag1 | 0.0295 | 12000 | non-linear screen; use as ranking only |
| INTARIAN_PEPPER_ROOT | 3 | trade_pressure_qty | 0.0074 | 12000 | non-linear screen; use as ranking only |

_Showing 40 of 48 rows._

## Cross-Product Relationships

Cross-product checks are expected because two products are present. The evidence is weaker than within-product signals.

| relationship | product_a | product_b | lag_ticks_a_predicts_b | correlation | n | decision_note |
| --- | --- | --- | --- | --- | --- | --- |
| mid_delta_1 same-timestamp corr | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 0 | 0.0011 | 29797 | weak cross-product evidence |
| top_imbalance same-timestamp corr | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 0 | 0.0021 | 29900 | weak cross-product evidence |
| book_imbalance same-timestamp corr | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 0 | -0.001 | 29900 | weak cross-product evidence |
| spread same-timestamp corr | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 0 | 0.0004 | 25597 | weak cross-product evidence |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -10 | -0.0097 | 29786 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -9 | 0.006 | 29789 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -8 | 0.0023 | 29789 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -7 | -0.0036 | 29789 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -6 | 0.0013 | 29791 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -5 | -0.0009 | 29791 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -4 | 0.0017 | 29791 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -3 | -0.0074 | 29792 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -2 | 0.005 | 29793 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | -1 | 0.0011 | 29794 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 0 | 0.0011 | 29797 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 1 | -0.0028 | 29794 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 2 | 0.0043 | 29793 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 3 | -0.006 | 29792 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 4 | 0.0026 | 29791 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 5 | -0.0029 | 29790 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 6 | 0.0017 | 29789 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 7 | 0.0103 | 29788 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 8 | -0.0156 | 29787 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 9 | 0.0138 | 29786 | weak lead-lag |
| lead_lag_mid_delta | ASH_COATED_OSMIUM | INTARIAN_PEPPER_ROOT | 10 | -0.0076 | 29785 | weak lead-lag |

## Clustering / Grouping Diagnostics

KMeans clusters are used only as a lightweight liquidity/regime grouping check. They are not direct strategy state.

| cluster | n | spread_mean | depth_mean | rolling_vol_mean | abs_imbalance_mean | future_delta_mean | future_delta_abs_mean | product | decision_note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6620 | 17.3002 | 50.1505 | 3.6132 | 0.1325 | 0.1181 | 1.6302 | ASH_COATED_OSMIUM | descriptive liquidity group |
| 1 | 7636 | 16.1046 | 73.6235 | 3.6186 | 0.0834 | -0.3209 | 1.5341 | ASH_COATED_OSMIUM | descriptive liquidity group |
| 2 | 744 | 8.1801 | 66.5081 | 3.6788 | 0.4704 | 2.4227 | 4.4765 | ASH_COATED_OSMIUM | possible defensive/execution regime |
| 0 | 6351 | 14.8539 | 40.6164 | 3.291 | 0.1024 | -0.4135 | 1.4993 | INTARIAN_PEPPER_ROOT | descriptive liquidity group |
| 1 | 6599 | 12.6168 | 60.499 | 3.2672 | 0.0272 | 0.0965 | 1.4714 | INTARIAN_PEPPER_ROOT | descriptive liquidity group |
| 2 | 2050 | 16.6195 | 46.0463 | 3.3069 | 0.3272 | 1.5434 | 2.1507 | INTARIAN_PEPPER_ROOT | possible defensive/execution regime |

## Imbalance Signal Summary

| product | day | feature | horizon_ticks | pearson_corr | pvalue | n |
| --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | -1 | top_imbalance | 1 | 0.6462 | 0.0 | 9969 |
| ASH_COATED_OSMIUM | -1 | book_imbalance | 1 | 0.4001 | 0.0 | 9969 |
| ASH_COATED_OSMIUM | -1 | spread | 1 | -0.0658 | 0.0 | 9221 |
| ASH_COATED_OSMIUM | -1 | book_total_volume | 1 | 0.0074 | 0.4614 | 9969 |
| ASH_COATED_OSMIUM | -1 | top_imbalance | 2 | 0.6412 | 0.0 | 9968 |
| ASH_COATED_OSMIUM | -1 | book_imbalance | 2 | 0.4053 | 0.0 | 9968 |
| ASH_COATED_OSMIUM | -1 | spread | 2 | -0.0777 | 0.0 | 9221 |
| ASH_COATED_OSMIUM | -1 | book_total_volume | 2 | 0.0143 | 0.1532 | 9968 |
| ASH_COATED_OSMIUM | -1 | top_imbalance | 3 | 0.6437 | 0.0 | 9967 |
| ASH_COATED_OSMIUM | -1 | book_imbalance | 3 | 0.3919 | 0.0 | 9967 |
| ASH_COATED_OSMIUM | -1 | spread | 3 | -0.0764 | 0.0 | 9220 |
| ASH_COATED_OSMIUM | -1 | book_total_volume | 3 | 0.0264 | 0.0085 | 9967 |
| ASH_COATED_OSMIUM | -1 | top_imbalance | 5 | 0.6413 | 0.0 | 9965 |
| ASH_COATED_OSMIUM | -1 | book_imbalance | 5 | 0.3998 | 0.0 | 9965 |
| ASH_COATED_OSMIUM | -1 | spread | 5 | -0.0436 | 0.0 | 9217 |
| ASH_COATED_OSMIUM | -1 | book_total_volume | 5 | 0.0081 | 0.4216 | 9965 |
| ASH_COATED_OSMIUM | -1 | top_imbalance | 10 | 0.6262 | 0.0 | 9960 |
| ASH_COATED_OSMIUM | -1 | book_imbalance | 10 | 0.3892 | 0.0 | 9960 |
| ASH_COATED_OSMIUM | -1 | spread | 10 | -0.0496 | 0.0 | 9214 |
| ASH_COATED_OSMIUM | -1 | book_total_volume | 10 | 0.0091 | 0.3642 | 9960 |

_Showing 20 of 120 rows._

## Conditional Patterns / Regimes

This table is long in the artifact; key rows are shown here. Use the CSV for full product/day/regime coverage.

| product | regime_type | regime | feature | horizon_ticks | pearson_corr | pvalue | n |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | spread_regime | tight | top_imbalance | 1 | 0.5863 | 0.0 | 19862 |
| ASH_COATED_OSMIUM | spread_regime | tight | book_imbalance | 1 | -0.0379 | 0.0 | 19862 |
| ASH_COATED_OSMIUM | spread_regime | tight | top_imbalance | 3 | 0.5771 | 0.0 | 19856 |
| ASH_COATED_OSMIUM | spread_regime | tight | book_imbalance | 3 | -0.0346 | 0.0 | 19856 |
| ASH_COATED_OSMIUM | spread_regime | tight | top_imbalance | 5 | 0.555 | 0.0 | 19850 |
| ASH_COATED_OSMIUM | spread_regime | tight | book_imbalance | 5 | -0.0438 | 0.0 | 19850 |
| ASH_COATED_OSMIUM | spread_regime | unknown | top_imbalance | 1 | 0.6804 | 0.0 | 2184 |
| ASH_COATED_OSMIUM | spread_regime | unknown | book_imbalance | 1 | 0.6804 | 0.0 | 2184 |
| ASH_COATED_OSMIUM | spread_regime | unknown | top_imbalance | 3 | 0.6775 | 0.0 | 2178 |
| ASH_COATED_OSMIUM | spread_regime | unknown | book_imbalance | 3 | 0.6775 | 0.0 | 2178 |
| ASH_COATED_OSMIUM | spread_regime | unknown | top_imbalance | 5 | 0.6694 | 0.0 | 2173 |
| ASH_COATED_OSMIUM | spread_regime | unknown | book_imbalance | 5 | 0.6694 | 0.0 | 2173 |
| ASH_COATED_OSMIUM | spread_regime | wide | top_imbalance | 1 | 0.628 | 0.0 | 7840 |
| ASH_COATED_OSMIUM | spread_regime | wide | book_imbalance | 1 | -0.2705 | 0.0 | 7840 |
| ASH_COATED_OSMIUM | spread_regime | wide | top_imbalance | 3 | 0.5808 | 0.0 | 7834 |
| ASH_COATED_OSMIUM | spread_regime | wide | book_imbalance | 3 | -0.2498 | 0.0 | 7834 |
| ASH_COATED_OSMIUM | spread_regime | wide | top_imbalance | 5 | 0.5249 | 0.0 | 7828 |
| ASH_COATED_OSMIUM | spread_regime | wide | book_imbalance | 5 | -0.2254 | 0.0 | 7828 |
| ASH_COATED_OSMIUM | liquidity_regime | high | top_imbalance | 1 | 0.5605 | 0.0 | 9675 |
| ASH_COATED_OSMIUM | liquidity_regime | high | book_imbalance | 1 | -0.3829 | 0.0 | 9675 |
| ASH_COATED_OSMIUM | liquidity_regime | high | top_imbalance | 3 | 0.5137 | 0.0 | 9669 |
| ASH_COATED_OSMIUM | liquidity_regime | high | book_imbalance | 3 | -0.3504 | 0.0 | 9669 |
| ASH_COATED_OSMIUM | liquidity_regime | high | top_imbalance | 5 | 0.4909 | 0.0 | 9663 |
| ASH_COATED_OSMIUM | liquidity_regime | high | book_imbalance | 5 | -0.3351 | 0.0 | 9663 |
| ASH_COATED_OSMIUM | liquidity_regime | low | top_imbalance | 1 | 0.6695 | 0.0 | 10002 |
| ASH_COATED_OSMIUM | liquidity_regime | low | book_imbalance | 1 | 0.5357 | 0.0 | 10002 |
| ASH_COATED_OSMIUM | liquidity_regime | low | top_imbalance | 3 | 0.6669 | 0.0 | 9995 |
| ASH_COATED_OSMIUM | liquidity_regime | low | book_imbalance | 3 | 0.5326 | 0.0 | 9995 |
| ASH_COATED_OSMIUM | liquidity_regime | low | top_imbalance | 5 | 0.6668 | 0.0 | 9990 |
| ASH_COATED_OSMIUM | liquidity_regime | low | book_imbalance | 5 | 0.5337 | 0.0 | 9990 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | top_imbalance | 1 | 0.5892 | 0.0 | 10209 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | book_imbalance | 1 | -0.2788 | 0.0 | 10209 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | top_imbalance | 3 | 0.5537 | 0.0 | 10203 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | book_imbalance | 3 | -0.252 | 0.0 | 10203 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | top_imbalance | 5 | 0.5235 | 0.0 | 10197 |
| ASH_COATED_OSMIUM | liquidity_regime | normal | book_imbalance | 5 | -0.2514 | 0.0 | 10197 |
| INTARIAN_PEPPER_ROOT | spread_regime | normal | top_imbalance | 1 | 0.5379 | 0.0 | 10643 |
| INTARIAN_PEPPER_ROOT | spread_regime | normal | book_imbalance | 1 | -0.061 | 0.0 | 10643 |
| INTARIAN_PEPPER_ROOT | spread_regime | normal | top_imbalance | 3 | 0.3742 | 0.0 | 10637 |
| INTARIAN_PEPPER_ROOT | spread_regime | normal | book_imbalance | 3 | -0.0461 | 0.0 | 10637 |

_Showing 40 of 78 rows._

## Trades And Flow Summary

| product | day | trade_rows | total_quantity | mean_quantity | median_quantity | q95_quantity | price_min | price_max | matched_mid_rate | mean_price_vs_mid | abs_price_vs_mid_q95 | positive_pressure_qty | negative_pressure_qty | zero_or_unmatched_pressure_qty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | -1 | 459 | 2348 | 5.1155 | 5.0 | 9.1 | 9982.0 | 10019.0 | 1.0 | -0.342 | 9.5 | 1118 | 1156 | 74 |
| ASH_COATED_OSMIUM | 0 | 471 | 2404 | 5.104 | 5.0 | 9.0 | 9979.0 | 10020.0 | 1.0 | -0.2516 | 9.5 | 1152 | 1147 | 105 |
| ASH_COATED_OSMIUM | 1 | 465 | 2375 | 5.1075 | 5.0 | 9.0 | 9980.0 | 10018.0 | 1.0 | -0.0763 | 9.5 | 1154 | 1137 | 84 |
| INTARIAN_PEPPER_ROOT | -1 | 331 | 1669 | 5.0423 | 5.0 | 7.0 | 10996.0 | 11998.0 | 1.0 | 0.2024 | 8.0 | 896 | 729 | 44 |
| INTARIAN_PEPPER_ROOT | 0 | 332 | 1671 | 5.0331 | 5.0 | 7.0 | 11998.0 | 12987.0 | 1.0 | 0.0377 | 8.5 | 830 | 762 | 79 |
| INTARIAN_PEPPER_ROOT | 1 | 333 | 1693 | 5.0841 | 5.0 | 7.4 | 12998.0 | 13999.0 | 1.0 | -0.0781 | 9.0 | 815 | 817 | 61 |

## Platform Logger / Validation Comparability

The available logger JSON is a no-trade platform result with status `FINISHED`, profit `0.0`, 2,000 activity rows, and no `ROUND2_STATE_PROBE` printed-state lines. It is useful for quote-subset comparability, not alpha.

| product | metric | sample_value | platform_value | difference | verdict | notes |
| --- | --- | --- | --- | --- | --- | --- |
| ASH_COATED_OSMIUM | rows | 10000.0 | 1000.0 | -9000.0 | no | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | overlap_rows | 10000.0 | 1000.0 | 0.0 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | two_sided_rate | 0.9214 | 0.907 | -0.0144 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | one_sided_rate | 0.0764 | 0.092 | 0.0156 | unclear | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | mean_spread | 16.2289 | 16.2514 | 0.0225 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | mean_book_total_volume | 60.6045 | 60.372 | -0.2325 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ASH_COATED_OSMIUM | mid_std | 5.0187 | 3.9419 | -1.0768 | unclear | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | rows | 10000.0 | 1000.0 | -9000.0 | no | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | overlap_rows | 10000.0 | 1000.0 | 0.0 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | two_sided_rate | 0.9248 | 0.929 | 0.0042 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | one_sided_rate | 0.0736 | 0.07 | -0.0036 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | mean_spread | 15.177 | 14.5942 | -0.5828 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | mean_book_total_volume | 48.4738 | 48.46 | -0.0138 | yes | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| INTARIAN_PEPPER_ROOT | mid_std | 288.7464 | 29.0797 | -259.6667 | unclear | Platform run has 1000 timestamps and no printed ROUND2_STATE_PROBE lines. |
| ALL | platform_profit |  | 0.0 |  | not_applicable | No-trade diagnostic logger, so PnL is not alpha evidence. |
| ALL | graph_rows |  | 500.0 |  | yes | Expected PnL graph is flat for no-trade logger. |

## Market Access Fee Value Estimation

This is an EDA-only proxy. It estimates gross executable-looking edge under simple fair-value references, then applies 25% extra access and capture-rate scenarios. It does not decide a final bid.

| edge_threshold | gross_edge_opportunity | extra_access_incremental_gross_proxy | capture_rate_assumption | incremental_pnl_proxy | break_even_bid_proxy | conservative_bid_floor | conservative_bid_ceiling | caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 31451.288 | 7862.822 | 0.01 | 78.6282 | 78.6282 | 0 | 39 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 0 | 31451.288 | 7862.822 | 0.025 | 196.5705 | 196.5705 | 0 | 98 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 0 | 31451.288 | 7862.822 | 0.05 | 393.1411 | 393.1411 | 0 | 196 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 0 | 31451.288 | 7862.822 | 0.1 | 786.2822 | 786.2822 | 0 | 393 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 1 | 30834.3286 | 7708.5822 | 0.01 | 77.0858 | 77.0858 | 0 | 38 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 1 | 30834.3286 | 7708.5822 | 0.025 | 192.7146 | 192.7146 | 0 | 96 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 1 | 30834.3286 | 7708.5822 | 0.05 | 385.4291 | 385.4291 | 0 | 192 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 1 | 30834.3286 | 7708.5822 | 0.1 | 770.8582 | 770.8582 | 0 | 385 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 2 | 29030.7619 | 7257.6905 | 0.01 | 72.5769 | 72.5769 | 0 | 36 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |
| 2 | 29030.7619 | 7257.6905 | 0.025 | 181.4423 | 181.4423 | 0 | 90 | Proxy only: bid acceptance depends on competitors; testing ignores bid(). |

_Showing 10 of 20 rows._

## Manual Research / Scale / Speed Scenario Analysis

The grid uses official Research and Scale formulas. Speed multiplier scenarios are rank-outcome proxies because actual rank is competitor-dependent.

| scenario | research_pct | scale_pct | speed_pct | speed_multiplier_assumption | budget_used | manual_pnl_proxy |
| --- | --- | --- | --- | --- | --- | --- |
| linear_rank_proxy | 16 | 48 | 36 | 0.388 | 50000.0 | 110065.314 |
| linear_rank_proxy | 16 | 49 | 35 | 0.38 | 50000.0 | 110030.9357 |
| linear_rank_proxy | 16 | 47 | 37 | 0.396 | 50000.0 | 109962.1791 |
| linear_rank_proxy | 17 | 48 | 35 | 0.38 | 50000.0 | 109927.6399 |
| linear_rank_proxy | 15 | 49 | 36 | 0.388 | 50000.0 | 109903.6022 |
| linear_rank_proxy | 17 | 47 | 36 | 0.388 | 50000.0 | 109892.568 |
| linear_rank_proxy | 15 | 48 | 37 | 0.396 | 50000.0 | 109869.9595 |
| linear_rank_proxy | 16 | 50 | 34 | 0.372 | 50000.0 | 109859.0442 |
| linear_rank_proxy | 17 | 49 | 34 | 0.372 | 50000.0 | 109822.4243 |
| linear_rank_proxy | 15 | 50 | 35 | 0.38 | 50000.0 | 109802.6742 |
| linear_rank_proxy | 16 | 46 | 38 | 0.404 | 50000.0 | 109721.5311 |
| linear_rank_proxy | 17 | 46 | 37 | 0.396 | 50000.0 | 109717.2088 |

_Showing 12 of 60 rows._

Manual scenario summary:

| scenario | best_manual_pnl_proxy | median_manual_pnl_proxy | q95_manual_pnl_proxy | evaluated_allocations | research_pct | scale_pct | speed_pct | speed_multiplier_assumption | budget_used | manual_pnl_proxy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| linear_rank_proxy | 110065.314 | 6882.8069 | 73295.2613 | 176851 | 16 | 48 | 36 | 0.388 | 50000.0 | 110065.314 |
| optimistic_rank_proxy | 204930.6238 | 33583.9968 | 150821.8183 | 176851 | 19 | 58 | 23 | 0.4837 | 50000.0 | 204930.6238 |
| pessimistic_rank_proxy | 65062.633 | -3013.1156 | 37300.9143 | 176851 | 14 | 42 | 44 | 0.3335 | 50000.0 | 65062.633 |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift + residual | timestamp, mid/order book, rolling residual | Current-round IPR level is trending, not fixed. | Prevents stale Round 1 fixed fair value. | drift-aware fair value candidate | stable in sample | strong | avoid hardcoding sample-end/day constants |
| ACO short-horizon reversal | mid deltas/order book | Price changes often reverse. | Possible market-making/reversion edge. | fair-value adjustment | stable in sample | medium/strong | execution costs and fill quality unknown |
| Top imbalance | best bid/ask volumes | Visible liquidity skew predicts near move. | Online signal from order_depths. | signal/skew candidate | stable enough for candidate queue | strong | exact sizing needs validation |
| Microprice deviation | best prices and volumes | Top-of-book pressure translated into price deviation. | May be more compact than raw imbalance. | exploratory challenger to top imbalance | unknown after validation | medium/exploratory | likely redundant with top imbalance |
| Spread regime | best bid/ask spread | Execution economics change across rows. | Can prevent bad fills or overtrading. | execution/risk filter | day-sensitive | medium | not standalone alpha |

## Negative Evidence

| Idea Or Signal | Why It Was Plausible | Evidence Against It | When To Reopen |
| --- | --- | --- | --- |
| Carry Round 1 fixed IPR fair value | Round 1 hint called IPR steady | Round 2 drift/process evidence contradicts fixed value | only with new final/platform evidence |
| Use cross-product lead-lag in first strategy | two products have aligned timestamps | lead-lag correlations are weak versus direct product signals | if platform logs reveal product coupling |
| Use PCA/clusters as bot state | PCA and clusters expose feature families/regimes | offline latent components are not direct TradingState features | only if spec defines a simple online proxy |
| Treat diagnostic logger PnL as meaningful | platform JSON has profit field | bot intentionally does not trade, profit is 0 | never for alpha; use only as quote evidence |
| Use trade pressure directly in first spec | market trades exist | sparse sample evidence and no printed state probe | after platform logs include market_trades dynamics |

## Downstream Feature Contract Implications

| Feature Or Relationship | Contract Implication | Online Proxy Needed? | Validation / Invalidation Check | Do Not Use Until |
| --- | --- | --- | --- | --- |
| IPR drift/residual | Needs explicit online drift/reference formula and missing-data fallback. | no; timestamp/mid/order_depths are available | markout/PnL under day/platform subset; fail if drift residual logic overfits day constants | reviewed strategy spec names parameters |
| ACO delta reversal | Needs state for previous mid/delta and spread-aware execution. | no; previous mids can be stored in traderData | post-fill markout and inventory adverse selection | reviewed strategy spec defines state and fallback |
| top imbalance / microprice | Choose one primary signal first to avoid redundancy. | no | compare top imbalance vs microprice variant one axis at a time | spec selects primary and backup |
| spread/depth regimes | Use as execution/risk filter, not alpha source. | no | PnL/fill split by spread/depth regime | spec states threshold or defensive behavior |
| cross-product lead-lag | Do not implement in first strategy. | not applicable | targeted EDA only if new evidence appears | new evidence contradicts current weak verdict |

## Assumptions

- MAF capture rates are scenario assumptions, not official mechanics.
- Manual Speed multiplier scenarios are rank proxies, not predictions.
- Platform activitiesLog is treated as 80% quote-subset evidence because Round 2 docs say testing uses default quotes and ignores bid().
- Multivariate regressions, PCA, mutual information, and clustering are research evidence only; uploadable bots need reviewed online Feature Contracts.

## Open Questions

- Exact Round 2 deadline remains unknown.
- Competitive Market Access Fee bid distribution is unknown.
- Manual Speed rank outcome is unknown.
- Platform market_trades behavior from printed `TradingState` logs is still missing because the saved JSON did not include `ROUND2_STATE_PROBE`.

## Signal Strength And Uncertainty

- Strong: IPR drift/residual, top imbalance.
- Medium/strong: ACO short-horizon reversal.
- Medium/exploratory: microprice deviation, spread regime, full-book imbalance as backup/context.
- Weak/negative: cross-product lead-lag for first strategy.
- Needs logs: trade pressure proxy.
- Uncertainty: sample data may differ from final simulation; platform testing quote subset is randomized.

## Downstream Use / Agent Notes

- Strong enough to consider: IPR drift plus residual, ACO short-horizon mean reversion, top imbalance, spread regime as an execution/risk filter.
- Exploratory only: microprice deviation, full-book imbalance as backup/context, liquidity/depth regime, clustering/grouping diagnostics.
- Do not use yet: cross-product lead-lag, trade pressure proxy, PCA components, cluster labels, latent states.
- Additional validation needed: strategy candidates must test whether promoted signals survive execution, position limits, randomized quote subsets, and platform PnL.
- How understanding should use this: consume `expanded_feature_promotion_decisions.csv`, process hypotheses, and negative evidence; do not collapse everything back to four fixed signals.
- Manual challenge handling: keep Research/Scale/Speed findings in a manual-only lane; they should not enter the Signal Ledger as bot features.
- Market Access Fee handling: carry as an algorithmic final-round mechanics/risk decision, separate from normal `Trader.run()` signals and separate from manual allocation.
- How strategy generation should use this: generate bounded candidates around drift/residual, ACO reversal, top imbalance or microprice challenger, and conservative spread/depth filters.
- How specification should use this: define online fields, state, missing-signal behavior, and invalidation checks; avoid CSV/day-specific constants.
- How implementation should use this: do not implement until a reviewed spec exists.
- How testing/debugging should use this: validate signal markouts and PnL by product, spread/depth regime, and platform quote subset.

## Reusable Metrics

- `spread`, `relative_spread`, `top_imbalance`, `book_imbalance`, `microprice_deviation`, `book_total_volume`, `depth_ratio`, `one_sided_book`, `mid_delta_lag1`, `rolling_vol_50`, `z_mid_50`, `drift_residual_z`, `trade_pressure_qty`.

## Strategy Implications

- Round 2 should not inherit a fixed Round 1 view of IPR.
- ACO and top imbalance signals deserve first strategy consideration.
- Microprice is worth a controlled challenger/variant, not immediate feature stacking.
- Spread/depth should be considered as execution/risk filters.
- Cross-product prediction is low ROI for first-pass strategy.
- MAF/manual decisions remain scenario/risk decisions, not bot signals.

## Interpretation Limits

- EDA is evidence, not a strategy.
- Sample data patterns are not official rules.
- Platform logger result is no-trade and cannot measure alpha.
- MAF and manual allocations are scenario analyses, not final submissions.
- Research-library outputs are not uploadable bot dependencies.

## Next Action

- EDA is completed with caveats and has been synthesized into `02_understanding.md`. Review Understanding next, then generate a small but not artificially capped strategy candidate set grounded in the promoted/exploratory/negative evidence above.
