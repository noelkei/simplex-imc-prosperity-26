# Strategy Spec: Round 3 Learning Batch Wave 2

## Status

`deferred under deadline`

## Review Status

- Status: `COMPLETED`
- Owner: `amin`
- Reviewer: `Unassigned`
- Reviewed on: `2026-04-25 (deadline deferral)`
- Deadline deferral reason: user explicitly requested immediate implementation, and the spec already captured signal, execution, risk, state, and validation requirements for the full Wave 2 batch

## Candidate

- Candidate ID: `Wave2-learning-batch`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`, `VEV_5400`, `VEV_5500`, `VEV_6000`, `VEV_6500`
- Linked candidate file: [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`
- Reviewer decision notes: explicit implementation direction from the user was used as a fast-mode deadline deferral; proceed with the full 19-bot cut
- Required changes before coding: none

## Objective

Implement a **post-synthesis Wave 2 batch** that does two jobs at once:

1. determine the best **champion architecture** after the 39-run synthesis,
2. keep a deliberate but disciplined coverage layer across the full tradable
   Round 3 universe so we do not leave potentially monetizable products
   completely unexplored.

This batch is intentionally split into:

- **Core bots (14)**: highest-ROI decision bots
- **Coverage-extension bots (5)**: smaller, lower-confidence, but still
  interpretable bots added because the user explicitly wants broader product
  exploitation across the tradable CSV universe

Total batch size: **19**

## Sources

- Wiki facts: [`../../../docs/prosperity_wiki/rounds/round_3.md`](../../../docs/prosperity_wiki/rounds/round_3.md), shared API and trading docs linked from `00_ingestion.md`
- EDA evidence: [`../01_eda/eda_option_surface_and_microstructure.md`](../01_eda/eda_option_surface_and_microstructure.md)
- Understanding summary: [`../02_understanding.md`](../02_understanding.md)
- Post-run research memory: [`../post_run_research_memory.md`](../post_run_research_memory.md)
- Current synthesis: [`../06_testing/round_3_full_performance_synthesis.md`](../06_testing/round_3_full_performance_synthesis.md)
- Path-quality artifacts:
  - [`../06_testing/artifacts/full_synthesis/full_path_family_summary.csv`](../06_testing/artifacts/full_synthesis/full_path_family_summary.csv)
  - [`../06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv`](../06_testing/artifacts/full_synthesis/full_path_reversal_candidates.csv)
- Strategy planning: [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)
- External paper research:
  - [`../../research/papers_processed/choi_2022_bachelier_guide_processed.md`](../../research/papers_processed/choi_2022_bachelier_guide_processed.md)
  - [`../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md`](../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md)
  - [`../../research/papers_processed/muravyev_2015_option_order_flow_processed.md`](../../research/papers_processed/muravyev_2015_option_order_flow_processed.md)
  - [`../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md`](../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md)
  - [`../../research/papers_processed/fengler_2005_surface_smoothing_processed.md`](../../research/papers_processed/fengler_2005_surface_smoothing_processed.md)
  - [`../../research/papers_processed/bergault_2022_multi_asset_mm_processed.md`](../../research/papers_processed/bergault_2022_multi_asset_mm_processed.md)

## Selection Trace

- Based on candidate: `03_next_wave_bot_planning.md`
- Signals used:
  - isolated delta-1 edge on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - ITM residual / anchor edge as an overlay rather than a base
  - selective active-voucher residual edge on `VEV_5300` and `VEV_5000 + VEV_5300`
  - path-analysis evidence that several active-voucher bots were `edge then reversal`
  - user-directed desire to maintain broader coverage over the tradable universe
- Alternatives considered:
  - another 25-bot broad learner sweep
  - reopening broad active baskets
  - reopening the surface branch
  - excluding floor and toxic strikes entirely from any future batch
- Why selected:
  - the synthesis is strong enough to shrink the core architecture to
    delta-1-first plus selective overlays
  - the path analysis justifies a new family of fast-unwind / time-stop / late-flatten bots
  - the user explicitly wants some controlled exploitation coverage across all
    tradable products
