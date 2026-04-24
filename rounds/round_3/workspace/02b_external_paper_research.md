# External Paper Research — Round 3

## Status

`IN_PROGRESS`

Phase logic: prompt generated; waiting for paper uploads. Strategy may proceed
while this phase is in a wait state. Phase is complete once at least one
processed paper exists in `../research/papers_processed/`.

## Sources

- Understanding summary: `02_understanding.md`
- Understanding context: `phase_02_understanding_context.md`
- EDA evidence: `01_eda/eda_option_surface_and_microstructure.md`
- Post-run research memory: none (first time in Round 3)
- Other named artifacts:
  - `../data/processed/derived_round_3_option_reversion_metrics.csv`
  - `../data/processed/derived_round_3_option_extrinsic_by_tte.csv`
  - `../data/processed/derived_round_3_option_surface_summary.csv`
  - `../data/processed/derived_round_3_underlying_option_lead_lag.csv`
  - `01_eda/artifacts/round_3_eda_summary_metrics.json`

## Research Goals

- Goal: find 5–8 high-ROI academic papers or practitioner resources that can
  inspire implementable techniques for short-dated call-option market-making
  and residual/extrinsic-value exploitation in a discrete, position-limited,
  low-TTE environment.
- Why this matters before strategy generation: understanding supplies the
  signal ledger and process hypotheses but does not provide calibrated methods
  for theta decay, surface arbitrage, or execution under wide option spreads.
  External literature can close the gap between "we see extrinsic reversion"
  and "here is a concrete formula or algorithm to exploit it."
- Prosperity runtime / Trader constraints to preserve:
  - `Trader.run()` must be a single Python function; no external libraries
    (no `scipy`, no `numpy`, no `pandas`) unless standard builtins.
  - All state must pass through `traderData` as a JSON string.
  - Per-symbol position limit is ±300 for each `VEV_*` voucher; ±50 for
    `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` (confirm exact limits in spec).
  - Orders are discrete integer price ticks; no fractional prices.
  - Historical TTE window is 6–8 days; live round runs at TTE 5 days
    (one step out-of-sample vs history).

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| `extrinsic_dev_day` (residual above day-product baseline) | `VEV_4000`–`VEV_5300` | `derived_round_3_option_reversion_metrics.csv` | strongest MI-ranked option signal; reversion corr `–0.7` for ITM strikes |
| intrinsic / extrinsic decomposition (call payoff structure) | all vouchers | `derived_round_3_option_extrinsic_by_tte.csv` | converts raw prices into option-theoretic space; needed for residual frame |
| same-time `VELVETFRUIT_EXTRACT` coupling | `VEV_5000`–`VEV_5300` | `derived_round_3_same_time_return_corr.csv` | correlations 0.72–0.76; defines anchor relationship, not lagged follow |
| `imbalance_1` (top-of-book bid/ask volume asymmetry) | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, active vouchers | `derived_round_3_product_signal_metrics.csv` | PCA isolates this on PC2 (16.7%); mild directional/overlay role |
| surface monotonicity / convexity across strikes | voucher family | `derived_round_3_option_surface_summary.csv` | 99.91%–100% stable in sample; useful as sanity check and residual frame |
| theta / TTE decay calibration | all vouchers | `derived_round_3_option_extrinsic_by_tte.csv` | extrinsic shrinks day-on-day; live is TTE 5d vs 6–8d in history |
| spread-aware execution filter | `VEV_5400`, `VEV_5500` and all options | `derived_round_3_trade_alignment_summary.csv` | relative spreads 900–1859 bps; raw signal likely dominated by costs |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| Lagged underlying-delta follow into vouchers | `derived_round_3_underlying_option_lead_lag.csv` | correlations collapse to near zero at lag 1, 2, 5, 10; complexity with no sample edge |
| Feature dumping across price-anchor family | `derived_round_3_option_pca_loadings.csv` | PC1 (72%) loads evenly on mid, intrinsic, moneyness, spread; they are all the same axis |
| Dynamic alpha from `VEV_6000` / `VEV_6500` | `derived_round_3_product_signal_metrics.csv` | constant 0.5 mids, zero variance, 20000 bps relative spread; floor regime only |
| Pooled linear model as standalone predictor | `derived_round_3_pooled_option_linear_model.csv` | `R² = 0.0159`; ranking evidence only, not direct bot logic |
| Treating hydrogel and velvetfruit as a cross-hedge | `derived_round_3_same_time_return_corr.csv` | correlation 0.006; independent processes |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| How much does extrinsic residual reversion strengthen or weaken at TTE 5d vs 8d? | live round is one step out-of-sample; misfit here could mean bad baselines | papers on short-dated option residual dynamics and theta acceleration near expiry |
| Is there a simple closed-form approximation for extrinsic value that works online without `scipy`? | Trader needs a fast per-tick valuation formula | analytic approximations to Black-Scholes or binomial near-expiry that avoid special functions |
| What is the cleanest way to detect and exploit cross-strike monotonicity / convexity violations? | surface sanity is a guardrail; residual logic may be improvable if structural breaks are detectable | calendar / butterfly spread arbitrage literature; surface arbitrage bounds |
| Is `imbalance_1` a stronger signal in option books than in equity books, given the wide spreads? | MI rank is modest; deciding primary vs overlay role shapes spec complexity | literature on order-book imbalance in illiquid or wide-spread derivative markets |
| What position-sizing or inventory management rules best handle ±300-limit multi-strike portfolios? | 10 voucher symbols with independent limits; cross-strike delta exposure is implicit | multi-asset inventory management under position limits; Avellaneda-Stoikov extensions |
| Are there simple passive execution heuristics for OTM options that survive costs better than aggressive fills? | `VEV_5400` / `VEV_5500` may only be viable passively | passive market-making with asymmetric fill probability and wide-spread environments |

