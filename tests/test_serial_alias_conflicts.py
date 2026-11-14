import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def load_module(relative, stubs=None, name="tested_module"):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, stubs or {}):
        spec.loader.exec_module(module)
    return module


class SerialAliasConflictTest(unittest.TestCase):
    def setUp(self):
        dummy = types.ModuleType("openplotterSettings.appsList")
        dummy.AppsList = mock.Mock()
        with mock.patch.dict(sys.modules, {"openplotterSettings.appsList": dummy}):
            self.module = load_module(
                "openplotterSettings/serialPorts.py",
                name="openplotterSettings.test_serial_ports",
            )
        self.module._ = lambda text: text
        self.ports = self.module.SerialPorts.__new__(self.module.SerialPorts)
        aliases = {
            "ttyOP_first": {"device": "ttyUSB0"},
            "ttyOP_second": {"device": "ttyUSB0"},
        }
        self.ports.conf = mock.Mock()
        self.ports.conf.get.return_value = repr(aliases)

    def test_reports_both_alias_connections(self):
        connections = [
            {"app": "Test", "id": "first", "device": "/dev/ttyOP_first"},
            {"app": "Test", "id": "second", "device": "/dev/ttyOP_second"},
        ]
        self.ports.getSerialUsedPorts = lambda: connections
        result = self.ports.conflicts()
        self.assertEqual(len(result), 2)
        self.assertTrue(any("first" in row for row in result))
        self.assertTrue(any("second" in row for row in result))

    def test_distinct_physical_devices_do_not_conflict(self):
        self.ports.getSerialUsedPorts = lambda: [
            {"app": "Test", "id": "first", "device": "/dev/ttyOP_first"},
            {"app": "Test", "id": "other", "device": "/dev/ttyUSB1"},
        ]
        self.assertFalse(self.ports.conflicts())


if __name__ == "__main__":
    unittest.main()
