# Autonomous Agents para Web Hacking

## Concepto

Múltiples agentes especializados coordinados por un orquestador. Cada uno es bueno en una fase. Comparten contexto vía bus / knowledge graph.

## Arquitectura

```
                  ┌─────────────────────┐
                  │   Orchestrator      │
                  │   (planifica, asigna)│
                  └─────────┬───────────┘
                            │
        ┌─────────┬─────────┼─────────┬──────────┐
        ▼         ▼         ▼         ▼          ▼
   Recon     JS Intel   API Agent  Exploit   Reporting
   Agent     Agent                 Agent     Agent
```

Cada agente:
- Tiene tools propios (Bash, MCPs específicos).
- Lee/escribe del context store compartido.
- Puede pedir ayuda a otro agente.

## Implementaciones posibles

### Claude Code subagents (más simple)
Usar `Agent` tool con `subagent_type` por especialidad. Coordinar desde main agent.

### LangGraph
DAG de nodos con state shared.

### CrewAI
Roles + tasks + processes.

### Custom (Python + asyncio)
Más control, menos abstracción.

## Recon Agent
- Tools: subfinder, amass, httpx, katana, dnsx
- Output: `recon_state.json` con hosts, endpoints, tech, ports

## JS Analysis Agent
- Tools: linkfinder, secretfinder, sourcemap parser, semgrep
- Output: nuevos endpoints, secrets, sinks

## API Agent
- Tools: Postman/Newman, schemathesis, jwt_tool, GraphQL introspection
- Output: endpoints + auth + parámetros + posibles BOLA candidatos

## Exploit Agent
- Tools: sqlmap, ffuf, dalfox, manual payload generation
- Acción: confirmar vuln con evidencia
- Output: findings con PoC reproducible

## Reporting Agent
- Input: findings consolidados
- Tools: generate_report.py
- Output: docx/pdf/md/html

## Coordination patterns

### Pipeline
Recon → JS → API → Exploit → Reporting (lineal).

### Hub & spoke
Orchestrator pide a cada uno y consolida.

### Event-driven
"Nuevo endpoint encontrado" → API Agent lo prueba.

## Riesgos

- Agentes con bash sin sandbox = potencial de ejecutar algo destructivo.
- Coordinación falla → loops infinitos.
- Token cost alto (cada agente lee contexto extenso).

Mitigaciones:
- Aislamiento por worktree para Claude Code.
- Quotas por agente (max iteraciones, max tools).
- Logging exhaustivo de cada decisión.

## Estado actual (2026)

- Frameworks como `nebula`, `xbow` (closed) demuestran agentes ofensivos competitivos.
- Open source: experimentos con Claude/GPT como reasoner + tools tradicionales.
- Camino más práctico hoy: Claude Code subagents + MCPs especializados.
