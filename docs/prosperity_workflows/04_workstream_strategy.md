# Workstream: Strategy Research

Strategy research converts facts and evidence into testable trading ideas. It should remain explicit about which claims are official facts and which are heuristics.

## Inputs

- Wiki facts for products, limits, API behavior, matching, and runtime constraints.
- EDA findings when available.
- Playbook heuristics for fair value, inventory management, risk, execution, and iteration.
- Current implementation context only when the task is to adapt or compare against existing code.

## Good outputs

- A strategy hypothesis with the expected source of edge.
- The fair value or signal definition, if applicable.
- Inventory and risk rules, including how the idea avoids limit rejection.
- Execution behavior: when it buys, sells, rests orders, or stays idle.
- Required state, if any, and whether it fits within `traderData` constraints.
- Test plan and known failure modes.

For active round workspaces, strategy work has two steps:

- Strategy candidates: generate and shortlist 1-3 non-duplicative candidates.
- Strategy specification: turn a shortlisted candidate into a reviewed implementation-ready spec.

Implementation must not start from the candidate list alone.

## Candidate quality

Good candidates are specific enough to compare and reject. Each candidate should include:

- product scope
- strategy family or source of edge
- evidence or heuristic basis
- key assumptions
- main risk
- expected failure case
- what would validate or falsify it

Generate a bounded set. Under normal 2-day pressure, 5-8 ideas is enough before shortlisting. Use 10-20 only when the team explicitly needs breadth. Shortlist 1-3 candidates, and deeply specify only 1-2 unless time allows more.

Score serious candidates with lightweight fields for evidence strength (`strong | medium | weak | contradictory`) plus implementation cost, validation speed, risk, expected upside, and priority (`high | medium | low`). Use the score to record a short priority rationale in `_index.md`; do not turn scoring into a formula.

Understanding implications and prioritized unknowns should drive candidate generation. If a candidate depends on an unresolved high-impact unknown, either route that unknown to EDA or record the risk before shortlisting.

## Spec review gate

Track spec status in `_index.md` as `approved`, `deferred`, or `not reviewed`. Implementation can proceed only when the spec is `approved` or explicitly `deferred under deadline`. A deadline deferral still requires a one-page spec with signal, execution, risk, state, and validation checks.

## Source discipline

Label claims clearly:

- "Wiki fact": official API, exchange, limit, runtime, platform, or round documentation.
- "EDA evidence": observed behavior from a named artifact or dataset.
- "Playbook heuristic": recommended pattern or risk habit.
- "Strategy assumption": a choice made for testing, not an official rule.

## Safe practice

- Avoid presenting one strategy pattern as the only correct approach.
- Keep round-specific strategy notes scoped to the active round or to examples of workflow.
- Prefer testable hypotheses over broad claims.
- Make risk and inventory behavior explicit before handing work to implementation.
- Reject or defer weak and duplicate ideas with a reason instead of letting the candidate list grow.
- If all candidates share the same weakness, propose alternatives or return to EDA/understanding.

## Exit criteria

Strategy generation is done when:

- candidates are grouped to avoid duplicate ideas
- each serious candidate has assumptions, main risk, and a validation/falsification path
- each shortlisted candidate has priority, evidence strength, and a short rationale
- weak or redundant ideas are rejected or deferred with a reason
- 1-3 candidates are shortlisted
- human prioritization is recorded

Strategy specification is done when:

- the reviewed spec defines signal or fair value, execution, inventory/risk, required state, expected failure cases, and validation checks
- assumptions are labeled as assumptions, not wiki facts
- spec review status is `approved` or explicitly `deferred under deadline`
- the spec is linked from `_index.md` or the phase context
- implementation can proceed without guessing

## Handoff checklist

- Hypothesis and intended products or scope.
- Factual constraints from the wiki.
- Evidence used from EDA or logs.
- Heuristics used from the playbook.
- Parameters or assumptions to implement.
- Tests that would falsify or validate the idea.
