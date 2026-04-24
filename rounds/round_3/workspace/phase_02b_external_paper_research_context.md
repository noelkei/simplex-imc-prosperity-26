# Phase 02b - External Paper Research Context

## Status

IN_PROGRESS

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-24

## What Has Been Done

- Read and consumed `02_understanding.md` and `01_eda/eda_option_surface_and_microstructure.md`.
- Generated the external research prompt targeting 7 Round 3 research questions:
  - Online closed-form call option fair value (no scipy)
  - Extrinsic residual dynamics near expiry (TTE 5–8d)
  - Multi-strike surface arbitrage / monotonicity-aware pricing
  - Imbalance signals in derivative / option markets
  - Multi-product inventory management under position limits
  - Passive execution heuristics for wide-spread OTM options
- Prompt written to `02b_external_paper_research.md`.
- Research folder structure expected at `../research/papers_raw/`.

## Current Findings

- No papers uploaded yet. Pipeline is in wait state.

## Decisions Made

- Papers are idea sources, not official facts.
- Strategy may proceed now (data-driven) while this phase waits for uploads.
- This phase becomes complete once at least one processed paper exists in `../research/papers_processed/`.

## Open Questions / Blockers

- Waiting for human to paste prompt into an external AI and upload PDFs to `../research/papers_raw/`.
- TTE 5d residual behavior remains unobserved in historical data (key open question for papers to address).

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)

## Next Priority Action

Human pastes the prompt from `02b_external_paper_research.md` into an external AI (Perplexity Pro, ChatGPT with browsing, or Gemini Deep Research), downloads recommended PDFs, and uploads them to `../research/papers_raw/`. Once any file arrives, convert to Markdown → processed summary. Strategy (Phase 03) should proceed now without waiting.

## Deadline Risk

Unknown.
