# Round 3 Understanding Summary

## Status

READY_FOR_REVIEW

Review outcome: `not reviewed`.

This artifact compresses Round 3 ingestion plus option-aware EDA into a
strategy-ready handoff. It does not create strategy candidates, specs, or bot
logic.

## Sources

- Wiki facts: `../../../docs/prosperity_wiki/rounds/round_3.md`, plus shared API
  and trading docs linked from `00_ingestion.md`.
- Ingestion: `00_ingestion.md`.
- EDA evidence: `01_eda/eda_option_surface_and_microstructure.md`.
- Other named artifacts:
  - `../data/processed/derived_round_3_product_signal_metrics.csv`
  - `../data/processed/derived_round_3_option_reversion_metrics.csv`
  - `../data/processed/derived_round_3_option_surface_summary.csv`
  - `../data/processed/derived_round_3_option_extrinsic_by_tte.csv`
  - `../data/processed/derived_round_3_same_time_return_corr.csv`
  - `../data/processed/derived_round_3_underlying_option_lead_lag.csv`
  - `../data/processed/derived_round_3_trade_alignment_summary.csv`
  - `../data/processed/derived_round_3_option_mutual_information.csv`
  - `../data/processed/derived_round_3_pooled_option_linear_model.csv`
  - `../data/processed/derived_round_3_option_pca_loadings.csv`
  - `01_eda/artifacts/round_3_eda_summary_metrics.json`
- Post-run research memory: absent for Round 3 at synthesis time.
- Playbook heuristics: none promoted as facts.

## Current Understanding

- Wiki fact: Round 3 algorithmic products are `HYDROGEL_PACK`,
  `VELVETFRUIT_EXTRACT`, and ten voucher symbols `VEV_4000` through
  `VEV_6500`; each voucher has a separate position limit of `300`.
- Wiki fact: the live Round 3 simulation is at TTE `5d`, while historical data
  maps to TTE `8d`, `7d`, and `6d`.
- Wiki fact: the Bio-Pod two-bid challenge is manual-only and must stay outside
  `Trader.run()`.
- EDA evidence: `HYDROGEL_PACK` is effectively independent from the
  `VELVETFRUIT_EXTRACT` plus voucher branch and should not be modeled as a
  hedge or shared signal family.
- EDA evidence: `VELVETFRUIT_EXTRACT` is the natural valuation anchor for the
  voucher family, especially `VEV_5000` to `VEV_5300`, where same-time return
  coupling is strongest.
- EDA evidence: the most decision-useful option features are
  `intrinsic_value` / `extrinsic_value`, `extrinsic_dev_day`, spread, and
  `imbalance_1`; delayed underlying-follow is negative evidence, not a promoted
  signal.
- EDA evidence: `VEV_6000` and `VEV_6500` behave as constant-floor instruments
  in sample data and should be excluded from first-wave implementations unless
  later evidence contradicts that.
