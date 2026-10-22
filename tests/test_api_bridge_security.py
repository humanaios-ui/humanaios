"""No-network synthetic security regression. No real database/credentials required."""
import importlib.util
import os
import pathlib
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "offline-integration" / "automation" / "api_bridge_db.py"
spec = importlib.util.spec_from_file_location("bridge_under_test", SOURCE)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)

SCOPE = {
    "BRIDGE_READ_TOKEN": "r" * 40,
    "BRIDGE_WRITE_TOKEN": "w" * 40,
    "BRIDGE_HARNESS_TOKEN": "h" * 40,
}

class FakeBridge:
    def __init__(self, db_url=None, org_id=None):
        pass
    def sync_state(self):
        return {"state": "synthetic"}
    def process_registry_submission(self, record):
        raise RuntimeError("DURABLE_STORE_UNAVAILABLE")
    def set_harness_mode(self, mode):
        raise RuntimeError("DURABLE_STORE_UNAVAILABLE")

class BridgeSecurityTests(unittest.TestCase):
    def make_client(self):
        ctx = patch.dict(os.environ, SCOPE)
        ctx.start()
        self.addCleanup(ctx.stop)
        mocked = patch.object(bridge, "APIBridge", FakeBridge)
        mocked.start()
        self.addCleanup(mocked.stop)
        return bridge.create_app().test_client()

    def test_missing_scoped_secrets_cannot_start(self):
        with patch.dict(os.environ, {k: "" for k in SCOPE}):
            with self.assertRaisesRegex(RuntimeError, "SCOPE_TOKENS"):
                bridge.create_app()

    def test_same_token_for_scopes_rejected(self):
        with patch.dict(os.environ, {k: "x" * 40 for k in SCOPE}):
            with self.assertRaisesRegex(RuntimeError, "SCOPE_TOKENS"):
                bridge.create_app()

    def test_missing_bearer_is_denied(self):
        client = self.make_client()
        for method, url in (("get", "/state/sync"),
                            ("post", "/harness/set"),
                            ("post", "/gate/registry")):
            self.assertEqual(getattr(client, method)(url).status_code, 401)

    def test_read_token_cannot_write(self):
        client = self.make_client()
        headers = {"Authorization": "Bearer " + SCOPE["BRIDGE_READ_TOKEN"]}
        self.assertEqual(client.post("/harness/set", json={"mode": "balanced"},
                                     headers=headers).status_code, 401)
        self.assertEqual(client.post("/gate/registry", json={"title": "synthetic"},
                                     headers=headers).status_code, 401)
        self.assertEqual(client.get("/state/sync", headers=headers).status_code, 200)

    def test_write_failure_returns_503_without_false_ack(self):
        client = self.make_client()
        cases = [("/gate/registry", "BRIDGE_WRITE_TOKEN", {"title": "synthetic"}),
                 ("/harness/set", "BRIDGE_HARNESS_TOKEN", {"mode": "balanced"})]
        for path, scope, record in cases:
            result = client.post(path, json=record,
                         headers={"Authorization": "Bearer " + SCOPE[scope]})
            self.assertEqual(result.status_code, 503)
            self.assertNotIn("durable", result.get_json())

    def test_bad_request_is_rejected(self):
        client = self.make_client()
        result = client.post("/gate/registry", data='[1,2]', content_type="application/json",
                             headers={"Authorization": "Bearer " + SCOPE["BRIDGE_WRITE_TOKEN"]})
        self.assertEqual(result.status_code, 400)

    def test_unicode_bearer_does_not_crash_server(self):
        client = self.make_client()
        response = client.get("/state/sync", headers={"Authorization": "Bearer " + chr(233) * 40})
        self.assertEqual(response.status_code, 401)

    def test_failed_query_rolls_back_transaction(self):
        class Session:
            rolled_back = False
            def query(self, *args):
                raise RuntimeError("synthetic read failure")
            def rollback(self):
                self.rolled_back = True
        raw = bridge.APIBridge.__new__(bridge.APIBridge)
        session = Session()
        raw.db_session = session
        raw.org_id = "00000000-0000-0000-0000-000000000001"
        with self.assertRaisesRegex(RuntimeError, "DURABLE_STORE_UNAVAILABLE"):
            raw.sync_state()
        self.assertTrue(session.rolled_back)

    def test_default_api_bridge_will_not_ack_ram(self):
        raw = bridge.APIBridge.__new__(bridge.APIBridge)
        raw.db_session = None
        raw.fallback = False
        raw.org_id = "00000000-0000-0000-0000-000000000001"
        with patch.object(bridge, "registry_gate", return_value=("CANDIDATE", "synthetic")):
            with self.assertRaisesRegex(RuntimeError, "DURABLE_STORE_UNAVAILABLE"):
                raw.process_registry_submission({"title": "synthetic"})
        with self.assertRaisesRegex(RuntimeError, "DURABLE_STORE_UNAVAILABLE"):
            raw.set_harness_mode("balanced")
        with self.assertRaisesRegex(RuntimeError, "DURABLE_STORE_UNAVAILABLE"):
            raw.sync_state()

if __name__ == "__main__":
    unittest.main()
