# Processed Paper Summary: Choi et al. (2022)

## Status

draft

## Paper Metadata

- Paper ID: `choi_2022_bachelier_guide`
- Title: `A Black-Scholes user's guide to the Bachelier model`
- Source / venue: `Journal of Futures Markets` / arXiv
- Authors: `Jaehyuk Choi`, `Minsuk Kwak`, `Chyng Wen Tee`, `Yumeng Wang`
- Year: `2022`
- Raw file: [`../papers_raw/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model/`](../papers_raw/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model/)
- Markdown file: [`../papers_md/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model.md`](../papers_md/choi_kwak_tee_wang_2022_black_scholes_users_guide_to_the_bachelier_model.md)
- Link: <https://arxiv.org/abs/2104.08686>

## Core Claim

The Bachelier / normal model is a practical closed-form alternative to
Black-Scholes when a desk needs a simple call-pricing backbone, especially for
short-dated or near-ATM contracts where a normal-volatility view is often good
enough. The paper's real value for Round 3 is not a full volatility stack, but
a compact fair-value kernel plus a few safe simplifications around ATM
inversion, Greeks, and BS-to-normal conversion.

## Assumptions

- `VELVETFRUIT_EXTRACT` mid can act as the live underlying anchor `S`.
- Voucher strikes behave like call-option strikes.
- A simple absolute-volatility proxy is acceptable; we do not need a full
  implied-volatility engine inside the bot.
- Round 3 only needs one short maturity regime, not a full term structure.

## Problem Addressed for Round 3

- We need a simple online fair-value baseline for `VEV_*` that can be computed
  inside a small Python `Trader` with no scientific libraries.
- We need a pricing anchor that sits above pure intrinsic value and below a full
  IV / surface-calibration stack.
- We need a better residual frame for `extrinsic_dev_day` than "option mid minus
  intrinsic" alone.

## What This Paper Gives Us

- Formula / approximation:
  Bachelier call price
  $$
  C_N(K) = (S-K)N(d) + \sigma_{abs}\sqrt{T}\,\phi(d),
  \qquad
  d = \frac{S-K}{\sigma_{abs}\sqrt{T}}
  $$
  plus ATM inversion and BS-to-normal conversion approximations.
- Constraints / checks:
  the paper makes clear that BS-equivalent volatility can become unreliable in
  extreme-strike regimes, which supports staying with a direct normal-model
  baseline rather than forcing a BS interpretation everywhere.
- Point of view:
  treat the normal model as a practical pricing kernel, not as a statement that
  the world is literally arithmetic Brownian motion.
- Simplification:
  we can use one lightweight normal-call fair and then let current-round EDA do
  the remaining work via residuals, surface checks, and execution filters.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| `VELVETFRUIT_EXTRACT` is the natural voucher anchor | direct fair-value input | high | the paper assumes a cleaner market than Prosperity |
| `extrinsic_dev_day` is the strongest promoted voucher signal | gives a better baseline residual frame than intrinsic-only | high | signal still needs current-round calibration |
| live round is TTE `5d` and history is `6d-8d` | short-dated model is a better fit than a heavy calibration stack | medium/high | paper is not specific to Prosperity's TTE gap |
| `VEV_6000` / `VEV_6500` behave like floor instruments | supports separating pricing kernel from round-specific floor heuristics | medium | the paper does not know about the observed `0.5` floor regime |

## Round 3 Mapping

- Use `VELVETFRUIT_EXTRACT` mid as `S` and voucher strike as `K`.
- Use the live Round 3 TTE assumption explicitly instead of carrying
  historical-day TTE blindly.
- Keep `VEV_5000` to `VEV_5300` as the highest-ROI first-wave scope for this
  fair-value backbone, because Understanding already promotes those strikes.
- Treat `VEV_4000` / `VEV_4500` as useful ITM structural anchors for validation
  and residual cross-checks.
- Keep the floor-like `VEV_6000` / `VEV_6500` outside the main Bachelier alpha
  scope; clamp them with round-specific logic if needed.

## Minimal Usable Adaptation

- Online-usable adaptation:
  compute a Bachelier-style fair per voucher, then trade residual mean
  reversion around that fair instead of around intrinsic value alone.
- Required proxy or simplification:
  estimate `sigma_abs` from recent `VELVETFRUIT_EXTRACT` move scale or from a
  stable per-day / per-TTE calibration, and implement `norm_cdf` with a small
  hand-coded approximation.
- Runtime / state caveat:
  keep prices integer-aware and avoid iterative IV solves or multi-model
  conversion loops.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  `Bachelier fair + extrinsic residual mean reversion` becomes a concrete first
  option candidate for `VEV_5000` to `VEV_5300`.
- Failure mode addressed:
  avoids relying on intrinsic-only residuals, which can mis-rank active strikes
  when time value matters.
- Validation implication:
  compare Bachelier-based residuals against intrinsic-only residuals and simple
  day baselines in replay / backtest before letting the model drive quotes.

## Do Not Overuse

- Do not build a full BS / displaced-BS / SABR stack just because the paper
  discusses those bridges.
- Do not treat BS-to-normal conversion as a required live component if one
  direct normal-volatility proxy is already stable enough.
- Do not let this paper override current-round evidence that the real alpha is
  in residual behavior and execution, not in theoretical pricing elegance.

## Risks And Limitations

- The paper is written for real-world derivatives markets, not Prosperity's
  discrete-tick simulator.
- We still need a robust online absolute-volatility proxy, which the paper does
  not hand to us for free.
- A good fair model does not solve wide-spread execution or family-level
  inventory by itself.

## Action Classification

- Classification: `new candidate`
- Why:
  this paper directly unlocks a concrete fair-value backbone that can sit under
  a first-wave Round 3 voucher strategy.

## Strategy Hooks

- Use Bachelier fair as the primary option-pricing backbone for first-wave
  voucher candidates.
- Measure residual mispricing against `fair - observed_mid`, not just against
  intrinsic value.
- Validate whether `VEV_4000` / `VEV_4500` residuals behave more cleanly than
  the near-ATM first-wave strikes when priced off the same kernel.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
