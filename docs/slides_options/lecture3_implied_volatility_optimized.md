# Lecture 3 — Implied Volatility

## Objetivo operativo
Esta presentación enseña cómo sacar la volatilidad implícita desde el precio de mercado y cómo invertir Black-Scholes de forma robusta.

Para un sistema de trading, la idea clave es:
- la **volatilidad implícita** es la variable de estado más útil;
- la superficie de vol resume el mercado mejor que una sola σ;
- la inversión numérica debe ser estable y rápida;
- la forma de la smile/term structure revela ineficiencias y límites del modelo BS.

## 1) Qué es la implied vol
En Black-Scholes, casi todo está observado salvo `σ`:
- `S_t`
- `K`
- `r`
- `τ = T - t`

Dado un precio de mercado `V_mkt`, buscamos `σ_impl` tal que:

`V_BS(σ_impl) = V_mkt`

Para calls europeas:
`C_BS(σ_impl) - C_mkt = 0`

## 2) Unicidad
La Vega es positiva en Black-Scholes:
- el precio de la call sube de forma estricta con `σ`;
- eso garantiza una implied vol única dentro del rango admisible del precio.

Rango teórico de la call:
`max(S_t - K e^{-rτ}, 0) <= C(σ) < S_t`

Interpretación práctica:
- si el mercado cotiza fuera de ese rango, hay error, fricción o una cotización inconsistente;
- dentro del rango, la inversa existe y es única.

## 3) Cómo resolver numéricamente
Hay dos métodos principales.

### A) Bisection
Ventajas:
- muy robusto;
- no necesita derivadas;
- converge si hay cambio de signo.

Desventajas:
- más lento.

Útil cuando:
- quieres seguridad;
- el mercado está raro;
- no confías en el punto inicial.

### B) Newton-Raphson
Iteración:
`σ_{n+1} = σ_n - F(σ_n)/F'(σ_n)`

donde:
`F(σ) = C_BS(σ) - C_mkt`

Ventajas:
- converge muy rápido cerca de la solución;
- ideal para producción.

Desventajas:
- depende del initial guess;
- puede fallar si el punto inicial es malo.

## 4) Initial guess recomendado
La presentación sugiere un inicio basado en la convexidad del precio:
`σ0 = sqrt( 2 | ln(S_t/K) + rτ | / τ )`

Uso práctico:
- sirve como arranque razonable para Newton;
- reduce riesgo de divergir;
- acelera la convergencia.

## 5) Qué te da la implied vol
La implied vol no es “la volatilidad real”; es la volatilidad que hace cuadrar BS con el mercado.

Eso significa:
- captura expectativas del mercado;
- absorbe skew, kurtosis y fricciones;
- resume el pricing cross-section.

## 6) Superficie de volatilidad
En la práctica, `σ_impl` cambia:
- por strike → **smile / skew**
- por vencimiento → **term structure**

Conclusión:
- BS con vol constante no explica bien los datos;
- la superficie de vol es una señal de que el mercado tiene colas gordas, clustering y/o jumps.

## 7) Deficiencias del modelo Black-Scholes
Supuestos que fallan en la realidad:
- trading continuo vs rehedging discreto;
- sin transaction costs;
- retornos normales;
- volatilidad constante.

Modelos alternativos:
- `σ(t)` term structure;
- `σ(S, t)` local vol;
- stochastic vol;
- jumps.

## 8) Qué implementar
### Función de implied vol
Inputs:
- `S, K, r, τ, market_price, call/put`

Outputs:
- `σ_impl`
- precio BS a esa σ
- error final
- número de iteraciones
- flag de convergencia

### Recomendación práctica
1. validar bounds de precio;
2. probar Newton con buen initial guess;
3. fallback a bisection si Newton falla;
4. cachear resultados por strike/vencimiento;
5. construir la surface por interpolación suave.

## 9) Uso en trading
La implied vol sirve para:
- rankear opciones baratas/caras;
- comparar strikes y vencimientos;
- detectar skew extremo;
- monitorizar cambios de régimen;
- decidir si hacer market making, delta-hedging o relative value.

## 10) Resumen para un agente
- Implied vol = inversión de BS.
- Vega positiva ⇒ solución única.
- Newton es rápido; bisection es seguro.
- La superficie de vol es más informativa que una sola σ.
- Si BS falla mucho, el problema no es numérico: es de modelo.

