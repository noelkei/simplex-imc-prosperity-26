# Round 4 EDA - Counterparty And Option Book

## Status

`READY_FOR_REVIEW`

## Question

- Question:
  What does the Round 4 raw data say about counterparty structure, option-book structure, and which `round_3` carry-forward lessons still deserve trust before understanding and strategy work?
- Product scope:
  `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Why this matters downstream:
  `round_4` is the same algorithmic market as `round_3`, but now trade data exposes named counterparties. We need to know whether that new layer creates reusable signal context, changes product-role framing, or weakens prior assumptions.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | yes | yes | likely | include |
| `VELVETFRUIT_EXTRACT` | yes | yes | likely | include |
| `VEV_4000` | yes | yes | likely | include |
| `VEV_4500` | yes | partial | possible | investigate |
| `VEV_5000` | yes | partial | possible | investigate |
| `VEV_5100` | yes | partial | possible | investigate |
| `VEV_5200` | yes | yes | possible | include cautiously |
| `VEV_5300` | yes | yes | likely | include cautiously |
| `VEV_5400` | yes | yes | possible | investigate |
| `VEV_5500` | yes | yes | possible | investigate |
| `VEV_6000` | yes | partial | no | exclude from default inventory scope |
| `VEV_6500` | yes | partial | no | exclude from default inventory scope |

- Product-scope rationale:
  all 12 algorithmic products have full quote coverage in the `prices_*` files, but trade coverage is highly uneven. `VEV_4500`, `VEV_5000`, and `VEV_5100` are effectively quote-rich and trade-poor. `VEV_6000` and `VEV_6500` are quoted constantly but behave like floor products with constant `0.5` mids and zero trade notional.
- Product branches:
  `(1)` delta-1 base `HYDROGEL_PACK`, `(2)` underlying anchor `VELVETFRUIT_EXTRACT`, `(3)` ITM structural vouchers `VEV_4000/4500`, `(4)` active zone `VEV_5000-5300`, `(5)` upper/passive `VEV_5400/5500`, `(6)` floor/monitor `VEV_6000/6500`.

## Algorithmic vs Manual Scope

Separate findings usable inside `Trader.run()` from manual-challenge findings.

| Finding | Scope | Why | Caveat |
| --- | --- | --- | --- |
| Counterparty-aware trade analysis | algorithmic | `buyer` and `seller` are visible in the algorithmic trade files | only raw-data evidence so far, not strategy proof |
| Linked option-book structure and strike-role findings | algorithmic | quote and trade files cover the full `VEV_*` family | raw-data framing, not run-performance proof |
| Manual challenge work | manual | manual products still lack contract-level raw data in repo | Phase 01 keeps manual as factual placeholder only |

## Data Sources

- Raw data:
  - `../../data/raw/prices_round_4_day_1.csv`
  - `../../data/raw/prices_round_4_day_2.csv`
  - `../../data/raw/prices_round_4_day_3.csv`
  - `../../data/raw/trades_round_4_day_1.csv`
  - `../../data/raw/trades_round_4_day_2.csv`
  - `../../data/raw/trades_round_4_day_3.csv`
- Processed data:
  - `../../data/processed/derived_round_4_data_quality_by_file.csv`
  - `../../data/processed/derived_round_4_data_quality_by_product.csv`
  - `../../data/processed/derived_round_4_trade_summary_by_symbol.csv`
  - `../../data/processed/derived_round_4_trade_summary_by_symbol_day.csv`
  - `../../data/processed/derived_round_4_trade_alignment_summary.csv`
  - `../../data/processed/derived_round_4_counterparty_summary.csv`
  - `../../data/processed/derived_round_4_counterparty_product_mix.csv`
  - `../../data/processed/derived_round_4_counterparty_time_bucket.csv`
  - `../../data/processed/derived_round_4_counterparty_side_asymmetry.csv`
  - `../../data/processed/derived_round_4_counterparty_concentration.csv`
  - `../../data/processed/derived_round_4_counterparty_stability.csv`
  - `../../data/processed/derived_round_4_counterparty_stability_scores.csv`
  - `../../data/processed/derived_round_4_counterparty_markout_by_side.csv`
  - `../../data/processed/derived_round_4_counterparty_markout_by_symbol_side.csv`
  - `../../data/processed/derived_round_4_counterparty_pair_summary.csv`
  - `../../data/processed/derived_round_4_counterparty_book_context.csv`
  - `../../data/processed/derived_round_4_option_book_summary.csv`
  - `../../data/processed/derived_round_4_local_cross_strike_context.csv`
  - `../../data/processed/derived_round_4_same_time_return_corr.csv`
  - `../../data/processed/derived_round_4_same_time_return_covariance.csv`
  - `../../data/processed/derived_round_4_lead_lag_summary.csv`
  - `../../data/processed/derived_round_4_trade_feature_corr.csv`
  - `../../data/processed/derived_round_4_trade_feature_covariance.csv`
  - `../../data/processed/derived_round_4_counterparty_controlled_regression.csv`
  - `../../data/processed/derived_round_4_feature_model_comparison.csv`
  - `../../data/processed/derived_round_4_engineered_feature_summary.csv`
  - `../../data/processed/derived_round_4_candidate_online_features.csv`
  - `../../data/processed/derived_round_4_product_regime_summary.csv`
  - `../../data/processed/derived_round_4_counterparty_conditioned_summary.csv`
  - `../../data/processed/derived_round_4_family_conditioned_regime_summary.csv`
- External context: none
- Run or log artifact: none
- Post-run research memory: none for `round_4` yet
- Prior-round artifact reuse:
  - `../00_prior_round_intake.md`
  - `../../round_3/workspace/01_eda/eda_option_surface_and_microstructure.md`
  - `../../round_3/workspace/01_eda/eda_round_3_retrospective_carry_forward.md`
  - `../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`
  - `../../round_3/workspace/post_run_research_memory.md`

## Prior-Round Compatibility

- Source round: `round_3`
- Compatibility verdict: `compatible`
- What is being reused:
  product-role framing, option-book framing, anti-patterns, and open hypotheses
- What must be revalidated:
  any strategy-level conclusion that may change when counterparties become visible

## Round Adaptation Check

| Check | Current-Round Evidence | Decision / Action |
| --- | --- | --- |
| Active round mechanics/API | `../../../docs/prosperity_wiki/rounds/round_4.md` | `Trader.run()` unchanged; no new Trader method |
| Products and limits | `../00_ingestion.md` | verified; same algorithmic product universe as `round_3` |
| Data schema | raw `prices_*` and `trades_*` files | classified; semicolon-delimited with stable quote grid and separate trade files |
| New or changed fields/mechanics | Round 4 exposes `buyer` / `seller` participant names | this is the main Phase 01 EDA question |
| Prior-round assumption at risk | buyer/seller fields are irrelevant or unavailable | reject |
| Prior-round assumption at risk | voucher basket can be framed without counterparty context | revalidate |

## Artifact Index

| Artifact Path | Type | Source Data | Useful For | Decision-Relevant? |
| --- | --- | --- | --- | --- |
| [`analyze_round_4_eda.py`](analyze_round_4_eda.py) | script | all 6 raw CSVs | full EDA reproduction | yes |
| [`../../data/processed/derived_round_4_data_quality_by_product.csv`](../../data/processed/derived_round_4_data_quality_by_product.csv) | processed file | `prices_*` | product coverage, spread, depth, constant-mid caveats | yes |
| [`../../data/processed/derived_round_4_trade_summary_by_symbol.csv`](../../data/processed/derived_round_4_trade_summary_by_symbol.csv) | processed file | `trades_*` | activity by symbol | yes |
| [`../../data/processed/derived_round_4_trade_alignment_summary.csv`](../../data/processed/derived_round_4_trade_alignment_summary.csv) | processed file | `prices_*` + `trades_*` | short-horizon trade follow-through and execution texture | yes |
| [`../../data/processed/derived_round_4_counterparty_concentration.csv`](../../data/processed/derived_round_4_counterparty_concentration.csv) | processed file | `trades_*` | product-level concentration and dominance | yes |
| [`../../data/processed/derived_round_4_counterparty_stability.csv`](../../data/processed/derived_round_4_counterparty_stability.csv) | processed file | `trades_*` | cross-day stability of names | yes |
| [`../../data/processed/derived_round_4_counterparty_stability_scores.csv`](../../data/processed/derived_round_4_counterparty_stability_scores.csv) | processed file | `trades_*` | formal stability classes and role persistence | yes |
| [`../../data/processed/derived_round_4_counterparty_markout_by_side.csv`](../../data/processed/derived_round_4_counterparty_markout_by_side.csv) | processed file | `prices_*` + `trades_*` | side-aware markouts by counterparty | yes |
| [`../../data/processed/derived_round_4_counterparty_pair_summary.csv`](../../data/processed/derived_round_4_counterparty_pair_summary.csv) | processed file | `prices_*` + `trades_*` | recurring buyer-seller ecology | yes |
| [`../../data/processed/derived_round_4_counterparty_book_context.csv`](../../data/processed/derived_round_4_counterparty_book_context.csv) | processed file | `prices_*` + `trades_*` | trade-to-book context by counterparty and symbol | yes |
| [`../../data/processed/derived_round_4_option_book_summary.csv`](../../data/processed/derived_round_4_option_book_summary.csv) | processed file | `prices_*` + `trades_*` | strike activity, spread, depth, role review | yes |
| [`../../data/processed/derived_round_4_local_cross_strike_context.csv`](../../data/processed/derived_round_4_local_cross_strike_context.csv) | processed file | `prices_*` + `trades_*` | neighbor-strike context | yes |
| [`../../data/processed/derived_round_4_lead_lag_summary.csv`](../../data/processed/derived_round_4_lead_lag_summary.csv) | processed file | `prices_*` | anchor-voucher same-time vs lagged linkage | yes |
| [`../../data/processed/derived_round_4_counterparty_controlled_regression.csv`](../../data/processed/derived_round_4_counterparty_controlled_regression.csv) | processed file | trade-aligned sample | whether counterparty identity adds simple linear explanatory power | yes |
| [`../../data/processed/derived_round_4_feature_model_comparison.csv`](../../data/processed/derived_round_4_feature_model_comparison.csv) | processed file | trade-aligned sample | incremental value of engineered context features | yes |
| [`../../data/processed/derived_round_4_engineered_feature_summary.csv`](../../data/processed/derived_round_4_engineered_feature_summary.csv) | processed file | trade-aligned sample | mini-EDA on newly engineered usable features | yes |
| [`../../data/processed/derived_round_4_candidate_online_features.csv`](../../data/processed/derived_round_4_candidate_online_features.csv) | processed file | processed trade + concentration context | downstream feature shortlist | yes |
| [`artifacts/round_4_counterparty_product_mix_heatmap.png`](artifacts/round_4_counterparty_product_mix_heatmap.png) | plot | `trades_*` | quick counterparty specialization review | yes |
| [`artifacts/round_4_counterparty_markout_bar.png`](artifacts/round_4_counterparty_markout_bar.png) | plot | aligned trade sample | quick view of side-aware top-name markouts | yes |
| [`artifacts/round_4_return_corr_heatmap.png`](artifacts/round_4_return_corr_heatmap.png) | plot | `prices_*` | cross-product relationship review | yes |
| [`artifacts/round_4_relative_spread_boxplot.png`](artifacts/round_4_relative_spread_boxplot.png) | plot | `prices_*` | spread hierarchy by product | yes |
| [`artifacts/round_4_top_buyer_timing.png`](artifacts/round_4_top_buyer_timing.png) | plot | `trades_*` | timing balance by top buyer | yes |
| [`artifacts/round_4_eda_summary_metrics.json`](artifacts/round_4_eda_summary_metrics.json) | processed file | generated outputs | fast downstream lookup | yes |
| [`eda_round_4_counterparty_profiles.md`](eda_round_4_counterparty_profiles.md) | annex | `trades_*` + processed tables | deeper participant profiles | yes |
| [`eda_round_4_option_book_structure.md`](eda_round_4_option_book_structure.md) | annex | `prices_*` + `trades_*` + processed tables | deeper strike/book structure | yes |
| [`eda_round_4_round3_revalidation.md`](eda_round_4_round3_revalidation.md) | annex | Round 4 raw data + Round 3 carry-forward artifacts | compatibility-qualified revalidation | yes |

## Data Quality And Filters

- Row counts by file and product:
  - prices: `360000` rows total = `3` files x `120000` rows each
  - trades: `4281` rows total = `1407`, `1333`, `1541` by day
  - each algorithmic product appears in `30000` quote rows
- Timestamp coverage and gaps:
  - `prices_*` cover `0` through `999900` on a regular `100`-step grid
  - `trades_*` span the day but are event-driven and much sparser
- Missing bid/ask counts, if order books are used:
  - top-of-book is populated throughout
  - deeper levels are much sparser, so Phase 01 uses top-of-book features by default
- Zero or blank `mid_price` counts:
  - no blank or zero mids for live products
  - `VEV_6000` and `VEV_6500` are constant at `0.5`; this is not missingness, but it is a structural floor caveat
- Filters applied:
  - manual challenge excluded from quantitative EDA because no manual contract-level raw data exists
  - multivariate trade-feature layer uses trade-aligned rows with complete price alignment
- Findings based on:
  `raw rows` for schema and counts, `filtered rows` for aligned trade diagnostics, and `mixed` for carry-forward interpretation
- Data quality caveats:
  `VEV_4500`, `VEV_5000`, and `VEV_5100` have near-zero trade coverage, so any direct trade-tape conclusion for those symbols is weak even though quote coverage is full.

## Feature Inventory

| Feature | Origin | Online Usability | Meaning | Role | Signal Strength | Stability | Actionability | Lifecycle Decision | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| counterparty identity in `buyer` / `seller` | csv | usable online | named participant context is visible in trade data | direct signal / diagnostic | medium | day-stable for top names | changes strategy and validation framing | promote | use as context, not standalone alpha |
| counterparty concentration by symbol/side | combined | usable online | measures whether a product is dominated by a few names | direct signal / risk control | strong | stable across days for many vouchers | changes strategy and validation framing | promote | especially strong in upper/floor strikes |
| time bucket | csv | usable online | early / mid / late session state | execution filter / risk control | medium | stable as a structural partition | changes strategy and risk framing | promote | raw trade flow is balanced overall, but spread regimes differ |
| same-time `VEX`-voucher linkage | combined | usable online | underlying-anchor relationship for the option family | direct signal | strong | stable in quote data | changes strategy family choice | promote | lagged follow remains weak |
| top-of-book spread / relative spread | csv | usable online | execution quality and friction proxy | execution filter / risk control | strong | stable by role and strike | changes strategy and execution | promote | spreads explode in upper/floor strikes |
| top-of-book imbalance | csv | usable online | local book skew | direct signal / execution filter | weak-to-medium | product-dependent | exploratory | keep exploratory | strongest use may be conditional or counterparty-aware |
| product role | combined | usable online | strike / family structural class | direct signal / risk control | strong | stable by construction plus raw evidence | changes strategy framing | promote | should be a first-class EDA output |
| buyer / seller stability class | combined | usable online | distinguishes broad structural names from specialists | contextual filter / regime feature | medium | medium-high across 3 days | helps compress counterparties into reusable roles | promote cautiously | use role buckets before raw names |
| symbol-dominance flags | combined | usable online | whether the active buyer or seller is the dominant participant for that symbol-side | contextual filter / danger-state feature | medium | high in upper/floor and `5300` | useful for strike-specific state detection | promote cautiously | stronger as context than as standalone alpha |
| trade location bucket | combined | usable online | whether the print hits bid, ask, or lands inside spread | microstructure context | medium | high | useful feature-engineering primitive | promote | also materially improves the controlled model |
| buyer-seller pair recurrence | combined | usable online with historical memory | flags repeated counterparty loops | interaction context | weak-to-medium | unclear from only 3 days | plausible but not ready | exploratory | pair ecology is interesting but still sample-limited |
| trade-aligned future 5-step move | combined | EDA-only | short-horizon post-trade follow-through proxy | diagnostic | medium | product-dependent | changes validation and strategy framing | EDA-only calibration | do not turn into bot logic without careful proxy design |

## Product / Role Classification

| Product Or Scope | Role Class | Interaction Class | Why This Role Fits | Downstream Use | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | `delta-1 base` | `standalone usable` | liquid, tight spread, near-zero linkage to voucher family | separate delta-1 branch | raw data does not prove final strategy quality |
| `VELVETFRUIT_EXTRACT` | `anchor` | `standalone usable` | tightest major spread, strongest same-time linkage to active vouchers | anchor and context product | could still carry standalone alpha |
| `VEV_4000` | `ITM structural` | `usable only with anchor` | active trade tape, moderate spreads, strong `VEX` linkage | structural overlay candidate | still not proven as standalone engine |
| `VEV_4500` | `ITM structural` | `usable only with anchor` | quote-rich but trade-poor | low-confidence structural candidate | weak tape evidence |
| `VEV_5000` / `VEV_5100` | `active zone` | `unclear` | same-time `VEX` linkage remains strong, but trade tape is nearly absent | keep in structural framing only | do not over-read the sparse prints |
| `VEV_5200` | `active zone` | `mainly veto / anti-signal` candidate | concentrated, one-sided seller flow and negative short-horizon trade alignment | danger-state or contextual candidate | still raw-data framing, not run proof |
| `VEV_5300` | `active zone` | `usable only with anchor` / special-case candidate | meaningful trade activity but high concentration and negative short-horizon alignment | treat as special candidate, not generic basket leg | raw data does not prove it should be traded |
| `VEV_5400` / `VEV_5500` | `upper/passive` | `mainly veto / anti-signal` | spreads widen sharply and flow is dominated by `Mark 01` buys vs `Mark 22` sells | passive-only or signal-only by default | not enough evidence for normal aggressive inventory |
| `VEV_6000` / `VEV_6500` | `floor/monitor` | `too toxic as default inventory` | constant `0.5` mids, `20000` bps relative spread, zero notional | monitor only | dynamic alpha should be rejected until contradictory evidence appears |

## Feature Engineering Notes

Serious engineered features used in Phase 01:

- `spread`, `rel_spread_bps`, `depth_1`, `imbalance_1`
- `mid_delta_1`, `future_mid_delta_5`, `future_mid_return_bps_5`
- `time_bucket`
- `product_role`
- counterparty concentration metrics
- counterparty role buckets for top buyers / sellers

Important engineering choices:

- kept top-of-book features as default because deeper-book levels are too sparse for reliable general use
- extended trade-aligned diagnostics to `1`, `5`, and `10` steps so counterparty-conditioned follow-through is not horizon-blind
- turned raw name information into reusable role features: stability class, symbol-dominance flags, trade-location bucket, and recurrent-pair flags
- ran a mini EDA on those new features rather than only listing them as ideas; this is captured in `derived_round_4_engineered_feature_summary.csv` and `derived_round_4_feature_model_comparison.csv`
- kept buyer/seller identity buckets as a baseline comparison so we can measure whether engineered context adds more than just raw names

## Feature Promotion Decisions

| Feature Or Signal | Decision | Destination | Reason | Caveat / Reopen Condition |
| --- | --- | --- | --- | --- |
| counterparty concentration by symbol/side | promote to understanding | Signal Ledger | strongest new Round 4 raw-data finding | still context, not standalone edge |
| product role classification | promote to understanding | Signal Ledger | essential to keep option-book framing clean | needs strategy-specific use later |
| same-time `VEX` anchor linkage | promote to understanding | Signal Ledger | stable and strong across active vouchers | do not reinterpret as delayed-follow |
| raw imbalance as universal direct alpha | keep exploratory | none | weaker and more product-dependent than role, spread, and concentration | reopen only with better conditional evidence |
| direct dynamic alpha in `VEV_6000/6500` | reject | Negative Evidence | constant mids and zero notional invalidate it | reopen only if live data breaks the floor |
| pure counterparty identity as standalone linear predictor | negative evidence / exploratory | Negative Evidence | controlled regression with raw buyer/seller buckets only reaches `R^2 = 0.0101`; names alone are too weak | may still matter in interaction with product, side, and trade location |
| engineered counterparty/book context | promote to understanding | Signal Ledger | engineered context features lift the controlled model to `R^2 = 0.0183`, well above the raw-name model | still explanatory only and still sample-limited to 3 days |

## Multivariate Feature Map

| Feature Set / Scope | Target Or Relationship | Method | Result | Decision Impact | Caveat |
| --- | --- | --- | --- | --- | --- |
| same-time product returns | cross-product relation | correlation | `HYDRO` vs `VEX` is effectively zero (`0.0013`), while `VEX` vs `VEV_5000/5100/5200` remains strong (`0.7542`, `0.7600`, `0.7315`) | keep `HYDRO` separate, keep `VEX` as main voucher anchor | same-time linkage is not delayed predictiveness |
| active-zone neighbor returns | cross-strike relation | correlation | local cross-strike correlation decays from `0.8985` (`5000-5100`) to `0.1688` (`5400-5500`) | active zone is linked but not homogeneous | spread and trade quality diverge sharply even where returns correlate |
| trade-aligned feature set | future 5-step return | linear regression with counterparty buckets + spread + imbalance + time bucket + symbol | `R^2 = 0.0101`; counterparty coefficients are nonzero but weak as a simple linear signal | use raw names as contextual features only | in-sample explanatory model only |
| engineered context feature set | future 5-step return | linear regression with stability class, symbol-dominance flags, trade location, pair recurrence, plus base controls | `R^2 = 0.0183`; engineered context adds more than raw names alone | prefer compact engineered context over naked name logic | still explanatory only, not causal proof |
| trade-aligned numeric features | redundancy / overlap | correlation + covariance | spread, depth, imbalance, and trade quantity are not interchangeable | keep spread and role context distinct from raw imbalance | numeric-only view misses symbolic counterparty structure |

## Redundancy / Dimensionality Check

| Feature Family | Redundant Or Dominant Features | Evidence | Decision | Downstream Effect |
| --- | --- | --- | --- | --- |
| delta-1 anchor family | `VEX` linkage across active strikes | same-time correlations strongest in `5000-5200` and weaker as strikes move upper/floor | keep one anchor family | strategy should anchor vouchers to `VEX`, not to delayed-follow logic |
| execution-friction family | relative spread dominates many upper/floor distinctions | option-book summary and family regime summary | keep spread as first-class execution filter | upper/floor branches need stricter passivity or exclusion |
| counterparty structure family | concentration dominates identity details for many voucher strikes | concentration table shows top1 share `0.70+` in `5200`, `0.80+` in `5300`, and near `1.0` in upper/floor strikes | keep concentration and dominant-side features | raw name buckets alone are less important than role concentration |
| trade-to-book context family | trade location adds information beyond spread and time bucket | engineered feature model and grouped summaries separate at-bid from at-ask prints materially | keep trade-location as a reusable primitive | strongest as a contextual or defensive feature |
| sparse tape family | `VEV_4500/5000/5100` trade prints are too thin to support rich trade features | trade counts `3`, `3`, `3` | downgrade trade-tape conclusions for these strikes | use quote-led reasoning only unless more data appears |

## Cross-Product Relationships

| Product Pair / Scope | Check | Horizon / Alignment | Result | Decision | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` vs `VELVETFRUIT_EXTRACT` | correlation / covariance | same-time returns | effectively no linkage (`0.0013`) | separate | supports independent delta-1 branch |
| `VELVETFRUIT_EXTRACT` vs `VEV_4000` | correlation | same-time returns | moderate anchor linkage (`0.5806`) | use | supports ITM structural framing |
| `VELVETFRUIT_EXTRACT` vs `VEV_5000/5100/5200` | correlation | same-time returns | strongest family linkage (`0.7542`, `0.7600`, `0.7315`) | use | active zone remains the main anchor-linked cluster |
| `VELVETFRUIT_EXTRACT` vs `VEV_5300/5400/5500` | correlation | same-time returns | linkage weakens as strikes move up (`0.6169`, `0.4671`, `0.2492`) | use cautiously | supports role divergence by strike |
| `VELVETFRUIT_EXTRACT` vs vouchers | lead-lag | lags `1`, `2`, `5`, `10` | correlations collapse toward zero after lag `0` | reject delayed-follow | same as Round 3 framing |

