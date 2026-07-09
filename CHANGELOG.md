# Changelog

Todas las fechas en hora local del proyecto (2026).

## [0.5.0] - 2026-07-09

### Añadido
- `dashboards/*.ndjson` (5 dashboards para OpenSearch Dashboards / Wazuh
  Dashboard): FortiGate Overview, Threats, VPN, IPS, Administration.
  Generados con `scripts/generate_dashboards.py`; JSON y referencias
  internas validadas automáticamente (7 saved objects por dashboard:
  1 index-pattern + 5 visualizaciones + 1 dashboard).
- `docs/mitre.md`: mapeo completo de las 33 técnicas MITRE ATT&CK usadas
  en el ruleset, agrupadas por táctica.
- `docs/logid-reference.md`: tabla de `logid` de FortiGate cubiertos por
  cada decoder, con referencias cruzadas a las reglas.
- `docs/troubleshooting.md`: 7 problemas comunes y su resolución
  (decodificación, reglas de correlación, listas CDB, IDs duplicados, etc.)
- `INSTALL.md`: guía paso a paso completa (copia de archivos, compilación
  de listas CDB, configuración de syslog en FortiGate, validación,
  importación de dashboards).
- `LICENSE` (MIT).
- `tests/application.log` (Application Control), pendiente en fases
  anteriores.

### Corregido
- `docs/logid-reference.md` documenta que el `logid` usado en
  `tests/application.log` es ilustrativo y no ha sido verificado contra
  un dispositivo real.

## [0.4.0] - 2026-07-09

### Añadido
- `rules/1008-fortigate-antivirus.xml` (6 reglas): detección de malware,
  malware crítico vía lista, ransomware, reinfección, origen de descarga.
- `rules/1009-fortigate-webfilter.xml` (5 reglas): bloqueo, categorías de
  alto riesgo, correlación de phishing repetido, evasión/proxy.
- `rules/1010-fortigate-dns.xml` (5 reglas): TLD de riesgo, DGA/tunneling,
  volumen anómalo de consultas, tipos de consulta inusuales.
- `rules/1011-fortigate-application.xml` (4 reglas): categorías de riesgo,
  acceso remoto no autorizado, almacenamiento en la nube.
- `rules/1012-fortigate-admin.xml` (7 reglas): login OK/fallido, fuerza
  bruta, cuenta no autorizada (lista), protocolo inseguro, cambio de config.
- `rules/1013-fortigate-system.xml` (5 reglas): reboot, firmware, licencia,
  recursos críticos, factory reset. Depende de la base `101200` de 1012.
- `rules/1014-fortigate-ha.xml` (5 reglas): failover, heartbeat perdido,
  nuevo miembro, flapping de cluster.
- `rules/1015-fortigate-dos.xml` (6 reglas): anomalía, bloqueado/no
  bloqueado, flood, DoS crítico repetido.
- `rules/1099-fortigate-correlation.xml` (7 reglas): correlación cruzada
  entre módulos (recon→exploit, exploit-IPS→VPN, malware→C2-DNS,
  admin-no-autorizado→config, DoS→failover-HA, fuerza-bruta multivector,
  cadena de infección phishing→malware).
- Decoders nuevos: `fortigate-dos` (`type="anomaly"`).
- `tests/antivirus.log`, `webfilter.log`, `dns.log`, `admin.log`,
  `system.log`, `ha.log`, `dos.log`.

### Validado
- Sintaxis XML de todos los decoders y reglas verificada con `xmllint`.
- Ausencia de IDs de regla duplicados verificada (85 reglas totales).

## [0.3.0] - 2026-07-09

### Añadido
- `rules/1007-fortigate-ips.xml` (13 reglas): severidad, bloqueado/no
  bloqueado, ataques repetidos (recon/persistencia), categorías por firma
  (web/fuerza bruta/C2), correlación con lista IOC por IP.
- Decoder `fortigate-ips` ampliado (`crscore`, `crlevel`, `profile`,
  `incidentserialno`).
- `lists/fortigate-ioc` ampliada con IPs de ejemplo.
- `tests/ips.log`.

## [0.2.0] - 2026-07-09

### Añadido
- `rules/1006-fortigate-vpn.xml` (11 reglas): login SSL-VPN fallido/
  correcto, fuerza bruta, password spraying, correlación login-tras-
  ataque, sesiones concurrentes, logout, errores/flapping IPsec, MFA.
- Decoder `fortigate-vpn` ampliado para reconocer tanto `type="vpn"` como
  `type="event" subtype="vpn"` (SSL-VPN en FortiOS 7.x).
- `tests/vpn.log`.

## [0.1.0] - 2026-07-09

### Añadido
- Estructura inicial del proyecto.
- `decoders/0100-fortigate_decoders.xml`: decoder raíz `fortigate`,
  decoder de cabecera común, y decoders hijos para firewall, vpn, ips,
  antivirus, webfilter, dns, application, admin, ha (base).
- `rules/1005-fortigate-firewall.xml` (11 reglas): tráfico permitido/
  denegado, escaneo por frecuencia, riesgo FortiGuard, geo-IOC,
  exfiltración por volumen, sesiones largas, servicios sensibles,
  correlación interna, implicit deny.
- `lists/fortigate-ioc`, `fortigate-services`, `fortigate-admins`,
  `fortigate-malware` (contenido de ejemplo).
- `tests/firewall.log`.
- `README.md`.

## Pendiente para 1.0.0

- Dashboards `.ndjson` sin probar contra una instancia real de OpenSearch
  Dashboards (ver aviso en README.md).
- Ampliar de 85 a 150+ reglas si se requiere mayor granularidad.
- Sustituir contenido de ejemplo en `lists/` por datos reales del entorno.
- Validación end-to-end contra un Wazuh manager real (no realizada en
  este entorno de desarrollo, sin acceso de red).
