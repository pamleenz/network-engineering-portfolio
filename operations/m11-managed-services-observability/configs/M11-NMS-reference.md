# M11-NMS Reference

## Interfaces

```text
ens33 - NAT / DHCP / Internet access
ens34 - 10.99.0.20/24 / VMnet2 management segment
```

Persistent management route:

```yaml
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: true
    ens34:
      addresses:
        - "10.99.0.20/24"
      routes:
        - to: 10.255.11.1/32
          via: 10.99.0.101
```

## LibreNMS Docker services used

```text
db
msmtpd
redis
librenms
dispatcher
snmptrapd
syslogng
```

## LibreNMS configuration used

```bash
docker compose exec librenms lnms config:set enable_syslog true
docker compose exec librenms lnms config:set snmptraps.eventlog unhandled
```

## SNMP trap receiver

The receiver listens on UDP/162. SNMPv3 receiver credentials and engine ID must match the sending device. Secrets are excluded from Git.

## Syslog

syslog-ng listens on UDP/TCP 514 and feeds LibreNMS.

## NTP

chrony synchronizes against upstream NTP and serves the management subnet. Relevant policy:

```text
allow 10.99.0.0/24
```

## NetFlow

A dedicated nfcapd instance was used for the lab:

```text
bind: 10.99.0.20
port: 2055/UDP
flow directory: /var/tmp/m11-netflow
rotation: 60 seconds
```

Example inspection:

```bash
nfdump -R /var/tmp/m11-netflow -o long
```

## Security

Do not commit SNMP auth/privacy secrets, passwords, API tokens or reusable credentials.
