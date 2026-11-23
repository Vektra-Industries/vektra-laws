"""Tests for the vektra-laws command and the setup wizard."""
import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from vektra_laws_core import cli, wizard  # noqa: E402


class WizardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = os.environ.get("VEKTRA_LAWS_HOME")
        os.environ["VEKTRA_LAWS_HOME"] = str(Path(self.tmp.name) / "home")
        self.proj = Path(self.tmp.name) / "proj"

    def tearDown(self):
        if self.old is None:
            os.environ.pop("VEKTRA_LAWS_HOME", None)
        else:
            os.environ["VEKTRA_LAWS_HOME"] = self.old
        self.tmp.cleanup()

    def run_cli(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = cli.main(list(argv))
        return rc, buf.getvalue()

    def test_setup_yes_writes_policy_and_passes_self_check(self):
        rc, out = self.run_cli("setup", "--yes", "--project", str(self.proj), "--kind", "all",
                               "--assigned", "ana")
        self.assertEqual(rc, 0, out)
        policy = (self.proj / "vektra-laws" / "creator-policy.yaml").read_text()
        self.assertIn("ana", policy)
        self.assertIn("override_estop", policy)
        self.assertNotIn("FAIL", out)
        key = next((Path(os.environ["VEKTRA_LAWS_HOME"]) / "keys").iterdir())
        if os.name == "posix":
            self.assertEqual(key.stat().st_mode & 0o777, 0o600)

    def test_setup_refuses_to_overwrite_without_force(self):
        self.run_cli("setup", "--yes", "--project", str(self.proj), "--assigned", "ana")
        rc, _ = self.run_cli("setup", "--yes", "--project", str(self.proj), "--assigned", "ana")
        self.assertEqual(rc, 1)

    def test_setup_needs_someone_in_command(self):
        rc, _ = self.run_cli("setup", "--yes", "--project", str(self.proj), "--assigned", "")
        self.assertEqual(rc, 2)

    def test_parse_tools_rejects_bad_levels(self):
        self.assertEqual(wizard.parse_tools("a=0, b=4"), {"a": 0, "b": 4})
        with self.assertRaises(ValueError):
            wizard.parse_tools("a=9")

    def test_check_outcomes_and_exit_codes(self):
        self.assertEqual(self.run_cli("check", "read", "--level", "0")[0], 0)
        self.assertEqual(self.run_cli("check", "send", "--level", "3")[0], 3)
        self.assertEqual(self.run_cli("check", "x", "--level", "0", "--effect", "harm_person")[0], 4)

    def test_verify(self):
        self.assertEqual(self.run_cli("verify")[0], 0)


if __name__ == "__main__":
    unittest.main()
