# Round 3 Closeout Retrospective

## Purpose

Close `round_3` as a retrospective evidence package, not as an active run queue.
This document separates:

1. work completed now from real `round_3` evidence,
2. validated lessons to carry into `round_4`,
3. untested `round_3` hypotheses we would have explored if the round stayed open,
4. default anti-patterns that should stay closed unless new evidence appears.

Primary numerical source:
[`round_3_full_performance_synthesis.md`](round_3_full_performance_synthesis.md)
with `101` analyzed JSON artifacts after absorbing the partial Wave 5 batch.

## Round 3 Retrospective Work Completed Now

### Wave 5 closeout ingestion

- Absorbed the `7` Wave 5 JSON artifacts that were still sitting in `../performances/amin/canonical/`.
- Normalized `candidate_w5_09_.json` to `candidate_w5_09_winner_plus_tiny_trio.json`.
- Extended the global synthesis from `94` to `101` runs.
- Added Wave 5 summary and decision-board artifacts:
  - `full_wave5_probe_summary.csv`
  - `full_wave5_decision_board.csv`

### Structural diagnostics completed

- `Moneyness-role audit`
  - `delta-1 base`: `HYDROGEL_PACK`, `VELVETFRUIT_EXTRACT`
  - `ITM structural`: `VEV_4000`, `VEV_4500`
  - `active zone`: `VEV_5000`, `VEV_5100`, `VEV_5200`, `VEV_5300`
  - `upper execution/passive`: `VEV_5400`, `VEV_5500`
  - `floor monitor`: `VEV_6000`, `VEV_6500`
- `Cross-strike context audit`
  - explicit `5100/5200/5300` comparison
  - toxic-pair aggregation for `5100 + 5200`
  - support / mixed / veto framing around `5300`
- `Portfolio-exposure audit`
  - final active exposure by family
  - active-limit pressure by family
  - relationship between family exposure and giveback

### Regime and retention diagnostics completed

- `Post-peak churn audit`
  - post-peak trade counts
  - post-peak trade ratios
  - early-peak / late-trading flags
- `Trade-horizon audit`
  - `1k`, `5k`, `10k` markouts by product and by run-product pair
- `Late-entry audit`
  - average peak timing
  - average post-peak trading intensity
  - early-peak giveback behavior by family
- `Counterfactual retention audit`
  - crude `2k` / `5k` giveback-stop exits
  - crude peak-retention floor exits

### Canonical cleanup completed

- Archived the `7` paired Wave 5 bots and performances into `historical/`.
- Archived the three legacy run-summary `.md` files that were still polluting `../performances/amin/canonical/`.
- Removed the unpaired Wave 5 bots from `canonical/` as `untested due to round close`.
- Left `round_3` canonical folders empty except maintenance files.

## Validated Lessons To Carry Into Round 4

These are framing rules, not speculative ideas.

### Product framing rules

- Treat `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` as `delta-1` products first.
- Treat `VEV_*` as an option book over `VELVETFRUIT_EXTRACT`, not as a bag of unrelated assets.
- Distinguish role before signal:
  - `delta-1 base`
  - `ITM structural`
  - `active option zone`
  - `upper passive/execution`
  - `floor/monitor`
- Do not assume one option architecture should span all strikes equally well.

### Signal framing rules

- For every candidate, explicitly classify the main signal as:
  - `valuation`
  - `microstructure`
  - `surface`
  - `regime`
- Always state whether `VEX` is acting as:
  - standalone alpha,
  - anchor/context,
  - or both.
- Always ask what the other strikes are saying before opening an option position.

### Execution and risk framing rules

- Every setup should declare whether the correct behavior is:
  - aggressive,
  - passive,
  - or `no-trade`.
- Every setup should declare its natural horizon:
  - fast scalp,
  - short hold,
  - medium hold.
- Every option branch should define the rule that prevents
  `edge -> giveback -> reversal`.
- `No-trade` is a legitimate design outcome, especially for toxic or late-session voucher states.

### Architecture lessons now validated

