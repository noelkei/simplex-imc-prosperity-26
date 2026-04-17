# Handoffs and Documentation

Handoffs make work reusable across contributors and agents. They should be short, specific, and source-aware.

Write phase artifacts for the next agent, not just for the current author. A good handoff tells the next agent what to use, what not to trust yet, and what to validate next.

## Standard handoff format

Use this structure when handing work to another workstream:

```md
## Summary
What changed or what was learned.

## Phase status
Status:
Index updated:

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

## Downstream use
What the next agent should use, avoid, or validate next.

## Next action
The next useful step and who can pick it up.
```

## Common handoff paths

- EDA to strategy: provide observed patterns, feature/signal hypotheses, reproduction steps, evidence limits, and which signals are usable, exploratory, or not ready.
- EDA to understanding: provide product scope, feature inventory, conditional patterns, signal confidence, caveats, and validation needs.
- Understanding to strategy: provide prioritized strategy-relevant insights, what should be tried, what should not be trusted yet, and open risks.
- Strategy spec to implementation: provide reviewed spec, parameters, risk behavior, and tests.
- Strategy/spec to variant generation: provide parent spec, insight being tested, allowed changed axes, expected effect, and validation check.
- Implementation to validation: provide changed behavior, expected outputs, and known risk areas.
- Validation to strategy: provide failures, logs, and whether the issue is factual, implementation-level, or heuristic.
- Platform run to post-run memory: provide reusable failure patterns, edge decomposition, counterfactuals, negative evidence, and links back to per-run artifacts.
- Round preparation to all workstreams: provide products, limits, manual/algorithmic separation, caveats, and data availability.

## Documentation rules

- Link to wiki facts instead of restating large rule blocks.
- Label playbook guidance as heuristic.
- Keep docs operational: what to do, what to check, and what to hand off.
- Prefer concise notes over long narratives.
- Do not hide uncertainty; make it easy to find and resolve.

## Platform run provenance

For each new platform run, save these together when possible:

- exact bot `.py`
- platform `.json`
- platform `.log`
- short decision note or run summary

Do not require hashes for normal competition flow. Raw `.log` files may be
untracked by repository ignore rules; keep them with the run when possible and
preserve decision evidence in tracked `.md` or `.json` summaries. If one of the
`.py`, `.json`, or `.log` artifacts is missing, keep analyzing, but record the
provenance caveat where the run is used for ranking, promotion, or post-run
memory.

## Minimal submission manifest

A final submission manifest should stay small and decision-focused:

```md
## Upload Decision

- Primary:
- Backup:
- Fallback:
- Rejected / not upload:
- Caveats:
- Last validation:
- Active file verified: yes | no
```

Do not turn the manifest into a large dashboard. Link out to run summaries or
platform artifact analysis for details.

## Good next actions

A good next action is concrete and bounded:

- "Run EDA on spread distribution for the active product data."
- "Implement the documented inventory cap in the reviewed strategy spec."
- "Validate aggregate order capacity against the active round limits."
- "Extract missing manual-only mechanics into the round doc."

Avoid vague next actions such as "improve bot" or "look into strategy."
