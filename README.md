# Network Engineering Portfolio

Hands-on network engineering portfolio focused on production-style enterprise, service-provider, security, WAN, data-centre, hybrid-cloud, automation, and managed-services operations.

The portfolio is structured around engineering validation rather than isolated command exercises. Each module follows a repeatable operational workflow:

**Design → Implement → Verify → Fault Inject → Troubleshoot → Recover → Document**

The overall goal is job readiness for Network Engineer, Senior Network Engineer, Network Security Engineer, and MSP / Managed Services roles, with particular relevance to New Zealand enterprise and service-provider environments.

## Current Portfolio

| Domain | Module | Status | Highlights |
|---|---|---|---|
| Routing | [Multi-Area OSPF Engineering Lab](routing/ospf/) | Completed | Multi-area OSPF, ABR/ASBR, Totally NSSA, Type 7→5 translation, E1/E2 redistribution, summarization, authentication, passive interfaces, fault injection and recovery |
| Routing | [Cisco BGP Job-Ready Lab](routing/bgp/) | Completed | eBGP/iBGP, route reflection, best-path selection, prefix filtering, route-maps, communities, maximum-prefix, aggregation, dual-upstream traffic engineering, route-leak protection, RTBH, RIB/CEF troubleshooting and failure recovery |
| Switching | [Enterprise Switching Job-Ready Lab](switching/enterprise-switching/) | Completed | VLANs, 802.1Q trunks, STP root placement, Root Guard, LACP EtherChannel, SVIs, HSRP, DHCP relay, DHCP Snooping, management services, fault injection and RCA |
| Security | [Fortinet Enterprise Firewall Job-Ready Lab](firewall/fortinet/) | Completed | Firewall policy, NAT/VIP, security profiles, route-based IKEv2 IPsec, SD-WAN, session/debug-flow troubleshooting, HA design, FortiManager/FortiAnalyzer operations, change and rollback |
| WAN / Service Provider | [Managed WAN & MPLS Services](wan/managed-wan-mpls/) | Completed | MPLS transport, L3VPN, VRF/RD/RT, MP-BGP VPNv4, PE-CE routing, DIA, BGP transit, BFD, DMVPN Phase 3, Fortinet ADVPN/SD-WAN architecture, incident/RCA workflows |
| Enterprise Access | [Enterprise Wireless & NAC](enterprise-wireless-nac/) | Completed | 802.1X, PEAP, EAP-TLS, RADIUS, NAC authorization, MAB, CoA/Disconnect, guest segmentation, Cisco ISE / Catalyst 9800 operational mapping, troubleshooting |
| Data Centre | [VXLAN EVPN / Nexus Operations & Failure Engineering](data-centre/module-07-data-centre-networking/) | Completed | Spine-leaf underlay, BGP EVPN, VXLAN, L2VNI/L3VNI, symmetric IRB, Type-2/3/5 routes, Border Leaf, DCI concepts, MTU/RT failure engineering and NX-OS mapping |
| Cloud / Hybrid | [M08 - Cloud & Hybrid Networking](cloud-hybrid-networking/) | Completed | Azure hub-spoke, S2S IPsec, BGP, gateway transit, NSG/UDR, Private Endpoint/DNS concepts, AWS VPN/TGW/Direct Connect architecture, hybrid troubleshooting |
| Automation | [M09 - Automation & Source of Truth](automation/m09-network-automation/) | Completed | Git-based change control, YAML intent, Python validation, Jinja2, Ansible resource modules, Vault, NetBox dynamic inventory, REST API, pre/post-check, rollback and GitHub Actions CI |
| Operations | [M11 - Managed Services & Observability](operations/m11-managed-services-observability/) | Completed | SNMP, Syslog, NetFlow/IPFIX, NMS, alert triage, service baselines, SLA/SLO thinking, configuration backup, capacity, incident, escalation and RCA workflows |
| Multi-Vendor | M10 - Multi-Vendor Operations & Migration | Current | Junos operational migration from Cisco, PAN-OS operational model, Check Point management/policy workflow, F5 BIG-IP fundamentals, Arista EOS mapping, cross-vendor troubleshooting and migration |
| Capstone | M12 - Integrated Managed Services Capstone | Planned | Service acceptance, production change, multi-vendor major incident, vendor/carrier escalation, RCA/PIR, automation/observability integration and final handover |

## Engineering Approach

The labs are designed to reflect production operations and managed-service workflows, including:

- topology and protocol design
- explicit implementation and change steps
- control-plane and data-plane verification
- deliberate failure injection
- structured troubleshooting from physical/interface state through routing, policy, sessions, tunnels and application reachability
- rollback and recovery validation
- incident-style documentation and root-cause analysis
- vendor-specific behaviour recorded separately from protocol fundamentals
- automation, source-of-truth integration, review gates and auditability where appropriate
- clear separation between hands-on validation, configuration/protocol labs, and design/operations knowledge where licensing or platform limitations prevent faithful emulation