## Target Research Questions

- Q1: What are the best simple online algorithms for tracking extrinsic /
  time value of a short-dated call option using only observable book data
  (mid, strike, TTE), and how do they handle the final few days before expiry?
- Q2: Are there closed-form or lookup-table approximations to call option fair
  value near expiry (TTE < 10 days) that require no `scipy` or special math
  functions, suitable for embedding in a Trader class?
- Q3: What does the literature say about residual mispricing and mean
  reversion in listed option markets, and which signal features predict
  reversion best in empirical studies?
- Q4: How should a market-maker or relative-value trader handle a strip of
  call options at multiple strikes simultaneously, given monotonicity and
  convexity surface constraints?
- Q5: What is the evidence for (or against) `imbalance_1`-style order-book
  signals in derivative markets, especially when spreads are very wide?
- Q6: How can a multi-product bot manage inventory across 10 correlated option
  symbols with individual position limits, without access to a proper portfolio
  delta / greeks calculator in real time?
- Q7: What execution models exist for passively market-making in illiquid
  options (relative spread > 500 bps), and what are their known failure modes?

## Generated External Research Prompt

```text
You are helping a team competing in IMC Prosperity 4, an algorithmic trading
competition. We are in Round 3, which introduces a set of call-option-like
instruments called "vouchers" (symbols VEV_4000 through VEV_6500) written on
an underlying called VELVETFRUIT_EXTRACT, plus a separate product
HYDROGEL_PACK. Our bots run as a simple Python Trader class with no external
libraries (no scipy, no numpy), discrete integer prices, ±300 position limits
per voucher, and all state passed as a JSON string.

Our EDA and understanding work has produced the following key findings:

SIGNALS WE TRUST:
• Extrinsic value (= mid_price - max(0, underlying - strike)) tracks a
  day-product baseline, and deviations from that baseline mean-revert
  (reversion correlation ~-0.70 for ITM strikes VEV_4000/4500). This is our
  strongest option signal.
• VELVETFRUIT_EXTRACT is the natural anchor for voucher valuation; same-time
  return correlations of 0.72–0.76 with VEV_5000/5100/5200 make it the
  best real-time fair-value proxy.
• The option surface is essentially always monotone (100%) and convex
  (~99.9%) across strikes, suggesting surface structure is useful as a
  sanity guardrail or residual frame.
• Top-of-book order imbalance (bid vol – ask vol / total) has a modest
  directional effect (MI rank 4th out of 5 features, R² contribution ~zero
  in pooled linear model), but is simple and online.

SIGNALS WE REJECT:
• Lagged underlying-to-option delta-follow: correlations collapse near zero
  at lag 1 and beyond. Complexity with no edge.
• VEV_6000/VEV_6500: constant 0.5 mids, zero variance — floor regime only.
  Not tradable for alpha.
• Feature stacking across price/intrinsic/moneyness/spread: all load onto
  the same PCA component (PC1 = 72%). Pick one anchor, not all of them.

KEY OPEN PROBLEMS:
1. We need a simple ONLINE call option fair value formula (no scipy.stats)
   for TTE 5–8 days, integer strikes, using only the underlying mid price
   and strike. It must be fast enough to call 1000+ times per backtest day.
2. We need to understand how extrinsic residual reversion behaves specifically
   in the TTE 5–6 day range (our live round is TTE 5d; our history only has
   TTE 6–8d). Does reversion speed accelerate near expiry? 
3. We need to manage inventory across 10 correlated option symbols with
   independent ±300 position limits, without computing Greeks in real time.
4. We need execution heuristics for very wide-spread OTM options (relative
   spread > 900 bps for VEV_5400/5500) where passive fills are the only
   viable approach.
5. We'd like to know whether order-book imbalance in option markets (vs
   equity markets) carries different predictive properties, especially near
   expiry.

Please find 5–8 high-ROI papers or practitioner resources that address our
open problems. For each, provide:
• Full title, authors, year
• arXiv / SSRN / DOI link or PDF source if available
• 2–3 sentence summary of the core method
• How it maps to our specific situation (short-dated calls, wide spreads,
  discrete prices, no scipy, position limits)
• Whether it suggests a concrete implementable formula or heuristic we
  could embed in a Python Trader class

Priority order for papers:
1. Simple closed-form / analytic approximations for short-dated call option
   fair value (Black-Scholes near-expiry, binomial trees, Bachelier model)
2. Extrinsic / time value residual dynamics and mean reversion in option
   markets near expiry
3. Multi-strike option surface arbitrage / monotonicity-aware pricing
4. Order-book imbalance signals in derivative / option markets
5. Inventory management for multi-product market-makers under position limits
   (Avellaneda-Stoikov extensions or similar)
6. Passive execution strategies for wide-spread / illiquid options

Please use internet search, deep research mode, and extended reasoning if
available. Focus on practical relevance over theoretical elegance. Prefer
results that can inspire a bot implementable in fewer than 200 lines of Python
with no external dependencies.

After generating your response, instruct us to download the most relevant
PDFs and upload them to:
  rounds/round_3/research/papers_raw/
so our pipeline can convert them to Markdown and extract strategy implications.
```

