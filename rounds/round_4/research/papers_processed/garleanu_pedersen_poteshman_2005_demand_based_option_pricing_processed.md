# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `garleanu_pedersen_poteshman_2005_demand_based_option_pricing`
- Title: `Demand-Based Option Pricing`
- Source / venue: `NBER working paper`
- Authors: `Nicolae Garleanu`, `Lasse Heje Pedersen`, `Allen M. Poteshman`
- Year: `2005`
- Raw file: [garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/garleanu_pedersen_poteshman_2005_demand_based_option_pricing.pdf)
- Markdown file: [garleanu_pedersen_poteshman_2005_demand_based_option_pricing.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/garleanu_pedersen_poteshman_2005_demand_based_option_pricing.md)
- Link: [NBER w11843](https://www.nber.org/papers/w11843)

## Core Claim

- Option demand pressure affects prices when options cannot be perfectly hedged, and those effects propagate across contracts according to the covariance of their unhedgeable components. In plain terms: one strike's demand can distort neighboring strikes structurally, not just locally.

## Assumptions

- `round_4` vouchers are sufficiently linked through `VEX` that family-level demand effects are plausible.
- We do not need the full incomplete-markets machinery; we need its directionally correct implication for family-level state.
- The transfer target is strategy framing and feature prioritization, not live formula replication.

## Problem Addressed for Round 4

- We need a principled reason to think in terms of `family pressure` and `cross-strike contagion`.
- EDA already hints that `5200`, `5300`, and upper strikes can distort each other under concentrated flow. This paper gives the theoretical backbone for that reading.

## What This Paper Gives Us

- Formula / approximation:
  cross-contract demand pressure should move related option prices according to shared unhedgeable risk.
- Constraints / checks:
  we do not have dealer/end-user inventories or the full covariance structure.
- Point of view:
  option prices can be demand-shaped across the family, not just mispriced one by one.
- Simplification:
  build a family-level state variable and avoid treating each strike as isolated.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| family-level voucher framing | direct support | high | theory is stronger than our data observability |
| cross-strike pressure around `5200/5300` | strongly relevant | high | needs a simple proxy in practice |
| upper-strike selling affecting active zone interpretation | conceptually useful | medium | not a direct proof of causal spillover here |
| `family imbalance` from round 3 unresolved backlog | excellent carry-forward support | high | still needs round-specific validation |

## Round X Mapping

- Use the paper to justify:
  - `family_pressure`
  - `cross_strike_context`
  - `residual + family flow` interpretations
- Treat these as structural context layers, not as direct formulas to compute dealer equilibrium.

## Minimal Usable Adaptation

- Online-usable adaptation:
  a simple family-level pressure metric over active voucher strikes.
- Required proxy or simplification:
  use trade flow, counterparty concentration, and strike-role weights instead of dealer inventory covariance.
- Runtime / state caveat:
  should remain a compact state summary, not a model calibration task.
- Implementability: `EDA-follow-up`

## Strategy Implications

- Candidate or execution idea:
  use family pressure as a gating or weighting layer for strike-specific trades.
- Failure mode addressed:
  reopening a broad basket as if strike-local signals were independent.
- Validation implication:
  test whether family-aware variants outperform strike-local-only variants.

## Do Not Overuse

- Do not claim the paper proves specific tick-level edges in our game.
- Do not try to port incomplete-markets equations directly into `Trader.run()`.
- Do not replace the `VEX` anchor with family pressure; use them jointly.

## Risks And Limitations

- The theory is strong, but our observability is much weaker.
- This is more valuable as framing and candidate justification than as a ready-made online rule.

## Action Classification

- Classification: `EDA follow-up`
- Why:
  it most strongly supports the construction and prioritization of family-level features, which may then become candidate inputs.

## Strategy Hooks

- `family_pressure`
- `cross_strike_context_gate`
- `family-aware residual interpretation`

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this is one of the most important theory papers for not treating the `VEV_*` family as independent symbols.
