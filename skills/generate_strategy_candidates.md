# Generate Strategy Candidates

Use this skill to generate, prioritize, reject, or defer strategy candidates
from existing ingestion, EDA, and understanding evidence.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Phase context: `../rounds/round_X/workspace/phase_03_strategy_context.md`
- Understanding: `../rounds/round_X/workspace/02_understanding.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Candidates: `../rounds/round_X/workspace/03_strategy_candidates.md`
- Candidate template: `../docs/templates/strategy_candidates_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Responsibilities

- Own phase 03 strategy candidate work.
- Read `../rounds/round_X/workspace/post_run_research_memory.md` when it exists before branching or pruning; use it as evidence input and cite relevant insights in `Decision Trace` when they influence selection.
- When post-run memory includes a Run Knowledge Index, check tested strategy families, changed axes, tested features/signals, knowledge deltas, and memory actions before adding a new branch.
- Read the Understanding Assumptions Carried Forward and EDA Round Adaptation Check before branching. Fill Round Coverage Check for current-round mechanics, fields, or product behaviors that could affect candidate selection.
- Consume existing understanding, EDA summaries, and candidates before adding new ideas.
- Generate only non-duplicative candidates tied to linked EDA signals, feature evidence, regime assumptions, understanding insights, playbook heuristics, or explicit strategy assumptions.
- Use EDA process/distribution hypotheses as strategy-family evidence when available; for example, mean-reverting evidence should support mean-reversion candidates, while trending or regime-switching evidence should shape momentum, threshold, defensive, or validation logic.
- Use EDA multivariate evidence to decide whether features are independent, redundant, controlled by spread/depth/regime, or cross-product useful. Reject candidates that stack redundant features unless the decision trace explains why the extra feature changes behavior.
- Start with an exploration board when evidence supports more than one plausible direction; keep these as conceptual branches, not active strategies.
- Generate conceptual branches by product or source of edge before prioritizing.
- Evaluate multi-product combinations conceptually when relevant, including compatibility, risk interaction, execution alignment, and cross-product dependency.
- Use post-run failure patterns, edge decomposition, counterfactual backlog, and negative evidence when present to prune weak branches and prioritize high-ROI candidates.
- Enforce the feature budget for each serious candidate: at most one primary edge feature or fair-value model, up to two supporting execution/risk filters, plus diagnostics that do not change decisions.
- Treat outputs from `arch`, `ruptures`, `sklearn`, `pingouin`, `statsmodels`, PCA/loadings, clustering, mutual information, or notebooks as evidence for simpler trading decisions, not as a reason to add offline model complexity. If a candidate relies on a research-only feature, latent state, PCA component, or cluster label, require an online proxy or route it back to EDA/spec before implementation.
- Require each serious candidate to link `feature -> signal -> decision -> expected edge -> validation check`.
- Reject or defer feature-dump candidates, candidates that depend on non-online-usable features without an online proxy, candidates whose features are weak or contradictory, and candidates whose feature set does not target a known opportunity or failure mode.
- Keep facts, EDA evidence, understanding insights, playbook heuristics, hypotheses, and assumptions separate.
- Score serious candidates using evidence strength, implementation cost, validation speed, risk level, expected upside, and priority.
- Record rejected or deferred alternatives and why they were pruned.
- Prune candidates whose family/axis/feature combination was already tested and marked `duplicate`, `tested-reject`, `discard`, or `superseded`, unless new evidence makes the retest decision-relevant.
- Reject or defer candidates that rely on prior-round product behavior, fair values, limits, or mechanics without current-round evidence.
- Prefer high-ROI Counterfactual Backlog items with `untested` or worth-retesting status when they have a clear falsification check and match the current champion weakness.
- Record a decision trace for serious and prioritized candidates: signals used,
  alternatives rejected or deferred, reason selected, role, priority tier, and
  caveat.
- Include why each prioritized candidate is not feature dumping.
- Fill multivariate evidence, process hypothesis, redundancy note, and online proxy fields for serious candidates. Mark `not checked` only when the source EDA does not contain the evidence and the gap is not worth reopening.
- Apply the exploration stop rule before writing specs; stop when more branches
  are duplicate, weak, unimplementable, unlikely to change the prioritized
  candidate queue, blocked by implementation/validation bottlenecks, dominated
  by a strong incumbent, or constrained by deadline pressure.
- Ask a lightweight human checkpoint only when the answer materially affects
  prioritization, risk appetite, product priority, or final submission posture;
  record the default if there is no answer.
- Keep all non-duplicative high-ROI candidates in `_index.md` or linked from it;
  use role, priority tier, and implementation wave instead of a hard count cap.
- Reject or defer only weak, duplicate, unsupported, non-online-usable, or
  low-ROI ideas, and record the reason plus evidence gap or risk.
- Update `../rounds/round_X/workspace/03_strategy_candidates.md`, `_index.md`, and `phase_03_strategy_context.md`.

## Boundaries

- Do not write implementation-ready specs.
- Do not mark spec review status.
- Do not hand off implementation directly.
- Do not implement combinations from the exploration board or compatibility
  matrix; they must first become prioritized candidates and then reviewed specs.
- Do not create candidates from scratch when EDA or understanding exists. If evidence is missing, label the gap and route it to targeted EDA when it could change the decision.
- Do not use `non-canonical/` drafts as evidence unless the user explicitly
  points to one; convert useful draft ideas into labeled assumptions before
  prioritizing.

## Handoff

Pass prioritized candidate IDs, evidence links, decision trace, priority
rationale, risks, stop-rule reason, and unresolved unknowns to
`skills/write_strategy_spec.md`.