- The clean full-stack winner family in `round_3` is `delta-1 + ITM` on the stronger Kalman-style base.
- The best clean fallback benchmark is now pure `delta-1`.
- `VEV_5300` is the only active strike with meaningful long-horizon support, but it is not a default winner leg.
- `VEV_5000`, `VEV_5100`, and `VEV_5200` are far more useful as danger-state evidence than as normal inventory by default.
- The old `>10k` and `~18k` paths contained real upside, but packaged with bad strike mix, bad continuation logic, and poor retention.

## Untested Round 3 Hypotheses We Would Have Explored

These are not validated findings. They are carry-forward hypotheses.

### Features and signals worth testing later

- Option residual explicitly anchored to `VEX`.
- `Toxic-strike veto` using `5100/5200` as penalizers or hard veto inputs.
- `Family imbalance`, not only single-symbol imbalance.
- Observable `VEX` regime state:
  - slope
  - speed
  - agitation
  - abrupt state change proxies
- `Late-session deterioration` as an explicit gate.
- State from the bot's own recent outcomes to reduce aggressiveness after local failure.
- Local surface-structure signals:
  - `5200-5300`
  - `5100-5300`
  - `5300-5400`

### Bot variants we would have tested

- `5300` only if `5100/5200` do not veto.
- `No-new-entry-after` plus `hard-flat-after`.
- Reentry caps and cooldowns by symbol.
- Variants where `5000/5100/5200` are signal-only, not traded.
- Winner base plus tiny option overlay, not large composites.
- `5300` variants with longer horizon and without fast unwind.
- Exposure penalties at family level, not only symbol level.
- Position sizing that changes by regime instead of using one global threshold.

### Future analysis backlog that still matters

- Product-by-product audit from first principles.
- Strike-role map by effective TTE.
- Explicit comparison:
  - `vouchers as residual book`
  - versus `vouchers as independent assets`
- Simple family state machine:
  - normal
  - opportunity
  - danger
  - off
- Validation of whether `delta-1` is best treated as final base or as infrastructure/context for vouchers.
- Re-check whether `VEV_4000/4500` still hide underused edge.

## Default Anti-Patterns / Things To Stop Doing Unless New Evidence Appears

- Do not reopen the broad `5000/5100/5200/5300` basket as standard trading architecture.
- Do not treat option imbalance as the main alpha source.
- Do not jump to HMM or hidden-state complexity before exhausting simple observable gates.
- Do not dump more redundant price-anchor features into the same family and call it progress.
- Do not treat huge intra-run peaks as proof of a promotable architecture.
- Do not assume cleaner inventory management alone rescues a bad strike mix.
- Do not evaluate vouchers as though they were just slower delta-1 assets.
- Do not keep active voucher branches on by default late in the session.

## First-Principles Audit Summary

### What the products really are

- `HYDROGEL_PACK` and `VELVETFRUIT_EXTRACT` are directly tradable `delta-1` instruments.
- `VEV_*` are options whose pricing and tradability should be read relative to:
  - underlying state,
  - strike role,
  - horizon,
  - and cross-strike context.

### What was fundamentally missing at times

- Too much option logic was still being evaluated per symbol, instead of as a small option book.
- Too much active-voucher work was framed as “can this strike mean-revert profitably?” rather than
  “under what option-book state is aggression justified at all?”
- Too many rescue attempts were really execution overlays on top of a still-bad family definition.

### What Round 4 should inherit from this

- A clean base/context branch.
- A role-aware option-book framing.
- Stronger regime and shutdown discipline.
- Explicit distinction between:
  - evidence,
  - carry-forward principles,
  - and still-untested hypotheses.

## Hand-off To Round 4

- Use this closeout together with:
  - [`round_3_full_performance_synthesis.md`](round_3_full_performance_synthesis.md)
  - [`post_run_research_memory.md`](../post_run_research_memory.md)
- Treat the `round_3` lessons as transfer candidates, not as facts of `round_4`.
- Re-confirm all carry-forward assumptions against `round_4` data, especially once counterparties enter the picture.
