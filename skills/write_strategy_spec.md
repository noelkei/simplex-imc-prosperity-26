# Write Strategy Spec

Use this skill to convert a shortlisted candidate into a reviewed or deadline-deferred implementation-ready strategy spec.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Phase context: `../rounds/round_X/workspace/phase_04_spec_context.md`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Specs: `../rounds/round_X/workspace/04_strategy_specs/`
- Spec template: `../docs/templates/strategy_spec_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Responsibilities

- Own phase 04 strategy specification work.
- Read `../rounds/round_X/workspace/post_run_research_memory.md` when it exists before writing specs; carry relevant insights into `Selection Trace`, evidence traceability, risk, or validation checks when they influence the spec.
- Write specs only for shortlisted candidates.
- Preserve links to EDA signals, feature evidence, regime assumptions, and understanding insights.
- Copy or summarize the candidate decision trace so the spec shows signals used, alternatives considered, why this strategy was selected, and known caveats.
- Define signal or fair value, execution, missing-signal behavior, position/risk handling, state/runtime, expected failures, validation checks, and allowed variant axes when useful.
- Keep facts, EDA evidence, understanding insights, playbook heuristics, hypotheses, and assumptions separate.
- Set initial spec status to `not reviewed`.
- Mark `approved` only when a recorded review outcome is approved or approved with caveats.
- Mark `deferred under deadline` only when deadline deferral is explicit.
- Refuse implementation handoff unless the spec status is `approved` or `deferred under deadline`, and unless the spec has a signal basis plus selection rationale. Deadline deferral must explicitly record any missing traceability.
- Update relevant spec files, `_index.md`, and `phase_04_spec_context.md`.

## Boundaries

- Do not create new strategy candidates.
- Do not approve your own spec without a recorded review outcome.
- Do not implement Trader code.
- If the shortlisted candidate lacks evidence needed for implementation, record the gap and route back to candidates, understanding, or EDA.

## Handoff

Pass the reviewed or deadline-deferred spec, implementation constraints, validation checks, and caveats to `skills/create_trader.md`.
