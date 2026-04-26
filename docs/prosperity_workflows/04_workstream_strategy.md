# Workstream: Strategy Research

Strategy research converts facts and evidence into testable trading ideas. It should remain explicit about which claims are official facts and which are heuristics, and it should preserve traceability from EDA signal evidence through understanding, candidate selection, specification, implementation, and variants.

## Inputs

- Wiki facts for products, limits, API behavior, matching, and runtime constraints.
- EDA findings when available.
- Understanding synthesis when available, especially strategy-relevant insights, what should be tried, what should not be trusted yet, and open risks.
- Prior-round closeout or carry-forward artifacts only after a
  `Prior-Round Compatibility Gate` says the previous round is compatible
  enough to matter.
- External paper research outputs when available, especially processed paper summaries and the explicit action classifications attached to them.
- Post-run research memory when present, especially failure patterns, edge decomposition, counterfactual backlog, and negative evidence.
- Playbook heuristics for fair value, inventory management, risk, execution, and iteration.
- Current implementation context only when the task is to adapt or compare against existing code.

## Good outputs

- A strategy hypothesis with the expected source of edge.
- A source classification for each serious candidate: `data-driven`,
  `paper-inspired`, `hybrid`, or `paper-rejected`.
- Links to EDA signal hypotheses, feature evidence, regime assumptions, and understanding insight.
- Links to any processed paper summary that materially shaped the candidate, plus the current-round evidence it maps back to.
- The fair value or signal definition, if applicable.
- Inventory and risk rules, including how the idea avoids limit rejection.
- Execution behavior: when it buys, sells, rests orders, or stays idle.
- Required state, if any, and whether it fits within `traderData` constraints.
- Test plan and known failure modes.
- A clear separation between:
  - `validated carry-forward principles`
  - `untested hypotheses`
  - `default anti-patterns / do not repeat by default`

When strategy work follows a meaningful validation batch, do not branch from
terminal PnL alone. Treat strategy as a synthesis step over platform ranking,
path-quality diagnostics, product or strike attribution, clean-vs-contaminated
test coverage, and newly revealed failure or opportunity patterns.

Make the branch posture explicit. A useful post-run strategy pass should say
whether a family is:

- `protect winner`
- `edge then reversal`
- `execution-limited`
- `inventory-limited`
- `no edge`
- or `not cleanly tested`

That label should drive what kind of next candidate is worth a slot. For
example, `edge then reversal` usually justifies retention, subset-pruning, or
exit redesign work before broad re-exploration.

For active round workspaces, strategy work has two steps:

- Strategy candidates: generate a prioritized, ROI-driven queue of
  non-duplicative candidates.
- Strategy specification: turn a prioritized candidate into a reviewed
  implementation-ready spec.

Implementation must not start from the candidate list alone.

## Candidate quality

Good candidates are specific enough to compare and reject. Each candidate should include:

- product scope
- product or strike role when role changes risk, execution, or interpretation
- strategy family or source of edge
- evidence or heuristic basis, including linked EDA signals and understanding insight when available
- feature evidence, multivariate relationships, process hypotheses, redundancy decisions, and regime assumptions
- primary feature or fair-value model, plus any supporting features
- signal class, such as valuation, microstructure, surface, or regime
- whether the product is being used as alpha, anchor, overlay, veto, or monitor
- whether the setup calls for aggression, passivity, or explicit no-trade behavior
- natural trade horizon
- the rule that is supposed to stop `edge -> giveback`
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

Strategy should not wait for the full paper pipeline. After the 02b prompt is
generated, proceed with data-driven candidate work and consume processed paper
summaries whenever they become available.

## Paper Intake Pass

When `research/papers_processed/` exists, strategy should begin with a short
paper intake pass before broad branching:

- Review only the materially relevant processed papers for the current round.
- Record which current-round signal, risk, regime, or open question each paper
  actually maps to.
- Classify each materially relevant paper as `used`, `hybrid`, `validation`,
  `rejected`, or `inspiration-only`.
- Stop importing additional paper ideas once they stop changing candidate
  priority, validation posture, or rejection logic.

This pass should stay compact. It is meant to prevent paper drift, not to turn
Strategy into literature review.

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

Paper-research output is inspiration, not truth. Use processed paper summaries
to suggest strategy families, validation checks, or failure-mode mitigations,
but do not let them override contradictory current-round EDA or understanding
evidence.

Always check `research/papers_processed/` when it exists. When no processed
papers are present yet, proceed without blocking and record that paper input was
not available.

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

## Post-Run Coverage Audit

