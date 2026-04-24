# Option Pricing: A Simplified Approach

## Source Metadata

- Input type: `pdf`
- Paper ID: `crr_1979_simplified_approach`
- Raw source file: [cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf)
- Primary source file: [cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf)
- Input assets preserved in raw source: tables and tree diagrams are embedded in the PDF only
- Conversion method: PDF-first structural extraction with section hierarchy, central equations, and embedded tables/trees preserved at the structural level; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, and core binomial formulas; `medium` for some continuous-limit derivations because the PDF extraction is noisy around hats, Greek letters, and subscripts
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant formulas verified or caveated, table/tree inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Option Pricing: A Simplified Approach`
- Authors: `John C. Cox`, `Stephen A. Ross`, `Mark Rubinstein`
- Date on title page: `March 1979 (revised July 1979)`
- Publication note on title page: `published under the same title in Journal of Financial Economics (September 1979)`

## Abstract

The paper introduces a discrete-time binomial framework for valuing options by
no-arbitrage replication. The model is intentionally elementary, but it already contains
the main economics of option pricing, extends naturally to backward-induction valuation
of early-exercise products, and converges to the Black-Scholes model in an appropriate
limit.

## Section Outline

### 1. Introduction

- Motivation for a discrete-time arbitrage-based option model
- Positioning relative to Black-Scholes and Merton
- Preview of limiting cases and numerical methods

### 2. The Basic Idea

- One-period example
- Levered hedge that replicates the call payoff
- Option value from no-arbitrage

### 3. The Binomial Option Pricing Formula

- Multiplicative stock tree with up/down states
- One-period call valuation
- Recursive multi-period valuation
- Closed-form complementary-binomial expression

### 4. Riskless Trading Strategies

- How to exploit market mispricing with hedge adjustments
- Why hedge rebalancing should be done through the underlying, not by buying back mispriced options

### 5. Limiting Cases

- Continuous-trading / lognormal limit leading to Black-Scholes
- Alternative jump-process limit

### 6. Dividends and Put Pricing

- Dividend-adjusted stock tree
- Early exercise for dividend-paying calls
- Backward induction for puts and American exercise

### 7. Conclusion

- Generality of the binomial framework
- Necessary and sufficient condition for stock-and-bond replication

## Key Equations / Core Method

### One-Period Replicating Portfolio

The source equates the end-of-period values of a stock-bond portfolio and the call:

$$
\Delta u S + rB = C_u,
\qquad
\Delta d S + rB = C_d.
$$

Solving gives the hedge ratio and bond position:

$$
\Delta = \frac{C_u - C_d}{(u-d)S},
\qquad
B = \frac{uC_d - dC_u}{r(u-d)}.
$$

This is the most implementation-relevant idea in the paper: replication sets option value
without needing the physical probability of an up move.

### Risk-Neutral Weight

The paper defines

$$
p = \frac{r-d}{u-d},
\qquad
1-p = \frac{u-r}{u-d}.
$$

Although derived from replication, `p` behaves like a risk-neutral probability weight.

### One-Period Call Value

The one-period no-arbitrage call value is:

$$
C = \frac{p C_u + (1-p) C_d}{r},
$$

provided this exceeds immediate exercise value; otherwise use `S-K` for an American call.

### Multi-Period Recursive Call Value

Working backward through the tree, the paper arrives at the `n`-period expression:

$$
C = \frac{1}{r^n}
\sum_{j=0}^{n}
\binom{n}{j}
p^j (1-p)^{n-j}
\max(0, u^j d^{n-j}S - K).
$$

This is the direct discrete-time pricing formula before simplifying it into the
complementary-binomial form.

### Closed-Form Binomial Expression

Let `a` be the smallest non-negative integer such that `u^a d^{n-a} S > K`. Then the paper
states the compact formula:

$$
C = S \, \phi[a;n,p'] - K r^{-n}\phi[a;n,p],
$$

where

$$
p' = \frac{u}{r}p
$$

and `phi[a;n,p]` is the complementary binomial distribution function.

This is the part most directly useful for a compact online tree pricer or for reasoning
about strike-by-strike sensitivity with a finite number of steps.

### Continuous-Time / Black-Scholes Limit

To obtain the Black-Scholes limit, the paper lets the time step shrink while choosing

$$
\hat r = r^{t/n},
\qquad
u = e^{\sigma \sqrt{t/n}},
\qquad
d = e^{-\sigma \sqrt{t/n}}.
$$

With the appropriate limit argument, the binomial price converges to the Black-Scholes
formula. The source presents the resulting Black-Scholes expression as:

$$
C = S N(x) - K r^{-t} N(x - \sigma \sqrt{t}),
$$

with

$$
x = \frac{\log(S/K) + \frac{1}{2}\sigma^2 t + \log r^t}{\sigma \sqrt{t}}.
$$

The notation is old-style, but the practical message is the same: the CRR tree is not an
alternative philosophy to Black-Scholes; it is a discrete-time route into it.

### Jump-Process Limit

The paper also states that a different scaling of `u`, `d`, and `q` leads to a jump-process
limit and gives a complementary-Poisson valuation formula. This is conceptually useful but
not central to Round 3.

### Dividends And Early Exercise

For a dividend-paying stock with dividend yield `delta` on known ex-dividend dates, the
paper replaces the next-period stock values by:

$$
u (1-\delta)^v S,
\qquad
d (1-\delta)^v S,
$$

where `v` indicates whether the next step ends on an ex-dividend date.

This turns call pricing into:

$$
C = \max\left(S-K, \frac{pC_u + (1-p)C_d}{\hat r}\right),
$$

and similarly for puts:

$$
P = \max\left(K-S, \frac{pP_u + (1-p)P_d}{\hat r}\right).
$$

The practical point preserved here is that once early exercise is possible, backward
induction is the natural object, not the closed-form complementary-binomial expression.

## Figures And Tables Asset Index

### Tables Embedded In The PDF

- `Table 1`: one-period arbitrage table illustrating the formation of a riskless hedge
- `Table 2`: binomial approximation of continuous-time call values for different volatilities, strikes, and maturities
- `Table 3`: three-period binomial tree for an American put with dividends and optimal early exercise marked

### Embedded Tree / Diagram Content

- One-period up/down stock tree
- One-period call tree
- Multi-period stock and call trees
- Hedge-ratio trees used in the mispricing examples

## Current-Round-Relevant Hooks

- The paper is the canonical lightweight reference for using a finite-step tree instead of a
  full continuous-time formula. That is highly relevant for Round 3 because a small-step
  tree is implementable in a simple `Trader` with no external libraries.
- For the current round, the highest-ROI use is not American exercise, but simple fair-value
  benchmarking across strikes and as a sanity check against Bachelier-style pricing.
- The source also reinforces a key implementation discipline: if we use a finite-step option
  model, it should be compact and online-usable, not a heavy offline-only calibration
  apparatus.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- The continuous-limit derivation uses notation that extracts noisily from the PDF; if we
  later implement a specific formula from the limit section, we should verify against the raw
  PDF.
- The paper is broader than the Round 3 need: its dividend and American-option machinery
  is historically important, but likely secondary to the finite-step European-style pricing
  intuition for this round.
