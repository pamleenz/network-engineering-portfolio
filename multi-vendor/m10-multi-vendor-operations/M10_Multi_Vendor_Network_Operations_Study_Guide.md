# M10 — Multi-Vendor Network Operations | Technical Study Guide

> **Evidence boundary:** Check Point R82 + Cisco IOL was used hands-on. Juniper Junos, Palo Alto PAN-OS, F5 BIG-IP LTM and Arista EOS are **design-based learning and configuration examples, not executed vendor labs**. Review all commands against the intended product release and license before production use. Documentation addresses (198.51.100.0/24 and 203.0.113.0/24) are not live public addresses.

## 1. As-Built: Check Point R82 + Cisco IOL

```text
ISP-R1 Cisco IOL 10.100.0.1/30
     |
Check Point R82 eth1 10.100.0.2/30 (WAN)
Check Point R82 eth2 10.101.0.2/30 (INSIDE)
     |
HQ-CORE Cisco IOL 10.101.0.1/30
HQ-USERS Cisco Loopback10 10.10.10.1/24 (simulated user network)
Check Point eth0 MGT 10.99.0.50/24 / Windows MGT 10.99.0.1 / NMS 10.99.0.20
```

Observed in the lab: Gaia interface/static routing; SmartConsole object and policy configuration; Publish + Install; management lockout recovered through console using `fw unloadlocal`; gateway object was missing newly enabled interfaces until Get Interfaces Without Topology and Publish/Install; temporary ICMP diagnostic rules helped prove forwarding. Check Point Hide NAT produced logged source translation `10.10.10.1 -> 10.100.0.2` even after removing an upstream route to the private HQ subnet.

**Scope caveat:** Diagnostic ICMP rules were later deleted. The historical successful ping does not establish a fresh post-cleanup policy or actual HTTP/HTTPS application acceptance. Anti-lockout rule and management-interface anti-spoofing settings were lab concessions, not production controls.

## 2. Juniper Junos — WAN/BGP (design only)

Mental model: Routing Engine (RE) runs configuration management and routing control plane; Packet Forwarding Engine (PFE) handles forwarding. `candidate` versus `active` and `commit` differ from ordinary Cisco IOS immediate running-config updates.

```text
configure
show | compare
commit check
commit confirmed 5
# verify management, BGP, RIB/FIB, customer traffic
commit
```

`rollback 1` loads an earlier configuration into candidate and still requires commit. A rescue configuration is a distinct, intentionally saved recovery reference.

Proposed dual-ISP edge: AS65010 receives default routes from ISP-A AS65020 and ISP-B AS65030. Import routing policy accepts only `0.0.0.0/0 exact`, sets higher LOCAL_PREF (200) for ISP-A versus 100 for ISP-B, explicitly rejects other prefixes, and restricts export. Route-policy term order matters. Static default route preference may prevent expected BGP failover. BGP staying Established cannot detect degraded application performance on its own.

Useful operational commands:

```text
show interfaces terse
show bgp summary
show route 0.0.0.0/0 exact detail
show route receive-protocol bgp <peer> hidden
show route advertising-protocol bgp <peer>
show route forwarding-table destination 0.0.0.0/0
show system commit
```

**Design caveat:** An upstream routing-only Juniper connected to a Check Point NAT hiding users behind a private transit address does **not** create real Internet reachability without a separate public-routing/NAT solution. Dual-ISP design must also account for inbound public addressing and return-path symmetry.

## 3. Palo Alto PAN-OS — enterprise edge / DMZ (design only)

Mental model: dedicated MGT and data interfaces; Security Zones govern policy matching, while a Virtual Router (legacy routing engine) or Logical Router (advanced routing engine) determines IP next hops. Security Policies and NAT Policies are independent, and the Session Table plus Traffic/Threat Logs establish runtime evidence. In managed deployments, Panorama Commit and device Push are distinct from local firewall Commit.

Proposed network:

```text
ethernet1/1 10.100.0.2/30 -> zone untrust; default route via 10.100.0.1
ethernet1/2 10.101.0.2/30 -> zone trust; 10.10.10.0/24 via 10.101.0.1
ethernet1/3 10.20.20.1/24 -> zone dmz
HQ source NAT: trust -> untrust, 10.10.10.0/24, DIPP to e1/1 interface address
Public VIP: 198.51.100.10:443 -> DNAT 10.20.20.10:443
```

**Critical DNAT distinction:** NAT Rule matches the original destination IP and the destination Zone from pre-NAT route lookup (`untrust -> untrust` in this model). A Security Rule for the published app matches original destination **IP** `198.51.100.10` but destination **Zone** `dmz` (post-NAT route result). Upstream must deliver the VIP to the firewall.

`application-default` and App-ID do not mean any TCP/443 application is automatically permitted. Validate encrypted applications, dependencies, exceptions and business transactions.

