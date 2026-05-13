# Metodologías formales

Selecciona una o combínalas. Cada engagement queda anclado a fases concretas para trazabilidad.

## PTES (Penetration Testing Execution Standard)
1. Pre-engagement Interactions
2. Intelligence Gathering
3. Threat Modeling
4. Vulnerability Analysis
5. Exploitation
6. Post Exploitation
7. Reporting

Mejor para: pentest formal de cliente con contrato.

## OWASP WSTG (Web Security Testing Guide v4.2)
- **WSTG-INFO** Information Gathering (10 controles)
- **WSTG-CONF** Configuration & Deployment Management
- **WSTG-IDNT** Identity Management
- **WSTG-ATHN** Authentication
- **WSTG-ATHZ** Authorization
- **WSTG-SESS** Session Management
- **WSTG-INPV** Input Validation
- **WSTG-ERRH** Error Handling
- **WSTG-CRYP** Cryptography
- **WSTG-BUSL** Business Logic
- **WSTG-CLNT** Client-Side
- **WSTG-APIT** API Testing

Mejor para: pentest web/API estandarizado, mapping a controles auditable.

## NIST SP 800-115
1. Planning
2. Discovery (passive + active)
3. Attack (gaining access, escalating, system browsing, install tools)
4. Reporting

Mejor para: contextos regulados (gobierno, banca, salud).

## OSSTMM (Open Source Security Testing Methodology Manual v3)
Canales: Human, Physical, Wireless, Telecom, Data Networks. Métricas RAV.

Mejor para: assessments holísticos no solo web.

## MITRE ATT&CK
Mapping de TTPs por hallazgo. Web-relevant tactics: Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Exfiltration, Impact.

Sub-techniques útiles para web:
- T1190 Exploit Public-Facing Application
- T1078 Valid Accounts
- T1212 Exploitation for Credential Access
- T1606 Forge Web Credentials (T1606.001 Web Cookies, T1606.002 SAML Tokens)
- T1199 Trusted Relationship

## CWE / CAPEC
- **CWE** clasifica el tipo de debilidad en el código (CWE-89 SQLi, CWE-79 XSS, CWE-352 CSRF, CWE-798 Hardcoded Credentials, CWE-22 Path Traversal, CWE-918 SSRF, etc.)
- **CAPEC** clasifica patrones de ataque (CAPEC-66 SQL Injection, CAPEC-63 XSS, CAPEC-115 Authentication Bypass, etc.)

Cada hallazgo del informe **debe** llevar CWE. CAPEC es un plus profesional.

## Mapping recomendado por tipo de engagement

| Engagement | Stack |
|------------|-------|
| Pentest web QA | OWASP WSTG + CWE |
| Pentest web prod regulado | PTES + NIST + OWASP WSTG + CWE |
| Bug bounty | OWASP WSTG + ATT&CK + CWE/CAPEC |
| Red team | PTES + ATT&CK |
| API-only | OWASP WSTG (ATHN/ATHZ/APIT) + OWASP API Top 10 |
| Audit holística | OSSTMM + PTES |

## Híbrido (recomendación default)

`OWASP WSTG (test cases) + PTES (fases) + ATT&CK (TTPs) + CWE/CAPEC (clasificación)` cubre el 95% de los casos profesionales sin redundancia.
