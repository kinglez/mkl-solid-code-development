"""Assert tool behavior, traceability and error cases; not merely process survival."""
import copy
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


validator = module("validate_delivery")
initializer = module("init_delivery")


class DeliveryValidationTests(unittest.TestCase):
    def setUp(self):
        self.record = validator.load_record(FIXTURES / "ready.json")

    def check(self, record=None):
        return validator.validate(self.record if record is None else record, FIXTURES)

    def codes(self, result, key):
        return {i["code"] for i in result[key]}

    def test_ready_fixture_has_complete_record_coverage(self):
        result = self.check()
        self.assertTrue(result["structure_valid"])
        self.assertTrue(result["record_ready"])

    def test_partial_is_structurally_valid_but_not_ready(self):
        result = self.check(validator.load_record(FIXTURES / "partial.json"))
        self.assertTrue(result["structure_valid"])
        self.assertFalse(result["record_ready"])
        self.assertIn("UNSETTLED_RULE", self.codes(result, "blockers"))

    def test_invalid_fixture_reports_actual_expected_defects(self):
        result = self.check(validator.load_record(FIXTURES / "invalid.json"))
        self.assertFalse(result["structure_valid"])
        self.assertTrue({"DUPLICATE_ID", "UNKNOWN_REFERENCE", "PASS_EXIT_MISMATCH", "ARTIFACT_MISSING"}
                        <= self.codes(result, "errors"))

    def test_confirmed_rule_needs_acceptance_coverage(self):
        self.record["rules"].append(dict(self.record["rules"][0], id="R2"))
        self.assertIn("RULE_WITHOUT_ACCEPTANCE", self.codes(self.check(), "blockers"))

    def test_general_review_cannot_replace_behavior_evidence(self):
        self.record["acceptance"][0]["evidence_ids"] = ["E2"]
        self.assertIn("CASE_WITHOUT_BEHAVIOR_EVIDENCE", self.codes(self.check(), "blockers"))

    def test_manual_behavior_check_can_support_a_visual_change(self):
        item = self.record["evidence"][0]
        item["method"] = "inspection"
        item["artifact"] = "evidence/inspection.md"
        del item["command"]
        del item["exit_code"]
        self.assertTrue(self.check()["record_ready"])

    def test_manual_check_cannot_claim_a_command_exit_code(self):
        self.record["evidence"][0]["method"] = "inspection"
        self.assertIn("INSPECTION_HAS_COMMAND", self.codes(self.check(), "errors"))

    def test_unconfirmed_dependency_blocks_case_even_if_marked_nonblocking(self):
        self.record["rules"][0]["status"] = "assumed"
        self.assertIn("CASE_USES_UNSETTLED_RULE", self.codes(self.check(), "blockers"))

    def test_nonblocking_unsettled_future_scope_does_not_block_delivery(self):
        self.record["rules"].append(dict(self.record["rules"][0], id="R2", status="open", blocks_completion=False))
        self.assertTrue(self.check()["record_ready"])

    def test_review_must_be_recorded_even_when_no_findings(self):
        self.record["review"]["evidence_ids"] = []
        self.assertIn("REVIEW_INCOMPLETE", self.codes(self.check(), "blockers"))

    def test_required_open_finding_blocks_implementation_but_not_review_report(self):
        self.record["review"]["findings"] = [
            {"id": "F1", "detail": "The dependency is not used as agreed", "required": True, "status": "open", "evidence_ids": []}]
        self.assertIn("REQUIRED_FINDING_OPEN", self.codes(self.check(), "blockers"))
        self.record["task"]["intent"] = "review"
        self.assertTrue(self.check()["record_ready"])

    def test_finding_completion_gate_respects_intent_required_and_resolution(self):
        for intent in ("implement", "design", "review"):
            for required in (True, False):
                for status in ("open", "deferred", "resolved"):
                    with self.subTest(intent=intent, required=required, status=status):
                        record = copy.deepcopy(self.record)
                        record["task"]["intent"] = intent
                        if intent == "design":
                            record["design"] = [{
                                "id": "D1", "decision": "Validate input before generating a result", "reason": "Preserve the interface contract",
                                "tradeoffs": "Do not return partial results on failure", "evidence_ids": ["E2"]}]
                        record["review"]["findings"] = [{
                            "id": "F1", "detail": "An agreed constraint still requires correction", "required": required,
                            "status": status, "evidence_ids": ["E2"] if status == "resolved" else []}]
                        result = self.check(record)
                        blocked = intent in ("implement", "design") and required and status != "resolved"
                        self.assertTrue(result["structure_valid"])
                        self.assertEqual(result["record_ready"], not blocked)
                        self.assertEqual("REQUIRED_FINDING_OPEN" in self.codes(result, "blockers"), blocked)

    def test_resolved_finding_requires_evidence(self):
        self.record["review"]["findings"] = [
            {"id": "F1", "detail": "Corrected dependency usage", "required": True, "status": "resolved", "evidence_ids": []}]
        self.assertIn("FIX_WITHOUT_EVIDENCE", self.codes(self.check(), "blockers"))

    def test_design_only_does_not_require_code_or_behavior_tests(self):
        self.record["task"]["intent"] = "design"
        self.record["rules"] = []
        self.record["acceptance"] = []
        self.record["evidence"] = [self.record["evidence"][1]]
        self.record["design"] = [{"id": "D1", "decision": "Bounded reads", "reason": "Avoid retaining the entire dataset in memory",
                                 "tradeoffs": "Requires temporary storage", "evidence_ids": ["E2"]}]
        self.assertTrue(self.check()["record_ready"])
        self.record["design"][0]["evidence_ids"] = []
        self.assertIn("DESIGN_WITHOUT_REVIEW", self.codes(self.check(), "blockers"))

    def test_not_run_is_not_passed_and_has_no_exit_code(self):
        self.record["evidence"][0]["status"] = "not_run"
        result = self.check()
        self.assertIn("NOT_RUN_EXIT_CODE", self.codes(result, "errors"))
        self.assertIn("CASE_WITHOUT_BEHAVIOR_EVIDENCE", self.codes(result, "blockers"))

    def test_missing_log_cannot_support_pass(self):
        self.record["evidence"][0]["artifact"] = "missing.log"
        self.assertIn("ARTIFACT_MISSING", self.codes(self.check(), "errors"))

    def test_paths_outside_root_are_rejected(self):
        for value in ("../outside.log", str((FIXTURES / "evidence/behavior.log").resolve())):
            with self.subTest(value=value):
                self.record["evidence"][0]["artifact"] = value
                self.assertIn("ARTIFACT_OUTSIDE_ROOT", self.codes(self.check(), "errors"))

    def test_symlink_cannot_escape_evidence_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            root = base / "project"
            root.mkdir()
            target = base / "outside.txt"
            target.write_text("outside", encoding="utf-8")
            link = root / "link.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable in this environment")
            record = copy.deepcopy(self.record)
            record["evidence"][0]["artifact"] = "link.txt"
            self.assertIn("ARTIFACT_OUTSIDE_ROOT", self.codes(validator.validate(record, root), "errors"))

    def test_evidence_resolution_failure_is_a_located_validation_error(self):
        real_resolve = Path.resolve

        def loop_for_artifact(path, *args, **kwargs):
            if path.name == "loop.log":
                raise RuntimeError("Symlink loop from test artifact")
            return real_resolve(path, *args, **kwargs)

        self.record["evidence"][0]["artifact"] = "loop.log"
        with patch.object(Path, "resolve", loop_for_artifact):
            result = self.check()
        self.assertFalse(result["structure_valid"])
        self.assertFalse(result["record_ready"])
        artifact_error = next(item for item in result["errors"] if item["code"] == "ARTIFACT_INVALID")
        self.assertEqual(artifact_error["location"], self.record["evidence"][0]["id"])

    def test_wrong_types_and_unknown_fields_report_errors_instead_of_crashing(self):
        mutations = [("task", []), ("rules", {}), ("evidence", 1), ("review", False), ("schema_version", True)]
        for field, value in mutations:
            with self.subTest(field=field):
                record = copy.deepcopy(self.record)
                record[field] = value
                self.assertFalse(self.check(record)["structure_valid"])
        self.record["task"]["statsu"] = "complete"
        self.assertIn("UNKNOWN_FIELD", self.codes(self.check(), "errors"))

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "record.json"
            p.write_text('{"task": {"status": "partial", "status": "complete"}}', encoding="utf-8")
            with self.assertRaises(ValueError):
                validator.load_record(p)

    def test_duplicate_reference_is_not_silently_accepted(self):
        self.record["acceptance"][0]["rule_ids"] = ["R1", "R1"]
        self.assertIn("DUPLICATE_REFERENCE", self.codes(self.check(), "errors"))


