# Processed Paper Summary: Bergault et al. (2022)

## Status

draft

## Paper Metadata

- Paper ID: `bergault_2022_multi_asset_mm`
- Title: `Closed-form approximations in multi-asset market making`
- Source / venue: arXiv / preprint
- Authors: `Philippe Bergault`, `David Evangelista`, `Olivier Gueant`, `Douglas Vieira`
- Year: `2022`
- Raw file: [`../papers_raw/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making/`](../papers_raw/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making/)
- Markdown file: [`../papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md`](../papers_md/bergault_evangelista_gueant_vieira_2022_closed_form_approximations_in_multi_asset_market_making.md)
- Link: <https://arxiv.org/abs/1810.04383>

## Core Claim

In multi-asset market making, optimal quoting depends on portfolio inventory
rather than isolated per-symbol positions, and that coupling can be approximated
with closed-form inventory terms instead of solving a full high-dimensional
control problem. For Round 3, the important contribution is the portfolio view:
correlated voucher inventory should influence quote skew across the whole active
family, not only inside each `VEV_*` symbol separately.

## Assumptions

- Active vouchers share enough underlying-driven risk that a portfolio-style
  inventory term is directionally correct.
- We do not need the paper's matrix ODE machinery online to get most of the ROI.
- A low-dimensional exposure proxy is acceptable in place of a full covariance
  or Greeks stack.

## Problem Addressed for Round 3

- We need a better family-level inventory framework for ten related vouchers with
  separate position limits.
- We need to decide whether the per-symbol skew from `Stoikov-Saglam` should be
  upgraded into a more explicitly cross-voucher quote skew.
- We need a principled way to make holdings in one strike affect behavior in
  nearby strikes.

## What This Paper Gives Us

- Formula / approximation:
  a quadratic value-function approximation whose quote skew depends on
  inventory, covariance, and liquidity jointly rather than symbol by symbol.
- Constraints / checks:
  the relevant inventory penalty is naturally portfolio-shaped, so independent
  position controls are only part of the story.
- Point of view:
  quote shifts should respond to aggregate correlated exposure, not just whether
  one symbol is locally long or short.
- Simplification:
  collapse the portfolio term into one small active-voucher exposure metric or a
  tiny weighted matrix over `VEV_5000` to `VEV_5300` instead of a full
  covariance-control engine.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| multi-symbol inventory coupling is a key open risk | strongest direct match in Batch 3 | high | the paper is more general and heavier than a simple Trader needs |
| `VEV_5000` to `VEV_5300` are first-wave active scope | supports coupling the most economically relevant strikes first | high | exact weights still need a current-round heuristic |
| `VEV_4000` / `VEV_4500` are structural anchors | supports letting ITM holdings affect nearby-strike quoting | medium/high | these strikes may be too sparse to deserve equal weight |
| `VEV_6000` / `VEV_6500` are floor-like in sample | supports deweighting or excluding inactive tail strikes from the family exposure term | medium | floor behavior is current-round evidence, not paper content |

## Round 3 Mapping

- Apply this paper only to the voucher branch, not to `HYDROGEL_PACK`.
- Use it as a second-layer refinement on top of `Stoikov-Saglam`, not as a
  replacement for the simpler inventory overlay.
- Build a family exposure metric centered on `VEV_5000` to `VEV_5300`, with
  optional lighter weights for `VEV_4000` / `VEV_4500` and little to no weight
  on the floor-like `VEV_6000` / `VEV_6500`.
- Let exposure in one active strike softly move fair-value shifts or quoting
  thresholds in adjacent active strikes.

## Minimal Usable Adaptation

- Online-usable adaptation:
  augment the per-symbol inventory penalty with an aggregate active-voucher
  exposure term, such as a weighted sum over positions by strike distance or
  moneyness band.
- Required proxy or simplification:
  use a fixed hand-tuned weight vector or tiny active-subset coupling matrix
  instead of explicit covariance estimation and matrix square roots.
- Runtime / state caveat:
  keep the family term small enough that it nudges quoting behavior without
  washing out the main residual signal.
- Implementability: `variant-only`

## Strategy Implications

- Candidate or execution idea:
  if the first inventory-aware voucher candidate still gets trapped in
  correlated holdings, a `family-coupled inventory` variant becomes justified.
- Failure mode addressed:
  avoids the situation where the bot looks safe per symbol but is directionally
  overloaded across the whole active voucher strip.
- Validation implication:
  compare per-symbol-only skew against per-symbol plus family-coupled skew and
  watch whether the latter improves flattening, turnover quality, or risk usage.

## Do Not Overuse

- Do not implement the paper's full multi-asset control machinery inside the
  first bot.
- Do not infer a large covariance-estimation project from a round with one
  small option family and a short deadline.
- Do not let family-coupled skew dominate the actual mispricing signal.

## Risks And Limitations

- The paper is designed for richer multi-asset dealer settings than Prosperity.
- A poor weight scheme could add complexity without improving behavior.
- Correlated-inventory logic is only useful if live validation actually shows
  family-level crowding or position lock-in.

## Action Classification

- Classification: `variant`
- Why:
  this paper is best used as an escalation path if simple per-symbol inventory
  skew is not enough.

## Strategy Hooks

- Add a family-level active-voucher exposure term to later inventory-aware
  voucher variants.
- Keep the coupling limited to the active strikes instead of the whole 10-symbol
  family by default.
- Compare `per-symbol only` versus `per-symbol + family exposure` in strategy
  prioritization.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
