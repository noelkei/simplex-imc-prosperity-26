# Workstream: Round Preparation

Round preparation extracts new official facts and prepares the repo for EDA, strategy, implementation, and validation work.

## Inputs

- New Prosperity round material captured in the repository's factual source area.
- Existing wiki structure and future-round guidance.
- Platform or round docs only when they are part of the accepted factual source set for this repo.

## Good outputs

- A round document with products, limits, challenge names, algorithmic facts, manual facts, and source caveats.
- Clear separation between algorithmic and manual mechanics.
- A short prep note for downstream contributors: available products, limits, data artifacts, and unresolved questions.
- Links to the wiki pages that define shared API, trading, runtime, and platform behavior.

## Safe practice

- Extract facts only from accepted factual sources.
- Do not convert product hints into strategy advice.
- Do not mix manual-only mechanics into bot implementation requirements.
- Keep new round facts out of reusable workflow docs unless they are examples of process.
- If a round appears to change the API contract, document the exact source language and caveat before implementation depends on it.

## Ingestion quality checklist

Before ingestion is marked complete:

- Official round wiki link is present.
- Accepted factual sources were reviewed.
- Algorithmic products, symbols, and position limits are explicit or marked unknown.
- Manual-only mechanics are separated from bot implementation requirements.
- Round-specific mechanics are separated from shared API and trading facts.
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
- Source caveats.
- Downstream-impacting unknowns and next actions.
- Downstream actions for EDA, strategy, implementation, and validation.
