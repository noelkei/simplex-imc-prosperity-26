# Round 2 Gen2 Bruno Battery Spec

## Spec Status

- Status: `approved with caveats`
- Review outcome: user requested implementation of all 13 Generation 2 bots after
  Battery 01 review.
- Owner/member: `bruno`
- Implementation destination: `rounds/round_2/bots/bruno/canonical/`
- Date: `2026-04-19`

## Sources

- Round facts: `docs/prosperity_wiki/rounds/round_2.md`
- Trader contract: `docs/prosperity_wiki/api/01_trader_contract.md`
- Datamodel: `docs/prosperity_wiki/api/02_datamodel_reference.md`
- Position limits: `docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Battery 01 analysis: `rounds/round_2/workspace/06_testing/round2_battery_01_analysis.md`
- Post-run memory: `rounds/round_2/workspace/post_run_research_memory.md`
- Gen2 queue: `rounds/round_2/workspace/06_testing/artifacts/battery_01_generation2_candidates.csv`

## Round-Specific Mechanics Contract

| Mechanic | Decision | Implementation |
| --- | --- | --- |
| `Trader.run(state)` | implement | Every bot returns `result, conversions, traderData`. |
| `Trader.bid()` | implement | All bots define `bid()`. G2-13 returns a scenario bid; all others return `0`. |
| Market Access Fee | mechanics-only | Testing ignores accepted bids; do not treat G2-13 test PnL as MAF evidence. |
| Manual Research/Scale/Speed | exclude | Manual challenge is separate and not implemented. |
| Products | implement | Only `INTARIAN_PEPPER_ROOT` and `ASH_COATED_OSMIUM`. |
| Position limits | implement | Both products use limit `80`; aggregate buy/sell capacity is capped. |

## Battery 01 Findings Carried Forward

| Finding | Impact On Gen2 |
| --- | --- |
| All positive Battery 01 PnL came from IPR. | Keep IPR as the competitive base and rerun strongest IPR families. |
| ACO ended with `0` PnL and `0` final position in every run. | Treat current ACO implementation as inactive/over-gated; test activation before judging alpha. |
| ACO top spread was rarely `<= 4`. | Replace hard narrow spread gates with product-specific wider spread handling. |
| C08 trials differed materially. | Gen2 includes rerun/robustness candidates, not one-shot champion selection. |
| C10 `bid()` was `0`. | MAF remains a separate scenario, not a proven alpha feature. |

## Feature Contracts

| Feature | Source Fields | Online Usability | Role | Parameters / Behavior | Missing-Signal Behavior | Validation Check |
| --- | --- | --- | --- | --- | --- | --- |
| IPR drift/residual | `TradingState.order_depths[IPR]`, `traderData` | usable online | alpha/fair value | Track mid and EWMA slope; trade when forecast fair value crosses top ask/bid by threshold. | Stay idle until both-sided book and warmup. | Compare repeated IPR PnL, final position, drawdown. |
| IPR residual extreme | same | usable online | high-confidence alpha | Same drift model with higher threshold/lower clip. | Stay idle until warmup. | Rerun C02-style candidate and compare median/worst-case. |
| IPR inventory flattening | `position`, order book | usable online | risk control | If position exceeds soft inventory, bias or cross small opposite-side orders. | No flattening if book missing. | Check final position reduction versus PnL cost. |
| Product-specific spread sizing | top bid/ask | usable online | execution/risk | Continuous size multiplier by spread instead of binary `spread <= 4`. | Reduce size to zero when spread is beyond max. | Check activity, PnL, and ACO activation. |
| ACO activation probe | ACO order book | usable online | diagnostic | Small passive/take orders around smoothed fair value with wider spread tolerance. | Stay idle if no visible side. | Must produce nonzero ACO attribution or position activity. |
| ACO top imbalance | ACO top volumes | usable online | alpha challenger | Use top imbalance to skew inside-spread quotes and occasional takes. | Stay idle if one side missing unless port logic supports one-sided mode. | Compare against activation probe. |
| ACO reversal | ACO mid history | usable online | process challenger | Use last mid delta as a reversal signal with wider spread handling. | Stay idle until at least one prior mid. | Compare against ACO imbalance. |
| ACO Kalman port | ACO mid history | usable online | Round 1 port side bet | Bruno Round 1-style stable Kalman fair value and inner quotes. | Stay idle if no visible side. | Keep only if ACO attribution improves. |
| ACO one-sided port | ACO one-sided/two-sided book | usable online | Round 1 port side bet | Noel Round 1-style fixed FV one-sided handling and inner quotes. | Stay idle if no visible side. | Compare to Bruno port and corrected ACO modules. |
| MAF bid scenario | `Trader.bid()` | final-only mechanic | mechanics-only | G2-13 returns a conservative scenario bid; testing PnL cannot validate it. | Not applicable. | Decide final bid separately. |

## Candidate Matrix

| Candidate | Bot File | Role | Product Scope | Primary Test |
| --- | --- | --- | --- | --- |
| `R2-G2-01` | `candidate_r2_g2_01_ipr_extreme_rerun_champion.py` | primary / robustness | IPR | Rerun C02-style residual extreme. |
| `R2-G2-02` | `candidate_r2_g2_02_ipr_drift_rerun_code_equiv.py` | primary / robustness | IPR | Rerun C07/C10 drift family without ACO. |
| `R2-G2-03` | `candidate_r2_g2_03_ipr_extreme_flatter_inventory.py` | risk challenger | IPR | C02-style entry plus inventory flattening. |
| `R2-G2-04` | `candidate_r2_g2_04_ipr_spread_retune.py` | execution diagnostic | IPR | Continuous spread sizing for IPR. |
| `R2-G2-05` | `candidate_r2_g2_05_aco_activation_probe.py` | diagnostic | ACO | Prove ACO can activate. |
| `R2-G2-06` | `candidate_r2_g2_06_aco_imbalance_wide_spread.py` | alpha challenger | ACO | Retest top imbalance with wider spread handling. |
| `R2-G2-07` | `candidate_r2_g2_07_aco_reversal_wide_spread.py` | process challenger | ACO | Retest reversal with wider spread handling. |
| `R2-G2-08` | `candidate_r2_g2_08_combined_ipr_extreme_aco_probe.py` | combined diagnostic | both | C02-style IPR plus small ACO activation probe. |
| `R2-G2-09` | `candidate_r2_g2_09_combined_ipr_extreme_aco_imbalance.py` | combined alpha | both | C02-style IPR plus corrected ACO imbalance. |
| `R2-G2-10` | `candidate_r2_g2_10_spread_overlay_continuous.py` | execution overlay | both | Continuous spread overlay on combined candidate. |
| `R2-G2-11` | `candidate_r2_g2_11_bruno_r1_kalman_r2_port.py` | side bet | both | Bruno Round 1 Kalman ACO port plus current IPR base. |
| `R2-G2-12` | `candidate_r2_g2_12_noel_r1_c26_r2_port.py` | side bet | both | Noel Round 1 C26 ACO port plus current IPR base. |
| `R2-G2-13` | `candidate_r2_g2_13_maf_bid_scenario.py` | mechanics-only | both + MAF | C02-style IPR plus MAF scenario bid. |

## Exclusions

- No CSV reads, file IO, platform JSON reads, or research-library imports.
- No cross-product lead-lag logic.
- No PCA, cluster, HMM, or latent labels as direct bot logic.
- No manual Research/Scale/Speed allocation.
- No timestamp-to-end liquidation or sample-length assumptions.
- No stochastic behavior.

## Validation Plan

1. Compile all 13 files.
2. Run a minimal smoke test that instantiates each `Trader`, calls `bid()`, and
   calls `run()` on a mock two-product state.
3. Upload all 13 to Prosperity testing.
4. Rank by real platform PnL, but classify close results as provisional because
   Round 2 quote subsets are randomized.
5. Require product attribution before promoting any ACO candidate.
6. Treat G2-13's bid as a final-only scenario, not as platform-test alpha.

## Caveats

- These are Generation 2 exploration bots, not final submission selections.
- ACO modules intentionally prioritize activation evidence before PnL
  maximization.
- G2-11 and G2-12 use Round 1 implementation ideas only as controlled side
  bets because Round 2 docs say products carry over; Round 1 behavior is not an
  official Round 2 rule.
