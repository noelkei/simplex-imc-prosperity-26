# Trader Contract

Source basis: `docs/prosperity_wiki_raw/10_writing_an_algorithm_in_python.md`.

## Required class

Implement a predefined `Trader` class.

Required method:

```python
def run(self, state: TradingState):
    ...
```

Round-specific method:

```python
def bid(self):
    ...
```

- `run()` contains the trading logic.
- For Algorithmic Trading Round 2, `Trader` should also define `bid()`.
- Defining `bid()` in every submission is allowed; it is ignored for all rounds except Round 2.

## `run()` input

`run()` receives a `TradingState` object.

The `TradingState` contains:

- recent own trades
- recent market trades
- per-product order books
- current positions
- observations
- `traderData`

See [02_datamodel_reference.md](02_datamodel_reference.md) for field definitions.

## `run()` output

The method returns:

```python
return result, conversions, traderData
```

Fields:

- `result`: dictionary where each key is a product name and each value is a list of `Order` objects.
- `conversions`: integer conversion request value.
- `traderData`: string delivered back as `TradingState.traderData` on the next execution.

Order construction and quantity signs are defined in [../trading/02_orders_and_position_limits.md](../trading/02_orders_and_position_limits.md).

## Iteration model

- The simulation calls `run()` once for each new trading state.
- Each iteration gives the algorithm a fresh `TradingState`.

See [../trading/01_exchange_mechanics.md](../trading/01_exchange_mechanics.md) for exchange behavior.

## Submission identifiers

When a `Trader` implementation is submitted:

- a submission identifier is generated as a UUID, for example `59f81e67-f6c6-4254-b61e-39661eac6141`
- a `runID` is generated, for example `"498"`, `"499"`, or `"500"`

The source says these identifiers help Prosperity staff trace submissions.
