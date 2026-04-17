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
- Verdict basis:

## Post-Run Research

- Analysis status: `not needed | lightweight | full`
- Source artifacts:
- Compared against:
- Memory update: `added | updated | no change`
- Memory update reason:

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
| IDEA | thresholds / timing / filter / inventory / sizing / execution | EVIDENCE | low / medium / high | test / defer / discard |

## Decision

- Continue / promote / debug / discard / revise spec / rerun / stop:
- Decision vs champion: `promote | backup | fallback | reject | rerun | not applicable`
- Candidate class: `primary | backup | fallback | reject | experimental | not applicable`

## Next Action

- Next:
