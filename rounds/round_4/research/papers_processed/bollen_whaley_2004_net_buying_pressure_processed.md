# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `bollen_whaley_2004_net_buying_pressure`
- Title: `Does Net Buying Pressure Affect the Shape of Implied Volatility Functions?`
- Source / venue: `empirical options paper`
- Authors: `Nicolas P. B. Bollen`, `Robert E. Whaley`
- Year: `2004`
- Raw file: [bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.pdf)
- Markdown file: [bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/bollen_whaley_2004_does_net_buying_pressure_affect_the_shape_of_implied_volatility_functions.md)
- Link: [SSRN abstract 319261](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=319261)

## Core Claim

- Net buying pressure distorts implied-volatility functions, and those distortions can be strong without creating clean arbitrage. Apparent residuals in option prices may reflect demand pressure rather than pure mispricing.

## Assumptions

- `round_4` voucher prices are sparse and game-like, but still surface-linked strongly enough that demand distortions can matter.
- We are not trying to rebuild a full implied-volatility literature stack; we want a good guardrail against reading every residual as alpha.
- Our adapted features must stay simple and anchor-aware.

## Problem Addressed for Round 4

- We already know from EDA that surface shape and residuals matter, but counterparties and concentrated flow can deform that surface.
- We need a principled reason to treat `residual + strong flow` as a possible veto state rather than an automatic trade.

## What This Paper Gives Us

- Formula / approximation:
  an empirical logic for conditioning surface interpretation on demand pressure.
- Constraints / checks:
  exact regression transport is inappropriate for Prosperity.
- Point of view:
  flow-distorted surface does not imply free money.
- Simplification:
  use residual signals only when they are not obviously accompanied by strong one-sided family flow or participant concentration.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `VEV_*` residuals under concentrated flow | directly relevant | high | our surface is much smaller and noisier |
| upper-strike seller dominance | helps reinterpret it as possible demand distortion | high | not a proof of volatility trading by itself |
| need for residual guardrails | strongly supports them | high | do not overfit residual thresholds |
| `5300` vs `5200+` interpretability | helps justify context-aware reading of mispricing | medium | still needs empirical validation in our game |

## Round X Mapping

- Read `surface distortion` through a joint lens:
  - residual versus `VEX` anchor
  - family pressure
  - participant concentration
- When all three agree, the setup may be real.
- When residual fights concentrated flow, treat it as caution or veto first.

## Minimal Usable Adaptation

- Online-usable adaptation:
  residual signals gated by family flow / counterparty state.
- Required proxy or simplification:
  no full IVF regression; just use local surface and family-pressure context.
- Runtime / state caveat:
  must remain a cheap logic layer, not a full volatility-surface engine.
- Implementability: `validation-only`

## Strategy Implications

- Candidate or execution idea:
  residual trades only when flow context is benign.
- Failure mode addressed:
  overtrading flow-distorted surface kinks.
- Validation implication:
  compare residual-only trades versus residual-plus-flow-filter trades.

## Do Not Overuse

- Do not use this as justification to add a heavy surface model live.
- Do not conclude that every skew move is demand-only and ignore anchor information.
- Do not treat this as a direct candidate source for naked alpha.

## Risks And Limitations

- The empirical setting is richer and cleaner than our game surface.
- This paper is most valuable as a guardrail, not as a standalone strategy driver.

## Action Classification

- Classification: `validation check`
- Why:
  its main role is to keep residual logic honest and reduce false alpha claims.

## Strategy Hooks

- `residual_with_flow_filter`
- `surface_distortion_veto`
- stronger skepticism on upper-strike residuals under one-sided selling

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this is one of the key guardrail papers for any residual-driven voucher strategy.
