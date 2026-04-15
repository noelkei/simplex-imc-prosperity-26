# Workstream: Bot Implementation

Bot implementation turns a documented strategy into code that respects the Prosperity API and exchange constraints.

## Inputs

- Wiki API and datamodel docs for method signatures, return values, field names, order signs, and runtime constraints.
- The active round wiki doc for products and position limits.
- A reviewed strategy spec from the active round workstream. In fast mode this can be a one-page spec, but it must still define signal, execution, risk, state, and validation checks.
- Evidence traceability from the spec: linked EDA signals, feature evidence, regime assumptions, and understanding insight.
- The Trader production template: `docs/templates/trader_production_template.md`.
- Debugging or validation findings when fixing existing behavior.

## Stable implementation constraints

- Implement against the `Trader.run(state)` contract and return `result, conversions, traderData`.
- Use wiki-defined order quantity signs: positive buys, negative sells.
- Respect per-product position limits and account for aggregate orders in an iteration.
- Treat `traderData` as the persistence path for state that must survive between calls.
- Keep runtime and supported-library constraints in mind when adding computation or imports.
- Consider round-specific methods such as `bid()` before submission.
- Do not infer official API behavior from round-local or legacy bot code or performance outputs.
- Do not implement from a loose strategy note, chat summary, or performance result. If a reviewed spec is missing, create or request the spec before coding.

## Controlled variants

Variants are allowed only as controlled implementations of a reviewed or deadline-deferred spec.

- Change one axis per variant: parameter, threshold, execution logic, risk band, or feature toggle.
- Use naming: `candidate_<id>_v01_<short_name>.py`.
- Keep max 2 active implementation candidates total.
- Record parent spec, parent bot if any, insight being tested, changed axis, exact change, expected effect based on EDA/understanding, validation check, and linked run.
- Do not drift into a new strategy without updating the spec.
- If a variant tests a new signal, feature relationship, or regime assumption, update the strategy spec before coding.
- Archive superseded variants under the owner's `historical/` folder.

## Good outputs

- A focused code change under `rounds/round_X/bots/<member>/canonical/` tied to a reviewed strategy spec, bug, or validation need.
- Clear handling of missing products, empty order books, and current positions when relevant.
- Validation notes showing which constraints were checked.
- Any strategy parameters or assumptions documented in or linked from the strategy spec, not hidden as unexplained magic.
- Variant metadata that makes clear which insight is being tested and why the expected effect follows from EDA or understanding.

## Safe practice

- Keep strategy logic, risk/inventory logic, and execution behavior understandable enough to debug.
- Avoid broad rewrites when the task only needs a narrow implementation change.
- Do not add round facts directly from memory or sample code; use the wiki round docs.
- If a strategy assumption is unclear, return to the spec or record it as a blocker instead of pretending it is official.

## Handoff checklist

- What behavior was implemented or changed.
- Link to the reviewed strategy spec.
- Insight being implemented or tested, with EDA/understanding link when relevant.
- Link to the Trader production readiness checklist or note which items passed.
- Which wiki facts constrained the implementation.
- Which strategy assumption or heuristic the code follows.
- How position limits and order signs were checked.
- Tests, simulations, or logs reviewed.
- Known remaining risks.
