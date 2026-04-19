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

- Strategy candidates: generate a prioritized, ROI-driven queue of
  non-duplicative candidates.
- Strategy specification: turn a prioritized candidate into a reviewed
  implementation-ready spec.

Implementation must not start from the candidate list alone.

## Candidate quality

Good candidates are specific enough to compare and reject. Each candidate should include:

- product scope
- strategy family or source of edge
- evidence or heuristic basis, including linked EDA signals and understanding insight when available
- feature evidence, multivariate relationships, process hypotheses, redundancy decisions, and regime assumptions
- primary feature or fair-value model, plus any supporting features
- key assumptions
- main risk
- expected failure case
- what would validate or falsify it

Generate a bounded but not artificially capped set. Under normal 2-day
pressure, 5-8 strong ideas is often enough before prioritization; use more when
additional candidates are differentiated, evidence-backed, and likely to
change specs, implementation, validation, or final selection. Keep all
high-ROI candidates in the queue and prune only low-ROI, duplicate,
unsupported, non-online-usable, or decision-irrelevant ideas. Deeply specify the
highest-ROI candidates first unless time and validation capacity support more.

Prioritize serious candidates with lightweight fields for evidence strength (`strong | medium | weak | contradictory`) plus implementation cost, validation speed, risk, expected upside, and priority (`high | medium | low`). Use those fields to record a short priority rationale in `_index.md`; do not turn prioritization into a formula.

Understanding implications and prioritized unknowns should drive candidate
generation. If a candidate depends on an unresolved high-impact unknown, either
route that unknown to EDA or record the risk before prioritizing.

Do not create candidates from scratch when EDA or understanding exists. Ground candidates in prior artifacts, or label the missing evidence as a strategy assumption and route it back to EDA when it could change the decision.

## Feature budget

Strategy candidates should be feature-light by default.

- Use at most one primary edge feature or fair-value model per candidate.
- Add at most two supporting execution filters or risk controls.
- Diagnostics are allowed when they do not change trading decisions.
- More features require explicit justification in the candidate decision trace.

Every serious candidate should be traceable as:

```text
feature -> signal -> decision -> expected edge -> validation check
```

Prune feature-dump strategies, candidates whose features are not online-usable
without a defined proxy, weak features that do not target a known failure mode,
and feature combinations that do not change candidate queue/spec decisions.

Research-library output is evidence, not a mandate for complexity. Use EDA
tests, multivariate relationships, process hypotheses, redundancy/PCA notes,
regime labels, clustering, and diagnostics to choose simpler strategies,
parameters, or validation checks. Do not prioritize for specs a candidate that requires
offline-only research packages, PCA components, latent states, or cluster labels
in `Trader.run()` unless the spec defines an online proxy and the wiki runtime
supports the needed imports.

## Round coverage

Before prioritizing candidates for specs, check current-round mechanics, fields,
and product behaviors from EDA/understanding. Use them only when
decision-relevant, but do not leave relevant new mechanics implicit.
Prior-round assumptions need current-round evidence or must remain labeled
assumptions.

## Multivariate and process evidence

Use EDA multivariate and process evidence to keep candidates simple and
traceable:

- Prefer one primary edge feature that survives redundancy and controlled checks.
- Treat cross-product relationships as candidates only when EDA or understanding marks them useful or worth validating.
- Let process hypotheses guide strategy family selection, such as mean reversion, trend, defensive regime logic, or flow-driven execution.
- Reject feature stacks that combine duplicate signals unless the decision trace explains the incremental behavior.
- Route missing high-impact multivariate or process evidence back to targeted EDA instead of adding speculative features.

## Branch Before Commit

Strategy research may explore 5-10 conceptual branches when evidence supports
breadth. Group branches by product or source of edge, and keep them conceptual
until they survive pruning. Multi-product combinations should be evaluated for
compatibility, risk interaction, execution alignment, and cross-product
dependency before specs are written.

All high-ROI candidates remain available in the prioritized candidate queue.
Every serious candidate needs decision traceability: signals used, alternatives
rejected or deferred, selection rationale, role, priority tier, implementation
wave, and caveats. The queue should explain why earlier candidates are better
uses of implementation time than later candidates without deleting useful
backlog ideas.

Stop exploring when additional branches are duplicate, weak, unimplementable,
unlikely to change the candidate queue, or when implementation/validation has
become the bottleneck. Also stop broad branching when a strong incumbent exists
or deadline pressure makes more exploration low ROI.

## Dynamic or regime logic

Before prioritizing dynamic thresholds, regime filters, CUSUM, HMM-style logic,
or adaptive controllers for specs, check whether EDA found the regime `actionable`,
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
- Prefer clear, traceable, high-ROI strategy candidates over many weakly
  explained ideas; do not impose arbitrary candidate-count limits when the
  extra candidates are differentiated and validation-relevant.
- Make risk and inventory behavior explicit before handing work to implementation.
- Reject or defer weak and duplicate ideas with a reason instead of letting the candidate list grow.
- If all candidates share the same weakness, propose alternatives or return to EDA/understanding.

## Exit criteria

Strategy generation is done when:

- exploration board is completed or explicitly skipped with a reason
- candidates are grouped to avoid duplicate ideas
- candidates cite linked EDA signals, feature evidence, regime assumptions, and understanding insight when those artifacts exist
- candidates cite multivariate evidence, process hypotheses, redundancy decisions, and online proxies when those artifacts influence behavior
- each serious candidate has assumptions, main risk, and a validation/falsification path
- each serious candidate respects the feature budget or records why it does not
- each prioritized candidate has role, priority tier, evidence strength, and a short rationale
- each prioritized candidate has a decision trace naming signals used, alternatives rejected or deferred, and why it has its queue position
- weak or redundant ideas are rejected or deferred with a reason
- exploration stop-rule reason is recorded before moving to specs
- all high-ROI candidates are retained in a prioritized queue, while weak,
  duplicate, unsupported, or low-ROI ideas are rejected or deferred
- human prioritization is recorded

Strategy specification is done when:

- the reviewed spec defines signal or fair value, execution, inventory/risk, required state, expected failure cases, and validation checks
- the reviewed spec copies or summarizes the candidate selection trace
- the reviewed spec preserves links to the candidate, EDA signals, feature evidence, regime assumptions, and understanding insight
- the reviewed spec records process assumptions, multivariate relationships, redundancy decisions, and invalidation checks for implemented features when relevant
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