## Retrospective EDA Decision

- Meaningful run evidence exists: `no` for `round_4`
- Retrospective run-informed EDA addendum needed: `no`
- Why:
  Phase 01 is still a raw-data EDA. `round_3` retrospective artifacts are reused as inputs, but `round_4` itself has no run history yet.
- Addendum artifact, if created:
  not needed yet

## Process / Distribution Hypotheses

| Product Or Scope | Hypothesized Process | Evidence | Confidence | Online Observables | Downstream Implication | Suggested Next Test | Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | liquid delta-1 process separate from option family | low spread (`15.7` bps), independent from `VEX`, balanced timing | medium-high | spread, depth, imbalance | keep separate branch in understanding | delta-1 EDA focused on counterparty-conditioned flow | promote | raw data does not prove best strategy family |
| `VELVETFRUIT_EXTRACT` | liquid anchor process with strongest structural link to active vouchers | lowest spread among major products (`9.5` bps), strongest same-time option linkage | high | mid, spread, imbalance, nearby voucher state | keep as option anchor and likely standalone branch | check whether specific counterparties change the anchor quality | promote | anchor role is stronger than any delayed-follow story |
| ITM vouchers | structural overlay with moderate liquidity and real trade tape in `4000` only | `VEV_4000` active, `VEV_4500` sparse, both retain meaningful same-time `VEX` linkage | medium | `VEX` mid + strike role + spread | use as structural rather than generic active cluster | quote-led residual framing | promote | `4500` tape is too thin for confidence |
| active zone `5000-5300` | linked option cluster with diverging execution texture | same-time cross-strike and `VEX` linkage remain strong, but spreads and trade concentration diverge sharply | high | spread, concentration, neighbor strikes, `VEX` | role-aware treatment, not homogeneous basket | strategy should separate `5000/5100`, `5200`, and `5300` logic | promote | trade evidence for `5000/5100` is weak |
| upper/passive `5400/5500` | thin, highly concentrated upper regime with worsening friction later in the day | very high spreads, strong `Mark 01` buyer vs `Mark 22` seller dominance, negative short-horizon trade alignment | medium-high | spread, counterparty dominance, time bucket | passive-only or signal-only by default | validate whether any counterparty-aware passive edge exists | defensive only | do not infer direct inventory edge from raw prints |
| floor `6000/6500` | floor / monitor process, not dynamic tradable series | constant `0.5` mids, `20000` bps spread, zero notional | high | constant floor behavior | exclude from direct trading logic | reopen only if later runs contradict floor behavior | reject | useful only as monitor or state marker if at all |

