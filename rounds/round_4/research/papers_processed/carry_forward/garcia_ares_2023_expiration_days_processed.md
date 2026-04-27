# Processed Paper Summary: Garcia-Ares (2023)

## Status

`draft`

## Round 4 Role

- Reference class: `carry-forward reference`
- Priority for Strategy: below the top-level `round4_raw_derived` processed core
- Allowed use: near-expiry framing, validation cross-checks, and horizon caution
- Caution: if current-round EDA or raw-derived `round_4` papers conflict with this note, prefer current-round evidence

## Paper Metadata

- Paper ID: `garcia_ares_2023_expiration_days`
- Title: `Equity Option Return Predictability and Expiration Days`
- Authors: Pablo Garcia-Ares
- Year: 2023
- Link: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4522770

## Core Claim

Option return predictability is not uniform across the option's lifecycle.
Near expiration, the dynamics of option prices are dominated by:
1. Gamma risk (large underlying moves have disproportionate impact).
2. Pin risk (underlying gravitates toward strikes due to dealer hedging).
3. Accelerated time decay (theta is highest in the last few days).
The paper finds that standard predictors (IV rank, delta, imbalance) weaken
near expiry and that strategies designed for mid-life options degrade.

## Assumptions

- Equity options on single stocks (but conceptually transferable to VEX vouchers).
- Standard BSM mechanics — some adjustment needed for Bachelier framework.
- No counterparty information (predates Round 4 data availability).

## Problem Addressed for Round 4

- We are now at TTE=4 (Round 4), which is well within "near-expiry" territory.
  Round 3 covered TTE=5 (also near-expiry by this paper's definition).
- Historical data only covers TTE=6–8. Our bots are trading out-of-sample.
- The paper warns that out-of-sample behaviour at TTE≤5 is systematically
  different: signals that worked at TTE=7–8 may not port directly.

## What This Paper Gives Us

- Key principle: near expiry, **theta harvest becomes the dominant P&L driver**,
  not delta or IV mispricing. This supports our short-vol strategy.
- Warning: **gamma risk is highest near expiry** for ATM strikes. Being short
  ATM gamma (short VEV_5200/5300) requires adequate delta hedging.
- Warning: **imbalance and order-flow signals weaken** as the expiry date
  approaches. The counterparty signal (Mark 22 seller) may be more robust than
  raw imbalance because it is structurally motivated, not return-predictive.
- Framework: at TTE=4, the dominant strategies are:
  - Short gamma / long theta (sell ATM options, hedge delta).
  - Stay flat or close out winners before gamma spikes can destroy gains.

## Relevance To Round 4

| Round | TTE | Regime |
|------:|----:|--------|
| 3 | 5 | near-expiry |
| **4** | **4** | **deep near-expiry** |
| 5 | 3 | very deep near-expiry |
| 6 | 2 | days-to-expiry |
| 7 | 1 | expiration day |

- **TTE=4 is the regime where theta dominates and gamma risk is highest.**
- Theta per day (×300 units): 5200→2373, 5300→2418 (computed from R4 data).
- This strongly supports maintaining the short-vol position through Round 4.
- Gamma risk for short 300 × VEV_5200: Γ×σ²×300 ≈ 0.0040 × 1491² × 300 ≈ very large.
  Delta hedge MUST be maintained. VEX hedge target ≈ +186 (computed below).

## Portfolio Delta Hedge (Round 4)

```
Short 300 VEV_5200: delta = -300 × 0.6199 = -185.97
Short 300 VEV_5300: delta = -300 × 0.3720 = -111.60
Short 300 VEV_5400: delta = -300 × 0.1582 =  -47.46
Short 300 VEV_5500: delta = -300 × 0.0648 =  -19.44
                             Total option delta: -364.47
Required VEX long to hedge: +364 (capped at +200 limit)
```

Hedge is partially feasible with 200-unit VEX limit. Priority:
1. Cover 5200 and 5300 first (highest delta, highest gamma).
2. Accept residual delta ≈ -364 + 200 = -164 (un-hedged tail risk).

## Action Classification

`promote` — near-expiry regime framing is directly applicable. Delta/gamma
numbers above are actionable targets for Round 4 bots.

## Downstream Use

- Strategy: use near-expiry framing to justify short-vol as primary strategy.
- Spec: enforce delta hedge gate; log un-hedged delta to traderData.
- Validation: track theta realized vs theoretical; monitor gamma spikes.
