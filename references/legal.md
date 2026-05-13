# Legal Framework

## Antes de cualquier prueba activa

Confirmar **por escrito**:
- Scope (dominios, IPs, apps móviles, ambientes).
- Out-of-scope explícito (3rd parties, prod sin ventana, integraciones).
- Tipo de prueba autorizada (SAST, DAST, social, red team, etc.).
- Ventanas autorizadas (días, horas, zona horaria).
- Rate-limit acordado.
- Persona autorizadora (debe tener autoridad — CISO, IT director).
- Política sobre datos sensibles encontrados (no dump, redactar en evidencia).
- Disclosure timeline.
- Indemnización / cláusula safe harbor.

## Documento mínimo

**Statement of Work (SoW)** firmado por ambas partes con:
- Identidad cliente y pentester.
- Objetivos.
- Scope detallado.
- Reglas de engagement (RoE).
- Entregables (informe, evidencias, reunión de cierre).
- Confidencialidad / NDA.
- Limitación de responsabilidad.
- Vigencia.

## Bug bounty

Cada plataforma (HackerOne, Intigriti, Bugcrowd) tiene **safe harbor** publicado por el programa. Leer antes de testear:
- Targets in/out of scope.
- Vulnerabilidades aceptadas / rechazadas.
- Restricciones de testing (no DoS, no social engineering, etc.).
- Bounty range.
- Prohibición de auto-disclosure pre-fix.

Si el target está fuera de plataforma pero tiene `security.txt` con `policy:` link, leer y respetar.

## Manejo de evidencia

- **Tokens / credenciales encontradas**: validar minimamente (verify alive, no abuse), reportar inmediato (no esperar al informe), recomendar rotación urgente.
- **PII / datos personales**: redactar en evidencia (mostrar 3-4 chars + asteriscos), NO conservar copia post-engagement.
- **Source code obtenido**: borrar al cierre del engagement salvo retención acordada.
- **Backups locales**: cifrar con `age`/`gpg`, retention según contrato.
- **Cadena de custodia**: timestamp + hash de cada evidencia material.

## Disclosure

- **Coordinated disclosure**: trabajar con vendor antes de publicar.
- **CVE assignment** (MITRE / GitHub Advisory) si vuln es en producto, no instalación.
- **Embargo period** típico: 90 días con extensión razonable.
- **Public writeup** solo con consentimiento del cliente y datos anonimizados.

## Países / jurisdicciones

- **Chile**: Ley 19.223 (delitos informáticos) — **autorización por escrito esencial**.
- **EE.UU.**: CFAA (Computer Fraud and Abuse Act) — autorización clave.
- **EU**: GDPR + Cybersecurity Act + leyes nacionales (NIS2).
- **Brasil**: Marco Civil da Internet + LGPD.

Si trabajas cross-border, considerar jurisdicción del cliente y del target.

## Red flags para rechazar engagement

- "Cliente" pide testear infra de un tercero (probar dominio que no es suyo).
- Sin SoW firmado.
- "Empezamos hoy y firmamos después".
- Pago en cripto sin identificación del cliente.
- Pidiendo retener/abusar de credenciales encontradas.
- Pidiendo DoS / data destruction como prueba.

## En caso de daño accidental

- Detener pruebas.
- Notificar inmediato al contacto del cliente.
- Documentar todo (qué se hacía, comando exacto, hora).
- No intentar "arreglar" sin coordinación (puede empeorar).
- Cooperar con el equipo de respuesta del cliente.
