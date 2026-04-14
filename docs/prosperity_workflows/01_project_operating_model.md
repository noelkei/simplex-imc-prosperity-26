# Project Operating Model

This repository supports multiple valid workstreams. Not every contributor is expected to edit the trading bot, and not every useful contribution produces a final submission file.

## Stable constraints

- The factual source of truth is [`../prosperity_wiki/`](../prosperity_wiki/).
- The strategy and process heuristic source is [`../prosperity_playbook/`](../prosperity_playbook/).
- `bots/` and `performances/` are local implementation and run-output artifacts, not sources of truth for rules, product facts, API contracts, or position limits.
- The Prosperity API contract should be treated as stable unless active round documentation explicitly says otherwise.
- Official rules, limits, product names, field names, and runtime constraints must not be inferred from examples, repo-local bot implementations, or performance outputs.
- Round-specific facts belong in round documentation or clearly labeled notes, not in reusable workflow rules.

## Valid contribution types

Useful contributions include:

- EDA outputs: summaries, charts, notebooks, scripts, or tables that answer a concrete data question.
- Strategy research: hypotheses, assumptions, expected edge, risk profile, and test plan.
- Bot implementation: code that implements a documented strategy under wiki-defined API and exchange constraints.
- Debugging and validation: logs, failure analysis, order-limit checks, runtime checks, and regression notes.
- Round preparation: extracted facts, caveats, product/limit tables, and algorithmic/manual separation for new rounds.
- Documentation and handoffs: concise notes that make work reproducible by someone else.

## Contribution shape

Prefer small, reviewable changes with a clear owner and handoff. A useful contribution should answer:

- What problem or question did this address?
- Which factual wiki pages and heuristic playbook sections were used?
- What changed, or what evidence was produced?
- Which assumptions remain unresolved?
- What should the next contributor do?

## No single workflow

The project can move from EDA to strategy to implementation, or from debugging back to strategy, or from round preparation directly to validation checklists. The correct workflow is the one that makes the current uncertainty smaller while preserving factual source boundaries.
