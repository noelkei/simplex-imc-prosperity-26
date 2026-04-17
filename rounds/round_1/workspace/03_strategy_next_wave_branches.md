# Round 1 - Next-Wave Creative Strategy Branches

## Status

COMPLETED

## Goal

Generate the next strategy wave after the platform-artifact analysis, without implementing bots yet. The aim is to produce non-duplicative branches that can become a second batch of 5-10 bots once the user chooses which directions to spec.

## Sources

- Platform artifact analysis: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- Raw platform artifact output: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.json`
- Strategy candidates: `03_strategy_candidates.md`
- Understanding: `02_understanding.md`
- Feature EDA: `01_eda/eda_strategy_expansion_feature_lab.md`
- Model EDA: `01_eda/eda_strategy_expansion_models.md`
- Cross-product EDA: `01_eda/eda_cross_product_relationships.md`

## Ground Rules From Evidence

- Platform-style JSON `profit` is the ranking score.
- Final `activitiesLog` product PnL is the product split.
- Local replay PnL is only a sanity heuristic.
- IPR +80 carry is the current base layer: all strong platform artifacts with final IPR `80` earn `7286.0` IPR PnL.
- ACO is the main improvement surface: current bar is ACO `2721.0` from `candidate_10_bot02_carry_tight_mm`.
- Do not use cross-product directional prediction unless new EDA contradicts current near-zero relationship evidence.
- Model overlays are interesting only if they preserve the IPR +80 layer.

## Extra Log Signals

These are strategy-shaping observations from the current platform/log artifacts, not official rules.

| Signal | Evidence | Strategy Consequence |
| --- | --- | --- |
| IPR is solved enough to lock | `candidate_10`, `23-bot`, `25-bot`, and Amin 26 all hit final IPR `80` and earn `7286.0` IPR PnL | Treat IPR +80 as a baseline module, not as the main creative space |
| ACO quality beats volume | `candidate_10` ACO edge is `12.09` with matched qty `225`; `23-bot` trades matched qty `275` but edge only `4.49` | Improve quote selection before increasing size |
| ACO flat finish is valuable | best artifact ends ACO `0` with ACO PnL `2721.0` | Explore inventory lifecycle and late flattening |
| Markov/adaptive ACO ideas are close | bot 04 ACO `2689.94`, bot 05 ACO `2448.44`; both lose total due weak IPR | Extract ACO logic only, graft onto +80 IPR |
| Time buckets are uneven | top ACO logs tend to sell early, accumulate mid-run, then reduce late | Time-aware ACO inventory targets may beat static skew |
| Pure microstructure failed as standalone | bot 03 total `1542.25`, IPR only `694.59` | Microstructure belongs as an execution gate, not the core bot |

## Candidate Families

### `candidate_14_aco_kalman_latent_fv`

Use a tiny Kalman filter for ACO latent fair value around `10000`. This is not a replacement for fixed FV; it is a way to decide when `10000` is still trustworthy, when to widen, and how to skew.

| Branch | Idea | Execution |
| --- | --- | --- |
| `14A_conservative_kalman` | Latent FV with very low process noise | Quote around Kalman mean only when innovation is small; otherwise fall back to wider fixed-FV quotes |
| `14B_innovation_adaptive` | Innovation magnitude controls aggressiveness | If observed mid deviates but snaps back, quote tighter; if innovation persists, widen or pause |
| `14C_inventory_coupled_kalman` | Inventory changes the measurement trust | If long ACO, require stronger undervaluation before buying more; if short, require stronger overvaluation before selling |

Why it is different: the bot carries a latent state estimate, not just a residual bucket or static threshold.

### `candidate_15_aco_hmm_regime_mm`

Use an offline Hidden Markov Model style regime filter for ACO. The hidden state is not directly "price"; it is a behavior mode: mean-reverting, neutral, toxic/noisy, or liquidity-rich.

| Branch | Idea | Execution |
| --- | --- | --- |
| `15A_three_state_hmm` | Hidden states: under-mean-revert, neutral, over-mean-revert | Buy/sell more only when posterior favors mean reversion back to `10000` |
| `15B_hmm_liquidity_state` | Add a hidden liquidity/toxic state | Stop posting tight quotes when spread/depth/imbalance suggests fills are adverse |
| `15C_time_aware_hmm` | State transition probabilities vary by time bucket | Allow more inventory mid-run; bias toward flattening in the last bucket |

Why it is different: Markov buckets observe residual state directly; HMM filters noisy observations into a hidden regime belief.

### `candidate_16_aco_edge_quality_gate`

Use log-derived trade quality as the main ACO gate. The target is not more fills; it is better fills.

| Branch | Idea | Execution |
| --- | --- | --- |
| `16A_static_edge_gate` | Quote only when expected roundtrip edge exceeds a hard threshold | Skip marginal states that resemble low-edge Amin 23/25 fills |
| `16B_contextual_edge_gate` | Threshold depends on residual, spread, inventory, and time bucket | Wider edge needed when inventory is already leaning or liquidity is poor |
| `16C_drawdown_adaptive_gate` | Tighten the gate after ACO drawdown | If ACO PnL dips, stop chasing volume and require cleaner edge |

Why it is different: explicit fill-quality optimization instead of FV or regime modeling.

### `candidate_17_aco_inventory_lifecycle`

Turn ACO inventory into a planned lifecycle: gather inventory when edge is good, hold while reversion is likely, flatten before inventory risk dominates.

| Branch | Idea | Execution |
| --- | --- | --- |
| `17A_late_flatten` | Keep normal ACO MM until late session, then bias to flat | After a timestamp threshold, quote only inventory-reducing orders unless edge is exceptional |
| `17B_target_position_curve` | Desired ACO inventory follows time bucket curve | Early/mid session allows +/-50; final bucket target decays toward 0 |
| `17C_profit_lock_inventory_stop` | Once ACO PnL exceeds a threshold, reduce risk | Lock gains by widening adds and favoring exits |

Why it is different: it treats time and inventory as first-class state, not a static skew coefficient.

### `candidate_18_aco_offline_policy_table`

Create a compact offline action table over ACO state buckets. It can be hand-built from EDA/log evidence, not trained online.

| Branch | Idea | Execution |
| --- | --- | --- |
| `18A_conservative_table` | State = residual bucket x inventory bucket | Maps to buy/sell/quote-both/skip with low complexity |
| `18B_time_policy_table` | Add time bucket | Same residual can produce different action early vs late |
| `18C_counterfactual_log_table` | Use platform logs to label high-quality states | Prefer states that historically produced high spread capture and low inventory pain |

Why it is different: discrete policy, easy to inspect, no continuous model instability.

### `candidate_19_ipr_execution_upgrade`

Keep IPR +80, but test whether the path to +80 can be improved without losing the carry.

| Branch | Idea | Execution |
| --- | --- | --- |
| `19A_frontload_sweep` | Reach +80 as early as possible | Take visible asks aggressively until position is +80 |
| `19B_kalman_drift_guard` | Small Kalman/EMA estimate of IPR intercept/slope | Only reduce target if early live slope materially contradicts +0.001/tick |
| `19C_paid_to_get_long` | Try to rest bids while building long, then sweep if not filled | Capture a little spread before committing to +80 |

Why it is different: IPR is not rethought as a model strategy; it is optimized as execution around a fixed target.

### `candidate_20_dual_product_risk_scheduler`

Use both products in one bot without directional cross-product prediction. This is portfolio scheduling, not pairs trading.

| Branch | Idea | Execution |
| --- | --- | --- |
| `20A_ipr_lock_then_aco` | First lock IPR +80, then let ACO run | Avoid ACO logic interfering with the primary PnL engine |
| `20B_total_pnl_guard` | If total PnL drawdown worsens, make ACO more conservative | IPR remains locked unless rule/position constraints force otherwise |
| `20C_barbell_mode` | High-confidence IPR plus only high-edge ACO | Accept fewer ACO trades in exchange for lower chance of dragging total below 10k |

Why it is different: it optimizes the combined bot objective, not product-local PnL in isolation.

### `candidate_21_one_sided_book_specialist`

One-sided books are common enough to be strategic. Current bots mostly treat them as null handling.

| Branch | Idea | Execution |
| --- | --- | --- |
| `21A_toxic_one_sided_skip` | One-sided state may indicate adverse selection | Stop adding inventory when only the dangerous side is visible |
| `21B_missing_side_provider` | Provide liquidity on the missing side when FV edge is large | Rest only inventory-safe quotes, not blind full-cap orders |
| `21C_one_sided_exit` | Use one-sided states to flatten ACO opportunistically | If a visible side lets us exit inventory at acceptable edge, prioritize it |

Why it is different: it turns a data-quality caveat into an execution state.

### `candidate_22_micro_alpha_rescue`

Rescue microstructure as an overlay only. The standalone micro bot lost because it abandoned the dominant carry/FV structure.

| Branch | Idea | Execution |
| --- | --- | --- |
| `22A_imbalance_quote_skew` | Use L1/L3 imbalance to skew ACO quote placement | Improve side selection while keeping fixed FV |
| `22B_spread_depth_liquidity_mode` | Use PCA-style liquidity axis manually | Quote tighter only when spread/depth conditions imply safer fills |
| `22C_sparse_sweep_overlay` | Immediate sweep only on unusually good best-quote edge | Take obvious edge, otherwise stay passive |

Why it is different: microstructure is demoted from strategy core to a small execution edge.

### `candidate_23_adaptive_aco_controller`

Meta-controller over ACO modules: fixed FV, Kalman, HMM, edge gate, and flattening. This is the most complex branch and should be used carefully.

| Branch | Idea | Execution |
| --- | --- | --- |
| `23A_hard_priority_switch` | Ordered rules choose one module | Example: late flatten overrides HMM; toxic state overrides all |
| `23B_weighted_score_ensemble` | Add small scores from Kalman/HMM/edge/inventory | Quote size and side from total score |
| `23C_conservative_fallback_controller` | Complex model can only reduce risk, not add aggression | Fixed FV remains base; models widen, pause, or flatten |

Why it is different: it tests whether combining small signals works better than any one model.

## Priority Table

| Candidate | Product Scope | Evidence Strength | Impl Cost | Validation Speed | Risk | Expected Upside | Priority | Why |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_14_aco_kalman_latent_fv` | ACO + IPR base | medium | medium | high | medium | high | high | Tests latent FV trust without abandoning FV=10000 |
| `candidate_15_aco_hmm_regime_mm` | ACO + IPR base | medium | medium-high | medium | medium-high | high | high | Directly addresses hidden-pattern hypothesis |
| `candidate_16_aco_edge_quality_gate` | ACO + IPR base | strong from logs | low-medium | high | low-medium | high | high | Current logs say quality beats volume |
| `candidate_17_aco_inventory_lifecycle` | ACO + IPR base | strong from logs | low | high | low | medium-high | high | Best run ends ACO flat; easy to test |
| `candidate_18_aco_offline_policy_table` | ACO + IPR base | medium | medium | high | medium | high | medium-high | Interpretable and non-black-box |
| `candidate_19_ipr_execution_upgrade` | IPR + ACO base | medium | low-medium | high | medium | low-medium | medium | IPR already strong, but path may matter |
| `candidate_20_dual_product_risk_scheduler` | both | medium | low-medium | high | low-medium | medium-high | medium-high | Optimizes total score and avoids ACO drag |
| `candidate_21_one_sided_book_specialist` | mostly ACO | weak-medium | medium | medium | medium | medium | medium | Underexplored execution state |
| `candidate_22_micro_alpha_rescue` | mostly ACO | medium | low-medium | high | medium | medium | medium | Keeps useful micro signal without repeating failed bot 03 |
| `candidate_23_adaptive_aco_controller` | ACO + IPR base | weak-medium | high | medium | high | very high | medium | Could combine winners, but complexity can hurt |

