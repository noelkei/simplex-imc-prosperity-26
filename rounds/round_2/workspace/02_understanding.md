# Round 2 Understanding Summary

## Status

COMPLETED

Review outcome: `approved with caveats`.

This artifact compresses the reviewed-with-caveats Round 2 ingestion and consolidated EDA into strategy-ready understanding. It does not generate strategy candidates, specs, or bot logic.

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_2.md`, plus shared API/trading/runtime docs listed in `00_ingestion.md`.
- Ingestion: `rounds/round_2/workspace/00_ingestion.md`.
- EDA evidence: `rounds/round_2/workspace/01_eda/eda_round2_fresh.md`.
- EDA compact artifacts:
  - `rounds/round_2/workspace/01_eda/artifacts/expanded_feature_promotion_decisions.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/process_distribution_hypotheses.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_regression_summary.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_redundancy_analysis.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_cross_product_relationships.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/maf_scenarios.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/manual_scenario_summary.csv`
- Post-run research memory: absent for Round 2 at synthesis time.
- Playbook heuristics: none promoted as facts.

## Current Understanding

- Wiki fact: Round 2 algorithmic products are `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, both with position limit 80.
- Wiki fact: Round 2 adds `Trader.bid()` for the Market Access Fee; accepted top-50% bids pay the fee and receive 25% more order-book quotes in final Round 2 only.
- Wiki fact: Round 2 testing ignores `bid()` and uses a slightly randomized 80% quote subset.
- Wiki fact: Manual Research / Scale / Speed allocation is separate from `Trader.run()` and manual-only.
- EDA evidence: `INTARIAN_PEPPER_ROOT` is a strong drift/residual product in sample data; fixed Round 1 fair value assumptions are contradicted.
- EDA evidence: `ASH_COATED_OSMIUM` behaves like a short-horizon mean-reverting microstructure product in sample data.
- EDA evidence: `top_imbalance` is the cleanest order-book directional signal; `microprice_deviation` is a plausible but redundant challenger.
- EDA evidence: `spread regime` should be carried as execution/risk-filter evidence, not standalone alpha.
- Hypothesis: first strategy candidates should be feature-light and product-specific, using one primary edge plus at most simple execution/risk filters.
- Unknown: final platform distribution, final 80% quote subset, exact deadline, competitive MAF bid distribution, manual Speed rank, and platform `market_trades` dynamics.

## Challenge Boundary / Do Not Mix

