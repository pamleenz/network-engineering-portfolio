# Failure Engineering Results

## Fault 1 - Single Leaf-to-Spine uplink failure

Injected `LEAF1 eth0 down`.

Observed: OSPF retained SPINE2 only; one inactive and one active route to remote VTEP remained. PC1-to-PC2 traffic survived. **Result: PASS.**

## Fault 2 - Single EVPN RR session failure

On LEAF1:

```text
router bgp 65000
 neighbor 10.255.0.1 shutdown
```

Observed RR1 `Idle (Admin)` while RR2 remained Established. Redundant EVPN control-plane path survived. **Result: PASS.**

## Fault 3 - Wrong RT import

Configured an incorrect import RT `65000:59999` under TENANT-A.

Observed:
- EVPN global table still contained Type-5 `203.0.113.0/24` and default route with RT 65000:50000.
- `show ip route vrf TENANT-A 203.0.113.0/24` returned `Network not in table`.

Restoring `route-target import auto` immediately reinstalled the route via Border VTEP 10.255.1.3. **Result: PASS.**

## Fault 4 - L3VNI dataplane state manipulation

`vxlan50000` was administratively toggled on LEAF1. The experiment exposed an important operational distinction: BGP EVPN adjacency remained up while tenant forwarding state could require reprogramming/re-import after dataplane changes. Internal cross-subnet traffic and north-south traffic did not fail identically. Treat this as a dataplane programming/recovery exercise, not as a deterministic proof that every L3VNI-down event produces the same symptom.

## Fault 5 - MTU / VXLAN blackhole

The normal underlay MTU was 1600. A controlled path was reduced to 1500 while the alternate path was removed.

Correct source-specific test:

```bash
ip vrf exec TENANT-A ping -I 10.10.50.1 -M do -s 1472 203.0.113.1
```

A 1472-byte ICMP payload creates a 1500-byte inner IP packet. VXLAN adds outer Ethernet/IP/UDP/VXLAN overhead, so the underlay frame exceeds 1500. The DF test black-holed. Smaller traffic could pass. **Result: PASS.**

Operational signature: small ping works, large DF ping fails -> suspect path MTU / PMTUD / encapsulation overhead.
