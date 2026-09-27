# Change / Verification / Rollback Notes

## Change 1 — Guest mode

**Change**
- Start `hostapd.guest.conf` on CORP-AP.
- Change SW1 AP-facing trunk native VLAN from 10 to 40.
- Keep tagged VLAN 99 for AP management/RADIUS.
- Apply `GUEST-IN` inbound on `Vlan40`.

**Verification**
- Client joins `GUEST-WIFI` with `key_mgmt=NONE`.
- Client reaches `10.10.40.1`.
- Client cannot reach VLANs 10, 20, 30, or 99.
- ACL deny counters increment.

**Rollback**
- Restart corporate hostapd configuration.
- Restore trunk native VLAN 10.
- Restore EAP-TLS supplicant configuration and corporate IP.

## Change 2 — RADIUS service failure test

**Fault injection**
```bash
sudo systemctl stop freeradius
```

**Observed**
- AP could still ping `10.10.99.20`.
- UDP/1812 and UDP/1813 were not listening.
- 802.1X authentication timed out.

**Recovery**
```bash
sudo systemctl start freeradius
```

**Verification**
- EAP-TLS returned to `SUCCESS`.
- Controlled port returned to `Authorized`.

## Change 3 — Untrusted EAP-TLS certificate

**Fault injection**
- Replace valid corporate client certificate with a self-signed `rogue-client` certificate.

**Observed**
- FreeRADIUS parsed `Subject=/CN=rogue-client` and `Issuer=/CN=rogue-client`.
- OpenSSL reported `self-signed certificate`, `unknown_ca`, and certificate verification failure.
- RADIUS sent `Access-Reject`.

**Rollback**
- Restore the known-good EAP-TLS supplicant configuration and certificate.

## Change 4 — Data-plane failure after successful authentication

**Fault injection**
```cisco
interface Ethernet0/0
 switchport trunk allowed vlan remove 10
```

**Observed**
- EAP-TLS: SUCCESS.
- Controlled port: Authorized.
- Corporate gateway `10.10.10.1`: unreachable.
- VLAN 99 remained allowed, so AAA remained healthy.

**Root cause**
Corporate VLAN 10 was removed from the AP-facing trunk allowed list. A native VLAN is still subject to the allowed-VLAN list.

**Rollback**
```cisco
interface Ethernet0/0
 switchport trunk allowed vlan add 10
```

**Verification**
- VLAN 10 appears in `show interfaces trunk`.
- Client successfully pings `10.10.10.1`.
