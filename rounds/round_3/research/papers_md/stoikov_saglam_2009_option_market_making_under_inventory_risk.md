# Option Market Making under Inventory Risk

## Source Metadata

- Input type: `pdf`
- Paper ID: `stoikov_saglam_2009_option_mm_inventory`
- Raw source file: [stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf)
- Primary source file: [stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf)
- Input assets preserved in raw source: figures and theorem/proof layout are embedded in the PDF only; there are no separate raw figure files
- Conversion method: PDF-first structural extraction with theorem-level formulas, section outline, and figure captions preserved; prose is compressed into a source-faithful research outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, and central quoting formulas; `medium` for notation details because several PDF equations use OCR-hostile Greek symbols and some extracted glyphs are imperfect
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant formulas verified or caveated, figure/table inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Option market making under inventory risk`
- Authors: `Sasha Stoikov`, `Mehmet Saglam`
- Date on title page: `December 29, 2008`
- Source note on title page: `Electronic copy available at SSRN abstract 1393818`
- Keywords on title page: `Delta`, `European options`, `Gamma`, `Inventory management`, `Liquidity`, `Market microstructure`, `Vega`

## Abstract

The paper studies how an option market maker should set bid and ask quotes when profits
come from spread capture but risk comes from carrying option inventory. It works through
three nested settings: a complete market with continuous delta hedging, a setting where
the underlying itself is illiquid and must also be quoted, and an incomplete-market
setting where residual gamma and vega risks remain even after delta hedging.

## Section Outline

### I. Introduction

- Motivation from option dealer inventory management
- Mean-variance framing instead of full expected-utility control
- Separation between intraday trading and overnight inventory risk

### II. The Complete Market Model

- Option market making with continuous delta hedging in a perfectly liquid underlying
- Inventory-neutral result for option quotes in the fully hedgeable case

### III. Illiquidity in the Underlying

- Joint quoting of the stock and the option
- One-period solution
- Multi-period recursion and quote tilting by net delta
- Efficient-frontier interpretation

### IV. Stochastic Volatility and Discrete Hedging

- Residual gamma risk from discrete hedging
- Residual vega risk from stochastic implied volatility
- One-period option-only quoting result
- Multi-period recursion for inventory-sensitive option quotes

### V. Conclusion

### Appendix

- Proofs of Theorems 1 to 5
- Auxiliary recursion lemmas for the multi-period setting

## Key Equations / Core Method

### Underlying and Option Dynamics

The stock follows geometric Brownian motion:

$$
dS_t = \sigma S_t \, dW_t.
$$

The option mid price is modeled through Black-Scholes Greeks:

$$
dC(S,t) = \Theta_t dt + \Delta_t dS_t + \frac{1}{2}\Gamma_t (dS_t)^2
= \Delta_t \sigma S_t dW_t.
$$

### Quote Parameterization

The dealer quotes around the option mid:

$$
p_t^{b,o} = C_t - \epsilon_t^{b,o},
\qquad
p_t^{a,o} = C_t + \epsilon_t^{a,o},
$$

where the premiums `epsilon` are the controlled spread captures.

### Arrival Intensities

For options, the paper uses a linear arrival-intensity form:

$$
\lambda^o(\epsilon) =
\begin{cases}
C - D \epsilon, & 0 \le \epsilon < C/D, \\
0, & \text{otherwise.}
\end{cases}
$$

When the stock is also quoted, an analogous linear form is used:

$$
\lambda^s(\epsilon) =
\begin{cases}
A - B \epsilon, & 0 \le \epsilon < A/B, \\
0, & \text{otherwise.}
\end{cases}
$$

### Objective

Across the main variants, the dealer maximizes expected marked-to-market profit penalized
by inventory-risk variance:

$$
v = \max E[Z_T] - \gamma \operatorname{Var}[I_T].
$$

This is the main bridge from spread capture to inventory-aware quote skewing.

## Key Results And Formulas

### Complete-Market Result: Hedge Delta, Then Quote the Revenue Maximizer

In the complete-market case, Theorem 1 gives the optimal stock hedge:

$$
\pi_t = - S_t \Delta_t q_t^o.
$$

Option premiums then solve

$$
\epsilon_t^{a,o} = -\frac{\lambda(\epsilon_t^{a,o})}{\lambda'(\epsilon_t^{a,o})},
\qquad
\epsilon_t^{b,o} = -\frac{\lambda(\epsilon_t^{b,o})}{\lambda'(\epsilon_t^{b,o})}.
$$

So in the fully hedgeable case, inventory disappears from the option quote itself; the
market maker handles risk by delta hedging rather than by quote skew.

### Illiquid-Underlying One-Period Result: Quote Tilt by Net Delta

When both the stock and the option are quoted and the underlying is illiquid, Theorem 2
shows that the optimal quotes are tilted by the net delta exposure:

$$
q_{n-1}^s + q_{n-1}^o \Delta_n.
$$

The option ask and bid premiums take the clipped linear form:

$$
\epsilon_{n-1}^{a,o}
=
\max\left(
0,
\min\left(
\frac{C}{D},
\frac{C}{2D}
- \gamma \sigma^2 (T-t_n) S_n^2 \Delta_n
\left(q_{n-1}^s + q_{n-1}^o \Delta_n - \frac{1}{2}\Delta_n\right)
\right)\right),
$$

$$
\epsilon_{n-1}^{b,o}
=
\max\left(
0,
\min\left(
\frac{C}{D},
\frac{C}{2D}
+ \gamma \sigma^2 (T-t_n) S_n^2 \Delta_n
\left(q_{n-1}^s + q_{n-1}^o \Delta_n + \frac{1}{2}\Delta_n\right)
\right)\right).
$$

The source highlights the interpretation directly: if the dealer is risk-averse, all quotes
are tilted away from the pure spread-maximizing solution in proportion to net delta.

### Illiquid-Underlying Multi-Period Result: Quote Tilt Slope Recursion

Theorem 3 keeps the same net-delta structure but replaces the one-step coefficient by a
time-dependent slope `m_i`:

$$
m_i = m_{i+1} + \Delta t \left(B I_i + D \Delta_n^2 J_i\right) m_{i+1}^2,
$$

with terminal condition

$$
m_n = -\gamma \sigma^2 S^2 (T - t_n).
$$

The implementation-level insight is that quote tilt steepens as the end of the day
approaches, making inventory flattening more aggressive near horizon end.

### Residual Gamma and Vega Risk Under Discrete Hedging

Section IV introduces residual option risk even after delta hedging. The source states the
vega-gamma relation:

$$
C_\sigma = \Gamma S^2 \sigma (T_{\text{mat}} - t).
$$

After delta hedging at each step, residual inventory PnL increments depend on gamma and
stochastic-volatility shocks:

$$
\Delta I_i
=
q_{i+1}^o
\left(
\frac{1}{2}\Gamma_i \sigma_i^2 S_i^2 (u^2 - 1)\Delta t
+
\Gamma_i \sigma_i \alpha S_i^2 (T_{\text{mat}} - t_i)\eta \sqrt{\Delta t}
\right).
$$

The source's interpretation is especially useful: for long-maturity options, the stochastic
volatility term can dominate, while for short-maturity options the discrete-hedging gamma
term becomes more important.

### Incomplete-Market One-Period Result: Quote Tilt by Net Option Inventory

Theorem 4 gives the option-only one-period premiums:

$$
\epsilon_{n-1}^{a,o}
=
\max\left(
0,
\min\left(
\frac{C}{D},
\frac{C}{2D} - \gamma k \left(q_{n-1}^o - \frac{1}{2}\right)
\right)\right),
$$

$$
\epsilon_{n-1}^{b,o}
=
\max\left(
0,
\min\left(
\frac{C}{D},
\frac{C}{2D} + \gamma k \left(q_{n-1}^o + \frac{1}{2}\right)
\right)\right),
$$

with

$$
k =
\left(
\frac{1}{2}\sigma_n^2 (T-t_n) + \alpha^2 (T_{\text{mat}} - t_n)^2
\right)
\cdot
\Gamma_n^2 S_n^4 \sigma_n^2 (T-t_n).
$$

This is the main option-specific inventory result: once delta is neutralized externally,
quote skew depends on pure option inventory and on residual gamma/vega risk.

### Incomplete-Market Multi-Period Result

Theorem 5 again yields clipped linear quotes with a recursively updated slope:

$$
\epsilon_i^{a,o}
=
\max\left(0,\min\left(\frac{C}{D}, \frac{C}{2D} + m_{i+1} q_i^o - \frac{1}{2}m_{i+1}\right)\right),
$$

$$
\epsilon_i^{b,o}
=
\max\left(0,\min\left(\frac{C}{D}, \frac{C}{2D} - m_{i+1} q_i^o - \frac{1}{2}m_{i+1}\right)\right),
$$

where

$$
m_i = m_{i+1} + \Delta t \left(D m_{i+1}^2 J_i\right),
$$

and the terminal slope depends on residual gamma and vega exposure:

$$
m_n =
-\gamma \sigma_n^2 S_n^2 \Gamma_n^2 (T-t_n)
\left(
\frac{1}{2}\sigma_n^2 S_n^2 (T-t_n)
+ \alpha^2 S^2 (T_{\text{mat}} - t_n)^2
\right).
$$

## Figures And Tables Asset Index

### Figures Embedded In The PDF

- `Figure 1`: optimal quoting policy with low risk aversion when there is no intraday stock movement
- `Figure 2`: optimal quoting policy with high risk aversion in the same no-intraday-movement setting
- `Figure 3`: efficient frontier of the dealer under joint stock/option quoting
- `Figure 4`: long-maturity option quoting policy under different stochastic-volatility levels `alpha`
- `Figure 5`: very short-maturity option quoting policy showing gamma-dominated behavior

### Tables

- No standalone numbered tables are central to the paper's main contribution; the source is theorem-driven and figure-driven

## Current-Round-Relevant Hooks

- The paper gives a direct path from correlated option inventory to quote skew without
  requiring a full online Greeks stack in the final bot.
- The net-delta and net-option-inventory decompositions are especially relevant for Round 3
  because we can approximate family-level exposure using `VELVETFRUIT_EXTRACT`,
  strike, and simple moneyness weights.
- The maturity split between gamma-dominated short maturities and vega-dominated long
  maturities is directly useful as a conceptual warning for TTE `5d`: near-expiry behavior
  should be treated as a different regime from longer-dated option datasets.
- The clipped linear premium formulas are simple enough to inspire implementation-level
  inventory penalties and quote-shift heuristics even if the full paper model is not used.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- Several Greek symbols and OCR-sensitive formulas are slightly noisy in the raw PDF
  extraction; any implementation-critical constant or theorem should be rechecked against
  the PDF.
- The paper assumes a dealer model with explicit stock and option quoting, continuous-time
  notation, and linear arrival intensities. Those are useful inspirations, not Round 3 facts.