| Track | Goes Into | Must Stay Out Of | Understanding Decision |
| --- | --- | --- | --- |
| Algorithmic trading | Signal Ledger, product view, strategy implications | manual allocation | Use only online-usable or explicitly proxied features for strategy/spec. |
| Market Access Fee | Round 2 mechanics/risk decision | normal `Trader.run()` signal ledger and manual allocation | Carry scenario evidence separately; final bid belongs in strategy/spec/human risk decision. |
| Manual Research / Scale / Speed | Manual-only section | bot features, Signal Ledger, MAF bid logic | Carry scenario candidates only; do not let manual findings influence bot signals. |

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` should not use a fixed Round 1 fair value. | ingestion + consolidated EDA | strong | high | Platform/final data shows drift structure materially changed. |
| IPR drift/residual is a serious fair-value basis. | process hypotheses + regression | strong | high | Platform markouts or validation show residual overfit to sample days. |
| `ASH_COATED_OSMIUM` supports a short-horizon reversal candidate. | process hypotheses + product behavior | medium/strong | high | Fill/markout validation shows reversal cannot overcome spread/adverse selection. |
| `top_imbalance` is the simplest strong order-book signal. | IC + controlled regression | strong | high | A one-axis microprice or full-book variant clearly beats it in validation. |
| `microprice_deviation` is plausible but redundant with `top_imbalance`. | redundancy analysis | medium | medium | Controlled variant beats top imbalance alone. |
| `full-book imbalance` is backup/context, not automatic co-primary feature. | IC + redundancy/process notes | medium | medium | It outperforms top imbalance under wide/one-sided regimes. |
| `spread regime` is useful as execution/risk filter. | EDA + controlled checks | medium | high | Platform PnL improves without spread/depth gating. |
| Cross-product lead-lag should not drive first-pass strategy. | cross-product artifact | weak/negative | medium | New platform evidence shows product coupling absent from sample data. |
| Trade pressure is not ready for implementation. | EDA + missing platform printed state probe | weak / needs logs | medium | Platform logs expose reliable `market_trades` dynamics. |
| Manual RSS allocation is separate from bot logic. | wiki facts + EDA challenge boundary | strong | high | Not expected to change; official docs would need to redefine mechanics. |

## Signal Validation Expectations

- Statistical or regime evidence used: process hypotheses, controlled regression, imbalance IC, redundancy checks, cross-product lead-lag, platform comparability, MAF/manual scenario tables.
- Features downgraded for weak confidence, redundancy, or offline-only status: `full-book imbalance`, `microprice_deviation`, liquidity/depth regime, cross-product lead-lag, PCA/clusters/latent components, trade pressure proxy.
- Research outputs not trusted yet: PCA components, cluster labels, latent-state interpretations, MAF PnL proxy as exact bid value, manual Speed rank proxy as prediction.

## Multivariate Relationships Carried Forward

| Relationship | Source EDA Artifact | Evidence | Decision Impact | Confidence | Caveat |
| --- | --- | --- | --- | --- | --- |
| ACO future mid delta vs `top_imbalance` | `multivariate_regression_summary.csv` | h1 standardized coef `2.31`, p=0, controlled model R2 `0.162` | use as primary ACO order-book signal candidate | high | Must validate after spread/fills. |
| ACO `microprice_deviation` vs `top_imbalance` | `multivariate_redundancy_analysis.csv` | correlation `0.959` | validate as one-axis challenger, not feature stack | medium | Direction differs in controlled model because it overlaps top imbalance/spread. |
| IPR future mid delta vs `drift_residual_z` | `multivariate_regression_summary.csv` | h3/h5 coefficients about `-1.41`, p=0 | use residual mean-reversion around drift as primary IPR candidate | high | Avoid sample-day constants. |
| Spread / relative spread | `multivariate_redundancy_analysis.csv` | ACO corr `1.000`, IPR corr `0.934` | keep absolute spread first | high | Relative spread only if cross-product comparability matters. |
| Cross-product lead-lag | `multivariate_cross_product_relationships.csv` | max absolute lead-lag corr about `0.016` | avoid first-pass cross-product strategy | high for rejection | Reopen if platform logs contradict sample. |

## Redundancy Decisions

| Feature Family | Keep | Merge / Downgrade / Drop | Evidence | Strategy Impact |
| --- | --- | --- | --- | --- |
| Top-book pressure | `top_imbalance` first | `microprice_deviation` exploratory challenger | corr about `0.958`; controlled model says overlap is material | Strategy should not stack both in first spec. |
| Book-depth pressure | `top_imbalance` first | `full-book imbalance` backup/context | EDA IC positive but controlled/redundancy notes favor simpler signal | Use full-book only as variant or regime backup. |
| Spread features | `spread` | `relative_spread` downgraded | ACO corr `1.000`, IPR corr `0.934` | Specs should name one spread filter. |
| Trade activity | none for first spec | `trade_count`, `trade_quantity`, `trade_pressure_qty` needs logs | trade count/quantity high redundancy; platform printed state missing | Keep out of first implementation. |
| PCA/clustering | none as direct feature | all latent components EDA-only | offline representation, no reviewed online proxy | Use only to simplify feature choices and diagnostics. |

## Process Hypotheses Carried Forward

| Product Or Scope | Process Hypothesis | EDA Evidence | Confidence | Online Observable / Proxy | Strategy Or Validation Implication |
| --- | --- | --- | --- | --- | --- |
| `ASH_COATED_OSMIUM` | short-horizon mean-reverting microstructure process | mean linear R2 `0.059`; mean delta AC1 `-0.500`; ARCH-day share `1.00` | medium/high | previous mids, current mid from order book, spread, rolling delta | Try reversal/fair-value adjustment with spread and fill validation. |
| `INTARIAN_PEPPER_ROOT` | strong deterministic trend plus residual mean-reversion/noise | mean linear R2 `1.000`; mean delta AC1 `-0.498`; mean day change `999.67`; ARCH-day share `1.00` | high | timestamp, current mid, drift reference, residual z-score | Try drift-aware fair value and residual mean-reversion; reject fixed fair value. |
| Spread/depth regimes | execution quality changes by visible liquidity | EDA promotes spread as execution/risk filter; depth exploratory | medium | best bid/ask spread, visible depth, missing levels | Use as filter/sizing/risk control before dynamic regime complexity. |

## Assumptions Carried Forward

| Assumption | Source | Current-Round Evidence | Risk | Action |
| --- | --- | --- | --- | --- |
| Round 1 fixed IPR fair value is usable | prior round hint | contradicted by Round 2 drift evidence | high | reject |
| Products and limits carry forward from Round 1 | Round 2 wiki | explicitly same products, limit 80 | low | use as wiki fact |
| ACO is volatile/patterned | prior round/EDA prompt | supported as short-horizon reversal, not broad volatility claim | medium | validate |
| Book imbalance is predictive | EDA | supported, especially top imbalance | medium | use/validate |
| Trade pressure is online useful | CSV and possible `market_trades` field | not enough platform evidence | medium | defer / needs logs |
| MAF bid has positive value | EDA proxy | plausible but competitor-dependent | high | carry as scenario only |
| Manual Speed outcome can be optimized exactly | manual formula intuition | false; rank is competitor-dependent | high | use scenarios only |

## Signal Ledger

Algorithmic trading signals only. Manual challenge findings are intentionally excluded.

| Signal | Product | Source Artifact | Feature Basis | Feature Origin | Online Usability | Role | Stability | Confidence | Decision Action | Risk | Next Phase Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IPR drift + residual | `INTARIAN_PEPPER_ROOT` | consolidated EDA / process hypotheses / regression | timestamp, mid/order book, drift reference, residual z-score | csv / online proxy | usable online | direct signal / fair-value basis | stable in sample | high | use | overfit to sample-day drift constants | strategy should create drift-aware candidate with explicit online formula and invalidation check |
| ACO short-horizon reversal | `ASH_COATED_OSMIUM` | consolidated EDA / process hypotheses | previous mid delta, current mid/order book | csv / online proxy | usable online | direct signal / fair-value adjustment | stable in sample | medium/high | use | adverse selection and spread may erase edge | strategy should test reversal candidate with spread-aware execution |
| Top imbalance | both, strongest ACO evidence | consolidated EDA / IC / regression | best bid/ask volumes | csv / online | usable online | direct signal / quote skew | stable enough for candidate queue | high | use | redundant with microprice; sizing unknown | strategy should use as one primary order-book pressure feature |
| Spread regime | both | consolidated EDA | best bid/ask spread | csv / online | usable online | execution filter / risk control | day-sensitive | medium | validate next | can over-filter if thresholds are too tight | spec should define threshold/fallback only if candidate uses it |

## Strategy-Relevant Insights

| Insight | Linked EDA Signals | Feature Evidence | Regime Assumptions | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| Round 2 should be product-specific first. | IPR drift/residual, ACO reversal | product processes differ materially | no cross-product dependence assumed | high | Generate separate product branches before combining. |
| IPR needs drift-aware fair value. | IPR drift/residual | linear R2 `1.000`, residual reversal evidence | drift structure persists enough to estimate online | high | Candidate should define drift/reference and residual logic. |
| ACO needs reversal plus execution discipline. | ACO reversal, top imbalance, spread regime | delta AC1 about `-0.500`; top imbalance controlled evidence | spread/fills may gate profitability | medium/high | Candidate should test reversal/order-book pressure with spread filter. |
| Top-book pressure is the first order-book feature family. | top imbalance, microprice deviation | top imbalance strong; microprice redundant/exploratory | top-of-book signal survives platform subset | high | Use one primary pressure feature; keep microprice as challenger. |
| Manual and MAF decisions are not normal alpha signals. | MAF scenarios, manual RSS scenarios | separate official mechanics | separate submission tracks | high | Strategy/spec may handle MAF; manual stays outside bot work. |

## Market Access Fee Understanding

| Item | Understanding | Evidence | Strategy Use | Caveat |
| --- | --- | --- | --- | --- |
| Mechanic | `Trader.bid()` can buy 25% more quotes if accepted in top 50% bids. | Round 2 wiki | Round-specific mechanics contract in spec | Testing ignores bid. |
| Value proxy | Incremental proxy ranges from about `78` to `786` at edge threshold 0 depending on capture rate `0.01` to `0.10`. | `maf_scenarios.csv` | Use for bid scenario discussion, not final exact bid | Competitor bid distribution unknown. |
| Conservative bid range | EDA proxy table gives conservative ceilings around `39`, `98`, `196`, `393` at threshold 0 across capture rates. | `maf_scenarios.csv` | Strategy should choose risk posture later | Accepted bids pay the fee; rejected bids pay nothing. |
| Boundary | MAF is not a normal `Trader.run()` signal. | challenge boundary | Keep separate from signal ledger | Final bid belongs in reviewed spec/human decision. |

## Manual Challenge Understanding

Manual-only. Do not put these rows into bot Signal Ledger or algorithmic strategy candidates.

| Scenario | Best Allocation | Best PnL Proxy | Interpretation | Caveat |
| --- | --- | ---: | --- | --- |
| pessimistic rank proxy | Research 14 / Scale 42 / Speed 44 | 65062.63 | More Speed helps if rank outcome is poor. | Speed rank is unknown. |
| linear rank proxy | Research 16 / Scale 48 / Speed 36 | 110065.31 | Balanced robust-looking allocation under middle rank model. | Scenario model, not prediction. |
| optimistic rank proxy | Research 19 / Scale 58 / Speed 23 | 204930.62 | Less Speed can win if rank multiplier is favorable. | Crowding can invalidate. |

Manual next action: keep these as manual allocation candidates and ask for human risk posture near final manual submission. They should not affect bot features, MAF bid logic, or strategy candidate selection.

## Product Attribution View

| Product | Opportunity / Risk Status | Evidence | Main Uncertainty | Strategy Implication |
| --- | --- | --- | --- | --- |
| `ASH_COATED_OSMIUM` | edge likely but execution-sensitive | mean-reverting process, strong top imbalance controlled evidence | whether spread/fills/adverse selection erase reversal | Try reversal/order-book pressure candidate with conservative execution filter. |
| `INTARIAN_PEPPER_ROOT` | edge likely via drift/residual | high drift R2 and residual mean-reversion evidence | online drift formula and final-day drift stability | Try drift-aware fair value candidate; avoid fixed fair value. |
| Both products | combined portfolio possible | both have separate signal families | interaction is weak, risk may come from shared inventory/execution | Treat products independently first; combine only if specs remain simple. |

## Cross-Product Verdict

- Verdict: `weak`
- Evidence: same-timestamp correlations are near zero, and max absolute mid-delta lead-lag correlation is about `0.016`.
- Caveat: this is sample-data evidence only, but it is strong enough negative evidence to avoid first-pass cross-product strategy.

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| Drift-aware residual fair value | IPR process hypothesis | `INTARIAN_PEPPER_ROOT` | strongest product-specific evidence; rejects stale fixed fair value | markout/PnL by day and platform subset; no sample-end constants |
| Short-horizon reversal market making | ACO process hypothesis | `ASH_COATED_OSMIUM` | mean-reverting microstructure with stable negative delta AC1 | fill quality, spread capture, adverse selection |
| Top-imbalance quote skew | top imbalance evidence | both, especially ACO | online, simple, strong controlled signal | compare against no-imbalance and microprice variants |
| Microprice challenger | redundancy/controlled evidence | both | may compact top pressure and spread | one-axis variant only; do not stack with top imbalance first |
| Spread-aware execution filter | spread regime evidence | both | likely improves risk/execution quality | PnL/fill split by spread regime |
| MAF bid scenario | Round 2 mechanics + proxy | final Round 2 bid only | extra quotes may have value | choose risk posture; cannot validate exactly in tests |

## What Should Not Be Trusted Yet

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| Fixed Round 1 IPR fair value | Round 2 drift contradicts it | systematic mispricing | reject unless final data contradicts EDA |
| Cross-product lead-lag | correlations are near zero | complexity without edge | reopen only with new platform evidence |
| Trade pressure proxy | platform `ROUND2_STATE_PROBE` absent and sample trades sparse | false flow signal | collect better `market_trades` logs |
| PCA / clusters / latent components | offline research representation, no Feature Contract | non-runtime-compatible bot logic | use only for diagnostics unless online proxy is specified |
| Manual allocation as bot feature | separate challenge | invalid strategy reasoning | keep manual-only |
| MAF proxy as exact bid | competitor distribution unknown | overpay or fail acceptance | scenario/risk decision later |

## Research Memory

Promising features:

| Feature Or Signal | Source | Why Promising | Needed Before Strategy |
| --- | --- | --- | --- |
| `microprice_deviation` | EDA redundancy/regression | plausible top-book pressure transformation | compare as one-axis challenger to top imbalance |
| `full-book imbalance` | EDA IC/redundancy | useful backup/context signal | validate under wide/one-sided regimes before promoting |
| spread/depth defensive filters | EDA process/regime notes | can target execution quality | spec-level threshold and PnL/fill split |

Rejected / noisy features:

| Feature Or Signal | Source | Evidence Against | Reopen Only If |
| --- | --- | --- | --- |
| cross-product lead-lag | cross-product artifact | max abs lag corr about `0.016` | platform logs show coupling |
| PCA/cluster direct logic | consolidated EDA | offline/latent, no online Feature Contract | simple online proxy is reviewed |
| fixed IPR fair value | Round 1 assumption check | contradicted by current-round drift | final data materially changes |

Unresolved / log-needed features:

| Feature Or Signal | Source | Missing Evidence | Next Action |
| --- | --- | --- | --- |
| trade pressure proxy | EDA trades/log caveat | platform `market_trades` dynamics from printed state | collect targeted logs if ROI justifies |
| MAF bid | MAF scenario table | competitor bids and final extra-access realized value | defer final bid until strategy/risk decision |
| manual Speed allocation | manual scenario grid | competitor Speed rank | choose scenario/risk posture near submission |

## Confidence And Impact

- Overall confidence: `medium/high` for direction, `medium` for implementation payoff.
- Highest-impact implication: Round 2 strategy should be product-specific and current-round evidence-driven; do not carry a fixed IPR fair value or feature-dump order-book signals.
- Main caveat: EDA is sample/platform-quote evidence, not final PnL proof; execution and platform variance must decide promotion.

## Assumptions

- Consolidated EDA is accepted for synthesis with caveats.
- No post-run research memory exists yet for Round 2.
- Final platform distribution and randomized testing quote subset may differ from sample data.
- Strategy specs can use online proxies for mid/residual/delta features via order books and `traderData`, but must define formulas and missing-signal behavior.

## Open Questions

- What is the exact Round 2 deadline?
- What MAF risk posture should the team prefer: low bid, base bid, aggressive bid, or no bid?
- Which manual RSS scenario should be favored near submission?
- Will platform `market_trades` logs become available before strategy/spec decisions?

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| Deadline unknown | strategy/spec/validation | high | clarify; switch to fast mode if less than 24h remains |
| Execution costs erase ACO reversal | strategy/spec/validation | high | require fill/markout validation |
| IPR drift formula overfits sample days | strategy/spec | high | spec must avoid hardcoded day-end constants |
| Randomized 80% quote subset changes results | validation | medium/high | platform validation and comparability notes |
| MAF bid overpays | final round decision | medium/high | scenario-based bid decision with explicit risk posture |
| Manual Speed rank is unknowable | manual | medium/high | keep multiple scenario candidates |

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| ACO reversal survives execution? | strategy/spec/validation | high | strategy candidate plus validation markouts |
| IPR drift/residual implementation formula | strategy/spec | high | define in candidate/spec without day constants |
| Top imbalance vs microprice | strategy/spec/variant | medium/high | one-axis candidate/variant decision |
| MAF bid range | spec/final | medium | defer to strategy after candidate PnL expectations |
| Trade pressure logs | EDA/strategy | medium | collect only if first candidates need flow diagnostics |
| Manual RSS selection | manual | medium | revisit near manual submission |

## Strategy Implications

- Candidate direction: start with product-specific branches, not a cross-product model.
- Candidate direction: likely useful branches are IPR drift/residual, ACO reversal, top-imbalance quote skew, microprice challenger, and spread-aware execution filter.
- Risk or constraint: keep feature budget tight; do not stack top imbalance, microprice, and full-book imbalance in the same first spec.
- Risk or constraint: MAF bid requires a Round-Specific Mechanics Contract but should not be mixed with normal signal logic.
- Risk or constraint: manual challenge remains manual-only.
- Validation/debug implication: every serious candidate needs product PnL split, fill/markout quality, spread/depth regime diagnostics, position-limit checks, and platform quote-subset caveats.

## Next Action

- Human review outcome: approved with caveats on 2026-04-19.
- Phase 03 Strategy Candidates should use this file plus the consolidated EDA.
- Strategy generation should build a bounded but not artificially tiny
  exploration board, then produce an ROI-driven prioritized candidate queue.
