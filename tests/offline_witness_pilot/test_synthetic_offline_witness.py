"""Subprocess observer is separate process, not independent human auditor."""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name("synthetic_offline_witness.py")

class IsolatedWitnessTest(unittest.TestCase):
    def test_denied_then_commit_crash_then_idempotent_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = pathlib.Path(tmp) / "sink with # and ? spaces"
            folder.mkdir()
            db = str(folder / "sink.sqlite3")
            def cmd(op, *args):
                return subprocess.run([sys.executable, str(SCRIPT), op, db, *args],
                    capture_output=True, text=True, timeout=45)
            self.assertEqual(cmd("init").returncode, 0)
            self.assertEqual(cmd("act").returncode, 3)
            pre = json.loads(cmd("witness").stdout)
            self.assertEqual(pre["committed_effects"], 0)
            self.assertEqual(cmd("approve").returncode, 0)
            self.assertEqual(cmd("act", "--crash-after-commit").returncode, 23)
            after = json.loads(cmd("witness").stdout)
            self.assertEqual(after["committed_effects"], 1)
            self.assertEqual(cmd("act").returncode, 0)
            retry = json.loads(cmd("witness").stdout)
            self.assertEqual(retry["committed_effects"], 1)
            self.assertEqual(after["sink_sha256"], retry["sink_sha256"])
            self.assertFalse(retry["independent_attestation"])
            self.assertEqual(retry["authority_effect"], "NONE")

if __name__ == "__main__":
    unittest.main()
