# Troubleshooting

## 1. El log no decodifica (`decoder.name` vacío en `wazuh-logtest`)

- Comprueba que la línea empieza literalmente por `date=YYYY-MM-DD
  time=HH:MM:SS` (el decoder raíz `fortigate` exige ese prematch exacto).
  Si tu FortiGate envía con cabecera de syslog delante (prioridad `<189>`,
  timestamp RFC3164, hostname), Wazuh normalmente la separa antes de
  aplicar los decoders — pero si no es así, habrá que ajustar el
  `prematch` de `fortigate` para tolerar ese prefijo.
- Verifica que el `type`/`subtype` del log coincide con alguno de los
  decoders hijos (ver `docs/logid-reference.md`). Si es una combinación
  nueva, hay que añadir un decoder (ver esa misma guía, sección "Cómo
  añadir un nuevo logid").

## 2. Decodifica pero no dispara ninguna regla

- Revisa con `wazuh-logtest` el valor exacto de los campos dinámicos
  (`srcip`, `action`, `severity`, etc.) — un `field name="action"` con
  regex `deny|blocked` no dispara si el valor real es `Deny` (Wazuh es
  sensible a mayúsculas salvo que uses `type="pcre2"` con `(?i)`).
- Comprueba que el archivo de reglas está realmente cargado:
  `sudo /var/ossec/bin/wazuh-analysisd -t` valida la sintaxis y el
  arranque; revisa `/var/ossec/logs/ossec.log` por errores de carga.

## 3. Reglas de correlación (`if_matched_sid`, `frequency`) no disparan

- `frequency`/`timeframe` cuentan repeticiones de la **misma regla ya
  disparada**, no del log crudo. Asegúrate de que la regla base referenciada
  (`100502`, `100601`, etc.) se dispara primero para cada evento individual.
- `same_srcip`, `same_field`, `different_srcip` comparan contra el evento
  que disparó la regla referenciada en `if_matched_sid`/`if_sid`, dentro de
  la ventana `timeframe`. Con `wazuh-logtest` en modo interactivo, pega las
  líneas una a una y en orden — el estado de frecuencia se mantiene durante
  la sesión.
- `1013-fortigate-system.xml` reutiliza la regla `101200` definida en
  `1012-fortigate-admin.xml`, y `1099-fortigate-correlation.xml` reutiliza
  reglas de casi todos los demás ficheros. Si copiaste manualmente solo
  algunos archivos a `/var/ossec/etc/rules/`, esas referencias fallarán
  silenciosamente (la regla dependiente simplemente no se compila/dispara).
  Copia siempre el directorio `rules/` completo.

## 4. Las listas CDB no funcionan (`list`/`lookup`)

- Las listas de texto plano en `lists/` deben compilarse a formato CDB
  antes de que Wazuh las use:
  ```bash
  for f in /var/ossec/etc/lists/fortigate-*; do
    sudo /var/ossec/bin/cdb_list -a "$(basename "$f")" "$f"
  done
  sudo systemctl restart wazuh-manager
  ```
- `lookup="address_match_key"` espera IPs o rangos CIDR; si la lista tiene
  texto que no es una IP (como los nombres de país en `fortigate-ioc`),
  esas líneas simplemente no matchean para ese lookup — no es un error,
  pero puede llevar a falsos negativos si esperabas que matchearan.

## 5. Reglas duplicadas / conflicto de IDs con otro ruleset

- Este proyecto usa el rango `100500-101599` (más `109901-109907` para
  correlación). Si ya tienes otro ruleset custom en ese rango, cambia los
  IDs antes de desplegar — Wazuh no arranca si hay `id` de regla
  duplicados en el conjunto activo. Verifícalo con:
  ```bash
  grep -rhoE '<rule id="[0-9]+"' /var/ossec/etc/rules/*.xml \
    | grep -oE '[0-9]+' | sort | uniq -d
  ```

## 6. OpenSearch / Wazuh Dashboard no muestra los campos nuevos

- Los campos dinámicos añadidos por los decoders (`data.srcip`,
  `data.attack`, `data.crlevel`, etc.) requieren refrescar el index
  pattern `wazuh-alerts-*` en el Dashboard (Stack Management → Index
  Patterns → Refresh) después de que empiecen a llegar eventos con esos
  campos, para que aparezcan como columnas filtrables.

## 7. Rendimiento: muchos `<regex offset="after_parent">` por decoder

- El patrón usado en este proyecto (varios regex independientes por
  decoder para tolerar campos en cualquier orden) es robusto pero más
  costoso en CPU que un único regex de captura fija. En entornos de muy
  alto volumen (varios miles de EPS), si el rendimiento de `wazuh-analysisd`
  se convierte en un cuello de botella, considera reducir el número de
  campos extraídos a los estrictamente necesarios para las reglas activas.
