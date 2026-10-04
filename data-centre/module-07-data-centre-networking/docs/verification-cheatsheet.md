# Verification Cheat Sheet

| Layer | FRR / Linux | Cisco Nexus / NX-OS |
|---|---|---|
| Physical | `ip link`, counters | `show interface`, `show interface counters errors` |
| OSPF underlay | `show ip ospf neighbor` | `show ip ospf neighbors` |
| RIB | `show ip route` | `show ip route` |
| EVPN sessions | `show bgp l2vpn evpn summary` | `show bgp l2vpn evpn summary` |
| EVPN NLRI | `show bgp l2vpn evpn` | `show bgp l2vpn evpn` |
| VNI | `show evpn vni`, `ip -d link` | `show nve vni` |
| NVE/VTEP peers | Linux FDB/EVPN routes | `show nve peers` |
| MAC/IP | `bridge fdb show`, `ip neigh show vrf TENANT-A` | `show l2route evpn mac-ip all`, `show mac address-table`, `show ip arp vrf TENANT-A` |
| IMET | EVPN Type-3 | `show l2route evpn imet all` |
| Tenant RIB | `show ip route vrf TENANT-A` | `show ip route vrf TENANT-A` |
| Packet proof | Wireshark/tcpdump UDP 4789 | SPAN/ERSPAN/capture platform tools |

## Packet-capture expectations

- L2VNI traffic: outer VTEP IPs, UDP/4789, VNI 10100/10200, inner host MACs.
- Symmetric IRB: outer VTEP IPs, UDP/4789, **VNI 50000**, inner source/destination leaf router MACs, original tenant IP packet.
- North-south: VXLAN VNI50000 inside the fabric; plain IP on Border-to-CE link.
