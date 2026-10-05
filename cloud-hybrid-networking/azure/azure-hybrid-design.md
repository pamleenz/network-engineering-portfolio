# Azure Hybrid Design

## Addressing

| Component | Prefix / ASN |
|---|---|
| On-prem aggregate | 10.70.0.0/16 |
| On-prem LAN | 10.70.10.0/24 |
| On-prem BGP loopback | 10.70.255.1/32, AS65070 |
| Hub VNet | 10.80.0.0/20 |
| GatewaySubnet | 10.80.0.0/27 |
| Azure BGP peer | 10.80.0.30, AS65515 |
| Spoke-A | 10.80.16.0/20 |
| Spoke-B | 10.80.32.0/20 |

## Control plane

- Route-based S2S IPsec to Azure VPN Gateway.
- eBGP between AS65070 and AS65515.
- On-prem advertises `10.70.10.0/24`.
- Azure advertised hub and both spoke prefixes after gateway transit was enabled.

## Verification achieved

- IPsec SA: Established.
- BGP: Established.
- Received prefixes: 3.
- Advertised prefixes: 1.
- Bidirectional data-plane test successful to both spoke workloads.

## Additional enterprise topics

- Private Endpoint / Private Link.
- Private DNS / conditional forwarding / Azure DNS Private Resolver.
- Overlapping address space and NAT/NVA workarounds.
- Asymmetric routing through stateful firewalls.
- Active-active VPN design and BGP/ECMP.
- ExpressRoute and VPN coexistence.