## Multivariate Model Notes

| Model / Check | Response | Predictors / Controls | Data Slice | Result | Leakage / Overfit Check | Actionability |
| --- | --- | --- | --- | --- | --- | --- |
| linear regression ladder | future 5-step return in bps after a trade | baseline microstructure controls, then raw buyer/seller buckets, then engineered context features | aligned trade rows with complete price context | baseline `R^2 = 0.0076`, raw names `0.0101`, engineered context `0.0183` | explanatory only, in-sample only | use this as evidence to prefer engineered context over naked names |

## Analyses Run

- Reproduction notes:
  `python3 rounds/round_4/workspace/01_eda/analyze_round_4_eda.py`
- Research tools used and why:
  - `pandas` / `numpy` for joins, grouping, role summaries, and aligned trade metrics
  - `sklearn` for one lightweight explanatory regression
  - `matplotlib` / `seaborn` for quick review plots
- Research tools considered but skipped:
  - clustering: not necessary yet because role concentration is already obvious from direct tables
  - mutual information / PCA: lower ROI than the direct concentration and linkage evidence
  - change-point tooling: not yet needed because current decisions are already clear without it
- Output artifacts:
  processed CSVs under `../../data/processed/` and plots under `artifacts/`
- Optional notebook:
  none

| Analysis | Status | Reason / Decision Impact | Artifact |
| --- | --- | --- | --- |
| schema + quality checks | run | mandatory base truth | `derived_round_4_data_quality_by_file.csv`, `derived_round_4_data_quality_by_product.csv` |
| trade activity summary | run | required for symbol importance and scope | `derived_round_4_trade_summary_by_symbol.csv` |
| counterparty concentration | run | main new Round 4 edge surface | `derived_round_4_counterparty_concentration.csv` |
| counterparty stability | run | needed to judge signal vs noise | `derived_round_4_counterparty_stability.csv` |
| counterparty stability scoring | run | compress names into reusable role classes | `derived_round_4_counterparty_stability_scores.csv` |
| product mix by counterparty | run | specialization analysis | `derived_round_4_counterparty_product_mix.csv` |
| side-aware counterparty markouts | run | check whether names matter more as buyer/seller contexts than as raw frequency | `derived_round_4_counterparty_markout_by_side.csv` |
| buyer-seller pair ecology | run | detect recurring loops and pair-conditioned follow-through | `derived_round_4_counterparty_pair_summary.csv` |
| trade-to-book context by counterparty | run | connect counterparties to spreads, depth, and trade location | `derived_round_4_counterparty_book_context.csv` |
| option-book summary | run | strike-role and friction mapping | `derived_round_4_option_book_summary.csv` |
| same-time cross-product relationships | run | anchor / separation decision | `derived_round_4_same_time_return_corr.csv` |
| lead-lag checks | run | delayed-follow rejection or support | `derived_round_4_lead_lag_summary.csv` |
| trade-aligned short-horizon diagnostics | run | contextual markout-like framing | `derived_round_4_trade_alignment_summary.csv` |
| controlled model | run | does counterparty identity add simple information? | `derived_round_4_counterparty_controlled_regression.csv` |
| engineered-feature mini EDA | run | test whether new usable features add signal or only description | `derived_round_4_engineered_feature_summary.csv`, `derived_round_4_feature_model_comparison.csv`, `derived_round_4_candidate_online_features.csv` |
| optional clustering / PCA / MI | skipped | low ROI relative to already-strong direct findings | none |

