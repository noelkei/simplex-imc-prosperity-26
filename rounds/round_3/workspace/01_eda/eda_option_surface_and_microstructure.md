# Round 3 EDA - Option Surface And Microstructure

## Status

`READY_FOR_REVIEW`

## Question

- Question: What does the Round 3 sample data say about delta-1 microstructure, voucher surface structure, underlying-voucher linkage, and high-ROI signals or exclusions for later strategy work?
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Why this matters downstream: Round 3 is the first option-heavy round. Strategy/spec work needs to know which vouchers behave like real signal carriers, which are mostly structural anchors or floor instruments, whether the underlying leads the vouchers in a tradable way, and whether the cleanest edge is directional, relative-value, or execution-filter based.

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | yes | yes | likely | include |
| `VELVETFRUIT_EXTRACT` | yes | yes | likely | include |
| `VEV_4000` | yes | yes | likely | include |
| `VEV_4500` | yes | partial | possible | investigate |
| `VEV_5000` | yes | yes | likely | include |
| `VEV_5100` | yes | yes | likely | include |
| `VEV_5200` | yes | yes | likely | include |
| `VEV_5300` | yes | yes | likely | include |
| `VEV_5400` | yes | yes | possible | investigate |
| `VEV_5500` | yes | partial | possible | investigate |
| `VEV_6000` | yes | partial | no | exclude |
| `VEV_6500` | yes | partial | no | exclude |

