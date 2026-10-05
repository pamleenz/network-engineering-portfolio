# Change - Verification - Rollback

## Pre-change

- Record tunnel status, BGP neighbors, received/advertised prefixes and routing tables.
- Confirm maintenance window, scope, dependencies and rollback trigger.
- Capture relevant cloud Effective Routes / route tables and security policy state.

## Change

- Change one control variable at a time.
- Prefer order: underlay/tunnel -> routing -> security policy -> application.
- Apply explicit prefix filters; avoid accidental route leaks.

## Verification

- IKE / IPsec SA established.
- BGP Established and message counters moving.
- Required prefixes received and advertised.
- Routes selected/installed in RIB/FIB and cloud route table.
- Security policies allow intended traffic.
- NAT behavior is intentional.
- Forward and return path are valid.
- End-to-end test succeeds in both directions.

## Rollback

- Restore route policy / routes / security policy first if they caused the incident.
- Remove or restore BGP changes.
- Remove tunnel changes last.
- Re-run the verification checklist after each rollback stage.
