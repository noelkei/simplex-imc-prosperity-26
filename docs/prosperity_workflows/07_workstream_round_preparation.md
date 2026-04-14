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

## Handoff checklist

- Factual source files reviewed.
- New or updated round doc path.
- Product and position-limit table status.
- Algorithmic/manual separation status.
- Source caveats.
- Downstream actions for EDA, strategy, implementation, and validation.
