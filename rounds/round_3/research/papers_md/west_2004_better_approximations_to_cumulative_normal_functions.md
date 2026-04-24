# Better Approximations to Cumulative Normal Functions

## Source Metadata

- Input type: `pdf`
- Paper ID: `west_2004_cumulative_normal`
- Raw source file: [west_2004_better_approximations_to_cumulative_normal_functions.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf)
- Primary source file: [west_2004_better_approximations_to_cumulative_normal_functions.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf)
- Input assets preserved in raw source: figures and VBA code listings are embedded in the PDF only
- Conversion method: PDF-first structural extraction with integral definitions, limiting identities, and implementation-focused caveats preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for the univariate-normal material and key cautionary examples; `medium` for embedded code listings because the raw PDF is typeset as article text rather than as a standalone code source
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant formulas preserved, embedded-asset limits caveated, no obvious truncation)

## Paper Metadata

- Title: `Better Approximations to Cumulative Normal Functions`
- Author: `Graeme West`
- Date in footer: `December 8, 2004`
- Source style: `practitioner note / technical article with embedded VBA snippets`

## Abstract

The note argues that numerical quality of normal CDF approximations matters much more
than many finance implementations assume, especially once a univariate approximation is
used as a building block inside bivariate and trivariate cumulative-normal routines.
West recommends using a higher-precision Hart-style rational approximation for the
univariate normal and documents several option-pricing failures that arise when lower-
precision cumulative-normal functions are reused inside exotic-option formulas.

## Section Outline

### 1. The Need for High Precision Cumulative Normal Functions

- Why low-precision univariate approximations contaminate higher-dimensional routines

### 2. Univariate Cumulative Normal

- Standard normal CDF definition
- Abramowitz-Stegun vs Hart-style rational approximations
- Why near-double-precision univariate code is useful

### 3. Bivariate Cumulative Normal

- Review of common approximations
- Drezner and Drezner-Wesolowsky style methods

### 4. Option Pricing Disasters

#### 4.1 Problems with the Univariate

- Negative exotic option values caused by low-precision normal approximation

#### 4.2 Problems with the Bivariate: `rho = ±1`

- Necessary limiting-case guards

#### 4.3 Problems with the Bivariate: Negative Option Values

#### 4.4 Problems with the Bivariate: Underflow

- Practical coding safeguard for DW2-style algorithms

### 5. The Trivariate Cumulative Normal Function

- Brief note on trivariate probability routines and numerical availability

## Key Equations / Core Method

### Univariate Standard Normal CDF

The source defines the cumulative standard normal as:

$$
N(x) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{x} e^{-X^2/2}\, dX.
$$

The paper's main practical point is that there is no closed form, so the chosen numerical
approximation becomes part of the pricing model.

### Hart-Style High-Precision Approximation

The note contrasts the common Abramowitz-Stegun polynomial approximation with a
Hart-style rational-function approach that is described as accurate to double precision
across the real line.

The embedded VBA code in `Figure 2` provides a reference implementation of the
high-precision univariate routine:

- piecewise treatment for moderate vs large `|x|`
- exponential factor `exp(-x^2/2)`
- rational-function numerator/denominator in the central region
- continued-fraction-style tail handling in the far tails

The exact code is in the PDF; for our Round 3 purposes the key idea is that a robust
hand-coded `norm_cdf` is feasible without external libraries.

### Bivariate Standard Normal CDF

The note defines the bivariate cumulative normal as:

$$
N_2(x,y,\rho)
=
\frac{1}{2\pi\sqrt{1-\rho^2}}
\int_{-\infty}^{x}\int_{-\infty}^{y}
\exp\left(
\frac{-(X^2 - 2\rho XY + Y^2)}{2(1-\rho^2)}
\right)
dY\, dX.
$$

This is mostly secondary for Round 3, but the paper's warnings about edge cases are
still broadly useful.

### Limiting Cases at `rho = ±1`

The note explicitly states the required limiting identities:

$$
N_2(x,y,1) = N(\min(x,y)),
$$

$$
N_2(x,y,-1) =
\begin{cases}
0, & y \le -x, \\
N(x) + N(y) - 1, & y > -x.
\end{cases}
$$

These are implementation safeguards: any bivariate routine should trap them directly
instead of allowing divide-by-zero style failures.

### Trivariate Standard Normal

The note also writes the trivariate cumulative-normal integral:

$$
N_3(x_1,x_2,x_3,\Sigma)
=
\frac{1}{(2\pi)^{3/2}\sqrt{|\Sigma|}}
\int_{-\infty}^{x_1}
\int_{-\infty}^{x_2}
\int_{-\infty}^{x_3}
\exp\left(\frac{1}{2}X' \Sigma^{-1} X\right)
dX_3\, dX_2\, dX_1.
$$

This is not directly actionable for the Round 3 bot, but it explains why low-quality
lower-dimensional building blocks can become expensive errors higher up the stack.

## Main Implementation Findings Preserved From Source

### Use a Double-Precision Univariate CDF

- The Hart approximation is presented as effectively double-precision across the real line.
- The note argues that the common Abramowitz-Stegun implementation is usually fine in the
  central region but can create serious downstream issues when reused in exotic formulas.
- The practical recommendation is simple: if the pricing stack needs a hand-coded normal
  CDF, use a higher-quality implementation once rather than patching problems later.

### Low-Precision CDFs Can Produce Nonsensical Option Prices

Section 4.1 documents exotic-option examples where approximation error in the univariate
normal propagates into negative prices through large multiplicative factors. The immediate
lesson for us is not about barrier options specifically, but about treating numerical
stability as part of model correctness.

### Bivariate Routines Need Explicit Edge-Case Guards

The note shows that Drezner-style bivariate implementations can fail when correlations
hit limiting values or when floating-point noise effectively pushes them there.

### Underflow And `0/0`-Type Failures Need Manual Protection

Section 4.4 gives a concrete example where an intermediate exponential underflows inside a
DW2 bivariate routine, creating a `0/0` style failure. The practical carryover is that
small custom math routines should include explicit safe guards, not just rely on nominal
formula algebra.

## Figures And Tables Asset Index

### Figures Embedded In The PDF

- `Figure 1`: relative values of several univariate normal approximations
- `Figure 2`: VBA implementation of a high-precision univariate normal function
- `Figure 3`: the bivariate cumulative normal function for a sample correlation
- `Figure 4`: option-pricing error example using a lower-quality bivariate routine
- `Figure 5`: deeper negative-value pathology as correlation approaches `-1`
- `Figure 6`: VBA version of a DW2-style bivariate routine
- `Figure 7`: modified DW2-style VBA routine with underflow safeguard

### Tables

- No separate tables; the source is example-driven and figure/code-driven

## Current-Round-Relevant Hooks

- This paper is not a strategy paper; it is an implementation-quality paper. Its highest-ROI
  use for Round 3 is justifying a robust hand-coded `norm_cdf` if we use Bachelier or any
  normal-model approximation inside the bot.
- The direct actionable takeaway is "do the math utility once and do it carefully." That is
  especially relevant because Round 3 bots cannot rely on `scipy.stats`.
- Everything beyond the univariate routine is mostly secondary for the current round, but
  the note is still a useful warning against quietly accepting unstable numerical helpers.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- The embedded VBA code is referenced structurally, not reproduced line-for-line as a code
  source artifact.
- The bivariate and trivariate sections are broader than the current Round 3 need; the main
  direct value here is the univariate-CDF quality discussion.
