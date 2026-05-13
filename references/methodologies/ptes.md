# PTES — Penetration Testing Execution Standard

## Origen y autoridad
Estándar abierto publicado por un consorcio de pentesters (Chris Nickerson, Dave Kennedy y otros) en 2009-2014. Es la metodología de referencia para pentests **profesionales con cliente** porque cubre el contrato, las reglas de engagement y la retención de evidencia, no solo la parte técnica.

Sitio oficial: http://www.pentest-standard.org

## Las 7 fases formales

### 1. Pre-engagement Interactions
- Definir alcance escrito (in-scope / out-of-scope).
- Reglas de engagement (RoE): ventanas autorizadas, rate-limits, técnicas permitidas (no DoS por defecto).
- Datos de contacto del cliente 24/7 y procedimiento de escalada si algo se rompe.
- NDA firmado, SoW firmado.
- Líneas de comunicación seguras (PGP, Signal).
- Acuerdo de retención y destrucción de evidencia.

### 2. Intelligence Gathering
- OSINT pasivo (Maltego, theHarvester, búsquedas en GitHub, Shodan).
- Footprinting activo (subfinder, amass, dnsx, masscan).
- Fingerprinting de stack (whatweb, wappalyzer, httpx -tech-detect).
- Identificación de personas clave (LinkedIn, repositorios públicos).

### 3. Threat Modeling
- Modelar activos críticos del cliente (dinero, PII, propiedad intelectual).
- Mapear actores de amenaza relevantes (insider, competidor, hacktivista, crimen organizado).
- Priorizar superficies de ataque según riesgo de negocio, no según facilidad técnica.

### 4. Vulnerability Analysis
- Escaneos automáticos con nuclei, sqlmap, dalfox, dirsearch.
- Análisis manual sobre los resultados (filtrar falsos positivos).
- Revisión de código si white/grey box (semgrep, trufflehog).
- Análisis de dependencias (retire.js, OSV scanner).

### 5. Exploitation
- Explotar vulnerabilidades identificadas con scope autorizado.
- Documentar cada paso (request, response, timing).
- Conservar cuentas/tokens creados con un naming pattern conocido para limpieza posterior.
- Evidencia con timestamp y hash.

### 6. Post Exploitation
- Determinar valor real del compromiso (acceso a datos sensibles, pivot a otros sistemas).
- Persistencia solo si está en alcance (red team).
- Limpieza: borrar cuentas creadas, archivos subidos, registros generados.

### 7. Reporting
- Executive summary (gerencia y compliance).
- Technical report con cada hallazgo: CVSS, CWE, descripción, impacto, PoC reproducible, remediación.
- Anexos: payloads, scripts, capturas, IOCs.
- Reunión de cierre con preguntas y comunicación de Q&A post-entrega.

## Cómo aplicar PTES a auditorías web/API

| Fase | Acción concreta web/API |
|------|--------------------------|
| Pre-engagement | Confirmar dominios, subdominios excluidos, ambientes (QA/prod), MFA bypass permitido o no, cuentas de prueba, ventana horaria, contactos del SOC. |
| Intelligence | `subfinder + httpx`, `katana` para endpoints, `linkfinder + SecretFinder` en JS bundles, `gitleaks/trufflehog` en repos públicos de la org. |
| Threat Modeling | Por flujo crítico (login, pago, recovery, admin): listar actores, datos en riesgo, controles esperados, abuse cases. |
| Vulnerability Analysis | `nuclei -severity high,critical`, `ffuf` content discovery, Burp passive scanner, manual review de OAuth/JWT/CSRF. |
| Exploitation | SQLi/XSS/SSRF/SSTI con sqlmap/dalfox/SSRFmap/tplmap; BOLA manual; JWT crack si HS256 débil. Cada exploit con PoC reproducible. |
| Post Exploitation | Si SSRF → cloud metadata → IAM enum (Pacu); si RCE → mapear filesystem para credentials.json/.env; si ATO → ver alcance de impacto en otros usuarios. |
| Reporting | Estructura del informe + scoring CVSS 3.1+4.0 + chains + matriz de riesgo. Usar `scripts/generate_report.py` para multi-formato. |

## Cuándo usar PTES
- Pentests **formales** con SoW y cliente externo.
- Auditorías que requieren **trazabilidad legal** (cumplimiento, regulación).
- Cuando hay que justificar tiempo dedicado por fase (ofertas por horas).

## Cuándo NO usar PTES (solo)
- Bug bounty rápido (la fase 1 PTES no aplica, ya hay safe harbor de la plataforma).
- Hot-fix de un único endpoint (overkill).
- Threat modeling puro sin explotación (usar OSSTMM o STRIDE).

## Combinaciones recomendadas
- **PTES + OWASP WSTG** → fases formales + test cases concretos web/API. Lo ideal en 90% de pentests profesionales.
- **PTES + NIST 800-115** → reguladas (banca, gobierno).
- **PTES + ATT&CK** → red team con mapping de TTPs.

## Entregables esperados (por fase)
| Fase | Artefacto |
|------|-----------|
| Pre-engagement | SoW firmado, RoE escrito, contactos |
| Intelligence | Mapa de superficie de ataque (subs, endpoints, tech, secrets) |
| Threat Modeling | Tabla de actores × activos × controles |
| Vulnerability Analysis | Lista de candidatos con confidence |
| Exploitation | PoCs reproducibles con timestamp |
| Post Exploitation | Diagrama de impacto / chain |
| Reporting | Informe ejecutivo + técnico + anexos |
