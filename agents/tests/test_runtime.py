"""Controles del ejecutor local: aprobación, alcance y contratos de reporte."""

import copy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from agents.runtime import (
    authorize_read,
    authorize_tool,
    build_tasks,
    load_manifest,
    run_demo,
    validate_report,
    validate_manifest,
)


SPEC = "Revisar frontend y backend de OPITA 360 sin cambiar funcionalidades."
SPECIALISTS = {"frontend", "backend", "calidad", "seguridad"}
ROOT = Path(__file__).resolve().parents[2]


class RuntimeTests(unittest.TestCase):
    def test_manifest_is_loaded_as_dictionary(self):
        manifest = load_manifest()
        self.assertIsInstance(manifest, dict)
        self.assertTrue(manifest)

    def test_manifest_rejects_expanded_privileges(self):
        for key in ("write", "network", "shell"):
            manifest = copy.deepcopy(load_manifest())
            manifest["limits"][key] = True
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_manifest(manifest)
        manifest = copy.deepcopy(load_manifest())
        manifest["tools"]["external_mcp"]["client_allowed_tools"].append("write_file")
        with self.assertRaises(ValueError):
            validate_manifest(manifest)

    def test_well_formed_but_false_evidence_is_rejected(self):
        base = run_demo(SPEC, approved=True)["reports"][0]
        for key, value in (("sha256", "0" * 64), ("bytes", 0)):
            report = copy.deepcopy(base)
            report["evidence"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_report(report)

    def test_frontend_can_read_assigned_source(self):
        source = authorize_read("frontend", "frontend/src/main.jsx")
        self.assertTrue(source.is_file())
        self.assertEqual(source.name, "main.jsx")

    def test_backend_can_read_assigned_source(self):
        self.assertTrue(authorize_read("backend", "backend/app/main.py").is_file())

    def test_unknown_role_is_rejected(self):
        with self.assertRaises(ValueError):
            authorize_read("administrador", "README.md")

    def test_frontend_cannot_read_backend_implementation(self):
        with self.assertRaises(ValueError):
            authorize_read("frontend", "backend/app/main.py")

    def test_paths_outside_allowlist_are_rejected(self):
        for role in SPECIALISTS:
            for path in ("../README.md", ".git/config", ".env", "database/schema.sql/../schema.sql"):
                with self.subTest(role=role, path=path), self.assertRaises(ValueError):
                    authorize_read(role, path)

    def test_tasks_cover_all_specialists_with_unique_ids(self):
        tasks = build_tasks(SPEC)
        self.assertEqual({task["agent"] for task in tasks}, SPECIALISTS)
        self.assertEqual(len({task["id"] for task in tasks}), len(tasks))
        for task in tasks:
            self.assertTrue(task["objective"])
        self.assertEqual({task["id"] for task in tasks}, {"T03", "T04", "T05", "T06"})
        self.assertEqual(len({task["objective"] for task in tasks}), 4)

    def test_limits_are_validated_and_consumed(self):
        for name, invalid in (("max_delegations", 0), ("max_delegations", True),
                              ("max_correction_rounds", 3), ("max_spec_chars", 0)):
            manifest = copy.deepcopy(load_manifest())
            manifest["limits"][name] = invalid
            with self.subTest(name=name, value=invalid), self.assertRaises(ValueError):
                validate_manifest(manifest)
        manifest = copy.deepcopy(load_manifest())
        manifest["limits"]["max_delegations"] = 3
        with patch("agents.runtime.load_manifest", return_value=manifest), self.assertRaises(ValueError):
            build_tasks(SPEC)
        manifest["limits"]["max_delegations"] = 4
        manifest["limits"]["max_spec_chars"] = 4
        with patch("agents.runtime.load_manifest", return_value=manifest), self.assertRaises(ValueError):
            build_tasks(SPEC)

    def test_read_requires_role_tool_permission(self):
        manifest = copy.deepcopy(load_manifest())
        manifest["agents"]["frontend"]["tools"] = []
        with patch("agents.runtime.load_manifest", return_value=manifest), self.assertRaises(ValueError):
            authorize_read("frontend", "frontend/src/main.jsx")
        with self.assertRaises(ValueError):
            authorize_tool("frontend", "delegate")

    def test_execution_requires_human_approval(self):
        with self.assertRaises(PermissionError):
            run_demo(SPEC)

    def test_demo_identifies_deterministic_mode_and_validates_reports(self):
        result = run_demo(SPEC, approved=True)
        self.assertEqual(result["mode"], "deterministic")
        self.assertEqual(len(result["reports"]), len(SPECIALISTS))
        for report in result["reports"]:
            validate_report(report)

    def test_empty_report_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_report({})

    def test_reports_require_issued_task_role_and_nonempty_evidence(self):
        base = copy.deepcopy(run_demo(SPEC, approved=True)["reports"][0])
        for key, value in (("task_id", "NONEXISTENT"), ("task_id", "T04"), ("evidence", [])):
            report = copy.deepcopy(base)
            report[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                validate_report(report)
        with self.assertRaises(ValueError):
            validate_report(base, [])

    def test_report_requires_complete_unique_task_evidence(self):
        tasks = build_tasks(SPEC)
        report = copy.deepcopy(run_demo(SPEC, approved=True)["reports"][0])
        report["evidence"] = report["evidence"][:1]
        with self.assertRaises(ValueError):
            validate_report(report, tasks)
        report["evidence"] = report["evidence"] * 2
        with self.assertRaises(ValueError):
            validate_report(report)

    def test_unknown_report_properties_are_rejected(self):
        report = copy.deepcopy(run_demo(SPEC, approved=True)["reports"][0])
        report["unapproved_shell_command"] = "arbitrary command"
        with self.assertRaises(ValueError):
            validate_report(report)

    def test_invalid_specifications_are_rejected(self):
        for spec in (None, {}, "", "  ", "x" * 4001):
            with self.subTest(spec_type=type(spec).__name__), self.assertRaises(ValueError):
                build_tasks(spec)

    def test_truthy_values_do_not_replace_explicit_approval(self):
        for approved in (1, "true", [True]):
            with self.subTest(approved=approved), self.assertRaises(PermissionError):
                run_demo(SPEC, approved=approved)

    def test_report_rejects_invalid_status_role_and_evidence(self):
        base = run_demo(SPEC, approved=True)["reports"][0]
        mutations = [
            ("version", "2.0.0"), ("agent", "orquestador"),
            ("status", "passed"), ("task_id", ""),
            ("findings", "all good"), ("limitations", [True]),
            ("evidence", {}),
        ]
        for field, value in mutations:
            report = copy.deepcopy(base)
            report[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_report(report)
        for field, value in (("path", ".env"), ("sha256", "invalid"),
                             ("bytes", -1), ("bytes", True)):
            report = copy.deepcopy(base)
            report["evidence"][0][field] = value
            with self.subTest(evidence_field=field), self.assertRaises(ValueError):
                validate_report(report)

    def test_reports_conform_to_published_json_schema(self):
        import jsonschema

        schema = json.loads((ROOT / "agents/report.schema.v1.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema)
        for report in run_demo(SPEC, approved=True)["reports"]:
            validator.validate(report)
        for field, value in (("status", "passed"), ("task_id", ""), ("evidence", {})):
            report = copy.deepcopy(run_demo(SPEC, approved=True)["reports"][0])
            report[field] = value
            with self.subTest(field=field), self.assertRaises(jsonschema.ValidationError):
                validator.validate(report)

    def test_model_execution_is_not_claimed(self):
        manifest = load_manifest()
        self.assertIn(manifest["mode"], ("deterministic", "ollama"))
        self.assertTrue(all(profile.get("executed", False) is False for profile in manifest["models"].values()))
        self.assertIs(run_demo(SPEC, approved=True)["llm_executed"], False)


class McpPolicyTests(unittest.TestCase):
    def test_client_allows_only_the_declared_read_tool(self):
        from agents.mcp_probe import authorize_tool

        authorize_tool("read_text_file")
        for tool in ("write_file", "edit_file", "move_file", "create_directory", "list_directory", "shell", ""):
            with self.subTest(tool=tool), self.assertRaises(PermissionError):
                authorize_tool(tool)


if __name__ == "__main__":
    unittest.main()
