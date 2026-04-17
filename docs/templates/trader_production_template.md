# Trader Production Template

Use this as the minimal production-readiness reference for Prosperity `Trader` files. It is not a strategy and must not introduce round facts.

## Minimal Safe Skeleton

```python
from datamodel import Order, TradingState


class Trader:
    # If the active round wiki/spec requires a round-specific method such as bid(),
    # add the documented signature and behavior here. Do not infer it.

    def run(self, state: TradingState):
        result = {}
        conversions = 0
        traderData = state.traderData if isinstance(state.traderData, str) else ""

        # Strategy code should:
        # - use products/symbols from the reviewed round ingestion/spec only
        # - handle missing products and empty order books safely
        # - stay idle when signals are missing or invalid
        # - respect order signs and aggregate position-limit capacity
        # - avoid unsupported libraries and excessive runtime

        return result, conversions, traderData
```

## Submission Readiness Checklist

- [ ] `class Trader` exists.
- [ ] `run(self, state)` returns `result, conversions, traderData`.
- [ ] `result` maps product symbols to lists of `Order` objects.
- [ ] `conversions` is an integer-compatible value, normally `0` unless the spec requires conversions.
- [ ] `traderData` is a string and size risk is considered.
- [ ] Product symbols match ingestion/wiki facts and the reviewed spec.
- [ ] Order signs are correct: positive buy, negative sell.
- [ ] Position limits and aggregate order capacity are considered.
- [ ] Missing products, empty order books, and missing signals are handled safely.
- [ ] Round-specific methods such as `bid()` are considered.
- [ ] Imports are supported by the wiki runtime guidance.
- [ ] Implementation links to a reviewed or deadline-deferred strategy spec.
- [ ] Strategy signal, feature evidence, and regime assumptions are traceable through the linked spec.
- [ ] Latest validation run summary is linked.
- [ ] Pre-upload overfit / cheat audit is passed, failed, or explicitly caveated.
- [ ] Active submission file is verified.

## Pre-upload Overfit / Cheat Audit

Before final upload, quickly check for:

- [ ] Use of `timestamp`, day, iteration count, known sample length, or time-to-end assumptions.
- [ ] End-of-sample flattening, liquidation, or close-before-sample-end logic.
- [ ] Reads of platform `.json`, `.log`, `activitiesLog`, `graphLog`, or `tradeHistory`.
- [ ] File IO or external state not required by the reviewed spec.
- [ ] Random or seed-dependent behavior.
- [ ] Unsupported imports.
- [ ] Excessive logging.
- [ ] Hidden state that depends on sample-specific behavior.
- [ ] Suspicious constants that reference sample length rather than strategy parameters.

Outcome: `passed | failed | caveat`.

## Contract Smoke Check

- [ ] File can be imported in the expected Prosperity environment.
- [ ] `Trader` can be instantiated.
- [ ] `run()` can be called with a minimal/mock-compatible state or reviewed test fixture.
- [ ] Return value is a 3-item tuple.
- [ ] `result` is dict-like.
- [ ] `conversions` is integer-compatible.
- [ ] `traderData` is a string.
- [ ] No obvious unsupported imports, excessive logging, or runtime risks are present.
