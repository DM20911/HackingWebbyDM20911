# OPSEC Ofensivo

## Por qué importa

- En pentest autorizado: evitar bloqueos del SOC del cliente que paralicen el engagement.
- En red team: evitar detección.
- En bug bounty: respetar rate-limits y no afectar producción.
- Siempre: no exponer tu infra real (IP, headers, fingerprints).

## Infraestructura rotada

- **Proxies residenciales** (BrightData, NetNut) para fuzzing pesado.
- **Cloud redirectors** (small VPS en GCP/AWS/DO) entre tu IP y el target.
- **Tor / proxychains** solo si latencia tolerable.
- **VPN comercial** mínimo (Mullvad, ProtonVPN) — nunca conectar directo desde IP residencial.

## Headers / fingerprints

- Cambiar `User-Agent` a navegador realista (no `python-requests`, no `curl/7.x`).
- TLS fingerprint: `curl_chrome` o `curl-impersonate` para evitar JA3 fingerprinting.
- Evitar headers únicos por tu pentest framework (algunos scanners agregan `X-Burp-*`).

## Rate limiting consciente

```bash
nuclei -rate-limit 50    # default 150 puede ser muy ruidoso
ffuf -rate 100
sqlmap --delay=1 --threads=1
```

## Separar tráfico

- Browser separado (perfil Chrome dedicado para target).
- Proxy diferente para recon vs explotación.
- No mezclar tráfico personal con engagement.

## Logging propio

- Toda request enviada al target debe quedar en log local con timestamp.
- Útil para reporte (timeline) y para defenderte si el cliente acusa daño.
- Burp project file + HAR exports + script logs.

## Atribución

- Nombre de tu callback domain — usar genérico (`oast.fun`, no `dm20911.cl`).
- Subdomain del Burp Collaborator/interactsh es público — atribuible si se loguea.
- En red team simular TTPs de un actor conocido (purple team).

## Tráfico OOB

- Burp Collaborator → registra en logs del cliente como `*.oastify.com`.
- interactsh self-hosted en VPS → mejor OPSEC pero más setup.
- DNS callbacks visibles en logs DNS del cliente.

## "Do no harm"

- No correr tools que pueden romper datos (`sqlmap --os-shell` sin pre-acuerdo).
- No correr DoS (incluyendo accidental por concurrencia alta).
- No tocar SCADA/IoT/medical sin scope expreso.
- Confirmar antes de cualquier cosa potencialmente destructiva.
- Siempre **tener canal directo con el SOC del cliente** durante el engagement.

## Checklist pre-engagement

- [ ] Scope firmado y rango IP/dominios escritos.
- [ ] Ventana de pruebas acordada (días/horas).
- [ ] Contactos emergencia 24/7 del cliente.
- [ ] Acuerdo sobre exfiltración (¿proof o full dump?).
- [ ] Política de cuentas creadas (eliminar al terminar).
- [ ] Evidencia retention (cuánto tiempo guardar).
- [ ] Disclosure responsable (timeframe).
- [ ] Whitelisting de IPs si es necesario para no triggerar WAF.
