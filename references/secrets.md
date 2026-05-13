# Secret Hunting

## Repos

```bash
# trufflehog (multi-source)
trufflehog github --org=target --concurrency=10
trufflehog gitlab --token=$GLAB --groups=target
trufflehog git https://github.com/target/repo --branch=main
trufflehog filesystem ./local-repo
trufflehog s3 --bucket=target-uploads
trufflehog docker --image=target/app:latest

# gitleaks
gitleaks detect --source ./repo -v --report-format json --report-path leaks.json
gitleaks detect --no-git -v --source ./web-files

# git-secrets (AWS-focused)
git secrets --scan
```

## GitHub dorks

```
"target.cl" password
"target.cl" filename:.env
"target.cl" extension:json api_key
org:target filename:credentials
org:target filename:.env
"jdbc:mysql://" "target"
"BEGIN RSA PRIVATE KEY" target
```

Tools: `gh-dorker`, `github-search`, manual con UI.

## JS / mobile / CI/CD

```bash
# Frontend bundles
SecretFinder -i 'js/*.js' -o cli

# APK
apkleaks -f app.apk
jadx-gui app.apk  # decompila y busca con grep

# IPA
class-dump-z + grep
```

## Slack / Discord / docs

- Slack token search: `xoxb-`, `xoxp-`
- Discord webhook: `https://discord.com/api/webhooks/`
- Slack workspace search por `password`, `secret`, `aws_access`.

## Dependency confusion / typosquatting

```bash
# confused (Visma)
confused -l npm package.json
confused -l pip requirements.txt
confused -l mvn pom.xml
```

## Validación de secrets encontrados

Antes de reportar, verifica que el secret está vivo:

```bash
# AWS key
aws sts get-caller-identity   # con keys exportadas

# GitHub PAT
curl -H "Authorization: token ghp_..." https://api.github.com/user

# Slack token
curl -X POST -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test

# Stripe
curl https://api.stripe.com/v1/charges -u sk_live_...:
```

Reportar key revocada/expirada baja la severidad y la credibilidad.

## Después del hallazgo

- **Notificar inmediatamente** al cliente para rotar (no esperar al informe).
- Documentar:
  - Dónde estaba (commit hash, archivo, línea).
  - Cuándo fue commiteada (puede llevar años expuesta).
  - Servicios afectados.
  - Privilegios del key.
