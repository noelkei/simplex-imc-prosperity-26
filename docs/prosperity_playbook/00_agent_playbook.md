# Prosperity Agent Playbook

Este documento es una guia heuristica para agentes que trabajan en este repo.
No es fuente oficial de reglas de Prosperity.

Para hechos del juego, API, datamodel, limites, runtime, flujo de plataforma,
productos de ronda y caveats, usa primero la wiki curada:
[`../prosperity_wiki/`](../prosperity_wiki/). La wiki cita
`docs/prosperity_wiki_raw/` como base factual, pero el punto de entrada de
trabajo en este repo es la wiki curada y los workflows.

## Modelo de autoridad

- Wiki: hechos oficiales y caveats.
- Workflows: como trabajar, validar, documentar y hacer handoffs.
- Playbook: heuristicas de estrategia, riesgo, debugging e iteracion.
- `AGENTS.md`: reglas locales de lectura, jerarquia de fuentes y seguridad.
- Skills de Codex: herramientas/procesos auxiliares cuando apliquen, no fuentes
  de reglas de Prosperity.
- `rounds/round_X/bots/` y `rounds/round_X/performances/`: artefactos
  locales; no son autoridad para reglas, limites, productos, API ni runtime.
- `non-canonical/`: borradores personales fuera del workflow formal; no son
  evidencia ni ejemplos salvo que el usuario apunte explicitamente a un archivo.

Si falta un hecho, esta ambiguo o contradice otra fuente, registra un caveat y
cita la fuente. No lo rellenes con memoria, intuicion, datos de sample o codigo
local.

## Orden de lectura recomendado

Antes de implementar, validar o documentar comportamiento oficial, lee:

1. [`../prosperity_wiki/README.md`](../prosperity_wiki/README.md)
2. [`../prosperity_wiki/api/01_trader_contract.md`](../prosperity_wiki/api/01_trader_contract.md)
3. [`../prosperity_wiki/api/02_datamodel_reference.md`](../prosperity_wiki/api/02_datamodel_reference.md)
4. [`../prosperity_wiki/api/03_runtime_and_resources.md`](../prosperity_wiki/api/03_runtime_and_resources.md)
5. [`../prosperity_wiki/trading/01_exchange_mechanics.md`](../prosperity_wiki/trading/01_exchange_mechanics.md)
6. [`../prosperity_wiki/trading/02_orders_and_position_limits.md`](../prosperity_wiki/trading/02_orders_and_position_limits.md)
7. El documento de ronda activa bajo [`../prosperity_wiki/rounds/`](../prosperity_wiki/rounds/). Si no existe una ronda mas nueva publicada, usa [`../prosperity_wiki/rounds/round_1.md`](../prosperity_wiki/rounds/round_1.md).
8. [`../prosperity_workflows/README.md`](../prosperity_workflows/README.md) y el workflow especifico de la tarea.
9. Este playbook, solo para juicio heuristico despues de conocer los hechos.

## Contrato minimo del bot

Hechos a verificar contra la wiki antes de tocar una implementacion:

- Implementar `Trader.run(state)`.
- Devolver `result, conversions, traderData`.
- `result` mapea simbolos/productos a listas de `Order`.
- En `Order`, `quantity > 0` compra y `quantity < 0` vende.
- En `OrderDepth`, `buy_orders` usa volumen positivo y `sell_orders` volumen
  negativo.
- Comprar aumenta la posicion; vender la reduce; una posicion negativa es short.
- `traderData` es string y es la ruta segura de persistencia entre llamadas.
- No confiar en globales o variables de clase para estado persistente.
- No cambiar la interfaz `Trader` salvo que la wiki de ronda lo requiera. El
  metodo `bid()` es especifico de Round 2 segun la wiki; no lo conviertas en una
  dependencia general.
- `conversions` puede ser `0` o `None` cuando la estrategia no usa conversiones.
  No inventes mecanicas de conversion si la ronda no las documenta.

Runtime y recursos:

