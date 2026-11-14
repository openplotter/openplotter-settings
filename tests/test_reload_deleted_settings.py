import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tempfile
import configparser
from openplotterSettings.conf import Conf


class ReloadSettingsTest(unittest.TestCase):
    def test_removed_option_is_not_resurrected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "openplotter.conf"
            path.write_text("[TEST]\nremoved = old\nkeep = first\n")
            config = Conf.__new__(Conf)
            config.conf_file = str(path)
            config.data_conf = configparser.ConfigParser()
            config.read()
            path.write_text("[TEST]\nkeep = second\n")
            self.assertEqual(config.get("TEST", "removed"), "")
            self.assertEqual(config.get("TEST", "keep"), "second")
            self.assertNotIn("old", path.read_text())

    def test_removed_section_stays_removed_on_write(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "openplotter.conf"
            path.write_text("[OLD]\nkey = old\n[TEST]\nkeep = first\n")
            config = Conf.__new__(Conf)
            config.conf_file = str(path)
            config.data_conf = configparser.ConfigParser()
            config.read()
            path.write_text("[TEST]\nkeep = second\n")
            config.set("TEST", "new", "value")
            self.assertNotIn("[OLD]", path.read_text())


if __name__ == "__main__":
    unittest.main()
