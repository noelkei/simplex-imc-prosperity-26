# Processed Paper Summary: Cox, Ross, and Rubinstein (1979)

## Status

draft

## Paper Metadata

- Paper ID: `crr_1979_simplified_approach`
- Title: `Option Pricing: A Simplified Approach`
- Source / venue: `Journal of Financial Economics`
- Authors: `John C. Cox`, `Stephen A. Ross`, `Mark Rubinstein`
- Year: `1979`
- Raw file: [`../papers_raw/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf`](../papers_raw/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.pdf)
- Markdown file: [`../papers_md/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.md`](../papers_md/cox_ross_rubinstein_1979_option_pricing_a_simplified_approach.md)
- Link: <https://doi.org/10.1016/0304-405X(79)90015-1>

## Core Claim

Option values can be computed by no-arbitrage replication on a small discrete
tree, and that finite-step view already contains the core economics of option
pricing. For Round 3, the high-ROI use is not to replace the main pricing
backbone by default, but to provide a simple discrete benchmark and fallback
when we want to sanity-check Bachelier-style fair values across strikes.

## Assumptions

- A finite-step tree is cheap enough to use in research or even online if kept
  very small.
- We only need a short-dated European-style benchmark, not the paper's broader
  dividend / American-exercise machinery.
- A discrete no-arbitrage benchmark is more valuable as a cross-check than as a
  source of standalone alpha.

## Problem Addressed for Round 3

- We need a simple benchmark for whether Bachelier fair values are distorting
  ITM or OTM vouchers.
- We need an alternative pricing lens that fits a discrete, short-horizon, no-
  `scipy` environment.
- We need a way to compare model choice without jumping immediately to a heavy
  implied-volatility stack.

## What This Paper Gives Us

- Formula / approximation:
  one-period and multi-period binomial pricing with risk-neutral weights and
  backward induction.
- Constraints / checks:
  price should be consistent with discrete replication and risk-neutral
  valuation, not just with one closed-form model assumption.
- Point of view:
  a simple discrete tree is often enough to benchmark whether a fair-value model
  is directionally sane.
- Simplification:
  use a tiny tree with a small number of steps as a benchmark or fallback rather
  than building a calibration-heavy lattice engine.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| Choi/Bachelier is the main fair-value backbone candidate | gives a clean benchmark against model misspecification | high | not obviously superior to Bachelier as the default live model |
| `VEV_4000` / `VEV_4500` and `VEV_5400` / `VEV_5500` may behave differently by strike | discrete benchmark can highlight where one model may underfit tails | medium/high | still needs a volatility proxy to run |
| integer prices and no external libs | tree pricing is compatible with current runtime constraints | medium/high | too many steps would still be overkill |
| one live TTE regime | finite-step tree matches short horizon naturally | medium | not a direct answer to the `TTE=5d` regime shift question |

## Round 3 Mapping

- Use CRR primarily as a benchmark for active vouchers and for model-choice
  checks around the first-wave scope.
- Reopen it as a live alternative only if Bachelier-based residuals show
  systematic bias by strike or moneyness.
- Prefer it as a benchmark for `VEV_4000` / `VEV_4500` and the wider OTM names,
  where closed-form normal approximations may be less trustworthy.
- Keep the implementation lightweight, with one or two steps per day at most if
  used online at all.

## Minimal Usable Adaptation

- Online-usable adaptation:
  keep a very small CRR tree as an offline benchmark or emergency fallback fair
  model, not as the main first-wave live engine.
- Required proxy or simplification:
  share the same simple volatility proxy used by the Bachelier candidate so the
  model comparison is apples-to-apples.
- Runtime / state caveat:
  the tree should remain small and deterministic; otherwise it stops being a
  practical benchmark for a compact Trader.
- Implementability: `validation-only`

## Strategy Implications

- Candidate or execution idea:
  Strategy should record CRR as a benchmark / challenger fair model if the
  Bachelier baseline proves fragile in validation.
- Failure mode addressed:
  reduces the chance that the team mistakes one model family for a fact about
  the round.
- Validation implication:
  compare residual rankings and strike ordering under Bachelier versus a small
  CRR tree before locking the main fair-value spec.

## Do Not Overuse

- Do not escalate this into a large lattice-calibration project.
- Do not drag in dividends, American exercise, or historical side roads that do
  not map to Round 3.
- Do not switch to CRR by default unless it solves a real model-quality problem.

## Risks And Limitations

- The tree still needs a volatility input, so it does not remove calibration
  uncertainty.
- If the live bot already has a stable normal-model baseline, CRR may only add
  implementation complexity without edge.
- The paper is foundational but not specific to short-horizon Prosperity books.

## Action Classification

- Classification: `validation check`
- Why:
  this paper is most useful as a discrete benchmark and fallback, not as a
  primary strategy source.

## Strategy Hooks

- Benchmark Bachelier-based fair values against a tiny CRR tree before final
  strategy commitment.
- Use CRR disagreement as a reason to inspect strike-specific residual behavior.
- Keep CRR in reserve as a challenger fair model, not as mandatory first-wave
  complexity.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
