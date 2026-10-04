# Sample Incident RCA - Tenant External Prefix Missing

**Symptom:** Hosts in TENANT-A could not reach 203.0.113.0/24. EVPN BGP sessions were Established.

**Impact:** North-south connectivity for TENANT-A only. Fabric underlay and other control-plane sessions remained healthy.

**Evidence:** EVPN Type-5 for 203.0.113.0/24 remained present with RT 65000:50000, but `show ip route vrf TENANT-A 203.0.113.0/24` returned `Network not in table`.

**Root cause:** Incorrect tenant import RT (65000:59999) prevented the correct Type-5 route from being imported into TENANT-A.

**Resolution:** Removed the incorrect RT and restored automatic RT import. The route immediately reappeared via Border VTEP 10.255.1.3.

**Prevention:** Template/automation validation for VRF/VNI/RT consistency; post-change verification must compare EVPN RIB and tenant RIB rather than checking BGP session state only.
