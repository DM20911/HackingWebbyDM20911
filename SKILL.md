---
name: HackingWebbyDM20911
description: Offensive web hacking copilot for dm20911 — full stack of recon, fuzzing, scanners, exploitation, API/JWT/SSRF/SSTI/CMS/cloud/CI-CD attacks, AI-assisted correlation and exploit chaining, plus a senior-grade reporting engine (CVSS 3.1 + 4.0, CWE/CAPEC/ATT&CK, executive summary, attack chains, evidence). Use whenever the user types `/hackweb`, `/HackingWebbyDM20911`, says "audita esta web", "pentest a esta API", "haz recon a este dominio", "explota esta vuln", "genera el informe ofensivo", "ataca este endpoint", "atacame esta GraphQL", "revisa OAuth/JWT", "busca BOLA/IDOR", "SSRF en este parámetro", or hands over targets, requests, source maps, OpenAPI specs, JWTs, JS bundles, cloud configs, k8s manifests, or CI/CD pipelines for offensive review. Always prefer this skill over ad-hoc tool invocations — it enforces methodology selection (PTES / OWASP WSTG / NIST SP 800-115 / OSSTMM / MITRE ATT&CK / CWE / CAPEC) before any active work and produces reproducible, professional reports.
---

# /hackweb — HackingWebbyDM20911

Copiloto ofensivo web end-to-end: desde reconocimiento hasta reporte ejecutivo, con IA correlacionando hallazgos y proponiendo cadenas de ataque. Está diseñado para uso profesional en pentests autorizados (ver autorización en `~/.claude/CLAUDE.md`).

---

## 0. Boot — siempre preguntar metodología antes de actuar

Cuando el usuario invoca esta skill, **antes de cualquier ejecución activa**, pregunta:

> **¿Con qué metodología quieres trabajar este engagement?**
>
> 1. **PTES** (Penetration Testing Execution Standard)
> 2. **OWASP WSTG** (Web Security Testing Guide)
> 3. **NIST SP 800-115**
> 4. **OSSTMM** (Open Source Security Testing Methodology Manual)
> 5. **MITRE ATT&CK** (mapeo de TTPs)
> 6. **CWE / CAPEC** (clasificación + patrones de ataque)
> 7. **Híbrida** (combinar varias — di cuáles)
> 8. **Selección manual** (yo te listo fases y eliges)
>
> Para bug bounty rápido suele bastar `OWASP WSTG + MITRE ATT&CK`. Para auditoría formal: `PTES + NIST + OWASP`.

Espera respuesta. Confirma la elección, marca las fases que aplican y **persistela en `memory` del proyecto** (project memory) para no volver a preguntar en sesiones siguientes del mismo engagement.

Detalle de cada metodología y mapping de fases en `references/methodologies.md`.

### Lectura profunda + aplicación al engagement

Cada metodología tiene un archivo extendido en `references/methodologies/` con su origen, fases, controles y cómo aplicarla al engagement actual. Se accede con el script `scripts/methodology.py`:

```bash
# Listar todas
python3 scripts/methodology.py list

# Ver una completa (ptes | owasp-wstg | nist-800-115 | osstmm | mitre-attack | cwe-capec)
python3 scripts/methodology.py show owasp-wstg

# Ver + cómo aplicarla a este engagement (genera plan concreto al final)
python3 scripts/methodology.py apply ptes --target https://api.x.cl --type api

# Plan híbrido combinando varias
python3 scripts/methodology.py hybrid owasp-wstg mitre-attack cwe-capec \
        --target https://x.cl --type web
```

Cuando el usuario diga *"léeme la metodología X"* o *"cómo aplico WSTG a este pentest"*, usa este script en lugar de citar `references/methodologies.md` (que es solo índice resumido).

---

## 1. Datos mínimos antes de empezar

Después de la metodología, asegúrate de tener:

- **Objetivo** (URL, dominio, IP, repo, app móvil, OpenAPI spec)
- **Alcance autorizado** (in-scope / out-of-scope)
- **Tipo** (black/grey/white box)
- **Credenciales de prueba** (si aplica)
- **Ventanas autorizadas / ritmo permitido** (rate-limit del cliente)
- **Foco prioritario** (Web / API / AI / Cloud / Mobile / Mixto)

