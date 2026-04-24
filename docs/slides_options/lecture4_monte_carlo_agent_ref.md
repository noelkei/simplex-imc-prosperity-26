# Monte Carlo Simulation for Option Pricing — Agent Reference
> **Source:** TU Delft Computational Finance, Lecture 4 (Dr. Fang Fang)  
> **Purpose:** Implementation-ready reference for algorithmic agents (Claude / Codex)

---

## 1. Theoretical Foundation

### 1.1 Core Idea
Monte Carlo integration estimates `E[f(X)]` by averaging over i.i.d. samples:

```
I ≈ (1/N) * Σ f(x_i),   x_i ~ target distribution
```

Guaranteed by the **Strong Law of Large Numbers (SLLN)**:  
`X̄_N → μ` almost surely as `N → ∞`

**Standard error decays at rate `1/√N`** (from CLT):
```
(X̄_N - μ) / (σ/√N)  →  N(0,1)
```

### 1.2 Convergence Types (strength order)
| Type | Notation | Meaning |
|------|----------|---------|
| Almost Sure | `Xₙ →ᵃˢ X` | Sample paths converge w.p. 1 (STRONGEST) |
| In Probability | `Xₙ →ᵖ X` | P(\|Xₙ-X\|>ε) → 0 |
| In Distribution | `Xₙ →ᵈ X` | CDFs converge (WEAKEST) |

**Implication chain:** a.s. ⇒ probability ⇒ distribution (not reversible)

---

## 2. SDE Simulation Schemes

### 2.1 General SDE
```
dXt = μ(t, Xt) dt + σ(t, Xt) dWt
```

### 2.2 Euler–Maruyama Scheme ⭐ (Default choice)
```python
# Time grid: tk = k*h, k=0,...,K,  K*h = T
# Zk ~ i.i.d. N(0,1)

X[0] = X0
for k in range(1, K+1):
    Z = np.random.standard_normal()
    X[k] = X[k-1] + mu(t[k-1], X[k-1])*h + sigma(t[k-1], X[k-1])*np.sqrt(h)*Z
```

**Convergence:**
- Strong order: β = 1/2
- Weak order: β = 1
- For European options in practice: O(h^(1/3)) due to non-smooth payoffs

### 2.3 Milstein Scheme (Higher accuracy)
```python
# Adds curvature correction term
X[k] = X[k-1] \
     + mu(t[k-1], X[k-1])*h \
     + sigma(t[k-1], X[k-1])*np.sqrt(h)*Z \
     + 0.5 * sigma(t[k-1], X[k-1]) * dsigma_dx(t[k-1], X[k-1]) * (Z**2 - 1)*h
```

**Convergence:** Strong β = 1, Weak β = 1  
**Caveat:** Hard to generalize to multi-dimensional SDEs.

### 2.4 Black–Scholes GBM (Exact simulation, preferred)
```python
# Exact — no discretization error
ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
# Z ~ N(0,1)
```

---

## 3. Variance Reduction Techniques

### 3.1 Antithetic Variates ⭐ (Easy, always try first)

**Idea:** For every path with shocks `Z`, also simulate `−Z`. Average both payoffs.

```python
def price_european_antithetic(S0, K, r, sigma, T, N=100_000):
    Z = np.random.standard_normal(N)
    
    ST_pos = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    ST_neg = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*(-Z))
    
    payoff = 0.5 * (np.maximum(ST_pos - K, 0) + np.maximum(ST_neg - K, 0))
    return np.exp(-r*T) * np.mean(payoff)
```

**Why it works:** `Cov(f(U), f(1-U)) < 0` when `f` is monotonic  
⇒ `Var(Î_M) = (1/M)[Var(f)/2 + Cov/2] < Var(I_M)`

**For path-dependent options:** negate the entire shock sequence `{Z_0,...,Z_{N-1}}`

### 3.2 Control Variates ⭐ (Use when analytical benchmark exists)

**Idea:** If `Y` is correlated with `X` and `E[Y]` is known:
```
Z_θ = X + θ*(E[Y] - Y),   E[Z_θ] = E[X]
```

Optimal: `θ* = Cov(X,Y) / Var(Y)`  
Variance reduction: `Var(Z_{θ*}) = (1 - ρ²_{XY}) * Var(X)`

