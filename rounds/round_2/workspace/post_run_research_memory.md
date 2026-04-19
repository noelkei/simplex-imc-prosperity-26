# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round: `round_2`
- Last updated: `2026-04-19`
- Current champion: `R2-CAND-10` by raw single-run PnL, but treated as provisional because `C10` is code-equivalent to lower/higher same-family runs and the quote subset is randomized.
- Latest platform artifact: [`rounds/round_2/performances/noel/historical/candidate_r2_cand_10_maf_bid_policy.json`](../performances/noel/historical/candidate_r2_cand_10_maf_bid_policy.json)
- Memory confidence: `medium`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
| `run_20260419_battery01_c10_trial_1` | `R2-CAND-10` | [`json`](../performances/noel/historical/candidate_r2_cand_10_maf_bid_policy.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c10_trial_1.md) | real platform PnL | primary | profit `2659.906`, IPR `2659.906`, ACO `0.000` |
| `run_20260419_battery01_c02_trial_1` | `R2-CAND-02` | [`json`](../performances/noel/historical/candidate_r2_cand_02_ipr_residual_extreme_execution.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c02_trial_1.md) | real platform PnL | primary | profit `2656.625`, IPR `2656.625`, ACO `0.000` |
| `run_20260419_battery01_c07_trial_1` | `R2-CAND-07` | [`json`](../performances/noel/historical/candidate_r2_cand_07_combined_ipr_aco_imbalance.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c07_trial_1.md) | real platform PnL | primary | profit `2359.703`, IPR `2359.703`, ACO `0.000` |
| `run_20260419_battery01_c08_trial_1` | `R2-CAND-08` | [`json`](../performances/noel/historical/candidate_r2_cand_08_combined_ipr_aco_reversal.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c08_trial_1.md) | real platform PnL | backup | profit `1669.594`, IPR `1669.594`, ACO `0.000` |
| `run_20260419_battery01_c09_trial_1` | `R2-CAND-09` | [`json`](../performances/noel/historical/candidate_r2_cand_09_spread_defensive_overlay.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c09_trial_1.md) | real platform PnL | experimental | profit `862.297`, IPR `862.297`, ACO `0.000` |
| `run_20260419_battery01_c08_trial_2` | `R2-CAND-08` | [`json`](../performances/noel/historical/candidate_r2_cand_08_combined_ipr_aco_reversal_v2.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c08_trial_2.md) | real platform PnL | backup | profit `837.500`, IPR `837.500`, ACO `0.000` |
| `run_20260419_battery01_c01_trial_1` | `R2-CAND-01` | [`json`](../performances/noel/historical/candidate_r2_cand_01_ipr_drift_fv_maker.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c01_trial_1.md) | real platform PnL | experimental | profit `559.000`, IPR `559.000`, ACO `0.000` |
| `run_20260419_battery01_c03_trial_1` | `R2-CAND-03` | [`json`](../performances/noel/historical/candidate_r2_cand_03_aco_reversal_maker.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c03_trial_1.md) | real platform PnL | reject | profit `0.000`, IPR `0.000`, ACO `0.000` |
| `run_20260419_battery01_c04_trial_1` | `R2-CAND-04` | [`json`](../performances/noel/historical/candidate_r2_cand_04_aco_top_imbalance_skew.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c04_trial_1.md) | real platform PnL | reject | profit `0.000`, IPR `0.000`, ACO `0.000` |
| `run_20260419_battery01_c05_trial_1` | `R2-CAND-05` | [`json`](../performances/noel/historical/candidate_r2_cand_05_aco_microprice_challenger.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c05_trial_1.md) | real platform PnL | reject | profit `0.000`, IPR `0.000`, ACO `0.000` |
| `run_20260419_battery01_c06_trial_1` | `R2-CAND-06` | [`json`](../performances/noel/historical/candidate_r2_cand_06_aco_full_book_depth_backup.json) / [`summary`](../performances/noel/canonical/run_20260419_battery01_c06_trial_1.md) | real platform PnL | reject | profit `0.000`, IPR `0.000`, ACO `0.000` |

