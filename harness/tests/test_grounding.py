"""Contraste y plazos. Los fallos simulados son tests, no inferencias de evidencia."""
import copy
import time
import unittest
from harness import core
from harness.grounding import select_source, technical_facts, verify_assertions, test_summary
from harness.stages import StageTimeout, execute_stage

class GroundingTests(unittest.TestCase):
    def setUp(self):
        self.spec, _ = core.load_spec("001")
        # A draft fixture must not depend on the lifecycle of the real S01.
        self.spec = copy.deepcopy(self.spec)
        self.spec["implementation"] = "not_started"
        self.spec["test_runs"] = []
        self.facts = technical_facts(self.spec, None)

    def test_pydantic_model_and_typed_handler_are_found(self):
        self.assertTrue(self.facts["facts"]["pydantic_request_validation"]["value"])

    def test_frontend_fallback_is_found_in_frontend(self):
        self.assertTrue(self.facts["facts"]["frontend_demo_fallback"]["value"])

    def test_draft_is_not_implemented_or_tested(self):
        self.assertFalse(self.facts["facts"]["spec_implementation_recorded"]["value"])
        self.assertFalse(self.facts["facts"]["spec_tests_executed"]["value"])

    def test_context_contains_model_fields_and_handler_not_only_seed(self):
        source = next(s for s in core.context("backend") if s["path"] == "backend/app/main.py")
        selected = select_source(source)
        text = "\n".join(e["text"] for e in selected["excerpts"])
        for token in ("TripRequest(BaseModel)", "Field(", "def recommend_trip", "request: TripRequest"):
            self.assertIn(token, text)
        self.assertTrue(all(e["start_line"] > 0 for e in selected["excerpts"]))

    def test_frontend_context_includes_fetch_and_fallback(self):
        source = next(s for s in core.context("frontend") if s["path"] == "frontend/src/main.jsx")
        text = "\n".join(e["text"] for e in select_source(source)["excerpts"])
        self.assertIn("fetch(", text)
        self.assertIn("catch {", text)
        self.assertIn("async function makeTrip", text)

    def test_false_claim_of_missing_pydantic_is_contradicted(self):
        result = verify_assertions({"claims": [{"fact": "pydantic_request_validation", "value": False}]}, [], self.facts)
        self.assertEqual(result["claims"][0]["status"], "contradicted")
        self.assertEqual(result["blocked_claims"], 1)
        self.assertFalse(result["human_acceptance"])

    def test_true_claim_is_checked_but_does_not_approve_prose(self):
        result = verify_assertions({"claims": [{"fact": "pydantic_request_validation", "value": True}], "findings": ["texto sin comprobar"]}, [], self.facts)
        self.assertEqual(result["claims"][0]["status"], "verified")
        self.assertEqual(result["unverified_prose"], ["texto sin comprobar"])
        self.assertFalse(result["human_acceptance"])

    def test_unknown_or_string_claim_is_not_accepted(self):
        result = verify_assertions({"claims": [{"fact": "unknown", "value": True}, {"fact": "base_checks_passed", "value": "yes"}]}, [], self.facts)
        self.assertEqual(result["blocked_claims"], 2)

    def test_exact_supplied_citation_is_verified(self):
        sources = core.context("backend")
        source = next(s for s in sources if s["path"] == "backend/app/main.py")
        line = next(i for i,s in enumerate(source["text"].splitlines(),1) if "class TripRequest" in s)
        quote = source["text"].splitlines()[line-1]
        answer = {"citations": [{"path": source["path"], "line": line, "quote": quote}]}
        self.assertEqual(verify_assertions(answer, sources, self.facts)["citations"][0]["status"], "quote_verified")

    def test_wrong_or_unauthorized_citation_is_rejected(self):
        for citation in ({"path":"../secret","line":1,"quote":"sensitive"}, {"path":"backend/app/main.py","line":1,"quote":"not an actual quote"}):
            result = verify_assertions({"citations":[citation]}, core.context("backend"), self.facts)
            self.assertEqual(result["citations"][0]["status"], "invalid_or_not_supplied")

    def test_base_checks_do_not_mark_spec_cases_executed(self):
        record = {"checks":[{"name":n,"exit_code":0,"stdout":"Ran 8 tests","stderr":""} for n in ["harness","agents","backend","frontend","build"]]}
        facts = technical_facts(self.spec, record)
        self.assertTrue(facts["facts"]["base_checks_passed"]["value"])
        self.assertFalse(facts["facts"]["spec_tests_executed"]["value"])
        self.assertEqual(test_summary(record)["new_feature_tests"], "not_executed")

    def test_watchdog_reaps_its_actual_owned_worker(self):
        start = time.monotonic()
        with self.assertRaises(StageTimeout) as captured:
            execute_stage("deadline-test", "orquestador", {}, .05)
        self.assertTrue(captured.exception.event["worker_reaped"])
        self.assertLess(time.monotonic()-start, 8)

    def test_invalid_deadline_or_command_is_rejected(self):
        for kind, seconds in (("shell",1),("llm",0),("mcp",181)):
            with self.assertRaises(ValueError):
                execute_stage(kind,"orquestador",{},seconds)

    def test_cli_parser_has_no_duplicate_options(self):
        import contextlib
        import io
        from harness.cli import main
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as captured:
            main(["--help"])
        self.assertEqual(captured.exception.code, 0)
