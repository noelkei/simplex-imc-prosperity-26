# Strategy Spec Template

Implementation must not start until this spec is reviewed. In fast mode, keep it short but do not omit signal, execution, risk, state, or validation checks.

## Spec Quality Checklist

- Candidate ID, priority, and evidence basis are linked from the shortlist.
- Signal or fair value logic is defined.
- Execution behavior says when to buy, sell, rest orders, or stay idle.
- Missing-data and missing-signal behavior is defined.
- Position limits and aggregate order capacity are considered.
- Parameters are visible and not hidden for code-time invention.
- State, runtime, imports, and `traderData` risks are considered.
- Expected failure cases are named.
- Validation checks are specific enough for testing.
- Assumptions are labeled and not presented as wiki facts.
- Reviewer, status, and date are filled, or deadline deferral is explicit.

## Review Status

- Status: `NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | COMPLETED`
- Owner:
- Reviewer:
- Reviewed on:

## Candidate

- Candidate ID:
- Shortlist priority: `high | medium | low`
- Evidence strength: `strong | medium | weak | contradictory`
- Product scope:
- Linked candidate file:

## Review Decision

- `_index.md` spec status: `approved | deferred | not reviewed`
- Approved for implementation: `yes | no | deferred under deadline`
- Reviewer decision notes:
- Required changes before coding:

## Sources

- Wiki facts:
- EDA evidence:
- Understanding summary:
- Playbook heuristics:

## Signal / Fair Value Logic

- Signal:
- Inputs:
- Missing-signal behavior:

## Execution Logic

- Buy behavior:
- Sell behavior:
- Passive/resting order behavior:
- Stay-idle behavior:

## Position And Risk Handling

- Position limits:
- Aggregate buy capacity:
- Aggregate sell capacity:
- Inventory skew or reduction:

## State And Runtime

- `traderData` use:
- Imports:
- Runtime risk:

## Expected Failure Cases

- Failure case:
- Mitigation or validation:

## Validation Plan

- Contract checks:
- Order sign and limit checks:
- Performance/run checks:
- Debug signals to inspect:

## Implementation Handoff

- Target bot path, normally `rounds/round_X/bots/<member>/canonical/...`:
- Parameters to implement:
- Known caveats:
