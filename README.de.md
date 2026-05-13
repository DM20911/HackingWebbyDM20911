<p align="center">
  <img src="./assets/banner.svg" alt="HackingWebbyDM20911 — Offensive Web Hacking Copilot" width="100%"/>
</p>

# 🕷️ HackingWebbyDM20911

> **Offensiver Web-Hacking-Copilot** — Recon, Exploitation, KI-gestützte Korrelation, Attack-Chaining und seniorenreifes Multi-Format-Reporting.

🌐 **Sprachen:** [Español](README.md) · [English](README.en.md) · [Português](README.pt.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [日本語](README.ja.md)

Claude Code / Claude Desktop Skill für Profis im offensiven Web-Pentesting. Bündelt Methodik, Tooling, empfohlene MCPs und einen integrierten Multi-Format-Berichtsgenerator (Markdown, Word, PDF, HTML, PowerPoint, JSON, SARIF).

## ⚡ Schnellinstallation

```bash
npx skills add DM20911/HackingWebbyDM20911
```

---

## Was es macht

End-to-End offensiver Copilot:

- **Recon / OSINT / ASM** — Subdomains, Endpoints, JS Intel, Source Maps, Secret Hunting.
- **Fuzzing & Scanner** — ffuf, feroxbuster, nuclei, sqlmap, dalfox, XSStrike.
- **Exploitation** — SQLi, XSS, SSRF, SSTI, Deserialization, IDOR/BOLA, Mass Assignment.
- **API tiefgreifend** — REST, GraphQL (Introspection, Batching, Depth, Alias), SOAP.
- **Auth Deep Dive** — JWT, OAuth2/OIDC, SAML, Sessions, MFA-Bypass, Race Conditions.
- **Cloud + K8s + CI/CD** — AWS/GCP/Azure SSRF + IAM, kube-hunter, GitHub Actions Abuse.
- **Browser-Sicherheit** — CSP-Bypass, postMessage, Service Workers, XS-Leaks, SameSite.
- **Business-Logic-Missbrauch** — Workflows, Race, Coupon/Refund/Transfer, Eskalation.
- **Attack Chaining** — intelligente Korrelation für kritische Ketten.
- **Senior-Reporting** — CVSS 3.1 + 4.0, CWE, CAPEC, ATT&CK, Attack Chains, Beweise; Export nach md/docx/pdf/html/pptx.

---

## Aufruf

In **Claude Code** oder **Claude Desktop**:

- `/hackweb`
- `/HackingWebbyDM20911`
- *„auditiere diese Web-App"*, *„Recon zu target.cl"*, *„Pentest dieser API"*
- *„exploite diese Vuln"*, *„suche BOLA / IDOR"*, *„SSRF in diesem Parameter"*
- *„prüfe OAuth/JWT"*, *„greife dieses GraphQL an"*
- *„generiere den offensiven Bericht"*

Die Skill fragt immer nach Methodik und Mindestdaten, bevor sie aktiv ausführt.

---

## Boot — Methodikauswahl

Erster Schritt vor jeder aktiven Ausführung:

```
Mit welcher Methodik möchtest du arbeiten?
  1. PTES
  2. OWASP WSTG
  3. NIST SP 800-115
  4. OSSTMM
  5. MITRE ATT&CK
  6. CWE / CAPEC
  7. Hybrid (mehrere kombinieren)
  8. Manuelle Auswahl
```

Die Wahl bleibt als Project Memory bestehen, damit sie in folgenden Sessions desselben Engagements nicht erneut gefragt wird. Siehe `references/methodologies.md`.

---

## Offensive Pipeline

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
    E["🎯  Fuzzing &amp; Scanner<br/>ffuf · feroxbuster · nuclei · arjun"]:::fuzz
    F["💥  Exploitation<br/>SQLi · XSS · SSRF · SSTI · IDOR · BOLA · Race"]:::exploit
    G["🧠  KI-Korrelation &amp; Attack-Chain Reasoning"]:::ai
    H["📦  Reproduzierbarer PoC + Evidenz<br/>CVSS 3.1 · CVSS 4.0 · CWE · CAPEC · ATT&amp;CK"]:::poc
    I["📄  Multi-Format Reporting<br/>md · txt · html · docx · pdf · pptx · json · sarif"]:::report

    A --> B --> C --> D --> E --> F --> G --> H --> I
    A -.->|kontinuierlich| A
    G -.->|neue Vektoren| E
```

---

## Tool-Stack

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


### Schnellbefehle

```bash
# Vollständige Recon
subfinder -d target.cl -all -silent | dnsx -silent | httpx -title -tech-detect -o live.txt

# Endpoints aus JS
katana -u https://target.cl -d 5 -jc -kf all -o endpoints.txt

# Schneller Scan
nuclei -u https://target.cl -severity critical,high -o nuclei.txt

# Automatisierter SQLi
sqlmap -u "https://target.cl/api?id=1" --batch --level=3 --risk=2

# JWT Crack
jwt_tool eyJ... -C -d rockyou.txt
```

## Berichtsgenerator

Multi-Format Python-Skript in `scripts/generate_report.py`. Formate: `md`, `txt`, `html`, `docx`, `pdf`, `pptx`, `json`, `all`.

```bash
python3 scripts/generate_report.py --input findings.json --format docx --output bericht.docx
python3 scripts/generate_report.py --input findings.json --format all --output ./out/
```

Input-Schema in `assets/example_findings.json`. 
---

## 🤖 Multi-KI-Unterstützung (optional)

Obwohl die Skill für **Claude Code / Claude Desktop** geboren wurde, läuft sie auch in anderen Copiloten, ohne den Kern anzufassen. Die gesamte Host-spezifische Logik liegt in `adapters/`.

| Host | Eintragsdatei |
|------|---------------|
| Claude Code / Desktop | natives `SKILL.md` |
| **Gemini CLI** | `adapters/gemini/GEMINI.md` |
| **Cursor** | `adapters/cursor/.cursorrules` |
| **Aider** | `adapters/aider/CONVENTIONS.md` |
| **OpenAI Codex CLI / generisch** | `adapters/openai-codex/AGENTS.md` |

```bash
bash adapters/install.sh                       # Auto-Erkennung
bash adapters/install.sh --host gemini         # Host erzwingen
```

Details in [`adapters/README.md`](./adapters/README.md).

---

## Installation

```bash
git clone https://github.com/DM20911/HackingWebbyDM20911 ~/.claude/skills/HackingWebbyDM20911
pip3 install python-docx python-pptx weasyprint markdown
```

Claude Desktop: mit `zip -r` packen und unter Settings → Capabilities → Skills importieren.

---

## Philosophie

> Tools sind nicht das Wichtigste. Wichtig ist, HTTP zu verstehen, Business-Logik, Auth-Flows, Trust Boundaries — und in Attack Chains zu denken.

Diese Skill ersetzt den Pentester nicht — sie macht ihn 10x schneller.

---

## Autor

dm20911

## Lizenz

Autorisierte interne Nutzung.
