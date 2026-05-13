# CWE + CAPEC — Common Weakness Enumeration & Common Attack Pattern Enumeration

## Origen y autoridad
Ambos mantenidos por **MITRE** bajo el National Cybersecurity FFRDC.
- **CWE** (Common Weakness Enumeration) — catálogo de **debilidades** en código/diseño que pueden llevar a vulnerabilidades. Existe desde 2006. Sitio: https://cwe.mitre.org
- **CAPEC** (Common Attack Pattern Enumeration and Classification) — catálogo de **patrones de ataque** que explotan esas debilidades. Sitio: https://capec.mitre.org

CWE describe el "qué está mal", CAPEC describe el "cómo se ataca". Son complementarios.

## Diferencia clave vs ATT&CK
| | CWE | CAPEC | ATT&CK |
|---|---|---|---|
| Granularidad | Debilidad puntual | Patrón de ataque | TTP de adversario |
| Audiencia | Devs + AppSec | Pentesters + AppSec | Red/Blue/Purple team |
| Ejemplo | CWE-89 SQLi (la debilidad) | CAPEC-66 SQL Injection (cómo se ataca) | T1190 Exploit Public-Facing App (táctica del actor) |

## CWE — debilidades más relevantes en web/API

### Inyección
- `CWE-89` SQL Injection
- `CWE-78` OS Command Injection
- `CWE-79` XSS (Cross-Site Scripting)
- `CWE-91` XML Injection
- `CWE-94` Code Injection
- `CWE-918` Server-Side Request Forgery
- `CWE-1336` Server-Side Template Injection
- `CWE-77` Command Injection (generic)
- `CWE-22` Path Traversal

### Autenticación / autorización
- `CWE-287` Improper Authentication
- `CWE-306` Missing Authentication for Critical Function
- `CWE-307` Improper Restriction of Excessive Authentication Attempts (no rate-limit)
- `CWE-639` Authorization Bypass Through User-Controlled Key (IDOR/BOLA)
- `CWE-862` Missing Authorization
- `CWE-863` Incorrect Authorization
- `CWE-285` Improper Authorization
- `CWE-269` Improper Privilege Management
- `CWE-798` Use of Hard-coded Credentials
- `CWE-522` Insufficiently Protected Credentials
- `CWE-521` Weak Password Requirements
- `CWE-384` Session Fixation
- `CWE-613` Insufficient Session Expiration
- `CWE-352` Cross-Site Request Forgery (CSRF)

### Configuración / crypto
- `CWE-1004` Sensitive Cookie Without HttpOnly Flag
- `CWE-614` Sensitive Cookie Without Secure Flag
- `CWE-200` Exposure of Sensitive Information to an Unauthorized Actor
- `CWE-538` Insertion of Sensitive Information into Externally-Accessible File
- `CWE-209` Generation of Error Message Containing Sensitive Information
- `CWE-326` Inadequate Encryption Strength
- `CWE-327` Use of a Broken or Risky Cryptographic Algorithm
- `CWE-330` Use of Insufficiently Random Values
- `CWE-345` Insufficient Verification of Data Authenticity

### Validación / mass assignment
- `CWE-915` Improperly Controlled Modification of Dynamically-Determined Object Attributes (mass assignment)
- `CWE-602` Client-Side Enforcement of Server-Side Security
- `CWE-20` Improper Input Validation
- `CWE-601` URL Redirection to Untrusted Site (Open Redirect)

### Race / lógica
- `CWE-362` Concurrent Execution using Shared Resource with Improper Synchronization (race condition)
- `CWE-841` Improper Enforcement of Behavioral Workflow

### Deserialization
- `CWE-502` Deserialization of Untrusted Data

### File upload
- `CWE-434` Unrestricted Upload of File with Dangerous Type
- `CWE-79` (stored) si el upload sirve HTML/SVG

## CAPEC — patrones de ataque correlacionados

| CAPEC | Patrón | CWE relacionado |
|-------|--------|-----------------|
| CAPEC-66 | SQL Injection | CWE-89 |
| CAPEC-63 | Cross-Site Scripting | CWE-79 |
| CAPEC-115 | Authentication Bypass | CWE-287 |
| CAPEC-39 | Manipulating Opaque Client-Based Data Tokens (IDOR/BOLA) | CWE-639 |
| CAPEC-664 | Server Side Request Forgery | CWE-918 |
| CAPEC-242 | Code Injection | CWE-94 |
| CAPEC-77 | Manipulating User-Controlled Variables (mass assignment) | CWE-915 |
| CAPEC-194 | Fake the Source of Data | CWE-345 |
| CAPEC-21 | Exploitation of Trusted Identifiers | CWE-384 |
| CAPEC-62 | Cross-Site Request Forgery | CWE-352 |
| CAPEC-148 | Content Spoofing | CWE-601 |
| CAPEC-227 | Sustained Client Engagement (timing/race) | CWE-362 |
| CAPEC-575 | Account Footprinting | CWE-200 |

## Cómo aplicar CWE + CAPEC a una auditoría

**Por cada hallazgo del informe**, asignar obligatoriamente:
- 1 CWE (la debilidad concreta).
- 1 CAPEC (el patrón de ataque, opcional pero recomendado).
- 1 OWASP mapping (categoría Top 10 / WSTG ID).
- 1 ATT&CK technique (si aplica).

Ejemplo (BOLA):
```yaml
finding:
  titulo: BOLA en /v1/cuentas/{id}
  cwe: CWE-639 — Authorization Bypass Through User-Controlled Key
  capec: CAPEC-39 — Manipulating Opaque Client-Based Data Tokens
  owasp: API1:2023 — Broken Object Level Authorization / WSTG-ATHZ-04
  attack: T1190 — Exploit Public-Facing Application
```

Este mapping cuádruple permite:
- Devs entender qué hay que arreglar en código (CWE).
- AppSec mappear a su pipeline de SAST/DAST (CWE + CAPEC).
- SOC correlacionar con detección (ATT&CK).
- Compliance reportar a auditor (OWASP / WSTG ID).

## Cuándo usar CWE/CAPEC
- **Cualquier informe profesional** — son obligatorios en informes serios.
- **Mapping con SAST/DAST** — herramientas como Semgrep, Checkmarx, Veracode usan CWE-IDs.
- **CVE assignment** — al solicitar CVE para un 0-day, MITRE pide el CWE.

## Cuándo NO son suficientes solos
- CWE/CAPEC no son una metodología — son un sistema de clasificación. Necesitan complementarse con PTES/WSTG/NIST que dicen **qué probar**.

## Combinaciones recomendadas
- **CWE + CAPEC + WSTG + OWASP Top 10** → clasificación completa por hallazgo.
- **CWE + CAPEC + ATT&CK** → mapping de findings a TTPs (purple team).
- **CWE + CVSS + CAPEC** → scoring + clasificación + patrón → estándar industrial completo.
