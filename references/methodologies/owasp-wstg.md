# OWASP WSTG — Web Security Testing Guide v4.2

## Origen y autoridad
Mantenida por la OWASP Foundation, comunidad open-source desde 2003. Es **la guía de referencia para test cases web/API**. Cada control tiene ID (`WSTG-XXXX-NN`), descripción, objetivos, cómo probar y herramientas sugeridas.

Sitio oficial: https://owasp.org/www-project-web-security-testing-guide/

## Estructura: 12 categorías

| Prefijo | Categoría | # Controles |
|---------|-----------|-------------|
| WSTG-INFO | Information Gathering | 10 |
| WSTG-CONF | Configuration & Deployment Management | 11 |
| WSTG-IDNT | Identity Management | 5 |
| WSTG-ATHN | Authentication | 10 |
| WSTG-ATHZ | Authorization | 4 |
| WSTG-SESS | Session Management | 8 |
| WSTG-INPV | Input Validation | 19 |
| WSTG-ERRH | Error Handling | 2 |
| WSTG-CRYP | Cryptography | 4 |
| WSTG-BUSL | Business Logic | 9 |
| WSTG-CLNT | Client-Side | 13 |
| WSTG-APIT | API Testing | 1 (placeholder, extendido en OWASP API Top 10) |

## Controles clave por categoría (ejemplo seleccionado)

### INFO (Information Gathering)
- `WSTG-INFO-01` Conduct Search Engine Discovery (Google dorks)
- `WSTG-INFO-02` Fingerprint Web Server
- `WSTG-INFO-03` Review Webserver Metafiles (robots.txt, sitemap.xml)
- `WSTG-INFO-04` Enumerate Applications on Webserver
- `WSTG-INFO-08` Fingerprint Web Application Framework

### CONF (Configuration)
- `WSTG-CONF-02` Test Application Platform Configuration
- `WSTG-CONF-03` Test File Extensions Handling
- `WSTG-CONF-04` Review Old Backup and Unreferenced Files
- `WSTG-CONF-06` Test HTTP Methods (OPTIONS, PUT, DELETE)
- `WSTG-CONF-07` Test HTTP Strict Transport Security
- `WSTG-CONF-08` Test RIA Cross Domain Policy
- `WSTG-CONF-11` Test Cloud Storage

### ATHN (Authentication)
- `WSTG-ATHN-01` Credentials Transported Over Encrypted Channel
- `WSTG-ATHN-02` Default Credentials
- `WSTG-ATHN-03` Weak Lock Out Mechanism
- `WSTG-ATHN-04` Bypassing Authentication Schema
- `WSTG-ATHN-05` Vulnerable Remember Password
- `WSTG-ATHN-07` Weak Password Policy
- `WSTG-ATHN-09` Weak Password Change or Reset Functionality
- `WSTG-ATHN-10` Weak Authentication in Alternative Channels (mobile API)

### ATHZ (Authorization)
- `WSTG-ATHZ-01` Directory Traversal / File Include
- `WSTG-ATHZ-02` Bypassing Authorization Schema
- `WSTG-ATHZ-03` Privilege Escalation
- `WSTG-ATHZ-04` Insecure Direct Object References (IDOR/BOLA)

### SESS (Session Management)
- `WSTG-SESS-01` Bypassing Session Management Schema
- `WSTG-SESS-02` Cookies Attributes (HttpOnly, Secure, SameSite)
- `WSTG-SESS-03` Session Fixation
- `WSTG-SESS-04` Exposed Session Variables
- `WSTG-SESS-05` Cross Site Request Forgery
- `WSTG-SESS-06` Logout Functionality
- `WSTG-SESS-07` Session Timeout
- `WSTG-SESS-08` Session Puzzling

### INPV (Input Validation) — la más extensa
- `WSTG-INPV-01` Reflected XSS
- `WSTG-INPV-02` Stored XSS
- `WSTG-INPV-03` HTTP Verb Tampering
- `WSTG-INPV-04` HTTP Parameter Pollution
- `WSTG-INPV-05` SQL Injection (subcontroles 05.x por motor de BD)
- `WSTG-INPV-06` LDAP Injection
- `WSTG-INPV-07` XML Injection / XXE
- `WSTG-INPV-09` Code Injection
- `WSTG-INPV-10` Command Injection
- `WSTG-INPV-11` Format String
- `WSTG-INPV-12` Incubated Vulnerability
- `WSTG-INPV-15` HTTP Smuggling
- `WSTG-INPV-18` Server-Side Request Forgery
- `WSTG-INPV-19` Mass Assignment

