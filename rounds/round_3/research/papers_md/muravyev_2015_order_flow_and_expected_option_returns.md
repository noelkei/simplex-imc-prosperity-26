# Order Flow and Expected Option Returns

## Source Metadata

- Input type: `pdf`
- Paper ID: `muravyev_2015_option_order_flow`
- Raw source file: [muravyev_2015_order_flow_and_expected_option_returns.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/muravyev_2015_order_flow_and_expected_option_returns.pdf)
- Primary source file: [muravyev_2015_order_flow_and_expected_option_returns.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/muravyev_2015_order_flow_and_expected_option_returns.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with section hierarchy, decomposition equations, regression setup, and figure/table captions preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, key equations, and main empirical findings; `medium` for some symbol-heavy microstructure notation because the PDF extraction introduces a few glyph substitutions
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant formulas verified or caveated, figure/table inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Order Flow and Expected Option Returns`
- Author: `Dmitriy Muravyev`
- PDF metadata title field: `Microsoft Word - Order Flow and Expected Option Returns 2015 2`
- Source style: `Journal of Finance-style manuscript with tables and figures embedded`

## Abstract

The paper argues that option market-maker inventory risk is a first-order driver of option
prices and returns. It builds both an intraday trade-impact decomposition and a daily
return-predictability framework, concluding that order imbalance associated with inventory
risk has a much larger effect on option prices than standard same-day OLS approaches
suggest and that past order imbalances outperform a large menu of other predictors of
future option returns.

## Section Outline

### I. Related Options Microstructure Literature

- Positioning within market-maker inventory and option spread literature
- Motivation for separating inventory risk from asymmetric information

### II. Price Impact Decomposition Method

#### A. The Idea

- Compare price responses of trading vs nontrading exchanges after the same trade

#### B. Conceptual Framework

- Multi-market-maker extension of classic inventory/information spread decomposition

#### C. Assumptions

- Transparent market, standardized information, many competitive market makers, no direct inventory sharing

### III. Data Description and Sample Construction

#### A. Data Description

#### B. Data Filters

#### C. Computation of Price Impact Components

### IV. Empirical Results

- Intraday price-impact decomposition
- Cross-sectional robustness by trade and option characteristics

### V. Inventory Risk and Daily Option Returns

#### A. Computation of Option Returns and Order Imbalances

#### B. Instrumental Variables Approach

#### C. Return Predictability: Inventory Risk versus Other Factors

### VI. Conclusion

## Key Equations / Core Method

### Trading vs Nontrading Exchange Idea

The core identification argument is that a trade reveals the same information to every
market maker, but only the exchange that actually fills the trade experiences the
inventory shock. Therefore:

- price response at the trading exchange = information component + inventory component
- price response at nontrading exchanges = information component only

The difference between the two responses identifies the inventory-risk component.

### Price Impact Decomposition

The paper's stylized setup writes price responses so that:

$$
\Delta p_{\text{trading}}
=
\text{information impact}
+
\text{inventory impact},
$$

$$
\Delta p_{\text{nontrading}}
=
\text{information impact}.
$$

The paper then generalizes this simple intuition into sign-adjusted empirical formulas.

The main decomposition equations are:

$$
\text{Asymmetric information impact}
=
E\left[s_i\left(\Delta p_{i^*} - E[\Delta v \mid \mathcal{F}_t]\right)\right],
$$

$$
\text{Inventory risk impact}
=
E\left[s_i\left(\Delta p_i - \Delta p_{i^*}\right)\right],
$$

where `s_i` is trade direction, `i` denotes the trading exchange, and `i*` denotes
nontrading exchanges quoting the same best price.

### Bid-Ask Spread Decomposition Intuition

Inside the conceptual framework, the paper writes quote setting so that bid-ask spreads
contain three components:

- asymmetric information
- inventory risk
- fixed costs

The practical implication preserved here is that inventory risk can move prices even when
the quoted spread itself is not the right place to look for the dominant effect.

## Daily Return And Order-Imbalance Setup

### Delta-Neutral Option Return

For the daily analysis, the paper computes option returns from a delta-neutral straddle
portfolio and treats those returns as a model-light measure of option risk premia.

The straddle value is:

$$
W_t = C_t + \frac{\Delta(C_t)}{|\Delta(P_t)|} P_t,
$$

and the one-day return is:

$$
\text{Return}_t = \frac{W_t - W_{t-1}}{W_{t-1}}.
$$

The exact PDF notation is more compact, but this is the structural object the paper uses.

### Individual Order Imbalance

The stock-level order imbalance is defined as the difference between option buy and sell
transactions by non-market-makers, normalized by total trades:

$$
\text{OrdImb}_{A,t}
=
\frac{\#\text{BuyTrades}_{A,t} - \#\text{SellTrades}_{A,t}}
{\#\text{Trades}_{A,t}}.
$$

### Market-Wide Order Imbalance

The market-wide imbalance is a volume-weighted average across stocks:

$$
\text{MWOrdImb}_t
=
\sum_i w_{i,t} \, \text{OrdImb}_{i,t},
$$

where weights use historical option volume.

This is central to the paper's portfolio-inventory interpretation: market makers manage
inventory on a portfolio basis, so market-wide imbalance carries more information than a
single-symbol imbalance alone.

## Key Regression Setups Preserved From Source

### Instrumental-Variables First and Second Stage

The paper estimates persistent order imbalance in the first stage:

$$
\text{AdjOrdImb}_{i,t}
=
\beta_0
+ \beta_1 \text{IVSet}_{i,t}
+ \beta' \text{Controls}_{i,t}
+ \varepsilon_{i,t},
$$

where the instrument sets include:

- expiration-day dummies centered on the post-expiration Monday
- lags of market-wide order imbalance
- lags of individual order imbalance

The second stage links instrumented imbalance to option returns:

$$
\text{OptRet}_{i,t}
=
\alpha_0
+ \alpha_1 \widehat{\text{AdjOrdImb}}_{i,t}
+ \alpha' \text{Controls}_{i,t}
+ \varepsilon_{i,t}.
$$

### Horse-Race Predictive Regression

The predictive comparison in Section V.C is:

$$
\text{OptRet}_{i,t}
=
\alpha_0
+ \alpha_1 \text{OrdImb}_{i,t-1}
+ \alpha_2 \text{MWOrdImb}_{t-1}
+ \beta' \text{OtherPredictors}_{i,t-1}
+ \varepsilon_{i,t}.
$$

This is the key bridge to Round 3: order imbalance is evaluated against many alternative
predictors and still wins.

## Main Empirical Findings Preserved From Source

### Intraday Price-Impact Findings

- The inventory-risk component of option trade price impact is larger than the asymmetric-information component for every stock in the sample.
- Table II reports a sample-wide mean information impact of about `0.22%` and mean inventory impact of about `0.41%` per trade, after normalization.
- Table III shows inventory impact grows strongly with trade size and is larger for lower absolute-delta options and shorter-dated options.

### Daily Return Findings

- In Table V, the IV estimate of the effect of order imbalance on same-day option returns is about `0.15` on average across instrument sets, versus about `0.025` under OLS.
- The paper interprets this as a typical inventory shock moving option prices by roughly `3.7%` on the same day, about five times the OLS implication.
- Order imbalance is highly persistent, with especially strong negative imbalance around option expiration and post-expiration Monday.

### Predictability Findings

- In Table VI, lagged individual imbalance and lagged market-wide imbalance jointly dominate a large predictor horse-race.
- The paper states that a one-standard-deviation increase in the combined imbalance factor predicts about `1%` higher next-day option return.
- This makes order imbalance the strongest predictor among more than 50 commonly used variables in the paper's comparison set.

## Figures And Tables Asset Index

### Figures Embedded In The PDF

- `Figure 1`: stylized trading-vs-nontrading exchange example for the decomposition method
- `Figure 2`: nonparametric inventory and information price impacts as a function of option trade size
- `Figure 3`: robustness checks for the nonparametric impact estimates across subsamples and settings

### Tables Embedded In The PDF

- `Table I`: summary statistics and sample filters for the intraday trade dataset
- `Table II`: price-impact components across 36 stocks and four ETFs
- `Table III`: dependence of information impact, inventory impact, and stock impact on trade/option characteristics
- `Table IV`: summary statistics for daily return and imbalance variables
- `Table V`: IV first-stage and second-stage results for imbalance and option returns
- `Table VI`: horse-race between order imbalance and other option-return predictors

## Current-Round-Relevant Hooks

- The paper strongly supports treating option-book imbalance as a real signal, but not as
  pure directional alpha. It is tied to market-maker inventory pressure.
- The market-wide / portfolio-level result is especially relevant for Round 3 because voucher
  symbols share a common underlying and likely share dealer-style inventory pressure.
- The source is a good justification for using imbalance as a secondary modifier or
  confirmation layer on top of the extrinsic residual, rather than as the main strategy axis.
- The expiration findings also connect naturally to the later Garcia-Ares paper, reinforcing
  the idea that near-expiry option behavior is flow- and inventory-regime dependent.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- Several equations in the PDF use notation that extracts noisily; any implementation or
  citation should be verified against the raw PDF.
- The paper relies on rich exchange-level datasets and offline econometrics. For Round 3 it
  should be treated as method inspiration and interpretation support, not as directly
  deployable code logic.