```python
def price_asian_control_variate(S0, K, r, sigma, T, n, N=100_000):
    # Arithmetic Asian (target) vs Geometric Asian (control, has closed form)
    dt = T / n
    paths = simulate_paths(S0, r, sigma, dt, n, N)  # shape (N, n)
    
    arith_avg = paths.mean(axis=1)
    geom_avg  = np.exp(np.log(paths).mean(axis=1))
    
    X = np.exp(-r*T) * np.maximum(arith_avg - K, 0)  # target
    Y = np.exp(-r*T) * np.maximum(geom_avg  - K, 0)  # control
    EY = geometric_asian_formula(S0, K, r, sigma, T, n)  # known closed form
    
    theta = np.cov(X, Y)[0,1] / np.var(Y)
    Z = X + theta * (EY - Y)
    return np.mean(Z), np.std(Z) / np.sqrt(N)
```

**Classic application:** Arithmetic Asian option (no closed form) controlled by Geometric Asian option (has closed form for equally-spaced monitoring dates).

### 3.3 Quasi-Monte Carlo (QMC) ⭐ (Better convergence for smooth payoffs)

**Replace** random samples with **low-discrepancy sequences**:
- Sobol, Halton, Faure, Lattice rules

**Convergence comparison:**
| Method | Rate |
|--------|------|
| Standard MC | O(N^{-1/2}) |
| QMC | O((log N)^d / N) |
| Quadrature (1D) | O(N^{-k}) but curse of dimensionality |

```python
from scipy.stats.qmc import Sobol
import scipy.stats as stats

def price_european_qmc(S0, K, r, sigma, T, N=100_000):
    sampler = Sobol(d=1, scramble=True)
    u = sampler.random(N).flatten()           # uniform [0,1]
    Z = stats.norm.ppf(u)                     # inverse CDF transform
    
    ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    payoff = np.maximum(ST - K, 0)
    return np.exp(-r*T) * np.mean(payoff)
```

**Note:** QMC convergence bound given by Koksma–Hlawka inequality:
`|estimator - true| ≤ V(f) * D*_N`  
where `D*_N` is star discrepancy (measures uniformity of point set).

### 3.4 Importance Sampling via Drift Shifting (Advanced, for deep OTM options)

**Idea:** Shift sampling distribution toward payoff-relevant region; correct with likelihood ratio.

**Setup:** `V = E[f(Z)]`, `Z ~ N(0,I)`. Introduce shift `θ`, simulate `Z* = Z + θ`:

```
V = E[f(Z+θ) * exp(-θᵀZ - ½‖θ‖²)]
```

**Black–Scholes example:**
```python
def price_european_is(S0, K, r, sigma, T, mu_shift, N=100_000):
    Z = np.random.standard_normal(N)
    Z_shifted = Z + mu_shift
    
    ST = S0 * np.exp((r - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z_shifted)
    payoff = np.maximum(ST - K, 0)
    
    # Likelihood ratio (Radon-Nikodym derivative)
    L = np.exp(-mu_shift*Z_shifted + 0.5*mu_shift**2)
    
    return np.exp(-r*T) * np.mean(payoff * L)

# Optimal shift: place mean of log(ST) at log(K) (at-the-money under shifted measure)
mu_optimal = (np.log(K/S0) - (r - 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
```

**Optimal θ:** Minimize second moment `M(θ) = E[f(Z+θ)² * exp(-2θᵀZ - ‖θ‖²)]`  
via first-order condition `∇_θ M(θ*) = 0`.

---

## 4. Change of Numeraire (Theory + Black–Scholes Derivation)

### 4.1 Core Formula
Under risk-neutral measure Q (bank account numeraire `Mt = e^{rt}`):
```
C0 = e^{-rT} E^Q[(ST - K)⁺]
   = e^{-rT} E^Q[ST 1_{ST>K}] - e^{-rT} K E^Q[1_{ST>K}]
```

Using stock `St` as numeraire (measure `Q^S`):
```
E^Q[ST 1_{ST>K}] = S0 * e^{rT} * Q^S(ST > K) = S0 * e^{rT} * N(d1)
```

**Radon-Nikodym derivative:**
```
dQ^S/dQ |_{Ft} = e^{-rt} St / S0
```

Under `Q^S`: `dSt = (r + σ²)St dt + σ St dW^S_t`

### 4.2 Black–Scholes Formula Recovery
```
d1 = [log(S0/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T

C0 = S0 N(d1) - K e^{-rT} N(d2)
```

---

## 5. Complete Implementation Template

