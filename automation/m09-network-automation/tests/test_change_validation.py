"""Offline unit tests: no network gear, credentials or NetBox access required."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_change.py"
spec = importlib.util.spec_from_file_location("validate_change", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def good():
    return (
        {"change": {"id": "CHG-M09-001", "objective": {"advertise_prefix": "203.0.113.0/24"},
                    "targets": {"devices": ["CE-AKL-01"], "upstreams": ["ISP1"]}}},
        {"devices": {"CE-AKL-01": {"local_as": 65010, "peer_ip": "192.0.2.1", "remote_as": 65001}}},
    )


class ChangeValidationTests(unittest.TestCase):
    def test_valid_documentation_prefix(self):
        change, devices = good()
        self.assertEqual(mod.validate(change, devices)["prefix"], "203.0.113.0/24")

    def test_reject_default_advertisement(self):
        change, devices = good()
        change["change"]["objective"]["advertise_prefix"] = "0.0.0.0/0"
        with self.assertRaises(ValueError):
            mod.validate(change, devices)

    def test_reject_more_specific_than_24(self):
        change, devices = good()
        change["change"]["objective"]["advertise_prefix"] = "203.0.113.0/25"
        with self.assertRaises(ValueError):
            mod.validate(change, devices)

    def test_reject_unrecognized_device(self):
        change, devices = good()
        change["change"]["targets"]["devices"] = ["UNKNOWN-ROUTER"]
        with self.assertRaises(ValueError):
            mod.validate(change, devices)

    def test_reject_duplicate_target(self):
        change, devices = good()
        change["change"]["targets"]["devices"] = ["CE-AKL-01", "CE-AKL-01"]
        with self.assertRaises(ValueError):
            mod.validate(change, devices)

    def test_reject_multicast_advertisement(self):
        change, devices = good()
        change["change"]["objective"]["advertise_prefix"] = "224.0.0.0/4"
        with self.assertRaises(ValueError):
            mod.validate(change, devices)


if __name__ == "__main__":
    unittest.main()
