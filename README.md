# fortigate-wazuh

Integración FortiGate FortiOS 7.4 ↔ Wazuh 4.14 / OpenSearch 2.x sobre Oracle Linux 9.5.

## Estado actual — Fase 1 (entregada)

- `decoders/0100-fortigate_decoders.xml`: decoder raíz `fortigate` + decoder de
  cabecera común + decoders hijos por tipo de log:
  `fortigate-firewall-v5` (traffic), `fortigate-vpn`, `fortigate-ips`,
  `fortigate-antivirus`, `fortigate-webfilter`, `fortigate-dns`,
  `fortigate-application`, `fortigate-admin`, `fortigate-ha`.
- `rules/1005-fortigate-firewall.xml`: 11 reglas base de firewall/tráfico
  (permitido, denegado, escaneo por frecuencia, riesgo FortiGuard, geo-IOC,
  exfiltración por volumen, sesiones largas tipo C2, servicios sensibles,
  correlación escaneo→acceso, implicit deny), con MITRE ATT&CK y grupos
  `pci_dss_*` / `gdpr_*`.
- `lists/`: `fortigate-ioc`, `fortigate-services`, `fortigate-admins`,
  `fortigate-malware` (contenido de ejemplo — deben depurarse antes de producción).
- `tests/firewall.log`: 9 eventos de ejemplo (accept, deny, escaneo por
  frecuencia, exfiltración/sesión larga) para validar con `wazuh-logtest`.

## Estado actual — Fase 2 (entregada)

- Decoder `fortigate-vpn` ampliado: ahora reconoce tanto `type="vpn"`
  (IPsec clásico) como `type="event" subtype="vpn"` (SSL-VPN en FortiOS 7.x),
  con campos adicionales `logdesc`, `login`, `usergroup`, `dst_host`.
- `rules/1006-fortigate-vpn.xml`: 10 reglas — login SSL-VPN fallido,
  fuerza bruta por IP, password spraying por cuenta, login correcto,
  correlación login-exitoso-tras-fuerza-bruta, sesiones concurrentes del
  mismo usuario desde IPs distintas, logout, errores/caídas IPsec repetidas,
  fallo de MFA. MITRE: T1110, T1110.001, T1110.003, T1078, T1111, T1499.
- `tests/vpn.log`: 13 eventos (fuerza bruta de 5 intentos, login posterior,
  sesión concurrente desde otra IP, flapping IPsec de 5 errores).

## Estado actual — Fase 3 (entregada)

- Decoder `fortigate-ips` ampliado con `crscore`, `crlevel`, `profile`,
  `incidentserialno`.
- `rules/1007-fortigate-ips.xml`: 12 reglas — severidad (low/medium/high/
  critical), ataque no bloqueado vs bloqueado, ataques repetidos desde
  mismo origen (recon), mismo ataque repetido contra mismo destino
  (explotación persistente), categorías por texto de firma (web attack,
  fuerza bruta, C2/backdoor), y correlación con lista IOC por IP
  (`address_match_key`). MITRE: T1190, T1210, T1595.002, T1110, T1071, T1105,
  T1059.
- `lists/fortigate-ioc` ampliada con IPs de ejemplo para el lookup por
  dirección (además de los países ya existentes para el lookup por texto).
- `tests/ips.log`: 7 eventos (RCE crítico no bloqueado, ataques web
  repetidos desde el mismo origen, tráfico C2 detectado).

## Estado actual — Fase 4 (entregada): categorías 1008–1015 y 1099

Todos los ficheros de `rules/` y sus decoders correspondientes están
completos y **validados con `xmllint`** (sintaxis XML correcta) y **sin IDs
de regla duplicados**:

