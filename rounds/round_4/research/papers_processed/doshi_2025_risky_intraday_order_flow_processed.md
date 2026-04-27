# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `doshi_2025_risky_intraday_order_flow`
- Title: `Risky Intraday Order Flow and Option Liquidity`
- Source / venue: `working paper`
- Authors: `Hitesh Doshi`, `Paola Pederzoli`, `Saim Ayberk Sert`
- Year: `2025`
- Raw file: [doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.pdf)
- Markdown file: [doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/doshi_pederzoli_sert_2025_risky_intraday_order_flow_and_option_liquidity.md)
- Link: [SSRN abstract 5006194](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5006194)

## Core Claim

- In short- and ultra-short-maturity options, the intraday distribution of order flow is a stronger driver of spreads than classical delta-hedging needs. Liquidity providers appear to manage risk primarily through trade matching and selective participation, not through textbook continuous hedging alone.

## Assumptions

- `round_4` vouchers are close enough to short-dated listed options that liquidity-state lessons can transfer directionally.
- We can only observe top-of-book, trades, counterparties, and simple rolling state, not exchange-level routing or institutional market structure.
- The useful object is not the paper's exact exchange-design identification, but the regime distinction between calm flow and unstable intraday flow.

## Problem Addressed for Round 4

- We need a principled basis for `danger-state`, `quote-suppression`, and `no-trade` logic in `VEV_5200+`.
- Our EDA already shows concentrated counterparties, widening friction, and negative markouts in upper strikes; this paper tells us how to think about those states: unstable flow is itself a liquidity risk, not just a symptom.

## What This Paper Gives Us

- Formula / approximation:
  a practical state variable family based on intraday order-flow volatility or instability, rather than relying only on signed imbalance.
- Constraints / checks:
  the paper's identification uses cross-exchange variation that we do not have, so we should not imitate the regressions literally.
- Point of view:
  short-dated option liquidity is mainly about whether incoming flow can be matched safely.
- Simplification:
  use a rolling `flow instability` proxy in the voucher family, especially `5200+`, as a defensive state variable.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `Mark 22` seller dominance in `VEV_5200+` | explains why repetitive one-sided flow should worsen liquidity state | high | counterparty identity is our proxy for flow state, not the paper's exact object |
| `post-trade markout` deterioration in upper strikes | supports quote suppression or no-trade logic | high | paper studies marketwide liquidity, not one game market |
| family-level flow instability vs signed imbalance | validates building `instability` rather than only `imbalance` features | high | requires a simple proxy from our data |
| delta hedge obsession in short-dated options | argues hedge need is secondary to matching conditions | medium | do not overgeneralize to all strikes equally |

## Round X Mapping

- Map the paper's `order-flow volatility` idea to a simple rolling state built from:
  - recent trade count variance,
  - side flipping or one-sided persistence,
  - counterparty concentration,
  - spread widening or depth thinning.
- Treat this as a `defensive regime feature`, not a direct directional signal.

## Minimal Usable Adaptation

- Online-usable adaptation:
  build a voucher-family `flow_instability_score` and reduce aggression when it spikes.
- Required proxy or simplification:
  because we do not have exchange-level routing, use rolling intraday windows over trades and book state.
- Runtime / state caveat:
  must stay O(1) or small rolling-window update; do not require regressions or cross-exchange panels.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  a `danger-state gate` for `VEV_5200+` and maybe `5300`, triggered by concentrated one-sided flow plus widening spread or weak depth.
- Failure mode addressed:
  continuing to quote or aggress in states where the book is matching badly and adverse selection is likely.
- Validation implication:
  any such gate should be tested against markout and fill-quality deterioration, not only PnL.

## Do Not Overuse

- Do not interpret this as proof that every one-sided flow event is bad.
- Do not turn `flow instability` into a giant composite feature bucket with too many ingredients to debug.
- Do not use it as a universal rule for all strikes without role-aware filtering.

## Risks And Limitations

- The paper's institutional setting is richer than Prosperity.
- Our proxies may confound toxicity with simple illiquidity unless validated carefully.
- The main transfer is the state-framing, not the exact coefficients.

## Action Classification

- Classification: `new candidate`
- Why:
  it directly supports a practical `danger-state / no-trade` family of strategy rules that the EDA already hinted at.

## Strategy Hooks

- `flow_instability_score` as a defensive gate for `VEV_5200+`
- combine with `Mark 22` seller-state and spread/depth deterioration
- use as quote suppression and size reduction, not naked alpha

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this is one of the strongest papers in the `round_4` raw-derived core for execution/risk posture.
