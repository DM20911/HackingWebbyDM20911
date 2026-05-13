# Auth / JWT / OAuth / OIDC / SAML / Sessions

## JWT — análisis y ataque

```bash
# Decode + análisis
jwt_tool eyJhbGc...
jwt_tool eyJhbGc... -M at        # alg=none
jwt_tool eyJhbGc... -M ks        # key confusion (RS256→HS256)
jwt_tool eyJhbGc... -C -d wordlist.txt   # crack secret
jwt_tool eyJhbGc... -X k -pk attacker.jwks   # jku injection
```

Vectores principales:
- `alg: none` aceptado.
- HS256 con clave débil → crack con `jwt-cracker` o hashcat (mode 16500).
- RS256→HS256 confusion (firmar con la pública como HMAC key).
- `jku`/`x5u` apuntando a JWKS controlado por atacante.
- `kid` SQLi/path traversal.
- Sin verificación de expiración.
- `aud`/`iss` no validados.
- Replay (mismo JWT funciona indefinidamente).

## OAuth2 / OIDC

Vulnerabilidades comunes:
- **redirect_uri abuse:** wildcard, subdomain, path traversal, unicode bypass.
  - `redirect_uri=https://atacker.cl@target.cl/cb`
  - `redirect_uri=https://target.cl.atacker.cl/cb`
  - `redirect_uri=https://target.cl/cb/../atacker`
- **CSRF en `state`:** falta de `state` o no validado → ataque login CSRF / account hijack.
- **PKCE missing/weak:** flujo público sin PKCE.
- **Implicit flow** todavía en uso (deprecado).
- **Scope escalation:** pedir scope adicional sin re-consent.
- **Authorization code reuse.**
- **Client secret en frontend** (SPA leakeando).
- **`response_type=token` en confidential client.**
- **Mix-up attack** (provider sustituido).

Test:
```bash
# Verificar PKCE requerido
curl "https://idp/authorize?response_type=code&client_id=X&redirect_uri=https://app.cl/cb"

# Probar redirect_uri variantes
for r in "https://app.cl/cb" "https://app.cl.atacker.cl/cb" "https://app.cl/cb/../atacker" "https://atacker.cl"; do
  curl -sI "https://idp/authorize?...&redirect_uri=$r" | head -3
done
```

## SAML

- **XML Signature Wrapping (XSW):** mover Assertion fuera del Signature.
- **Comment injection:** `admin@x.cl<!---->.atacker.cl` puede leer como `admin@x.cl`.
- **Signature stripping** si `Signature` opcional.
- **Replay** (sin `OneTimeUse`).
- **Audience restriction missing.**

Tool: SAML Raider (extensión Burp).

## Sessions

- Cookie sin `HttpOnly`, `Secure`, `SameSite`.
- Session ID predecible / corto.
- Session fixation (no rota tras login).
- Session no expira en logout server-side.
- Concurrencia (mismo user, varias sesiones, sin notificación).

## MFA bypass patterns

- Endpoint `/verify-mfa` sin sesión válida.
- TOTP brute (sin rate-limit en código de 6 dígitos).
- Reusar código antes de expirar.
- Race condition en validación.
- Saltarse paso vía cookie `mfa_verified=true` desde response anterior.
- Response manipulation (`{"mfa_required": false}` desde Burp).

## Password reset / account recovery

- Token predecible / sin expiración / reusable.
- Host header poisoning para enviar link a dominio atacante:
  ```
  Host: atacker.cl
  ```
- Email enumeration (mensajes distintos para usuario válido vs no válido).
- Skip MFA tras reset.

## Brute / credential stuffing

```bash
hydra -l admin -P rockyou.txt https-post-form "/login:username=^USER^&password=^PASS^:F=invalid"
patator http_fuzz url=https://target.cl/login method=POST body='u=^USER^&p=^PASS^' 0=users.txt 1=passwords.txt
```

Burp Turbo Intruder para alta concurrencia + race.

## Race conditions en auth

Ver `race-conditions.md`. Útil contra: rate-limit, MFA, coupon, withdrawal, transfer.
