# M11 Final Technical Summary

## 1. Objective

Build a production-style observability workflow that answers five different operational questions:

1. **Is the device/service reachable?**
2. **What is its current state and trend?**
3. **What changed?**
4. **What happened around the change?**
5. **Who generated the traffic?**

The module used Cisco IOS-XE plus LibreNMS and supporting Linux collectors rather than treating monitoring as a single GUI exercise.

## 2. Architecture and management identity

- M11-NMS management/collector interface: `10.99.0.20/24`
- M11-R1 transport interface: `10.99.0.101/24`
- M11-R1 stable management Loopback: `10.255.11.1/32`
- LibreNMS device target: `10.255.11.1`
- Static route on M11-NMS: `10.255.11.1/32 via 10.99.0.101 dev ens34`

A Loopback gives the NMS a stable logical identity. It does not remove the need for working routing to that Loopback.

## 3. LibreNMS deployment

LibreNMS was deployed with the official Docker Compose example and validated with:

- LibreNMS application container
- MariaDB
- Redis
- dispatcher
- snmptrapd
- syslog-ng
- msmtpd

A Docker bridge issue after an accidental VM shutdown was isolated by proving that the service worked inside the container while host routing to the Docker bridge network was missing. Recreating the Compose stack network restored service without deleting volumes.

Lesson: separate application health, host socket state, container networking and external reachability during troubleshooting.

## 4. SNMP polling

### SNMPv3 security

The polling design used SNMPv3 `authPriv`, with a view, group, user and NMS ACL. Secrets are intentionally excluded from this repository.

Key concepts:

- UDP/161: polling / queries
- UDP/162: traps / notifications
- Authentication and privacy are independent SNMPv3 security functions
- Net-SNMP password-to-key validation requires sufficiently long secrets

### OIDs and MIBs

An OID is the numeric identifier of a managed object. A MIB gives names, structure and meaning to those OIDs.

Examples:

```text
SNMPv2-MIB::sysName.0
1.3.6.1.2.1.1.5.0

IF-MIB::ifDescr
1.3.6.1.2.1.2.2.1.2

IF-MIB::ifHCInOctets
1.3.6.1.2.1.31.1.1.1.6

IF-MIB::ifHCOutOctets
1.3.6.1.2.1.31.1.1.1.10
```

The numeric base identifies the column/object and the final index identifies the interface row.

### GET, GETNEXT, WALK and BULK

- `snmpget`: retrieve an exact scalar/instance
- `snmpgetnext`: retrieve the lexicographically next OID
- `snmpwalk`: repeatedly walk a subtree
- `snmpbulkget`: fetch multiple table objects efficiently

LibreNMS effectively automates large-scale versions of these operations.

### Counters and rates

The lab generated controlled ICMP traffic and observed `ifHCInOctets` increasing. LibreNMS converts counter deltas into rates:

```text
rate = (new_counter - old_counter) / elapsed_time
```

For high-speed links, 64-bit HC counters are preferred over legacy 32-bit octet counters.

## 5. SNMP traps

A separate SNMPv3 trap user was created and matched to the receiver-side engine ID/user configuration.

The lab verified:

- UDP/162 reachability
- SNMPv3 encrypted packets in tcpdump
- snmptrapd process and configuration
- LibreNMS trap handler integration
- linkDown/linkUp events for Loopback1

Important lesson: receiving UDP/162 does not prove the application can authenticate/decrypt/process the SNMPv3 trap. Troubleshoot transport, USM/security, handler and database/UI as separate layers.

## 6. Syslog

The syslog-ng sidecar was enabled and LibreNMS syslog support activated.

Cisco used:

- Loopback0 as the source interface
- UDP/514 as the destination transport
- informational threshold
- millisecond timestamps

The lab correlated Cisco severity with standard Syslog levels:

```text
4 -> warning
5 -> notice
6 -> informational
```

Syslog added causal context not available from interface state alone, such as:

```text
%LINK-5-CHANGED
Interface ... changed state to administratively down
```

That wording strongly points toward administrative/configuration action rather than a physical carrier failure.

## 7. NTP and timeline integrity

M11-NMS was configured as an NTP server using chrony.

The router reached:

```text
Clock is synchronized, stratum 4, reference is 10.99.0.20
```

This made timestamps from:

- router console
- Syslog
- SNMP traps
- packet captures
- LibreNMS events
- LibreNMS alerts

comparable during RCA.

## 8. NetFlow / IPFIX concepts

Flexible NetFlow was built from:

```text
record -> monitor -> exporter -> interface attachment
```

The lab used the predefined `netflow-original` record and exported NetFlow v9 to `10.99.0.20:2055`.

The collector exposed real conversations, including SNMP, ICMP and NTP.

Operational model:

- SNMP tells how much traffic an interface carries.
- NetFlow tells which conversations account for the traffic.

NetFlow v9 is template-based and strongly influenced the standardized IPFIX model.

## 9. Alerting and noise reduction

The initial LibreNMS rule collection demonstrated alert duplication: device down, ICMP failure, port down, latency and other conditions can all describe one underlying failure.

The lab reduced the active rule set to a single primary actionable device-down rule for the final incident.

Principle:

> Telemetry should be comprehensive; paging/alerting should be selective and actionable.

## 10. Availability and SLA interpretation

The final outage showed that polling-based monitoring has finite temporal resolution.

Actual outage:

```text
10:24:44.736 -> 10:30:06.043
~321 seconds
```

Polling observed:

```text
Down detected 10:27:47
Up detected   10:31:07
```

The NMS-observed outage is therefore not identical to the real service outage.

Use the term **TTD / detection delay** for a single event. **MTTD** requires multiple incidents and an average.

High availability targets require measurement resolution appropriate to the SLA; a five-minute polling cycle is too coarse to measure very short outages precisely.

## 11. Configuration and operational hygiene

The router configuration was saved to startup-config at the end of the module.

Production practice should also include:

- off-device configuration backup
- change tickets and peer review
- pre/post-check evidence
- rollback criteria
- credential and secret management
- NTP consistency
- alert ownership and escalation paths

Local IOS configuration archive is useful but is not a substitute for off-device backup.

## 12. Troubleshooting lessons

1. Do not assume a platform-specific command exists; verify capability and syntax.
2. Do not confuse a green recovered Alert Log row with an active alert simply because the rule name still says “Device Down”.
3. Distinguish detected event, outage record and alert state.
4. Trap/Syslog delivery depends on a surviving path to the collector.
5. If the management path itself fails, polling may be the only mechanism able to discover total loss.
6. On recovery, event-driven telemetry can arrive before the next poll.
7. Time synchronization is part of observability architecture, not a cosmetic setting.
8. A device being reachable is not proof that the network service or business service is healthy.

## 13. Production mental model

```text
Telemetry
  -> Collection
  -> Normalization
  -> Baseline
  -> Rule evaluation
  -> Alert / incident
  -> Triage
  -> Correlation
  -> Escalation
  -> Remediation
  -> Validation
  -> RCA / improvement
```

M11 is complete when the engineer can move through this lifecycle using evidence instead of relying on one monitoring screen.