- Hypothesis: first strategy work should branch into `(1)` delta-1
  microstructure candidates for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`,
  `(2)` residual / surface-aware voucher candidates for `VEV_5000` to
  `VEV_5300`, with `VEV_4000` / `VEV_4500` as second-wave ITM anchor variants.
- Unknown: the real TTE `5d` day is one step out-of-sample, and sparse printed
  trades in some vouchers mean execution validation matters more than raw
  surface structure alone.

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` should be treated as a separate strategy branch. | EDA same-time return correlation | strong | high | Live data or runs show a material hydrogel-velvetfruit linkage absent from sample. |
| `VELVETFRUIT_EXTRACT` should anchor voucher valuation. | wiki + EDA same-time coupling | strong | high | Official mechanics contradict option-underlying linkage or live books behave materially differently. |
| `VEV_5000` to `VEV_5300` are the highest-ROI active voucher subset. | EDA spread, coupling, extrinsic tables | strong | high | Fill-aware validation shows costs dominate this subset or another strike family clearly outperforms. |
| `VEV_4000` / `VEV_4500` are useful ITM structural anchors, but not the first execution focus. | EDA extrinsic reversion + sparse trade tape | medium/high | medium/high | Validation shows ITM residual logic is cleaner net of cost than the active subset. |
| Option residual logic is more promising than delayed-follow logic. | EDA MI, lead-lag, reversion metrics | strong | high | Live logs reveal stale option books or latency that creates real delayed-follow alpha. |
| Stable cross-strike surface shape should be used as a guardrail. | EDA surface summary | strong | medium/high | Final-day books show repeated monotonicity/convexity breaks. |
| `VEV_5400` / `VEV_5500` are execution-sensitive, not core first-wave products. | EDA relative spread + trade alignment | medium/high | medium | Passive fills or live economics show those strikes can be monetized despite wide spreads. |
| `VEV_6000` / `VEV_6500` should be excluded from first-wave bots. | EDA constant floor behavior | strong | high | Live or final-day data breaks the `0.5` floor regime. |
| `imbalance_1` is worth carrying forward, but only as a modest directional aid or filter. | EDA process metrics + linear model | medium | medium/high | Fill-aware validation shows it does not survive cost or a simpler anchor-only strategy beats it cleanly. |

## Signal Validation Expectations

- Statistical or regime evidence used: same-time return correlation,
  underlying-to-option lead-lag rejection, extrinsic reversion correlations,
  trade alignment summaries, mutual information ranking, pooled linear control
  model, PCA/loadings, and cross-strike monotonicity/convexity checks.
- Features downgraded for weak confidence, instability, or offline-only status:
  lagged underlying delta as alpha, the full duplicated price-anchor stack,
  aggressive use of `VEV_5400` / `VEV_5500` without execution filters, and all
  dynamic-alpha logic in `VEV_6000` / `VEV_6500`.
- Research outputs not trusted yet: the exact size of TTE `5d` decay, any
  trade-flow feature built from sparse prints in `VEV_4500` / `VEV_5000` /
  `VEV_5100`, and the pooled linear model as a standalone predictive engine.

## Multivariate Relationships Carried Forward

