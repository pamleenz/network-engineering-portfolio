# Network Engineering Portfolio

Hands-on network engineering portfolio focused on routing, switching, network security, WAN, MPLS, automation, and multi-vendor troubleshooting.

The portfolio is structured around engineering validation rather than isolated command exercises. Each module is developed using a repeatable operational workflow:

**Design → Implement → Verify → Fault Inject → Troubleshoot → Recover → Document**

## Current Portfolio

| Domain | Module | Status | Highlights |
|---|---|---|---|
| Routing | [Multi-Area OSPF Engineering Lab](routing/ospf/) | Completed | Multi-area OSPF, ABR/ASBR, Totally NSSA, Type 7→5 translation, E1/E2 redistribution, summarization, authentication, passive interfaces, fault injection and recovery |
| Routing | BGP | Planned | eBGP/iBGP, route policy, path selection, communities, filtering, failure handling |
| Switching | Enterprise Switching | Planned | VLANs, trunks, STP, LACP, SVIs, redundancy, campus troubleshooting |
| Security | Fortinet / Firewall | Planned | Policies, NAT, VPN, HA, SD-WAN, logging and session troubleshooting |
| WAN / VPN | Enterprise WAN | Planned | IPsec, GRE, DMVPN, dual-ISP and WAN failover scenarios |
| Service Provider | MPLS / L3VPN | Planned | LDP, MP-BGP VPNv4, VRF, RD/RT and PE-CE routing |
| Operations | Monitoring & Troubleshooting | Planned | Alert triage, monitoring, change verification, rollback and RCA workflows |
| Automation | Network Automation | Planned | Python, Ansible, Jinja2, Git and configuration validation |

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

## Platforms and Technologies

The portfolio will progressively cover Cisco, Fortinet, Palo Alto, Juniper, Huawei, Meraki and open networking platforms where appropriate. Current OSPF validation was performed with **GNS3 and FRR 10.3**, with Cisco IOS/IOS-XE validation planned for vendor-specific behaviors where it adds value.

## Featured Project

### Multi-Area OSPF Engineering Lab

The first completed module validates a five-router design with a redundant Area 0 core, a Totally NSSA edge area, ABR/ASBR behavior, external redistribution, inter-area and external summarization, MD5 authentication, passive-interface advertisement, and deliberate control-plane failure scenarios.

→ [Open the OSPF lab](routing/ospf/)

## Repository Structure

```text
network-engineering-portfolio/
├── README.md
└── routing/
    └── ospf/
        ├── README.md
        ├── topology/
        ├── configs/
        └── docs/
```

Additional modules will be added to the same repository as they are completed.

## Security Note

All credentials, authentication keys, and environment-specific secrets are redacted before publication. Example addressing and lab-only routes are used for portfolio documentation.
