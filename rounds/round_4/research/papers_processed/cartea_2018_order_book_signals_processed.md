# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `cartea_2018_order_book_signals`
- Title: `Enhancing Trading Strategies with Order Book Signals`
- Source / venue: `execution / market-microstructure paper`
- Authors: `Álvaro Cartea`, `Ryan Donnelly`, `Sebastian Jaimungal`
- Year: `2018`
- Raw file: [cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.pdf)
- Markdown file: [cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/cartea_donnelly_jaimungal_2018_enhancing_trading_strategies_with_order_book_signals.md)
- Link: [SSRN abstract 2668277](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2668277)

## Core Claim

- Order-book imbalance improves trading decisions primarily by reducing adverse selection and improving execution placement. The main value is defensive and executional, not necessarily directional.

## Assumptions

- Our top-of-book state and book imbalance measures are rich enough to serve as a lightweight analogue of the source setting.
- We do not need the continuous-time control model to benefit from the imbalance logic.
- `round_4` already has useful `trade-to-book context` from EDA that can pair well with this paper.

## Problem Addressed for Round 4

- We need practical rules for when to quote, when to suppress quotes, and when to reduce size in the voucher book.
- EDA has already shown that some contexts are best used defensively. This paper gives that defensive posture a strong external basis.

## What This Paper Gives Us

- Formula / approximation:
  imbalance as a state variable for execution and adverse-selection control.
- Constraints / checks:
  full stochastic control is too heavy for live logic.
- Point of view:
  imbalance is most valuable because it protects you from bad fills.
- Simplification:
  use imbalance and trade-to-book context as part of a quote filter or quote-location modifier.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `trade-to-book context` from EDA | directly supported | high | our book is much smaller and noisier |
| `danger-state` / no-trade logic | strongly supported | high | needs role-aware thresholds by strike |
| quote suppression in `VEV_5200+` | directly useful | high | not all imbalance is equally toxic |
| use of imbalance alongside counterparties | strong complement | high | should not become a giant composite monster |

## Round X Mapping

- Map imbalance to:
  - `quote less aggressively`
  - `skip aggressive fills`
  - `reduce size`
  - `prefer passive only`
- Combine with counterparty state instead of replacing it.

## Minimal Usable Adaptation

- Online-usable adaptation:
  lightweight imbalance-based quoting gates and quote-offset adjustments.
- Required proxy or simplification:
  use top-of-book imbalance, recent flow, and spread state instead of a full Markov model.
- Runtime / state caveat:
  should be implemented as a simple deterministic policy layer, not a control solver.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  imbalance-conditioned execution overlays on top of `VEX` anchor and strike-role logic.
- Failure mode addressed:
  getting lifted or hit in adverse local book states.
- Validation implication:
  compare fills and markouts with and without the imbalance filter.

## Do Not Overuse

- Do not import the full mathematical control stack.
- Do not assume one imbalance threshold works for every product or strike role.
- Do not mistake execution improvement for direct alpha.

## Risks And Limitations

- The source market is deeper and more continuous than Prosperity.
- Overcomplicating imbalance state will quickly reduce debuggability.

## Action Classification

- Classification: `new candidate`
- Why:
  it gives a very practical route to turn EDA imbalance findings into execution logic for `03 Strategy`.

## Strategy Hooks

- `imbalance_gate`
- `quote_suppression_on_bad_book_state`
- `trade_to_book_context_filter`

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this paper is strongest as an execution and adverse-selection overlay, not a pricing engine.
