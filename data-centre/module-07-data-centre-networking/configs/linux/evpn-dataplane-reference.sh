#!/bin/bash
# Reconstructed dataplane pattern from the verified lab.
# This is a reference reconstruction script, not an exact final snapshot.
set -e

ip link add TENANT-A type vrf table 1001 2>/dev/null || true
ip link set TENANT-A up

for BR in br100 br200 br50000; do
  ip link add "$BR" type bridge 2>/dev/null || true
  ip link set "$BR" up
done

ip link set br100 master TENANT-A 2>/dev/null || true
ip link set br200 master TENANT-A 2>/dev/null || true
ip link set br50000 master TENANT-A 2>/dev/null || true

# Replace LOCAL_VTEP and ROUTER_MAC per leaf before use.
LOCAL_VTEP=${LOCAL_VTEP:-10.255.1.1}
ROUTER_MAC=${ROUTER_MAC:-02:00:00:50:00:01}

ip link add vxlan10100 type vxlan id 10100 local "$LOCAL_VTEP" dstport 4789 nolearning 2>/dev/null || true
ip link add vxlan10200 type vxlan id 10200 local "$LOCAL_VTEP" dstport 4789 nolearning 2>/dev/null || true
ip link add vxlan50000 type vxlan id 50000 local "$LOCAL_VTEP" dstport 4789 nolearning 2>/dev/null || true

ip link set vxlan10100 master br100
ip link set vxlan10200 master br200
ip link set vxlan50000 master br50000
ip link set vxlan10100 up
ip link set vxlan10200 up
ip link set vxlan50000 up
ip link set br50000 address "$ROUTER_MAC"

# Lab anycast gateway model (Linux simplification):
ip addr replace 192.168.100.1/24 dev br100
ip addr replace 192.168.200.1/24 dev br200

# In the actual lab, access NIC membership and MAC addresses were set per leaf.
# LEAF1: PC1 on VLAN100, PC3 on VLAN200. LEAF2: PC2/PC4.
