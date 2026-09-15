# Final Incident RCA — Degraded Inter-Distribution EtherChannel

## Ticket / Alert

Inter-distribution `Port-channel1` is operational but degraded. One of two LACP members is suspended. No immediate user outage is reported.

## Impact and Scope

- Customer/user outage: none observed
- Port-channel operational state: up
- Active members: 1 of 2
- Aggregate bandwidth: reduced from 20000 Kbit/s to 10000 Kbit/s in the lab image
- Physical redundancy: lost
- HSRP: stable
- STP: stable, but path cost increased because the bundle lost one member

## Evidence

```text
Po1(SU) LACP Et0/0(s) Et0/1(P)
```

On DSW1:

```text
%ETC-5-CANNOT_BUNDLE2: Et0/0 is not compatible with Et0/1 and will be suspended
(DHCP snooping state of Et0/0 is Untrusted, Et0/1 is Trusted)
```

`show etherchannel 1 detail`:

```text
Probable reason: DHCP snooping state of Et0/0 is Untrusted, Et0/1 is Trusted
```

Configuration comparison showed that DSW1 Ethernet0/1 had an unintended `ip dhcp snooping trust` command while Ethernet0/0 did not.

## Root Cause

An EtherChannel member configuration inconsistency was introduced on DSW1. The two physical members had different DHCP Snooping trust states. IOS treated the members as incompatible and suspended Ethernet0/0 from the bundle.

DSW2 reported the secondary symptom that LACP was not enabled on the remote member. The decisive root-cause evidence was on DSW1.

## Change Plan

Purpose: restore member consistency and return Po1 to two active links.

Change:

```cisco
interface Ethernet0/1
 no ip dhcp snooping trust
```

Risk: brief LACP/STP reconvergence while the member rejoins the bundle.

Rollback command:

```cisco
interface Ethernet0/1
 ip dhcp snooping trust
```

The rollback reproduces the original fault and is documented only as the inverse configuration action.

## Verification

```text
Po1(SU) LACP Et0/0(P) Et0/1(P)
Members in this channel: Et0/0 Et0/1
BW 20000 Kbit/sec
```

STP root-path cost returned from 100 to 56 on VLANs that cross Po1, and `show spanning-tree inconsistentports` returned zero inconsistent ports. HSRP remained in the intended Active/Standby state.

## Preventive Actions

- Treat the Port-channel as one logical interface and keep member policies consistent.
- Compare all member configurations before and after changes.
- Include `show etherchannel summary` and `show etherchannel <group> detail` in the validation checklist.
- Apply access-edge DHCP Snooping trust policy at the correct trust boundary; do not casually apply it to one distribution EtherChannel member.
- Escalate degraded redundancy even when end-user traffic is still passing.