Si falta algo, pregúntalo en bloque, no goteo. Si CLAUDE.md ya garantiza autorización por defecto (caso del usuario actual), no preguntes por autorización.

---

## 2. Pipeline ofensivo (referencia)

```
ASM / Recon ─► Fingerprint ─► Crawl & JS Intel ─► API/Auth Mapping
     │              │                │                    │
     ▼              ▼                ▼                    ▼
 Subdominios   Tech stack      Endpoints/secrets    Flujos OAuth/JWT
     │                                                    │
     └─────────► Fuzzing & Scanners ◄────────────────────┘
                       │
                       ▼
        Exploitation por vector (SQLi/XSS/SSRF/SSTI/IDOR/...)
                       │
                       ▼
        AI Correlation & Attack Chain Reasoning
                       │
                       ▼
        PoC Reproducible + Evidencia + CVSS + CWE/CAPEC
                       │
                       ▼
        Reporting (Markdown/DOCX/PDF/SARIF/JSON)
```

Cada caja tiene su archivo de referencia detallado. **Carga solo el que necesites según la fase activa** — no leas todo de golpe.

---

## 3. Mapa de referencias (carga bajo demanda)

| Fase / Tema | Archivo |
|-------------|---------|
| Metodologías formales (PTES/WSTG/NIST/OSSTMM/ATT&CK/CWE/CAPEC) | `references/methodologies.md` |
| Recon / OSINT / ASM / Continuous recon | `references/recon.md` |
| Web proxy & interceptación (Burp, ZAP, Caido, mitmproxy) | `references/proxy.md` |
| Content discovery & fuzzing (ffuf, feroxbuster, arjun, paramspider) | `references/fuzzing.md` |
| Vulnerability scanners (nuclei, nikto, Nessus, Acunetix, Invicti) | `references/scanners.md` |
| SQL Injection (sqlmap, ghauri, NoSQLMap, blind/time-based) | `references/sqli.md` |
| XSS (XSStrike, Dalfox, XSSHunter, DOM/Stored/Reflected/Blind, CSP bypass) | `references/xss.md` |
| API security (REST/GraphQL/SOAP, BOLA, mass assignment, schemathesis) | `references/api.md` |
| GraphQL specialization (introspection, batching, alias, depth, field auth) | `references/graphql.md` |
| JWT / OAuth / OIDC / SAML / SSO / MFA / sessions | `references/auth.md` |
| SSRF / SSTI / Deserialization / Out-of-band (interactsh, Collaborator) | `references/advanced-vulns.md` |
| CMS hacking (WordPress, Drupal, Joomla) | `references/cms.md` |
| JavaScript analysis (LinkFinder, SecretFinder, source maps, retire.js) | `references/js-intel.md` |
| Cloud + Kubernetes + Containers (ScoutSuite, Prowler, Pacu, kube-hunter) | `references/cloud.md` |
| CI/CD attack surface (GH Actions, GitLab CI, Jenkins, Argo) | `references/cicd.md` |
| Secret hunting (trufflehog, gitleaks, gitrob) | `references/secrets.md` |
| Race conditions (Turbo Intruder, race-the-web) | `references/race-conditions.md` |
| HTTP desync / request smuggling (CL.TE/TE.CL/H2) | `references/desync.md` |
| Web cache deception/poisoning (Param Miner) | `references/cache-attacks.md` |
| Browser security (CSP bypass, postMessage, SW, XS-Leaks, SameSite) | `references/browser-sec.md` |
| Business logic testing (workflows, state, race, abuse cases) | `references/business-logic.md` |
| Mobile ↔ Web correlation (JWT reuse, hardcoded API, Android/iOS) | `references/mobile-web.md` |
| WAF/EDR evasion (Unicode, smuggling, header mutation) | `references/evasion.md` |
| Attack chaining patterns (XSS→ATO, SSRF→Redis, IDOR→PrivEsc, SSTI→RCE) | `references/attack-chains.md` |
| Vulnerability correlation engine | `references/correlation.md` |
| Exploitability & remediation prioritization | `references/prioritization.md` |
| Wordlists & payloads (SecLists, PayloadsAllTheThings, custom) | `references/wordlists.md` |
| Labs (Juice Shop, DVWA, WebGoat, HTB, THM, PortSwigger Academy) | `references/labs.md` |
| OPSEC ofensivo (rotating infra, VPN/Tor, attribution reduction) | `references/opsec.md` |
| Legal framework (scope, evidence handling, safe harbor) | `references/legal.md` |
| Reporting engine — estructura senior completa | `references/reporting.md` |
| CVSS engine (3.1 + 4.0 + explicación de vector) | `references/cvss.md` |
| MCP ecosystem (qué MCPs existen, cuáles crear) | `references/mcp.md` |
| Knowledge graph & AI memory ofensiva | `references/ai-memory.md` |
| Autonomous agents (recon/JS/API/exploit/reporting agents) | `references/agents.md` |
| Roadmap dm20911 Offensive Web (niveles 1-4) | `references/roadmap.md` |