## Platforms and Technologies

The portfolio currently includes hands-on or production-mapped work across:

- Cisco IOS / IOS-XE and NX-OS concepts
- FRRouting / Linux networking
- Fortinet FortiGate / FortiManager / FortiAnalyzer concepts
- Azure and AWS hybrid networking
- NetBox
- Ansible
- Python
- Jinja2
- Git / GitHub Actions
- FreeRADIUS / hostapd / Linux 802.1X components

The remaining roadmap adds Juniper Junos, Palo Alto PAN-OS, Check Point, F5 BIG-IP fundamentals, and concise Arista EOS operational mapping where they add practical multi-vendor value.

## Featured Projects

### M11 - Managed Services & Observability

A production-style observability module combining LibreNMS, SNMPv3 polling/traps, Syslog, NTP, NetFlow v9, alert lifecycle, noise reduction, SLA measurement caveats and an end-to-end managed-services incident/RCA.

→ [Open the M11 observability lab](operations/m11-managed-services-observability/)

### M09 - Automation & Source of Truth

A production-oriented automation workflow for a controlled BGP prefix advertisement change using NetBox dynamic inventory, Ansible Vault, Cisco resource modules, validation, pre-check/backup/change/post-check/rollback and GitHub Actions CI.

→ [Open the M09 automation lab](automation/m09-network-automation/)

### Fortinet Enterprise Firewall Job-Ready Lab

A production-style enterprise edge firewall lab covering policy, NAT/VIP, route-based IPsec, SD-WAN, session/debug-flow evidence, HA operating model, central management/logging concepts, change control and incident troubleshooting.

→ [Open the Fortinet firewall lab](firewall/fortinet/)

### Managed WAN & MPLS Services

A WAN-focused engineering module covering MPLS transport/L3VPN, DIA and BGP transit, BFD, DMVPN, SD-WAN/ADVPN architecture, service demarcation, managed-services troubleshooting, carrier escalation and RCA.

→ [Open the managed WAN/MPLS lab](wan/managed-wan-mpls/)

### Data Centre VXLAN EVPN

A spine-leaf EVPN/VXLAN project using FRR/Linux for the validated control/data plane and mapping the operational model to Cisco Nexus / NX-OS.

→ [Open the data-centre lab](data-centre/module-07-data-centre-networking/)

### Cloud & Hybrid Networking

Hybrid networking work covering Azure hands-on VPN/BGP connectivity and AWS architecture/troubleshooting mapping, with emphasis on routing, security policy, return path and on-prem/cloud fault isolation.

→ [Open the cloud/hybrid module](cloud-hybrid-networking/)

## Remaining Roadmap

The remaining modules are intentionally focused on operational gaps rather than repeating protocol theory already demonstrated elsewhere in this repository.

### M11 — Managed Services & Observability ✅

Completed production-style observability work covering:

- SNMP polling and traps
- Syslog and event correlation
- NetFlow / IPFIX
- NMS design and alert triage
- service baselines and capacity
- SLA / SLO thinking
- configuration backup and operational hygiene
- incident, escalation and RCA workflow

### M10 — Multi-Vendor Operations & Migration (Current)

Convert existing Cisco/Fortinet knowledge into practical cross-vendor operational competency:

- Juniper Junos configuration model, routing policy, verification and rollback
- Palo Alto PAN-OS zones, security/NAT policy, sessions, VPN and candidate/commit workflow
- Check Point Gaia / Management Server / objects / policy package / publish / install-policy model
- F5 BIG-IP LTM operational fundamentals
- concise Arista EOS operational mapping
- cross-vendor API differences
- evidence-driven troubleshooting
- FortiGate → Palo Alto migration workflow

### M12 — Integrated Managed Services Capstone

Reuse the operational environment built in M09–M11 and the multi-vendor skills from M10 in a realistic customer lifecycle:

- service acceptance and baseline
- planned production change
- multi-vendor major incident
- vendor/carrier escalation
- business validation and rollback decision
- RCA / PIR
- monitoring and automation improvement
- final operational handover

M12 introduces no new protocol syllabus; it is the integration and assessment stage.

## Repository Structure

```text
network-engineering-portfolio/
├── README.md
├── routing/
│   ├── ospf/
│   └── bgp/
├── switching/
│   └── enterprise-switching/
├── firewall/
│   └── fortinet/
├── wan/
│   └── managed-wan-mpls/
├── enterprise-wireless-nac/
├── data-centre/
│   └── module-07-data-centre-networking/
├── cloud-hybrid-networking/
├── automation/
│   └── m09-network-automation/
└── operations/
    └── m11-managed-services-observability/
```

M11 is complete. M10 is now the active module, followed by the M12 integrated capstone.

## Security Note

All credentials, authentication keys, API tokens, pre-shared keys, and environment-specific secrets are excluded or redacted before publication. Example addressing and lab-only routes are used for portfolio documentation.
