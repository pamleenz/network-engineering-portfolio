# Verification Guide

## Baseline

```text
show ip ospf
show ip ospf neighbor
show ip ospf interface <interface>
show ip ospf database
show ip ospf route
show ip route ospf
```

## LSDB-specific checks

```text
show ip ospf database router <router-id>
show ip ospf database network <dr-interface-ip>
show ip ospf database summary <lsa-id>
show ip ospf database external <lsa-id>
show ip ospf database nssa-external <lsa-id>
```

## Final-state evidence to retain

- R1-R2: Full adjacency with MD5 authentication
- R2-R3: broadcast segment with DR behavior
- R3: ABR with Area 0 and Area 1 LSDBs
- R4: Totally NSSA edge behavior and Type 7 externals
- Area 0: `172.168.1.0/29` inter-area summary
- Area 0: `203.0.113.0/29` translated external summary
- R4 eth1: `No Hellos (Passive interface)` while `10.0.45.0/30` remains advertised
