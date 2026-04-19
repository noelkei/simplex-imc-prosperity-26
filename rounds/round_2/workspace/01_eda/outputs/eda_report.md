# Round 2 — Deep EDA Outputs

Data dir: `/home/user/simplex-imc-prosperity-26/rounds/round_2/workspace/01_eda/scripts/../../../data/raw`


## 1. Descriptive Stats (per product per day)

| Product | Day | n (all) | n (usable) | mid mean | mid std | mid min | mid max | spread mean | spread mode | bv1 mean | av1 mean | mid[0] | mid[-1] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INTARIAN_PEPPER_ROOT | -1 | 10000 | 9246 | 11501.16 | 288.27 | 10998.0 | 12001.5 | 13.07 | 13.0 | 11.6 | 11.6 | 11001.5 | 11999.5 |
| INTARIAN_PEPPER_ROOT | 0 | 10000 | 9230 | 12501.43 | 288.46 | 11997.5 | 13000.5 | 14.12 | 13.0 | 11.6 | 11.6 | 11998.5 | 13000.0 |
| INTARIAN_PEPPER_ROOT | 1 | 10000 | 9248 | 13500.11 | 289.16 | 12997.0 | 14001.0 | 15.18 | 14.0 | 11.6 | 11.6 | 13000.0 | 13999.5 |
| ASH_COATED_OSMIUM | -1 | 10000 | 9237 | 10000.83 | 3.86 | 9986.5 | 10014.5 | 16.22 | 16.0 | 14.2 | 14.2 | 9991.0 | 10002.0 |
| ASH_COATED_OSMIUM | 0 | 10000 | 9257 | 10001.58 | 5.22 | 9982.0 | 10019.5 | 16.25 | 16.0 | 14.3 | 14.2 | 10003.0 | 10008.0 |
| ASH_COATED_OSMIUM | 1 | 10000 | 9214 | 10000.15 | 4.48 | 9985.0 | 10014.0 | 16.23 | 16.0 | 14.2 | 14.2 | 10008.0 | 9993.0 |

## 2. IPR Linear Drift Fit (mid ~ slope * t + intercept)

| Day | slope (per tick) | intercept | resid stdev | start fit | end fit | total drift |
|---|---|---|---|---|---|---|
| -1 | 0.001000 | 10999.98 | 2.19 | 11000.0 | 11999.9 | +999.9 |
| 0 | 0.001000 | 12000.01 | 2.36 | 12000.0 | 12999.9 | +999.9 |
| 1 | 0.001000 | 12999.92 | 2.54 | 12999.9 | 13999.9 | +999.9 |

## 3. ACO AR(1) Fit on mid-minus-mean

| Day | mean mid | phi (AR1) | sigma (innov) | half-life (ticks) |
|---|---|---|---|---|
| -1 | 10000.83 | 0.6576 | 3.364 | 1.7 |
| 0 | 10001.61 | 0.7880 | 3.485 | 2.9 |
| 1 | 10000.21 | 0.7303 | 3.428 | 2.2 |

## 4. Autocorrelation of delta-mid (lags 1..20)

| Product | Day | AC(1) | AC(2) | AC(5) | AC(10) | AC(20) |
|---|---|---|---|---|---|---|
| INTARIAN_PEPPER_ROOT | -1 | -0.498 | -0.007 | -0.019 | -0.004 | +0.001 |
| INTARIAN_PEPPER_ROOT | 0 | -0.489 | -0.014 | -0.019 | +0.006 | -0.010 |
| INTARIAN_PEPPER_ROOT | 1 | -0.508 | +0.031 | -0.008 | +0.002 | -0.007 |
| ASH_COATED_OSMIUM | -1 | -0.506 | +0.019 | +0.007 | -0.018 | +0.005 |
| ASH_COATED_OSMIUM | 0 | -0.506 | +0.014 | -0.004 | -0.004 | -0.005 |
| ASH_COATED_OSMIUM | 1 | -0.491 | -0.005 | -0.040 | -0.009 | -0.003 |

## 5. Kalman Filter Grid Search — Best (Q, R) per product per day

