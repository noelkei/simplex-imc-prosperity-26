# Processed Paper Summary: Garcia-Ares (2023/2025)

## Status

draft

## Paper Metadata

- Paper ID: `garcia_ares_2023_expiration_days`
- Title: `Equity Option Return Predictability and Expiration Days`
- Source / venue: SSRN working paper
- Authors: `Pedro A. Garcia-Ares`
- Year: `2023` first version, `2025` current version in raw PDF
- Raw file: [`../papers_raw/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf`](../papers_raw/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.pdf)
- Markdown file: [`../papers_md/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.md`](../papers_md/garcia_ares_2023_equity_option_return_predictability_and_expiration_days.md)
- Link: <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4595840>

## Core Claim

Much of the return behavior usually attributed to generic option predictability
is actually concentrated in a short expiration-window regime driven by rolling
activity, intermediary frictions, and order imbalance. For Round 3, the main
value is not a parameter transfer but a strong warning that live `TTE=5d` may
behave meaningfully differently from the `6d-8d` history used in EDA.

## Assumptions

- Prosperity vouchers can enter an expiry-sensitive regime even though their
  mechanics are not identical to listed monthly equity options.
- The live Round 3 day is close enough to expiry that regime effects matter more
  than long-horizon average behavior.
- We care more about risk framing and validation posture than about reproducing
  the paper's delta-hedged return calculations.

## Problem Addressed for Round 3

- We need to decide how much confidence to place in residual reversion metrics
  measured at `TTE=6d-8d` when the live round runs at `TTE=5d`.
- We need to know whether near-expiry should change holding assumptions,
  thresholds, or risk appetite in voucher strategies.
- We need a principled reason to treat imbalance and order pressure differently
  near expiry than away from it.

## What This Paper Gives Us

- Formula / approximation:
  no compact live pricing formula, but a useful return-decomposition frame and a
  strong empirical result that a short expiry-adjacent window dominates much of
  the average option-return effect.
- Constraints / checks:
  do not assume that full-period average option behavior is stable once expiry
  pressure enters the book.
- Point of view:
  near-expiry option behavior is often a flow- and intermediary-driven regime,
  not just the same signal with slightly faster theta.
- Simplification:
  treat `TTE=5d` as a distinct caution regime and validate faster signal decay,
  shorter holding expectations, and stricter entries instead of extrapolating
  historical half-lives mechanically.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| live round is `TTE=5d` while history is `6d-8d` | strongest direct match | high | the paper studies listed monthly U.S. equity options, not Prosperity vouchers |
| `extrinsic_dev_day` reversion is promoted from historical data | supports treating live decay speed as uncertain and possibly sharper | high | does not tell us the exact live half-life |
| imbalance is only a modest promoted signal | supports using flow pressure as a regime modifier near expiry | medium/high | our imbalance proxy is thinner than the paper's signed-volume data |
| `VEV_5400` / `VEV_5500` are execution-sensitive | suggests expiry pressure may worsen execution quality and adverse selection | medium | not a direct paper result |

## Round 3 Mapping

- Use this paper as a regime-warning layer on top of the main voucher residual
  strategies, especially `VEV_5000` to `VEV_5300`.
- Shorten expected holding assumptions and consider more conservative exits for
  live-round voucher positions.
- Raise evidence requirements for using historical residual half-life estimates
  directly in specs.
- Use imbalance and order-pressure overlays more defensively near expiry instead
  of treating them as generic alpha enhancers.

## Minimal Usable Adaptation

- Online-usable adaptation:
  do not add new live features from this paper; instead tighten residual-entry
  thresholds, decay memory faster, and flatten inventory sooner in the live
  `TTE=5d` round than the historical analysis alone would suggest.
- Required proxy or simplification:
  represent the entire live day as an expiry-sensitive regime with stricter
  thresholds rather than trying to detect sub-regimes from sparse flow data.
- Runtime / state caveat:
  this is mainly a risk/validation overlay and should not become a pseudo-signal
  with many extra knobs.
- Implementability: `validation-only`

## Strategy Implications

- Candidate or execution idea:
  any first-wave voucher strategy should explicitly include a `TTE=5d caution`
  clause in its spec, even if the core alpha remains residual reversion.
- Failure mode addressed:
  prevents the team from overtrusting historical reversion speeds and holding
  periods in the only live day that is out of sample.
- Validation implication:
  compare a baseline residual strategy against a stricter expiry-aware variant
  before assuming the historical calibration is portable.

## Do Not Overuse

- Do not import the paper's exact expiration-Friday / Monday calendar logic into
  Prosperity.
- Do not treat this as proof that vouchers must crash or reverse on any fixed
  intraday schedule.
- Do not replace current-round signals with a vague "expiry effect" story.

## Risks And Limitations

- The market structure is much richer than Prosperity and uses real signed
  option-volume data.
- The paper gives regime evidence, not a compact pricing or quoting formula.
- Overreacting to expiry caution could make the bot too timid exactly where the
  round's best opportunity may still exist.

## Action Classification

- Classification: `validation check`
- Why:
  this paper should change how Strategy and Spec validate live-round assumptions
  more than it should create a standalone candidate.

## Strategy Hooks

- Add an explicit `TTE=5d regime caution` section to voucher strategy specs.
- Validate a stricter-threshold / faster-decay variant against the baseline
  residual strategy.
- Treat expiry-sensitive execution degradation as a live validation question,
  not as something settled by historical `6d-8d` evidence.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
