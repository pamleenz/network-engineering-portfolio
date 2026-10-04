# Data-Centre Platform Ecosystem

## Cisco Nexus / NX-OS
Primary production mapping for this module: physical Clos fabric, VXLAN EVPN, NVE/VNI, Border Leaf and operations.

## NDFC
Nexus Dashboard Fabric Controller centralizes fabric design/provisioning, VXLAN EVPN deployment, consistency/compliance and operations. It is management/automation, not a different forwarding protocol.

## ACI
Controller/policy-based Cisco data-centre fabric. Operational objects are higher-level (Tenant, VRF, Bridge Domain, EPG, Contract) rather than hand-building every VLAN/VNI/NVE element.

## VMware NSX-T
Virtualization-layer overlay. Network engineers often need to determine whether a failure belongs to the NSX overlay, hypervisor edge, or physical fabric.

## Arista EOS
Comparable standards-based BGP EVPN / VXLAN Clos architecture; most conceptual knowledge transfers, while syntax and platform operations differ.

## F5
ADC/load-balancing service layer: VIPs, pools, health checks, SSL offload, SNAT and routing. Often connected through service/border leaf designs. Network troubleshooting focuses on VLAN/VRF, reachability, return path, routing/BGP and NAT behavior.
