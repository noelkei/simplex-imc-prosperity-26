# External Paper Research

Use `docs/templates/external_paper_research_template.md` as the structure for this file.

## Status

NOT_STARTED

## Sources

- Understanding summary:
- Understanding context:
- EDA evidence:
- Post-run research memory:

## Research Goals

- Goal:
- Why this matters before strategy generation:
- Prosperity runtime / Trader constraints to preserve:

## Target Research Questions

- Question:

## Generated External Research Prompt

```text
TBD
```

## Paper Pipeline Status

- Expected upload folder: `../research/papers_raw/`
- Raw papers detected: none
- Markdown conversions pending: none
- Processed summaries pending: none
- Strategy may proceed now: `no`
- Waiting state: `prompt-generated-waiting`

## Processed Paper Index

| Paper ID | Raw File | Markdown File | Processed Summary | Status | Action Classification |
| --- | --- | --- | --- | --- | --- |
| TBD | none | none | none | waiting | no action |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open questions.
- Non-implementable ideas should be marked `inspiration only` or routed to validation / EDA, not forced into Trader logic.
- Do not hallucinate paper contents before files exist.
- Do not block strategy on the full paper pipeline.

## Assumptions

- Assumption:

## Open Questions / Blockers

- Understanding summary required before generating the default external research prompt.

## Next Action

- Next: generate the external research prompt from the completed understanding summary, then let strategy proceed while waiting for files in `../research/papers_raw/`.
