# M12 — Integrated MSP Capstone | Final Service Handover Pack

**Case:** Auckland Business Services (ABS), fictional NZ managed-services customer.  
**Status:** Stages 1–6 design and operations work completed; individual Senior Engineer final assessment **pending**. Formal customer acceptance **not obtained**.

> This document is a **design/simulation handover**, not a signed As-Built or production implementation record. Actual hands-on work was Cisco IOL + Check Point R82; Juniper, Palo Alto, F5 and Arista activities were design exercises.

## 1. Executive Summary

An MSP takes over a small enterprise network, establishes a baseline, reviews an HA target architecture, prepares a Check Point → Palo Alto migration, coordinates a simulated P1 web outage, prepares a problem RCA/PIR and proposes monitoring/change improvements.

**Service disposition:** PENDING ACCEPTANCE. No real ABS production service exists; no multi-vendor live cutover occurred.

## 2. Evidence Register

| ID | Domain | Actual evidence | Boundary |
|---|---|---|---|
| E01 | WAN / Cisco | Cisco IOL ISP-R1 10.100.0.1/30; HQ-CORE 10.101.0.1/30 | Lab-only private WAN |
| E02 | Firewall / CP | Check Point R82 eth1 10.100.0.2/30; eth2 10.101.0.2/30 | Actual VM |
| E03 | HQ user network | Loopback 10.10.10.1/24 | No actual client workstations |
| E04 | SNAT | Check Point log showed 10.10.10.1 → 10.100.0.2 | Historical observed |
| E05 | ICMP | ISP/HQ tests succeeded with temporary diagnostic rules | Cannot claim a current passing post-cleanup policy test |
| E06 | Management | CP eth0 10.99.0.50, Windows 10.99.0.1, NMS 10.99.0.20 | Lab management network |
| E07 | M11 monitoring | Ubuntu NMS deployment and M11 documentation | Latest end-to-end alert chain needs renewed acceptance |
| D01 | Juniper + ISP HA | Dual-ISP edge and BGP failover design | No Junos device tests |
| D02 | Palo Alto | Zones, NAT, DMZ, HA and firewall migration design | No PAN-OS VM tests |
| D03 | F5 | VS, pool, SNAT, monitors, simulated failure | No BIG-IP VM tests |
| D04 | Arista | MLAG and EVPN/VXLAN mapping | No EOS VM tests |

## 3. Service Catalogue and Ownership

| Service | Operational owner | Key evidence |
|---|---|---|
| Internet/WAN | Network team + Carrier | BGP, routes, FIB, interface/error, external probes |
| Corporate LAN | Network team | VLAN/gateway, adjacency, DHCP/DNS, access reachability |
| Security boundary | Security team | Policy install/commit, NAT, sessions, threat/logs |
| Customer portal | App + ADC + Security teams | DNS/TLS/HTTP/login, F5 VS/pool/backend, firewall |
| Monitoring | NOC / Observability | polling, syslog, traps, alert notification and recovery |
| Changes | Change Manager + implementer | approval, tested MOP, rollback, post-check, acceptance |

## 4. Six-Stage Summary

### Stage 1 — Service Transition and Baseline

Identify assets, software/licences, support contracts, management paths, configuration backups, carrier escalation, topology and actual service tests. A running router does not prove operational readiness. Record **As-Is** versus future **To-Be** and leave unvalidated acceptance criteria open.

### Stage 2 — Target Architecture Review

Proposed: two truly diverse ISPs, resilient Juniper WAN edge, Palo Alto Active/Passive HA, Cisco LAN, F5 LTM HA, Arista MLAG data-centre access, dedicated management/OOB and NMS. Design requirements include failure-domain diversity, route symmetry, public address reachability across failover, HA links, NAT behaviour, DMZ isolation, server return paths and end-to-end application testing.

**Design caveat:** Private Check Point/Palo Alto WAN interface addresses are not a substitute for public IP allocation, upstream NAT or globally routable prefixes. Additional L3/translation design is required for actual Internet service.

### Stage 3 — CHG-ABS-001: Planned Firewall Migration

**Scope:** Check Point R82 → Palo Alto, keeping ISP/Cisco core unchanged. 

**Pre-change:** approval, test plan, configuration and management-DB backup, OOB access, rule/objects/NAT/zone map, routing and gateway topology, HA readiness and tested rollback. Preserve old system as a standby recovery option without simultaneously enabling duplicate production IPs.

**Staging:** On isolated interfaces, configure Palo Alto untrust 10.100.0.2/30, trust 10.101.0.2/30, default via 10.100.0.1, HQ route 10.10.10.0/24 via 10.101.0.1, security policy and DIPP source NAT. Verify management and versions. PAN-OS DNAT Security Rule must use pre-NAT destination IP and post-NAT destination zone.

**Cutover:** final Go/No-Go → freeze → disable old data path → activate new data path → check adjacent MAC/ARP, sessions, routing and security → test real client DNS/TLS/HTTP/business transaction → business sign-off or rollback.

**Acceptance matrix:**