- Product-scope rationale: all 12 algorithmic symbols appear in raw price data, but they do not deserve equal downstream attention. `VEV_6000` and `VEV_6500` are effectively constant tick-floor instruments in sample data. `VEV_4500`, `VEV_5000`, and `VEV_5100` have full quote history but sparse printed trades, so later strategy/spec work should treat their trade-tape evidence as limited even though their book evidence is usable. `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are clearly liquid delta-1 products and should be modeled separately from the voucher family.
- Product branches, if any: branch the round into `(1)` `HYDROGEL_PACK` delta-1 microstructure, `(2)` `VELVETFRUIT_EXTRACT` as option anchor underlying, `(3)` active voucher surface `VEV_4000` through `VEV_5500`, and `(4)` deep OTM floor vouchers `VEV_6000` / `VEV_6500`.

## Algorithmic vs Manual Scope

Separate findings usable inside `Trader.run()` from manual-challenge findings.

| Finding | Scope | Why | Caveat |
| --- | --- | --- | --- |
| Orderable option symbols should be treated as concrete `VEV_*` products | algorithmic | Orders are sent by product symbol, and raw Round 3 data enumerates only concrete `VEV_*` symbols | The round page still names `VELVETFRUIT_EXTRACT_VOUCHER` as a family label |
| Voucher surface, moneyness, intrinsic/extrinsic, spread, and imbalance findings | algorithmic | These all come from quote/trade artifacts available to later strategy/spec work | Sample data observations are not official rules |
| Two-bid Bio-Pod challenge and below-mean second-bid penalty formula | manual | This lives outside `Trader.run()` and should not contaminate bot logic | Exact fill-probability wording remains ambiguous in the source |
| Manual challenge symbol handling | manual | No manual symbol is exposed in the official Round 3 page or raw CSVs | Keep manual docs separate from bot assumptions |

## Data Sources

- Raw data:
  - `../../data/raw/prices_round_3_day_0.csv`
  - `../../data/raw/prices_round_3_day_1.csv`
  - `../../data/raw/prices_round_3_day_2.csv`
  - `../../data/raw/trades_round_3_day_0.csv`
  - `../../data/raw/trades_round_3_day_1.csv`
  - `../../data/raw/trades_round_3_day_2.csv`
- Processed data:
  - `../../data/processed/derived_round_3_data_quality_by_file.csv`
  - `../../data/processed/derived_round_3_data_quality_by_product.csv`
  - `../../data/processed/derived_round_3_trade_summary_by_symbol.csv`
  - `../../data/processed/derived_round_3_trade_alignment_summary.csv`
  - `../../data/processed/derived_round_3_option_surface_summary.csv`
  - `../../data/processed/derived_round_3_option_extrinsic_by_tte.csv`
  - `../../data/processed/derived_round_3_same_time_return_corr.csv`
  - `../../data/processed/derived_round_3_same_time_return_covariance.csv`
  - `../../data/processed/derived_round_3_underlying_option_lead_lag.csv`
  - `../../data/processed/derived_round_3_product_signal_metrics.csv`
  - `../../data/processed/derived_round_3_option_reversion_metrics.csv`
  - `../../data/processed/derived_round_3_pooled_option_linear_model.csv`
  - `../../data/processed/derived_round_3_option_mutual_information.csv`
  - `../../data/processed/derived_round_3_option_feature_corr.csv`
  - `../../data/processed/derived_round_3_option_feature_covariance.csv`
  - `../../data/processed/derived_round_3_option_pca_loadings.csv`
  - `../../data/processed/derived_round_3_option_pca_explained_variance.csv`
- External context: none
- Run or log artifact: none
- Post-run research memory: none present

## Round Adaptation Check

Use this once per EDA artifact to prevent hidden prior-round assumptions.

| Check | Current-Round Evidence | Decision / Action |
| --- | --- | --- |
| Active round mechanics/API | `../../../docs/prosperity_wiki/rounds/round_3.md`, `../../../docs/prosperity_wiki/api/01_trader_contract.md` | Use `Trader.run(state)` only; no Round-3-specific `bid()` mechanic |
| Products and limits | `../../../docs/prosperity_wiki/rounds/round_3.md`, `../00_ingestion.md` | Verified; use concrete `VEV_*` symbols and 300 limit per voucher symbol |
| Data schema | raw Round 3 price/trade CSVs | Classified; semicolon-delimited with stable timestamp grid and 12-symbol coverage in price files |
| New or changed fields/mechanics | voucher strike family, TTE mapping, manual two-bid challenge | Use for EDA question and later Round-Specific Mechanics Contract; exclude manual mechanics from bot logic |
| Prior-round assumption at risk | delta-1-only framing | Reject; Round 3 needs option-aware EDA and surface-aware strategy framing |
| Prior-round assumption at risk | generic voucher symbol is directly tradable | Revalidate; use concrete `VEV_*` symbols as working bot assumption |
| Prior-round assumption at risk | all options are equally tradable / informative | Reject; sample evidence supports excluding `VEV_6000` and `VEV_6500` initially |

## Artifact Index

Persist reusable artifacts under existing round-local paths and link them here.

| Artifact Path | Type | Source Data | Useful For | Decision-Relevant? |
| --- | --- | --- | --- | --- |
| [`analyze_round_3_eda.py`](analyze_round_3_eda.py) | script | all six raw CSVs | full EDA reproduction | yes |
| [`../../data/processed/derived_round_3_data_quality_by_product.csv`](../../data/processed/derived_round_3_data_quality_by_product.csv) | processed file | price CSVs | product coverage, spread/depth comparison | yes |
| [`../../data/processed/derived_round_3_trade_alignment_summary.csv`](../../data/processed/derived_round_3_trade_alignment_summary.csv) | processed file | price + trade CSVs | execution diagnostics | yes |
| [`../../data/processed/derived_round_3_option_surface_summary.csv`](../../data/processed/derived_round_3_option_surface_summary.csv) | processed file | price CSVs | monotonicity/convexity checks | yes |
| [`../../data/processed/derived_round_3_option_extrinsic_by_tte.csv`](../../data/processed/derived_round_3_option_extrinsic_by_tte.csv) | processed file | price CSVs | strike/TTE surface and theta-like decay | yes |
| [`../../data/processed/derived_round_3_same_time_return_corr.csv`](../../data/processed/derived_round_3_same_time_return_corr.csv) | processed file | price CSVs | cross-product correlation and redundancy | yes |
| [`../../data/processed/derived_round_3_same_time_return_covariance.csv`](../../data/processed/derived_round_3_same_time_return_covariance.csv) | processed file | price CSVs | scale-sensitive product interaction | yes |
| [`../../data/processed/derived_round_3_underlying_option_lead_lag.csv`](../../data/processed/derived_round_3_underlying_option_lead_lag.csv) | processed file | price CSVs | delayed-follow viability check | yes |
| [`../../data/processed/derived_round_3_product_signal_metrics.csv`](../../data/processed/derived_round_3_product_signal_metrics.csv) | processed file | price CSVs | per-product process and signal metrics | yes |
| [`../../data/processed/derived_round_3_option_reversion_metrics.csv`](../../data/processed/derived_round_3_option_reversion_metrics.csv) | processed file | price CSVs | extrinsic mean-reversion evidence | yes |
| [`../../data/processed/derived_round_3_pooled_option_linear_model.csv`](../../data/processed/derived_round_3_pooled_option_linear_model.csv) | processed file | price CSVs | explanatory pooled option model | yes |
| [`../../data/processed/derived_round_3_option_mutual_information.csv`](../../data/processed/derived_round_3_option_mutual_information.csv) | processed file | price CSVs | nonlinear feature ranking | yes |
| [`../../data/processed/derived_round_3_option_feature_corr.csv`](../../data/processed/derived_round_3_option_feature_corr.csv) | processed file | price CSVs | feature redundancy analysis | yes |
| [`../../data/processed/derived_round_3_option_feature_covariance.csv`](../../data/processed/derived_round_3_option_feature_covariance.csv) | processed file | price CSVs | magnitude-sensitive feature overlap | yes |
| [`../../data/processed/derived_round_3_option_pca_loadings.csv`](../../data/processed/derived_round_3_option_pca_loadings.csv) | processed file | price CSVs | dimensionality check | yes |
| [`artifacts/round_3_option_extrinsic_by_tte.png`](artifacts/round_3_option_extrinsic_by_tte.png) | plot | price CSVs | TTE / strike surface review | yes |
| [`artifacts/round_3_return_corr_heatmap.png`](artifacts/round_3_return_corr_heatmap.png) | plot | price CSVs | quick cross-product relationship review | yes |
| [`artifacts/round_3_imbalance_signal_bins.png`](artifacts/round_3_imbalance_signal_bins.png) | plot | price CSVs | directional value of order-book imbalance | yes |
| [`artifacts/round_3_extrinsic_reversion_bins.png`](artifacts/round_3_extrinsic_reversion_bins.png) | plot | price CSVs | option residual mean-reversion review | yes |
| [`artifacts/round_3_relative_spread_boxplot.png`](artifacts/round_3_relative_spread_boxplot.png) | plot | price CSVs | execution filter calibration | yes |
| [`artifacts/round_3_eda_summary_metrics.json`](artifacts/round_3_eda_summary_metrics.json) | processed file | all generated metrics | fast downstream lookup | yes |

## Data Quality And Filters

- Row counts by file and product:
  - prices: `360000` rows total = `3` files x `120000` rows each
  - trades: `4048` rows total = `1309`, `1408`, `1334` rows by day
  - each algorithmic product appears in `30000` price rows
- Timestamp coverage and gaps:
  - price files cover `0` through `999900`
  - timestamps are perfectly regular at `100`-step intervals in every price file
  - trade timestamps start later inside the day (`2500`, `4500`, `900`) but span almost the full sample day
- Missing bid/ask counts, if order books are used:
  - best level is populated throughout the price data
  - level 2 and especially level 3 are sparse for many vouchers
  - level-2 missingness rises from `0%` in `VEV_4000` / `VEV_4500` to `100%` in `VEV_6000` / `VEV_6500`
  - level-3 depth is mostly absent even in liquid products, so this EDA uses top-of-book features by default
- Zero or blank `mid_price` counts, if mid prices are used:
  - zero `mid_price` count: `0`
  - `VEV_6000` and `VEV_6500` are constant at `0.5`, which is not missing data but does create constant-series caveats
- Filters applied:
  - manual challenge excluded from quantitative EDA because no manual columns exist in raw files
  - pooled option regression limited to `VEV_5000` through `VEV_5500`
  - PCA/loadings exclude `VEV_6000` and `VEV_6500` because they are constant-floor instruments
  - trade-alignment checks use raw joined rows at exact `(day, timestamp, symbol)` matches
- Findings based on: `mixed, explain`
  - raw rows for quality, spread, depth, trade alignment, and surface checks
  - filtered rows for pooled option model, PCA, and selected plots
- Data quality caveats:
  - raw trade counts are very uneven across vouchers; trade-tape evidence is especially weak for `VEV_4500`, `VEV_5000`, and `VEV_5100`
  - historical data covers TTE `8d`, `7d`, and `6d`, while the final Round 3 day is `5d`; later strategy work must extrapolate one day of option decay
  - constant `VEV_6000` / `VEV_6500` series produce `NaN` correlation entries by construction

## Feature Inventory

Use [`docs/prosperity_workflows/11_dataset_eda_framework.md`](../../../docs/prosperity_workflows/11_dataset_eda_framework.md) as the checklist.

Include raw features and derived features created during EDA. Keep this compact; detail only features that could change a downstream decision.

Feature lifecycle states:

- `observed`: appears in CSV, `TradingState`, logs, manual mechanics, or a combined analysis.
- `classified`: origin, online usability, and role are known.
- `evaluated`: signal strength, stability, and actionability are checked.
- `promoted`: should enter Understanding / strategy as a signal.
- `rejected`: meaningful negative evidence exists.
- `specified`: exact bot use belongs in a reviewed strategy spec.
- `implemented`: present in a bot and validated through runs.

Origins: `csv | online | log/post-run | combined | manual-only`.
Online usability: `usable online | EDA-only | log-only | unknown`.
Roles: `direct signal | execution filter | risk control | diagnostic | manual | avoid`.

| Feature | Origin | Online Usability | Meaning | Role | Signal Strength | Stability | Actionability | Lifecycle Decision | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `imbalance_1` | csv | usable online | top-of-book volume skew | direct signal / execution filter | medium | stable across many products, stronger in some vouchers | changes strategy and parameters | promote | positive correlation with future 5-step delta for delta-1 products and several vouchers |
| `rel_spread_bps` | csv | usable online | execution cost proxy normalized by price | execution filter / risk control | strong | highly stable by product/strike family | changes execution and product scope | promote | widens sharply as strikes move OTM; `VEV_6000` / `VEV_6500` sit at `20000` bps |
| `underlying_delta_1` | combined | usable online | contemporaneous `VELVETFRUIT_EXTRACT` move | diagnostic / calibration | strong same-time, weak predictive | stable same-time, not lag-stable | changes what not to build | negative evidence / EDA-only calibration | useful for mapping voucher family, not as delayed-follow alpha |
| `moneyness` | combined | usable online | `underlying_mid - strike` | direct signal / classification | strong | stable and structurally meaningful | changes strategy family and grouping | promote | needed to compare vouchers on a common scale |
| `intrinsic_value` | combined | usable online | call-like intrinsic component | diagnostic / direct signal | strong | stable | changes valuation framework | promote | deep ITM vouchers are almost pure intrinsic in sample |
| `extrinsic_value` | combined | usable online | time value beyond intrinsic | direct signal / calibration | strong | day- and strike-sensitive | changes strategy and validation | promote | decays with TTE for active strikes |
| `extrinsic_dev_day` | combined | usable online | deviation from day/product average extrinsic | direct signal | medium | strongest in ITM and near-ATM region | changes strategy and validation | promote | mean reversion strongest in `VEV_4000` / `VEV_4500`, weaker farther OTM |
| `surface_shape_checks` | combined | EDA-only | monotonicity and convexity of voucher mids across strike | diagnostic / avoid | strong | extremely stable across all three sample days | changes validation and cross-strike logic | promote | almost perfect monotone/convex surface; use as structural sanity check |

## Feature Engineering Notes

Target simple, hypothesis-driven transformations before complex ones. Do not document brute-force feature explosion.

Evaluate each serious feature against:

- Signal gate: does it predict, explain, or classify something useful?
- Stability gate: does it persist across days, timestamps, products, or regimes?
- Actionability gate: would it change strategy, parameters, risk, validation, or debugging?

Feature explosion controls:

- Max 5-8 serious feature candidates in this artifact unless explicitly justified.
- Max 1-3 promoted signal hypotheses.
- Do not document every failed transform; preserve only decision-relevant negative evidence.

| Transformation Or Feature | Purpose | Gate Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| `spread`, `rel_spread_bps`, `depth_1`, `imbalance_1` | quantify microstructure and execution cost | strong signal gate for imbalance; strong actionability gate for spreads | yes | validate on replay / live logs whether fill quality tracks spread and imbalance as expected |
| `strike`, `tte_days`, `moneyness` | compare vouchers on a common option-aware axis | strong signal/stability/actionability gates | yes | carry into understanding/spec as mandatory classification features |
| `intrinsic_value`, `extrinsic_value` | separate structural call value from residual/time value | strong signal and actionability gates | yes | validate whether later bot logic should trade total price, residual, or both |
| `extrinsic_dev_day` | isolate relative mispricing around each voucher's day-level extrinsic baseline | medium-to-strong signal gate, strongest in ITM / near-ATM vouchers | yes | validate with later markout/replay before strategy commits |
| same-time return correlations | decide whether products interact or should be modeled separately | strong actionability gate | yes | carry into product scope and hedge/reject decisions |
| lead-lag horizons `(1, 2, 5, 10)` | test delayed-follow intuition from underlying to vouchers | failed predictive gate; useful negative evidence | no as alpha | keep as rejection evidence in later strategy work |
| pooled option linear model | test whether simple controls survive together for future voucher delta | low R^2, but imbalance survives better than underlying delta | maybe | use as weak directional evidence only, not standalone signal |
| PCA/loadings and MI | reduce feature overlap and detect nonlinear importance | high redundancy signal for price/intrinsic/moneyness; imbalance isolated; extrinsic nonlinear importance survives | yes | use to keep later specs feature-light |

## Feature Promotion Decisions

Promote only features that change a concrete downstream decision. EDA-only features may support reasoning, but must not enter bot specs unless an online proxy exists.

| Feature Or Signal | Decision | Destination | Reason | Caveat / Reopen Condition |
| --- | --- | --- | --- | --- |
| `imbalance_1` across delta-1 and active vouchers | promote to understanding | understanding / strategy | consistent positive relation to short-horizon future mid delta | later validation should confirm fill-adjusted edge survives costs |
| voucher `intrinsic_value` + `extrinsic_value` decomposition | promote to understanding | understanding / strategy / spec | option family is cleaner when decomposed into structural intrinsic plus residual/time value | relies on call-option interpretation from round text |
| `extrinsic_dev_day` mean reversion in ITM / near-ATM vouchers | promote to understanding | understanding / strategy | strongest option-specific tradable pattern found in this EDA | weaker and noisier farther OTM |
| `surface_shape_checks` | promote to understanding | understanding / validation | structural cross-strike consistency is strong enough to become a sanity framework | this is calibration/validation evidence, not direct alpha |
| same-time underlying delta -> voucher delta relationship | EDA-only calibration | understanding / spec | helps define valuation anchor and grouping by moneyness | no delayed predictive edge found |
| delayed underlying-follow signal | reject | none | lagged correlations collapse toward zero immediately after lag 0 | reopen only if run/log data shows latency or fill frictions create a delay not visible in sample |
| `VEV_6000` / `VEV_6500` dynamic alpha | reject | none | constant `0.5` mids and no return variance make them poor signal carriers in sample | reopen only if final-day books/logs show floor break or non-constant behavior |

## Multivariate Feature Map

Run this on the serious engineered feature set, not every raw column. Mark
skipped checks when they are low ROI or not applicable.

| Feature Set / Scope | Target Or Relationship | Method | Result | Decision Impact | Caveat |
| --- | --- | --- | --- | --- | --- |
| same-time product returns | cross-product relation | correlation | `VELVETFRUIT_EXTRACT` has same-time return correlation `0.72` to `0.77` with `VEV_5000` to `VEV_5200`; `HYDROGEL_PACK` is near zero against the whole voucher family | promote option-family grouping; separate hydrogel branch | `VEV_6000` / `VEV_6500` are constant and produce `NaN` |
| same-time product returns | cross-product relation | covariance | covariance confirms magnitude-sensitive coupling inside the voucher family and near-zero hydrogel linkage | use covariance where scale matters for risk and sizing | covariance is less informative for constant-price floor symbols |
| pooled active option feature set | future 5-step voucher mid delta | linear regression | pooled `R^2 = 0.0159`; standardized coef strongest on `imbalance_1 = 0.1261`, near zero for contemporaneous underlying delta and extrinsic deviation | downgrade simple linear directional models; keep imbalance as weak filter, not core alpha | linear model is explanatory only |
| pooled active option feature set | future 5-step voucher mid delta | mutual information | `extrinsic_dev_day = 0.3358`, `spread = 0.2224`, `imbalance_1 = 0.0565`, `underlying_delta_1 = 0.0003` | promote nonlinear residual/surface features over delayed underlying-follow | MI is ranking evidence, not direct tradable effect size |
| option feature family (`mid`, `intrinsic`, `extrinsic`, `moneyness`, `spread`, `imbalance`) | redundancy / feature overlap | PCA/loadings | `PC1 = 72.0%` explained by price/intrinsic/moneyness/spread, `PC2 = 16.7%` almost pure imbalance, `PC3 = 10.8%` mostly extrinsic | merge price/intrinsic/moneyness family; keep imbalance and extrinsic as distinct axes | PCA is for pruning, not bot logic |
| underlying delta vs option delta by lag | cross-product lead-lag | lead-lag correlations | correlation is material at lag `0` and collapses around zero for lags `1`, `2`, `5`, `10` | reject delayed-follow strategies based on sample data | same-time coupling can still matter for valuation anchors |

## Redundancy / Dimensionality Check

Use this to avoid feature dumping. PCA/loadings are optional and should explain
feature structure, not become bot logic.

| Feature Family | Redundant Or Dominant Features | Evidence | Decision | Downstream Effect |
| --- | --- | --- | --- | --- |
| price-anchor family | `mid_price`, `intrinsic_value`, `moneyness`, parts of `spread` | PCA `PC1` loads `0.47` to `0.48` on most of these variables | keep one anchor family, do not stack all four as independent signals | later specs should choose one valuation anchor plus a residual rather than feature-dump |
| residual/time-value family | `extrinsic_value`, `extrinsic_dev_day` | MI and reversion metrics show residual matters beyond intrinsic | keep | option strategies can be written around residual mispricing, not raw price alone |
| order-book microstructure family | `imbalance_1` vs `rel_spread_bps` | PCA isolates imbalance on `PC2`; spreads stay with price-anchor family | keep both, but for different jobs | imbalance can be directional; spreads are mainly execution/risk filters |
| deep OTM floor family | `VEV_6000`, `VEV_6500` | zero return variance, constant `0.5` mids, `NaN` correlations | drop from signal family | later specs should exclude them unless live evidence contradicts the floor behavior |

## Cross-Product Relationships

Use when multiple products have aligned timestamps or plausible interaction.
Mark `not applicable` for single-product or clearly independent scopes.

| Product Pair / Scope | Check | Horizon / Alignment | Result | Decision | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` vs `VELVETFRUIT_EXTRACT` | correlation / covariance | same-time returns | correlation `0.0060`, effectively no linkage | separate | supports independent strategy branches |
| `VELVETFRUIT_EXTRACT` vs `VEV_5000` / `VEV_5100` / `VEV_5200` | correlation | same-time returns | strongest same-time correlations in family: `0.7524`, `0.7627`, `0.7192` | use | suggests these strikes are the cleanest active option set |
| `VELVETFRUIT_EXTRACT` vs voucher family | lead-lag | underlying lags `1`, `2`, `5`, `10` steps | lagged correlations collapse toward zero after lag `0` | reject delayed-follow | use same-time anchoring, not delayed chase |
| voucher family across strike | surface monotonicity / convexity | same timestamp, same day | monotone `100%` of timestamps on all days; convex `99.91%` to `100%` | use | strong evidence for cross-strike residual logic and validation guardrails |
| `VELVETFRUIT_EXTRACT` vs `VEV_6000` / `VEV_6500` | correlation | same-time returns | not applicable because vouchers are constant-floor series | exclude | dynamic linkage cannot be inferred from constant series |

