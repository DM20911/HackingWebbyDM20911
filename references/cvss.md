# CVSS Engine

Cada hallazgo debe llevar **CVSS 3.1 + 4.0** (ambos son estándar hoy).

## CVSS 3.1

Vector: `CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_`

| Métrica | Valores |
|---------|---------|
| AV (Attack Vector) | N(etwork) / A(djacent) / L(ocal) / P(hysical) |
| AC (Attack Complexity) | L(ow) / H(igh) |
| PR (Privileges Required) | N(one) / L(ow) / H(igh) |
| UI (User Interaction) | N(one) / R(equired) |
| S (Scope) | U(nchanged) / C(hanged) |
| C (Confidentiality) | H(igh) / L(ow) / N(one) |
| I (Integrity) | H / L / N |
| A (Availability) | H / L / N |

Calculator: https://www.first.org/cvss/calculator/3.1

### Ejemplos típicos

| Vuln | Vector |
|------|--------|
| SQLi auth bypass | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` → 9.8 |
| BOLA | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` → 6.5 |
| Stored XSS | `CVSS:3.1/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N` → 5.4 |
| SSRF interna | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` → 7.7 |
| RCE auth | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H` → 8.8 |
| Open redirect | `CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:N/A:N` → 4.7 |

## CVSS 4.0

Vector: `CVSS:4.0/AV:_/AC:_/AT:_/PR:_/UI:_/VC:_/VI:_/VA:_/SC:_/SI:_/SA:_`

Cambios vs 3.1:
- **AT** (Attack Requirements): N / P
- **UI** ahora: N / P (Passive) / A (Active)
- Métricas separadas para sistema vulnerable (V) y sistema subsiguiente (S):
  - **VC/VI/VA** = impacto en sistema vulnerable
  - **SC/SI/SA** = impacto en sistema subsiguiente
- Sin "Scope" — reemplazado por la separación V/S.

Calculator: https://www.first.org/cvss/calculator/4-0

### Ejemplos

| Vuln | Vector |
|------|--------|
| SQLi auth bypass | `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H` → 9.4 |
| BOLA | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N` → 6.9 |
| Stored XSS | `CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:A/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N` → 5.1 |

## Severidad por score

| Score | Severidad |
|-------|-----------|
| 0.0 | None |
| 0.1–3.9 | Low |
| 4.0–6.9 | Medium |
| 7.0–8.9 | High |
| 9.0–10.0 | Critical |

## Cómo decidir cada métrica (CVSS 3.1)

**AV:**
- N: explotable desde Internet sin acceso intermedio
- A: requiere LAN / Bluetooth / NFC
- L: requiere acceso local al host (no remoto)
- P: requiere acceso físico

**AC:**
- L: ataque consistente, sin condiciones especiales
- H: requiere timing, MITM activo, info especializada del target

**PR:**
- N: anónimo
- L: cuenta usuario regular
- H: cuenta admin/privileged

**UI:**
- N: ningún clic/acción del usuario
- R: víctima debe hacer algo (clic, abrir archivo)

**S (Scope):**
- U: impacto limitado al componente vulnerable
- C: impacto trasciende a otros componentes (ej: XSS impacta navegador del usuario, no solo el server)

**C/I/A:**
- H: información completa o todo el sistema afectado
- L: parcial / restringido
- N: sin impacto

## Helper: explicar vector

Para un vector cualquiera, generar:
- Score numérico.
- Severidad.
- Explicación en lenguaje natural por métrica.

Implementación en `scripts/generate_report.py` (funciones `cvss31_to_dict`, `explain_vector`).
