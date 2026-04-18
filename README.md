# simplex-imc-prosperity-26

This repository supports a small team building Prosperity trading bots under a tight round deadline. Use it as a workflow system, not as a collection of isolated `.py` files.

If you are new here, start with this README, then open the relevant round folder under `rounds/round_X/`. The live control panel for a round is `rounds/round_X/workspace/_index.md`.

## Environment Setup

Use a project-local virtual environment for EDA, research, notebooks, validation, and development scripts. Do not rely on a global Anaconda/pyenv environment.

Required Python version: Python 3.11.x.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Optional notebook kernel:

```bash
python -m ipykernel install --user --name simplex-imc-prosperity-26 --display-name "simplex-imc-prosperity-26"
```

This environment is for repo research work only. EDA, understanding synthesis, strategy research, plotting, notebooks, replay analysis, validation, and debugging scripts may use the packages in `requirements.txt`.

Prosperity bot submissions must remain platform-compatible. Do not import repo-only research dependencies in uploadable `Trader` files unless the official Prosperity runtime docs explicitly allow them. Keep the existing feature lifecycle rule: EDA-only features must not enter a bot unless a reviewed spec defines an online-usable proxy.

The research stack is a toolbelt, not a checklist. Use these libraries when they improve signal validation, regime detection, feature engineering, fill analysis, or handoff clarity; skip them when a simple table or standard-library script answers the decision.

## Quick Start

1. Read the source hierarchy below so you know what is authoritative.
2. Open the relevant round README, for example `rounds/round_1/README.md`.
3. Open `rounds/round_X/workspace/_index.md` to see the current phase, product scope, blockers, active strategies, active implementations, and next priority action.
4. Use the relevant phase context file as the short resumption note.
5. If you are only drafting personal ideas, use `non-canonical/<member>/` and do not treat that work as formal evidence until it is moved or summarized into `rounds/round_X/`.

## Current Repository State

The active round `_index.md` is the live source of truth. Do not rely on this
README for current phase status, blockers, active candidates, latest PnL, or
final submission decisions.

## Source Hierarchy

- `docs/prosperity_wiki/`: operational factual source for API contracts, datamodel fields, exchange mechanics, position limits, runtime constraints, platform flow, round facts, and caveats.
- `docs/prosperity_wiki_raw/`: underlying factual base for curating and checking the operational wiki.
- `docs/prosperity_playbook/`: heuristic guidance for strategy framing, risk habits, debugging, and iteration.
- `docs/prosperity_workflows/`: process guidance for team and agent work.
- `rounds/`: formal round-local execution workspaces, bots, data, and performance summaries.
- `workstreams/round_template/`: reusable scaffold for creating or repairing round workspaces.
- `non-canonical/`: informal personal scratch space outside the formal workflow.

Do not infer products, limits, signs, runtime behavior, or manual mechanics from round-local bots, performance outputs, or `non-canonical/` drafts.

## Formal And Informal Work

Formal work belongs in `rounds/round_X/`. This includes reviewed phase artifacts, EDA summaries, strategy candidates, specs, bot candidates, run summaries, debugging notes, and final submission state.

Informal work belongs in `non-canonical/<member>/`. It is allowed, but it is not evidence, not source of truth, not a reference implementation, and not part of the official workflow. Agents should ignore it unless the user explicitly points to a file there.

## 2 Day Workflow

Every round should run through the same phases, but under a 2 day constraint the depth is controlled:

1. Round ingestion.
2. Minimal EDA, or an explicit "EDA skipped with reason."
3. Research / understanding summary.
4. Strategy generation and shortlist.
5. Reviewed strategy specification.
6. Implementation.
7. Testing / performance analysis.
8. Debugging / iteration.
9. Final submission decision.

Mandatory gates:

- No implementation without an approved strategy spec or an explicit `deferred under deadline` review decision.
- No final submission without a readable validation or performance summary.
- No phase is complete if facts, hypotheses, assumptions, and evidence are mixed together.
- No stale prior-round assumption moves forward unless current-round evidence supports it or the risk is explicitly labeled.
- Round-specific mechanics and changed online fields must be implemented, excluded, marked not applicable, or blocked in the reviewed spec before coding.

## Round Folders

Round folders are pre-created:

```text
rounds/round_1/
rounds/round_2/
rounds/round_3/
rounds/round_4/
rounds/round_5/
```

Each round has:

```text
rounds/round_X/
  README.md
  workspace/
  bots/
    <member>/
      canonical/
      historical/
  performances/
    <member>/
      canonical/
      historical/
  data/
```

Start with `rounds/round_X/README.md`, then open `rounds/round_X/workspace/_index.md`.

The `_index.md` file tracks phase status, active strategies, active implementations, latest results, blockers, and the next priority action. Agents should read it first when continuing a round.

Reusable artifact templates live in:

```text
docs/templates/
```

`workstreams/round_template/` is the scaffold used to create or repair round workspaces. Do not put active round work there.

Repo task skills live in:

```text
skills/
```

Use them as phase-specific operating guides after reading the relevant workflow:

| Task | Skill |
| --- | --- |
| New round setup | `skills/add_new_round.md` |
| Round ingestion | `skills/analyze_round.md` |
| EDA | `skills/run_eda.md` |
| Understanding synthesis | `skills/synthesize_understanding.md` |
| Strategy candidates / shortlist | `skills/generate_strategy_candidates.md` |
| Strategy specs / implementation readiness | `skills/write_strategy_spec.md` |
| Trader implementation | `skills/create_trader.md` |
| Validation/run summaries | `skills/validate_trader.md` |
| Debugging | `skills/debug_trader.md` |
| Controlled variants | `skills/generate_trader_variant.md` |
| Phase state sync / drift repair | `skills/manage_phase_state.md` |

`skills/develop_strategy.md` is a deprecated compatibility wrapper. Use
`skills/generate_strategy_candidates.md` for candidate work and
`skills/write_strategy_spec.md` for implementation-ready specs.

Use `skills/manage_phase_state.md` when starting, resuming, or closing a phase, or when status, blocker, review state, artifact link, or next-action drift appears across the round index, phase context, and main artifact.

Each phase also has a short context file:

```text
rounds/round_X/workspace/phase_YY_<phase>_context.md
```

These files are resumption notes. Update them whenever work is added, decisions change, a phase status changes, implementation affects understanding, performance changes priorities, or debugging changes the next action.

## Artifact Locations

| Need | Location |
| --- | --- |
| Official facts | `docs/prosperity_wiki/` |
| Raw factual source archive | `docs/prosperity_wiki_raw/` |
| Heuristic strategy/process advice | `docs/prosperity_playbook/` |
| Process guidance | `docs/prosperity_workflows/` |
| Reusable artifact templates | `docs/templates/` |
| Live round state | `rounds/round_X/workspace/_index.md` |
| Phase resumption notes | `rounds/round_X/workspace/phase_YY_<phase>_context.md` |
| Round data | `rounds/round_X/data/` |
| Post-run research memory | `rounds/round_X/workspace/post_run_research_memory.md` |
| Formal bot candidates | `rounds/round_X/bots/<member>/canonical/` |
| Archived bot attempts | `rounds/round_X/bots/<member>/historical/` |
| Current run evidence | `rounds/round_X/performances/<member>/canonical/` |
| Archived run evidence | `rounds/round_X/performances/<member>/historical/` |
| Personal scratch work | `non-canonical/<member>/` |

## How To Know Where We Are

Open `rounds/round_X/workspace/_index.md` and read:

- `Current Next Priority Action`
- `Phase Status`
- `Product Scope`
- `Blockers And Decisions Needed`
- `Active Strategies`
- `Active Implementations`
- `Final Submission Status`

If the relevant official round facts file under `docs/prosperity_wiki/rounds/` does not exist yet, keep that round `NOT_STARTED` and do not invent facts in `rounds/`.

## Advancing A Phase

Use the phase status table in `_index.md`:

- `NOT_STARTED`: no usable work exists yet.
- `IN_PROGRESS`: an owner is actively producing the artifact.
- `BLOCKED`: progress needs missing data, source clarification, platform/run access, or a human decision.
- `READY_FOR_REVIEW`: the artifact exists and the owner believes exit criteria are met.
- `COMPLETED`: review is done, or review deferral is explicitly recorded under deadline pressure.

Review outcomes are `not reviewed`, `approved`, `approved with caveats`, `changes requested`, or `deferred under deadline`.

Do not mark a phase `COMPLETED` while review is pending, recommended, or unassigned. Do not mark a phase `COMPLETED` unless the next phase can use its outputs without reinterpretation and status is synchronized across `_index.md`, the phase context, and the main phase artifact. If a phase is skipped or compressed, record the reason in both `_index.md` and the phase context.

## Closing Work Cleanly

Before leaving a task or closing a phase:

- Confirm the required artifact exists or the deferral is explicit.
- Confirm review outcome is recorded when closure depends on review.
- Confirm `_index.md`, the phase context, and the main phase artifact agree on status, blocker, artifact link, and next action.
- Update `_index.md` with status, blockers, active candidates, latest results, or final submission state as relevant.
- Update the matching phase context with what changed, decisions made, open questions, and next action.
- Link sources and artifacts rather than relying on memory.
- Mark the phase `READY_FOR_REVIEW`, `COMPLETED`, or `BLOCKED`; ask for human review when direction, risk, priority, or submission readiness changes.

## Time Budget

For a roughly 48 hour round-to-submission window:

- Hours 0-3: round ingestion and `_index.md` setup.
- Hours 3-10: targeted EDA only for questions likely to affect bot behavior.
- Hours 10-14: understanding summary and bounded strategy generation.
- Hours 14-20: shortlist and write 1-2 implementation-ready specs.
- Hours 20-32: implement and validate first candidates.
- Hours 32-42: debug and iterate on the best 1-2 candidates.
- Hours 42-46: freeze feature work, run final validation, choose active submission.
- Hours 46-48: submit, verify active file, document final state.