---

## 4. Modos de operación

El usuario puede pedir distintos modos. Detéctalos por contexto:

| Modo | Cuándo | Carga referencias |
|------|--------|-------------------|
| **Recon rápido** | "haz recon a X", "subdominios de Y" | `recon.md` |
| **Pentest dirigido** | "audita endpoint Z", "BOLA aquí" | la categoría correspondiente + `reporting.md` |
| **Pentest completo** | "audita esta web/API end-to-end" | `methodologies.md` + el pipeline completo |
| **Bug bounty** | "esto es para HackerOne/Intigriti" | `recon.md` + `attack-chains.md` + `reporting.md` (formato bounty) |
| **Solo reporte** | "arma el informe con esto" | `reporting.md` + `cvss.md` |
| **Triage rápido** | "qué hago con esto" | tu juicio + 1-2 referencias |

---

## 5. Tooling — capability check + instalación bajo demanda

### 5.1 Tres niveles de capacidad (no mezclar)

Para evitar que el usuario piense que hay automatización end-to-end donde solo hay guía, **toda capacidad está explícitamente clasificada** en uno de tres niveles:

| Nivel | Qué significa | Quién ejecuta | Ejemplos |
|-------|---------------|---------------|----------|
| **L1 NATIVE** | Lógica/scripts dentro de la skill. Disponible siempre que la skill esté instalada. | La IA, vía Bash. | `generate_report.py`, `methodology.py`, `capability_check.py`, `references/` |
| **L2 EXTERNAL** | Herramienta o MCP externo presente en el host. La IA la invoca directamente. | La IA, vía Bash o MCP. | nuclei, ffuf, sqlmap, nmap, dalfox, jwt_tool, burp-mcp, n8n-mcp |
| **L3 GUIDED** | Capacidad **solo documentada/guiada**. Sin ejecución directa: la IA describe pasos, el humano los ejecuta (o requiere UI, auth manual, decisión legal). | El usuario humano. | Burp UI sin MCP, ROE/autorización legal, plataformas BB, decisiones de scope |

**Regla:** antes de prometer un workflow, declara explícitamente de qué nivel es cada paso. Si un paso es L3 (ej. *"aprobar el scope con el cliente"*), no lo automatices ni lo ocultes en un comando — explícita que es manual.

### 5.2 Capability check obligatorio

Antes de prometer ejecución de cualquier fase activa (recon automatizado, scan masivo, exploitation), corre:

```bash
python3 ~/.claude/skills/HackingWebbyDM20911/scripts/capability_check.py
```

Salida: tabla por nivel mostrando qué está disponible, versión detectada, qué falta y qué es crítico. Para integrarlo en el informe final (anexo "Entorno de testing", trazabilidad de hallazgos):

```bash
python3 ~/.claude/skills/HackingWebbyDM20911/scripts/capability_check.py --json > /tmp/env.json
```

Opciones útiles:

- `--strict` — exit code ≠ 0 si falta algo L2 marcado como crítico (útil en CI / pre-pentest gate).
- `--only L1|L2|L3` — filtrar por nivel.
- `--category recon|fuzzing|scanner|sqli|xss|api|auth|mcp|secrets|...` — filtrar por fase.

**Cuándo correrlo:**

1. Al inicio del engagement (después del paso 0 de metodología).
2. Cuando el usuario pida "audita esto end-to-end" — declara qué hay y qué falta antes de prometer.
3. Antes de generar el informe — el JSON se anexa como evidencia del entorno real usado.

