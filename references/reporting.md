# Reporting Engine — Estructura Senior

Estructura completa de un informe ofensivo profesional, agnóstico de cliente.

## Estructura completa

```
1. Portada
2. Tabla de Contenido
3. Introducción
4. Resumen Ejecutivo
5. Alcance
6. Metodología
7. Resumen de Hallazgos (tabla)
8. Hallazgos Técnicos (uno por sección)
9. Attack Chains
10. Matriz de Riesgo
11. Impacto sobre CIA
12. Estado de Explotabilidad
13. Timeline de Testing
14. Limitaciones
15. Recomendaciones (priorizadas)
16. Conclusión General
17. Anexos (payloads, wordlists, scripts, IOC)
```

## 1. Portada

- Nombre del assessment
- Cliente
- Tipo: Pentest Web / API / Red Team / Bug Bounty / Security Assessment
- Fecha
- Clasificación: Público / Interno / Confidencial / Restringido
- Versión del informe (1.0, 1.1, ...)
- Autor(es)
- Logo cliente
- Código interno

## 3. Introducción

```
El presente informe documenta las actividades de evaluación de seguridad
realizadas sobre la aplicación web XXXXX con el objetivo de identificar
vulnerabilidades explotables que puedan comprometer la confidencialidad,
integridad y disponibilidad de la información.
```

Incluir: objetivo, tipo, limitaciones, fechas, ventanas autorizadas, supuestos.

## 4. Resumen Ejecutivo

Lectores: gerencia, CTO, compliance, legales.

- Nivel de riesgo global (Crítico / Alto / Medio / Bajo / Aceptable).
- Cantidad de hallazgos por severidad.
- Impacto potencial al negocio.
- Superficie comprometida.
- Top 3 hallazgos críticos en lenguaje no técnico.
- Recomendaciones de alto nivel.

## 7. Resumen de Hallazgos

| ID | Vulnerabilidad | Severidad | CVSS 3.1 | CVSS 4.0 | CWE | Estado |
|----|----------------|-----------|----------|----------|-----|--------|
| H1 | SQL Injection en login | Crítico | 9.8 | 9.4 | CWE-89 | Confirmado |
| H2 | BOLA en /orders | Alto | 8.6 | 8.7 | CWE-639 | Confirmado |

## 8. Estructura PERFECTA de cada hallazgo

```markdown
### H1 — SQL Injection en endpoint de autenticación

**Severidad:** Crítica

**CVSS 3.1:** 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)
**CVSS 4.0:** 9.4 (`CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H`)

**CWE:** CWE-89 — Improper Neutralization of Special Elements used in an SQL Command
**CAPEC:** CAPEC-66 — SQL Injection
**OWASP:** A03:2021 — Injection
**MITRE ATT&CK:** T1190 — Exploit Public-Facing Application

**Activo afectado:** https://target.cl/login
**Parámetro vulnerable:** POST `username`

**Descripción:**
[Qué es. Cómo ocurre. Por qué ocurre aquí. Dónde ocurre. NO copiar definición OWASP genérica.]

**Impacto:**
Un atacante no autenticado podría ejecutar consultas arbitrarias sobre la
base de datos, obteniendo acceso a información sensible, credenciales,
tokens de sesión y potencialmente comprometiendo la totalidad de la
aplicación.

**Probabilidad de explotación:** Alta
**Confidence:** High
**Validación manual:** Sí

**Riesgo de negocio:**
Compromiso total de cuentas de clientes y fuga de información sensible
(PII, credenciales, datos transaccionales).

**Evidencia técnica:**
[requests, responses, headers, payloads, capturas, tokens, diffs, timing]

**PoC reproducible:**

Paso 1: Configuración inicial
Se configuró Burp Suite como proxy interceptador con el objetivo de
capturar las solicitudes enviadas al endpoint de autenticación.

Paso 2: Captura de la solicitud
\`\`\`http
POST /login HTTP/1.1
Host: target.cl
Content-Type: application/x-www-form-urlencoded

username=admin&password=test
\`\`\`
Se identificó que el parámetro "username" era reflejado directamente en
una consulta SQL backend.

Paso 3: Inyección SQL
\`\`\`bash
sqlmap -u https://target.cl/login \\
  --data="username=admin&password=test" \\
  -p username --risk=3 --level=5 --batch
\`\`\`
El parámetro "-p username" indica a sqlmap el parámetro objetivo. Los
parámetros "--risk=3" y "--level=5" incrementan la agresividad de las
pruebas.

Respuesta obtenida:
\`\`\`
[INFO] parameter 'username' appears to be injectable
[INFO] Type: time-based blind, error-based, UNION query
\`\`\`

Análisis:
La herramienta logró identificar múltiples vectores SQLi válidos,
confirmando que la entrada del usuario no es sanitizada adecuadamente.

Resultado final:
Se logró extraer información de la base de datos y enumerar usuarios.

**Remediación:**
- *Inmediata:* Implementar consultas parametrizadas / prepared statements.
- *Recomendada:* Validar y sanitizar todas las entradas del usuario.
- *Hardening adicional:* WAF con reglas específicas para SQL Injection,
  least-privilege en cuenta DB de la aplicación, monitoreo de queries
  anómalas, logging de errores SQL en SIEM.

**Referencias:**
- OWASP SQL Injection Prevention Cheat Sheet
- CWE-89: https://cwe.mitre.org/data/definitions/89.html
- CAPEC-66: https://capec.mitre.org/data/definitions/66.html
- PortSwigger SQLi Academy
- NIST SP 800-53 SI-10
```

