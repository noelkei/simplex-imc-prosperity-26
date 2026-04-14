# Runtime and Resources

Source basis:

- `docs/prosperity_wiki_raw/10_writing_an_algorithm_in_python.md`
- `docs/prosperity_wiki_raw/09_programming_resources.md`

## Simulation size

- Testing on historical data: `1_000` iterations.
- Final simulation for round PnL: `10_000` iterations.

## Runtime limit

- Each `run()` call should generate a response in `900ms`.
- The source says the average should be `<= 100ms`.
- If the call exceeds the limit, the function call times out.

## Stateless container

- The trading container is based on an Amazon Web Services Lambda function.
- The source says AWS cannot guarantee class variables or global variables remain in place on subsequent calls.
- Use `traderData` for state that must be delivered to the next execution.

## `traderData`

- `traderData` is a string returned by `Trader.run()`.
- It is delivered back as `TradingState.traderData` on the next execution.
- Python variables can be serialized to string with `jsonpickle` and deserialized on the next call.
- The container does not interfere with the content.
- The external framework cuts the string to `50 000` characters.
- The source warns that this can make restored values unusable.

## Conversions

`Trader.run()` returns a `conversions` value for conversion requests.

Source conditions:

- You need to obtain either a long or short position earlier.
- A conversion request cannot exceed possessed item count.
- If you have 10 items short (`-10`), you can only request from 1 to 10.
- A request for 11 or more in that case is fully ignored.
- Conversion requires covering transportation and import/export tariff.
- Conversion request is not mandatory.
- You can send `0` or `None`.

## Supported libraries

The source says all standard Python libraries included in Python 3.12 are fully supported.

It also lists:

- `pandas`
- `NumPy`
- `statistics`
- `math`
- `typing`
- `jsonpickle`

The source says importing other external libraries is not supported.

## Sample data and logs

- For every new product, several days of sample data are provided.
- For each sample day, two `.csv` files are available:
  - trades done on that day
  - market orders at every time step
- On upload, the algorithm is tested for 1000 iterations using data from a sample day different from the actual challenge day.
- A log file is provided after the run.
- The log file includes output from `print` statements inside `run()`.

## Local tooling

- All algorithmic trading happens in Python.
- The raw docs recommend a recent Python 3 version, with Python 3.12 given as an example.
- The raw docs recommend using a text editor or IDE with Python syntax highlighting, with VS Code given as an example.
