# External Paper Research

Use this folder for manually uploaded external papers and their derived
artifacts.

## Structure

```text
research/
  papers_raw/
  papers_md/
  papers_processed/
```

- `papers_raw/`: PDFs or original source files uploaded by humans.
- `papers_md/`: Markdown conversions of raw papers.
- `papers_processed/`: concise strategy-useful summaries.

## Incremental Rules

- If a file exists in `papers_raw/` but not in `papers_md/`, convert only that file.
- If a file exists in `papers_md/` but not in `papers_processed/`, process only that file.
- Do not reprocess every paper because one new paper was added.
- Strategy does not wait for the full pipeline. Proceed as soon as the prompt exists, and start consuming paper input as soon as at least one processed paper exists.

## Source Discipline

- Papers are idea sources and method references, not official truth.
- Paper-inspired ideas must still map back to current-round signals, features, risks, regimes, or open questions.
- If a paper method cannot fit a simple Prosperity `Trader`, keep it as inspiration, validation guidance, or EDA follow-up rather than forcing it into strategy logic.