## 9. Attack Chains

Por cada chain identificado:
- Diagrama (boxes y flechas).
- Componentes individuales con su CVSS.
- CVSS agregado del chain.
- PoC end-to-end.
- Impacto consolidado.

## 10. Matriz de Riesgo

| Criticidad | Cantidad |
|-----------|----------|
| Crítico | 2 |
| Alto | 4 |
| Medio | 7 |
| Bajo | 3 |
| Info | 12 |

Heatmap visual (impacto × probabilidad).

## 11. Impacto sobre CIA

| Hallazgo | Confidencialidad | Integridad | Disponibilidad |
|----------|------------------|------------|----------------|
| H1 SQLi | Alto | Alto | Alto |
| H2 BOLA | Alto | Medio | Bajo |

## 12. Estado de Explotabilidad

| Hallazgo | Explotable | Auth requerida | PoC adjunto |
|----------|-----------|----------------|-------------|
| H1 SQLi | Sí | No | Sí |

## 13. Timeline de Testing

```
2026-05-05  Reconocimiento pasivo
2026-05-06  Enumeración activa, fingerprinting
2026-05-07  Explotación H1, H2
2026-05-08  Validación y chaining
2026-05-09  Reporting
```

## 14. Limitaciones

```
- No se realizaron pruebas de DoS/DDoS por restricciones del cliente.
- El alcance excluyó subdominios de terceros (CDN, marketing).
- Las pruebas se realizaron exclusivamente en ambiente QA.
- La ventana fue 09:00–18:00 CLT, lunes a viernes.
```

## 16. Conclusión General

Estado general, madurez, exposición, urgencia, prioridades.

```
La evaluación realizada permitió identificar múltiples vulnerabilidades
críticas explotables remotamente, evidenciando debilidades en los
controles de validación de entrada, autenticación y segregación de
privilegios.

Se recomienda priorizar la remediación de los hallazgos críticos y altos
debido al impacto potencial sobre información sensible y continuidad
operacional.
```

## 17. Anexos

- Payloads utilizados.
- Wordlists.
- Herramientas y versiones.
- Hashes de evidencia.
- IOCs.
- Configuraciones encontradas.
- Scripts personalizados.
- Headers completos.

---

## Estilo de redacción

- **Texto justificado** en todos los párrafos del informe (configurar en exportadores).
- Sin guiones largos en cuerpo de texto (solo en títulos).
- Tildes correctas según RAE.
- Frase tipo "Un atacante podría..." en sección de Impacto.
- Referencias con links cuando aplique (OWASP, CWE, CVE, MITRE).
- Confidence siempre indicado (High/Medium/Low).
- Validación manual indicada (Sí/No) por hallazgo.

## Reproducibilidad y trazabilidad

Cada evidencia debe tener:
- Timestamp.
- Endpoint completo.
- Request ID si aplica.
- Herramienta usada y versión.
- Comando exacto.

## Generación

Ver script `scripts/generate_report.py` que produce: Markdown, TXT, DOCX, PDF, HTML, PPTX, JSON, SARIF.
