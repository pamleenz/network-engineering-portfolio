# Network Engineering Portfolio

Production-style network engineering portfolio covering enterprise LAN/WAN, service-provider routing, security, data-centre networking, hybrid cloud, automation, monitoring and MSP service operations.

The approach across modules is **Design → Implement (where platforms are available) → Verify → Fault Inject → Troubleshoot → Recover → Document**. The work is intended to support Network Engineer / Senior Network Engineer / Network Security Engineer / Managed Services role preparation, particularly in New Zealand.

> **Evidence policy:** “Completed” describes the learning module, **not** universal hardware validation or production certification. Each module distinguishes hands-on test evidence, reference configurations, vendor/platform limitations, and design-only scenarios. M10’s non-Check-Point vendors and M12’s fictional multi-vendor production incident have **not** been deployed and verified as one live network.

## Portfolio Index

| Area | Module | Learning status | Evidence / special scope |
|---|---|---|---|
| Routing | [M01 — Multi-Area OSPF](routing/ospf/) | Completed | GNS3 / FRR 10.3 hands-on; BFD and some platform behaviours explicitly limited |
| Routing | [M02 — Cisco BGP](routing/bgp/) | Completed | Multi-AS Cisco routing, route policies, communities, failover, RTBH and fault analysis |
| Switching | [M03 — Enterprise Switching](switching/enterprise-switching/) | Completed | CML / Cisco IOL L2; VLAN, STP, LACP, HSRP, DHCP relay/snooping and fault analysis |
| Security | [M04 — Fortinet Enterprise Firewall](firewall/fortinet/) | Completed | FortiGate-VM hands-on for policy/NAT/IPsec/SD-WAN; HA and central management design; eval limitations documented |
| Managed WAN | [M05/M06 — Managed WAN & MPLS Services](wan/managed-wan-mpls/) | Completed | MPLS L3VPN / PE-CE, transit, BFD, Cisco DMVPN; Fortinet ADVPN limitations marked |
| Enterprise Access | [Enterprise Wireless & NAC](enterprise-wireless-nac/) | Completed | FreeRADIUS / hostapd / 802.1X, PEAP, EAP-TLS, CoA/MAB; Cisco ISE/C9800 conceptual mapping |
| Data Centre | [M07 — VXLAN EVPN & Nexus Operations](data-centre/module-07-data-centre-networking/) | Completed | FRR/Linux VXLAN/EVPN tested; NX-OS configuration is reference mapping, not N9Kv validation |
| Cloud / Hybrid | [M08 — Cloud & Hybrid Networking](cloud-hybrid-networking/) | Completed | Azure hybrid connectivity hands-on; AWS architecture and troubleshooting design |
| Automation | [M09 — Automation & Source of Truth](automation/m09-network-automation/) | Completed | Ansible, NetBox, BGP change workflow, GitHub Actions; CI validates syntax and intent, not live network deployment |
| Multi-Vendor | [M10 — Multi-Vendor Operations & Migration](multi-vendor/m10-multi-vendor-operations/) | **Curriculum completed** | Check Point R82 hands-on; Junos, PAN-OS, F5 LTM, Arista EOS **design-based only** |
| Observability | [M11 — Managed Services & Observability](operations/m11-managed-services-observability/) | Completed | LibreNMS, SNMPv3, traps, Syslog, NTP, NetFlow, alert triage, RCA; module-level lab evidence |
| Capstone | [M12 — Integrated Enterprise / MSP Capstone](operations/m12-integrated-ms-capstone/) | **Six design stages completed; final individual assessment pending** | Service handover, HLD, change/MOP, simulated incident, RCA/PIR/CAPA; customer is fictional, **no production acceptance** |

The WAN numbering groups connected provider/WAN work, while Enterprise Wireless/NAC remains an additional standalone study area. The portfolio index reflects actual repository directories rather than implying every section shares a uniform numeric module label.

## Featured Projects

### M12 — Integrated MSP Service Handover

A six-stage fictional managed-services customer lifecycle: transition and network baseline, multi-vendor architecture review, Check Point → Palo Alto migration **plan**, major incident **simulation**, evidence-based RCA/PIR, and operational handover. Includes runbooks and explicit acceptance blockers. No fictional P1 outage is claimed as a real incident.

→ [M12 capstone and service handover](operations/m12-integrated-ms-capstone/)

### M10 — Multi-Vendor Operations