Si una herramienta L2 crítica falta, **no inventes el resultado**: o instálala (sección siguiente) o degrada al modo L3 (guiar al usuario) y marca el hallazgo con `confidence: low` y `limitations`.

### 5.3 Verificación puntual e instalación

Para chequear una sola herramienta en línea:

```bash
command -v <tool> >/dev/null 2>&1 || echo "Falta: <tool>"
```

Si falta, ofrece el one-liner de instalación:

| Tool | Instalación rápida (macOS) |
|------|------|
| nuclei, httpx, katana, dnsx, naabu, subfinder | `brew install <tool>` o `go install -v github.com/projectdiscovery/<tool>/v3/cmd/<tool>@latest` |
| ffuf | `brew install ffuf` |
| feroxbuster | `brew install feroxbuster` |
| sqlmap | `brew install sqlmap` |
| amass | `brew install amass` |
| arjun, paramspider | `pipx install arjun` / `pipx install paramspider` |
| jwt_tool | `pipx install jwt-tool` |
| trufflehog | `brew install trufflehog` |
| gitleaks | `brew install gitleaks` |
| nmap, masscan | `brew install nmap masscan` |
| interactsh-client | `go install -v github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest` |
| dalfox, kxss | `brew install dalfox` / `go install github.com/Emoe/kxss@latest` |
| XSStrike | `pipx install xsstrike` |

**Regla:** si el usuario pidió ejecución rápida (ej: `/hackweb recon target.cl`), **ejecuta sin explicar** la instalación a menos que falle. Si pidió explícitamente "explícame la instalación / setup", entonces sí entra paso a paso.

Lista completa por categoría: `references/recon.md`, `references/scanners.md`, etc.

---

## 6. MCPs — guía de configuración

El stack ideal incluye MCPs ofensivos (burp-mcp, nuclei-mcp, sqli-mcp, api-security-mcp, etc.). Si el usuario pide configurar uno y no está disponible:

- **Si no pidió paso a paso:** ejecuta lo necesario, instala silenciosamente.
- **Si pidió "guíame para configurarlo":** abre `references/mcp.md` y sigue el paso a paso (descarga, `claude mcp add`, validación, ejemplo de uso).

Ver catálogo completo de MCPs recomendados (existentes y a crear) en `references/mcp.md`.

---

## 7. Reporting — siempre senior, multi-formato

Esta skill **incluye un generador propio** en `scripts/generate_report.py` que produce el informe en cualquier formato que pida el usuario (md, txt, html, docx, pdf, pptx, json/sarif, o `all` de una vez).

**Uso rápido:**
```bash
python3 ~/.claude/skills/HackingWebbyDM20911/scripts/generate_report.py \
  --input findings.json --format docx --output informe.docx
```

Formatos soportados:

| Formato | Cuándo usarlo |
|---------|---------------|
| `md` | Repo, commit, issue tracker |
| `txt` | Pipes, terminal, ticket plano |
| `html` | Compartir por web, vista rápida con estilo |
| `docx` | Cliente que va a editar (texto justificado, tablas con color por severidad, bloques de código tipo terminal) |
| `pdf` | Entregable final firmado. Backend con fallback automático: weasyprint, luego Chrome/Chromium/Brave/Edge headless, luego wkhtmltopdf. En macOS con SIP usa Chrome headless sin requerir `brew install pango`. |
| `pptx` | **Presentación simple** de resultados ejecutivos (portada, resumen, matriz, top hallazgos, conclusión) |
| `json` | Ingesta a otro sistema, knowledge graph |
| `all` | Genera todos en un directorio |

**Schema del JSON de entrada:** ver `assets/example_findings.json` — tiene meta, introducción, resumen ejecutivo, alcance, metodología, findings (con CVSS 3.1+4.0, CWE, CAPEC, OWASP, ATT&CK, PoC con `descripcion`+`cmd`+`output`), attack_chains, timeline, limitaciones, conclusión, anexos.

Cualquier hallazgo debe ir a un informe que cumpla la estructura de `references/reporting.md`. Mínimo obligatorio por hallazgo:

