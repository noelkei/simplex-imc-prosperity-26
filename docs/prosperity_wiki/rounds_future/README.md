# Future Rounds

Use this folder for new round documents as Prosperity releases them.

## File rule

- Add one separate `.md` file per new round.
- Use a clear filename such as `round_2.md`.
- Match the structure of [../rounds/round_1.md](../rounds/round_1.md).
- Use only `docs/prosperity_wiki_raw/` as the source of truth.

## Required structure

Each future round file should include:

- Objective
- Tradable products
- Position limits
- Product behavior hints
- Algorithmic challenge details
- Manual challenge details
- Execution-relevant facts
- Manual-only mechanics
- Source caveats, if the source is inconsistent or unclear

## Extraction checklist

Extract only facts stated in the raw source:

- round objective
- algorithmic products
- manual products
- per-product limits
- source-stated product hints
- algorithmic challenge name and mechanics
- manual challenge name and mechanics
- execution-relevant facts for algorithm implementation
- manual-only facts that should not affect bot implementation

## Separation rule

Keep algorithmic and manual content separate.

- Algorithmic content affects algorithm implementation.
- Manual content belongs under "Manual challenge details" or "Manual-only mechanics".
- Do not convert product hints into strategy advice.
