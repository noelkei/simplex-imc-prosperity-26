# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `roos_2026_arbitrage_free_interpolation`
- Title: `Simple, Flexible, Analytic, Arbitrage Free Option Price Interpolation`
- Source / venue: `technical working paper`
- Author: `Thomas Roos`
- Year: `2026`
- Raw file: [roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.pdf)
- Markdown file: [roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/roos_2026_simple_flexible_analytic_arbitrage_free_option_price_interpolation.md)
- Link: [SSRN abstract 5215592](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5215592)

## Core Claim

- Option prices can be interpolated across strikes and expiries with an analytic, arbitrage-free scheme that is far lighter than a full stochastic-volatility stack while still preserving smoothness, wing control, and surface coherence.

## Assumptions

- `round_4` voucher quotes are sparse and noisy enough that a cheap surface-sanity layer could improve interpretation.
- We do not need the paper's full interpolation machinery live to benefit from its design principles.
- The main transfer is `cheap arbitrage-aware surface context`, not a production-quality options library.

## Problem Addressed for Round 4

- We need a better surface-aware mental model than flat-vol, but we do not want to promote Heston/COS-style research infrastructure into live bot logic.
- EDA already showed that residual and surface interpretation matter, especially when flow distorts upper strikes.

## What This Paper Gives Us

- Formula / approximation:
  a lightweight, analytic, arbitrage-aware interpolation framework for option prices.
- Constraints / checks:
  our market has only one short family and much sparser data than the paper's intended use.
- Point of view:
  surface structure should be smoothed and sanity-checked before being treated as alpha.
- Simplification:
  use a cheap local surface or residual sanity layer rather than a full calibration engine.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| sparse and noisy voucher quotes | supports smoothing / sanity filtering | high | our quote set is much smaller |
| residual logic around upper strikes | useful structural framing | medium | does not create a direct signal by itself |
| avoiding Heston-heavy live logic | directly supports lightweight alternative | high | still mostly an offline or spec-level tool |
| local cross-strike interpretation | useful for EDA / validation follow-up | medium | expiration dimension is limited in our setting |

## Round X Mapping

- Map the paper's value to:
  - `surface sanity layer`
  - `cheap residual backbone`
  - `do not trust every kink`
- Treat it as support for offline framing, validation, or a very lightweight pricing overlay.

## Minimal Usable Adaptation

- Online-usable adaptation:
  at most a tiny local residual/surface check based on neighboring strikes.
- Required proxy or simplification:
  use local cross-strike smoothing or interpolation heuristics, not the full paper model.
- Runtime / state caveat:
  keep any live use extremely cheap and transparent; likely better as EDA/validation support first.
- Implementability: `EDA-follow-up`

## Strategy Implications

- Candidate or execution idea:
  no direct candidate by itself; it can support a later surface-aware residual overlay if Strategy already wants one.
- Failure mode addressed:
  overtrading noisy quote kinks or fake local mispricings in a sparse book.
- Validation implication:
  compare any residual-based idea against a cheap smoothed baseline before calling it alpha.

## Do Not Overuse

- Do not import the full interpolation framework into the live bot by default.
- Do not assume arbitrage-free interpolation creates edge on its own.
- Do not let a surface model outrank stronger `VEX` anchor and counterparty-state evidence.

## Risks And Limitations

- The paper is a technical interpolation note, not a market-microstructure study.
- Prosperity has limited expiries and sparse local quotes, so some advantages shrink.
- The best use is as a structural filter or offline sanity layer, not core live strategy.

## Action Classification

- Classification: `EDA follow-up`
- Why:
  it is best used to improve residual and surface framing if later strategy work needs that layer, not as an immediate candidate source.

## Strategy Hooks

- `surface_sanity_filter`
- `neighbor_strike_residual_check`
- `smoothed_baseline_before_calling_mispricing`

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this is the cleanest lightweight alternative to overcommitting to heavy stochastic-vol tooling.
