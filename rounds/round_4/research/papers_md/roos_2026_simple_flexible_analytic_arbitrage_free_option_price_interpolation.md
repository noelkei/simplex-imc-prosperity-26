# Simple, Flexible, Analytic, Arbitrage Free Option Price Interpolation

## Source Metadata

- Input type: `pdf`
- Paper ID: `roos_2026_arbitrage_free_interpolation`
- Raw source file: [roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf)
- Primary source file: [roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with clean abstract and section recovery; focus placed on the practical interpolation scheme and its operational tradeoffs
- Fidelity status: `high`
- QA gate: `usable`

## Paper Metadata

- Title: `Simple, Flexible, Analytic, Arbitrage Free Option Price Interpolation`
- Author: `Thomas Roos`
- Year: `2026`
- Version note on title page: `v1.0 March 17, 2026`
- Topic frame: strike interpolation, expiry interpolation, arbitrage-free option-price construction

## Abstract

The paper introduces an interpolation methodology for option prices across strikes at a given expiry. The scheme is asset-class independent, arbitrage free, flexible enough to match an arbitrary number of input quotes, and allows explicit wing control. Prices and implied volatilities are analytically computed at a cost comparable to Black-Scholes evaluation, while retaining `C^2` smoothness and an intuitive discrete-time local-volatility interpretation. The paper also discusses arbitrage-free interpolation across expiries.

## Section Outline

### 1. Introduction

- Motivation for simple, fast, arbitrage-free interpolation

### 2. Rate-like Underlyings

- Special-case framing and motivation

### 3. Option Prices

- Desired structural properties for price interpolation

### 4. The Asset Model

- Model backbone used to guarantee arbitrage-free interpolation

### 5. Calibration

- Matching input quotes and controlling wings

### 6. Risk

- Smoothness and risk sensitivity implications

### 7. Expiry Interpolation

- Arbitrage-free handling across maturities

### 8. Numerical Results

- Practical examples and computational behavior

### 9. Conclusion

- Simple analytic interpolation as a robust middle ground between naive BS and heavy stochastic-vol stacks

## Key Equations / Core Method

### Core Promise

The paper aims to interpolate option prices directly rather than forcing a noisy implied-vol fit, while preserving:

- no static arbitrage across strikes
- flexibility to match observed quotes
- explicit wing control
- analytic speed close to Black-Scholes

### Strategy-Relevant Translation

For `round_4`, the value is not "implement Roos live in full". It is:

- use a simple arbitrage-aware surface backbone
- avoid reading every kink in sparse quotes as alpha
- preserve a cheap local surface context for residual checks or sanity filtering

This is a good candidate for `EDA follow-up` or offline validation support rather than immediate bot logic.

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - interpolation examples across strikes
  - wing-control illustrations
  - numerical comparisons showing low computational cost

## Current-Round-Relevant Hooks

- Good source for a lightweight `surface sanity layer`
- Helps avoid overreacting to sparse or noisy voucher quotes
- More compatible with Prosperity runtime constraints than a full Heston/COS deployment

## Conversion Caveats

- This is a recent technical interpolation note, not a microstructure paper
- Its main value is structural and diagnostic; any live use should likely be a simplified residual/surface check, not a full-model dependency
