# Wordlists & Payloads

## Repos

```bash
# SecLists (todo en uno)
git clone https://github.com/danielmiessler/SecLists ~/wordlists/SecLists

# PayloadsAllTheThings
git clone https://github.com/swisskyrepo/PayloadsAllTheThings ~/wordlists/PayloadsAllTheThings

# FuzzDB
git clone https://github.com/fuzzdb-project/fuzzdb ~/wordlists/fuzzdb

# Assetnote (best wordlists)
mkdir ~/wordlists/assetnote && cd ~/wordlists/assetnote
wget -r -np -nH --cut-dirs=2 https://wordlists-cdn.assetnote.io/data/

# Jhaddix all.txt (subdomain)
wget https://gist.githubusercontent.com/jhaddix/86a06c5dc309d08580a018c66354a056/raw/all.txt -O ~/wordlists/jhaddix-all.txt
```

## Top wordlists para usos comunes

| Uso | Wordlist |
|-----|----------|
| Subdominios pequeño | `SecLists/Discovery/DNS/subdomains-top1million-5000.txt` |
| Subdominios grande | `assetnote/best-dns-wordlist.txt` |
| Directorios web | `SecLists/Discovery/Web-Content/raft-medium-directories.txt` |
| Files | `SecLists/Discovery/Web-Content/raft-medium-files.txt` |
| Parámetros | `SecLists/Discovery/Web-Content/burp-parameter-names.txt` |
| API endpoints | `SecLists/Discovery/Web-Content/api/api-endpoints.txt` |
| Backup files | `SecLists/Discovery/Web-Content/Common-DB-Backups.txt` |
| Pwd top | `SecLists/Passwords/Common-Credentials/10-million-password-list-top-10000.txt` |
| RockYou | `/usr/share/wordlists/rockyou.txt` (Kali) |

## Custom wordlist generation

Por target:
```bash
# CeWL — wordlist desde el sitio
cewl -d 3 -m 6 https://target.cl > custom_words.txt

# Combinar nombres empresa, productos, tech
echo -e "target\nproducto1\nadmin\napi\nv1\nv2\ndev\nstage\nuat\nqa" > base.txt

# Kruzz / radamsa para mutaciones
radamsa -n 1000 base.txt > mutated.txt
```

## Payloads esenciales por categoría

Todos en `~/wordlists/PayloadsAllTheThings/`:
- SQL Injection / NoSQL Injection
- XSS Injection
- SSRF
- Command Injection
- Server Side Template Injection
- XPATH Injection
- LDAP Injection
- File Inclusion (LFI/RFI)
- Insecure Deserialization
- JWT
- OAuth Misconfiguration
- File Upload
- Open Redirect
- Race Condition
- Request Smuggling
- WebSockets
- XXE Injection

## Tips

- **Inicia chico** (top-5k) y solo si necesario sube a 100k+.
- Auto-calibrar siempre (ffuf `-ac`).
- Filtrar por status code y tamaño respuesta — los más útiles son los outliers.
- Para subdominios reales (no brute), `subfinder + amass passive` antes de brute.
