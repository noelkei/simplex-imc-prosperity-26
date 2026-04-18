# Round 2 - "Growing Your Outpost"

Source capture: Round 2 Notion wiki content pasted by Noel on 2026-04-18.

## Round Objective

It is the second trading round, and the final opportunity to reach the threshold goal of a net PnL of 200,000 XIRECs or more before the leaderboard resets for Phase 2. These first 2 rounds act as qualifiers for the final mission.

Trading activity has accelerated significantly since arrival. With the outposts actively trading Ash-Coated Osmium and Intarian Pepper Root, the market has become increasingly competitive and dynamic.

In Round 2 on Intara, participants continue trading `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`. This time, participants have the opportunity to gain access to additional market volume. To compete for this increased capacity, participants must incorporate a Market Access Fee bid into the Python program.

Participants should also analyze previous round performance and refine the algorithm accordingly.

XIREN has provided a 50,000 XIRECs investment budget to allocate across three growth pillars to accelerate outpost development. Participants must decide how to distribute this budget strategically to maximize profit once the trading round closes.

Objective: optimize the Python program to trade `ASH_COATED_OSMIUM` and `INTARIAN_PEPPER_ROOT`, incorporate a Market Access Fee to potentially gain access to additional market volume, and allocate the 50,000 XIRECs investment budget across three growth pillars.

## Algorithmic Trading Challenge: "limited Market Access"

Attachment referenced by the source: `Wiki_ROUND_2_data.zip`.

Products:

- `INTARIAN_PEPPER_ROOT`
- `ASH_COATED_OSMIUM`

Position limits:

- `ASH_COATED_OSMIUM`: 80
- `INTARIAN_PEPPER_ROOT`: 80

In this round, participants can bid for 25% more quotes in the order book. The volumes and prices of these quotes fit perfectly in the distribution of the already available quotes.

Example extra market access:

Order book for participants with no extra market access:

- ask, 10 volume, $9
- ask, 10 volume, $7
- bid, 10 volume, $5
- bid, 5 volume, $4

Order book for participants with extra market access:

- ask, 10 volume, $9
- ask, 5 volume, $8, extra flow to trade against
- ask, 10 volume, $7
- bid, 10 volume, $5
- bid, 5 volume, $4

Participants bid for extra market access by incorporating a `bid()` function inside `class Trader`:

```python
class Trader:
    def bid(self):
        return 15

    def run(self, state: TradingState):
        (Implementation)
```

The Market Access Fee is a one-time fee at the start of Round 2 paid only if the bid is accepted. It only determines who gets extra market access and is not used in the simulation dynamics. The top 50% of bids across all participants are accepted.

Example bidding mechanism:

- Bids: `[10, 20, 15, 19, 21, 34]`
- Accepted: `[No, Yes, No, No, Yes, Yes]`
- Explanation: the median of the bids is 19.5, so all bids higher than 19.5 are accepted. These participants get extra market access flow while paying the price they bid, and all bids below 19.5 are rejected and do not pay the fee.

Accepted bids are subtracted from Round 2 profits to compute final PnL:

- For participants with full market access, `profit = profit from round 2 - bid for getting full market access`.
- For participants with no full market access, `profit = profit from round 2`.

The Market Access Fee is unique to Round 2 and does not apply to any other round. Any `bid()` function in Rounds 1, 3, 4, and 5 is ignored.

The Market Access Fee is ignored during testing of Round 2 because bids are only compared when the final simulation of Round 2 starts. It is a blind auction for extra flow.

During testing of Round 2, the default set of quotes is 80% of all generated quotes, i.e. no extra market access. This 80% has been slightly randomized for every submission to reflect real-world conditions where not all patterns in trading behavior are up 100% of the time.

Game theory note: to get extra market access, a participant only needs to be in the top 50% of bidders, not necessarily the highest bidder. Placing an extremely high bid will almost certainly yield full market access, but participants may be able to save XIRECs by bidding less while staying in the top 50% of bidders.

## Manual Trading Challenge: "Invest & Expand"

Participants expand the outpost into a market making firm with a budget of `50 000` XIRECs. This budget is allocated across three pillars:

- Research
- Scale
- Speed

Participants choose percentages for each pillar between 0 and 100%. Total allocation cannot exceed 100%.

Final PnL score:

```text
PnL = (Research x Scale x Speed) - Budget_Used
```

### Pillars

Research determines trading edge. It grows logarithmically from `0` for `0` invested to `200 000` for `100` invested. Formula:

```python
research(x) = 200_000 * np.log(1 + x) / np.log(1 + 100)
```

Scale determines how broadly the strategy is deployed across markets. It grows linearly from `0` for `0` invested to `7` for `100` invested.

Speed determines how often targeted trades are won. It is rank-based across all players:

- Highest speed investment receives a `0.9` multiplier.
- Lowest receives `0.1`.
- Everyone in between is scaled linearly by rank.
- Equal investments share the same rank.

Example: if people invested `70, 70, 70, 50, 40, 40, 30`, they get ranks `1, 1, 1, 4, 5, 5, 7`. The first three players get `0.9`, the last player gets `0.1`, and everyone in between is linearly scaled between top and bottom rank.

Example: if three players invest `95, 20, 10`, their ranks are `1, 2, 3`, and hit rates are `0.9, 0.5, 0.1`.

Research, Scale, and Speed outcomes are multiplied together to form gross PnL. The used part of the budget is then deducted.

## Submit Your Orders

Participants choose the distribution of budget by assigning percentages to the three pillars directly in the Manual Challenge Overview window and clicking the Submit button. Participants can resubmit new distributions until the end of the trading round. When the round ends, the last submitted distribution is locked in and processed.
