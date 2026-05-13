# Attack Chaining Patterns

Lo que diferencia hallazgos OK de hallazgos críticos.

## Chains famosos

### XSS → Account Takeover
```
Stored XSS en perfil → JS roba cookie/token → atacante usa sesión → ATO completo
```

### XSS → CSRF chain
```
XSS en target.cl → fetch a /api/change-email con cookie de víctima → email atacante → reset password → ATO
```

### IDOR → Privilege Escalation
```
GET /users/1 con token de user A → leakea hash/token de user 1 (admin) → atacante usa token admin
```

### IDOR → Mass Data Exfiltration
```
GET /orders/{1..1000000} → enumera todas las órdenes con datos PII
```

### SSRF → Cloud Takeover
```
SSRF en image-fetcher → http://169.254.169.254/iam/security-credentials/role → AWS keys → asume rol → S3 dump → BD dump
```

### SSRF → Internal Service → RCE
```
SSRF → http://localhost:6379 (Redis sin auth) → SET malicious cron job → RCE en host
SSRF → http://localhost:8500 (Consul) → register service → RCE
SSRF → Elasticsearch → leer indices con tokens → ATO de cuentas leakeadas
```

### Subdomain Takeover → Phishing / Cookie Theft
```
abandoned.target.cl → CNAME apunta a S3/Heroku/GitHub Pages no claimed → atacante claima → sirve HTML malicioso desde subdomain legítimo → cookies con domain=.target.cl son enviadas
```

### SSTI → RCE
```
SSTI Jinja2 en email template editor → {{ ''.__class__.__mro__[1].__subclasses__()[XX]('id', shell=True...).read() }} → RCE
```

### Open Redirect → OAuth Token Theft
```
Open redirect en target.cl/login?next=// → redirect_uri abuse → token de OAuth llega a atacante → ATO en provider
```

### CRLF Injection → Session Fixation / Cache Poisoning
```
CRLF en header injectable → Set-Cookie atacante → fija sesión víctima
CRLF + cache → poison de respuestas para todos
```

### File Upload → RCE
```
Upload .php.jpg → server interpreta como PHP por misconfig Apache → RCE
Upload .htaccess → reescribe ejecución de directorio → RCE
Upload SVG con XSS + script → stored XSS server-side render PDF → SSRF
```

### Insecure Deserialization → RCE
```
Endpoint acepta cookie/param serializado Java → ysoserial CommonsCollections → RCE
```

### JWT Crack → Account Takeover
```
JWT HS256 con secret débil → crack offline → forjar JWT con role=admin → admin access
```

### CORS Misconfig → API Token Theft
```
target.cl/api con Access-Control-Allow-Origin: <reflected> + Credentials: true
→ atacante.cl carga script que fetcha api con cookies víctima → leak respuesta
```

### CSP missing + Self-XSS + Login CSRF
```
Login CSRF loguea víctima en cuenta atacante → víctima hace acción → atacante ve "self-XSS" pero en cuenta de víctima → ATO real
```

### Race Condition → Coupon Abuse
```
Coupon "10% off, single use" → 100 requests paralelos → 100 órdenes con descuento → pérdida cuantificable
```

### Cache Poisoning → DoS / XSS de masa
```
Header no-keyed reflejado → atacante envenena cache de homepage → todos los usuarios reciben HTML modificado
```

## Cómo modelarlo en informe

Cada chain debe tener:
1. **Diagrama** del flujo (boxes y flechas).
2. **Componentes individuales** listados (cada uno con su CVSS/CWE).
3. **CVSS del chain completo** (suele ser mayor que cualquier individual).
4. **PoC end-to-end** que demuestra el chain.
5. **Impacto agregado** (ej: "compromiso completo de tenant + lateral a otros tenants").

## Reasoning AI-asistido

Pedir al modelo:
> "Tengo estos hallazgos individuales: [lista]. ¿Qué chains pueden formarse? Priorizar por impacto y viabilidad."

LLM con contexto del stack puede sugerir chains no obvios.
