#!/usr/bin/env python3
"""
methodology.py — Lector de metodologías y aplicación al engagement.

Uso:
    python3 methodology.py list
        Lista todas las metodologías disponibles.

    python3 methodology.py show <nombre>
        Imprime el archivo completo de la metodología.
        nombre: ptes | owasp-wstg | nist-800-115 | osstmm | mitre-attack | cwe-capec

    python3 methodology.py apply <nombre> [--target URL] [--type web|api|mobile|cloud] [--scope desc]
        Imprime la metodología y al final agrega una sección concreta de cómo
        aplicarla al engagement actual con los parámetros dados.

    python3 methodology.py hybrid <m1> <m2> [...] [--target ...] [--type ...]
        Combina varias metodologías y produce un plan híbrido.
"""

import argparse
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "references", "methodologies"))

CATALOG = {
    "ptes":          ("PTES — Penetration Testing Execution Standard",
                      "Pentest formal con cliente, fases completas, retención evidencia."),
    "owasp-wstg":    ("OWASP WSTG v4.2 — Web Security Testing Guide",
                      "Test cases concretos web/API. La referencia técnica más completa."),
    "nist-800-115":  ("NIST SP 800-115 — Technical Guide to Information Security Testing",
                      "Auditorías reguladas (banca/salud/gobierno). Trazabilidad legal."),
    "osstmm":        ("OSSTMM v3 — Open Source Security Testing Methodology",
                      "Holística (multi-canal), métricas RAV reproducibles."),
    "mitre-attack":  ("MITRE ATT&CK — Tactics, Techniques & Procedures",
                      "Mapping de TTPs. Lenguaje común entre red, blue y purple team."),
    "cwe-capec":     ("CWE + CAPEC — Common Weakness & Attack Pattern Enumeration",
                      "Clasificación obligatoria por hallazgo. Mapping a SAST/DAST."),
}

C = {
    "blue":   "\033[1;34m", "green":  "\033[1;32m", "yellow": "\033[1;33m",
    "cyan":   "\033[1;36m", "gray":   "\033[0;90m", "reset":  "\033[0m",
    "bold":   "\033[1m",
}

def color(s, c):
    if not sys.stdout.isatty(): return s
    return f"{C[c]}{s}{C['reset']}"


def cmd_list(_):
    print(color("\n═══ Metodologías disponibles ═══\n", "blue"))
    width = max(len(k) for k in CATALOG) + 2
    for key, (title, desc) in CATALOG.items():
        print(f"  {color(key.ljust(width), 'cyan')}{color(title, 'bold')}")
        print(f"  {' ' * width}{color(desc, 'gray')}\n")
    print(color("Uso:", "yellow"))
    print(f"  python3 methodology.py show <nombre>")
    print(f"  python3 methodology.py apply <nombre> --target <url> --type <web|api|mobile|cloud>")
    print(f"  python3 methodology.py hybrid <m1> <m2> [...] --target <url> --type <tipo>\n")


def load(name):
    if name not in CATALOG:
        print(color(f"\n[!] Metodología desconocida: {name}", "yellow"))
        print(f"    Disponibles: {', '.join(CATALOG)}\n")
        sys.exit(1)
    path = os.path.join(DOCS, f"{name}.md")
    if not os.path.exists(path):
        print(color(f"\n[!] Archivo no encontrado: {path}", "yellow"))
        sys.exit(2)
    return open(path, encoding="utf-8").read()


def cmd_show(args):
    print(load(args.nombre))


