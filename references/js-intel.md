# JavaScript Analysis / Intelligence

## Recolección de JS bundles

```bash
katana -u https://target.cl -d 5 -jc | grep "\.js$" | sort -u > js_files.txt
hakrawler -url https://target.cl -depth 3 -plain | grep "\.js$" >> js_files.txt
```

Bajar todos:
```bash
mkdir -p js && wget -i js_files.txt -P js/
```

## LinkFinder — extraer endpoints

```bash
linkfinder -i js/main.chunk.js -o cli
linkfinder -i 'js/*.js' -o html_report.html

# En conjunto
for f in js/*.js; do linkfinder -i "$f" -o cli 2>/dev/null; done | sort -u > endpoints_from_js.txt
```

## SecretFinder — credenciales hardcoded

```bash
SecretFinder -i js/main.js -o cli
for f in js/*.js; do SecretFinder -i "$f" -o cli 2>/dev/null; done > secrets.txt
```

Patrones que encuentra: AWS keys, Slack tokens, JWT secrets, API keys, Google API, Stripe, Twilio, Heroku, Mailgun, GitHub PAT.

## Source maps (HUGE)

Si encuentras `.map`:
```bash
curl -sk "https://target.cl/static/js/main.chunk.js.map" -o /tmp/main.map
python3 -c "import json; d=json.load(open('/tmp/main.map')); [print(s) for s in d.get('sources',[])]"
```

Recupera código fuente original (TypeScript, comentarios, paths internos).

## retire.js — librerías vulnerables

```bash
retire --path js/
retire --js https://target.cl
```

## semgrep para JS

```bash
semgrep --config p/javascript js/
semgrep --config p/owasp-top-ten js/
semgrep --config p/security-audit js/
```

## trufflehog en JS y repos

```bash
trufflehog filesystem ./js
trufflehog git https://github.com/target/repo --branch main
trufflehog github --org=target
```

## gitleaks

```bash
gitleaks detect --source ./repo -v
gitleaks detect --source . --report-format json --report-path leaks.json
```

## Patterns to grep manually

```bash
grep -rEi "(api[_-]?key|secret|password|token|bearer|aws_access|firebase|mongodb)" js/
grep -rE "https?://[^\"' ]{10,}" js/ | sort -u
grep -rE "/[a-z0-9_/-]{8,}" js/ | sort -u   # rutas internas
```

## DOM XSS sources/sinks (ver xss.md)

## Service workers

```bash
curl https://target.cl/service-worker.js
curl https://target.cl/sw.js
```

A veces cachean rutas internas no expuestas en navegación normal.

## Webpack chunks

Lista de chunks en el bundle principal:
```bash
grep -oE '"[a-z0-9-]+":"[a-f0-9]{20}"' js/main.js  # mapping chunkID → hash
```
Luego descargar uno por uno.

## SPA routing

Buscar definiciones de rutas (React Router, Vue Router, Angular):
```bash
grep -E "(path:|Route|RouterModule)" js/main.js | head -50
```
