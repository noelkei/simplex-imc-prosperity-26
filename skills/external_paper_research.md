# External Paper Research

Use this skill to run the formal Phase 02b external paper research workflow.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- Understanding context: `../rounds/round_X/workspace/phase_02_understanding_context.md`
- External paper research context: `../rounds/round_X/workspace/phase_02b_external_paper_research_context.md`
- External paper research artifact: `../rounds/round_X/workspace/02b_external_paper_research.md`
- Research folders: `../rounds/round_X/research/`
- Template: `../docs/templates/external_paper_research_template.md`
- Processed paper template: `../docs/templates/paper_processed_summary_template.md`
- Workflow: `../docs/prosperity_workflows/13_external_paper_research.md`

## Responsibilities

- Own phase 02b external paper research work.
- Run by default after understanding unless the user explicitly skips the phase.
- Read `_index.md`, `02_understanding.md`, `phase_02_understanding_context.md`, `phase_02b_external_paper_research_context.md`, and any existing files under `research/` before writing.
- Generate one grounded prompt for an external AI using current-round understanding inputs such as signal ledger, feature inventory, product attribution, negative evidence, open questions, regime hypotheses, strategy-relevant risks, and Prosperity runtime constraints.
- Explicitly ask the external AI to use internet, deep research, and extended reasoning if available.
- Ask for roughly 5-10 highest-ROI papers or resources, not a broad literature dump.
- Prefer practical, strategy-useful methods that can inspire implementable simple online trading bots.
- Include upload instructions for `rounds/round_X/research/papers_raw/` at the end of the prompt.
- Record the target research questions, expected upload folder, current wait state, strategy-readiness, and next action.
- After prompt generation, leave strategy free to proceed while this phase waits for uploads.
- Treat the phase as complete once at least one paper exists in `papers_processed/`.
- If the user explicitly skips the phase, record the skip/defer reason and do not block strategy.
- Do not hallucinate paper contents, titles, methods, or processed summaries before files exist.
- When files exist in `papers_raw/` but not `papers_md/`, convert only the missing files.
- When files exist in `papers_md/` but not `papers_processed/`, create concise processed summaries only for the missing files.
- Keep the pipeline incremental; do not reprocess all papers because one new file arrived.
- Do not wait for every uploaded paper to finish the full pipeline before strategy starts.
- Treat papers as idea sources and method references, not as official truth or as replacements for current-round EDA/understanding evidence.
- Mark paper-derived ideas as `implementable`, `variant-only`, `validation-only`, `EDA follow-up`, `no action`, or `inspiration-only` when relevant.
- Update `../rounds/round_X/workspace/02b_external_paper_research.md`, `_index.md`, and `phase_02b_external_paper_research_context.md`.

## Boundaries

- Do not fetch papers from the internet.
- Do not build search automation, embeddings, rankings, citation managers, or a database workflow.
- Do not bypass strategy generation by turning papers directly into implementation work.
- Do not let paper ideas override contradictory current-round evidence.

## Handoff

Pass the generated prompt, wait-state status, processed paper summaries, and
their action classifications to `skills/generate_strategy_candidates.md`.
