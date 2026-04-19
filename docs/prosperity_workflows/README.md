# Prosperity Workflows

This folder defines how contributors and coding agents should work in this repository.

It is not a strategy manual and it does not define one correct path to a winning Python file. Useful work can come from exploratory data analysis, strategy research, bot implementation, debugging, validation, round documentation, or handoff cleanup.

## Source hierarchy

- Use [`../prosperity_wiki/`](../prosperity_wiki/) for factual rules: API contracts, datamodel fields, exchange mechanics, position limits, runtime constraints, platform flow, round facts, and source caveats.
- Use [`../prosperity_playbook/`](../prosperity_playbook/) for heuristics: strategy patterns, risk habits, debugging practices, and iteration advice.
- Do not use round-local bot or performance artifacts as a source of truth.
- Do not use [`../../non-canonical/`](../../non-canonical/) as evidence or examples unless the user explicitly points to a draft.
- Treat the Prosperity API contract as stable unless round documentation explicitly says otherwise.

When a fact is missing, ambiguous, or inconsistent, record a caveat. Do not invent official rules.

## How To Use These Workflows

For active round work, start from `rounds/round_X/workspace/_index.md`, then read the relevant phase context and the task-specific workflow below.

When starting a phase, confirm required inputs and update the phase context. When continuing, update the existing artifact instead of creating duplicates. When closing, check the exit criteria, update `_index.md`, update the phase context, and leave a concrete next action.

When `rounds/round_X/workspace/post_run_research_memory.md` exists, treat it as
round-local evidence input for EDA, understanding, strategy, spec, and variant
decisions. Cite relevant insights when they influence a decision; do not treat
the memory as official Prosperity rules.

Keep the lightweight gates aligned across phases:

- EDA owns the feature lifecycle, Round Adaptation Check, compact multivariate/redundancy layer, and process/distribution hypotheses.
- Understanding compresses promoted signals, multivariate/process evidence, redundancy decisions, and assumptions carried forward.
- Strategy enforces the feature budget and Round Coverage Check.
- Specs define the Feature Contract, including online proxies and invalidation checks for process or multivariate assumptions, and Round-Specific Mechanics Contract.
- Validation owns the ROI-gated run update decision: `update`, `update lightly`, or `no update`, including process/multivariate feedback when it changes future decisions.

## Research Environment Use

Use the repo `.venv` and `requirements.txt` for research, EDA, notebooks, validation, and post-run diagnostics when they improve decision quality. These packages do not expand Prosperity bot runtime permissions; uploadable `Trader` files must still follow the wiki runtime docs and reviewed specs.

Use research tools only when they answer a decision-relevant question faster or more rigorously. Record the method and caveat in the artifact. Do not force libraries into small checks, overfit sample data, or turn offline models into bot logic without an online-usable Feature Contract.

### Phase Usage Rules

| Phase | Should Use | Optional | Do Not Use |
| --- | --- | --- | --- |
| Round preparation / ingestion | Standard library for file/source checks | `pandas` for schema summaries when data exists | modeling libraries; strategy conclusions |
| EDA | `pandas`/`numpy`, `scipy`, `statsmodels`, `pingouin`, plots for distributions, signals, multivariate checks, redundancy, process hypotheses, and tests | `polars` for large CSV/logs, `numba` for repeated loops, `arch`/`ruptures` for regime questions, `sklearn` for PCA, clustering, mutual information, or feature screening | broad ML, feature catalogs, or tests that cannot change a downstream decision |
| Understanding | statistical confidence, effect size, stability, and negative evidence from EDA | small follow-up summaries using existing processed data | rerunning broad EDA or promoting weak/offline-only features |
| Strategy candidates | EDA/understanding outputs as evidence for feature-light candidates | request targeted EDA for unresolved high-impact unknowns | adding models or research-library dependencies to candidates just because they exist |
| Strategy spec | research outputs only as traceable evidence and parameter rationale | validation checks derived from statistical confidence or regimes | requiring bot imports from research-only packages unless the wiki runtime allows them |
| Implementation | none beyond local static/smoke tooling | tiny standard-library online proxies named in the spec | importing research-only packages into uploadable bots |
| Validation / post-run | `pandas`/`polars` for logs, `numba` for replay loops, statistics for fill quality and adverse selection | `ruptures` for failure windows, `arch` for volatility regimes, `pingouin`/`scipy` for confidence checks | precise PnL prediction models, heavy ML, or proxy rankings presented as real PnL |

