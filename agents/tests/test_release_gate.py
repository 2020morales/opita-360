"""Fixtures de registros: no simulan navegador ni inferencias LLM."""
import copy
import unittest
from unittest.mock import patch
from agents.release_gate import validate_release, REQUIRED_BROWSER


class ReleaseGateTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {"sha256": "source", "files": {"a": "hash"}}
        self.browser = {"timestamp": "2026-11-19T00:00:00+00:00", "browser": "Chrome",
                        "snapshot": self.snapshot, "checks": [
                            {"name": n, "passed": True, "observed": "fixture"} for n in sorted(REQUIRED_BROWSER)]}

    def test_success_keeps_human_approval_pending(self):
        with patch("agents.release_gate.validate_checks"):
            result = validate_release({}, self.browser, self.snapshot)
        self.assertEqual(result["human_approval"], "pending")
        self.assertFalse(result["publication_allowed"])

    def test_bad_browser_blocks(self):
        for mutate in (lambda b: b.update(fatal_error="CDP error"),
                       lambda b: b.update(checks=[]),
                       lambda b: b["checks"][0].update(passed=False),
                       lambda b: b["checks"][0].update(passed=1),
                       lambda b: b.update(snapshot={"sha256": "other", "files": {}}),
                       lambda b: b["checks"].append(b["checks"][0]),
                       lambda b: b.update(timestamp="2026-11-19")):
            record = copy.deepcopy(self.browser)
            mutate(record)
            with self.subTest(record=record), patch("agents.release_gate.validate_checks"), self.assertRaises(ValueError):
                validate_release({}, record, self.snapshot)

    def test_failed_checks_cannot_be_bypassed(self):
        with self.assertRaises(ValueError):
            validate_release({}, self.browser, self.snapshot)
