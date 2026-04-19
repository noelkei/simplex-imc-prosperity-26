# Post-Run Research Memory

Curated reusable evidence from platform or platform-style runs. This is not a
dump of every metric; keep only insights that change future decisions.

## Status

- Round:
- Last updated:
- Current champion:
- Latest platform artifact:
- Memory confidence: `high | medium | low`

## Source Runs

| Run | Candidate | Artifacts | PnL Source | Decision Relevance | Notes |
| --- | --- | --- | --- | --- | --- |
| RUN_ID | CANDIDATE | .py / .json / .log / summary | real platform PnL / calibrated proxy / weak proxy | primary / backup / fallback / rejected / research | NOTES |

## Run Knowledge Index

Compact index for deduplication and run-aware updates. Use this to decide whether a run adds knowledge, confirms a known belief, contradicts a current decision, or can be ignored in future reasoning.

| Run | Candidate | Strategy Family | Changed Axis | Tested Feature / Signal | PnL Source | Comparable To | Knowledge Delta | Memory Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RUN_ID | CANDIDATE | FAMILY | parameter / threshold / feature toggle / execution / risk / baseline | FEATURE_OR_NONE | real platform / calibrated proxy / weak proxy | RUN_OR_CHAMPION | new / confirms / contradicts / duplicate / unclear | update / update lightly / no update |

Dedup heuristic: `candidate + strategy family + changed axis + tested feature/signal + data/source + PnL source`.

## Current Reusable Insights

| Insight ID | Products | Based On Runs | Analysis Mode | Finding | Confidence | Portability | Reuse In | Caveat |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INSIGHT_ID | PRODUCTS | RUNS | failure / edge / counterfactual / negative evidence | FINDING | high / medium / low | round-specific / likely reusable / uncertain | EDA / understanding / strategy / spec / variant | CAVEAT |

## Feature Feedback

Use this to update feature confidence after serious platform or platform-style runs. Keep only feedback that changes a future decision.

| Feature Or Signal | Runs | Outcome | Evidence Method | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| FEATURE | RUNS | helped / failed / unclear | fill stats / markout / statistical test / regime split / counterfactual / none | up / down / unchanged | keep / variant / EDA / discard |

## Multivariate Relationship Feedback

Record only run evidence that confirms, weakens, or contradicts a relationship
used by understanding, strategy, or a spec.

| Relationship | Runs | EDA Expectation | Run Evidence | Confidence Change | Next Action |
| --- | --- | --- | --- | --- | --- |
| FEATURE_OR_PRODUCT_RELATIONSHIP | RUNS | EXPECTATION | confirms / weakens / contradicts / unclear | up / down / unchanged | keep / EDA / spec revision / discard |

## Process Hypothesis Feedback

Use this when platform or platform-style runs provide evidence about a process
assumption such as mean reversion, trend, regime switching, flow sensitivity, or
volatility clustering.

| Process Hypothesis | Products | Runs | Run Evidence | Confidence Change | Strategy / Spec Impact |
| --- | --- | --- | --- | --- | --- |
| HYPOTHESIS | PRODUCTS | RUNS | supports / weakens / contradicts / unclear | up / down / unchanged | IMPACT |

## Redundancy Decision Feedback

Use this when a run tests whether a feature was unnecessary, duplicate,
harmful, or worth adding back.

| Feature Family | Prior Redundancy Decision | Runs | Evidence | Next Action |
| --- | --- | --- | --- | --- |
| FAMILY | keep / merge / downgrade / drop / unclear | RUNS | EVIDENCE | keep / reopen EDA / spec revision / discard |

## Statistical Confidence Notes

Record only confidence evidence that changes future decisions. Examples: adverse-selection markouts, fill quality differences, effect sizes, confidence intervals, volatility/regime shifts, or change-point windows.

- Decision-relevant confidence update:
- Tool or method used:
- Caveat or overfit risk:

## Log-Derived Feature Discoveries

Features discovered from `own_trades`, `market_trades`, execution diagnostics, or logs should enter the pipeline as targeted EDA questions, counterfactuals, or spec updates.

| Feature Or Signal | Source Runs / Logs | Evidence | Online Usability | Proposed Use | Next Step |
| --- | --- | --- | --- | --- | --- |
| FEATURE | RUNS_OR_LOGS | EVIDENCE | usable online / log-only / unknown | direct signal / execution filter / risk control / diagnostic | EDA / strategy / spec / variant / discard |

## Feature Confidence Updates

| Feature Or Signal | Previous Confidence | New Confidence | Reason | Affected Artifact |
| --- | --- | --- | --- | --- |
| FEATURE | high / medium / low / unknown | high / medium / low / rejected | REASON | EDA / understanding / strategy / spec / variant |

## Failure Patterns

| Pattern | Runs | Conditions | Failure Class | Action |
| --- | --- | --- | --- | --- |
| PATTERN | RUNS | CONDITIONS | signal / execution / timing / inventory / risk / unclear | ACTION |

## Edge Decomposition Memory

| Edge | Runs | Driver | Real Edge Or Fragile? | Evidence | Reuse |
| --- | --- | --- | --- | --- | --- |
| EDGE | RUNS | signal / spread / inventory mark / execution / product carry | real edge / fragile / unclear | EVIDENCE | HOW_TO_USE |

## Counterfactual Backlog

Status values: `untested | tested-promote | tested-reject | defer | discard | superseded`.

| Idea | Source Run | Improvement Axis | Expected ROI | Status | Next Action |
| --- | --- | --- | --- | --- | --- |
| IDEA | RUN | thresholds / timing / filter / inventory / sizing / execution | high / medium / low | untested / tested-promote / tested-reject / defer / discard / superseded | ACTION |

## Negative Evidence / Do Not Rediscover

| Idea | Runs | Why It Failed Or Was Weak | Reopen Only If |
| --- | --- | --- | --- |
| IDEA | RUNS | REASON | CONDITION |

## Downstream Notes

- EDA:
- Understanding:
- Strategy generation:
- Spec writing:
- Variant generation:
