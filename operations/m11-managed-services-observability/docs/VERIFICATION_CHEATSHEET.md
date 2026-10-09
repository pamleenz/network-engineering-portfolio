# M11 Verification Cheatsheet

## LibreNMS / Docker

```bash
cd /opt/librenms/docker-master/examples/compose

docker compose ps
docker compose logs --tail=100 snmptrapd
docker compose logs --tail=100 syslogng
docker compose exec librenms lnms config:get enable_syslog
docker compose exec librenms lnms config:get snmptraps.eventlog
```

## Linux management path

```bash
ip addr show ens34
ip route get 10.255.11.1
ping -c 4 10.255.11.1

sudo ss -lunp | grep ':162'
sudo ss -lunp | grep ':514'
sudo ss -lunp | grep ':2055'
sudo ss -lunp | grep ':123'
```

## SNMPv3

```bash
snmpget -v3 -l authPriv \
  -u librenms \
  -a SHA -A '<AUTH_SECRET>' \
  -x AES -X '<PRIV_SECRET>' \
  10.255.11.1 1.3.6.1.2.1.1.5.0

snmpwalk -v3 -l authPriv \
  -u librenms \
  -a SHA -A '<AUTH_SECRET>' \
  -x AES -X '<PRIV_SECRET>' \
  10.255.11.1 1.3.6.1.2.1.2.2.1.2

snmpwalk -v3 -l authPriv \
  -u librenms \
  -a SHA -A '<AUTH_SECRET>' \
  -x AES -X '<PRIV_SECRET>' \
  10.255.11.1 1.3.6.1.2.1.31.1.1.1.6
```

## Packet captures

```bash
sudo tcpdump -ni ens34 -tttt udp port 162
sudo tcpdump -ni ens34 -tttt -A udp port 514
sudo tcpdump -ni ens34 -tttt -vv udp port 123
sudo tcpdump -ni ens34 -tttt udp port 2055
```

## NetFlow collector

```bash
sudo ss -lunp | grep ':2055'
ls -lh /var/tmp/m11-netflow
nfdump -R /var/tmp/m11-netflow -o long
```

## Chrony

```bash
chronyc tracking
chronyc sources -v
sudo chronyc accheck 10.99.0.101
sudo chronyc clients
```

## Cisco - baseline

```text
show ip interface brief
show interfaces Ethernet0/0
show processes cpu
show processes memory
show clock detail
```

## Cisco - SNMP

```text
show snmp
show snmp user
show snmp host
show snmp engineID
show snmp mib ifmib traps
```

## Cisco - Syslog

```text
show logging
show running-config | include ^logging
```

## Cisco - NTP

```text
show ntp associations
show ntp associations detail
show ntp status
show clock detail
```

## Cisco - NetFlow

```text
show flow record
show flow exporter M11-EXPORTER
show flow monitor M11-MONITOR
show running-config | section flow
show running-config interface Ethernet0/0
```

## Operational interpretation

```text
Polling = What is the state?
Trap    = What changed just now?
Syslog  = What happened / why / severity?
NetFlow = Who is using the traffic?
NTP     = Can I trust the timeline?
Alert   = Is this condition actionable?
```
