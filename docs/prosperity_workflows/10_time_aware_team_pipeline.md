# Time-Aware Team Pipeline

This workflow addendum makes the existing Prosperity process usable under a roughly 2 day round-to-submission deadline. It does not replace the workstream docs; it controls time, state, and handoffs across them.

## Mandatory Gates

Every round still passes through:

1. Round ingestion.
2. EDA, or an explicit "EDA skipped with reason."
3. Research / understanding.
4. Strategy generation and shortlist.
5. Strategy specification.
6. Implementation.
7. Testing / performance analysis.
8. Debugging / iteration.
9. Final submission decision.

Required gates:

- No implementation without a reviewed strategy spec.
- No final submission without a readable validation or performance summary.
- No phase is complete if facts, hypotheses, assumptions, and evidence are mixed together.
- No stale prior-round assumption may move forward unless current-round evidence supports it or the risk is explicitly labeled.
- Round-specific mechanics, Trader methods, and changed fields must be implemented, excluded, marked not applicable, or blocked in the spec before coding.
- Round-local member-owned bot/performance folders remain non-authoritative execution artifacts; removed top-level `bots/` and `performances/` must not be recreated.
- `non-canonical/` can hold personal drafts, but it is outside this pipeline until useful content is moved or summarized into a formal round artifact.

## Time Budget

For a 48 hour window:

- Hours 0-3: round ingestion and `_index.md` setup.
- Hours 3-10: targeted EDA only for questions likely to affect bot behavior.
- Hours 10-14: understanding summary and bounded strategy generation.
- Hours 14-20: shortlist and write 1-2 implementation-ready specs.
- Hours 20-32: implement and validate first candidates.
- Hours 32-42: debug and iterate on the best 1-2 candidates.
- Hours 42-46: freeze feature work, run final validation, choose active submission.
- Hours 46-48: submit, verify active file, document final state.

Stop exploring when one of these is true:

- There is enough evidence for 1-2 plausible specs.
- EDA is no longer changing decisions.
- Less than 24 hours remain.
- Implementation or validation is the bottleneck.

Stop iterating when one of these is true:

- Less than 6 hours remain.
- The best candidate is rule-valid and better than baseline by available evidence.
- Remaining issues are strategy uncertainty rather than correctness.
- New changes would not get enough validation time.

Strong-incumbent rule:

- Once a platform-validated candidate is above the current target, treat it as the champion and stop broad exploration.
- New bots should be challengers with one clear improvement axis and practical ROI.
- A challenger replaces the champion only if it has better real platform PnL, or slightly lower PnL with materially better robustness.
- If the robustness gain is small, keep the higher-PnL champion.
- Near deadline, prioritize final validation, artifact preservation, and active-file verification over new complexity.

## Complexity Limits

- Keep at most 3 active strategy candidates per round.
- Keep at most 2 implementation candidates in active testing.
- Keep one baseline/reference bot separate from active candidates.
- Treat broad idea generation as optional. Default to 5-8 ideas, and use 10-20 only when the team explicitly needs breadth.
- Converge to 1-3 shortlisted candidates before strategy specification.
- Do not create a new strategy candidate for a parameter tweak unless it materially changes signal, execution, or risk behavior.

## Phase Statuses

Use these statuses in each round index:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `READY_FOR_REVIEW`
- `COMPLETED`

Review outcomes:

- `not reviewed`
- `approved`
- `approved with caveats`
- `changes requested`
- `deferred under deadline`

Transitions:

- `NOT_STARTED -> IN_PROGRESS`: an owner begins work and creates or updates the phase context file.
- `IN_PROGRESS -> BLOCKED`: missing artifact, source conflict, human decision, or platform/run access blocks useful progress.
- `BLOCKED -> IN_PROGRESS`: blocker is resolved or explicitly accepted as an assumption or risk.
- `IN_PROGRESS -> READY_FOR_REVIEW`: required artifact exists and owner believes exit criteria are met.
- `READY_FOR_REVIEW -> COMPLETED`: reviewer approves, approves with caveats, or review is explicitly deferred under deadline pressure.
- `COMPLETED -> IN_PROGRESS`: allowed only if new round facts, new EDA evidence, implementation behavior, or performance/debug results materially change the phase.

Do not mark a phase `COMPLETED` while review is merely recommended, unassigned, or pending. Use `READY_FOR_REVIEW` until a review outcome is recorded.

General completion rule: outputs must be usable without reinterpretation, facts and hypotheses must be labeled, artifacts must be non-duplicative, links must be present in `_index.md`, statuses must match across `_index.md`, phase context, and the main artifact, and downstream work must be able to proceed without rework.

Phase-specific completion:

