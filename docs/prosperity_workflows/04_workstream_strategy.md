# Workstream: Strategy Research

Strategy research converts facts and evidence into testable trading ideas. It should remain explicit about which claims are official facts and which are heuristics.

## Inputs

- Wiki facts for products, limits, API behavior, matching, and runtime constraints.
- EDA findings when available.
- Playbook heuristics for fair value, inventory management, risk, execution, and iteration.
- Current implementation context only when the task is to adapt or compare against existing code.

## Good outputs

- A strategy hypothesis with the expected source of edge.
- The fair value or signal definition, if applicable.
- Inventory and risk rules, including how the idea avoids limit rejection.
- Execution behavior: when it buys, sells, rests orders, or stays idle.
- Required state, if any, and whether it fits within `traderData` constraints.
- Test plan and known failure modes.

## Source discipline

Label claims clearly:

- "Wiki fact": official API, exchange, limit, runtime, platform, or round documentation.
- "EDA evidence": observed behavior from a named artifact or dataset.
- "Playbook heuristic": recommended pattern or risk habit.
- "Strategy assumption": a choice made for testing, not an official rule.

## Safe practice

- Avoid presenting one strategy pattern as the only correct approach.
- Keep round-specific strategy notes scoped to the active round or to examples of workflow.
- Prefer testable hypotheses over broad claims.
- Make risk and inventory behavior explicit before handing work to implementation.

## Handoff checklist

- Hypothesis and intended products or scope.
- Factual constraints from the wiki.
- Evidence used from EDA or logs.
- Heuristics used from the playbook.
- Parameters or assumptions to implement.
- Tests that would falsify or validate the idea.
