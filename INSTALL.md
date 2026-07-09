# Instalación

Requisitos: Wazuh manager 4.14.x sobre Oracle Linux 9.5, acceso `sudo`.

## 1. Copiar decoders y reglas

```bash
sudo cp decoders/0100-fortigate_decoders.xml /var/ossec/etc/decoders/
sudo cp rules/*.xml /var/ossec/etc/rules/
sudo cp lists/* /var/ossec/etc/lists/
```

## 2. Compilar las listas CDB

```bash
for f in /var/ossec/etc/lists/fortigate-*; do
  sudo /var/ossec/bin/cdb_list -a "$(basename "$f")" "$f"
done
```

> Antes de producción, edita `lists/fortigate-ioc`, `fortigate-admins` y
> `fortigate-malware`: el contenido actual es de ejemplo.

## 3. Validar sintaxis antes de reiniciar

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

Si devuelve `Configuration OK`, continúa. Si hay errores, revisa
`docs/troubleshooting.md`.

## 4. Reiniciar el manager

```bash
sudo systemctl restart wazuh-manager
sudo systemctl status wazuh-manager
```

## 5. Configurar la recepción de logs de FortiGate

En `/var/ossec/etc/ossec.conf`, en la sección `<ossec_config>` del manager,
añade (o confirma que existe) un bloque de syslog remoto para el puerto que
uses en FortiGate (UDP 514 por defecto, TCP 514 recomendado en producción):

```xml
<remote>
  <connection>syslog</connection>
  <port>514</port>
  <protocol>udp</protocol>
  <allowed-ips>IP_DEL_FORTIGATE/32</allowed-ips>
</remote>
```

En el FortiGate (CLI), configura el envío de logs al Wazuh manager:

```
config log syslogd setting
    set status enable
    set server "IP_DEL_WAZUH_MANAGER"
    set port 514
    set format default
    set facility local7
end
```

Reinicia el manager tras cambiar `ossec.conf`:

```bash
sudo systemctl restart wazuh-manager
```

## 6. Validar con `wazuh-logtest`

```bash
sudo /var/ossec/bin/wazuh-logtest
```

Pega una línea de cualquier archivo en `tests/*.log` y confirma:
- `decoder.name` correcto (ver `docs/logid-reference.md`)
- Regla disparada con el nivel/descr. esperados

## 7. Importar dashboards (OpenSearch Dashboards / Wazuh Dashboard)

Desde la interfaz: **Stack Management → Saved Objects → Import**, sube
cada archivo de `dashboards/*.ndjson`. Requiere que el índice
`wazuh-alerts-*` ya exista (se crea automáticamente al llegar el primer
evento).

## 8. Habilitar reglas en el grupo si usas filtrado por grupo

Si tu configuración de Wazuh filtra reglas por `<group>` en algún nivel
superior, asegúrate de que `fortigate` está incluido en los grupos
permitidos.
