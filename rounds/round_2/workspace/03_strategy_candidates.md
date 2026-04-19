# Round 2 Strategy Candidates

## Status

COMPLETED

Review outcome: `approved with caveats`.

Phase 03 converts the approved-with-caveats Understanding and consolidated EDA
into a prioritized, ROI-driven strategy candidate queue. It does not create
strategy specs, bot code, or final MAF/manual decisions.

Candidate count is evidence-driven, not fixed. All non-duplicative high-ROI
candidates are retained and prioritized by role, priority tier, and
implementation wave.

## Sources

- Wiki facts: `docs/prosperity_wiki/rounds/round_2.md`, shared API and trading docs from `00_ingestion.md`.
- Understanding summary: `rounds/round_2/workspace/02_understanding.md`.
- Consolidated EDA: `rounds/round_2/workspace/01_eda/eda_round2_fresh.md`.
- EDA artifacts:
  - `rounds/round_2/workspace/01_eda/artifacts/expanded_feature_promotion_decisions.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/process_distribution_hypotheses.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_regression_summary.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_redundancy_analysis.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/multivariate_cross_product_relationships.csv`
  - `rounds/round_2/workspace/01_eda/artifacts/maf_scenarios.csv`
- Post-run research memory: absent for Round 2 at candidate generation time.
- Playbook heuristics: used only as heuristics, not facts.

## Feature Budget

- Primary edge: one primary feature, signal, or fair-value model per candidate.
- Supporting logic: up to two execution filters or risk controls.
- Diagnostics may be included when they do not change trading decisions.
- Multi-product candidates may use one primary edge per product only when the
  products remain independent modules and the decision trace justifies the
  combination.

Required chain for serious candidates:

```text
feature -> signal -> decision -> expected edge -> validation check
```

## Round Coverage Check

| Item | Source | Candidate Impact | Decision |
| --- | --- | --- | --- |
| Products `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, limit 80 each | Round 2 wiki / ingestion | affects product scope and risk | use |
| `Trader.bid()` Market Access Fee | Round 2 wiki / Understanding / MAF scenarios | affects final-round mechanics and risk, not normal alpha | use as mechanics-only candidate |
| Testing ignores `bid()` and uses randomized 80 percent quote subset | Round 2 wiki / Understanding | affects validation comparability | record caveat in specs and run summaries |
| Manual Research / Scale / Speed | Round 2 wiki / Understanding | separate manual challenge | exclude from bot candidates |
| Cross-product lead-lag | EDA cross-product relationships | weak evidence; no first-pass cross-product alpha | reject for first-pass strategy |
| Trade pressure / `market_trades` dynamics | EDA / platform log caveat | possible future flow signal | defer until better logs |

## Exploration Board

| Idea ID | Product | Source Signal | Primary Feature / Signal | Supporting Features | Process Hypothesis | Online Proxy Needed? | Approach | Expected Edge | Main Risk | Implementation Realism | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R2-IDEA-01` | IPR | IPR drift plus residual | drift-aware fair value | spread, inventory | deterministic trend plus residual mean reversion | no | market making around drift FV | capture residual mispricing | overfit drift formula | high | candidate |
| `R2-IDEA-02` | IPR | IPR residual extremes | residual z-score threshold | spread, inventory | residual mean reversion | no | trade only stronger dislocations | higher-confidence entries | missed opportunities | high | candidate |
| `R2-IDEA-03` | ACO | ACO reversal | previous mid delta | spread, inventory | short-horizon mean reversion | no | reversal market making | profit from microstructure reversal | adverse selection | high | candidate |
| `R2-IDEA-04` | ACO | top imbalance | best bid/ask volume imbalance | spread, inventory | order-book pressure | no | quote skew | directional top-book pressure | redundancy with microprice | high | candidate |
| `R2-IDEA-05` | ACO | microprice deviation | microprice deviation | spread, inventory | order-book pressure transform | no | one-axis challenger to imbalance | better compact pressure signal | redundant without PnL gain | medium | candidate |
| `R2-IDEA-06` | ACO | full-book imbalance / depth | full-book imbalance or depth regime | spread, inventory | liquidity-regime behavior | no | depth-aware backup | improve wide/one-sided regimes | lower evidence than top-book | medium | candidate |
| `R2-IDEA-07` | both | IPR drift + ACO top imbalance | product-specific independent modules | spread, inventory | independent product processes | no | combined final-bot path | additive independent edges | module interaction/inventory | high | candidate |
| `R2-IDEA-08` | both | IPR drift + ACO reversal | product-specific independent modules | spread, inventory | independent product processes | no | combined challenger | compare ACO hypothesis in final bot | reversal execution cost | high | candidate |
| `R2-IDEA-09` | both | spread regime | spread filter | inventory | execution quality regimes | no | defensive overlay | reduce bad fills | over-filtering | high | candidate |
| `R2-IDEA-10` | Round 2 final | MAF scenarios | bid policy | risk posture | extra quote-access value | n/a | mechanics policy | improve final information access | overpay / rejection | medium | candidate |

