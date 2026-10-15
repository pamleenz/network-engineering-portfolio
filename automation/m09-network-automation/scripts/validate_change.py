"""Offline checks for CHG-M09-001 intent. Does not test a live BGP neighbor."""
from pathlib import Path
import ipaddress
import json
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
CHANGE_FILE = ROOT / "data/changes/CHG-M09-001.yml"
DEVICE_FILE = ROOT / "data/devices.yml"
OUTPUT_FILE = ROOT / "outputs/CHG-M09-001-plan.json"


def validate(change_data, device_data):
    change = change_data["change"]
    raw_prefix = change["objective"]["advertise_prefix"]
    try:
        prefix = ipaddress.ip_network(raw_prefix, strict=True)
    except (ValueError, TypeError) as error:
        raise ValueError(f"Invalid prefix: {error}") from error

    if prefix.version != 4 or prefix.prefixlen == 0 or prefix.prefixlen > 24:
        raise ValueError("Only a specific IPv4 prefix with length /1 to /24 is supported")
    if prefix.is_multicast or prefix.is_loopback or prefix.is_link_local or prefix.is_unspecified:
        raise ValueError(f"Unsafe advertisement range: {prefix}")

    targets = change["targets"]
    devices = targets["devices"]
    upstreams = targets["upstreams"]
    if not devices or not upstreams:
        raise ValueError("Devices and upstreams must both be non-empty")
    if len(devices) != len(set(devices)) or len(upstreams) != len(set(upstreams)):
        raise ValueError("Duplicated devices or upstreams are not permitted")
    defined = device_data["devices"]
    for name in devices:
        if name not in defined:
            raise ValueError(f"Device not present in inventory definition: {name}")
        required = ("local_as", "peer_ip", "remote_as")
        if any(key not in defined[name] for key in required):
            raise ValueError(f"Incomplete peer definition for: {name}")
        try:
            peer_ip = ipaddress.ip_address(defined[name]["peer_ip"])
        except ValueError as error:
            raise ValueError(f"Invalid BGP peer IP for {name}: {error}") from error
        if peer_ip.version != 4:
            raise ValueError(f"IPv4 only: {name}")

    if not change.get("id"):
        raise ValueError("Missing change ID")

    return {
        "change_id": change["id"],
        "prefix": str(prefix),
        "devices": devices,
        "upstreams": upstreams,
        "validation": "PASS",
        "scope": "offline intent validation only; no device or route check",
    }


def main():
    with CHANGE_FILE.open(encoding="utf-8") as f:
        change_data = yaml.safe_load(f)
    with DEVICE_FILE.open(encoding="utf-8") as f:
        device_data = yaml.safe_load(f)
    try:
        plan = validate(change_data, device_data)
    except (ValueError, KeyError, TypeError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        return 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2)
    print(f"[PASS] Intent checked: {plan['change_id']} {plan['prefix']}")
    print(f"[PASS] Targets: {', '.join(plan['devices'])}")
    print("[INFO] Offline check only; verify actual BGP neighbors and forwarding separately")
    return 0


if __name__ == "__main__":
    sys.exit(main())
