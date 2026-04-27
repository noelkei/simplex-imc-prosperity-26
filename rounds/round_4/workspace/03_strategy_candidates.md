# Strategy Candidates

Use [`docs/templates/strategy_candidates_template.md`](../../../docs/templates/strategy_candidates_template.md) as the structure for this file.

Candidate count is ROI-driven, not fixed. For `round_4`, the first
implementation wave is intentionally set to `15` exploration bots so we can
test the genuinely new information layer in this round, re-check what still
works from `round_3`, and isolate which paper-inspired ideas deserve to survive
into later waves.

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts:
  - [`../../../docs/prosperity_wiki/rounds/round_4.md`](../../../docs/prosperity_wiki/rounds/round_4.md)
- Understanding summary:
  - [`02_understanding.md`](02_understanding.md)
- External paper research:
  - [`02b_external_paper_research.md`](02b_external_paper_research.md)
  - [`02b_strategy_handoff.md`](02b_strategy_handoff.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
  - [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
  - [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
  - [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- Post-run research memory:
  - [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)
- Playbook heuristics:
  - none required as primary evidence

## Carry-Forward Ledger

Separate what is already learned from what still needs proof.

### Validated carry-forward principles

| Principle | Source Artifact | Why It Still Matters | Current-Round Revalidation Need |
| --- | --- | --- | --- |
| `delta-1 first` remains the cleanest starting architecture | `02_understanding.md`, `round_3` memory | best-supported base family and best control for new overlays | light |
| `VEX` is the primary same-time voucher anchor | `02_understanding.md`, EDA | strongest current-round structural linkage | none |
| the voucher book is role-first, not a homogeneous basket | `02_understanding.md`, `round_3` closeout | strike behavior diverges sharply by role and friction | none |
| counterparties are context first, not naked alpha first | `02_understanding.md`, EDA | strongest new round fact, but mostly contextual so far | light |
| `5300` is special and should not be treated as a generic active leg | `02_understanding.md`, `round_3` memory | only active strike with real carry-forward interest | full |
| upper/floor strikes should stay out of default aggressive trading | `02_understanding.md`, EDA | friction and tradability remain too poor | light |

### Untested hypotheses

| Hypothesis | Origin | Why It Is Still Interesting | Clean Test Needed |
| --- | --- | --- | --- |
| `5200` is better as signal-only / veto than as inventory | `round_3` closeout + `round_4` EDA | strongest new counterparty danger-state story | yes |
| `5300` needs a slower horizon and explicit no-new-entry logic | `round_3` memory + `round_4` EDA | markout shape and specialness still support it | yes |
| family imbalance / family pressure adds value over symbol-local logic | `round_3` unresolved backlog + `02b` | linked option-book framing now has better paper support | yes |
| counterparty concentration beats raw-name logic | `round_4` EDA + `02b` | direct round novelty with better-than-raw explanatory value | yes |
| ITM overlay quality changes under counterparty-conditioned filtering | `round_3` winner family + `round_4` EDA | tests whether the old winner survives or improves in the new tape | yes |
| lightweight surface sanity can prevent fake residual entries | `round_4` EDA + `02b` | could improve selectivity without heavy runtime | yes |

### Default anti-patterns

| Anti-Pattern | Evidence Source | Why To Avoid | Reopen Only If |
| --- | --- | --- | --- |
| broad `5000/5100/5200/5300` active basket as default architecture | `round_3` closeout, `02_understanding.md` | repeated toxic strike mix and poor retention | a new isolated branch proves otherwise |
| raw buyer/seller name alpha | `round_4` EDA | raw names add weak explanatory value alone | interaction-driven evidence becomes much stronger |
| trading `5100/5200` as normal inventory by default | `round_3` memory, `round_4` EDA | best current evidence says danger-state / anti-signal | isolated clean winners appear |
| heavy Heston / COS live machinery | `round_4` EDA, `02b` | complexity outruns evidence and runtime realism | later spec defines a tiny online proxy with clear lift |
| feature-dump candidates with many correlated context signals | workflow + EDA model ladder | will hide attribution and slow validation | one added feature clearly changes decisions |

## Paper Intake Pass

| Paper ID | Current-Round Mapping | Strategy Use | Candidate Impact | Note |
| --- | --- | --- | --- | --- |
| `doshi_2025_risky_intraday_order_flow` | unstable-flow danger-state in `5200+` | used | changes candidate design | strongest support for no-trade / defensive gating |
| `vasios_2015_mimicking_non_anonymous` | visible-participant flow as context | used | changes candidate design | best support for non-anonymous context features |
| `cartea_2018_order_book_signals` | trade-to-book and imbalance execution filtering | used | changes candidate design | strongest lightweight execution overlay |
| `kaeck_2019_informed_index_options` | family / cross-strike flow framing | used | changes candidate design | supports linked-book candidates |
| `bollen_whaley_2004_net_buying_pressure` | flow-distorted surface / residual caution | validation | validation only | prevents overreading residuals |
| `goncalves_pinto_sala_2025_incremental_option_volume` | baseline-vs-context discipline | validation | validation only | forces incremental-value testing |
| `nimalendran_son_2024_cream_skimming_toxic_flow` | toxic vs liquidity-harvesting participant behavior | validation | rejection logic | sharpens danger-state interpretation |
| `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | family-demand distortion | hybrid | changes candidate design | supports family-pressure overlay ideas |
| `roos_2026_arbitrage_free_interpolation` | surface sanity / residual support | inspiration-only | validation only | keep offline / proxy-first |
| `muravyev_2015_option_order_flow` | inventory pressure vs information | hybrid | changes candidate design | useful secondary carry-forward |
| `stoikov_saglam_2009_option_mm_inventory` | short-dated inventory-risk quoting | hybrid | changes candidate design | good support for quote-tilt overlays |
| `bergault_2022_multi_asset_mm` | family exposure control | validation | validation only | use for exposure framing, not primary alpha |
| `choi_2022_bachelier_guide` | simple pricing backbone and Greeks | hybrid | changes candidate design | supports simple pricing choices |
| `fengler_2005_surface_smoothing` | surface sanity guard | validation | validation only | strong warning against noisy kinks |
| `garcia_ares_2023_expiration_days` | near-expiry timing caution | validation | validation only | supports horizon-aware and no-new-entry tests |

## Feature Budget

Strategies should be feature-light by default.

- Wave 1 is fixed at `15` exploration bots by user direction, but each bot
  still gets at most:
  - `1` primary edge feature or fair-value model
  - up to `2` supporting execution / risk filters
- Whenever possible, a new bot should differ from its nearest control on one
  major axis only:
  - product role
  - counterparty context
  - execution filter
  - horizon rule
  - family-state overlay
- Any idea that needs more than this budget is deferred out of Wave 1.
- Every serious candidate keeps a visible trace:

```text
feature -> signal -> decision -> expected edge -> validation check
```

## Candidate Count And Roles

- Wave 1 is intentionally set to `15` exploration bots.
- Roles:
  - `primary`: strongest architecture or control candidates
  - `secondary`: high-ROI overlays and conditional branches
  - `exploratory`: lower-confidence but still useful clean tests
  - `deferred` / `rejected`: recorded but not in Wave 1
- All `15` candidates belong to `wave 1`; the queue order below defines spec
  and implementation order inside that wave.

## Round Coverage Check

| Item | Source | Candidate Impact | Decision |
| --- | --- | --- | --- |
| `Trade.buyer` / `Trade.seller` are now visible | round doc + EDA | affects edge / execution / validation | use |
| same algorithmic products as `round_3` | round doc + prior-round intake | affects carry-forward reuse | use |
| manual products remain out of scope for bot wave | wiki + understanding | affects strategy scope | exclude |
| `VEX` remains strongest voucher anchor | understanding | affects edge / execution | use |
| sparse tape in `4500/5000/5100` | understanding | affects validation and product choice | use cautiously |
| `5200+` concentrated seller-state risk | understanding + EDA | affects risk / execution | use |
| no `round_4` run evidence yet | understanding | affects validation posture | use |

## Exploration Board

| Idea ID | Product | Source Signal | Primary Feature / Signal | Supporting Features | Process Hypothesis | Online Proxy Needed? | Approach | Expected Edge | Main Risk | Implementation Realism | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B01` | `VEX` | clean anchor process | local delta-1 maker edge | spread, imbalance | liquid anchor process | no | control | clean base | low upside ceiling | high | candidate |
| `B02` | `HYDRO` | clean independent process | local delta-1 maker edge | spread, imbalance | independent delta-1 process | no | control | clean base | may add little to later stacks | high | candidate |
| `B03` | `VEX + 4000` | ITM structural role | `4000` overlay trigger | spread, role gate | structural overlay | no | selective overlay | additive edge | low incremental lift | high | candidate |
| `B04` | `VEX + 5300` | `5300` specialness | `5300` anchor overlay | spread, role gate | slower active strike | no | selective overlay | retained active edge | giveback | medium/high | candidate |
| `B05` | `5200+` context | `Mark 22` seller danger-state | participant veto | spread/depth deterioration | unstable flow hurts inventory | no | defensive gate | avoid bad states | identity overfit | high | candidate |
| `B06` | voucher family | concentration / dominance | concentration gate | `VEX` anchor, spread | contextual state > raw names | no | defensive gate | filter weak states | may redescribe bad products | high | candidate |
| `B07` | `VEX + vouchers` | trade-to-book context | book-state execution overlay | concentration, spread | adverse fills matter | no | execution overlay | better fill quality | over-shutdown | high | candidate |
| `B08` | family | family pressure hypothesis | family imbalance / pressure | role split, `VEX` | linked-book state | yes | context overlay | better branch timing | proxy quality weak | medium | candidate |
| `B09` | `VEX + 5300` | toxic neighbors | `5300` only when `5100/5200` quiet | `Mark 22`, spread | anti-signal neighbors matter | no | gated overlay | keep only cleaner `5300` trades | too conditional | high | candidate |
| `B10` | family | `5200` signal-only role | `5200` veto monitor | `Mark 22`, family state | toxic strike as monitor | no | monitor / veto | cleaner rest-of-book entries | no direct monetization | high | candidate |
| `B11` | `VEX + 5300` | horizon/giveback | longer hold + no-new-entry | giveback cutoff | `5300` is not a fast scalp | no | horizon redesign | retain more of the path | sample risk | high | candidate |
| `B12` | `5400/5500` | upper passive regime | passive-only quote probe | spread, concentration | passive upper may still be informative | no | exploratory probe | passive edge or clean exclusion | no fills | medium | candidate |
| `B13` | `VEX + 4000` | benign-flow ITM | `4000` only under benign counterparty state | trade-location, concentration | old winner improves with better execution context | no | conditioned overlay | cleaner ITM add-on | too little change | high | candidate |
| `B14` | voucher overlays | surface sanity | neighbor-strike residual filter | `VEX`, demand-distortion guard | cheap residual sanity can help | yes | pricing filter | avoid fake residual trades | complexity without lift | medium | candidate |
| `B15` | `VEX + 4000` family | round-3 winner revalidation | old winner stack plus round-4 defensive context | `Mark 22` veto, trade-to-book | old winner may improve under new tape | no | hybrid revalidation | best all-around exploration candidate | attribution ambiguity | high | candidate |
| `B16` | broad active basket | old basket | `5000/5100/5200/5300` composite | many | basket mean reversion | no | reopen | broad upside | repeated toxicity | high | prune |
| `B17` | vouchers | raw-name alpha | naked buyer/seller names | none | names alone are enough | no | direct alpha | simple novelty | weak evidence | high | prune |
| `B18` | vouchers | heavy pricing stack | Heston/COS live logic | Greeks, calibration | richer pricing creates edge | yes | full quant stack | cleaner surface edge | low runtime ROI | low | prune |

## Per-Product Branches

| Product | Top Branches | Strongest Signal | Weakest Assumption | Pruning Note |
| --- | --- | --- | --- | --- |
| `HYDRO` | `r4_s02_hydro_base_control` | clean delta-1 process | usefulness inside later combos | keep as control, not as mandatory combo leg |
| `VEX` | `r4_s01_vex_base_control`, `r4_s15_round3_winner_revalidation` | same-time anchor and clean delta-1 base | standalone alpha size vs pure anchor role | keep as central branch |
| `VEV_4000` | `r4_s03_vex_4000_overlay`, `r4_s13_4000_benign_flow_overlay`, `r4_s15_round3_winner_revalidation` | ITM structural overlay | incremental value size | keep in low-complexity overlay space |
| `VEV_4500` | none in Wave 1 | quote structure only | tape too sparse | deprioritize |
| `VEV_5000/5100` | `r4_s09_5300_toxic_strike_gate` as anti-signal context | strongest use is as danger-state context | could still hide value | keep out of direct inventory logic |
| `VEV_5200` | `r4_s05_mark22_veto_gate`, `r4_s10_5200_signal_only_veto` | clearest danger-state story | could be sparse artifact | test as signal-only, not inventory |
| `VEV_5300` | `r4_s04_vex_5300_overlay`, `r4_s09_5300_toxic_strike_gate`, `r4_s11_5300_horizon_hold` | special active strike | retained edge not proven | keep separate from the basket |
| `VEV_5400/5500` | `r4_s12_upper_passive_probe` | passive upper regime only | fills may be zero | low-priority exploratory only |

## Combination / Compatibility Matrix

| Pairing | Compatibility | Risk Interaction | Execution Alignment | Cross-Product Dependency | Verdict |
| --- | --- | --- | --- | --- | --- |
| `VEX + VEV_4000` | high | manageable | aligned | useful | move forward |
| `VEX + VEV_5300` | high | medium | mixed but acceptable | useful | move forward |
| `VEX + 5200 signal-only veto` | high | low | aligned | useful | move forward |
| `HYDRO + voucher overlays` | low | mixed | mixed | weak | backup |
| `VEV_4000 + VEV_5300` | medium | medium | mixed | useful | backup |
| `VEX + upper passive probe` | medium | low | aligned | weak | backup |

## Candidate Table

| Candidate ID | Role | Source Classification | Product Scope | Source Of Edge | Primary Feature / Signal | Supporting Features | Feature Role | Lifecycle Label | Metric Availability | Baseline / Richer Verdict | Linked EDA Signals | Feature Evidence | External Research Input | Paper Idea Handling | Multivariate Evidence | Supporting Process Hypothesis | Redundancy Note | Online Proxy Needed? | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Why Not Feature Dumping | ROI / Pruning Rationale | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority Tier | Implementation Wave | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_s01_vex_base_control` | primary | data-driven | `VEX` | clean delta-1 anchor process | `VEX` local maker edge | spread gate, imbalance gate | direct signal | implementation candidate | implemented | baseline only | `VEX_anchor_same_time` | low spread + strong carry-forward | none | none | none needed | liquid anchor process | keep | no | normal `VEX` liquidity | `delta-1 base` default | clean base still matters | modest upside ceiling | one edge + two filters | required control for every overlay | strong | low | high | low | medium-high | spec-first | wave 1 | prioritized |
| `r4_s02_hydro_base_control` | primary | data-driven | `HYDRO` | clean independent delta-1 process | `HYDRO` local maker edge | spread gate, imbalance gate | direct signal | implementation candidate | implemented | baseline only | `HYDRO` independence | isolated branch positive in `round_3` | none | none | none needed | independent delta-1 process | keep | no | normal `HYDRO` liquidity | separate delta-1 branch | isolated HYDRO still has value | may add little to later stacks | one edge + two filters | required independent control | strong | low | high | low | medium | spec-first | wave 1 | prioritized |
| `r4_s03_vex_4000_overlay` | secondary | hybrid | `VEX + VEV_4000` | ITM structural add-on | `4000` VEX-anchored overlay | strike-role gate, spread filter | direct signal | implementation candidate | implemented | richer adds value | `option_book_role_split`, `VEX_anchor_same_time` | `4000` tape + anchor linkage | `carry_forward/choi_2022_bachelier_guide_processed.md` | hybrid | low redundancy vs base | ITM structural overlay | keep | no | benign ITM spread state | ITM remains best additive overlay candidate | `4000` can add without dominating | low incremental lift | one overlay + two simple filters | direct test of old winner ingredient | medium-high | low | high | medium | medium-high | spec-first | wave 1 | prioritized |
| `r4_s04_vex_5300_overlay` | secondary | hybrid | `VEX + VEV_5300` | special active-strike overlay | `5300` VEX-anchored overlay | strike-role gate, spread filter | direct signal | implementation candidate | implemented_as_proxy_only | richer adds value | `5300` specialness, `VEX_anchor_same_time` | `5300` role divergence + carry-forward interest | `kaeck_2019_informed_index_options_processed.md` | used | role-aware and cross-strike aware | slower active strike | keep | no | `5300` only in cleaner states | `5300` is special, not generic | `5300` still has retained-edge potential | edge then reversal | one overlay + two filters | essential active-strike baseline re-test | medium-high | low-medium | medium | medium-high | high | spec-first | wave 1 | prioritized |
| `r4_s05_mark22_veto_gate` | primary | hybrid | `VEX + voucher context` | adverse-selection avoidance | `Mark 22` seller veto in `5200+` | spread/depth deterioration, `VEX` anchor | risk control | implementation candidate | implemented | richer adds value | `mark22_seller_danger_state` | seller dominance + adverse markout | `doshi_2025_risky_intraday_order_flow_processed.md`, `vasios_2015_mimicking_non_anonymous_processed.md` | used | identity only survives with context | unstable-flow danger state | keep | no | persistent seller-state in upper-middle strikes | counterparties are context first | visible names are stable enough short-term | identity overfit | one veto + one market-state check | strongest new round-4 test axis | medium-high | low | high | medium-high | high | spec-first | wave 1 | prioritized |
| `r4_s06_counterparty_concentration_gate` | secondary | hybrid | selective `VEV_*` overlays | contextual state filter | concentration / dominance state | `VEX` anchor, spread state | execution filter | implementation candidate | implemented | richer adds value | `counterparty_concentration_context`, `engineered_context_over_raw_names` | model ladder + concentration stability | `vasios_2015_mimicking_non_anonymous_processed.md`, `goncalves_pinto_sala_2025_incremental_option_volume_processed.md` | hybrid | model ladder and stability scoring | concentrated-flow regime | merge raw names into buckets | no | concentrated strike state | engineered context beats naked names | concentration adds usable state | may just redescribe bad products | one state + two controls | clean way to test context > raw names | medium-high | low | high | medium | medium-high | implement-first | wave 1 | prioritized |
| `r4_s07_trade_to_book_execution_overlay` | primary | hybrid | `VEX + selective vouchers` | execution improvement | trade-location / book-state context | concentration state, spread state | execution filter | implementation candidate | implemented | richer adds value | `trade_location_context` | book-state and markout evidence | `cartea_2018_order_book_signals_processed.md`, `doshi_2025_risky_intraday_order_flow_processed.md` | used | book context is independent enough | bad-book-state execution risk | keep | no | poor local book states are toxic | execution should be first-class | fill quality improves if we gate book state | over-shutdown | one execution edge + two supports | highest-ROI microstructure overlay | medium-high | low | high | medium | high | spec-first | wave 1 | prioritized |
| `r4_s08_family_pressure_overlay` | exploratory | hybrid | voucher family + `VEX` | linked-book family state | family pressure / family imbalance | role split, `VEX` anchor | regime feature | implementation candidate | partially_available | not checked | family framing, linked-book verdict | unresolved carry-forward + paper support | `kaeck_2019_informed_index_options_processed.md`, `garleanu_pedersen_poteshman_2005_demand_based_option_pricing_processed.md`, `carry_forward/bergault_2022_multi_asset_mm_processed.md` | hybrid | cross-product useful but untested | linked option-book state | keep if simple proxy exists | yes | family state matters more than symbol-only state | family framing is still unresolved | simple family proxy is enough | proxy quality may be weak | one family state + two supports | high learning value even if weak | medium | medium | medium | medium | medium-high | validate-next | wave 1 | prioritized |
| `r4_s09_5300_toxic_strike_gate` | secondary | hybrid | `VEX + VEV_5300` with `5100/5200` context | cross-strike anti-signal gating | `5300` only when `5100/5200` are quiet | `Mark 22` state, spread state | direct signal | implementation candidate | implemented | richer adds value | `5300` specialness, toxic-neighbor context | `5100/5200` danger-state carry-forward | `doshi_2025_risky_intraday_order_flow_processed.md`, `nimalendran_son_2024_cream_skimming_toxic_flow_processed.md` | hybrid | cross-strike context materially useful | anti-signal neighbors matter | keep | no | toxic-neighbor regime is observable | `5300` should be isolated and gated | anti-signals actually improve `5300` quality | too conditional / low trade count | one overlay + two anti-signal filters | directly tests key carry-forward hypothesis | medium-high | medium | medium | medium-high | high | implement-first | wave 1 | prioritized |
| `r4_s10_5200_signal_only_veto` | exploratory | data-driven | family context, no `5200` trading | signal-only monitor | `5200` danger-state monitor | `Mark 22`, family state | monitor | implementation candidate | implemented | richer adds value | `mark22_seller_danger_state`, `counterparty_concentration_context` | strongest current danger-state story | `nimalendran_son_2024_cream_skimming_toxic_flow_processed.md` | validation | likely signal-only not inventory | toxic strike as monitor | keep | no | `5200` activity reveals bad family state | `5200` may be better as veto only | signal-only use is enough | no direct monetization | one monitor + two supports | direct test of major unresolved hypothesis | medium-high | low | high | low-medium | medium | implement-first | wave 1 | prioritized |
| `r4_s11_5300_horizon_hold` | secondary | hybrid | `VEX + VEV_5300` | retention / hold redesign | longer `5300` hold horizon | no-new-entry-after, giveback cutoff | direct signal | implementation candidate | implemented | richer adds value | `5300` specialness, late-entry risk | markout horizon shape from carry-forward | `carry_forward/garcia_ares_2023_expiration_days_processed.md` | validation | process/horizon evidence matters | `5300` is not a fast scalp | keep | no | later-session gating matters product-specifically | `5300` needs horizon-aware design | small sample still indicative | may undertrade | one horizon axis + two controls | tests edge-then-reversal rather than no-edge | medium-high | low-medium | medium | medium | medium-high | implement-first | wave 1 | prioritized |
| `r4_s12_upper_passive_probe` | exploratory | data-driven | `VEV_5400/5500` | passive upper microstructure probe | passive-only upper quote posture | spread threshold, dominance avoidance | direct signal | implementation candidate | implemented | baseline only | `upper_floor_exclusion` | upper movement exists but tradability weak | none | none | weak cross-strike support | passive upper regime | keep as low-priority probe | no | extreme friction but possible passive niche | upper branch remains research-only | may produce zero fills | one posture + two filters | cheap way to close or rescue upper branch | weak-medium | low | high | medium | low-medium | validate-next | wave 1 | prioritized |
| `r4_s13_4000_benign_flow_overlay` | secondary | hybrid | `VEX + VEV_4000` | old winner ingredient under new context | `4000` only in benign flow state | trade-location, concentration filter | direct signal | implementation candidate | implemented | richer adds value | `4000` overlay + counterparty context | old winner plus new tape conditioning | `vasios_2015_mimicking_non_anonymous_processed.md`, `doshi_2025_risky_intraday_order_flow_processed.md`, `carry_forward/choi_2022_bachelier_guide_processed.md` | hybrid | context should improve additive overlay | ITM overlay under benign execution state | keep | no | counterparty state affects add-on quality | old winner may improve under new info | may be too similar to plain 4000 overlay | one overlay + two context filters | direct test of whether counterparties improve the old winner | medium-high | low | high | medium | medium-high | implement-first | wave 1 | prioritized |
| `r4_s14_surface_sanity_filter` | exploratory | paper-inspired | selective voucher overlays | residual quality filter | neighbor-strike surface sanity | `VEX` anchor, demand-distortion guard | diagnostic | implementation candidate | partially_available | richer low ROI unless simple | `surface_awareness_not_flat_vol` | surface layer matters but only as framing | `roos_2026_arbitrage_free_interpolation_processed.md`, `bollen_whaley_2004_net_buying_pressure_processed.md`, `carry_forward/fengler_2005_surface_smoothing_processed.md` | inspiration-only | residual evidence is mostly supportive | cheap local surface sanity | keep only if tiny proxy exists | yes | sparse/noisy quote kinks can mislead | simplified pricing support only | complexity without enough lift | one filter + two sanity guards | worthwhile only as a compact test | medium | medium | medium | medium | medium | validate-next | wave 1 | prioritized |
| `r4_s15_round3_winner_revalidation` | primary | hybrid | `VEX + VEV_4000` plus round-4 filters | old winner family under new info | round-3 winner stack with round-4 danger filters | `Mark 22` veto, trade-to-book gate | direct signal | implementation candidate | implemented | richer adds value | `VEX_anchor_same_time`, `4000` overlay, danger-state context | strongest carry-forward architecture + new filters | `carry_forward/stoikov_saglam_2009_option_mm_inventory_processed.md`, `carry_forward/muravyev_2015_option_order_flow_processed.md`, `doshi_2025_risky_intraday_order_flow_processed.md`, `vasios_2015_mimicking_non_anonymous_processed.md` | hybrid | blend of carry-forward and new state | winner protection / revalidation | keep despite composite nature | no | old winner still best starting family | round-3 winner may survive or improve | attribution can blur | one old winner edge + two new filters | highest-ROI question from carry-forward side | strong | medium | high | medium | high | spec-first | wave 1 | prioritized |

## Derivative / Linked-Product Framing

| Candidate ID | Product Role | Signal Class | Underlying Role | Trading Posture | Natural Hold Horizon | Giveback Prevention Rule | Cross-Product Dependency | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r4_s01_vex_base_control` | delta-1 | microstructure | alpha and anchor | passive / conditional | scalp / short hold | spread + imbalance discipline | low | base control |
| `r4_s02_hydro_base_control` | delta-1 | microstructure | alpha | passive / conditional | scalp / short hold | spread + imbalance discipline | none | independent control |
| `r4_s03_vex_4000_overlay` | ITM structural | valuation / regime | anchor | conditional | short / medium hold | role gate and spread filter | high | low-complexity overlay |
| `r4_s04_vex_5300_overlay` | active risk leg | valuation / regime | anchor | conditional | short / medium hold | spread gate and strike isolation | high | special strike branch |
| `r4_s05_mark22_veto_gate` | monitor / veto | microstructure / regime | anchor | no-trade when active | session state | hard veto on bad participant state | medium | explicit round-4 novelty |
| `r4_s06_counterparty_concentration_gate` | monitor / veto | regime | anchor | conditional | session state | concentration threshold | medium | engineered-context branch |
| `r4_s07_trade_to_book_execution_overlay` | execution overlay | microstructure | anchor | passive / conditional | short hold | no-trade in bad book state | medium | execution-first branch |
| `r4_s08_family_pressure_overlay` | family context | regime / surface | anchor | conditional | session state | family-state filter | high | linked-book hypothesis test |
| `r4_s09_5300_toxic_strike_gate` | active risk leg | regime / microstructure | anchor | conditional | short / medium hold | neighbor anti-signal veto | high | direct strike-pruning test |
| `r4_s10_5200_signal_only_veto` | monitor | regime | anchor | no-trade context | session state | `5200` veto only | medium | signal-only hypothesis |
| `r4_s11_5300_horizon_hold` | active risk leg | regime | anchor | conditional | medium hold | no-new-entry-after + giveback cutoff | high | retention-focused branch |
| `r4_s12_upper_passive_probe` | upper passive leg | microstructure | anchor or none | passive only | short hold | passive-only discipline | medium | research-only upper probe |
| `r4_s13_4000_benign_flow_overlay` | ITM structural | valuation / microstructure | anchor | conditional | short / medium hold | benign-flow filter | high | old winner ingredient under new tape |
| `r4_s14_surface_sanity_filter` | support layer | surface | anchor | conditional | session state | residual sanity reject | high | support-only if simple |
| `r4_s15_round3_winner_revalidation` | delta-1 + ITM hybrid | mixed | anchor and alpha | conditional | short / medium hold | veto + execution overlay | high | direct carry-forward revalidation |

## Rejected Or Deferred Ideas

| Idea | Source Classification | Paper Idea Handling | Reason | Evidence Gap Or Risk |
| --- | --- | --- | --- | --- |
| broad `5000/5100/5200/5300` active basket reopen | data-driven | rejected | repeated strike-mix toxicity and poor retention | needs genuinely new evidence |
| raw-name alpha bot | paper-rejected | rejected | raw names alone are weak and overfit-prone | needs much stronger incremental value |
| `5100` direct inventory branch | data-driven | rejected | sparse/tactical anti-signal only for now | needs isolated positive evidence |
| full Heston / COS live logic | paper-inspired | rejected | runtime complexity too high for current support | needs tiny online proxy and clear lift |
| pair-recurrence direct trigger bot | data-driven | deferred | too sample-sensitive under 3-day tape | needs stronger run evidence |
| manual / algorithmic mixed strategy branch | data-driven | deferred | manual scope is out of lane | needs manual contract detail |

## Prioritized Candidate Queue

| Order | Candidate ID | Priority Tier | Implementation Wave | Why This Early / Later | Spec Action |
| --- | --- | --- | --- | --- | --- |
| 1 | `r4_s15_round3_winner_revalidation` | spec-first | wave 1 | highest-ROI carry-forward revalidation under new tape | write spec |
| 2 | `r4_s01_vex_base_control` | spec-first | wave 1 | core anchor control for all voucher overlays | write spec |
| 3 | `r4_s02_hydro_base_control` | spec-first | wave 1 | independent delta-1 control and architecture check | write spec |
| 4 | `r4_s05_mark22_veto_gate` | spec-first | wave 1 | strongest direct round-4 novelty test | write spec |
| 5 | `r4_s07_trade_to_book_execution_overlay` | spec-first | wave 1 | strongest execution overlay from EDA + papers | write spec |
| 6 | `r4_s03_vex_4000_overlay` | spec-first | wave 1 | clean ITM structural re-check | write spec |
| 7 | `r4_s04_vex_5300_overlay` | spec-first | wave 1 | clean special-strike re-check | write spec |
| 8 | `r4_s06_counterparty_concentration_gate` | implement-first | wave 1 | best engineered-context test after identity veto | write spec |
| 9 | `r4_s13_4000_benign_flow_overlay` | implement-first | wave 1 | tests whether new tape improves old winner ingredient | write spec |
| 10 | `r4_s09_5300_toxic_strike_gate` | implement-first | wave 1 | tests anti-signal gating on the only serious active strike | write spec |
| 11 | `r4_s11_5300_horizon_hold` | implement-first | wave 1 | tests `edge then reversal` rather than pure signal failure | write spec |
| 12 | `r4_s10_5200_signal_only_veto` | implement-first | wave 1 | tests signal-only role cleanly without direct inventory | write spec |
| 13 | `r4_s08_family_pressure_overlay` | validate-next | wave 1 | high learning value but proxy quality less certain | write spec |
| 14 | `r4_s12_upper_passive_probe` | validate-next | wave 1 | closes or rescues upper branch cheaply | write spec |
| 15 | `r4_s14_surface_sanity_filter` | validate-next | wave 1 | useful only if a very small proxy is possible | write spec |

## Decision Trace

| Candidate | Signals Used | Alternatives Rejected Or Deferred | Reason For Priority | Caveat |
| --- | --- | --- | --- | --- |
| `r4_s15_round3_winner_revalidation` | `VEX` anchor, `4000` overlay, danger-state context | broad basket reopen, raw-name alpha | best single test of whether the old winner survives or improves | attribution can blur |
| `r4_s01_vex_base_control` | `VEX` base microstructure | none | required base control for every overlay branch | may not be final winner |
| `r4_s02_hydro_base_control` | `HYDRO` base microstructure | HYDRO inside composites | required independent control and carry-forward check | may be lower upside |
| `r4_s05_mark22_veto_gate` | `Mark 22` seller-state | raw-name alpha bot | cleanest direct round-4 novelty test | identity persistence risk |
| `r4_s07_trade_to_book_execution_overlay` | trade-location, imbalance, spread | pure pricing complexity | strongest execution-only overlay | could over-shut down |
| `r4_s03_vex_4000_overlay` | ITM structural role | passive standalone ITM | tests the most credible additive overlay | may be too small |
| `r4_s04_vex_5300_overlay` | `5300` specialness | broad active basket | tests active strike value in isolation | retention risk |
| `r4_s06_counterparty_concentration_gate` | concentration / dominance state | raw-name logic | tests engineered context over naked names | may just mirror bad products |
| `r4_s13_4000_benign_flow_overlay` | ITM overlay + benign context | plain `4000` overlay only | tests whether new info upgrades the old add-on | may be too similar to `r4_s03` |
| `r4_s09_5300_toxic_strike_gate` | `5300` plus toxic-neighbor quiet state | plain `5300` overlay | tests cross-strike anti-signal framing | may be too conditional |
| `r4_s11_5300_horizon_hold` | `5300` horizon shape | fast-unwind style rescue | tests retention-specific redesign | sample still small |
| `r4_s10_5200_signal_only_veto` | `5200` as monitor only | `5200` direct inventory branch | cleanest test of signal-only role | no direct monetization |
| `r4_s08_family_pressure_overlay` | family pressure / imbalance | symbol-local only logic | useful linked-book test once basics are covered | proxy risk |
| `r4_s12_upper_passive_probe` | upper passive regime | upper direct aggression | cheap way to confirm or close upper branch | likely zero fills |
| `r4_s14_surface_sanity_filter` | local surface sanity | full Heston/COS logic | smallest possible pricing-support test | easy to add low-value complexity |

## Exploration Stop Rule

- Stop reason:
  the candidate queue already covers the highest-ROI current-round differences:
  clean controls, counterparty novelty, cross-strike gating, retention logic,
  family context, upper passive probe, and lightweight pricing support.
- Low-ROI branching signal:
  `duplicate ideas | weak evidence | likely feature dumping | broad basket reopening | heavy runtime complexity`
- Ready to write specs: `yes`

## Human Checkpoint

No checkpoint required. The user has already chosen the key prioritization
decision for this phase: the first implementation wave should contain `15`
exploration bots.

## Wave 1 Learning Matrix

This wave is not trying to pick an immediate final winner. It is designed to
answer the highest-ROI `round_4` questions quickly and with clean controls.

| Candidate ID | Main Question | Nearest Control | Success Signal | Failure Interpretation |
| --- | --- | --- | --- | --- |
| `r4_s15_round3_winner_revalidation` | does the best `round_3` family survive the new tape if we add defensive context? | `r4_s01`, `r4_s03` | beats both plain base and plain `4000` overlay with cleaner path | old winner no longer survives or new context over-shuts it |
| `r4_s01_vex_base_control` | how strong is plain `VEX` now as the anchor baseline? | none | stable positive control and clean path quality | anchor still useful, but not enough alone |
| `r4_s02_hydro_base_control` | does `HYDRO` still deserve independent attention or is `VEX` clearly better? | `r4_s01` | distinct positive behavior, not just weaker duplicate | `HYDRO` is a lower-value control only |
| `r4_s05_mark22_veto_gate` | is visible `Mark 22` seller flow a real danger-state veto? | `r4_s01`, `r4_s04` | fewer bad entries and better markout/fill quality | identity story is too unstable or too product-specific |
| `r4_s07_trade_to_book_execution_overlay` | does trade-to-book context improve execution on otherwise similar logic? | `r4_s01`, `r4_s15` | path improvement with similar or slightly lower trade count | book-state overlay is descriptive only |
| `r4_s03_vex_4000_overlay` | does the plain ITM structural overlay still add value? | `r4_s01` | incremental improvement over base with tolerable risk | `4000` no longer improves enough in `round_4` |
| `r4_s04_vex_5300_overlay` | does isolated `5300` still deserve active attention? | `r4_s01` | positive incremental edge without toxic churn | `5300` specialness is not monetizable directly |
| `r4_s06_counterparty_concentration_gate` | do engineered participant-state features beat raw-name stories? | `r4_s01`, `r4_s05` | improves decisions without depending on one identity | concentration mostly just mirrors bad products |
| `r4_s13_4000_benign_flow_overlay` | does benign-flow conditioning improve the old ITM add-on? | `r4_s03` | cleaner overlay than plain `4000` | context adds little beyond the plain role-based overlay |
| `r4_s09_5300_toxic_strike_gate` | do toxic-neighbor states explain when `5300` should be suppressed? | `r4_s04`, `r4_s11` | better `5300` selectivity than ungated variants | neighbor veto is too conditional or redundant |
| `r4_s11_5300_horizon_hold` | is `5300` mainly a horizon problem rather than a signal problem? | `r4_s04`, `r4_s09` | stronger retention and less giveback | `5300` issue is not primarily hold design |
| `r4_s10_5200_signal_only_veto` | should `5200` live only as a monitor/veto? | `r4_s05`, `r4_s06` | improves family branches without needing direct `5200` inventory | `5200` signal-only framing is overstated |
| `r4_s08_family_pressure_overlay` | does family-level state add more than symbol-local context? | `r4_s01`, `r4_s06` | distinct lift in linked-book situations | family proxy is too weak or redundant |
| `r4_s12_upper_passive_probe` | is there any cheap passive-only value in the upper loop? | `r4_s01` | limited but clean fills without toxicity | upper branch should stay research-only |
| `r4_s14_surface_sanity_filter` | can a tiny surface sanity proxy improve selectivity without complexity? | `r4_s04`, `r4_s03` | fewer fake residual-style entries with negligible runtime burden | pricing-support layer is not worth live complexity |

## Spec Grouping Recommendation

`04 Spec` should stay grouped so that implementation and validation compare
clean families instead of `15` completely unrelated one-off specs.

| Spec Pack | Candidates | Shared Theme | Why Group Them |
| --- | --- | --- | --- |
| `pack_a_delta1_controls` | `r4_s01`, `r4_s02` | clean controls | provides the comparison floor for every later branch |
| `pack_b_round3_revalidation` | `r4_s15`, `r4_s03`, `r4_s13` | old winner family and ITM overlays | all test whether the best `round_3` ingredient survives or improves |
| `pack_c_5300_active_family` | `r4_s04`, `r4_s09`, `r4_s11` | isolated `5300` hypotheses | all ask whether `5300` is real and what gating/horizon it needs |
| `pack_d_counterparty_defensive` | `r4_s05`, `r4_s06`, `r4_s10` | counterparty-conditioned danger-state logic | isolates the main new `round_4` information layer |
| `pack_e_execution_and_family_context` | `r4_s07`, `r4_s08` | execution and linked-book overlays | both are contextual layers over anchor-first logic |
| `pack_f_low_priority_probes` | `r4_s12`, `r4_s14` | cheap closure probes | good to spec compactly because both are low-confidence but informative |

## Next Action

- Next:
  open `04 Spec` and write grouped implementation-ready specs pack by pack:
  start with `pack_a_delta1_controls`, `pack_b_round3_revalidation`, and
  `pack_d_counterparty_defensive`, then continue with the remaining packs in
  queue order.
