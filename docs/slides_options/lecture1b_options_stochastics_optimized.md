# Lecture 1B — Options, stochastic processes y fundamentos para trading

## Objetivo operativo
Esta presentación construye la base para trabajar con opciones y precios de activos como procesos aleatorios. Para un sistema de trading, lo importante es:
- identificar el payoff correcto;
- usar no-arbitraje para detectar precios inconsistentes;
- entender cuándo una estrategia de cobertura replica el payout;
- modelar retornos/precios con un proceso simple pero útil;
- usar **put-call parity**, **bounds** y **delta hedging** como señales de mercado.

## 1) Conceptos mínimos de opciones
Una opción da el derecho, no la obligación, de comprar o vender un subyacente a un strike antes o en una fecha dada. Los campos relevantes son:
- subyacente;
- strike `K`;
- vencimiento `T`;
- tipo: call / put;
- estilo: European / American / Bermudan;
- features: barrier, asian, etc.

### Payoffs al vencimiento
- Call europea: `max(S_T - K, 0)`
- Put europea: `max(K - S_T, 0)`

## 2) Qué mueve el precio de una opción
El precio depende sobre todo de:
- `S_t` (spot actual),
- `K`,
- `T - t` (tiempo restante),
- volatilidad esperada del subyacente.

Regla práctica:
- más tiempo ⇒ más valor temporal;
- más volatilidad ⇒ más valor de opción;
- opciones OTM tienen solo valor temporal; ITM tienen valor intrínseco + temporal.

## 3) Hedging y no-arbitraje
Idea central: un escritor de opciones puede **cubrir** su riesgo comprando `Δ` acciones para replicar el payoff en escenarios discretos.

En el ejemplo del curso, el hedge se construye imponiendo que el portfolio cubierto valga lo mismo en ambos estados (up/down). Eso fija:
- el ratio de cobertura `Δ`,
- el precio justo por replicación.

Mensaje clave:
- si la cobertura es perfecta, el precio “justo” no deja beneficio esperado extra;
- el escritor gana por spread/fees o por hedges imperfectos, no por magia.

### Implicación para trading
Busca:
- opciones mal cotizadas vs precio replicable;
- violaciones de parity;
- oportunidades donde el hedge discreto sea barato o imposible por liquidez.

## 4) Put-call parity
Para opciones europeas con mismo `K` y `T`:

`C(t) + K e^{-r(T-t)} = P(t) + S(t)`

Interpretación:
- call + cash replican put + stock;
- si no se cumple, hay arbitraje teórico o fricciones de mercado.

### Bounds útiles
Para calls europeas:
- `C(t) >= max(S_t - K e^{-r(T-t)}, 0)`
- `C(t) <= S_t`

Esto sirve como filtro rápido de sanity-check para cotizaciones.

## 5) Randomness de precios y procesos estocásticos
Los retornos diarios se parecen a ruido, así que el modelo natural es probabilístico.

### Proceso estocástico
`X(t)` es una familia de variables aleatorias indexadas por tiempo.

### Wiener / Brownian motion
Propiedades:
- `W(0) = 0`
- incrementos independientes y estacionarios
- `W(t) ~ N(0, t)`
- trayectorias continuas

### Modelos básicos
- **ABM**: `dX = μ dt + σ dW`
- **GBM**: `dS = μ S dt + σ S dW`
- **OU**: `dX = κ(θ - X) dt + σ dW`

Lectura práctica:
- ABM: útil para variables que pueden cruzar cero;
- GBM: modelo base para precios positivos;
- OU: útil para mean reversion.

## 6) Samuelson / GBM para precios
Modelo base:
`dS(t) = μ S(t) dt + σ S(t) dW(t)`

Interpretación:
- `μ` = drift determinista;
- `σ dW` = ruido;
- el proceso es Markov: el futuro depende del presente, no de todo el pasado.

En discreto:
`S_{t+Δt} ≈ S_t + μ S_t Δt + σ S_t (W_{t+Δt} - W_t)`

### Retornos
Usa log-retornos para modelar:
`r_t = log(S_{t+1} / S_t)`

En datos reales:
- la distribución suele tener colas gordas;
- el supuesto normal es una aproximación, no una verdad absoluta.

## 7) EMH (hipótesis de mercado eficiente)
La versión débil dice que el precio actual ya incorpora la historia pasada. Para trading, esto significa:
- el historial de precios puro suele tener poca señal predictiva;
- necesitas microestructura, flujos, o desalineaciones con el modelo.

## 8) Ito’s Lemma
Si:
`dX = μ dt + σ dW`
y `Y = g(t, X)`, entonces:

`dY = (g_t + μ g_x + 1/2 σ^2 g_xx) dt + σ g_x dW`

Esto es la herramienta que permite pasar de una dinámica de precio a la dinámica de una función del precio, como `log(S)` o el precio de una opción.

### Ejemplo útil
Si `dS = μS dt + σS dW`, entonces:
`d(log S) = (μ - σ^2/2) dt + σ dW`

## 9) Qué debe implementar un agente
Prioridad de implementación:
1. leer precios spot, strikes y vencimientos;
2. calcular payoff teórico;
3. aplicar put-call parity y bounds;
4. modelar `S` con GBM como baseline;
5. usar `log-return` stats para detectar régimen;
6. si hay opciones, estimar si el precio implícito es razonable vs modelo.

## 10) Checklist de uso rápido
- ¿La opción es call o put?
- ¿Es europea o americana?
- ¿Está ITM / ATM / OTM?
- ¿Cumple parity?
- ¿Está dentro de los bounds?
- ¿Hay suficiente volatilidad/tiempo para que el valor temporal sea relevante?
- ¿GBM es una aproximación aceptable o hay mean reversion / saltos?

