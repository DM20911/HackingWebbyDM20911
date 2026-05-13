# Exploitability & Remediation Prioritization

## Más allá de severidad

Severidad CVSS no es prioridad. Calcular además:

| Factor | Pregunta |
|--------|----------|
| Internet exposure | ¿Está accesible desde Internet o solo intranet? |
| Auth requirement | ¿Anónimo, low-priv, o admin requerido? |
| Exploit availability | ¿Existe PoC público / metasploit module? |
| Exploit maturity | Conceptual / functional / weaponized / wild |
| Detectability | ¿Genera logs visibles? ¿Hay EDR/SIEM? |
| Lateral movement | ¿Permite pivot a otros sistemas? |
| Business impact | PII, PCI, $$, reputación, downtime |
| Chain potential | ¿Combinable con otro hallazgo? |
| Remediation effort | Hot-fix / sprint / refactor mayor |
| Compensating controls | ¿WAF, MFA, anomaly detection mitigan parcialmente? |

## Matriz de priorización

```
              Bajo esfuerzo    Alto esfuerzo
Alto impacto  ┌────────────┬────────────────┐
              │   QUICK    │   STRATEGIC    │
              │   WIN      │   PROJECT      │
              │ (hacer ya) │ (planificar)   │
              ├────────────┼────────────────┤
Bajo impacto  │   MAYBE    │   IGNORE       │
              │ (backlog)  │ (riesgo aceptado)│
              └────────────┴────────────────┘
```

## Score sugerido (custom)

```
priority_score = CVSS
               + (internet_exposed ? 2 : 0)
               + (anon_exploit ? 2 : 0)
               + (exploit_in_wild ? 3 : 0)
               + (chain_potential ? 1.5 : 0)
               + (sensitive_data ? 2 : 0)
               - (compensating_controls ? 1.5 : 0)
```

## En el informe

Para cada hallazgo:
- **Prioridad de remediación**: Inmediata / 7 días / 30 días / 90 días / Backlog.
- **Justificación de prioridad** (no solo "porque es Critical").
- **Quick win recommendation** si aplica (control compensatorio mientras se trabaja la fix definitiva).

## Tabla ejecutiva ejemplo

| ID | Hallazgo | CVSS | Internet | Auth | Exploit | Prioridad |
|----|----------|------|----------|------|---------|-----------|
| H1 | SQLi en login | 9.8 | Sí | None | Wild | **Inmediata** |
| H2 | BOLA en /orders | 8.6 | Sí | Low | PoC propio | **Inmediata** |
| H3 | XSS reflected en search | 6.1 | Sí | None | Conceptual | 7 días |
| H4 | Outdated jQuery | 5.4 | Sí | None | Conceptual | 30 días |
| H5 | Missing CSP | 3.1 | Sí | N/A | N/A | 90 días |
