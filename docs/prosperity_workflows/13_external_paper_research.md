# Workstream: External Paper Research

External paper research is a lightweight bridge between understanding and
strategy generation. It turns current-round evidence into a prompt for an
external AI with internet or deep-research capability, may use controlled
online paper search or metadata verification when needed, waits for
human-uploaded paper files or source folders, and distills those papers into strategy-useful
summaries.

This workflow does not auto-download papers into the repo, hallucinate paper
contents, or treat papers as official truth. Canonical pipeline inputs remain
the local files under `rounds/round_X/research/papers_raw/`.

By default, this phase always generates the external research prompt after
understanding. It is intentionally lightweight and non-blocking in practice:
strategy may proceed after the prompt is generated, while processed papers are
consumed incrementally whenever they become available.

## Inputs

- Understanding summary, especially signal ledger, product attribution,
  negative evidence, open questions, regime hypotheses, strategy-relevant
  risks, and what should or should not be tried.
- Understanding context, especially blockers, decisions, and next action.
- EDA evidence when understanding links back to specific artifacts that clarify
  signal mechanics or uncertainty.
- Post-run research memory when present, especially failure patterns or
  counterfactual backlog that should shape external research requests.
- Prosperity runtime and Trader constraints from the wiki and reviewed workflow
  rules.

## Good Outputs

- One grounded external research prompt tailored to the active round.
- Optional online shortlist notes when the local paper set is missing or
  insufficient.
- A concise list of target research questions tied to current-round evidence.
- A clear wait state pointing to `rounds/round_X/research/papers_raw/`.
- Normalized raw-paper naming, input-type detection, and batch planning.
- Incremental Markdown conversions for newly uploaded raw papers.
- Markdown conversions with metadata, fidelity, and conversion caveats.
- Incremental processed paper summaries that extract practical methods,
  limitations, and strategy implications.
- A handoff that leaves strategy free to proceed after prompt generation while
  making processed papers available as optional inputs whenever they exist.

## Prompt Generation Rules

The generated prompt should:

- explicitly ask the external AI to use internet, deep research, and extended
  reasoning if available
- ask for roughly 5-10 highest-ROI papers or resources rather than a broad
  literature dump
- prioritize practical relevance to the current round's signals, regimes,
  failure modes, and risks
- prefer methods that can inspire implementable simple online trading bots
- ask for links, citations, and PDFs when available
- avoid purely theoretical work with no clear strategy or validation value
- preserve Prosperity runtime constraints and simple Trader implementation
  realism

The prompt footer should instruct the human to upload selected PDFs or source
folders into `rounds/round_X/research/papers_raw/` and then resume the raw ->
md -> processed pipeline.

## Online Search And Traceability

Online search is allowed inside Phase 02b only when it improves the local paper
pipeline without replacing it. Good reasons include:

- no useful local shortlist exists yet
- the current raw set is clearly insufficient for a high-priority research
  question from understanding
- a paper title, metadata field, or source identity needs verification before
  naming or processing

Rules:

- prefer primary sources such as arXiv, SSRN, DOI landing pages, or official
  publisher pages
- record the search intent, accepted shortlist, and rejected shortlist in the
  main phase artifact when online search materially shaped the paper set
- do not auto-download or write papers into the repo from internet sources
- do not treat online summaries as substitutes for local canonical inputs
- once a paper enters the repo, the local raw asset becomes the canonical input

## Wait-State Rules

After generating the prompt:

- record the prompt, target questions, expected upload folder, and waiting
  status in the main phase artifact
- enter a wait state if no raw papers exist yet
- leave strategy free to proceed after the prompt, even while this phase is
  still waiting
- do not infer paper findings, titles, or methods before files are uploaded
- do not claim paper inputs exist when they do not

Phase completion rule:

- once at least one paper exists in `papers_processed/`, this phase is
  considered complete
- later uploaded papers should still be processed incrementally without
  reopening the full pipeline

If paper research is explicitly skipped by the user:

- record the reason explicitly in `_index.md`, the phase context, and the main
  phase artifact
- leave strategy free to proceed without paper inputs

## Folder Pipeline

Use this round-local structure:

```text
rounds/round_X/research/
  papers_raw/
  papers_md/
  papers_processed/
```

Rules:

- `papers_raw/`: human-uploaded PDFs or source files; ignore dotfiles, cache
  junk, and non-paper artifacts when enumerating the folder
- `papers_md/`: Markdown conversions of raw files
- `papers_processed/`: concise strategy-useful summaries
- do not require every paper to pass through every stage before strategy starts
- strategy may proceed data-driven after the prompt is generated, and it must
  begin consuming paper input as soon as at least one processed paper exists
- convert only files in `papers_raw/` that do not yet have a corresponding file
  in `papers_md/`
- process only files in `papers_md/` that do not yet have a corresponding file
  in `papers_processed/`
- do not reprocess the whole folder because one new file arrived

## Raw Intake And Naming Rules

Each raw paper should go through a lightweight normalization pass before
conversion:

1. ignore junk such as dotfiles, cache artifacts, `.gitkeep`, and unrelated
   helper files
2. inspect the title page, PDF metadata, source folder contents, or landing-page
   metadata when needed
3. normalize the raw name
4. assign a stable `paper_id`
5. decide its ROI batch

Supported input types:

- `pdf`
- `latex_source`
- `mixed`

Naming defaults:

- raw file or folder: `author_slug_year_descriptive_title`
- `paper_id`: `surname_year_short_handle`
- Markdown file: same slug as the canonical raw asset with `.md`
- processed file: `<paper_id>_processed.md`

Compatibility rules:

- PDF-only papers may remain single files
- LaTeX source papers should remain folders
- when both a PDF and source folder exist for the same paper, prefer the source
  folder as the canonical raw asset and record the PDF path in metadata if it is
  kept locally

## Raw -> Markdown Conversion Rules

Do not create a separate `papers_md` template file. Instead, each Markdown
conversion should follow this section order:

1. `Title`
2. `Source Metadata`
3. `Paper Metadata`
4. `Abstract`
5. `Section Outline`
6. `Key Equations / Core Method`
7. `Figures And Tables Asset Index`
8. `Current-Round-Relevant Hooks`
9. `Conversion Caveats`

Input-type rules:

- `latex_source`: source equations are authoritative; preserve asset references
  and section structure directly from the source tree when possible
- `pdf`: preserve formulas in LaTeX blocks when recoverable; if recovery is
  uncertain, keep the structural method summary and record the uncertainty in
  `Conversion Caveats`
- `mixed`: use the source folder as the formula authority and the local PDF as a
  visual or metadata cross-check when useful

Formula policy:

- prioritize correctness over cleanliness
- critical formulas likely to influence `papers_processed` should be manually
  verified if parsing looks suspect
- if a formula remains uncertain, do not guess; summarize the role and mark the
  uncertainty explicitly

Figure policy:

- do not recreate figures
- for source folders, link raw assets and preserve captions when available
- for PDF-only papers, preserve figure index and captions, and note that the
  asset is embedded in the PDF only

Table policy:

- use Markdown tables only when extraction is clearly clean
- otherwise use fenced blocks or a structured summary
- never guess missing cells; fall back to a raw-reference note or caveat

## Markdown Usability QA Gate

Every `papers_md` file must record a fidelity label:

- `high`
- `medium`
- `needs_review`

Minimum QA before a Markdown conversion is usable downstream:

- title and author metadata are correct
- abstract or core method is captured
- all strategy-relevant formulas are verified or explicitly caveated
- figure and table inventory is captured or explicitly absent
- no obvious truncation or broken section structure remains
- fidelity is not `needs_review`

Only `usable` Markdown files should move into `papers_processed/`.

## Processed Paper Design

Processed papers are decision fichas, not academic summaries. Use this section
order:

