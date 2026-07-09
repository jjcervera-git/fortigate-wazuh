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

## Pendiente (fases siguientes)

Los archivos `rules/1006` a `1015` y `1099-fortigate-correlation.xml`,
los dashboards `.ndjson` y la documentación completa (`docs/mitre.md`,
`docs/logid-reference.md`, `docs/troubleshooting.md`, `INSTALL.md`,
`CHANGELOG.md`, `LICENSE`) **todavía no se han generado** — se irán
construyendo módulo a módulo sobre esta misma base de decoders, siguiendo
el mismo patrón (regex `after_parent` + `<order>`, MITRE, niveles de
severidad 3–15) para llegar a las 150+ reglas previstas:

| Archivo | Contenido previsto |
|---|---|
| `1006-fortigate-vpn.xml` | SSL-VPN / IPsec: login fallido, MFA, geo-anomalías, sesiones concurrentes |
| `1007-fortigate-ips.xml` | Firmas IPS por severidad, ataques repetidos, CVEs críticos |
| `1008-fortigate-antivirus.xml` | Detección malware/ransomware, uso de `lists/fortigate-malware` |
| `1009-fortigate-webfilter.xml` | Categorías bloqueadas, C2/phishing, DLP básico |
| `1010-fortigate-dns.xml` | DNS a dominios maliciosos, DGA, tunneling DNS |
| `1011-fortigate-application.xml` | Apps de alto riesgo (P2P, proxies, VPN no autorizadas) |
| `1012-fortigate-admin.xml` | Login admin fuera de `lists/fortigate-admins`, cambios de config |
| `1013-fortigate-system.xml` | Reinicios, actualizaciones de firmware, fallos de licencia |
| `1014-fortigate-ha.xml` | Failover HA, pérdida de heartbeat |
| `1015-fortigate-dos.xml` | Ataques DoS/DDoS detectados por FortiGate |
| `1099-fortigate-correlation.xml` | Correlación cross-módulo (ej. IPS + VPN + admin) |

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
