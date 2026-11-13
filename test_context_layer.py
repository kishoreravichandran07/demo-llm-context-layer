"""Unit tests for the context layer demo. Run: python3 -m unittest test_context_layer.py -v"""

import json
import re
import unittest
from pathlib import Path

import context_layer as cl

HERE = Path(__file__).resolve().parent


class TestWorkRelevance(unittest.TestCase):
    def test_work_item_accepted(self):
        self.assertTrue(cl.is_work_relevant("Project Falcon: pilot pricing agreed"))

    def test_personal_item_rejected(self):
        self.assertFalse(cl.is_work_relevant("Sure - here is a packing list for the trail."))


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.known = ["Project Falcon", "Project Kestrel"]

    def test_known_project_passes(self):
        ok, unknown = cl.validate_against_db("Project Falcon: pricing agreed", self.known)
        self.assertTrue(ok)
        self.assertEqual(unknown, [])

    def test_unknown_project_quarantined(self):
        ok, unknown = cl.validate_against_db("Project Nimbus: slipped a week", self.known)
        self.assertFalse(ok)
        self.assertEqual(unknown, ["Project Nimbus"])

    def test_item_without_project_passes(self):
        ok, unknown = cl.validate_against_db("Security questionnaire sent", self.known)
        self.assertTrue(ok)


class TestShareSeparation(unittest.TestCase):
    """Quarantined and personal items must never reach a recipient digest."""

    def test_quarantine_not_shared(self):
        items = ["Project Nimbus: slipped", "Project Falcon: on track", "book club novel"]
        validated, quarantined = cl.shareable_items("alex", items, ["Project Falcon"])
        self.assertEqual([i for i, _ in validated], ["Project Falcon: on track"])
        self.assertEqual([i for i, _ in quarantined], ["Project Nimbus: slipped"])

    def test_access_list_controls_recipients(self):
        # alex shares with priya and sam; priya shares only with alex.
        self.assertIn("sam", cl.ACCESS_LIST["alex"])
        self.assertNotIn("sam", cl.ACCESS_LIST["priya"])
        self.assertIn("alex", cl.ACCESS_LIST["priya"])

    def test_end_to_end_quarantine_excluded(self):
        known = json.loads((cl.DATA / "project_db.json").read_text())["projects"]
        owner, items = cl.ingest_chat_export(cl.DATA / "llm_export_chat.json")
        validated, quarantined = cl.shareable_items(owner, items, known)
        shared_text = " ".join(i for i, _ in validated)
        self.assertNotIn("Nimbus", shared_text)
        self.assertTrue(any("Nimbus" in i for i, _ in quarantined))
        # personal message from the chat export must be filtered out
        self.assertNotIn("packing list", shared_text)


class TestNoSecrets(unittest.TestCase):
    """The shipped files must not contain secret-looking values."""

    PATTERNS = [r"api[_-]?key\s*[:=]", r"secret\s*[:=]", r"password\s*[:=]",
                r"-----BEGIN", r"ghp_[A-Za-z0-9]{20,}", r"sk-[A-Za-z0-9]{20,}"]

    def test_no_secret_looking_strings(self):
        for path in HERE.iterdir():
            if path.suffix not in {".py", ".json", ".md"} or path.name == "test_context_layer.py":
                continue  # the test file legitimately contains the patterns it scans for
            text = path.read_text()
            for pattern in self.PATTERNS:
                self.assertIsNone(re.search(pattern, text, re.IGNORECASE),
                                  f"{path.name} matches {pattern}")


if __name__ == "__main__":
    unittest.main()