| ID | Check |
|---|---|
| V01 | Restricted management/OOB available |
| V02 | WAN interface and next hop good |
| V03 | HQ prefix route valid |
| V04 | Source NAT address as expected |
| V05 | Intended Security Rule and logs |
| V06 | DNS resolution from client |
| V07 | TLS plus HTTP response |
| V08 | Key business transaction accepted by owner |
| V09 | NMS collection and test notification |
| V10 | Traffic/System Logs and event time correlation |

**Rollback trigger:** critical transaction unavailable and restoration would overrun rollback budget, major control-plane/HA instability, management access lost, or other approved stop criterion. Remove Palo Alto from production path, restore Check Point with no duplicate IP, verify customer service and communicate. This MOP was **not executed**.

### Stage 4 — INC-ABS-0042: Major Incident (Simulation)

Simulated time 09:12–09:47, **35 min**. External portal unavailable. ISP-A BGP down but ISP-B active; PAN-OS permitted and destination-NATed traffic; F5 VS and pool appeared healthy. Simulated packet captures showed F5 backend SYN with original remote client source; backend SYN-ACK returned via Palo Alto (10.20.20.1), bypassing F5. Standard Virtual Server `source-address-translation { type none }` conflicted with approved one-arm design. Simulated recovery restored `automap`, then externally validated HTTPS/login.

**Important:** All packet captures, exact timeline and outcomes in this section were invented as a teaching incident, not retrieved from deployed Juniper, PAN-OS, F5 or Arista.

ISP-A outage is a distinct degraded-redundancy tracking item in the simulation; correlation in time does not prove it caused the application outage.

### Stage 5 — RCA, PIR, CAPA

**Proven within the constructed scenario:** One-arm F5 asymmetric server return path was the proximate failure mechanism.

**Unknown even in scenario:** who/what removed SNAT and when, whether a particular change-control weakness caused it. Real RCA would require configuration history, change records, audit logs, HA sync, and packet evidence.

CAPA proposals: approved VS SNAT/return-path baseline; drift detection with change correlation; pre-deploy topology/semantic checks; external multi-point synthetic DNS/TLS/HTTP and transaction monitoring; tested failover/rollback; assigned owners, due dates and measurable closure evidence.

### Stage 6 — Service Handover and Acceptance

Package requirements: service catalogue/SLA, actual topology and addresses, asset inventory, supported releases, support/carrier contacts, access and OOB procedure, sanitised config backups, monitoring/alert routing, role-based runbooks, change history, incidents/problems/CAPA, application validation and written acceptance.

**Acceptance blockers:** no Palo Alto or other new vendor VMs, no validated HA/failover, actual HTTPS business client, latest Check Point post-cleanup policy recheck, full monitored alert-to-notification verification, restored-backup test or actual customer SLA/approval.

## 5. Operational Runbooks (read-only first)

**RB-01: WAN degraded.** Verify interface and carrier demarc → BGP and prefixes accepted → route selection and FIB → return path/public address → customer application. Escalate with circuit ID, timestamps, counters, optical power if available, and relevant traces. Avoid ungrounded LOCAL_PREF changes.

**RB-02: Firewall/NAT.** Confirm ingress interface/zone → router route and next-hop → matching NAT and Security Rule → actual session/translation and drop logs → reverse path → business transaction. In Check Point, distinguish Gaia interface/routing, SmartConsole database Publish and Gateway Install.

**RB-03: Public web.** External DNS/VIP → WAN routing → DNAT/Security → F5 Virtual Server/pool/monitor → server TCP/TLS → application transaction. Pool Green ≠ business acceptance. One-arm design must ensure backend return through F5.

**RB-04: Switch/data-centre.** Interface/port channel/LACP → MLAG peer link and control → MAC/ARP → L3 route → EVPN/VXLAN VTEP/VNI when present. Avoid simultaneous unplanned MLAG peer restart.

**RB-05: P1.** Define impact and severity → create incident bridge and owners → gather read-only evidence in parallel → test explicit hypotheses → authorise restorative action or rollback → verify customer service → record incident timeline → update client → create Problem/RCA actions with remaining carrier risk.

## 6. Final Independent Senior Engineer Assessment — Pending

**Scenario:** Firewall cutover has 15 minutes left; verified rollback requires 10. WAN/route/SNAT/Ping good; F5 pool green, ISP-A BGP down, but payment transaction fails and the application owner refuses acceptance.

Score five criteria (0–2 each): (1) business impact and decision; (2) technical evidence beyond Ping/SNAT; (3) multi-layer fault isolation without assuming ISP-A root cause; (4) change governance/customer communication; (5) safe rollback and transaction validation.

**No grade has been awarded:** The learner has not submitted the independent answer.

## 7. Final Risk Disposition

- **Course:** six design stages completed.
- **Operational service:** pending acceptance, fictional customer.
- **Hands-on evidence:** only specifically observed Cisco + Check Point and past independent M01–M11 labs.
- **Unverified:** Junos, PAN-OS, F5, Arista command behaviour and real data plane, HA failover, user business transaction tests.

Never publish real customer credentials, API keys, certificates or sensitive addressing into a public portfolio.
