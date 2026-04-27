# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `vasios_2015_mimicking_non_anonymous`
- Title: `Profiting from Mimicking Strategies in Non-Anonymous Markets`
- Source / venue: `MPRA / SSRN working paper`
- Authors: `Ingmar Nolte`, `Richard Payne`, `Michalis Vasios`
- Year: `2015` posting, `2013` manuscript date
- Raw file: [vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.pdf)
- Markdown file: [vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/vasios_payne_nolte_2015_profiting_from_mimicking_strategies_in_non_anonymous_markets.md)
- Link: [MPRA PDF](https://mpra.ub.uni-muenchen.de/61710/3/MPRA_paper_61710.pdf)

## Core Claim

- In non-anonymous markets, identity-conditioned order flow can improve decision quality, but not because names are magic labels. The real edge comes from persistent heterogeneity in what different participants' flow tends to mean.

## Assumptions

- Visible `buyer/seller` fields in `round_4` are close enough to non-anonymous post-trade disclosure for the logic to transfer.
- Our goal is not to copy a portfolio-construction result, but to learn how identity and flow should interact.
- Participant effects in Prosperity may be less stable than broker effects in the paper's equity market.

## Problem Addressed for Round 4

- We need to decide how to use `Mark 22`-style information without overfitting to raw names.
- The EDA already suggests raw names alone are weak, while flow-conditioned identity is more useful. This paper is the cleanest external support for that distinction.

## What This Paper Gives Us

- Formula / approximation:
  no single live formula; the main object is `identity-conditioned net flow`.
- Constraints / checks:
  the original result is built on daily portfolio formation in equities, not live option market making.
- Point of view:
  participant identity matters when it changes the meaning of flow.
- Simplification:
  prefer `recent dominant flow by participant` and `participant-conditioned danger state` over blunt `if name then trade`.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `Mark 22` seller-state in `VEV_5200+` | near-direct conceptual match | high | our data horizon is much shorter |
| raw names weak, engineered context stronger | strongly supports current EDA reading | high | no exact coefficient transfer |
| counterparty concentration by symbol/side | helps interpret concentration as meaningfully heterogeneous | medium | concentration alone still not enough |
| role-aware participant flow features | motivates them directly | high | should stay simple and robust |

## Round X Mapping

- Interpret `Mark XX` not as alpha labels but as modifiers of order-flow meaning.
- Favor features such as:
  - `recent participant dominance`
  - `participant-conditioned side persistence`
  - `participant flow role by strike cluster`

## Minimal Usable Adaptation

- Online-usable adaptation:
  use counterparty-aware gating and participant-conditioned context features.
- Required proxy or simplification:
  replace broker-level forecast systems with simple rolling state derived from `buyer/seller`, side, and recent repetition.
- Runtime / state caveat:
  must degrade gracefully if participant behavior changes.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  hard or soft veto layers based on repeated adverse participant-side states in toxic strikes.
- Failure mode addressed:
  overreacting to raw names or underreacting to persistent participant-conditioned flow.
- Validation implication:
  compare `raw name seen` against `participant-conditioned state` for incremental value.

## Do Not Overuse

- Do not build identity-as-destination logic like `always fade/follow X`.
- Do not assume participant effects are stationary.
- Do not extrapolate return magnitudes from the source market to Prosperity.

## Risks And Limitations

- The paper is equity-focused and slower-frequency than our setting.
- Participant role drift is a real risk in `round_4`.
- The transferable value is framing and feature design, not direct mimicry.

## Action Classification

- Classification: `new candidate`
- Why:
  it directly supports a high-ROI counterparty feature family already hinted at by EDA and Understanding.

## Strategy Hooks

- `participant_conditioned_danger_state`
- `recent_dominant_seller_by_cluster`
- `counterparty_context_gate` for `VEV_5200+`

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this is one of the clearest papers for the new visible-counterparty layer in `round_4`.
