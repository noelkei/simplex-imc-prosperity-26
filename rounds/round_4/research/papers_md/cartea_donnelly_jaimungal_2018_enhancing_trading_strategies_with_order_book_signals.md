# Enhancing Trading Strategies with Order Book Signals

## Source Metadata

- Input type: `pdf`
- Paper ID: `cartea_2018_order_book_signals`
- Raw source file: [cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf)
- Primary source file: [cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with abstract preservation and section-level recovery; stochastic-control details are summarized at the implementation-significant level rather than fully rederived
- Fidelity status: `high` for metadata, abstract, and high-level model structure; `medium` for exact equation notation in the dynamic-programming section
- QA gate: `usable`

## Paper Metadata

- Title: `Enhancing Trading Strategies with Order Book Signals`
- Authors: `Álvaro Cartea`, `Ryan Donnelly`, `Sebastian Jaimungal`
- Year: `2018`
- Source note on title page: `SSRN abstract 2668277`
- Topic frame: order-book imbalance, adverse selection, execution with limit orders

## Abstract

The paper constructs a volume-imbalance measure from the limit order book and shows that it predicts both the sign of the next market order and immediate post-trade price changes. It then embeds imbalance into a Markov chain modulated pure-jump model of price, spread, limit-order and market-order arrivals. In a stochastic-control execution problem, strategies that use imbalance outperform comparable strategies that ignore it, largely because imbalance helps reduce adverse-selection costs and positions quotes to benefit from favorable price moves.

## Section Outline

### 1. Introduction

- Motivation for using order-book state variables in execution and market making
- Why imbalance can matter even when spreads are tight

### 2. Volume Imbalance: Order Arrival and Price Revisions

- Definition and empirical behavior of volume imbalance
- Predictive relation between imbalance, next market-order sign, and short-horizon price moves

### 3. Trading Algorithm with Volume Imbalance Information

- Continuous-time Markov model for price, spread, order arrivals, and imbalance
- Stochastic-control problem for a limit-order trader under inventory penalties
- Out-of-sample performance comparison

### 4. Empirical / Out-of-Sample Performance

- Incremental value of imbalance-aware quoting
- Reduced adverse selection as the main improvement channel

## Key Equations / Core Method

### Core Signal: Volume Imbalance

The paper builds a buy-vs-sell pressure measure from visible order-book volume. The exact formula is not perfectly preserved by text extraction, but the source clearly uses posted depth on both sides of the book to form an imbalance state.

### State-Dependent Execution Model

The source models:

- price
- spread
- limit-order arrivals
- market-order arrivals
- imbalance state

as a joint continuous-time Markov system. The trader then optimizes limit-order placement subject to inventory penalties.

### Strategy-Relevant Result

The practical takeaway is simple and strong: imbalance improves trading performance primarily because it lowers adverse-selection costs. That maps directly into `round_4` as:

- quote less aggressively in bad imbalance states
- suppress exposure when flow and book state point the same way
- let imbalance act as a defensive filter even if it is not a direct alpha

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - imbalance-predictability figures
  - model calibration / out-of-sample performance tables
  - execution-performance comparisons with and without imbalance

## Current-Round-Relevant Hooks

- Strong candidate source for `no-trade`, `quote-suppression`, and `reduce-size` rules
- Supports using book state as a first-class feature alongside counterparty state
- Helps connect `trade-to-book context` from the EDA to strategy logic
- Reinforces the idea that some signals are best used defensively, not as naked directional alpha
- Good translation layer for `danger-state` implementation in `VEV_5200+` and potentially `5300`

## Conversion Caveats

- The value of the paper for `round_4` is mostly operational and structural, not tied to its full continuous-time optimization machinery
- Exact equation recovery for the dynamic-programming section is partial; use the paper for signal design and execution guardrails, not for copying the full control model