## Per-Product Branches

| Product | Top Branches | Strongest Signal | Weakest Assumption | Pruning Note |
| --- | --- | --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | drift FV maker, residual extreme execution | drift plus residual | final-day drift remains online-estimable without sample-end constants | keep both because execution behavior differs materially |
| `ASH_COATED_OSMIUM` | reversal maker, top imbalance skew, microprice challenger, full-book backup | top imbalance and reversal | fills/spread may erase edge | prioritize top imbalance and reversal first; keep microprice/depth as targeted challengers |
| Both | combined imbalance, combined reversal, spread overlay | independent product signals | shared risk/inventory may reduce additive value | combine only after single-product specs can attribute edge |
| Round 2 mechanics | MAF bid policy | MAF value proxy | competitor bids unknown | keep separate from `Trader.run()` alpha |

## Combination / Compatibility Matrix

| Pairing | Compatibility | Risk Interaction | Execution Alignment | Cross-Product Dependency | Verdict |
| --- | --- | --- | --- | --- | --- |
| IPR drift FV + ACO top imbalance | high | independent product risk, shared capital attention | aligned if risk code is shared | none | move forward |
| IPR drift FV + ACO reversal | high | independent product risk, ACO execution-sensitive | aligned if risk code is shared | none | move forward |
| ACO top imbalance + microprice | low | redundant top-book pressure | mixed | none | reject stack; use microprice only as challenger |
| ACO top imbalance + full-book depth | medium | possible regime backup | mixed | none | backup only after top-book weakness appears |
| Product modules + spread overlay | high | may reduce fills but improve markouts | aligned | none | validate as overlay |
| Cross-product lead-lag | low | added complexity without evidence | conflicting | weak | reject |

## Candidate Table