- Cada llamada a `run()` debe responder dentro del limite documentado de `900ms`;
  la fuente recomienda promedio `<= 100ms`.
- `traderData` se corta externamente a `50 000` caracteres.
- Usar librerias soportadas por la wiki: Python 3.12 standard library y las
  librerias listadas alli. No agregar dependencias externas no soportadas.
- Los logs incluyen `print()` dentro de `run()`, pero el logging tambien consume
  presupuesto y espacio de salida.

## Modelo mental operativo

Segun la wiki, el algoritmo opera en la exchange de Prosperity contra bots de
Prosperity. Los algoritmos de distintos equipos corren por separado y no operan
entre si.

Implicaciones heuristicas:

- El objetivo global es generar PnL en XIRECs, pero no toda contribucion tiene
  que ser codigo de bot; EDA, validacion, documentacion y handoffs tambien
  reducen incertidumbre.
- Una orden que cruza el libro ejecuta contra la mejor contraparte disponible
  segun matching y prioridad precio-tiempo.
- Una orden no ejecutada puede descansar durante la iteracion, quedar visible
  para bots y cancelarse al final de la iteracion.
- El control de inventario y la validez de ordenes importan mas que una senal
  brillante pero fragil.

## Ronda activa y productos

No hardcodees productos, limites ni mecanicas manuales fuera del documento de
ronda activa.

Con los documentos publicados actualmente en `rounds/`, Round 1 define:

- Productos algoritmicos: `ASH_COATED_OSMIUM` e `INTARIAN_PEPPER_ROOT`.
- Limite de posicion: `80` para cada uno.
- Pistas de producto: `INTARIAN_PEPPER_ROOT` se describe como bastante estable;
  `ASH_COATED_OSMIUM` se describe como mas volatil y posiblemente con patron
  oculto.
- Productos manuales: `DRYLAND_FLAX` y `EMBER_MUSHROOM`; sus mecanicas no deben
  contaminar la implementacion algoritmica.

Estas pistas son hechos de ronda, no estrategias completas. Convertirlas en una
estrategia requiere una hipotesis etiquetada, evidencia o un plan de prueba.

## Marco heuristico de estrategia

Una estrategia facil de revisar suele separar cuatro piezas:

- Fair value o senal: como estima el valor justo o el sesgo esperado.
- Decision: cuando compra, vende, descansa ordenes o no hace nada.
- Riesgo e inventario: como evita acumulacion peligrosa y rechazo por limites.
- Ejecucion: precios y tamanos de orden, considerando el `order_depth`.

Patrones utiles, siempre como heuristicas:

- Market making cuando hay un valor razonablemente estable o un spread
  explotable.
- Mean reversion cuando la evidencia sugiere desviaciones temporales.
- Senales simples y falsables antes de modelos complejos.
- Skew de inventario: volverse mas agresivo vendiendo cuando la posicion es
  larga, y mas agresivo comprando cuando la posicion es corta.
- Dejar de operar o reducir tamano cuando el libro esta vacio, la senal falta o
  la posicion esta cerca del limite.

No hay una estrategia unica correcta. Prefiere cambios pequenos, parametros
explicables y una forma clara de falsar la idea.

## Guardrails de riesgo

Antes de devolver ordenes, valida capacidad agregada por producto:

- Capacidad de compra: `limit - current_position`.
- Capacidad de venta en valor absoluto: `limit + current_position`.
- La suma de cantidades de compra de una iteracion no debe exceder la capacidad
  de compra.
- La suma absoluta de cantidades de venta de una iteracion no debe exceder la
  capacidad de venta.

La exchange rechaza/cancela ordenes si la cantidad agregada podria romper el
limite de posicion. Por eso no basta con validar cada orden aislada.

Tambien recuerda:

- Las ordenes que no ejecutan inmediatamente pueden descansar durante la
  iteracion y ser visibles para bots.
- Si no se ejecutan, se cancelan al final de la iteracion.
- La prioridad es precio-tiempo.
- Las ordenes manuales y el reto manual se tratan aparte del bot.

