# MITRE ATT&CK — Adversarial Tactics, Techniques, and Common Knowledge

## Origen y autoridad
Framework mantenido por MITRE Corporation desde 2013. **No es una metodología de pentest** estrictamente — es un **catálogo de TTPs** (Tactics, Techniques, Procedures) reales observados en actores de amenaza. Su valor: **lenguaje común** entre rojo, azul y púrpura, y mapping a herramientas defensivas (EDR, SIEM, threat intel).

Sitio oficial: https://attack.mitre.org

## Estructura
- **Tactics** = el "por qué" del paso (objetivo táctico del adversario)
- **Techniques** = el "cómo" (método empleado)
- **Sub-techniques** = variantes específicas
- **Procedures** = implementación concreta vista en el wild

## Las 14 Tactics de Enterprise ATT&CK

| ID | Tactic |
|----|--------|
| TA0043 | Reconnaissance |
| TA0042 | Resource Development |
| TA0001 | Initial Access |
| TA0002 | Execution |
| TA0003 | Persistence |
| TA0004 | Privilege Escalation |
| TA0005 | Defense Evasion |
| TA0006 | Credential Access |
| TA0007 | Discovery |
| TA0008 | Lateral Movement |
| TA0009 | Collection |
| TA0011 | Command and Control |
| TA0010 | Exfiltration |
| TA0040 | Impact |

## Techniques relevantes para auditorías web

### Reconnaissance (TA0043)
- `T1595` Active Scanning (`T1595.001` IP block, `T1595.002` vuln scanning, `T1595.003` wordlist scanning)
- `T1592` Gather Victim Host Information
- `T1589` Gather Victim Identity Information (`T1589.002` Email Addresses)
- `T1596` Search Open Technical Databases
- `T1593` Search Open Websites/Domains

### Initial Access (TA0001)
- `T1190` **Exploit Public-Facing Application** ← la más común en web pentest
- `T1078` Valid Accounts (creds leaked/cracked)
- `T1133` External Remote Services
- `T1566` Phishing (si scope lo incluye)

### Execution (TA0002)
- `T1059` Command and Scripting Interpreter (post-RCE)
- `T1203` Exploitation for Client Execution (XSS, drive-by)

### Persistence (TA0003)
- `T1505` Server Software Component (`T1505.003` Web Shell)
- `T1136` Create Account

### Privilege Escalation (TA0004)
- `T1068` Exploitation for Privilege Escalation
- `T1078` Valid Accounts (escalada horizontal)

### Defense Evasion (TA0005)
- `T1027` Obfuscated Files or Information
- `T1140` Deobfuscate/Decode Files
- `T1562` Impair Defenses

### Credential Access (TA0006)
- `T1110` Brute Force (`T1110.001` Password Guessing, `T1110.003` Password Spraying, `T1110.004` Credential Stuffing)
- `T1212` Exploitation for Credential Access
- `T1552` Unsecured Credentials (`T1552.001` Creds In Files, `T1552.004` Private Keys, `T1552.005` Cloud Instance Metadata)
- `T1539` Steal Web Session Cookie
- `T1606` **Forge Web Credentials** (`T1606.001` Web Cookies, `T1606.002` SAML Tokens)

### Discovery (TA0007)
- `T1083` File and Directory Discovery
- `T1087` Account Discovery (`T1087.004` Cloud Account)
- `T1518` Software Discovery

### Lateral Movement (TA0008)
- `T1210` Exploitation of Remote Services
- `T1550` Use Alternate Authentication Material (`T1550.001` Application Access Token, `T1550.003` Pass the Ticket)

### Collection (TA0009)
- `T1213` Data from Information Repositories (`T1213.003` Code Repositories)
- `T1530` Data from Cloud Storage

### Exfiltration (TA0010)
- `T1041` Exfiltration Over C2 Channel
- `T1567` Exfiltration Over Web Service

### Impact (TA0040)
- `T1499` Endpoint Denial of Service (si scope autoriza)
- `T1565` Data Manipulation

## Cómo aplicar ATT&CK a una auditoría web

1. **Por cada hallazgo, mapear a la(s) technique(s) que aplican.** Ej:
   - SQL Injection en login → `T1190` (Initial Access) + posiblemente `T1078` (Valid Accounts si extrae creds)
   - JWT alg=none bypass → `T1606.001` (Forge Web Cookies)
   - SSRF a cloud metadata → `T1552.005` (Unsecured Credentials / Cloud Metadata)
   - BOLA enumerando users → `T1087` (Account Discovery)
   - XSS robando sesión → `T1539` (Steal Web Session Cookie)
   - Web shell tras file upload → `T1505.003` (Web Shell)

2. **Attack chains como secuencias ATT&CK.** Ej:
   ```
   T1595.002 (vuln scan) → T1190 (exploit SQLi) → T1212 (extract hashes)
   → T1110.001 (crack offline) → T1078 (valid creds) → T1530 (cloud data)
   → T1567 (exfil to atacker)
   ```

3. **Coverage report para purple team.** Reportar qué techniques se probaron, cuáles tuvieron éxito, cuáles fueron detectadas por el SOC del cliente.

## Particularidades de ATT&CK
- **No es exhaustivo** para web — algunas vulns no tienen technique-id exacta (ej. business logic abuse).
- **Mapping bidireccional**: el SOC del cliente puede ver desde sus reglas SIEM hacia ATT&CK y ver gaps.
- **Updates frecuentes** — versión actual es v15.x (2024+).
- **Sub-frameworks**: Enterprise (lo que usamos), Mobile, ICS, Cloud.

## Cuándo usar ATT&CK
- **Red team / purple team** — su uso principal.
- **Threat-informed pentest** — adversary emulation de un APT específico.
- **Auditorías con foco en detección**, no solo en findings (¿el SOC nos vio?).
- **Reporting a clientes maduros** con SOC y EDR.

## Cuándo NO es suficiente
- Sin WSTG/PTES, ATT&CK no te dice qué probar en una web — solo te ayuda a clasificar lo que encuentras.
- Bug bounty puro — clasificación opcional, no requerida.
- Auditorías de cumplimiento — usar WSTG/CWE primero, ATT&CK como complemento.

## Combinaciones recomendadas
- **ATT&CK + WSTG** → ATT&CK clasifica TTPs, WSTG dicta qué probar.
- **ATT&CK + CWE + CAPEC** → clasificación completa de cada hallazgo (técnica, debilidad, patrón de ataque).
- **ATT&CK + PTES** → red team formal con cliente.
