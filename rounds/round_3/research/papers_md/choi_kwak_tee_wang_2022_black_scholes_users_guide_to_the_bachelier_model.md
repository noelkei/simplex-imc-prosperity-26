# A Black-Scholes User's Guide to the Bachelier Model

## Source Metadata

- Input type: `latex_source`
- Paper ID: `choi_2022_bachelier_guide`
- Raw source folder: [choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model:1)
- Primary source file: [BachelierModel.tex](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model/BachelierModel.tex:1)
- Input assets preserved in raw source: figure PDFs under the same raw folder
- Conversion method: structure-first source extraction with equations and asset references preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, equations, and asset inventory; `medium` for prose because this file intentionally avoids full-text reproduction
- QA gate: `usable` (title/authors checked, core method captured, key equations preserved, asset inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `A Black-Scholes user's guide to the Bachelier model`
- Authors: `Jaehyuk Choi`, `Minsuk Kwak`, `Chyng Wen Tee`, `Yumeng Wang`
- Date in source: `14 January, 2022`
- Journal field in source: `Journal of Futures Markets`
- Keywords in source: `Bachelier model`, `Black-Scholes model`, `Displaced diffusion model`, `Normal model`

## Abstract

The paper reviews the Bachelier model as a practical alternative to
Black-Scholes, motivated in part by the temporary switch of commodity option
exchanges to normal-model pricing during the 2020 negative-oil episode. It
collects practical results on volatility conversion, hedging, stochastic
volatility, and barrier pricing, and presents the displaced Black-Scholes model
as a continuous bridge between the Bachelier and Black-Scholes limits.

## Section Outline

### 1. Introduction

- Historical context for Bachelier's arithmetic-Brownian-motion model
- Modern motivation from negative rates and negative commodity prices
- Practical goals: volatility conversion, hedging interpretation, DBS/SABR
  bridge, barrier pricing

### 2. Bachelier Model

- Bachelier and Black-Scholes model definitions
- Generalized normal-payoff pricing case
- Alternative specification discussion

### 3. Models Generalizing the Bachelier and BS Models

- Displaced Black-Scholes model
- SABR and CEV connections

### 4. Volatility

- Volatility inversion under the Bachelier model
- Conversion between BS, Bachelier, and displaced BS volatilities

### 5. Greeks, Hedging, and Exchange Margin

- Closed-form Greeks
- Volatility backbone interpretation
- Exchange margin comparison under Bachelier vs BS

### 6. Bachelier SV Model

- Review of stochastic-volatility extensions and smile generation

### 7. Pricing Other Derivatives

- Basket, spread, and Asian options
- Barrier options

### 8. Conclusion

### Appendix. Barrier Option Prices under the (Displaced) BS Model

## Key Equations / Core Method

### Core Bachelier Dynamics

The forward price follows arithmetic Brownian motion:

$$
dF_t = \sigma_N \, dW_t
$$

The undiscounted Bachelier call price in the source is:

$$
C_N(K) = (F_0 - K) N(d_N) + \sigma_N \sqrt{T}\, n(d_N),
\qquad
d_N = \frac{F_0 - K}{\sigma_N \sqrt{T}}.
$$

At-the-money, the source gives the simplified inversion:

$$
C_N(F_0) = \sigma_N \sqrt{\frac{T}{2\pi}},
\qquad
\sigma_N = C_N(F_0)\sqrt{\frac{2\pi}{T}}.
$$

### Generalized Normal-Payoff Form

When only the terminal mean and standard deviation matter, the source gives:

$$
C_N(K) = sd(F_T)\left(d_N N(d_N) + n(d_N)\right),
\qquad
d_N = \frac{\mu(F_T)-K}{sd(F_T)}.
$$

### Black-Scholes Benchmark

The source contrasts Bachelier with geometric Brownian motion:

$$
\frac{dF_t}{F_t} = \sigma_{BS} \, dW_t
$$

and the standard Black call formula:

$$
C_{BS}(K) = F_0 N(d_1) - K N(d_2),
\qquad
d_{1,2} = \frac{\log(F_0/K)}{\sigma_{BS}\sqrt{T}} \pm \frac{\sigma_{BS}\sqrt{T}}{2}.
$$

### Displaced Black-Scholes Bridge

The displaced dynamics in the source are:

$$
\frac{dF_t}{D(F_t)} = \sigma_D \, dW_t,
\qquad
D(F_t) = \beta F_t + (1-\beta)A.
$$

The corresponding call price is:

$$
C_D(K) = \frac{D(F_0)N(d_{1D}) - D(K)N(d_{2D})}{\beta},
$$

with

$$
d_{1D,2D} =
\frac{\log(D(F_0)/D(K))}{\beta \sigma_D \sqrt{T}}
\pm \frac{\beta \sigma_D \sqrt{T}}{2}.
$$

The source explicitly shows that the Bachelier model appears in the
`beta -> 0` limit with `sigma_N = A sigma_D`.

### BS to Bachelier Volatility Conversion

The paper's improved BS-to-normal conversion formula is:

$$
\sigma_N(K) \approx
\sigma_{BS} F_0 \sqrt{k}\left(1+\frac{\log^2 k}{24}\right)
\Big/
\left(1+\frac{\sigma_{BS}^2 T}{24}\right),
\qquad
k = \frac{K}{F_0}.
$$

The inverse approximation included in the source is:

$$
\sigma_{BS}(K) \approx
\frac{\sigma_N}{F_0 \sqrt{k}}
\left(1+\frac{\sigma_N^2 T}{24 k F_0^2}\right)
\Big/
\left(1+\frac{\log^2 k}{24}\right).
$$

The source warns that the normal-to-BS conversion is unreliable for very small
strikes because the equivalent BS volatility may fail to exist.

### Bachelier Greeks

The source lists the main Greeks:

$$
\Delta_N = N(d_N),
\qquad
\Gamma_N = \frac{n(d_N)}{\sigma_N \sqrt{T}},
\qquad
Vega_N = \sqrt{T}\, n(d_N),
\qquad
\Theta_N = -\frac{\sigma_N n(d_N)}{2\sqrt{T}}.
$$

### Volatility Backbone Adjustment

The source explains the delta difference through vega-rotated delta:

$$
\frac{\partial C}{\partial F_0}
=
\Delta + \frac{\partial \sigma_{BS}}{\partial F_0} Vega.
$$

For the Bachelier-implied BS volatility backbone, the source derives the
approximation:

$$
\Delta_N
\approx
\Delta_{BS} - \frac{\sigma_{BS}}{2F_0} Vega_{BS}.
$$

## Figures And Tables Asset Index

### Figures

- `iv-bs-skew.pdf`
  Source caption: BS volatility skew implied by Bachelier, displaced BS, and BS
  models.
- `iv-bs2norm.pdf`
  Source caption: exact vs approximate BS-to-Bachelier volatility conversion.
- `delta.pdf`
  Source caption: delta comparison across Bachelier, DBS, and BS models.
- `backbone.pdf`
  Source caption: backbone-induced BS skew change under the Bachelier model.
- `spanrisk_long.pdf`
  Source caption: SPAN risk comparison for long option positions.
- `spanrisk_short.pdf`
  Source caption: SPAN risk comparison for short option positions.
- `nsvh-vov.pdf`
  Source caption: normal-SV smile response to vol-of-vol.
- `sabr0-vov.pdf`
  Source caption: SABR with `beta=0` smile response to vol-of-vol.
- `nsvh-rho.pdf`
  Source caption: normal-SV smile response to correlation.
- `sabr0-rho.pdf`
  Source caption: SABR with `beta=0` smile response to correlation.
- `barrier.pdf`
  Source caption: barrier option prices under Bachelier, DBS, and BS.

### Tables

- `tab:greeks`
  Source content: side-by-side Bachelier vs displaced-BS price and Greeks.
- `tab:span`
  Source content: SPAN risk-array comparison under Bachelier vs BS.

## Current-Round-Relevant Hooks

- The Bachelier formula is explicitly simple enough for online use with only
  `S`, `K`, `T`, and normal `pdf/cdf`.
- The displaced-BS bridge gives a way to reason continuously between normal and
  lognormal assumptions.
- The BS-to-normal conversion formula is directly useful when checking whether a
  normal-model anchor is distorting cross-strike comparisons.
- The volatility-backbone section provides a concrete explanation for why model
  choice changes hedge sensitivity even when vanilla prices match.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a
  full-text reproduction of the paper.
- The raw LaTeX source remains the canonical reference for any omitted proofs,
  derivations, or less relevant sections.
- Formulas above are copied from the source's central results, but if a later
  strategy/spec depends on a niche result outside this subset, verify it against
  the raw source.
- The paper covers more than short-dated vanilla pricing; barrier and
  stochastic-volatility sections are preserved only at the structural level here.
