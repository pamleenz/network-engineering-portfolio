# M08 - Cloud & Hybrid Networking

Network-engineering portfolio module focused on hybrid connectivity rather than generic cloud administration.

## Scope

- Azure: VNet/subnet, peering, NSG, UDR, hub-spoke, S2S IPsec, BGP, gateway transit, Private Endpoint/DNS, ExpressRoute concepts, troubleshooting.
- AWS: VPC, Security Group/NACL, dual-tunnel Site-to-Site VPN, BGP, Transit Gateway, Direct Connect, troubleshooting simulation.
- On-prem mapping: FortiGate route-based IPsec, BGP, prefix filtering, firewall policy, no-NAT.

## Lab outcome

The Azure hands-on lab achieved end-to-end hybrid connectivity:

- On-prem simulator: `10.70.0.0/16`, BGP AS `65070`
- Azure Hub: `10.80.0.0/20`, Azure VPN Gateway BGP AS `65515`
- Spoke-A: `10.80.16.0/20`
- Spoke-B: `10.80.32.0/20`
- IPsec: Established
- BGP: Established, 3 Azure prefixes received / 1 on-prem prefix advertised
- Bidirectional traffic: successful to both spokes

Fault injection included BGP outbound filtering and IPsec failure/recovery.

## Important boundary

The Azure section was completed hands-on. The AWS section is an architecture/configuration/troubleshooting simulation because the AWS account entered identity/payment verification suspension before live resources were created. The repository does **not** claim a live AWS deployment.

## Key engineering lessons

1. `Tunnel UP` does not imply `BGP OK`.
2. `BGP Established` does not imply required prefixes are advertised/installed.
3. A withdrawn specific prefix may still be reachable via a less-specific fallback route.
4. Control-plane state may lag behind a data-plane failure.
5. Stateful firewalls require attention to the return path and routing symmetry.
6. Hybrid private traffic normally uses no NAT unless translation is intentionally part of the design.
7. AWS dual-tunnel VPN and TGW are routing problems as much as cloud-service problems.

## Repository layout

```text
cloud-hybrid-networking/
├── README.md
├── topology/
│   └── hybrid-cloud-reference.md
├── azure/
│   ├── azure-hybrid-design.md
│   ├── fortigate-azure-reference.conf
│   └── troubleshooting.md
├── aws/
│   ├── aws-hybrid-design.md
│   ├── fortigate-aws-reference.conf
│   └── troubleshooting.md
├── change-verification-rollback.md
└── M08_Cloud_Hybrid_Networking_Technical_Summary.docx
```

## Interview summary

> I designed and tested a hybrid cloud networking lab covering Azure hub-and-spoke, route-based IPsec VPN, BGP, gateway transit, NSGs and UDRs. I mapped the on-prem side to FortiGate and extended the architecture to AWS dual-tunnel VPN, Transit Gateway and Direct Connect. The troubleshooting work covered tunnel, BGP, route-policy, security-policy and return-path failures.
