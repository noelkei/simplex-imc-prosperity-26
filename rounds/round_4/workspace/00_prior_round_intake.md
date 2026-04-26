# Prior-Round Intake

## Current Round

- Round: `round_4`
- Date: `2026-04-26`
- Owner: `Codex`

## Candidate Prior Round

- Source round: `round_3`
- Why reuse is being considered:
  - same algorithmic products
  - same voucher family
  - same core option-book structure
  - new counterparty layer added in Round 4

## Prior-Round Compatibility Gate

| Check | Evidence | Verdict |
| --- | --- | --- |
| Products overlap | `round_3` and `round_4` wiki docs list the same algorithmic universe | yes |
| Mechanics overlap | shared `Trader.run()` contract and same tradable algorithmic products | yes |
| Constraints / limits overlap | Round 4 limits match Round 3 for algorithmic products | yes |
| Signal structure overlap | same `delta-1` plus `VEV_*` option-book problem | yes |
| New online fields or counterparties change the problem materially | Round 4 exposes `buyer` / `seller` participant names | yes |

- Compatibility verdict: `compatible`
- Summary rationale:
  Round 4 clearly continues the Round 3 algorithmic market, so product-role
  framing, anti-patterns, and backlog ideas transfer. However, visible
  counterparties are a real information change, so no Round 3 strategy
  conclusion should be auto-promoted without EDA revalidation.

## What Can Be Reused

| Item | Type | Why It Transfers | Caveat |
| --- | --- | --- | --- |
| `delta-1` versus option-book role framing | principle | same products and same option family | re-check if counterparties change execution priorities |
| `VEX` as likely anchor/context product | principle | same underlying / voucher structure | do not assume exact same fair-value behavior before EDA |
| `5000/5100/5200/5300` are not a homogeneous basket | principle | same strike set | verify whether counterparty behavior rescues any strike |
| toxic-strike veto, family imbalance, regime gating | hypothesis | these were high-ROI next tests in Round 3 | still untested in Round 4 |
| do not reopen the broad active basket by default | anti-pattern | strongly supported by Round 3 closeout | only reopen if Round 4 evidence is genuinely different |

## What Must Be Revalidated

| Item | Why Revalidation Is Needed | Suggested Check |
| --- | --- | --- |
| whether `delta-1` remains the best clean base | counterparties may add new alpha to other legs | compare markout and path quality by counterparty-aware slices |
| whether `5300` is still the only meaningful active strike | named participants may create new strike-specific behavior | cross-strike counterparty EDA |
| whether `5100/5200` are signal-only rather than inventory | this may change if specific participants systematically trade them | trade-flow and markout by participant and strike |
| shutdown / late-session logic | visible participants may make late trades more or less toxic | timing and participant concentration by session bucket |

## What Must Not Be Inherited

| Item | Why Not |
| --- | --- |
| exact Round 3 winners as immediate Round 4 champions | Round 4 adds counterparties and needs new data-driven validation |
| raw Round 3 thresholds / sizing assumptions | no current-round evidence yet |
| any assumption that buyer/seller fields are not useful | now directly contradicted by Round 4 facts and raw data |

## Downstream Use

- EDA:
  start by testing whether counterparty behavior changes the Round 3 product-role framing.
- Understanding:
  keep Round 3 lessons as `carry-forward principles`, not as Round 4 facts.
- Strategy:
  allow only compatibility-qualified reuse, with explicit revalidation notes.
- Validation:
  keep an eye on whether any product works better as signal than inventory once participant names are visible.
- Next action:
  create the first targeted EDA artifact on participant concentration, side asymmetry, product preference, and timing.
