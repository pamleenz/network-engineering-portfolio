# Managed Services Incident — RCA / C-V-R

## Symptoms

- Wellington ERP intermittent
- Teams quality poor
- General web browsing normal
- Carrier reports circuit up

## Fault-domain conclusion

Physical and routing adjacencies remained up. Service-quality probes on the MPLS path showed loss/jitter under load. The alternate encrypted DIA path was healthy.

## Carrier RCA (scenario)

A lower-than-contracted policer profile was mistakenly applied to the Wellington 100 Mbps service after provider maintenance. The port, BGP, and BFD stayed up, but burst traffic was dropped.

## Temporary change

Steer affected corporate traffic to the secure DIA overlay while the carrier remediates MPLS.

## Verification

- Backup tunnel and routes healthy
- Return path verified
- ERP transactions normal
- Teams quality/SLA normal
- No unexpected Internet breakout impact

## Rollback

After carrier fix and stable observation window, restore MPLS preference and re-run routing, SLA, application, and log checks.