1. Nombre técnico
2. Severidad + **CVSS 3.1 (vector + score)** y **CVSS 4.0 (vector + score)**
3. **CWE** (siempre, no olvidar) + **CAPEC** + **OWASP mapping** + **MITRE ATT&CK** si aplica
4. Activo afectado, parámetro vulnerable
5. Descripción (qué/cómo/por qué/dónde)
6. Impacto (negocio + técnico, frase "Un atacante podría...")
7. Probabilidad de explotación + Confidence + Validación manual (sí/no)
8. Riesgo de negocio
9. Evidencia técnica (req/resp/headers/payloads/timing)
10. **PoC reproducible** con la estructura de pasos en `references/reporting.md` (configuración inicial → captura → comando + explicación → respuesta + análisis → resultado)
11. **Evidence trace (obligatorio, auditable)** — cada hallazgo lleva al menos un objeto `evidence` con:
    - `tool` (nombre exacto, ej. `nuclei`)
    - `tool_version` (string devuelto por `--version`)
    - `capability_level` (`L1_NATIVE` | `L2_EXTERNAL` | `L3_GUIDED`)
    - `command` (línea exacta ejecutada, copy-paste)
    - `output` (stdout/stderr relevante, recortado pero verbatim)
    - `timestamp` (ISO-8601 UTC)
    - `confidence` (`high` | `medium` | `low`) + justificación
    - `limitations` (qué NO se verificó, falsos positivos posibles, alcance de la prueba)

    Si `capability_level: L3_GUIDED`, declara `command: "manual"` y describe los pasos humanos en `output`. Nunca inventes salida de herramienta que no se ejecutó.
12. Remediación (inmediata, recomendada, hardening adicional)
13. Referencias (OWASP, CWE, CVE, PortSwigger, MITRE, NIST)

El informe completo añade: portada, TOC, resumen ejecutivo, alcance, metodología, matriz de riesgo, attack chaining, impacto CIA, timeline, limitaciones, conclusión, anexos.

---

## 8. Reglas operativas heredadas (de CLAUDE.md global y proyecto)

- **Comandos para el usuario:** una sola línea, sin `\` de continuación, sin espacios al inicio.
- **WAF:** siempre añadir User-Agent de navegador en scripts Python/curl.
- **404 ≠ 401/403:** un 404 inesperado en un endpoint que debería rechazar = posible BOLA confirmado.
- **macOS grep:** evitar paréntesis complejos.
- **Source maps:** descargar a `/tmp` antes de parsear.
- **VPN-friendly:** todo comando debe ser copy-paste, no asumir acceso al terminal.

---

## 9. Loop de trabajo recomendado

1. Boot → preguntar metodología
2. Recopilar datos mínimos
3. Ejecutar fase actual del pipeline (carga la referencia correspondiente)
4. Documentar cada hallazgo en formato senior (sección 7)
5. Pasar a la siguiente fase
6. Al cerrar: generar informe final + actualizar memoria del proyecto con bypasses, payloads útiles y WAF fingerprints (`references/ai-memory.md`)

---

## 10. Anti-patrones (no hacer)

- ❌ Saltarse el paso 0 (preguntar metodología) — produce informes sin estructura.
- ❌ Lanzar nuclei/sqlmap masivos sin scope confirmado.
- ❌ Reportar hallazgos sin CWE.
- ❌ Reportar sin CVSS 3.1 **y** 4.0 (ambos hoy son estándar).
- ❌ PoC sin pasos reproducibles (otro pentester debe poder repetirlo).
- ❌ Confundir "no hay datos en QA" con "no hay vulnerabilidad".
- ❌ Generar payloads weaponizados para CVE críticos recientes salvo lab controlado.
- ❌ Olvidar guardar bypasses/payloads exitosos en memory del proyecto.
- ❌ Prometer "automatización end-to-end" sin haber corrido `capability_check.py` — confunde L2 (ejecutable) con L3 (solo guiado).
- ❌ Reportar un hallazgo sin `evidence` (tool + version + command + output + timestamp + confidence + limitations). Si no es trazable, no es un hallazgo: es una hipótesis.
- ❌ Inventar output de una herramienta cuando el `capability_check` la marcó como `NO`. Degrada a L3 y dilo.