When a round already has meaningful run evidence, strategy should perform a
compact coverage audit before proposing the next wave:

- Which hypotheses were tested cleanly and are now sufficiently answered?
- Which hypotheses were only tested inside contaminated composites and still
  need an isolated or cleaner test?
- Which paper-derived ideas changed validation posture only, versus genuinely
  earning another live test?
- Which branches showed `no edge`, versus `edge then reversal`, versus
  `execution-limited` behavior?
- Which branches reached meaningful intra-run edge or high peak PnL, but failed
  to retain it?
- Which products or strikes built the upside, and which gave it back?
- Which products or subsets remain untested but still matter for current-round
  ROI?

When the next round or next wave may inherit from a prior one, this audit
should also separate four outputs explicitly:

- `retrospective work completed`
- `validated carry-forward principles`
- `untested hypotheses worth revisiting`
- `default anti-patterns / rejected habits`

This audit should stay decision-oriented. It exists to reduce duplicate waves
and improve learning value, not to create unnecessary process overhead.

When linked products or derivatives exist, the audit should also ask whether a
signal was tested as:

- standalone product logic,
- underlying-anchored overlay logic,
- or only inside a contaminated composite where attribution stayed unclear.

## Derivative / Linked-Product Framing Check

Before prioritizing a serious candidate in a linked-product or derivative-heavy
round, answer these questions explicitly:

- Is this product behaving like `delta-1`, ITM structural, active risk leg,
  upper passive leg, floor/monitor, or another named role?
- Is the main signal valuation, microstructure, surface, or regime?
- Is the underlying being used as alpha, anchor, or both?
- Does the setup ask for aggressive quoting, passive quoting, or no-trade?
- What is the natural hold horizon?
- What rule is supposed to prevent large giveback if the edge appears early?

If these answers are not clear enough to influence candidate ranking, route the
gap back to targeted EDA or understanding instead of hiding it inside a broad
composite candidate.

## Branch Before Commit

Strategy research may explore 5-10 conceptual branches when evidence supports
breadth. Group branches by product or source of edge, and keep them conceptual
until they survive pruning. Multi-product combinations should be evaluated for
compatibility, risk interaction, execution alignment, and cross-product
dependency before specs are written.

When paper summaries exist, cite them only when the linked idea is still
grounded in current-round signals, risks, regimes, or open questions. Mark
paper-derived ideas as `used`, `hybrid`, `validation`, `rejected`, or
`inspiration-only`, and record the candidate source classification as
`data-driven`, `paper-inspired`, `hybrid`, or `paper-rejected`.

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

When run evidence is already rich, also stop broad branching when the remaining
open questions are mostly hold/unwind design, subset pruning, execution
refinement, or clean coverage of still-important but untested hypotheses.

## Dynamic or regime logic

Before prioritizing dynamic thresholds, regime filters, CUSUM, HMM-style logic,
or adaptive controllers for specs, check whether EDA found the regime `actionable`,
`defensive only`, `weak`, or `not worth implementing`.

Use dynamic logic only when it can be observed online and it targets a concrete
weakness in the current champion. If the evidence is weak, keep the idea as
optional guidance or route it back to EDA instead of adding implementation
complexity.

Prefer an explicit complexity ladder:

- simple no-trade, no-new-entry, or retention gates first
- transformed thresholds, vetoes, or linked-product filters second
- lightweight trend or slope logic third
- hidden-state or HMM-style logic only after simpler online-usable controls
  fail cleanly

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
- "External paper inspiration": a processed paper summary used as a method reference, not as current-round truth.
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
- processed papers are checked when present, without blocking the phase when
  none are available yet
- a paper intake pass is recorded when processed papers exist
- candidates cite linked EDA signals, feature evidence, regime assumptions, and understanding insight when those artifacts exist
- paper-derived ideas are explicitly classified as `used`, `hybrid`,
  `validation`, `rejected`, or `inspiration-only`
- each serious candidate records a source classification of `data-driven`,
  `paper-inspired`, `hybrid`, or `paper-rejected`
- candidates cite multivariate evidence, process hypotheses, redundancy decisions, and online proxies when those artifacts influence behavior
- each serious candidate has assumptions, main risk, and a validation/falsification path
- each serious candidate respects the feature budget or records why it does not
- each prioritized candidate has role, priority tier, evidence strength, and a short rationale
- each prioritized candidate has a decision trace naming signals used, alternatives rejected or deferred, and why it has its queue position
- when run evidence is already rich, each prioritized candidate also has a
  branch posture such as `protect winner`, `rescue via retention`,
  `clean isolation test`, `coverage gap`, or `prune`
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
