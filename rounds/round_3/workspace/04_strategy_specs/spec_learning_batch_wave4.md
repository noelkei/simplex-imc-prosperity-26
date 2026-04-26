# Strategy Spec: Round 3 Finalist Batch Wave 4

## Status

`deferred under deadline`

## Review Status

- Status: `COMPLETED`
- Owner: `amin`
- Reviewer: `Unassigned`
- Reviewed on: `2026-04-26 (deadline deferral)`
- Deadline deferral reason: the user explicitly requested writing the Wave 4
  spec and implementing the full 12-bot finalist batch now, using the
  post-Wave-3 evidence to move from exploration into winner selection

## Candidate

- Candidate ID: `Wave4-finalist-batch`
- Candidate priority tier: `spec-first`
- Evidence strength: `strong`
- Product scope: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`,
  `VEV_4500`, `VEV_5100`, `VEV_5300`
- Linked candidate file:
  [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`
- Reviewer decision notes: the user explicitly wants the winner-focused Wave 4
  spec plus implementation immediately, and the current 82-run evidence already
  narrows the design space enough to support a disciplined final/pre-final cut
- Required changes before coding: none

## Objective

Implement a **winner-focused Round 3 finalist wave** that no longer spends
slots on broad exploration.

This batch should do five jobs:

1. freeze and refine the current **clean champion path** around `W3-15`,
2. test the best remaining **additive overlay thesis** by porting active ITM
   onto that champion base,
3. decide whether `VEV_5300` deserves one **real micro-overlay slot** in final
   architecture,
4. distill the old `>10k` / `~18k` upside into **sustainable peak-salvage**
   designs without reopening the toxic basket,
5. close one still-open strike-sign ambiguity with a **forced-tradability
   inverse diagnostic**.

Total batch size: **12**

## Sources

- Wiki facts:
  [`../../../docs/prosperity_wiki/rounds/round_3.md`](../../../docs/prosperity_wiki/rounds/round_3.md)
  plus the shared API and trading docs
- EDA evidence:
  [`../01_eda/eda_option_surface_and_microstructure.md`](../01_eda/eda_option_surface_and_microstructure.md)
- Understanding summary:
  [`../02_understanding.md`](../02_understanding.md)
- Post-run research memory:
  [`../post_run_research_memory.md`](../post_run_research_memory.md)
- Full synthesis:
  [`../06_testing/round_3_full_performance_synthesis.md`](../06_testing/round_3_full_performance_synthesis.md)
