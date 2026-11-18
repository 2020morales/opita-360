"""Pruebas del arnes; no simulan evidencias de inferencia ni funcionalidades turisticas."""
import asyncio
import copy
import unittest
from unittest.mock import patch
from harness import core
from harness.cli import redact
from harness.runtime import run

class HarnessTests(unittest.TestCase):
    def test_exactly_five_complete_draft_specs(self):
        specs = core.validate_structure()
        self.assertEqual(len(specs), 5)
        self.assertTrue(all(s["status"] == "draft" for s in specs))

    def test_compass_is_one_to_one_with_acceptance(self):
        s, _ = core.load_spec("002")
        cases = core.compass(s)
        self.assertEqual([c["acceptance_id"] for c in cases["cases"]], [c["id"] for c in s["acceptance"]])
        self.assertEqual(cases["execution"], "not_run")
        self.assertTrue(all(c["status"] == "not_implemented" for c in cases["cases"]))

    def test_compass_preserves_observable_assertions(self):
        s, _ = core.load_spec("002")
        self.assertEqual(core.compass(s)["cases"][0]["assert"], s["acceptance"][0]["then"])

    def test_compass_does_not_mutate_specification(self):
        s, _ = core.load_spec("001")
        before = copy.deepcopy(s)
        core.compass(s)
        self.assertEqual(s, before)

    def test_rejects_duplicate_or_incomplete_criteria(self):
        s, _ = core.load_spec("001")
        duplicate = copy.deepcopy(s); duplicate["acceptance"].append(duplicate["acceptance"][0])
        missing = copy.deepcopy(s); del missing["acceptance"][0]["then"]
        empty = copy.deepcopy(s); empty["acceptance"][0]["then"] = " "
        for invalid in (duplicate, missing, empty):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                core.compass(invalid)

    def test_amber_is_integer_from_one_to_nine(self):
        s, _ = core.load_spec("001")
        for value in (0, 10, True, "3"):
            invalid = copy.deepcopy(s); invalid["amber"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                core.validate_spec(invalid)

    def test_unknown_spec_and_traversal_rejected(self):
        for sid in ("../001", "999", ""):
            with self.subTest(sid=sid), self.assertRaises(ValueError):
                core.load_spec(sid)

    def test_forbidden_paths(self):
        for path in ("../README.md", "/etc/passwd", ".git/config", ".env", "frontend\\src\\main.jsx"):
            with self.subTest(path=path), self.assertRaises(PermissionError):
                core.safe_path(path)

    def test_tool_denial_by_default(self):
        for role, tool in (("unknown", "read_context"), ("frontend", "shell"),
                           ("backend", "write"), ("calidad", "delegate"), ("seguridad", "read_mcp")):
            with self.subTest(role=role, tool=tool), self.assertRaises(PermissionError):
                core.authorize(role, tool)

    def test_explicit_model_for_all_roles(self):
        m = core.manifest()
        self.assertEqual(set(m["agents"]), set(core.ROLES))
        self.assertEqual(m["model"]["name"], "qwen3.5:4b")
        self.assertTrue(all(not p["write"] and not p["shell"] for p in m["agents"].values()))

    def test_manifest_rejects_model_or_permission_expansion(self):
        original = core.manifest()
        for field in ("model", "permissions"):
            invalid = copy.deepcopy(original)
            if field == "model":
                invalid["model"]["provider"] = "remote"
            else:
                invalid["agents"]["frontend"]["write"] = True
            with patch("harness.core.json.loads", return_value=invalid), self.assertRaises(ValueError):
                core.manifest()

    def test_read_context_has_real_hashes(self):
        sources = core.context("frontend")
        self.assertTrue(sources)
        for s in sources:
            raw = (core.ROOT / s["path"]).read_bytes()
            self.assertEqual(s["sha256"], core.digest(raw))
            self.assertEqual(s["bytes"], len(raw))

    def test_approval_is_required_before_context_or_network(self):
        with patch("harness.runtime.load_spec") as load:
            with self.assertRaises(PermissionError):
                asyncio.run(run("001", approved=False))
            load.assert_not_called()

    def test_truthy_string_is_not_approval(self):
        with self.assertRaises(PermissionError):
            asyncio.run(run("001", approved="yes"))

    def test_inventory_is_not_inference(self):
        result = asyncio.run(run("001", approved=True))
        self.assertEqual(len(result["reports"]), 5)
        self.assertFalse(result["traces"])
        self.assertFalse(result["mcp"])
        self.assertFalse(result["code_modified"])
        self.assertTrue(all(r["model"] is None for r in result["reports"]))

    def test_report_rejects_fake_hash_missing_evidence_and_wrong_role(self):
        result = asyncio.run(run("001", approved=True))
        base = result["reports"][1]
        fake = copy.deepcopy(base); fake["evidence"][0]["sha256"] = "0" * 64
        empty = copy.deepcopy(base); empty["evidence"] = []
        role = copy.deepcopy(base); role["task"] = "review-backend"
        model = copy.deepcopy(base); model["model"] = "invented"
        for invalid in (fake, empty, role, model):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                core.validate_report(invalid)

    def test_reports_require_nonempty_findings_and_limitations(self):
        base = asyncio.run(run("001", approved=True))["reports"][0]
        for key in ("findings", "limitations"):
            invalid = copy.deepcopy(base); invalid[key] = []
            with self.assertRaises(ValueError):
                core.validate_report(invalid)

    def test_redaction_keeps_test_results(self):
        source = str(core.ROOT / "frontend") + " tests=9 exit_code=0"
        actual = redact(source)
        self.assertIn("<WORKTREE_T6>", actual)
        self.assertIn("tests=9 exit_code=0", actual)
        self.assertNotIn(str(core.ROOT), actual)

    def test_existing_api_and_historical_agents_are_not_edit_tools(self):
        m = core.manifest()
        for policy in m["agents"].values():
            self.assertNotIn("write_file", policy["tools"])
            self.assertNotIn("run_shell", policy["tools"])

    def test_stale_or_incomplete_checks_are_rejected(self):
        base = {"source_snapshot": core.snapshot(), "checks": []}
        with self.assertRaises(ValueError):
            core.validate_checks(base)
        base["source_snapshot"] = {}
        with self.assertRaises(ValueError):
            core.validate_checks(base)

    def test_llm_requires_current_checks_before_network(self):
        with patch("harness.runtime.execute_stage") as review:
            with self.assertRaises(ValueError):
                asyncio.run(run("001", approved=True, llm=True))
            review.assert_not_called()

    def test_failed_model_preserves_stage_without_claiming_execution(self):
        from harness.runtime import ReviewFailure
        with patch("harness.runtime.validate_checks"), patch("harness.runtime.safe_path") as path, patch("harness.runtime.execute_stage", side_effect=TimeoutError()):
            path.return_value.read_text.return_value = "{}"
            with self.assertRaises(ReviewFailure) as captured:
                asyncio.run(run("001", approved=True, llm=True, checks_path="docs/taller-6/ejecuciones/test/checks.json"))
        self.assertEqual(captured.exception.partial["stage"], "llm")
        self.assertEqual(captured.exception.partial["role"], "orquestador")
        self.assertEqual(captured.exception.partial["traces"], [])
        self.assertIn("TimeoutError", str(captured.exception))
