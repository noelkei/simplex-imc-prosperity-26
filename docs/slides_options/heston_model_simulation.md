# Guía de Implementación: Modelo de Volatilidad Estocástica de Heston y Simulación

Este documento está optimizado para sistemas de agentes (como Claude o Codex) enfocados en el trading algorítmico, específicamente para extraer e implementar las matemáticas y simulaciones del Modelo de Heston detalladas en la "Lecture 7".

## 1. Definición del Modelo de Heston
El modelo de Heston asume que el precio del activo subyacente $S_t$ y su varianza $\nu_t$ siguen un proceso de difusión bidimensional:
- $dS_t = r S_t dt + \sqrt{\nu_t} S_t dW_t^S$
- $d\nu_t = \kappa(\bar{\nu} - \nu_t)dt + \gamma \sqrt{\nu_t} dW_t^\nu$

### Parámetros:
* **$r$**: Tasa de interés libre de riesgo.
* **$\bar{\nu}$**: Reversión a la media (long-run mean) de la varianza.
* **$\kappa$**: Velocidad de reversión a la media ($\kappa > 0$).
* **$\gamma$**: Volatilidad de la volatilidad (vol-of-vol, $\gamma > 0$).
* **$\rho$**: Correlación entre los movimientos brownianos $dW_t^S dW_t^\nu = \rho dt$.

### Condición de Feller
Para asegurar que la varianza $\nu_t$ sea estrictamente positiva, se debe cumplir la condición de Feller:
$2\kappa\bar{\nu} \geq \gamma^2$

## 2. Simulación de Monte Carlo (Discretización de Euler)
Para la implementación de agentes en competiciones de trading (como IMC Prosperity), una simulación rápida es la discretización de Euler.

Dado un paso de tiempo $\Delta t$:
1. Generar variables normales estándar independientes $Z_1, Z_2 \sim N(0,1)$.
2. Correlacionar los choques: 
   $Z_S = Z_1$
   $Z_\nu = \rho Z_1 + \sqrt{1 - \rho^2} Z_2$
3. Actualizar la varianza (usando un esquema de truncamiento o reflexión para evitar valores negativos debido al error de discretización, por ejemplo, Full Truncation):
   $\nu_{t+\Delta t} = \nu_t + \kappa(\bar{\nu} - \nu_t^+)\Delta t + \gamma \sqrt{\nu_t^+} \sqrt{\Delta t} Z_\nu$
   donde $\nu_t^+ = \max(\nu_t, 0)$.
4. Actualizar el log-precio $X_t = \ln(S_t)$:
   $X_{t+\Delta t} = X_t + (r - \frac{1}{2}\nu_t^+)\Delta t + \sqrt{\nu_t^+} \sqrt{\Delta t} Z_S$

## 3. Simulación Exacta (Esquema de Broadie-Kaya)
Para mayor precisión y evitar errores de discretización en pasos de tiempo grandes:
1. Simular la varianza $\nu_{t+\Delta t}$ condicionada a $\nu_t$ a partir de una distribución Chi-cuadrado no central (Non-central Chi-squared).
2. Simular la varianza integrada $\int_t^{t+\Delta t} \nu_s ds$ condicionada a $\nu_t$ y $\nu_{t+\Delta t}$ (esto es computacionalmente intensivo, se hace a través de la transformada de Fourier o métodos de aceptación-rechazo).
3. Simular el precio final integrando los procesos, dado que, condicionado a la varianza y su integral, el precio es log-normal.

### Notas de Implementación para Agentes (Codex/Claude)
* **Eficiencia:** Para competiciones de trading de alta frecuencia, prefiera Euler con esquema *Full Truncation* (Lord et al., 2010) debido a su bajo costo computacional frente a la Simulación Exacta.
* **Generación de Variables Aleatorias:** Vectorice las operaciones con `numpy` para escalar la simulación a múltiples caminos de Monte Carlo simultáneos de forma matricial.
