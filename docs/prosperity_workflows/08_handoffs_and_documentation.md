# Handoffs and Documentation

Handoffs make work reusable across contributors and agents. They should be short, specific, and source-aware.

## Standard handoff format

Use this structure when handing work to another workstream:

```md
## Summary
What changed or what was learned.

## Sources
Wiki facts:
Playbook heuristics:
Data/log artifacts:

## Assumptions
What is assumed but not official.

## Evidence
Commands, files, charts, logs, or observations.

## Risks or caveats
Known gaps, ambiguity, or fragility.

## Next action
The next useful step and who can pick it up.
```

## Common handoff paths

- EDA to strategy: provide observed patterns, reproduction steps, and evidence limits.
- Strategy to implementation: provide hypothesis, parameters, risk behavior, and tests.
- Implementation to validation: provide changed behavior, expected outputs, and known risk areas.
- Validation to strategy: provide failures, logs, and whether the issue is factual, implementation-level, or heuristic.
- Round preparation to all workstreams: provide products, limits, manual/algorithmic separation, caveats, and data availability.

## Documentation rules

- Link to wiki facts instead of restating large rule blocks.
- Label playbook guidance as heuristic.
- Keep docs operational: what to do, what to check, and what to hand off.
- Prefer concise notes over long narratives.
- Do not hide uncertainty; make it easy to find and resolve.

## Good next actions

A good next action is concrete and bounded:

- "Run EDA on spread distribution for the active product data."
- "Implement the documented inventory cap in the strategy note."
- "Validate aggregate order capacity against the active round limits."
- "Extract missing manual-only mechanics into the round doc."

Avoid vague next actions such as "improve bot" or "look into strategy."
