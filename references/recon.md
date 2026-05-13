# Recon / OSINT / ASM

## Subdominios (passive primero, active después)

```bash
# Passive
subfinder -d target.cl -all -silent -o subs_passive.txt
amass enum -passive -d target.cl -o subs_amass.txt
assetfinder --subs-only target.cl > subs_af.txt
findomain -t target.cl -u subs_fd.txt

# Active / brute (con resolvers limpios)
shuffledns -d target.cl -w wordlist.txt -r resolvers.txt -o subs_brute.txt
dnsx -l subs_all.txt -resp -a -aaaa -cname -o resolved.txt
```

Consolida y deduplica:
```bash
cat subs_*.txt | sort -u > subs_all.txt
```

## Probing HTTP/HTTPS

```bash
httpx -l subs_all.txt -title -tech-detect -status-code -web-server -ip -o live.txt
```

## Crawling y endpoints

```bash
katana -u https://target.cl -d 5 -jc -kf all -o endpoints.txt
hakrawler -url https://target.cl -depth 3 -plain >> endpoints.txt
gau target.cl >> endpoints_archive.txt
waybackurls target.cl >> endpoints_archive.txt
```

## Screenshots para triage visual

```bash
aquatone -ports 80,443,8080,8443 < live.txt
# o
eyewitness --web -f live.txt -d eyewitness_out
```

Útil para ubicar paneles admin, Jenkins, Grafana, Kibana, dev/staging expuestos.

## Port scanning

```bash
naabu -l live.txt -top-ports 1000 -o ports.txt
masscan -p1-65535 --rate 1000 -iL ips.txt -oG masscan.gnmap
nmap -sV -sC -p- -iL ips.txt -oA nmap_full
```

## Tech fingerprinting

```bash
whatweb -a 3 https://target.cl
httpx -l live.txt -tech-detect -title
wappalyzer-cli https://target.cl   # o extensión navegador
```

## ASN / IP intelligence

```bash
amass intel -org "Target Inc"
amass intel -asn 12345
```

## OSINT humano / docs

- `theHarvester -d target.cl -b all`
- `recon-ng` (workspaces + módulos)
- Maltego para grafos
- Google dorks: `site:target.cl ext:pdf`, `intitle:"index of"`, etc.

## Continuous recon

Stack ProjectDiscovery + Notify para diffs:
```bash
chaos -d target.cl | dnsx | httpx -silent | notify -bulk -id slack
```

Monitorea:
- Cambios en certificados (crt.sh, certstream)
- Nuevos subdominios
- Nuevos JS endpoints (diff JS bundles)
- Nuevos buckets

## Secret hunting en repos públicos

Ver `secrets.md`.

## Output esperado por fase

| Fase | Archivo |
|------|---------|
| Subdominios | `subs_all.txt` |
| Resueltos | `resolved.txt` |
| HTTP vivos | `live.txt` |
| Endpoints | `endpoints.txt` |
| Puertos | `ports.txt` |
| Screenshots | `aquatone_out/` |
| Tech | `tech.json` |

Llevar todo a un único directorio `recon/<target>/<YYYY-MM-DD>/` para versionado.