- Known caveats:
  - `VEV_5100`, `VEV_5200`, `VEV_6000`, and `VEV_6500` remain low-confidence and
    should appear only in tightly bounded coverage bots
  - the batch must stay interpretable enough to validate cleanly

## Evidence Traceability

- Linked EDA Signals:
  - delta-1 reversion / imbalance on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - intrinsic / extrinsic decomposition
  - extrinsic residual reversion
  - surface monotonicity / convexity as guardrail only
  - floor persistence for `VEV_6000` / `VEV_6500`
- Feature Evidence:
  - `wave1_delta1` mean final PnL `+547.158`
  - `wave1_itm` mean final PnL `+78.383`, with `VEX + ITM` positive
  - `wave1_active` mean final PnL `-4089.567`, but mean path peak `1691.109`
  - `wave1_surface` mean path peak only `25.359`
  - `VEV_5100` and `VEV_5200` as strongest strike-level negative evidence
- Multivariate Evidence:
  - `HYDROGEL_PACK` remains independent from the VEX/voucher branch
  - `VELVETFRUIT_EXTRACT` remains the strongest same-time valuation anchor
  - price-anchor family redundancy still favors one compact fair-value model
- Process / Distribution Assumptions:
  - live Round 3 is a distinct `TTE=5d` regime
  - selective active vouchers may still have monetizable entry edge even when
    their close-to-close PnL is poor
  - upper and floor names are execution problems first, alpha problems second
- Redundancy Decisions:
  - do not reopen broad basket residuals
  - do not reopen surface as a primary family
  - use ITM as overlay, not standalone champion
- Regime Assumptions:
  - late-session active-voucher behavior may be more dangerous than early-session behavior
  - floor regime still holds unless contradicted by live runs
- Understanding Insight:
  - split the round into a hydro branch and a VEX-plus-voucher branch
  - keep vouchers selective, not monolithic
- Research tool evidence used, if any:
  - path-quality summary from timestamp-level `activitiesLog` aggregation
- Evidence gaps or strategy assumptions:
  - the user explicitly wants broader product coverage, so this spec includes a
    coverage-extension layer for products that are not currently promotion-ready

## Batch Scope

- Batch size cap: `25`
- Recommended implemented set in this spec: `19`
- Intent: `learning / validation / architecture selection / controlled coverage`
- Promotion target: no single champion yet; the batch is meant to decide the Wave 2 champion family

## Strategy Families Covered