## Recommended Next Batch If We Build 5 Bots

1. `14A_conservative_kalman`: safest Kalman branch.
2. `15A_three_state_hmm`: clean HMM hidden-regime test.
3. `16B_contextual_edge_gate`: strongest log-grounded execution idea.
4. `17A_late_flatten`: low-cost inventory lifecycle test.
5. `18A_conservative_table`: interpretable policy-table branch.

## Recommended Extended Batch If We Build 8 Bots

Add:

6. `20C_barbell_mode`: total-score protection around the >10k baseline.
7. `21C_one_sided_exit`: turns one-sided states into inventory exits.
8. `23C_conservative_fallback_controller`: lets models reduce risk without adding too much complexity.

## EDA Needed Before Specs

| EDA Task | Why It Matters | Output Needed |
| --- | --- | --- |
| Estimate ACO Kalman noise parameters from residuals | Choose Q/R without guessing wildly | Small table of conservative/aggressive Q/R constants |
| Fit or approximate 3-state ACO HMM offline | Define transition/emission constants for HMM branch | Hardcoded transition matrix, emission means/variances, posterior update formula |
| Label ACO log states by realized edge and inventory pain | Support edge-quality and policy-table branches | State bucket table with keep/skip suggestions |
| Time-bucket ACO inventory/PnL attribution | Choose lifecycle thresholds | Recommended target inventory curve by timestamp bucket |
| One-sided-book conditional analysis | Decide whether one-sided is skip, provide, or exit | Conditional edge and reversion stats for one-sided rows |

## Promotion And Test Plan

When bots are eventually built:

1. Preserve IPR +80 behavior unless the branch explicitly says otherwise.
2. Change only one ACO concept per bot where possible.
3. Save `.py`, platform `.json`, and `.log` together.
4. Rerun `../performances/noel/canonical/analyze_platform_artifacts.py`.
5. Promote only if platform JSON `profit` beats the bar or product split explains a useful tradeoff.

Current bar:

- Total PnL: `10007.0`
- IPR PnL: `7286.0`
- ACO PnL: `2721.0`
- Final IPR: `80`
- Final ACO: `0`

## Review Notes

- User selected all 10 families for implementation on 2026-04-17.
- This is a candidate-expansion artifact, not the final submission decision.
- Implemented specs/bots are tracked in `04_strategy_specs/spec_next_wave_10_bot_matrix.md` and `../bots/noel/canonical/next_wave_submission_manifest.md`.
