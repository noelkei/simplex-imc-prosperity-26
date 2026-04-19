# Understanding Summary Template

## Status

`NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | COMPLETED`

## Sources

- Wiki facts:
- EDA evidence:
- Post-run research memory:
- Playbook heuristics:
- Other named artifacts:

## Current Understanding

- Fact:
- Evidence:
- Hypothesis:

## Evidence Synthesis

| Claim Or Observation | Source | Evidence Strength | Decision Impact | What Would Change This |
| --- | --- | --- | --- | --- |
| ITEM | ingestion / EDA / playbook | strong / medium / weak / contradictory | high / medium / low | CONDITION |

## Signal Validation Expectations

Use EDA research outputs to compress confidence, not to rerun broad analysis. Retain effect sizes, stability checks, regime/change-point evidence, statistical tests, and negative evidence only when they change strategy, spec, validation, or debugging decisions.

- Statistical or regime evidence used:
- Features downgraded for weak confidence, instability, or offline-only status:
- Research outputs not trusted yet:

## Multivariate Relationships Carried Forward

Use only compact EDA relationships that change product scope, feature
selection, strategy family, spec parameters, or validation checks. Do not rerun
broad EDA here.

| Relationship | Source EDA Artifact | Evidence | Decision Impact | Confidence | Caveat |
| --- | --- | --- | --- | --- | --- |
| FEATURE_OR_PRODUCT_RELATIONSHIP | ARTIFACT | correlation / covariance / regression / lead-lag / MI / other | use / validate / avoid / defer | high / medium / low | CAVEAT |

## Redundancy Decisions

Carry forward which features should be kept, merged, downgraded, or avoided so
strategy candidates do not rediscover feature dumps.

| Feature Family | Keep | Merge / Downgrade / Drop | Evidence | Strategy Impact |
| --- | --- | --- | --- | --- |
| FAMILY | FEATURES | FEATURES | corr / covariance / VIF / PCA / controlled model / other | IMPACT |

## Process Hypotheses Carried Forward

Preserve only process interpretations that should influence strategy,
specification, risk, or validation.

| Product Or Scope | Process Hypothesis | EDA Evidence | Confidence | Online Observable / Proxy | Strategy Or Validation Implication |
| --- | --- | --- | --- | --- | --- |
| PRODUCT_OR_SCOPE | trending / mean-reverting / random-walk-like / jumpy / multimodal / volatility-clustered / regime-switching / flow-driven / unclear | EVIDENCE | high / medium / low | FIELD_OR_PROXY | IMPLICATION |

## Assumptions Carried Forward

Only carry assumptions from prior rounds when current-round evidence supports them or the risk is explicit.

| Assumption | Source | Current-Round Evidence | Risk | Action |
| --- | --- | --- | --- | --- |
| ASSUMPTION | ingestion / EDA / post-run memory / playbook / prior round | EVIDENCE_OR_NONE | high / medium / low | use / validate / reject / defer |

## Signal Ledger

Retain the compact signal memory that strategy agents should use. Keep one row per usable signal, not one row per raw column.

| Signal | Product | Source Artifact | Feature Basis | Feature Origin | Online Usability | Role | Stability | Confidence | Decision Action | Risk | Next Phase Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SIGNAL | PRODUCT | ARTIFACT | FEATURES | csv / online / log/post-run / combined / manual-only | usable online / EDA-only / log-only / unknown | direct signal / execution filter / risk control / diagnostic / manual / avoid | stable / day-sensitive / timestamp-sensitive / regime-dependent / unknown | high / medium / low | use / validate / avoid / defer | RISK | ACTION |

## Strategy-Relevant Insights

Prioritize the few insights another agent should actually use. Link back to EDA evidence instead of restating full EDA.

| Insight | Linked EDA Signals | Feature Evidence | Regime Assumptions | Confidence | Strategy Impact |
| --- | --- | --- | --- | --- | --- |
| INSIGHT | SIGNAL_OR_ARTIFACT | FEATURES | REGIME_OR_NONE | high / medium / low | ACTIONABLE_IMPACT |

## Product Attribution View

| Product | Opportunity / Risk Status | Evidence | Main Uncertainty | Strategy Implication |
| --- | --- | --- | --- | --- |
| PRODUCT | edge likely / unclear / risk-heavy / low priority | EVIDENCE | UNCERTAINTY | IMPLICATION |

## Cross-Product Verdict

- Verdict: `useful | weak | not applicable | needs targeted EDA`
- Evidence:
- Caveat:

## What Should Be Tried

| Candidate Direction | Supporting Insight | Product Scope | Why Try It | Validation Needed |
| --- | --- | --- | --- | --- |
| DIRECTION | INSIGHT | PRODUCTS | RATIONALE | CHECK |

## What Should Not Be Trusted Yet

| Signal Or Claim | Why Not Trusted | Risk If Used | Next Validation |
| --- | --- | --- | --- |
| SIGNAL | REASON | RISK | CHECK_OR_DEFER |

## Research Memory

Preserve useful feature evidence without promoting weak ideas into strategy.

Promising features:

| Feature Or Signal | Source | Why Promising | Needed Before Strategy |
| --- | --- | --- | --- |
| FEATURE | ARTIFACT | REASON | VALIDATION |

Rejected / noisy features:

| Feature Or Signal | Source | Evidence Against | Reopen Only If |
| --- | --- | --- | --- |
| FEATURE | ARTIFACT | EVIDENCE | CONDITION |

Unresolved / log-needed features:

| Feature Or Signal | Source | Missing Evidence | Next Action |
| --- | --- | --- | --- |
| FEATURE | ARTIFACT | GAP | ACTION |

## Confidence And Impact

- Overall confidence: `high | medium | low`
- Highest-impact implication:
- Main caveat:

## Assumptions

- Assumption:

## Open Questions

- Question:

## Open Risks And Unknowns

| Risk Or Unknown | Affects | Severity | Mitigation Or Next Action |
| --- | --- | --- | --- |
| RISK | strategy / spec / implementation / validation | high / medium / low | ACTION |

## Prioritized Unknowns

| Unknown | Affects | Priority | Next Action |
| --- | --- | --- | --- |
| UNKNOWN | EDA / strategy / implementation / validation | high / medium / low | clarify / EDA / defer with risk |

## Strategy Implications

- Candidate direction:
- Risk or constraint:
- Validation/debug implication:

## Next Action

- Next:
