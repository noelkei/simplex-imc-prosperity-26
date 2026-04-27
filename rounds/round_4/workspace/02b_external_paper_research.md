# External Paper Research

## Status

`COMPLETED`

## Sources

- Understanding summary:
  [`02_understanding.md`](02_understanding.md) (`READY_FOR_REVIEW`)
- Understanding context:
  [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
  - [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
  - [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
  - [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- Post-run research memory:
  - none yet for `round_4`
  - carry-forward reference:
    [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)
- Other named artifacts:
  - [`00_prior_round_intake.md`](00_prior_round_intake.md)
  - [`02b_processed_set_audit.md`](02b_processed_set_audit.md)
  - [`02b_strategy_handoff.md`](02b_strategy_handoff.md)

## Research Goals

- Goal:
  Build a high-ROI paper layer for `round_4` that sharpens
  `counterparty-aware option-book strategy`, `danger-state / no-trade logic`,
  `cross-strike family framing`, and `lightweight surface-aware pricing`.
- Why this matters before strategy generation:
  `round_4` keeps the `round_3` product universe but adds visible
  counterparties, which creates a genuinely new source of contextual state that
  needs better framing than naive raw-name alpha.
- Prosperity runtime / Trader constraints to preserve:
  pure Python stdlib in `Trader.run()`, no heavy calibration stacks, no
  external calls, small rolling state only, and only online-observable fields
  should influence live logic.

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| `VEX` as same-time voucher anchor | `VEX` + `VEV_*` | understanding + EDA | strongest current-round structural link |
| role split across strikes | voucher family | understanding + EDA | `5000/5100/5200/5300` are not homogeneous |
| counterparty concentration / dominance | `VEV_5200+`, upper strikes | EDA | strongest new `round_4` context layer |
| `Mark 22` seller-state and upper-strike danger-state | `VEV_5200+` | EDA | clearest adverse-selection / no-trade story |
| engineered context beating raw names | market-wide | EDA | supports compact context features over naked identity |
| surface-aware but lightweight residual framing | voucher family | EDA | flat-vol mental model is too naive, but heavy live pricing is not justified |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| broad active voucher basket reopening | `round_3` closeout + `round_4` understanding | strikes are heterogeneous in role, friction, and concentration |
| raw buyer/seller names as naked alpha | `round_4` EDA + understanding | descriptive structure is stronger than direct predictive value |
| upper/floor direct aggression | `round_4` EDA + understanding | extreme spread / sparse tape / deterministic flows |
| heavy Heston/COS live machinery | `round_4` EDA + understanding | runtime complexity exceeds evidence strength |
| mistaking concentrated seller flow for guaranteed directional edge | `round_4` understanding | product-selection and regime confounds remain real |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| How should visible participants be used as context rather than raw alpha? | core new information layer in `round_4` | non-anonymous flow and participant-conditioned microstructure papers |
| How do we separate `signal-only / veto-worthy` strikes from `inventory-worthy` strikes? | crucial for `5200+` and `5300` | cross-strike and option-book flow papers |
| What lightweight surface-aware backbone is enough when flat-vol is too naive? | needed for residual sanity without live overkill | demand-distorted surface and cheap interpolation papers |
| What execution / no-trade logic is justified under concentrated or unstable flow? | key to upper-strike danger-state logic | intraday option-liquidity and order-book signal papers |
| How hard should flow-heavy signals be benchmarked against simple baselines? | avoids overclaiming on counterparties | guardrail papers on incremental information content |

## Target Research Questions

- Question 1:
  How should visible participant / order-flow structure be used as contextual
  state rather than naive direct alpha in options or linked-product trading?
- Question 2:
  How can we distinguish `signal-only / veto-worthy` derivatives from
  `inventory-worthy` derivatives in short-dated or fragmented option books?
- Question 3:
  What lightweight surface-aware pricing or residual frameworks are robust
  enough for short-dated option families when flat-vol is too naive but full
  stochastic-vol live machinery is overkill?
- Question 4:
  What no-trade, quote-suppression, adverse-selection, or defensive gating
  ideas work best when participant concentration and unstable flow worsen?
- Question 5:
  What family-level / cross-strike exposure or imbalance frameworks are useful
  in small option books where some strikes are better as context than inventory?

## Online Search / Shortlist Notes

- Mode used: `mixed`
- Queries / intent:
  targeted shortlist-building and metadata verification for papers on
  non-anonymous markets, option-book flow, adverse selection, intraday option
  liquidity, demand-distorted surfaces, and lightweight pricing support.
- Accepted shortlist:
  `vasios`, `doshi`, `kaeck`, `bollen_whaley`, `garleanu_pedersen_poteshman`,
  `cartea`, `nimalendran_son`, `goncalves_pinto_sala`, `roos`
- Rejected shortlist and why:
  `muravyev`, `stoikov_saglam`, `fengler`, and `choi` were excluded from the
  new raw set because they were already processed and reused from `round_3`;
  `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`
  remained preferred but unavailable locally.

## Generated External Research Prompt

```text
You are helping with external research for a trading-research project. Use internet search, deep research, and extended reasoning if available.

Your task is to identify the 5-10 highest-ROI papers, technical notes, SSRN/arXiv papers, practitioner writeups, or primary resources that would be most useful for the very specific trading problem below.

This is not a generic options-literature request. Please optimize for relevance, implementation realism, and decision usefulness.

Project context
---------------
We are working on a Python trading bot for a competition market with:
- one simple delta-1 product: HYDROGEL_PACK
- one underlying / anchor product: VELVETFRUIT_EXTRACT ("VEX")
- a family of short-dated option-like vouchers on VEX:
  VEV_4000, VEV_4500, VEV_5000, VEV_5100, VEV_5200, VEV_5300, VEV_5400, VEV_5500, VEV_6000, VEV_6500

Important new information in this round:
- market trade data now includes visible counterparties in buyer / seller fields
- counterparties look like "Mark 01", "Mark 22", etc.

The live bot must remain simple and online-implementable. Research outputs may inspire framing, validation, and simple features, but should NOT require a heavy offline model stack at runtime.

Current empirical understanding
------------------------------
Please treat these as current project findings, not as claims you need to prove:

1. The option-family products are structurally linked to VEX, and VEX is the strongest same-time anchor.
2. Delayed-follow logic looks weak; same-time anchor logic is much stronger.
3. The voucher family is not homogeneous. Rough role split:
   - VEV_4000 / 4500: ITM structural overlay candidates
   - VEV_5000 / 5100: anchor-linked but trade-sparse
   - VEV_5200: possibly danger-state / signal-only candidate
   - VEV_5300: special active strike, still unresolved
   - VEV_5400 / 5500: upper/passive / likely signal-only or passive-only
   - VEV_6000 / 6500: floor / monitor, not default inventory
4. Counterparty information appears useful as contextual state, but raw participant names alone have weak direct predictive value.
5. Concentration and dominance by counterparty are strong in parts of the option family, especially from VEV_5200 upward.
6. One specific pattern that matters:
   seller-dominant flow associated with "Mark 22" in VEV_5200+ looks like the clearest danger-state / adverse-selection story in the raw data.
7. A more advanced option-pricing analysis suggests flat-volatility thinking is too naive, but a full Heston/COS engine is probably too heavy for live bot logic.

Key open research questions
---------------------------
Please find resources that best help with these questions:

1. How should visible participant / order-flow structure be used as contextual state rather than naive direct alpha in options or linked-product trading?
2. How can we distinguish "signal-only / veto-worthy" derivatives from "inventory-worthy" derivatives in short-dated or fragmented option books?
3. What lightweight surface-aware pricing or residual frameworks are robust enough for short-dated option families, when flat-vol is too naive but full stochastic-volatility live machinery is overkill?
4. What no-trade, quote-suppression, adverse-selection, or defensive gating ideas work best when friction and participant concentration worsen?
5. What family-level / cross-strike exposure or imbalance frameworks are useful in small option books where some strikes may be better as context than inventory?

What NOT to optimize for
------------------------
Please avoid prioritizing:
- purely theoretical option-pricing papers with no practical adaptation path
- papers that require heavy continuous-time calibration or large offline infrastructure to be useful
- generic deep learning papers
- papers that ignore market microstructure, execution, or adverse selection
- papers that would only be useful if we were building a full market-making stack with rich institutional infrastructure

What we DO want
---------------
Please prioritize resources that are:
- practical
- implementable or at least simplifiable into an online trading bot
- useful for strategy design, regime filters, validation checks, or risk gating
- strongly connected to market microstructure, options flow, participant behavior, adverse selection, or simple relative-value / residual thinking

Desired output format
---------------------
Please return:

1. A ranked shortlist of 5-10 highest-ROI resources.

For each resource:
- title
- authors
- year
- link
- PDF link if available
- resource type (paper / technical note / practitioner article / survey / thesis / chapter)
- why it is relevant to THIS project specifically
- which of the 5 research questions it helps answer
- whether its value is:
  - candidate-driving
  - validation-only
  - guardrail-only
  - inspiration-only
- whether it seems:
  - implementable with simple online features
  - only useful as validation or framing
  - too heavy / too theoretical
- a 3-6 sentence summary focused on adaptation, not generic summary

2. A "best next 3 to read first" recommendation with rationale.

3. A "do not waste time on these sub-literatures" section, if relevant.

4. A short synthesis:
- what simple methods seem most promising for this project
- what methods seem dangerous to overuse
- what likely belongs in framing/validation only rather than live bot logic

5. If you can, suggest 2-4 search queries that would help deepen the shortlist further.

Important constraints
---------------------
- Assume the downstream bot is a simple Python competition trader with online-observable fields only.
- Do not assume access to complex institutional datasets beyond order book, trades, counterparties, and simple rolling state.
- Keep adaptation realism front and center.

At the end, remind the human to upload the selected PDFs or source folders into:
rounds/round_4/research/papers_raw/
so they can be converted into markdown and processed summaries locally.
```

## Prompt Requirements Checklist

- Ask external AI to use internet / deep research / extended reasoning if available: `yes`
- Ask for roughly 5-10 highest-ROI papers or resources: `yes`
- Prioritize implementable methods for simple online trading bots: `yes`
- Ask for links / citations / PDFs if available: `yes`
- Include upload instruction for `rounds/round_4/research/papers_raw/`: `yes`

## Batch Plan

| Batch | Goal | Papers | Stop Condition |
| --- | --- | --- | --- |
| Batch 1 | first-candidate-changing core | `doshi`, `kaeck`, `vasios`, `bollen_whaley`, `cartea`, `garleanu_pedersen_poteshman` | all six have usable processed summaries |
| Batch 2 | guardrail / regime / validation | `nimalendran_son`, `goncalves_pinto_sala` | both have usable processed summaries |
| Batch 3 | benchmark / utility / surface support | `roos` | usable processed summary exists |

## Paper Pipeline Status

- Expected upload folder:
  `rounds/round_4/research/papers_raw/`
- Raw papers detected:
  `9`
- Markdown conversions pending:
  `0`
- Processed summaries pending:
  `0` for the uploaded raw-paper set
- Strategy may proceed now: `yes`
- Waiting state: `fully-processed`

## Canonical Strategy Paper Core

Use these first when opening `03 Strategy`:

| Paper ID | Primary Use | Implementability | Why It Matters Most |
| --- | --- | --- | --- |
| `doshi_2025_risky_intraday_order_flow` | danger-state / no-trade logic | `implementable` | strongest external support for unstable-flow defensive gating |
| `kaeck_2019_informed_index_options` | family / cross-strike flow framing | `variant-only` | strongest link to voucher-family flow as a linked book |
| `vasios_2015_mimicking_non_anonymous` | participant-conditioned context | `implementable` | best direct support for non-anonymous flow as contextual state |
| `bollen_whaley_2004_net_buying_pressure` | residual / flow distortion guardrail | `validation-only` | helps prevent misreading flow-distorted surface as alpha |
| `cartea_2018_order_book_signals` | order-book / execution gating | `implementable` | strongest lightweight execution overlay paper |
| `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | family-demand framing | `EDA-follow-up` | cleanest theory for cross-strike pressure and demand-distorted pricing |

Secondary but still useful:

- `nimalendran_son_2024_cream_skimming_toxic_flow`:
  guardrail for `counterparty danger-state` interpretation
- `goncalves_pinto_sala_2025_incremental_option_volume`:
  benchmark discipline for flow-feature promotion
- `roos_2026_arbitrage_free_interpolation`:
  lightweight surface-sanity and residual framing support

Useful `round_3` carry-forward references remain available as secondary paper
inputs, especially:
`muravyev`, `stoikov_saglam`, `bergault`, `choi`, `fengler`, and
`garcia_ares`. These should support `03 Strategy` after the top-level
`round4_raw_derived` core, not outrank it.

For the shortest downstream bridge into `03 Strategy`, use
[`02b_strategy_handoff.md`](02b_strategy_handoff.md).

## Processed Paper Index

| Paper ID | Input Type | Raw File | Markdown File | MD Fidelity | Processed Summary | Batch | Status | Action Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `doshi_2025_risky_intraday_order_flow` | `pdf` | `doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf` | `doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.md` | `medium` | `doshi_2025_risky_intraday_order_flow_processed.md` | Batch 1 | processed | `new candidate` |
| `kaeck_2019_informed_index_options` | `pdf` | `kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf` | `kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.md` | `medium` | `kaeck_2019_informed_index_options_processed.md` | Batch 1 | processed | `new candidate` |
| `vasios_2015_mimicking_non_anonymous` | `pdf` | `vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.pdf` | `vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.md` | `medium` | `vasios_2015_mimicking_non_anonymous_processed.md` | Batch 1 | processed | `new candidate` |
| `bollen_whaley_2004_net_buying_pressure` | `pdf` | `bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf` | `bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.md` | `medium` | `bollen_whaley_2004_net_buying_pressure_processed.md` | Batch 1 | processed | `validation check` |
| `cartea_2018_order_book_signals` | `pdf` | `cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf` | `cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.md` | `medium` | `cartea_2018_order_book_signals_processed.md` | Batch 1 | processed | `new candidate` |
| `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | `pdf` | `garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf` | `garleanu_pedersen_poteshman_2005_demand_based_option_pricing.md` | `medium` | `garleanu_pedersen_poteshman_2005_demand_based_option_pricing_processed.md` | Batch 1 | processed | `EDA follow-up` |
| `nimalendran_son_2024_cream_skimming_toxic_flow` | `pdf` | `nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf` | `nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.md` | `medium` | `nimalendran_son_2024_cream_skimming_toxic_flow_processed.md` | Batch 2 | processed | `validation check` |
| `goncalves_pinto_sala_2025_incremental_option_volume` | `pdf` | `goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf` | `goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.md` | `medium` | `goncalves_pinto_sala_2025_incremental_option_volume_processed.md` | Batch 2 | processed | `validation check` |
| `roos_2026_arbitrage_free_interpolation` | `pdf` | `roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf` | `roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.md` | `high` | `roos_2026_arbitrage_free_interpolation_processed.md` | Batch 3 | processed | `EDA follow-up` |

## Guardrails

- Papers are idea sources, not official facts.
- Current-round EDA and understanding outrank paper-derived enthusiasm.
- The top-level `round4_raw_derived` processed summaries are the primary paper
  inputs for `03 Strategy`.
- `carry_forward/` files are secondary references, not co-equal with the
  current raw-derived core.
- `manual_reference/` files are outside the algorithmic `VEX` / `VEV_*`
  strategy lane unless manual scope is explicitly reopened.
- `knowledge_draft/` files are non-canonical support notes and should not be
  promoted to live logic without stronger current-round support.
- Non-implementable ideas belong in `validation`, `EDA follow-up`, or
  `inspiration-only`, not in `Trader.run()` by default.

## Assumptions

- The uploaded nine-paper local set is sufficient to start `03 Strategy`
  without further online search.
- The missing preferred paper
  `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`
  would be useful but is not necessary for strategy readiness.
- The main value of `02b` is to improve framing, candidate design, and
  validation discipline, not to replace current-round evidence.

## Open Questions / Blockers

- No blocker inside `02b` prevents `03 Strategy`.
- Exact round deadline remains unknown.

## Next Action

- Next:
  start `03 Strategy` using `02_understanding.md`,
  [`02b_strategy_handoff.md`](02b_strategy_handoff.md), and the nine-paper
  canonical `round4_raw_derived` core, while keeping `round_3` carry-forward
  papers as clearly secondary references.
