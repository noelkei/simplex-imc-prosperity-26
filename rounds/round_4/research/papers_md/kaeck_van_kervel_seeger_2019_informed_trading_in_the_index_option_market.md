# Informed Trading in the Index Option Market

## Source Metadata

- Input type: `pdf`
- Paper ID: `kaeck_2019_informed_index_options`
- Raw source file: [kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf)
- Primary source file: [kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with abstract and section hierarchy preserved; the VAR/SVAR setup is summarized around the delta/vega aggregation idea that matters for current-round adaptation
- Fidelity status: `high` for metadata, abstract, and the core delta/vega-flow methodology; `medium` for equation-level notation beyond the central decomposition idea
- QA gate: `usable`

## Paper Metadata

- Title: `Informed Trading in the Index Option Market`
- Authors: `Andreas Kaeck`, `Vincent van Kervel`, `Norman J. Seeger`
- Year: `2019` working-paper form
- Source note on title page: `SSRN abstract 2981332`
- Topic frame: informed trading, option order-flow aggregation, underlying-price and volatility information

## Abstract

The paper proposes a structural VAR framework to detect informed trading in option markets. Its key move is to decompose option order flow into exposure to the underlying price via option delta and exposure to volatility via option vega, then aggregate those flows across strikes and maturities. The fitted model finds that option trades can be informative about both the underlying and volatility. The main methodological value is the aggregation logic: instead of treating each contract as a separate noisy series, it compresses the cross section into more interpretable family-level flow variables.

## Section Outline

### 1. Introduction

- Why informed option trading is hard to detect at the single-contract level
- Need to aggregate across strikes and maturities without losing economic meaning

### 2. Model / Identification Logic

- Structural framework for linking option order flow to underlying and volatility information
- Economic interpretation of delta and vega flow

### 3. Empirical Setup

- Construction of signed option order flow
- Aggregation into delta and vega order-flow measures
- VAR specification linking flows, underlying returns, and volatility changes

### 4. Empirical Results

- Evidence that option flow is informative about both price and volatility
- Incremental value of delta-flow and vega-flow decomposition

### 5. Conclusion

- Aggregated Greeks-based option flow is more informative than contract-level fragmentation

## Key Equations / Core Method

### Delta and Vega Order Flow

The central method is to convert raw signed option trading into family-level economic exposures:

- `delta order flow`: signed option flow weighted by option delta
- `vega order flow`: signed option flow weighted by option vega

This lets the researcher aggregate trades across strikes and maturities while preserving whether the flow is effectively about the underlying price or about volatility.

### Structural VAR Framing

The paper then places:

- underlying-return changes
- volatility changes
- delta order flow
- vega order flow
- underlying cash-market order flow

inside a VAR-style system to identify how informed option flow transmits into the broader market.

### Strategy-Relevant Translation

For `round_4`, the biggest payoff is not the exact econometrics. It is the idea that option-book flow should be compressed into economically meaningful family variables instead of staying as isolated strike-local counts.

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - model-identification illustrations for delta and vega order flow
  - VAR result tables for flow informativeness
  - empirical comparisons between aggregated and fragmented flow views

## Current-Round-Relevant Hooks

- Strong support for `cross-strike / family-level flow` over symbol-isolated logic
- Useful inspiration for building `VEX-linked family pressure` and `surface-aware flow` features
- Suggests a role split between `price-like flow` and `vol-like flow`, which may matter for interpreting upper-strike selling
- Good source for deciding whether some `VEV_*` strikes should be treated as flow context rather than direct inventory

## Conversion Caveats

- The source is built for institutional option data with richer cross-section and maturity structure than Prosperity
- The exact VAR identification is likely too heavy for live bot logic; the main reusable object is the flow aggregation scheme
