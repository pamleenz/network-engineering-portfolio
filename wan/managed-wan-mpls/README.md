# Module 06 — Managed WAN & MPLS Services

## Portfolio Positioning

This module focuses on production-style WAN service delivery, routing policy, resiliency, troubleshooting, and managed-services operations rather than certification-style command coverage.

## What I validated hands-on

- MPLS transport using OSPF + LDP, including LFIB verification and an MPLS-only forwarding failure while IP reachability remained healthy.
- MPLS L3VPN using VRFs, RD/RT, MP-BGP VPNv4, PE-CE eBGP, and customer route exchange.
- Four L3VPN fault domains: RT import, VPNv4 address-family, MPLS data plane, and CE route origination.
- Static-routed DIA coexisting with MPLS private WAN service.
- 100 Mbps service-demarc policing configuration and policy verification (not ASIC line-rate benchmarking).
- BGP IP Transit with customer egress filtering, provider ingress prefix/AS-path validation, max-prefix protection, and route-leak testing.
- BFD-triggered BGP fast failure detection using a synthetic blackhole while interfaces remained up/up.
- Cisco DMVPN Phase 3 with mGRE/NHRP/EIGRP, direct spoke-to-spoke shortcut, IKEv2/IPsec protection, and PSK-failure troubleshooting.

## Fortinet ADVPN 2.0 scope

I reviewed and configured the relevant FortiOS 7.6.7 feature set on a valid single FortiGate VM and mapped the production architecture:

- IPsec parent overlays
- ADVPN sender/receiver roles
- SD-WAN overlay zone
- transport groups
- Performance SLA
- BGP-on-loopback / Dynamic BGP design
- edge discovery, path management, and health updates

A full three-node ADVPN 2.0 shortcut was **not** functionally validated because additional FortiGate VMs were unlicensed. I therefore classify the multi-node ADVPN work as **CONFIG REVIEW + DESIGN/OPS KNOWLEDGE**, not a completed production-equivalent lab.

## Core troubleshooting model

`Impact & Scope → Physical/Interface → VLAN/L2 → Routing → Authentication/Policy → WAN/Carrier → Security → Logs/Monitoring → Root Cause`

The recurring lesson across MPLS, BGP, BFD, DMVPN, and SD-WAN is that a healthy interface or protocol adjacency does not by itself prove service health. Verification must include routing policy, forwarding state, labels/tunnels, return path, SLA telemetry, and application impact.

## Managed-services outcomes

- Evidence-driven carrier escalation
- Change / Verification / Rollback discipline
- Route-leak prevention and independent trust boundaries
- Separation of control-plane, data-plane, security-overlay, and service-quality failures
- Hybrid WAN modernization: MPLS, DIA, Internet, 5G, encrypted overlays, and SD-WAN can coexist during staged migration

## Lab classifications

| Area | Classification |
|---|---|
| MPLS Transport / L3VPN | REAL / PROTOCOL LAB |
| L3VPN Fault Domains | REAL TROUBLESHOOTING LAB |
| DIA / BGP Transit | REAL CONFIG LAB |
| BFD | PROTOCOL LAB |
| Cisco DMVPN Phase 3 + IKEv2/IPsec | CONFIG / PROTOCOL LAB |
| Fortinet ADVPN 2.0 multi-node behavior | CONFIG REVIEW + DESIGN/OPS |
| Hybrid WAN / Managed Services Incident | DESIGN/OPS SCENARIO |
