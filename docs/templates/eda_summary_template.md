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

## Algorithmic vs Manual Scope

Separate findings usable inside `Trader.run()` from manual-challenge findings.

| Finding | Scope | Why | Caveat |
| --- | --- | --- | --- |
| FINDING | algorithmic / manual / both / not applicable | REASON | CAVEAT |

## Data Sources

- Raw data:
- Processed data:
- External context:
- Run or log artifact:
- Post-run research memory:

## Round Adaptation Check

Use this once per EDA artifact to prevent hidden prior-round assumptions.

| Check | Current-Round Evidence | Decision / Action |
| --- | --- | --- |
| Active round mechanics/API | ROUND_DOC_OR_SOURCE | use / exclude / not applicable / blocker |
| Products and limits | ROUND_DOC_OR_SOURCE | verified / unknown / blocker |
| Data schema | ARTIFACT_OR_SOURCE | classified / changed / unclear |
| New or changed fields/mechanics | FIELD_OR_MECHANIC | EDA question / spec decision / no action |
| Prior-round assumption at risk | ASSUMPTION | reject / revalidate / carry as assumption |

## Artifact Index

Persist reusable artifacts under existing round-local paths and link them here.

| Artifact Path | Type | Source Data | Useful For | Decision-Relevant? |
| --- | --- | --- | --- | --- |
| PATH | table / plot / notebook / script / processed file / raw log | SOURCE | USE | yes / no / maybe |

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

Include raw features and derived features created during EDA. Keep this compact; detail only features that could change a downstream decision.

Feature lifecycle states:

- `observed`: appears in CSV, `TradingState`, logs, manual mechanics, or a combined analysis.
- `classified`: origin, online usability, and role are known.
- `evaluated`: signal strength, stability, and actionability are checked.
- `promoted`: should enter Understanding / strategy as a signal.
- `rejected`: meaningful negative evidence exists.
- `specified`: exact bot use belongs in a reviewed strategy spec.
- `implemented`: present in a bot and validated through runs.

Origins: `csv | online | log/post-run | combined | manual-only`.
Online usability: `usable online | EDA-only | log-only | unknown`.
Roles: `direct signal | execution filter | risk control | diagnostic | manual | avoid`.

| Feature | Origin | Online Usability | Meaning | Role | Signal Strength | Stability | Actionability | Lifecycle Decision | Notes / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FEATURE | csv / online / log/post-run / combined / manual-only | usable online / EDA-only / log-only / unknown | MEANING | direct signal / execution filter / risk control / diagnostic / manual / avoid | strong / medium / weak / contradictory | stable / day-sensitive / timestamp-sensitive / regime-dependent / unknown | changes strategy / changes parameters / changes validation / no decision impact | promote / exploratory / negative evidence / EDA-only calibration / needs logs / reject | NOTES |

## Feature Engineering Notes

Target simple, hypothesis-driven transformations before complex ones. Do not document brute-force feature explosion.

Evaluate each serious feature against:

- Signal gate: does it predict, explain, or classify something useful?
- Stability gate: does it persist across days, timestamps, products, or regimes?
- Actionability gate: would it change strategy, parameters, risk, validation, or debugging?

Feature explosion controls:

- Max 5-8 serious feature candidates in this artifact unless explicitly justified.
- Max 1-3 promoted signal hypotheses.
- Do not document every failed transform; preserve only decision-relevant negative evidence.

| Transformation Or Feature | Purpose | Gate Result | Keep? | Next Validation |
| --- | --- | --- | --- | --- |
| FEATURE_OR_TRANSFORM | WHY_ATTEMPTED | signal / stability / actionability result | yes / no / maybe | VALIDATION |

## Feature Promotion Decisions

Promote only features that change a concrete downstream decision. EDA-only features may support reasoning, but must not enter bot specs unless an online proxy exists.

| Feature Or Signal | Decision | Destination | Reason | Caveat / Reopen Condition |
| --- | --- | --- | --- | --- |
| FEATURE_OR_SIGNAL | promote to understanding / keep exploratory / negative evidence / EDA-only calibration / needs logs / reject | Signal Ledger / Research Memory / Negative Evidence / none | REASON | CAVEAT |

## Analyses Run

- Reproduction notes: commands, script, table, plot, or manual steps:
- Research tools used and why:
- Research tools considered but skipped:
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

## Research Tool Notes

Use tools only when they improve decision quality. Typical use: `pandas`/`numpy` for core tables, `polars` for large logs, `numba` for heavy loops, `scipy`/`statsmodels`/`pingouin` for tests and confidence, `arch` for volatility regimes, `ruptures` for change points, and `sklearn` for lightweight clustering or feature screening.

- Tools that changed a decision:
- Tools that were unnecessary:
- Risk of overfitting or over-modeling:

## Distribution Hypotheses

Use lightweight interpretations only when they affect strategy, risk, or validation.

| Product Or Scope | Hypothesis | Evidence | Strategy Implication | Caveat |
| --- | --- | --- | --- | --- |
| PRODUCT_OR_SCOPE | mean-reverting / trending / mixture / regime-switching / noisy/unclear | EVIDENCE | IMPLICATION | CAVEAT |

## Facts

- Wiki fact:

## Conditional Patterns / Regimes

| Condition Or Regime | Dependent Features | Observed Behavior | Strategy Relevance | Confidence | Caveats |
| --- | --- | --- | --- | --- | --- |
| CONDITION | FEATURES | BEHAVIOR | USE_OR_AVOID | strong / medium / weak / contradictory | CAVEATS |

## Threshold / Execution Findings

Capture execution-relevant breakpoints rather than broad parameter sweeps.

| Finding | Feature Basis | Threshold Or Zone | Execution / Risk Use | Readiness | Caveat |
| --- | --- | --- | --- | --- | --- |
| FINDING | FEATURES | LEVEL_OR_ZONE | USE | usable / exploratory / not ready | CAVEAT |

## Signal Hypotheses

| Signal | Feature Dependencies | What It Means | Why It Matters | Strategy Use | Stability | Confidence | Limitations / Caveats |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SIGNAL | RAW_OR_DERIVED_FEATURES | MEANING | DECISION_IMPACT | HOW_TO_USE | stable / regime-dependent / unknown | strong / medium / weak / contradictory | CAVEATS |

## Negative Evidence

Preserve meaningful failed checks so later agents do not rediscover weak ideas.

| Idea Or Signal | Why It Was Plausible | Evidence Against It | When To Reopen |
| --- | --- | --- | --- |
| IDEA_OR_SIGNAL | RATIONALE | EVIDENCE | CONDITION |

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
