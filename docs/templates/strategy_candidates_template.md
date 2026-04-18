# Strategy Candidates Template

Maximum active candidates per round: 3.

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

## Round Coverage Check

List only current-round mechanics, fields, or product behaviors that could change candidate selection.

| Item | Source | Candidate Impact | Decision |
| --- | --- | --- | --- |
| MECHANIC_FIELD_OR_BEHAVIOR | EDA / understanding / round doc / post-run memory | affects edge / execution / risk / validation / none | use / exclude / defer / needs EDA |

## Exploration Board

Conceptual candidate ideas before commitment. These are not active strategies yet.

| Idea ID | Product | Source Signal | Primary Feature / Signal | Supporting Features | Approach | Expected Edge | Main Risk | Implementation Realism | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IDEA_ID | PRODUCT | SIGNAL | FEATURE | FEATURES_OR_NONE | APPROACH | EDGE | RISK | high / medium / low | explore / prune / candidate |

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

| Candidate ID | Product Scope | Source Of Edge | Primary Feature / Signal | Supporting Features | Feature Role | Linked EDA Signals | Feature Evidence | Regime Assumptions | Understanding Insight | Key Assumptions | Main Risk | Why Not Feature Dumping | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CANDIDATE_ID | PRODUCT | EDGE | FEATURE_OR_FV | FEATURES_OR_NONE | direct signal / execution filter / risk control / diagnostic | SIGNALS | FEATURES | REGIMES | INSIGHT | ASSUMPTIONS | RISK | FEATURE_BUDGET_RATIONALE | strong / medium / weak / contradictory | high / medium / low | high / medium / low | high / medium / low | high / medium / low | high / medium / low | draft |

## Rejected Or Deferred Ideas

| Idea | Reason | Evidence Gap Or Risk |
| --- | --- | --- |
| IDEA | feature weak / not online-usable / too complex / no decision impact / duplicate / unsupported / other | GAP_OR_RISK |

## Shortlist

Shortlist 1-3 non-duplicative candidates before writing specs.

- Shortlisted:
- Rationale:

## Decision Trace

Explain why shortlisted candidates were selected over the alternatives.

| Selected Candidate | Signals Used | Alternatives Rejected | Reason Selected | Caveat |
| --- | --- | --- | --- | --- |
| CANDIDATE_ID | SIGNALS | ALTERNATIVES | REASON | CAVEAT |

## Exploration Stop Rule

- Stop reason:
- Low-ROI branching signal: `duplicate ideas | weak evidence | unimplementable | unlikely to change shortlist | implementation/validation bottleneck | strong incumbent | deadline pressure`
- Ready to write specs: `yes | no`

## Human Checkpoint

Optional, maximum 1-3 high-value questions.

| Decision Needed | Default If No Answer | Options | Why It Matters |
| --- | --- | --- | --- |
| DECISION | DEFAULT | OPTIONS | IMPACT |

## Next Action

- Next:
