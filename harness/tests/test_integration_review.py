"""Pure contract tests; no LLM execution is simulated or claimed."""
import unittest
from harness.runtime import review_instruction, validate_inference_metadata


class IntegrationReviewTests(unittest.TestCase):
    def test_prompt_uses_actual_lifecycle_instead_of_assuming_draft(self):
        for state in ('implemented', 'not_started'):
            prompt = review_instruction('seguridad', {'status': 'approved', 'implementation': state})
            self.assertIn('implementation=' + state, prompt)
            self.assertNotIn('Revisa un BORRADOR', prompt)
            self.assertIn('pueden incluir regresiones y casos nuevos', prompt)

    def test_incomplete_and_wrong_model_have_distinct_metadata_diagnostics(self):
        with self.assertRaisesRegex(ValueError, 'Incomplete inference:.*length.*1000'):
            validate_inference_metadata({'model': 'configured', 'done': True, 'done_reason': 'length', 'eval_count': 1000}, 'configured')
        with self.assertRaisesRegex(ValueError, 'Unexpected model'):
            validate_inference_metadata({'model': 'other', 'done': True}, 'configured')
        validate_inference_metadata({'model': 'configured', 'done': True, 'done_reason': 'stop'}, 'configured')

    def test_total_context_cap_preserves_facts_and_does_not_mutate_original(self):
        import copy
        import json
        from harness.runtime import compact_payload
        source = {'path': 'sample.py', 'excerpts': [{'start_line': 1, 'end_line': 500, 'text': '\n'.join('line ' + str(i) + ' x' * 30 for i in range(500))}]}
        payload = {'specification': {'id': '005'}, 'technical_facts': {'fact': True}, 'test_results': {'passed': 140}, 'sources': [source], 'mcp': [{'content_equal': True, 'content': 'duplicate' * 3000}]}
        before = copy.deepcopy(payload)
        result = compact_payload(payload, 1800)
        self.assertLessEqual(len(json.dumps(result)), 1800)
        self.assertEqual(payload, before)
        self.assertEqual(result['technical_facts'], payload['technical_facts'])
        self.assertEqual(result['test_results'], payload['test_results'])
        self.assertTrue(result['context_limit']['truncated'])
        self.assertNotIn('content', result['mcp'][0])
        self.assertTrue(result['mcp'][0]['content_equal'])

    def test_mandatory_metadata_cannot_silently_bypass_context_cap(self):
        from harness.runtime import compact_payload
        with self.assertRaisesRegex(ValueError, 'metadata exceeds cap'):
            compact_payload({'specification': {'text': 'x' * 5000}, 'sources': []}, 1800)

    def test_a_citation_removed_by_compaction_is_not_verified(self):
        from harness import core
        from harness.grounding import technical_facts, verify_assertions
        sources = core.context('backend')
        source = next(s for s in sources if s['path'] == 'backend/app/main.py')
        line = next(i for i, s in enumerate(source['text'].splitlines(), 1) if 'class TripRequest' in s)
        answer = {'citations': [{'path': source['path'], 'line': line, 'quote': source['text'].splitlines()[line - 1]}]}
        spec, _ = core.load_spec('005')
        result = verify_assertions(answer, sources, technical_facts(spec, None), supplied_sources=[{'path': source['path'], 'excerpts': []}])
        self.assertEqual(result['citations'][0]['status'], 'invalid_or_not_supplied')
