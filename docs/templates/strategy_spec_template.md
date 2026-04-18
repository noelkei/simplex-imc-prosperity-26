# Strategy Spec Template

Implementation must not start until this spec is reviewed. In fast mode, keep it short but do not omit signal, execution, risk, state, or validation checks.

## Spec Quality Checklist

- Candidate ID, priority, and evidence basis are linked from the shortlist.
- Selection trace from the candidate decision is copied or summarized.
- Linked EDA signals, feature evidence, regime assumptions, and understanding insight are recorded.
- Each implemented feature has a Feature Contract.
- Important features intentionally excluded from the bot are listed.
- Round-specific mechanics, Trader methods, and changed fields are classified.
- No prior-round assumption is used without current-round evidence or an explicit strategy assumption.
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

- `_index.md` spec status: `approved | deferred under deadline | not reviewed`
- Approved for implementation: `yes | no | deferred under deadline`
- Reviewer decision notes:
- Required changes before coding:

## Sources

- Wiki facts:
- EDA evidence:
- Understanding summary:
- Post-run research memory:
- Playbook heuristics:

## Selection Trace

- Based on candidate:
- Signals used:
- Alternatives considered:
- Why selected:
- Known caveats:

## Evidence Traceability

- Linked EDA Signals:
- Feature Evidence:
- Regime Assumptions:
- Understanding Insight:
- Evidence gaps or strategy assumptions:

## Round-Specific Mechanics Contract

Use this for round mechanics that are not normal features, such as special Trader methods or auction mechanics.

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| MECHANIC | ROUND_DOC_OR_SPEC | implement / exclude / not applicable / blocked | BEHAVIOR_OR_REASON | CHECK |

## Feature Contract

Define every feature that changes trading behavior. EDA-only features must not be implemented unless this spec names an online proxy.

| Feature | Source Fields | Online Availability | Role | Parameters | Missing-Signal Behavior | State / `traderData` Required | Validation Check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FEATURE | FIELDS | usable online / EDA-only with proxy / log-only diagnostic / unknown | direct signal / execution filter / risk control / diagnostic | PARAMS | FALLBACK_OR_DISABLE | STATE | CHECK |

## Feature Exclusions

List important features considered but intentionally not implemented.

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| FEATURE | CSV-only / weak evidence / too complex / no decision impact / not in shortlist | CONDITION |

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
