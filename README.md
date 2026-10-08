# Network Engineering Portfolio

Hands-on network engineering portfolio focused on routing, switching, network security, WAN, MPLS, automation, cloud/hybrid networking, and multi-vendor troubleshooting.

The portfolio is structured around engineering validation rather than isolated command exercises. Each module is developed using a repeatable operational workflow:

**Design → Implement → Verify → Fault Inject → Troubleshoot → Recover → Document**

## Current Portfolio

| Domain | Module | Status | Highlights |
|---|---|---|---|
| Routing | [Multi-Area OSPF Engineering Lab](routing/ospf/) | Completed | Multi-area OSPF, ABR/ASBR, Totally NSSA, Type 7→5 translation, E1/E2 redistribution, summarization, authentication, passive interfaces, fault injection and recovery |
| Routing | [Cisco BGP Job-Ready Lab](routing/bgp/) | Completed | eBGP/iBGP, route reflection, best-path selection, prefix filtering, route-maps, communities, maximum-prefix, aggregation, dual-upstream traffic engineering, route-leak protection, RTBH, RIB/CEF troubleshooting and failure recovery |
| Switching | [Enterprise Switching Job-Ready Lab](switching/enterprise-switching/) | Completed | VLANs, 802.1Q trunks, STP root placement, Root Guard, LACP EtherChannel, SVIs, inter-VLAN routing, DHCP relay, management services, fault injection and recovery |
| Automation | [M09 - Automation & Source of Truth](automation/m09-network-automation/) | Completed | Git-based change control, YAML change intent, Python validation, Jinja2, Ansible resource modules, Vault, NetBox dynamic inventory, REST API, pre/post-check, rollback and GitHub Actions CI |
| Security | Fortinet / Firewall | Planned | Policies, NAT, VPN, HA, SD-WAN, logging and session troubleshooting |
| WAN / VPN | Enterprise WAN | Planned | IPsec, GRE, DMVPN, dual-ISP and WAN failover scenarios |
| Service Provider | MPLS / L3VPN | Planned | LDP, MP-BGP VPNv4, VRF, RD/RT and PE-CE routing |
| Operations | Managed Services & Observability | Planned | SNMP, Syslog, NetFlow/IPFIX, NMS, alert triage, SLA, configuration backup, capacity, incident, escalation and RCA workflows |

## Engineering Approach

The labs are designed to reflect production operations and managed-service workflows, including:

- topology and protocol design
- explicit implementation and change steps
- control-plane and data-plane verification
- deliberate failure injection
- structured troubleshooting from interface state through protocol tables and the RIB/FIB
- rollback and recovery validation
- incident-style documentation and root-cause analysis
- vendor-specific behavior recorded separately from protocol fundamentals
- automation, source-of-truth integration, review gates and auditability where appropriate

## Platforms and Technologies

The portfolio progressively covers Cisco, Fortinet, Palo Alto, Juniper, Huawei, Meraki, FRR/Linux and cloud networking platforms where they add practical value.

## Featured Projects

### M09 - Automation & Source of Truth

A production-oriented automation workflow for a controlled BGP prefix advertisement change using NetBox dynamic inventory, Ansible Vault, Cisco resource modules, validation, pre-check/backup/change/post-check/rollback and GitHub Actions CI.

→ [Open the M09 automation lab](automation/m09-network-automation/)

### Multi-Area OSPF Engineering Lab

A five-router design with a redundant Area 0 core, a Totally NSSA edge area, ABR/ASBR behavior, external redistribution, inter-area and external summarization, authentication, passive-interface advertisement, and deliberate control-plane failure scenarios.

→ [Open the OSPF lab](routing/ospf/)

## Repository Structure

```text
network-engineering-portfolio/
├── README.md
├── routing/
├── switching/
├── firewall/
├── wan/
├── data-centre/
├── cloud-hybrid-networking/
└── automation/
    └── m09-network-automation/
```

Additional modules will be added to the same repository as they are completed.

## Security Note

All credentials, authentication keys, API tokens, and environment-specific secrets are excluded or redacted before publication. Example addressing and lab-only routes are used for portfolio documentation.
