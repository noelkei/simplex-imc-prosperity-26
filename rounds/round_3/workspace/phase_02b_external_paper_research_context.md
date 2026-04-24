# Phase 02b - External Paper Research Context

## Status

COMPLETED

## Owner / Reviewer

- Owner: Unassigned
- Reviewer: Unassigned

## Last Updated

2026-04-24

## What Has Been Done

- Recorded the external research prompt in the phase artifact.
- Recorded that 02b used a mixed mode:
  prompt generation, controlled online shortlist / metadata verification, and
  local pipeline processing from `papers_raw/`.
- Confirmed that eight raw papers are present under `../research/papers_raw/`.
- Normalized the Round 3 paper set into stable `paper_id`s with consistent raw
  naming, usable `papers_md` files, and strategy-facing `papers_processed/`
  summaries.
- Converted the two source-first papers (`Choi` and `Bergault`) into structure-faithful Markdown files under `../research/papers_md/`.
- Converted four additional PDF-only papers (`Stoikov-Saglam`, `Muravyev`, `Garcia-Ares`, and `Fengler`) into structure-faithful Markdown files under `../research/papers_md/`.
- Converted the final two PDF-only papers (`CRR` and `West`) into structure-faithful Markdown files under `../research/papers_md/`.
- Processed the Batch 1 papers (`Choi`, `Muravyev`, and `Stoikov-Saglam`) into strategy-facing summaries under `../research/papers_processed/`.
- Processed the Batch 2 papers (`Garcia-Ares` and `Fengler`) into strategy-facing summaries under `../research/papers_processed/`.
- Processed the Batch 3 papers (`Bergault`, `CRR`, and `West`) into strategy-facing summaries under `../research/papers_processed/`.

## Current Findings

- The current paper set is now strong on Bachelier/normal pricing, static-arbitrage surface guardrails, multi-asset inventory-aware quoting, option inventory risk, option order flow, and near-expiry regime effects.
- Source-first conversion is working well for equation-heavy papers because formulas and figure assets can be referenced directly from raw source.
- PDF-first conversion is also working acceptably for the four highest-ROI strategy papers, with enough fidelity for theorem structure, regression setup, and figure/table captions.
- All currently uploaded raw papers now have corresponding `papers_md` conversions.
- Batch 1 now gives Strategy three immediately usable paper inputs:
  Bachelier fair-value backbone, imbalance-as-secondary-modifier framing, and
  inventory-aware voucher quote skewing.
- Batch 2 now adds two strong control layers:
  a live `TTE=5d` regime-caution frame and explicit surface-shape guardrails
  for cross-strike voucher logic.
- Batch 3 now closes the remaining gaps:
  family-coupled inventory heuristics, a discrete-tree fair-value benchmark,
  and implementation-quality guidance for `norm_cdf`.
- The current raw set is now `fully-processed`, not just operationally complete.
- The phase artifact now records batch coverage, input types, usable Markdown
  fidelity, and shortlist notes in the same shape the refactored workflow
  expects.

## Decisions Made

- Papers are idea sources, not official facts.
- Controlled online shortlist-building is allowed in 02b, but canonical
  pipeline inputs remain the local files under `../research/papers_raw/`.
- Strategy may proceed after the prompt is generated, even while this phase remains in a wait state.
- This phase becomes complete once at least one processed paper exists, or when the user explicitly skips it with reason.
- Convert source-first papers before PDF-only papers when possible.
- Batch processing order should follow ROI for Strategy, not raw-file arrival order.

## Open Questions / Blockers

- No blocker remains for Strategy.
- No paper-processing follow-on work is pending for the current raw set.

## Linked Artifacts

- [`_index.md`](_index.md)
- [`02b_external_paper_research.md`](02b_external_paper_research.md)

## Next Priority Action

Let Phase 03 Strategy consume the full processed paper set and classify the
paper-derived ideas as `used`, `hybrid`, `validation`, `rejected`, or
`inspiration-only` inside the strategy artifact.

## Deadline Risk

Low for Phase 02b itself; the round deadline is still unknown at the round level.
