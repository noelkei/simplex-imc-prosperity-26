# Round 1 To Round 2 - Pre-EDA Note

## Status

READY_FOR_EDA_INPUT

## Purpose

Prepare Round 2 EDA without carrying Round 1 assumptions forward as facts.

This note compares only official wiki facts and known workspace state. It is not
an EDA result and does not promote any strategy.

## Official Facts That Carry Forward

| Item | Round 1 | Round 2 | Status |
| --- | --- | --- | --- |
| `ASH_COATED_OSMIUM` tradable by algorithm | Yes | Yes | Carry forward as fact |
| `INTARIAN_PEPPER_ROOT` tradable by algorithm | Yes | Yes | Carry forward as fact |
| `ASH_COATED_OSMIUM` position limit | 80 | 80 | Carry forward as fact |
| `INTARIAN_PEPPER_ROOT` position limit | 80 | 80 | Carry forward as fact |
| Shared `Trader.run(state)` contract | `result, conversions, traderData` | `result, conversions, traderData` | Carry forward as fact |
| Shared exchange mechanics | Standard matching and position-limit rules | Same shared docs apply | Carry forward as fact |

## Official Facts That Changed

| Area | Round 1 | Round 2 | EDA / Workflow Impact |
| --- | --- | --- | --- |
| Algorithmic challenge | First Intarian Goods | limited Market Access | Round 2 has an extra market-access decision. |
| Round-specific `Trader` method | No Round 1-specific method required | `Trader.bid()` is relevant for final Round 2 | Spec must decide implement/exclude/block before coding. |
| Market access | Normal accessible quote set | Accepted bid receives 25% more order-book quotes | EDA should estimate incremental value before bid choice. |
| Testing comparability | No Round 2 MAF behavior | Testing ignores `bid()` and uses randomized 80% quote subset | Validation should expect some run variance. |
| Manual challenge | Exchange Auction | Research / Scale / Speed allocation | Round 1 manual auction assumptions do not apply. |
| Product hint | IPR steady, ACO more volatile/possibly patterned | Same products, market accelerated/more competitive/dynamic | Treat Round 1 behavior as hypothesis only. |

## Prior-Round Assumptions At Risk

- Any fixed fair value or drift assumption from Round 1.
- Any Round 1 spread, volatility, fill-rate, or market-order frequency estimate.
- Any Round 1 quote-depth or accessible-flow assumption.
- Any Round 1 manual challenge logic.
- Any Round 1 bot constants, thresholds, inventory skew, or timing behavior.
- Any expectation that a single Round 2 platform test is fully comparable, because
  the official Round 2 docs say the testing quote subset is slightly randomized.

## Round 2 EDA Questions Seeded By This Comparison

1. Do the two products have stable, online-usable price structure across Round 2 sample days?
2. Does Round 2 data support or reject the broad Round 1 product hints?
3. Which top-of-book and depth features are predictive enough to justify implementation?
4. How much executable opportunity is likely added by 25% extra market access?
5. How sensitive are validation conclusions to randomized quote access?
6. What manual Research / Scale / Speed allocations are robust under plausible Speed ranks?

## Historical / Quarantined Inputs

The previous pre-kickoff EDA outputs have been archived under:

`01_eda/historical/2026-04-19_unreviewed_pre_kickoff_eda/`

They may be inspected later as historical context, but they are not active
Round 2 evidence until explicitly reviewed or rerun.

## Next Action

Start a fresh exhaustive EDA from the official Round 2 wiki facts, raw CSV data,
and this comparison note.
