# M10 — Multi-Vendor Network Operations & Migration

**Status:** Curriculum / design exercises completed; mixed hands-on and design-based evidence.  
**Scope:** Check Point R82, Juniper Junos, Palo Alto PAN-OS, F5 BIG-IP LTM, Arista EOS, cross-vendor operations.  
**Date:** October 2026.

## Evidence classification

| Platform | Coverage | Evidence |
|---|---|---|
| Check Point R82 Standalone | Gaia networking, SmartConsole/Management, topology sync, Publish/Install, anti-spoofing, policies, SNAT, logs | **Hands-on** in VMware + Cisco CML/IOL lab |
| Juniper Junos | RE/PFE, candidate/commit/rollback, WAN Edge, BGP route policies | **Design-based; no Junos VM validation** |
| Palo Alto PAN-OS | Zones, Virtual/Logical Router, App-ID, NAT, DMZ/DNAT, sessions, migration | **Design-based; no PAN-OS VM validation** |
| F5 BIG-IP LTM | Virtual Server, Pool/Member, health monitor, SNAT, TLS, HA | **Design-based; no BIG-IP VM validation** |
| Arista EOS | SysDB, switching, MLAG, EVPN/VXLAN, configuration sessions, eAPI | **Design-based; no EOS VM validation** |
| Cross-vendor | Operational runbooks, change, evidence-led troubleshooting, API/commit differences | **Design review** |

## Verified Check Point lab

```text
ISP-R1 (Cisco IOL) 10.100.0.1/30
            |
Check Point R82 eth1 10.100.0.2/30
Check Point R82 eth2 10.101.0.2/30
            |
HQ-CORE (Cisco IOL) 10.101.0.1/30
HQ-USERS simulated as 10.10.10.1/24 Loopback
```

Management: Check Point eth0 `10.99.0.50/24`, Windows `10.99.0.1`, M11 NMS `10.99.0.20` over LAB-MGMT/VMnet2.

**Historical observed evidence:** NAT log proved `10.10.10.1 → 10.100.0.2` while ISP-R1 lacked a return route for `10.10.10.0/24`. Some ICMP successes depended on temporary diagnostic rules subsequently removed; do **not** present these as a passing final-policy application test. Gateway object interface resynchronisation and management lockout recovery were also directly experienced.

## Documentation

- [Multi-vendor technical study guide](M10_Multi_Vendor_Network_Operations_Study_Guide.md)
- [M12 integrated MSP capstone](../../operations/m12-integrated-ms-capstone/)

## Production lessons

1. Vendor configuration success is not customer application acceptance.
2. Check Point: Gaia network, Management policy database, Publish, and Gateway Install are distinct.
3. Junos: Candidate Configuration requires Commit, with version-specific rollback behaviour.
4. PAN-OS: NAT and Security rules are separate; DNAT Security Policy uses pre-NAT destination IP and post-NAT destination zone.
5. F5: Pool health cannot prove full user transaction success; one-arm return paths need explicit design.
6. EOS: default running configuration changes differ from optional configuration sessions; protect against concurrent edits.
7. Record *As-Built*, *Reference/Design*, and *Not Validated* separately.

**Publishing safeguards:** This is a learning portfolio, not vendor-certified implementation guidance. Do not expose real production addressing, customer information, credentials, secrets, or original unredacted backups.
