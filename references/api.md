# API Security (REST / SOAP)

GraphQL en `graphql.md`.

## OWASP API Top 10 (2023)

| ID | Nombre |
|----|--------|
| API1 | Broken Object Level Authorization (BOLA/IDOR) |
| API2 | Broken Authentication |
| API3 | Broken Object Property Level Authorization (mass assignment) |
| API4 | Unrestricted Resource Consumption |
| API5 | Broken Function Level Authorization |
| API6 | Unrestricted Access to Sensitive Business Flows |
| API7 | Server Side Request Forgery |
| API8 | Security Misconfiguration |
| API9 | Improper Inventory Management |
| API10 | Unsafe Consumption of APIs |

## Discovery

```bash
# Endpoints desde JS
katana -u https://app.target.cl -jc | grep -E '/api/|/v[0-9]+/'

# Shadow API (versiones sin documentar)
ffuf -u https://api.target.cl/v1/FUZZ -w api-endpoints.txt
ffuf -u https://api.target.cl/FUZZ/users -w common-paths.txt  # v1, v2, v3, beta, internal

# OpenAPI / Swagger común
for p in swagger.json swagger.yaml openapi.json openapi.yaml api-docs swagger-ui swagger /v2/api-docs; do
  curl -s -o /dev/null -w "%{http_code} $p\n" https://api.target.cl/$p
done
```

## BOLA / IDOR (API1)

Estrategia:
1. Identificar todos los endpoints con identificador en path o body (`/users/123`, `/orders/abc`, `?id=`).
2. Crear dos cuentas (A y B).
3. Repetir cada request de A reemplazando ID por el de B.
4. Esperar 401/403; si responde 200/404 con datos = BOLA.

Burp `Autorize` automatiza esto. **Recordatorio (lección operativa):** un 404 inesperado donde se debería ver 401/403 confirma BOLA — el server procesó sin validar identidad.

## Mass Assignment (API3)

Probar enviar campos extra en `POST/PATCH/PUT`:
```json
{
  "username": "test",
  "email": "test@x.cl",
  "isAdmin": true,
  "role": "admin",
  "verified": true,
  "balance": 999999
}
```

## Function Level Auth (API5)

Endpoints administrativos accesibles a usuario normal:
- `/admin/users`, `/internal/`, `/api/v1/admin/`
- Métodos no permitidos: usar `OPTIONS` para enumerar (`Allow: GET, POST, DELETE`).
- Cambiar verbo: `GET` → `PUT`, `POST` → `DELETE`.

## Rate-limit / Resource Consumption (API4)

```bash
# Probar paginación abusiva
curl "https://api.target.cl/users?limit=999999"

# Bypass por header
curl -H "X-Forwarded-For: 1.1.1.1" -H "X-Real-IP: 1.1.1.1" ...

# Burst test
seq 100 | xargs -P 100 -I{} curl -s https://api.target.cl/login -d "user=a&pass=b"
```

## Schemathesis (property-based testing desde OpenAPI)

```bash
schemathesis run https://api.target.cl/openapi.json --checks all
```

Detecta: status code mismatch, esquema roto, server errors, headers faltantes.

## Postman / Insomnia

- Importar OpenAPI/Swagger → testear cada endpoint con auth válida e inválida.
- Pre-request scripts para refresh de token.

## Astra (Postman collection scanner)

```bash
python astra.py -u https://api.target.cl -c collection.json
```

## inql (GraphQL → ver `graphql.md`)

## Patrón operativo

1. Mapear: `endpoints + métodos + auth + parámetros`.
2. Para cada endpoint, probar: BOLA, mass assignment, auth bypass, rate-limit, params hidden (arjun).
3. Documentar en tabla por endpoint con resultados.
