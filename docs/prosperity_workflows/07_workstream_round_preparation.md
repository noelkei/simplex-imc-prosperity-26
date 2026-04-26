# Workstream: Round Preparation

Round preparation extracts new official facts and prepares the repo for EDA, strategy, implementation, and validation work.

## Inputs

- New Prosperity round material captured in the repository's factual source area.
- Existing wiki structure and future-round guidance.
- Prior-round closeout artifacts only when the new round plausibly continues a
  prior market or product context.
- Platform or round docs only when they are part of the accepted factual source set for this repo.

## Good outputs

- A round document with products, limits, challenge names, algorithmic facts, manual facts, and source caveats.
- Clear separation between algorithmic and manual mechanics.
- A compact Round Mechanics Delta: products/limits, changed Trader/API mechanics, data/schema changes, manual-only mechanics, and prior-round assumptions at risk.
- A `Prior-Round Compatibility Gate` result when prior-round evidence may be
  relevant.
- A compact prior-round intake note when compatibility is not `not compatible`.
- A short prep note for downstream contributors: available products, limits, data artifacts, and unresolved questions.
- Links to the wiki pages that define shared API, trading, runtime, and platform behavior.

## Safe practice

- Extract facts only from accepted factual sources.
- Do not convert product hints into strategy advice.
- Do not mix manual-only mechanics into bot implementation requirements.
- Keep new round facts out of reusable workflow docs unless they are examples of process.
- If a round appears to change the API contract, document the exact source language and caveat before implementation depends on it.
- Do not inherit prior-round strategy conclusions, product roles, or anti-patterns
  by default. First classify the compatibility explicitly.

## Prior-Round Compatibility Gate

Run this gate whenever the team is tempted to reuse prior-round evidence.

Check:

- Do the rounds share the same or materially overlapping products?
- Do they share the same market mechanics or only superficial naming overlap?
- Do they expose the same online fields or the same type of state?
- Do they pose the same strategy problem, or only a related one?
- Would prior-round evidence change EDA/understanding questions if reused?

Classify the result as:

- `compatible`: principles, negative evidence, and test backlog may be reused,
  still labeled as prior-round evidence
- `partially compatible`: reuse only abstract framing, hypotheses, and
  anti-patterns; revalidate strategy conclusions from scratch
- `not compatible`: do not reuse strategy conclusions; keep only generic
  process heuristics

When compatibility is not `not compatible`, write a compact prior-round intake:

- prior rounds checked
- compatibility verdict
- products/mechanics/fields compared
- validated principles worth carrying forward
- untested hypotheses worth rechecking
- anti-patterns that should not be repeated by default
- assumptions that must be revalidated immediately

## Ingestion quality checklist

Before ingestion is marked complete:

- Official round wiki link is present.
- Accepted factual sources were reviewed.
- Algorithmic products, symbols, and position limits are explicit or marked unknown.
- Manual-only mechanics are separated from bot implementation requirements.
- Round-specific mechanics are separated from shared API and trading facts.
- New or changed Trader/API mechanics are recorded as implement / exclude / not applicable / blocker candidates for later spec work.
- Prior-round assumptions at risk are listed for EDA or understanding.
- Prior-round compatibility is recorded when prior-round reuse is plausible.
- Source caveats and conflicts are recorded.
- Available and missing data artifacts are noted.
- Unknowns that may affect EDA, strategy, or implementation are separated from facts and have a next action.
- No facts were inferred from bots, performances, memory, or playbook heuristics.

Ingestion cannot be `COMPLETED` unless each material unknown has a clarification path, targeted EDA action, or explicit deadline-risk deferral. These unknowns should seed the first EDA questions and the understanding summary.

## Handoff checklist

- Factual source files reviewed.
- New or updated round doc path.
- Product and position-limit table status.
- Algorithmic/manual separation status.
- Prior-round compatibility verdict, if checked.
- Prior-round intake note, if any.
- Source caveats.
- Downstream-impacting unknowns and next actions.
- Downstream actions for EDA, strategy, implementation, and validation.
