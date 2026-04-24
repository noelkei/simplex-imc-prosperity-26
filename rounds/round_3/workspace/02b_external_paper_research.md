# External Paper Research

Use `docs/templates/external_paper_research_template.md` as the structure for this file.

## Status

COMPLETED

## Sources

- Understanding summary: [`02_understanding.md`](02_understanding.md)
- Understanding context: [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- EDA evidence: [`01_eda/eda_option_surface_and_microstructure.md`](01_eda/eda_option_surface_and_microstructure.md)
- Post-run research memory: none present for Round 3
- Other named artifacts:
  - `../research/papers_raw/`
  - `../research/papers_md/`
  - `../research/papers_processed/`

## Research Goals

- Goal: collect high-ROI external methods that can sharpen Round 3 option fair
  value, residual logic, inventory control, and execution heuristics without
  violating Prosperity runtime constraints.
- Why this matters before strategy generation:
  - Round 3 is the first option-heavy round in this repo.
  - Current EDA / understanding already identify residual mispricing, surface
    sanity, and inventory / execution risk as the main open areas.
  - Papers should improve candidate design, validation checks, or
    inventory / execution heuristics rather than replace current-round
    evidence.
- Prosperity runtime / Trader constraints to preserve:
  - simple Python `Trader`
  - no external scientific libraries in the uploadable bot
  - integer prices
  - per-symbol position limits
  - online logic should stay compact and state-light

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| intrinsic / extrinsic decomposition | voucher family | understanding / EDA | strongest structural pricing frame for vouchers |
| `extrinsic_dev_day` mean reversion | `VEV_4000` to `VEV_5300` | understanding / EDA | strongest option-specific signal currently promoted |
| same-time `VELVETFRUIT_EXTRACT` anchor | active vouchers | understanding / EDA | natural fair-value anchor for option logic |
| surface monotonicity / convexity | voucher family | understanding / EDA | structural guardrail and residual frame |
| `imbalance_1` | delta-1 and active vouchers | understanding / EDA | simple online directional modifier or execution filter |
| multi-symbol inventory coupling | voucher family | understanding | key open risk because products are correlated despite separate limits |
| wide-spread passive execution | `VEV_5400`, `VEV_5500` | understanding / EDA | edge may be execution-limited rather than signal-limited |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| lagged underlying-follow | understanding / EDA | sample evidence rejects it as alpha after lag `0` |
| hydrogel-voucher hedge framing | understanding / EDA | products are effectively independent in current sample |
| dynamic alpha in floor vouchers | understanding / EDA | `VEV_6000` / `VEV_6500` are constant-floor in sample |
| feature dumping across price-anchor transforms | understanding / EDA | redundancy is high and strategy should stay parsimonious |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| TTE `5d` may behave differently from `6d-8d` history | live round is one step out-of-sample | near-expiry option-return / residual / inventory behavior |
| residual signals may need a simple analytic fair-value backbone | online implementation needs a compact formula | normal-model or short-dated call approximations |
| correlated inventory should skew per-symbol quotes | many voucher symbols share risk | multi-asset or option market-making approximations |
| wide-spread OTM options likely need passive execution rules | raw spread cost may dominate signal | limit-order placement or quote-skew heuristics |

## Target Research Questions

- What is the highest-ROI simple online fair-value approximation for short-dated
  call-like instruments when only `S`, `K`, and `T` are available?
- What literature is most useful for interpreting extrinsic / time-value
  residuals and their behaviour close to expiry?
- Which papers give implementable static-arbitrage or surface-sanity guardrails
  for cross-strike pricing?
- Which option-market or dealer-inventory papers most directly justify using
  imbalance as a secondary modifier rather than a primary alpha?
- Which multi-asset market-making papers best translate correlated inventory
  into per-symbol quote shifts without a full online Greeks stack?
- Which execution papers are actually helpful for wide-spread, low-liquidity
  option-like quoting under passive-first assumptions?

## Generated External Research Prompt

```text
You are helping a team competing in IMC Prosperity 4, an algorithmic trading competition. We are in Round 3, which introduces a set of call-option-like instruments called vouchers (symbols VEV_4000 through VEV_6500) written on an underlying called VELVETFRUIT_EXTRACT, plus a separate product HYDROGEL_PACK.

Our current round evidence says:
- HYDROGEL_PACK should be treated separately from the VELVETFRUIT_EXTRACT plus voucher family.
- VELVETFRUIT_EXTRACT is the natural anchor for voucher valuation.
- The strongest option-specific signal so far is extrinsic-value residual mean reversion, especially in VEV_4000 to VEV_5300.
- The voucher surface is almost always monotone and convex across strike.
- Order-book imbalance is a modest online modifier, not a proven primary alpha.
- Delayed underlying-follow is rejected by the data.
- VEV_5400 and VEV_5500 are execution-sensitive; VEV_6000 and VEV_6500 behave like floor instruments in sample data.

We want 5-10 highest-ROI papers or practitioner resources that improve one or more of these problems:
1. Simple online short-dated call fair value approximation usable in a basic Python Trader with no external libraries.
2. Near-expiry residual or extrinsic dynamics, especially around TTE 5-6 days.
3. Cross-strike no-arbitrage or surface-aware pricing constraints for a small set of call-like instruments.
4. Option-market order-flow / dealer-inventory interpretation relevant to imbalance and expected returns.
5. Correlated multi-product inventory-aware market making that can inspire simple quote skewing rules.
6. Passive execution or quote placement heuristics for wide-spread, low-liquidity option-like instruments.

Please prioritize practical relevance over theory. For each paper/resource, provide:
- full title, authors, year
- primary link (arXiv / SSRN / DOI / PDF)
- 2-3 sentence summary of the core method
- how it maps to our setting
- whether it suggests an implementable heuristic for a simple Trader

Please instruct us to place the selected PDFs or source folders into:
rounds/round_3/research/papers_raw/
```

## Prompt Requirements Checklist

- Ask external AI to use internet / deep research / extended reasoning if available: `yes`
- Ask for roughly 5-10 highest-ROI papers or resources: `yes`
- Prioritize implementable methods for simple online trading bots: `yes`
- Ask for links / citations / PDFs if available: `yes`
- Include upload instruction for `rounds/round_X/research/papers_raw/`: `yes`

## Online Search / Shortlist Notes

- Mode used: `mixed`
  External prompt generation, direct in-agent online shortlist / metadata
  verification, and local manual normalization of uploaded paper inputs.
- Queries / intent:
  - shortlist simple short-dated call-pricing papers with online-usable formulas
  - find option order-flow / inventory papers relevant to imbalance
  - find near-expiry / expiration-day option-return papers
  - find surface-arbitrage guardrail papers for small call sets
  - find multi-asset or option-MM papers that can be simplified into quote skew rules
- Accepted shortlist:
  - `choi_2022_bachelier_guide`
  - `muravyev_2015_option_order_flow`
  - `stoikov_saglam_2009_option_mm_inventory`
  - `garcia_ares_2023_expiration_days`
  - `fengler_2005_surface_smoothing`
  - `bergault_2022_multi_asset_mm`
  - `crr_1979_simplified_approach`
  - `west_2004_cumulative_normal`
- Rejected shortlist and why:
  - `cont_kukanov_optimal_order_placement`
    useful intuition but lower ROI than direct option-specific inventory papers
  - `baviera_massaria_additive_bachelier`
    variant-only once `Choi` already covered the normal-model backbone better
  - `andreasen_huge` and `breeden_litzenberger`
    interesting background, but lower immediate impact for a single-expiry,
    10-strike Round 3 bot

## Batch Plan

| Batch | Goal | Papers | Stop condition |
| --- | --- | --- | --- |
| 1 | unlock the first serious candidate family | `choi_2022_bachelier_guide`, `muravyev_2015_option_order_flow`, `stoikov_saglam_2009_option_mm_inventory` | stop once Strategy can branch with a paper intake pass plus at least one serious voucher candidate family |
| 2 | tighten guardrails and live-regime posture | `garcia_ares_2023_expiration_days`, `fengler_2005_surface_smoothing` | stop once these papers no longer change thresholds, validation posture, or cross-strike guardrails |
| 3 | add support variants and implementation-quality backstops | `bergault_2022_multi_asset_mm`, `crr_1979_simplified_approach`, `west_2004_cumulative_normal` | process only while they can still change spec boundaries, implementation quality, or second-wave candidate ranking |

## Paper Pipeline Status

- Expected upload folder: `../research/papers_raw/`
- Raw papers detected: `8`
- Markdown conversions pending: none
- Processed summaries pending: none
- Strategy may proceed now: `yes`
- Waiting state: `fully-processed`

## Processed Paper Index

| Paper ID | Input Type | Raw File | Markdown File | MD Fidelity | Processed Summary | Batch | Status | Action Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `choi_2022_bachelier_guide` | `latex_source` | `../research/papers_raw/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model/` | `../research/papers_md/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model.md` | `high` | `../research/papers_processed/choi_2022_bachelier_guide_processed.md` | `1` | `processed` | `new candidate` |
| `muravyev_2015_option_order_flow` | `pdf` | `../research/papers_raw/muravyev_2015_order_flow_and_expected_option_returns.pdf` | `../research/papers_md/muravyev_2015_order_flow_and_expected_option_returns.md` | `medium` | `../research/papers_processed/muravyev_2015_option_order_flow_processed.md` | `1` | `processed` | `variant` |
| `stoikov_saglam_2009_option_mm_inventory` | `pdf` | `../research/papers_raw/stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf` | `../research/papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md` | `medium` | `../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md` | `1` | `processed` | `variant` |
| `garcia_ares_2023_expiration_days` | `pdf` | `../research/papers_raw/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf` | `../research/papers_md/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.md` | `medium` | `../research/papers_processed/garcia_ares_2023_expiration_days_processed.md` | `2` | `processed` | `validation check` |
| `fengler_2005_surface_smoothing` | `pdf` | `../research/papers_raw/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf` | `../research/papers_md/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.md` | `medium` | `../research/papers_processed/fengler_2005_surface_smoothing_processed.md` | `2` | `processed` | `validation check` |
| `bergault_2022_multi_asset_mm` | `latex_source` | `../research/papers_raw/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making/` | `../research/papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md` | `high` | `../research/papers_processed/bergault_2022_multi_asset_mm_processed.md` | `3` | `processed` | `variant` |
| `crr_1979_simplified_approach` | `pdf` | `../research/papers_raw/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf` | `../research/papers_md/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.md` | `medium` | `../research/papers_processed/crr_1979_simplified_approach_processed.md` | `3` | `processed` | `validation check` |
| `west_2004_cumulative_normal` | `pdf` | `../research/papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf` | `../research/papers_md/west_2004_better_approximations_to_cumulative_normal_functions.md` | `medium` | `../research/papers_processed/west_2004_cumulative_normal_processed.md` | `3` | `processed` | `validation check` |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open
  questions.
- Non-implementable ideas should be marked `inspiration-only`,
  `validation-only`, or routed to EDA / validation, not forced into `Trader`
  logic.
- Online shortlist-building is allowed, but canonical pipeline inputs remain the
  local files under `../research/papers_raw/`.
- Do not block Strategy on the full paper pipeline.

## Assumptions

- Source-first papers should be converted before PDF-only papers when possible
  because formulas and figure references are more reliable.
- Strategy should not wait for every paper to be fully processed, but it should
  perform a paper intake pass once Batch 1 or any materially relevant processed
  set exists.

## Open Questions / Blockers

- No blocker remains for Strategy.
- No paper-processing follow-on work is pending for the current raw set.

## Next Action

- Next: start Phase 03 Strategy with a paper intake pass over the current
  `papers_processed/` set, then build the prioritized candidate queue using
  EDA, Understanding, and paper-derived ideas classified as `used`, `hybrid`,
  `validation`, `rejected`, or `inspiration-only`.
