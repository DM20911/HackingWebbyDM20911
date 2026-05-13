# Web Cache Deception / Poisoning

## Cache Deception

Cliente fuerza a la caché a almacenar contenido autenticado:
```
GET /profile/foo.css HTTP/1.1
```
Si el cache obedece extensión y el server sirve `/profile` (ignorando `.css` en path), el atacante puede luego pedir `/profile/foo.css` sin auth y recibir el `/profile` cacheado del usuario A.

## Cache Poisoning

Atacante envia request con header no-keyed que afecta la respuesta:

```
GET / HTTP/1.1
Host: target.cl
X-Forwarded-Host: atacker.cl
```

Si la respuesta refleja `X-Forwarded-Host` y la caché solo keyea por path → toda solicitud subsiguiente recibe HTML con dominio atacker.

## Param Miner (extensión Burp)

Detecta:
- Headers no-keyed que afectan respuesta.
- Parámetros ocultos.
- Cookies que cambian respuesta.

```
Right-click → Param Miner → Guess headers / params / cookies
```

## Headers comunes para probar

```
X-Forwarded-Host, X-Host, X-Forwarded-Server
X-Forwarded-Scheme, X-Forwarded-Proto, X-Forwarded-Port
X-Original-URL, X-Rewrite-URL
X-Forwarded-For (a veces afecta logs/respuesta)
True-Client-IP, X-Cluster-Client-IP
X-Accel-Internal
```

## Cache key determination

Probar variaciones para entender qué entra en la key:
- Case-sensitive del path? `/HOME` vs `/home`
- Trailing slash? `/page` vs `/page/`
- Param order? `?a=1&b=2` vs `?b=2&a=1`
- Fat GET (params en cuerpo de GET)
- HTTP method (HEAD usado para poison de GET)

## Impacto

- DoS si poison incluye header rompedor.
- XSS si poison incluye `<script>` reflejado.
- Account takeover si poison incluye `<base href="//atacker">`.
- Phishing si poison cambia branding/dominio.

## Recursos
- https://portswigger.net/web-security/web-cache-poisoning
- https://portswigger.net/web-security/web-cache-deception
