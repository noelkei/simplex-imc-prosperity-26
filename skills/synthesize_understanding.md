# Synthesize Understanding

Use this skill to turn ingestion and EDA artifacts into a concise understanding summary for strategy work.

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
4. Do not duplicate full EDA reports; link them and summarize only decision-useful conclusions.
5. Do not use `non-canonical/` drafts unless the user explicitly points to one; if useful, summarize the relevant point as a labeled assumption or question.
6. If a high-impact unknown blocks strategy selection, set the phase or blocker accordingly and propose targeted EDA or clarification.
7. Update `../rounds/round_X/workspace/02_understanding.md`, `_index.md`, and `phase_02_understanding_context.md`.
8. Handoff with what is known, what is uncertain, what strategy directions are implied, and the next priority action.