## Facts

- Round 4 exposes named counterparties in `Trade.buyer` and `Trade.seller`.
- All 12 algorithmic products have full quote coverage in the uploaded price files.
- The option family still has concrete `VEV_*` symbols rather than one generic tradable voucher symbol in the raw files.

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| upper/floor voucher regime | spread, counterparty concentration, trade alignment | very high friction and highly concentrated flow | use defensively or avoid as default inventory | strong | still raw-data framing only |
| active-zone middle regime | `VEX` linkage, local cross-strike correlation, concentration | structurally linked but execution texture diverges sharply by strike | do not treat as homogeneous basket | strong | `5000/5100` tape is sparse |
| time bucket regime in upper strikes | relative spread by bucket | upper spreads worsen from early to mid/late | supports timing-aware passivity or no-trade | medium | trade counts themselves are not late-skewed overall |
| overall counterparty timing | top buyer / seller counts by bucket | major names are active across the whole day, not only in one late window | weakens universal late-only story | medium | does not rule out product-specific late toxicity |
| seller-dominant voucher regime | seller dominance, side-aware markouts, pair ecology | `Mark 22` seller flow in `5200+` aligns with favorable seller-side markouts and recurring pair loops | supports danger-state / veto framing | medium-high | still not a license for direct name-based aggression |

