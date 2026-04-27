# Does Net Buying Pressure Affect the Shape of Implied Volatility Functions?

## Source Metadata

- Input type: `pdf`
- Paper ID: `bollen_whaley_2004_net_buying_pressure`
- Raw source file: [bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf)
- Primary source file: [bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first extraction with title-page abstract recovery, section hierarchy reconstruction, and emphasis on the empirical link between demand pressure and implied-volatility shape
- Fidelity status: `medium` for clean prose because the older PDF has more extraction noise; `high` for title, abstract meaning, major sections, and core empirical claim
- QA gate: `usable`

## Paper Metadata

- Title: `Does Net Buying Pressure Affect the Shape of Implied Volatility Functions?`
- Authors: `Nicolas P. B. Bollen`, `Robert E. Whaley`
- Year: `2004`
- Source note: title-page manuscript format with embedded abstract and empirical tables
- Topic frame: option demand pressure, implied-volatility distortions, cross-strike surface effects

## Abstract

The paper studies whether net buying pressure from public order flow changes the shape of the implied-volatility function. Using index and single-stock options, it finds that movements in implied volatility are directly related to net buying pressure, with especially strong effects in index options and in index puts. The paper also shows that simple apparent mispricing in the implied-volatility function does not survive a more complete hedging treatment once vega risk is accounted for. The practical message is that demand can bend the surface without implying easy arbitrage.

## Section Outline

### I. Sample Description

#### A. Data

- CBOE trade and quote data

#### B. Implied Volatility Computation

- Construction of implied volatilities and comparison across contracts

#### C. Implied Volatility Functions

- Building the strike-by-strike surface representation

#### D. Empirical Properties of IVFs

- Stylized facts for index vs stock-option surfaces

### II. Net Buying Pressure and Movements in Implied Volatility

#### A. Empirical Methodology

- Regressions of implied-vol changes on demand pressure

#### B. Main Results

- Demand pressure matters for the shape of the surface

### III. Trading Strategy Interpretation

- Delta-neutral option-selling tests
- Vega-hedged interpretation of apparent abnormal returns

### IV. Conclusion

- Demand pressure distorts the surface, but not every distortion is exploitable

## Key Equations / Core Method

### Core Regressor: Net Buying Pressure

The paper defines a demand-pressure variable based on contracts bought minus contracts sold, with later regressions scaling the pressure by the absolute value of option delta so that demand is expressed in stock/index-equivalent terms.

### Dependent Variable: Change in Implied Volatility

The empirical tests relate changes in implied volatility to:

- current net buying pressure
- lagged changes in implied volatility
- controls that help distinguish demand effects from information or learning effects

### Strategy-Relevant Result

The paper's most important implication for `round_4` is not "trade the residual". It is:

- residuals or skew changes can be demand distortions
- strong flow plus unusual surface shape is often `state`, not `arbitrage`
- naive delta-neutral monetization can look better than it really is unless vega exposure is treated properly

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - implied-volatility function examples
  - regression tables linking net buying pressure to implied-vol movements
  - trading-strategy tables comparing delta-neutral and vega-aware interpretations

## Current-Round-Relevant Hooks

- Strong guardrail against over-reading `VEV_*` residuals as clean alpha
- Supports `flow-distorted surface` logic for `5200+` and potentially `5300`
- Helps justify using flow and surface jointly as a veto or caution layer
- Useful for understanding why upper-strike selling may be a volatility-demand signal rather than simple cheap/rich mispricing

## Conversion Caveats

- The PDF extraction is noisier than for the more recent papers, especially in older footnotes and line wrapping
- The source uses institutional option datasets and full implied-vol surface language; adaptation to Prosperity should focus on the direction of the effect, not on exact coefficient transport
