# Round 1 Strategy Research Pass - Per-Product Top 3 And 3x3 Matrix

## Status

READY_FOR_REVIEW

## Scope

This pass revisits Round 1 evidence across wiki facts, sample CSVs, EDA, platform JSON/log artifacts, run summaries, current bots, historical bots, and existing strategy/spec artifacts.

Constraint applied throughout: no strategy here uses known sample length, time remaining, or end-of-sample liquidation timing. Rolling windows, local horizons, current inventory, current order book state, and local signal persistence are allowed.

## Source Map

- Wiki facts: `docs/prosperity_wiki/rounds/round_1.md`, API contract, datamodel, exchange mechanics, and position-limit docs.
- EDA: `01_eda/eda_round_1.md`, `01_eda/eda_strategy_expansion_feature_lab.md`, `01_eda/eda_strategy_expansion_models.md`, `01_eda/eda_cross_product_relationships.md`, `01_eda/eda_advanced_signal_research.md`.
- Processed metrics: `../data/processed/strategy_expansion_metrics.json`, `../data/processed/advanced_signal_research_metrics.json`.
- Performance evidence: `../performances/noel/canonical/run_20260417_platform_artifact_analysis.md`, `../performances/noel/canonical/run_20260416_cross_bot_log_insights.md`.
- Bot evidence: Noel canonical/historical Round 1 bots and related Amin/Bruno artifacts listed in the performance analysis.

## 1. Evidence Review

### Official Constraints

| Fact | Strategy Impact |
| --- | --- |
| `Trader.run(state)` must return `result, conversions, traderData` | All candidates must fit inside a single pure-Python `trader.py` with O(1) online inference. |
| `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT` both have position limit +/-80 | Long and short are both legal, but every candidate must capacity-clip both sides before order placement. |
| Positive order quantity buys; negative order quantity sells | Short-side exploitation is just sell-side order logic plus inventory/risk control, not a special API. |
| Resting orders can be hit by platform bots during the iteration | Passive maker policy matters; local immediate-fill replay is not enough for ACO ranking. |

### Strongest Repeatable Glimpses

| Finding | Class | Product | Suggests | Repeatability | Affects |
| --- | --- | --- | --- | --- | --- |
| IPR +80 carry repeatedly earns `7286.0` IPR PnL in platform artifacts | strong | IPR | Treat max-long carry as the base IPR module | high across all strong Noel next-wave runs and Amin comparison artifacts | signal/risk |
| IPR round-trip or short-aware bots give up too much carry | strong | IPR | IPR shorts should be defensive/special-case only, not primary | high: `candidate_09/12` IPR `1862.0`, `candidate_13` `5194.4`, `candidate_11` `694.6` | signal/risk |
| ACO best result is balanced two-sided maker: `2721.0` ACO, final ACO `0`, buy/sell `225/225` | strong | ACO | Spread capture around FV 10000 with inventory skew is still the clean base | high in logs and consistent with EDA | execution/risk |
| ACO Markov/regime logic nearly matches best ACO but failed total due IPR choice | medium-strong | ACO | Steal the ACO filter, not the whole old bot | repeatable enough: `candidate_12` ACO `2689.9`; `candidate_14` ACO `2553.8` on +80 IPR base | signal/execution |
| ACO edge-quality beats raw volume | strong | ACO | Quote selection matters more than blindly increasing size | high: high-volume low-edge variants underperform lower-volume high-edge variants | execution |
| ACO microprice/imbalance/one-sided states help as overlays, not standalone cores | medium | ACO mostly | Use book-state to skew/skip/exit, not to replace FV | supported by EDA and candidates 21/22, contradicted by pure micro bot 11 | execution |
| Cross-product directional relationship is near zero | strong | both | Do not build pairs trading or lead-lag between products | high in current CSV analysis; strongest residual lag magnitude about `0.0168` | regime |
| Time-bucket or lifecycle flattening is dangerous if it assumes sample ending | misleading if used directly | ACO | Use local inventory and fill-quality control; avoid "end soon" rules | candidate 17 underperformed and violates the spirit if tied to fixed sample horizon | risk |