### Library Map

| Library | Phase(s) | Use Case | When To Use | When Not To Use |
| --- | --- | --- | --- | --- |
| `numpy`, `pandas` | EDA, validation, post-run | core arrays, tables, rolling features, PnL splits | default for moderate data and durable tables | tiny one-off checks where standard library is clearer |
| `polars` | EDA, validation, post-run | fast CSV/log scans and group/window operations | large multi-day files, big platform logs, repeated aggregations | small tables where it adds a second dataframe style for no gain |
| `scipy`, `statsmodels` | EDA, understanding | distributions, correlations, regressions, time-series diagnostics | signal strength, stability, or uncertainty affects decisions | to create opaque models without a strategy use |
| `pingouin` | EDA, understanding, post-run | effect sizes, confidence intervals, compact statistical tests | comparing features, regimes, fills, or variants | when a simple descriptive table is enough |
| `arch` | EDA, understanding | volatility/regime diagnostics | volatility clustering could change risk, sizing, or filters | if volatility does not affect the next decision |
| `ruptures` | EDA, validation, post-run | change-point and failure-window detection | regime shifts, drift breaks, or run failures need segmentation | as a decorative regime label with no action |
| `scikit-learn` | EDA, strategy evidence | PCA/loadings, mutual information, clustering, feature screening, simple predictive baselines | hypotheses need lightweight validation, redundancy analysis, or grouping | training complex offline models for direct bot use |
| `numba` | EDA, validation, post-run | fast replay, markouts, rolling loops, order-book sweeps | repeated Python loops are a bottleneck | small scripts where JIT startup costs more than it saves |
| `matplotlib`, `seaborn`, `plotly`, `jupyterlab` | EDA, handoffs | charts, notebooks, exploratory inspection | visuals make distributions/regimes/fills easier to review | when a table and Markdown handoff are clearer |

## Workstream map

- [`01_project_operating_model.md`](01_project_operating_model.md): shared operating model for contributors and agents.
- [`02_sources_of_truth.md`](02_sources_of_truth.md): how to combine wiki facts with playbook heuristics.
- [`03_workstream_eda.md`](03_workstream_eda.md): exploratory data analysis workflow.
- [`04_workstream_strategy.md`](04_workstream_strategy.md): strategy research workflow.
- [`05_workstream_bot_implementation.md`](05_workstream_bot_implementation.md): bot implementation workflow.
- [`06_workstream_debugging_and_validation.md`](06_workstream_debugging_and_validation.md): debugging and validation workflow.
- [`07_workstream_round_preparation.md`](07_workstream_round_preparation.md): new-round documentation and preparation workflow.
- [`08_handoffs_and_documentation.md`](08_handoffs_and_documentation.md): safe handoff patterns between workstreams.
- [`09_safe_change_rules.md`](09_safe_change_rules.md): durable rules for safe repo changes.
- [`10_time_aware_team_pipeline.md`](10_time_aware_team_pipeline.md): 2-day deadline workflow, phase state tracking, round indexes, and fast mode.
- [`11_dataset_eda_framework.md`](11_dataset_eda_framework.md): column classification, adaptive EDA, and EDA-as-knowledge-transfer guidance.
- [`12_top_level_artifact_audit.md`](12_top_level_artifact_audit.md): historical cleanup audit for removed top-level `bots/` and `performances/`.
- [`../templates/`](../templates/): reusable Markdown templates for EDA, understanding, strategy candidates, strategy specs, run summaries, post-run research memory, and debugging issues.

## Operating rule

Each contribution should make the next contributor's job easier. A good handoff states what changed, which sources were used, what assumptions remain, what evidence exists, and what the next useful action is.
