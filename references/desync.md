# HTTP Desync / Request Smuggling

## Tipos clásicos (HTTP/1.1)

- **CL.TE** — frontend usa `Content-Length`, backend usa `Transfer-Encoding`.
- **TE.CL** — al revés.
- **TE.TE** — ambos usan TE pero uno se puede ofuscar (`Transfer-Encoding: chunked\r\nTransfer-Encoding: x`).

## HTTP/2 desync

- H2.CL — H2 frontend → H1 backend con CL inyectado.
- H2.TE — same con TE.
- H2 request splitting via header injection.

## Detección

```bash
# Smuggler (Defparam)
smuggler -u https://target.cl

# Burp HTTP Request Smuggler extension (PortSwigger, gold standard)
# Probe → si confirma, generate exploit
```

## Payload CL.TE básico

```http
POST / HTTP/1.1
Host: target.cl
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```

## Impactos

- Cache poisoning (servir respuesta de otra request a otros usuarios).
- Bypass de WAF / auth (request smuggleada no pasa por el frontend).
- Robo de requests de otros usuarios (sus headers acaban en tu request).
- Reflection del cookie del próximo cliente.

## Tips

- Probar tras CDN (Cloudflare, Akamai, AWS ALB, F5).
- HTTP/2 → HTTP/1 downgrade en backend = vector más común hoy.
- Usar Burp Repeater "Send group in single packet" para confirmar timing.

## Recursos
- https://portswigger.net/web-security/request-smuggling
- https://github.com/PortSwigger/http-request-smuggler
