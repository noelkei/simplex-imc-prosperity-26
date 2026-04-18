# EDA Workspace

Use this folder for targeted EDA artifacts for this round.

EDA is optional only when skipped or deferred with an explicit reason in `_index.md` and `phase_01_eda_context.md`.

Required closure summary sections:

- Product scope
- Algorithmic vs manual scope
- Round Adaptation Check
- Data quality and filters
- Feature inventory
- Feature engineering notes
- Feature promotion decisions
- Facts
- Conditional patterns / regimes
- Threshold / execution findings, when decision-relevant
- Signal hypotheses
- Negative evidence for meaningful failed checks
- Open questions
- Reusable metrics
- Downstream use / agent notes

Do not treat sample data patterns, existing bots, or performance outputs as official rules.

Markdown is the canonical handoff. Optional notebooks may support human inspection, charts, exploratory code, or feature experiments, but downstream agents should be able to use the Markdown without rerunning EDA.