## Uso de datos, logs y EDA

Los sample data y logs sirven para generar evidencia, no para definir reglas
oficiales.

Buenas practicas:

- Nombrar el archivo, dia, run o log usado.
- Separar observacion de interpretacion.
- No afirmar que un patron seguira en el dia real solo porque aparece en un
  sample.
- Usar EDA para responder preguntas concretas: estabilidad de precio, spread,
  volumen disponible, fill behavior, PnL por componente o errores de limite.
- Guardar la conclusion como evidencia y proponer el siguiente workstream:
  estrategia, implementacion, validacion o mas EDA.

## Workflows de trabajo

Usa el workflow que corresponde a la tarea:

- EDA: [`../prosperity_workflows/03_workstream_eda.md`](../prosperity_workflows/03_workstream_eda.md)
- Estrategia: [`../prosperity_workflows/04_workstream_strategy.md`](../prosperity_workflows/04_workstream_strategy.md)
- Implementacion: [`../prosperity_workflows/05_workstream_bot_implementation.md`](../prosperity_workflows/05_workstream_bot_implementation.md)
- Debugging y validacion: [`../prosperity_workflows/06_workstream_debugging_and_validation.md`](../prosperity_workflows/06_workstream_debugging_and_validation.md)
- Preparacion de ronda: [`../prosperity_workflows/07_workstream_round_preparation.md`](../prosperity_workflows/07_workstream_round_preparation.md)
- Handoffs y docs: [`../prosperity_workflows/08_handoffs_and_documentation.md`](../prosperity_workflows/08_handoffs_and_documentation.md)
- Cambios seguros: [`../prosperity_workflows/09_safe_change_rules.md`](../prosperity_workflows/09_safe_change_rules.md)

Un buen handoff dice:

- Que cambio o que se aprendio.
- Que fuentes de wiki se usaron.
- Que heuristicas del playbook se usaron.
- Que datos, logs, comandos o archivos dan evidencia.
- Que supuestos siguen sin resolver.
- Cual es la siguiente accion concreta.

Para tareas de submission o plataforma, vuelve a la wiki de plataforma: los
equipos pueden subir varios programas, pero el resultado de ronda se calcula con
el algoritmo activo/final procesado segun la UI. Las entregas manuales son
separadas del algoritmo.

## Uso de Skills de Codex

Si una tarea menciona un Skill o encaja claramente con uno disponible:

- Lee primero su `SKILL.md`.
- Usa solo las partes necesarias para la tarea.
- Tratalo como una ayuda de proceso o herramienta, no como fuente de hechos de
  Prosperity.
- Si una instruccion del Skill choca con `AGENTS.md`, la wiki o los workflows de
  este repo, sigue las fuentes del repo y deja un caveat breve.
- Si no hay un Skill aplicable, no fuerces su uso.

## Errores comunes

- Usar artefactos round-locales de bots o performances para deducir reglas oficiales.
- Usar `non-canonical/` como evidencia formal o implementacion de referencia.
- Reutilizar productos o limites de otra ronda.
- Mezclar mecanicas manuales en el algoritmo.
- Validar ordenes individualmente en vez de validar cantidades agregadas.
- Guardar estado critico en globales en vez de `traderData`.
- Superar el presupuesto de runtime con modelos, imports o logs innecesarios.
- Convertir hints de producto o sample-data observations en reglas.
- Ocultar parametros magicos sin explicar su razon o como se validaran.

## Checklist antes de entregar

- Fuentes factuales revisadas y enlazadas.
- `Trader.run(state)` y retorno `result, conversions, traderData` intactos.
- Simbolos, campos y signos alineados con la wiki.
- Limites de posicion validados por cantidad agregada.
- `traderData`, runtime e imports dentro de restricciones.
- Ronda activa y mecanicas manuales separadas.
- Supuestos etiquetados como heuristica, evidencia EDA o estrategia.
- Tests, logs o razon de no haberlos ejecutado documentados.
- Handoff con caveats y siguiente accion concreta.
