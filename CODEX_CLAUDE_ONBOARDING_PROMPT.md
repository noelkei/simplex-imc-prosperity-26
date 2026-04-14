# Codex / Claude Onboarding Prompt

Use this file when you open a fresh Codex or Claude session and want the agent to understand this repository before doing work.

Copy either the Spanish or English prompt below.

## Prompt En Español

```text
Quiero que actúes como guía experto de este repositorio de Prosperity.

Antes de responder o proponer trabajo, lee y usa la estructura real del repo. Empieza por:

1. README.md
2. AGENTS.md
3. docs/prosperity_wiki/README.md
4. docs/prosperity_workflows/README.md
5. rounds/README.md
6. Si estoy trabajando en una ronda concreta, lee también:
   - rounds/round_X/README.md
   - rounds/round_X/workspace/_index.md
   - el phase_*_context.md relevante

Respeta esta jerarquía:

- docs/prosperity_wiki/ = fuente factual operativa
- docs/prosperity_wiki_raw/ = base factual bruta
- docs/prosperity_playbook/ = heurísticas, no reglas oficiales
- docs/prosperity_workflows/ = proceso y handoffs
- docs/templates/ = plantillas reutilizables
- rounds/ = trabajo formal de cada ronda
- non-canonical/ = borradores personales informales, no evidencia ni fuente de verdad

No inventes reglas de Prosperity, productos, límites, mecánicas, APIs ni estrategias. No uses bots, performances ni non-canonical como fuente de verdad. Si algo falta o está ambiguo, dilo como caveat o blocker.

Quiero que me expliques:

1. Cómo funciona este sistema de trabajo.
2. Qué tengo que saber para usarlo bien.
3. Qué carpetas son importantes y cuáles debo ignorar salvo que hagan falta.
4. Qué es autoritativo y qué no.
5. Cómo se empieza una ronda.
6. Cómo se continúa una fase.
7. Cómo se cierra una fase correctamente.
8. Cómo se usan _index.md y los phase_*_context.md.
9. Cómo colaboran humanos y agentes Codex/Claude en este repo.
10. En qué estado está ahora mismo el repo.
11. Qué tocaría hacer ahora mismo si quiero continuar de forma segura.
12. Qué blockers, riesgos o decisiones humanas hay, si los hay.

Si detectas que no hay una ronda activa, dilo claramente y explica cuál sería el siguiente paso para empezar una. Si detectas una ronda activa, resume su estado desde rounds/round_X/workspace/_index.md.

No modifiques archivos todavía. Primero dame un resumen operativo y una recomendación de siguiente acción.

Formato de respuesta:

## Resumen
Di en pocas líneas qué es este repo y cómo se usa.

## Estado Actual
Explica si hay una ronda activa, qué fases están empezadas o bloqueadas, y qué artefactos existen.

## Cómo Usarlo Bien
Lista las reglas prácticas más importantes para no romper el workflow.

## Qué Hacer Ahora
Da la siguiente acción recomendada, concreta y pequeña.

## Preguntas
Haz solo preguntas necesarias que cambien la dirección del trabajo, la prioridad, el riesgo o la decisión de submission.
```

## Prompt In English

```text
I want you to act as an expert guide for this Prosperity repository.

Before answering or proposing work, read and use the repository's actual structure. Start with:

1. README.md
2. AGENTS.md
3. docs/prosperity_wiki/README.md
4. docs/prosperity_workflows/README.md
5. rounds/README.md
6. If I am working on a specific round, also read:
   - rounds/round_X/README.md
   - rounds/round_X/workspace/_index.md
   - the relevant phase_*_context.md

Respect this hierarchy:

- docs/prosperity_wiki/ = operational factual source
- docs/prosperity_wiki_raw/ = raw factual base
- docs/prosperity_playbook/ = heuristics, not official rules
- docs/prosperity_workflows/ = process and handoffs
- docs/templates/ = reusable templates
- rounds/ = formal round work
- non-canonical/ = informal personal drafts, not evidence or source of truth

Do not invent Prosperity rules, products, limits, mechanics, APIs, or strategies. Do not use bots, performances, or non-canonical drafts as source of truth. If something is missing or ambiguous, state it as a caveat or blocker.

I want you to explain:

1. How this workflow system works.
2. What I need to know to use it properly.
3. Which folders matter and which ones should be ignored unless needed.
4. What is authoritative and what is not.
5. How to start a round.
6. How to continue a phase.
7. How to close a phase correctly.
8. How _index.md and phase_*_context.md are used.
9. How humans and Codex/Claude agents should collaborate in this repo.
10. What state the repository is in right now.
11. What should be done next if I want to continue safely.
12. What blockers, risks, or human decisions exist, if any.

If there is no active round, say so clearly and explain the next step to start one. If there is an active round, summarize its state from rounds/round_X/workspace/_index.md.

Do not modify files yet. First give me an operational summary and a recommended next action.

Response format:

## Summary
Briefly explain what this repo is and how it is used.

## Current State
Explain whether there is an active round, which phases are started or blocked, and which artifacts exist.

## How To Use It Well
List the most important practical rules for not breaking the workflow.

## What To Do Now
Give the next recommended action, concrete and small.

## Questions
Ask only necessary questions that would change direction, priority, risk, or submission decisions.
```
