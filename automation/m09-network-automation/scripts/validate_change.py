from pathlib import Path
import ipaddress
import json
import sys
import yaml

CHANGE_FILE = Path("data/changes/CHG-M09-001.yml")
OUTPUT_FILE = Path("outputs/CHG-M09-001-plan.json")


def fail(message):
    print(f"[FAIL] {message}")
    sys.exit(1)


# Read change intent
with CHANGE_FILE.open(encoding="utf-8") as f:
    change = yaml.safe_load(f)["change"]

prefix_text = change["objective"]["advertise_prefix"]
devices = change["targets"]["devices"]
upstreams = change["targets"]["upstreams"]

# Validate prefix
try:
    prefix = ipaddress.ip_network(prefix_text, strict=True)
except ValueError as error:
    fail(f"Invalid prefix: {error}")

# Lab policy: Internet advertisements must not be longer than /24
if prefix.version != 4:
    fail("This workflow currently supports IPv4 only.")

if prefix.prefixlen > 24:
    fail(f"{prefix} violates the lab advertisement policy (maximum /24).")

# Validate targets
if not devices:
    fail("No target devices defined.")

if not upstreams:
    fail("No upstreams defined.")

# Produce machine-readable change plan
plan = {
    "change_id": change["id"],
    "prefix": str(prefix),
    "devices": devices,
    "upstreams": upstreams,
    "validation": "PASS"
}

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(plan, f, indent=2)

print(f"[PASS] Change: {change['id']}")
print(f"[PASS] Prefix: {prefix}")
print(f"[PASS] Devices: {', '.join(devices)}")
print(f"[PASS] Upstreams: {', '.join(upstreams)}")
print(f"[PASS] Plan: {OUTPUT_FILE}")