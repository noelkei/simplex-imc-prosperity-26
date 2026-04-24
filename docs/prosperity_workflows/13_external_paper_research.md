# Workstream: External Paper Research

External paper research is a lightweight bridge between understanding and
strategy generation. It turns current-round evidence into a prompt for an
external AI with internet or deep-research capability, waits for human-uploaded
paper files, and distills those papers into strategy-useful summaries.

This workflow does not fetch papers itself. It does not browse the internet,
hallucinate paper contents, or treat papers as official truth.

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
- A concise list of target research questions tied to current-round evidence.
- A clear wait state pointing to `rounds/round_X/research/papers_raw/`.
- Incremental Markdown conversions for newly uploaded raw papers.
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

The prompt footer should instruct the human to upload selected PDFs into
`rounds/round_X/research/papers_raw/` and then resume the raw -> md ->
processed pipeline.

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

- `papers_raw/`: human-uploaded PDFs or source files
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

## Source Discipline

- Papers are idea sources, not official Prosperity facts.
- Current-round EDA, understanding, and reviewed specs remain the decision
  authority for round behavior.
- A paper may inspire a method, validation check, or failure-mode mitigation,
  but it cannot override contradictory current-round evidence.
- If a paper method is offline-only, too complex, or not practical for a simple
  `Trader`, mark it as `inspiration only`, `validation check`, or `EDA
  follow-up` instead of forcing it into strategy candidates.
- Any paper-derived idea must map back to a current-round signal, feature,
  regime, or risk, or else remain explicitly exploratory / inspiration-only.

## Processed Paper Expectations

Each processed paper summary should extract:

- title / source / link if known
- core method or idea
- assumptions
- problem solved
- relevance to current-round signals or risks
- possible strategy implications
- possible simple-Trader adaptation
- risks / limitations
- action classification: `new candidate`, `variant`, `validation check`, `EDA
  follow-up`, or `no action`

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

Strategy candidates should also record a source classification:

- `data-driven`
- `paper-inspired`
- `hybrid`
- `paper-rejected`

Paper-inspired ideas that are not implementable in a simple Trader should stay
tagged as `inspiration-only`, `validation`, or `EDA follow-up` rather than
entering the active candidate queue as normal bot logic.
