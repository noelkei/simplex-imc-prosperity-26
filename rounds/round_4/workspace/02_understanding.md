# Understanding Summary

Use [`docs/templates/understanding_template.md`](../../../docs/templates/understanding_template.md) as the structure for this file.

## Status

READY_FOR_REVIEW

## Sources

- Wiki facts:
  - [`../../docs/prosperity_wiki/rounds/round_4.md`](../../docs/prosperity_wiki/rounds/round_4.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
  - [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
  - [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
  - [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- Post-run research memory:
  - none yet for `round_4`
- Playbook heuristics:
  - none required as primary evidence
- Other named artifacts:
  - [`00_ingestion.md`](00_ingestion.md)
  - [`00_prior_round_intake.md`](00_prior_round_intake.md)
  - [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)
  - [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)

## Current Understanding

- Fact:
  `round_4` keeps the same algorithmic product universe and limits as `round_3`, but now exposes named counterparties in `Trade.buyer` and `Trade.seller`.
- Evidence:
  Raw-data EDA strongly supports `VEX` as the primary same-time anchor of the voucher family, a role-first option-book framing, and the view that counterparties matter as context more than as standalone alpha.
- Hypothesis:
  The highest-ROI `round_4` strategy space is likely `delta-1 base / anchor-first` plus compact counterparty-aware option-book filters, not a broad reopening of the active voucher basket.

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| `round_4` is algorithmically the same market as `round_3` plus visible counterparties | wiki + ingestion | strong | high | contradictory round facts or new market structure evidence |
| `HYDRO` remains structurally separate from the voucher family | EDA | strong | high | later run evidence showing consistent cross-product dependency |
| `VEX` remains the strongest same-time anchor for vouchers | EDA | strong | high | later validation showing voucher logic works equally well without `VEX` anchor context |
| The voucher family is linked structurally but execution-fragmented | EDA | strong | high | later run evidence showing homogeneous tradability across the cluster |
| `5000/5100/5200/5300` are not homogeneous | EDA + round_3 carry-forward | strong | high | contradictory run evidence after strike-specific testing |
| Counterparty specialization is real and stable enough for contextual use | EDA | strong | high | later data showing instability or no incremental decision value |
| Raw counterparty names alone are weak; engineered context is better | EDA | medium-high | high | richer out-of-sample evidence showing raw names are enough |
| `5200+` seller-dominant flow, especially `Mark 22`, is the clearest danger-state story | EDA | medium-high | high | later runs showing it is harmless or directly monetizable as inventory |
| `5300` is still special, but not validated as a direct winner leg | EDA + round_3 carry-forward | medium-high | high | clean `round_4` strategy tests showing positive retained edge |
| Advanced option pricing supports surface-aware framing, not a heavy live stack | EDA | medium | medium-high | later specs showing a simple surface-aware proxy is actually necessary and online-usable |
| Manual products remain out of operational algorithmic scope for now | wiki + ingestion | strong | medium | contract-level manual raw data becoming available |
| Much of the new counterparty evidence is descriptive structure first and predictive edge second | EDA | strong | high | later run evidence showing direct monetizable gains from the same signals |

## Signal Validation Expectations

Use the EDA outputs as confidence compression, not as permission to over-implement.

- Statistical or regime evidence used:
  same-time return correlations, lead-lag rejection, spread hierarchy, concentration metrics, side-aware markouts, controlled regression ladder, and BS-vs-Heston fit comparison.
- Features downgraded for weak confidence, instability, or offline-only status:
  raw buyer/seller names as standalone alpha, pair recurrence as direct trigger, delayed-follow logic, upper/floor direct aggression, pure Heston/COS logic as live machinery.
- Research outputs not trusted yet:
  direct `5200` danger-state trigger, direct `5300` salvage alpha, counterparty-pair online triggers, and any strategy claim that depends on only three days of tape without run validation.
- Operational-causality warning:
  most counterparty findings currently improve market-state description,
  filtering, and product-role framing more than they prove a direct
  open-or-close rule will add PnL.

## Operational Interpretation Limits

| Finding | What Seems Real | What Is Not Yet Proven | Allowed Use In Strategy |
| --- | --- | --- | --- |
| Counterparty concentration and dominance | market structure is genuinely concentrated by strike and side | that concentration alone creates tradable directional alpha | context, regime filters, danger-state framing |
| `Mark 22` seller pressure in `5200+` | recurring seller-side structure with adverse short-horizon environment for naive inventory | that a direct `if Mark22 then trade` rule is profitable | conditional veto / defensive test branch only |
| `5300` specialness | distinct mix of tape, spread, concentration, and role | that `5300` is a retained-edge live leg in `round_4` | isolated candidate family, not default basket member |
| Engineered context beating raw names | context features carry more explanatory value than naked identities | that the current engineered set is already sufficient or stable enough for bot use | compact feature shortlist, not full implementation permission |
| Surface-aware pricing layer | flat-vol mental model is incomplete for short-dated vouchers | that live Heston/COS machinery is necessary or ROI-positive | simplified pricing backbone selection and residual framing only |


## Multivariate Relationships Carried Forward

| Relationship | Source EDA Artifact | Evidence | Decision Impact | Confidence | Caveat |
| --- | --- | --- | --- | --- | --- |
| `HYDRO` vs `VEX` are effectively unlinked | `01_eda/eda_round_4_counterparty_and_option_book.md` | same-time return correlation `0.0013` | use separate delta-1 framing | high | raw-data only |
| `VEX` vs `5000/5100/5200` is the strongest family linkage | `01_eda/eda_round_4_counterparty_and_option_book.md` | same-time return correlations `0.7542`, `0.7600`, `0.7315` | use `VEX` as anchor | high | does not imply delayed-follow |
| Cross-strike linkage decays sharply from `5200` upward | `01_eda/eda_round_4_option_book_structure.md` | `5000-5100 = 0.8985`, `5400-5500 = 0.1688` | split strike logic and execution posture | high | friction diverges faster than correlations |
| Raw buyer/seller buckets add little simple explanatory power | `01_eda/eda_round_4_counterparty_and_option_book.md` | model ladder `R^2 = 0.0101` with raw names | do not use naked names as primary signal | medium-high | explanatory only |
| Engineered counterparty/book context adds more than raw names | `01_eda/eda_round_4_counterparty_and_option_book.md` | model ladder `R^2 = 0.0183` with engineered context | prefer compact engineered context | medium-high | still explanatory only |

## Redundancy Decisions

| Feature Family | Keep | Merge / Downgrade / Drop | Evidence | Strategy Impact |
| --- | --- | --- | --- | --- |
| `VEX`-anchor family | same-time anchor linkage, role-aware residual framing | downgrade delayed-follow variants | same-time corr strong, lagged corr weak | anchor-first option logic |
| Counterparty structure family | concentration, dominance, stability class, trade location | downgrade raw-name-only logic | concentration and model ladder | context features beat naked names |
| Friction family | relative spread, strike role, time bucket | downgrade universal raw imbalance | spread hierarchy and regime tables | execution/no-trade posture should be first-class |
| Sparse-tape strikes | quote-led reasoning for `4500/5000/5100` | drop rich tape claims for these strikes | trade counts `3/3/3` | strategy should not pretend tape support exists |
| Advanced pricing family | IV surface, Greeks, simple pricing backbone choice | downgrade full Heston engine for bot logic | moderate Heston improvement only | use as framing, not runtime complexity |

## Process Hypotheses Carried Forward

| Product Or Scope | Process Hypothesis | EDA Evidence | Confidence | Online Observable / Proxy | Strategy Or Validation Implication |
| --- | --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | liquid independent delta-1 process | low spread, balanced flow, no link to voucher family | medium-high | spread, depth, imbalance, own trade flow | preserve separate delta-1 branch |
| `VELVETFRUIT_EXTRACT` | liquid anchor process for the voucher book | lowest major spread, strongest same-time linkage | high | mid, spread, own counterparty flow, nearby strikes | anchor-first strategy family remains favored |
| `VEV_4000/4500` | ITM structural overlay, not generic active cluster | `4000` has usable tape, `4500` sparse, both link to `VEX` | medium | `VEX` state + strike role + spread | use as structural overlay candidates |
| `VEV_5000-5300` | linked active zone with diverging execution texture | linkage strong, friction and concentration diverge | high | spread, concentration, neighbor strikes, `VEX` | split active-zone logic by strike |
| `VEV_5400/5500` | thin upper/passive regime | huge spreads, deterministic counterparties, poor short-horizon alignment | medium-high | spread, counterparty dominance, time bucket | passive-only or signal-only by default |
| `VEV_6000/6500` | floor / monitor regime | constant `0.5` mids, zero notional | high | constant mid behavior | exclude from direct trading logic |

## Assumptions Carried Forward

| Assumption | Source | Current-Round Evidence | Risk | Action |
| --- | --- | --- | --- | --- |
| `round_3` framing still matters | prior-round intake | compatibility gate says `compatible` | medium | use with revalidation |
| `VEX` is the correct voucher anchor | `round_3` + round_4 EDA | strongly supported by same-time linkage | low | use |
| counterparties can create contextual state without creating naked alpha | round_4 EDA | concentration and markouts support context > direct alpha | medium | use |
| three days of raw data are enough for structural framing but not final strategy quality | round_4 EDA | stability is visible, but no run evidence exists | medium | use cautiously |
| manual challenge should stay separate until contract data exists | wiki + ingestion | still missing symbols/strikes/barriers/payouts | low | use |

## Round 3 Unresolved Learnings Carried Forward

These are important because `round_3` did not fully settle them, and `round_4`
should inherit them as live questions rather than bury them.

| Unresolved Learning | `round_4` Status | Why It Still Matters | Current Action |
| --- | --- | --- | --- |
| `5100/5200` as signal-only or danger-state rather than inventory | still plausible, partly reinforced | `5200` now has strong concentrated seller context; `5100` still sparse | carry to strategy as explicit test axis |
| `5300` as special strike with different horizon | still plausible, still unresolved | raw data keeps it special but does not prove retained edge | carry as special-case candidate, not as fact |
| family imbalance as better signal than single-symbol imbalance | still unresolved | EDA now reinforces family framing and concentration logic | carry as strategy/validation hypothesis |
| late-session deterioration / no-new-entry logic | weakened as universal claim, still plausible product-specifically | top names trade all day, but upper-strike friction worsens later | carry as conditional execution hypothesis |
| small overlays over a clean base | still plausible | `round_3` favored this architecture; `round_4` does not contradict it | carry as candidate architecture |
| whether `delta-1` is final champion or infrastructure/context | still unresolved in `round_4` | raw data supports clean base framing, not final winner proof | keep open for strategy ranking and later validation |
| whether `4000/4500` still hide underused structural edge | still unresolved | `4000` remains active; `4500` remains sparse | keep in low-complexity overlay scope only |

## Signal Ledger

| Signal | Product | Source Artifact | Feature Basis | Feature Origin | Online Usability | Role | Stability | Confidence | Decision Action | Risk | Next Phase Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `VEX_anchor_same_time` | `VELVETFRUIT_EXTRACT` + `VEV_*` | `01_eda/eda_round_4_counterparty_and_option_book.md` | same-time corr + lag rejection | combined | usable online | direct signal / anchor | stable | high | use | may be overcomplicated later | use as default anchor in candidate framing |
| `option_book_role_split` | voucher family | `01_eda/eda_round_4_option_book_structure.md` | strike role + friction + concentration | combined | usable online | risk control / diagnostic | stable | high | use | later runs may refine boundaries | force role-specific candidates |
| `counterparty_concentration_context` | `VEV_5200+`, `5300`, upper/floor | `01_eda/eda_round_4_counterparty_profiles.md` | top-share concentration, dominance flags, stability class | combined | usable online | execution filter / regime feature | stable | high | use | can be over-read as alpha | test only as contextual state |
| `mark22_seller_danger_state` | `VEV_5200+` | `01_eda/eda_round_4_counterparty_profiles.md` | seller-side markout + concentration + family exposure | combined | usable online | risk control / contextual veto | stable | medium-high | validate next | sample still only three days | candidate strategy axis, not fact |
| `trade_location_context` | trade-aligned symbols | `01_eda/eda_round_4_counterparty_and_option_book.md` | at-bid / at-ask / inside-spread bucket | combined | usable online | execution filter / diagnostic | stable | medium | use | needs simple online implementation | keep as reusable primitive |
| `upper_floor_exclusion` | `VEV_5400+`, `6000/6500` | `01_eda/eda_round_4_option_book_structure.md` | relative spread, deterministic flows, constant mids | combined | usable online | avoid | stable | high | avoid | could hide passive-only edge later | keep out of default trading sets |
| `engineered_context_over_raw_names` | market-wide trade layer | `01_eda/eda_round_4_counterparty_and_option_book.md` | model ladder `0.0076 -> 0.0101 -> 0.0183` | combined | usable online | diagnostic / modeling rule | stable | medium-high | use | explanatory only | shape candidate feature budget |
| `surface_awareness_not_flat_vol` | `VEV_*` | `01_eda/eda_round_4_option_volatility_and_pricing.md` | IV surface, Greeks, BS-vs-Heston | combined | EDA-only / proxyable | diagnostic / pricing context | stable enough in panels | medium | validate next | runtime complexity risk | use in framing, not as direct bot requirement |

## Strategy-Relevant Insights

| Insight | Linked EDA Signals | Feature Evidence | Regime Assumptions | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| `delta-1 base` and `VEX` anchor should remain the default starting point | `VEX_anchor_same_time`, `option_book_role_split` | strong same-time linkage, clean delta-1 separation | stable market structure | high | make anchor-first and base-first candidates the queue default |
| Counterparties are best treated as contextual state, not naked alpha | `counterparty_concentration_context`, `engineered_context_over_raw_names` | concentration and model ladder | stable for top names | high | design contextual filters, not name-trigger bots |
| `5200` and nearby upper-middle flow deserve explicit danger-state testing | `mark22_seller_danger_state`, `counterparty_concentration_context` | side-aware seller markout and seller dominance | likely state-dependent | medium-high | include danger-state / veto candidate directions |
| `5300` remains special but unresolved | `option_book_role_split`, `mark22_seller_danger_state` | trade count, concentration, friction divergence | may need distinct horizon | medium-high | keep `5300` separate from generic active basket |
| Upper/floor vouchers should not re-enter default aggressive inventory | `upper_floor_exclusion` | huge spreads, deterministic names, constant-floor behavior | robust | high | default passive-only / signal-only / avoid |
| Advanced pricing layer supports better framing, not immediate live complexity | `surface_awareness_not_flat_vol` | moderate Heston improvement, Greeks concentrated in `5200/5300` | short-dated surface not flat | medium | allow simplified pricing backbones, reject heavy runtime stack |

## Product Attribution View

| Product | Opportunity / Risk Status | Evidence | Main Uncertainty | Strategy Implication |
| --- | --- | --- | --- | --- |
| `HYDROGEL_PACK` | edge likely / clean base candidate | liquid, independent, role-consistent | whether counterparties add anything useful | keep as separate delta-1 branch |
| `VELVETFRUIT_EXTRACT` | edge likely / anchor candidate | strongest linkage and best friction among major products | how much standalone alpha vs pure anchor role | keep as core branch and context backbone |
| `VEV_4000` | plausible structural overlay | real trade tape and anchor linkage | whether it is worth standalone risk | keep in low-complexity overlay space |
| `VEV_4500` | unclear | quote-rich but trade-poor | too little and too unbalanced tape | do not over-prioritize |
| `VEV_5000/5100` | unclear / structure-rich but tape-poor | strongest anchor linkage but almost no tape | whether missing trades hide opportunity or irrelevance, and whether any inference is just quote structure | quote-led only, not tape-led |
| `VEV_5200` | risk-heavy but informative | seller concentration and poor short-horizon alignment | true danger-state vs sparse artifact vs product-selection confound | prioritize as contextual test axis |
| `VEV_5300` | unclear but still important | special concentration, trade count, role divergence | tradable edge vs contextual importance only, under sample imbalance | keep as separate candidate family |
| `VEV_5400/5500` | risk-heavy | friction explosion and deterministic flows | whether passive-only edge exists | default avoid/aggressive no |
| `VEV_6000/6500` | low priority / monitor only | constant floor mids and zero notional | almost none | exclude from active logic |

## Cross-Product Verdict

- Verdict: `useful`
- Evidence:
  `VEX`-voucher linkage is strong, strike-role and friction are family-shaped, and `HYDRO` is clearly separate.
- Caveat:
  usefulness is strongest for framing and context; direct cross-product alpha still needs run validation.

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| anchor-first delta-1 + option-book candidate family | `delta-1 base` + `VEX` anchor insight | `HYDRO`, `VEX`, selective `VEV_*` | best-supported carry-forward architecture | real run comparison vs simpler delta-1 control |
| counterparty-aware danger-state filters | `5200+` seller danger-state insight | `VEV_5200+`, especially `5200/5300` | strongest new `round_4` information surface | run tests proving context helps more than hurts |
| `5300` special-case branch | `5300` unresolved special-strike insight | `VEX` + `VEV_5300` | raw data keeps it distinct and non-generic | retained-edge validation, not just raw path |
| ITM structural overlay candidate | `4000` structural overlay insight | `VEX` + `VEV_4000` | low-complexity way to test structural option add-on | compare to pure anchor/base control |
| time-bucket defensive execution rules in upper/middle strikes | upper/passive regime insight | `5200+` | later friction worsens and flows are concentrated | validation on no-trade / passive-only outcomes |

## What Should Not Be Trusted Yet

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| raw buyer/seller names as primary alpha | simple explanatory power is weak | strategy overfits names | keep only as context and compare against no-name baseline |
| `5200` as proven direct danger-state trigger | still raw-data level only | false vetoes or bad inventory decisions | test in strategy variants |
| `5300` as proven rescue winner | no `round_4` run evidence yet | repeating old active-voucher failure modes | validate with clean, isolated runs |
| full Heston / COS logic as live machinery | EDA improvement is only moderate | complexity without runtime ROI | only use simplified proxies if needed |
| universal late-session toxicity | raw timing is mixed by counterparty | over-shuts down valid opportunities | test product-specific time rules only |
| pair recurrence as ready-made trigger | only three days, heavily explained by concentration | noise disguised as structure | keep exploratory |
| direct causal interpretation of counterparty identities | product choice and regime may explain part of the observed effect | building logic on spurious attribution | use role/concentration context before identity-specific rules |

## Research Memory

Promising features:

| Feature Or Signal | Source | Why Promising | Needed Before Strategy |
| --- | --- | --- | --- |
| counterparty concentration / dominance | round_4 EDA | strongest new contextual structure | convert to simple online feature contract |
| trade-location bucket | round_4 EDA | ties microstructure and counterparties together | define lightweight online computation |
| `VEX` same-time anchor + role-aware residual framing | round_4 EDA + round_3 carry-forward | strongest structural option-book story | choose simple live kernel |
| `5200/5300` contextual family-state features | round_4 EDA + round_3 unresolved backlog | directly connects new data with old gaps | strategy isolation and validation |

Rejected / noisy features:

| Feature Or Signal | Source | Evidence Against | Reopen Only If |
| --- | --- | --- | --- |
| delayed-follow voucher logic | round_4 EDA | lagged correlations collapse after lag `0` | later run evidence reveals latency edge |
| upper/floor direct aggression | round_4 EDA | extreme friction and deterministic flows | passive-only tests show clear retained edge |
| raw-name linear signals | round_4 EDA | weak model ladder contribution | interaction-driven evidence becomes much stronger |
| counterparty-specific direct causality claims | round_4 EDA | current evidence mixes participant identity with strike selection and friction regime | later run evidence isolates incremental value cleanly |

Unresolved / log-needed features:

| Feature Or Signal | Source | Missing Evidence | Next Action |
| --- | --- | --- | --- |
| `5200` true signal-only role | round_3 closeout + round_4 EDA | no run evidence in `round_4` | test contextual veto branch |
| `5300` retained-edge role | round_3 closeout + round_4 EDA | no clean retained PnL evidence in `round_4` | run special-case branch |
| family imbalance | round_3 unresolved backlog | not yet engineered/tested in live strategy context | consider in strategy only if it fits feature budget |

## Confidence And Impact

- Overall confidence: `medium-high`
- Highest-impact implication:
  `round_4` should be approached as `delta-1 / VEX anchor first`, with counterparties treated as contextual state and with the voucher family split by role rather than reopened as a broad basket.
- Main caveat:
  this is still raw-data understanding; no `round_4` run evidence yet separates useful context from monetizable edge.
- Secondary caveat:
  the sample is not only short (`3` days); it is also highly unbalanced by
  strike, so confidence is much stronger for structural role conclusions than
  for strike-specific predictive claims.

## Assumptions

- The top visible `Mark XX` names represent stable enough structural participants to justify contextual use in early strategy work.
- The uploaded `day_1..3` files are representative enough for framing, but not enough for final strategy confidence.

## Open Questions

- Can counterparty-conditioned context materially improve retained strategy quality rather than just describe the tape?
- Is `5200` truly better as veto/state than as inventory?
- Does `5300` deserve active treatment in `round_4`, or is it still mostly a structural curiosity with unresolved edge?
- How much of the advanced pricing layer survives simplification into an online-usable residual context?

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| no `round_4` run evidence yet | strategy / validation | high | keep claims contextual and test them cleanly |
| manual contract detail missing | strategy | low for algorithmic, high for manual | keep manual out of current strategy path |
| deadline still unknown | prioritization | medium | confirm deadline before broad candidate expansion |
| sparse tape for `4500/5000/5100` | strategy / validation | medium | avoid tape-led claims there |
| counterparty context may overfit names | strategy / implementation | high | prefer role buckets and baseline comparisons |
| product-selection confound inside counterparty effects | strategy / validation | high | test counterparty context against matched product/role baselines |
| non-stationarity of visible `Mark XX` identities | strategy / implementation | high | prefer degradable role/context features over brittle identity rules |

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| whether contextual counterparty features improve a clean base architecture | strategy / validation | high | candidate design + run test |
| whether `5200` is veto-only | strategy | high | targeted strategy branch |
| whether `5300` has retained edge in `round_4` | strategy / validation | high | isolated strategy branch |
| whether family imbalance adds anything beyond concentration/role | strategy | medium | only test if feature budget allows |
| whether upper strikes hide passive-only edge | strategy | low-medium | consider only after base candidates |

## Strategy Implications

- Candidate direction:
  start from `delta-1 base + VEX anchor` and add only compact option-book or counterparty context where it targets a known uncertainty or risk.
- Risk or constraint:
  do not let counterparty novelty create feature dumping, and do not promote raw-name logic over role/concentration context.
- Pricing translation rule:
  inherit from the advanced pricing layer only simplified residual/surface
  awareness, strike sensitivity, and anchor choice; do not inherit calibrated
  Heston parameters, COS machinery, or direct Greek-driven bot logic unless a
  later spec defines a lightweight online proxy.
- Validation/debug implication:
  treat `5200/5300` and counterparty-aware filters as explicit test axes, and evaluate whether they function better as context/veto than as inventory logic.

## 02b Seed Set

Use these directly for `Phase 02b External Paper Research`.

| Research Question | Why It Matters | Desired Paper Type / Method | Mode |
| --- | --- | --- | --- |
| How should visible participant flow in options or linked books be converted into contextual state rather than direct alpha? | This is the main new `round_4` information layer. | option microstructure, order-flow conditioning, participant segmentation | candidate-driving |
| What lightweight methods best separate `signal-only` derivatives from `inventory-worthy` derivatives in short-dated option books? | Directly maps to `5200/5300` and upper-strike decisions. | option-book microstructure, market-making, adverse selection | candidate-driving |
| What simplified surface-aware pricing or residual methods are robust enough for short-dated option books without requiring heavy stochastic-volatility machinery online? | Needed to turn the advanced EDA layer into practical strategy options. | short-dated option pricing, residual/surface models, pragmatic quant methods | candidate-driving |
| What evidence-based gating or no-trade rules work best when friction and participant concentration worsen later in the session? | Maps to upper/passive and possible late-session defensive logic. | execution, regime gating, adverse selection, inventory control | validation-only |
| How should family-level exposure or family imbalance be framed in multi-strike option books when signals are highly concentrated? | This is a direct unresolved carry-forward from `round_3`. | portfolio exposure, option MM, cross-strike risk control | guardrail-only |

## Next Action

- Next:
  review this understanding package, then generate the default `02b` external
  paper research prompt and open `03 Strategy` using the carry-forward
  principles, unresolved `round_3` learnings, promoted contextual signals, and
  explicit anti-patterns recorded here.