## Run Knowledge Index

| Run | Candidate | Strategy Family | Changed Axis | Tested Feature / Signal | PnL Source | Comparable To | Knowledge Delta | Memory Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `run_20260419_battery01_c10_trial_1` | `R2-CAND-10` | maf_policy_probe | feature/execution | IPR drift + ACO imbalance + bid placeholder | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c02_trial_1` | `R2-CAND-02` | ipr_extreme | feature/execution | IPR residual extreme | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c07_trial_1` | `R2-CAND-07` | combined_ipr_aco_imbalance | feature/execution | IPR drift + ACO imbalance | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c08_trial_1` | `R2-CAND-08` | combined_ipr_aco_reversal | feature/execution | IPR drift + ACO reversal | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c09_trial_1` | `R2-CAND-09` | spread_defensive_overlay | feature/execution | IPR drift + ACO imbalance + spread overlay | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c08_trial_2` | `R2-CAND-08` | combined_ipr_aco_reversal | feature/execution | IPR drift + ACO reversal | real platform | randomized R2 platform subset | new | update |
| `run_20260419_battery01_c01_trial_1` | `R2-CAND-01` | ipr_drift | feature/execution | IPR drift/residual | real platform | randomized R2 platform subset | new | update lightly |
| `run_20260419_battery01_c03_trial_1` | `R2-CAND-03` | aco_reversal | feature/execution | ACO short-horizon reversal | real platform | randomized R2 platform subset | contradicts | update |
| `run_20260419_battery01_c04_trial_1` | `R2-CAND-04` | aco_imbalance | feature/execution | ACO top imbalance | real platform | randomized R2 platform subset | contradicts | update |
| `run_20260419_battery01_c05_trial_1` | `R2-CAND-05` | aco_microprice | feature/execution | ACO microprice | real platform | randomized R2 platform subset | contradicts | update |
| `run_20260419_battery01_c06_trial_1` | `R2-CAND-06` | aco_full_book | feature/execution | ACO full-book/depth | real platform | randomized R2 platform subset | contradicts | update |

## Current Reusable Insights

| Insight ID | Products | Based On Runs | Analysis Mode | Finding | Confidence | Portability | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R2-MEM-01` | IPR | C01/C02/C07/C08/C09/C10 | edge decomposition | Positive platform PnL is entirely IPR-attributed in Battery 01. | medium/high | round-specific | strategy/spec/variant | single-run rankings are noisy under randomized quote subset |
| `R2-MEM-02` | ACO | C03/C04/C05/C06 plus combined runs | failure | Current ACO modules produced zero final ACO PnL and zero ACO position. | high for current implementation | round-specific | spec/variant/debugging | this weakens implementation, not necessarily the EDA ACO signals |
| `R2-MEM-03` | both | C08 two trials, C07/C10 same active logic | confidence | Platform testing is materially non-deterministic because the quote subset changes. | high | round-specific | validation/champion choice | use repeated trials before choosing close champions |
| `R2-MEM-04` | MAF | C10 | negative evidence | MAF remains untested because current `bid()` is 0. | high | round-specific | final mechanics | testing ignores bid acceptance anyway |
| `R2-MEM-05` | both | repo state | provenance | Active bot files were expected in canonical; repaired by copying from historical to canonical, but raw JSON stayed historical and no `.log` exists. | high | not applicable | validation hygiene | future uploads should preserve exact py/json/log bundle |

## Feature Feedback

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| IPR residual extreme | C02 | helped | real platform PnL and IPR attribution | up | rerun and add inventory challenger |
| IPR drift/residual | C01/C07/C08/C09/C10 | helped but noisy | product attribution and same-family variance | unchanged/up | repeated trials before champion choice |
| ACO top imbalance | C04/C07/C09/C10 | failed to activate in current implementation | zero ACO PnL/position | down for implementation | activation probe and spread retune |
| ACO reversal | C03/C08 | failed to activate as ACO module; combined PnL came from IPR | product attribution | down for implementation | retest only after spread activation fix |
| Spread defensive overlay | C09 | likely harmful/over-throttled | lower PnL, observed spread gates | down | replace binary gate with continuous/product-specific sizing |
| MAF bid policy | C10 | not tested | `maf_bid=0` | unchanged | final scenario decision later |

