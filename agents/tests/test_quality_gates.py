"""Regresiones de la auditoría; no sustituyen ni simulan inferencias LLM."""
import copy
import unittest

from agents.quality_gates import validate_checks, review_context, human_review_gate


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = {"sha256": "abc", "branch": "audit", "files": {"a.py": "123"}}
        self.record = {"version": "1.1.0", "finished_at": "2026-11-14T00:00:00+00:00",
                       "snapshot": self.snapshot, "checks": []}
        commands = {
            "agents": ["python.exe", "-B", "-m", "unittest", "discover", "-s", "agents/tests", "-v"],
            "backend": ["python.exe", "-B", "-m", "unittest", "discover", "-s", "backend/tests", "-v"],
            "backend_compile": ["python.exe", "-m", "compileall", "app"],
            "frontend_build": ["npm.cmd", "run", "build"],
        }
        for name, command in commands.items():
            self.record["checks"].append({"check": name, "command": command,
                "cwd": "backend" if name == "backend_compile" else "frontend" if name == "frontend_build" else ".",
                "exit_code": 0, "stdout": "observed", "stderr": "Ran 1 test in 0.001s\n\nOK\n"})

    def test_complete_checks_accepted(self):
        validate_checks(self.record, self.snapshot)

    def test_empty_partial_duplicate_unknown_checks_rejected(self):
        cases = [[], self.record["checks"][:1], self.record["checks"] + [self.record["checks"][0]]]
        unknown = copy.deepcopy(self.record["checks"])
        unknown[0]["check"] = "unknown"
        cases.append(unknown)
        for checks in cases:
            record = copy.deepcopy(self.record)
            record["checks"] = checks
            with self.subTest(checks=len(checks)), self.assertRaises(ValueError):
                validate_checks(record, self.snapshot)

    def test_failed_or_incomplete_record_rejected(self):
        for key, value in (("exit_code", 1), ("exit_code", False), ("stdout", None),
                           ("command", ["echo", "OK"]), ("cwd", "elsewhere")):
            record = copy.deepcopy(self.record)
            record["checks"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_checks(record, self.snapshot)

    def test_stale_or_inconsistent_snapshot_rejected(self):
        for key, value in (("sha256", "other"), ("files", {})):
            record = copy.deepcopy(self.record)
            record["snapshot"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_checks(record, self.snapshot)

    def test_git_metadata_does_not_invalidate_identical_content(self):
        record = copy.deepcopy(self.record)
        record["snapshot"].update(branch="review-branch", git_head="another-commit")
        validate_checks(record, self.snapshot)

    def test_empty_zero_and_failed_suite_summaries_rejected(self):
        for name in ("agents", "backend"):
            for output in ("", "Ran 0 tests in 0.000s\nOK", "Ran 2 tests in 0.001s\nFAILED (failures=1)"):
                record = copy.deepcopy(self.record)
                entry = next(c for c in record["checks"] if c["check"] == name)
                entry.update(stdout="", stderr=output)
                with self.subTest(name=name, output=output), self.assertRaises(ValueError):
                    validate_checks(record, self.snapshot)

    def test_findings_cannot_be_automatically_accepted(self):
        self.assertEqual(human_review_gate([{"status": "blocked"}]), "blocked")
        self.assertEqual(human_review_gate([{"status": "inspected", "findings": ["review me"]}]),
                         "awaiting_human_findings_review")
        self.assertEqual(human_review_gate([]), "awaiting_human_review")

    def test_timestamp_and_version_required(self):
        for key, value in (("finished_at", "invalid"), ("finished_at", "2026-11-14"), ("version", "unknown")):
            record = copy.deepcopy(self.record)
            record[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_checks(record, self.snapshot)

    def test_both_reviewers_receive_reports_checks_and_mcp(self):
        ledger = [{"role": role, "content_equal": True, "outside_scope_denied": True}
                  for role in ("frontend", "backend")]
        for role in ("calidad", "seguridad"):
            context = review_context(role, [{"agent": "frontend"}], self.record["checks"], ledger)
            self.assertEqual(context["mcp_verifications"], ledger)
            self.assertTrue(context["prior_reports"])
            self.assertEqual(len(context["checks"]), 4)

    def test_incomplete_or_failed_mcp_ledger_rejected(self):
        for ledger in ([], [{"role": "frontend", "content_equal": True, "outside_scope_denied": True}],
                       [{"role": r, "content_equal": False, "outside_scope_denied": True} for r in ("frontend", "backend")]):
            with self.subTest(ledger=ledger), self.assertRaises(ValueError):
                review_context("calidad", [], [], ledger)
