# Guía de Implementación: El Método COS (Paper de Fang & Oosterlee)

Documento analítico detallado basado en el paper "A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions". Está adaptado para ser consumido por un LLM en tareas de codificación para el algoritmo de pricing.

## 1. Idea Principal del Método COS
El método COS es una técnica de integración numérica que reemplaza la función de densidad de probabilidad (PDF) del activo subyacente con su **expansión en series de Fourier-Coseno**. La clave reside en que los coeficientes de esta expansión están estrechamente relacionados con la **Función Característica (ChF)** del proceso, la cual suele ser conocida de forma analítica para modelos complejos (como Lévy y Heston).

## 2. Derivación Matemática y Fórmula de Pricing
El precio de una opción europea se obtiene tomando la esperanza bajo la medida neutral al riesgo.
$V(x, t_0) = e^{-r\Delta t} \mathbb{E}^{\mathbb{Q}}[V(y, T) | x]$

Donde $x$ es el log-precio inicial y $y$ es el log-precio en madurez $T$.
1. **Truncamiento del dominio:** La integral infinita de la esperanza se aproxima truncando el soporte de la densidad al intervalo $[a, b]$.
2. **Expansión:**
   $f(y|x) \approx \sum_{k=0}^{N-1} \sideset{|}{'}\sum F_k(x) \cos\left( k\pi \frac{y-a}{b-a} \right)$
   El símbolo $\sideset{|}{'}\sum$ indica que el primer término (k=0) se multiplica por $1/2$.
3. **Coeficientes a partir de la ChF:**
   $F_k(x) = \frac{2}{b-a} \Re \left\{ \phi\left(\frac{k\pi}{b-a}; x\right) e^{-i k \pi \frac{a}{b-a}} \right\}$
   $\phi(\omega; x)$ es la función característica del estado $y$ condicionada a $x$.
4. **Fórmula final del Método COS:**
   $V(x, t_0) \approx e^{-r\Delta t} \sum_{k=0}^{N-1} \sideset{|}{'}\sum \Re \left\{ \phi\left(\frac{k\pi}{b-a}; x\right) e^{-i k \pi \frac{a}{b-a}} \right\} V_k$
   Donde $V_k$ son los coeficientes de la expansión en coseno de la **función de pago (payoff)**.

## 3. Coeficientes de Payoff ($V_k$)
Para opciones Plain Vanilla, las integrales de los coeficientes $V_k$ tienen solución analítica, lo que confiere al método una complejidad computacional lineal $O(N)$.
* **Call Option** (pago $\max(K(e^y - 1), 0)$):
    Requiere el cálculo de integrales del tipo $\chi_k(c,d)$ y $\psi_k(c,d)$, que son integrales conocidas de funciones trigonométricas y exponenciales.

## 4. Convergencia
El método exhibe una **convergencia exponencial** para funciones de densidad suaves (como en el modelo de Black-Scholes y Heston). Se requiere un $N$ pequeño (e.g., $N=128$ o $N=256$) para alcanzar precisiones de $10^{-6}$.

### Notas de Implementación (Python/Codex)
* **Cálculo Vectorizado:** Es vital pre-calcular el vector $\omega_k = \frac{k\pi}{b-a}$ y utilizar aritmética de arrays (`numpy.exp`, `numpy.cos`) para calcular todos los sumandos en un solo paso matricial, eliminando bucles `for`.
* **Elección de [a, b]:** Se define en función de los cumulantes del log-retorno $y$. Generalmente $a = c_1 - L \sqrt{c_2 + \sqrt{c_4}}$ y $b = c_1 + L \sqrt{c_2 + \sqrt{c_4}}$ con $L = 10$.
