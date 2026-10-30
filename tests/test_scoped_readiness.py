"""Check ready stage prefixes through public CLI/API with neutral protocol data."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_delivery.py"
FIXTURES = ROOT / "tests/fixtures"
spec = importlib.util.spec_from_file_location("scoped_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ScopedReadinessTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        shutil.copytree(FIXTURES / "evidence", self.root / "evidence")
        self.record = validator.load_record(FIXTURES / "ready.json")
        self.record["task"]["status"] = "in_progress"
        self.record["review"] = {"status": "not_run", "evidence_ids": [], "findings": []}
        self.record["handoffs"] = [self.stage(index) for index in range(1, 8)]
        for name in ("structure.puml", "interaction.puml"):
            (self.root / name).write_text("Neutral declared source for protocol validation.\n", encoding="utf-8")
        self.record["design_views"] = {
            "profile": "detailed", "reason": "Inspect a bounded protocol handoff", "rule_ids": ["R1"],
            "state_model": {"requirement": "not_applicable", "reason": "No lifecycle within this neutral scope"},
            "views": [
                {"id": "VS", "kind": "class", "status": "completed", "notes": "Declared source",
                 "artifact": "structure.puml", "evidence_ids": ["E2"]},
                {"id": "VI", "kind": "sequence", "status": "completed", "notes": "Declared source",
                 "artifact": "interaction.puml", "evidence_ids": ["E2"]}],
            "consistency_review": {"status": "completed", "view_ids": ["VS", "VI"],
                                   "evidence_ids": ["E2"], "notes": "Declared neutral inspection",
                                   "unresolved_issues": []}}

    def stage(self, index, ready=None):
        ready = index <= 4 if ready is None else ready
        return {"id": f"H{index}", "stage": f"Arbitrary phase {index}",
                "status": "completed" if ready else "pending",
                "input_ids": [f"O{index - 1}"] if ready and index > 1 else [],
                "outputs": [{"id": f"O{index}", "summary": "Neutral usable result",
                             "artifact": "evidence/inspection.md"}] if ready else [],
                "notes": "Source and consumer readiness are recorded for the scoped protocol."}

    def invoke(self, *flags):
        record = self.root / "record.json"
        record.write_text(json.dumps(self.record), encoding="utf-8")
        return subprocess.run([sys.executable, "-B", str(SCRIPT), str(record), *flags],
                              capture_output=True, text=True)

    def check(self, target="H4"):
        return validator.validate(self.record, self.root, require_through=target)

    def test_ready_prefix_allows_pending_future_work_and_incomplete_final_review(self):
        process = self.invoke("--require-design", "--require-through", "H4")
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertTrue(result["structure_valid"])
        self.assertTrue(result["design_ready"])
        self.assertTrue(result["through_ready"])
        self.assertEqual(result["through_blockers"], [])
        self.assertFalse(result["record_ready"])

    def test_scoped_gate_is_not_claimed_when_not_requested(self):
        result = validator.validate(self.record, self.root)
        self.assertIsNone(result["through_ready"])
        self.assertEqual(result["through_blockers"], [])

    def test_invalidated_or_blocked_input_stops_prefix_until_repaired(self):
        for status in ("pending", "blocked", "invalidated"):
            with self.subTest(status=status):
                self.record["handoffs"][2]["status"] = status
                process = self.invoke("--require-design", "--require-through", "H4")
                self.assertEqual(process.returncode, 1, process.stderr)
                result = json.loads(process.stdout)
                self.assertTrue(result["design_ready"])
                self.assertFalse(result["through_ready"])
                self.assertIn("HANDOFF_INPUT_NOT_READY", {b["code"] for b in result["through_blockers"]})
                self.record["handoffs"][2]["status"] = "completed"
                restored = self.invoke("--require-design", "--require-through", "H4")
                self.assertEqual(restored.returncode, 0, restored.stderr)
                self.assertFalse(json.loads(restored.stdout)["record_ready"])

    def test_target_must_be_completed_or_reused(self):
        for status in ("pending", "blocked", "invalidated", "skipped"):
            with self.subTest(status=status):
                self.record["handoffs"][3] = self.stage(4)
                self.record["handoffs"][3]["status"] = status
                if status == "skipped":
                    self.record["handoffs"][3]["outputs"] = []
                result = self.invoke("--require-through", "H4")
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertFalse(json.loads(result.stdout)["through_ready"])

    def test_missing_or_invalid_target_is_an_explicit_gate_failure(self):
        for target in ("MISSING", "", "  "):
            with self.subTest(target=target):
                result = self.invoke("--require-through", target)
                self.assertEqual(result.returncode, 1, result.stderr)
                payload = json.loads(result.stdout)
                self.assertFalse(payload["through_ready"])
                self.assertTrue(payload["through_blockers"])

    def test_missing_handoffs_cannot_satisfy_the_prefix_gate(self):
        del self.record["handoffs"]
        result = self.invoke("--require-through", "H4")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertFalse(json.loads(result.stdout)["through_ready"])

    def test_prefix_needs_real_outputs_and_predecessor_links(self):
        original = copy.deepcopy(self.record)
        for missing in ("output", "link"):
            with self.subTest(missing=missing):
                self.record = copy.deepcopy(original)
                stage = self.record["handoffs"][3]
                stage["outputs" if missing == "output" else "input_ids"] = []
                result = self.check()
                self.assertTrue(result["structure_valid"])
                self.assertFalse(result["through_ready"])
                self.assertIn("HANDOFF_OUTPUT_REQUIRED" if missing == "output" else "HANDOFF_NOT_CONNECTED",
                              {b["code"] for b in result["through_blockers"]})

    def test_self_forward_and_unknown_references_do_not_pass_the_prefix(self):
        for input_id in ("O4", "O3", "UNKNOWN"):
            with self.subTest(input_id=input_id):
                self.record["handoffs"][1]["input_ids"] = [input_id]
                result = self.check()
                self.assertFalse(result["structure_valid"])
                self.assertFalse(result["through_ready"])

    def test_missing_artifact_cannot_pass_the_prefix(self):
        self.record["handoffs"][3]["outputs"][0]["artifact"] = "missing.md"
        result = self.check()
        self.assertFalse(result["structure_valid"])
        self.assertFalse(result["through_ready"])
        self.assertIn("HANDOFF_ARTIFACT_MISSING", {e["code"] for e in result["errors"]})

    def test_reused_outputs_and_justified_skips_preserve_the_active_chain(self):
        self.record["handoffs"][2]["status"] = "reused"
        self.record["handoffs"].insert(2, {"id": "HS", "stage": "Unneeded scoped view",
            "status": "skipped", "input_ids": [], "outputs": [], "notes": "No view required in this scope."})
        self.assertTrue(self.check()["through_ready"])

    def test_later_blocked_consumers_do_not_block_the_selected_prefix(self):
        self.record["handoffs"][4].update(status="blocked",
            outputs=[{"id": "O5", "summary": "Unready later result"}], input_ids=["O4"])
        self.record["handoffs"][5]["input_ids"] = ["O5"]
        result = self.check()
        self.assertTrue(result["through_ready"])
        self.assertFalse(result["record_ready"])

    def test_arbitrary_stage_labels_and_historical_stage_count_remain_supported(self):
        self.record["handoffs"] = [self.stage(index, ready=index <= 8) for index in range(1, 13)]
        self.assertTrue(self.check("H8")["through_ready"])
        self.assertFalse(self.check("H8")["record_ready"])

    def test_scoped_and_final_gates_are_cumulative(self):
        for final_flag in ("--require-ready", "--require-handoffs"):
            with self.subTest(flag=final_flag):
                process = self.invoke("--require-design", "--require-through", "H4", final_flag)
                self.assertEqual(process.returncode, 1, process.stderr)
                result = json.loads(process.stdout)
                self.assertTrue(result["through_ready"])
                self.assertTrue(result["design_ready"])
                self.assertFalse(result["record_ready"])

    def test_selected_rule_confirmation_and_prefix_readiness_are_separate_checks(self):
        self.record["rules"][0].update(status="open", blocks_completion=False)
        process = self.invoke("--require-design", "--require-through", "H4")
        self.assertEqual(process.returncode, 1, process.stderr)
        payload = json.loads(process.stdout)
        self.assertTrue(payload["through_ready"])
        self.assertFalse(payload["design_ready"])

    def test_unselected_future_rule_does_not_block_current_combined_gate(self):
        self.record["rules"].append({"id": "R-FUTURE", "text": "Future protocol question",
            "status": "open", "source": "Separate future scope", "blocks_completion": False})
        process = self.invoke("--require-design", "--require-through", "H4")
        self.assertEqual(process.returncode, 0, process.stderr)

    def test_recorded_commands_are_not_executed_by_the_scoped_gate(self):
        marker = self.root / "unexpected"
        self.record["evidence"][0]["command"] = f"touch {marker}"
        result = self.invoke("--require-design", "--require-through", "H4")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