## Prompt Requirements Checklist

- Ask external AI to use internet / deep research / extended reasoning if available: `yes`
- Ask for roughly 5-10 highest-ROI papers or resources: `yes` (5–8)
- Prioritize implementable methods for simple online trading bots: `yes`
- Ask for links / citations / PDFs if available: `yes`
- Include upload instruction for `rounds/round_3/research/papers_raw/`: `yes`

## Paper Pipeline Status

- Expected upload folder: `../research/papers_raw/`
- Raw papers detected: none
- Markdown conversions pending: none
- Processed summaries pending: none
- Strategy may proceed now: `yes` — proceed data-driven while waiting for papers
- Waiting state: `prompt-generated-waiting`

## Processed Paper Index

| Paper ID | Raw File | Markdown File | Processed Summary | Status | Action Classification |
| --- | --- | --- | --- | --- | --- |
| TBD | none | none | none | waiting | no action yet |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open questions.
- Non-implementable ideas should be marked `inspiration only` or routed to
  validation / EDA, not forced into Trader logic.
- Do not hallucinate paper contents before files exist.
- Do not block strategy on the full raw → md → processed pipeline.

## Assumptions

- The voucher instruments behave like vanilla call options (call-payoff at
  expiry) written on `VELVETFRUIT_EXTRACT`.
- Historical TTE labels (day 0 = 8d, day 1 = 7d, day 2 = 6d) are correct.
- The live round runs at TTE 5d, one step beyond the historical sample.
- Simple Python arithmetic (no scipy) can produce a usable fair value estimate
  if we find the right approximation formula.

## Open Questions / Blockers

- No processed papers yet; pipeline is in wait state.
- TTE 5d residual behavior remains unobserved in historical data.

## Next Action

- **You (human + external AI)**: paste the prompt above into an AI with
  internet or deep-research access (e.g. Perplexity Pro, ChatGPT with
  browsing, Gemini Deep Research). Download the most relevant PDFs it
  recommends and upload them to `rounds/round_3/research/papers_raw/`.
- **This pipeline**: once any file appears in `papers_raw/`, convert it to
  Markdown in `papers_md/` and produce a processed summary in
  `papers_processed/`, then mark this phase `COMPLETED`.
- **Strategy (Phase 03)**: proceed now, data-driven; consume any processed
  papers incrementally as they become available.
