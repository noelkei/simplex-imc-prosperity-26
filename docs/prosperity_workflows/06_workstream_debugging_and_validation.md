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

## Platform-first ranking

When platform artifacts exist, rank candidates by the platform JSON `profit`.
Use the final per-product rows in `activitiesLog` for product attribution.
Treat `graphLog`, trade-history reconstruction, and local replay as audit or
sanity signals unless a run summary explicitly labels them as a proxy.

Every validation summary that compares performance must state:

- PnL source: `real platform PnL | calibrated proxy | weak proxy`
- proxy confidence when applicable: `high | medium | low`
- current champion, if one exists
- challenger under review
- decision versus champion: `promote | backup | fallback | reject | rerun`

Proxy PnL is only for upload priority, early filtering, or debugging. It must
not be presented as real PnL, and it must not drive final promotion unless an
explicit deadline deferral is recorded.

## Lightweight proxy calibration

Before using a proxy to rank candidates, check whether comparable platform
`.json`, `.log`, or run summaries already exist for the round. If none exist,
the proxy is `weak`.

When platform evidence exists, keep calibration heuristic and practical:

- Note whether replay or another proxy has been directionally useful or
  misleading for similar bots.
- Identify which product layer drove real PnL.
- Check whether final inventory, matched quantity, spread capture, or product
  split explains the real ranking better than total replay PnL.
- Lower confidence when a proxy looked good locally but failed on platform.

Do not build a regression model, weighted scoring system, or precise PnL
prediction as part of this workflow.

## Champion and challenger decisions

After a candidate has the best comparable platform evidence, treat it as the
champion. New variants are challengers. A challenger becomes the primary
candidate only when it beats the champion on real platform PnL, or when it has
slightly lower PnL but a clearly material robustness improvement. If the
robustness improvement is small, keep the higher-PnL champion.

Classify serious candidates as:

- `primary`: best upload candidate.
- `backup`: close challenger, same family or slightly safer.
- `fallback`: simpler or lower-risk, but lower PnL.
- `reject`: not worth uploading.

## Promotion tradeoff checklist

Before final upload or primary promotion, compare the champion and challenger
using the fields that are available:

- total PnL
- product PnL split
- final inventory
- max drawdown
- max absolute position
- own trade count and matched quantity
- average buy/sell and gross spread capture
- whether improvement comes from realized trade quality or final inventory mark

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
- PnL source and proxy confidence when applicable
- champion/challenger decision and candidate class
- explicit decision: continue, promote, debug, discard, revise spec, rerun, or stop
- next action

Promotion does not mean the strategy is correct. It means the candidate is the best supported option by available evidence.

## Run comparability

Before using a run to compare, promote, debug, or discard a candidate, record:

- whether it is comparable to the baseline or prior run: `yes`, `no`, or `unclear`
- linked bot path and reviewed spec
- data source, run id, and raw artifact if available
- known differences in bot version, spec version, data, or platform conditions
- provenance caveat if exact `.py`, platform `.json`, and platform `.log` are not saved together
- the decision: continue, promote, debug, discard, revise spec, rerun, or stop

Non-comparable runs can still support debugging, but they should not drive promotion unless the caveat is explicit. Update `_index.md` with the run reference, comparability, decision, and one-line note after meaningful runs.

## Post-Run Research Memory

After serious platform or platform-style runs, fill the `Post-Run Research`
section in the run summary. Use it to capture reusable learning, not every
metric: failure-driven analysis, edge decomposition, and lightweight
counterfactuals.

Update `rounds/round_X/workspace/post_run_research_memory.md` only when the run
changes reusable knowledge, such as champion choice, a failure pattern, an edge
explanation, a counterfactual worth testing, or negative evidence. If the run
teaches nothing new, mark `Memory update: no change` in the run summary.

Every aggregate memory insight must link back to a per-run summary or raw
artifact. Treat the memory as evidence input for later phases, not as official
Prosperity rules.

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