Troubleshooting sequence: interface and routing; NAT Policy Match; Security Policy Match; live Session; Traffic Log end reason; receive/firewall/drop/transmit packet capture where needed; end-to-end business tests. In HA design validate failover, forwarding symmetry and real sessions. No Palo Alto VM was deployed in this course.

## 4. F5 BIG-IP LTM — application delivery (design only)

Objects: **Standard Virtual Server** (front-end), **Pool** (member set), **Node** (IP), **Pool Member** (IP:port) and **Health Monitor** (probe). A Full Proxy Standard Virtual Server has separate client- and server-side connections. A healthy Pool is not proof of successful external login/payment transaction.

Example single-arm design:

```text
Palo Alto DNAT 198.51.100.10:443 -> F5 VIP 10.20.20.100:443
F5 self IP 10.20.20.2/24
pool_web_https: 10.20.20.11:443, 10.20.20.12:443
Server gateway: Palo Alto 10.20.20.1
```

Illustrative tmsh:

```text
create ltm pool pool_web_https members add { 10.20.20.11:443 10.20.20.12:443 } monitor https
create ltm virtual vs_public_web destination 10.20.20.100:443 ip-protocol tcp pool pool_web_https profiles add { tcp } source-address-translation { type automap }
show ltm virtual vs_public_web
show ltm pool pool_web_https
list ltm virtual vs_public_web
save sys config
```

Without an approved return-path mechanism, the server may reply directly to its Palo Alto gateway, bypassing F5. SNAT Automap is a common one-arm remedy, but removes the real source IP at L3 from backend logs unless application-layer forwarding is separately designed. TLS passthrough does not expose HTTP headers for Cookie Insert or X-Forwarded-For modifications; these require terminating and inspecting HTTP/TLS through supported profiles.

Health checks should probe meaningful application readiness, not just ICMP or TCP accept. Also review Disabled versus Forced Offline, drains, HA ConfigSync, and persistent long-lived connections.

## 5. Arista EOS — switching and data centre (design only)

EOS uses Linux-based agents coordinated via SysDB. Ordinary CLI changes typically affect running configuration immediately; optional Configuration Sessions allow staged changes. Save using `copy running-config startup-config`; check the exact EOS release's session diff/commit syntax before use.

```text
configure terminal
vlan 10
 name APP-SERVERS
interface Ethernet1
 switchport mode access
 switchport access vlan 10
ip routing
interface Vlan10
 ip address 10.20.10.1/24
```

MLAG: two independent switches share a peer link and peer communication VLAN/SVI to provide a cross-device downstream Port-Channel. Check `show mlag`, `show mlag interfaces`, `show lacp neighbor`, `show interfaces port-channel 100`. Review peer-link failures, orphan ports, and dual-primary protections; never reboot peers as an undifferentiated fix.

EVPN/VXLAN: Underlay reaches VTEP loopbacks; EVPN control plane carries MAC/IP/prefix reachability; VXLAN encapsulates overlay traffic. `interface Vxlan1`, `vxlan source-interface` and `vxlan vlan 10 vni 10010` are only fragments, **not** a complete BGP EVPN fabric. Check BGP EVPN, VTEP peers and VNI/VLAN mappings.

eAPI provides a JSON-RPC interface; enable only through an approved restricted management interface/VRF with TLS, authentication and policy controls.

## 6. Cross-vendor operations matrix

| Platform | Usual change model | Post-change requirement |
|---|---|---|
| Cisco IOS | running config changes immediately | save to startup, validate RIB/FIB/business |
| Arista EOS | ordinary CLI immediately; optional configuration sessions | save, verify member/MLAG/FIB, confirm sessions |
| Junos | candidate then commit | confirmed-commit safety, verify then confirm |
| FortiGate | platform-specific immediate configuration | verify sessions, NAT, SD-WAN, security profiles |
| Check Point | Gaia network plus Management database | Publish, Install Policy, inspect Gateway/logs |
| Palo Alto | candidate then Commit; Panorama push where used | verify commit jobs, route, Policy/NAT/Session |
| F5 BIG-IP | runtime tmsh changes then explicit save | VS/pool/monitor, client + backend response, HA |

API success, configuration validation, BGP Established, Allow action, and Healthy pool status are **each insufficient by themselves** to prove a customer's application works.

## 7. Multi-layer troubleshooting workflow

```text
Service impact, timeline, approved change history
  -> physical interface and L2
  -> BGP / routing RIB and forwarding FIB
  -> firewall zones / security / NAT and session
  -> ADC VS / pool / members / monitor / server-side path
  -> application handshake, transaction and monitoring
  -> recovery validation, communication and RCA/PIR
```

Create explicit baselines, change approval, OOB access, configuration backups and tested rollback. Treat design-only output as teaching examples, not observed device results.

## 8. M12 handover

The [M12 integrated MSP capstone](../../operations/m12-integrated-ms-capstone/) reuses the actual Cisco + Check Point evidence while modelling migrations and multi-vendor incident scenarios. Formal application acceptance, full HA and Junos/PAN-OS/F5/EOS verification remain outstanding.
