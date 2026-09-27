# Enterprise Wireless & NAC — Job-Ready Lab

> A production-oriented lab for secure enterprise access using 802.1X, EAP-TLS, RADIUS, NAC authorization, MAB, CoA, guest segmentation, and incident troubleshooting.

## Why this lab exists

This lab is not a Wi-Fi command exercise. Its purpose is to practise the control-plane and data-plane reasoning used by enterprise Network Engineers and Network Security Engineers when operating secure access networks.

The lab deliberately separates three questions:

1. **Authentication — who/what is connecting?**
2. **Authorization — what access should it receive?**
3. **Enforcement — did the network actually apply that decision?**

## Topology

```text
                         +----------------------+
                         |      RADIUS1         |
                         | Ubuntu / FreeRADIUS  |
                         | 10.10.99.20/24       |
                         +----------+-----------+
                                    |
                                    | VLAN 99
                                    |
+-------------+    Wi-Fi     +------+-------+       +----------------+
| CORP-CLIENT |~~~~~~~~~~~~~~|   CORP-AP    |-------|      SW1       |
| 10.10.10.10 |   EAPOL      | hostapd      | trunk | IOS-XE IOL-L2  |
+-------------+              | br0.99 .10   |       +-------+--------+
                             +--------------+               |
                                                            |
                                                     +------+-------+
                                                     | IOT-PRINTER  |
                                                     | Alpine       |
                                                     +--------------+

RADIUS1 ens3 -> CML NAT-INTERNET (used for package access, not treated as guest Internet validation)
```

## VLAN plan

| VLAN | Name | Purpose | Gateway / Key IP |
|---:|---|---|---|
| 10 | CORP-WLAN | Corporate authenticated users | SW1 10.10.10.1 |
| 20 | NAC-RESTRICTED | Restricted / unmanaged endpoints | SW1 10.10.20.1 |
| 30 | IOT-DEVICES | Printer / IoT segment | SW1 10.10.30.1 |
| 40 | GUEST-WIFI | Guest/untrusted users | SW1 10.10.40.1 |
| 99 | INFRA-RADIUS | AP management and RADIUS | SW1 10.10.99.1, AP 10.10.99.10, RADIUS1 10.10.99.20 |

## Lab classification

| Capability | Classification | Notes |
|---|---|---|
| RADIUS Access-Request / Accept / Reject / Challenge | **REAL PROTOCOL LAB** | Real FreeRADIUS exchanges |
| PEAP/MSCHAPv2 | **REAL PROTOCOL LAB** | Real EAP negotiation |
| EAP-TLS | **REAL PROTOCOL LAB** | Real PKI and mutual TLS flow |
| RADIUS Accounting | **REAL PROTOCOL LAB** | Accounting packets observed |
| CoA / Disconnect on UDP/3799 | **REAL PROTOCOL LAB** | Real DAS listener and Disconnect-ACK |
| RADIUS authorization attributes | **REAL PROTOCOL LAB** | VLAN attributes returned by RADIUS |
| Wired MAB enforcement on SW1 | **CONFIG / PROTOCOL LAB** | IOL-L2 image lacks required 802.1X/MAB commands |
| Dynamic VLAN enforcement on Linux AP | **CONFIG / PROTOCOL LAB** | Not forced into custom Linux bridge engineering |
| Physical RF, RSSI/SNR/interference/roaming | **DESIGN / OPS KNOWLEDGE** | CML does not model real radio physics |

## Completed scenarios

### 1. Infrastructure and RADIUS baseline

- Built VLANs 10/20/30/40/99.
- AP management traffic uses tagged VLAN 99.
- Corporate user traffic is locally bridged and mapped to the switch native user VLAN.
- FreeRADIUS listens on UDP/1812 (authentication) and UDP/1813 (accounting).

### 2. WPA2-Enterprise with PEAP/MSCHAPv2

Validated the complete chain:

```text
Client -> EAPOL -> AP/Authenticator -> RADIUS -> FreeRADIUS
```

A correct password completed PEAP/MSCHAPv2 and authorized the controlled port. A wrong password failed authentication.

### 3. EAP-TLS and PKI

Created a lab CA and certificates for RADIUS1 and corporate endpoints. The client validates the RADIUS server and the RADIUS server validates the client certificate.

Successful client state included:

```text
wpa_state=COMPLETED
Supplicant PAE state=AUTHENTICATED
suppPortStatus=Authorized
EAP state=SUCCESS
selectedMethod=13 (EAP-TLS)
```

### 4. NAC authorization decisions

FreeRADIUS returned different authorization results by identity:

```text
corp-client       -> VLAN 10
restricted-client -> VLAN 20
```

This lab proves the **authorization decision** at protocol level. Dynamic enforcement on the virtual AP was intentionally not over-engineered.

### 5. MAB / IoT policy simulation

A known printer MAC was represented as a MAB identity and returned VLAN 30. An unknown endpoint was first rejected, then matched a lab-only restricted fallback to VLAN 20.

Important: the `Auth-Type := Accept` fallback used in the lab is a demonstration shortcut. Production ISE/ClearPass policy should match endpoint database/profiling/authorization conditions rather than simply accepting unknown Ethernet devices.

### 6. CoA / Disconnect

The AP was configured as a Dynamic Authorization Server (DAS) listener on UDP/3799. FreeRADIUS sent a Disconnect-Request identifying the active session. The AP returned `Disconnect-ACK`, removed the session, and the client reauthenticated.

### 7. Guest / untrusted wireless

The AP was temporarily switched to `GUEST-WIFI` and the AP-facing trunk native VLAN was changed to VLAN 40. An inbound SVI ACL enforced isolation:

