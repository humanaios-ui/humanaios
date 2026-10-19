import unittest
import os
from types import SimpleNamespace
from unittest.mock import patch

from scripts.document_intelligence_census import classify, inventory, parse_tree


class CensusTests(unittest.TestCase):
    def test_parse_tree_preserves_newline_and_non_ascii_paths(self):
        records = (
            b"100644 blob " + b"a" * 40 + b"\tline\nbreak-\xc3\xa9.md\0"
        )

        self.assertEqual(
            parse_tree(records),
            [
                {
                    "path": "line\nbreak-é.md",
                    "mode": "100644",
                    "object_type": "blob",
                    "object_id": "a" * 40,
                }
            ],
        )

    def test_classify_keeps_every_path_pending_until_review(self):
        item = classify(
            {
                "path": "docs/guide.md",
                "mode": "100644",
                "object_type": "blob",
                "object_id": "b" * 40,
            }
        )

        self.assertEqual(item["source_kind"], "text-or-source-candidate")
        self.assertEqual(item["review_state"], "pending")
        self.assertEqual(item["controlling_doc_id"], "PENDING")
        self.assertEqual(item["owner"], "PENDING")

    def test_special_files_are_excluded_with_reason(self):
        generated = classify(
            {
                "path": "tests/__pycache__/audit.pyc",
                "mode": "100644",
                "object_type": "blob",
                "object_id": "c" * 40,
            }
        )
        private_candidate = classify(
            {
                "path": ".empirica_reflex_logs/event.jsonl",
                "mode": "100644",
                "object_type": "blob",
                "object_id": "d" * 40,
            }
        )

        self.assertEqual(generated["source_kind"], "generated")
        self.assertIn("compiled artifact", generated["disposition"])
        self.assertEqual(private_candidate["sensitivity"], "candidate")
        self.assertEqual(private_candidate["review_state"], "pending")

    def test_submodule_is_not_misreported_as_reviewed(self):
        item = classify(
            {
                "path": "vendor/example",
                "mode": "160000",
                "object_type": "commit",
                "object_id": "e" * 40,
            }
        )

        self.assertEqual(item["source_kind"], "submodule")
        self.assertEqual(item["review_state"], "metadata-only")
        self.assertIn("not enumerated", item["disposition"])

    def test_explicit_commit_sha_and_hook_environment_isolation(self):
        commit = "a" * 40
        tree = b"100644 blob " + b"b" * 40 + b"\tdocs/guide.md\0"
        with patch.dict(os.environ, {"GIT_DIR": "/tmp/wrong-repo", "GIT_WORK_TREE": "/tmp/wrong-worktree"}):
            with patch("scripts.document_intelligence_census.subprocess.run", side_effect=[
                SimpleNamespace(stdout=commit + "\n"),
                SimpleNamespace(stdout=tree),
            ]) as run:
                result = inventory(commit)
        self.assertEqual(result["tracked_path_count"], 1)
        self.assertTrue(result["items"][0]["object_access"].startswith("git-blob-unverified"))
        for call in run.call_args_list:
            self.assertNotIn("GIT_DIR", call.kwargs["env"])
            self.assertNotIn("GIT_WORK_TREE", call.kwargs["env"])
            self.assertEqual(call.kwargs["timeout"], 120)

    def test_moving_refs_rejected(self):
        with self.assertRaisesRegex(ValueError, "40-character"):
            inventory("main")

    def test_pinned_tree_accounts_for_every_path(self):
        result = inventory("ebe164d2d2170c154a7710d97c4590dbddf31f70")
        paths = [item["path"] for item in result["items"]]

        self.assertEqual(result["tracked_path_count"], 976)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(result["counts_by_review_state"], {
            "metadata-only": 48,
            "pending": 928,
        })
        self.assertTrue(
            all(
                item["object_id"]
                and item["object_type"]
                and item["object_access"].startswith("git-blob-unverified")
                and item["controlling_doc_id"] == "PENDING"
                and item["owner"] == "PENDING"
                for item in result["items"]
            )
        )


if __name__ == "__main__":
    unittest.main()
