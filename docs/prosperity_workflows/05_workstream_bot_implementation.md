# Workstream: Bot Implementation

Bot implementation turns a documented strategy into code that respects the Prosperity API and exchange constraints.

## Inputs

- Wiki API and datamodel docs for method signatures, return values, field names, order signs, and runtime constraints.
- The active round wiki doc for products and position limits.
- A strategy note or explicit implementation request.
- Debugging or validation findings when fixing existing behavior.

## Stable implementation constraints

- Implement against the `Trader.run(state)` contract and return `result, conversions, traderData`.
- Use wiki-defined order quantity signs: positive buys, negative sells.
- Respect per-product position limits and account for aggregate orders in an iteration.
- Treat `traderData` as the persistence path for state that must survive between calls.
- Keep runtime and supported-library constraints in mind when adding computation or imports.
- Do not infer official API behavior from `bots/` code or `performances/` outputs.

## Good outputs

- A focused code change tied to a stated strategy, bug, or validation need.
- Clear handling of missing products, empty order books, and current positions when relevant.
- Validation notes showing which constraints were checked.
- Any strategy parameters or assumptions documented near the handoff, not hidden as unexplained magic.

## Safe practice

- Keep strategy logic, risk/inventory logic, and execution behavior understandable enough to debug.
- Avoid broad rewrites when the task only needs a narrow implementation change.
- Do not add round facts directly from memory or sample code; use the wiki round docs.
- If a strategy assumption is unclear, document the assumption instead of pretending it is official.

## Handoff checklist

- What behavior was implemented or changed.
- Which wiki facts constrained the implementation.
- Which strategy assumption or heuristic the code follows.
- How position limits and order signs were checked.
- Tests, simulations, or logs reviewed.
- Known remaining risks.