## Multivariate Relationship Feedback

| Relationship | Runs | EDA Expectation | Run Evidence | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| Top-book pressure may help ACO | C04/C07/C09/C10 | promote/exploratory | not actually tested due zero ACO attribution | unchanged for EDA, down for implementation | targeted ACO activation run |
| Cross-product lead-lag weak | all | do not use first-pass | no bot used cross-product lead-lag | unchanged | keep rejected |

## Process Hypothesis Feedback

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| IPR drift/residual is exploitable | IPR | positive IPR runs | supports, but needs repeated trials | up | keep IPR as base engine |
| ACO mean reversion/pressure is exploitable | ACO | C03-C06 | not tested because current modules did not activate | unchanged/down for current specs | rewrite activation before judging |
| Testing quote subset is stochastic | both | C08 two trials, C07/C10 | supports | up | rerun top candidates and avoid overfitting single PnL |

## Redundancy Decision Feedback

| Feature Family | Prior Redundancy Decision | Runs | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| ACO pressure variants | keep challengers separate | C04/C05/C06 | none activated | reopen implementation/spec, not EDA | retest after spread fix |
| Combined C07/C10 | unclear | C07/C10 | active logic effectively same with different PnL | mark as stochastic duplicate | use one family with repeated trials |

## Statistical Confidence Notes

- Decision-relevant confidence update: C08 fell from `1669.594` to `837.500` across two trials, showing material test-subset variance.
- Tool or method used: platform JSON parsing with product attribution, graphLog drawdown, spread gate coverage.
- Caveat or overfit risk: no own-trades/fill logs, no same-subset paired tests, exact platform quote subset unknown.

## Log-Derived Feature Discoveries

| Feature Or Signal | Source Runs / Logs | Evidence | Online Usability | Proposed Use | Next Step |
| --- | --- | --- | --- | --- | --- |
| Product-specific spread gate | all Battery 01 JSONs | ACO spread <=4 was effectively unavailable; current gates shut down ACO | usable online | execution filter / size curve | spec variant |
| Stochastic robustness score | C08/C07/C10 | repeated/same-family divergence | validation-only | champion selection | rerun top candidates |

## Feature Confidence Updates

| Feature Or Signal | Previous Confidence | New Confidence | Reason | Affected Artifact |
| --- | --- | --- | --- | --- |
| IPR residual extreme | medium/high | high enough to rerun | near-best real platform PnL | Gen2 strategy/spec |
| ACO current implementations | medium | rejected current implementation | zero product attribution | Gen2 strategy/spec |
| Spread hard gate <=4 | medium | rejected for ACO, questionable for IPR | spread diagnostics | Gen2 spec |

## Failure Patterns

| Pattern | Runs | Conditions | Failure Class | Action |
| --- | --- | --- | --- | --- |
| ACO shutdown | C03-C06 and combined ACO modules | top spread usually much wider than configured gate | execution | widen/replace spread gate and add activation probe |
| Single-run over-ranking | C08 trials, C07/C10 | randomized 80% quote subset | evidence gap | require repeated trials for champions |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| IPR residual/drift family | C02/C07/C10 | IPR product PnL | real but stochastic | real platform profit and final IPR attribution | base engine for Gen2 |
| ACO pressure/reversal | C03-C06 | no observed ACO activity | unclear | zero final ACO PnL/position | activation diagnostics first |