### Required Lightweight Direction Verdicts

| Direction | ACO Verdict | IPR Verdict | Reason |
| --- | --- | --- | --- |
| Microprice + order book imbalance | medium | weak-medium | ACO micro corr `0.322`, L1 imbalance sign `0.916`; IPR similar book signal exists but total PnL says do not replace carry. |
| Residual z-score vs book/FV | strong | strong as execution, not core | ACO z50 2.0 hit `0.964` over `2584` rows; IPR z50 2.0 hit `0.970`, but carry dominates. |
| Change-point / CUSUM | weak-medium | weak-medium | Reversal hit rates are not strong enough as primary; useful as defensive guard if FV/carry breaks. |
| OU / half-life | medium | weak-medium | ACO half-life around `2.28` observations supports short local reversion; IPR half-life near zero mostly reflects bounce/snapback around drift FV. |
| Trade flow / signed pressure proxy | weak | medium | ACO trade pressure sign accuracy about random; IPR pressure sign `0.672`, but sparse and weaker than carry. |
| Spread regime model | medium | weak-medium | Helps quote width/liquidity filtering; not directional enough alone. |
| Volatility regime filter | medium | weak-medium | Useful to widen/skip, but no evidence it should decide exposure alone. |
| Targeted conditional feature interactions | strong | medium | Residual+imbalance interactions are very strong for ACO; IPR interactions are real but mostly execution-level. |
| Inventory-skew optimization | strong | medium | ACO final-flat best run and edge/volume tradeoff make this central; IPR inventory should mostly target +80. |
| Maker vs taker policy learned offline | strong | medium | ACO passive fills explain platform edge; sparse high-edge taker sweeps can be added. IPR taker policy is mostly how to get long safely. |

### Short-Side Analysis

Current good runs are heavily long-biased on IPR and genuinely two-sided on ACO.

For IPR, short-side opportunity is not attractive as a primary source of PnL. The best artifacts buy to +80 and do not sell. Bots that trade both sides or finish short lose the dominant drift carry. A short-aware IPR module is still useful as a guard if early live evidence contradicts the drift, but it should not consume the base strategy.

For ACO, short-side exploitation is essential. The best ACO result is not long-only; it buys below fair, sells above fair, finishes flat, and earns from both sides. The next gains should come from better sell-side exits, one-sided-book exits, and inventory-aware ask placement rather than from forcing directional shorts.

## 2. Top 3 Candidates For `ASH_COATED_OSMIUM`

### A1 - Clean Fixed-FV Balanced Maker

| Field | Detail |
| --- | --- |
| Strategy family | Fixed fair-value market making plus inventory skew |
| Signals | `FV=10000`, best bid/ask edge, spread capture, current inventory |
| Feature basis | ACO fixed FV evidence, platform best ACO `2721.0`, final ACO `0`, buy/sell `225/225` |
| Longs/shorts | Both |
| Why it fits | ACO is stable enough around 10000 and platform passive fills reward clean two-sided quoting |
| Expected edge | Highest proven base; target is to preserve `2700+` ACO and avoid dragging IPR |
| Main risk | Too much volume at low edge or weak inventory skew can turn fills toxic |
| Implementation difficulty | low |
| Origin | corrected/evolved from `candidate_10_bot02_carry_tight_mm` |

Decision: keep as clean base and exploit carefully.

### A2 - Residual-Regime Maker With Markov/Kalman/Z-Score Gates

