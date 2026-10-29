"""Exercise opt-in design initialization without inventing ready design outputs."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("design_init", ROOT / "scripts/init_delivery.py")
initializer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(initializer)


class DesignInitializationTests(unittest.TestCase):
    def test_profile_cli_creates_an_explicitly_unready_draft(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "task"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/init_delivery.py"),
                                     str(destination), "--id", "T-1", "--summary", "Design current scope",
                                     "--design-profile", "detailed"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            record = json.loads((destination / "delivery-record.json").read_text())
            self.assertEqual(record["task"]["status"], "in_progress")
            bundle = record["design_views"]
            self.assertEqual(bundle["profile"], "detailed")
            self.assertEqual(bundle["state_model"]["requirement"], "unresolved")
            self.assertFalse(bundle["views"])
            self.assertEqual(bundle["consistency_review"]["status"], "not_run")
            self.assertTrue(bundle["consistency_review"]["unresolved_issues"])

    def test_legacy_initialization_does_not_silently_choose_a_design_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "task"
            initializer.initialize(destination, "T-1", "Bounded correction", "implement")
            record = json.loads((destination / "delivery-record.json").read_text())
            self.assertNotIn("design_views", record)

    def test_invalid_profile_does_not_create_a_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "task"
            with self.assertRaises(ValueError):
                initializer.initialize(destination, "T-1", "Current scope", "implement",
                                       design_profile="unknown")
            self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
