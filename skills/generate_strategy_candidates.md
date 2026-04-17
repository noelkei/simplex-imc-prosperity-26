# Generate Strategy Candidates

Use this skill to generate, lightly prioritize, reject, defer, or shortlist strategy candidates from existing ingestion, EDA, and understanding evidence.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Phase context: `../rounds/round_X/workspace/phase_03_strategy_context.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Candidate template: `../docs/templates/strategy_candidates_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Responsibilities

- Own phase 03 strategy candidate work.
- Read `../rounds/round_X/workspace/post_run_research_memory.md` when it exists before branching or pruning; use it as evidence input and cite relevant insights in `Decision Trace` when they influence selection.
- Consume existing understanding, EDA summaries, and candidates before adding new ideas.
- Generate only non-duplicative candidates tied to linked EDA signals, feature evidence, regime assumptions, understanding insights, playbook heuristics, or explicit strategy assumptions.
- Start with an exploration board when evidence supports more than one plausible direction; keep these as conceptual branches, not active strategies.
- Generate conceptual branches by product or source of edge before shortlisting.
- Evaluate multi-product combinations conceptually when relevant, including compatibility, risk interaction, execution alignment, and cross-product dependency.
- Use post-run failure patterns, edge decomposition, counterfactual backlog, and negative evidence when present to prune weak branches and prioritize high-ROI candidates.
- Keep facts, EDA evidence, understanding insights, playbook heuristics, hypotheses, and assumptions separate.
- Score serious candidates using evidence strength, implementation cost, validation speed, risk level, expected upside, and priority.
- Record rejected or deferred alternatives and why they were pruned.
- Record a decision trace for shortlisted candidates: signals used, alternatives rejected, reason selected, and caveat.
- Apply the exploration stop rule before writing specs; stop when more branches are duplicate, weak, unimplementable, unlikely to change the shortlist, blocked by implementation/validation bottlenecks, dominated by a strong incumbent, or constrained by deadline pressure.
- Ask a lightweight human checkpoint only when the answer materially affects shortlist, risk appetite, or product priority; record the default if there is no answer.
- Keep at most 3 active strategies in `_index.md`.
- Shortlist 1-3 candidates and reject or defer weak/redundant ideas with a reason and evidence gap or risk.
- Update `../rounds/round_X/workspace/03_strategy_candidates.md`, `_index.md`, and `phase_03_strategy_context.md`.

## Boundaries

- Do not write implementation-ready specs.
- Do not mark spec review status.
- Do not hand off implementation directly.
- Do not implement combinations from the exploration board or compatibility matrix; they must first become shortlisted candidates and then reviewed specs.
- Do not create candidates from scratch when EDA or understanding exists. If evidence is missing, label the gap and route it to targeted EDA when it could change the decision.
- Do not use `non-canonical/` drafts as evidence unless the user explicitly points to one; convert useful draft ideas into labeled assumptions before shortlisting.

## Handoff

Pass shortlisted candidate IDs, evidence links, decision trace, priority rationale, risks, stop-rule reason, and unresolved unknowns to `skills/write_strategy_spec.md`.