## Counterfactual Backlog

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
| R2-G2-01-IPR-EXTREME-RERUN-CHAMPION | battery01 | Rerun C02-style IPR extreme logic without ACO to estimate quote-subset variance. | high | untested | Run at least 2 more platform trials; compare median, worst-case, final inventory, and drawdown. |
| R2-G2-02-IPR-DRIFT-RERUN-CODE-EQUIV | battery01 | Rerun the C07/C10 IPR drift family with ACO disabled for clean comparability. | high | untested | 2-3 repeated uploads, compare to C02 under same summary metrics. |
| R2-G2-03-IPR-EXTREME-FLATTER-INVENTORY | battery01 | Add late/soft inventory neutralization to C02 without changing residual entry logic. | high | untested | Head-to-head vs C02 reruns: PnL, final position, drawdown, and missed upside. |
| R2-G2-04-IPR-SPREAD-RETUNE | battery01 | Replace hard spread gate with continuous size/price throttling at wider spreads. | high | untested | Compare fill/activity proxy through PnL change ticks and real PnL; reject if wider spreads cause adverse selection. |
| R2-G2-05-ACO-ACTIVATION-PROBE | battery01 | Create small-size ACO probe with spread gate widened to realistic ACO levels and explicit activity logging. | high | untested | Require nonzero ACO position/PnL-change ticks; PnL can be secondary for this probe. |
| R2-G2-06-ACO-IMBALANCE-WIDE-SPREAD | battery01 | Retest top imbalance with realistic spread handling and conservative quote sizes. | high | untested | Compare to ACO activation probe; promote only if ACO PnL improves after activity exists. |
| R2-G2-07-ACO-REVERSAL-WIDE-SPREAD | battery01 | Retest reversal with realistic spread handling and minimum fill opportunities. | high | untested | Head-to-head against G2-06 on ACO-only logs. |
| R2-G2-08-COMBINED-IPR-EXTREME-ACO-PROBE | battery01 | Use C02-style IPR as base and add small ACO activation module. | high | untested | Product attribution must show IPR still positive and ACO no worse than small controlled loss. |
| R2-G2-09-COMBINED-IPR-EXTREME-ACO-IMBALANCE | battery01 | C02-style IPR plus corrected ACO imbalance module. | high | untested | Promote only if total PnL beats IPR-only median or ACO adds nonnegative product attribution. |
| R2-G2-10-SPREAD-OVERLAY-CONTINUOUS | battery01 | Convert spread overlay from binary gate to product-specific size curve. | high | untested | Apply only to current champion family; compare against no-overlay paired run. |
| R2-G2-11-BRUNO-R1-KALMAN-R2-PORT | battery01 | Port Bruno Kalman ACO module into Round 2 wrapper with current IPR base, R2 limits, bid=0, and R2 logging. | high | untested | Treat as challenger; reject if ACO attribution remains zero or worse than corrected ACO probes. |
| R2-G2-12-NOEL-R1-C26-R2-PORT | battery01 | Port Noel C26 ACO one-sided/exit overlay into Round 2 wrapper with current IPR base and R2 logging. | high | untested | Compare against Bruno port and corrected ACO imbalance; keep only if attribution is positive or risk better. |
| R2-G2-13-MAF-BID-SCENARIO | battery01 | Choose a bid policy from EDA scenario table after champion PnL stabilizes. | high | untested | Use EDA MAF scenarios plus champion robustness; do not confuse with Trader.run alpha. |

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| Treat C10 as a MAF-tested bot | C10 | `bid()` is 0 and testing ignores accepted bids | final MAF scenario decision |
| Use current ACO bots unchanged | C03-C06 | zero ACO activity/PnL | after spread/activation spec rewrite |
| Choose champion from one PnL point | all | randomized quote subset causes high variance | repeated trials or deadline deferral |

## Downstream Notes

- EDA: targeted post-run EDA should focus on spread gates and activation, not broad rediscovery.
- Understanding: carry IPR stronger, ACO implementation weaker, ACO EDA not fully invalidated.
- Strategy generation: Gen2 should include IPR reruns, ACO activation fixes, two controlled Round 1 ports, and MAF as separate mechanics.
- Spec writing: every ACO spec must define product-specific spread handling and an activation falsification check.
- Variant generation: no broad parameter fishing; change one axis per bot unless the bot is explicitly combined.
