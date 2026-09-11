# Final Technical Summary

## Core Mental Model

BGP troubleshooting should follow the routing pipeline rather than start with random configuration checks:

```text
Route Origination
 -> BGP Advertisement
 -> Inbound Policy
 -> NEXT_HOP Validation
 -> Best Path Selection
 -> Global RIB Selection
 -> CEF/FIB
 -> Data Plane / Return Path
```

## Best Path - Practical Order

1. Highest Weight (Cisco-local only)
2. Highest LOCAL_PREF
3. Locally originated
4. Shortest AS_PATH
5. Lowest Origin type: IGP < EGP < incomplete
6. Lowest MED (normally comparable for paths from the same neighbouring AS unless knobs alter this behaviour)
7. eBGP over iBGP
8. Lowest IGP metric to NEXT_HOP
9. Later tie-breakers such as oldest external path, lower router ID/originator ID, shorter cluster list, lower neighbour address

Administrative Distance is not part of BGP best-path selection. It is considered later when the BGP best path competes with routes from other sources in the global RIB.

## Policy Architecture

A production-style ISP/customer policy can be modelled as:

```text
Customer ingress
 -> Validate authorised prefix
 -> Validate AS / trigger attributes
 -> Tag community
 -> Set LOCAL_PREF
 -> Propagate internally
 -> Egress policy matches community
 -> Permit / deny / prepend / blackhole
```

## Dual-Upstream Design

### Outbound

Use LOCAL_PREF inside the customer AS:

```text
ISP-A = 200
ISP-B = 100
```

### Inbound

Use AS-PATH prepend or provider-defined communities. Prepending affects remote preference but cannot guarantee remote selection because other attributes may be preferred first.

## Route Leak Prevention

Do not rely on AS-loop prevention as the primary customer export control. Apply explicit outbound filters on every upstream so the CE only advertises authorised customer prefixes.

## RTBH

The lab used community `65002:666` as the customer blackhole trigger. The ISP ingress route-map validated the /32 and community, set a discard next hop, set LOCAL_PREF 250, added `no-export`, and propagated it internally. CEF confirmed recursive resolution to Null0.

The `ebgp-multihop 2` requirement encountered in this IOL lab is platform/lab-specific and must not be treated as a universal RTBH design requirement.

## Maximum-Prefix

Maximum-prefix protects an ISP from customer leaks or unexpectedly receiving a full table. Exceeding the configured limit caused the session to enter `Idle (PfxCt)` and withdraw customer routes. Removing the bad route did not automatically restore the neighbour; a reset was required in this lab.

## Aggregation

`aggregate-address ... summary-only` advertised the aggregate while suppressing specifics. A discard route for the aggregate appeared through Null0, protecting against forwarding loops for addresses covered by the aggregate but not by any specific route.

## Default Route

`neighbor ... default-originate` generated a default toward a neighbour on this IOS-XE lab even when the local RIB had no 0/0. This is different from `network 0.0.0.0`, which normally relies on an exact default route being present in the local RIB.

## Soft Changes

- `clear ip bgp <peer>`: hard session reset
- `clear ip bgp <peer> soft in`: re-evaluate inbound routing policy
- `clear ip bgp <peer> soft out`: re-advertise with current outbound policy
- Route Refresh: request routes again without tearing down the session
- `soft-reconfiguration inbound`: store pre-policy routes locally; useful for `received-routes` but consumes more memory

## Show Commands

```text
show ip bgp summary
show ip bgp <prefix>
show ip bgp neighbors <peer> routes
show ip bgp neighbors <peer> advertised-routes
show ip prefix-list
show route-map
show ip route <destination>
show ip route <next-hop>
show ip cef <destination> detail
```

## Strongest Takeaways

```text
Session up != route exists
Route exists != route is usable
Valid != best
Best != installed in RIB
Installed in RIB != forwarding works
One policy permits != full policy chain permits
BGP best-path selection != Administrative Distance comparison
Outbound TE -> LOCAL_PREF
Inbound TE -> AS_PATH / provider community
```