## Process / Distribution Hypotheses

Use lightweight interpretations only when they affect strategy, risk,
specification, or validation. This is hypothesis generation, not formal proof.

| Product Or Scope | Hypothesized Process | Evidence | Confidence | Online Observables | Downstream Implication | Suggested Next Test | Status | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | short-horizon noisy mean-reverting delta-1 process with imbalance sensitivity | `delta_acf_1 = -0.1292`, `imbalance_corr_future_delta_5 = 0.1387`, mean spread `15.7` bps | medium | top-of-book spread, depth, imbalance | separate hydrogel branch with delta-1 microstructure logic | replay fill-adjusted imbalance / reversion logic | promote | sample does not prove net PnL after crossing costs |
| `VELVETFRUIT_EXTRACT` | tighter delta-1 anchor with mild short-horizon mean reversion and imbalance signal | `delta_acf_1 = -0.1585`, `imbalance_corr_future_delta_5 = 0.1441`, mean spread `9.5` bps | high | best bid/ask, mid, imbalance | use as valuation anchor for vouchers and as standalone delta-1 candidate | replay whether anchor-based fair value and imbalance combine cleanly | promote | directional edge strength still moderate |
| `VEV_4000` / `VEV_4500` | deep ITM call-like instruments, mostly intrinsic with residual snap-back | extrinsic mean about `0.01`; extrinsic deviation correlations `-0.7023` and `-0.7030` | medium-high | underlying mid plus strike mapping | use as structural anchors or residual mean-reversion candidates | validate on quote-crossing simulations because printed trades are uneven | promote | `VEV_4500` trade tape is sparse |
| `VEV_5000` / `VEV_5100` / `VEV_5200` / `VEV_5300` | active option regime with meaningful extrinsic and same-time underlying coupling | strongest same-time underlying correlations, positive extrinsic across TTE slices, nontrivial spreads | high | underlying mid, spread, imbalance, strike | best starting option subset for strategy candidates | test relative-value vs directional variants | promote | final round is TTE `5d`, not covered directly in sample |
| `VEV_5400` / `VEV_5500` | thin OTM option regime with high relative spread and mostly bid-side prints | rel spread about `900` to `1859` bps, strong at-or-below-bid trade shares, lower underlying coupling | medium | spread, imbalance, top-of-book levels | use cautiously, likely with strong execution filters only | validate whether passive-only logic is needed | exploratory | dynamic signal exists but execution may dominate |
| `VEV_6000` / `VEV_6500` | tick-floor / nearly inactive floor process | constant `0.5` mid, zero std, `20000` bps relative spread, `NaN` return correlations | high | floor price / one-tick spread | exclude from first implementation wave | reopen only if live data/logs break the floor | reject | they still print trades at bid `0`, so manual review remains prudent |

