# Equity Option Return Predictability and Expiration Days

## Source Metadata

- Input type: `pdf`
- Paper ID: `garcia_ares_2023_expiration_days`
- Raw source file: [garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf)
- Primary source file: [garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_3/research/papers_raw/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with equation skeleton, event-study findings, and figure/table captions preserved; prose is compressed into a source-faithful outline rather than reproduced verbatim
- Fidelity status: `high` for metadata, section structure, and the main empirical findings; `medium` for formula formatting because line wrapping in the PDF sometimes splits long expressions
- QA gate: `usable` (title/authors checked, core method captured, strategy-relevant formulas caveated where needed, figure/table inventory recorded, no obvious truncation)

## Paper Metadata

- Title: `Equity Option Return Predictability and Expiration Days`
- Author: `Pedro A. Garcia-Ares`
- First version on title page: `October 8, 2023`
- Current version on title page: `March 13, 2025`
- Affiliations on title page: `Notre Dame University` and `ITAM`
- Keywords on title page: `Option returns`, `option anomalies`, `expiration rollover`, `intermediary asset pricing`

## Abstract

The paper argues that much of the well-known predictability in equity option returns is
concentrated on two rollover days each month: standard option expiration Friday and
especially the following Monday. The proposed mechanism is intermediary friction:
covered-call writers and other option users roll positions around expiry, market makers
absorb the resulting order imbalance, and option prices are pushed down during that
short window.

## Section Outline

### 1. Introduction

- Predictable option returns reinterpreted through intermediary frictions
- Expiration Friday and post-expiration Monday as the dominant liquidity window

### 2. Related Literature

- Option return anomalies
- Demand pressure and intermediary constraints

### 3. Data and Methodology

#### 3.1 Option and Stock Data

- OptionMetrics, CRSP, Compustat, and signed option volume from major exchanges

#### 3.2 Monthly and Intra-monthly Delta-Hedged Option Return Computation

- Calendar-month option returns
- Daily decomposition around expiration

### 4. Empirical Results

#### 4.1 Option Returns around Expiration Days

#### 4.2 Intra-month Options Returns

#### 4.3 Option Rolling Activity and Option Returns

### 5. Revisiting Option Return Predictability

- Long-short anomaly returns with and without the expiration window

### 6. Tests for Robustness

#### 6.1 Daily and Weekly Delta-Hedge Call Option Returns

#### 6.2 Straddle Monthly Option Returns

#### 6.3 Delta-Hedged Put Option Returns

#### 6.4 Delta-Hedged Call Option Returns for Different Moneyness Intervals

### 7. Conclusions

### Appendix A

- Anomaly dictionary used in the characteristic sorts

## Key Equations / Core Method

### Stock-Level Option Order Imbalance

Following Muravyev-style signed option-volume data, the paper defines stock-level option
order imbalance as:

$$
\text{OIMB}_{i,t}
=
\frac{\sum_i (\text{Buy}_{i,t} - \text{Sell}_{i,t})}
{\sum_i (\text{Buy}_{i,t} + \text{Sell}_{i,t})}.
$$

Positive imbalance means investors are net buyers of options on that stock; negative
imbalance means net selling pressure.

### Monthly Delta-Hedged Call Gain

The paper's monthly delta-hedged gain is:

$$
\Pi_{t+\tau}
=
C_{t+\tau} - C_t
- \sum_{n=0}^{N-1}\Delta_{C,t_n}[S(t_{n+1}) - S(t_n)]
- \sum_{n=0}^{N-1}\frac{a_n r_{t_n}}{365}[C(t_n) - \Delta_{C,t_n}S(t_n)].
$$

The corresponding return scales this gain by the absolute initial delta-hedged capital.

### Return-Decomposition Components

The paper then decomposes the monthly return into parts associated with:

- terminal option value
- initial option value
- stock-hedge PnL
- financing carry

using equations `(3)` to `(6)` in the PDF. This decomposition is used to isolate the
expiration-window contribution.

## Main Empirical Findings Preserved From Source

### Expiration Window Dominates Monthly Average Option Returns

Table 2 reports the most important decomposition for strategy interpretation:

- full end-of-month to end-of-month average delta-hedged monthly call return: `-0.203%`
- end-of-month to one day before expiration: `+0.188%`
- one day before expiration to two days after expiration: `-0.430%`
- two days after expiration to month-end: `+0.039%`

This is the paper's central message in one table: the negative monthly average is mostly
an expiration-window phenomenon.

### Order Imbalance Around Expiration

Figure 3 and Table 3 show that order imbalance turns sharply negative around the
post-expiration Monday, especially for opening positions. The paper interprets this as
rolling activity in which investors close expiring positions and then open new short
positions in later expiries.

### Option Return Anomalies Shrink Outside the Rollover Window

Table 4 decomposes long-short anomaly returns into:

- full month
- full month excluding the expiration Friday plus following Monday
- rollover window only

For the cross-anomaly average:

- full month: `-0.64%`
- full month ex-rollover: `-0.28%`
- rollover only: `-0.36%`

So more than half of the full-month anomaly return is concentrated in the short rollover
window.

### S&P 500 Subsample: Expiration Effects Dominate Even More

Table 5 shows that in S&P 500 stocks:

- full-month cross-anomaly average: `-0.10%`
- rollover return alone: `-0.14%`

The paper interprets this as evidence that expiration effects can explain essentially all of
the anomaly predictability in the most actively traded option names.

### Daily and Weekly Robustness

Table 6 shows that:

- average daily delta-hedged return for all options is negative
- Mondays are much more negative than average
- Mondays after expiration are especially negative at about `-0.514%` for all options
- if expiration Mondays are excluded, the average daily effect becomes much weaker

This is the part most relevant to short-horizon regime thinking.

## Figures And Tables Asset Index

### Figures Embedded In The PDF

- `Figure 1`: option volume cycles around expiration dates
- `Figure 2`: average delta-hedged returns around the standard monthly expiration day
- `Figure 3`: option order imbalances around the standard monthly expiration day
- `Figure 4`: average returns of anomaly-sorted spread portfolios around expiration
- `Figure A1`: example of end-of-month to end-of-month portfolio formation and holding period

### Tables Embedded In The PDF

- `Table 1`: summary statistics for returns and characteristics
- `Table 2`: intra-month average delta-hedged returns and the expiration decomposition
- `Table 3`: post-expiration Monday order imbalance sorts
- `Table 4`: anomaly returns, full month vs ex-rollover vs rollover
- `Table 5`: same anomaly decomposition for S&P 500 stocks
- `Table 6`: daily and weekly robustness for call options
- `Table 7`: straddle monthly option returns
- `Table 8`: delta-hedged put option returns
- `Table 9`: delta-hedged call returns by moneyness bucket

## Current-Round-Relevant Hooks

- The paper is strong evidence that near-expiry option behavior can enter a different flow-
  and inventory-driven regime, even if average behavior away from expiry looks calmer.
- For Round 3, the main lesson is not "copy expiration Monday logic" but "do not assume
  that TTE `6d-8d` residual behavior transfers unchanged to TTE `5d`."
- It supports faster signal decay, shorter holding assumptions, and stricter entry thresholds
  for expiry-sensitive voucher trades.
- The focus on order imbalance and rollover pressure makes this paper a good validation
  source for treating imbalance as a regime modifier around expiry rather than a universal
  alpha.

## Conversion Caveats

- This file is a structural Markdown conversion for strategy research, not a full-text
  reproduction of the paper.
- The empirical setting is monthly U.S. equity option expiration with third-Friday rollover,
  which is not mechanically identical to Prosperity Round 3.
- The useful carryover is regime interpretation, not direct parameter transfer.
