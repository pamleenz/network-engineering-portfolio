# BGP Troubleshooting Playbook

## 1. Start With Scope

Before changing configuration, identify whether the issue affects:

- one prefix or all prefixes;
- one neighbour or all neighbours;
- control plane only or actual forwarding;
- inbound traffic, outbound traffic, or both.

## 2. Session Layer

```text
show ip bgp summary
show ip bgp neighbors <peer>
show ip interface brief
ping <peer>
```

If the neighbour is not Established, check IP reachability, interface state, remote AS, TCP/179, authentication, update source, timers and administrative shutdown state.

## 3. Route Origination

```text
show ip bgp <prefix>
show ip route <prefix>
show running-config | section router bgp
```

A `network` statement does not create a route. The exact prefix normally has to exist in the local RIB before BGP can originate it.

## 4. Advertisement Boundary

```text
show ip bgp neighbors <peer> advertised-routes
```

If the prefix exists locally but is not advertised, inspect outbound prefix-lists and route-maps. Remember that a route-map ends in an implicit deny.

## 5. Receive / Accept Boundary

```text
show ip bgp neighbors <peer> routes
show ip bgp <prefix>
show ip prefix-list
show route-map
```

If the sender advertises the route but the receiver does not accept it, inspect inbound policy, AS-path loop prevention, communities and maximum-prefix state.

## 6. NEXT_HOP Reachability

Typical symptom:

```text
10.0.12.1 (inaccessible)
Paths: (1 available, no best path)
```

Check:

```text
show ip route <next-hop>
show ip cef <next-hop> detail
```

For iBGP, use `next-hop-self` where the receiving router otherwise cannot reach an external next hop.

## 7. BGP Best vs Global RIB

Typical RIB-failure symptom:

```text
r> 198.18.101.0 ...
```

The `>` means BGP selected the path as best. `r` means the global routing table preferred another route source, often because of a lower administrative distance.

Compare:

```text
show ip bgp <prefix>
show ip route <prefix>
```

## 8. CEF / Data Plane

```text
show ip cef <destination> detail
ping <next-hop>
ping <destination> source <customer-source>
traceroute <destination>
```

A route being present in BGP and the RIB does not prove forwarding or return-path success.

## 9. Common Fault Patterns From This Lab

| Symptom | Evidence | Likely Cause |
|---|---|---|
| Neighbour Active | Underlay ping fails | Interface/IP reachability problem |
| Prefix local but not advertised | Missing in `advertised-routes` | Outbound prefix-list / route-map |
| Sender advertises, receiver missing | Receiver policy | Inbound filter / implicit deny |
| Route present, no best | NEXT_HOP inaccessible | Underlay / `next-hop-self` |
| `r>` | BGP best but not in RIB | Better AD route, e.g. static |
| `Idle (PfxCt)` | MAXPFXEXCEED logs | Maximum-prefix exceeded |
| RTBH /32 present internally but absent externally | `no-export` | Expected behaviour |
| Route visible through wrong long path | Direct export missing | Policy omission / route leak path |

## 10. Safe Change Workflow

```text
Ticket / Alert
 -> Impact and scope
 -> Evidence collection
 -> Hypothesis
 -> Change plan
 -> Risk and rollback
 -> Implementation
 -> Verification
 -> Customer update
 -> RCA / documentation
```
