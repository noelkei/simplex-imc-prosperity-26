# Risky Intraday Order Flow and Option Liquidity

## Source Metadata

- Input type: `pdf`
- Paper ID: `doshi_2025_risky_intraday_order_flow`
- Raw source file: [doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf)
- Primary source file: [doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with title-page abstract, section hierarchy, and empirical design preserved; explanatory prose compressed into a strategy-relevant research outline
- Fidelity status: `high` for metadata, abstract, section structure, and central empirical claims; `medium` for regression-specification details not yet retyped equation-by-equation
- QA gate: `usable`

## Paper Metadata

- Title: `Risky Intraday Order Flow and Option Liquidity`
- Authors: `Hitesh Doshi`, `Paola Pederzoli`, `Saim Ayberk Sert`
- Year on title page: `2025`
- Source note on title page: July 28, 2025 draft with conference/seminar acknowledgements
- Topic frame: short- and ultra-short-maturity options, spreads, order-flow volatility, inventory management

## Abstract

The paper analyzes trading costs for short- and ultra-short-maturity options and focuses on two classes of inventory-risk proxies: order-flow distribution and delta-hedging costs. The main result is that intraday order-flow volatility is the dominant driver of spreads, while delta-hedging needs are secondary. The authors use cross-exchange variation to isolate this effect and argue that liquidity providers rely more on trade matching than on delta hedging to manage inventory risk. This directly pushes against overly hedge-centric interpretations of short-dated option liquidity.

## Section Outline

### 1. Introduction

- Why short-dated option liquidity behaves differently from textbook delta-hedging stories
- Motivation for focusing on the intraday distribution of order flow

### 2. Theoretical Framework and Literature Review

- Inventory management, trade matching, and option-liquidity theory
- Why order-flow distribution can matter more than aggregate daily imbalance

### 3. Data

- Short- and ultra-short-maturity option sample
- Exchange-level and marketwide spread construction

### 4. Empirical Results

- Spread sensitivity to intraday order-flow volatility
- Secondary role of delta-hedging proxies
- Cross-exchange identification and robustness

### 5. Conclusion

- Active inventory management in short-dated options is driven more by unstable matching conditions than by simple hedge cost alone

## Key Equations / Core Method

### Intraday Order-Flow Distribution

The paper partitions the trading day into equispaced intervals, computes interval-level order imbalance, and then studies the volatility of that imbalance distribution within the day. That intraday volatility measure is the key liquidity-state proxy.

### Spread Regressions

The empirical design links spreads to:

- intraday order-flow volatility
- delta-hedging-cost proxies
- controls for volume, Greeks, and broader market conditions
- time or exchange structure that helps isolate the effect

### Strategy-Relevant Result

The most important current-round translation is:

- unstable intraday flow is itself a liquidity-risk state
- trade matching conditions can matter more than textbook hedge costs
- `no-trade`, `quote-widen`, or `de-risk` decisions should respond to intraday flow instability, not only to directional imbalance

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - spread regressions for short- and ultra-short-maturity options
  - comparisons between order-flow-volatility proxies and delta-hedging proxies
  - cross-exchange evidence supporting the identification argument

## Current-Round-Relevant Hooks

- Probably the single best paper in the batch for `danger-state` and `no-trade` design
- Supports building `flow-volatility` or `flow-instability` features instead of relying only on signed imbalance
- Reinforces the `VEV_5200+` reading that deteriorating liquidity can be more about matching/toxicity than about static mispricing
- Helps connect `counterparty concentration + unstable flow + widening spreads` into one defensive regime

## Conversion Caveats

- The source is recent and clean, but the full regression table detail has not yet been transcribed
- The paper's exact exchange-level instrumentation is richer than Prosperity; the transferable part is the regime logic, not the literal identification design
