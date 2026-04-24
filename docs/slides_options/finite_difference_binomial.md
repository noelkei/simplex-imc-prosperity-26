# Guía de Implementación: Diferencias Finitas y Método Binomial

Extracción exhaustiva de la "Lecture 10: Finite Difference Methods for Option Pricing" (5-FiniteDifference.pdf), orientada a que un sistema agente pueda codificar valoradores numéricos en Python.

## 1. El Método Binomial (Binomial Tree)
Es un modelo en tiempo discreto asumiendo una dinámica tipo Movimiento Browniano Geométrico (GBM). Se modela el precio del activo mediante un árbol recombinante.

### Parámetros de Calibración de Cox-Ross-Rubinstein (CRR)
Dada la volatilidad $\sigma$ y el número de pasos de tiempo $M$ hasta la madurez $T$, el paso de tiempo es $\delta t = T/M$.
* **Movimiento al alza ($u$):** $u = e^{\sigma\sqrt{\delta t}}$
* **Movimiento a la baja ($d$):** $d = e^{-\sigma\sqrt{\delta t}}$ (note que $u \cdot d = 1$, asegurando que el árbol sea recombinante).
* **Probabilidad Neutral al Riesgo ($p$):**
    $p = \frac{e^{r\delta t} - d}{u - d}$

### Implementación del Agente (Inducción Hacia Atrás)
1.  **Inicialización:** En el vencimiento $i = M$, calcular el payoff en todos los nodos posibles $S_n^M = S_0 u^n d^{M-n}$.
    $V_n^M = \max(S_n^M - K, 0)$
2.  **Inducción Hacia Atrás (Backward Recursion):** Iterar desde $i = M-1$ hasta $0$:
    $V_n^i = e^{-r\delta t} \left( p V_{n+1}^{i+1} + (1-p) V_n^{i+1} \right)$
    *(Si es una opción Americana, insertar una condición en este bucle: $V_n^i = \max(\text{Valor de Ejercicio Temprano}, V_n^i)$)*

## 2. Métodos de Diferencias Finitas (PDE de Black-Scholes)
La Ecuación Diferencial Parcial de Black-Scholes:
$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + rS \frac{\partial V}{\partial S} - rV = 0$

### 2.1 Transformación de Dominio
Para estabilizar los esquemas numéricos, el agente debe transformar $X = \ln(S)$ e invertir el tiempo $\tau = T - t$.
La nueva PDE parabólica es:
$\frac{\partial W}{\partial \tau} = \frac{1}{2}\sigma^2 \frac{\partial^2 W}{\partial X^2} + (r - \frac{1}{2}\sigma^2) \frac{\partial W}{\partial X}$
(con variables auxiliares adicionales explicadas en las slides).

### 2.2 Esquemas Numéricos
Se define una malla bidimensional espaciada por h (precio) y k (tiempo):
1.  **Esquema Explícito (FTCS):**
    Avanza en el tiempo utilizando solo los valores del nivel de tiempo anterior. Es fácil de programar, pero condicionalmente inestable (limitaciones estrictas de tamaño de paso $k / h^2$).
2.  **Esquema Implícito (BTCS):**
    Incondicionalmente estable, pero requiere resolver un sistema de ecuaciones tridiagonal en cada paso de tiempo.
    $\mathbf{A} V^{n+1} = V^n$
3.  **Esquema Crank-Nicolson:**
    Promedio entre el explícito y el implícito. Converge más rápido en el dominio temporal $O(k^2 + h^2)$ y es incondicionalmente estable. Se debe resolver el sistema:
    $\mathbf{M_1} V^{n+1} = \mathbf{M_2} V^n$

### Notas para Programación en Python
* Para resolver sistemas tridiagonales (Implícito o Crank-Nicolson), el agente **no debe usar la inversión estándar de matrices** (`np.linalg.inv`). Debe utilizar el algoritmo de Thomas o el *solver* de banda de Scipy (`scipy.linalg.solve_banded`) para obtener una complejidad computacional óptima $O(N_{espacio})$.
* Se deben definir condiciones de frontera claras para $X_{min}$ (ej. $V \approx 0$ para call) y $X_{max}$ (ej. $V \approx e^X - K e^{-r\tau}$ para call).
