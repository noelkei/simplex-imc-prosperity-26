# Arbitrage-Free Smoothing of the Implied Volatility Surface

## Source Metadata

- Input type: `pdf`
- Paper ID: `fengler_2005_surface_smoothing`
- Raw source file: [fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf)
- Primary source file: [fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with no-arbitrage constraints, spline program, and figure/table captions preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, and central equations; `medium` for some matrix-layout details because PDF extraction occasionally splits multi-line equations
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant equations verified or caveated, figure/table inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Arbitrage-free smoothing of the implied volatility surface`
- Author: `Matthias R. Fengler`
- Date on paper title page: `March 23, 2005`
- Working-paper label in raw PDF: `SFB 649 Discussion Paper 2005-019`

## Abstract

The paper proposes smoothing the implied volatility surface by moving from implied
volatility space into call-price space and fitting natural cubic splines under shape
constraints that enforce no arbitrage. The resulting procedure is computationally cheap,
works even when the input quotes are themselves contaminated by arbitrage, and is aimed
at producing stable inputs for local-volatility pricing engines.

## Section Outline

### 1. Introduction

- Why local-volatility pricing breaks when the input surface contains arbitrage
- Why common interpolation/smoothing procedures are not enough
- Motivation for moving from implied-vol space into option-price space

### 2. No-Arbitrage Constraints on the IVS

- Call-price monotonicity, convexity, and price bounds
- Translation from option-price space to implied-volatility and total-variance space
- Calendar-arbitrage condition via total variance

### 3. Spline Smoothing

#### 3.1 Generic Set-up

- Natural cubic spline representation
- Value-second-derivative representation
- Quadratic-program formulation

#### 3.2 Cubic Spline Smoothing Under No-Arbitrage Constraints

- Linear inequality constraints implementing monotonicity, convexity, and bounds

#### 3.3 Estimating an Arbitrage-Free IVS

- Backward maturity-by-maturity fitting procedure

#### 3.4 Choice of the Smoothing Parameter

- AIC-based proxy for smoothing-parameter choice

### 4. Applications

- DAX examples at short and longer maturities
- Entire surface reconstruction

### 5. Conclusion

## Key Equations / Core Method

### Penalized Smoothing Objective

The basic spline problem is:

$$
\sum_{i=1}^n \{y_i - g(u_i)\}^2 + \lambda \int_a^b \{g''(v)\}^2 dv,
$$

subject to no-arbitrage shape constraints.

This is the paper's core object: fit prices while penalizing roughness.

### Call-Price Representation

Under a risk-neutral transition density `phi`, the European call price is:

$$
C(S_t,t,K,T,r_{t,\tau},\delta_{t,\tau})
=
e^{-r_{t,\tau}\tau}
\int_0^\infty \max(S_T - K, 0)\,\phi(S_T,T \mid S_t,t,r_{t,\tau},\delta_{t,\tau})\, dS_T.
$$

From this representation the source derives the standard shape constraints.

### Strike Monotonicity and Convexity

The call-price function must satisfy:

$$
-e^{-r_{t,\tau}\tau}
\le
\frac{\partial C}{\partial K}
\le
0,
$$

and

$$
\frac{\partial^2 C}{\partial K^2}
=
e^{-r_{t,\tau}\tau}\phi(\cdot)
\ge 0.
$$

These are the two most strategy-relevant constraints for the Round 3 single-expiry
surface: decreasing in strike and convex in strike.

### Call-Price Bounds

The source also states:

$$
\max(e^{-\delta_{t,\tau}\tau}S_t - e^{-r_{t,\tau}\tau}K, 0)
\le
C
\le
e^{-\delta_{t,\tau}\tau}S_t.
$$

### Black-Scholes Surface and Risk-Neutral Density Relation

The Black-Scholes call price in the paper is:

$$
C_t^{BS}
=
e^{-\delta_{t,\tau}\tau}S_t \Phi(\bar d_1)
- e^{-r_{t,\tau}\tau}K \Phi(\bar d_2).
$$

Differentiating twice when implied volatility depends on strike yields the paper's density
expression in terms of the smile and its derivatives. The practical point preserved here is
that enforcing no arbitrage directly in IV space is highly nonlinear and inconvenient.

### Total Variance

The paper defines total variance as:

$$
\nu^2(\kappa,\tau) = \hat\sigma^2(\kappa,\tau)\tau,
$$

where `kappa = K / F_t^T` is forward moneyness.

### Calendar-Arbitrage Condition

Proposition 2.1 states that if total variance is strictly increasing in maturity for fixed
forward moneyness, then there is no calendar arbitrage. The proof builds around a
calendar spread and the monotonicity of a Black-Scholes-normalized pricing function in
total variance.

### Natural-Spline Constraint Representation

The source rewrites the natural cubic spline in value-second-derivative form and obtains:

$$
Q^\top g = R\gamma,
$$

with roughness penalty:

$$
\int_a^b g''(u)^2 du = \gamma^\top R \gamma.
$$

This turns the fit into a convex quadratic program.

### Quadratic Program

Using the paper's block-matrix notation, the smoothing task becomes:

$$
\min_x -y^\top x + \frac{1}{2}x^\top Bx
\quad \text{subject to} \quad A^\top x = 0.
$$

### No-Arbitrage Constraints for the Spline

The paper enforces convexity via:

$$
\gamma_i \ge 0.
$$

It then adds boundary monotonicity and price-bound constraints:

$$
\frac{g_2 - g_1}{u_2 - u_1} \ge -e^{-r_{t,\tau}\tau},
\qquad
g_{n-1} - g_n \ge 0,
$$

$$
e^{-\delta_{t,\tau}\tau}S_t - e^{-r_{t,\tau}\tau}u_1 \le g_1 \le e^{-\delta_{t,\tau}\tau}S_t,
\qquad
g_n \ge 0.
$$

These are the most implementation-relevant conditions in the paper for a small
cross-strike option family.

### Backward Surface-Fitting Procedure

For the full maturity surface, the paper proposes:

1. rough pre-smoothing in total-variance space on a forward-moneyness grid
2. then stepping backwards from the last maturity to the first
3. solving the constrained spline problem at each maturity
4. enforcing cross-maturity conditions to prevent calendar arbitrage

## Figures And Tables Asset Index

### Figures Embedded In The PDF

- `Figure 1`: DAX call-price data contaminated by strike arbitrage
- `Figure 2`: total variance plot showing calendar-arbitrage intersections
- `Figure 3`: AIC minimization for the smoothing parameter
- `Figure 4`: arbitrage-free spline fitted to short-dated DAX call prices
- `Figure 5`: implied-volatility curve implied by the short-dated spline
- `Figure 6`: residual plots for the short-dated fit
- `Figure 7`: arbitrage-free spline for the 28-day maturity example
- `Figure 8`: implied-volatility curve for the 28-day maturity example
- `Figure 9`: residual plots for the 28-day maturity example
- `Figure 10`: full arbitrage-free implied-volatility surface and total-variance surface

### Tables Embedded In The PDF

- `Table 1`: DAX sample maturities and interest-rate inputs used in the application section

## Current-Round-Relevant Hooks

- The paper is a strong primary source for the static-arbitrage constraints already surfaced
  by Round 3 EDA: call prices should be monotone decreasing and convex in strike.
- The single-expiry part is much more relevant than the full local-volatility machinery for
  our round. The high-ROI takeaway is the constraint set, not the whole surface-pricing
  engine.
- For Round 3, the paper supports using cross-strike sanity guards or residual clamps in
  voucher pricing and in any fitted fair-value curve across strikes.
- The total-variance calendar part is less directly actionable for the live round because
  Round 3 has one live TTE, but it remains useful for historical cross-day interpretation.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- The paper is broader than the Round 3 need: it targets an entire implied-volatility
  surface for local-volatility pricing engines, not a small single-expiry bot.
- If later strategy/spec work needs exact spline-program details, recheck the raw PDF for
  matrix dimensions and constraint indexing.