## Multivariate Model Notes

Keep models explanatory and lightweight. Do not tune heavy predictors or
recommend offline-only model logic for `Trader.run()`.

| Model / Check | Response | Predictors / Controls | Data Slice | Result | Leakage / Overfit Check | Actionability |
| --- | --- | --- | --- | --- | --- | --- |
| linear regression | standardized future 5-step option mid delta | standardized `underlying_delta_1`, `imbalance_1`, `extrinsic_dev_day` | pooled `VEV_5000` to `VEV_5500` rows with complete fields | low `R^2 = 0.0159`; only `imbalance_1` shows a modest positive coefficient | explanatory only, no train/test split used because purpose is ranking controls | use only as weak support for imbalance, not as strategy proof |
| mutual information | future 5-step option mid delta | `underlying_delta_1`, `imbalance_1`, `extrinsic_dev_day`, `spread` | same pooled option slice | `extrinsic_dev_day` and `spread` dominate nonlinear ranking | no predictive model built; ranking only | use to prioritize surface/residual features over delayed-underlying features |
| PCA | option feature structure | `mid_price`, `intrinsic_value`, `extrinsic_value`, `moneyness`, `spread`, `imbalance_1` | all non-floor option rows | PC1 price-anchor family, PC2 imbalance, PC3 extrinsic | dimensionality tool only; no bot logic from components | use to keep later specs parsimonious |

