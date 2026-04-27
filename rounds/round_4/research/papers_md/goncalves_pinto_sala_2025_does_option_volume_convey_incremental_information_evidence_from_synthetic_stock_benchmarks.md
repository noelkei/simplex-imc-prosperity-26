# Does Option Volume Convey Incremental Information? Evidence from Synthetic Stock Benchmarks

## Source Metadata

- Input type: `pdf`
- Paper ID: `goncalves_pinto_sala_2025_incremental_option_volume`
- Raw source file: [goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf)
- Primary source file: [goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf)
- Input assets preserved in raw source: figures and tables are embedded in the PDF only
- Conversion method: PDF-first structural extraction with abstract preservation and section recovery; emphasis placed on the benchmark logic that limits overclaiming from option-flow predictability
- Fidelity status: `high` for metadata, abstract, and central empirical claim; `medium` for full theoretical-model detail
- QA gate: `usable`

## Paper Metadata

- Title: `Does Option Volume Convey Incremental Information? Evidence from Synthetic Stock Benchmarks`
- Authors: `Luis Goncalves-Pinto`, `Carlo Sala`
- Year: `2025`
- Source note on title page: working-paper style manuscript with theory plus empirical tests
- Topic frame: option-volume predictability, synthetic-stock benchmarks, guardrail against overstated option-flow information

## Abstract

The paper argues that if option volume contains incremental information, it should forecast the spread between actual stock returns and synthetic option-implied stock returns, not just raw stock returns. Testing this around earnings, material events, and regular calendar windows, the authors find that signed and unsigned option volume consistently fails to predict that spread. Apparent predictability is weak, economically negligible, or sign-reversing. Their conclusion is that much prior literature likely overstated the informational value of option volume by not benchmarking against synthetic returns.

## Section Outline

### 1. Introduction

- Why standard option-volume predictability claims may be too generous
- Motivation for a stricter synthetic-benchmark test

### 2. Theoretical Framework

- Noisy rational-expectations setting with informed trading across stock and options
- Testable implication for actual-vs-synthetic return spreads

### 3. Empirical Analysis

- Earnings, filings, and calendar-event tests
- Signed vs unsigned volume
- Strength and economic significance of any residual predictability

### 4. Conclusion

- Option volume should not automatically be treated as incremental information

## Key Equations / Core Method

### Synthetic-Benchmark Logic

The paper's key methodological move is to ask a tougher question than "does option volume predict returns?":

- does option volume predict actual returns relative to synthetic option-implied returns?

If not, then observed predictability may just be restating information already contained in prices rather than adding new information.

### Strategy-Relevant Translation

For `round_4`, this is an excellent anti-self-deception paper. It suggests that:

- `counterparty flow` and `option flow` need benchmarked validation
- descriptive structure alone is not enough
- any participant-flow signal should be tested against what is already encoded in `VEX`, spreads, and the local surface

## Figures And Tables Asset Index

- PDF-only asset layout; no separate raw figure files
- Most relevant embedded items are:
  - tests around earnings and event windows
  - comparisons of signed and unsigned option volume
  - benchmark-based predictability tables

## Current-Round-Relevant Hooks

- Strong guardrail against overpromoting `option-flow alpha`
- Supports the policy of testing participant-conditioned features for incremental value over baseline market-state features
- Useful validation reference once strategy candidates start producing apparently strong flow-based edges

## Conversion Caveats

- The paper is more useful as a validation discipline than as a direct source of bot features
- Its benchmark logic is richer than Prosperity's minimal market, so adaptation should focus on `incremental-value testing`, not on reproducing the exact empirical design