| Relationship | Source EDA Artifact | Evidence | Decision Impact | Confidence | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` vs `VELVETFRUIT_EXTRACT` | `derived_round_3_same_time_return_corr.csv` | same-time return correlation `0.0060` | separate product branches | high | negative evidence is sample-based, not a platform guarantee |
| `VELVETFRUIT_EXTRACT` vs `VEV_5000` / `VEV_5100` / `VEV_5200` | `derived_round_3_same_time_return_corr.csv` | same-time correlations `0.7524`, `0.7627`, `0.7192` | use the underlying as voucher anchor and prioritize this subset | high | same-time coupling is not delayed predictive alpha |
| underlying lagged delta into options | `derived_round_3_underlying_option_lead_lag.csv` | material only at lag `0`; near zero at lags `1`, `2`, `5`, `10` | avoid delayed-follow strategies | high | reopen only if live logs show stale books or latency |
| option residual and spread vs future option movement | `derived_round_3_option_mutual_information.csv`, `derived_round_3_pooled_option_linear_model.csv` | MI ranks `extrinsic_dev_day` `0.3358`, `spread` `0.2224`, `imbalance_1` `0.0565`, `underlying_delta_1` `0.0003`; pooled linear `R^2 = 0.0159` | prioritize residual / surface features over simple underlying-follow | medium/high | MI is ranking evidence, not direct PnL proof |
| option feature family redundancy | `derived_round_3_option_pca_loadings.csv`, `derived_round_3_option_pca_explained_variance.csv` | `PC1 = 72.0%` price-anchor family, `PC2 = 16.7%` imbalance, `PC3 = 10.8%` extrinsic | keep specs parsimonious and avoid feature dumping | high | PCA is explanatory only |
| voucher surface by strike | `derived_round_3_option_surface_summary.csv` | monotone `100%`; convex `99.91%` to `100%` | use as cross-strike sanity check and residual frame | high | stable structure is not alpha by itself |

## Redundancy Decisions

| Feature Family | Keep | Merge / Downgrade / Drop | Evidence | Strategy Impact |
| --- | --- | --- | --- | --- |
| price-anchor family | one valuation anchor plus residual | merge `mid_price`, `intrinsic_value`, `moneyness`, and raw spread context rather than stacking them | PCA `PC1` loads about `0.47` to `0.48` on these variables | voucher specs should pick one anchor formulation and one residual, not all raw transforms |
| residual/time-value family | `extrinsic_value`, `extrinsic_dev_day` | keep | MI and reversion metrics show residual information survives beyond intrinsic structure | option candidates can be residual-driven instead of raw-price-driven |
| microstructure family | `imbalance_1` as directional aid; spread as execution filter | keep both but with different roles | PCA isolates imbalance on `PC2`; spread stays with price-anchor family | do not confuse spread with alpha or imbalance with valuation |
| trade-tape family | none as first-wave primary feature | downgrade sparse voucher trade-flow ideas | trade summary is too uneven across strikes | if used later, treat as diagnostic or execution evidence only |
| deep OTM floor family | none | drop `VEV_6000` / `VEV_6500` from active signal family | zero variance, `0.5` mids, undefined correlations | first-wave specs should explicitly exclude them |

## Process Hypotheses Carried Forward

| Product Or Scope | Process Hypothesis | EDA Evidence | Confidence | Online Observable / Proxy | Strategy Or Validation Implication |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | short-horizon noisy delta-1 mean reversion with imbalance sensitivity | `delta_acf_1 = -0.1292`, `imbalance_corr_future_delta_5 = 0.1387`, mean rel spread `15.7` bps | medium | top-of-book mids, spread, imbalance | try a separate hydrogel microstructure candidate; require fill-aware validation |
| `VELVETFRUIT_EXTRACT` | tighter delta-1 anchor with mild reversion and modest imbalance signal | `delta_acf_1 = -0.1585`, `imbalance_corr_future_delta_5 = 0.1441`, mean rel spread `9.5` bps | high | best bid/ask, mid, imbalance | try both a standalone delta-1 branch and anchor logic for vouchers |
| `VEV_4000` / `VEV_4500` | deep ITM call-like instruments dominated by intrinsic value with residual snap-back | extrinsic reversion correlations `-0.7023` and `-0.7030`; extrinsic mean near zero | medium/high | underlying mid plus strike metadata | useful ITM anchor or structural residual branch; validate carefully because trade prints are sparse |
| `VEV_5000` / `VEV_5100` / `VEV_5200` / `VEV_5300` | active option regime with meaningful extrinsic, same-time underlying coupling, and tradable residual dynamics | strongest same-time coupling, non-zero extrinsic, manageable but still wide spreads | high | underlying mid, strike, extrinsic residual, imbalance, spread | best first-wave option subset for relative-value or residual-reversion candidates |
| `VEV_5400` / `VEV_5500` | thin OTM option regime where execution dominates raw signal quality | rel spread about `900` to `1859` bps; trades skew heavily to bid | medium | spread, top-of-book, passive fill behavior | only pursue with strong execution filters or passive-only logic |
| `VEV_6000` / `VEV_6500` | floor / nearly inactive regime | constant `0.5` mids, `20000` bps relative spread, undefined return correlations | high | floor price and spread only | exclude from first implementation wave; reopen only if live data breaks the floor |

## Assumptions Carried Forward

| Assumption | Source | Current-Round Evidence | Risk | Action |
| --- | --- | --- | --- | --- |
| voucher payoffs are call-like | ingestion + round text | intrinsic-value structure and monotone surface are consistent with calls | medium | use |
| tradable voucher symbols are the concrete `VEV_*` products, not a separate generic symbol | ingestion | raw data enumerates only concrete symbols; `Order` works on per-symbol products | medium | use and validate |
| historical day mapping `0 -> 8d`, `1 -> 7d`, `2 -> 6d` is correct | wiki fact | explicit round text | low | use |
| TTE `6d -> 5d` behavior will be directionally similar to `8d -> 7d -> 6d` | EDA hypothesis | extrinsic decays smoothly across observed days for active strikes | high | validate |
| `VEV_6000` / `VEV_6500` remain floor instruments on the live day | EDA evidence | constant sample mids and zero variance | medium | defer and reopen only on contradictory evidence |

## Signal Ledger

| Signal | Product | Source Artifact | Feature Basis | Feature Origin | Online Usability | Role | Stability | Confidence | Decision Action | Risk | Next Phase Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hydrogel imbalance-plus-reversion | `HYDROGEL_PACK` | `01_eda/eda_option_surface_and_microstructure.md` | `imbalance_1`, short-horizon delta reversion, spread | csv / online | usable online | direct signal | stable | medium | use | edge may disappear after crossing costs | generate a delta-1 hydrogel candidate with conservative execution checks |
| velvetfruit anchor imbalance-plus-reversion | `VELVETFRUIT_EXTRACT` | `derived_round_3_product_signal_metrics.csv` | `imbalance_1`, lag-1 reversion, spread | csv / online | usable online | direct signal | stable | medium/high | use | standalone directional effect is modest | generate a standalone VEX branch and carry it into voucher anchoring |
| intrinsic / extrinsic decomposition | `VEV_4000` to `VEV_5500` | `derived_round_3_option_extrinsic_by_tte.csv` | `intrinsic_value`, `extrinsic_value`, strike metadata | csv / online | usable online | direct signal | stable | high | use | relies on call-like interpretation and TTE-aware calibration | make this the valuation base for serious voucher candidates |
| extrinsic residual reversion | `VEV_4000` to `VEV_5300` | `derived_round_3_option_reversion_metrics.csv` | `extrinsic_dev_day` around day-product baseline | csv / online | usable online | direct signal | day-sensitive | medium/high | use | signal may weaken at TTE `5d` or after costs | prioritize in option candidates and validate on fill-aware markouts |
| surface sanity frame | voucher family | `derived_round_3_option_surface_summary.csv` | monotonicity and convexity across strike | csv / online | usable online | risk control | stable | high | use | structural sanity is not alpha | define as validation guardrail in later specs |
| spread-aware execution filter | `VEV_5400` / `VEV_5500` and all options | `derived_round_3_trade_alignment_summary.csv` | relative spread, trade alignment vs bid/ask | csv / online | usable online | execution filter | regime-dependent | medium/high | use | passive economics may still fail | if those strikes are tried, require strong spread gates |
| delayed underlying-follow | active vouchers | `derived_round_3_underlying_option_lead_lag.csv` | lagged underlying delta | csv / online | usable online | avoid | stable | high | avoid | using it adds complexity without sample support | keep as negative evidence in strategy generation |
| deep OTM floor behavior | `VEV_6000`, `VEV_6500` | `derived_round_3_product_signal_metrics.csv` | constant mid, zero variance, one-tick spread | csv / online | usable online | avoid | stable | high | avoid | live day could differ | classify as excluded-from-first-wave, not ignored |

## Strategy-Relevant Insights

| Insight | Linked EDA Signals | Feature Evidence | Regime Assumptions | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| Round 3 should be split into a hydrogel branch and a velvetfruit-plus-voucher branch. | hydrogel imbalance-plus-reversion; same-time return separation | hydrogel-vex correlation `0.0060` | products behave independently in sample | high | do not force a multi-product hedge framework in first specs |
| `VELVETFRUIT_EXTRACT` is an anchor, not just another delta-1 product. | intrinsic / extrinsic decomposition; same-time coupling | strongest option coupling around `VEV_5000` to `VEV_5200` | same-time anchor relation remains meaningful at TTE `5d` | high | option specs should define valuation relative to underlying |
| First-wave option work should focus on residual mispricing, not delayed-follow. | extrinsic residual reversion; delayed underlying-follow reject | MI ranks residual and spread above underlying delta | same-time coupling exists but lagged chase does not | high | prioritize relative-value / residual candidates |
| ITM vouchers and active near-ATM vouchers deserve different roles. | ITM residual snap-back; active option regime | `VEV_4000` / `VEV_4500` mostly intrinsic, `VEV_5000` to `VEV_5300` hold more extrinsic | distinct process groups by moneyness | medium/high | split candidate families instead of one monolithic voucher model |
| OTM and floor vouchers are mainly execution or exclusion problems. | spread-aware execution filter; deep OTM floor behavior | `VEV_5400` / `VEV_5500` wide spreads; `VEV_6000` / `VEV_6500` constant floors | execution dominates signal quality there | high | deprioritize them for first-wave bots |

## Product Attribution View

| Product | Opportunity / Risk Status | Evidence | Main Uncertainty | Strategy Implication |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | edge likely but execution-sensitive | mild reversion plus positive imbalance signal | whether the edge survives costs better than on options | keep as its own simple delta-1 branch |
| `VELVETFRUIT_EXTRACT` | edge likely and high leverage to the rest of the round | tight spread, stable imbalance effect, anchor role for vouchers | whether standalone alpha is strong enough versus using it mainly as anchor | treat as both standalone candidate and voucher valuation anchor |
| `VEV_4000` | structural anchor / second-wave opportunity | strong ITM residual snap-back and strong underlying coupling | sparse printed trades vs book-derived signals | include in understanding and second-wave option queue |
| `VEV_4500` | structural anchor but evidence-light on execution | similar ITM structure to `VEV_4000` with only one printed trade | whether execution is too thin to matter | keep in second-wave queue, not first-wave core |
| `VEV_5000` / `VEV_5100` / `VEV_5200` / `VEV_5300` | best first-wave option scope | strongest same-time coupling, meaningful extrinsic, workable spreads | TTE `5d` extrapolation and fill quality | prioritize for residual / surface-aware candidates |
| `VEV_5400` / `VEV_5500` | risk-heavy / execution-heavy | very wide relative spreads and bid-side print skew | whether passive execution can rescue economics | do not use early unless the candidate is explicitly passive/filter-heavy |
| `VEV_6000` / `VEV_6500` | low priority / likely no edge | constant `0.5` mids and zero variance | floor may break live | exclude from first wave but keep in coverage tables |

## Cross-Product Verdict

- Verdict: `useful`
- Evidence: cross-product structure matters inside the
  `VELVETFRUIT_EXTRACT` plus voucher family, especially for same-time anchoring,
  surface sanity, and residual logic; hydrogel remains a separate branch.
- Caveat: this is useful same-time structure, not evidence for lagged
  follow-the-underlying alpha.

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| simple hydrogel microstructure candidate | separate hydrogel branch | `HYDROGEL_PACK` | the product has clean online features and does not depend on option complexity | fill-aware reversion and imbalance markouts |
| velvetfruit standalone anchor / delta-1 candidate | anchor-plus-standalone role | `VELVETFRUIT_EXTRACT` | tightest spreads in the round and likely useful even if option logic underperforms | compare standalone edge vs anchor-only usage |
| residual-reversion option candidate | residual mispricing insight | `VEV_5000` / `VEV_5100` / `VEV_5200` / `VEV_5300` | strongest first-wave option subset with nontrivial extrinsic | cost-aware replay, TTE `5d` robustness, spread filters |
| ITM structural-anchor option candidate | ITM vouchers have different role | `VEV_4000` / `VEV_4500` | deep ITM instruments may offer cleaner residual anchoring than near-ATM names | validate despite sparse printed trades |
| passive / filtered OTM option variant | execution-heavy OTM regime | `VEV_5400` / `VEV_5500` | only if we want a later challenger focused on passive economics | passive fill assumptions and spread-gated performance |

## What Should Not Be Trusted Yet

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| lagged underlying-follow into vouchers | lead-lag evidence is strongly negative after lag `0` | complexity without edge | keep rejected unless live logs contradict sample |
| exact TTE `5d` residual decay | live round is one day shorter than sample | overfit residual baselines or thresholds | validate in runs and keep assumptions explicit |
| sparse trade-tape signals for `VEV_4500` / `VEV_5000` / `VEV_5100` | too few prints to promote flow-style features | false confidence about execution or trade pressure | use books first; revisit with richer logs only if needed |
| `VEV_6000` / `VEV_6500` as dynamic alpha sources | constant mids remove any sample signal | waste implementation effort | only reopen on contradictory live evidence |
| generic pooled linear predictor for options | `R^2` is too low and underlying delta contributes almost nothing | false predictive comfort | use only as ranking evidence, not direct bot logic |
| exact manual second-bid rule below `avg_b2` | source wording remains ambiguous | wrong manual bidding assumptions | defer to manual decision process, not bot work |

## Research Memory

Promising features:

| Feature Or Signal | Source | Why Promising | Needed Before Strategy |
| --- | --- | --- | --- |
| `imbalance_1` | `derived_round_3_product_signal_metrics.csv` | simple online signal that helps both delta-1 and some active vouchers | decide whether it is primary edge or just execution overlay per product |
| intrinsic / extrinsic decomposition | `derived_round_3_option_extrinsic_by_tte.csv` | turns voucher family into a coherent option problem instead of isolated prices | choose exact valuation anchor in strategy candidates |
| `extrinsic_dev_day` | `derived_round_3_option_reversion_metrics.csv` | strongest option-specific mispricing signal found so far | validate TTE `5d` robustness and cost survivability |
| surface monotonicity / convexity | `derived_round_3_option_surface_summary.csv` | strong structural guardrail for later specs and validation | define how to use it as sanity check rather than alpha |
| same-time VEX-voucher coupling | `derived_round_3_same_time_return_corr.csv` | supports product grouping and active strike prioritization | convert into simple anchor logic, not lag-follow logic |

Rejected / noisy features:

| Feature Or Signal | Source | Evidence Against | Reopen Only If |
| --- | --- | --- | --- |
| lagged underlying-follow | `derived_round_3_underlying_option_lead_lag.csv` | correlations collapse toward zero after lag `0` | live logs show stale option books or latency |
| hydrogel-vex hedge framing | `derived_round_3_same_time_return_corr.csv` | near-zero correlation | later runs show real shared risk or inventory interactions |
| dynamic alpha in `VEV_6000` / `VEV_6500` | `derived_round_3_product_signal_metrics.csv` | constant floors, zero variance | live day breaks the floor regime |
| price-anchor feature dumping | `derived_round_3_option_pca_loadings.csv` | heavy redundancy across anchor variables | a spec proves an incremental role for more than one anchor feature |

Unresolved / log-needed features:

| Feature Or Signal | Source | Missing Evidence | Next Action |
| --- | --- | --- | --- |
| TTE `5d` residual behavior | EDA vs live-day gap | final-day decay is unobserved historically | keep explicit as strategy/spec risk and validate in runs |
| sparse voucher trade-flow evidence | trade summary / alignment tables | too few prints for some strikes | only collect extra logs if first-wave candidates need flow diagnostics |
| live behavior of `VEV_5400` / `VEV_5500` passive fills | trade alignment plus wide spread | sample suggests execution pain but not passive PnL | reserve for later variant if first-wave logic stalls |
| live behavior of `VEV_6000` / `VEV_6500` | constant-floor sample | no evidence whether floor holds in final day | keep product coverage but exclude from first-wave logic |

## Confidence And Impact

- Overall confidence: `medium/high` for strategy direction, `medium` for net
  implementation payoff.
- Highest-impact implication: Round 3 should be treated as a separate
  hydrogel branch plus an option family anchored on `VELVETFRUIT_EXTRACT`, with
  first-wave option work focused on residual / surface logic rather than
  delayed-follow.
- Main caveat: the real round is at TTE `5d`, one step beyond the historical
  sample, and option execution costs may dominate raw signal quality.

## Assumptions

- The voucher family behaves like call options on `VELVETFRUIT_EXTRACT`.
- Concrete `VEV_*` symbols are the effective orderable products for bot logic.
- Sample surface structure and residual behavior are useful evidence, not
  official rules.
- First-wave strategy work should stay feature-light and validate execution
  before adding complexity.

## Open Questions

- How much sharper will residual decay or surface behavior become at TTE `5d`
  versus the observed `8d`, `7d`, and `6d` history?
- Is the best first option candidate the active near-ATM subset
  `VEV_5000` to `VEV_5300`, or an ITM anchor variant around `VEV_4000` /
  `VEV_4500`?
- Can `VEV_5400` / `VEV_5500` support any passive-only economics, or should
  they remain purely deprioritized?
- Will the floor behavior of `VEV_6000` / `VEV_6500` hold on the live day?
- Outside bot work, what is the exact manual fill rule when `b2 < avg_b2`?

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| TTE `5d` is out-of-sample relative to available history | strategy / spec / validation | high | keep TTE assumptions explicit and validate in first runs |
| option spreads may erase raw residual edge | strategy / validation | high | use spread as filter and require fill-aware markouts |
| sparse prints in some strikes may mislead execution intuition | strategy / spec / validation | medium/high | prefer book-based signals first; treat trade-flow as diagnostic only |
| live floor break in `VEV_6000` / `VEV_6500` | strategy / validation | medium | keep those products covered in monitoring but exclude from first-wave logic |
| exact round-end timestamp remains unknown | planning | medium | keep deadline as `UNKNOWN`; clarify only if timing pressure becomes material |
| manual second-bid wording remains ambiguous | manual challenge | low for algorithmic work | defer separately and do not let it block strategy work |

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| best first-wave option subset net of costs | strategy / spec / validation | high | compare active `VEV_5000` to `VEV_5300` vs ITM anchor variants in Phase 03 |
| TTE `5d` robustness of residual signals | strategy / spec / validation | high | keep as explicit candidate/spec risk and validate quickly in runs |
| role of `imbalance_1` in option candidates | strategy / spec | medium/high | decide whether it is primary edge or overlay per candidate |
| viability of `VEV_5400` / `VEV_5500` passive logic | strategy / later variants | medium | defer unless first-wave ideas stall or validation capacity remains |
| live behavior of floor vouchers | validation | medium | monitor in runs; reopen only on contradictory evidence |

## Strategy Implications

- Candidate direction: begin Phase 03 with separate branches for
  `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, active voucher residual logic, and
  ITM structural-anchor voucher logic.
- Candidate direction: keep first-wave option scope centered on
  `VEV_5000` / `VEV_5100` / `VEV_5200` / `VEV_5300`, while carrying
  `VEV_4000` / `VEV_4500` as differentiated second-wave variants.
- Risk or constraint: keep the feature budget tight; each serious candidate
  should use one primary edge feature or fair-value model plus at most simple
  spread / imbalance support.
- Risk or constraint: specs must explicitly classify `VEV_*` symbol metadata,
  TTE assumptions, spread filters, and the exclusion or deprioritization of
  `VEV_5400` / `VEV_5500` / `VEV_6000` / `VEV_6500`.
- Validation/debug implication: first validations should prioritize fill-aware
  markouts, TTE sensitivity, and checks that the strategy is not silently
  relying on rejected delayed-follow logic.

## Next Action

- Next: review this understanding summary, then generate the default
  `02b_external_paper_research.md` prompt focused on short-dated option
  microstructure, residual/surface-aware pricing, and execution under wide
  spreads before Phase 03 strategy generation.

## Review

- Reviewer: Unassigned
- Review outcome: not reviewed
- Date: 2026-04-24
