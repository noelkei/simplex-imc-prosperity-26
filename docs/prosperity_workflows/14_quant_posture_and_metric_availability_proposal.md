# Proposal - Quant Posture, Metric Availability, And Feature Promotion Guards

## Status

Historical rationale. The core recommendations from this proposal have been
implemented in repository rules, workflows, templates, and EDA skill guidance.
Keep this file as design context, not as a pending task list.

## Why This Proposal Exists

Recent round work surfaced a set of practices that are clearly high-value, but
are still only partially enforced by the current system.

The core issue is not that the repo lacks good workflows. The issue is that a
few especially important `quant-style` behaviors still depend too much on the
agent noticing them, instead of the system asking for them explicitly.

The most important gaps are:

- metric feasibility is often implicit instead of explicitly audited,
- engineered features can be promoted without a minimal incremental-value check,
- richer models are not always forced to justify themselves against simple
  baselines,
- research-grade analytics and bot-grade logic are not always separated with
  the same explicit taxonomy,
- ambitious user requests can tempt the system into either overpromising or
  under-delivering unless approximation rules are stated clearly.

## Recommendation Summary

Implement the following as first-class system behavior:

1. `Metric Availability Audit`
2. `Feature Promotion Requires Mini EDA`
3. `Baseline vs Richer Model Ladder`
4. `Research-Grade vs Bot-Grade Classification`
5. `Honest Approximation Rule For Incomplete Quant Requests`
6. `Quant Posture` guidance in `AGENTS.md`

These changes are worth implementing. They increase truthfulness, reduce
wasted complexity, and make advanced quant work more reusable without making
the system heavier for simple tasks.

## Proposal 1 - Metric Availability Audit

### Problem

The system says “do not invent facts”, but it does not always force an explicit
answer to:

- is the requested metric truly available,
- only proxyable,
- or not honestly computable from the current data?

This matters for requests involving:

- put-call parity,
- open interest,
- CVA,
- default probability,
- exposure metrics,
- surface or term-structure claims,
- and many other quant diagnostics.

### Proposed rule

When a task requests advanced market or risk metrics, the artifact should
explicitly classify each metric as one of:

- `implemented`
- `implemented_as_proxy_only`
- `partially_available`
- `not_available`

and should state why.

### Best place to encode it

- `AGENTS.md`
- `docs/prosperity_workflows/03_workstream_eda.md`
- `docs/prosperity_workflows/11_dataset_eda_framework.md`

### Suggested AGENTS language

Add a hard rule like:

- When a requested metric depends on market fields, contracts, or exposures
  that are not fully present, do not silently approximate it. First classify it
  as `implemented`, `proxy-only`, `partially available`, or `not available`,
  and record the reason.

## Proposal 2 - Feature Promotion Requires Mini EDA

### Problem

The system already encourages hypothesis-driven EDA, but it does not yet make
explicit enough that newly engineered features should be tested before being
promoted.

That means a feature can be described as useful without a minimal check such as:

- correlation / covariance context,
- group-conditioned outcomes,
- controlled baseline comparison,
- redundancy check,
- stability split,
- or negative evidence.

### Proposed rule

Any feature promoted as `usable`, `online-usable`, or `strategy-relevant`
should receive a minimal evidence check appropriate to the phase.

That can be very lightweight, for example:

- grouped summary,
- markout split,
- correlation against the relevant target,
- redundancy check against stronger features,
- or model-ladder incremental value.

### Best place to encode it

- `docs/prosperity_workflows/03_workstream_eda.md`
- `docs/prosperity_workflows/04_workstream_strategy.md`
- `AGENTS.md`

### Suggested workflow language

Under EDA:

- If a feature is promoted beyond exploratory status, run a compact
  feature-specific check showing whether it adds decision-relevant information,
  duplicates stronger features, or should remain exploratory.

Under Strategy:

- Do not treat a feature as a promoted candidate input unless EDA has either
  validated it directly or clearly labeled the missing validation as an
  assumption.

## Proposal 3 - Baseline vs Richer Model Ladder

### Problem

The system encourages evidence, but it does not explicitly force richer models
to justify themselves against simpler alternatives.

This matters for:

- pricing models,
- regime models,
- counterparty layers,
- residual frameworks,
- and advanced quant add-ons in general.

Without a required ladder, complex models can appear justified just because
they are sophisticated.

### Proposed rule

When an artifact introduces a materially richer quantitative model, compare it
against a simpler baseline and report the incremental value.

Examples:

- flat-vol BS vs Heston,
- raw names vs engineered context,
- simple residual vs structured residual,
- naive spread filter vs richer execution context.

### Best place to encode it

- `docs/prosperity_workflows/03_workstream_eda.md`
- `docs/prosperity_workflows/04_workstream_strategy.md`
- `AGENTS.md`

### Suggested AGENTS language

- Prefer a model ladder when adding quant complexity: start with a simple
  baseline, compare the richer model against it, and report the incremental
  value before promoting the richer model as decision-relevant.

## Proposal 4 - Research-Grade vs Bot-Grade Classification

