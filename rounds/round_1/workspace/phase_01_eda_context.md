# Phase 01 EDA Context

## Status

COMPLETED

## Current Notes

- EDA completada el 2026-04-16 sobre 6 CSV (3 prices, 3 trades), días −2, −1, 0.
- **IPR**: drift lineal perfecta, slope=0.001/timestamp, R²=0.9999, residual std≈2. FV(t) = day_start + 0.001×t.
- **ACO**: FV fijo ≈10000. 94.4% del mid_price dentro de ±10. Trade price median = 10000 exacto.
- Spread: IPR≈13, ACO≈16.
- Caveats: zeros de mid_price (~0.3%) y book de un solo lado (~12%) deben manejarse en implementación.
- "Patrón oculto" de ACO no evidenciado en datos — tratarlo como FV=10000 hasta observar desvío.

## Next Action

Aprobado. Iniciar Fase 02 Understanding.
