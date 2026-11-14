import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tempfile
from openplotterSettings.conf import Conf


class PercentSettingsTest(unittest.TestCase):
    def test_literal_values_round_trip(self):
        with tempfile.TemporaryDirectory() as temp:
            with (
                mock.patch.dict("os.environ", {"USER": "boat"}),
                mock.patch("os.path.exists", return_value=True),
                mock.patch.object(Conf, "read"),
            ):
                config = Conf()
            config.conf_file = str(Path(temp) / "openplotter.conf")
            for value in ("50%", "100% ready", "%(missing)s", "plain"):
                with self.subTest(value=value):
                    config.set("TEST", "label", value)
                    self.assertEqual(config.get("TEST", "label"), value)


if __name__ == "__main__":
    unittest.main()
