# Azure Hybrid Troubleshooting

## Order of operations

1. Confirm underlay/public reachability.
2. Confirm IKE / IPsec SA.
3. Confirm BGP neighbor state and timers.
4. Inspect received/advertised prefixes.
5. Verify selected route / Effective Routes.
6. Verify NSG / Effective Security Rules.
7. Verify FortiGate/firewall policy and no unintended NAT.
8. Verify forward and return path.
9. Test end-to-end application traffic.

## Lab failure 1 - outbound prefix policy

- IPsec remained UP.
- BGP remained Established.
- `PfxSnt` changed from 1 to 0.
- `10.70.10.0/24` disappeared from Azure Effective Routes.
- Ping still succeeded because `10.70.0.0/16` remained as a less-specific fallback route.

Lesson: a withdrawn specific route does not guarantee an outage when a valid covering route exists.

## Lab failure 2 - IPsec stopped

- Data plane failed immediately: 100% loss.
- BGP temporarily remained Established because the hold timer had not yet expired.
- Later the BGP session reset.
- Restarting StrongSwan restored IPsec, BGP and traffic.

Lesson: control-plane state can lag behind a data-plane failure.
