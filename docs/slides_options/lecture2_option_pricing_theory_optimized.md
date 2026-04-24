# Lecture 2 — Option Pricing Theory

## Objetivo operativo
Esta presentación conecta tres formas equivalentes de pricing:
- replicación / hedging;
- PDE de Black-Scholes;
- martingalas bajo medida risk-neutral.

Para implementar un módulo útil en trading, lo esencial es:
1. saber calcular precio europeo cerrado;
2. saber calcular **delta** y **gamma**;
3. poder usar pricing por expectativa o por Monte Carlo si el pay-off no es vanilla;
4. entender que el drift real `μ` no entra en el precio arbitrage-free.

## 1) Black-Scholes como modelo base
Dinámica bajo la medida real:
- `dS_t = μ S_t dt + σ S_t dW_t^P`
- `dM_t = r M_t dt`

Supuestos importantes:
- `r` y `σ` constantes;
- sin costos de transacción;
- sin dividendos;
- no arbitraje.

## 2) Derivación por hedging
Se construye un portfolio cubierto:
`Π(t, S_t) = V(t, S_t) - Δ(t, S_t) S_t`

Con Ito:
`dV = (V_t + μ S V_S + 1/2 σ^2 S^2 V_SS) dt + σ S V_S dW`

Elegir `Δ = V_S` elimina el riesgo instantáneo.

Entonces el portfolio cubierto debe crecer al tipo libre de riesgo:
`dΠ = r Π dt`

y aparece la PDE de Black-Scholes:

`V_t + r S V_S + 1/2 σ^2 S^2 V_SS - r V = 0`

con condición terminal:
`V(S, T) = g(S)`

## 3) Interpretación de Greeks
Para trading algorítmico, los Greeks son más importantes que la fórmula sola:
- **Delta** `∂V/∂S`: cobertura lineal;
- **Gamma** `∂²V/∂S²`: estabilidad de delta;
- **Theta**: decaimiento temporal;
- **Vega**: sensibilidad a volatilidad.

Regla práctica:
- gamma alto ⇒ rebalancear más seguido;
- vega alto ⇒ el precio cambia mucho con la vol.

## 4) Martingale / medida risk-neutral
Bajo la medida `Q`:
`dS_t = r S_t dt + σ S_t dW_t^Q`

El precio arbitrage-free cumple:
`V(t, S_t) = e^{-r(T-t)} E^Q[g(S_T) | F_t]`

Interpretación:
- el descuento por `e^{-rt}` hace al precio martingala;
- el drift real `μ` desaparece del precio;
- el precio depende de payoff + parámetros bajo `Q`.

## 5) Feynman–Kac
La Feynman–Kac une la PDE con la expectativa risk-neutral. En práctica, esto te dice:
- si puedes simular `S_T`, puedes pricear;
- si tienes una PDE simple, puedes resolverla directamente;
- ambas rutas son equivalentes para Black-Scholes.

## 6) Solución cerrada para una call europea
Con `τ = T - t`:

`C = S_t N(d1) - K e^{-rτ} N(d2)`

donde:
`d1 = [ln(S_t/K) + (r + σ²/2)τ] / (σ sqrt(τ))`
`d2 = d1 - σ sqrt(τ)`

Put por parity:
`P = C - S_t + K e^{-rτ}`

## 7) Qué implementar
### Función de precio BS
Inputs:
- `S`, `K`, `r`, `σ`, `τ`, tipo call/put

Outputs:
- precio,
- `d1`, `d2`,
- delta,
- gamma,
- vega.

### Uso en trading
- valorar cotizaciones rápidas;
- comparar quote vs modelo;
- estimar mispricing;
- construir hedge con `Δ`;
- medir si un spread compensa el riesgo gamma/vega.

## 8) Fórmulas prácticas
Delta de call europea:
`Δ_call = N(d1)`

Delta de put europea:
`Δ_put = N(d1) - 1`

Gamma:
`Γ = φ(d1) / (S σ sqrt(τ))`

Vega:
`Vega = S φ(d1) sqrt(τ)`

donde `φ` es la pdf normal estándar.

## 9) Algoritmo mínimo recomendado
1. Recibir mercado: `S, K, r, τ, mid_price`
2. Calcular `σ` si ya existe, o usar un `σ` baseline.
3. Obtener `C_BS`, `Δ`, `Γ`, `Vega`
4. Comparar `mid_price - C_BS`
5. Si la desviación es suficiente y el hedge es viable, abrir trade + hedge
6. Rebalancear si gamma o spot cambian mucho

## 10) Mensajes clave para un agente
- El modelo base es Black-Scholes.
- El precio arbitrage-free se obtiene bajo `Q`, no con el drift real.
- La cobertura local se construye con delta.
- Gamma y vega determinan si la estrategia es robusta o frágil.
- Para payoffs complejos, usar Monte Carlo / integración / métodos numéricos.

