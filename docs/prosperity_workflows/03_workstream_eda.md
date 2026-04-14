# Workstream: Exploratory Data Analysis

EDA turns sample data and run outputs into evidence. It does not need to produce bot code.

## Inputs

- A concrete question, such as price stability, spread behavior, volume distribution, fill behavior, or PnL breakdown.
- Data files, logs, or run artifacts available in the repo or from the platform.
- Wiki facts for interpreting fields, signs, products, and runtime context.
- Playbook heuristics only as research prompts, not as proof.

## Good outputs

- A short summary of the question, method, and result.
- Reproducible artifacts: notebook, script, table, plot, or command notes.
- Clear source references for the data used.
- A distinction between observed evidence and strategy interpretation.
- A recommendation for the next workstream: more EDA, strategy research, implementation, or validation.

## Safe practice

- Keep product names, symbols, and signs aligned with the wiki.
- Do not claim that a strategy is valid just because a pattern appears in sample data.
- Do not overfit conclusions to one sample day without saying so.
- Preserve surprising or contradictory findings as evidence, not as rules.

## Handoff checklist

- Data source and date or run identifier.
- Exact question answered.
- Main findings in a few bullets.
- Files or commands needed to reproduce.
- Assumptions and unresolved questions.
- Suggested next action.