### CRYP
- `WSTG-CRYP-01` TLS Configuration
- `WSTG-CRYP-02` Padding Oracle
- `WSTG-CRYP-04` Weak Encryption

### BUSL (Business Logic) — la más subestimada
- `WSTG-BUSL-01` Business Logic Data Validation
- `WSTG-BUSL-02` Forgeable Identifiers
- `WSTG-BUSL-03` Integrity Checks
- `WSTG-BUSL-04` Process Timing (race conditions)
- `WSTG-BUSL-05` Number of Times Function Can Be Used (refund/coupon abuse)
- `WSTG-BUSL-06` Circumvention of Workflows
- `WSTG-BUSL-07` Defenses Against Misuse
- `WSTG-BUSL-08` Upload Unexpected File Types
- `WSTG-BUSL-09` Upload Malicious Files

### CLNT (Client-Side)
- `WSTG-CLNT-01` DOM-Based XSS
- `WSTG-CLNT-03` HTML Injection
- `WSTG-CLNT-04` Client-Side URL Redirect
- `WSTG-CLNT-06` Clickjacking
- `WSTG-CLNT-07` Cross Origin Resource Sharing
- `WSTG-CLNT-09` Server-Sent Events
- `WSTG-CLNT-11` Local Storage
- `WSTG-CLNT-13` Cross-Site Script Inclusion

## Cómo aplicar OWASP WSTG a la auditoría

1. **Checklist por categoría:** marcar cada `WSTG-XX-NN` que aplica al scope.
2. **Mapping a hallazgos:** cada finding debe llevar su WSTG ID en el campo `owasp` del JSON (ej. `WSTG-INPV-05.2 / A03:2021 SQL Injection`).
3. **Cobertura medible:** al cierre, reportar % de controles WSTG ejecutados sobre los aplicables (no todos aplican; ej. WSTG-CONF-11 solo si hay cloud storage).
4. **Trazabilidad:** cada test ejecutado con su evidencia (request/response) referenciada al WSTG ID.

## Mapping rápido herramienta → control

| Control | Tool sugerido |
|---------|---------------|
| WSTG-INFO-02 | `whatweb`, `httpx -tech-detect` |
| WSTG-INFO-08 | `wappalyzer-cli`, `httpx` |
| WSTG-CONF-04 | `ffuf` con wordlist `Common-DB-Backups.txt`, `feroxbuster` |
| WSTG-CONF-06 | `curl -X OPTIONS`, Burp Repeater |
| WSTG-ATHN-04 | Manual + Autorize (Burp ext) |
| WSTG-ATHN-07 | Burp Intruder, hydra |
| WSTG-ATHZ-04 | Autorize, manual con cuentas A y B |
| WSTG-SESS-02 | Cookie inspector, Burp |
| WSTG-INPV-01/02 | dalfox, XSStrike, kxss |
| WSTG-INPV-05 | sqlmap, ghauri |
| WSTG-INPV-18 | SSRFmap, interactsh |
| WSTG-BUSL-04 | Turbo Intruder |
| WSTG-CLNT-01 | XSStrike, manual DOM analysis |

## Cuándo usar WSTG
- **Cualquier pentest web/API** — es lo más completo y reconocido.
- Auditorías que necesitan **mapping a controles auditables** (clientes corporate piden esto).
- Bug bounty (combinar con ATT&CK para añadir TTPs).

## Cuándo es insuficiente
- Pentest formal con cliente regulado → complementar con PTES (fases) y NIST 800-115.
- Red team con persistencia → complementar con ATT&CK.
- API móvil → complementar con OWASP MASVS / MSTG.

## Combinaciones recomendadas
- **PTES + WSTG** → estándar industrial para clientes corporate.
- **WSTG + OWASP API Top 10** → API testing completo.
- **WSTG + ATT&CK + CWE** → bug bounty con clasificación profesional.
