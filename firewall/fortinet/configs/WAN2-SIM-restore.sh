#!/bin/sh
# Rebuild the non-persistent Alpine WAN2 simulator used in the GNS3 lab.
# Lab-only helper. Adjust interface names/addresses if reused elsewhere.

set -eu

ip link set eth0 up
ip addr flush dev eth0 || true
ip addr add 172.16.2.1/30 dev eth0

ip link set eth1 up
udhcpc -i eth1

apk update
apk add iptables iproute2-tc

sysctl -w net.ipv4.ip_forward=1

iptables -t nat -F POSTROUTING
iptables -F FORWARD
iptables -t nat -A POSTROUTING -s 172.16.2.0/30 -o eth1 -j MASQUERADE
iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
iptables -A FORWARD -i eth1 -o eth0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Remove any previous netem impairment and return to the default qdisc where possible.
tc qdisc del dev eth0 root 2>/dev/null || true

ip addr show eth0
ip addr show eth1
ip route
iptables -t nat -L POSTROUTING -n -v
