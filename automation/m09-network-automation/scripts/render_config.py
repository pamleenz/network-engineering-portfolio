import ipaddress
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


with open("data/changes/CHG-M09-001.yml") as f:
    change = yaml.safe_load(f)["change"]

with open("data/devices.yml") as f:
    devices = yaml.safe_load(f)["devices"]

prefix = ipaddress.ip_network(
    change["objective"]["advertise_prefix"]
)

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("cisco_bgp_advertisement.j2")

for device_name in change["targets"]["devices"]:
    device = devices[device_name]

    config = template.render(
        local_as=device["local_as"],
        prefix=prefix.network_address,
        netmask=prefix.netmask,
        peer_ip=device["peer_ip"],
        remote_as=device["remote_as"]
    )

    output = Path(f"outputs/{device_name}-candidate.cfg")
    output.write_text(config + "\n")

    print(f"[GENERATED] {output}")