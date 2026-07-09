# Referencia de logid (FortiOS 7.4)

Tabla de los `logid` de FortiGate utilizados en `tests/*.log` y cubiertos
por los decoders/reglas del proyecto. Los valores de `logid` son los
identificadores oficiales de Fortinet (Log Reference de FortiOS); esta
tabla es una referencia práctica para este proyecto, **no** el listado
completo de Fortinet (que tiene varios miles de entradas).

> Fuente oficial completa: FortiOS Log Reference, docs.fortinet.com
> (buscar "FortiOS Log Reference" + versión 7.4).

| logid | type | subtype | Descripción | Decoder | Reglas relacionadas |
|---|---|---|---|---|---|
| 0000000013 | traffic | forward | Log de tráfico de política de firewall | `fortigate-firewall-v5` | 1005 (100500-100510) |
| 0101039951 | event | vpn | SSL-VPN login fallido | `fortigate-vpn` | 1006 (100601-100603) |
| 0101039947 | event | vpn | SSL-VPN login correcto | `fortigate-vpn` | 1006 (100604-100606) |
| 0101037127 | event | vpn | Error de negociación IPsec phase 1/2 | `fortigate-vpn` | 1006 (100608-100609) |
| 0419016384 | utm | ips | Detección de firma IPS | `fortigate-ips` | 1007 (100700-100712) |
| 0211008192 | utm | virus | Detección de malware/virus | `fortigate-antivirus` | 1008 (100800-100805) |
| 0317013312 | utm | webfilter | Bloqueo/registro de filtrado web | `fortigate-webfilter` | 1009 (100900-100904) |
| 1500032220 | utm | dns | Consulta DNS registrada/filtrada | `fortigate-dns` | 1010 (101000-101004) |
| 0100032001 | event | system | Login administrativo correcto | `fortigate-admin` | 1012 (101201, 101204) |
| 0100032002 | event | system | Login administrativo fallido | `fortigate-admin` | 1012 (101202-101203) |
| 0100020001 | event | system | Reinicio del sistema | `fortigate-admin` | 1013 (101301) |
| 0100044547 | event | system | Actualización de firmware | `fortigate-admin` | 1013 (101302) |
| 0100045000 | event | system | Licencia/contrato FortiGuard expirado | `fortigate-admin` | 1013 (101303) |
| 0100037001 | event | system | Uso crítico de recursos (CPU/memoria/disco) | `fortigate-admin` | 1013 (101304) |
| 0104032002 | event | ha | Heartbeat HA perdido | `fortigate-ha` | 1014 (101402) |
| 0104032003 | event | ha | Failover / conmutación HA | `fortigate-ha` | 1014 (101401, 101404) |
| 0507021521 | anomaly | — | Anomalía de tráfico / ataque DoS detectado | `fortigate-dos` | 1015 (101500-101505) |

## Notas sobre `application` (1011)

Los eventos de Application Control (`type="utm" subtype="app-ctrl"`) usan
en `tests/application.log` un `logid` **ilustrativo** (`1319014336`, con
el prefijo `13` típico de app-ctrl en la documentación de Fortinet) que no
ha sido verificado contra un dispositivo real — el decoder
`fortigate-application` y las reglas 1011 no dependen del valor exacto de
`logid` (usan `type`/`subtype` y campos como `app`/`appcat`), así que
funcionan igual, pero conviene sustituir esa línea por una muestra real
anonimizada de tu FortiGate en cuanto la tengas.

## Cómo añadir un nuevo logid

1. Identifica `type` y `subtype` del log en la documentación oficial de Fortinet.
2. Si ya existe un decoder para esa combinación (ver tabla), no hace falta
   tocar `decoders/0100-fortigate_decoders.xml`; solo añade reglas nuevas
   en el archivo `rules/10XX-*.xml` correspondiente.
3. Si es una combinación `type`/`subtype` nueva, añade un decoder hijo en
   `0100-fortigate_decoders.xml` siguiendo el patrón existente (regex
   `offset="after_parent"` + `<order>` por cada campo relevante).
4. Añade una línea de ejemplo real (anonimizada) a `tests/*.log` y valida
   con `wazuh-logtest`.
