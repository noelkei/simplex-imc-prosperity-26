# Add New Round

Use this skill when documenting a newly released Prosperity round in the repo wiki.

## Required sources

- Wiki structure: `../docs/prosperity_wiki/README.md`
- Future-round guidance: `../docs/prosperity_wiki/rounds_future/README.md`
- Shared facts: `../docs/prosperity_wiki/api/`, `../docs/prosperity_wiki/trading/`, `../docs/prosperity_wiki/platform/`
- Workflow: `../docs/prosperity_workflows/07_workstream_round_preparation.md`
- Safe changes: `../docs/prosperity_workflows/09_safe_change_rules.md`

## Steps

1. Confirm the new round material is in the accepted factual source set for this repo.
2. Follow the existing round wiki structure; do not add strategy advice to round facts.
3. Extract products, limits, challenge names, algorithmic facts, manual facts, and source caveats.
4. Keep manual-only mechanics separate from bot implementation requirements.
5. If the source appears to change the API contract, quote or paraphrase the exact source and mark the caveat before implementation depends on it.
6. Do not use `bots/`, `performances/`, sample outputs, or memory as authority.
7. Handoff with reviewed sources, new or updated round doc path, unresolved facts, and downstream actions.
