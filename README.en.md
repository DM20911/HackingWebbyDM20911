<p align="center">
  <img src="./assets/banner.svg" alt="HackingWebbyDM20911 — Offensive Web Hacking Copilot" width="100%"/>
</p>

# 🕷️ HackingWebbyDM20911

> **Offensive Web Hacking copilot** — recon, exploitation, AI-assisted correlation, attack chaining and senior multi-format reporting.

🌐 **Languages:** [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md)

Claude Code / Claude Desktop skill for offensive web pentesting professionals. Bundles methodology, tooling, recommended MCPs and a built-in multi-format report generator (Markdown, Word, PDF, HTML, PowerPoint, JSON, SARIF).

---

## What it does

End-to-end offensive copilot:

- **Recon / OSINT / ASM** — subdomains, endpoints, JS intel, source maps, secret hunting.
- **Fuzzing & Scanners** — ffuf, feroxbuster, nuclei, sqlmap, dalfox, XSStrike.
- **Exploitation** — SQLi, XSS, SSRF, SSTI, deserialization, IDOR/BOLA, mass assignment.
- **Deep API testing** — REST, GraphQL (introspection, batching, depth, alias), SOAP.
- **Auth deep dive** — JWT, OAuth2/OIDC, SAML, sessions, MFA bypass, race conditions.
- **Cloud + K8s + CI/CD** — AWS/GCP/Azure SSRF + IAM, kube-hunter, GitHub Actions abuse.
- **Browser security** — CSP bypass, postMessage, Service Workers, XS-Leaks, SameSite.
- **Business logic abuse** — workflows, race, coupon/refund/transfer, escalation.
- **Attack chaining** — smart correlation to build critical chains.
- **Senior reporting** — CVSS 3.1 + 4.0, CWE, CAPEC, ATT&CK, attack chains, evidence; export to md/docx/pdf/html/pptx.

---

## How to invoke

In **Claude Code** or **Claude Desktop**:

- `/hackweb`
- `/HackingWebbyDM20911`
- *"audit this web app"*, *"recon target.cl"*, *"pentest this API"*
- *"exploit this vuln"*, *"hunt BOLA / IDOR"*, *"SSRF in this param"*
- *"review OAuth/JWT"*, *"attack this GraphQL"*
- *"generate the offensive report"*

The skill always asks for methodology and minimal data before executing anything active.

---

## Boot — methodology selection

First step, before any active execution:

```
Which methodology do you want to work with?
  1. PTES
  2. OWASP WSTG
  3. NIST SP 800-115
  4. OSSTMM
  5. MITRE ATT&CK
  6. CWE / CAPEC
  7. Hybrid (combine several)
  8. Manual selection
```

The choice persists as project memory so the skill won't ask again in subsequent sessions of the same engagement. See `references/methodologies.md`.

---

## Offensive pipeline

```mermaid
flowchart TB
    classDef recon fill:#0d1b2a,stroke:#00ffaa,color:#00ffaa,stroke-width:2px
    classDef map fill:#1a1a2e,stroke:#7a5fff,color:#cdb4ff,stroke-width:2px
    classDef fuzz fill:#2a1a3a,stroke:#ff5fff,color:#ffb4ff,stroke-width:2px
    classDef exploit fill:#3a0a0a,stroke:#ff3344,color:#ff9999,stroke-width:2px
    classDef ai fill:#0a2540,stroke:#33aaff,color:#99ddff,stroke-width:2px
    classDef poc fill:#403a00,stroke:#ffcc00,color:#fff099,stroke-width:2px
    classDef report fill:#003322,stroke:#00ff99,color:#aaffcc,stroke-width:2px

    A["🛰️  ASM &amp; Recon<br/>subfinder · amass · httpx"]:::recon
    B["🔬  Fingerprint &amp; Tech<br/>whatweb · wappalyzer · nuclei -tags tech"]:::recon
    C["🕷️  Crawl &amp; JS Intel<br/>katana · linkfinder · sourcemaps"]:::map
    D["🔐  API &amp; Auth Mapping<br/>OpenAPI · GraphQL · JWT · OAuth"]:::map
    E["🎯  Fuzzing &amp; Scanners<br/>ffuf · feroxbuster · nuclei · arjun"]:::fuzz
    F["💥  Exploitation<br/>SQLi · XSS · SSRF · SSTI · IDOR · BOLA · Race"]:::exploit
    G["🧠  AI Correlation &amp; Attack-Chain Reasoning"]:::ai
    H["📦  Reproducible PoC + Evidence<br/>CVSS 3.1 · CVSS 4.0 · CWE · CAPEC · ATT&amp;CK"]:::poc
    I["📄  Multi-format Reporting<br/>md · txt · html · docx · pdf · pptx · json · sarif"]:::report

    A --> B --> C --> D --> E --> F --> G --> H --> I
    A -.->|continuous| A
    G -.->|new vectors| E
```

