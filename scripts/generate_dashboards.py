import json

INDEX_ID = "wazuh-alerts-fortigate"
INDEX_TITLE = "wazuh-alerts-*"

def index_pattern_obj():
    return {
        "type": "index-pattern",
        "id": INDEX_ID,
        "attributes": {
            "title": INDEX_TITLE,
            "timeFieldName": "timestamp"
        },
        "references": [],
        "migrationVersion": {"index-pattern": "7.6.0"},
        "coreMigrationVersion": "7.6.0"
    }

def vis_search_source(extra_filter_kuery=""):
    query = extra_filter_kuery if extra_filter_kuery else ""
    return json.dumps({
        "index": INDEX_ID,
        "query": {"query": query, "language": "kuery"},
        "filter": []
    })

def visualization_obj(vis_id, title, vis_state, kuery=""):
    return {
        "type": "visualization",
        "id": vis_id,
        "attributes": {
            "title": title,
            "visState": json.dumps(vis_state),
            "uiStateJSON": "{}",
            "description": "",
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": vis_search_source(kuery)
            }
        },
        "references": [
            {"id": INDEX_ID, "name": "kibanaSavedObjectMeta.searchSourceJSON.index", "type": "index-pattern"}
        ],
        "migrationVersion": {"visualization": "7.10.0"},
        "coreMigrationVersion": "7.10.0"
    }