## Analyses Run

- Reproduction notes: `python rounds/round_3/workspace/01_eda/analyze_round_3_eda.py`
- Research tools used and why:
  - `pandas` / `numpy` for joins, rolling deltas, group-by aggregation, and panel reshaping
  - `sklearn` for PCA, mutual information, and a lightweight linear regression fallback
  - `matplotlib` / `seaborn` for plots that summarize surface, correlation, imbalance, and spread patterns
- Research tools considered but skipped:
  - `polars`: not installed and unnecessary for current dataset size
  - `arch`, `ruptures`: considered low ROI because volatility clustering / change-point detail would not change the next strategy decision yet
  - clustering: skipped because no clear online-observable action mapping beat the simpler strike/TTE grouping
  - `statsmodels`: import path is broken in the local environment because of a `scipy` compatibility issue, so the explanatory regression was done with `sklearn` instead
- Output artifacts:
  - processed CSVs under `../../data/processed/`
  - plots and JSON manifest under `artifacts/`
- Optional notebook: none
- Descriptive stats: run
- Distribution checks: run
- Volatility / regime checks: run at lightweight level via autocorrelation, spread regime splits, and zero-delta shares
- Spread / microstructure checks: run
- Correlation / covariance checks: run
- Feature redundancy checks: run
- Multivariate regression / controlled checks: run
- PCA / dimensionality checks: run
- Mutual information / non-linear checks: run
- Cross-product correlation / covariance: run
- Lead-lag checks: run
- Cross-product lead-lag checks: run
- Process / distribution checks: run
- Clustering / grouping checks: deferred as low ROI
- Price vs trade alignment: run
- Volume behavior: run at summary level
- Order book dynamics: run at top-of-book level

