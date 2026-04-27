# External Paper Research

Use `docs/templates/external_paper_research_template.md` as the structure for this file.

## Status

IN_PROGRESS

## Sources

- Understanding summary:
  - [`02_understanding.md`](02_understanding.md)
- Understanding context:
  - [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- EDA evidence:
  - [`01_eda/eda_round_4_counterparty_and_option_book.md`](01_eda/eda_round_4_counterparty_and_option_book.md)
  - [`01_eda/eda_round_4_counterparty_profiles.md`](01_eda/eda_round_4_counterparty_profiles.md)
  - [`01_eda/eda_round_4_option_book_structure.md`](01_eda/eda_round_4_option_book_structure.md)
  - [`01_eda/eda_round_4_option_volatility_and_pricing.md`](01_eda/eda_round_4_option_volatility_and_pricing.md)
  - [`01_eda/eda_round_4_round3_revalidation.md`](01_eda/eda_round_4_round3_revalidation.md)
- Post-run research memory:
  - [`../../round_3/workspace/post_run_research_memory.md`](../../round_3/workspace/post_run_research_memory.md)
- Other named artifacts:
  - [`00_ingestion.md`](00_ingestion.md)
  - [`00_prior_round_intake.md`](00_prior_round_intake.md)
  - [`../../round_3/workspace/06_testing/round_3_closeout_retrospective.md`](../../round_3/workspace/06_testing/round_3_closeout_retrospective.md)

## Research Goals

- Goal:
  find the highest-ROI external papers or primary resources that can help turn
  the current `round_4` understanding into better strategy candidates without
  bloating the bot with offline-only quant machinery.
- Why this matters before strategy generation:
  `round_4` adds visible counterparties to the same algorithmic market as
  `round_3`, and the main open questions are not generic finance questions:
  they are about participant-conditioned option-book context, danger-state vs
  inventory-worthiness, simple surface-aware pricing, and no-trade / defensive
  gating under concentrated flow and widening friction.
- Prosperity runtime / Trader constraints to preserve:
  - uploadable bot is a simple Python `Trader.run(state)` style agent
  - current-round strategy must rely on online-observable fields only
  - offline research outputs may shape framing and validation, but should not
    force heavyweight runtime dependencies
  - simple, implementable, role-aware logic is preferred over academically
    elegant but operationally heavy models

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| `VEX` same-time anchor linkage | `VELVETFRUIT_EXTRACT` + `VEV_*` | understanding / EDA | strongest structural pricing and role anchor in the voucher family |
| role-first option-book framing | `VEV_*` family | understanding / EDA | `5000/5100/5200/5300/5400+/6000+` are not homogeneous and should not be treated as one basket |
| counterparty concentration and dominance | `VEV_5200+`, `5300`, upper/floor | understanding / EDA | strongest new `round_4` information surface; likely contextual rather than naked alpha |
| `Mark 22` seller danger-state story | `VEV_5200+` | understanding / EDA | best current candidate for a participant-conditioned defensive or veto-style state |
| trade-location context | aligned trade layer | understanding / EDA | links counterparties to book microstructure better than raw names alone |
| `5300` special-strike behavior | `VEV_5300` | understanding / EDA + `round_3` carry-forward | still the most important unresolved active-strike question |
| surface-aware but lightweight pricing context | `VEV_*` | understanding / EDA | IV/Greeks/Heston evidence says flat-vol framing is incomplete, but live heavy quant stack is probably wrong |
| family imbalance / family-level exposure | voucher family | understanding / unresolved `round_3` backlog | still unresolved and potentially more useful than symbol-local imbalance |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| broad reopening of `5000/5100/5200/5300` as one active basket | understanding + `round_3` closeout | repeatedly bad framing in `round_3`, not rescued by `round_4` raw data |
| delayed-follow voucher logic | understanding / EDA | lagged correlations collapse after lag `0` |
| raw counterparty names as primary alpha | understanding / EDA | descriptive structure is real, but direct predictive power is weak |
| upper/floor direct aggression | understanding / EDA | friction and concentration are extreme, and floor strikes are structurally non-tradable by default |
| heavy live Heston / COS machinery | understanding / EDA | useful research benchmark, poor default runtime choice |
| universal late-session toxicity as a global rule | understanding + `round_3` unresolved carry-forward | timing deterioration may be product-specific rather than universal |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| when does participant flow become useful as contextual state rather than direct alpha? | key `round_4` novelty | practical methods and diagnostics from option/market microstructure |
| how to distinguish signal-only derivatives from inventory-worthy derivatives in short-dated books? | central `5200` / `5300` / upper-strike question | simple, implementable frameworks or empirical heuristics |
| what lightweight surface-aware pricing or residual methods are robust enough for short-dated option books? | advanced pricing layer needs pragmatic translation | residual / local-surface / simple option-pricing references |
| how to design no-trade / defensive gating when friction and participant concentration worsen? | directly affects execution and risk posture | execution, adverse-selection, and market-making guardrail literature |
| how should family-level option exposure or imbalance be framed without overcomplication? | unresolved `round_3` carry-forward | option MM / cross-strike risk-control papers with simple usable ideas |

## Target Research Questions

- Which papers or practitioner-grade resources best explain how to use visible participant or order-flow structure as contextual state in options or linked-product trading, rather than as naive direct alpha?
- Which papers best distinguish adverse-selection / toxic-flow states from inventory-worthy states in short-dated or highly fragmented option books?
- Which practical pricing or residual frameworks are simplest and most robust for short-dated option families when flat-vol is too naive but a full stochastic-volatility live stack is too heavy?
- Which papers give actionable no-trade, quote-suppression, or defensive gating ideas for widening-spread / concentrated-flow regimes?
- Which papers are most useful for family-level or cross-strike exposure framing in small option books, especially when some strikes may be better as signal or veto inputs than as direct inventory?

## Online Search / Shortlist Notes

- Mode used: `mixed`
- Queries / intent:
  - find highest-ROI papers for `round_4` that are genuinely new relative to
    `round_3`
  - verify title / author metadata for uploaded raw files before conversion
  - filter out already-processed `round_3` papers such as Muravyev, Stoikov /
    Saglam, Fengler, and Choi
- Accepted shortlist:
  - `vasios_2015_mimicking_non_anonymous`
  - `cartea_2018_order_book_signals`
  - `kaeck_2019_informed_index_options`
  - `bollen_whaley_2004_net_buying_pressure_iv_shape`
  - `nimalendran_son_2024_cream_skimming_toxic_flow`
  - `doshi_2025_risky_intraday_order_flow`
  - `roos_2026_arbitrage_free_option_price_interpolation`
  - `goncalves_pinto_sala_2025_incremental_option_volume`
  - `garleanu_pedersen_poteshman_2005_demand_based_option_pricing`
- Rejected shortlist and why:
  - `muravyev_2015_order_flow_and_expected_option_returns`: already processed
    in `round_3`
  - `stoikov_saglam_2009_option_market_making_under_inventory_risk`: already
    processed in `round_3`
  - `fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface`:
    already processed in `round_3`
  - `choi_2022_black_scholes_users_guide_to_the_bachelier_model`: already
    processed in `round_3`
  - `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`:
    shortlisted, but not yet present in local raw set

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
5. What family-level / cross-strike exposure or imbalance frameworks are useful in small option books where some strikes are better as context than inventory?

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
- Include upload instruction for `rounds/round_X/research/papers_raw/`: `yes`

## Batch Plan

| Batch | Goal | Papers | Stop Condition |
| --- | --- | --- | --- |
| Batch 1 | FIRST-CANDIDATE-CHANGING | `vasios_2015_mimicking_non_anonymous`, `doshi_2025_risky_intraday_order_flow`, `kaeck_2019_informed_index_options`, `bollen_whaley_2004_net_buying_pressure`, `cartea_2018_order_book_signals` | once the first 2-4 selected papers materially affect candidate ranking |
| Batch 2 | GUARDRAIL_OR_REGIME | `nimalendran_son_2024_cream_skimming_toxic_flow`, `goncalves_pinto_sala_2025_incremental_option_volume` | once strategy guardrails and validation checks are sufficiently grounded |
| Batch 3 | BENCHMARK_OR_UTILITY | `roos_2026_arbitrage_free_interpolation`, `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | once pricing/framing and family-risk notes stop changing spec or validation posture |

## Paper Pipeline Status

- Expected upload folder: `rounds/round_4/research/papers_raw/`
- Raw papers detected: 9 normalized PDFs in local raw set
- Markdown conversions pending: none
- Processed summaries pending: all 9 raw papers
- Strategy may proceed now: `yes`
- Waiting state: `ready-to-process`

## Processed Paper Index

| Paper ID | Input Type | Raw File | Markdown File | MD Fidelity | Processed Summary | Batch | Status | Action Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `vasios_2015_mimicking_non_anonymous` | `pdf` | `vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.pdf` | `vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.md` | `medium` | none | Batch 1 | `converted-usable` | `new candidate` |
| `cartea_2018_order_book_signals` | `pdf` | `cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf` | `cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.md` | `medium` | none | Batch 1 | `converted-usable` | `new candidate` |
| `kaeck_2019_informed_index_options` | `pdf` | `kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf` | `kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.md` | `medium` | none | Batch 1 | `converted-usable` | `new candidate` |
| `bollen_whaley_2004_net_buying_pressure` | `pdf` | `bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf` | `bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.md` | `medium` | none | Batch 1 | `converted-usable` | `validation check` |
| `doshi_2025_risky_intraday_order_flow` | `pdf` | `doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf` | `doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.md` | `high` | none | Batch 1 | `converted-usable` | `new candidate` |
| `nimalendran_son_2024_cream_skimming_toxic_flow` | `pdf` | `nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf` | `nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.md` | `medium` | none | Batch 2 | `converted-usable` | `validation check` |
| `goncalves_pinto_sala_2025_incremental_option_volume` | `pdf` | `goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf` | `goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.md` | `high` | none | Batch 2 | `converted-usable` | `no action` |
| `roos_2026_arbitrage_free_interpolation` | `pdf` | `roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf` | `roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.md` | `high` | none | Batch 3 | `converted-usable` | `EDA follow-up` |
| `garleanu_pedersen_poteshman_2005_demand_based_option_pricing` | `pdf` | `garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf` | `garleanu_pedersen_poteshman_2005_demand_based_option_pricing.md` | `high` | none | Batch 3 | `converted-usable` | `EDA follow-up` |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open questions.
- Online shortlist-building is allowed, but canonical pipeline inputs remain the local files under `papers_raw/`.
- Non-implementable ideas should be marked `inspiration-only` or routed to validation / EDA, not forced into Trader logic.
- Do not hallucinate paper contents before files exist.
- Do not block strategy on the full raw -> md -> processed pipeline.

## Assumptions

- `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`
  remains desirable but is not required to start the local conversion pipeline
  because `vasios_2015_mimicking_non_anonymous` covers a closely adjacent
  non-anonymous-flow theme.

## Open Questions / Blockers

- Missing from the preferred long shortlist:
  `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`.
- Exact deadline is still unknown.

## Next Action

- Next:
  process the converted Batch 1 Markdown files into
  `rounds/round_4/research/papers_processed/`, starting with
  `doshi_2025_risky_intraday_order_flow`, `kaeck_2019_informed_index_options`,
  and `vasios_2015_mimicking_non_anonymous`, while keeping `03 Strategy`
  unblocked.
