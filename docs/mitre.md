# Mapeo MITRE ATT&CK

Técnicas cubiertas por el ruleset `fortigate-wazuh`, agrupadas por táctica.
Cada técnica indica en qué archivo(s) de reglas se usa.

## Reconnaissance

| Técnica | Nombre | Reglas |
|---|---|---|
| T1595 | Active Scanning | 1005 (100503, 109901), 1007 (100707) |
| T1595.002 | Active Scanning: Vulnerability Scanning | 1007 (100707) |

## Initial Access

| Técnica | Nombre | Reglas |
|---|---|---|
| T1190 | Exploit Public-Facing Application | 1005, 1007, 1099 |
| T1133 | External Remote Services | 1006 (109902 correlación), 1099 |
| T1566 | Phishing | 1009 (100903), 1099 (109907) |
| T1566.002 | Phishing: Spearphishing Link | 1009 (100902) |

## Execution

| Técnica | Nombre | Reglas |
|---|---|---|
| T1059 | Command and Scripting Interpreter | 1007 (100709) |
| T1204 | User Execution | 1008 (100801-100804), 1099 (109907) |

## Persistence / Defense Evasion

| Técnica | Nombre | Reglas |
|---|---|---|
| T1078 | Valid Accounts | 1006, 1012 (101204), 1099 (109902, 109904) |
| T1090 | Proxy | 1009 (100904), 1011 (100101, 101102) |
| T1562 | Impair Defenses | 1012 (101206), 1099 (109904) |
| T1219 | Remote Access Software | 1011 (101102) |
| T1568.002 | Dynamic Resolution: Domain Generation Algorithms | 1010 (101002), 1099 (109903) |

## Credential Access

| Técnica | Nombre | Reglas |
|---|---|---|
| T1110 | Brute Force | 1006, 1007 (100710), 1012, 1099 (109906) |
| T1110.001 | Brute Force: Password Guessing | 1006 (100602), 1012 (101203) |
| T1110.003 | Brute Force: Password Spraying | 1006 (100603) |
| T1111 | Multi-Factor Authentication Interception | 1006 (100610) |

## Discovery / Lateral Movement

| Técnica | Nombre | Reglas |
|---|---|---|
| T1046 | Network Service Discovery | 1005 (100502, 100503, 109901) |
| T1021 | Remote Services | 1005 (100508) |

## Command and Control

| Técnica | Nombre | Reglas |
|---|---|---|
| T1071 | Application Layer Protocol | 1005 (100504), 1007 (100711), 1009 (100902) |
| T1071.004 | Application Layer Protocol: DNS | 1010, 1099 (109903) |
| T1571 | Non-Standard Port | 1005 (100507) |
| T1105 | Ingress Tool Transfer | 1007 (100711), 1008 (100801, 100805), 1099 (109907) |

## Exfiltration

| Técnica | Nombre | Reglas |
|---|---|---|
| T1041 | Exfiltration Over C2 Channel | 1005 (100506) |
| T1048 | Exfiltration Over Alternative Protocol | 1010 (101003) |
| T1567.002 | Exfiltration Over Web Service: Cloud Storage | 1011 (101103) |

## Impact

| Técnica | Nombre | Reglas |
|---|---|---|
| T1485 | Data Destruction | 1013 (101305) |
| T1486 | Data Encrypted for Impact (ransomware) | 1008 (100803, 100802), 1099 (109903) |
| T1498 | Network Denial of Service | 1015, 1099 (109905) |
| T1498.001 | Direct Network Flood | 1015 (101502, 101503, 101504) |
| T1499 | Endpoint Denial of Service | 1005 (100510... no aplica), 1013 (101304), 1014, 1099 (109905) |
| T1601 | Modify System Image | 1013 (101302) |
| T1529 | System Shutdown/Reboot | 1013 (101301) |

---

**Nota**: este mapeo es orientativo y facilita la priorización de alertas
por táctica en el dashboard "FortiGate Threats". No sustituye un análisis
de detección formal frente al framework completo de MITRE ATT&CK for
Enterprise.
