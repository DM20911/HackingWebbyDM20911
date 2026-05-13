<p align="center">
  <img src="./assets/banner.svg" alt="HackingWebbyDM20911 — Offensive Web Hacking Copilot" width="100%"/>
</p>

# 🕷️ HackingWebbyDM20911

> **Offensive Web Hacking copilot** — recon, exploitation, AI-assisted correlation, attack chaining y reporting senior multi-formato.

🌐 **Idiomas:** [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md)

Skill de Claude Code / Claude Desktop para profesionales de pentesting web ofensivo. Empaqueta la metodología, las herramientas, los MCPs recomendados y un generador de informes propio (Markdown, Word, PDF, HTML, PowerPoint, JSON, SARIF).

---

## Índice

1. [¿Qué hace?](#qué-hace)
2. [Cómo se invoca](#cómo-se-invoca)
3. [Boot — selección de metodología](#boot--selección-de-metodología)
4. [Pipeline ofensivo](#pipeline-ofensivo)
5. [Stack de herramientas](#stack-de-herramientas)
6. [Generador de informes (multi-formato)](#generador-de-informes)
7. [Tutoriales paso a paso](#tutoriales)
8. [Integración con MCPs](#mcps)
9. [Instalación](#instalación)
10. [Estructura del proyecto](#estructura)

---

## ¿Qué hace?

Esta skill convierte a Claude en un copiloto ofensivo end-to-end:

- **Recon / OSINT / ASM** — subdominios, endpoints, JS intel, source maps, secret hunting.
- **Fuzzing & Scanners** — ffuf, feroxbuster, nuclei, sqlmap, dalfox, XSStrike.
- **Exploitation** — SQLi, XSS, SSRF, SSTI, deserialization, IDOR/BOLA, mass assignment.
- **APIs profundo** — REST, GraphQL (introspection, batching, depth, alias), SOAP.
- **Auth deep dive** — JWT, OAuth2/OIDC, SAML, sesiones, MFA bypass, race conditions.
- **Cloud + K8s + CI/CD** — AWS/GCP/Azure SSRF + IAM, kube-hunter, GitHub Actions abuse.
- **Browser security** — CSP bypass, postMessage, Service Workers, XS-Leaks, SameSite.
- **Business logic abuse** — workflows, race, coupon/refund/transfer, escalación.
- **Attack chaining** — correlación inteligente para construir chains críticos.
- **Reporting senior** — informes con CVSS 3.1 + 4.0, CWE, CAPEC, ATT&CK, attack chains, evidencia, exportables a md/docx/pdf/html/pptx.

---

## Cómo se invoca

En **Claude Code** o **Claude Desktop**, escribe alguno de estos:

- `/hackweb`
- `/HackingWebbyDM20911`
- *"audita esta web"*, *"haz recon a target.cl"*, *"pentest a esta API"*
- *"explota esta vuln"*, *"busca BOLA / IDOR"*, *"SSRF en este parámetro"*
- *"revisa OAuth/JWT"*, *"atacame esta GraphQL"*
- *"genera el informe ofensivo"*

La skill arranca preguntando metodología y datos mínimos antes de cualquier acción.

---

## Boot — selección de metodología

Primer paso siempre, antes de ejecutar nada activo:

```
¿Con qué metodología quieres trabajar?
  1. PTES
  2. OWASP WSTG
  3. NIST SP 800-115
  4. OSSTMM
  5. MITRE ATT&CK
  6. CWE / CAPEC
  7. Híbrida (combinar varias)
  8. Selección manual
```

El usuario puede elegir una o combinar. La elección se persiste como project memory para no preguntar de nuevo en sesiones siguientes del mismo engagement.

Detalle en `references/methodologies.md`.

---

## Pipeline ofensivo

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
    H["📦  PoC Reproducible + Evidencia<br/>CVSS 3.1 · CVSS 4.0 · CWE · CAPEC · ATT&amp;CK"]:::poc
    I["📄  Reporting Multi-formato<br/>md · txt · html · docx · pdf · pptx · json · sarif"]:::report

    A --> B --> C --> D --> E --> F --> G --> H --> I
    A -.->|continuous| A
    G -.->|new vectors| E
```

<details>
<summary>Vista alternativa (terminal)</summary>

```
   ╭──────────────╮     ╭──────────────╮     ╭──────────────╮     ╭──────────────╮
   │ 🛰️  RECON   │ ──► │ 🔬 FINGER-  │ ──► │ 🕷️  CRAWL  │ ──► │ 🔐 API/AUTH │
   │  ASM/OSINT  │     │  PRINTING   │     │  & JS INTEL │     │   MAPPING   │
   ╰──────────────╯     ╰──────────────╯     ╰──────────────╯     ╰──────────────╯
                                                                          │
   ╭──────────────╮     ╭──────────────╮     ╭──────────────╮              │
   │ 📄 REPORTING │ ◄── │ 📦   PoC    │ ◄── │ 🧠 AI CHAIN │              │
   │ md/docx/pdf  │     │ +EVIDENCIA  │     │  REASONING  │              │
   │ html/pptx    │     │ +CVSS+CWE   │     │             │              │
   ╰──────────────╯     ╰──────────────╯     ╰──────────────╯              │
                                                  ▲                        │
                                                  │                        ▼
                                          ╭──────────────╮      ╭──────────────╮
                                          │ 💥 EXPLOIT  │ ◄── │ 🎯 FUZZING  │
                                          │ SQLi · XSS  │     │ + SCANNERS  │
                                          │ SSRF · BOLA │     │             │
                                          ╰──────────────╯      ╰──────────────╯
```
</details>

---

## Stack de herramientas

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


### Comandos rápidos típicos

```bash
# Recon completo
subfinder -d target.cl -all -silent | dnsx -silent | httpx -title -tech-detect -o live.txt

# Endpoints desde JS bundles
katana -u https://target.cl -d 5 -jc -kf all -o endpoints.txt

# Vuln scan rápido
nuclei -u https://target.cl -severity critical,high -o nuclei.txt

# Fuzzing
ffuf -u https://target.cl/FUZZ -w wordlists/raft-medium-directories.txt -ac -mc 200,301,302,401,403

# SQLi automatizado
sqlmap -u "https://target.cl/api?id=1" --batch --level=3 --risk=2

# JWT crack
jwt_tool eyJ... -C -d rockyou.txt

# OOB callback
interactsh-client -v
```

Ver detalles por categoría en `references/`.

---

## Generador de informes

Script Python multi-formato en `scripts/generate_report.py`.

### Formatos soportados

| Flag | Output | Uso típico |
|------|--------|-----------|
| `--format md` | Markdown | Repo / GitHub issue / commit |
| `--format txt` | Texto plano | Ticket sin formato |
| `--format html` | HTML standalone con estilo | Vista web rápida |
| `--format docx` | Word con texto justificado, tablas con color por severidad, bloques de código tipo terminal | Cliente que edita |
| `--format pdf` | PDF (vía weasyprint) | Entregable final firmado |
| `--format pptx` | PowerPoint con portada, resumen ejecutivo, matriz por severidad, slide por hallazgo crítico, conclusión | **Presentación simple de resultados** |
| `--format json` | JSON normalizado | Ingesta a knowledge graph / SARIF |
| `--format all` | Todos a la vez en un directorio | Entrega completa |

### Uso

```bash
python3 scripts/generate_report.py --input findings.json --format docx --output informe.docx
python3 scripts/generate_report.py --input findings.json --format all --output ./out/
```

### JSON de entrada

Ver `assets/example_findings.json` para schema completo. Estructura:

```json
{
  "meta": { "titulo": "...", "cliente": "...", "tipo": "...", "fecha": "...", "clasificacion": "...", "version": "1.0", "autor": "..." },
  "introduccion": "...",
  "resumen_ejecutivo": "...",
  "alcance": "...",
  "metodologia": "...",
  "findings": [
    {
      "titulo": "...",
      "severidad": "Crítica | Alta | Media | Baja | Info",
      "cvss31_score": 9.1,
      "cvss31_vector": "CVSS:3.1/...",
      "cvss40_score": 8.7,
      "cvss40_vector": "CVSS:4.0/...",
      "cwe": "CWE-639 — ...",
      "capec": "CAPEC-39",
      "owasp": "API1:2023 — ...",
      "attack": "T1190",
      "activo": "https://...",
      "parametro": "path id",
      "descripcion": "...",
      "impacto": "Un atacante podría ...",
      "riesgo_negocio": "...",
      "confidence": "High",
      "validacion_manual": "Sí",
      "probabilidad": "Alta",
      "evidencia": "...",
      "poc": [
        {
          "descripcion": "Qué hace el comando, qué resultado tendrá, qué llamar la atención.",
          "cmd": "curl ...",
          "output": "HTTP/1.1 200 OK ..."
        }
      ],
      "remediacion": "...",
      "referencias": ["..."],
      "estado": "Confirmado"
    }
  ],
  "attack_chains": [
    { "nombre": "...", "componentes": ["..."], "cvss_agregado": "9.8", "descripcion": "..." }
  ],
  "timeline": ["2026-05-08 Recon", "..."],
  "limitaciones": "...",
  "conclusion": "...",
  "anexos": { "Herramientas": "...", "Wordlists": "..." }
}
```

---

## Tutoriales

### Tutorial 1: pentest web rápido

```bash
# 1. Invocar la skill
> /hackweb audita https://demo.target.cl

# 2. Responder metodología (ej: "Híbrida: WSTG + ATT&CK + CWE")

# 3. La skill ejecuta el pipeline:
subfinder -d demo.target.cl -all | httpx -title -tech-detect
nuclei -u https://demo.target.cl -severity critical,high
katana -u https://demo.target.cl -d 5 -jc | grep -E '/api/'

# 4. Documenta hallazgos en findings.json

# 5. Genera informe
python3 scripts/generate_report.py -i findings.json -f docx -o informe.docx
```

### Tutorial 2: bug bounty workflow

```bash
# Recon pasivo amplio
subfinder -d target.cl -all -silent | tee subs.txt
amass enum -passive -d target.cl >> subs.txt
sort -u subs.txt | dnsx -silent | httpx -title -tech-detect -o live.txt

# Crawl + JS intel
katana -l live.txt -d 5 -jc -kf all -o endpoints.txt
cat endpoints.txt | grep -E '\.js$' | xargs -I{} curl -sk {} | grep -oE '(api[_-]?key|secret|token)["\047]?\s*[:=]\s*["\047][^"\047]+'

# Vuln scan
nuclei -l live.txt -severity critical,high -tags exposure,cve -o nuclei.txt

# Reportar a la plataforma con findings.json + render md
python3 scripts/generate_report.py -i findings.json -f md -o report.md
```

### Tutorial 3: configurar un MCP propio

```bash
# 1. Crear esqueleto Python
pip install mcp[cli]

cat > recon_mcp.py <<'EOF'
from mcp.server.fastmcp import FastMCP
import subprocess
mcp = FastMCP("recon-mcp")

@mcp.tool()
def subdomains(domain: str) -> list[str]:
    out = subprocess.check_output(["subfinder", "-d", domain, "-silent"])
    return out.decode().splitlines()

if __name__ == "__main__":
    mcp.run()
EOF

# 2. Registrar en Claude Code
claude mcp add recon-mcp -- python recon_mcp.py

# 3. Verificar
claude mcp list
```

### Tutorial 4: presentación ejecutiva en 1 comando

```bash
python3 scripts/generate_report.py -i findings.json -f pptx -o presentacion.pptx
open presentacion.pptx
```

Genera: portada, slide de resumen ejecutivo, matriz por severidad, slide por hallazgo Crítico/Alto, slide de conclusión.

---

## MCPs

Catálogo recomendado en `references/mcp.md`. Resumen:

**Existentes / oficiales:**

| MCP | Para qué |
|-----|----------|
| **[Burp Suite MCP Server](https://portswigger.net/bappstore/9952290f04ed4f628e624d0aa9dccebc)** (oficial PortSwigger) | Expone Repeater, scanner, tráfico interceptado y demás funciones de Burp a clientes IA. Repo: [github.com/portswigger/mcp-server](https://github.com/portswigger/mcp-server) |

**Blueprints sugeridos para construir** (la skill documenta su superficie de capacidades; aún no son MCPs publicados):

| MCP | Para qué |
|-----|----------|
| `nuclei-mcp` | Templates + correlación de findings |
| `sqli-mcp` | SQLi detect + WAF evasion |
| `xss-mcp` | Payload mutation + CSP bypass gen |
| `api-security-mcp` | OpenAPI ingest + BOLA detection |
| `auth-mcp` | JWT analysis + race conditions |
| `cloud-web-mcp` | S3, K8s, IAM enum |
| `reporting-mcp` | Generación de reports server-side |
| `cvss-engine-mcp` | Calcular CVSS 3.1 + 4.0 |
| `bugbounty-brain-mcp` | Memoria persistente de bypasses + payloads |
| `web-attack-chain-mcp` | Sugerir chains a partir de findings |

---

## 🤖 Soporte multi-IA (opcional)

Aunque la skill nació para **Claude Code / Claude Desktop**, también puede usarse desde otros copilotos sin tocar el núcleo. Toda la lógica de host vive en `adapters/`, separada del resto.

| Host | Cómo lo usa |
|------|-------------|
| Claude Code / Claude Desktop | `SKILL.md` nativo (default) |
| **Gemini CLI** | `adapters/gemini/GEMINI.md` + `gemini-extension.json` |
| **Cursor** | `adapters/cursor/.cursorrules` |
| **Aider** | `adapters/aider/CONVENTIONS.md` + `.aider.conf.yml` |
| **OpenAI Codex CLI / OpenHands / genéricos** | `adapters/openai-codex/AGENTS.md` o `adapters/generic/AGENTS.md` |

**Auto-detección:**
```bash
bash adapters/install.sh                       # detecta tu host disponible
bash adapters/install.sh --host gemini         # forzar host
bash adapters/install.sh --host cursor --project-dir /ruta
```

El instalador detecta `claude`, `gemini`, `cursor`, `aider`, `codex` (y como fallback variables `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `OPENAI_API_KEY`). El generador de informes Python es agnóstico y funciona idéntico en cualquier host.

Detalles completos en [`adapters/README.md`](./adapters/README.md).

---

## Instalación

### Claude Code

```bash
git clone https://github.com/DM20911/HackingWebbyDM20911 ~/.claude/skills/HackingWebbyDM20911
pip3 install python-docx python-pptx weasyprint markdown
```

### Claude Desktop

1. Empaquetar (desde repo clonado):
   ```bash
   python3 -m scripts.package_skill ~/.claude/skills/HackingWebbyDM20911
   ```
2. Importar el `.skill` resultante en Settings → Capabilities → Skills.

### Dependencias del generador de informes

```bash
pip3 install python-docx python-pptx weasyprint markdown
```

PDF requiere weasyprint (en macOS necesita `brew install pango cairo gdk-pixbuf libffi`).

---

## Estructura

```
HackingWebbyDM20911/
├── SKILL.md                     # Brain de la skill (cargado siempre)
├── README.md                    # Este archivo
├── scripts/
│   └── generate_report.py       # Generador multi-formato
├── assets/
│   └── example_findings.json    # Ejemplo de input para el generador
└── references/                  # Cargadas bajo demanda según fase
    ├── methodologies.md
    ├── recon.md
    ├── proxy.md
    ├── fuzzing.md
    ├── scanners.md
    ├── sqli.md
    ├── xss.md
    ├── api.md
    ├── graphql.md
    ├── auth.md
    ├── advanced-vulns.md
    ├── cms.md
    ├── js-intel.md
    ├── cloud.md
    ├── cicd.md
    ├── secrets.md
    ├── race-conditions.md
    ├── desync.md
    ├── cache-attacks.md
    ├── browser-sec.md
    ├── business-logic.md
    ├── mobile-web.md
    ├── evasion.md
    ├── attack-chains.md
    ├── correlation.md
    ├── prioritization.md
    ├── wordlists.md
    ├── labs.md
    ├── opsec.md
    ├── legal.md
    ├── reporting.md
    ├── cvss.md
    ├── mcp.md
    ├── ai-memory.md
    ├── agents.md
    └── roadmap.md
```

---

## Filosofía

> Las herramientas no son lo más importante. Lo importante es entender HTTP, lógica de negocio, auth flows, trust boundaries, y pensar en attack chains.

Esta skill no reemplaza al pentester — lo hace 10x más rápido.

---

## Autor

dm20911

## Licencia

Uso interno autorizado.
