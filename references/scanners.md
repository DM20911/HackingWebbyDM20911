# Vulnerability Scanners

## nuclei (líder open-source)

Templates YAML, comunidad activa, integrable en CI/CD.

```bash
# Update templates
nuclei -update-templates

# Scan básico
nuclei -u https://target.cl -severity critical,high,medium

# Scan masivo desde lista
nuclei -l live.txt -severity high,critical -rate-limit 100 -o nuclei_out.txt

# Tags específicos
nuclei -u https://target.cl -tags cve,exposure,misconfiguration

# Templates personalizados
nuclei -u https://target.cl -t custom-templates/

# Con proxy a Burp
nuclei -u https://target.cl -proxy http://127.0.0.1:8080
```

Crear template propio (`my-check.yaml`):
```yaml
id: custom-check
info:
  name: Custom check
  severity: medium
http:
  - method: GET
    path: ["{{BaseURL}}/admin"]
    matchers:
      - type: status
        status: [200]
```

## nikto (clásico, ruidoso)

```bash
nikto -h https://target.cl -o nikto.html -Format html
```

Útil para baseline, pero genera mucho ruido. Filtrar manualmente.

## Comerciales (cliente provee licencia)

| Scanner | Foco | Notas |
|---------|------|-------|
| Nessus | Infra + web | Plugins web limitados |
| Acunetix | Web + API | Bueno con SPA y APIs |
| Invicti / Netsparker | Web | Confidence rating fuerte |
| Qualys WAS | Web cloud-based | Reportes ejecutivos |
| AppScan (HCL) | Enterprise | DAST + IAST |
| Burp Suite Enterprise | Web | Integración CI/CD |

## Vega / wapiti

Open source, menos mantenidos. Útiles solo como backup.

## Patrones

- Nunca confíes ciegamente en output de scanner. **Validar manualmente** cada hallazgo antes de reportar.
- Marcar `Confidence` (Confirmed / Likely / Unconfirmed) en el informe.
- Correlacionar resultados de varios scanners + manual; lo que más vale es lo que el scanner NO encontró.