### Problem

The current system already distinguishes official facts from heuristics and
online-usable bot logic from research packages, but it still lacks one compact
classification for outputs themselves.

That creates avoidable ambiguity between:

- something useful only for EDA,
- something valid for understanding,
- something that is online-usable,
- and something actually worth implementing in a bot.

### Proposed rule

Add a small lifecycle vocabulary for advanced signals, models, and metrics:

- `EDA-only`
- `research-only`
- `understanding carry-forward`
- `online-usable`
- `implementation candidate`

### Best place to encode it

- `AGENTS.md`
- `docs/prosperity_workflows/03_workstream_eda.md`
- `docs/prosperity_workflows/08_handoffs_and_documentation.md`

### Suggested workflow language

- Every advanced feature, model, or metric that materially influences a round
  should leave the phase with a lifecycle label, not just a narrative
  description.

## Proposal 5 - Honest Approximation Rule For Incomplete Quant Requests

### Problem

Users can ask for industry-standard quant diagnostics even when the repository
does not have the full data needed to implement them literally.

Today the system is good at not inventing facts, but it is less explicit about
what to do next. That can lead to two bad outcomes:

- fake precision,
- or premature refusal when a useful partial implementation would still help.

### Proposed rule

When the user requests a standard quant metric that is not fully supported by
the data, do the strongest honest version available and label it clearly.

Examples:

- true CVA unavailable -> implement a clearly named structural stress proxy
- open interest unavailable -> implement volume-only analysis and availability
  note
- full term structure unavailable -> implement short-maturity decay view and
  label it accordingly

### Best place to encode it

- `AGENTS.md`
- `docs/prosperity_workflows/03_workstream_eda.md`
- `docs/prosperity_workflows/11_dataset_eda_framework.md`

### Suggested AGENTS language

- When a requested quant metric is only partially supported by the current
  data, implement the strongest honest approximation available, label it as a
  proxy or partial metric, and explain why the full metric is not available.

## Proposal 6 - Quant Posture In `AGENTS.md`

### Should AGENTS say “be a Quant Researcher / Analyst / Trader”?

Yes in spirit, but not as a vague label.

Just adding “act like a quant” would be too soft and would not create durable
behavior. What is more useful is a short concrete section that defines how a
quant-minded agent should behave inside this repository.

### Recommended AGENTS section

Suggested section title:

`## Quant posture`

Suggested content:

- Prefer explicit assumptions over silent financial inference.
- Distinguish `research-only`, `EDA-only`, `online-usable`, and
  `implementation candidate` outputs.
- Do not present unavailable market metrics as if they were observable.
- When promoting engineered features, run a compact incremental-value or
  redundancy check when the phase allows it.
- Compare advanced models against simple baselines before promoting them.
- Treat market structure, execution, and data availability as first-class
  constraints, not afterthoughts.
- When the user requests advanced quant analytics, implement the strongest
  honest version supported by the current data and label any proxy clearly.

This is worth adding because it gives agents a crisp quant behavior contract
without turning the whole repo into a quant-library project.

## File-Level Change Proposal

### `AGENTS.md`

Add:

- a new `Quant posture` section
- one hard rule for metric availability classification
- one hard rule for richer-model baseline comparison
- one hard rule for feature promotion checks

### `docs/prosperity_workflows/README.md`

Add:

- one short paragraph in the “How To Use These Workflows” section that
  advanced quant metrics must pass availability classification and lifecycle
  labeling

### `docs/prosperity_workflows/03_workstream_eda.md`

Add explicit subsections for:

- `Metric Availability Audit`
- `Feature Promotion Mini EDA`
- `Baseline vs Richer Model Ladder`
- `Approximation And Proxy Rules`

### `docs/prosperity_workflows/04_workstream_strategy.md`

Add:

- a rule that strategy should prefer promoted features that survived EDA checks
- a reminder that rich pricing or counterparty models need incremental evidence
  over simpler baselines

### `docs/prosperity_workflows/08_handoffs_and_documentation.md`

Add:

- a required field or checklist line for:
  - lifecycle classification
  - metric availability classification
  - proxy caveats

### `docs/prosperity_workflows/11_dataset_eda_framework.md`

Add:

- an explicit note that some standard market metrics may be unavailable in the
  dataset and should be labeled rather than silently omitted or fabricated

## Priority Recommendation

### Implement now

- `Quant posture` in `AGENTS.md`
- metric availability audit
- feature promotion mini EDA rule
- baseline vs richer model ladder

### Implement next

- lifecycle labels in handoffs
- proxy rules in dataset EDA framework

### Nice to have

- templates updated to include these fields by default

## Final Recommendation

This proposal is worth implementing.

It does not add bureaucracy for normal work. It mainly makes explicit a small
set of high-ROI behaviors that were already proving useful in advanced EDA and
quant-style round analysis.

The big win is not “making the system more academic”.
The big win is:

- fewer fake metrics,
- fewer unjustified complex models,
- clearer promotion of engineered features,
- and cleaner separation between research output and bot-worthy logic.
