# Prosperity Workflows

This folder defines how contributors and coding agents should work in this repository.

It is not a strategy manual and it does not define one correct path to a winning Python file. Useful work can come from exploratory data analysis, strategy research, bot implementation, debugging, validation, round documentation, or handoff cleanup.

## Source hierarchy

- Use [`../prosperity_wiki/`](../prosperity_wiki/) for factual rules: API contracts, datamodel fields, exchange mechanics, position limits, runtime constraints, platform flow, round facts, and source caveats.
- Use [`../prosperity_playbook/`](../prosperity_playbook/) for heuristics: strategy patterns, risk habits, debugging practices, and iteration advice.
- Do not use round-local bot or performance artifacts as a source of truth.
- Do not use [`../../non-canonical/`](../../non-canonical/) as evidence or examples unless the user explicitly points to a draft.
- Treat the Prosperity API contract as stable unless round documentation explicitly says otherwise.

When a fact is missing, ambiguous, or inconsistent, record a caveat. Do not invent official rules.

## How To Use These Workflows

For active round work, start from `rounds/round_X/workspace/_index.md`, then read the relevant phase context and the task-specific workflow below.

When starting a phase, confirm required inputs and update the phase context. When continuing, update the existing artifact instead of creating duplicates. When closing, check the exit criteria, update `_index.md`, update the phase context, and leave a concrete next action.

When `rounds/round_X/workspace/post_run_research_memory.md` exists, treat it as
round-local evidence input for EDA, understanding, strategy, spec, and variant
decisions. Cite relevant insights when they influence a decision; do not treat
the memory as official Prosperity rules.

Keep the lightweight gates aligned across phases:

- EDA owns the feature lifecycle and Round Adaptation Check.
- Understanding compresses promoted signals and assumptions carried forward.
- Strategy enforces the feature budget and Round Coverage Check.
- Specs define the Feature Contract and Round-Specific Mechanics Contract.
- Validation owns the ROI-gated run update decision: `update`, `update lightly`, or `no update`.

## Workstream map

- [`01_project_operating_model.md`](01_project_operating_model.md): shared operating model for contributors and agents.
- [`02_sources_of_truth.md`](02_sources_of_truth.md): how to combine wiki facts with playbook heuristics.
- [`03_workstream_eda.md`](03_workstream_eda.md): exploratory data analysis workflow.
- [`04_workstream_strategy.md`](04_workstream_strategy.md): strategy research workflow.
- [`05_workstream_bot_implementation.md`](05_workstream_bot_implementation.md): bot implementation workflow.
- [`06_workstream_debugging_and_validation.md`](06_workstream_debugging_and_validation.md): debugging and validation workflow.
- [`07_workstream_round_preparation.md`](07_workstream_round_preparation.md): new-round documentation and preparation workflow.
- [`08_handoffs_and_documentation.md`](08_handoffs_and_documentation.md): safe handoff patterns between workstreams.
- [`09_safe_change_rules.md`](09_safe_change_rules.md): durable rules for safe repo changes.
- [`10_time_aware_team_pipeline.md`](10_time_aware_team_pipeline.md): 2-day deadline workflow, phase state tracking, round indexes, and fast mode.
- [`11_dataset_eda_framework.md`](11_dataset_eda_framework.md): column classification, adaptive EDA, and EDA-as-knowledge-transfer guidance.
- [`12_top_level_artifact_audit.md`](12_top_level_artifact_audit.md): historical cleanup audit for removed top-level `bots/` and `performances/`.
- [`../templates/`](../templates/): reusable Markdown templates for EDA, understanding, strategy candidates, strategy specs, run summaries, post-run research memory, and debugging issues.

## Operating rule

Each contribution should make the next contributor's job easier. A good handoff states what changed, which sources were used, what assumptions remain, what evidence exists, and what the next useful action is.
