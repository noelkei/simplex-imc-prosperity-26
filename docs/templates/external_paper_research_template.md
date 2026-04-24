# External Paper Research Template

## Status

`NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | COMPLETED`

Phase logic:

- generate the prompt by default after understanding
- strategy may proceed while the phase is waiting or only partially processed
- Phase 02b is operationally complete once at least one file exists in
  `papers_processed/`
- the artifact should still distinguish between partially processed and fully
  processed local paper sets
- if the user explicitly skips the phase, record the reason and do not block
  strategy

## Sources

- Understanding summary:
- Understanding context:
- EDA evidence:
- Post-run research memory:
- Other named artifacts:

## Research Goals

- Goal:
- Why this matters before strategy generation:
- Prosperity runtime / Trader constraints to preserve:

## Current Round Inputs

### Signals And Features To Target

| Signal / Feature / Risk | Product Or Scope | Source | Why It Matters |
| --- | --- | --- | --- |
| ITEM | PRODUCT_OR_SCOPE | understanding / EDA / post-run memory | RATIONALE |

### Negative Evidence And Failure Modes

| Item | Source | Why It Should Be Avoided Or Addressed |
| --- | --- | --- |
| ITEM | understanding / EDA / post-run memory | REASON |

### Open Questions And Regime Hypotheses

| Question Or Hypothesis | Why It Matters | Desired External Research Help |
| --- | --- | --- |
| ITEM | IMPACT | NEED |

## Target Research Questions

- Question:

## Online Search / Shortlist Notes

- Mode used: `none | local-only | online-shortlist | online-metadata-verification | mixed`
- Queries / intent:
- Accepted shortlist:
- Rejected shortlist and why:

## Generated External Research Prompt

```text
PASTE_PROMPT_HERE
```

## Prompt Requirements Checklist

- Ask external AI to use internet / deep research / extended reasoning if available: `yes | no`
- Ask for roughly 5-10 highest-ROI papers or resources: `yes | no`
- Prioritize implementable methods for simple online trading bots: `yes | no`
- Ask for links / citations / PDFs if available: `yes | no`
- Include upload instruction for `rounds/round_X/research/papers_raw/`: `yes | no`

## Batch Plan

| Batch | Goal | Papers | Stop Condition |
| --- | --- | --- | --- |
| Batch 1 | FIRST-CANDIDATE-CHANGING | PAPER_IDS | CONDITION |
| Batch 2 | GUARDRAIL_OR_REGIME | PAPER_IDS_OR_NONE | CONDITION |
| Batch 3 | BENCHMARK_OR_UTILITY | PAPER_IDS_OR_NONE | CONDITION |

## Paper Pipeline Status

- Expected upload folder: `rounds/round_X/research/papers_raw/`
- Raw papers detected:
- Markdown conversions pending:
- Processed summaries pending:
- Strategy may proceed now: `yes | no`
- Waiting state: `prompt-generated-waiting | shortlist-ready | ready-to-convert | ready-to-process | partially-processed | fully-processed | explicitly-skipped`

## Processed Paper Index

| Paper ID | Input Type | Raw File | Markdown File | MD Fidelity | Processed Summary | Batch | Status | Action Classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPER_ID | pdf / latex_source / mixed / unknown | FILE_OR_NONE | FILE_OR_NONE | high / medium / needs_review / none | FILE_OR_NONE | Batch 1 / Batch 2 / Batch 3 / none | waiting / converted-usable / converted-needs-review / processed | new candidate / variant / validation check / EDA follow-up / no action |

## Guardrails

- Papers are idea sources, not official facts.
- Paper ideas must map back to current-round evidence, risks, or open questions.
- Online shortlist-building is allowed, but canonical pipeline inputs remain the local files under `papers_raw/`.
- Non-implementable ideas should be marked `inspiration-only` or routed to validation / EDA, not forced into Trader logic.
- Do not hallucinate paper contents before files exist.
- Do not block strategy on the full raw -> md -> processed pipeline.

## Assumptions

- Assumption:

## Open Questions / Blockers

- Blocker:

## Next Action

- Next:
