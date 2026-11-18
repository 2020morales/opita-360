"""Políticas sin simular respuestas LLM ni sustituir la integración real."""
import asyncio
import unittest
from unittest.mock import patch

from agents.llm_workflow import main_run
from agents.runtime import authorize_tool, load_manifest


class WorkflowTests(unittest.TestCase):
    def test_llm_requires_explicit_approval_before_io(self):
        with self.assertRaises(PermissionError):
            asyncio.run(main_run("review", False))

    def test_all_roles_have_explicit_models(self):
        manifest = load_manifest()
        for role, declaration in manifest["agents"].items():
            profile = manifest["models"][declaration["model_profile"]]
            self.assertEqual(profile["provider"], "ollama-local")
            self.assertEqual(profile["model"], "qwen3.5:4b")
            authorize_tool(role, "llm_chat")

    def test_mcp_restricted_to_source_specialists(self):
        for role in ("frontend", "backend"):
            authorize_tool(role, "external_mcp")
        for role in ("calidad", "seguridad"):
            with self.assertRaises(ValueError):
                authorize_tool(role, "external_mcp")

    def test_stale_checks_rejected_before_model_call(self):
        with patch("agents.llm_workflow.snapshot", return_value={"sha256": "deliberately-stale"}):
            with self.assertRaises(ValueError):
                asyncio.run(main_run("review", True))
