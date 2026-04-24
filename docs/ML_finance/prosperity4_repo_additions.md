# Prosperity 4 Repository Additions
## Actionable ideas distilled from `mfrdixon/ML_Finance_Codes`

This note is written for an agentic codebase that needs to stay compatible with IMC Prosperity 4.

## What this external repository is good for

`mfrdixon/ML_Finance_Codes` is a notebook-heavy reference implementation for *Machine Learning in Finance: From Theory to Practice*. The most relevant ideas for a trading repo are:

- probabilistic modeling and Bayesian inference
- Gaussian Processes and uncertainty-aware forecasting
- neural networks and Bayesian neural networks
- interpretability and feature attribution
- sequence modeling with ARIMA, PCA, RNNs, CNNs, autoencoders
- probabilistic sequence modeling with Kalman filters and Viterbi
- reinforcement learning for market making, execution, allocation, and option hedging
- inverse reinforcement learning for learning reward structures from behavior

## What to add to our repository first

### 1) A proper market-state and feature pipeline
Create a single feature layer that every strategy can reuse.

Recommended features:
- mid-price, spread, microprice
- order flow imbalance (OFI)
- short-window returns and volatility
- inventory, cash, realized/unrealized PnL
- rolling z-scores and mean-reversion signals
- volume, VWAP deviation, book pressure
- product-specific features for each round

Why this matters:
- The external repo explicitly uses OFI in ARIMA-style HFT forecasting and sequence modeling ideas that depend on stable, reusable feature engineering.
- A shared feature layer prevents every agent from rebuilding slightly different logic.

### 2) Stationarity checks and regime detection
Before fitting any predictive model, add:
- Dickey-Fuller / stationarity checks
- rolling autocorrelation and partial autocorrelation
- regime flags based on volatility and spread behavior

Why this matters:
- The repo’s sequence modeling notebooks use stationarity analysis and ACF/PACF to select ARIMA structure.
- In Prosperity, regime shifts happen quickly, so the strategy should know when to trust a predictor.

### 3) Uncertainty-aware predictors
Add models that output confidence, not just point forecasts.

Best candidates:
- Bayesian linear regression
- Gaussian Process regression
- Bayesian neural nets for small, noisy signals

How to use them:
- use forecast uncertainty to scale order size
- reduce inventory when uncertainty is high
- widen quotes when forecast confidence drops

Why this matters:
- The repo’s Chapter 2 and Chapter 3 material focuses on Bayesian estimation and Gaussian Processes with uncertainty bands.
- This is especially useful in competition settings where overconfident signals are expensive.

### 4) Mean-reversion and spread-trading modules
Build a dedicated statistical-arbitrage layer for paired or basket products.

Recommended pieces:
- rolling hedge ratio estimation
- spread z-score
- entry/exit thresholds
- half-life / reversion speed estimates
- basket vs. constituent decomposition

Why this matters:
- The repo includes PCA over multiple assets and regression-style modeling that is useful for basket spread logic.
- This is one of the most likely patterns to matter in Prosperity-style rounds involving related products.

### 5) Market-making and inventory control
This should be a first-class module, not an afterthought.

Add:
- fair-value estimator
- bid/ask skew based on inventory
- inventory limits and soft/hard caps
- quote refresh logic
- adverse-selection filters
- kill-switches for unstable conditions

Why this matters:
- The RL chapter in the repo includes market making and market impact notebooks.
- Prosperity rewards robust quoting and inventory management as much as prediction.

### 6) Execution and market-impact logic
Add a simple execution engine that decides:
- when to cross the spread
- when to passively quote
- when to fade or reduce size
- how to avoid self-defeating churn

Why this matters:
- The repo explicitly covers optimal execution and market impact.
- Even good alpha loses value if execution costs are ignored.

### 7) RL-ready environment wrappers
Build a clean environment interface around the competition simulator.

Recommended design:
- `state`: market features, inventory, pnl, time, product context
- `action`: quote, cancel, buy, sell, size
- `reward`: pnl minus inventory risk and execution cost
- `episode`: one competition round or one session chunk

Why this matters:
- The repository has RL notebooks for financial cliff walking, market making, stock execution, wealth management, option pricing, and inverse RL.
- This is useful for future rounds, even if the final competition bot stays rule-based or hybrid.

### 8) Interpretability and debugging tools
Add observability for every strategy decision.

Recommended outputs:
- top features driving each signal
- why a trade was blocked
- why inventory was reduced
- forecast vs. realized move plots
- strategy performance by regime

Why this matters:
- The repo includes several interpretability notebooks and a deep factor model notebook with walk-forward evaluation.
- In a live competition, debugging speed matters.

### 9) Walk-forward backtesting and experiment tracking
Add a standard evaluation harness.

Required features:
- walk-forward splits
- fixed seed runs
- parameter sweep logging
- per-product metrics
- per-round scoreboards
- summary artifacts for each agent

Why this matters:
- The external repo repeatedly uses train/test splits and walk-forward optimization concepts.
- Without this, teams tend to overfit notebook experiments.

### 10) Derivatives / option-style tooling for future rounds
Even if not needed immediately, keep a module ready for option-like products.

Add:
- Black-Scholes helpers
- Greeks
- simple hedging logic
- GP-based price approximation
- volatility estimation

Why this matters:
- The repo includes Black-Scholes, GP pricing, Heston-related work, and QLBS-style RL for option pricing and hedging.
- These are the most reusable foundations if Prosperity introduces derivative-like products later.

## What to prioritize for Round 3

For a round where the product set is still evolving, the highest-value additions are:

1. shared market-feature pipeline
2. uncertainty-aware fair value estimation
3. market-making with inventory skew
4. execution / anti-churn logic
5. walk-forward backtesting
6. simple RL wrappers for future automation

If the round introduces paired products, add mean-reversion and spread-trading immediately.
If the round introduces noisy trend products, add ARIMA-style forecasting and regime detection.
If the round introduces option-like behavior, activate the derivatives module.

## Prosperity 4 constraints the code must respect

- The challenge is made of 5 rounds.
- Each round has one algorithmic challenge and one manual challenge.
- Algorithmic and manual scores are independent.
- Team composition can change only in the first two rounds.
- After Round 2, team composition is locked.
- The algorithmic bot must be a Python program.
- The platform is a simulated market, so every strategy should be deterministic enough to reproduce and debug.

## Implementation rules for agents

When adding any strategy module:
- keep the module small and deterministic
- use shared dataclasses for state, orders, fills, positions, and metrics
- expose a single `decide_orders(state)` entry point
- add a matching backtest stub
- log every decision with the inputs that triggered it
- keep round-specific logic isolated from reusable infrastructure

## Suggested repository structure

- `core/`
  - market state models
  - order and trade models
  - feature generation
  - risk and inventory utilities
- `strategies/`
  - market_making.py
  - mean_reversion.py
  - forecasting.py
  - execution.py
  - hybrid_controller.py
- `models/`
  - bayesian/
  - gp/
  - arima/
  - rl/
- `backtest/`
  - walk_forward.py
  - scenario_runner.py
  - metrics.py
- `analysis/`
  - interpretability.py
  - regime_report.py
  - performance_report.py

## Bottom line

The strongest ideas to borrow from `ML_Finance_Codes` are not the notebooks themselves, but the design patterns:
- uncertainty-aware prediction
- feature-driven market structure analysis
- inventory-aware market making
- execution cost awareness
- walk-forward evaluation
- RL wrappers for later rounds

These will make the repository more robust for Round 3 and set it up for future rounds without locking the team into one brittle approach.
