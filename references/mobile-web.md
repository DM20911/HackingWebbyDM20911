# Mobile ↔ Web Correlation

Las APIs móviles suelen tener menos controles que las web. Compara siempre.

## Setup

### Android
- Frida + Objection (bypass SSL pinning, root detection)
- jadx / apktool (decompile)
- Burp como proxy con CA en system store (root) o Magisk module
- Ver skill `android-pentest` para flujo completo

### iOS
- Frida en jailbroken / corellium
- Hopper / Ghidra para decompile
- Burp con CA en Profiles + jailbreak para system trust

## Qué buscar

### Hardcoded secrets
```bash
apkleaks -f app.apk
strings app.apk | grep -iE "(api|key|secret|token)"

# IPA
class-dump-z app | grep -i secret
strings Payload/App.app/App | grep -i api_key
```

### Endpoints distintos vs web
- Mobile suele tener `/api/v1/mobile/...` separado.
- Misma funcionalidad pero sin rate-limit web.
- Auth con header custom (`X-Mobile-Token`) sin validación robusta.
- Endpoints debug `/debug`, `/test` solo en mobile.

### JWT reuse
- Token mobile aceptado en web → bypass de MFA.
- Token web aceptado en mobile.
- Refresh token de larga duración (mobile suele 90 días+).
- `device_id` no validado.

### Deep links / Intent injection (Android)
Ver `android-pentest` skill.

### WebViews
- `setJavaScriptEnabled(true)` + `loadUrl(usuario)` → XSS local con acceso a JS-Java bridge → RCE en device.
- `addJavascriptInterface` con clase poderosa.

### Certificate pinning
Si presente, bypass con:
```bash
objection -g com.target.app explore
> android sslpinning disable
```

## Patrón comparativo

Para cada endpoint web, ejecutar el equivalente mobile y diffear:
- Status code
- Response body
- Headers requeridos
- Validaciones (rate-limit, MFA, auth)

Si mobile permite algo que web no → reportar como hallazgo separado de la web.

## Tips operativos

- Capturar tráfico mobile con `mitmproxy` + transparent proxy si Burp falla con HTTP/2.
- Algunos endpoints mobile usan gRPC / Protobuf — necesitas decodificar con `proto-buster` o decompile del .proto desde el binario.
- WebSockets en mobile suelen estar peor protegidos (auth solo en handshake, no en cada msg).