| Family | Products | Why Included |
| --- | --- | --- |
| Delta-1 champion controls | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | strongest clean live family |
| ITM passive / overlay refinement | `VEV_4000`, `VEV_4500` | historical winner family still matters, but as add-on |
| Selective Bachelier residual retests | `VEV_5300`, `VEV_5000 + VEV_5300` | fair clean re-test of the surviving active subset |
| Active path-rescue bots | `VEV_5300`, `VEV_5000 + VEV_5300` | entry edge exists, retention is broken |
| Inventory / imbalance selective overlays | `VEV_5000 + VEV_5300`, `VEX + VEV_5300` | strongest paper-derived gaps still open |
| Upper anchored / passive refinement | `VEV_5400`, `VEV_5500` with or without `VEX` | keep some monetization attempt alive without reopening the whole branch |
| Toxic-strike controlled rescue | `VEV_5100`, `VEV_5200` | user-directed full-product coverage under tiny-risk, non-promotional conditions |
| Floor micro probes | `VEV_6000`, `VEV_6500` | user-directed full-product coverage under floor-aware, ultra-defensive conditions |

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run(state)` | wiki API docs | implement | all bots return `result, conversions, traderData` | compile and smoke-run |
| Round 3 product list | round doc | implement | coverage limited to official Round 3 symbols only | product names match live artifacts |
| Position limits `200` for delta-1 and `300` per voucher | round doc | implement | all position sizing and inventory overlays must respect these hard caps | final positions and order sizes stay within limits |
| Integer pricing | exchange docs | implement | quote and fair values round to ints before order placement | no float order prices |
| Conversions | round doc | exclude | no conversions used in this wave | `conversions = 0` |
| Manual Bio-Pod challenge | round doc | not applicable | excluded from algorithmic bot logic | no Bio-Pod symbols in code |
| Live regime `TTE=5d` | round doc + challenge brief | implement | expiry-aware exit logic and caution variants may use session-time logic, not hidden multi-day TTE estimates | time-stop / flatten behavior visible in runs |
| `traderData` state persistence | API docs | implement | store EMA anchors, previous mids, time-stop state, and mode flags compactly | state stays serializable and bounded |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01 Delta-1 reversion fair | top-of-book best bid / ask, mid, position | usable online | direct signal | previous-mid lookback, spread gate, max lean | separate from voucher branch; strongest standalone live family | short-horizon mean reversion survives with cleaner execution | keep as core base family | stay idle on missing book | previous mid and optional spread state | compare to Wave 1 `L01/L04/L06` |
| F02 Passive / spread-sensitive delta-1 execution | best bid / ask, spread, position | usable online | execution filter | quote distance, passive/active mode, spread threshold | complements F01 rather than replaces it | HYDRO may have edge only if it stops crossing too much | keep as carry-forward gap closer | revert to idle or one-sided quoting | previous mode and fill-side flags | `W2-02` should clarify whether HYDRO is execution- or signal-limited |
| F03 Centered Bachelier residual on selective subset | VEX mid, voucher mid, strike, position | usable online | direct signal | residual EMA anchor, edge threshold, symbol universe | VEX is the anchor; price-anchor redundancy still argues for one compact fair model | selective strikes can still mean-revert around fair | keep for `5300` and `5000+5300`; exclude broad basket | stay idle on missing VEX or voucher book | residual anchor EMA per active symbol | compare to Wave 1 `L15/L16/L25` and broad C06 failures |
| F04 Fast take-profit / time-stop | current mark-to-market edge, entry timestamp, current inventory | usable online | risk control | take-profit band, max hold ticks, force-flat trigger | targets path reversal, not a new alpha source | selective active legs lose because they hold too long after edge realization | keep as primary rescue axis | if state missing, flatten and reset | entry timestamp, entry-side, running mode | path peak retention should improve vs Wave 1 selective active bots |
| F05 Late-session flatten / shutdown | current timestamp, current position, current edge | usable online | risk control | no-new-entry time, hard-flat time | targets expiry/tail risk, not core fair value | late session is toxic for selective active vouchers | keep as separate rescue axis from F04 | stop new entries or flatten | current session mode only | compare early-vs-late PnL retention |
| F06 Inventory overlay on clean subset | current position, per-product limits | usable online | risk control | linear skew coefficient, max one-sided inventory | supports selective subset only | inventory helps only after strike pruning | keep only for `5000+5300`, not broad basket | zero skew if state is missing | current positions only | compare to same subset without overlay |
| F07 VEX sidecar / anchor leg | VEX book, VEX position | usable online | direct signal / combo support | same params as delta-1 bots | VEX is the best combo leg across evidence | VEX can carry mixed bots while voucher leg is selective | keep as default combo sidecar | run voucher branch only if VEX missing | previous VEX mid | combo bot should not simply devolve into pure VEX PnL |
| F08 Voucher imbalance confirmation | voucher best bid/ask sizes, VEX sizes optional | usable online | execution filter | imbalance threshold, agreement rule, de-risk rule | Muravyev-style modifier, not standalone alpha | imbalance helps mainly as pressure/selection filter | keep only as supporting feature | fall back to residual-only logic | none or lightweight recent imbalance cache | should improve retention or selectivity, not trade count alone |
| F09 Upper anchored passive quoting | upper-strike book, optional VEX book, position | usable online | execution style / direct signal | passive quote offset, anchor bias, max size | upper branch is execution-dominated | upper edge may need anchoring plus passive posture | keep as narrow research branch | stay idle on thin books | optional anchor flag | compare to `L24` and `L21-L23` |
| F10 Toxic-strike micro-rescue | `VEV_5100` or `VEV_5200` book, optional `VEX` or `VEV_5300` sidecar, position | usable online | coverage rescue | tiny max size, hard time-stop, hard stop-loss | contradicted by current evidence; included only under user directive | these strikes may only be tradable as tiny anchored scalps | downgraded from main branch to coverage-only | stay idle if not in ideal setup | entry timestamp and tiny-risk mode | must show cleaner path or gets permanently excluded |
| F11 Floor micro probe | `VEV_6000` / `VEV_6500` book, spread, position | usable online | coverage rescue / diagnostic | tiny passive size, floor-break trigger, zero-cross rule | current evidence says floor, not alpha | occasional one-tick passive or floor-break opportunities might exist | keep only because user asked for whole-universe coverage | default idle unless floor conditions trigger | minimal floor-state flags | if still zero activity/zero edge, close the family permanently |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| broad active basket `5000+5100+5200+5300` | repeated failures and strike toxicity | a new structural thesis overturns current evidence |
| pure surface relative-value family | current implementation shows almost no positive path | a new signal definition replaces current local spread EMA |
| CRR online pricing as a primary live fair model | benchmark-quality idea, not yet worth live batch budget | Bachelier selective retests fail in a way that points to model bias |
| Bergault-style family portfolio coupling as a main live control engine | too heavy before simpler selective subset tests survive | the clean subset survives and inventory still dominates losses |
| floor names as standard directional alpha products | current evidence says floor persistence | a live run breaks the floor regime materially |
| unrestricted `VEV_5100` / `VEV_5200` inclusion | strongest negative strike evidence in the round | tiny rescue bots show real retained edge |

## Signal / Fair Value Logic

- Signal:
  - For delta-1 bots: short-horizon mid reversion with spread-aware execution.
  - For selective voucher bots: centered Bachelier residual on `5300` or `5000 + 5300`.
  - For path-rescue bots: same selective residual or combo entry, but with
    explicit profit-capture and hold-horizon logic.
  - For coverage bots: anchored, tiny-risk versions only.
- Inputs:
  - best bid / ask, top-level volumes, mid, current position, timestamp
  - `VELVETFRUIT_EXTRACT` mid as underlying anchor for voucher bots
  - strike metadata from product symbol
- Missing-signal behavior:
  - idle by default; no synthetic backfilling beyond simple EMA anchors
- Process assumption that would invalidate this logic:
  - if selective active vouchers show no path improvement even under fast exits,
    then the branch should be treated as structurally weak rather than badly held
- Multivariate or redundancy caveat:
  - keep one compact fair model and one rescue axis at a time; do not stack
    multiple valuation schemes into one bot

## Execution Logic

- Buy behavior:
  - buy when delta-1 fair or selective voucher fair indicates undervaluation
    and spread / imbalance / time filters allow entry
- Sell behavior:
  - sell when fair indicates overvaluation, or when take-profit / late-flatten /
    hard-risk logic forces exit
- Passive/resting order behavior:
  - preferred for HYDRO passive, ITM passive, upper anchored passive, and floor
    micro probes
  - selective active bots may still cross occasionally, but only under bounded
    edge and bounded size conditions
- Stay-idle behavior:
  - idle on missing books, too-wide spreads, late-session blocked windows, or
    when tiny-risk coverage conditions are not present

## Position And Risk Handling

- Position limits:
  - `200` for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - `300` per voucher symbol
- Aggregate buy capacity:
  - bounded per symbol by remaining limit and per-bot per-iteration caps
- Aggregate sell capacity:
  - bounded per symbol by current long plus short capacity
- Inventory skew or reduction:
  - only explicit on the clean `5000 + 5300` inventory bots
  - coverage bots on `5100`, `5200`, `6000`, `6500` should use much smaller
    hard caps than the exchange maximums

## State And Runtime

- `traderData` use:
  - previous mids for delta-1
  - residual EMA anchors for selective vouchers
  - entry timestamps / position mode for fast-unwind bots
  - late-session mode flags
  - minimal floor-state flags for `6000/6500`
- Imports:
  - stdlib only
- Runtime risk:
  - too many variants could tempt code duplication; implementation should keep
    shared helpers compact
- Research-only dependencies excluded from uploadable bot: `yes`

## Bot Batch

### Core Decision Bots (14)

- `W2-01` delta-1 champion control: `HYDRO + VEX`
- `W2-02` HYDRO passive / wider-spread execution carry-forward
- `W2-03` ITM passive pair carry-forward: `VEV_4000 + VEV_4500`
- `W2-04` delta-1 + ITM overlay control
- `W2-05` selective Bachelier residual: `VEV_5300`
- `W2-06` selective Bachelier residual: `VEV_5000 + VEV_5300`
- `W2-07` `VEV_5300` fast take-profit / time-stop
- `W2-08` `VEV_5000 + VEV_5300` fast take-profit / time-stop
- `W2-09` `VEV_5300` late-session flatten / shutdown
- `W2-10` `VEV_5000 + VEV_5300` late-session flatten / shutdown
- `W2-11` `VEV_5000 + VEV_5300` inventory overlay on top of rescue logic
- `W2-12` `VEX + VEV_5300` fast-unwind combo
- `W2-13` selective active imbalance filter bot (`VEV_5300` or `VEV_5000 + VEV_5300`)
- `W2-14` upper anchored passive refinement (`VEX + VEV_5400 + VEV_5500` or `VEV_5400 + VEV_5500`)

### Coverage-Extension Bots (5)

- `W2-15` `VEV_5100` tiny-risk rescue bot
- `W2-16` `VEV_5200` tiny-risk rescue bot
- `W2-17` active/upper bridge: `VEV_5300 + VEV_5400 + VEV_5500`
- `W2-18` VEX-plus-upper anchored combo
- `W2-19` floor micro probe: `VEV_6000 + VEV_6500`

## Variant Rules

- One main hypothesis per bot.
- Core bots should decide architecture; coverage bots should never be used as
  promotion evidence unless they win cleanly and interpretably.
- `VEV_5100`, `VEV_5200`, `VEV_6000`, and `VEV_6500` are coverage-only in this spec.
- No bot may reopen the broad basket or the old composite architecture.
- Surface logic remains excluded from this wave.

## Expected Failure Cases

- Failure case: delta-1 control underperforms because Wave 1 success was noise
  - Mitigation or validation: compare to `L06` and standalone product controls
- Failure case: selective voucher rescue bots still reverse heavily after entry
  - Mitigation or validation: examine peak retention and late-session giveback
- Failure case: inventory overlay suppresses too much selective active alpha
  - Mitigation or validation: compare `W2-11` directly against `W2-08` / `W2-10`
- Failure case: toxic-strike rescue bots lose immediately despite tiny risk
  - Mitigation or validation: treat as permanent branch closure
- Failure case: floor bots never trade or never show positive path
  - Mitigation or validation: use this as final evidence to close the floor branch

## Validation Plan

- Contract checks:
  - verify order signs, integer prices, and per-symbol limits
  - verify `traderData` remains compact and serializable
- Order sign and limit checks:
  - focus especially on coverage bots with tiny intended size
- Performance/run checks:
  - rank by real platform PnL from JSON `profit` or `activitiesLog` final-sum
  - inspect path quality, not only final PnL
  - compare peak, end-from-peak, and positive-time ratio for selective voucher rescue bots
  - compare combo bots versus their base legs to see whether overlays add value
- Debug signals to inspect:
  - selective active entry timestamps
  - time-to-peak and giveback after peak
  - late-session PnL erosion
  - final inventory concentration
  - floor-name trade count and any deviation from `0.5` behavior

## Implementation Handoff

- Target bot path, normally `rounds/round_3/bots/<member>/canonical/...`:
  - `rounds/round_3/bots/amin/canonical/` for the new Wave 2 batch
- Generated implementation manifest:
  - `rounds/round_3/workspace/05_implementation/learning_batch_wave2_manifest.md`
- Parameters to implement:
  - delta-1 spread gates and passive offsets
  - selective Bachelier residual thresholds on `5300` and `5000 + 5300`
  - take-profit, max-hold, no-new-entry, and hard-flat times
  - inventory skew only on the clean subset
  - tiny-risk caps for `5100`, `5200`, `6000`, `6500`
- Known caveats:
  - this spec intentionally mixes high-confidence core bots and lower-confidence
    coverage bots because the user explicitly asked for broader product exploitation
  - coverage wins should be treated as welcome surprises, not expected base cases
