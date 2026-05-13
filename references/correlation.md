# Vulnerability Correlation Engine

## Por qué importa

Dos Lows pueden formar un Critical. Scanners reportan en silos; el atacante encadena.

## Reglas de correlación a aplicar siempre

| Hallazgo A | + Hallazgo B | = |
|-----------|-----------|---|
| Open redirect | OAuth flow | Token theft → ATO |
| CORS reflected | API auth via cookie | Token exfiltration cross-origin |
| XSS | Cookie sin HttpOnly | ATO directo |
| XSS | CSRF en endpoint sensible | Acción no autorizada via XSS |
| Subdomain takeover | Cookie con `domain=.target.cl` | Cookie/CSRF token theft |
| Email enumeration | Brute-force sin rate-limit | Credential stuffing efectivo |
| Verbose errors | SQLi blind sospecha | Confirmación de injection |
| File upload sin validación | Path traversal | RCE / web shell |
| SSRF | Cualquier servicio interno expuesto | Lateral / RCE |
| Mass assignment | Endpoint sin function-level auth | Priv esc trivial |
| Source map expuesto | Cualquier vuln cliente-side | Mapeo total + nuevos vectores |
| Hardcoded secret en JS | Cualquier service externo | Acceso directo a backend service |
| Race condition | Coupon/refund/withdraw | Pérdida monetaria |

## Cómo correlacionar manualmente

1. Listar todos los hallazgos.
2. Tag cada uno con: tipo (CWE), capa afectada (frontend/backend/infra/cloud), gravedad individual, requisitos (auth/anon).
3. Buscar combinaciones que multipliquen impacto.
4. Documentar como **chain** separado en el informe (ver `attack-chains.md`).

## Reasoning AI

Para correlación a escala:
- Embeddings de descripciones de hallazgos para clustering.
- LLM con contexto de los hallazgos pidiendo "qué chains forman".
- Knowledge graph (ver `ai-memory.md`) para queries tipo: "dame todos los SSRFs en hosts con Redis interno".

## Output esperado

En el informe, sección **Attack Chains**:
- Tabla con: Chain → Componentes → CVSS agregado → Impacto.
- Diagrama por chain.
- PoC end-to-end por chain.
