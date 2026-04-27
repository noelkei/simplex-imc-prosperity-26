# Strategy Specs

Put reviewed, implementation-ready strategy specs here.

Use [`docs/templates/strategy_spec_template.md`](../../../../docs/templates/strategy_spec_template.md) for each spec.

For `round_4`, specs are grouped by Wave 1 learning pack rather than written as
`15` fully disconnected one-off notes. Each grouped spec must still define:

- the candidate set it covers,
- the shared feature contracts,
- the candidate-specific differences,
- the round-specific mechanics contract,
- and the validation checks needed to separate the branch outcomes cleanly.

Current grouped Wave 1 specs:

- [`spec_pack_a_delta1_controls.md`](spec_pack_a_delta1_controls.md)
- [`spec_pack_b_round3_revalidation.md`](spec_pack_b_round3_revalidation.md)
- [`spec_pack_c_5300_active_family.md`](spec_pack_c_5300_active_family.md)
- [`spec_pack_d_counterparty_defensive.md`](spec_pack_d_counterparty_defensive.md)
- [`spec_pack_e_execution_and_family_context.md`](spec_pack_e_execution_and_family_context.md)
- [`spec_pack_f_low_priority_probes.md`](spec_pack_f_low_priority_probes.md)

Implementation must not start from a loose candidate note alone. Fast mode may
use a one-page spec, but it still requires signal, execution, risk, state, and
validation checks.
