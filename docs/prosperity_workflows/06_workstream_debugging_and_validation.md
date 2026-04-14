# Workstream: Debugging and Validation

Debugging and validation determine whether a contribution behaves correctly and whether the evidence supports the next step.

## Inputs

- Wiki facts for API shape, order signs, position limits, matching behavior, runtime, sample data, and logs.
- Run logs, local test output, sample-data results, or platform feedback.
- Implementation diffs or strategy notes under review.
- Playbook heuristics for common failure patterns and iteration habits.

## Validate factual constraints

Check whether the work:

- Returns the expected `Trader.run()` shape.
- Uses product symbols, datamodel fields, and order signs consistently with the wiki.
- Keeps aggregate buy and sell orders inside position-limit capacity.
- Handles `traderData` size and serialization assumptions safely.
- Avoids unsupported imports and excessive runtime cost.
- Separates algorithmic and manual challenge mechanics.

## Validate strategy behavior

Check whether the work:

- Matches the documented strategy hypothesis.
- Uses EDA evidence or logs consistently.
- Manages inventory in the way the strategy claimed.
- Fails gracefully when order books are empty or signals are unavailable.
- Produces interpretable logs or artifacts for follow-up.

## Report failures clearly

Separate issues into:

- Rule or contract failure: conflicts with wiki facts.
- Implementation bug: code does not do what the strategy or task described.
- Heuristic weakness: the approach is allowed but likely fragile, overfit, slow, or hard to debug.
- Evidence gap: more data, logging, or reproduction is needed.

## Handoff checklist

- Artifact reviewed: file, run, log, sample day, or command.
- Pass/fail summary.
- Concrete failures with source category.
- Reproduction steps.
- Suggested next action: fix code, revise strategy, run more EDA, or update documentation.