class DeliveryCliTests(unittest.TestCase):
    def invoke(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "scripts/validate_delivery.py"), *map(str, args)],
                              capture_output=True, text=True)

    def test_strict_mode_distinguishes_partial_and_ready(self):
        ready = self.invoke(FIXTURES / "ready.json", "--require-ready")
        partial = self.invoke(FIXTURES / "partial.json", "--require-ready")
        normal = self.invoke(FIXTURES / "partial.json")
        self.assertEqual(ready.returncode, 0)
        self.assertEqual(partial.returncode, 1)
        self.assertEqual(normal.returncode, 0)
        self.assertFalse(json.loads(normal.stdout)["record_ready"])

    def test_unreadable_and_malformed_input_use_exit_two(self):
        self.assertEqual(self.invoke(FIXTURES / "missing.json").returncode, 2)
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.json"
            p.write_text('{', encoding="utf-8")
            self.assertEqual(self.invoke(p).returncode, 2)

    def test_symlink_loop_returns_structured_cli_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            link = root / "loop.log"
            try:
                link.symlink_to("loop.log")
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable in this environment")
            record = validator.load_record(FIXTURES / "ready.json")
            record["evidence"][0]["artifact"] = "loop.log"
            record_path = root / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = self.invoke(record_path, "--project-root", root, "--require-ready")
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["structure_valid"])
            self.assertFalse(payload["record_ready"])
            self.assertTrue({"ARTIFACT_INVALID", "ARTIFACT_MISSING"} & {item["code"] for item in payload["errors"]})
            self.assertEqual(result.stderr, "")

    def test_recorded_commands_are_never_executed(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            marker = p / "executed.txt"
            record = validator.load_record(FIXTURES / "ready.json")
            record["evidence"][0]["command"] = f"touch {marker}"
            record_path = p / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = self.invoke(record_path, "--project-root", FIXTURES, "--require-ready")
            self.assertEqual(result.returncode, 0)
            self.assertFalse(marker.exists())

    def test_required_design_finding_blocks_strict_cli_until_resolved(self):
        record = validator.load_record(FIXTURES / "ready.json")
        record["task"]["intent"] = "design"
        record["design"] = [{"id": "D1", "decision": "Validate input", "reason": "Preserve the interface contract",
                             "tradeoffs": "Reject invalid input", "evidence_ids": ["E2"]}]
        record["review"]["findings"] = [{"id": "F1", "detail": "A required constraint remains unmet", "required": True,
                                         "status": "open", "evidence_ids": []}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "design.json"
            path.write_text(json.dumps(record), encoding="utf-8")
            normal = self.invoke(path, "--project-root", FIXTURES)
            strict = self.invoke(path, "--project-root", FIXTURES, "--require-ready")
            self.assertEqual(normal.returncode, 0)
            self.assertFalse(json.loads(normal.stdout)["record_ready"])
            self.assertEqual(strict.returncode, 1)
            record["review"]["findings"][0].update(status="resolved", evidence_ids=["E2"])
            path.write_text(json.dumps(record), encoding="utf-8")
            resolved = self.invoke(path, "--project-root", FIXTURES, "--require-ready")
            self.assertEqual(resolved.returncode, 0)
            self.assertTrue(json.loads(resolved.stdout)["record_ready"])


class InitializationTests(unittest.TestCase):
    def test_unencodable_arguments_leave_no_files_and_allow_valid_retry(self):
        for field in ("task_id", "summary"):
            for with_brief in (False, True):
                with self.subTest(field=field, with_brief=with_brief), tempfile.TemporaryDirectory() as tmp:
                    root = Path(tmp) / "delivery"
                    args = {"task_id": "TASK-1", "summary": "Generic delivery objective", "intent": "design",
                            "with_brief": with_brief}
                    args[field] = "bad\udcff"
                    with self.assertRaises(UnicodeEncodeError):
                        initializer.initialize(root, **args)
                    self.assertFalse(root.exists())
                    outputs = initializer.initialize(root, "TASK-1", "\u6709\u6548\u7684\u4e2d\u6587\u6458\u8981", "design", with_brief)
                    self.assertTrue(all(p.is_file() for p in outputs))
                    self.assertEqual(validator.load_record(root / "delivery-record.json")["task"]["summary"],
                                     "\u6709\u6548\u7684\u4e2d\u6587\u6458\u8981")

    def test_later_write_failure_removes_only_new_outputs_and_allows_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "keep.txt"
            existing.write_text("Existing content", encoding="utf-8")
            real_open = Path.open

            def fail_brief(path, *args, **kwargs):
                if path == root / "implementation-brief.md":
                    raise OSError("simulated second output failure")
                return real_open(path, *args, **kwargs)

            with patch.object(Path, "open", fail_brief), self.assertRaises(OSError):
                initializer.initialize(root, "TASK-1", "Generic delivery objective", "design", True)
            self.assertEqual([p.name for p in root.iterdir()], ["keep.txt"])
            self.assertEqual(existing.read_text(encoding="utf-8"), "Existing content")
            self.assertEqual(len(initializer.initialize(root, "TASK-1", "Valid retry", "design", True)), 2)

    def test_main_rejects_unencodable_argument_with_exit_two_and_allows_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "delivery"
            args = [str(root), "--id", "TASK-1", "--summary", "bad\udcff", "--with-brief"]
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                self.assertEqual(initializer.main(args), 2)
            self.assertIn("Cannot initialize:", stderr.getvalue())
            self.assertFalse(root.exists())
            args[4] = "Valid summary"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(initializer.main(args), 0)

    def test_initialized_record_is_valid_and_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "delivery"
            outputs = initializer.initialize(root, "TASK-1", "Preserve the declared input contract", "implement", True)
            self.assertEqual({p.name for p in outputs}, {"delivery-record.json", "implementation-brief.md"})
            record = validator.load_record(root / "delivery-record.json")
            self.assertEqual(record["task"]["id"], "TASK-1")
            result = validator.validate(record, root)
            self.assertTrue(result["structure_valid"])
            self.assertFalse(result["record_ready"])

    def test_existing_output_is_not_overwritten_and_no_other_file_is_created(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "implementation-brief.md"
            existing.write_text("Existing user content", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                initializer.initialize(root, "TASK-1", "Change", "implement", True)
            self.assertEqual(existing.read_text(encoding="utf-8"), "Existing user content")
            self.assertFalse((root / "delivery-record.json").exists())

    def test_invalid_input_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "new"
            with self.assertRaises(ValueError):
                initializer.initialize(root, " ", "summary", "implement")
            self.assertFalse(root.exists())


if __name__ == "__main__":
    unittest.main()
