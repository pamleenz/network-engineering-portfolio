# Change / Verification / Rollback Template

## Pre-change

- Record interface, OSPF, EVPN, NVE/VNI, VRF route and MAC/ARP baselines.
- Confirm dual path / dual RR redundancy before intentionally removing one component.
- Save FRR configuration (`write memory`).
- Remember: Linux `ip link` / `ip addr` runtime objects are not persisted by FRR; use the dataplane reconstruction script after reboot.

## Change

Apply one controlled variable only: uplink, RR session, RT, VNI state, MTU or policy.

## Verification

Use both protocol state and a business-path test. For VXLAN, packet capture is preferred when the question is “which VNI/path did the traffic actually use?”

## Rollback

- Restore interface/admin state.
- Restore RT/VNI/policy.
- Restore consistent underlay MTU.
- Recheck OSPF, EVPN sessions, VNI state, tenant RIB, MAC/ARP and end-to-end traffic.

## Close

Document symptom, blast radius, exact root cause, corrective action and evidence of restored service.
