# Hybrid Cloud Reference Topology

```text
                         On-premises
                 FortiGate / Router AS65070
                    10.70.0.0/16
                           |
              +------------+-------------+
              |                          |
        Internet IPsec                Private Circuit
         + BGP                         + BGP
              |                          |
      +-------+-------+          +-------+-------+
      |               |          |               |
   Azure VPN        AWS S2S   ExpressRoute   Direct Connect
   Gateway          VPN/TGW
      |               |
   Hub VNet       Transit Gateway
   /     \          /       \
Spoke-A Spoke-B   VPC-A     VPC-B
```

## Layer responsibilities

- **IPsec / VPN:** secure overlay and encrypted transport over the Internet.
- **BGP:** dynamic prefix exchange and path control.
- **Cloud route tables / TGW / Gateway Transit:** cloud-side forwarding.
- **NSG / Security Group / NACL / FortiGate policy:** traffic authorization.
- **DNS:** name-to-private-endpoint resolution.
- **Return path:** must be valid and preferably symmetric through stateful security devices.
