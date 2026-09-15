# CML / IOL Platform Limitations Observed

This lab uses Cisco CML Free with IOS-XE IOL L2 images. It is suitable for control-plane and configuration practice, but it is not a physical Catalyst switch.

## Observed limitations / artifacts

### `storm-control`

The current IOL image rejected the `storm-control` interface command. The production purpose and common Catalyst syntax were reviewed, but data-plane storm-control behaviour was not reproduced.

### `%AMDP2_FE-6-EXCESSCOLL`

The lab repeatedly produced excessive-collision messages on virtual Ethernet interfaces. Interface counters showed full duplex, no CRC, no late collisions, and no carrier errors. This was treated as an IOL/virtual-platform artifact.

On real full-duplex Catalyst interfaces, increasing collision/error counters should trigger investigation of duplex/PHY/cabling/transceiver/hardware.

### Hardware and chassis features

The lab does not reproduce:

- StackWise / StackWise Virtual
- VSS
- Nexus vPC
- Aruba VSX / Juniper MC-LAG class multi-chassis LAG
- PoE and endpoint power negotiation
- Physical transceiver DOM / optics / cabling faults
- ASIC buffer, microburst and line-rate forwarding behaviour

### Access security

DHCP Snooping CLI and trust-boundary design were validated. DAI and IP Source Guard were not forced without a real DHCP binding database. This avoids manufacturing a misleading success state in a platform-limited lab.

## Cross-vendor conceptual mapping

| Cisco | Aruba CX | Juniper EX | Meraki MS |
|---|---|---|---|
| VLAN / 802.1Q trunk | VLAN / tagged interfaces | VLAN / ethernet-switching | VLAN / trunk port |
| Rapid-PVST+ / MST | RPVST / MSTP | RSTP / MSTP | RSTP |
| LACP EtherChannel | LAG / LACP | ae interface / LACP | Link aggregation |
| HSRP | VRRP | VRRP | Warm spare / routed design options |
| DHCP Snooping / DAI | DHCP Snooping / ARP protection features | DHCP security / DAI equivalents by platform | DHCP server policy / access security features |
| CDP / LLDP | LLDP | LLDP | CDP/LLDP visibility |

The exact CLI and feature set varies by model/software release. The transferable skill is the design and troubleshooting model, not memorising one vendor's command syntax.
