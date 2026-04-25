# Write Strategy Spec

Use this skill to convert a prioritized candidate into a reviewed or
deadline-deferred implementation-ready strategy spec.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Phase context: `../rounds/round_X/workspace/phase_04_spec_context.md`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- External paper research when present: `../rounds/round_X/workspace/02b_external_paper_research.md` and `../rounds/round_X/research/papers_processed/`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Specs: `../rounds/round_X/workspace/04_strategy_specs/`
- Spec template: `../docs/templates/strategy_spec_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Responsibilities

- Own phase 04 strategy specification work.
- Read `../rounds/round_X/workspace/post_run_research_memory.md` when it exists before writing specs; carry relevant insights into `Selection Trace`, evidence traceability, risk, or validation checks when they influence the spec.
- Write specs only for candidates from the prioritized candidate queue.
- Preserve links to EDA signals, feature evidence, multivariate relationships, process/distribution assumptions, redundancy decisions, regime assumptions, and understanding insights.
- Record research-tool evidence when it affects the spec, such as statistical confidence, correlation/covariance, controlled regressions, cross-product lead-lag, redundancy/PCA findings, volatility/regime findings, change points, clustering, or post-run diagnostics.
- Allow processed paper summaries to appear in the evidence trace as non-authoritative inspiration or method references, never as substitutes for current-round EDA, understanding, or round facts.
- If a paper-derived idea survives into the spec, cite the processed paper file
  directly in the evidence traceability.
- Copy or summarize the candidate decision trace so the spec shows signals used, alternatives considered, why this strategy was selected, and known caveats.
- When the spec follows a non-trivial run batch, preserve the key post-run framing that justified the candidate: whether it is a clean carry-forward, a path-rescue design, a coverage test, a paper-gap test, or a reopen-after-pruning hypothesis.
- Define a Feature Contract for every feature that changes trading behavior, including source fields, online availability, role, parameters, multivariate relationship, process assumption, redundancy decision, missing-signal behavior, `traderData` state requirements, and validation/invalidation checks.
- When a processed paper contributes a method or simplification, pull its
  `Minimal Usable Adaptation` into the relevant `Feature Contract`, `Feature
  Exclusions`, or `Validation Plan` instead of leaving it implicit.
- Name any process/distribution assumption that changes trading behavior. If the assumption fails in validation, the spec must say whether to disable the feature, change thresholds, reroute to EDA, or treat the result as expected risk.
- Require an online proxy before implementing PCA components, cluster labels, latent states, HMM-style regimes, change-point labels, or any other research-only representation. If no proxy exists, record the finding as EDA-only evidence or exclude it.
- Define a Round-Specific Mechanics Contract for every current-round mechanic, Trader method, or changed online field that could affect implementation. Mark each as implement, exclude, not applicable, or blocked.
- Record important Feature Exclusions for features that were considered but intentionally left out because they are CSV-only, weak, too complex, not online-usable, or not decision-relevant.
- Carry forward `Do Not Overuse` warnings from processed papers into feature
  exclusions, validation caveats, or implementation boundaries when they matter
  to the selected candidate.
- Define signal or fair value, execution, missing-signal behavior, position/risk handling, state/runtime, expected failures, validation checks, and allowed variant axes when useful.
- When relevant, make the validation plan explicit about what kind of failure the run should distinguish: `no edge`, `edge then reversal`, `inventory-limited`, `execution-limited`, or `subset contamination`.
- Treat validation-only or utility papers as validation or implementation-quality
  inputs, not as core signal logic.
- Explicitly exclude research-only dependencies from uploadable bot imports unless the wiki runtime docs allow them and the reviewed spec names that import.
- Keep facts, EDA evidence, understanding insights, playbook heuristics, hypotheses, and assumptions separate.
- Set initial spec status to `not reviewed`.
- Mark `approved` only when a recorded review outcome is approved or approved with caveats.
- Mark `deferred under deadline` only when deadline deferral is explicit.
- Refuse implementation handoff unless the spec status is `approved` or `deferred under deadline`, and unless the spec has a signal basis plus selection rationale. Deadline deferral must explicitly record any missing traceability.
- Do not add unreviewed new features in the spec if they were absent from strategy candidates or understanding; route back to strategy/understanding/EDA unless the deadline deferral explicitly records the assumption.
- Update relevant spec files, `_index.md`, and `phase_04_spec_context.md`.

## Boundaries

- Do not create new strategy candidates.
- Do not approve your own spec without a recorded review outcome.
- Do not implement Trader code.
- Do not leave current-round mechanics implicit. If a mechanic is relevant but unused, record the exclusion reason in the spec.
- If the prioritized candidate lacks evidence or a Feature Contract needed for
  implementation, record the gap and route back to candidates, understanding, or
  EDA.

## Handoff

Pass the reviewed or deadline-deferred spec, implementation constraints, validation checks, and caveats to `skills/create_trader.md`.
