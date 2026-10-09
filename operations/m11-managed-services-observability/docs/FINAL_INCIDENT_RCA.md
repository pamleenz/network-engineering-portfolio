# M11 Final Incident / RCA

## Incident

**Title:** Loss of management reachability to M11-R1

**Severity in lab:** Critical monitoring incident

**Affected target:** `10.255.11.1` (M11-R1 management Loopback)

## Impact

LibreNMS lost ICMP and SNMP reachability to the router. Because Ethernet0/0 was the only management transport, the router also lost its path for delivering Syslog and SNMP traps to the NMS while the interface was down.

The lab did not model an end-user business application, so the demonstrated impact is management/observability loss rather than a measured customer application outage.

## Timeline

| NZDT | Evidence |
|---|---|
| 10:24:44.736 | E0/0 administratively shut; real management outage begins |
| 10:27:47 | LibreNMS Event Log: Device status changed to Down from icmp,snmp check |
| 10:27:47 | Critical Device Down (SNMP unreachable) alert fires |
| 10:30:06.043 | E0/0 link returns Up |
| 10:30:08 | Syslog: line protocol Ethernet0/0 changed state to up |
| 10:30:10 | SNMP trap: linkUp Ethernet0/0 |
| 10:31:07 | LibreNMS polling marks device Up |
| 10:31:11 | Device Down alert enters recovered/green state |

## Detection metrics

```text
Single-event detection delay:
10:27:47 - 10:24:44.736
= ~182 seconds

Actual lab management outage:
10:30:06.043 - 10:24:44.736
= ~321 seconds

Polling recovery delay:
10:31:07 - 10:30:06.043
= ~61 seconds

Alert clear delay:
10:31:11 - 10:30:06.043
= ~65 seconds
```

These are single-incident measurements. They are not MTTD/MTTR averages.

## Root cause

Ethernet0/0 was administratively shut as the deliberate fault injection.

This interface was the sole transport between the NMS subnet and the router management Loopback. The Loopback itself remained logically up, but became unreachable because the path to it was removed.

## Why the monitoring sources behaved differently

### During failure

- Local Cisco Syslog messages were generated.
- The router had no working transport to the collector, so the failure event could not be delivered remotely.
- The same path dependency affected SNMP trap delivery.
- LibreNMS eventually discovered total loss by active ICMP/SNMP polling.

### During recovery

Once E0/0 came back:

1. Syslog could immediately leave the router again.
2. SNMP linkUp trap could be delivered.
3. The next polling cycle independently confirmed Device Up.
4. The alert rule cleared.

This validates the need to combine polling with event-driven telemetry.

## Resolution

```text
interface Ethernet0/0
 no shutdown
```

## Validation

Recovery was not accepted based on one ping alone. Evidence included:

- Ethernet0/0 returned up/up.
- Syslog reported line protocol Up.
- SNMP linkUp trap appeared in LibreNMS.
- ICMP and SNMP polling resumed.
- LibreNMS Device state returned Up.
- The critical Device Down alert recovered.

## Monitoring improvement

The initial ruleset produced overlapping conditions that could become an alert storm.

For the final test, nonessential rules were disabled and the primary actionable condition retained:

```text
Device Down (SNMP unreachable)
```

Production design should use deduplication, dependency/suppression logic, sensible severity, interface scoping and ownership rather than forwarding every detected anomaly to an engineer.

## Corrective / preventive actions

- Provide independent or redundant out-of-band management for critical devices where justified.
- Use stable management identities but remember that Loopbacks still depend on routing.
- Keep NTP consistent across devices and collectors.
- Keep off-device configuration backups.
- Define polling frequency based on service criticality and measurement objectives.
- Use Trap/Syslog for fast event context and polling for independent state confirmation.
- Tune alerts to represent actionable service conditions rather than raw telemetry.