| Field | Detail |
| --- | --- |
| Strategy family | Offline residual regime model over fixed FV |
| Signals | residual bucket, z-score, Kalman innovation, local OU/reversion state |
| Feature basis | ACO Markov under/over buckets revert; z50 2.0 hit `0.964`; `candidate_12` ACO `2689.9`; `candidate_14` ACO `2553.8` while preserving IPR +80 |
| Longs/shorts | Both |
| Why it fits | ACO has hidden-pattern hints and stronger local reversion than IPR |
| Expected edge | Potential to beat A1 if it keeps A1 volume while filtering bad states |
| Main risk | Over-filtering reduces matched quantity; model state can become a slower version of fixed FV |
| Implementation difficulty | medium |
| Origin | evolved from prior Markov/Kalman/HMM work, corrected to preserve IPR base |

Decision: exploit further, but only as an ACO module grafted onto B1/B3.

### A3 - Book-State Execution Overlay

| Field | Detail |
| --- | --- |
| Strategy family | Microprice, imbalance, one-sided-book, maker/taker policy overlay |
| Signals | L1 imbalance, microprice offset, one-sided book state, spread/depth/liquidity state, sparse taker edge |
| Feature basis | ACO L1 imbalance sign `0.916`, micro sign `0.901`, residual+imbalance interactions up to `0.968` hit rate; `candidate_21` ACO `2477.5`, `candidate_22` ACO `2371.2` |
| Longs/shorts | Both, with special value on inventory-reducing sells/buys |
| Why it fits | ACO gains are now execution-limited, not fair-value-limited |
| Expected edge | Medium standalone, high as overlay on A1 |
| Main risk | Pure microstructure failed when it replaced core FV; must remain an overlay |
| Implementation difficulty | medium |
| Origin | evolved from microstructure and one-sided-book experiments |

Decision: exploit further as an overlay, not as standalone.

## 3. Top 3 Candidates For `INTARIAN_PEPPER_ROOT`

### B1 - Max-Long Drift Carry

| Field | Detail |
| --- | --- |
| Strategy family | Directional carry to position +80 |
| Signals | deterministic positive drift, stable historical FV slope, position capacity |
| Feature basis | All strong platform artifacts with final IPR +80 earn `7286.0`; +75 earns `6836.5`; round-trip versions earn far less |
| Longs/shorts | Long-only in normal regime |
| Why it fits | IPR drift edge is larger and more reliable than short-horizon round-trip edge in run history |
| Expected edge | Strongest proven IPR module |
| Main risk | If live drift/intercept breaks, concentrated long exposure hurts |
| Implementation difficulty | low |
| Origin | corrected/evolved from `candidate_10` and `candidate_19` |

Decision: keep as clean base. Do not make it clever unless evidence changes.

### B2 - Drift-FV Residual Market Maker

| Field | Detail |
| --- | --- |
| Strategy family | Drift fair-value market making / round-trip residual reversion |
| Signals | `FV = intercept + 0.001*t`, residual z-score, best quote edge, local reversion |
| Feature basis | CSV residual/z-score reversion is strong, but platform artifacts show IPR PnL only `1862.0` when it replaces carry |
| Longs/shorts | Both |
| Why it fits | It is the only real IPR short-aware candidate with evidence; useful if carry fails |
| Expected edge | Lower than B1 in current evidence; possible defensive alternative |
| Main risk | Sacrifices the main drift carry; short side fights the best known signal |
| Implementation difficulty | low-medium |
| Origin | evolved from `candidate_09` and `candidate_12` |

Decision: keep as backup/short-side research, not primary.

### B3 - Guarded Carry With Local Regime Checks

| Field | Detail |
| --- | --- |
| Strategy family | B1 carry plus defensive CUSUM/slope/volatility/liquidity guard |
| Signals | early local slope sanity, residual z-score anomaly, CUSUM-like drift break, spread/one-sided state |
| Feature basis | B1 is strongest; CUSUM is not strong enough as alpha but useful for guardrails; IPR pressure and z-score can refine execution |
| Longs/shorts | Mostly long; shorts only under explicit drift-break evidence |
| Why it fits | Keeps the proven +80 behavior while adding a small escape hatch |
| Expected edge | Similar to B1 if guard does not trigger; lower upside but better robustness |
| Main risk | Guard can falsely de-risk and lose the best PnL source |
| Implementation difficulty | medium |
| Origin | new/corrected overlay from change-point and defensive-regime work |

