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

## Current Canonical EDA

The single canonical Round 2 EDA handoff for Understanding is available at:

```text
eda_round2_fresh.md
```

It is consolidated: first-pass data quality/product/MAF/manual evidence plus
multivariate, redundancy, cross-product, process/distribution, PCA, MI,
clustering, and controlled-regression evidence.

Reproduce the consolidated report with:

```bash
.venv/bin/python rounds/round_2/workspace/01_eda/eda_round2_consolidated.py
```

The first-pass base EDA script remains available for provenance:

```bash
.venv/bin/python rounds/round_2/workspace/01_eda/eda_round2_fresh.py
```

Supporting tables and plots are under:

```text
artifacts/
```

## Historical / Unreviewed Outputs

Pre-kickoff EDA outputs from an earlier test run were archived at:

```text
historical/2026-04-19_unreviewed_pre_kickoff_eda/
```

Do not treat those files as active Round 2 evidence unless they are explicitly
reviewed or rerun. Fresh/consolidated EDA should write new active artifacts in this folder.

Required closure summary sections:

- Facts
- Patterns observed
- Hypotheses
- Open questions
- Reusable metrics
- Downstream use

Do not treat sample data patterns, existing bots, or performance outputs as official rules.