```python
import numpy as np
from scipy.stats import norm
from scipy.stats.qmc import Sobol

class MonteCarloOptionPricer:
    """
    European/path-dependent option pricer with variance reduction.
    Supports: plain MC, antithetic, QMC, importance sampling.
    """
    
    def __init__(self, S0, K, r, sigma, T):
        self.S0, self.K, self.r, self.sigma, self.T = S0, K, r, sigma, T
    
    def black_scholes_call(self):
        """Analytical benchmark."""
        d1 = (np.log(self.S0/self.K) + (self.r + 0.5*self.sigma**2)*self.T) / \
             (self.sigma*np.sqrt(self.T))
        d2 = d1 - self.sigma*np.sqrt(self.T)
        return self.S0*norm.cdf(d1) - self.K*np.exp(-self.r*self.T)*norm.cdf(d2)
    
    def _simulate_ST(self, Z):
        return self.S0 * np.exp(
            (self.r - 0.5*self.sigma**2)*self.T + self.sigma*np.sqrt(self.T)*Z
        )
    
    def price(self, N=100_000, method='antithetic'):
        if method == 'plain':
            Z = np.random.standard_normal(N)
            payoff = np.maximum(self._simulate_ST(Z) - self.K, 0)
            
        elif method == 'antithetic':
            Z = np.random.standard_normal(N)
            payoff = 0.5 * (
                np.maximum(self._simulate_ST(Z)  - self.K, 0) +
                np.maximum(self._simulate_ST(-Z) - self.K, 0)
            )
            
        elif method == 'qmc':
            sampler = Sobol(d=1, scramble=True)
            u = sampler.random(N).flatten()
            Z = norm.ppf(np.clip(u, 1e-10, 1-1e-10))
            payoff = np.maximum(self._simulate_ST(Z) - self.K, 0)
            
        elif method == 'importance_sampling':
            mu = (np.log(self.K/self.S0) - (self.r - 0.5*self.sigma**2)*self.T) / \
                 (self.sigma*np.sqrt(self.T))
            Z = np.random.standard_normal(N)
            Z_s = Z + mu
            payoff = np.maximum(self._simulate_ST(Z_s) - self.K, 0) * \
                     np.exp(-mu*Z_s + 0.5*mu**2)
        
        price = np.exp(-self.r*self.T) * np.mean(payoff)
        se = np.exp(-self.r*self.T) * np.std(payoff) / np.sqrt(N)
        return price, se


# --- Usage ---
pricer = MonteCarloOptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1.0)

bs    = pricer.black_scholes_call()
plain = pricer.price(N=100_000, method='plain')
anti  = pricer.price(N=100_000, method='antithetic')
qmc   = pricer.price(N=100_000, method='qmc')
is_   = pricer.price(N=100_000, method='importance_sampling')

print(f"Black-Scholes:        {bs:.4f}")
print(f"Plain MC:             {plain[0]:.4f}  ±{plain[1]:.4f}")
print(f"Antithetic:           {anti[0]:.4f}  ±{anti[1]:.4f}")
print(f"QMC (Sobol):          {qmc[0]:.4f}  ±{qmc[1]:.4f}")
print(f"Importance Sampling:  {is_[0]:.4f}  ±{is_[1]:.4f}")
```

---

## 6. Decision Guide for Agents

```
Goal: price an option via MC with lowest variance for fixed compute budget N

1. Is there a closed-form solution?  → Use it directly (Black-Scholes for European)

2. Path-dependent (Asian, Barrier, Lookback)?
   a. Smooth payoff + d ≤ 10 dimensions → QMC (Sobol) + Antithetic
   b. Rough/discontinuous payoff        → Antithetic + Control Variate
   c. Deep OTM, rare event              → Importance Sampling

3. High-dimensional (d >> 10)?
   → MC with Antithetic (QMC degrades for large d)

4. Always compute standard error: SE = σ̂/√N  (95% CI: estimate ± 1.96*SE)

5. Variance reduction priority:
   Antithetic (free) > Control Variates (needs benchmark) > 
   QMC (needs smooth integrand) > Importance Sampling (needs optimal shift)
```

---

## 7. Key Formulas Cheatsheet

| Concept | Formula |
|---------|---------|
| MC standard error | `σ/√N` |
| MC convergence | `O(N^{-1/2})` |
| QMC convergence | `O((log N)^d / N)` |
| Euler step | `X_{k+1} = X_k + μh + σ√h Z` |
| Milstein extra term | `+ ½ σ (∂σ/∂x)(Z²-1)h` |
| Antithetic variance | `Var = ½Var(f) + ½Cov(f(U),f(-U))` |
| Control variate θ* | `Cov(X,Y)/Var(Y)` |
| CV variance reduction | `(1-ρ²_{XY}) * Var(X)` |
| IS likelihood ratio (1D) | `L(z*) = exp(-μz* + ½μ²)` |
| BS d1 | `[log(S/K) + (r+σ²/2)T] / (σ√T)` |
| BS d2 | `d1 - σ√T` |

---

*Reference: Glasserman (2004) Monte Carlo Methods in Financial Engineering — the standard textbook for all implementations above.*
