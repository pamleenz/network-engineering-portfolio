# Architecture and Operations Notes

## 1. HA - Active/Passive FGCP

A production HA design adds appliance redundancy in addition to WAN redundancy.

Core concepts:

```text
Heartbeat
Primary election
Monitored interfaces
Configuration synchronization
Session synchronization
Failover / failback behavior
```

Representative configuration model (not executed in this constrained three-interface lab):

```text
config system ha
    set mode a-p
    set group-name "HQ-FW-CLUSTER"
    set group-id 10
    set password <SECRET>
    set hbdev "port3" 50 "port4" 50
    set priority 200
    set override disable
    set monitor "port1" "port2"
    set session-pickup enable
    set session-pickup-connectionless enable
end
```

Useful operational commands:

```text
get system ha status
diagnose system ha status
diagnose sys ha history read
diagnose sys ha checksum cluster
execute ha manage <index> <username>
```

Design lesson: two firewalls do not automatically make the entire network highly available. Upstream/downstream switches, WAN circuits, heartbeat paths and application dependencies can still be single points of failure.

## 2. FortiManager

FortiManager is the centralized configuration and policy-management plane.

Operational model:

```text
Change ticket
 -> Modify FortiManager database
 -> Review policy/device diff
 -> Install Preview
 -> Approval
 -> Install to FortiGate(s)
 -> Verify
 -> Reconcile drift / rollback if required
```

Important concepts:

- ADOM: logical administrative boundary.
- Device Manager: device-level configuration such as interfaces, routing, VPN and SD-WAN.
- Policy & Objects / Policy Package: centralized firewall/security policy deployment.
- Revision: configuration history and comparison.
- Install Preview: inspect intended changes before pushing them.
- Configuration drift: FortiManager desired state differs from device running state.

Emergency direct CLI changes must be reconciled back into the management platform.

## 3. FortiAnalyzer

FortiAnalyzer is the centralized logging, analytics, event and reporting platform for Fortinet environments.

Three practical log categories:

- **Traffic logs:** source/destination, interfaces, policy, action, NAT, bytes/session behavior.
- **Event logs:** admin/config changes, interface events, HA events, VPN/system events.
- **Security/UTM logs:** IPS, AV, web filter, DNS filter, application control and other security engines.

Typical investigation workflow:

```text
Confirm time/source/destination/symptom
 -> Search Traffic Log
 -> Check action/policy/NAT
 -> If accepted, inspect UTM/security logs
 -> Correlate Event logs for link/HA/config changes
 -> Escalate to live session/sniffer/debug only when needed
```

FortiAnalyzer is not a replacement for a broad multi-vendor SIEM. A SIEM may aggregate Fortinet plus EDR, identity, cloud, server and application telemetry.

## 4. Upgrade / Operations Lifecycle

```text
Change request
 -> Baseline
 -> Backup / rollback preparation
 -> Validate release notes + supported upgrade path
 -> Implement in maintenance window
 -> Technical verification
 -> Business verification
 -> Observation window
 -> Close change OR rollback + RCA
```

Pre/post checks should be comparable. A successful device boot is not sufficient evidence of service recovery.

## 5. High-Level Cross-Vendor Mapping

The mapping below is approximate; products and operating models are not one-to-one equivalents.

| Fortinet | Palo Alto Networks | Cisco Secure Firewall |
|---|---|---|
| Firewall Policy | Security Policy | Access Control Policy (ACP) |
| Address/Service Objects | Address/Service Objects | Network/Port Objects |
| Security Profiles | Security Profiles / Profile Groups | IPS/File/Malware/Security policy components |
| VIP / DNAT | NAT Policy | NAT Rules |
| Route-based IPsec interface | Tunnel Interface + IKE/IPsec objects | Site-to-Site VPN / VTI where supported |
| SD-WAN | PAN-OS SD-WAN / routing policy capabilities | Usually broader Cisco SD-WAN architecture rather than a direct FTD feature equivalent |
| FGCP HA | Active/Passive or Active/Active HA (platform/design dependent) | Secure Firewall HA pair / clustering (platform dependent) |
| FortiManager | Panorama | Secure Firewall Management Center (FMC) |
| FortiAnalyzer | Panorama/logging services for PAN telemetry; broader SIEM often external | FMC event visibility plus external SIEM/log platforms |

The transferable engineering skills are policy design, routing/NAT reasoning, VPN troubleshooting, HA state, centralized change control and evidence-driven operations rather than memorizing identical menu names.
