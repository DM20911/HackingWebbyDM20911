# Content Discovery & Fuzzing

## ffuf (rápido, flexible)

Ver también skill `ffuf-skill` ya instalada.

```bash
# Directorios
ffuf -u https://target.cl/FUZZ -w wordlists/raft-medium-directories.txt -mc 200,204,301,302,307,401,403,500 -ac

# Parámetros GET
ffuf -u "https://target.cl/api?FUZZ=test" -w wordlists/burp-parameter-names.txt -fs 0 -ac

# Subdominios virtual host
ffuf -u https://target.cl -H "Host: FUZZ.target.cl" -w subs.txt -fs 1234

# Recursivo
ffuf -u https://target.cl/FUZZ -w common.txt -recursion -recursion-depth 2

# Con autenticación (raw request)
ffuf -request raw.txt -request-proto https -w payloads.txt
```

Auto-calibración crítica: `-ac` y `-acc <regex>` para descartar falsos positivos.

## feroxbuster (recursivo, Rust, rápido)

```bash
feroxbuster -u https://target.cl -w wordlists/raft-medium.txt -t 50 -d 4 -x php,html,js
```

## dirsearch / gobuster

Alternativas. Útiles cuando ffuf falla por TLS quirks o Cloudflare.

## arjun (param discovery por reflexión + heurística)

```bash
arjun -u https://target.cl/api/endpoint -m POST
arjun -u https://target.cl/api -i endpoints.txt -t 20 -oJ arjun_out.json
```

## paramspider (parámetros desde Wayback)

```bash
paramspider -d target.cl -o params.txt
```

## qsreplace (sustituir valor de query)

```bash
cat urls.txt | qsreplace 'FUZZ' | httpx -mc 200
```

## kxss (XSS reflejado rápido)

```bash
cat urls.txt | kxss
```

## Wordlists recomendadas

- SecLists (`/usr/share/wordlists/SecLists`)
- raft-{small,medium,large}-{words,directories,files}
- burp-parameter-names
- common.txt (assetnote)
- assetnote wordlists (best-dns, best-paths, etc.)

## Anti-patrones

- ❌ Lanzar wordlist gigante sin auto-calibrar → ruido y falsos positivos.
- ❌ Fuzzear sin filtros (`-fc`, `-fs`, `-fw`) → resultados inservibles.
- ❌ Ignorar 401/403 — muchas veces son endpoints válidos sin auth o BOLA potencial.
