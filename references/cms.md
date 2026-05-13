# CMS Hacking

## WordPress — WPScan

```bash
# Update
wpscan --update

# Enum básico
wpscan --url https://target.cl --enumerate u,p,t,vp,vt --random-user-agent

# Con API token (CVE data)
wpscan --url https://target.cl -e u,p,vp --api-token YOUR_TOKEN

# Brute users
wpscan --url https://target.cl --usernames admin,user --passwords rockyou.txt

# Plugins solo
wpscan --url https://target.cl -e ap --plugins-detection aggressive
```

Endpoints útiles:
- `/wp-json/wp/v2/users` (enumera usuarios sin auth en versiones vulnerables)
- `/?author=1`, `/?author=2` (enumera por redirect)
- `/wp-content/uploads/` (browsing si está expuesto)
- `/xmlrpc.php` (brute amplificado, pingback SSRF)
- `/wp-config.php.bak`, `.swp`, `~`

## Drupal — droopescan

```bash
droopescan scan drupal -u https://target.cl
```

CVEs históricos: Drupalgeddon (CVE-2014-3704), Drupalgeddon2 (CVE-2018-7600), Drupalgeddon3 (CVE-2018-7602).

## Joomla — joomscan

```bash
joomscan -u https://target.cl
```

## CMS detection

```bash
whatweb -a 3 https://target.cl
wappalyzer https://target.cl
nuclei -u https://target.cl -tags wordpress,drupal,joomla
```

## Patrones comunes en cualquier CMS

- Backups del config en webroot (`wp-config.php.bak`, `.git/`).
- Plugins/themes con CVE conocido.
- Admin panel sin MFA (`/wp-admin`, `/user/login`, `/administrator`).
- File upload sin validación de tipo (avatar, media).
- SSRF via plugin de imágenes/oembed/proxy.
- Stored XSS en comentarios o profile fields.