Hands-on Check Point R82 Standalone: Gaia/SmartConsole object and policy model, Publish/Install, gateway topology synchronisation, management recovery, NAT/traffic log evidence with Cisco IOL. Design-only Junos WAN, PAN-OS zone/NAT/DMZ, F5 LTM, Arista EOS/MLAG/EVPN and cross-vendor automation/rollback comparison.

→ [M10 technical guide](multi-vendor/m10-multi-vendor-operations/)

### M11 — Managed Services & Observability

LibreNMS deployment with Cisco telemetry: SNMPv3, traps, Syslog, NTP, NetFlow, monitoring/alert triage, baseline and RCA.

→ [M11 monitoring lab](operations/m11-managed-services-observability/)

### M09 — Network Automation

Git-based BGP prefix change automation with source-of-truth data, validation, Cisco resource modules, Ansible Vault, backup/pre/post checks and GitHub Actions syntax/intent verification. CI has **no access to production devices**, so passing it does not prove device configuration or live service success.

→ [M09 automation lab](automation/m09-network-automation/)

### Firewall, WAN and Data Centre

- [Fortinet Firewall — NAT, VPN, SD-WAN and troubleshooting](firewall/fortinet/)
- [Managed WAN/MPLS — L3VPN, DIA/BGP, DMVPN, BFD](wan/managed-wan-mpls/)
- [Data Centre EVPN/VXLAN — FRR/Linux lab and Nexus mapping](data-centre/module-07-data-centre-networking/)
- [Cloud/Hybrid — Azure hands-on and AWS reference](cloud-hybrid-networking/)

## Engineering Practices

The projects prioritize failure-domain isolation, RIB-versus-FIB validation, security/NAT sessions, application and return-path testing, service-level impact, safe management/OOB access, configuration backup, change review, rollback, monitoring, carrier escalation, and evidence-led RCA/PIR. Where constrained by platform or license, scenarios are explicitly labelled **DESIGN / REFERENCE / SIMULATED** instead of portraying hypothetical output as captured evidence.

## Technology Inventory

- **Hands-on in specific modules:** Cisco IOL / IOS(-XE), GNS3 FRRouting/Linux, FortiGate-VM under evaluation constraints, Check Point R82 Standalone, FreeRADIUS/hostapd, Azure hybrid infrastructure, LibreNMS, Python/Ansible/NetBox-related workflows.
- **Vendor mapping / design, not live vendor labs in M10:** Juniper Junos, Palo Alto PAN-OS, F5 BIG-IP LTM, Arista EOS. Cisco Nexus/NX-OS sections in M07 are reference material.
- **Tooling:** Git/GitHub Actions, YAML/Jinja2, Ansible resource modules and Vault, source-of-truth and monitoring workflows.

## Repository Structure

```text
network-engineering-portfolio/
├── README.md
├── .github/workflows/
├── routing/{ospf,bgp}/
├── switching/enterprise-switching/
├── firewall/fortinet/
├── wan/managed-wan-mpls/
├── enterprise-wireless-nac/
├── data-centre/module-07-data-centre-networking/
├── cloud-hybrid-networking/
├── automation/m09-network-automation/
├── multi-vendor/m10-multi-vendor-operations/
└── operations/
    ├── m11-managed-services-observability/
    └── m12-integrated-ms-capstone/
```

## Portfolio Audit

[2026-10-15 repository content and evidence audit](PORTFOLIO_AUDIT_2026-10-15.md) documents verified directory coverage, known platform limitations, CI versus live-device boundaries, and prioritized follow-up checks. This review is not a line-by-line verification of all device configurations.

## Current Completion and Validation

- **M01–M11:** Learning exercises documented, with platform-specific evidence and exclusions in each module.
- **M10:** Completed as mixed-evidence learning; only Check Point R82 in that module has actual vendor VM evidence.
- **M12:** All six design/ops stages documented; the independent scenario answer and grading are still pending.
- **Production readiness:** No actual multi-vendor ABS production network was deployed or signed off. The fictional customer's service acceptance stays **pending**.

## Security and Reuse

This is a public **educational portfolio**. Secrets, credentials, authentication keys, API tokens, private keys, customer data and live configuration backups must not be committed. Some sample material includes legacy protocols or deliberately weakened **lab-only** crypto due to evaluation image constraints; such examples are **not production hardening advice**. Public address examples use RFC documentation ranges; private IPs are lab addressing. Validate commands and vendor functionality against the actual product version before reuse.
