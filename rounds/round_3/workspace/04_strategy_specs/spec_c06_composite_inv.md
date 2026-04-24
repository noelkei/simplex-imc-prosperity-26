# Strategy Spec: C06-inv — Full-Scope Composite Trader (Inventory Variant)

This spec inherits all logic from `spec_c06_composite_base.md` and adds inventory-skew features from C04.

## Review Status

- Status: `deferred under deadline`
- Owner: amin
- Reviewer: Unassigned
- Reviewed on: 2026-04-24 (deadline deferral)
- Deadline deferral reason: variant of base spec; single changed axis (inventory skew)

## Candidate

- Candidate ID: `C06-inv` (variant of C06, incorporating C04)
- Candidate priority tier: `validate-next`
- Evidence strength: `medium/high`
- Product scope: same as C06 base
- Linked candidate file: [`03_strategy_candidates.md`](../03_strategy_candidates.md)
- Parent spec: [`spec_c06_composite_base.md`](spec_c06_composite_base.md)

## Review Decision

- `_index.md` spec status: `deferred under deadline`
- Approved for implementation: `deferred under deadline`

## Changed Axis vs Base

The ONLY differences from `spec_c06_composite_base.md` are:

1. **Per-symbol inventory skew on vouchers**: quote mid is shifted by `penalty = skew_factor * position / limit` per voucher symbol, making the bot more eager to flatten concentrated positions.
2. **Imbalance confirmation filter on vouchers**: residual entry is confirmed when imbalance agrees with the trade direction; softened when it disagrees.
3. **TTE-adaptive thresholds**: entry thresholds widen slightly and exit is faster, incorporating C07 caution.

## Additional Feature Contract entries (all others inherited from base spec)

### F7: Per-Symbol Inventory Skew (vouchers)

| Field | Value |
| --- | --- |
| Feature | linear inventory-aware quote shift |
| Source Fields | `state.position[symbol]`, position limit (300) |
| Online Availability | usable online |
| Role | risk control |
| Parameters | `penalty = inventory_skew_factor * position / limit`; shifts fair value down when long, up when short |
| Multivariate Relationship | per-symbol position is correlated across voucher family via VEX |
| Process Assumption | concentrated inventory degrades fill quality and increases risk (Stoikov-Saglam) |
| Redundancy Decision | non-redundant (risk overlay, not alpha signal) |
| Missing-Signal Behavior | default to 0 (no skew) if position missing |
| State / traderData Required | none (position from state.position) |
| Validation / Invalidation Check | compare position utilization and PnL flatness vs base spec |

### F8: Imbalance Confirmation Filter (vouchers)

| Field | Value |
| --- | --- |
| Feature | imbalance confirmation on residual entries |
| Source Fields | voucher order_depths bid/ask volumes |
| Online Availability | usable online |
| Role | execution filter |
| Parameters | if residual says buy AND imbalance > 0: strengthen entry; if residual says buy AND imbalance < -confirm_threshold: weaken entry |
| Multivariate Relationship | imbalance orthogonal to price anchor (PCA PC2) |
| Process Assumption | option imbalance reflects inventory pressure (Muravyev) |
| Redundancy Decision | non-redundant (different PCA component) |
| Missing-Signal Behavior | proceed without confirmation (default to base behavior) |
| State / traderData Required | none |
| Validation / Invalidation Check | compare fill rate and adverse selection vs base spec |

## Execution Logic Changes

- Voucher buy: entry threshold is `base_threshold * (1 + 0.2)` when imbalance disagrees (negative); `base_threshold * (1 - 0.1)` when imbalance agrees (positive). Vice versa for sells.
- Voucher fair shift: `adjusted_fair = bachelier_fair - penalty`; when long, fair moves down making the bot more eager to sell and less eager to buy
- Delta-1 logic: identical to base spec

## Implementation Handoff

- Target bot path: `rounds/round_3/bots/amin/canonical/candidate_c06_composite_inv.py`
- Additional parameters: `inventory_skew_factor` (start ~3-5), `imbalance_confirm_threshold` (start ~0.2)
- Known caveats: inventory skew may suppress profitable voucher trades; imbalance filter may reduce fill rate; compare carefully against base
