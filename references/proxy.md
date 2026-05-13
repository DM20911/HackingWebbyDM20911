# Web Proxy / Interceptación

## Burp Suite (estándar de oro)

- **Proxy** → intercept on/off, history, repeater, intruder, comparer, decoder, sequencer
- **Scanner** (Pro) → active + passive
- **Collaborator** → OOB para SSRF/XSS blind/SSTI/RCE OOB
- **Extensions imprescindibles:**
  - Autorize (BOLA/IDOR auto)
  - Param Miner (cache poisoning, hidden params, headers)
  - Turbo Intruder (race conditions, throughput alto)
  - JWT Editor
  - Logger++
  - Hackvertor (encoding chains)
  - Active Scan++ (más checks)
  - Backslash Powered Scanner
  - SAML Raider
  - InQL (GraphQL)
  - JS Link Finder
  - HTTP Request Smuggler
  - Stepper

## OWASP ZAP

Open source, scripteable. Útil para CI/CD y baseline scans.
```bash
zap-baseline.py -t https://target.cl -r baseline.html
zap-full-scan.py -t https://target.cl -r full.html
zap-api-scan.py -t openapi.json -f openapi -r api.html
```

## Caido

Alternativa moderna a Burp (Rust, UI Tauri). Replays y workflows visuales. Bueno para coexistir con Burp.

## mitmproxy

CLI/scripteable Python. Ideal para automatizar:
```bash
mitmdump -s addon.py -p 8080
```

Útil para mobile app interception (Android/iOS) con CA instalada.

## proxify (ProjectDiscovery)

Captura tráfico para análisis posterior.
```bash
proxify -output traffic/
```

## HTTP Toolkit

GUI moderna. Bueno para QA y devs no-pentesters.

## Patrones operativos

- **Siempre** usar Burp/ZAP como upstream cuando corras herramientas (`-x http://127.0.0.1:8080`).
- Un proyecto Burp por engagement; guardar como `.burp` en el directorio del cliente.
- Usar **scope** estricto en Burp para no enviar tráfico fuera de alcance.
- **Match & Replace** para inyectar headers de auth en todas las requests.
- **Macros** para mantener sesión viva durante scans.
