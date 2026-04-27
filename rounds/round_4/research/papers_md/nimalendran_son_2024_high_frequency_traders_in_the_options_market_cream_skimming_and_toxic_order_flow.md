# High-Frequency Traders in the Options Market: Cream Skimming and Toxic Order Flow

## Source Metadata

- Input type: `pdf`
- Paper ID: `nimalendran_son_2024_cream_skimming_toxic_flow`
- Raw source file: [nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf)
- Primary source file: [nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/nimalendran_son_2024_high_frequency_traders_in_the_options_market_cream_skimming_and_toxic_order_flow.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with title-page abstract recovery, section-outline reconstruction, and emphasis on the toxic-vs-non-toxic flow distinction that matters for current-round adaptation
- Fidelity status: `high` for metadata and abstract, `medium` for exact model notation and proof detail
- QA gate: `usable`

## Paper Metadata

- Title: `High-Frequency Traders in the Options Market: Cream Skimming and Toxic Order Flow`
- Authors: `Mahendrarajah Nimalendran`, `Matthew G. Son`
- Year: `2024` working-paper form
- Source note on title page: CBOE-data study of professional customers in options markets
- Topic frame: option-market microstructure, professional customers, stale-quote arbitrage, cream skimming, spread widening

## Abstract

The paper studies high-frequency options traders, labeled professional customers (PCs), and examines how they affect option-market microstructure. It develops a model in which speed advantage creates two mechanisms: toxic arbitrage that exploits stale quotes and non-toxic arbitrage that cream-skims uninformed flow. Both widen spreads, but cream skimming dominates in low-volatility states. Using CBOE data, the paper finds that PCs target large uninformed customer orders, avoid informed flow, and withdraw around earnings, which shifts adverse-selection risk to market makers and increases spreads materially.

## Section Outline

### 1. Model

- Speed advantage and the distinction between toxic and non-toxic arbitrage
- How option-market structure changes the impact of fast traders relative to equities

### 2. Empirical Implications of the Model

- Predictions for spread widening, flow selection, and state dependence
- When cream skimming dominates versus when toxic arbitrage becomes more important

### 3. Empirical Results

- Evidence that professional customers target uninformed flow
- Evidence that they avoid more informationally dangerous states
- Spread effects and market-quality implications

### 4. Conclusion

- Fast options flow changes liquidity provision through both toxicity and selective liquidity-taking

## Key Equations / Core Method

### Dual Mechanism: Toxic Arbitrage vs Cream Skimming

The paper's central contribution is conceptual rather than a single simple formula:

- `toxic arbitrage`: exploit stale quotes or informational lag
- `cream skimming`: selectively trade against uninformed customer flow before market makers can monetize it

Both mechanisms worsen market-making conditions, but they imply different runtime interpretations. Toxic flow is danger-state flow; cream-skimming flow is selective extraction of easy liquidity.

### Strategy-Relevant Translation

For `round_4`, the paper is valuable because it sharpens the distinction between:

- a participant who is informative because they are directionally right
- and a participant who is dangerous because they selectively attack bad liquidity states

That distinction is crucial for deciding whether `Mark XX`-style flow should be read as alpha, veto, or quote-suppression context.

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - spread and liquidity comparisons across states
  - evidence on professional-customer targeting behavior
  - state-dependent decomposition of toxic vs cream-skimming effects

## Current-Round-Relevant Hooks

- Strong guardrail for interpreting concentrated seller flow in `VEV_5200+`
- Supports `danger-state` logic where the real problem is selective exploitation of fragile liquidity
- Helps explain why some participant patterns should lead to `quote less`, `reduce size`, or `do not join`
- Useful bridge between `counterparty ecology` and `trade-to-book context`

## Conversion Caveats

- The paper is centered on professional-customer classification, which Prosperity does not expose directly
- The main reusable layer is the behavioral distinction between flow types, not the exact participant labels or market-share magnitudes
