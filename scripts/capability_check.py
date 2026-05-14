#!/usr/bin/env python3
"""
Capability check for HackingWebbyDM20911.

Detecta qué capacidades están realmente disponibles en el entorno actual y las
clasifica explícitamente en tres niveles para evitar la confusión de "creer que
hay automatización end-to-end donde solo hay guía".

Niveles
-------
L1 NATIVE     — scripts/lógica que viven dentro de esta skill (siempre disponibles
                si la skill está instalada). Ej.: generate_report.py, methodology.py.
L2 EXTERNAL   — herramientas/MCPs instalados en el sistema que la IA puede invocar
                directamente vía Bash o MCP (nuclei, ffuf, sqlmap, nmap, burp-mcp...).
L3 GUIDED     — capacidades que la IA solo *documenta/guía* (sin ejecución directa):
                el usuario las corre manualmente o requieren auth/UI/setup humano.

Uso
---
    python3 scripts/capability_check.py              # report tabla + resumen
    python3 scripts/capability_check.py --json       # salida machine-readable
    python3 scripts/capability_check.py --strict     # exit !=0 si falta algo L2 crítico
    python3 scripts/capability_check.py --only L2    # filtra por nivel

La salida JSON se puede embedir en el informe final como anexo "Entorno de testing"
para que cada hallazgo sea trazable a la herramienta y versión que lo produjo.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

SKILL_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Catálogo
# ---------------------------------------------------------------------------

@dataclass
class Capability:
    name: str
    level: str                # L1_NATIVE | L2_EXTERNAL | L3_GUIDED
    category: str             # recon, fuzzing, scanner, sqli, xss, api, auth, mcp, report...
    check: str                # cómo se verifica: "bin", "python_mod", "file", "mcp", "manual"
    target: str               # binario / módulo / path / nombre MCP
    version_cmd: Optional[str] = None
    critical: bool = False    # si True, su ausencia rompe el workflow esperado
    notes: str = ""

    # Resultados (rellenados al ejecutar)
    available: bool = False
    version: Optional[str] = None
    path: Optional[str] = None
    error: Optional[str] = None


CATALOG: list[Capability] = [
    # ---------- L1 NATIVE ----------
    Capability("generate_report.py", "L1_NATIVE", "report", "file",
               str(SKILL_ROOT / "scripts" / "generate_report.py"),
               version_cmd=None, critical=True,
               notes="Generador multi-formato del informe (md/docx/pdf/html/pptx/json)."),
    Capability("methodology.py", "L1_NATIVE", "methodology", "file",
               str(SKILL_ROOT / "scripts" / "methodology.py"),
               critical=True,
               notes="Aplicador de metodologías (PTES/WSTG/NIST/OSSTMM/ATT&CK/CWE-CAPEC)."),
    Capability("references/", "L1_NATIVE", "docs", "file",
               str(SKILL_ROOT / "references"),
               critical=True,
               notes="Catálogo de referencias por fase (recon, sqli, xss, api, auth, ...)."),
    Capability("assets/example_findings.json", "L1_NATIVE", "schema", "file",
               str(SKILL_ROOT / "assets" / "example_findings.json"),
               critical=False,
               notes="Schema de findings con CVSS 3.1/4.0, CWE, CAPEC, ATT&CK."),

    # ---------- L2 EXTERNAL — recon ----------
    Capability("subfinder", "L2_EXTERNAL", "recon", "bin", "subfinder",
               version_cmd="subfinder -version", critical=False),
    Capability("amass", "L2_EXTERNAL", "recon", "bin", "amass",
               version_cmd="amass -version", critical=False),
    Capability("httpx", "L2_EXTERNAL", "recon", "bin", "httpx",
               version_cmd="httpx -version", critical=False),
    Capability("dnsx", "L2_EXTERNAL", "recon", "bin", "dnsx",
               version_cmd="dnsx -version", critical=False),
    Capability("naabu", "L2_EXTERNAL", "recon", "bin", "naabu",
               version_cmd="naabu -version", critical=False),
    Capability("katana", "L2_EXTERNAL", "recon", "bin", "katana",
               version_cmd="katana -version", critical=False),
    Capability("nmap", "L2_EXTERNAL", "recon", "bin", "nmap",
               version_cmd="nmap --version", critical=True),
    Capability("masscan", "L2_EXTERNAL", "recon", "bin", "masscan",
               version_cmd="masscan --version", critical=False),

    # ---------- L2 EXTERNAL — fuzzing ----------
    Capability("ffuf", "L2_EXTERNAL", "fuzzing", "bin", "ffuf",
               version_cmd="ffuf -V", critical=True),
    Capability("feroxbuster", "L2_EXTERNAL", "fuzzing", "bin", "feroxbuster",
               version_cmd="feroxbuster --version", critical=False),
    Capability("arjun", "L2_EXTERNAL", "fuzzing", "bin", "arjun",
               version_cmd="arjun --version", critical=False),
    Capability("paramspider", "L2_EXTERNAL", "fuzzing", "bin", "paramspider",
               version_cmd="paramspider --help", critical=False),

    # ---------- L2 EXTERNAL — scanners ----------
    Capability("nuclei", "L2_EXTERNAL", "scanner", "bin", "nuclei",
               version_cmd="nuclei -version", critical=True),
    Capability("nikto", "L2_EXTERNAL", "scanner", "bin", "nikto",
               version_cmd="nikto -Version", critical=False),
    Capability("wpscan", "L2_EXTERNAL", "scanner", "bin", "wpscan",
               version_cmd="wpscan --version", critical=False),

    # ---------- L2 EXTERNAL — explotación ----------
    Capability("sqlmap", "L2_EXTERNAL", "sqli", "bin", "sqlmap",
               version_cmd="sqlmap --version", critical=True),
    Capability("ghauri", "L2_EXTERNAL", "sqli", "bin", "ghauri",
               version_cmd="ghauri --version", critical=False),
    Capability("dalfox", "L2_EXTERNAL", "xss", "bin", "dalfox",
               version_cmd="dalfox version", critical=False),
    Capability("XSStrike", "L2_EXTERNAL", "xss", "bin", "xsstrike",
               version_cmd="xsstrike --help", critical=False),
    Capability("kxss", "L2_EXTERNAL", "xss", "bin", "kxss",
               version_cmd="kxss -h", critical=False),

    # ---------- L2 EXTERNAL — auth/api ----------
    Capability("jwt_tool", "L2_EXTERNAL", "auth", "bin", "jwt_tool",
               version_cmd="jwt_tool --help", critical=False),
    Capability("schemathesis", "L2_EXTERNAL", "api", "bin", "schemathesis",
               version_cmd="schemathesis --version", critical=False),

    # ---------- L2 EXTERNAL — secrets ----------
    Capability("trufflehog", "L2_EXTERNAL", "secrets", "bin", "trufflehog",
               version_cmd="trufflehog --version", critical=False),
    Capability("gitleaks", "L2_EXTERNAL", "secrets", "bin", "gitleaks",
               version_cmd="gitleaks version", critical=False),

    # ---------- L2 EXTERNAL — OOB ----------
    Capability("interactsh-client", "L2_EXTERNAL", "oob", "bin", "interactsh-client",
               version_cmd="interactsh-client -version", critical=False),

    # ---------- L2 EXTERNAL — MCPs ----------
    Capability("burp-mcp", "L2_EXTERNAL", "mcp", "mcp", "mcp__burp__",
               critical=False,
               notes="Burp MCP — control de Repeater/Intruder/Collaborator desde la IA."),
    Capability("n8n-mcp", "L2_EXTERNAL", "mcp", "mcp", "mcp__n8n__",
               critical=False,
               notes="Pipelines de orquestación ofensiva vía n8n."),

    # ---------- L3 GUIDED — UIs y procesos humanos ----------
    Capability("Burp Suite (UI)", "L3_GUIDED", "proxy", "manual", "burpsuite",
               critical=False,
               notes="Si no hay burp-mcp, la IA solo describe pasos manuales en la UI."),
    Capability("Caido", "L3_GUIDED", "proxy", "manual", "caido", critical=False),
    Capability("ZAP", "L3_GUIDED", "proxy", "manual", "zap", critical=False),
    Capability("PortSwigger Academy labs", "L3_GUIDED", "labs", "manual",
               "portswigger.net", critical=False,
               notes="Solo guía; ejecución la hace el humano."),
    Capability("Bug Bounty triage policy", "L3_GUIDED", "process", "manual",
               "platform-policy", critical=False,
               notes="Cada plataforma (H1, Intigriti, YesWeHack) tiene scope/rules propios."),
    Capability("Client engagement legal", "L3_GUIDED", "process", "manual",
               "rules-of-engagement", critical=True,
               notes="ROE, autorización escrita, ventanas. La IA NO ejecuta sin esto."),
]


# ---------------------------------------------------------------------------
# Probing
# ---------------------------------------------------------------------------

def _run(cmd: str, timeout: int = 5) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or r.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except Exception as e:
        return 1, str(e)


def probe(cap: Capability) -> Capability:
    if cap.check == "file":
        p = Path(cap.target)
        cap.available = p.exists()
        cap.path = str(p) if cap.available else None
        if not cap.available:
            cap.error = "missing"
        return cap

    if cap.check == "bin":
        path = shutil.which(cap.target)
        cap.available = path is not None
        cap.path = path
        if cap.available and cap.version_cmd:
            rc, out = _run(cap.version_cmd)
            cap.version = out.splitlines()[0][:120] if out else None
        elif not cap.available:
            cap.error = "not in PATH"
        return cap

    if cap.check == "mcp":
        # No podemos invocar MCPs aquí (requieren aprobación). Marcamos como
        # "declared" — la IA verá la disponibilidad real cuando intente usarlo.
        cap.available = False
        cap.error = "mcp presence cannot be probed from CLI — check `claude mcp list`"
        return cap

    if cap.check == "manual":
        cap.available = False
        cap.error = "guided-only (no automated probe)"
        return cap

    if cap.check == "python_mod":
        rc, out = _run(f"python3 -c 'import {cap.target}; print({cap.target}.__version__)'")
        cap.available = rc == 0
        cap.version = out if cap.available else None
        cap.error = None if cap.available else out
        return cap

    cap.error = f"unknown check type: {cap.check}"
    return cap


# ---------------------------------------------------------------------------
# Reporte
# ---------------------------------------------------------------------------

LEVEL_LABEL = {
    "L1_NATIVE":   "L1 NATIVE   (skill-owned)",
    "L2_EXTERNAL": "L2 EXTERNAL (auto-invokable)",
    "L3_GUIDED":   "L3 GUIDED   (AI guide only)",
}


def render_text(caps: list[Capability]) -> str:
    from collections import defaultdict
    buckets: dict[str, list[Capability]] = defaultdict(list)
    for c in caps:
        buckets[c.level].append(c)

    out: list[str] = []
    out.append("=" * 78)
    out.append(f"HackingWebbyDM20911 — Capability check  ({datetime.now(timezone.utc).isoformat()})")
    out.append("=" * 78)

    for level in ("L1_NATIVE", "L2_EXTERNAL", "L3_GUIDED"):
        items = buckets.get(level, [])
        if not items:
            continue
        ok = sum(1 for c in items if c.available)
        out.append("")
        out.append(f"## {LEVEL_LABEL[level]}   [{ok}/{len(items)} available]")
        out.append("-" * 78)
        for c in sorted(items, key=lambda x: (x.category, x.name)):
            mark = "OK " if c.available else ("--" if c.check in ("mcp", "manual") else "NO")
            crit = " *" if c.critical and not c.available else "  "
            ver = f" [{c.version}]" if c.version else ""
            err = f"  ({c.error})" if (not c.available and c.error) else ""
            out.append(f"  {mark}{crit} [{c.category:8}] {c.name:24}{ver}{err}")

    # Resumen
    missing_critical = [c for c in caps if c.critical and not c.available and c.check != "manual"]
    out.append("")
    out.append("-" * 78)
    out.append(f"Summary: {sum(1 for c in caps if c.available)}/{len(caps)} available, "
               f"{len(missing_critical)} critical missing")
    if missing_critical:
        out.append("Critical missing: " + ", ".join(c.name for c in missing_critical))
        out.append("→ Install with the one-liners in SKILL.md §5 before automated workflows.")
    out.append("=" * 78)
    return "\n".join(out)


def render_json(caps: list[Capability]) -> str:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skill": "HackingWebbyDM20911",
        "skill_root": str(SKILL_ROOT),
        "levels": {
            "L1_NATIVE":   "Capabilities owned by the skill itself",
            "L2_EXTERNAL": "External tools/MCPs the AI can invoke directly",
            "L3_GUIDED":   "Documented-only: AI guides, human executes",
        },
        "capabilities": [asdict(c) for c in caps],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Capability check for HackingWebbyDM20911")
    ap.add_argument("--json", action="store_true", help="JSON output")
    ap.add_argument("--strict", action="store_true",
                    help="exit !=0 if any critical L2 capability is missing")
    ap.add_argument("--only", choices=["L1", "L2", "L3"], help="filter by level")
    ap.add_argument("--category", help="filter by category (recon, fuzzing, scanner, ...)")
    args = ap.parse_args()

    caps = [probe(c) for c in CATALOG]
    if args.only:
        prefix = {"L1": "L1_NATIVE", "L2": "L2_EXTERNAL", "L3": "L3_GUIDED"}[args.only]
        caps = [c for c in caps if c.level == prefix]
    if args.category:
        caps = [c for c in caps if c.category == args.category]

    print(render_json(caps) if args.json else render_text(caps))

    if args.strict:
        missing_critical = [c for c in caps if c.critical and not c.available and c.check != "manual"]
        return 2 if missing_critical else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
