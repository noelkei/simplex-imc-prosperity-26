# Phase 02b - External Paper Research Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Codex
- Reviewer: Unassigned

## Last Updated

2026-04-27

## What Has Been Done

- Consumed the completed understanding summary and phase context.
- Generated a grounded external research prompt in
  [`02b_external_paper_research.md`](02b_external_paper_research.md).
- Wrote target research questions, negative evidence, and a batch plan aligned
  to current `round_4` strategy needs.
- Ran a controlled shortlist / metadata-verification pass to avoid repeating
  papers already processed in `round_3`.
- Normalized the current raw-paper filenames under `../research/papers_raw/`
  using canonical slugs derived from title-page inspection.
- Converted Batch 1 papers into usable Markdown files under
  `../research/papers_md/`.
- Converted the remaining Batch 2 and Batch 3 papers into usable Markdown files
  under `../research/papers_md/`.

## Current Findings

- Strategy does not need to wait for the paper pipeline.
- The highest-ROI external research themes are:
  participant-conditioned option-book context, signal-only vs inventory-worthy
  derivatives, lightweight surface-aware pricing/residual methods, defensive
  gating under concentrated flow, and family-level exposure framing.
- The current raw set contains 9 useful new papers and is ready for
  incremental raw -> md -> processed work.
- One preferred shortlist paper is still absent from the local raw set:
  `linnainmaa_saar_2012_lack_of_anonymity_and_the_inference_from_order_flow`.
- All 9 local raw papers now have usable Markdown conversions and the phase is
  ready for ROI-ordered processed summaries.

## Decisions Made

- Keep Phase `02b` non-blocking and leave it in `ready-to-process` after full
  raw -> md conversion.
- Let `03 Strategy` proceed immediately using the completed understanding
  artifact.
- Keep paper work incremental once uploads arrive; do not re-open broad
  research setup.

## Open Questions / Blockers

- Whether to upload the remaining preferred paper before or after Batch 1
  conversion.
- Exact deadline remains unknown.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02_understanding.md`](02_understanding.md)
- [`phase_02_understanding_context.md`](phase_02_understanding_context.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)

## Next Priority Action

Process the converted Markdown files into `../research/papers_processed/`,
starting with the highest-ROI trio from Batch 1, while keeping `03 Strategy`
unblocked.

## Deadline Risk

Low for `02b` itself because the prompt is ready, the raw set is present, and
strategy is unblocked; medium for the round overall until the deadline is
confirmed.
