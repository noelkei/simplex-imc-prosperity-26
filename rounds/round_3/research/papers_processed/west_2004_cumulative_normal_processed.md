# Processed Paper Summary: West (2004)

## Status

draft

## Paper Metadata

- Paper ID: `west_2004_cumulative_normal`
- Title: `Better Approximations to Cumulative Normal Functions`
- Source / venue: practitioner note / technical article
- Authors: `Graeme West`
- Year: `2004`
- Raw file: [`../papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf`](../papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf)
- Markdown file: [`../papers_md/west_2004_better_approximations_to_cumulative_normal_functions.md`](../papers_md/west_2004_better_approximations_to_cumulative_normal_functions.md)
- Link: [`../papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf`](../papers_raw/west_2004_better_approximations_to_cumulative_normal_functions.pdf)

## Core Claim

If a pricing stack depends on the normal CDF, the numerical approximation is
part of the model and low-quality implementations can create surprisingly bad
downstream behavior. For Round 3, this is an implementation-quality paper: it
supports doing `norm_cdf` carefully once so that a Bachelier-based voucher model
does not rest on a shaky math helper.

## Assumptions

- We are likely to use a normal-model pricing backbone or at least a benchmark
  that depends on `N(x)`.
- A hand-coded `norm_cdf` is allowed and preferable to importing unavailable
  scientific libraries.
- Numerical stability matters even in a simple bot because fair-value ranking
  errors can change quote placement.

## Problem Addressed for Round 3

- We need a stable `norm_cdf` implementation if we use Bachelier pricing online.
- We need to avoid quietly accepting a low-quality helper that can distort the
  relative fair values of nearby strikes.
- We need to decide whether this belongs in Strategy, Spec, or only later in
  implementation validation.

## What This Paper Gives Us

- Formula / approximation:
  justification for using a high-quality rational approximation to the univariate
  normal CDF instead of a looser textbook shortcut.
- Constraints / checks:
  numerical quality of helper functions is part of model correctness, not a
  cosmetic detail.
- Point of view:
  if the model depends on `N(x)`, then the chosen approximation deserves the
  same care as any other modeling assumption.
- Simplification:
  implement one robust univariate `norm_cdf` and stop there; the paper's
  bivariate and trivariate material is not needed for Round 3.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| Choi/Bachelier fair-value candidate needs `N(x)` | strongest direct match | high | only matters if Strategy actually adopts a normal-model fair backbone |
| no external scientific libraries are allowed in the bot | directly supports a local helper implementation | high | paper is implementation-focused, not strategic |
| close strike ranking matters for active vouchers | better CDF quality can reduce avoidable fair-value noise | medium/high | practical gain may be small if thresholds are coarse |
| CRR remains a backup benchmark | helps keep model-comparison noise from coming from bad math utilities | medium | still secondary to picking the right model family |

## Round 3 Mapping

- Treat this paper as supporting infrastructure for any Choi-inspired option
  pricing path.
- Do not create a separate strategy candidate from it; fold it into spec or
  implementation-quality requirements when the fair model is chosen.
- Keep only the univariate normal-CDF part; ignore the bivariate / trivariate
  and exotic-option sections for this round.
- Use it to justify verifying the math helper before trusting subtle residual
  rankings across active voucher strikes.

## Minimal Usable Adaptation

- Online-usable adaptation:
  implement one robust hand-coded `norm_cdf` routine and use it consistently in
  any Bachelier-style pricing logic.
- Required proxy or simplification:
  choose a compact rational approximation with symmetry handling and reasonable
  tail behavior; no need to reproduce the whole paper's code ecosystem.
- Runtime / state caveat:
  this is utility-quality work, not a new signal, so keep it tiny and fully
  deterministic.
- Implementability: `implementable`

## Strategy Implications

- Candidate or execution idea:
  none directly; this belongs as a quality requirement under any candidate that
  depends on normal-model pricing.
- Failure mode addressed:
  avoids avoidable fair-value drift caused by a poor CDF helper rather than by
  true round economics.
- Validation implication:
  if Strategy adopts Bachelier-style pricing, Spec should explicitly call for a
  robust `norm_cdf` utility and not an ad hoc approximation chosen at random.

## Do Not Overuse

- Do not turn this into a paper-driven search for mathematical perfection.
- Do not import its bivariate or exotic-option cautionary material into a round
  that only needs univariate normal calls.
- Do not treat helper precision as a substitute for choosing the right fair
  model in the first place.

## Risks And Limitations

- The practical benefit may be modest if live quote thresholds are wide enough.
- This paper does not help with strategy direction unless normal-model pricing is
  already chosen.
- Overengineering the helper would be a bad use of time under deadline.

## Action Classification

- Classification: `validation check`
- Why:
  this paper is about implementation quality control for likely pricing logic,
  not about generating a new strategy family.

## Strategy Hooks

- If Strategy uses Bachelier, Spec should require a robust hand-coded `norm_cdf`
  rather than a casual approximation.
- Keep the CDF helper discussion attached to pricing-model choice, not as a
  separate strategy thread.
- Use this paper to justify a small math-utility review before implementation.

## Notes

- Strategy must later classify actual use as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- This paper is an idea source, not a source of official Prosperity mechanics.
