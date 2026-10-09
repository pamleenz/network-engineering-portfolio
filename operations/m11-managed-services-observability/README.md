# M11 - Managed Services & Observability

Production-style managed-services observability lab built around Cisco IOS-XE, LibreNMS, SNMPv3, Syslog, NetFlow v9, NTP, alerting, incident correlation, and RCA.

## What this module demonstrates

- LibreNMS deployment and device onboarding
- Stable management identity using a router Loopback
- SNMPv3 polling with authentication and privacy
- MIB/OID interpretation, IF-MIB tables, 64-bit interface counters, GET/NEXT/BULK
- SNMP linkUp/linkDown traps and receiver-side USM validation
- Syslog collection over UDP/514 with stable Loopback source identity
- NTP synchronization so NMS, traps, Syslog and packet captures can be correlated
- Flexible NetFlow v9 export to nfcapd/nfdump
- Alert lifecycle, duplicate/noisy alert reduction, outage detection and recovery
- Detection-delay and SLA/availability implications of periodic polling
- Production-style incident timeline, validation and RCA

## Topology

```text
                           +----------------------------+
                           |          M11-NMS           |
                           | Ubuntu 24.04               |
                           |                            |
Internet/NAT -------------| ens33: DHCP                |
                           | ens34: 10.99.0.20/24       |
                           | LibreNMS / MariaDB / Redis |
                           | snmptrapd / syslog-ng      |
                           | chrony / nfcapd / nfdump   |
                           +-------------+--------------+
                                         |
                                  VMnet2 / CML Bridge1
                                         |
                           +-------------+--------------+
                           |          M11-R1            |
                           | Cisco IOS-XE 17.18.2       |
                           | E0/0: 10.99.0.101/24       |
                           | Lo0: 10.255.11.1/32        |
                           +----------------------------+
```

LibreNMS monitors `10.255.11.1` as the stable management identity. M11-NMS reaches that Loopback through:

```text
10.255.11.1/32 via 10.99.0.101 dev ens34
```

## Telemetry model

| Source | Operational question | What was validated |
|---|---|---|
| SNMP polling | What is the current state? | Device/interface state, counters, CPU, memory, traffic |
| SNMP trap | What changed just now? | linkDown/linkUp events delivered to LibreNMS |
| Syslog | What happened and what was the context? | Cisco subsystem, severity, mnemonic and message |
| NetFlow | Who is using the traffic? | Source/destination, protocol, port, packets, bytes |
| NTP | Can all evidence share one timeline? | Router synchronized to M11-NMS |

The key production lesson is that these data sources are complementary rather than interchangeable.

## SNMPv3

LibreNMS polls the router Loopback with SNMPv3 `authPriv`.

Example verification:

```bash
snmpget -v3 -l authPriv \
  -u librenms \
  -a SHA -A '<AUTH_SECRET>' \
  -x AES -X '<PRIV_SECRET>' \
  10.255.11.1 \
  1.3.6.1.2.1.1.5.0
```

IF-MIB examples used in the lab:

```text
1.3.6.1.2.1.2.2.1.2       ifDescr
1.3.6.1.2.1.31.1.1.1.6    ifHCInOctets
1.3.6.1.2.1.31.1.1.1.10   ifHCOutOctets
```

The lab also verified `snmpgetnext` and `snmpbulkget`, then correlated raw counters with LibreNMS graphs.

## SNMP traps

A separate SNMPv3 trap user was configured and the LibreNMS `snmptrapd` sidecar was validated.

The lab deliberately tested `Loopback1` linkDown/linkUp events and confirmed the corresponding LibreNMS Event Log entries.

Important operational lesson:

> Trap delivery can be fast, but only while a working path to the collector still exists.

When the sole management transport `Ethernet0/0` was shut, the router could no longer deliver the down event to the NMS. Polling eventually detected total device loss. After the transport recovered, Syslog and SNMP traps arrived quickly again.

## Syslog

Validated pipeline:

```text
M11-R1
  -> UDP/514
  -> M11-NMS
  -> syslog-ng
  -> LibreNMS Syslog
```

Packet capture proved the stable source identity:

```text
10.255.11.1:<ephemeral> -> 10.99.0.20:514
SYSLOG local7.notice
%SYS-5-CONFIG_I
```

The PRI value was also correlated with Cisco severity. For example, `local7.notice` produces PRI 189 because:

```text
23 * 8 + 5 = 189
```

## NTP

M11-NMS runs chrony and serves NTP to the management subnet.

Validated final state on M11-R1:

```text
*~10.99.0.20
Clock is synchronized, stratum 4, reference is 10.99.0.20
loopfilter state is 'CTRL' (Normal Controlled Loop)
```

NTP was essential for correlating Router CLI, Syslog, SNMP traps, packet captures, Event Log and Alert Log.

## NetFlow v9

Cisco Flexible NetFlow was configured as:

```text
Record:   netflow-original
Monitor:  M11-MONITOR
Exporter: M11-EXPORTER
Target:   10.99.0.20 UDP/2055
Source:   Loopback0
Attach:   Ethernet0/0 input
```

The collector used `nfcapd` / `nfdump`.

Observed flows included:

```text
10.99.0.20 -> 10.255.11.1  UDP/161  SNMP polling
10.99.0.20 -> 10.255.11.1  ICMP     management reachability
10.99.0.20 -> 10.99.0.101  UDP/123  NTP
```

This demonstrates the practical distinction:

```text
SNMP     -> how much / what state
NetFlow  -> who / where / protocol / port / packets / bytes
```

## Alerting and noise reduction

LibreNMS collection rules initially produced many overlapping alert conditions. The lab temporarily reduced the enabled rules to one primary actionable condition:

```text
Device Down (SNMP unreachable)
```

This demonstrates a core MSP/NOC principle:

> Monitor broadly, alert selectively.

One incident should not automatically become an alert storm.

## Final managed-services incident

The final incident intentionally shut the sole management transport on M11-R1.

| NZDT | Event |
|---|---|
| 10:24:44.736 | E0/0 administratively shut; real outage begins |
| 10:27:47 | LibreNMS polling detects Device Down |
| 10:27:47 | Critical Device Down alert fires |
| 10:30:06.043 | E0/0 link restored |
| 10:30:08 | Syslog reports line protocol Up |
| 10:30:10 | SNMP linkUp trap received |
| 10:31:07 | LibreNMS polling marks Device Up |
| 10:31:11 | Device Down alert recovers |

Calculated observations:

```text
Detection delay             ~182 s
Actual lab outage            ~321 s
Polling recovery delay       ~61 s
Alert clear delay            ~65 s
```

The NMS-recorded outage did not equal the real service outage because polling introduces sampling delay at failure and recovery boundaries.

See:
- [Final technical summary](docs/FINAL_TECHNICAL_SUMMARY.md)
- [Incident and RCA](docs/FINAL_INCIDENT_RCA.md)
- [Verification cheatsheet](docs/VERIFICATION_CHEATSHEET.md)
- [M11-R1 reference configuration](configs/M11-R1.cfg)
- [M11-NMS reference notes](configs/M11-NMS-reference.md)

## Repository structure

```text
m11-managed-services-observability/
├── README.md
├── configs/
│   ├── M11-NMS-reference.md
│   └── M11-R1.cfg
└── docs/
    ├── FINAL_INCIDENT_RCA.md
    ├── FINAL_TECHNICAL_SUMMARY.md
    └── VERIFICATION_CHEATSHEET.md
```

## Security

Credentials, SNMP authentication/privacy secrets and other reusable secrets are redacted. The configuration files are reference configurations and intentionally omit unrelated IOS-XE boilerplate.