For IPR we fit on the detrended mid (mid - drift(t)) to separate drift from noise. For ACO we fit on raw mid (since no drift).

| Product | Day | Best Q | Best R | NLL per tick | K steady-state |
|---|---|---|---|---|---|
| INTARIAN_PEPPER_ROOT | -1 | 0.0001 | 4.0 | 2.2157 | 0.0051 |
| INTARIAN_PEPPER_ROOT | 0 | 0.0001 | 8.0 | 2.3096 | 0.0037 |
| INTARIAN_PEPPER_ROOT | 1 | 0.0001 | 8.0 | 2.3641 | 0.0037 |
| ASH_COATED_OSMIUM | -1 | 0.1 | 8.0 | 2.4372 | 0.1057 |
| ASH_COATED_OSMIUM | 0 | 0.1 | 8.0 | 2.4362 | 0.1057 |
| ASH_COATED_OSMIUM | 1 | 0.1 | 8.0 | 2.4428 | 0.1057 |

## 6. 2-State Gaussian HMM on ACO delta-mid (Baum-Welch, 30 iters)

Interpretation: state 0 = low-vol, state 1 = high-vol. High persistence (avg run > 50 ticks) would support regime-aware quoting.

| Day | mu_low | sigma_low | mu_high | sigma_high | P(low->low) | P(high->high) | state0 frac | avg run_0 | avg run_1 | switches |
|---|---|---|---|---|---|---|---|---|---|---|
| -1 | +0.000 | 0.997 | +0.002 | 6.035 | 0.833 | 0.700 | 0.694 | 7.4 | 3.2 | 1878 |
| 0 | +0.001 | 0.991 | -0.001 | 6.079 | 0.841 | 0.704 | 0.697 | 7.7 | 3.4 | 1804 |
| 1 | -0.002 | 0.975 | -0.000 | 6.013 | 0.833 | 0.701 | 0.691 | 7.4 | 3.3 | 1854 |

## 7. Order-Book Imbalance IC at lag 1..5

corr( imbalance(t), delta_mid(t+k) ). Positive values mean a buy-side imbalance at tick t predicts an up-move at tick t+k.

| Product | Day | IC@1 | IC@2 | IC@3 | IC@5 |
|---|---|---|---|---|---|
| INTARIAN_PEPPER_ROOT | -1 | +0.382 | +0.404 | +0.393 | +0.406 |
| INTARIAN_PEPPER_ROOT | 0 | +0.392 | +0.396 | +0.399 | +0.397 |
| INTARIAN_PEPPER_ROOT | 1 | +0.403 | +0.401 | +0.408 | +0.392 |
| ASH_COATED_OSMIUM | -1 | +0.382 | +0.368 | +0.383 | +0.381 |
| ASH_COATED_OSMIUM | 0 | +0.384 | +0.374 | +0.381 | +0.363 |
| ASH_COATED_OSMIUM | 1 | +0.368 | +0.357 | +0.374 | +0.379 |

## 8. Trade summary (market flow)

| Product | Day | n trades | avg qty | price min | price max | total volume |
|---|---|---|---|---|---|---|
| INTARIAN_PEPPER_ROOT | -1 | 331 | 5.0 | 10996.0 | 11998.0 | 1669 |
| INTARIAN_PEPPER_ROOT | 0 | 332 | 5.0 | 11998.0 | 12987.0 | 1671 |
| INTARIAN_PEPPER_ROOT | 1 | 333 | 5.1 | 12998.0 | 13999.0 | 1693 |
| ASH_COATED_OSMIUM | -1 | 459 | 5.1 | 9982.0 | 10019.0 | 2348 |
| ASH_COATED_OSMIUM | 0 | 471 | 5.1 | 9979.0 | 10020.0 | 2404 |
| ASH_COATED_OSMIUM | 1 | 465 | 5.1 | 9980.0 | 10018.0 | 2375 |

## 9. IPR cross-day level continuity

- day -1: first mid = 11001.5, last mid = 11999.5
- day 0: first mid = 11998.5, last mid = 13000.0
- day 1: first mid = 13000.0, last mid = 13999.5