## Linked-Product / Book Framing Notes

- Are products best treated as standalone symbols or a linked book:
  `HYDRO` should stay separate; `VEX` plus vouchers should be treated as a linked option book.
- Products that look better as signal than inventory:
  `VEV_5200`, `VEV_5400`, `VEV_5500`, `VEV_6000`, and `VEV_6500`
- Cross-product or cross-strike context that changes decisions:
  `VEX` linkage is strongest in `5000-5200`; neighbor-strike correlation and trade concentration diverge sharply from `5200` upward.
- Family-level exposure concerns:
  raw concentration is family-shaped, not symbol-independent; upper/floor trades look like a small number of recurring counterparty loops.
- Natural hold horizon differences across products or setups:
  raw data does not prove final hold horizons, but short-horizon trade alignment is already materially worse in `5200+` than in `VEX` or `4000`.

## Threshold / Execution Findings

| Finding | Feature Basis | Threshold Or Zone | Execution / Risk Use | Readiness | Caveat |
| --- | --- | --- | --- | --- | --- |
| upper strike friction explosion | relative spread by strike | `VEV_5400+` | passive-only or avoid by default | usable | raw EDA only |
| floor-product exclusion | constant mids + `20000` bps spread + zero notional | `VEV_6000/6500` | exclude from default inventory | usable | reopen only if later evidence contradicts |
| sparse active tape | trade counts by symbol | `VEV_4500/5000/5100` | avoid direct tape-based alpha claims | usable | quote-led analysis may still matter |
| concentrated seller dominance | counterparty concentration | `VEV_5200+` seller side | treat with caution as potential danger-state context | exploratory | needs strategy-phase translation |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| counterparty specialization context | counterparty concentration, side asymmetry, product mix, stability | a small set of `Mark` names repeatedly occupy distinct product/side roles | new Round 4 information may be strategy-relevant | contextual filter / regime feature | stable across 3 days for top names | strong as context, weak as standalone alpha | do not use as a naked name-based trigger |
| side-aware voucher seller pressure | seller-side markouts, dominance flags, pair ecology, strike concentration | repeated `Mark 22` seller flow in `5200+` aligns with favorable seller-side follow-through | strongest new counterparty-conditioned danger-state story | contextual veto / defensive regime feature | stable at raw-data level in `5200+` | medium-high | still not enough to justify direct name-only trading logic |
| trade-to-book location context | trade location bucket, spread, depth | at-bid / at-ask / inside-spread prints separate trade follow-through better than raw names alone | helps bridge counterparties with microstructure | feature-engineering primitive | stable by construction | medium | use as a reusable building block, not as standalone trigger |
| `VEX` same-time anchor still dominates voucher linkage | same-time corr + lead-lag rejection | vouchers still move with `VEX` mainly at lag `0`, not with delayed follow | preserves the core anchor framing from `round_3` | anchor / valuation context | stable | strong | not a claim about final trading style |
| active voucher family is structurally linked but execution-fragmented | local cross-strike corr, spreads, trade counts, concentration | `5000-5300` is one family structurally, but not one clean trading basket | supports strike-specific logic and danger-state use | role-aware option-book logic | stable at raw-data level | strong | sparse `5000/5100` tape limits direct claims |