| Analysis | Status | Reason / Decision Impact | Artifact |
| --- | --- | --- | --- |
| correlation matrix | run | needed to separate hydrogel from option family and map same-time underlying linkage | `../../data/processed/derived_round_3_same_time_return_corr.csv` |
| covariance matrix | run | needed where scale matters for product interaction and risk intuition | `../../data/processed/derived_round_3_same_time_return_covariance.csv` |
| redundancy analysis | run | prevents feature-dump option specs | `../../data/processed/derived_round_3_option_feature_corr.csv`, `../../data/processed/derived_round_3_option_feature_covariance.csv` |
| multivariate regression | run | tested whether simple controls survive together for future option delta | `../../data/processed/derived_round_3_pooled_option_linear_model.csv` |
| cross-product checks | run | decides whether products should be combined or separated | `../../data/processed/derived_round_3_same_time_return_corr.csv` |
| PCA / loadings | run | high ROI because option feature set is clearly redundant | `../../data/processed/derived_round_3_option_pca_loadings.csv` |
| mutual information / non-linear dependence | run | high ROI because linear model looked weak and residual logic could still matter | `../../data/processed/derived_round_3_option_mutual_information.csv` |
| clustering / grouping | deferred | strike/TTE grouping already maps cleanly to actions; clustering would likely be decorative | none |
| process / distribution hypotheses | run | needed to split delta-1, active option, and floor-option regimes | `../../data/processed/derived_round_3_product_signal_metrics.csv`, `../../data/processed/derived_round_3_option_reversion_metrics.csv` |

## Research Tool Notes

Use tools only when they improve decision quality. Typical use: `pandas`/`numpy` for core tables, `polars` for large logs, `numba` for heavy loops, `scipy`/`statsmodels`/`pingouin` for tests, confidence, correlations, and lightweight regressions, `arch` for volatility regimes, `ruptures` for change points, and `sklearn` for PCA/loadings, lightweight clustering, or feature screening.

- Tools that changed a decision:
  - `sklearn` PCA/loadings changed the feature-budget decision by isolating imbalance and extrinsic as distinct axes and merging price-anchor features
  - `sklearn` mutual information changed the ranking of serious option features by showing residual/surface features matter more than delayed underlying delta
  - `matplotlib` / `seaborn` plots changed the decision to exclude `VEV_6000` / `VEV_6500` and to treat `VEV_5400` / `VEV_5500` as execution-sensitive rather than core signal carriers
