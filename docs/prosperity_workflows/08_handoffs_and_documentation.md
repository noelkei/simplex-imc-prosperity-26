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

## Metric availability
Advanced metrics or models used: implemented / proxy-only / partially available / not available.

## Lifecycle labels
Which findings are EDA-only, research-only, understanding carry-forward, online-usable, or implementation candidates.

## Carry-forward principles
Validated rules, framing, or reusable lessons that downstream work should keep using.

## Untested hypotheses
Ideas worth exploring later, clearly marked as not yet validated.

## Do not repeat by default
Rejected or de-prioritized habits, branches, or assumptions that should stay closed unless new evidence appears.

## Risks or caveats
Known gaps, ambiguity, or fragility.

## Downstream use
What the next agent should use, avoid, or validate next.

## Run classification
When handing off a platform or proxy run: strategy family, changed axis, tested feature/signal, knowledge delta, ROI-gated memory action, portability, and dedup caveat.

## Next action
The next useful step and who can pick it up.
```

If the handoff crosses rounds or explicitly reuses prior-round learning, add:

```md
## Prior-round compatibility
- Source round:
- Compatibility verdict: compatible | partially compatible | not compatible
- What can be reused:
- What must be revalidated:
```

## Common handoff paths

- EDA to strategy: provide observed patterns, feature/signal hypotheses, reproduction steps, evidence limits, and which signals are usable, exploratory, or not ready.
- EDA to strategy: also provide any metric-availability caveats, proxy notes,
  baseline-vs-richer-model verdicts, and lifecycle labels for serious features
  or models.
- EDA to understanding: provide product scope, feature inventory, feature origin, online usability, role, lifecycle decision, conditional patterns, signal confidence, caveats, and validation needs.
- Understanding to strategy: provide prioritized strategy-relevant insights, what should be tried, what should not be trusted yet, and open risks.
- Strategy spec to implementation: provide reviewed spec, Feature Contract, Round-Specific Mechanics Contract, parameters, risk behavior, and tests.
- Strategy/spec to variant generation: provide parent spec, insight being tested, allowed changed axes, feature toggle if applicable, expected effect, and validation check.
- Implementation to validation: provide changed behavior, expected outputs, and known risk areas.
- Validation to strategy: provide failures, logs, whether the issue is factual, implementation-level, heuristic, or better reinterpreted as `signal-only candidate`, plus any carry-forward principles, untested hypotheses, and anti-patterns opened by the batch.
- Platform run to post-run memory: provide run classification, knowledge delta, ROI-gated memory action, reusable failure patterns, edge decomposition, feature feedback, counterfactuals, negative evidence, and links back to per-run artifacts.
- Round preparation to all workstreams: provide products, limits, manual/algorithmic separation, caveats, data availability, and the Prior-Round Compatibility Gate verdict when prior-round learning is being considered.
- Round closeout to next round: provide the closeout artifact, validated carry-forward principles, untested hypotheses, anti-patterns, canonical/historical cleanup state, and compatibility guidance for the next round.

## Platform run handoff fields

When a handoff includes a platform or platform-style run, include these fields if available:

- Candidate and strategy family.
- Changed axis and tested feature/signal.
- PnL source and comparability.
- Knowledge delta: `new | confirms | contradicts | duplicate | unclear`.
- ROI-gated memory action: `update | update lightly | no update`.
- Portability: `round-specific | likely reusable | uncertain | not applicable`.
- Reroute: champion decision, targeted EDA, spec revision, debugging, one-axis variant, or ignore.

## Documentation rules

- Link to wiki facts instead of restating large rule blocks.
- Label playbook guidance as heuristic.
- Keep docs operational: what to do, what to check, and what to hand off.
- Prefer concise notes over long narratives.
- Do not hide uncertainty; make it easy to find and resolve.
- Do not mix validated evidence, transferable principles, untested hypotheses, and anti-patterns in one unlabeled summary.
- If prior-round learning is reused, state the compatibility verdict explicitly instead of assuming continuity.
- If a requested quant metric was not fully supported, record whether it was
  omitted, proxied, or only partially implemented instead of leaving the reader
  to guess.

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