| Candidate ID | Role | Product Scope | Source Of Edge | Primary Feature / Signal | Supporting Features | Feature Role | Linked EDA Signals | Feature Evidence | Multivariate Evidence | Supporting Process Hypothesis | Redundancy Note | Online Proxy Needed? | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Why Not Feature Dumping | ROI / Pruning Rationale | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority Tier | Implementation Wave | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `R2-CAND-01-IPR-DRIFT-FV-MAKER` | primary | IPR | drift-aware fair value | drift FV plus residual | spread, inventory | direct signal / fair-value basis | IPR drift plus residual | mean linear R2 near 1.000; residual reversal evidence | h3/h5 residual coefficients about -1.41, p=0 | deterministic trend plus residual mean reversion | rejects fixed Round 1 FV | no | drift persists enough to estimate online | IPR needs drift-aware fair value | no sample-end constants; timestamp/order book online only | drift overfit | one primary FV model plus two controls | highest IPR evidence and fastest isolation test | strong | medium | high | medium | high | spec-first | wave 1 | draft |
| `R2-CAND-02-IPR-RESIDUAL-EXTREME-EXECUTION` | secondary | IPR | residual mean reversion | residual z-score threshold | spread, inventory | direct signal / execution style | IPR drift plus residual | residual evidence same as C01, but stricter entry logic | same residual model as C01 | residual mean reversion/noise | execution variant, not new feature stack | no | extreme residuals mean revert enough to offset fewer fills | IPR drift formula must avoid stale FV | threshold can be chosen without overfitting | under-trading / missed edge | same primary signal, materially different execution | useful controlled variant if C01 overtrades | medium/high | low | high | medium | medium/high | implement-first | wave 2 | draft |
| `R2-CAND-03-ACO-REVERSAL-MAKER` | primary | ACO | short-horizon reversal | previous mid delta | spread, inventory | direct signal / fair-value adjustment | ACO short-horizon reversal | mean delta AC1 about -0.500 | controlled/process evidence supports reversal framing | mean-reverting microstructure | separate from top imbalance | no | reversal survives spread and fills | ACO needs reversal plus execution discipline | previous mids via `traderData` are reliable | adverse selection | one primary time-series signal plus controls | tests ACO process hypothesis directly | medium/high | medium | high | medium/high | high | spec-first | wave 1 | draft |
| `R2-CAND-04-ACO-TOP-IMBALANCE-SKEW` | primary | ACO | order-book pressure | top imbalance | spread, inventory | direct signal / quote skew | top imbalance | strongest order-book signal in Understanding | h1 standardized coef 2.31, p=0, R2 0.162 | order-book pressure / microstructure | keep over microprice first | no | top-book pressure survives platform subset | top-book pressure is first order-book family | imbalance signal remains stable in validation | redundancy / sizing | one primary top-book feature plus controls | strongest controlled ACO order-book candidate | strong | medium | high | medium | high | spec-first | wave 1 | draft |
| `R2-CAND-05-ACO-MICROPRICE-CHALLENGER` | secondary / exploratory | ACO | top-book pressure transform | microprice deviation | spread, inventory | direct signal challenger | microprice deviation | plausible but redundant challenger | corr with top imbalance about 0.959 | order-book pressure transform | do not stack with top imbalance | no | microprice compacts spread/size better than imbalance | microprice is one-axis challenger | must replace, not add to, top imbalance | redundant without PnL gain | one primary alternative feature | worth testing only against C04 | medium | low | high | medium | medium | validate-next | wave 3 | draft |
| `R2-CAND-06-ACO-FULL-BOOK-DEPTH-BACKUP` | exploratory | ACO | deeper book pressure | full-book imbalance or depth regime | spread, inventory | direct signal or defensive filter | full-book imbalance, depth regime | EDA positive but weaker than top-book | controlled/redundancy notes favor simpler top imbalance | liquidity/depth regimes | backup/context first | no | depth matters in wide or one-sided regimes | full-book imbalance is backup/context | depth levels are available enough online | added complexity without improvement | one depth feature only if promoted in spec | keep as triggerable backlog | medium | medium | medium | medium | medium | backlog | backlog | draft |
| `R2-CAND-07-COMBINED-IPR-ACO-IMBALANCE` | primary final-bot path | both | independent product edges | IPR drift FV plus ACO top imbalance | spread, inventory | direct product-specific modules | IPR drift plus residual; top imbalance | combines strongest product-specific evidence | cross-product lead-lag rejected, so modules stay independent | independent IPR trend/residual and ACO top-book pressure | one primary edge per product, no stack | no | product signals remain independent | product-specific first; combine only if simple | shared code can attribute product PnL | module interaction / inventory | one primary edge per product plus shared controls | best first final-bot path | strong | high | medium | medium/high | high | spec-first | wave 1 | draft |
| `R2-CAND-08-COMBINED-IPR-ACO-REVERSAL` | secondary final-bot challenger | both | independent product edges | IPR drift FV plus ACO reversal | spread, inventory | direct product-specific modules | IPR drift plus residual; ACO reversal | strong IPR plus ACO process evidence | cross-product lead-lag rejected, so modules stay independent | IPR trend/residual and ACO mean reversion | one primary edge per product, no stack | no | ACO reversal beats imbalance after execution | compare ACO process vs top-book pressure | same risk scaffolding as C07 | ACO execution cost | controlled challenger to C07 | high for IPR, medium/high for ACO | high | medium | medium/high | high | implement-first | wave 2 | draft |
| `R2-CAND-09-SPREAD-DEFENSIVE-OVERLAY` | secondary overlay | both | execution quality | spread regime | inventory | execution filter / risk control | spread regime | promoted filter candidate, not alpha | spread/relative spread redundancy favors one spread field | liquidity/execution regime | not a standalone alpha signal | no | bad regimes reduce markout quality | spread should be execution/risk filter | overlay must improve net PnL, not just reduce trades | over-filtering | no new alpha feature | useful overlay for champion/final specs | medium | low | high | low/medium | medium | validate-next | wave 2/3 | draft |
| `R2-CAND-10-MAF-BID-POLICY` | mechanics-only | Round 2 final | extra quote access | Market Access Fee bid policy | risk posture | round-specific mechanic | MAF scenario table | incremental proxy about 78-786 at threshold 0 depending capture rate | EDA-only calibration, not PnL proof | extra visible quotes may increase opportunities | not a `Trader.run()` alpha signal | n/a | final round accepts bid top 50 percent | MAF is separate mechanics/risk decision | competitor bids unknown | overpay or fail acceptance | separate mechanics policy | required before final submission posture | medium | low | low | medium/high | medium/high | spec-first | final mechanics | draft |

## Rejected Or Deferred Ideas

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| Cross-product lead-lag strategy | weak / unsupported | max absolute lead-lag correlation about 0.016; first-pass complexity not justified |
| Trade pressure proxy | needs logs | platform printed state did not expose enough `market_trades` dynamics |
| PCA / clustering / latent direct bot logic | not online-usable / too complex | EDA-only representation without reviewed online proxy |
| Fixed Round 1 IPR fair value | contradicted | Round 2 IPR drift evidence rejects stale fixed FV |
| Manual Research / Scale / Speed as bot feature | invalid boundary | separate manual challenge; must not influence `Trader.run()` logic |
| Top imbalance plus microprice feature stack | duplicate / feature dumping | correlation about 0.959; use one-axis challenger instead |

## Prioritized Candidate Queue