- Tools that were unnecessary:
  - `arch`, `ruptures`, clustering, and notebook tooling for this first EDA pass
- Risk of overfitting or over-modeling:
  - biggest risk is not model complexity but over-interpreting sample-only option relationships and extrapolating TTE `6d` sample behavior to the final `5d` round day

## Distribution Hypotheses (Optional Compact Summary)

Use only when a shorter summary helps review. Prefer the richer `Process / Distribution Hypotheses` table above for new decision work.

| Product Or Scope | Hypothesis | Evidence | Strategy Implication | Caveat |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | noisy short-horizon mean reversion with imbalance help | negative lag-1 autocorrelation and positive imbalance correlation | treat as separate delta-1 candidate | edge must survive wider absolute spread than `VELVETFRUIT_EXTRACT` |
| `VELVETFRUIT_EXTRACT` | tighter anchor with mild reversion | narrow spread and stable imbalance effect | use as option anchor and standalone candidate | predictive strength is moderate, not overwhelming |
| active vouchers `VEV_5000` to `VEV_5300` | same-time anchored option family with nontrivial residual dynamics | strong same-time correlation plus positive extrinsic across TTE | best starting set for option strategy candidates | final day needs one-step TTE extrapolation |
| floor vouchers `VEV_6000` / `VEV_6500` | near-inactive floor regime | constant `0.5` mids and `NaN` returns | exclude initially | may still need live-data sanity check |

## Facts

