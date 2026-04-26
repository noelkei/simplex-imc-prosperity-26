# Round 3 Final Exploitation And Upside-Distillation Planning

## Status

READY_FOR_REVIEW

## Objective

Turn the full **94-run Round 3 evidence base** into one last
high-ROI **winner-focused** wave before final submission selection.

This planning pass has two jobs at once:

1. protect and compare the current clean winners,
2. distill the old `>10k` / `~18k` upside into much safer descendants instead
   of reopening the old self-destructive basket.

## Source Inputs

- [`03_strategy_candidates.md`](03_strategy_candidates.md)
- [`03_signal_strategy_learning_matrix.md`](03_signal_strategy_learning_matrix.md)
- [`06_testing/round_3_full_performance_synthesis.md`](06_testing/round_3_full_performance_synthesis.md)
- [`06_testing/artifacts/full_synthesis/full_run_metrics.csv`](06_testing/artifacts/full_synthesis/full_run_metrics.csv)
- [`06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv`](06_testing/artifacts/full_synthesis/full_wave4_probe_summary.csv)
- [`06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv`](06_testing/artifacts/full_synthesis/full_wave4_decision_board.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt10k_runs.csv)
- [`06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv`](06_testing/artifacts/full_synthesis/full_high_peak_gt10k_product_giveback.csv)
- [`06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv`](06_testing/artifacts/full_synthesis/full_no_trade_candidates.csv)
- [`06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv`](06_testing/artifacts/full_synthesis/full_trade_markout_by_product.csv)
- [`06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv`](06_testing/artifacts/full_synthesis/full_trade_markout_by_run_product.csv)
- [`post_run_research_memory.md`](post_run_research_memory.md)
- processed papers under `../research/papers_processed/`

## Executive Planning Verdict

- The clean winner has improved again: **`W4-03 = 1606.305`** is now the best
  overall real PnL in Round 3.
- `W4-04 = 1604.305` confirms the same family almost exactly, so the true
  winner axis is now **`delta-1 + ITM` on the Kalman base**, not pure
  `delta-1` alone.
- `W4-01 = W4-02 = W3-15 = 1527.305` means the light retention tweak on the
  pure champion did not change anything material.
- `W4-06`, `W4-07`, and `W4-09` prove that tiny `5300` overlays can coexist
  with the winner base, but they are still **subtractive** versus `W4-03`.
- `W4-05`, `W4-08`, and `W4-12` show that the remaining standalone `5300`
  finalists are not good enough as direct endgame bets.
- The only route left to a ceiling far above `~1.6k` is **not** more `5300`
  refinement. It is a final **upside-distillation** pass built from the old
  `>10k` runs using all the later lessons:
  - prune strikes hard,
  - anchor on `VELVETFRUIT_EXTRACT`,
  - use strict no-reentry / cutoff / giveback logic,
  - and treat `VEV_5100/5200` more as danger signals than as normal legs.

## What Wave 4 Resolved

### Resolved Positively

- `delta-1 + active ITM` is now the best clean family.
- Kalman on the base is stable, not a one-off.
- A conservative fallback still exists in pure `delta-1`.

### Resolved Negatively

- Standalone `5300` is not submission-grade.
- Trend-only `5300` rescue is not convincing enough.
- Direct forced inverse closure on `5100` still did not trade cleanly.

### Still Open

- whether the final submission should simply be `W4-03/W4-04` class,
- whether one last upside-distillation branch can get materially above the
  clean `~1.6k` ceiling while staying positive,
- whether toxic strikes should survive only as filters / vetoes instead of as
  direct inventory legs.

## What The `>10k` Runs Really Imply

The five `>10k` runs are:

- `B08-regime`
- `C06-legacy`
- `B04-surf`
- `B03-pure`
- `B06-tte`

What they teach now:

- the upside was real,
- the retention was terrible,
- the main damage came from `VEV_5100`, `VEV_5000`, and `VEV_5200`,
- `VEV_5300` was still harmful, but materially less toxic,
- and `VELVETFRUIT_EXTRACT` looked more like an anchor / stabilizer than a
  destroyer.

So the final salvage logic should be:

1. no broad basket,
2. no normal `5200` trading,
3. no assumption that every active strike deserves equal weight,
4. no unlimited continuation after the profitable window,
5. and no pure voucher-led final bet without a clean control alongside it.

## Design Rules For The Next Wave

Every new bot in the next wave should satisfy at least one of these:

1. protect or refine the current best clean winner (`W4-03` / `W4-04`),
2. test whether the old `>10k` logic survives when converted into a
   **VEX-anchored, strike-pruned, retention-disciplined** form,
3. use toxic strikes as **filters / vetoes / transformed-threshold inputs**
   rather than as default long-lived inventory,
4. or provide a necessary control so we know whether a new upside branch
   actually beats the clean winner.

And every active-salvage bot should include several of these controls:

- hard session cutoff or hard no-new-entry window,
- portfolio peak ratchet / giveback stop,
- cooldown after large giveback,
- low per-strike caps,
- limited reentries,
- `VEX` regime or slope gate,
- transformed thresholds using cross-strike disagreement,
- and optional Kalman smoothing only when it remains online-usable and
  interpretable.

## What We Will Not Spend Slots On

- broad `5000/5100/5200/5300` basket reruns,
- normal direct `5200` active trading,
- generic standalone `5300` reruns,
- upper or floor branches,
- HMM / hidden-state complexity,
- or another forced direct inverse slot unless the user explicitly wants it.

