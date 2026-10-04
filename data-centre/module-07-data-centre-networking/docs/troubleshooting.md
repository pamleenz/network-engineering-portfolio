# VXLAN EVPN Troubleshooting Tree

## 1. Scope the failure first

- One host only -> access port, MAC/ARP, endpoint issue.
- One VLAN/VNI only -> VLAN-VNI mapping, VNI state, RT, Type-2/3.
- One tenant/VRF only -> L3VNI, RT, Type-5, VRF route installation.
- All tenants on one leaf -> NVE/VTEP/underlay/uplink.
- Fabric-wide -> RR/BGP/underlay/common policy.
- North-south only -> Border Leaf, Type-5, external eBGP/policy/default route.

## 2. Ordered checks

1. Interface state, errors and MTU.
2. Underlay adjacency and VTEP loopback route.
3. BGP EVPN session health.
4. NVE peers and VNI operational state.
5. VLAN-VNI / VRF-L3VNI mapping; RD/RT.
6. Type-3 membership and Type-2 host routes.
7. Type-5 prefix routes for routed/north-south traffic.
8. Tenant RIB/FIB installation.
9. MAC/FDB and ARP/ND programming.
10. Packet capture.

## Key diagnostic patterns

### EVPN route exists, VRF route missing
Strongly suspect RT import/mapping or RIB programming.

### NVE peer Up and VNI Up, but host unreachable
Inspect Type-2, MAC table, ARP/ND, L2RIB/FIB programming and packet capture.

### VLAN100 works, VLAN200 fails
Do not start with OSPF. Check VLAN200-to-VNI mapping, VNI10200 state, Type-2/3, RT and access attachment.

### Small packets work, large DF packets fail
Path-MTU / PMTUD / encapsulation overhead.

### MAC moves once
Can be normal VM migration.

### MAC moves repeatedly between VTEPs
Suspect loop, duplicate MAC, bad dual-homing, hypervisor/vSwitch issue or EVPN multihoming problem.
