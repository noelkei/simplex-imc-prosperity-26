# Synthesize Understanding

Use this skill to turn ingestion and EDA artifacts into a concise understanding summary that strategy, spec, implementation, variant, validation, and debugging agents can consume without redoing the analysis.

## Required sources

- Round state: `../rounds/round_X/workspace/_index.md`
- Ingestion: `../rounds/round_X/workspace/00_ingestion.md`
- EDA summaries: `../rounds/round_X/workspace/01_eda/`
- Post-run research memory, when present: `../rounds/round_X/workspace/post_run_research_memory.md`
- Phase context: `../rounds/round_X/workspace/phase_02_understanding_context.md`
- Template: `../docs/templates/understanding_template.md`
- Workflow: `../docs/prosperity_workflows/04_workstream_strategy.md`

## Steps

1. Read `_index.md`, ingestion, EDA summaries, and phase context before writing. If `../rounds/round_X/workspace/post_run_research_memory.md` exists, read it as an evidence input and cite relevant insight IDs or descriptions when they influence conclusions.
2. Preserve source labels: wiki fact, EDA evidence, playbook heuristic, hypothesis, assumption, and unknown.
3. Convert ingestion unknowns and EDA findings into evidence synthesis, confidence/impact, prioritized unknowns, and strategy implications.
4. Compress EDA Round Adaptation Checks into Assumptions Carried Forward. Do not promote prior-round assumptions unless current-round evidence supports them or the risk/action is explicit.
5. Prioritize the strongest EDA signals and downgrade or discard weak, contradictory, under-validated, or not-online-usable signals.
6. Identify actionable features/signals, high-confidence vs low-confidence areas, multivariate relationships, redundancy decisions, and process/regime assumptions that strategy agents must preserve. Use EDA statistical tests, effect sizes, confidence intervals, correlation/covariance, controlled relationships, redundancy/PCA notes, cross-product lead-lag evidence, change-point/regime evidence, process hypotheses, and negative evidence as confidence inputs when available; do not rerun broad research during synthesis.
7. Convert only promoted EDA features and relevant post-run memory insights into the `Signal Ledger`, including product, source artifact, feature basis, feature origin, online usability, role, stability, confidence, decision action, risk, and next phase action.
8. Require each retained signal to state whether it is a direct signal, execution filter, risk control, diagnostic, manual signal, or avoid/do-not-use item.
9. Fill `Multivariate Relationships Carried Forward`, `Redundancy Decisions`, and `Process Hypotheses Carried Forward` from EDA when those sections exist. Downgrade or defer signals that are redundant, offline-only without a proxy, process-dependent without validation, or contradicted by controlled/multivariate evidence.
10. Preserve meaningful intermediate findings in `Research Memory`: promising, rejected/noisy, and unresolved/log-needed. Carry forward negative evidence so strategy agents do not rediscover weak ideas.
11. Carry forward product-level opportunity, uncertainty, and risk in `Product Attribution View`.
12. Produce a `Cross-Product Verdict` when multiple products exist: `useful`, `weak`, `not applicable`, or `needs targeted EDA`.
13. Convert each retained signal into a decision label: try, avoid, validate next, defer, or treat as an assumption.
14. Fill `Strategy-Relevant Insights`, `What Should Be Tried`, `What Should Not Be Trusted Yet`, and `Open Risks And Unknowns`.
15. Do not duplicate full EDA reports; link them and summarize only decision-useful conclusions.
16. Do not rerun broad EDA during synthesis. If EDA is insufficient, record the gap and route only high-impact unresolved questions back to phase 01.
17. Prefer fewer clear, reusable insights over many unclear findings.
18. Do not use `non-canonical/` drafts unless the user explicitly points to one; if useful, summarize the relevant point as a labeled assumption or question.
19. If a high-impact unknown blocks strategy selection, set the phase or blocker accordingly and propose targeted EDA or clarification.
20. Update `../rounds/round_X/workspace/02_understanding.md`, `_index.md`, and `phase_02_understanding_context.md`.
21. Handoff with signal ledger, research memory, product attribution, cross-product verdict, multivariate relationships, redundancy decisions, process hypotheses, feature origin/usability/role/status, what to use, what not to trust yet, what strategy directions are implied, what validation is needed, and the next priority action.