## Downstream Feature Contract Implications

| Feature Or Relationship | Contract Implication | Online Proxy Needed? | Validation / Invalidation Check | Do Not Use Until |
| --- | --- | --- | --- | --- |
| counterparty concentration / identity | if used, must be framed as contextual state, not naked primary alpha | no | check stability and product specificity in validation | until understanding compresses which names and roles matter |
| `VEX` anchor relationship | later specs may anchor voucher logic to `VEX` same-time state | no | invalidate if later runs show no benefit over standalone voucher logic | until strategy chooses the exact residual logic |
| upper/floor exclusion | later specs should default these to monitor/passive/avoid states | no | reopen only if validation or richer data contradicts raw EDA | until contradictory evidence appears |
| sparse-tape strikes `4500/5000/5100` | avoid tape-based claims and use quote-led framing only | no | invalidate if later data adds meaningful trade coverage | until more evidence exists |

## Negative Evidence

| Idea Or Signal | Why It Was Plausible | Evidence Against It | When To Reopen |
| --- | --- | --- | --- |
| delayed `VEX`-follow option logic | `VEX` and vouchers are strongly linked | lagged correlations collapse toward zero after lag `0` | only if later execution or run evidence reveals a latency effect |
| `HYDRO` as option-family proxy | both are major algorithmic products | same-time return corr vs `VEX` is only `0.0013` | only if later strategy evidence shows cross-product utility |
| upper/floor vouchers as normal direct inventory | all vouchers have full quote coverage | spreads explode and flow is nearly deterministic by counterparty | only if later validation proves a passive edge |
| pure name-based linear alpha | named counterparties are the new feature | controlled model `R^2 = 0.0101` is too weak alone | only if interaction features with side/product materially strengthen it |
| buyer-seller pair recurrence as ready-made alpha | repeated pairs can look very structured | recurrent pairs are interesting, but the strongest ones are mostly explained by strike concentration and only 3 days of sample | only if later runs or more data show stable incremental value over concentration and product-role context |
| universal late-session deterioration from raw trade timing | Round 3 made this plausible | top counterparties are active across all three session buckets | reopen only at product-specific or run-specific level |

