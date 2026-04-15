# EDA Summary Template

EDA turns named data or run artifacts into evidence. Do not turn sample patterns, bot behavior, or performance outputs into official Prosperity rules.

## Status

`NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | COMPLETED`

## Question

- Question:
- Product scope:
- Why this matters downstream:

## Product Scope

| Product | Present In Data | Usable Evidence | Likely Trader Scope | Decision |
| --- | --- | --- | --- | --- |
| PRODUCT | yes / no | yes / no / partial | likely / possible / no / unknown | include / defer / exclude / investigate |

- Product-scope rationale:
- Product branches, if any:

## Data Sources

- Raw data:
- Processed data:
- External context:
- Run or log artifact:

## Data Quality And Filters

- Row counts by file and product:
- Timestamp coverage and gaps:
- Missing bid/ask counts, if order books are used:
- Zero or blank `mid_price` counts, if mid prices are used:
- Filters applied:
- Findings based on: `raw rows | filtered rows | mixed, explain`
- Data quality caveats:

## Feature Inventory

Use [`docs/prosperity_workflows/11_dataset_eda_framework.md`](../prosperity_workflows/11_dataset_eda_framework.md) as the checklist.

Include raw features and derived features created during EDA. Keep this compact; detail features that could change a downstream decision.

| Feature | Source | Meaning | Classification | Strategy Use | Stability | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- |
| FEATURE | raw / derived | MEANING | predictive / descriptive / execution/risk / noisy / unknown | HOW_TO_USE_OR_AVOID | stable / regime-dependent / unknown | NOTES |

## Feature Engineering Notes

Target simple, hypothesis-driven transformations before complex ones. Do not document brute-force feature explosion.

| Transformation Or Feature | Purpose | Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| FEATURE_OR_TRANSFORM | WHY_ATTEMPTED | worked / did not work / promising / unclear | yes / no / maybe | VALIDATION |

## Analyses Run

- Reproduction notes: commands, script, table, plot, or manual steps:
- Output artifacts:
- Optional notebook:
- Descriptive stats:
- Distribution checks:
- Volatility / regime checks:
- Spread / microstructure checks:
- Correlation / covariance checks:
- Lead-lag checks:
- Price vs trade alignment:
- Volume behavior:
- Order book dynamics:

## Facts

- Wiki fact:

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| CONDITION | FEATURES | BEHAVIOR | USE_OR_AVOID | strong / medium / weak / contradictory | CAVEATS |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SIGNAL | RAW_OR_DERIVED_FEATURES | MEANING | DECISION_IMPACT | HOW_TO_USE | stable / regime-dependent / unknown | strong / medium / weak / contradictory | CAVEATS |

## Assumptions

- Assumption:

## Open Questions

- Question:

## Signal Strength And Uncertainty

- Strength: `strong | medium | weak | contradictory`
- Evidence:
- Uncertainty:

## Downstream Use / Agent Notes

- Strong enough to consider:
- Exploratory only:
- Do not use yet:
- Additional validation needed:
- How understanding should use this:
- How strategy generation should use this:
- How specification should use this:
- How implementation should use this:
- How testing/debugging should use this:

## Reusable Metrics

- Metric:

## Strategy Implications

- What this changes:
- If not actionable, say why:

## Interpretation Limits

- Limit:

## Next Action

- Next:
