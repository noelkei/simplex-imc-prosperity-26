# Synthesize Understanding

Use this skill to turn ingestion and EDA artifacts into a concise understanding summary that strategy, spec, implementation, variant, validation, and debugging agents can consume without redoing the analysis.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Ingestion: `../rounds/round_X/workspace/00_ingestion.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Phase context: `../rounds/round_X/workspace/phase_02_understanding_context.md`
- Template: `../docs/templates/understanding_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Steps

1. Read `_index.md`, ingestion, EDA summaries, and phase context before writing.
2. Preserve source labels: wiki fact, EDA evidence, playbook heuristic, hypothesis, assumption, and unknown.
3. Convert ingestion unknowns and EDA findings into evidence synthesis, confidence/impact, prioritized unknowns, and strategy implications.
4. Prioritize the strongest EDA signals and downgrade or discard weak, contradictory, or under-validated signals.
5. Identify actionable features/signals, high-confidence vs low-confidence areas, and regime assumptions that strategy agents must preserve.
6. Convert each retained signal into a decision label: try, avoid, validate next, defer, or treat as an assumption.
7. Fill `Strategy-Relevant Insights`, `What Should Be Tried`, `What Should Not Be Trusted Yet`, and `Open Risks And Unknowns`.
8. Do not duplicate full EDA reports; link them and summarize only decision-useful conclusions.
9. Do not rerun broad EDA during synthesis. If EDA is insufficient, record the gap and route a targeted question back to phase 01.
10. Prefer fewer clear, reusable insights over many unclear findings.
11. Do not use `non-canonical/` drafts unless the user explicitly points to one; if useful, summarize the relevant point as a labeled assumption or question.
12. If a high-impact unknown blocks strategy selection, set the phase or blocker accordingly and propose targeted EDA or clarification.
13. Update `../rounds/round_X/workspace/02_understanding.md`, `_index.md`, and `phase_02_understanding_context.md`.
14. Handoff with what to use, what not to trust yet, what strategy directions are implied, what validation is needed, and the next priority action.