Decision: correct/test as an overlay; do not use as a standalone replacement.

## 4. 3x3 Combination Matrix

| Pair | Compatibility | Why | One `trader.py` Realism | Execution/Risk Alignment | Interference Risk | Short-Side Effect | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 + B1 | high | Best proven ACO base plus best proven IPR base | high | Simple independent modules; shared capacity clipping only | low | Strong ACO shorts, no IPR shorts | move forward |
| A1 + B2 | medium | A1 is robust, but B2 gives up IPR carry | high | Both are maker-style and simple | medium: B2 may churn IPR away from drift | Strongest simple two-product short usage, but lower expected PnL | backup only |
| A1 + B3 | high | A1 stable; B3 preserves carry with guard | high | Clean base plus conservative risk overlay | low-medium: guard false positives | ACO shorts remain; IPR shorts rare/defensive | move forward |
| A2 + B1 | high | Highest-upside ACO model while preserving IPR +80 | medium-high | A2 needs careful volume/inventory control; B1 stays simple | medium: A2 over-filtering can underperform A1 | ACO shorts active; no IPR shorts | move forward |
| A2 + B2 | low-medium | Both sides become model/regime-heavy and B2 loses IPR carry | medium | Too many moving pieces for a first combined promotion | high: simultaneous overfitting and IPR churn | More shorts, but not the right shorts | reject early |
| A2 + B3 | medium-high | Robust IPR plus model ACO is coherent | medium | B3 guard and A2 regime logic both need state, but products are independent | medium: complexity can reduce fill quality | ACO shorts active; IPR shorts only defensive | backup / later move forward |
| A3 + B1 | medium-high | Execution overlay on ACO with proven IPR base | medium-high | A3 must be constrained to not replace A1 entirely | medium: micro overlay can overreact to bounce | Best viable short-side exploitation through ACO exits | move forward / backup |
| A3 + B2 | medium-low | Maximizes short-side experimentation but sacrifices proven IPR edge | medium | Both are execution-sensitive; harder to rank cleanly | high: IPR churn plus ACO micro noise | Most explicit shorts, but likely lower total | backup for short research only |
| A3 + B3 | medium | Defensive/execution-heavy pair; robust but may under-trade | medium | Coherent if A3 is only an overlay and B3 guard is conservative | medium-high: too many gates can starve fills | ACO shorts active; IPR shorts rare | keep as backup |

## 5. Best Combined Directions

| Category | Pair | Reason |
| --- | --- | --- |
| Best overall pair | A1 + B1 | It is the only combination already proven over the `10000` platform-artifact bar: total `10007.0`, IPR `7286.0`, ACO `2721.0`. |
| Safest pair | A1 + B1 | Lowest complexity, strongest run evidence, cleanest product independence. |
| Highest-upside pair | A2 + B1 | Keeps the full IPR engine while trying to recover the near-best ACO Markov/Kalman edge and possibly exceed A1. |
| Best viable pair for exploiting shorts | A3 + B1 | Uses ACO short-side and one-sided exits aggressively without sacrificing the IPR carry engine. |
| Pair most likely to fail from execution/risk mismatch | A2 + B2 | It combines ACO model risk with IPR churn and gives up the most repeatable source of PnL. |

## 6. Exploit More vs Keep Base

### Per-Product Candidates

