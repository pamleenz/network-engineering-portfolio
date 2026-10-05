# AWS Hybrid Troubleshooting Simulation

| Symptom | First checks |
|---|---|
| Both tunnels down | Internet/public IP, IKE proposal, PSK, Phase1 |
| IPsec up, BGP down | inside tunnel IP, ASN, BGP neighbor |
| BGP Established, no routes | prefix policy, route propagation |
| AWS has routes, on-prem does not | outbound TGW/VGW advertisement and BGP policy |
| Routes exist, traffic fails | Security Group, NACL, FortiGate policy, NAT |
| One direction only | return route / asymmetric routing |
| Tunnel 1 fails and traffic also fails | Tunnel 2 BGP session, route selection, propagation |
| VPC-A works, VPC-B fails | TGW association/propagation and VPC route table |

## Diagnostic chain

```text
IPsec
  -> BGP
  -> TGW/VGW route
  -> VPC route table
  -> Security Group / NACL
  -> FortiGate policy
  -> Return path
```
