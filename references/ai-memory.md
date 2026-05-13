# AI Memory & Knowledge Graph Ofensivo

## Por qué importa

El conocimiento ofensivo se acumula. Sin memoria persistente, repites trabajo.

## Qué guardar (por engagement y global)

### Por engagement (project memory)
- Stack tecnológico del target.
- WAF detectado y bypasses que funcionaron.
- Endpoints descubiertos.
- Credenciales / tokens validados (con cuidado de retención).
- Hallazgos confirmados con su evidencia.
- Decisiones arquitecturales que afectaron la prueba.

### Global (user memory, cross-engagement)
- Bypasses de WAFs por proveedor.
- Payloads que funcionaron en contextos específicos (cuando y por qué).
- Gadget chains de deserialización útiles.
- Wordlists/dictionaries que rinden mejor por tipo de target.
- Templates nuclei custom escritos.
- Lecciones aprendidas (qué romper la próxima vez).

## Estructura sugerida

```
~/offensive-knowledge/
├── waf-bypasses/
│   ├── cloudflare.md
│   ├── aws-waf.md
│   └── akamai.md
├── payloads/
│   ├── xss/
│   ├── sqli/
│   ├── ssrf/
│   ├── ssti/
│   └── deserialization/
├── nuclei-templates-custom/
├── wordlists-custom/
├── methodology-notes/
└── engagements/
    ├── client-X-2026-Q1/
    │   ├── recon/
    │   ├── findings/
    │   └── notes.md
    └── ...
```

## Knowledge graph

Modelo conceptual:
```
(Host)-[RUNS]->(Tech)-[VERSION]->(VulnVersion)-[CVE]->(Exploit)
(Host)-[EXPOSES]->(Endpoint)-[ACCEPTS]->(Param)-[VULN_TO]->(Class)
(Engagement)-[FOUND]->(Finding)-[OF_CLASS]->(Class)-[CWE]->(CWEnumber)
(Finding)-[CHAINS_TO]->(Finding)
```

Implementación pragmática: Neo4j local + script Python que ingiere reportes JSON.

Queries útiles:
- "Hosts con tech vulnerable a CVE-X".
- "Findings que comparten patron CWE-Y across engagements".
- "Chains de longitud >= 2 que llevan a RCE".

## AI memory en Claude

Esta skill ya respeta el sistema `auto memory` de tu setup. Para guardar bypass / payload exitoso:

1. Detectar en conversación: "este payload bypaseó el WAF X".
2. Crear memory tipo `feedback` o `reference` con:
   - Categoría (waf-bypass, payload-xss, etc.).
   - Contexto (cuando funciona, cuando no).
   - Por qué funciona.
3. Indexar en `MEMORY.md` global.

## Continuous learning

- Después de cada engagement: 30 min de retro → qué hallazgos fueron nuevos vs repetidos → actualizar metodología.
- Suscribirse a:
  - PortSwigger research blog.
  - HackerOne disclosed reports.
  - Intigriti writeups.
  - GitHub Advisory Database.
  - AWS/GCP/Azure security bulletins.

## Datasets propios

Construir con tiempo:
- Payloads ofensivos categorizados.
- Bypasses de WAFs versionados.
- JWT secrets descubiertos (anonimizar antes).
- Regexes para detección de tecnologías custom.
- Signatures internas.

Útil para fine-tuning de LLM ofensivo o reranking de payloads.
