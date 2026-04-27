# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `kaeck_2019_informed_index_options`
- Title: `Informed Trading in the Index Option Market`
- Source / venue: `working paper`
- Authors: `Andreas Kaeck`, `Vincent van Kervel`, `Norman J. Seeger`
- Year: `2019`
- Raw file: [kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.pdf)
- Markdown file: [kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/kaeck_van_kervel_seeger_2019_informed_trading_in_the_index_option_market.md)
- Link: [SSRN abstract 2981332](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2981332)

## Core Claim

- Option order flow becomes more informative when it is aggregated into economically meaningful exposures such as delta order flow and vega order flow, rather than treated as isolated contract-by-contract noise. This helps detect information about both the underlying price and volatility.

## Assumptions

- `round_4` vouchers share enough anchor linkage through `VEX` that family-level aggregation is meaningful.
- We do not need the full structural VAR; we need the paper's aggregation logic.
- Option Greek estimates used online would have to be simplified and role-aware, not fully institutional.

## Problem Addressed for Round 4

- Our EDA already says the voucher family behaves more like a linked option book than a set of independent symbols.
- We need a principled reason to promote `family-level flow` and `cross-strike context` over strike-local counts.

## What This Paper Gives Us

- Formula / approximation:
  aggregate signed option flow into `price-like` and `vol-like` economic exposures instead of raw symbol-local flow.
- Constraints / checks:
  the exact VAR model is too heavy for live use and the maturity structure in Prosperity is much smaller.
- Point of view:
  compress the option family into interpretable state variables rather than dozens of noisy per-strike observations.
- Simplification:
  use strike-role weights or simple delta-style weights to build a `family pressure` or `active-zone pressure` metric.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| need for family-level voucher framing | strongly supports it | high | the original setting has richer data than Prosperity |
| `5100/5200/5300` not homogeneous | supports role-aware aggregation rather than equal basket logic | high | we still need our own role weights |
| upper-strike selling may be vol-like state | offers a clean conceptual frame | medium | exact delta/vega decomposition may be too heavy online |
| cross-strike and anchor-aware features | helps prioritize them over raw names or raw counts | high | must stay simple enough to debug |

## Round X Mapping

- Use the paper to justify building:
  - `family_flow_pressure`
  - `active_zone_flow_pressure`
  - possibly `price-like` versus `vol-like` simplified bucket signals
- Avoid staying at the level of `per-strike raw trade count`.

## Minimal Usable Adaptation

- Online-usable adaptation:
  simple weighted aggregation across `VEV_*` using strike roles or rough deltas.
- Required proxy or simplification:
  replace exact institutional Greeks with our lightweight calibrated table or role buckets.
- Runtime / state caveat:
  do not carry over the structural VAR into bot logic.
- Implementability: `variant-only`

## Strategy Implications

- Candidate or execution idea:
  build a family-level or active-zone pressure signal to supplement `VEX` anchor logic and counterparty context.
- Failure mode addressed:
  treating each voucher as if it were an isolated symbol with independent flow.
- Validation implication:
  compare family-aggregated features against symbol-local features for incremental value.

## Do Not Overuse

- Do not port the VAR machinery into live logic.
- Do not claim `delta flow` or `vega flow` are exact in our game.
- Do not force every strike into one common metric if role split argues against it.

## Risks And Limitations

- Exact Greek-based decomposition may be fragile in a sparse game setting.
- The biggest value is conceptual compression, not formula transport.

## Action Classification

- Classification: `new candidate`
- Why:
  it directly supports a family-level feature direction that could change candidate design in `03 Strategy`.

## Strategy Hooks

- `family_flow_pressure` as a first-class feature
- `active_zone_pressure` around `5200/5300`
- use family-level flow as context for `VEX`-anchored option decisions

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this paper is best used to justify and shape a simpler family-flow abstraction, not to import heavy econometrics.
