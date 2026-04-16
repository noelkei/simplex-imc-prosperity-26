# Phase 05 — Implementation Context

## Status

READY_FOR_REVIEW

## Owner: Claude | Member: bruno

## Bot Path

`rounds/round_1/bots/bruno/canonical/candidate_03_combined.py`

## Linked Spec

`rounds/round_1/workspace/04_strategy_specs/spec_candidate_03_combined.md` (approved 2026-04-16)

## Approach Synthesis

Merges **our EDA-backed specs** and **Bruno's proven `new_bot.py`** (baseline P&L: 22,102.5).

### IPR: Directional Max-Long (from Bruno)
- With IPR drifting +1000/day (EDA R²=0.9999), max-long dominates market-making.
- Spec deviation: spec proposed FV-based MM; Bruno's directional approach outperforms (12,099.5 P&L day 0).
- Execution: sweep all asks → post bid at `best_bid+1` for remaining capacity → target +80.

### ACO: FV=10000 Market Maker (Bruno + spec enhancements)
- HALF_SPREAD=5, SKEW_FACTOR=3 (from Bruno, proven). Added FV alert counter from spec.
- Execution: sweep mispriced levels → post full resting orders at skewed bid/ask.

### Key Decisions

| Aspect | Spec | Bruno | Chosen | Rationale |
|---|---|---|---|---|
| IPR strategy | Drift MM | Max-long | Max-long | 12,099 P&L proven |
| ACO spread | 8 | 5 | 5 | Tighter captures more |
| ACO skew | 0.1 | 3 | 3 | Proven flattening |
| Position cap | 75 | 80 | 80 | Full utilization |
| Error handling | try/except | None | try/except | Safety |
| traderData | Semicolon KV | JSON | JSON | Extensible |

## Checklist

- [x] Syntax verified (AST parse)
- [x] Contract: `run()` returns `(result, conversions, traderData)`
- [x] Order signs correct
- [x] Position limits respected
- [x] Empty book handling
- [x] try/except per product
- [ ] Backtest validation pending (Phase 06)

## Caveats
- IPR max-long has zero downside protection if drift reverses live.
- ACO FV=10000 hardcoded; alert counter will flag shifts.

## Next Action

Human review → Phase 06 backtest on days -2, -1, 0.
