# MPLS / DIA / BGP Transit / BFD — Reference Patterns

## MPLS core

```text
router ospf 100
 router-id <LOOPBACK>
 ...
mpls ldp router-id Loopback0 force
interface <CORE-IF>
 mpls ip
```

## CUSTOMER-A VRF

```text
vrf definition CUSTOMER-A
 rd 65000:10X
 route-target import 65000:100
 route-target export 65000:100
```

## BGP Transit trust boundary

```text
Customer egress: permit only authorized customer prefix(es)
Provider ingress: validate prefix + origin AS-path + maximum-prefix
```

Validated service separation in the lab:

- MPLS neighbor: only `192.168.10.0/24`
- Transit neighbor: only `203.0.113.0/25`

## BFD

```text
interface <PE-CE>
 bfd interval 300 min_rx 300 multiplier 3
router bgp <AS>
 neighbor <PEER> fall-over bfd
```

A synthetic ACL blackhole kept interfaces up/up while BFD detected forwarding failure and triggered BGP down immediately.