| Archivo | Reglas | Contenido |
|---|---|---|
| `1005-fortigate-firewall.xml` | 11 | accept/deny, escaneo, riesgo FortiGuard, geo-IOC, exfiltración, sesiones largas, correlación interna |
| `1006-fortigate-vpn.xml` | 11 | SSL-VPN/IPsec: fuerza bruta, password spraying, sesiones concurrentes, MFA, flapping IPsec |
| `1007-fortigate-ips.xml` | 13 | severidad, bloqueado/no bloqueado, recon, explotación persistente, web/C2/fuerza bruta, IOC |
| `1008-fortigate-antivirus.xml` | 6 | detección, malware crítico (lista), ransomware, reinfección, origen de descarga |
| `1009-fortigate-webfilter.xml` | 5 | bloqueo, categorías de alto riesgo, phishing repetido, evasión/proxy |
| `1010-fortigate-dns.xml` | 5 | TLD de riesgo, DGA/tunneling, volumen anómalo, tipos de consulta inusuales |
| `1011-fortigate-application.xml` | 4 | categorías de riesgo, acceso remoto no autorizado, almacenamiento en la nube |
| `1012-fortigate-admin.xml` | 7 | login OK/fallido, fuerza bruta, cuenta no autorizada, protocolo inseguro, cambio de config |
| `1013-fortigate-system.xml` | 5 | reboot, firmware, licencia, recursos críticos, factory reset |
| `1014-fortigate-ha.xml` | 5 | failover, heartbeat perdido, nuevo miembro, flapping de cluster |
| `1015-fortigate-dos.xml` | 6 | anomalía, bloqueado/no bloqueado, flood, DoS crítico repetido |
| `1099-fortigate-correlation.xml` | 7 | 7 cadenas de ataque cruzadas entre módulos (ver abajo) |
| **Total** | **85** | |

**Correlaciones cruzadas (1099)**: recon→exploit, exploit-IPS→VPN,
malware→C2-DNS, admin-no-autorizado→cambio-config, DoS→failover-HA,
fuerza-bruta-VPN+admin (mismo IP), phishing→malware (cadena de infección
completa).

Se han añadido también los decoders que faltaban: `fortigate-dos`
(`type="anomaly"`) y ampliaciones de `fortigate-vpn` e `fortigate-ips`.
Todos los `tests/*.log` están creados (uno por categoría) y listos para
`wazuh-logtest`.

> **Importante — orden de carga**: `1013-fortigate-system.xml` reutiliza la
> regla base `101200` de `1012-fortigate-admin.xml`, y `1099-fortigate-
> correlation.xml` reutiliza reglas de todos los demás ficheros. Si usas
> `<rule_dir>` en `ossec.conf` esto no es un problema (Wazuh carga primero
> todas las reglas y resuelve referencias después), pero si copias los
> ficheros manualmente asegúrate de que **todos** estén presentes antes de
> reiniciar el manager.

## Pendiente

- 5 dashboards `.ndjson` (Overview, Threats, VPN, IPS, Administration)
- `docs/mitre.md`, `docs/logid-reference.md`, `docs/troubleshooting.md`
- `INSTALL.md`, `CHANGELOG.md`, `LICENSE`
- Para llegar a las 150+ reglas previstas originalmente: ampliar
  granularidad (más firmas IPS por categoría, más anomalías DoS
  específicas por tipo de flood, reglas por franja horaria en VPN, etc.)

## Cómo probar (Wazuh manager en Oracle Linux 9.5)

```bash
sudo cp decoders/0100-fortigate_decoders.xml /var/ossec/etc/decoders/
sudo cp rules/1005-fortigate-firewall.xml /var/ossec/etc/rules/
sudo cp lists/* /var/ossec/etc/lists/
# Compilar las listas CDB:
sudo /var/ossec/bin/cdb_list -a fortigate-ioc /var/ossec/etc/lists/fortigate-ioc 2>/dev/null || true
sudo systemctl restart wazuh-manager

sudo /var/ossec/bin/wazuh-logtest
# Pega una línea de tests/firewall.log y confirma:
#  - decoder.name = fortigate-firewall-v5
#  - regla disparada (100501 accept / 100502 deny / 100503 escaneo, etc.)
```

> Nota: las reglas de correlación por frecuencia (100503, 100509) requieren
> enviar varias líneas seguidas (mismo `srcip`) dentro de la ventana de
> tiempo indicada — `wazuh-logtest` en modo interactivo sirve para esto.