- Ingestion: products, limits, algorithmic/manual split, caveats, and Round Mechanics Delta reviewed.
- EDA: product scope, Round Adaptation Check, data quality, feature inventory/lifecycle, feature promotion decisions, signal hypotheses, open questions, and downstream agent notes are clear.
- Understanding: EDA evidence, promoted signals, rejected/unresolved research memory, assumptions carried forward, open risks, and candidate implications are compressed.
- Strategy generation: 1-3 shortlisted candidates selected, feature budget respected, and Round Coverage Check addressed.
- Strategy spec: at least one reviewed implementation-ready spec exists with Feature Contract and Round-Specific Mechanics Contract.
- Implementation: bot maps to a reviewed spec and passes contract/rule plus round adaptation checks.
- Testing/performance: readable run summary links bot, spec, raw run, metrics, limits, run classification, and ROI-gated memory action.
- Debugging: issue has reproduction, expected vs observed behavior, linked spec/run, classification, and next action.

## Data Arrival Rule

When raw data, logs, or run artifacts arrive after ingestion has already started or closed:

- update the ingestion artifact's data availability and stale unknowns
- update the relevant phase context blockers and next action
- update `_index.md` blockers, recently changed artifacts, and current next priority action
- update the round data or performance README if it previously said no artifacts existed
- keep data observations labeled as EDA evidence, not official wiki facts

Do this before or during EDA so downstream phases do not inherit obsolete "no data" blockers.

## Phase Context Files

Each active round should contain:

```text
rounds/round_X/workspace/phase_00_ingestion_context.md
rounds/round_X/workspace/phase_01_eda_context.md
rounds/round_X/workspace/phase_02_understanding_context.md
rounds/round_X/workspace/phase_03_strategy_context.md
rounds/round_X/workspace/phase_04_spec_context.md
rounds/round_X/workspace/phase_05_implementation_context.md
rounds/round_X/workspace/phase_06_testing_context.md
rounds/round_X/workspace/phase_07_debugging_context.md
```

Required sections:

- Status
- Owner / reviewer
- Last updated
- What has been done
- Current findings
- Decisions made
- Open questions / blockers
- Linked artifacts
- Next priority action
- Deadline risk

Update the relevant context file whenever new work is added, a human decision changes direction, a phase status changes, implementation contradicts the spec, performance changes prioritization, or debugging changes understanding.

Keep context files short. They are resumption notes, not full reports.

## Round Index

`rounds/round_X/workspace/_index.md` is the round control panel. It must allow a human to understand the project in under 1 minute and an agent to resume without rereading everything.

Required sections:

- Round and deadline.
- Current next priority action.
- Phase status table with phase, status, owner, reviewer, artifact link, and blocker.
- Product scope.
- Active strategies, max 3.
- Active implementations, max 2.
- Baseline/reference bot, if any.
- Historical / non-decision artifacts, if any exist and could confuse active state.
- Latest results and best current candidate.
- Post-run research memory link, if present and decision-relevant.
- Blockers and decisions needed.
- Final submission status: candidate, file, last validation, active-file verification.
- Recently changed artifacts.

Agents should update `_index.md` after any phase closure, shortlist change, implementation candidate change, performance result, blocker, or final submission decision.

## Agent Behavior

Agents act as guides, not passive executors.

Before work:

- Read `_index.md` when it exists.
- Read the relevant phase context.
- Read wiki facts and the task-specific workflow.
- Report missing artifacts and propose a bounded next action.

During work:

- Keep changes small.
- Preserve fact/hypothesis separation.
- Update phase context.
- Ask for human decisions when direction, prioritization, shortlist, spec approval, deadline tradeoff, or final submission choice matters.

When asked to skip ahead:

- Allow safe compression.
- Do not skip mandatory strategy spec or validation gates.
- In fast mode, a one-page strategy spec is acceptable if signal, execution, risk, state, and validation checks are clear.

When blocked:

- Classify the blocker as missing data, source conflict, human prioritization, implementation uncertainty, platform artifact missing, or deadline tradeoff.
- Suggest the smallest useful unblock.

Before closing a phase:

- Check exit criteria.
- Check status is synchronized across `_index.md`, phase context, and the main artifact.
- Check blocker and next-action text is not stale.
- Check artifact links point to files that exist, or record the missing artifact as a blocker.
- Record review outcome as `not reviewed`, `approved`, `approved with caveats`, `changes requested`, or `deferred under deadline`.
- Update `_index.md` and the relevant phase context.
- Mark the phase `READY_FOR_REVIEW`, `COMPLETED`, or `BLOCKED`, or record a deadline-mode deferral.
- Request human review when closure changes direction, priority, risk, or submission readiness.

## Fast Mode

Use fast mode when less than 24 hours remain, exploration is no longer the bottleneck, or the team needs a valid candidate quickly.

Rules:

- EDA: one or two targeted questions only; no broad chart suite unless already available.
- Strategy generation: max 3-5 candidates; shortlist 1-2.
- Spec: one page is acceptable if it includes signal, execution, risk, state, and validation checks.
- Implementation: one primary candidate plus one fallback/baseline at most.
- Testing: run the fastest meaningful validation first; store raw output and a short summary.
- Debugging: fix rule/contract/limit bugs first; defer speculative tuning unless it is clearly high impact.
- Freeze: with less than 6 hours left, only fix correctness issues or extremely low-risk parameter changes, then validate, verify the active upload file, and submit.

Fast mode does not relax source hierarchy, strategy spec requirement, Trader contract, position-limit checks, or final validation summary.