def aplica_block(metodologia_key, target, tipo, scope):
    title = CATALOG[metodologia_key][0]
    fases_por_metodo = {
        "ptes": [
            "Pre-engagement (cierre formal de scope, RoE, contactos, NDA)",
            "Intelligence Gathering (recon pasivo + activo + OSINT)",
            "Threat Modeling (actores × activos × abuse cases)",
            "Vulnerability Analysis (scanners + manual)",
            "Exploitation (PoC reproducibles, sin destruir)",
            "Post Exploitation (impacto, lateral, limpieza)",
            "Reporting (ejecutivo + técnico + anexos)",
        ],
        "owasp-wstg": [
            "Filtrar categorías WSTG aplicables al tipo de target",
            "Construir checklist de controles INFO/CONF/ATHN/ATHZ/SESS/INPV/...",
            "Por cada hallazgo: mapear WSTG ID y CWE en el JSON",
            "Reportar cobertura % al cierre",
        ],
        "nist-800-115": [
            "Planning con autorización formal del Authorizing Official",
            "Discovery passive (OSINT, docs, sniff)",
            "Discovery active (port scan, vuln scan)",
            "Attack: gain → escalate → browse → install (si autorizado)",
            "Reporting NIST-style con evidence appendix y reproducibilidad",
        ],
        "osstmm": [
            "Definir canales aplicables (Data Networks para web/API)",
            "Module Tests: Visibility, Access, Trust, Controls, Configuration, Segregation, Exposure, Privileges, Survivability, Logs",
            "Capturar inputs cuantitativos para RAV scoring",
            "Reportar RAV final por canal",
        ],
        "mitre-attack": [
            "Mapear cada hallazgo a 1+ technique-id (T1xxx)",
            "Construir attack chains como secuencias de techniques",
            "Reportar coverage map (qué techniques se probaron)",
            "Para purple team: comparar vs detección del SOC del cliente",
        ],
        "cwe-capec": [
            "Por cada hallazgo: asignar 1 CWE obligatorio",
            "Asignar 1 CAPEC complementario (patrón de ataque)",
            "Combinar con OWASP / WSTG ID + CVSS 3.1+4.0",
            "Validar mapping con devs y AppSec del cliente",
        ],
    }
    fases = fases_por_metodo.get(metodologia_key, [])
    out = []
    out.append("\n" + "═" * 78)
    out.append(color(f"  Aplicación al engagement actual — {title}", "blue"))
    out.append("═" * 78 + "\n")
    out.append(f"  {color('Fecha:', 'bold')}    {date.today().isoformat()}")
    out.append(f"  {color('Target:', 'bold')}   {target or '(sin definir)'}")
    out.append(f"  {color('Tipo:', 'bold')}     {tipo or '(sin definir)'}")
    if scope:
        out.append(f"  {color('Scope:', 'bold')}    {scope}")
    out.append("")
    out.append(color("  Plan de fases concretas para este engagement:", "yellow"))
    for i, fase in enumerate(fases, 1):
        out.append(f"    {color(f'{i}.', 'cyan')} {fase}")
    out.append("")
    if tipo:
        out.append(color(f"  Notas específicas para target tipo '{tipo}':", "yellow"))
        notes = {
            "web":    "  • Foco en WSTG-INPV/ATHN/ATHZ/SESS/CLNT + Cookies SameSite/HttpOnly/Secure.\n"
                      "  • Revisar JS bundles + source maps (references/js-intel.md).",
            "api":    "  • Foco en OWASP API Top 10 (BOLA, mass assignment, function-level auth).\n"
                      "  • GraphQL: introspection, batching, depth (references/graphql.md).",
            "mobile": "  • Comparar API mobile vs web (references/mobile-web.md).\n"
                      "  • SSL pinning, deep links, hardcoded secrets, WebViews.",
            "cloud":  "  • IAM enum (Pacu/ScoutSuite), buckets públicos, K8s exposure (references/cloud.md).\n"
                      "  • CI/CD attack surface (references/cicd.md).",
        }
        out.append(notes.get(tipo, "  (tipo no estándar — usar criterio profesional)"))
        out.append("")
    out.append(color("  Próximo paso:", "yellow"))
    out.append("    Llenar findings.json con hallazgos confirmados y generar el informe:")
    out.append(color(f"    python3 scripts/generate_report.py -i findings.json -f all -o ./out/", "green"))
    out.append("")
    return "\n".join(out)


def cmd_apply(args):
    print(load(args.nombre))
    print(aplica_block(args.nombre, args.target, args.type, args.scope))


def cmd_hybrid(args):
    nombres = args.nombres
    for n in nombres:
        if n not in CATALOG:
            print(color(f"[!] Metodología desconocida: {n}", "yellow"))
            sys.exit(1)
    print(color("\n═══ Plan híbrido ═══", "blue"))
    print(f"  Combinando: {', '.join(CATALOG[n][0] for n in nombres)}\n")
    for n in nombres:
        print(color(f"\n──── {CATALOG[n][0]} ────", "cyan"))
        print(load(n))
        print(aplica_block(n, args.target, args.type, args.scope))
    print(color("\n═══ Plan híbrido consolidado ═══\n", "blue"))
    print(f"  Usar este plan combinado para el engagement contra {args.target or '<target>'}.")
    print(f"  Cada hallazgo del informe debe llevar mapping a TODAS las metodologías aplicables.\n")


def main():
    ap = argparse.ArgumentParser(prog="methodology.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="Lista metodologías disponibles")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Imprime una metodología completa")
    p_show.add_argument("nombre", choices=list(CATALOG))
    p_show.set_defaults(func=cmd_show)

    p_app = sub.add_parser("apply", help="Imprime metodología + cómo aplicarla al engagement")
    p_app.add_argument("nombre", choices=list(CATALOG))
    p_app.add_argument("--target", default="")
    p_app.add_argument("--type", choices=["web","api","mobile","cloud"], default="")
    p_app.add_argument("--scope", default="")
    p_app.set_defaults(func=cmd_apply)

    p_hyb = sub.add_parser("hybrid", help="Combina varias metodologías en un plan único")
    p_hyb.add_argument("nombres", nargs="+", choices=list(CATALOG))
    p_hyb.add_argument("--target", default="")
    p_hyb.add_argument("--type", choices=["web","api","mobile","cloud"], default="")
    p_hyb.add_argument("--scope", default="")
    p_hyb.set_defaults(func=cmd_hybrid)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