1. `Paper Metadata`
2. `Core Claim`
3. `Assumptions`
4. `Problem Addressed for Round X`
5. `What This Paper Gives Us`
6. `Relevance To Current Round`
7. `Round X Mapping`
8. `Minimal Usable Adaptation`
9. `Strategy Implications`
10. `Do Not Overuse`
11. `Risks And Limitations`
12. `Action Classification`
13. `Strategy Hooks`
14. `Notes`

Required structure inside key sections:

- `What This Paper Gives Us`:
  `formula / approximation`, `constraints / checks`, `point of view`,
  `simplification`
- `Minimal Usable Adaptation`:
  `online-usable adaptation`, `required proxy or simplification`,
  `runtime / state caveat`, `implementability`

Classification stack:

- in `papers_processed`:
  `implementable | variant-only | validation-only | EDA-follow-up | inspiration-only`
- action classification:
  `new candidate | variant | validation check | EDA follow-up | no action`
- later in Strategy:
  `used | hybrid | validation | rejected | inspiration-only`

## Batching And Stop Rules

Process papers by ROI, not by file arrival order:

- `Batch 1`: papers that can change the first serious candidate family
  immediately; typical size `2-4`
- `Batch 2`: papers that change guardrails, regime posture, or validation logic
  for Batch 1 candidates; typical size `1-3`
- `Batch 3`: benchmark, utility, or second-layer variant papers; only process
  them if they still have a credible path to changing strategy/spec decisions

Stop rules:

- Strategy may start as soon as Batch 1 exists
- Batch 2 is only worth doing if it can still change thresholds, risk posture,
  or candidate ranking
- Batch 3 is only worth doing if it can still change candidate ranking, spec
  boundaries, or implementation quality
- stop 02b work for the current raw set when all current papers are processed or
  the remaining ones are clearly support-only and no longer decision-relevant

## Phase State Semantics

Use richer wait-state labels in the phase artifact:

- `prompt-generated-waiting`
- `shortlist-ready`
- `ready-to-convert`
- `ready-to-process`
- `partially-processed`
- `fully-processed`
- `explicitly-skipped`

Phase 02b is still considered operationally complete once at least one paper
exists in `papers_processed/`, but the artifact should still distinguish between
partially processed and fully processed local paper sets.

## Source Discipline

- Papers are idea sources, not official Prosperity facts.
- Current-round EDA, understanding, and reviewed specs remain the decision
  authority for round behavior.
- A paper may inspire a method, validation check, or failure-mode mitigation,
  but it cannot override contradictory current-round evidence.
- If a paper method is offline-only, too complex, or not practical for a simple
  `Trader`, mark it as `inspiration-only`, `validation check`, or `EDA
  follow-up` instead of forcing it into strategy candidates.
- Any paper-derived idea must map back to a current-round signal, feature,
  regime, or risk, or else remain explicitly exploratory / inspiration-only.

## Handoff To Strategy

Strategy generation should read `02b_external_paper_research.md` and
`research/papers_processed/` when present.

Strategy should always check `papers_processed/` when the folder exists. If no
processed papers exist yet, proceed data-driven rather than blocking on the
full paper pipeline.

Paper-derived ideas must be mapped back to:

- a current-round signal
- a promoted feature
- a regime or distribution hypothesis
- a known failure mode
- or an explicit open question from understanding

For each paper-derived idea, strategy should explicitly classify actual usage
as `used`, `hybrid`, `validation`, `rejected`, or `inspiration-only`.

Strategy should begin with a paper intake pass whenever processed papers exist:

- review which processed papers materially map to current-round signals, risks,
  open questions, or failure modes
- classify each materially relevant paper by actual use
- stop importing additional paper ideas once they stop changing candidate
  priority or validation posture

Strategy candidates should also record a source classification:

- `data-driven`
- `paper-inspired`
- `hybrid`
- `paper-rejected`

Paper-inspired ideas that are not implementable in a simple Trader should stay
tagged as `inspiration-only`, `validation`, or `EDA follow-up` rather than
entering the active candidate queue as normal bot logic.
