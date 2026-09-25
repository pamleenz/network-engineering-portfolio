# Troubleshooting Cases

The cases below distinguish real faults from controlled fault injection and lab-environment limitations.

## Method Used

```text
Impact & Scope
  -> Interface / L2
  -> Routing / SD-WAN
  -> Firewall Policy
  -> NAT
  -> Session
  -> Security Profile
  -> VPN / Service
  -> Logs / Debug Flow / Packet Capture
  -> Root Cause
  -> Fix
  -> Verification
  -> Rollback / RCA
```

## Case 1 - strongSwan / Linux XFRM SA State Mismatch

### Symptom

Branch hosts could not reach HQ even though the FortiGate still temporarily reported the IPsec selector as up.

### Evidence

- Branch WAN underlay `192.168.201.134 -> 192.168.201.132` was reachable.
- `ip xfrm policy` still contained the tunnel selectors.
- `ip xfrm state` was empty.
- FortiGate retained the previous SA/counters for a period of time.

This created a mismatch between branch kernel IPsec state and the FortiGate's retained tunnel state.

### Root Cause

The branch-side strongSwan/charon process had lost/restarted its active SA state, leaving XFRM policies without usable ESP states while the FortiGate still retained the previous SA.

### Resolution

```bash
ipsec restart
ipsec up HQ-BRANCH-WAN1
ipsec statusall
ip xfrm state
```

### Verification

- IKE_SA: `ESTABLISHED`
- CHILD_SA: `INSTALLED`
- Inbound/outbound XFRM ESP states present
- Branch-to-HQ ping restored
- FortiGate selectors returned to `1/1`
- IPsec packet counters incremented in both directions

### Lesson

Do not declare a VPN healthy from one endpoint or from a single control-plane status. When needed, validate kernel/data-plane SA state as well.

---

## Case 2 - Link Alive but SD-WAN SLA Failed

### Type

Controlled fault injection using Linux `tc netem`.

### Symptom

WAN2 remained physically up but new Internet flows were steered to WAN1.

### Evidence

Examples observed:

```text
state(alive)
sla_map=0x0
```

- ~165-173 ms latency exceeded the 80 ms threshold.
- ~30% loss caused SLA failure.
- High jitter caused SLA failure even while latency remained below its threshold.

### Behavior

Debug flow confirmed new traffic selected WAN1 and SNATed to the WAN1 address. After impairment was cleared, new traffic returned to preferred WAN2.

### Lesson

`state(alive)` only means the path still responds. It does not mean it meets business-quality requirements. Inspect `latency`, `jitter`, `packet-loss` and `sla_map`.

---

## Case 3 - Hard WAN Failure and Session Behavior

### Type

Controlled fault injection.

### Symptom

WAN2 was taken down completely.

### Evidence

FortiGate reported WAN2 `state(dead)` and new Internet flows moved to WAN1.

A pre-failure ICMP flow used:

```text
gateway=172.16.2.1
SNAT=172.16.2.2
sdwan_mbr_seq=2
```

After hard failure, a new flow used:

```text
gateway=192.168.201.2
SNAT=192.168.201.132
sdwan_mbr_seq=1
```

### Failback Observation

After WAN2 recovered, an existing healthy WAN1 session remained on WAN1 while a new session selected preferred WAN2.

### Lesson

Do not describe SD-WAN failover as universally seamless. Session continuity depends on protocol, NAT state, application behavior and whether the session can survive a source/path change.

---

## Case 4 - Internet SD-WAN Redundancy Did Not Protect the VPN Overlay

### Type

Architecture validation / controlled underlay failure.

### Symptom

With WAN1 disabled:

```text
port1: dead
port3: alive, SLA pass
HQ Internet: working
HQ-BRANCH-WAN1: selectors 1/0
Branch -> HQ: failed
```

### Evidence

The IPsec Phase 1 was explicitly bound to WAN1:

```text
set interface "port1"
```

### Root Cause

This was a design dependency, not a firewall software fault. The lab provided dual-WAN resilience for general Internet access but only a single underlay for the branch overlay.

### Design Improvement

A production requirement for VPN path redundancy should use multiple overlay paths across independent underlays (or an appropriate dynamic VPN design), then apply routing/SD-WAN health logic to the overlays.

### Lesson

**Internet SD-WAN redundancy does not automatically provide IPsec overlay redundancy.**

---

## Case 5 - GNS3 Docker Nodes Lost Runtime State After Restart

### Type

Lab-environment limitation.

### Symptom

After a project restart, the Alpine WAN2 simulator and branch VPN container lost IPv4 addressing, routes, packages and runtime configuration.

### Root Cause

The Docker nodes used in the lab were non-persistent/recreated between restarts.

### Recovery

Re-applied addressing, IP forwarding, iptables/NAT, strongSwan and tunnel configuration, then re-established a known-good baseline before continuing firewall troubleshooting.

### Lesson

Always verify the lab/production baseline before attributing a symptom to a new network fault.

---

## Useful Commands

### Interface / Routing / SD-WAN

```text
get system interface physical
get router info routing-table all
show router static
diagnose sys sdwan member
diagnose sys sdwan health-check
diagnose sys sdwan service4
```

### Policy / NAT

```text
show firewall policy
show full-configuration firewall policy <id>
```

### Debug Flow

```text
diagnose debug reset
diagnose debug flow filter clear
diagnose debug flow filter saddr <src>
diagnose debug flow filter daddr <dst>
diagnose debug flow filter proto <proto>
diagnose debug flow show function-name enable
diagnose debug enable
diagnose debug flow trace start <count>

# Always stop/reset after use
diagnose debug disable
diagnose debug reset
```

### Packet Capture

```text
diagnose sniffer packet <interface> '<filter>' 4 <count> l
```

### IPsec

```text
get vpn ipsec tunnel summary
diagnose vpn tunnel list name <tunnel>
```

strongSwan/Linux:

```text
ipsec statusall
ip xfrm policy
ip xfrm state
```
