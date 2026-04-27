# Demand-Based Option Pricing

## Source Metadata

- Input type: `pdf`
- Paper ID: `garleanu_pedersen_poteshman_2005_demand_based_option_pricing`
- Raw source file: [garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf)
- Primary source file: [garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with clean abstract and section recovery; emphasis on the demand-pressure propagation logic across option contracts
- Fidelity status: `high` for metadata, abstract, and central conceptual result; `medium` for full derivation detail
- QA gate: `usable`

## Paper Metadata

- Title: `Demand-Based Option Pricing`
- Authors: `Nicolae Garleanu`, `Lasse Heje Pedersen`, `Allen M. Poteshman`
- Year on NBER working paper: `2005`
- Source note on title page: `NBER Working Paper 11843`
- Topic frame: demand pressure, incomplete hedging, cross-contract covariance, option smirks and expensiveness

## Abstract

The paper models how demand pressure affects option prices when options cannot be perfectly hedged. It shows that demand pressure in one option raises its own price in proportion to the variance of its unhedgeable component and raises other option prices in proportion to the covariance of their unhedgeable components. Empirically, the authors use dealer and end-user positions to explain familiar option-pricing puzzles, including expensive index options, the smirk, and the pricing of single-stock options. The key message is that demand can move whole regions of the option surface, not just isolated contracts.

## Section Outline

### 1. Introduction

- Why demand matters when option risk cannot be perfectly hedged
- Link to smirks, expensive puts, and broad option-pricing puzzles

### 2. Theoretical Framework

- Incomplete-hedging environment
- Demand pressure and the unhedgeable component of option payoffs

### 3. Price Effects of Demand Pressure

- Own-contract and cross-contract demand transmission
- Covariance structure as the channel of surface propagation

### 4. Descriptive Statistics

- Dealer and end-user positions
- Demand patterns across option classes

### 5. Empirical Results

- Demand-based explanations for index-option expensiveness and skew/smirk
- Evidence of cross-contract pricing effects

### 6. Conclusion

- Demand pressure is a structural pricing input, not just noise

## Key Equations / Core Method

### Core Theoretical Result

The paper's essential result is:

- demand pressure raises the price of a contract in proportion to the variance of its unhedgeable component
- demand pressure in one contract raises the price of another in proportion to the covariance of their unhedgeable components

That is the theoretical backbone for thinking of the option book as a family rather than a list of disconnected symbols.

### Strategy-Relevant Translation

For `round_4`, this is one of the best framing papers for:

- `family pressure`
- `cross-strike contagion`
- `surface distortion from concentrated demand`

It strongly supports using a family-level state in the voucher book instead of relying purely on strike-local logic.

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - demand-pressure theory illustrations
  - descriptive tables for dealer / end-user positions
  - empirical evidence linking demand to skew and cross-contract pricing

## Current-Round-Relevant Hooks

- Excellent theoretical support for treating `VEV_*` as a linked family
- Helps justify `family imbalance` or `family pressure` features
- Reinforces the idea that `5200`, `5300`, and upper strikes may affect each other through demand, not only through underlying moves

## Conversion Caveats

- The paper is theory-heavy and not directly implementable as live bot logic
- Its main use should be as framing, candidate justification, and validation for family-level features rather than direct formula transport
