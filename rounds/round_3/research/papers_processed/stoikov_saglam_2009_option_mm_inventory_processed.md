# Processed Paper Summary: Stoikov and Saglam (2009)

## Status

draft

## Paper Metadata

- Paper ID: `stoikov_saglam_2009_option_mm_inventory`
- Title: `Option market making under inventory risk`
- Source / venue: SSRN working paper
- Authors: `Sasha Stoikov`, `Mehmet Saglam`
- Year: `2009`
- Raw file: [`../papers_raw/stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf`](../papers_raw/stoikov_saglam_2009_option_market_making_under_inventory_risk.pdf)
- Markdown file: [`../papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md`](../papers_md/stoikov_saglam_2009_option_market_making_under_inventory_risk.md)
- Link: <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1393818>

## Core Claim

Option market-makers should not manage risk only with hard position caps; they
should tilt quotes as inventory risk builds, and the relevant exposure is a mix
of net delta plus residual gamma / vega risk when hedging is incomplete. For
Round 3, the useful takeaway is the quoting logic and point of view, not the
full continuous-time control problem.

## Assumptions

- Prosperity bots do not have a separate hedge engine, so incomplete-market
  intuition is more relevant than the paper's fully hedgeable case.
- Voucher family risk can be approximated with strike / moneyness exposure
  weights instead of live Greeks.
- A simple quote-skew rule is more realistic than solving the paper's recursive
  dynamic program online.

## Problem Addressed for Round 3

- We need to manage inventory across ten correlated vouchers with independent
  position limits and no real-time Greek stack.
- We need a principled way to shift quotes when voucher inventory becomes too
  concentrated, especially near the active `VEV_5000` to `VEV_5300` region.
- We need something better than pure hard stops for inventory control.

## What This Paper Gives Us

- Formula / approximation:
  clipped linear quote-premium formulas and the general mean-variance objective
  that moves quotes away from spread-maximizing levels as inventory risk rises.
- Constraints / checks:
  if risk is perfectly hedgeable, quote skew should be small; if risk is not
  hedgeable, inventory should enter the quote itself.
- Point of view:
  inventory belongs in reservation-price or quote-skew logic, not only in
  separate "stop trading" gates.
- Simplification:
  replace explicit delta / gamma / vega control with per-symbol position
  penalties plus one aggregate voucher-exposure proxy weighted by strike or
  moneyness.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| multi-symbol inventory coupling is a key open risk | this is the strongest direct paper match in the batch | high | the full paper is more complex than a Prosperity bot should be |
| `VEV_5000` to `VEV_5300` are first-wave active scope | supports stronger skew where exposure is economically meaningful | high | weights still need a simple current-round proxy |
| TTE `5d` live regime may be sharper than history | paper's horizon-end steepening supports more aggressive flattening near the end | medium/high | paper is not calibrated to Prosperity TTE |
| `VEV_6000` / `VEV_6500` look like floor products | supports low exposure weights or exclusion from aggregate risk terms | medium | sample floor behavior is current-round evidence, not paper content |

## Round 3 Mapping

- Apply this paper to the voucher family only, not to the separate
  `HYDROGEL_PACK` branch.
- Keep the core residual / surface signal, but shift quotes or reservation
  prices by both per-symbol inventory and aggregate weighted voucher exposure.
- Weight `VEV_5000` to `VEV_5300` more heavily than `VEV_5400` / `VEV_5500`,
  and heavily deweight or exclude `VEV_6000` / `VEV_6500`.
- Use the TTE `5d` risk caveat to justify slightly faster flattening or wider
  entry thresholds than a purely static residual model would use.

## Minimal Usable Adaptation

- Online-usable adaptation:
  shift voucher fair values by
  `penalty_i = a * pos_i / limit_i + b * agg_weighted_exposure * weight_i`,
  then skew bids / asks away from building more of the same exposure.
- Required proxy or simplification:
  use strike or moneyness buckets as exposure weights, not explicit live
  Greeks, and keep one small inventory-memory state rather than a full dynamic
  recursion.
- Runtime / state caveat:
  this should stay as a small overlay on top of a pricing signal; otherwise the
  bot risks becoming an inventory controller with no alpha backbone.
- Implementability: `variant-only`

## Strategy Implications

- Candidate or execution idea:
  an inventory-aware variant of the main voucher residual candidate is worth
  prioritizing early, especially if first validation shows position pressure or
  sticky one-sided holdings.
- Failure mode addressed:
  reduces the risk that a good residual signal keeps adding into correlated
  voucher inventory until fills or markouts collapse.
- Validation implication:
  compare per-symbol-only penalties versus per-symbol plus family-exposure
  penalties and watch whether quote skew improves realized flattening without
  killing too much spread capture.

## Do Not Overuse

- Do not implement the paper's full recursive control, continuous hedging, or
  explicit gamma / vega machinery inside the first Prosperity bot.
- Do not assume the theoretical quote formulas are numerically optimal under
  discrete ticks and thin books.
- Do not let inventory overlays replace the underlying pricing / residual edge.

## Risks And Limitations

- The paper assumes richer market structure and more continuous control than we
  actually have.
- Exposure weights chosen from strike or moneyness will be heuristic rather than
  theoretically exact.
- Overweighting inventory penalties could suppress the very trades that create
  alpha in the active vouchers.

## Action Classification

- Classification: `variant`
- Why:
  the paper is best used to create an inventory-aware variant of a core voucher
  strategy, not as a standalone signal source.

## Strategy Hooks

- Add per-symbol inventory skew before hitting hard position blocks.
- Add a family-level weighted exposure term across active vouchers.
- Increase flattening pressure as the effective horizon shortens or when
  family exposure is one-sided.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