def date_histogram_vis(vis_id, title, kuery=""):
    vis_state = {
        "title": title,
        "type": "histogram",
        "params": {
            "type": "histogram",
            "grid": {"categoryLines": False},
            "categoryAxes": [{"id": "CategoryAxis-1", "type": "category", "position": "bottom", "show": True,
                               "scale": {"type": "linear"}, "labels": {"show": True, "truncate": 100}, "title": {}}],
            "valueAxes": [{"id": "ValueAxis-1", "name": "LeftAxis-1", "type": "value", "position": "left",
                            "show": True, "scale": {"type": "linear", "mode": "normal"},
                            "labels": {"show": True, "rotate": 0, "filter": False, "truncate": 100},
                            "title": {"text": "Eventos"}}],
            "seriesParams": [{"show": True, "type": "histogram", "mode": "stacked", "data": {"label": "Count", "id": "1"},
                                "valueAxis": "ValueAxis-1", "drawLinesBetweenPoints": True, "showCirclesOnLines": True,
                                "interpolate": "linear", "lineWidth": 2}],
            "addTooltip": True, "addLegend": True, "legendPosition": "right", "times": [], "addTimeMarker": False
        },
        "aggs": [
            {"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}},
            {"id": "2", "enabled": True, "type": "date_histogram", "schema": "segment",
             "params": {"field": "timestamp", "timeRange": {"from": "now-7d", "to": "now"}, "useNormalizedEsInterval": True,
                        "interval": "auto", "drop_partials": False, "min_doc_count": 1, "extended_bounds": {}}}
        ]
    }
    return visualization_obj(vis_id, title, vis_state, kuery)

def pie_vis(vis_id, title, field, size=10, kuery=""):
    vis_state = {
        "title": title,
        "type": "pie",
        "params": {"type": "pie", "addTooltip": True, "addLegend": True, "legendPosition": "right",
                    "isDonut": True, "labels": {"show": False, "values": True, "last_level": True, "truncate": 100}},
        "aggs": [
            {"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}},
            {"id": "2", "enabled": True, "type": "terms", "schema": "segment",
             "params": {"field": field, "orderBy": "1", "order": "desc", "size": size, "otherBucket": False,
                        "otherBucketLabel": "Other", "missingBucket": False, "missingBucketLabel": "Missing"}}
        ]
    }
    return visualization_obj(vis_id, title, vis_state, kuery)

def table_vis(vis_id, title, field, size=10, kuery=""):
    vis_state = {
        "title": title,
        "type": "table",
        "params": {"perPage": 10, "showPartialRows": False, "showMetricsAtAllLevels": False,
                    "showTotal": True, "totalFunc": "sum"},
        "aggs": [
            {"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}},
            {"id": "2", "enabled": True, "type": "terms", "schema": "bucket",
             "params": {"field": field, "orderBy": "1", "order": "desc", "size": size, "otherBucket": False,
                        "otherBucketLabel": "Other", "missingBucket": False, "missingBucketLabel": "Missing"}}
        ]
    }
    return visualization_obj(vis_id, title, vis_state, kuery)

def metric_vis(vis_id, title, kuery=""):
    vis_state = {
        "title": title,
        "type": "metric",
        "params": {"metric": {"percentageMode": False, "useRanges": False, "colorSchema": "Green to Red",
                                "metricColorMode": "None", "colorsRange": [{"from": 0, "to": 10000}],
                                "labels": {"show": True}, "invertColors": False, "style": {"bgFill": "#000",
                                "bgColor": False, "labelColor": False, "subText": "", "fontSize": 60}}},
        "aggs": [{"id": "1", "enabled": True, "type": "count", "schema": "metric", "params": {}}]
    }
    return visualization_obj(vis_id, title, vis_state, kuery)

def dashboard_obj(dash_id, title, description, panels):
    panels_json = []
    references = []
    for i, (vis_id, x, y, w, h) in enumerate(panels):
        ref_name = f"panel_{i}"
        panels_json.append({
            "version": "7.10.0",
            "type": "visualization",
            "gridData": {"x": x, "y": y, "w": w, "h": h, "i": str(i)},
            "panelIndex": str(i),
            "embeddableConfig": {},
            "panelRefName": ref_name
        })
        references.append({"id": vis_id, "name": ref_name, "type": "visualization"})
    return {
        "type": "dashboard",
        "id": dash_id,
        "attributes": {
            "title": title,
            "hits": 0,
            "description": description,
            "panelsJSON": json.dumps(panels_json),
            "optionsJSON": json.dumps({"useMargins": True, "hidePanelTitles": False}),
            "version": 1,
            "timeRestore": True,
            "timeTo": "now",
            "timeFrom": "now-24h",
            "refreshInterval": {"pause": True, "value": 0},
            "kibanaSavedObjectMeta": {
                "searchSourceJSON": json.dumps({"query": {"query": "", "language": "kuery"}, "filter": []})
            }
        },
        "references": references,
        "migrationVersion": {"dashboard": "7.9.3"},
        "coreMigrationVersion": "7.9.3"
    }

def write_ndjson(path, objects):
    with open(path, "w") as f:
        for obj in objects:
            f.write(json.dumps(obj) + "\n")

# ---------------------------------------------------------------------------
# 1. FortiGate Overview
# ---------------------------------------------------------------------------
ov_hist = date_histogram_vis("fg-ov-timeline", "FortiGate - Eventos en el tiempo", "rule.groups:fortigate")
ov_pie_groups = pie_vis("fg-ov-groups", "FortiGate - Eventos por categoria", "rule.groups", 12, "rule.groups:fortigate")
ov_metric_total = metric_vis("fg-ov-total", "FortiGate - Total de eventos", "rule.groups:fortigate")
ov_table_srcip = table_vis("fg-ov-top-srcip", "FortiGate - Top 10 IP origen", "data.srcip", 10, "rule.groups:fortigate")
ov_pie_level = pie_vis("fg-ov-level", "FortiGate - Distribucion por nivel de regla", "rule.level", 10, "rule.groups:fortigate")
overview_dashboard = dashboard_obj(
    "fortigate-overview", "FortiGate Overview",
    "Vision general de todos los eventos FortiGate procesados por Wazuh: volumen, categorias, top IPs origen y distribucion por severidad.",
    [("fg-ov-total", 0, 0, 12, 8),
     ("fg-ov-timeline", 12, 0, 36, 15),
     ("fg-ov-groups", 0, 8, 24, 15),
     ("fg-ov-level", 24, 8, 24, 15),
     ("fg-ov-top-srcip", 0, 23, 48, 15)]
)
write_ndjson("dashboards/FortiGate Overview.ndjson",
             [index_pattern_obj(), ov_hist, ov_pie_groups, ov_metric_total, ov_table_srcip, ov_pie_level, overview_dashboard])

# ---------------------------------------------------------------------------
# 2. FortiGate Threats (AV, Webfilter, DNS, DoS, correlacion)
# ---------------------------------------------------------------------------
th_kuery = "rule.groups:(fortigate_antivirus or fortigate_webfilter or fortigate_dns or fortigate_dos or fortigate_correlation)"
th_timeline = date_histogram_vis("fg-th-timeline", "Amenazas - Eventos en el tiempo", th_kuery)
th_pie_virus = pie_vis("fg-th-top-virus", "Top malware detectado", "data.virus", 10, "rule.groups:fortigate_antivirus")
th_table_webcat = table_vis("fg-th-webcat", "Top categorias webfilter bloqueadas", "data.catdesc", 10, "rule.groups:fortigate_webfilter")
th_table_correlation = table_vis("fg-th-correlation", "Alertas de correlacion (multi-etapa)", "rule.description", 10, "rule.groups:fortigate_correlation")
th_metric_critical = metric_vis("fg-th-critical", "Alertas nivel >= 12", "rule.level >= 12 and rule.groups:fortigate")
threats_dashboard = dashboard_obj(
    "fortigate-threats", "FortiGate Threats",
    "Panel de amenazas: malware, sitios maliciosos, DNS sospechoso, DoS y alertas de correlacion multi-etapa.",
    [("fg-th-critical", 0, 0, 12, 8),
     ("fg-th-timeline", 12, 0, 36, 15),
     ("fg-th-top-virus", 0, 8, 24, 15),
     ("fg-th-webcat", 24, 8, 24, 15),
     ("fg-th-correlation", 0, 23, 48, 15)]
)
write_ndjson("dashboards/FortiGate Threats.ndjson",
             [index_pattern_obj(), th_timeline, th_pie_virus, th_table_webcat, th_table_correlation, th_metric_critical, threats_dashboard])

# ---------------------------------------------------------------------------
# 3. FortiGate VPN
# ---------------------------------------------------------------------------
vpn_kuery = "rule.groups:fortigate_vpn"
vpn_timeline = date_histogram_vis("fg-vpn-timeline", "VPN - Eventos en el tiempo", vpn_kuery)
vpn_table_users = table_vis("fg-vpn-top-users", "Top usuarios VPN", "data.login", 10, vpn_kuery)
vpn_table_srcip = table_vis("fg-vpn-top-srcip", "Top IP origen VPN", "data.srcip", 10, vpn_kuery)
vpn_pie_action = pie_vis("fg-vpn-action", "VPN por accion", "data.action", 10, vpn_kuery)
vpn_metric_bruteforce = metric_vis("fg-vpn-bruteforce", "Alertas de fuerza bruta VPN", "rule.groups:fortigate_vpn_bruteforce")
vpn_dashboard = dashboard_obj(
    "fortigate-vpn", "FortiGate VPN",
    "Actividad SSL-VPN e IPsec: logins, top usuarios y origenes, fuerza bruta y estado de tuneles.",
    [("fg-vpn-bruteforce", 0, 0, 12, 8),
     ("fg-vpn-timeline", 12, 0, 36, 15),
     ("fg-vpn-top-users", 0, 8, 24, 15),
     ("fg-vpn-top-srcip", 24, 8, 24, 15),
     ("fg-vpn-action", 0, 23, 48, 15)]
)
write_ndjson("dashboards/FortiGate VPN.ndjson",
             [index_pattern_obj(), vpn_timeline, vpn_table_users, vpn_table_srcip, vpn_pie_action, vpn_metric_bruteforce, vpn_dashboard])

# ---------------------------------------------------------------------------
# 4. FortiGate IPS
# ---------------------------------------------------------------------------
ips_kuery = "rule.groups:fortigate_ips"
ips_timeline = date_histogram_vis("fg-ips-timeline", "IPS - Eventos en el tiempo", ips_kuery)
ips_pie_severity = pie_vis("fg-ips-severity", "IPS por severidad", "data.severity", 6, ips_kuery)
ips_table_attack = table_vis("fg-ips-top-attack", "Top firmas IPS", "data.attack", 15, ips_kuery)
ips_table_srcip = table_vis("fg-ips-top-srcip", "Top IP atacante", "data.srcip", 10, ips_kuery)
ips_metric_notblocked = metric_vis("fg-ips-notblocked", "Ataques alta/critica NO bloqueados", "rule.groups:fortigate_ips_not_blocked")
ips_dashboard = dashboard_obj(
    "fortigate-ips", "FortiGate IPS",
    "Actividad de prevencion de intrusiones: severidad, firmas mas frecuentes, atacantes y ataques no bloqueados.",
    [("fg-ips-notblocked", 0, 0, 12, 8),
     ("fg-ips-timeline", 12, 0, 36, 15),
     ("fg-ips-severity", 0, 8, 16, 15),
     ("fg-ips-top-attack", 16, 8, 32, 15),
     ("fg-ips-top-srcip", 0, 23, 48, 15)]
)
write_ndjson("dashboards/FortiGate IPS.ndjson",
             [index_pattern_obj(), ips_timeline, ips_pie_severity, ips_table_attack, ips_table_srcip, ips_metric_notblocked, ips_dashboard])

# ---------------------------------------------------------------------------
# 5. FortiGate Administration
# ---------------------------------------------------------------------------
adm_kuery = "rule.groups:(fortigate_admin or fortigate_system or fortigate_ha)"
adm_timeline = date_histogram_vis("fg-adm-timeline", "Administracion - Eventos en el tiempo", adm_kuery)
adm_table_users = table_vis("fg-adm-top-users", "Top usuarios administrativos", "data.user", 10, "rule.groups:fortigate_admin")
adm_pie_status = pie_vis("fg-adm-status", "Logins admin por estado", "data.status", 5, "rule.groups:fortigate_admin")
adm_table_ha = table_vis("fg-adm-ha-events", "Eventos HA recientes", "rule.description", 10, "rule.groups:fortigate_ha")
adm_metric_unauthorized = metric_vis("fg-adm-unauthorized", "Cuentas admin no autorizadas", "rule.groups:fortigate_admin_unauthorized_account")
adm_dashboard = dashboard_obj(
    "fortigate-administration", "FortiGate Administration",
    "Actividad administrativa y de sistema: logins, cambios de configuracion, eventos HA y cuentas no autorizadas.",
    [("fg-adm-unauthorized", 0, 0, 12, 8),
     ("fg-adm-timeline", 12, 0, 36, 15),
     ("fg-adm-top-users", 0, 8, 24, 15),
     ("fg-adm-status", 24, 8, 24, 15),
     ("fg-adm-ha-events", 0, 23, 48, 15)]
)
write_ndjson("dashboards/FortiGate Administration.ndjson",
             [index_pattern_obj(), adm_timeline, adm_table_users, adm_pie_status, adm_table_ha, adm_metric_unauthorized, adm_dashboard])

print("Dashboards generados correctamente")
