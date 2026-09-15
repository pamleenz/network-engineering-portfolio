# Enterprise Switching Verification Cheat Sheet

## Physical / Interface

```cisco
show interfaces status
show interfaces Ethernet0/x
show interfaces counters errors
```

Check link state, negotiated speed/duplex, CRC/errors/drops, and interface descriptions.

## VLAN / Trunk

```cisco
show vlan brief
show interfaces trunk
show interfaces Ethernet0/x switchport
```

Confirm VLAN existence, native VLAN, allowed VLAN list, and active/forwarding VLANs.

## STP / Protection

```cisco
show spanning-tree root
show spanning-tree vlan 10
show spanning-tree inconsistentports
```

Confirm intended roots, root/alternate ports, path cost, and Root Guard inconsistencies.

## EtherChannel / LACP

```cisco
show etherchannel summary
show etherchannel 1 detail
show lacp neighbor
show interfaces port-channel1
```

`P` = bundled; `s` = suspended. A bundle can remain up while redundancy is lost.

## MAC / ARP

```cisco
show mac address-table dynamic
show mac address-table vlan 10
show ip arp
```

Use these to confirm data-plane learning and the actual forwarding direction.

## SVI / Routing / HSRP

```cisco
show ip interface brief
show ip route
show standby brief
show ip interface Vlan10
```

Verify SVI state, connected routes, HSRP Active/Standby ownership, helper address, and IP interface features.

## DHCP Snooping

```cisco
show ip dhcp snooping
show ip dhcp snooping binding
```

Validate operational VLANs, trusted ports, Option 82 behaviour, and learned bindings.

## Management / Discovery

```cisco
show ip ssh
show cdp neighbors
show lldp neighbors
```

Use CDP/LLDP to confirm cabling/topology before changing configuration.

## Production Troubleshooting Order

```text
Impact & Scope
→ Physical / Interface
→ VLAN
→ Trunk
→ STP / LACP
→ MAC / ARP
→ L3 / SVI / HSRP
→ Service Verification
→ Root Cause
```
