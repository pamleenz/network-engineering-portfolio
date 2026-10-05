# AWS Hybrid Design Simulation

> This section is a design/configuration/troubleshooting simulation. No live AWS VPN resources were created because the account entered identity/payment verification suspension.

## Base addressing

- On-prem: `10.70.0.0/16`, AS65070
- AWS VPC: `10.90.0.0/16`
- Example workload subnet: `10.90.10.0/24`
- AWS VPN/TGW ASN used in examples: AS64512

## Site-to-Site VPN

AWS S2S VPN provides two independent IPsec tunnels. Each should be configured with its own:

- AWS outside public IP
- PSK
- inside tunnel addressing
- BGP neighbor

Example:

```text
Tunnel 1: 169.254.10.2 (on-prem) <-> 169.254.10.1 (AWS)
Tunnel 2: 169.254.20.2 (on-prem) <-> 169.254.20.1 (AWS)
```

## Transit Gateway

- **Attachment:** connection from VPC/VPN/DX to TGW.
- **Association:** which TGW route table an attachment uses for lookup.
- **Propagation:** which TGW route tables receive an attachment's routes.

Use multiple TGW route tables for segmentation such as Prod / Dev / Shared Services.

## Direct Connect

- Private VIF: private VPC connectivity.
- Public VIF: AWS public services.
- Transit VIF: Direct Connect Gateway + Transit Gateway.
- Still uses BGP.
- Private connectivity does not automatically mean encrypted traffic.
