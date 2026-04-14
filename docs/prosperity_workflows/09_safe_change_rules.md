# Safe Change Rules

These rules apply across docs, research, implementation, and validation.

## Always preserve source boundaries

- Wiki facts define official constraints.
- Playbook guidance defines heuristics and best practices.
- Repo-local `bots/` code and `performances/` outputs are local artifacts, not authority.
- Strategy assumptions must be labeled as assumptions.
- Unknown or inconsistent source material must become a caveat, not an invented rule.

## Keep changes reviewable

- Make focused changes tied to one workstream or handoff.
- Avoid unrelated refactors while changing strategy or docs.
- Record the reason for non-obvious parameters, thresholds, or validation choices.
- Prefer links to source docs over duplicated rule text.
- Keep reusable workflow docs round-neutral.

## Protect implementation safety

- Check order signs, position signs, and aggregate order capacity before relying on an algorithm change.
- Keep `traderData`, runtime, and supported-library constraints visible when adding state or dependencies.
- Treat manual challenge mechanics as separate from algorithmic implementation requirements.
- Use logs and sample data for validation, but do not treat sample performance as proof of future performance.

## Protect research safety

- Keep EDA findings tied to named artifacts.
- Distinguish observation from interpretation.
- Do not overstate a strategy from one sample, one run, or one chart.
- Prefer falsifiable strategy notes with explicit failure modes.

## Before handoff

Confirm that the contribution states:

- Source category: wiki fact, playbook heuristic, EDA evidence, implementation context, or strategy assumption.
- Scope: which workstream and products or files it affects.
- Evidence: what was checked or produced.
- Caveats: what remains uncertain.
- Next action: the most useful continuation.
