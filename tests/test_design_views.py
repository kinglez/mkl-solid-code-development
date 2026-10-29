"""Check declared design-view gates; synthetic sources are not semantic evidence."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_delivery.py"
spec = importlib.util.spec_from_file_location("design_view_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class DesignViewTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for name in ("class.puml", "module.puml", "sequence.puml", "state.puml", "review.md", "checks.log", "preview.svg"):
            (self.root / name).write_text("Synthetic fixture for record validation only.\n")
        self.record = {
            "schema_version": 1,
            "task": {"id": "T", "intent": "implement", "summary": "Scoped synthetic contract", "status": "complete"},
            "rules": [{"id": "R1", "text": "A confirmed contract", "status": "confirmed", "source": "Synthetic input", "blocks_completion": True}],
            "acceptance": [{"id": "A1", "scenario": "A scoped request", "expected": "The specified result", "rule_ids": ["R1"], "evidence_ids": ["E-CHECK"]}],
            "design": [{"id": "D1", "decision": "Use the scoped interface", "reason": "It owns the responsibility", "tradeoffs": "Retains the current seam", "evidence_ids": ["E-REVIEW"]}],
            "evidence": [
                {"id": "E-REVIEW", "kind": "design_review", "method": "inspection", "status": "passed", "summary": "Synthetic declared review, not proof of semantic consistency", "artifact": "review.md"},
                {"id": "E-CHECK", "kind": "behavior", "method": "command", "status": "passed", "summary": "Synthetic declared check", "artifact": "checks.log", "command": "synthetic-not-executed", "exit_code": 0}],
            "review": {"status": "completed", "evidence_ids": ["E-REVIEW"], "findings": []},
            "limitations": []}
        self.record["design_views"] = {
            "profile": "detailed", "reason": "A new responsibility and interaction contract", "rule_ids": ["R1"],
            "state_model": {"requirement": "not_applicable", "reason": "No lifecycle is affected within this scope"},
            "views": [self.view("V-CLASS", "class"), self.view("V-SEQUENCE", "sequence")],
            "consistency_review": {"status": "completed", "view_ids": ["V-CLASS", "V-SEQUENCE"], "evidence_ids": ["E-REVIEW"], "notes": "Reviewed the declared current view set", "unresolved_issues": []}}

    def view(self, identifier, kind, status="completed"):
        return {"id": identifier, "kind": kind, "status": status, "artifact": kind + ".puml", "evidence_ids": ["E-REVIEW"], "notes": "Current source and applicability were inspected"}

    def check(self):
        return validator.validate(self.record, self.root)

    def invoke(self, *args):
        path = self.root / "record.json"
        path.write_text(json.dumps(self.record))
        return subprocess.run([sys.executable, str(SCRIPT), str(path), "--project-root", str(self.root), *args], capture_output=True, text=True)

    def test_legacy_record_does_not_claim_a_design_assessment(self):
        self.record.pop("design_views")
        result = self.check()
        self.assertTrue(result["record_ready"])
        self.assertIsNone(result["design_ready"])
        self.assertEqual(result["design_blockers"], [])

    def test_required_design_rejects_a_missing_bundle(self):
        self.record.pop("design_views")
        result = self.invoke("--require-design")
        self.assertEqual(result.returncode, 1, result.stderr)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["design_ready"])
        self.assertFalse(payload["record_ready"])

    def test_preimplementation_design_can_be_ready_while_delivery_is_not(self):
        self.record["task"]["status"] = "in_progress"
        self.record["acceptance"][0]["evidence_ids"] = []
        self.record["review"] = {"status": "not_run", "evidence_ids": [], "findings": [
            {"id": "F-CODE", "detail": "The requested implementation remains to be written", "required": True, "status": "open", "evidence_ids": []}]}
        self.record["handoffs"] = [{"id": "H-FUTURE", "stage": "Implementation", "status": "pending", "input_ids": [], "outputs": [], "notes": "Code is future work"}]
        result = self.invoke("--require-design")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["structure_valid"])
        self.assertTrue(payload["design_ready"])
        self.assertFalse(payload["record_ready"])
        for flag in ("--require-ready", "--require-handoffs"):
            combined = self.invoke("--require-design", flag)
            self.assertEqual(combined.returncode, 1, combined.stderr)
            self.assertTrue(json.loads(combined.stdout)["design_ready"])

    def test_detailed_design_accepts_class_or_module_without_forcing_classes(self):
        for kind in ("class", "module"):
            with self.subTest(kind=kind):
                self.record["design_views"]["views"][0] = self.view("V-CLASS", kind)
                self.assertTrue(self.check()["design_ready"])

    def test_detailed_design_requires_both_structure_and_sequence(self):
        original = copy.deepcopy(self.record)
        for kind in ("class", "sequence"):
            with self.subTest(missing=kind):
                self.record = copy.deepcopy(original)
                self.record["design_views"]["views"] = [v for v in self.record["design_views"]["views"] if v["kind"] != kind]
                self.record["design_views"]["consistency_review"]["view_ids"] = [v["id"] for v in self.record["design_views"]["views"]]
                self.assertFalse(self.check()["design_ready"])
                self.assertFalse(self.check()["record_ready"])

    def test_required_views_cannot_be_satisfied_by_unready_or_skipped_results(self):
        original = copy.deepcopy(self.record)
        for status in ("pending", "blocked", "invalidated", "skipped"):
            with self.subTest(status=status):
                self.record = copy.deepcopy(original)
                item = self.record["design_views"]["views"][0]
                item["status"] = status
                if status == "skipped":
                    item.pop("artifact")
                    item["evidence_ids"] = []
                self.assertFalse(self.check()["design_ready"])

    def test_required_state_view_applies_even_to_a_lightweight_profile(self):
        self.record["design_views"]["profile"] = "lightweight"
        self.record["design_views"]["state_model"] = {"requirement": "required", "reason": "Allowed operations depend on lifecycle"}
        self.assertFalse(self.check()["design_ready"])
        self.record["design_views"]["views"].append(self.view("V-STATE", "state"))
        self.record["design_views"]["consistency_review"]["view_ids"].append("V-STATE")
        self.assertTrue(self.check()["design_ready"])

    def test_state_applicability_must_be_resolved_and_explained(self):
        self.record["design_views"]["state_model"]["requirement"] = "unresolved"
        self.assertFalse(self.check()["design_ready"])
        self.record["design_views"]["state_model"] = {"requirement": "not_applicable", "reason": ""}
        self.assertFalse(self.check()["structure_valid"])

    def test_only_selected_blocking_unsettled_rules_block_the_design_gate(self):
        self.record["rules"].append({"id": "R-OTHER", "text": "Unrelated branch", "status": "open", "source": "Input", "blocks_completion": True})
        result = self.check()
        self.assertTrue(result["design_ready"])
        self.assertFalse(result["record_ready"])
        self.record["design_views"]["rule_ids"].append("R-OTHER")
        self.assertFalse(self.check()["design_ready"])
        self.record["rules"][-1]["blocks_completion"] = False
        self.assertTrue(self.check()["design_ready"])

    def test_detailed_scope_requires_rule_references_but_lightweight_can_explain_omission(self):
        bundle = self.record["design_views"]
        bundle["rule_ids"] = []
        self.assertFalse(self.check()["design_ready"])
        bundle.update(profile="lightweight", reason="A bounded change reuses the inspected contract", views=[])
        bundle["consistency_review"]["view_ids"] = []
        self.assertTrue(self.check()["design_ready"])
        bundle["reason"] = ""
        self.assertFalse(self.check()["structure_valid"])

    def test_reused_sources_and_passed_view_evidence_are_required(self):
        item = self.record["design_views"]["views"][0]
        item["status"] = "reused"
        self.assertTrue(self.check()["design_ready"])
        item["evidence_ids"] = []
        self.assertFalse(self.check()["design_ready"])
        item["evidence_ids"] = ["E-REVIEW"]
        (self.root / "class.puml").unlink()
        self.assertFalse(self.check()["structure_valid"])

    def test_structure_evidence_can_support_a_view_but_not_replace_consistency_review(self):
        self.record["evidence"][0]["kind"] = "structure"
        self.assertFalse(self.check()["design_ready"])
        self.record["evidence"].append({"id": "E-CONSISTENCY", "kind": "manual_review", "method": "inspection", "status": "passed", "summary": "Actual declared cross-view inspection", "artifact": "review.md"})
        self.record["design_views"]["consistency_review"]["evidence_ids"] = ["E-CONSISTENCY"]
        self.assertTrue(self.check()["design_ready"])

    def test_consistency_review_covers_active_views_and_has_no_unresolved_issues(self):
        review = self.record["design_views"]["consistency_review"]
        review["view_ids"] = ["V-CLASS"]
        self.assertFalse(self.check()["design_ready"])
        review["view_ids"].append("V-SEQUENCE")
        review["unresolved_issues"] = ["A message has no allocated operation"]
        self.assertFalse(self.check()["design_ready"])
        review["unresolved_issues"] = []
        review["status"] = "pending"
        self.assertFalse(self.check()["design_ready"])
        review["status"] = "completed"
        review["unresolved_issues"] = [""]
        self.assertFalse(self.check()["structure_valid"])

    def test_skipped_views_cannot_claim_produced_sources_or_evidence(self):
        self.record["design_views"]["views"].append(self.view("V-OTHER", "other", "skipped"))
        self.assertFalse(self.check()["structure_valid"])
        item = self.record["design_views"]["views"][-1]
        item.pop("artifact")
        item["evidence_ids"] = []
        self.assertTrue(self.check()["design_ready"])

    def test_sources_may_share_a_document_with_identified_sections(self):
        for item in self.record["design_views"]["views"]:
            item["artifact"] = "review.md"
        self.assertTrue(self.check()["design_ready"])

    def test_unknown_references_duplicate_ids_and_unknown_fields_are_rejected(self):
        original = copy.deepcopy(self.record)
        mutations = [
            lambda b: b["rule_ids"].append("R-MISSING"),
            lambda b: b["views"][0].update(id="R1"),
            lambda b: b["views"][1].update(id="V-CLASS"),
            lambda b: b["views"][0]["evidence_ids"].append("E-MISSING"),
            lambda b: b["consistency_review"]["view_ids"].append("V-MISSING"),
            lambda b: b.update(unknown=True)]
        for offset, mutate in enumerate(mutations):
            with self.subTest(mutation=offset):
                self.record = copy.deepcopy(original)
                mutate(self.record["design_views"])
                self.assertFalse(self.check()["structure_valid"])

    def test_optional_preview_must_exist_and_paths_stay_inside_the_root(self):
        item = self.record["design_views"]["views"][0]
        item["preview_artifact"] = "preview.svg"
        self.assertTrue(self.check()["design_ready"])
        for path in ("missing.svg", "../outside.svg", str(self.root / "preview.svg")):
            with self.subTest(path=path):
                item["preview_artifact"] = path
                self.assertFalse(self.check()["structure_valid"])

    def test_view_symlink_loop_reports_a_structured_failure(self):
        path = self.root / "loop.puml"
        try:
            path.symlink_to("loop.puml")
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable")
        self.record["design_views"]["views"][0]["artifact"] = "loop.puml"
        result = self.invoke("--require-design")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["design_ready"])
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_bundle_values_report_errors_without_crashing(self):
        original = copy.deepcopy(self.record)
        mutations = [None, False, [], {"profile": "detailed"}]
        for value in mutations:
            with self.subTest(bundle=value):
                self.record = copy.deepcopy(original)
                self.record["design_views"] = value
                result = self.check()
                self.assertFalse(result["structure_valid"])
                self.assertFalse(result["design_ready"])
        for key in ("rule_ids", "views", "state_model", "consistency_review"):
            with self.subTest(field=key):
                self.record = copy.deepcopy(original)
                self.record["design_views"][key] = 5
                self.assertFalse(self.check()["structure_valid"])

    def test_gate_does_not_execute_recorded_commands(self):
        marker = self.root / "executed"
        self.record["evidence"][1]["command"] = str(marker)
        result = self.invoke("--require-design", "--require-ready")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())

    def test_malformed_view_and_review_fields_are_structured_errors(self):
        original = copy.deepcopy(self.record)
        for target, key, value in (("view", "kind", []), ("view", "id", {}),
                                   ("view", "status", []), ("view", "evidence_ids", {}),
                                   ("view", "artifact", True), ("review", "view_ids", [False]),
                                   ("review", "unresolved_issues", {})):
            with self.subTest(target=target, key=key):
                self.record = copy.deepcopy(original)
                bundle = self.record["design_views"]
                item = bundle["views"][0] if target == "view" else bundle["consistency_review"]
                item[key] = value
                result = self.check()
                self.assertFalse(result["structure_valid"])
                self.assertFalse(result["design_ready"])


if __name__ == "__main__":
    unittest.main()
