# Adapters — Multi-AI support

> Esta capa permite usar **HackingWebbyDM20911** desde otros hosts de IA además de Claude Code / Claude Desktop, **sin modificar la skill original**.

## Filosofía

El núcleo (`SKILL.md`, `references/`, `scripts/`, `assets/`) es **agnóstico**. Lo único que cambia entre hosts es el **archivo de entrada** que cada uno espera leer:

| Host | Archivo de entrada | Ubicación típica |
|------|-------------------|------------------|
| Claude Code / Claude Desktop | `SKILL.md` (raíz) | `~/.claude/skills/HackingWebbyDM20911/` |
| Gemini CLI | `GEMINI.md` + `gemini-extension.json` | `~/.gemini/extensions/HackingWebbyDM20911/` |
| Cursor | `.cursorrules` | Raíz del proyecto |
| Aider | `CONVENTIONS.md` | Raíz del proyecto |
| OpenAI Codex CLI / generic | `AGENTS.md` | Raíz del proyecto |

Todos los adapters apuntan al mismo contenido base. El comportamiento de la skill (boot con pregunta de metodología, pipeline ofensivo, generación de informes) es idéntico.

## Instalación automática

```bash
bash adapters/install.sh
```

El script detecta tu CLI de IA disponible y configura el adapter correcto. Si detecta varios, te pregunta cuál usar.

## Detección que hace el instalador

| Indicador | Host inferido |
|-----------|---------------|
| `command -v claude` | Claude Code |
| `command -v gemini` | Gemini CLI |
| `command -v cursor-agent` o `command -v cursor` | Cursor |
| `command -v aider` | Aider |
| `command -v codex` | OpenAI Codex CLI |
| `$ANTHROPIC_API_KEY` | Claude API user |
| `$GEMINI_API_KEY` o `$GOOGLE_API_KEY` | Gemini |
| `$OPENAI_API_KEY` | OpenAI |
| Ninguno | Cae al adapter `generic` (`AGENTS.md`) |

## Self-detection en runtime (limitada)

Cada adapter incluye al inicio de su entry-point una instrucción para que el modelo:

1. Identifique al primer mensaje qué host detecta (por sus capacidades, herramientas disponibles, etc.).
2. Persista esa identidad como memoria del proyecto si el host lo soporta.
3. Use la nomenclatura de tools del host (`Bash` en Claude, `run_shell_command` en Gemini, etc.).

La detección 100% confiable se hace en el **instalador**, no en runtime — el modelo en sí no expone su host de forma estandarizada.

## Manual override

Si quieres saltarte la detección y forzar un host:

```bash
bash adapters/install.sh --host gemini
bash adapters/install.sh --host cursor --project-dir /ruta/al/proyecto
bash adapters/install.sh --host aider --project-dir .
```

## Estructura

```
adapters/
├── README.md             # este archivo
├── install.sh            # instalador con auto-detección
├── gemini/
│   ├── GEMINI.md
│   └── gemini-extension.json
├── cursor/
│   └── .cursorrules
├── aider/
│   ├── CONVENTIONS.md
│   └── .aider.conf.yml
├── openai-codex/
│   └── AGENTS.md
└── generic/
    └── AGENTS.md         # fallback para cualquier host con system prompts
```

## Aviso de paridad

- **Claude Code / Claude Desktop** es el host de referencia donde toda la funcionalidad (Skill tool, MCPs, scripts en background) está garantizada.
- **Gemini CLI** soporta extensions con system prompts y tool calling (`run_shell_command`, `read_file`, etc.). El generador de informes Python funciona idéntico.
- **Cursor / Aider** principalmente como copilotos de chat — los scripts se ejecutan en terminal por el usuario, la skill guía paso a paso.
- En cualquier host: el script `scripts/generate_report.py` es agnóstico (Python puro), produce los mismos `.docx`/`.pdf`/`.pptx`/`.html`/`.md`/`.txt`.