---

## Tooling stack

<div align="center">


#### 🛰️ Recon / OSINT / ASM

[![subfinder](https://img.shields.io/badge/subfinder-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/subfinder) [![amass](https://img.shields.io/badge/amass-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/owasp-amass/amass) [![assetfinder](https://img.shields.io/badge/assetfinder-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/tomnomnom/assetfinder) [![findomain](https://img.shields.io/badge/findomain-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/Findomain/Findomain) [![httpx](https://img.shields.io/badge/httpx-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/httpx) [![katana](https://img.shields.io/badge/katana-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/katana) [![hakrawler](https://img.shields.io/badge/hakrawler-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/hakluke/hakrawler) [![gau](https://img.shields.io/badge/gau-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/lc/gau) [![waybackurls](https://img.shields.io/badge/waybackurls-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/tomnomnom/waybackurls) [![dnsx](https://img.shields.io/badge/dnsx-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/dnsx) [![naabu](https://img.shields.io/badge/naabu-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/naabu) [![masscan](https://img.shields.io/badge/masscan-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/robertdavidgraham/masscan) [![nmap](https://img.shields.io/badge/nmap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://nmap.org) [![aquatone](https://img.shields.io/badge/aquatone-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/michenriksen/aquatone) [![recon-ng](https://img.shields.io/badge/recon--ng-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/lanmaster53/recon-ng) [![theHarvester](https://img.shields.io/badge/theHarvester-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/laramies/theHarvester)

#### 🛰️ Proxy / Interceptación

[![Burp Suite](https://img.shields.io/badge/Burp_Suite-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://portswigger.net/burp) [![OWASP ZAP](https://img.shields.io/badge/OWASP_ZAP-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://www.zaproxy.org) [![Caido](https://img.shields.io/badge/Caido-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://caido.io) [![mitmproxy](https://img.shields.io/badge/mitmproxy-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://mitmproxy.org) [![proxify](https://img.shields.io/badge/proxify-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/proxify)

#### 🎯 Fuzzing

[![ffuf](https://img.shields.io/badge/ffuf-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/ffuf/ffuf) [![feroxbuster](https://img.shields.io/badge/feroxbuster-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/epi052/feroxbuster) [![dirsearch](https://img.shields.io/badge/dirsearch-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/maurosoria/dirsearch) [![gobuster](https://img.shields.io/badge/gobuster-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/OJ/gobuster) [![arjun](https://img.shields.io/badge/arjun-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/s0md3v/Arjun) [![paramspider](https://img.shields.io/badge/paramspider-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/devanshbatham/ParamSpider) [![qsreplace](https://img.shields.io/badge/qsreplace-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/tomnomnom/qsreplace) [![kxss](https://img.shields.io/badge/kxss-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/Emoe/kxss)

#### 🧪 Vulnerability Scanners

[![nuclei](https://img.shields.io/badge/nuclei-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/nuclei) [![nikto](https://img.shields.io/badge/nikto-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/sullo/nikto) [![Nessus](https://img.shields.io/badge/Nessus-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://www.tenable.com/products/nessus) [![Acunetix](https://img.shields.io/badge/Acunetix-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://www.acunetix.com) [![Invicti](https://img.shields.io/badge/Invicti-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://www.invicti.com)

#### 💉 SQL Injection

[![sqlmap](https://img.shields.io/badge/sqlmap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://sqlmap.org) [![ghauri](https://img.shields.io/badge/ghauri-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/r0oth3x49/ghauri) [![NoSQLMap](https://img.shields.io/badge/NoSQLMap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/codingo/NoSQLMap)

#### 🪲 XSS

[![XSStrike](https://img.shields.io/badge/XSStrike-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/s0md3v/XSStrike) [![Dalfox](https://img.shields.io/badge/Dalfox-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/hahwul/dalfox) [![kxss](https://img.shields.io/badge/kxss-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/Emoe/kxss) [![XSSHunter](https://img.shields.io/badge/XSSHunter-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://xsshunter.com)

#### 🔌 APIs

[![Postman](https://img.shields.io/badge/Postman-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://www.postman.com) [![inql](https://img.shields.io/badge/inql-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/doyensec/inql) [![graphqlmap](https://img.shields.io/badge/graphqlmap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/swisskyrepo/GraphQLmap) [![schemathesis](https://img.shields.io/badge/schemathesis-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/schemathesis/schemathesis) [![Astra](https://img.shields.io/badge/Astra-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/flipkart-incubator/Astra)

#### 🔐 Auth / JWT

[![jwt_tool](https://img.shields.io/badge/jwt__tool-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/ticarpi/jwt_tool) [![jwt-cracker](https://img.shields.io/badge/jwt--cracker-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/lmammino/jwt-cracker) [![Hydra](https://img.shields.io/badge/Hydra-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/vanhauser-thc/thc-hydra) [![Patator](https://img.shields.io/badge/Patator-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/lanjelot/patator) [![AuthMatrix](https://img.shields.io/badge/AuthMatrix-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/SecurityInnovation/AuthMatrix)

#### 🛰️ SSRF / SSTI / Deserialization

[![SSRFmap](https://img.shields.io/badge/SSRFmap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/swisskyrepo/SSRFmap) [![tplmap](https://img.shields.io/badge/tplmap-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/epinna/tplmap) [![ysoserial](https://img.shields.io/badge/ysoserial-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/frohoff/ysoserial) [![interactsh](https://img.shields.io/badge/interactsh-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/projectdiscovery/interactsh)

#### 🧱 CMS

[![WPScan](https://img.shields.io/badge/WPScan-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/wpscanteam/wpscan) [![droopescan](https://img.shields.io/badge/droopescan-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/SamJoan/droopescan) [![joomscan](https://img.shields.io/badge/joomscan-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/OWASP/joomscan)

#### 📜 JS / Secrets

[![LinkFinder](https://img.shields.io/badge/LinkFinder-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/GerbenJavado/LinkFinder) [![SecretFinder](https://img.shields.io/badge/SecretFinder-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/m4ll0k/SecretFinder) [![retire.js](https://img.shields.io/badge/retire.js-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://retirejs.github.io/retire.js/) [![semgrep](https://img.shields.io/badge/semgrep-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://semgrep.dev) [![trufflehog](https://img.shields.io/badge/trufflehog-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/trufflesecurity/trufflehog) [![gitleaks](https://img.shields.io/badge/gitleaks-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/gitleaks/gitleaks)

#### ☁️ Cloud / K8s / CI-CD

[![ScoutSuite](https://img.shields.io/badge/ScoutSuite-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/nccgroup/ScoutSuite) [![Prowler](https://img.shields.io/badge/Prowler-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/prowler-cloud/prowler) [![Pacu](https://img.shields.io/badge/Pacu-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/RhinoSecurityLabs/pacu) [![kube-hunter](https://img.shields.io/badge/kube--hunter-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/aquasecurity/kube-hunter) [![trivy](https://img.shields.io/badge/trivy-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/aquasecurity/trivy) [![docker-bench-security](https://img.shields.io/badge/docker--bench--security-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/docker/docker-bench-security) [![octoscan](https://img.shields.io/badge/octoscan-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/synacktiv/octoscan) [![zizmor](https://img.shields.io/badge/zizmor-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/woodruffw/zizmor)

#### 📚 Wordlists / Payloads

[![SecLists](https://img.shields.io/badge/SecLists-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/danielmiessler/SecLists) [![PayloadsAllTheThings](https://img.shields.io/badge/PayloadsAllTheThings-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/swisskyrepo/PayloadsAllTheThings) [![FuzzDB](https://img.shields.io/badge/FuzzDB-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://github.com/fuzzdb-project/fuzzdb) [![Assetnote](https://img.shields.io/badge/Assetnote-FFFFFF?style=for-the-badge&labelColor=003B1F&color=003B1F)](https://wordlists.assetnote.io)


</div>


### Quick commands

```bash
# Full recon
subfinder -d target.cl -all -silent | dnsx -silent | httpx -title -tech-detect -o live.txt

# JS endpoint mining
katana -u https://target.cl -d 5 -jc -kf all -o endpoints.txt

# Fast vuln scan
nuclei -u https://target.cl -severity critical,high -o nuclei.txt

# Fuzzing
ffuf -u https://target.cl/FUZZ -w wordlists/raft-medium-directories.txt -ac -mc 200,301,302,401,403

# Automated SQLi
sqlmap -u "https://target.cl/api?id=1" --batch --level=3 --risk=2

# JWT crack
jwt_tool eyJ... -C -d rockyou.txt

# OOB callback
interactsh-client -v
```

---

## Report generator

Multi-format Python script at `scripts/generate_report.py`.

| Flag | Output | Typical use |
|------|--------|-------------|
| `--format md` | Markdown | Repo / GitHub issue / commit |
| `--format txt` | Plain text | Plain ticket |
| `--format html` | Standalone styled HTML | Quick web view |
| `--format docx` | Word with justified text, severity-colored cells, terminal-style code blocks | Client editable |
| `--format pdf` | PDF (via weasyprint) | Final signed deliverable |
| `--format pptx` | PowerPoint with cover, executive summary, severity matrix, top findings, conclusion | **Simple results presentation** |
| `--format json` | Normalized JSON | Knowledge graph ingest |
| `--format all` | Everything in one directory | Full delivery |

```bash
python3 scripts/generate_report.py --input findings.json --format docx --output report.docx
python3 scripts/generate_report.py --input findings.json --format all --output ./out/
```

See `assets/example_findings.json` for input schema. 
---

## Tutorials

### 1. Quick web pentest

```bash
> /hackweb audit https://demo.target.cl
# Pick methodology (e.g. "Hybrid: WSTG + ATT&CK + CWE")
# Skill executes pipeline:
subfinder -d demo.target.cl -all | httpx -title -tech-detect
nuclei -u https://demo.target.cl -severity critical,high
katana -u https://demo.target.cl -d 5 -jc | grep -E '/api/'
# Document findings.json, generate report
python3 scripts/generate_report.py -i findings.json -f docx -o report.docx
```

### 2. Bug bounty workflow

```bash
subfinder -d target.cl -all -silent | tee subs.txt
amass enum -passive -d target.cl >> subs.txt
sort -u subs.txt | dnsx -silent | httpx -title -tech-detect -o live.txt
katana -l live.txt -d 5 -jc -kf all -o endpoints.txt
nuclei -l live.txt -severity critical,high -tags exposure,cve -o nuclei.txt
python3 scripts/generate_report.py -i findings.json -f md -o report.md
```

### 3. Build your own MCP

```bash
pip install mcp[cli]
cat > recon_mcp.py <<'EOF'
from mcp.server.fastmcp import FastMCP
import subprocess
mcp = FastMCP("recon-mcp")
@mcp.tool()
def subdomains(domain: str) -> list[str]:
    out = subprocess.check_output(["subfinder", "-d", domain, "-silent"])
    return out.decode().splitlines()
if __name__ == "__main__": mcp.run()
EOF
claude mcp add recon-mcp -- python recon_mcp.py
```

### 4. Executive presentation in one command

```bash
python3 scripts/generate_report.py -i findings.json -f pptx -o presentation.pptx
open presentation.pptx
```

---

## MCPs

Recommended catalog in `references/mcp.md`.

**Existing / official:**

| MCP | Purpose |
|-----|---------|
| **[Burp Suite MCP Server](https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc)** (official PortSwigger) | Exposes Repeater, scanner, intercepted traffic and other Burp features to AI clients. Repo: [github.com/portswigger/mcp-server](https://github.com/portswigger/mcp-server) |

**Suggested blueprints to build** (the skill documents their capability surface; not yet published MCPs):

| MCP | Purpose |
|-----|---------|
| `nuclei-mcp` | Templates + finding correlation |
| `sqli-mcp` | SQLi detect + WAF evasion |
| `xss-mcp` | Payload mutation + CSP bypass gen |
| `api-security-mcp` | OpenAPI ingest + BOLA detection |
| `auth-mcp` | JWT analysis + race conditions |
| `cloud-web-mcp` | S3, K8s, IAM enum |
| `reporting-mcp` | Server-side report generation |
| `cvss-engine-mcp` | CVSS 3.1 + 4.0 calculation |
| `bugbounty-brain-mcp` | Persistent memory of bypasses + payloads |
| `web-attack-chain-mcp` | Suggest chains from findings |

---

## 🤖 Multi-AI support (optional)

Although the skill was born for **Claude Code / Claude Desktop**, it can also run on other copilots without touching the core. All host-specific logic lives in `adapters/`, kept separate from the rest.

| Host | Entry file used |
|------|-----------------|
| Claude Code / Claude Desktop | native `SKILL.md` (default) |
| **Gemini CLI** | `adapters/gemini/GEMINI.md` + `gemini-extension.json` |
| **Cursor** | `adapters/cursor/.cursorrules` |
| **Aider** | `adapters/aider/CONVENTIONS.md` + `.aider.conf.yml` |
| **OpenAI Codex CLI / OpenHands / generic** | `adapters/openai-codex/AGENTS.md` or `adapters/generic/AGENTS.md` |

**Auto-detection:**
```bash
bash adapters/install.sh                       # detect your available host
bash adapters/install.sh --host gemini         # force a host
bash adapters/install.sh --host cursor --project-dir /path
```

The installer detects `claude`, `gemini`, `cursor`, `aider`, `codex` (with fallback to `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`). The Python report generator is host-agnostic and behaves identically everywhere.

Full details in [`adapters/README.md`](./adapters/README.md).

---

## Installation

### Claude Code
```bash
git clone https://github.com/DM20911/HackingWebbyDM20911 ~/.claude/skills/HackingWebbyDM20911
pip3 install python-docx python-pptx weasyprint markdown
```

### Claude Desktop
1. Build the bundle: `zip -r HackingWebbyDM20911.skill HackingWebbyDM20911 -x "*.git*"`
2. Import the `.skill` file in Settings → Capabilities → Skills.

PDF export needs `brew install pango cairo gdk-pixbuf libffi` plus `pip install weasyprint`.

---

## Project structure

```
HackingWebbyDM20911/
├── SKILL.md
├── README.md (es) + README.en/.pt/.fr/.de/.it/.ja.md
├── scripts/generate_report.py
├── assets/example_findings.json
└── references/  (36 specialized files loaded on demand)
```

---

## Philosophy

> Tools aren't what matters most. What matters is understanding HTTP, business logic, auth flows, trust boundaries, and thinking in attack chains.

This skill doesn't replace the pentester — it makes them 10x faster.

---

## Author

dm20911

## License

Authorized internal use.
