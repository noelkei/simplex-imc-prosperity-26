# Performance Run Summary Template

Raw logs are not durable by default. Preserve current decision evidence in `rounds/round_X/performances/<member>/canonical/` and archive superseded evidence in `rounds/round_X/performances/<member>/historical/`.

## Run Metadata

- Run ID:
- Date:
- Round:
- Member / owner:
- Candidate ID:
- Variant ID:
- Decision relevance: `canonical | historical | draft`
- Bot path:
- Parent bot:
- Strategy spec:
- Variant hypothesis:
- Insight being tested:
- Linked signal/regime assumption:
- Linked process hypothesis:
- Linked multivariate relationship:
- Linked redundancy decision:
- Raw artifact path:
- Data day / source:
- Baseline / comparison run:
- Current champion:
- Changed axis:
- Exact change:
- Expected effect based on EDA/understanding:
- Falsification metric:
- Validation check:

## Result Summary

- Status:
- Profit / score:
- Runtime issues:
- Rejections or errors:
- Position-limit concerns:
- PnL source: `real platform PnL | calibrated proxy | weak proxy`
- Proxy confidence: `high | medium | low | not applicable`
- Proxy evidence basis:

## Run Classification

- Strategy family:
- Tested feature / signal:
- Changed axis type: `parameter | threshold | feature toggle | execution | risk | baseline | unclear`
- Dedup key:
- Dedup verdict: `new | confirms | contradicts | duplicate | unclear`
- Knowledge delta: `new | confirms | contradicts | duplicate | unclear`
- ROI-gated memory action: `update | update lightly | no update`
- Memory action rationale:
- Round adaptation audit: `passed | caveat | failed | not checked`
- Round adaptation caveat:
- Portability: `round-specific | likely reusable | uncertain | not applicable`
- Reroute: `champion decision | targeted EDA | spec revision | debugging | one-axis variant | ignore`

## Run Diagnostics

- Product PnL split:
- Final positions:
- Own trades:
- Buy / sell qty:
- Matched qty:
- Avg buy / avg sell:
- Gross spread capture:
- Max drawdown:
- Max abs position:
- Inventory / mark caveat:
- Advanced diagnostics used, if any:
- Statistical or regime confidence:

## Feature Diagnostics

Optional but recommended when the run tests a feature, signal, or feature toggle.

| Feature Or Signal | Expected Effect | Observed Effect | Diagnostic Method | Confidence Update | Next Action |
| --- | --- | --- | --- | --- | --- |
| FEATURE | EXPECTED | OBSERVED | fill stats / markout / statistical test / regime split / none | up / down / unchanged / unclear | keep / variant / EDA / discard |

## Process And Multivariate Diagnostics

Optional but recommended when the strategy depends on an EDA process
hypothesis, cross-product relationship, controlled feature relationship, or
redundancy decision.

| Assumption Or Relationship | Expected In Run | Observed In Run | Diagnostic Method | Verdict | Next Action |
| --- | --- | --- | --- | --- | --- |
| PROCESS_OR_RELATIONSHIP | EXPECTED | OBSERVED | markout / fill stats / regime split / product split / controlled comparison / none | supports / weakens / contradicts / not tested | keep / targeted EDA / spec revision / variant / discard |

## Comparability

- Comparable to baseline: `yes | no | unclear`
- Same data/source: `yes | no | unclear`
- Same bot/spec version basis: `yes | no | unclear`
- Exact `.py` / `.json` / `.log` saved together: `yes | no | partial | not applicable`
- Known differences:

## Interpretation Limits

- Non-authoritative evidence:
- Missing artifacts:
- Comparability caveats:

## Findings

- Finding:
- Signal/regime evidence verdict: `supports | weakens | contradicts | not tested`
- Process/multivariate evidence verdict: `supports | weakens | contradicts | not tested`
- Verdict basis:

## Post-Run Research

- Analysis status: `not needed | lightweight | full`
- Source artifacts:
- Compared against:
- Memory file change: `added | updated | no change`
- ROI-gated memory action: `update | update lightly | no update`
- Memory action / file-change reason:

### Failure-Driven Analysis

- Losing product / interval:
- Conditions:
- Failure class: `signal | execution | timing | inventory | risk | provenance | unclear`
- Evidence:
- Reusable lesson:

### Edge Decomposition

- Main PnL driver:
- Product contribution:
- Spread capture vs inventory mark:
- Signal quality:
- Fragility: `real edge | mark-driven | execution-sensitive | unclear`
- Evidence:

### Counterfactuals

| Counterfactual | Expected Improvement Axis | Evidence Basis | Cost | Verdict |
| --- | --- | --- | --- | --- |
| IDEA | thresholds / timing / filter / inventory / sizing / execution | EVIDENCE | low / medium / high | untested / tested-promote / tested-reject / defer / discard / superseded |

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop:
- Decision vs champion: `promote | backup | fallback | reject | rerun | not applicable`
- Candidate class: `primary | backup | fallback | reject | experimental | not applicable`

## Next Action

- Next:
