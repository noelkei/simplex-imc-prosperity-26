# Strategy Candidates Template

Candidate count is ROI-driven, not fixed. Keep every non-duplicative
high-ROI candidate that is evidence-backed or based on a clearly labeled
testable assumption. Use role, priority tier, and implementation wave to manage
focus instead of imposing a hard cap.

## Status

`NOT_STARTED | IN_PROGRESS | BLOCKED | READY_FOR_REVIEW | COMPLETED`

## Sources

- Wiki facts:
- Understanding summary:
- EDA evidence:
- Post-run research memory:
- Playbook heuristics:

## Feature Budget

Strategies should be feature-light by default:

- Primary edge: max 1 feature, signal, or fair-value model.
- Supporting logic: max 2 execution filters or risk controls.
- Diagnostics may be included when they do not change trading decisions.
- More features require explicit justification in the decision trace.

Link every serious feature chain as:

```text
feature -> signal -> decision -> expected edge -> validation check
```

Use EDA multivariate and process evidence to keep candidates feature-light:

- A redundant feature needs an explicit reason to remain.
- A process hypothesis should support the strategy family when available.
- PCA, clustering, latent-state, or other EDA-only findings need an online proxy before they can influence bot behavior.
- Cross-product relationships should be used only when EDA or understanding marks them useful or worth validating.

## Candidate Count And Roles

- Typical target: 5+ strong candidates when the evidence supports them.
- No hard cap when additional candidates are differentiated, online-usable or
  proxied, testable, and validation-relevant.
- Candidate roles: `primary | secondary | exploratory | mechanics-only |
  manual-only | deferred | rejected`.
- Priority tiers: `spec-first | implement-first | validate-next | backlog |
  defer`.
- Prune only low-ROI, duplicate, unsupported, non-online-usable, or
  decision-irrelevant ideas.

## Round Coverage Check

List only current-round mechanics, fields, or product behaviors that could change candidate selection.

| Item | Source | Candidate Impact | Decision |
| --- | --- | --- | --- |
| MECHANIC_FIELD_OR_BEHAVIOR | EDA / understanding / round doc / post-run memory | affects edge / execution / risk / validation / none | use / exclude / defer / needs EDA |

## Exploration Board

Conceptual candidate ideas before commitment. These are not active strategies yet.

| Idea ID | Product | Source Signal | Primary Feature / Signal | Supporting Features | Process Hypothesis | Online Proxy Needed? | Approach | Expected Edge | Main Risk | Implementation Realism | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IDEA_ID | PRODUCT | SIGNAL | FEATURE | FEATURES_OR_NONE | PROCESS_OR_NONE | yes / no / unknown | APPROACH | EDGE | RISK | high / medium / low | explore / prune / candidate |

## Per-Product Branches

| Product | Top Branches | Strongest Signal | Weakest Assumption | Pruning Note |
| --- | --- | --- | --- | --- |
| PRODUCT | BRANCHES | SIGNAL | ASSUMPTION | NOTE |

## Combination / Compatibility Matrix

Use this for multi-product rounds before writing specs. Mark `not applicable` when products are independent or only one product matters.

| Pairing | Compatibility | Risk Interaction | Execution Alignment | Cross-Product Dependency | Verdict |
| --- | --- | --- | --- | --- | --- |
| PAIRING | high / medium / low / not applicable | RISK | aligned / mixed / conflicting | useful / weak / none | move forward / backup / reject / not applicable |

## Candidate Table

| Candidate ID | Role | Product Scope | Source Of Edge | Primary Feature / Signal | Supporting Features | Feature Role | Linked EDA Signals | Feature Evidence | Multivariate Evidence | Supporting Process Hypothesis | Redundancy Note | Online Proxy Needed? | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Why Not Feature Dumping | ROI / Pruning Rationale | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority Tier | Implementation Wave | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_ID | primary / secondary / exploratory / mechanics-only / manual-only / deferred / rejected | PRODUCT | EDGE | FEATURE_OR_FV | FEATURES_OR_NONE | direct signal / execution filter / risk control / diagnostic | SIGNALS | FEATURES | corr / covariance / regression / lead-lag / redundancy / none | PROCESS_OR_NONE | keep / merge / downgrade / not checked / not applicable | yes / no / unknown | REGIMES | INSIGHT | ASSUMPTIONS | RISK | FEATURE_BUDGET_RATIONALE | WHY_KEEP_OR_PRUNE | strong / medium / weak / contradictory | high / medium / low | high / medium / low | high / medium / low | high / medium / low | spec-first / implement-first / validate-next / backlog / defer | WAVE_OR_NONE | draft |

## Rejected Or Deferred Ideas

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| IDEA | feature weak / not online-usable / too complex / no decision impact / duplicate / unsupported / other | GAP_OR_RISK |

## Prioritized Candidate Queue

Prioritize before writing specs. This is not a hard cap; it is the ordered
queue for spec, implementation, and validation.

| Order | Candidate ID | Priority Tier | Implementation Wave | Why This Early / Later | Spec Action |
| --- | --- | --- | --- | --- | --- |
| 1 | CANDIDATE_ID | spec-first / implement-first / validate-next / backlog / defer | wave 1 / wave 2 / backlog / none | RATIONALE | write spec / defer spec / needs decision |

## Decision Trace

Explain why prioritized candidates are earlier or later in the queue than the
alternatives.

| Candidate | Signals Used | Alternatives Rejected Or Deferred | Reason For Priority | Caveat |
| --- | --- | --- | --- | --- |
| CANDIDATE_ID | SIGNALS | ALTERNATIVES | REASON | CAVEAT |

## Exploration Stop Rule

- Stop reason:
- Low-ROI branching signal: `duplicate ideas | weak evidence | unimplementable | unlikely to change candidate queue | implementation/validation bottleneck | strong incumbent | deadline pressure`
- Ready to write specs: `yes | no`

## Human Checkpoint

Optional, maximum 1-3 high-value questions.

| Decision Needed | Default If No Answer | Options | Why It Matters |
| --- | --- | --- | --- |
| DECISION | DEFAULT | OPTIONS | IMPACT |

## Next Action

- Next:
