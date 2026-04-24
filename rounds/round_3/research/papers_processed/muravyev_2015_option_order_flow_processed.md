# Processed Paper Summary: Muravyev (2015)

## Status

draft

## Paper Metadata

- Paper ID: `muravyev_2015_option_order_flow`
- Title: `Order Flow and Expected Option Returns`
- Source / venue: `Journal of Finance-style manuscript` / SSRN working-paper distribution
- Authors: `Dmitriy Muravyev`
- Year: `2015`
- Raw file: [`../papers_raw/muravyev_2015_order_flow_and_expected_option_returns.pdf`](../papers_raw/muravyev_2015_order_flow_and_expected_option_returns.pdf)
- Markdown file: [`../papers_md/muravyev_2015_order_flow_and_expected_option_returns.md`](../papers_md/muravyev_2015_order_flow_and_expected_option_returns.md)
- Link: <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1963865>

## Core Claim

Option order flow contains economically meaningful information because market
makers absorb inventory shocks and reprice risk. The paper's main value for
Round 3 is not a literal replication of its regressions, but the lens that
option imbalance is best treated as an inventory-pressure signal and a return
modifier, not as a clean standalone alpha.

## Assumptions

- Prosperity top-of-book imbalance is only a proxy for the signed option-trade
  flow studied in the paper.
- Voucher symbols are correlated enough that family-level inventory pressure can
  matter more than isolated per-symbol imbalance.
- We care more about simple online interpretation than about reproducing the
  paper's identification design.

## Problem Addressed for Round 3

- We need to decide how much trust to place in `imbalance_1`, which EDA ranked
  as modest but nonzero.
- We need a principled reason not to overpromote imbalance beyond the residual /
  pricing signals already favored by Understanding.
- We need guidance on whether cross-voucher or family-level imbalance may be
  more informative than a single-symbol view.

## What This Paper Gives Us

- Formula / approximation:
  symbol-level and market-wide order-imbalance definitions, plus a decomposition
  viewpoint that separates information effects from inventory effects.
- Constraints / checks:
  the paper argues that portfolio-level dealer inventory matters, so imbalance
  interpretation should not stop at one contract.
- Point of view:
  option order flow is often inventory pressure first and pure directional alpha
  second.
- Simplification:
  treat imbalance as a secondary modifier, confirmation filter, or passive-quote
  caution signal rather than a primary strategy backbone.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `imbalance_1` is promoted only as a modest aid | gives a strong interpretation frame for that exact decision | high | Prosperity imbalance is a proxy, not the paper's exact signed-trade metric |
| voucher family is correlated despite separate limits | supports looking at family-level pressure, not only symbol-level imbalance | medium/high | we do not have a true market-wide options tape |
| wide-spread option quotes face adverse-selection risk | supports using imbalance as a passive-quote caution signal | medium | paper is broader than wide-spread single-book execution |
| delayed underlying-follow is rejected | helps keep imbalance usage focused on inventory / flow, not stale-underlying chasing | medium | not a direct result of the paper |

## Round 3 Mapping

- Keep `imbalance_1` in the feature contract, but only as an overlay on the
  residual / fair-value framework already promoted by Understanding.
- For `VEV_5000` to `VEV_5300`, compare symbol-level imbalance against a simple
  family-level aggregate imbalance across active vouchers.
- Use imbalance to lean or de-risk passive quotes in `VEV_5400` / `VEV_5500`
  instead of asking it to carry the entire signal stack.
- Avoid applying this logic to `VEV_6000` / `VEV_6500`, where floor behavior
  overwhelms dynamic flow interpretation in the sample.

## Minimal Usable Adaptation

- Online-usable adaptation:
  only strengthen a residual-reversion entry when the residual signal and the
  imbalance proxy agree, and soften passive quotes when imbalance implies
  adverse selection.
- Required proxy or simplification:
  use existing top-of-book `imbalance_1` and optionally a light family-average
  imbalance across `VEV_5000` to `VEV_5300`; do not recreate the paper's trade
  classification or IV regressions.
- Runtime / state caveat:
  this is a small quote or threshold adjustment, not a standalone prediction
  engine.
- Implementability: `variant-only`

## Strategy Implications

- Candidate or execution idea:
  residual-based voucher candidates can add an imbalance-confirmation filter or
  fair-value nudge instead of promoting imbalance to first-class alpha.
- Failure mode addressed:
  helps avoid buying into residual mean reversion when the live book is leaning
  hard the other way.
- Validation implication:
  test symbol-only imbalance versus family-average imbalance and verify that the
  modifier improves fills / markouts rather than just increasing churn.

## Do Not Overuse

- Do not treat imbalance as a standalone predictive engine just because the
  paper finds strong return predictability in real options markets.
- Do not copy the paper's trade-flow definitions, cross-exchange decomposition,
  or IV design into a Prosperity bot.
- Do not let imbalance override stronger current-round evidence from intrinsic /
  extrinsic residual structure.

## Risks And Limitations

- The paper studies real listed options with richer trade data and multiple
  exchanges; Prosperity gives us a much thinner proxy.
- Market-wide option-flow insights may compress poorly into only ten vouchers
  and one synthetic exchange.
- The paper supports interpretation more than it provides a ready-made formula.

## Action Classification

- Classification: `variant`
- Why:
  this paper most naturally strengthens an existing residual candidate with an
  inventory / flow overlay rather than creating a clean standalone candidate.

## Strategy Hooks

- Use `imbalance_1` as confirmation for residual-reversion entries, not as the
  entry trigger by itself.
- Build one simple family-level imbalance metric for the active voucher subset
  and compare it against per-symbol imbalance.
- Widen passive quotes or reduce size when imbalance signals adverse fill risk.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