Stop exploring when there is enough evidence for 1-2 plausible specs, EDA is no longer changing decisions, less than 24 hours remain, or implementation/validation is the bottleneck.

Stop iterating when less than 6 hours remain, the best candidate is rule-valid and better than baseline by available evidence, remaining issues are strategy uncertainty rather than correctness, or new changes would not get enough validation time.

## Typical Prompts

Use prompts like these with Codex or Claude:

```text
Start round X.
Start round ingestion for Round X.
Start targeted EDA for Round X using the current round index.
Synthesize understanding for Round X from ingestion and EDA.
Continue strategy generation and shortlist candidates.
Generate strategy candidates for Round X.
Write a strategy spec for candidate Y.
Implement candidate Y from its reviewed spec.
Analyze performance of candidate Y run Z.
Debug issue Q from run Z.
Close EDA phase if the exit criteria are met.
Show me the next priority action for Round X.
Prepare final submission decision.
Generate a controlled variant for candidate Y.
```

## Agent Behavior

Agents should guide the work:

- Use `rounds/round_X/workspace/_index.md` for live round state.
- If a round workspace is missing or damaged, use `workstreams/round_template/` rather than inventing a workspace shape.
- Read `_index.md`, the relevant phase context, wiki facts, and the task-specific workflow before acting.
- Report missing artifacts and suggest the smallest useful next action.
- Preserve the source hierarchy and label facts, evidence, heuristics, hypotheses, and assumptions.
- Ask for human decisions on strategy shortlist, spec approval, deadline tradeoffs, and final submission choice.
- Redirect attempts to skip mandatory strategy spec or validation gates.
- Update `_index.md` and the relevant phase context when status or priority changes.

Agents should proceed without asking when the next step is determined by the repo state, such as creating a missing context file from the template or summarizing a linked artifact. Agents should ask when a choice changes strategy direction, prioritization, risk appetite, review approval, or final submission selection.

## Phase Guidance

| Phase | User provides | Agent produces | Done when |
| --- | --- | --- | --- |
| Round ingestion | Active round or source material | Products, limits, algorithmic/manual split, caveats | Reviewed ingestion context, Round Mechanics Delta, and `_index.md` links |
| EDA | Data/log path and question | Reproducible outputs and summary | Product scope, Round Adaptation Check, data quality, feature lifecycle, signal hypotheses, open questions, reusable metrics, and downstream agent notes are clear |
| Understanding | Reviewed ingestion and EDA | Evidence-aware market understanding | Strategy-relevant insights, signal ledger, research memory, assumptions carried forward, risks, and candidate implications are clear |
| Strategy generation | Priorities and risk appetite | Grouped candidates and shortlist | 1-3 non-duplicative candidates are selected, feature budget is respected, and Round Coverage Check is addressed |
| Strategy specification | Shortlisted candidate | Implementation-ready spec | Signal, execution, risk, state, Feature Contract, Round-Specific Mechanics Contract, validation checks, and evidence traceability are defined, with review outcome recorded |
| Implementation | Approved or deadline-deferred spec | Bot implementation | Contract, signs, limits, runtime/imports, Feature Contract, Round-Specific Mechanics Contract, and spec alignment are checked |
| Testing | Bot, spec, run artifact | Run summary | Results link bot, spec, raw run, metrics, limits, run classification, ROI-gated memory action, and next action |
| Debugging | Issue or suspicious run | Classified debugging note | Reproduction, expected vs observed behavior, linked spec/run, classification, and next action are present |

## Fast Mode

Use fast mode when less than 24 hours remain, exploration is no longer the bottleneck, or the team needs a valid candidate quickly.

- EDA: one or two targeted questions only.
- Strategy generation: max 3-5 candidates; shortlist 1-2.
- Spec: one page is acceptable if signal, execution, risk, state, and validation checks are clear.
- Implementation: one primary candidate plus one fallback/baseline at most.
- Testing: fastest meaningful validation first, with raw output and a short summary.
- Debugging: fix rule, contract, and limit bugs before speculative tuning.
- Freeze: with less than 6 hours left, only correctness fixes or extremely low-risk parameter changes.

Fast mode does not relax source hierarchy, strategy spec requirement, Trader contract, position-limit checks, review outcome recording, or final validation summary.

## Performance Artifacts

Raw `.log` files are ignored by the repository by default. Preserve platform
`.json`, exact bot path, and a tracked run summary under
`rounds/round_X/performances/<member>/canonical/`; keep the matching `.log`
with the run when possible, or record a provenance caveat if it is unavailable
or untracked. Archive superseded evidence under
`rounds/round_X/performances/<member>/historical/`, using
`docs/templates/run_summary_template.md`.

When a platform run adds reusable learning, update
`rounds/round_X/workspace/post_run_research_memory.md` from
`docs/templates/post_run_research_memory_template.md`. If the run teaches
nothing new, mark `ROI-gated memory action: no update` in the run summary.

## Trader Production Readiness

Use `docs/templates/trader_production_template.md` before treating a bot as submission-ready. It contains the minimal `Trader` skeleton, submission readiness checklist, contract smoke-check guidance, and Round Adaptation Smoke Check.