## Assumptions

- Counterparty names in the sample files are representative enough to study Phase 01 framing.
- Three days of raw data are sufficient to classify strong structural patterns, but not to prove final strategy quality.

## Open Questions

- Do specific counterparty combinations produce stable enough conditional markouts to justify strategy-level use?
- Is `VEV_5200` a true danger-state indicator or just a sparse-sample artifact?
- Does `5300` stay special once later validation includes real run behavior rather than raw tape alone?
- How much of the visible counterparty structure is exploitable versus only useful for avoiding bad states?

## Signal Strength And Uncertainty

- Strength: `strong`
- Evidence:
  raw counterparty specialization, role divergence across strikes, and same-time anchor relationships are all clearly visible
- Uncertainty:
  the new information is strong as framing/context, but much weaker as direct standalone predictive alpha at Phase 01 stage

## Downstream Use / Agent Notes

- Strong enough to consider:
  counterparty specialization as contextual state, `VEX` as anchor, strike-role framing, upper/floor exclusion by default
- Exploratory only:
  pure counterparty alpha, `5200` as danger-state trigger, exact use of `5300`
- Do not use yet:
  delayed-follow logic, pure name-based linear signals, upper/floor direct aggression
- Additional validation needed:
  participant-conditioned markouts, counterparty-aware strategy tests, and real run evidence
