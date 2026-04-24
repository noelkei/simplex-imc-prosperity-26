# Guía de Implementación: Métodos de Fourier para Pricing de Opciones

Este MD sintetiza las técnicas numéricas y computacionales detalladas en la "Lecture 6: Fourier methods for option pricing", focalizado en proveer contexto de codificación para LLMs.

## 1. Familia Fourier y Función Característica (ChF)
En finanzas computacionales, rara vez conocemos la función de densidad (PDF) analítica de los retornos bajo modelos complejos, pero sí conocemos su transformada de Fourier, la Función Característica (ChF):
$\phi(\omega) = \mathbb{E}[e^{i\omega X_T}]$

**Ejemplo Black-Scholes (GBM):**
Si $X_T = \ln(S_T)$, la dinámica bajo GBM arroja una ChF que corresponde a una distribución normal con media $X_0 + (r - \delta - \frac{1}{2}\sigma^2)T$ y varianza $\sigma^2 T$.

## 2. Aplicación Práctica: Pricing mediante el Método COS
El método COS aprovecha la dualidad de Fourier y las series de coseno discreto.
Pasos a programar por el agente:

### Paso 2.1: Definición de Rango de Truncamiento [a, b]
El dominio de integración debe capturar casi toda la masa de probabilidad. Se utilizan los *Cumulantes* ($c_n$):
* $c_1 = \text{Media}$
* $c_2 = \text{Varianza}$
* $c_4 = \text{Curtosis}$ (si es aplicable)

Fórmula general recomendada:
$a = c_1 - L \sqrt{c_2 + \sqrt{c_4}}$
$b = c_1 + L \sqrt{c_2 + \sqrt{c_4}}$
Donde $L$ (nivel de truncamiento) usualmente está entre 10 y 12.

### Paso 2.2: Generación de Coeficientes del Payoff
El payoff $\max(S_T - K, 0)$ en el espacio de los log-precios necesita expandirse:
$U_k = \frac{2}{b-a} \int_0^{b} \max(e^y - e^k, 0) \cos\left(k\pi\frac{y-a}{b-a}\right) dy$
Las slides establecen fórmulas directas para calcular esto sin integración numérica (basado en sumas algebraicas que combinan senos y exponenciales). El programador debe implementar las subrutinas $\chi_k$ y $\psi_k$.

### Paso 2.3: Sumatoria Discreta Lineal
$V(x,t) \approx e^{-r\Delta t} \sum_{k=0}^{N-1} \sideset{|}{'}\sum \Re \left\{ \phi\left(\frac{k\pi}{b-a}\right) e^{-i k\pi \frac{a}{b-a}} \right\} V_k$

### Ventajas Estratégicas para Competiciones:
1.  **Complejidad $O(N)$ vs FFT:** A diferencia del Fast Fourier Transform tradicional (Carr-Madan) que cuesta $O(N \log N)$, la sumatoria COS es directamente $O(N)$.
2.  **Múltiples Strikes:** Si cambias el parámetro del strike $K$, solo necesitas recalcular $V_k$, mientras que la evaluación de $\phi(\omega)$ (la parte computacionalmente más pesada) se reutiliza y se almacena en caché.
