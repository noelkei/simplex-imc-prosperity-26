# Prosperity Workflows

This folder defines how contributors and coding agents should work in this repository.

It is not a strategy manual and it does not define one correct path to a winning Python file. Useful work can come from exploratory data analysis, strategy research, bot implementation, debugging, validation, round documentation, or handoff cleanup.

## Source hierarchy

- Use [`../prosperity_wiki/`](../prosperity_wiki/) for factual rules: API contracts, datamodel fields, exchange mechanics, position limits, runtime constraints, platform flow, round facts, and source caveats.
- Use [`../prosperity_playbook/`](../prosperity_playbook/) for heuristics: strategy patterns, risk habits, debugging practices, and iteration advice.
- Do not use `bots/` or `performances/` as a source of truth.
- Treat the Prosperity API contract as stable unless round documentation explicitly says otherwise.

When a fact is missing, ambiguous, or inconsistent, record a caveat. Do not invent official rules.

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

## Operating rule

Each contribution should make the next contributor's job easier. A good handoff states what changed, which sources were used, what assumptions remain, what evidence exists, and what the next useful action is.
