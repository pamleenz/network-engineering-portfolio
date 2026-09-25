# Change, Verification, Rollback and RCA

## Capstone Change

**Change:** Convert HQ Internet access from a single WAN to dual-WAN FortiGate SD-WAN while preserving the existing branch IPsec service.

## Scope

- Add WAN2 underlay.
- Add WAN1/WAN2 to `virtual-wan-link`.
- Configure performance SLA and member preference.
- Move the Internet default route to the SD-WAN zone.
- Update the corporate Internet policy to use the SD-WAN zone with NAT.
- Preserve and verify the route-based branch IPsec tunnel.

## Risks

- Incorrect WAN member/gateway configuration.
- Missing/incorrect default route.
- Firewall policy still pointing to a physical WAN instead of the SD-WAN zone.
- NAT disabled or misapplied.
- SLA thresholds too aggressive, causing path flapping.
- Existing sessions disrupted when path/NAT source changes.
- Branch VPN remains dependent on WAN1 because the overlay is bound to `port1`.

## Pre-Change Baseline

Record at minimum:

```text
get system status
get system interface physical
get router info routing-table all
diagnose sys sdwan health-check
get vpn ipsec tunnel summary
show firewall policy
```

Business checks:

```text
HQ client -> Internet
Branch client -> HQ
```

## Implementation Sequence

1. Configure WAN2 addressing and upstream gateway.
2. Verify WAN2 underlay connectivity.
3. Enable SD-WAN and create the `virtual-wan-link` zone.
4. Add WAN1 and WAN2 as members.
5. Configure `INTERNET_SLA` for latency, jitter and packet loss.
6. Configure the corporate Internet SD-WAN service rule.
7. Replace the standalone default route with an SD-WAN-zone default route.
8. Update the corporate Internet firewall policy destination to `virtual-wan-link`.
9. Confirm source NAT remains enabled.
10. Verify existing branch route and IPsec status.

## Post-Change Verification

Use the same checks as the pre-change baseline wherever possible.

### SD-WAN

```text
diagnose sys sdwan member
diagnose sys sdwan health-check
diagnose sys sdwan service4
```

### Routing

```text
get router info routing-table all
```

### Policy/NAT Path

Use debug flow when the actual forwarding member must be proven:

```text
received packet
Match policy routing
find route
find SNAT
Allowed by Policy-X
```

### VPN

```text
get vpn ipsec tunnel summary
diagnose vpn tunnel list name HQ-BRANCH-WAN1
```

### Service Verification

- HQ client reaches Internet.
- Branch reaches HQ.
- Fail WAN2: new Internet flows use WAN1.
- Restore WAN2: new flows return to preferred WAN2.
- Fail WAN1: Internet survives via WAN2, but the single-underlay branch VPN fails as expected.

## Rollback Triggers

Rollback if a critical requirement cannot be restored within the approved change window, for example:

- HQ Internet remains unavailable.
- Routing or NAT behavior is incorrect.
- Critical branch connectivity cannot be restored.
- SD-WAN instability/flapping causes unacceptable business impact.

## Rollback Plan

Return to the previous known-good single-WAN architecture:

1. Remove/disable the new SD-WAN forwarding dependency as required.
2. Restore the original WAN1 default route.
3. Restore the corporate Internet policy to `port2 -> port1`.
4. Confirm NAT is enabled.
5. Verify Internet and branch IPsec service.
6. Preserve logs/outputs for RCA before closing the incident/change.

## RCA Template

```text
Incident / Change ID:
Date / Time:
Business Impact:
Affected Sites / Services:

Trigger:
What event/change started the failure?

Technical Root Cause:
What specific technical state caused the service failure?

Evidence:
Which logs, counters, debug flow, packet captures or status commands prove the cause?

Contributing Factors:
What design/process/monitoring weakness increased impact or delayed recovery?

Resolution:
What was changed to restore service?

Verification:
How was service restoration confirmed?

Rollback (if used):
What known-good state was restored?

Preventive Actions:
What design, monitoring, automation or change-control improvement will prevent recurrence?
```

## Change Principle

A rollback plan is defined **before** implementation. It is not improvised after the change fails.