| Order | Candidate ID | Priority Tier | Implementation Wave | Why This Early / Later | Spec Action |
| --- | --- | --- | --- | --- | --- |
| 1 | `R2-CAND-07-COMBINED-IPR-ACO-IMBALANCE` | spec-first | wave 1 | best first final-bot path combining strongest product-specific evidence with no cross-product dependency | write spec first |
| 2 | `R2-CAND-01-IPR-DRIFT-FV-MAKER` | spec-first | wave 1 | isolates the strongest IPR evidence and protects against fixed-FV mistakes | write spec first |
| 3 | `R2-CAND-04-ACO-TOP-IMBALANCE-SKEW` | spec-first | wave 1 | strongest controlled ACO order-book evidence | write spec first |
| 4 | `R2-CAND-03-ACO-REVERSAL-MAKER` | spec-first | wave 1 | tests ACO process hypothesis directly | write spec first if time supports four specs |
| 5 | `R2-CAND-08-COMBINED-IPR-ACO-REVERSAL` | implement-first | wave 2 | controlled final-bot challenger to C07 with alternate ACO module | write after C03/C07 evidence |
| 6 | `R2-CAND-02-IPR-RESIDUAL-EXTREME-EXECUTION` | implement-first | wave 2 | useful if C01 overtrades or needs stricter entry | spec as variant or separate spec after C01 |
| 7 | `R2-CAND-09-SPREAD-DEFENSIVE-OVERLAY` | validate-next | wave 2/3 | overlay likely changes execution quality across candidates | add to specs/variants after base markouts |
| 8 | `R2-CAND-05-ACO-MICROPRICE-CHALLENGER` | validate-next | wave 3 | one-axis challenger to top imbalance | spec only after C04 baseline exists |
| 9 | `R2-CAND-10-MAF-BID-POLICY` | spec-first | final mechanics | must be decided before final Round 2 posture, but cannot be validated exactly now | include in final mechanics spec/risk decision |
| 10 | `R2-CAND-06-ACO-FULL-BOOK-DEPTH-BACKUP` | backlog | backlog | preserve only if top-book/spread validation exposes a weakness | defer until triggered |

## Implementation Sequence Recommendation

No bots are created in Phase 03. After reviewed specs:

1. Bot A: IPR-only drift FV maker, to isolate IPR edge.
2. Bot B: ACO-only top imbalance, to isolate ACO imbalance edge.
3. Bot C: ACO-only reversal, to compare ACO process hypothesis.
4. Bot D: combined IPR plus ACO imbalance, first final-bot candidate.
5. If validation remains ROI-positive: microprice challenger, combined reversal
   challenger, spread defensive overlay, and final MAF policy.

Implementation count should follow reviewed specs, differentiation, deadline
risk, and validation capacity. There is no fixed bot cap.

## Decision Trace

| Candidate | Signals Used | Alternatives Rejected Or Deferred | Reason For Priority | Caveat |
| --- | --- | --- | --- | --- |
| `R2-CAND-07-COMBINED-IPR-ACO-IMBALANCE` | IPR drift/residual, ACO top imbalance, spread | cross-product lead-lag, microprice stack | highest-value final-bot path with independent modules | combined bot still needs product attribution |
| `R2-CAND-01-IPR-DRIFT-FV-MAKER` | IPR drift/residual | fixed Round 1 FV | strongest single-product evidence and fastest isolation test | drift formula must be online-safe |
| `R2-CAND-04-ACO-TOP-IMBALANCE-SKEW` | top imbalance | microprice stack, full-book first | strongest controlled ACO order-book evidence | validate fills/spread capture |
| `R2-CAND-03-ACO-REVERSAL-MAKER` | previous mid delta reversal | broad volatility claim | direct test of ACO process hypothesis | adverse selection may dominate |
| `R2-CAND-10-MAF-BID-POLICY` | MAF scenarios | treating MAF as alpha | required Round 2 mechanics/risk decision | competitor bid distribution unknown |

## Exploration Stop Rule

- Stop reason: enough high-ROI differentiated candidates exist to move to specs;
  additional branches would mostly be duplicate, weak, or log-blocked.
- Low-ROI branching signals: `duplicate ideas`, `weak evidence`,
  `implementation/validation bottleneck`, `needs logs`.
- Ready to write specs: `yes`, after human review of this candidate queue.

## Human Checkpoint

| Decision Needed | Default If No Answer | Options | Why It Matters |
| --- | --- | --- | --- |
| MAF risk posture | base/conservative scenario from EDA, deferred until final mechanics spec | low bid / base bid / aggressive bid / no bid | affects `Trader.bid()` final-round behavior |
| Manual RSS allocation | keep manual-only scenario table for later review | pessimistic / linear / optimistic / custom | separate challenge; not needed for bot specs |

## Next Action

- Human review outcome: approved with caveats on 2026-04-19.
- Phase 04 specs were created for all 10 candidates.
- Do not implement bots until specs are reviewed or explicitly deferred under
  deadline pressure.
