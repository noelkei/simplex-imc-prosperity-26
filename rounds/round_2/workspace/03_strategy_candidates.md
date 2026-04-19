# Strategy Candidates

Use [`docs/templates/strategy_candidates_template.md`](../../../docs/templates/strategy_candidates_template.md) as the structure for this file.

Maximum active candidates per round: 3.

## Status

IN_PROGRESS

## Sources

- Wiki facts: `../../../docs/prosperity_wiki/rounds/round_2.md`, `../../../docs/prosperity_wiki/api/01_trader_contract.md`, `../../../docs/prosperity_wiki/trading/02_orders_and_position_limits.md`
- Understanding summary: `02_understanding.md` (still sparse, caveat carried forward)
- EDA evidence: `01_eda/eda_report.md`
- Playbook heuristics: not used as facts

## Candidate Table

| Candidate ID | Product Scope | Source Of Edge | Evidence / Heuristic Basis | Key Assumptions | Main Risk | Evidence Strength | Implementation Cost | Validation Speed | Risk Level | Expected Upside | Priority | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `r2_amin_hybrid_01` | IPR + ACO | IPR drift + ACO fixed-FV MM | EDA supports strong IPR drift and ACO mean reversion around 10000 | ACO fixed FV is stable enough | fixed FV underreacts to visible-book distortions | medium | low | high | medium | medium | high | implemented |
| `r2_amin_feeaware_kalman_02` | IPR + ACO | IPR drift + ACO adaptive Kalman MM + fee-aware extra-access robustness | EDA Kalman grid for ACO favored `Q=0.1`, `R=8.0`; user reports Bruno Kalman line worked best so far | Round 2 extra quotes help but are not required; conservative positive bid can be worth it | bid may reduce net PnL if too high; adaptive FV may overfit noisy one-sided books | medium | medium | medium | medium | high | high | implemented |
| `r2_amin_feeaware_microprice_03` | IPR + ACO | IPR pressure-follow reposting + ACO Kalman microprice MM | Fast raw-data check shows ACO top-of-book imbalance and microprice displacement have strong next-tick predictive value | Faster response to one-sided books while keeping `_02` latent fair-value backbone; still fee-aware and extra-depth-friendly | stronger pressure-following could overreact in noisy books or widen inventory swings | medium | medium | medium | medium | high | high | implemented |
| `r2_amin_regime_depth_04` | IPR + ACO | IPR pressure-aware reposting + ACO Kalman regime-aware depth-price MM | Round 2 data check shows depth-weighted price shift is useful, but mainly in tight and wide spread regimes rather than uniformly | More directly aligned with Round 2 extra-quote economics, because extra visible depth should improve fair-value estimation if bid is accepted | regime gating may underuse depth signal in some paths; local harness advantage is modest | medium | medium | medium | medium | high | high | implemented |
| `r2_amin_conviction_sprint_05` | IPR + ACO | IPR carry + ACO conviction-based sprint trading | Aggressive brainstorm branch built to exploit strong short-horizon directional bursts rather than just quoting cleaner around fair value | Potential upside jump if platform randomness rewards visible pressure persistence and one-sided burst capture | materially higher overtrading and reversal risk; local harness does not clearly prefer it | medium | low | medium | medium | high | very high | implemented |

## Rejected Or Deferred Ideas

| Idea | Reason |
| --- | --- |
| Full HMM regime-switching ACO bot | Too complex for current round pressure, not clearly justified by existing evidence |
| Aggressive symmetric IPR long/short bot | Current evidence still heavily favors long-drift posture |
| EV-optimized nontrivial Market Access Fee model | Testing ignores `bid()`, so official evidence is missing |

## Shortlist

- `r2_amin_hybrid_01`
- `r2_amin_feeaware_kalman_02`
- Rationale: keep one simple robust baseline and one adaptive Kalman variant closer to the strongest line the team has seen so far.

## Human Decisions Needed

- Decide whether to validate both candidates or promote the Kalman variant directly for final iteration.
- Decide whether `MARKET_ACCESS_BID = 12` is acceptably conservative or should be changed after scenario analysis.

## Next Action

- Run validation / replay comparison between the two active Amin candidates on Round 2 sample data, then update testing artifacts and pick the stronger PR target.
