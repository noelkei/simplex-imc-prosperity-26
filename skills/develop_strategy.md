# Develop Strategy

Use this skill to generate, score, shortlist, or specify strategy candidates from reviewed understanding.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Specs: `../rounds/round_X/workspace/04_strategy_specs/`
- Candidate template: `../docs/templates/strategy_candidates_template.md`
- Spec template: `../docs/templates/strategy_spec_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Steps

1. Read `_index.md`, understanding, EDA summaries, and current candidates before generating new ideas.
2. Keep facts, evidence, heuristics, hypotheses, and assumptions separate.
3. Generate only non-duplicative candidates tied to evidence, heuristics, or explicit assumptions.
4. Score serious candidates using evidence strength, implementation cost, validation speed, risk level, expected upside, and priority.
5. Keep at most 3 active strategies in `_index.md`; reject or defer weak/redundant ideas with a reason.
6. Shortlist 1-3 candidates and deeply specify only 1-2 under time pressure.
7. Write specs only for shortlisted candidates using the spec template.
8. Mark spec status in `_index.md` as `approved`, `deferred`, or `not reviewed`.
9. Do not use `non-canonical/` drafts as evidence unless the user explicitly points to one; convert useful draft ideas into labeled assumptions before shortlisting.
10. Refuse implementation handoff unless the spec is `approved` or explicitly `deferred under deadline`.
11. Update `03_strategy_candidates.md`, relevant spec files, `_index.md`, and phase contexts.
