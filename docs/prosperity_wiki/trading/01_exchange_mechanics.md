# Exchange Mechanics

Source basis:

- `docs/prosperity_wiki_raw/10_writing_an_algorithm_in_python.md`
- `docs/prosperity_wiki_raw/08_trading_glossary.md`
- `docs/prosperity_wiki_raw/05_game_mechanics_overview.md`

## Market participants

- The algorithm trades on Prosperity's exchange against Prosperity trading bots.
- Algorithms from different players trade separately.
- There is no interaction between algorithms of different players.

## Matching

BUY order behavior:

- A BUY order executes immediately if there is an active SELL order with price equal to or lower than the BUY order price.
- The trade price is the SELL order price.
- The executed quantity is the minimum of the BUY and SELL quantities.
- If the SELL quantity is smaller than the BUY quantity, the remaining BUY quantity can rest in the market.

SELL order behavior:

- A SELL order executes immediately if there is an active BUY order with price equal to or higher than the SELL order price.
- The higher buy price is better for the seller.
- Apart from side symmetry, SELL orders behave like BUY orders.

## Price-time priority

Prosperity uses price-time priority:

- Incoming orders first match against the existing order with the most attractive price from the incoming order's perspective.
- If multiple orders exist at that price level, the oldest order is executed first.

## Resting quotes

- If an algorithm order does not execute immediately, or only partially executes, the remaining quantity is visible to bots.
- Bots may decide to trade against that remaining quote during the iteration.
- If no bot trades against the remaining quote, it is cancelled at the end of the iteration.
- After cancellation and before the next `TradingState`, bots may also trade with each other.

## Timing

- Order execution on Prosperity's exchange is instantaneous.
- The source says player orders arrive at the exchange matching engine without delay.
- The source says no bot can send an order faster than the player's order and get the opportunity instead.

## Order book state

- `TradingState.order_depths` contains buy and sell orders per product that originated from bots and are available to trade with.
- Every buy price level should be strictly lower than every sell price level.
- If this is not true, the source says there is a potential match and a bot trade should have happened.

Order and volume signs are defined in [02_orders_and_position_limits.md](02_orders_and_position_limits.md).
