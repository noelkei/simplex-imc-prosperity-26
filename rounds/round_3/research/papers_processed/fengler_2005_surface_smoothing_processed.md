# Processed Paper Summary: Fengler (2005)

## Status

draft

## Paper Metadata

- Paper ID: `fengler_2005_surface_smoothing`
- Title: `Arbitrage-free smoothing of the implied volatility surface`
- Source / venue: `SFB 649 Discussion Paper 2005-019`
- Authors: `Matthias R. Fengler`
- Year: `2005`
- Raw file: [`../papers_raw/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf`](../papers_raw/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.pdf)
- Markdown file: [`../papers_md/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.md`](../papers_md/fengler_2005_arbitrage_free_smoothing_of_the_implied_volatility_surface.md)
- Link: <https://edoc.hu-berlin.de/bitstreams/4af0fb58-fda0-4e91-8fb2-fa451714a275/download>

## Core Claim

Option surfaces should be fit in call-price space under explicit no-arbitrage
shape constraints rather than smoothed freely in implied-volatility space. For
Round 3, the high-ROI takeaway is the constraint set itself: monotone
decreasing call prices by strike, convexity across strike, and basic price
bounds.

## Assumptions

- Round 3 voucher family is close enough to a single-expiry call strip that the
  single-maturity shape constraints are the useful part of the paper.
- We do not need the full spline/QP machinery to get most of the ROI.
- Surface guardrails are valuable as sanity filters even when the actual alpha
  comes from residual reversion.

## Problem Addressed for Round 3

- We need to formalize how the almost-always-monotone and almost-always-convex
  voucher surface should be used in strategy and spec work.
- We need a principled way to reject or clamp fair values that violate obvious
  cross-strike structure.
- We need to know whether surface shape should be a signal, a guardrail, or both.

## What This Paper Gives Us

- Formula / approximation:
  no-arbitrage conditions in call-price space:
  decreasing in strike, convex in strike, and bounded between intrinsic-style
  lower bounds and simple upper bounds.
- Constraints / checks:
  these shape restrictions are the paper's most directly usable output for a
  small single-expiry option family.
- Point of view:
  fit or sanity-check in price space with explicit structural constraints, not
  by trusting a noisy unconstrained curve.
- Simplification:
  use monotonicity, convexity, and basic price bounds as online validation /
  clamp rules without implementing the full spline optimization.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| voucher surface is almost always monotone and convex in EDA | strongest direct match | high | EDA evidence is current-round specific; the paper gives the theory behind it |
| residual pricing across strikes needs guardrails | supports turning surface structure into explicit checks | high | paper is broader than the round's single-expiry need |
| `VEV_5000` to `VEV_5300` are first-wave active scope | supports rejecting cross-strike inconsistencies among the active set | medium/high | only helpful when multiple strikes are quoted clearly enough |
| fitted fair-value curves may mis-rank wide-spread strikes | supports clamp logic before acting on noisy cross-strike dislocations | medium/high | guardrails are not alpha by themselves |

## Round 3 Mapping

- Treat the active voucher family as a small single-expiry call strip and apply
  strike-shape checks to observed mids and any fitted fair vector.
- Use monotonicity and convexity checks as residual sanity filters for
  `VEV_5000` to `VEV_5300`.
- Use simple price bounds to suppress obviously invalid fair values, especially
  when wide-spread names like `VEV_5400` / `VEV_5500` produce noisy books.
- Keep calendar-arbitrage material as secondary background only; the live round
  has one current TTE.

## Minimal Usable Adaptation

- Online-usable adaptation:
  before acting on a voucher residual, check whether the local cross-strike
  surface around that strike remains monotone and convex; if not, either clamp
  the fitted fair or require a larger edge before trading.
- Required proxy or simplification:
  use neighboring strikes and linear interpolation tests instead of a full
  spline or quadratic program.
- Runtime / state caveat:
  this should stay a light structural filter, not a large online optimization
  routine.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  residual-based voucher strategies should carry a `surface guardrail` block in
  the feature contract and execution logic.
- Failure mode addressed:
  reduces the chance that the bot trades against noisy or internally
  inconsistent cross-strike books as if they were clean mispricings.
- Validation implication:
  compare raw residual trades against residuals gated by monotonicity/convexity
  checks and see whether the guardrails reduce bad fills or unstable PnL.

## Do Not Overuse

- Do not implement the paper's full arbitrage-free smoothing engine unless later
  validation proves that a simple clamp is insufficient.
- Do not confuse shape-consistency with alpha; the surface can be arbitrage-free
  and still offer no trade.
- Do not let the guardrail suppress every trade in slightly noisy books unless
  that actually improves net performance.

## Risks And Limitations

- The paper targets a full implied-volatility surface and local-volatility
  workflow, which is much heavier than Prosperity needs.
- Some Round 3 books may be too sparse for clean local convexity checks at every
  timestamp.
- Overly rigid guardrails could block good trades in temporarily noisy but still
  profitable books.

## Action Classification

- Classification: `validation check`
- Why:
  this paper mostly upgrades strategy and spec quality by formalizing structural
  guardrails rather than creating a new standalone candidate.

## Strategy Hooks

- Add monotonicity and convexity checks to voucher residual strategy specs.
- Clamp or downweight fitted fair values that violate neighboring-strike shape
  constraints.
- Test whether edge thresholds should be wider when the observed surface locally
  breaks expected shape.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