- Wiki fact: Round 3 tradable algorithmic symbols are `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, and ten voucher symbols `VEV_4000` through `VEV_6500`.
- Wiki fact: `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` have limit `200`; each voucher symbol has limit `300`.
- Wiki fact: vouchers are options on `VELVETFRUIT_EXTRACT` and have TTE `5d` in the actual Round 3 simulation.
- Wiki fact: historical Round 3 sample mapping is day `0 -> TTE 8d`, day `1 -> TTE 7d`, day `2 -> TTE 6d`.
- Wiki fact: manual Bio-Pod bids are separate from the Python trading algorithm and should not be mixed into `Trader.run()` logic.

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| higher moneyness / ITM region (`VEV_4000` to `VEV_5200`) | same-time underlying coupling, extrinsic deviation | strongest same-time return linkage and cleaner residual structure | best area for first relative-value candidates | strong | `VEV_4500` printed-trade evidence is thin |
| farther OTM strikes (`VEV_5400` / `VEV_5500`) | spreads, trade alignment, zero-delta share | spreads widen sharply and trades skew to bid side | use only with strict execution filters or passive logic | medium | signal may be swallowed by execution cost |
| deep OTM floor (`VEV_6000` / `VEV_6500`) | mid price, return variance, spread bps | constant `0.5` mids and one-tick spread floor | exclude from first bot wave | strong | live simulation could still differ |
| strong positive imbalance | `imbalance_1`, future 5-step delta | average future mid delta rises with imbalance across selected products | viable short-horizon directional / filter feature | medium | needs fill-aware validation |
| day / TTE decay from `8d` to `6d` | average extrinsic by strike | extrinsic falls by about `1.7` to `8.1` points per day for active strikes | later strategy/spec should include TTE-aware calibration | medium-high | final day is `5d`, so one more decay step is still out-of-sample |

## Threshold / Execution Findings

Capture execution-relevant breakpoints rather than broad parameter sweeps.

| Finding | Feature Basis | Threshold Or Zone | Execution / Risk Use | Readiness | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are the only genuinely tight-spread products in sample | mean relative spread | about `15.7` bps for `HYDROGEL_PACK`, `9.5` bps for `VELVETFRUIT_EXTRACT` | good first candidates for active delta-1 execution | usable | still requires fill-aware validation |
| active voucher zone is `VEV_5000` to `VEV_5300` | mean relative spread and same-time coupling | roughly `237` to `455` bps | best starting option subset if the expected edge is large enough | usable | execution costs are still meaningful |
| `VEV_5400` / `VEV_5500` are execution-sensitive | mean relative spread | about `900` and `1859` bps | require strong filter or passive-only treatment | exploratory | signal edge may not survive crossing |
| `VEV_6000` / `VEV_6500` behave like floor instruments | mid and spread | fixed `0.5` mid, one-tick spread, `20000` bps relative spread | exclude initially | usable | reopen if live data breaks the floor behavior |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| short-horizon imbalance signal | `imbalance_1`, top-of-book prices and sizes | positive imbalance tends to precede positive short-horizon mid movement | gives a cheap online directional feature for both delta-1 and active vouchers | execution filter or mild directional overlay | stable but product-dependent | medium | effect sizes are modest and must survive cost |
| option residual mean reversion | `underlying_mid`, `strike`, `intrinsic_value`, `extrinsic_value`, `extrinsic_dev_day` | ITM / near-ATM voucher residuals tend to snap back after deviations from local extrinsic baseline | strongest option-specific signal found in this EDA | relative-value / residual-reversion family | strongest in `VEV_4000` / `VEV_4500`, moderate in `VEV_5000` | medium | weaker farther OTM and sample is one TTE step away from the real round |
| stable option surface as trading frame | strike, TTE, same-time cross-section | the voucher family is structurally monotone and nearly perfectly convex across strike | suggests mispricing should be measured as deviations from a stable surface, not raw independent option prices | cross-strike sanity checks and surface-relative features | highly stable | strong | structural stability alone is not an alpha |

## Downstream Feature Contract Implications

Use this to prepare later strategy specs without writing implementation logic.

| Feature Or Relationship | Contract Implication | Online Proxy Needed? | Validation / Invalidation Check | Do Not Use Until |
| --- | --- | --- | --- | --- |
| `VEV_*` symbol family | later specs should map each voucher by concrete symbol, strike, and TTE-aware metadata | no | symbol coverage in logs / runtime should match concrete `VEV_*` set | an official simulator-facing source contradicts the symbol set |
| `imbalance_1` | if used, spec must define sign convention, missing-depth fallback, and per-product thresholds or bins | no | validate by markout / replay that imbalance survives cost | fill-aware validation exists |
| `intrinsic_value` / `extrinsic_value` | option logic should explicitly define whether decisions trade on total price, residual, or both | no | invalidate if residual signal disappears on final-day or live runs | strategy family chooses a valuation anchor |
| `extrinsic_dev_day` | residual strategy should specify grouping scope and missing-signal fallback | no | invalidate if reversion weakens materially at TTE `5d` or after cost | later strategy candidate confirms product subset |
| wide-spread OTM vouchers | strategy/spec should treat spread as an execution filter or exclusion rule | no | invalidate if passive fills or live books materially improve economics | execution assumptions are reviewed |
| delayed underlying-follow | do not use lagged underlying delta as direct option alpha by default | no | reopen only if live logs show real latency / stale quotes | contradictory run evidence appears |

## Negative Evidence

Preserve meaningful failed checks so later agents do not rediscover weak ideas.

| Idea Or Signal | Why It Was Plausible | Evidence Against It | When To Reopen |
| --- | --- | --- | --- |
| delayed-follow strategy from `VELVETFRUIT_EXTRACT` into vouchers | options should relate to the underlying and sample data clearly links them at lag `0` | lead-lag correlations collapse toward zero immediately after lag `0` across active strikes | if live logs show stale option books or execution latency not visible in historical sample |
| hydrogel / velvetfruit hedge or shared signal family | both are delta-1 products in the same round | same-time return correlation is only `0.0060` and covariance is negligible | if later runs show common shocks or shared inventory/risk interactions |
| using `VEV_6000` / `VEV_6500` as dynamic signal instruments | they print trades and appear in the book every timestamp | mids are constant at `0.5`, std is `0`, and correlations are undefined | if final-day or live-run books show non-floor behavior |
| simple linear future-delta model driven by underlying delta | underlying and options move together same-time | pooled linear model has very low `R^2`, and contemporaneous underlying delta contributes almost nothing after controls | if richer targets or live fills reveal a usable linear effect |

## Assumptions

- The voucher family behaves as call-like options because the Round 3 page describes them as giving the right to buy `VELVETFRUIT_EXTRACT` later at a strike price.
- Historical file day mapping follows the official round text: `day 0 -> TTE 8d`, `day 1 -> TTE 7d`, `day 2 -> TTE 6d`.
- `VELVETFRUIT_EXTRACT_VOUCHER` is treated here as a family label, while the concrete tradable bot symbols are the observed `VEV_*` products.
- Sample order-book and trade patterns are treated as EDA evidence, not as official exchange rules or guaranteed final-day behavior.

## Open Questions

- How much of the active-voucher extrinsic decay from TTE `6d` to final TTE `5d` will look like the historical `8 -> 7 -> 6` pattern versus a sharper terminal effect?
- Why are printed trades so sparse in `VEV_4500`, `VEV_5000`, and `VEV_5100` despite active quote panels? Is that just bot-to-bot inactivity, or does it hint at fill behavior we should validate separately?
- Will `VEV_6000` / `VEV_6500` remain floor instruments in the final day, or is the sample masking rare but real dynamic episodes?
- Manual challenge question remains open outside algorithmic work: the exact fill-probability interpretation below `avg_b2` is still not explicit in the source wording.

## Reusable Metrics

- `imbalance_1 = (bid_volume_1 - ask_volume_1) / (bid_volume_1 + ask_volume_1)`
- `rel_spread_bps = (ask_price_1 - bid_price_1) / mid_price * 10000`
- `moneyness = underlying_mid - strike`
- `intrinsic_value = max(underlying_mid - strike, 0)`
- `extrinsic_value = option_mid - intrinsic_value`
- `extrinsic_dev_day = extrinsic_value - mean_day_product_extrinsic`
- same-time return correlation and covariance matrices for cross-product scope decisions
- lagged underlying-to-option delta correlation table for delayed-follow rejection

## Downstream Use / Agent Notes

- Use this EDA to start Phase 02 Understanding with four strong guardrails:
  - branch `HYDROGEL_PACK` separately from the voucher family
  - anchor voucher reasoning on `VELVETFRUIT_EXTRACT`
  - treat `VEV_5000` to `VEV_5300` as the highest-ROI active option subset
  - exclude `VEV_6000` / `VEV_6500` from first-wave bot logic unless later evidence contradicts the floor behavior
- Later strategy generation should prioritize:
  - delta-1 microstructure candidates for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - surface-aware residual strategies for the active voucher subset
  - execution filters based on relative spread and one-sided trade alignment for farther OTM strikes
- Later specs should not:
  - assume delayed underlying-follow is alpha
  - assume every voucher strike deserves equal implementation effort
  - mix manual Bio-Pod mechanics into the bot
- Best immediate next phase action: compress this EDA into a short Understanding artifact with 1-3 promoted signal hypotheses, one negative-evidence block, and an explicit product shortlist for strategy generation.
