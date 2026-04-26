# Strategy Spec: Round 3 Learning Batch Wave 3

## Status

`deferred under deadline`

## Review Status

- Status: `COMPLETED`
- Owner: `amin`
- Reviewer: `Unassigned`
- Reviewed on: `2026-04-26 (deadline deferral)`
- Deadline deferral reason: the user explicitly requested immediate Wave 3 specification plus implementation, and the planning artifact already narrowed the next wave to a traceable final exploratory cut

## Candidate

- Candidate ID: `Wave3-learning-batch`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500`, `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
- Linked candidate file: [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`
- Reviewer decision notes: the user explicitly asked for the full Wave 3 spec and bot implementation now; proceed with the final exploratory cut instead of waiting for a separate formal review loop
- Required changes before coding: none

## Objective

Implement a **last or penultimate exploratory Round 3 wave** that is no longer
about broad coverage, but about closing the highest-value architecture
questions before we pivot into final-bot selection.

This batch should do four jobs:

1. keep a clean **delta-1 champion path** alive,
2. try the best remaining **`VEV_5300` rescue designs** under explicit
   no-trade / no-new-entry logic,
3. decide whether toxic active strikes become useful only as **tiny inverse
   diagnostics**,
4. test a very small number of **higher-complexity but still online-usable**
   refinements: transformed thresholds, lightweight trend gating, and one or
   two Kalman adaptations.

Total batch size: **24**

## Sources

- Wiki facts: [`../../../docs/prosperity_wiki/rounds/round_3.md`](../../../docs/prosperity_wiki/rounds/round_3.md), shared API and trading docs linked from `00_ingestion.md`
- EDA evidence: [`../01_eda/eda_option_surface_and_microstructure.md`](../01_eda/eda_option_surface_and_microstructure.md)
- Understanding summary: [`../02_understanding.md`](../02_understanding.md)
- Post-run research memory: [`../post_run_research_memory.md`](../post_run_research_memory.md)
- Full synthesis: [`../06_testing/round_3_full_performance_synthesis.md`](../06_testing/round_3_full_performance_synthesis.md)
- Key full-synthesis artifacts:
  - [`../06_testing/artifacts/full_synthesis/full_run_metrics.csv`](../06_testing/artifacts/full_synthesis/full_run_metrics.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_runs.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_runs.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv)
  - [`../06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv`](../06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
- Strategy planning: [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)
- External paper research:
  - [`../../research/papers_processed/choi_2022_bachelier_guide_processed.md`](../../research/papers_processed/choi_2022_bachelier_guide_processed.md)
  - [`../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md`](../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md)
  - [`../../research/papers_processed/muravyev_2015_option_order_flow_processed.md`](../../research/papers_processed/muravyev_2015_option_order_flow_processed.md)
  - [`../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md`](../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md)
  - [`../../research/papers_processed/fengler_2005_surface_smoothing_processed.md`](../../research/papers_processed/fengler_2005_surface_smoothing_processed.md)

## Selection Trace

- Based on candidate: `03_next_wave_bot_planning.md`
- Signals used:
  - clean positive delta-1 evidence on `HYDROGEL_PACK` and
    `VELVETFRUIT_EXTRACT`
  - historical `VEX + ITM` family still positive enough to deserve one cleaner
    active refresh
  - `VEV_5300` as the only active strike with positive `10k` mean markout
  - repeated evidence that many selective active runs are `edge then reversal`,
    not pure `no edge`
  - repeated evidence that `VEV_5000`, `VEV_5100`, and `VEV_5200` stay
    negative in the ordinary direction
- Alternatives considered:
  - stop exploration now and move directly to final-bot exploitation
  - reopen the old broad active basket because some legacy runs reached `+5k`,
    `+10k`, or even `+18k`
  - jump immediately to HMM/Markov-style regime detection
  - skip inverse tests and close toxic strikes without one last sign check
- Why selected:
  - the user explicitly wants the next wave to include regime/no-trade ideas,
    trend ideas, nonlinear thresholds, inverse tests, and Kalman where it makes
    sense
  - the current evidence is strong enough to make the next exploration wave
    targeted instead of broad
  - a final architecture choice still needs cleaner evidence on `5300`,
    `VEX + ITM`, and toxic-strike sign direction
- Known caveats:
  - `VEV_5300` still may fail even in the best rescue design
  - inverse bots are diagnostic slots, not promotion defaults
  - Kalman is included only as a compact online proxy, not as a license for
    hidden-state complexity

## Evidence Traceability

- Linked EDA Signals:
  - delta-1 reversion on `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - intrinsic / extrinsic decomposition
  - residual reversion structure across vouchers
  - surface monotonicity / convexity as validation guard, not alpha
- Feature Evidence:
  - `L06`, `W2-01`, and `W2-04` revalidated delta-1 as the clean base family
  - `B02-resid` remains the best absolute tested artifact and is still
    `VEX + ITM` shaped
  - `VEV_5300` has positive `10k` markout while `5000/5100/5200` do not
  - several selective active bots peak early and then continue trading far too
    long afterwards
- Multivariate Evidence:
  - vouchers are option products linked to `VELVETFRUIT_EXTRACT`, not
    independent products
  - `HYDROGEL_PACK` remains the most independent branch
  - price-anchor redundancy still favors one compact option fair-value model
- Process / Distribution Assumptions:
  - Round 3 remains a distinct `TTE=5d` regime
  - `5300` is slower-horizon, not fast-scalp
  - toxic active strikes may only be useful as anti-signals or not at all
- Redundancy Decisions:
  - no broad active basket reopening
  - no broad surface family reopening
  - no HMM/Markov in Wave 3
  - Kalman only where it gives a compact online denoising proxy
- Regime Assumptions:
  - no-trade / no-new-entry logic now has stronger evidence than “better fair
    value model” as the next active-voucher axis
  - transformed thresholds and lightweight trend gating are worth testing
    before hidden-state models
- Understanding Insight:
  - use `VELVETFRUIT_EXTRACT` as both standalone delta-1 edge and voucher anchor
  - split the round into a strong delta-1 base, selective vouchers, and mostly
    closed toxic branches
- Research tool evidence used, if any:
  - timestamp-level path analysis
  - cross-run markout aggregation by product and horizon
  - `>5k` peak / giveback analysis
- Evidence gaps or strategy assumptions:
  - online no-trade logic must use observable proxies rather than full-run PnL
  - inverse bots assume that sign error is at least plausible on toxic strikes;
    they are included to close that question cleanly

## Batch Scope

- Batch size cap: `27`
- Recommended implemented set in this spec: `24`
- Intent: `targeted final exploration / architecture narrowing / branch closure`
- Promotion target:
  - likely `delta-1 first`
  - maybe `delta-1 + VEX + ITM`
  - maybe `delta-1 + one tiny gated 5300 overlay`

## Strategy Families Covered

| Family | Products | Why Included |
| --- | --- | --- |
| Delta-1 champion controls | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | current clean base family |
| Delta-1 regime / Kalman refinements | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | best chance to improve the champion without option overreach |
| VEX + ITM active refresh | `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500` | strongest historical family still deserves one cleaner modern test |
| Selective `5300` rescue | `VEV_5300` with or without `VEX` / delta-1 sidecars | only active strike with positive long-horizon markout |
| `5000 + 5300` capped salvage | `VEV_5000`, `VEV_5300` | last fair test for keeping `5000` alive |
| Inverse diagnostics | `VEV_5000`, `VEV_5100`, `VEV_5200` with and without `VEX` sidecars | close the toxic-strike sign question cheaply |
| Near-final architecture stacks | delta-1 base plus ITM and/or micro `5300` | bridge from exploration toward final-bot selection |

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run(state)` | wiki API docs | implement | all bots return `result, conversions, traderData` | compile and smoke-check |
| Round 3 product list | round doc | implement | use only official Round 3 symbols | symbols match spec and files |
| Position limits `200` / `300` | round doc | implement | all sizing and working limits respect round caps | order quantities remain within remaining capacity |
| Integer prices | exchange docs | implement | all quotes and cross prices round to `int` | no float order prices |
| Conversions | round doc | exclude | all Wave 3 bots use `conversions = 0` | constant zero |
| Manual Bio-Pod challenge | round doc | not applicable | excluded from all bot files | no Bio-Pod symbol usage |
| Live `TTE=5d` regime | round doc + live brief confirmation | implement | voucher logic may use session-time gates and expiry-style caution | no stale `TTE=6d-8d` assumptions hidden in code |
| `traderData` persistence | API docs | implement | compact state only: mids, EMA anchors, slope windows, Kalman state, position progress, cooldown flags | serializable and bounded |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01 Delta-1 reversion base | top-of-book mid, spread, position | usable online | direct signal | previous-mid or Kalman fair, spread gate, quote edge | independent from voucher branch | delta-1 mean reversion survives clean execution | keep as base family | idle on missing book | previous mids, optional Kalman state | compare against `L06`, `W2-01`, `W2-04` |
| F02 Simple regime gate | short-term move, slope, Kalman gap, spread | usable online | execution filter / no-trade gate | absolute caps on move/slope/gap | reduces exposure when microstructure gets unstable | some states are better skipped than traded through | use before hidden-state logic | disable new entries if state missing | short rolling histories and optional Kalman state | should improve retention or reduce damage without killing all activity |
| F03 ITM active refresh | VEX mid plus ITM voucher mids | usable online | direct signal / overlay | smaller active sizes, tighter working limits | tied to VEX as underlying anchor | passive ITM was too dead; lightly active ITM may monetize better | keep as add-on family, not base | idle on missing VEX or voucher book | residual anchors per ITM symbol | compare to `B02-*`, `W2-03`, `W2-04` |
| F04 Centered Bachelier residual on `5300` | VEX mid or Kalman anchor, voucher mid, strike | usable online | direct signal | residual anchor EMA, centered residual, edge threshold | vouchers are linked to VEX, not independent | `5300` still has slower-horizon residual edge | keep alive only on `5300` and tiny subsets | idle on missing VEX or voucher book | residual anchors per symbol | compare to `L15`, `W2-05`, `W2-09` |
| F05 No-trade / no-new-entry timing | timestamp, local progress, current position | usable online | risk control | early cutoff, hard flatten, cooldown | targets path reversal, not alpha | useful active states are concentrated early | keep as primary rescue axis | default to safer state if timing missing | entry timestamp, cooldown flag | should reduce post-peak trading and giveback |
| F06 Giveback stop | entry-centered residual, best local improvement | usable online | risk control | activation threshold, giveback width, cooldown | targets `edge then reversal` directly | local progress can be tracked well enough online | use before global PnL-style logic | disable if state missing | entry-centered state, best improvement | should cut late reversals without forcing zero activity |
| F07 VEX-linked calm-state gate | VEX move, slope, imbalance, Kalman gap, agitation EMA | usable online | execution filter | absolute caps and/or sidecar controls | explicitly models option-underlying linkage | active vouchers fail more in unstable VEX states | keep as main voucher gate family | block entries on missing VEX state | VEX rolling metrics | compare calm-gated `5300` against ungated `5300` |
| F08 Transformed threshold | VEX move, slope, spread excess, agitation EMA | usable online | nonlinear entry filter | dynamic threshold coefficients | still tied to VEX-linked option dynamics | residual entry quality depends on underlying agitation | use before HMM/Markov | fall back to base threshold if state missing | same VEX metrics as F07 | should improve selectivity more than it reduces useful fills |
| F09 Lightweight trend gate | rolling slope of VEX mid | usable online | execution filter | buy/sell directional slope constraints | tied to VEX state only, not a separate alpha family | avoid fading strong underlying trend states | test before hidden-state trend models | disable trend filter on missing history | short VEX history window | should help `5300` more than a raw early cutoff alone |
| F10 Inverse diagnostic | centered residual sign and fair-value direction | usable online | direct signal test | inverse direction mode, tiny limits, hard exits | only justified on strikes with persistent negative markouts | some toxic strikes may be anti-signals, not signals | diagnostic only, never promotion default | idle if state missing | same residual anchor as normal branch | if inverse stays bad, close the strike |
| F11 Kalman denoising | mid observations only | usable online | direct signal support / anchor refinement | process variance, observation variance | compact denoising proxy, not hidden-state modeling | noise reduction may matter in delta-1 fair or VEX anchor | keep only in 1-2 bots | fall back to raw mid if state resets | small Kalman mean/variance state | if no benefit, remove from next wave |
| F12 Capped subset salvage | `5000` / `5300` residuals plus time and VEX calm filters | usable online | direct signal + risk control | tiny working limits, early cutoff, calm-state caps | subset still linked through VEX anchor | if `5000` survives at all, it does so only in a tiny narrow state | one last fair salvage only | idle if setup missing | same residual and VEX state | if still poor, demote `5000` below serious next-wave scope |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| Broad active basket `5000+5100+5200+5300` | strongest repeated giveback evidence in the round | a future run contradicts both markouts and path analysis |
| Surface family as live alpha | current implementations look like adverse selection, not salvageable edge | a new surface definition survives targeted offline checks first |
| Upper branch in Wave 3 | currently low-damage but low-ROI relative to open active questions | delta-1 and voucher questions are closed and extra budget remains |
| HMM/Markov regime logic | too complex before simple observable gates are exhausted | simple gates, transformed thresholds, and trend filters all fail cleanly |
| Full inventory-coupled voucher controller | inventory is not the main bottleneck before state selection is fixed | calm-state `5300` survives but still dies mainly via inventory |

## Signal / Fair Value Logic

- Signal:
  - delta-1 bots use compact mean reversion around either previous mid or a
    Kalman mean
  - voucher bots use centered Bachelier residuals around a VEX-linked anchor
  - inverse bots explicitly flip the residual direction on toxic strikes
- Inputs:
  - best bid / ask, spread, top-level volumes, mid, position, timestamp
  - `VELVETFRUIT_EXTRACT` mid or Kalman-smoothed VEX anchor for vouchers
  - strike metadata from voucher symbol
- Missing-signal behavior:
  - idle by default; no backfilling from offline data
- Process assumption that would invalidate this logic:
  - if calm-state `5300` still has no retained edge, the active branch is much
    closer to dead than mis-held
- Multivariate or redundancy caveat:
  - VEX-linked gating is deliberate and should not be duplicated with many
    separate latent-state proxies in the same bot

## Execution Logic

- Buy behavior:
  - buy delta-1 when fair is above current mid enough to justify crossing or
    one-sided quoting
  - buy vouchers when residual logic and regime filters both allow it
  - buy inverse bots only when the anti-signal configuration says so
- Sell behavior:
  - symmetric to buy, plus flattening, stop-out, giveback-stop, and hard-flat
    logic
- Passive/resting order behavior:
  - delta-1 continues to rely on passive quotes plus bounded crossing
  - ITM refresh is lightly active, not purely passive
  - vouchers still quote more selectively than delta-1
- Stay-idle behavior:
  - idle on missing books, wide spreads, blocked regime states, cooldowns, or
    expired early windows

## Position And Risk Handling

- Position limits:
  - `200` for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - `300` per voucher
- Aggregate buy capacity:
  - bounded by remaining long room and much smaller internal working limits on
    experimental overlays and inverse bots
- Aggregate sell capacity:
  - bounded by current inventory plus short room
- Inventory skew or reduction:
  - used mainly as a stabilizer, not as the primary rescue mechanism
  - inverse and salvage bots stay deliberately tiny

## State And Runtime

- `traderData` use:
  - previous mids / EMA / short histories
  - residual anchors
  - Kalman mean / variance
  - entry timestamp, best local improvement, cooldown block
  - compact VEX agitation state
- Imports:
  - stdlib only
- Runtime risk:
  - more branch logic than Wave 2, but still O(1) or tiny-window per product
- Research-only dependencies excluded from uploadable bot: `yes`

## Bot Batch

### Core Wave 3 Bots (14)

- `W3-01` delta-1 dual control
- `W3-02` delta-1 with simple regime gate
- `W3-03` `VEX + ITM` active refresh
- `W3-04` `5300` early-window no-trade / late flatten
- `W3-05` `5300` giveback halt with cooldown
- `W3-06` VEX-linked `5300` calm-state gate
- `W3-07` `5300` slower-horizon hold
- `W3-08` delta-1 plus tiny gated `5300` overlay
- `W3-09` `5000 + 5300` capped peak salvage
- `W3-10` `5300` transformed-threshold gate
- `W3-11` `5300` lightweight trend gate
- `W3-12` `5000` inverse tiny diagnostic
- `W3-13` `5100` inverse tiny diagnostic
- `W3-14` `5200` inverse tiny diagnostic

### Extension Bots (10)

- `W3-15` delta-1 dual Kalman control
- `W3-16` `5300` Kalman-anchor rescue
- `W3-17` `5300` imbalance filter
- `W3-18` `5300` VEX-agitation gate
- `W3-19` `5000 + 5300` VEX-calm salvage
- `W3-20` `5000` inverse with VEX sidecar
- `W3-21` `5100` inverse with VEX sidecar
- `W3-22` `5200` inverse with VEX sidecar
- `W3-23` delta-1 plus ITM active combo
- `W3-24` delta-1 plus ITM plus tiny `5300` stack

## Variant Rules

- One main hypothesis per bot.
- Core bots decide architecture; extension bots close ambiguity or bridge toward
  final composition.
- Inverse bots are diagnostic by construction and must stay tiny.
- Kalman is allowed only as compact denoising, not as a broader adaptive
  controller.
- No Wave 3 bot may reopen the old broad active basket, the surface family, or
  HMM/Markov-style regime logic.

## Expected Failure Cases

- Failure case: delta-1 refinements do not beat the simple dual control
  - Mitigation or validation: keep `W3-01` as the comparison anchor
- Failure case: `5300` still fails even under calm-state and no-trade logic
  - Mitigation or validation: treat that as stronger closure evidence than a
    plain negative PnL alone
- Failure case: inverse bots trade but remain negative
  - Mitigation or validation: close the corresponding strike rather than
    recycling it into another exploratory wave
- Failure case: Kalman bots do not improve path quality or entry quality
  - Mitigation or validation: drop Kalman from future rounds and return to
    simpler anchor choices
- Failure case: stacked architecture bots are only VEX-driven
  - Mitigation or validation: use product attribution and markouts before
    promoting any stack toward final selection

## Validation Plan

- Contract checks:
  - verify `Trader.run()` contract, order signs, integer prices, and compact
    `traderData`
- Order sign and limit checks:
  - especially on tiny inverse bots and multi-leg stack bots
- Performance/run checks:
  - real platform PnL first
  - then path peak, end-from-peak, time-above-positive, and post-peak trade
    ratio
  - then product attribution and `10k` markout by product
- Debug signals to inspect:
  - whether `5300` stops trading after the early useful window
  - whether inverse bots are merely less bad or actually positive
  - whether Kalman changes entry quality rather than just lowering trade count
  - whether stacked bots are additive or simply VEX-dominated again

## Implementation Handoff

- Target bot path, normally `rounds/round_3/bots/<member>/canonical/...`: `rounds/round_3/bots/amin/canonical/candidate_w3_*.py`
- Parameters to implement:
  - `24` bots exactly as listed above
  - shared generator/template allowed
  - stdlib only in uploadable files
- Known caveats:
  - this is still an exploratory wave, not a final submission set
  - inverse and Kalman branches are included because they are now high-value
    closure questions, not because they are already trusted
