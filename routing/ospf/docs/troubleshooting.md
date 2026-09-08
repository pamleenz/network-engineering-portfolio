# OSPF Troubleshooting Notes

## Standard workflow

```text
Physical / Interface
  -> IP reachability
  -> OSPF interface parameters
  -> Neighbor state
  -> LSDB
  -> OSPF route calculation
  -> Global RIB / FIB
```

## Faults validated

### Area mismatch
- **Symptom:** Interface up, direct ping succeeds, no OSPF adjacency.
- **Evidence:** R1 eth0 Area 0 vs R2 eth0 Area 1.
- **Resolution:** Restore matching area IDs.

### Authentication mismatch
- **Symptom:** Full neighbor stops refreshing and disappears after Dead Timer expiry.
- **Evidence:** MD5 enabled both sides but key material differs.
- **Resolution:** Restore matching key.

### Hello/Dead mismatch
- **Symptom:** IP connectivity remains, adjacency is not maintained.
- **Evidence:** 10/40 on one side vs 5/20 on the other.
- **Resolution:** Restore matching timers.

### Duplicate Router ID
- **Symptom:** Abnormal adjacency/LSDB behavior.
- **Resolution:** Assign unique RID and reset/reconverge as required.

### Route control
- **ABR Type 3 filter:** source-area Type 1 remains; remote Type 3 is withdrawn.
- **Redistribution route-map:** local static remains; denied prefix never becomes an external LSA.
- **RIB competition:** an OSPF LSA and OSPF-calculated route can exist while a lower-AD route wins the Global RIB.
