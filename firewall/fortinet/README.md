# Fortinet Enterprise Firewall Job-Ready Lab

A scenario-based FortiGate lab covering enterprise Internet edge, segmentation, security profiles, DNAT/VIP, route-based IPsec, SD-WAN, production troubleshooting, HA design, FortiManager/FortiAnalyzer operations, and change/rollback practice.

> Lab platform: FortiGate-VM64-KVM, FortiOS 7.6.7, GNS3 + QEMU/KVM. This lab used a permanent EVAL license with feature constraints. It is a portfolio lab, not a production deployment.

## 1. Business Scenario

The HQ firewall protects a corporate LAN and provides resilient Internet access through two WAN underlays. A branch network connects to HQ with a route-based IKEv2 IPsec tunnel. The design is validated under quality degradation, hard WAN failure, failback, session persistence, and VPN underlay failure.

```text
                            Internet
                         /            \
                    WAN1/ISP1      WAN2/ISP2
                       |               |
                 port1 |               | port3
             192.168.201.132      172.16.2.2/30
                       \               /
                        \             /
                         +--- HQ-FGT ---+
                              |
                           port2
                              |
                        10.10.10.0/24
                              |
                         HQ-PC .10

Branch overlay (single underlay in this lab):

BR-PC 10.20.20.10 --- BR-VPN/strongSwan --- IPsec --- HQ-BRANCH-WAN1 --- HQ-FGT
                                                ^
                                                |
                                         bound to port1
```

## 2. What Was Implemented

| Stage | Scope | Result |
|---|---|---|
| 0 | Lab/licensing readiness | Completed |
| 1 | Enterprise Internet edge | Completed |
| 2 | Segmentation + security profiles | Completed |
| 3 | VIP/DNAT public service | Completed |
| 4 | Route-based IKEv2 IPsec | Completed |
| 5 | Dual-WAN SD-WAN | Completed |
| 6 | Integrated production troubleshooting | Completed |
| 7 | HA + FortiManager + FortiAnalyzer + operations | Design/operations knowledge completed |
| 8 | Change, verification, rollback, RCA, portfolio packaging | Completed |

## 3. Key Design Decisions

### Internet Edge

- HQ corporate LAN: `10.10.10.0/24` on `port2`.
- WAN1: DHCP on `port1` (`192.168.201.132/24` during validation).
- WAN2: `172.16.2.2/30` on `port3`, gateway `172.16.2.1`.
- Internet firewall policy uses the SD-WAN zone `virtual-wan-link` and source NAT.
- DNS forwarding was enabled on the corporate interface for the lab.

### SD-WAN

Custom SLA `INTERNET_SLA` monitored `8.8.8.8` using latency, jitter and packet loss.

Lab thresholds:

- Latency: 80 ms
- Jitter: 30 ms
- Packet loss: 5%
- Preferred member: WAN2 (`port3`)
- Fallback member: WAN1 (`port1`)

### IPsec

- Route-based IKEv2 tunnel: `HQ-BRANCH-WAN1`.
- HQ selector: `10.10.10.0/24`.
- Branch selector: `10.20.20.0/24`.
- Tunnel explicitly bound to `port1`, which intentionally demonstrated that Internet SD-WAN redundancy does not automatically create VPN underlay redundancy.

> **Crypto note:** The FortiGate EVAL image used in this lab exposed only low-encryption DES proposals. DES was used solely to make the constrained lab interoperate. Production deployments should use modern supported cryptography such as AES-GCM or AES with SHA-2 according to current organizational/vendor standards.

## 4. Validation Highlights

### SD-WAN quality degradation

Controlled `tc netem` impairment on WAN2 demonstrated that a link can remain physically alive while failing performance SLA.

Observed examples:

```text
state(alive) + sla_map=0x0
```

- ~165-173 ms latency exceeded the 80 ms threshold.
- ~30% injected loss produced an out-of-SLA state.
- Jitter-only degradation also caused SLA failure near the configured threshold.

New flows were steered to WAN1 while WAN2 remained physically up.

### Hard failover and failback

- WAN2 hard failure -> new Internet sessions used WAN1.
- WAN2 recovery -> established WAN1 sessions remained pinned, while new flows returned to preferred WAN2.
- This demonstrates that SD-WAN failover/failback is session-aware; it should not be described as universal zero-disruption migration.

### Underlay vs overlay

When WAN1 was disabled:

```text
port1: dead
port3: alive / SLA pass
HQ Internet: working through WAN2
HQ-BRANCH-WAN1: selectors 1/0
Branch -> HQ: failed
```

**Conclusion:** dual-WAN Internet resilience is not the same as dual-underlay VPN resilience. A production design requiring resilient branch VPN connectivity needs multiple overlay paths (or an appropriate dynamic VPN architecture) across independent underlays.

## 5. Production Troubleshooting Method

The lab used a fixed troubleshooting sequence:

```text
Impact & Scope
  -> Interface / L2
  -> Routing / SD-WAN
  -> Firewall Policy
  -> NAT
  -> Session
  -> Security Profiles
  -> VPN / Service
  -> Logs / Debug Flow / Packet Capture
  -> Root Cause
  -> Fix
  -> Verification
  -> Rollback / RCA
```

A representative FortiGate debug flow showed the complete forwarding evidence chain:

```text
received packet from port2
Match policy routing
find route via 172.16.2.1 / port3
find SNAT 172.16.2.2
Allowed by Policy-1: SNAT
SNAT 10.10.10.10 -> 172.16.2.2
```

A WAN-side packet capture then confirmed both request and reply:

```text
172.16.2.2 -> 8.8.8.8: ICMP echo request
8.8.8.8 -> 172.16.2.2: ICMP echo reply
```

## 6. Troubleshooting Cases

Detailed cases are in [`docs/troubleshooting.md`](docs/troubleshooting.md), including:

- strongSwan / Linux XFRM SA state mismatch.
- SD-WAN performance SLA degradation.
- Hard WAN failure and session behavior.
- Internet SD-WAN vs IPsec overlay dependency.
- Non-persistent GNS3 Docker node recovery as a lab-environment limitation.

## 7. Change / Verification / Rollback

The capstone change converted the Internet edge from a single WAN to dual-WAN SD-WAN while preserving the existing branch VPN. The change plan, pre/post checks, rollback triggers and RCA format are documented in [`docs/change-verification-rollback.md`](docs/change-verification-rollback.md).

## 8. HA / Central Management / Logging

Stage 7 covered the production operating model around the firewall platform:

- FGCP active-passive HA, heartbeat, election, interface monitoring and session pickup.
- HA troubleshooting with status/history/checksum concepts.
- FortiManager: ADOMs, device manager, policy packages, revisions, install preview, install workflow and configuration drift.
- FortiAnalyzer: traffic/event/security logs, FortiView, incident investigation, central retention and operational evidence.
- Upgrade lifecycle: backup, pre-check, implementation, post-check, observation window, rollback and RCA.

See [`docs/architecture-and-operations.md`](docs/architecture-and-operations.md).

## 9. Repository Files

```text
fortinet-enterprise-firewall/
├── README.md
├── configs/
│   ├── HQ-FGT-clean-reference.conf
│   ├── BR-VPN-strongswan.conf
│   └── WAN2-SIM-restore.sh
└── docs/
    ├── troubleshooting.md
    ├── change-verification-rollback.md
    └── architecture-and-operations.md
```

## 10. Security / Publishing Notes

- No real passwords or pre-shared keys are published.
- IPs are lab-only addressing.
- The configuration files are reference excerpts, not a full production export.
- EVAL-specific DES configuration must not be copied into production.
