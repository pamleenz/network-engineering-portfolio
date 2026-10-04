# Cisco Nexus / NX-OS Production Mapping

## Core commands

```text
show nve interface nve1 detail
show nve peers
show nve vni
show bgp l2vpn evpn summary
show bgp l2vpn evpn
show l2route evpn mac-ip all
show l2route evpn imet all
show ip route vrf TENANT-A
show mac address-table
show ip arp vrf TENANT-A
show interface counters errors
```

## Localized outage example

If VLAN100 is healthy but VLAN200 fails, prioritize:

```text
show nve vni
show running-config vlan 200
show l2route evpn imet all
show l2route evpn mac-ip all
```

A mismatch such as VLAN200 -> VNI10210 on one leaf while all other leaves use 10200 produces a local VNI-specific failure even though underlay and EVPN sessions are healthy.

## Control-plane vs dataplane distinction

- `show bgp l2vpn evpn` proves the route exists in BGP.
- It does **not** alone prove the route/MAC was successfully installed in the tenant RIB, L2RIB, FIB or ASIC.
- Always combine protocol state with `show ip route vrf`, MAC/ARP/L2route tables, counters and packet testing.

## vPC reference

vPC peer-link carries coordination/state and selected data traffic. Peer-keepalive is liveness detection, not a forwarding replacement. Peer-link down while keepalive is up normally causes the secondary to suspend local vPC member ports; keepalive loss alone degrades protection but does not normally stop data forwarding.