```text
Guest -> VLAN 10   DENY
Guest -> VLAN 20   DENY
Guest -> VLAN 30   DENY
Guest -> VLAN 99   DENY
Guest -> other     PERMIT
```

ACL counters incremented during tests, proving policy enforcement rather than simple route absence.

### 8. Incident troubleshooting

Three failure domains were tested.

| Incident | Authentication plane | Data plane | Root cause |
|---|---|---|---|
| RADIUS service failure | FAIL | N/A | FreeRADIUS stopped; UDP/1812-1813 not listening |
| Rogue EAP-TLS certificate | FAIL | N/A | Self-signed client certificate; `unknown_ca` / certificate verify failure |
| VLAN 10 removed from AP trunk | PASS | FAIL | Authentication succeeded but L2 forwarding for corporate VLAN was broken |

The third incident is particularly important operationally: **“Wi-Fi connected” or “ISE authentication passed” does not prove user traffic can reach the network.**

## Troubleshooting model

When a user reports “Corporate Wi-Fi is not working”, work down the stack instead of immediately restarting an AP:

```text
Impact & Scope
   -> RF / Association
   -> 802.1X / EAP
   -> RADIUS / NAC
   -> Authentication
   -> Authorization
   -> VLAN / ACL / SGT enforcement
   -> DHCP / Client IP
   -> Gateway / Routing
   -> Firewall / DNS / Application
```

A useful early split is:

```text
Authentication / control-plane problem?
                 OR
Data-plane forwarding problem?
```

## Production mapping

| Lab component | Cisco enterprise equivalent | Aruba / other equivalent |
|---|---|---|
| wpa_supplicant | Windows/macOS native supplicant / enterprise endpoint supplicant | Same endpoint role |
| hostapd AP/authenticator | Catalyst AP + Catalyst 9800 WLC | Aruba AP + Mobility Gateway / Central |
| FreeRADIUS | Cisco ISE Policy Service Node | Aruba ClearPass |
| authorize file | ISE Policy Set / Authentication / Authorization rules | ClearPass Service / Role Mapping / Enforcement Policy |
| VLAN tunnel attributes | ISE Authorization Profile | ClearPass Enforcement Profile |
| RADIUS debug | ISE Live Logs | ClearPass Access Tracker |
| CoA / Disconnect | ISE CoA / Reauthenticate / Disconnect | ClearPass CoA |
| Guest VLAN ACL | WLAN/Policy Profile + ACL/dACL/firewall policy | Role / Enforcement / firewall policy |

### Cisco ISE mental model

```text
Policy Set
   -> Authentication Policy
   -> Authorization Policy
   -> Authorization Profile
```

- **Authentication** asks who/what the endpoint is and how it proves identity.
- **Authorization** decides what access it should receive.
- **Authorization Profile** returns the enforcement result, such as VLAN, dACL, SGT, or permit/restrict action.

### Catalyst 9800 mental model

```text
WLAN Profile      = wireless service / SSID / security
Policy Profile    = VLAN / AAA override / ACL / forwarding behaviour
Policy Tag        = binds WLAN to Policy Profile
AP Tagging        = determines what service an AP advertises
```

In a typical centralized Cisco WLAN, the WLC is the RADIUS NAD/NAS and the AP transports client traffic/control to the controller.

### Profiling, dACL, SGT, posture and BYOD

These are important production concepts but were not artificially forced into CML:

- **Profiling:** classify endpoints from RADIUS/DHCP/OUI/CDP/LLDP/SNMP and other telemetry.
- **dACL:** download endpoint-specific ACL policy rather than relying only on VLAN separation.
- **SGT / TrustSec:** apply role-based policy using security group tags instead of only IP/VLAN identity.
- **Posture:** evaluate endpoint compliance and place it into full, restricted, or remediation access.
- **BYOD onboarding:** register personal devices and typically provision certificates for later certificate-based access.

## Key operational lessons

- Association, authentication, authorization, IP connectivity, and application reachability are separate states.
- Ping reachability to a RADIUS host does not prove UDP/1812 authentication service is healthy.
- EAP-TLS certificate validation belongs at the authentication server; an AP/WLC normally transports EAP inside RADIUS.
- MAB is weaker than EAP-TLS because a MAC address can be spoofed.
- RADIUS packet `Code` determines Accept/Reject/Challenge; tunnel attributes describe authorization results.
- A native VLAN still has to be permitted by the trunk allowed-VLAN list.
- Authentication success should immediately move troubleshooting toward DHCP/VLAN/trunk/gateway/firewall/DNS if the user still has no service.

## Repository contents

```text
enterprise-wireless-nac/
├── README.md
├── configs/
│   ├── sw1.txt
│   ├── hostapd-corp.conf
│   ├── hostapd-guest.conf
│   ├── wpa-supplicant-eaptls.conf
│   ├── freeradius-authorize-snippets.txt
│   └── freeradius-coa-example.txt
└── docs/
    └── change-verification-rollback.md
```

## Skills demonstrated

`802.1X` · `EAP-TLS` · `PEAP/MSCHAPv2` · `RADIUS` · `PKI` · `NAC` · `MAB` · `CoA` · `Guest Segmentation` · `VLAN/Trunking` · `ACL` · `Troubleshooting` · `RCA` · `Cisco ISE Concepts` · `Catalyst 9800 Concepts`

## Scope / limitations

This lab intentionally does **not** claim physical RF testing, real Cisco ISE GUI configuration, real Catalyst wired MAB enforcement, or production-grade dynamic VLAN enforcement on the Linux AP. Where the virtual platform could not faithfully reproduce production behaviour, the result is explicitly classified as protocol/configuration/design knowledge rather than a real enforcement test.
