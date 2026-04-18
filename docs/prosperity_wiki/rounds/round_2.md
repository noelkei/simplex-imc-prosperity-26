# Round 2 - "Growing Your Outpost"

Source basis: `docs/prosperity_wiki_raw/13_round_2.md`.

## Objective

Optimize the Python program for `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, and incorporate a Round-2-only Market Access Fee bid to potentially gain access to additional market volume.

Also allocate a `50 000` XIRECs manual investment budget across three growth pillars: Research, Scale, and Speed.

The source states Round 2 is the final opportunity before the Phase 2 leaderboard reset to reach a net PnL threshold of `200 000` XIRECs or more.

## Tradable products

Algorithmic products:

| Product name | Symbol |
| --- | --- |
| Ash-Coated Osmium | `ASH_COATED_OSMIUM` |
| Intarian Pepper Root | `INTARIAN_PEPPER_ROOT` |

Manual challenge inputs:

| Pillar | Manual input |
| --- | --- |
| Research | Percentage allocation from the `50 000` XIRECs budget |
| Scale | Percentage allocation from the `50 000` XIRECs budget |
| Speed | Percentage allocation from the `50 000` XIRECs budget |

## Position limits

General position-limit mechanics are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

| Product | Limit |
| --- | ---: |
| `ASH_COATED_OSMIUM` | 80 |
| `INTARIAN_PEPPER_ROOT` | 80 |

## Product behavior hints

The source states:

- The products are the same as Round 1.
- Trading activity has accelerated.
- The market has become more competitive and dynamic.

The source does not give a new Round 2 product-specific fair value, drift, volatility model, or signal.

## Algorithmic challenge details

- Challenge name: "limited Market Access".
- Algorithmic products: `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`.
- Position limits: 80 for each algorithmic product.
- Participants can bid for 25% more quotes in the order book.
- The additional quotes' volumes and prices fit into the distribution of already available quotes.
- The Market Access Fee is a one-time fee at the start of Round 2.
- The fee is paid only if the bid is accepted.
- The top 50% of bids across all participants are accepted.
- Accepted bids are subtracted from Round 2 profits.
- Rejected bids do not pay the fee and do not receive extra market access.
- The Market Access Fee only determines extra market access and is not used in simulation dynamics.
- The Market Access Fee is unique to Round 2.
- Any `bid()` function in Rounds 1, 3, 4, and 5 is ignored.
- During Round 2 testing, bids are ignored because final bid comparison happens only when the final Round 2 simulation starts.
- During Round 2 testing, the default quotes are 80% of all generated quotes, i.e. no extra market access.
- The testing quote subset is slightly randomized for every submission.

Round 2 bid example:

```python
class Trader:
    def bid(self):
        return 15

    def run(self, state: TradingState):
        ...
```

Bid acceptance example from the source:

- Bids: `[10, 20, 15, 19, 21, 34]`
- Median: `19.5`
- Accepted bids: `20`, `21`, and `34`
- Rejected bids: `10`, `15`, and `19`

Profit calculation:

| Access status | Profit calculation |
| --- | --- |
| Full market access | `profit = profit from round 2 - bid for getting full market access` |
| No full market access | `profit = profit from round 2` |

## Manual challenge details

- Challenge name: "Invest & Expand".
- Manual budget: `50 000` XIRECs.
- Inputs: percentage allocation to Research, Scale, and Speed.
- Each allocation is between 0 and 100%.
- Total allocation cannot exceed 100%.
- The final submitted distribution is locked when the round ends.

Manual PnL formula:

```text
PnL = (Research x Scale x Speed) - Budget_Used
```

Research outcome:

```python
research(x) = 200_000 * np.log(1 + x) / np.log(1 + 100)
```

where `x` is the Research percentage allocation from 0 to 100.

Scale outcome:

- Linear from `0` at 0 invested to `7` at 100 invested.

Speed outcome:

- Rank-based across all players.
- Highest Speed investment receives a `0.9` multiplier.
- Lowest Speed investment receives a `0.1` multiplier.
- Everyone in between is scaled linearly by rank.
- Equal Speed investments share the same rank.

Speed examples from the source:

| Speed investments | Ranks | Multipliers |
| --- | --- | --- |
| `70, 70, 70, 50, 40, 40, 30` | `1, 1, 1, 4, 5, 5, 7` | top rank gets `0.9`; bottom rank gets `0.1`; ranks between are linearly scaled |
| `95, 20, 10` | `1, 2, 3` | `0.9, 0.5, 0.1` |

## Execution-relevant facts

- `Trader.run(state)` still returns `result, conversions, traderData`; the shared contract is defined in [../api/01_trader_contract.md](../api/01_trader_contract.md).
- Round 2 requires a `bid()` method only for bidding for extra market access in the final Round 2 simulation.
- `bid()` is ignored during Round 2 testing and ignored in other rounds.
- Extra market access changes the order book quotes available to trade against, not the matching rules.
- Manual Research, Scale, and Speed allocations are separate from the Python trading algorithm.

## Manual-only mechanics

- The `50 000` XIRECs budget allocation is submitted in the Manual Challenge Overview window.
- Participants can resubmit until round end.
- The last submitted distribution is processed.
- Manual budget allocation does not change `Trader.run()` or the Market Access Fee `bid()`.

## Source caveats

- The source references `Wiki_ROUND_2_data.zip`; the attachment itself is not stored in the wiki source capture.
- The exact tie behavior at the Market Access Fee cutoff is not specified beyond the provided median example and "top 50%" language.
- The exact randomization procedure for the 80% testing quote subset is not specified.
- The final challenge day or final simulation data distribution is not stated.
- The exact Round 2 deadline is not stated in the pasted source.
- Manual Speed depends on other players' Speed investments, so the final Speed multiplier cannot be known from the source alone before round close.
