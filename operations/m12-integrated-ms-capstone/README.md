# M12 — Integrated Enterprise / MSP Capstone

**Status:** Stage 1–6 **design and handover exercises complete**. Final independent Senior Engineer scenario answer and grading remain **pending**.  
**Customer:** Auckland Business Services (ABS) — **fictional learning scenario**.  
**Validation:** Actual Cisco IOL + Check Point R82 lab evidence is separated from simulated Juniper/Palo Alto/F5/Arista operations.

## Stages and artefacts

| Stage | Workstream | Output |
|---|---|---|
| 1 | Service Transition / Baseline | As-Is inventory, evidence register, operational acceptance gaps |
| 2 | Multi-Vendor Architecture Review | Proposed dual-ISP Juniper, Palo Alto HA, F5/DMZ and Arista design; HLD risk register |
| 3 | Firewall Migration / Production Change | CHG-ABS-001, pre-change, staged cutover, test matrix V01–V10, rollback |
| 4 | Major Incident / Multi-Layer Troubleshooting | INC-ABS-0042 **simulation**, WAN → NGFW → ADC → switch → application |
| 5 | RCA / PIR / CAPA | Technical cause, unknown configuration provenance, corrective/preventive controls |
| 6 | Service Handover / Assessment | Runbooks, acceptance gates, residual risks, final interview-style question (**not yet scored**) |

## Main document

[Final Service Handover Pack — Markdown](M12_Final_Service_Handover.md)

This is a simulated MSP deliverable, **not** a signed production acceptance. It contains an evidence register, runbooks, change/rollback summary, simulated RCA/PIR, and assessment rubric.

## Evidence limitations

- **Historical hands-on:** Cisco IOL routing and Check Point R82 SNAT / policy logs in a private-address lab.
- **Needs renewed acceptance:** Latest Check Point installed policy after diagnostic-rule cleanup, backup/restore, M11 alert notification chain, actual HTTP/HTTPS transaction.
- **Design only:** Juniper BGP dual ISP, PAN-OS HA/DMZ, F5 LTM, Arista MLAG/EVPN.
- **Simulation only:** INC-ABS-0042, timestamped 35-minute incident, packet captures, fictitious carrier fault.
- **Not accomplished:** Live customer production migration, HA/ISP failover, actual M12 business sign-off.

See also [M10 Multi-Vendor Operations](../../multi-vendor/m10-multi-vendor-operations/).

## Operational disposition

**Service acceptance: PENDING.** It would be incorrect to equate completion of this educational capstone with a production-ready, accepted multi-vendor network.

All addresses are laboratory or documentation values. No live customer identifiers or secrets belong in this public repository.