- How understanding should use this:
  compress the market into `delta-1 base`, `anchor`, `ITM structural`, `active zone`, `upper/passive`, `floor/monitor`, and explicitly separate strong context from direct alpha
- How strategy generation should use this:
  treat counterparties as contextual candidates, not as proof of a ready-made strategy; keep `round_3` anti-patterns alive unless `round_4` evidence clearly beats them
- How specification should use this:
  any buyer/seller use must be explicit in the Feature Contract, with a stability caveat
- How implementation should use this:
  keep counterparty logic lightweight and defensively gated if it appears at all
- How testing/debugging should use this:
  check whether branches work better as signal-only reuse than as full inventory logic

## Reusable Metrics

- total price rows: `360000`
- total trade rows: `4281`
- controlled model ladder:
  baseline `R^2 = 0.0076`
  raw-name model `R^2 = 0.0101`
  engineered-context model `R^2 = 0.0183`
- top buyer counts:
  `Mark 01 = 1599`, `Mark 14 = 1127`, `Mark 38 = 733`, `Mark 55 = 598`
- top seller counts:
  `Mark 22 = 1542`, `Mark 14 = 1045`, `Mark 38 = 745`, `Mark 55 = 600`
- top side-aware markouts:
  `Mark 22` seller `+20.48` bps at `5` steps
  `Mark 67` buyer `+3.71` bps at `5` steps
  `Mark 49` seller `-3.47` bps seller-aligned
- same-time `VEX` correlations:
  `VEV_4000 = 0.5806`, `VEV_5000 = 0.7542`, `VEV_5100 = 0.7600`, `VEV_5200 = 0.7315`, `VEV_5300 = 0.6169`, `VEV_5400 = 0.4671`, `VEV_5500 = 0.2492`
- upper/floor concentration:
  `VEV_5400` buyer top1 share `0.9529`, seller top1 share `1.0000`
  `VEV_5500` buyer top1 share `0.9771`, seller top1 share `1.0000`
  `VEV_6000` and `VEV_6500` buyer top1 share `1.0000`, seller top1 share `1.0000`
