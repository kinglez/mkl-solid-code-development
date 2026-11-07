"""Neutral record protocol checks; these files are not architecture acceptance."""
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
spec = importlib.util.spec_from_file_location("architecture_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ArchitectureViewTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        for name in ("context", "container", "component", "module", "quality", "class", "sequence", "review"):
            (self.root / (name + ".txt")).write_text("Neutral declared artifact; no semantic claim.\n")
        self.record = {
            "schema_version": 1,
            "task": {"id": "T", "intent": "design", "summary": "Inspect a scoped structure", "status": "in_progress"},
            "rules": [{"id": "R", "text": "A supplied constraint", "source": "Neutral protocol input", "status": "confirmed", "blocks_completion": True}],
            "acceptance": [], "design": [],
            "evidence": [{"id": "E", "kind": "design_review", "method": "inspection", "status": "passed", "artifact": "review.txt", "summary": "Declared inspection for protocol tests"}],
            "review": {"status": "not_run", "evidence_ids": [], "findings": []}, "limitations": [],
            "architecture_views": {
                "profile": "system", "reason": "System boundary and application responsibilities",
                "rule_ids": ["R"], "views": [self.view("C", "context"), self.view("N", "container"), self.view("Q", "quality")],
                "consistency_review": {"status": "completed", "view_ids": ["C", "N", "Q"], "evidence_ids": ["E"], "notes": "Declared scope, qualities and cross-view inspection", "unresolved_issues": []}}}

    def view(self, identifier, kind):
        return {"id": identifier, "kind": kind, "status": "completed", "artifact": kind + ".txt", "evidence_ids": ["E"], "notes": "Current source inspected within scope"}

    def check(self, **options):
        return validator.validate(self.record, self.root, **options)

    def invoke(self, *options):
        target = self.root / "record.json"
        target.write_text(json.dumps(self.record))
        return subprocess.run([sys.executable, str(SCRIPT), str(target), *options], capture_output=True, text=True)

    def add_design(self):
        self.record["design_views"] = {
            "profile": "detailed", "reason": "Refine current architecture responsibilities", "rule_ids": ["R"],
            "architecture_view_ids": ["C", "N", "Q"],
            "state_model": {"requirement": "not_applicable", "reason": "No lifecycle in this protocol scope"},
            "views": [self.view("D", "class"), self.view("S", "sequence")],
            "consistency_review": {"status": "completed", "view_ids": ["D", "S"], "evidence_ids": ["E"], "notes": "Declared refinement and allocation review", "unresolved_issues": []}}

    def test_architecture_only_gate_does_not_require_detailed_design_or_code(self):
        result = self.invoke("--require-architecture")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["architecture_ready"])
        self.assertFalse(payload["record_ready"])
        self.assertIsNone(payload["design_ready"])

    def test_missing_architecture_bundle_is_not_silently_accepted(self):
        self.record.pop("architecture_views")
        result = self.invoke("--require-architecture")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["architecture_ready"])

    def test_system_scope_requires_context_container_and_quality_outputs(self):
        original = copy.deepcopy(self.record)
        for kind in ("context", "container", "quality"):
            with self.subTest(missing=kind):
                self.record = copy.deepcopy(original)
                bundle = self.record["architecture_views"]
                bundle["views"] = [v for v in bundle["views"] if v["kind"] != kind]
                bundle["consistency_review"]["view_ids"] = [v["id"] for v in bundle["views"]]
                self.assertFalse(self.check()["architecture_ready"])

    def test_bounded_scope_uses_a_module_without_inventing_a_system(self):
        bundle = self.record["architecture_views"]
        bundle.update(profile="bounded", reason="A bounded module, without a new deployed system",
                      views=[self.view("M", "module"), self.view("Q", "quality")])
        bundle["consistency_review"]["view_ids"] = ["M", "Q"]
        self.assertTrue(self.check()["architecture_ready"])
        bundle["views"].pop(0)
        bundle["consistency_review"]["view_ids"] = ["Q"]
        self.assertFalse(self.check()["architecture_ready"])

    def test_lightweight_scope_still_records_quality_and_review(self):
        bundle = self.record["architecture_views"]
        bundle.update(profile="lightweight", reason="Checked existing architecture; a bounded delta",
                      views=[self.view("Q", "quality")])
        bundle["consistency_review"]["view_ids"] = ["Q"]
        self.assertTrue(self.check()["architecture_ready"])
        bundle["views"] = []
        bundle["consistency_review"]["view_ids"] = []
        self.assertFalse(self.check()["architecture_ready"])

    def test_unsettled_architecture_decisions_block_but_not_unrelated_future_rules(self):
        self.record["rules"].append({"id": "LATER", "text": "Outside the selected scope", "source": "Input", "status": "open", "blocks_completion": False})
        self.assertTrue(self.check()["architecture_ready"])
        self.record["architecture_views"]["rule_ids"].append("LATER")
        self.assertFalse(self.check()["architecture_ready"])

    def test_pending_invalidated_or_unreviewed_architecture_cannot_feed_design(self):
        self.add_design()
        original = copy.deepcopy(self.record)
        for status in ("pending", "invalidated", "blocked"):
            with self.subTest(status=status):
                self.record = copy.deepcopy(original)
                self.record["architecture_views"]["views"][0]["status"] = status
                result = self.invoke("--require-design")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertFalse(json.loads(result.stdout)["design_ready"])
        self.record = copy.deepcopy(original)
        self.record["architecture_views"]["consistency_review"]["unresolved_issues"] = ["A necessary ownership decision remains open"]
        self.assertFalse(self.check()["design_ready"])

    def test_design_must_account_for_current_architecture_outputs(self):
        self.add_design()
        self.assertTrue(self.check()["design_ready"])
        for mapping in ([], ["C", "N"], ["UNKNOWN"]):
            with self.subTest(mapping=mapping):
                self.record["design_views"]["architecture_view_ids"] = mapping
                self.assertFalse(self.check()["design_ready"])

    def test_design_architecture_ids_cannot_be_supplied_without_their_bundle(self):
        self.add_design()
        self.record.pop("architecture_views")
        self.assertFalse(self.check()["structure_valid"])

    def test_legacy_design_retains_its_original_narrow_gate(self):
        self.add_design()
        self.record.pop("architecture_views")
        self.record["design_views"].pop("architecture_view_ids")
        result = self.check(require_design=True)
        self.assertTrue(result["design_ready"])
        self.assertIsNone(result["architecture_ready"])

    def test_explicit_integrated_gate_does_not_accept_a_legacy_design_as_architecture(self):
        self.add_design()
        self.record.pop("architecture_views")
        self.record["design_views"].pop("architecture_view_ids")
        self.assertEqual(self.invoke("--require-design").returncode, 0)
        result = self.invoke("--require-architecture", "--require-design")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["architecture_ready"])

    def test_architecture_exit_can_precede_a_declared_future_detailed_design(self):
        self.add_design()
        self.record["design_views"]["views"][0]["status"] = "pending"
        result = self.invoke("--require-architecture")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["architecture_ready"])
        self.assertFalse(payload["design_ready"])
        self.assertEqual(self.invoke("--require-architecture", "--require-design").returncode, 1)

    def test_architecture_ids_are_unique_across_bundles(self):
        self.add_design()
        self.record["design_views"]["views"][0]["id"] = "C"
        self.assertFalse(self.check()["structure_valid"])

    def test_artifact_paths_and_malformed_values_fail_without_a_traceback(self):
        original = copy.deepcopy(self.record)
        for value in (None, [], False, {"profile": "system"}):
            with self.subTest(bundle=value):
                self.record = copy.deepcopy(original)
                self.record["architecture_views"] = value
                self.assertFalse(self.check()["structure_valid"])
        for value in ("missing.txt", "../outside.txt", str(self.root / "context.txt")):
            with self.subTest(path=value):
                self.record = copy.deepcopy(original)
                self.record["architecture_views"]["views"][0]["artifact"] = value
                result = self.invoke("--require-architecture")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_ready_prefix_and_architecture_gate_allow_future_work_but_invalidate_together(self):
        self.record["handoffs"] = []
        for n in range(1, 9):
            ready = n <= 4
            self.record["handoffs"].append({"id": f"H{n}", "stage": f"Scoped stage {n}",
                "status": "completed" if ready else "pending", "input_ids": [f"O{n-1}"] if n > 1 else [],
                "outputs": [{"id": f"O{n}", "summary": "Declared artifact; status controls usability", "artifact": "review.txt"}],
                "notes": "Source-based scoped stage with declared inputs"})
        result = self.invoke("--require-architecture", "--require-through", "H4")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.record["handoffs"][2]["status"] = "invalidated"
        self.assertEqual(self.invoke("--require-architecture", "--require-through", "H4").returncode, 1)
        self.record["handoffs"][2]["status"] = "reused"
        self.assertEqual(self.invoke("--require-architecture", "--require-through", "H4").returncode, 0)


if __name__ == "__main__":
    unittest.main()
