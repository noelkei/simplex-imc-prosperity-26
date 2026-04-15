# Generate Strategy Candidates

Use this skill to generate, score, reject, defer, or shortlist strategy candidates from existing ingestion, EDA, and understanding evidence.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Phase context: `../rounds/round_X/workspace/phase_03_strategy_context.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Candidate template: `../docs/templates/strategy_candidates_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Responsibilities

- Own phase 03 strategy candidate work.
- Consume existing understanding, EDA summaries, and candidates before adding new ideas.
- Generate only non-duplicative candidates tied to linked EDA signals, feature evidence, regime assumptions, understanding insights, playbook heuristics, or explicit strategy assumptions.
- Keep facts, EDA evidence, understanding insights, playbook heuristics, hypotheses, and assumptions separate.
- Score serious candidates using evidence strength, implementation cost, validation speed, risk level, expected upside, and priority.
- Keep at most 3 active strategies in `_index.md`.
- Shortlist 1-3 candidates and reject or defer weak/redundant ideas with a reason and evidence gap or risk.
- Update `../rounds/round_X/workspace/03_strategy_candidates.md`, `_index.md`, and `phase_03_strategy_context.md`.

## Boundaries

- Do not write implementation-ready specs.
- Do not mark spec review status.
- Do not hand off implementation directly.
- Do not create candidates from scratch when EDA or understanding exists. If evidence is missing, label the gap and route it to targeted EDA when it could change the decision.
- Do not use `non-canonical/` drafts as evidence unless the user explicitly points to one; convert useful draft ideas into labeled assumptions before shortlisting.

## Handoff

Pass shortlisted candidate IDs, evidence links, priority rationale, risks, and unresolved unknowns to `skills/write_strategy_spec.md`.
