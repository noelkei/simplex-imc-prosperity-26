# Prosperity Agent Playbook

Este documento complementa la documentación oficial de Prosperity (`docs/prosperity_wiki_raw/`) y está diseñado para ayudar a agentes de código (Codex, Claude) a desarrollar estrategias efectivas de trading.

Nota de autoridad: usa `docs/prosperity_wiki_raw/` y la wiki curada en `docs/prosperity_wiki/` para hechos del juego. No uses `bots/` ni `performances/` como fuente de verdad.

---

# 🎯 Objetivo del sistema

El objetivo es maximizar el PnL (profit and loss) en XIRECs mediante:
- trading algorítmico (principal)
- trading manual (secundario)

El algoritmo:
- interactúa con un order book simulado
- compite contra bots (NO contra otros jugadores)
- se ejecuta en iteraciones discretas

---

# 🧠 Modelo mental correcto

## ❌ Lo que NO es
- no es predicción pura de precios
- no es ML-heavy por defecto
- no es un mercado real con latencia

## ✅ Lo que SÍ es
- un entorno de market making + arbitrage + heurísticas
- un sistema determinista con señales limitadas
- una simulación donde el control de inventario es clave

---

# ⚙️ Estructura recomendada del bot

Separar claramente:

## 1. Fair Value
- estimación del valor "justo" del producto
- puede ser:
  - constante (productos estables)
  - media móvil
  - modelo simple

## 2. Strategy
- decide:
  - cuándo comprar
  - cuándo vender
- ejemplos:
  - market making
  - mean reversion
  - arbitrage

## 3. Risk / Inventory
- controla posición
- evita:
  - acumular demasiado inventario
  - romper límites

## 4. Execution
- decide:
  - precios de órdenes
  - cantidades
- interactúa con order_depth

---

# 📊 Principios clave de trading

## 1. Position limits
- restricción dura del sistema
- si se supera → TODAS las órdenes se cancelan
- SIEMPRE validar antes de enviar órdenes

## 2. Inventory management
- tener inventario alto = riesgo
- estrategias deben:
  - reducir posición
  - balancear buy/sell

## 3. Spread capture
- beneficio típico:
  - comprar barato
  - vender caro
- no necesitas predecir mercado → solo capturar spread

## 4. Order book reading
- mejores señales:
  - best bid
  - best ask
  - profundidad

---

# 🔁 Ciclo de decisión del bot

En cada iteración:

1. leer `TradingState`
2. calcular fair value por producto
3. analizar order book
4. decidir órdenes
5. validar límites de posición
6. devolver órdenes

---

# ⚠️ Errores comunes

## ❌ Ignorar position limits
→ provoca cancelación completa de órdenes

## ❌ No gestionar inventario
→ acumulas riesgo → pérdidas

## ❌ Overfitting al sample data
→ el día real será distinto

## ❌ Estrategias demasiado complejas
→ timeout (900ms) o bugs

## ❌ No usar logs
→ no puedes debuggear

---

# 🧪 Estrategia mínima recomendada

Para empezar:

## Productos estables
- usar fair value fijo
- hacer market making:
  - buy ligeramente por debajo
  - sell ligeramente por encima

## Productos volátiles
- usar media móvil o heurística simple
- detectar patrones básicos

---

# 🧰 Uso de herramientas del sistema

## Logs
- contienen:
  - output de print
  - trades ejecutados
- clave para debug

## Sample data
- usar para:
  - entender dinámica de precios
  - probar estrategias

## traderData
- permite persistencia entre iteraciones
- usar con cuidado (limitado a 50k chars)

---

# 🧠 Prioridades del agente

Al desarrollar código:

1. ✅ Correctitud (no romper reglas)
2. ✅ Cumplir position limits
3. ✅ Generar órdenes válidas
4. ✅ Simplicidad
5. ❌ Optimización prematura

---

# 🧩 Cómo mejorar iterativamente

1. implementar bot simple
2. probar en sample data
3. analizar logs
4. ajustar lógica
5. repetir

---

# 🔗 Relación con otros documentos

- API → [../prosperity_wiki/api/01_trader_contract.md](../prosperity_wiki/api/01_trader_contract.md)
- datamodel → [../prosperity_wiki/api/02_datamodel_reference.md](../prosperity_wiki/api/02_datamodel_reference.md)
- reglas → [../prosperity_wiki/trading/02_orders_and_position_limits.md](../prosperity_wiki/trading/02_orders_and_position_limits.md), [../prosperity_wiki/appendix/competition_context.md](../prosperity_wiki/appendix/competition_context.md)
- rondas → [../prosperity_wiki/rounds/tutorial.md](../prosperity_wiki/rounds/tutorial.md), [../prosperity_wiki/rounds/round_1.md](../prosperity_wiki/rounds/round_1.md)

---

# 🧠 Nota final

El objetivo no es encontrar "la estrategia perfecta", sino:

→ construir un sistema robusto  
→ iterar rápido  
→ evitar errores críticos  
→ capturar oportunidades simples de forma consistente
