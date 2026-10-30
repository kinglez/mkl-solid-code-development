"""Verify stage outputs are real, linked inputs rather than completion labels."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures'
spec = importlib.util.spec_from_file_location('handoff_validator', ROOT / 'scripts/validate_delivery.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def step(identifier, inputs, output, status='completed'):
    return {'id': identifier, 'stage': 'Scoped stage ' + identifier, 'status': status,
            'input_ids': inputs, 'outputs': [{'id': output, 'summary': 'Usable result of ' + identifier,
                                            'artifact': 'evidence/inspection.md'}],
            'notes': 'Initial source: supplied task.' if not inputs else 'Read and checked the referenced result.'}


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.record = validator.load_record(FIXTURES / 'ready.json')
        self.record['handoffs'] = [step('H1', [], 'A1'), step('H2', ['A1'], 'A2')]

    def check(self):
        return validator.validate(self.record, FIXTURES)

    def codes(self, result, key='blockers'):
        return {entry['code'] for entry in result[key]}

    def test_linked_completed_stages_are_ready(self):
        result = self.check()
        self.assertTrue(result['structure_valid'])
        self.assertTrue(result['record_ready'])

    def test_completed_stage_requires_a_usable_output(self):
        self.record['handoffs'][1]['outputs'] = []
        result = self.check()
        self.assertTrue(result['structure_valid'])
        self.assertFalse(result['record_ready'])
        self.assertIn('HANDOFF_OUTPUT_REQUIRED', self.codes(result))

    def test_empty_output_text_or_notes_are_rejected(self):
        for mutate in ('summary', 'notes'):
            with self.subTest(field=mutate):
                record = copy.deepcopy(self.record)
                if mutate == 'summary':
                    record['handoffs'][0]['outputs'][0]['summary'] = ''
                else:
                    record['handoffs'][0]['notes'] = ''
                result = validator.validate(record, FIXTURES)
                self.assertFalse(result['structure_valid'])
                self.assertIn('TEXT_REQUIRED', self.codes(result, 'errors'))

    def test_unknown_input_is_rejected(self):
        self.record['handoffs'][1]['input_ids'] = ['DOES-NOT-EXIST']
        result = self.check()
        self.assertFalse(result['structure_valid'])
        self.assertIn('UNKNOWN_REFERENCE', self.codes(result, 'errors'))

    def test_self_and_forward_inputs_are_rejected(self):
        for input_id in ('A1', 'A2'):
            with self.subTest(input_id=input_id):
                record = copy.deepcopy(self.record)
                record['handoffs'][0]['input_ids'] = [input_id]
                result = validator.validate(record, FIXTURES)
                self.assertFalse(result['structure_valid'])
                self.assertIn('HANDOFF_FORWARD_REFERENCE', self.codes(result, 'errors'))

    def test_next_stage_must_consume_the_previous_active_result(self):
        self.record['handoffs'].append(step('H3', ['A1'], 'A3'))
        result = self.check()
        self.assertTrue(result['structure_valid'])
        self.assertFalse(result['record_ready'])
        self.assertIn('HANDOFF_NOT_CONNECTED', self.codes(result))

    def test_unready_upstream_results_cannot_be_consumed(self):
        for status in ('pending', 'blocked', 'invalidated'):
            with self.subTest(status=status):
                record = copy.deepcopy(self.record)
                record['handoffs'][0]['status'] = status
                result = validator.validate(record, FIXTURES)
                self.assertTrue(result['structure_valid'])
                self.assertFalse(result['record_ready'])
                self.assertIn('HANDOFF_INPUT_NOT_READY', self.codes(result))

    def test_skipped_stage_preserves_the_last_real_output(self):
        self.record['handoffs'].insert(1, {'id': 'HS', 'stage': 'Unneeded diagram', 'status': 'skipped',
                                         'input_ids': [], 'outputs': [], 'notes': 'The existing contract is sufficient.'})
        self.assertTrue(self.check()['record_ready'])
        self.record['handoffs'][1]['outputs'] = [{'id': 'AS', 'summary': 'Invented result'}]
        self.assertIn('SKIPPED_HANDOFF_HAS_OUTPUT', self.codes(self.check(), 'errors'))

    def test_reused_outputs_require_readiness_and_may_be_inline(self):
        first = self.record['handoffs'][0]
        first['status'] = 'reused'
        first['notes'] = 'Read existing rules and checked applicability to the current scope.'
        del first['outputs'][0]['artifact']
        self.assertTrue(self.check()['record_ready'])

    def test_missing_or_escaping_output_artifacts_are_rejected(self):
        for artifact, code in [('missing.md', 'HANDOFF_ARTIFACT_MISSING'),
                               ('../outside.md', 'HANDOFF_ARTIFACT_OUTSIDE_ROOT'),
                               (str(FIXTURES.resolve() / 'evidence/inspection.md'), 'HANDOFF_ARTIFACT_OUTSIDE_ROOT')]:
            with self.subTest(artifact=artifact):
                record = copy.deepcopy(self.record)
                record['handoffs'][0]['outputs'][0]['artifact'] = artifact
                result = validator.validate(record, FIXTURES)
                self.assertIn(code, self.codes(result, 'errors'))

    def test_output_ids_are_unique_across_the_whole_record(self):
        for duplicate in ('A1', 'R1', 'E1', 'H1'):
            with self.subTest(duplicate=duplicate):
                record = copy.deepcopy(self.record)
                record['handoffs'][1]['outputs'][0]['id'] = duplicate
                self.assertIn('DUPLICATE_ID', self.codes(validator.validate(record, FIXTURES), 'errors'))

    def test_output_symlink_cannot_escape_the_project_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'project'
            root.mkdir()
            (root / 'proof.md').write_text('Synthetic inspection fixture')
            outside = Path(tmp) / 'outside.md'
            outside.write_text('Outside the allowed artifact root')
            try:
                (root / 'escape.md').symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unavailable in this environment')
            record = copy.deepcopy(self.record)
            for item in record['evidence']:
                item['artifact'] = 'proof.md'
            for stage in record['handoffs']:
                stage['outputs'][0]['artifact'] = 'proof.md'
            record['handoffs'][0]['outputs'][0]['artifact'] = 'escape.md'
            result = validator.validate(record, root)
            self.assertIn('HANDOFF_ARTIFACT_OUTSIDE_ROOT', self.codes(result, 'errors'))

    def test_empty_or_all_skipped_handoffs_cannot_claim_readiness(self):
        for stages in ([], [{'id': 'HS', 'stage': 'Everything', 'status': 'skipped',
                             'input_ids': [], 'outputs': [], 'notes': 'No stages performed.'}]):
            with self.subTest(stages=stages):
                self.record['handoffs'] = stages
                result = self.check()
                self.assertTrue(result['structure_valid'])
                self.assertFalse(result['record_ready'])
                self.assertIn('HANDOFFS_EMPTY', self.codes(result))

    def test_design_and_review_requests_can_end_with_their_own_artifacts(self):
        for intent in ('design', 'review'):
            with self.subTest(intent=intent):
                record = copy.deepcopy(self.record)
                record['task']['intent'] = intent
                record['rules'], record['acceptance'] = [], []
                record['evidence'] = [record['evidence'][1]]
                record['handoffs'] = [step('H1', [], 'A1')]
                if intent == 'design':
                    record['design'] = [{'id': 'D1', 'decision': 'Keep a narrow interface', 'reason': 'Stable callers',
                                         'tradeoffs': 'Explicit constraints', 'evidence_ids': ['E2']}]
                else:
                    record['review']['findings'] = [{'id': 'F1', 'detail': 'Unresolved issue in the reviewed change',
                                                     'required': True, 'status': 'open', 'evidence_ids': []}]
                self.assertTrue(validator.validate(record, FIXTURES)['record_ready'])

    def test_malformed_handoff_values_report_errors_without_crashing(self):
        for value in (None, {}, [False], [{'id': 'H1', 'stage': 'Work', 'status': 'completed',
                                          'input_ids': {}, 'outputs': [False], 'notes': 'Source: task.'}]):
            with self.subTest(value=value):
                self.record['handoffs'] = value
                self.assertFalse(self.check()['structure_valid'])

    def test_strict_cli_requires_handoffs_and_accepts_a_complete_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'record.json'
            command = [sys.executable, str(ROOT / 'scripts/validate_delivery.py'), str(path),
                       '--project-root', str(FIXTURES), '--require-handoffs']
            legacy = copy.deepcopy(self.record)
            del legacy['handoffs']
            path.write_text(json.dumps(legacy))
            missing = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertIn('HANDOFFS_MISSING', {entry['code'] for entry in json.loads(missing.stdout)['blockers']})
            self.assertTrue(validator.validate(legacy, FIXTURES)['record_ready'])
            path.write_text(json.dumps(self.record))
            ready = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(ready.returncode, 0)
            self.assertTrue(json.loads(ready.stdout)['record_ready'])


    def seven_stage_chain(self):
        stages = ("Requirements clarification", "Requirements baseline", "Analysis",
                  "Detailed design", "Coding", "Change review", "Architecture review")
        result = []
        for index, label in enumerate(stages, 1):
            item = step(f"H{index}", [f"A{index - 1}"] if index > 1 else [], f"A{index}")
            item["stage"] = label
            result.append(item)
        return result

    def test_seven_stage_chain_is_ready_without_a_new_record_schema(self):
        self.record["handoffs"] = self.seven_stage_chain()
        result = self.check()
        self.assertTrue(result["structure_valid"])
        self.assertTrue(result["record_ready"])
        self.assertEqual(self.record["schema_version"], 1)

    def test_seven_stage_chain_does_not_consume_a_blocked_analysis(self):
        self.record["handoffs"] = self.seven_stage_chain()
        self.record["handoffs"][2]["status"] = "blocked"
        result = self.check()
        self.assertTrue(result["structure_valid"])
        self.assertFalse(result["record_ready"])
        self.assertIn("HANDOFF_INPUT_NOT_READY", self.codes(result))

    def test_revision_requires_ready_replacement_inputs_before_completion(self):
        self.record["handoffs"] = self.seven_stage_chain()
        self.record["handoffs"][1]["status"] = "invalidated"
        self.assertIn("HANDOFF_INPUT_NOT_READY", self.codes(self.check()))
        # The producer supplies a new version. A consumer still using the retired
        # identifier must not silently regain readiness.
        self.record["handoffs"][1]["status"] = "completed"
        self.record["handoffs"][1]["outputs"][0]["id"] = "A2-REV2"
        stale = self.check()
        self.assertFalse(stale["structure_valid"])
        self.assertIn("UNKNOWN_REFERENCE", self.codes(stale, "errors"))
        self.record["handoffs"][2]["input_ids"] = ["A2-REV2"]
        self.assertTrue(self.check()["record_ready"])

    def test_legacy_stage_count_remains_supported(self):
        self.record["handoffs"] = [step(f"H{i}", [f"A{i-1}"] if i > 1 else [], f"A{i}")
                                    for i in range(1, 13)]
        self.assertTrue(self.check()["record_ready"])


if __name__ == '__main__':
    unittest.main()