- Key full-synthesis artifacts:
  - [`../06_testing/artifacts/full_synthesis/full_wave3_decision_board.csv`](../06_testing/artifacts/full_synthesis/full_wave3_decision_board.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
  - [`../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv`](../06_testing/artifacts/full_synthesis/full_high_peak_gt5k_product_giveback.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
  - [`../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](../06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- Strategy planning:
  [`../03_next_wave_bot_planning.md`](../03_next_wave_bot_planning.md)
- External paper research:
  - [`../../research/papers_processed/choi_2022_bachelier_guide_processed.md`](../../research/papers_processed/choi_2022_bachelier_guide_processed.md)
  - [`../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md`](../../research/papers_processed/stoikov_saglam_2009_option_mm_inventory_processed.md)
  - [`../../research/papers_processed/muravyev_2015_option_order_flow_processed.md`](../../research/papers_processed/muravyev_2015_option_order_flow_processed.md)
  - [`../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md`](../../research/papers_processed/garcia_ares_2023_expiration_days_processed.md)

## Selection Trace

- Based on candidate: `03_next_wave_bot_planning.md`
- Signals used:
  - `W3-15` is the best clean architecture in the whole round at `1527.305`
  - `W3-23` proves the **active ITM overlay thesis**, even though it still sat
    on the older delta-1 base
  - `W3-17` is the best standalone `5300` winner and `W3-11` remains the best
    trend-led comparator
  - `VEV_5300` is the only active strike with positive aggregate `10k` markout
  - `VEV_5000`, `VEV_5100`, and `VEV_5200` remain negative in ordinary
    direction and are closed-by-default for final-bot purposes
  - the old `>10k` / `~18k` runs are still the strongest evidence that a lot of
    Round 3 upside was **real but badly retained**
- Alternatives considered:
  - rerun `W3-23` exactly without lifting its overlay onto the stronger Kalman
    base
  - reopen the broad `5000-5300` basket because of giant historical peaks
  - skip all remaining `5300` work and move directly to pure delta-1 finalists
  - skip the forced inverse closure slot and just assume toxic strikes are dead
- Why selected:
  - the most valuable untested near-final idea is **champion base plus active
    ITM overlay**
  - `5300` deserves one last tightly bounded decision pass because it is still
    the only non-ITM active strike with positive `10k` markout
  - the old high peaks should influence the next wave only through
    shutdown/retention logic and smaller overlays
  - a single forced inverse diagnostic is enough to close the toxic-strike sign
    question without spending a whole subfamily on it
- Known caveats:
  - the champion-plus-ITM stack is a high-ROI extrapolation from `W3-15` and
    `W3-23`, not a previously run exact file
  - `5300` may still stay positive only standalone and subtractive in stacks
  - simple retention rules derived from path analysis are still proxies, not
    guarantees against future giveback

## Evidence Traceability

- Linked EDA Signals:
  - delta-1 reversion in `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - Bachelier-style intrinsic / extrinsic structure for vouchers
  - residual reversion is stronger as a **linked underlying-option** thesis
    than as an isolated voucher-only thesis
- Feature Evidence:
  - `W3-15` materially improved the clean base over `W3-01`
  - `W3-23` added `+79` of ITM contribution on top of the old base
  - `W3-24` showed that the extra tiny `5300` layer was still subtractive in
    the best late-stage stack tested so far
  - `W3-17` and `W3-11` are the strongest remaining `5300` rescue evidence
  - `W3-04`, `W3-10`, and related runs show that `5300` rescue still needs
    stricter time-window and giveback discipline
- Multivariate Evidence:
  - vouchers are linked to `VELVETFRUIT_EXTRACT` by option structure and should
    be filtered against the underlying state
  - `HYDROGEL_PACK` remains the most independent clean branch and acts as a
    stabilizing delta-1 leg in the champion family
- Process / Distribution Assumptions:
  - Round 3 remains a `TTE=5d` regime
  - `5300` edge, when present, is slower-horizon and highly state-dependent
  - the giant historical peaks came from the wrong basket and continuation
    logic, not from a ready-made final architecture
- Redundancy Decisions:
  - do not rerun exact old-basket logic
  - do not spend slots on surface, upper, or broad toxic-strike families
  - use one forced inverse closure bot rather than an inverse family
  - port the ITM overlay thesis directly onto the champion base instead of
    spending a slot on an exact old-base repeat
- Regime Assumptions:
  - no-trade / no-new-entry / giveback control are more valuable than adding
    hidden-state complexity
  - selective `5300` should be judged under strict timing and underlying-state
    control
- Understanding Insight:
  - `VELVETFRUIT_EXTRACT` is both a standalone edge and the correct online
    anchor for voucher logic
  - active vouchers should now be overlays, not base architecture
- Research tool evidence used, if any:
  - `82`-run synthesis
  - `>10k` peak counterfactual analysis
  - trade markouts by product and by run-product
- Evidence gaps or strategy assumptions:
  - there is still no clean platform answer on whether `5100` works as a tiny
    inverse branch because prior inverse tests did not cleanly trade the target
    leg

## Batch Scope

- Batch size cap: `12`
- Recommended implemented set in this spec: `12`
- Intent: `winner-focused exploitation / final architecture narrowing / closure`
- Promotion target:
  - likely pure `delta-1` champion,
  - or `delta-1 + active ITM`,
  - with `5300` surviving only if a tiny overlay proves truly additive

## Strategy Families Covered

| Family | Products | Why Included |
| --- | --- | --- |
| Champion base finalists | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT` | choose the final clean base architecture |
| Champion plus ITM | `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`, `VEV_4000`, `VEV_4500` | highest-ROI additive thesis not yet tested on the champion base |
| Selective `5300` | `VEV_5300` with or without champion sidecars | decide whether `5300` survives as a micro-overlay candidate |
| Distilled peak-salvage | `VEV_5300` with or without champion sidecars | capture some old upside only through pruned, sustainable logic |
| Forced inverse closure | `VEV_5100` | close the highest-value remaining toxic-strike ambiguity |

## Round-Specific Mechanics Contract

| Mechanic / Trader Function / Field | Source | Decision | Bot Behavior | Validation Check |
| --- | --- | --- | --- | --- |
| `Trader.run(state)` | wiki API docs | implement | all bots return `result, conversions, traderData` | compile and smoke-check |
| Round 3 product list | round doc | implement | use only official Round 3 symbols | symbols match spec and files |
| Position limits `200` / `300` | round doc | implement | all sizing and working limits remain below the official caps | aggregate order capacity remains valid |
| Integer prices | exchange docs | implement | all quotes and active prices are rounded to `int` | no float order prices |
| Conversions | round doc | exclude | all Wave 4 bots return `conversions = 0` | constant zero |
| Manual Bio-Pod challenge | round doc | not applicable | excluded from all bot files | no Bio-Pod usage |
| Live `TTE=5d` regime | round doc + live challenge brief | implement | voucher logic keeps time-window control and expiry-style caution calibrated for the Round 3 live regime | no stale `TTE=6d-8d` constants hidden in code |
| `traderData` persistence | API docs | implement | compact state only: mids, anchors, short histories, Kalman state, local progress, cooldown flags | serializable and bounded |

## Feature Contract

| Feature | Source Fields | Online Availability | Role | Parameters | Multivariate Relationship | Process Assumption | Redundancy Decision | Missing-Signal Behavior | State / `traderData` Required | Validation / Invalidation Check |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F01 Champion delta-1 Kalman base | top-of-book mid, spread, position, small rolling history | usable online | direct signal | Kalman fair, quote edge, trade threshold, inventory skew | independent from voucher alpha but stabilizes hybrid stacks | clean delta-1 mean reversion still dominates Round 3 | keep as base family | idle on missing book | previous mids, EMA, Kalman state | compare directly to `W3-15`, `W3-01`, `W3-02` |
| F02 Light delta-1 retention gate | short move, slope, Kalman gap, spread | usable online | execution filter / risk control | loose absolute caps, slightly higher trade threshold, optional smaller sizes | modifies base only through state selection | champion path can lose less late without sacrificing most activity | one light gate and one stress variant only | default to safer idle if state is missing | same delta state as F01 | must not collapse trade count to near zero |
| F03 Active ITM overlay on champion base | VEX mid, ITM voucher mids, residual anchor | usable online | additive overlay | smaller working limits, active crossing pad, VEX-linked calm caps | explicitly linked to `VELVETFRUIT_EXTRACT` as underlying | ITM edge is real only as a small overlay on a strong base | keep active ITM, not passive ITM | idle on missing VEX or voucher book | residual anchors per symbol | compare to `W3-23` thesis and pure champion base |
| F04 Strict ITM activation | same as F03 plus stronger underlying-state caps | usable online | overlay cleaner / noise reduction | higher entry thresholds, tighter working limits, earlier no-new-entry cutoff | same option-underlying linkage as F03 | some ITM fills are additive only in calmer states | test as one stricter sibling, not a new family | fall back to no ITM trade | same as F03 | should preserve some ITM contribution while reducing slippage/noise |
| F05 Selective `5300` centered residual | VEX mid or Kalman anchor, `VEV_5300` mid, strike | usable online | direct signal | centered residual, signal weight, inventory skew | `5300` is treated as an overlay linked to `VEX`, not an independent asset | `5300` has slower-horizon retained edge in selected states | keep only on `5300` | idle on missing books | anchor EMA, entry-centered state | compare to `W3-17`, `W3-11`, and `W3-08` |
| F06 `5300` filter axis: imbalance vs trend | book imbalance, rolling VEX slope | usable online | execution filter | imbalance minima / maxima and/or VEX slope caps | both are option-underlying state filters, not new alpha | one of these filters is likely the cleanest final `5300` gate | compare, do not stack many filters blindly | disable affected side on missing state | VEX slope history and per-symbol imbalance | decide whether imbalance-led or trend-led `5300` survives |
| F07 Time-window / no-new-entry / giveback control | timestamp, centered residual progress, cooldown state | usable online | risk control | early window, hard flat, giveback activation / stop, cooldown | targets retention, not fair-value estimation | the useful `5300` regime is earlier and shorter than current total trading time | high-priority rescue axis | default to safer idle / flatten | entry timestamp, best improvement, block-until | should reduce post-peak trading and improve retained PnL |
| F08 Micro-overlay sizing | current position, remaining capacity, product scope | usable online | risk control / integration control | tiny working limits and small passive/aggressive sizes | protects the champion base from overlay contamination | small overlays can be additive where larger ones are subtractive | use for all `5300` overlays and inverse bot | if sizing state missing, use smaller default | no extra state beyond positions | overlay should not dominate symbol count or PnL attribution |
| F09 Distilled peak-salvage logic | `5300` residual, VEX calm metrics, timestamp, giveback state | usable online | direct signal + risk control | earlier cutoff, short max hold, sharper giveback, stricter calm-state caps | distilled from broad-basket legacy paths into a one-strike overlay | historical upside can survive only in pruned, sustainable form | do not reopen `5000/5100/5200` here | idle if calm-state filters fail | same as F05/F07 | compare to old giant-peak lessons without basket reintroduction |
| F10 Forced inverse closure | `VEV_5100` centered residual sign, wider tradability threshold | usable online | direct signal test | inverse direction mode, deliberately lower threshold, tiny working limit, early shutdown | still VEX-linked, but used only for sign closure | if `5100` truly acts as an anti-signal, it should trade even in tiny size under forced tradability | one bot only | idle on missing VEX or voucher book | same residual anchor state as normal voucher legs | if it still does not trade or loses, close `5100` for final-bot purposes |

## Feature Exclusions

| Feature | Why Excluded | Reopen Only If |
| --- | --- | --- |
| Broad `VEV_5000-5300` basket | repeatedly creates and destroys giant peaks with terrible retention | a future run contradicts both the markouts and the path study |
| `VEV_5000` or `VEV_5200` as normal active legs | negative at every meaningful horizon in the current evidence | a clean future diagnostic overturns the sign story |
| Exact old-base rerun of `W3-23` | lower ROI than porting the ITM thesis onto the champion base | champion-base + ITM fails in a way that points back to the old base |
| Surface / upper / floor branches | no longer on the critical path for final selection | final architecture is still unresolved and new direct evidence appears |
| HMM / Markov / hidden-state logic | lower ROI than simple gates and more overfit risk at this stage | simple gates fail and a new round still leaves time for deeper regime work |

## Signal / Fair Value Logic

- Signal:
  - champion bots use Kalman-smoothed delta-1 reversion on
    `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - ITM overlay bots use VEX-linked Bachelier residuals on `VEV_4000` and
    `VEV_4500`
  - `5300` bots use centered Bachelier residuals with smarter state filters and
    tighter retention logic
  - the inverse closure bot explicitly flips the residual direction on
    `VEV_5100`
- Inputs:
  - best bid / ask, top-level volumes, spread, position, timestamp
  - `VELVETFRUIT_EXTRACT` mid or Kalman-smoothed anchor for voucher logic
  - strike metadata from voucher symbols
- Missing-signal behavior:
  - idle by default; never backfill from offline artifacts
- Process assumption that would invalidate this logic:
  - if champion-base overlays never add beyond the pure champion, Round 3 is
    probably best solved as mostly clean delta-1
- Multivariate or redundancy caveat:
  - ITM and `5300` overlays already consume the option-underlying linkage;
    do not add extra latent-state proxies on top

## Execution Logic

- Buy behavior:
  - delta-1 base crosses or quotes when its fair exceeds current mid by enough
  - ITM and `5300` overlays only buy when residual direction, time window, and
    underlying state all agree
  - the inverse bot only buys when the forced anti-signal setup fires
- Sell behavior:
  - symmetric to buy, plus hard flatten, time stop, giveback stop, and stop-out
    logic
- Passive/resting order behavior:
  - champion delta-1 keeps passive quoting plus bounded crossing
  - ITM is lightly active, not passive dead weight
  - `5300` overlays quote selectively and stay tiny
- Stay-idle behavior:
  - idle on missing books, wide spreads, blocked regime states, expired early
    windows, or cooldown

## Position And Risk Handling

- Position limits:
  - `200` for `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT`
  - `300` per voucher
- Aggregate buy capacity:
  - bounded by official limits and smaller internal working limits
- Aggregate sell capacity:
  - bounded by short room plus current inventory
- Inventory skew or reduction:
  - champion family uses modest skew
  - all voucher overlays and inverse diagnostics remain much smaller than the
    base family

## State And Runtime

- `traderData` use:
  - previous mids, short histories, EMA and Kalman state
  - per-voucher residual anchors
  - entry timestamp, best local improvement, and cooldown blocks
- Imports:
  - stdlib only
- Runtime risk:
  - still O(1) or tiny-window per product; no research-only libraries in
    uploadable files
- Research-only dependencies excluded from uploadable bot: `yes`

## Bot Batch

### Finalist Architecture Bots

- `W4-01` clean `W3-15` champion control
- `W4-02` `W3-15` with a light retention gate
- `W4-03` champion base plus active ITM overlay
- `W4-04` champion base plus stricter active ITM overlay

### `5300` Decision Bots

- `W4-05` refined standalone selective `5300`
- `W4-06` champion base plus tiny selective `5300`
- `W4-07` champion base plus ITM plus tiny selective `5300`

### Distilled Peak-Salvage Bots

- `W4-08` standalone `5300` peak-salvage
- `W4-09` champion base plus tiny `5300` peak-salvage overlay

### Closure / Insurance Bots

- `W4-10` forced-tradability `VEV_5100` inverse closure
- `W4-11` champion stress-control variant
- `W4-12` trend-led `5300` final comparator

## Variant Rules

- One main decision per bot.
- Champion-base improvements must stay close enough to the current clean
  champion to remain interpretable.
- ITM overlays must remain small and clearly attributable.
- `5300` overlays must stay tiny enough that the base still dominates the
  architecture.
- Peak-salvage bots must never reopen a multi-strike active basket.
- The inverse closure bot is diagnostic and must not become a default promotion
  target without very strong evidence.

## Expected Failure Cases

- Failure case: champion-base overlays still underperform the pure champion
  - Mitigation or validation: choose the pure champion and demote overlays to
    optional challengers only
- Failure case: `5300` stays positive standalone but subtractive in every stack
  - Mitigation or validation: keep `5300` out of final architecture even if the
    standalone branch is mildly profitable
- Failure case: distilled peak-salvage still gives back too much
  - Mitigation or validation: treat the old `>10k` paths as analytical lessons,
    not as live-architecture candidates
- Failure case: forced inverse closure still does not trade or stays negative
  - Mitigation or validation: close `5100` decisively for final-bot purposes

## Validation Plan

- Contract checks:
  - verify `Trader.run()` contract, integer prices, and compact `traderData`
- Order sign and limit checks:
  - especially on small overlays, stacks, and the inverse closure bot
- Performance/run checks:
  - real platform PnL first
  - then base-versus-overlay attribution
  - then path peak, end-from-peak, post-peak trade ratio, and retained profit
  - then per-product `10k` markout and overlay contamination
- Debug signals to inspect:
  - whether the ITM overlay is additive on top of the Kalman champion
  - whether `5300` improves any finalist stack or only survives standalone
  - whether peak-salvage bots actually shut down earlier and cleaner
  - whether the inverse closure bot trades the intended voucher leg

## Implementation Handoff

- Target bot path, normally `rounds/round_X/bots/<member>/canonical/...`:
  `rounds/round_3/bots/amin/canonical/candidate_w4_*.py`
- Parameters to implement:
  - `12` bots exactly as listed above
  - shared generator/template allowed
  - stdlib only in uploadable files
- Known caveats:
  - this wave is winner-focused, but still not the final single submission
  - the champion-plus-ITM and champion-plus-`5300` stacks are deliberate
    near-final hybrids, not exact reruns of previously uploaded files
