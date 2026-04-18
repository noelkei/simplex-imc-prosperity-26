# Safe Change Rules

These rules apply across docs, research, implementation, and validation.

## Always preserve source boundaries

- Wiki facts define official constraints.
- Playbook guidance defines heuristics and best practices.
- Repo-local bot code and performance outputs are local artifacts, not authority. New work belongs under member-owned `rounds/round_X/bots/<member>/` and `rounds/round_X/performances/<member>/`; removed top-level `bots/` and `performances/` must not be recreated.
- `non-canonical/` is personal scratch space. Do not use it as evidence, examples, or implementation source unless the user explicitly points to a draft, and then summarize useful parts into formal artifacts before relying on them.
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
- Follow the reviewed spec's Feature Contract and Round-Specific Mechanics Contract; do not invent feature behavior or round mechanics in code.
- Treat prior-round products, limits, fair values, constants, and mechanics as invalid until current-round evidence or a labeled assumption supports them.
- Treat manual challenge mechanics as separate from algorithmic implementation requirements.
- Use logs and sample data for validation, but do not treat sample performance as proof of future performance.

## Protect research safety

- Keep EDA findings tied to named artifacts.
- Distinguish observation from interpretation.
- Do not overstate a strategy from one sample, one run, or one chart.
- Prefer falsifiable strategy notes with explicit failure modes.
- Keep strategy candidates feature-light; use the feature budget and reject feature dumping unless explicitly justified.

## Before handoff

Confirm that the contribution states:

- Source category: wiki fact, playbook heuristic, EDA evidence, implementation context, or strategy assumption.
- Scope: which workstream and products or files it affects.
- Evidence: what was checked or produced.
- Caveats: what remains uncertain.
- Next action: the most useful continuation.
