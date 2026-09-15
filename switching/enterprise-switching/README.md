# Enterprise Switching Job-Ready Lab

Production-oriented Cisco campus / managed-LAN lab built in Cisco CML using IOS-XE IOL L2 images.

## What this lab demonstrates

- VLAN design and 802.1Q trunking with an unused native VLAN
- Rapid-PVST+ root engineering and deterministic L2 forwarding
- PortFast, BPDU Guard, and Root Guard
- LACP EtherChannel and degraded-member troubleshooting
- SVI-based inter-VLAN routing
- HSRP first-hop redundancy aligned with STP root placement
- DHCP Relay (`ip helper-address`) on user VLAN SVIs
- DHCP Snooping trust-boundary design at the access layer
- SSH management, CDP/LLDP, MAC-table and interface-counter operations
- Production-style incident handling: impact, triage, evidence, root cause, change, verification, rollback, RCA

## Topology

```text
                     +----------------------+
                     |        DSW1          |
                     |  L3 / HSRP / STP     |
                     +----------+-----------+
                                ||
                                ||  Po1 / LACP
                                ||
                     +----------+-----------+
                     |        DSW2          |
                     |  L3 / HSRP / STP     |
                     +----------+-----------+

                         Distribution Pair

                 DSW1 E0/2           DSW2 E0/2
                     |                   |
                     | 802.1Q trunk      | 802.1Q trunk
                     |                   |
                     +---------+---------+
                               |
                           +---+---+
                           | ASW1  |
                           +---+---+
                               |
                  +------------+------------+
                  |                         |
              ASW1 E0/2                 ASW1 E0/3
               VLAN 10                   VLAN 40
                  |                         |
               CLIENT                     SRV1
```

### Physical Links

| Local | Remote | Purpose |
|---|---|---|
| DSW1 E0/0 | DSW2 E0/0 | LACP Po1 member 1 |
| DSW1 E0/1 | DSW2 E0/1 | LACP Po1 member 2 |
| DSW1 E0/2 | ASW1 E0/0 | 802.1Q trunk |
| DSW2 E0/2 | ASW1 E0/1 | 802.1Q trunk |
| ASW1 E0/2 | CLIENT E0 | Access VLAN 10 |
| ASW1 E0/3 | SRV1 ens2 | Access VLAN 40 |

## VLAN and gateway plan

| VLAN | Name | Subnet | HSRP VIP | Preferred Active/Root |
|---:|---|---|---|---|
| 10 | CORP-USERS | 10.10.10.0/24 | 10.10.10.1 | DSW1 |
| 20 | ENGINEERING | 10.10.20.0/24 | 10.10.20.1 | DSW1 |
| 30 | GUEST | 10.10.30.0/24 | 10.10.30.1 | DSW2 |
| 40 | SERVICES | 10.10.40.0/24 | 10.10.40.1 | DSW2 |
| 99 | MANAGEMENT | 10.10.99.0/24 | 10.10.99.1 | DSW1 |
| 999 | NATIVE-BLACKHOLE | No SVI | — | DSW1 STP root |

## Final incident / RCA

The final production-style incident was not an artificial link shutdown. `Port-channel1` remained up, but one LACP member was suspended, reducing aggregate bandwidth and eliminating physical redundancy.

Evidence:

```text
Po1(SU) LACP Et0/0(s) Et0/1(P)
```

`show etherchannel 1 detail` identified the root cause on DSW1:

```text
Probable reason: DHCP snooping state of Et0/0 is Untrusted, Et0/1 is Trusted
```

A stray `ip dhcp snooping trust` command existed on only one physical EtherChannel member. Removing the inconsistent per-member setting restored:

```text
Po1(SU) LACP Et0/0(P) Et0/1(P)
BW 20000 Kbit/sec
STP root-path cost 56
0 inconsistent STP ports
```

See [`docs/final-incident-rca.md`](docs/final-incident-rca.md) for the full workflow.

## Repository structure

```text
enterprise-switching/
├── README.md
├── configs/
│   ├── ASW1.cfg
│   ├── DSW1.cfg
│   └── DSW2.cfg
└── docs/
    ├── final-incident-rca.md
    ├── platform-limitations.md
    └── verification-cheatsheet.md
```

## Notes

The configuration files are **clean reference configurations** representing the final intended lab state, not raw `show running-config` exports. Credentials are redacted. Features not faithfully reproduced by the current CML/IOL image are documented separately.
