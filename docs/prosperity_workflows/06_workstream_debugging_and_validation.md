# Workstream: Debugging and Validation

Debugging and validation determine whether a contribution behaves correctly and whether the evidence supports the next step.

## Inputs

- Wiki facts for API shape, order signs, position limits, matching behavior, runtime, sample data, and logs.
- Run logs, local test output, sample-data results, or platform feedback.
- Implementation diffs and the reviewed strategy spec under review.
- The linked performance run or validation artifact that exposed the issue, when available.
- Playbook heuristics for common failure patterns and iteration habits.

## Validate factual constraints

Check whether the work:

- Returns the expected `Trader.run()` shape.
- Passes the contract smoke check in `docs/templates/trader_production_template.md`.
- Uses product symbols, datamodel fields, and order signs consistently with the wiki.
- Keeps aggregate buy and sell orders inside position-limit capacity.
- Handles `traderData` size and serialization assumptions safely.
- Avoids unsupported imports and excessive runtime cost.
- Separates algorithmic and manual challenge mechanics.

## Validate strategy behavior

Check whether the work:

- Matches the documented strategy hypothesis.
- Matches the linked reviewed strategy spec.
- Uses EDA evidence or logs consistently.
- Manages inventory in the way the strategy claimed.
- Fails gracefully when order books are empty or signals are unavailable.
- Produces interpretable logs or artifacts for follow-up.

## Promotion criteria

A bot candidate can be promoted only when there is an evidence summary that includes:

- run summary under `rounds/round_X/performances/<member>/canonical/`
- linked reviewed strategy spec
- linked bot path
- contract readiness or smoke-check status
- contract and rule checks
- one meaningful run or validation summary
- runtime, rejection, error, and position-limit concerns
- interpretation limits
- explicit decision: continue, promote, debug, discard, revise spec, rerun, or stop
- next action

Promotion does not mean the strategy is correct. It means the candidate is the best supported option by available evidence.

## Run comparability

Before using a run to compare, promote, debug, or discard a candidate, record:

- whether it is comparable to the baseline or prior run: `yes`, `no`, or `unclear`
- linked bot path and reviewed spec
- data source, run id, and raw artifact if available
- known differences in bot version, spec version, data, or platform conditions
- the decision: continue, promote, debug, discard, revise spec, rerun, or stop

Non-comparable runs can still support debugging, but they should not drive promotion unless the caveat is explicit. Update `_index.md` with the run reference, comparability, decision, and one-line note after meaningful runs.

## Report failures clearly

Every debugging artifact must include:

- linked strategy spec
- linked performance run or validation artifact, normally from `rounds/round_X/performances/<member>/canonical/`
- reproduction steps
- expected behavior
- observed behavior
- issue classification
- next action

Separate issues into:

- Rule or contract failure: conflicts with wiki facts.
- Implementation bug: code does not do what the strategy or task described.
- Data/EDA gap: more data, metrics, or interpretation is needed before deciding.
- Heuristic weakness: the approach is allowed but likely fragile, overfit, slow, or hard to debug.
- Execution tuning issue: behavior is valid but likely needs parameter, sizing, or quoting adjustment.
- Evidence gap: more data, logging, or reproduction is needed.

## Reroute rules

- Rule or contract failure: fix implementation or revisit ingestion if the documented fact is unclear.
- Implementation bug: fix narrowly against the reviewed spec.
- Data/EDA gap: return to targeted EDA before changing strategy behavior.
- Heuristic weakness: return to strategy generation or strategy specification.
- Execution tuning issue: adjust only low-risk parameters unless the spec needs review.
- Evidence gap: collect a clearer run, log, or reproduction before deciding.

## Handoff checklist

- Artifact reviewed: file, run, log, sample day, or command.
- Linked strategy spec.
- Linked performance run or validation artifact.
- Pass/fail summary.
- Expected vs observed behavior.
- Concrete failures with source category.
- Reproduction steps.
- Suggested next action: fix code, revise strategy, run more EDA, or update documentation.
