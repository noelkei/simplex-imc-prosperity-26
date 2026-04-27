# Processed Paper Summary

## Status

`draft`

## Paper Metadata

- Paper ID: `goncalves_pinto_sala_2025_incremental_option_volume`
- Title: `Does Option Volume Convey Incremental Information? Evidence from Synthetic Stock Benchmarks`
- Source / venue: `working paper`
- Authors: `Luis Goncalves-Pinto`, `Carlo Sala`
- Year: `2025`
- Raw file: [goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_raw/goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.pdf)
- Markdown file: [goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.md](/Users/noelp/PycharmProjects/simplex-imc-prosperity-26/rounds/round_4/research/papers_md/goncalves_pinto_sala_2025_does_option_volume_convey_incremental_information_evidence_from_synthetic_stock_benchmarks.md)
- Link: [SSRN abstract 5341921](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5341921)

## Core Claim

- Option volume should only be treated as informative if it predicts returns beyond what is already encoded in synthetic option-implied benchmarks. Much apparent option-volume predictability becomes weak, negligible, or sign-reversing under that stricter test.

## Assumptions

- We cannot build the paper's exact synthetic-stock benchmark in Prosperity.
- The useful lesson is methodological: flow-based claims need an incremental-value test against prices, anchors, and local surface information.
- `round_4` already has enough baseline state from `VEX`, spreads, depth, and cross-strike structure to run simpler benchmark logic.

## Problem Addressed for Round 4

- We need a strong external reason not to overpromote counterparty or voucher-flow signals just because they look narratively appealing.
- Our EDA already showed that raw participant names add little alone and engineered context matters more; this paper provides the right validation posture.

## What This Paper Gives Us

- Formula / approximation:
  a benchmark discipline for asking whether flow adds information beyond what prices already imply.
- Constraints / checks:
  exact synthetic-return construction is unavailable in our game setting.
- Point of view:
  option-flow signals should earn their place by beating a baseline, not by sounding microstructurally interesting.
- Simplification:
  test any flow feature against a baseline containing `VEX`, spread, depth, and local surface context.

## Relevance To Current Round

| Current-Round Signal / Risk / Open Question | Relevance | Strength | Caveat |
| --- | --- | --- | --- |
| raw counterparty names add little alone | directly reinforces current finding | high | paper is about volume, not visible names |
| engineered context beats naive flow stories | supports our feature ladder | high | needs local validation, not blind import |
| `Mark 22` and upper-strike danger-state claims | useful benchmark discipline | medium | does not tell us the sign or exact threshold |
| residual or surface-aware features vs flow | encourages incremental-value testing | high | no exact synthetic benchmark available |

## Round X Mapping

- Map the paper's benchmark logic to:
  - `baseline model first`
  - `add counterparty / flow features second`
  - keep only what improves decisions materially.
- Use it as a rule for feature promotion, not as a source of a live signal.

## Minimal Usable Adaptation

- Online-usable adaptation:
  none directly; the main adaptation is in offline validation discipline.
- Required proxy or simplification:
  compare candidate flow features against a simple baseline using `VEX`, spread, imbalance, depth, and local cross-strike context.
- Runtime / state caveat:
  should constrain research and validation, not add runtime complexity.
- Implementability: `validation-only`

## Strategy Implications

- Candidate or execution idea:
  no direct new candidate; instead, require flow-based ideas to clear a tougher incremental-value bar.
- Failure mode addressed:
  building strategies around counterparty or option-flow narratives that do not add beyond obvious market state.
- Validation implication:
  every counterparty or flow-heavy candidate should be benchmarked against a simpler anchor/book-state variant.

## Do Not Overuse

- Do not read this as proof that all option flow is useless.
- Do not turn benchmark discipline into a reason to reject every contextual feature before testing.
- Do not attempt to reconstruct the full synthetic-benchmark machinery in the live bot.

## Risks And Limitations

- The paper studies a richer listed-options environment than Prosperity.
- The exact benchmark object does not transport directly.
- Its main value is to prevent overclaiming, not to generate alpha.

## Action Classification

- Classification: `validation check`
- Why:
  this is the cleanest guardrail for deciding whether a flow- or counterparty-based feature is genuinely additive or just redescribing baseline state.

## Strategy Hooks

- `baseline_then_context_model_ladder`
- `flow_feature_incremental_value_gate`
- `reject_flow_signal_without_anchor_adjusted_lift`

## Notes

- Strategy must later classify actual use as `used | hybrid | validation | rejected | inspiration-only`.
- Keep paper facts/paraphrase in `Paper Metadata` and `Core Claim`; keep current-round interpretation in `Relevance`, `Round X Mapping`, `Minimal Usable Adaptation`, and `Strategy Hooks`.
- Note:
  this paper should influence how we trust signals more than which signals we invent.