Direct inverse trading was considered and is not ignored; the current read is
that **anti-signal / veto use of toxic strikes is higher ROI** than trying to
force a clean tradable inverse branch one more time.

## Recommended Wave Size

**12 bots**

Why `12`:

- `4` slots for clean finalist protection and refinement,
- `6` slots for genuine upside-distillation descendants of the `>10k` runs,
- `2` slots for filter-driven or Kalman-driven salvage variants that reuse
  toxic strikes as information rather than as default inventory.

This is big enough to attack the ceiling and still small enough to stay
interpretable.

## Proposed Wave 5 Bot Set

| Bot ID | Bucket | Ancestor / Rationale | Core Idea | Why It Deserves A Slot |
| --- | --- | --- | --- | --- |
| `W5-01` | finalist control | `W4-03` | freeze the best clean winner exactly | Every salvage attempt needs a live benchmark against the actual best-known architecture. |
| `W5-02` | finalist retention | `W4-03` | `W4-03` plus portfolio peak-ratchet / giveback lock | `W4-03` still gives back ~`800`; this is the highest-ROI “safe improvement” slot. |
| `W5-03` | finalist retention | `W4-03` | `W4-03` plus late-window no-new-entry / cooldown | Tests whether the clean winner can retain more by trading less after the profitable core regime. |
| `W5-04` | finalist benchmark | `W4-01` or `W4-11` style | pure champion benchmark / conservative fallback | Needed so every upside-distillation bot is judged against both the best stack and the best clean fallback. |
| `W5-05` | upside-distillation | `B08-regime` / `C06-legacy` | `VEX + {5000,5100,5300}` with `5200` excluded, hard cutoff, hard no-reentry, portfolio ratchet | Closest controlled descendant of the highest `>10k` family without reopening the full toxic basket. |
| `W5-06` | upside-distillation | `B06-tte` | `VEX + {5100,5300}` with aggression decay after mid-session | Keeps the strongest peak-producing strike and the least-toxic strike, but with explicit expiry-style caution. |
| `W5-07` | upside-distillation | `B03-pure` | pure active `{5000,5100,5300}` one-shot salvage with strict trade cap and hard flatten | One slot should still ask whether the active cluster can carry upside on its own once continuation is brutally constrained. |
| `W5-08` | upside-distillation | `B04-surf` | `VEX`-anchored cross-strike ordered salvage on `5100/5300` only | Reuses the old full-surface intuition, but only as a pruned relative-value gate instead of a broad directionally loaded surface bot. |
| `W5-09` | upside-distillation | `W4-03` + legacy peaks | `W4-03` plus tiny active salvage trio overlay `{5000,5100,5300}` | Safest route to ask whether old upside can ride on top of the best clean winner. |
| `W5-10` | upside-distillation | `W4-03` + legacy peaks | `W4-03` plus tiny active salvage duo `{5100,5300}` | Isolates whether removing `5000` improves the salvage overlay while keeping the strongest peak driver (`5100`). |
| `W5-11` | transformed-threshold salvage | toxic-strike anti-signal | trade only `5300`, but require `5100/5200` disagreement / veto logic | Uses toxic strikes as information, not inventory, and directly tests the user idea of nonlinear thresholds with product linkage. |
| `W5-12` | Kalman / regime salvage | `B08/C06` distilled | `VEX`-anchored active salvage cluster with Kalman-smoothed composite residual and simple trend gate | Best place to reuse Kalman outside the base winner family, because Wave 4 proved smoothing can help when the signal is otherwise noisy. |

## Why These 12 And Not A Different 12

### Finalist Protection

- `W5-01` to `W5-04` make sure we do not lose the current best architecture
  while chasing upside.

### High-Upward-Ceiling Extraction

- `W5-05` to `W5-10` are all descendants of actual `>10k` ancestors, not
  invented side ideas.
- They differ on exactly the right axes:
  - whether `5000` stays or goes,
  - whether `5100` is used directly or only through structure,
  - whether the active cluster needs `VEX`,
  - and whether the upside belongs as a standalone branch or as a tiny overlay
    on the current clean winner.

### Information-First Toxic-Strike Use

- `W5-11` and `W5-12` are the best remaining place to honor:
  - the user idea about transformed / nonlinear thresholds,
  - the linkage between vouchers and the underlying,
  - and the evidence that toxic strikes may still say something useful even
    when they are poor default tradable legs.

## Promotion Rules After Wave 5

After Wave 5, the decision should be:

1. **final winner now** if no upside-distillation bot materially beats
   `W5-01/W5-02/W5-03`,
2. **mini final runoff** if one or two salvage bots close well above the clean
   finalists,
3. **close active upside exploration** if the salvage set still cannot turn the
   historical `>10k` peak logic into a positive, retainable architecture.

And for a salvage bot to be treated as a true finalist, it should ideally:

- finish clearly positive,
- avoid catastrophic giveback,
- show interpretable product attribution,
- and not depend on the full toxic basket returning.

## Concrete Recommendation

Proceed with **all 12 bots** above.

This is the right final exploratory / exploitation blend because:

- it protects the best clean winner,
- it directly attacks the upside ceiling problem the user pointed out,
- it reuses the real `>10k` evidence instead of ignoring it,
- and it still avoids the biggest known traps: broad basket relapse, blind
  `5200`, and uncontrolled continuation.

## Next Priority Action

Write the **Wave 5 spec** from this planning artifact and implement the 12 bots.