| Candidate | Decision | Rationale |
| --- | --- | --- |
| A1 Clean Fixed-FV Balanced Maker | keep as clean base and exploit further | Proven top ACO; optimize quote size/skew/fill policy without changing the identity. |
| A2 Residual-Regime Maker | exploit further | Strong enough to test, but must be grafted onto B1 and benchmarked against A1. |
| A3 Book-State Execution Overlay | exploit further as overlay | Valuable for short-side/execution, weak as standalone. |
| B1 Max-Long Drift Carry | keep as clean base | This is the most repeatable IPR edge. |
| B2 Drift-FV Residual MM | correct implementation/execution only as backup | Useful for short-side research, but current evidence says discard as primary. |
| B3 Guarded Carry | correct/test as overlay | Worth adding only if it rarely interrupts B1 and only reacts to clear drift-break evidence. |

### Best Pairings

| Pair | Decision | Rationale |
| --- | --- | --- |
| A1 + B1 | keep as clean base | Current champion; use as control and minimum bar. |
| A2 + B1 | exploit further | Best high-upside research pair. |
| A3 + B1 | exploit further | Best viable short-side/execution pair. |
| A1 + B3 | keep as safety variant | Good robustness test if B3 is conservative. |
| A2 + B2 | discard | Over-complex and gives up IPR carry. |
| A3 + B2 | backup only | Interesting short research, not a likely final submission path. |

## 7. Recommended Next Actions

Move forward with these per-product candidates:

1. A1 as the control ACO module.
2. A2 as the high-upside ACO module.
3. B1 as the locked IPR module.
4. A3 as the execution/short-side overlay if we want a third combined bot.

Move forward with these pairings:

1. A1 + B1 - control / current bar.
2. A2 + B1 - highest-upside next bot.
3. A3 + B1 - best execution and short-side test.

Do not spend the next implementation slot on B2 unless the explicit goal is short-side research rather than beating `10007.0`. B2 is useful knowledge, but not the best path to a final Round 1 submission.

The 3x3 stage is trustworthy enough for selecting next specs because the evidence is not only CSV-based: it is also backed by platform JSON/log splits and historical bot behavior. The remaining uncertainty is not "what families should we consider"; it is "which ACO execution variant beats A1 without lowering fill volume too much."

Recommended build path:

1. Write one-page specs for A2+B1 and A3+B1, preserving A1+B1 as the control.
2. Implement 2 bots only at first: A2+B1 and A3+B1.
3. Run platform submissions and rank by JSON `profit`; use final `activitiesLog` per-product PnL for attribution.
4. Promote only if total beats `10007.0` or if ACO beats `2721.0` without weakening IPR `7286.0`.

## 8. Additional Strategy Directions Worth Testing

The current candidate set is sufficiently comprehensive for Round 1 strategy-family selection. It covers:

- the proven base edge: B1 + A1;
- hidden-pattern/model ideas: A2;
- execution and short-side extraction: A3;
- defensive regime handling: B3;
- backup IPR shorts/round-trip: B2.

No broad new direction should be researched before implementing the best current candidates. Further breadth would mostly duplicate one of the selected axes or distract from the real bottleneck: ACO fill quality under platform matching.

If extra work is available after A2+B1 and A3+B1 are tested, it should be a narrow refinement inside the selected set, not a new family:

| Direction | Why Not Separate Top Candidate | Unique Edge | Timing | Priority |
| --- | --- | --- | --- | --- |
| ACO quote-size and inventory-skew optimizer | It is an A1/A3 refinement, not a new signal family | Could improve ACO matched quantity without lowering average edge | after first A2/A3 pair tests | medium |
| Conservative IPR drift-break guard | It is B3, not a new candidate | Could prevent rare catastrophic carry failure | after the baseline/control remains stable | low-medium |

## Final Recommendation

The next serious push should not be ten more unrelated bots. It should be a tight control-plus-two challengers:

1. Control: A1 + B1.
2. Challenger 1: A2 + B1.
3. Challenger 2: A3 + B1.

That gives us one proven base, one high-upside model/regime ACO variant, and one execution/short-side ACO variant, all while preserving the strongest IPR engine.

