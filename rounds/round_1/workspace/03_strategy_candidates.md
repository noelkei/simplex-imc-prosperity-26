# Round 1 - Strategy Candidates

## Status

COMPLETED

## Reopen Note

Phase 03 was reopened on 2026-04-16 after the user requested conceptually orthogonal strategy exploration before validating the current implementation. The goal is not mathematical zero covariance; it is to avoid repeating the same idea with small parameter changes.

## Next-Wave Note

Phase 03 was reopened again on 2026-04-17 after platform JSON/log analysis showed that the current >10k baseline is `candidate_10_carry_tight_mm`, with IPR effectively solved by +80 carry and ACO as the main improvement surface. The next-wave creative branch artifact is `03_strategy_next_wave_branches.md`.

User selected all 10 next-wave families for implementation on 2026-04-17.

## Sources

- Wiki facts: `workspace/00_ingestion.md`
- Prior understanding: `workspace/02_understanding.md`
- Original EDA: `workspace/01_eda/eda_round_1.md`
- Feature expansion EDA: `workspace/01_eda/eda_strategy_expansion_feature_lab.md`
- Model expansion EDA: `workspace/01_eda/eda_strategy_expansion_models.md`
- Cross-product EDA: `workspace/01_eda/eda_cross_product_relationships.md`
- Processed metrics: `../data/processed/strategy_expansion_metrics.json`
- Platform artifact analysis: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`
- Next-wave branch artifact: `03_strategy_next_wave_branches.md`
- Playbook heuristics: none applied as evidence

---

## Conceptual Orthogonality Map

| Approach Family | Edge Source | Product Scope | Relationship To Existing Strategy |
| --- | --- | --- | --- |
| Fair-value market making | quote around estimated FV and capture spread | both | existing core approach |
| Directional carry | hold exposure in direction of deterministic drift | IPR | different risk profile from market making |
| Microstructure scalping | exploit sparse best-quote edge, spread, imbalance, and one-sided states | both | execution/margin approach, not FV-only |
| Markov regime model | hardcoded offline transition matrix over residual buckets | mostly ACO | state/regime approach |
| Light linear state score | hardcoded offline coefficients over residual/spread/imbalance/depth | both | model-scored execution approach |
| Defensive regime switch | reduce/stop exposure when FV assumptions break | both | risk-control approach |
| Cross-product trading | use one product to predict the other | both | tested and not supported by current evidence |

---

## Per-Product Strategy Bank

### `INTARIAN_PEPPER_ROOT`

| Strategy ID | Approach | Signal / Edge | Status | Why Keep It |
| --- | --- | --- | --- | --- |
| `ipr_s1_drift_fv_mm` | Drift FV market making | `FV = day_start + 0.001*t`, quote around residual | primary | strongest clean FV evidence |
| `ipr_s2_directional_carry` | Max-long carry | persistent positive drift, target +80 | experimental | different risk/reward from market making |
| `ipr_s3_micro_scalper` | Microstructure edge | best-quote edge, spread, imbalance | experimental | tests small-margin execution edge |
| `ipr_s4_linear_score` | Light model score | residual + imbalance + spread/depth score | experimental | tests embeddable model without online training |
| `ipr_s5_defensive_hybrid` | Regime-aware hybrid | drift FV with exposure cut when residual/liquidity breaks | overlay/experimental | protects against slope/intercept failure |

### `ASH_COATED_OSMIUM`

| Strategy ID | Approach | Signal / Edge | Status | Why Keep It |
| --- | --- | --- | --- | --- |
| `aco_s1_fixed_fv_mm` | Fixed FV market making | `FV=10000`, spread capture, skew | primary | strongest clean ACO evidence |
| `aco_s2_tight_inventory_mm` | Aggressive tight MM | tighter quotes with stronger inventory skew | experimental | aims to maximize fills around stable FV |
| `aco_s3_micro_scalper` | Microstructure edge | sparse best-quote edge, imbalance, one-sided states | experimental | tests margin extraction |
| `aco_s4_markov_regime` | Offline Markov model | residual bucket expected next delta | experimental | tests hidden-pattern/regime hypothesis |
| `aco_s5_adaptive_defensive_fv` | Adaptive/regime FV | EMA fallback if fixed FV breaks | overlay/experimental | protects against hidden FV shift |

## Five-Bot Experiment Matrix

These bots are approved by user direction on 2026-04-16 for implementation as a performance-testing batch. The batch may contain more implementations than the active control panel; after validation, promote the best 1-2 to active testing.

| Bot ID | Candidate ID | IPR Strategy | ACO Strategy | Main Difference | Expected Strength | Main Risk |
| --- | --- | --- | --- | --- | --- | --- |
| `bot_01` | `candidate_09_baseline_fv_combo` | `ipr_s1_drift_fv_mm` | `aco_s1_fixed_fv_mm` | clean baseline FV bot | high robustness | may under-trade vs aggressive variants |
| `bot_02` | `candidate_10_carry_tight_mm` | `ipr_s2_directional_carry` | `aco_s2_tight_inventory_mm` | aggressive exposure and fills | high upside | concentrated IPR drift risk |
| `bot_03` | `candidate_11_microstructure_scalper` | `ipr_s3_micro_scalper` | `aco_s3_micro_scalper` | margin/microstructure approach | differentiated | may overfit book bounce |
| `bot_04` | `candidate_12_aco_markov_overlay` | `ipr_s1_drift_fv_mm` | `aco_s4_markov_regime` | Markov matrix for ACO | hidden-pattern test | bucket overfit |
| `bot_05` | `candidate_13_hybrid_adaptive_model` | `ipr_s5_defensive_hybrid` + `ipr_s4_linear_score` | `aco_s5_adaptive_defensive_fv` + light score | complex adaptive ensemble | robust/adaptive upside | complexity and parameter risk |

---

## Candidate Table

| Candidate ID | Product Scope | Source Of Edge | Linked EDA Signals | Feature Evidence | Regime Assumptions | Key Assumptions | Main Risk | Evidence Strength | Impl Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `candidate_01_ipr_drift_mm` | `INTARIAN_PEPPER_ROOT` | Drifting FV + spread capture | IPR drift slope 0.001/tick, R2=0.9999 | `FV(t)`, residual, spread | slope stable; day-start estimable | live slope remains close to historical | slope/intercept break | strong | low | high | low-medium | high | medium | reference candidate |
| `candidate_02_aco_fixed_fv_mm` | `ASH_COATED_OSMIUM` | Fixed FV + spread capture + inventory skew | ACO FV 10000; 94.4% within +/-10 | residual, spread, skew | FV stable; no hidden pattern active | live FV remains near 10000 | hidden pattern shifts FV | strong | low | high | low-medium | high | medium | reference candidate |
| `candidate_03_combined` | both | Independent combination of IPR drift FV and ACO fixed FV | original EDA + cross-product correlations near zero | combined residual/spread features | products independent by default | both product assumptions hold | compounded exposure to FV breaks | strong | low | high | medium | high | high | shortlisted |
| `candidate_04_ipr_directional_carry` | `INTARIAN_PEPPER_ROOT` | Maximize long exposure to deterministic positive drift | IPR +1000/day drift, R2=0.9999 | timestamp, drift FV, position capacity | drift stays positive during live round | long exposure beats spread capture | no downside if drift breaks | medium-strong | low | high | high | high | medium | deferred |
| `candidate_05_microstructure_edge_scalper` | both | Sparse best-quote edge + imbalance-aware execution | positive best-quote edge shares; imbalance corr ~0.64 | best bid/ask vs FV, spread, imbalance, one-sided flag | microstructure patterns persist | fill/replay preserves edge | overtrades bounce/noise | medium | medium | medium | medium | medium-high | high | shortlisted |
| `candidate_06_aco_markov_regime_mm` | `ASH_COATED_OSMIUM` | Hardcoded Markov transition matrix over residual buckets | ACO under bucket mean next delta +4.67; over bucket -4.06 | residual bucket, expected next delta | ACO mean-reversion states persist | buckets remain stable live | overfit; sparse deep states | medium | medium | medium | medium | medium-high | high | shortlisted |
| `candidate_07_light_linear_state_score` | both | Hardcoded linear score over residual/spread/imbalance/depth | day-0 R2 0.40-0.50; sign accuracy 0.66-0.82 | residual, imbalance, spread, depth, one-sided | short-horizon book state stable | simplified coeffs still work after collinearity removal | model chases bid-ask bounce | medium | medium-high | medium | medium-high | medium | medium | deferred |
| `candidate_08_defensive_regime_switch` | both | Reduce exposure when FV or book regime breaks | ACO deviation monitor; IPR slope/intercept caveats; cross-product independence | residual anomaly, spread/depth state, one-sided flags | breaks are detectable early | lower risk is worth lower historical PnL | too conservative; misses edge | weak-medium | medium | medium | low-medium | medium | medium | deferred overlay |
| `candidate_09_baseline_fv_combo` | both | Baseline FV combo | IPR drift FV; ACO fixed FV | residual, spread, inventory | historical FV regimes persist | product FVs remain stable | under-trades high-edge states | strong | low | high | medium | high | high | implementation batch |
| `candidate_10_carry_tight_mm` | both | IPR carry + aggressive ACO tight MM | IPR drift; ACO fixed FV | position capacity, tight spread, skew | drift and ACO FV persist | max-long IPR remains profitable | directionally concentrated | medium-strong | low | high | high | high | high | implementation batch |
| `candidate_11_microstructure_scalper` | both | Edge scalping and imbalance | best-quote edge; imbalance corr ~0.64 | edge, imbalance, spread, one-sided flags | book microstructure repeats | fills preserve quoted edge | overfits bounce | medium | medium | high | medium-high | medium-high | high | implementation batch |
| `candidate_12_aco_markov_overlay` | both | IPR FV + ACO Markov regime | ACO bucket mean next deltas | residual bucket, expected delta | ACO residual transitions persist | matrix remains stable live | sparse-state overfit | medium | medium | medium | medium | medium-high | high | implementation batch |
| `candidate_13_hybrid_adaptive_model` | both | defensive adaptive ensemble | light model metrics + regime caveats | residual, imbalance, EMA, spread/depth | regimes detectable online | adaptive logic avoids bad regimes | complexity/parameter risk | medium | high | medium | medium | high | medium-high | implementation batch |

---

## Shortlist

Shortlisted candidates (max 3 active):

1. `candidate_03_combined` - baseline production candidate with independent product FV logic.
2. `candidate_05_microstructure_edge_scalper` - conceptually different execution/margin strategy.
3. `candidate_06_aco_markov_regime_mm` - model/regime candidate aimed at the ACO hidden-pattern possibility.

Rationale:

- `candidate_03_combined` preserves the strongest existing evidence and is the safest baseline.
- `candidate_05_microstructure_edge_scalper` directly targets the user's request to exploit small interactions and margins without being only a parameter variant.
- `candidate_06_aco_markov_regime_mm` is the cleanest way to test an offline matrix/probability model while staying simple enough for the bot.
- `candidate_04_ipr_directional_carry` is plausible but not shortlisted because it is directionally concentrated and offers little protection if the IPR drift breaks.
- `candidate_07_light_linear_state_score` is promising but should be simplified before spec; raw and log residual are collinear.
- `candidate_08_defensive_regime_switch` is better as an overlay or fallback than as the next primary spec.

## Next-Wave Creative Backlog

The next-wave backlog is in `03_strategy_next_wave_branches.md`. It is not implementation-ready yet; it is a reviewed-strategy-candidate input for the next spec batch.

Recommended next 5 branches if the team wants a compact bot batch:

1. `14A_conservative_kalman`
2. `15A_three_state_hmm`
3. `16B_contextual_edge_gate`
4. `17A_late_flatten`
5. `18A_conservative_table`

Recommended additional branches if the team wants an 8-bot batch:

6. `20C_barbell_mode`
7. `21C_one_sided_exit`
8. `23C_conservative_fallback_controller`

Review caveat: these branches are grounded in platform logs and existing EDA, but they still need lightweight specs before implementation.

---

## Rejected Or Deferred Ideas

| Idea | Decision | Reason | Evidence Gap Or Risk |
| --- | --- | --- | --- |
| Log-transform-only strategy | rejected | Raw residual and price-scaled log residual have correlation 1.000 for both products | Adds complexity without new signal |
| Directional cross-product arbitrage / pairs trading | rejected | Same-time and lead-lag correlations are near zero; strongest residual lag magnitude is 0.0168 | No actionable relationship in sample |
| PCA-only trading rule | rejected | PCA gives useful state axes but not a direct tradable signal | Needs a strategy layer; not orders by itself |
| ACO deep-state Markov aggression | deferred | Deep buckets have too few observations (`deep_under` 4, `deep_over` 9) | Sparse states would overfit |
| Broad nonlinear feature search | deferred | Could explode scope without changing next implementation decision | Needs a targeted question first |

---

## Strategy Notes For Spec Writers

- Any combined bot must run product strategies in one `Trader.run()` and share `traderData` safely.
- Cross-product analysis does not support directional dependency. Treat products as independent unless a defensive shared risk overlay is explicitly selected.
- Markov and linear candidates must use offline constants only; no in-bot training and no external libraries.
- Microstructure candidates must specify capacity clipping before order placement, because exchange rejection cancels all orders that breach limits.
- One-sided books are common enough to require explicit behavior in every spec.
- Model-based candidates should include a fallback to the baseline FV logic when state is missing or malformed.

---

## Human Decisions Needed

- User approved moving to a five-bot performance batch on 2026-04-16.
- User requested creative next-wave strategy branches on 2026-04-17 before creating more bots.
- User decision recorded: implement all 10 families from `03_strategy_next_wave_branches.md`.
- Next human decision: choose which deployed files to run on the platform first if upload slots/time are limited.

---

## Next Action

Run next-wave platform submissions, preserve JSON/log artifacts, then rank with `analyze_platform_artifacts.py`.

---

## Review

- Reviewer: user request
- Review outcome: approved with caveats for implementation of all 10 families
- Date: 2026-04-17
- Notes: previous five-bot matrix was approved with caveats on 2026-04-16; next-wave families are approved for implementation exploration, not final submission.
