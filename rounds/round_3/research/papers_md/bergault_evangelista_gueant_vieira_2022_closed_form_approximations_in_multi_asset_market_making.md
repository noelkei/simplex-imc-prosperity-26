# Closed-Form Approximations in Multi-Asset Market Making

## Source Metadata

- Input type: `latex_source`
- Paper ID: `bergault_2022_multi_asset_mm`
- Raw source folder: [bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making:1)
- Primary source file: [main.tex](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making/main.tex:1)
- Input assets preserved in raw source: figure PDFs under the raw `images/` directory
- Conversion method: structure-first source extraction with equations, quote formulas, and figure references preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, central equations, and asset inventory; `medium` for prose because this file intentionally avoids full-text reproduction
- QA gate: `usable` (title/authors checked, core method captured, key equations preserved, asset inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Closed-form approximations in multi-asset market making`
- Authors: `Philippe Bergault`, `David Evangelista`, `Olivier Gueant`, `Douglas Vieira`
- Source type: `preprint` in an `elsarticle` template
- Keywords in source: `Algorithmic trading`, `Market making`, `Stochastic optimal control`, `Closed-form approximations`, `Monte-Carlo methods`

## Abstract

The paper studies multi-asset extensions of Avellaneda-Stoikov-style market
making and proposes closed-form approximations of the value function and the
resulting quotes. The main goal is to replace high-dimensional numerical
schemes with analytical proxies that remain useful as direct heuristics,
reinforcement-learning value priors, or immediately usable quoting rules.

## Section Outline

### 1. Introduction

- Motivation: multi-asset quoting is hard when correlated inventories make
  numerical dynamic programming expensive
- Goal: derive interpretable closed-form proxies for value functions and greedy
  quotes

### 2. The Multi-Asset Market Making Model

- Model setup
- Two objective functions
- Hamilton-Jacobi-Bellman and Hamilton-Jacobi equations
- Existing theoretical results and quote characterization

### 3. A Quadratic Approximation of the Value Function and Its Applications

- Quadratic approximation of Hamiltonians
- Closed-form proxy of the value function
- Asymptotics and resulting quoting heuristics

### 4. Beyond the Quadratic Approximation: Towards a Correction Term

- Perturbative refinement around the closed-form proxy

### 5. A Multi-Asset Market Making Model with Additional Features

- Drift in prices
- Client tiering
- Multiple request sizes
- Fixed transaction costs

### 6. Numerical Results

- Two-asset illustration
- Quote comparisons and PnL distributions

### 7. On the Construction of the Processes `N^{i,b}` and `N^{i,a}`

- Technical appendix on admissible point-process construction

## Key Equations / Core Method

### Reference Price Dynamics

For each asset `i`, the source models the reference price as:

$$
dS_t^i = \sigma^i dW_t^i,
$$

with cross-asset covariance matrix

$$
\Sigma = (\rho^{i,j} \sigma^i \sigma^j)_{1 \le i,j \le d}.
$$

### Inventory Dynamics

With transaction size `z^i`, inventory evolves as:

$$
dq_t^i = z^i dN_t^{i,b} - z^i dN_t^{i,a}.
$$

### Quote Distances and Intensities

The source defines quote distances as:

$$
\delta_t^{i,b} = S_t^i - S_t^{i,b},
\qquad
\delta_t^{i,a} = S_t^{i,a} - S_t^i.
$$

The fill intensities are:

$$
\lambda_t^{i,b} = \Lambda^{i,b}(\delta_t^{i,b})
\mathbf{1}_{\{q_{t-}^i + z^i \le Q^i\}},
\qquad
\lambda_t^{i,a} = \Lambda^{i,a}(\delta_t^{i,a})
\mathbf{1}_{\{q_{t-}^i - z^i \ge -Q^i\}}.
$$

This is the key place where liquidity and position limits enter the quoting
problem.

### Objective Functions

The source treats two optimization problems:

- `Model A`: maximize expected CARA utility of terminal marked-to-market wealth
- `Model B`: maximize expected marked-to-market wealth penalized by running
  quadratic inventory risk

The quadratic inventory-risk term is driven by:

$$
\frac{1}{2}\gamma q^\intercal \Sigma q.
$$

### Hamiltonian Functions

For each asset and side, the source defines Hamiltonians:

$$
H_\xi^{i,b}(p)=
\begin{cases}
\sup_\delta \frac{\Lambda^{i,b}(\delta)}{\xi z^i}
\left(1-\exp(-\xi z^i(\delta-p))\right), & \xi > 0, \\
\sup_\delta \Lambda^{i,b}(\delta)(\delta-p), & \xi = 0,
\end{cases}
$$

and similarly for `H_\xi^{i,a}`.

These Hamiltonians summarize how quote aggressiveness maps into expected
execution benefit after inventory/risk adjustment.

### Reduced Hamilton-Jacobi Equation

Using the source's ansatz, both Model A and Model B reduce to solving for a
function `theta(t,q)`:

$$
0
=
\partial_t \theta(t,q)
- \frac{1}{2}\gamma q^\intercal \Sigma q
+ \sum_i z^i H_\xi^{i,b}\!\left(
\frac{\theta(t,q)-\theta(t,q+z^i e^i)}{z^i}
\right)
+ \sum_i z^i H_\xi^{i,a}\!\left(
\frac{\theta(t,q)-\theta(t,q-z^i e^i)}{z^i}
\right),
$$

with terminal condition

$$
\theta(T,q)=0.
$$

### Optimal Quotes as Functions of `theta`

The source states that optimal quotes are recovered through:

$$
\delta_t^{i,b*}
=
\tilde{\delta}^{i,b*}_\xi
\left(
\frac{\theta(t,q_{t-})-\theta(t,q_{t-}+z^i e^i)}{z^i}
\right),
$$

$$
\delta_t^{i,a*}
=
\tilde{\delta}^{i,a*}_\xi
\left(
\frac{\theta(t,q_{t-})-\theta(t,q_{t-}-z^i e^i)}{z^i}
\right).
$$

So the quoting problem is reduced to approximating inventory finite
differences of the value function.

## Closed-Form Approximation Machinery

### Quadratic Hamiltonian Approximation

The paper replaces the original Hamiltonians with quadratic surrogates:

$$
\check{H}^{i,b}(p)=\alpha_0^{i,b}+\alpha_1^{i,b}p+\frac{1}{2}\alpha_2^{i,b}p^2,
\qquad
\check{H}^{i,a}(p)=\alpha_0^{i,a}+\alpha_1^{i,a}p+\frac{1}{2}\alpha_2^{i,a}p^2.
$$

The source explicitly notes that a natural choice is Taylor expansion around
`p = 0`.

### Quadratic Value-Function Ansatz

The approximate value function is taken in the source as:

$$
\check{\theta}(t,q) = -q^\intercal A(t) q - q^\intercal B(t) - C(t).
$$

This converts the approximate Hamilton-Jacobi problem into matrix and vector
ODEs for `A`, `B`, and `C`.

### Closed-Form Solution Skeleton

The source derives a Riccati-style solution with:

$$
A(t)
=
\frac{1}{2} D_+^{-1/2}\widehat{A}
\left(e^{\widehat{A}(T-t)}-e^{-\widehat{A}(T-t)}\right)
\left(e^{\widehat{A}(T-t)}+e^{-\widehat{A}(T-t)}\right)^{-1}
D_+^{-1/2},
$$

where

$$
\widehat{A}
=
\sqrt{\gamma}\left(D_+^{1/2}\Sigma D_+^{1/2}\right)^{1/2}.
$$

This is the heart of the paper's multi-asset coupling: price covariance and
liquidity terms combine through the matrix square-root structure.

### Greedy Quotes from the Proxy

The closed-form proxy produces approximate quotes of the form:

$$
\check{\delta}_t^{i,b}
=
\tilde{\delta}_\xi^{i,b*}
\left(
2 q_{t-}^\intercal A(t)e^i
+ z^i {e^i}^\intercal A(t)e^i
+ {e^i}^\intercal B(t)
\right),
$$

$$
\check{\delta}_t^{i,a}
=
\tilde{\delta}_\xi^{i,a*}
\left(
-2 q_{t-}^\intercal A(t)e^i
+ z^i {e^i}^\intercal A(t)e^i
- {e^i}^\intercal B(t)
\right).
$$

### Asymptotic Quote Form

For large-horizon asymptotics, the source obtains simplified quotes:

$$
\breve{\delta}_t^{i,b}
=
\tilde{\delta}^{i,b*}_\xi
\left(
\sqrt{\gamma} q_{t-}^\intercal \Gamma e^i
+ \frac{1}{2}\sqrt{\gamma} z^i {e^i}^\intercal \Gamma e^i
- {e^i}^\intercal D_+^{-1/2}\widehat{A}\widehat{A}^+ D_+^{-1/2}
\left(
V_- + \frac{1}{2}\sqrt{\gamma} D_- \mathcal{D}(\Gamma)
\right)
\right),
$$

with the analogous ask quote having the inventory term negated.

The source interprets the dependence on

$$
q^\intercal \Gamma e^i
$$

as the multi-asset coupling between inventory, covariance, and liquidity.

### Symmetric Exponential-Intensity Special Case

Under symmetric exponential intensities

$$
\Lambda^{i,b}(\delta)=\Lambda^{i,a}(\delta)=A^i e^{-k^i \delta},
$$

the source derives especially simple asymptotic quotes:

$$
\breve{\delta}_t^{i,b}
=
\sqrt{\gamma}
\left(
q_{t-}^\intercal \Gamma e^i
+ \frac{1}{2} z^i {e^i}^\intercal \Gamma e^i
\right)
+ \frac{1}{\gamma z^i}\log\left(1+\frac{\gamma z^i}{k^i}\right)
$$

for Model A, and

$$
\breve{\delta}_t^{i,b}
=
\sqrt{\gamma}
\left(
q_{t-}^\intercal \Gamma e^i
+ \frac{1}{2} z^i {e^i}^\intercal \Gamma e^i
\right)
+ \frac{1}{k^i}
$$

for Model B, with matching ask-side expressions.

This is one of the most implementation-relevant parts of the paper.

## Figures And Tables Asset Index

### Figure Assets

- `conv_deltas_BEGV.pdf`
- `theta_3d_BEGV.pdf`
- `delta_b_3d_asset_1_size_0_BEGV.pdf`
- `delta_b_3d_asset_2_size_0_BEGV.pdf`
- `theta_hat_3d_BEGV.pdf`
- `delta_hat_b_3d_asset_1_size_0_BEGV.pdf`
- `delta_hat_b_3d_asset_2_size_0_BEGV.pdf`
- `deltas_comp_asset_1_q_1_different_sizes_BEGV.pdf`
- `deltas_comp_asset_1_q_2_different_sizes_BEGV.pdf`
- `deltas_comp_asset_2_q_1_different_sizes_BEGV.pdf`
- `deltas_comp_asset_2_q_2_different_sizes_BEGV.pdf`
- `pnl_distrib_optimal_BEGV.pdf`
- `pnl_distrib_approx_BEGV.pdf`

### Figure Captions Preserved at the Structural Level

- inventory-to-quote convergence over time
- true value function `theta`
- optimal bid-quote surfaces by asset
- proxy value function `check(theta)`
- proxy bid-quote surfaces by asset
- quote-vs-approximation comparisons by trade size and inventory slice
- PnL distributions under optimal quotes vs approximations

## Current-Round-Relevant Hooks

- The paper gives a direct template for translating correlated multi-product
  inventory into quote shifts without solving the full dynamic program online.
- The `q^\intercal \Gamma e^i` structure is especially relevant when several
  vouchers share the same underlying and have correlated risk even with
  independent position limits.
- The symmetric exponential-intensity special case yields formulas close enough
  to a simple Trader implementation to inspire inventory penalties and quote
  skewing rules.
- The source is not option-specific by default, but it is explicitly aware of
  options-market market making in the literature context.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a
  full-text reproduction of the paper.
- The raw LaTeX source remains the canonical reference for omitted proofs,
  extensions, and appendix details.
- The paper is more general than the Round 3 use case; it includes drift,
  client tiering, trade-size discretization, and fixed costs that are not all
  directly relevant to Prosperity Round 3.
- If later strategy/spec work needs a specific theorem statement or derivation,
  verify it against the raw source before implementation.
