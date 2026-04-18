# EDA Workspace

Use this folder for targeted EDA artifacts for this round.

EDA is optional only when skipped or deferred with an explicit reason in `_index.md` and `phase_01_eda_context.md`.

## Round 2 Starting Points

Useful first questions:

- Compare Round 2 sample data against Round 1 behavior for `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Estimate whether extra market access could add enough incremental PnL to justify a Market Access Fee bid.
- Analyze the manual Research / Scale / Speed budget problem under multiple Speed rank assumptions.
- Preserve the distinction between official round facts, sample-data evidence, and strategy assumptions.

Decision-support script:

```bash
python rounds/round_2/workspace/01_eda/round_2_decision_tools.py manual-grid
python rounds/round_2/workspace/01_eda/round_2_decision_tools.py maf-grid
```

Required closure summary sections:

- Facts
- Patterns observed
- Hypotheses
- Open questions
- Reusable metrics
- Downstream use

Do not treat sample data patterns, existing bots, or performance outputs as official rules.
