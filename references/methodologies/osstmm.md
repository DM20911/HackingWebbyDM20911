# OSSTMM — Open Source Security Testing Methodology Manual

## Origen y autoridad
Publicada por ISECOM (Institute for Security and Open Methodologies). Versión 3 es la actual; v4 en draft. Es la metodología más **holística** (no solo web) y la única con **métricas científicas** (RAV — Risk Assessment Values).

Sitio oficial: https://www.isecom.org/OSSTMM.3.pdf

## Filosofía
A diferencia de PTES/NIST que se enfocan en proceso, OSSTMM se enfoca en **medir la postura de seguridad** con números reproducibles. Cada test produce un score numérico (RAV) que permite comparar entre auditorías y entre clientes.

## Los 5 canales (Channels)
OSSTMM evalúa la seguridad por canal de interacción:

| Canal | Cobertura |
|-------|-----------|
| **Human** | Ingeniería social, phishing, vishing |
| **Physical** | Tailgating, dumpster diving, lock picking |
| **Wireless** | WiFi, Bluetooth, NFC, RFID, IR |
| **Telecommunications** | PBX, fax, voicemail, mobile network |
| **Data Networks** | Web, API, network protocols, lo que aquí nos importa |

Para auditorías web ofensivas, el canal relevante es **Data Networks**, pero un pentest completo de empresa puede combinar varios canales.

## Los 4 puntos de medición (POSTURE)

Por cada canal:
- **Porosity** — cuántos puntos de entrada existen.
- **Controls** — qué tan bien están protegidos esos puntos.
- **Limitations** — debilidades conocidas (vulns, misconfigs).
- **OpSec** — segregación operacional.

## Las 17 categorías de Module Tests (Data Networks)

1. Posture Review
2. Logistics
3. Active Detection Verification
4. Visibility Audit
5. Access Verification
6. Trust Verification
7. Controls Verification
8. Process Verification
9. Configuration Verification
10. Property Validation
11. Segregation Review
12. Exposure Verification
13. Competitive Intelligence Scouting
14. Quarantine Verification
15. Privileges Audit
16. Survivability Validation
17. Alert and Log Review

## RAV (Risk Assessment Values)

Score numérico que combina:
- **OpSec score** (cómo está la seguridad operacional)
- **Controls score** (qué tan robustos son los controles)
- **Limitations score** (cuántas vulns/debilidades)

Resultado: número 0-100% que permite **comparar postura** entre engagements del mismo cliente en el tiempo, o entre clientes similares.

## Cómo aplicar OSSTMM a una auditoría web

| Module Test | Acción concreta web/API |
|-------------|--------------------------|
| Visibility Audit | Inventario subs + endpoints + tech stack via recon pasivo. ¿Qué se ve desde Internet sin auth? |
| Access Verification | ¿Se requiere auth donde corresponde? Anonymous → privileged paths. |
| Trust Verification | ¿La app confía en headers cliente (XFF, Cookie, Origin) sin validar? CORS reflected, CSP self con dominios CDN third-party. |
| Controls Verification | WAF presente? Rate-limit? CSP/HSTS? SameSite? MFA? |
| Configuration Verification | Headers de seguridad, métodos HTTP permitidos, debug endpoints expuestos, source maps. |
| Segregation Review | ¿Tenant isolation correcto en multi-tenant? ¿Backend admin separado del público? |
| Exposure Verification | Datos sensibles en respuestas, source maps, JS bundles, errors verbosos. |
| Privileges Audit | RBAC funciona como debería? IDOR/BOLA tests. |
| Survivability | Tolerancia a abuso (rate-limit, race conditions, DoS prevention). |
| Alert and Log Review | ¿El cliente detecta nuestros ataques? Coordinación con SOC. |

## Particularidades de OSSTMM
- **Métricas numéricas** que permiten benchmarking.
- **Mayor énfasis en survivability** (resiliencia, no solo "exists vuln Y/N").
- **Considera ingeniería social y físico** si scope lo incluye.
- **Más teórico** — la curva de aprendizaje es mayor que WSTG.
- Documentación extensa pero menos comunidad práctica.

## Cuándo usar OSSTMM
- **Programas de seguridad maduros** que necesitan métricas comparables en el tiempo.
- **Auditorías multi-canal** (no solo web — también red interna, física, social).
- **Compliance internacional** (citada en marcos europeos).
- Cuando el cliente busca **trending de postura** entre auditorías consecutivas.

## Cuándo NO es ideal
- Pentest web one-shot rápido → WSTG es más directo.
- Bug bounty → no encaja con el formato.
- Equipo sin experiencia OSSTMM → curva de aprendizaje cara.

## Combinaciones recomendadas
- **OSSTMM + WSTG** → métricas RAV con detalle técnico web.
- **OSSTMM + PTES** → audit holística profesional.
- **OSSTMM solo** → assessment de programa de seguridad completo (todos los canales).
