# Workstream: Strategy Research

Strategy research converts facts and evidence into testable trading ideas. It should remain explicit about which claims are official facts and which are heuristics, and it should preserve traceability from EDA signal evidence through understanding, candidate selection, specification, implementation, and variants.

## Inputs

- Wiki facts for products, limits, API behavior, matching, and runtime constraints.
- EDA findings when available.
- Understanding synthesis when available, especially strategy-relevant insights, what should be tried, what should not be trusted yet, and open risks.
- Post-run research memory when present, especially failure patterns, edge decomposition, counterfactual backlog, and negative evidence.
- Playbook heuristics for fair value, inventory management, risk, execution, and iteration.
- Current implementation context only when the task is to adapt or compare against existing code.

## Good outputs

- A strategy hypothesis with the expected source of edge.
- Links to EDA signal hypotheses, feature evidence, regime assumptions, and understanding insight.
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
- evidence or heuristic basis, including linked EDA signals and understanding insight when available
- feature evidence and regime assumptions
- key assumptions
- main risk
- expected failure case
- what would validate or falsify it

Generate a bounded set. Under normal 2-day pressure, 5-8 ideas is enough before shortlisting. Use 10-20 only when the team explicitly needs breadth. Shortlist 1-3 candidates, and deeply specify only 1-2 unless time allows more.

Prioritize serious candidates with lightweight fields for evidence strength (`strong | medium | weak | contradictory`) plus implementation cost, validation speed, risk, expected upside, and priority (`high | medium | low`). Use those fields to record a short priority rationale in `_index.md`; do not turn prioritization into a formula.

Understanding implications and prioritized unknowns should drive candidate generation. If a candidate depends on an unresolved high-impact unknown, either route that unknown to EDA or record the risk before shortlisting.

Do not create candidates from scratch when EDA or understanding exists. Ground candidates in prior artifacts, or label the missing evidence as a strategy assumption and route it back to EDA when it could change the decision.

## Branch Before Commit

Strategy research may explore 5-10 conceptual branches when evidence supports
breadth. Group branches by product or source of edge, and keep them conceptual
until they survive pruning. Multi-product combinations should be evaluated for
compatibility, risk interaction, execution alignment, and cross-product
dependency before specs are written.

Only 1-3 candidates become active shortlist items. Every shortlisted candidate
needs decision traceability: signals used, alternatives rejected, selection
rationale, and caveats. The shortlist should explain why the selected candidates
are better uses of implementation time than the pruned alternatives.

Stop exploring when additional branches are duplicate, weak, unimplementable,
unlikely to change the shortlist, or when implementation/validation has become
the bottleneck. Also stop broad branching when a strong incumbent exists or
deadline pressure makes more exploration low ROI.

## Dynamic or regime logic

Before shortlisting dynamic thresholds, regime filters, CUSUM, HMM-style logic,
or adaptive controllers, check whether EDA found the regime `actionable`,
`defensive only`, `weak`, or `not worth implementing`.

Use dynamic logic only when it can be observed online and it targets a concrete
weakness in the current champion. If the evidence is weak, keep the idea as
optional guidance or route it back to EDA instead of adding implementation
complexity.

## Historical bots

Historical bots are evidence mines, not truth. Use them to find partial signals,
execution ideas, bugs, and failure modes. Do not copy behavior into a new
candidate unless the reusable idea is captured in a spec and supported by run,
log, or EDA evidence.

## Spec review gate

Track spec status in `_index.md` as `approved`, `deferred under deadline`, or `not reviewed`. Implementation can proceed only when the spec is `approved` or explicitly `deferred under deadline`. A deadline deferral still requires a one-page spec with signal, execution, risk, state, and validation checks.

## Source discipline

Label claims clearly:

- "Wiki fact": official API, exchange, limit, runtime, platform, or round documentation.
- "EDA evidence": observed behavior from a named artifact or dataset.
- "Understanding insight": a synthesized decision-useful conclusion from the active understanding artifact.
- "Post-run memory insight": reusable evidence from platform or platform-style runs, linked back to run summaries or raw artifacts.
- "Playbook heuristic": recommended pattern or risk habit.
- "Strategy assumption": a choice made for testing, not an official rule.

## Safe practice

- Avoid presenting one strategy pattern as the only correct approach.
- Keep round-specific strategy notes scoped to the active round or to examples of workflow.
- Prefer testable hypotheses over broad claims.
- Prefer a few clear, traceable strategy candidates over many weakly explained ideas.
- Make risk and inventory behavior explicit before handing work to implementation.
- Reject or defer weak and duplicate ideas with a reason instead of letting the candidate list grow.
- If all candidates share the same weakness, propose alternatives or return to EDA/understanding.

## Exit criteria

Strategy generation is done when:

- exploration board is completed or explicitly skipped with a reason
- candidates are grouped to avoid duplicate ideas
- candidates cite linked EDA signals, feature evidence, regime assumptions, and understanding insight when those artifacts exist
- each serious candidate has assumptions, main risk, and a validation/falsification path
- each shortlisted candidate has priority, evidence strength, and a short rationale
- each shortlisted candidate has a decision trace naming signals used, alternatives rejected, and why it was selected
- weak or redundant ideas are rejected or deferred with a reason
- exploration stop-rule reason is recorded before moving to specs
- 1-3 candidates are shortlisted
- human prioritization is recorded

Strategy specification is done when:

- the reviewed spec defines signal or fair value, execution, inventory/risk, required state, expected failure cases, and validation checks
- the reviewed spec copies or summarizes the candidate selection trace
- the reviewed spec preserves links to the candidate, EDA signals, feature evidence, regime assumptions, and understanding insight
- assumptions are labeled as assumptions, not wiki facts
- spec review status is `approved` or explicitly `deferred under deadline`
- the spec is linked from `_index.md` or the phase context
- implementation can proceed without guessing

## Handoff checklist

- Hypothesis and intended products or scope.
- Factual constraints from the wiki.
- Evidence used from EDA or logs, including linked signal hypotheses and feature evidence.
- Understanding insight and regime assumptions being implemented.
- Heuristics used from the playbook.
- Parameters or assumptions to implement.
- Tests that would falsify or validate the idea.
