# MCP Ecosystem

## Catálogo de MCPs ofensivos

### Existentes / públicos
- **Burp Suite MCP Server (oficial PortSwigger)** — extensión BApp que expone Repeater, scanner, tráfico interceptado y otras funciones de Burp a través de MCP. Autoría: Daniel S y Daniel Allen (PortSwigger).
  - BApp Store: https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc
  - Repo: https://github.com/portswigger/mcp-server
  - Instalación: BApp Store dentro de Burp → activar la pestaña MCP → usar el botón installer para auto-configurar Claude Desktop, o configurar el cliente MCP manualmente.
- **anthropic-fetch / brave-search MCP** — recon pasivo, OSINT.
- **github MCP** — secret hunting en repos.
- **shodan MCP** — host intelligence (depende de plan).

### A crear (alta prioridad)

#### `burp-mcp` ya existe oficial → ver sección "Existentes / públicos" arriba
PortSwigger publicó el MCP Server oficial. Ya no es un MCP "a crear" — usar el oficial.

#### `nuclei-mcp`
- `run_templates(target, severity, tags)`
- `create_custom_template(yaml)`
- `map_cves(target)`
- `correlate_findings(findings[])`
- `prioritize_risk(findings[])`
- `auto_verify(finding)`

#### `sqli-mcp`
- `detect_sqli(url, params)`
- `fingerprint_db(url)`
- `dump_schema(url)`
- `tamper_payloads(payload, waf)`
- `evade_waf(waf_name, technique)`
- `blind_sqli_optimizer(url)`

#### `xss-mcp`
- `payload_generation(context)`
- `context_detection(reflection)`
- `dom_xss_analysis(js_bundle)`
- `csp_bypass_generation(policy)`
- `blind_xss_tracking(callback)`

#### `api-security-mcp`
- `import_openapi(url|file)`
- `discover_shadow_api(domain)`
- `test_bola(endpoints[], tokens[])`
- `jwt_analysis(token)`
- `graphql_introspection(url)`
- `auth_bypass_detection(endpoint)`

#### `auth-mcp`
- `weak_jwt_detection(token, wordlist)`
- `alg_none_attack(token)`
- `auth_flow_mapping(target)`
- `session_fixation_detection(target)`
- `race_condition_testing(endpoint)`

#### `advanced-web-vuln-mcp`
- `detect_ssrf(url, param)`
- `detect_ssti(url, param)`
- `generate_deserialization_chain(lang, gadget)`
- `out_of_band_tracking()`
- `cloud_metadata_attack(target)`

#### `cms-mcp`
- `enumerate_plugins(url)`
- `detect_cves(url)`
- `weak_admin_detection(url)`
- `exploit_matching(cve)`

#### `js-analysis-mcp`
- `endpoint_extraction(js_url)`
- `secret_detection(js_url)`
- `source_map_analysis(map_url)`
- `client_side_vuln_detection(js_url)`

#### `cloud-web-mcp`
- `enumerate_s3(target)`
- `detect_public_buckets(target)`
- `k8s_exposure(target)`
- `iam_misconfig(creds)`
- `ci_cd_leak_detection(repo)`

#### `reporting-mcp`
- `generate_report(findings[], template, format)`
- `generate_cvss(vector)`
- `generate_executive_summary(findings[])`
- `create_attack_chain(findings[])`
- `normalize_findings(raw[])`
- `export_docx(report)`
- `export_pdf(report)`

#### `finding-knowledge-mcp`
- `deduplicate_findings(findings[])`
- `correlate_findings(findings[])`
- `classify_cwe(description)`
- `map_owasp(finding)`
- `estimate_business_impact(finding, context)`

#### `cvss-engine-mcp`
- `calculate_cvss31(metrics)`
- `calculate_cvss40(metrics)`
- `explain_vector(vector)`
- `estimate_severity(description)`

#### `bugbounty-brain-mcp`
- `save_methodology(name, steps)`
- `save_bypass(waf, technique)`
- `save_payload(category, payload, context)`
- `rank_exploits(category)`
- `cluster_by_technology(findings[])`

#### `web-attack-chain-mcp`
- `correlate(findings[])`
- `suggest_chain(finding)` → ej: SSRF → Redis → RCE
- `generate_chain_poc(chain)`

## Cómo configurar un MCP en Claude Code

```bash
# 1. Instalar el server (npm o python)
npm install -g @owner/some-mcp-server

# 2. Agregarlo a Claude Code
claude mcp add some-mcp -- some-mcp-server --arg=value

# 3. Verificar
claude mcp list
claude mcp get some-mcp

# 4. Reiniciar Claude Code y probar invocación
```

## Cómo configurar un MCP en Claude Desktop

1. Settings → Capabilities → MCP servers (o Connectors).
2. "Add custom MCP".
3. URL del server o comando local.
4. Confirmar permisos al primer uso.

## Tutorial paso a paso (cuando el usuario lo pide)

```bash
# Crear un MCP propio en Python
pip install mcp[cli]

# Esqueleto
cat > my_offensive_mcp.py <<'EOF'
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("offensive-recon")

@mcp.tool()
def subdomains(domain: str) -> list[str]:
    """Enumera subdominios pasivos del dominio dado."""
    import subprocess
    out = subprocess.check_output(["subfinder", "-d", domain, "-silent"])
    return out.decode().splitlines()

if __name__ == "__main__":
    mcp.run()
EOF

# Registrar
claude mcp add offensive-recon -- python my_offensive_mcp.py
```

## Patrón operativo

- Por defecto: ejecutar herramientas vía Bash (más simple, menos overhead).
- Crear MCP cuando: quieres reusar capacidad entre sesiones, multi-step con state, o exponerla a otros agentes.
- MCPs ofensivos pueden requerir aprobación explícita (ver CLAUDE.md global).
