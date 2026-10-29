"""Behavioral checks for prerequisite discovery and honest failure reporting."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_prerequisites", ROOT / "scripts/check_prerequisites.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


def install(root, names):
    for name in names:
        target = root / name / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"---\nname: {name}\ndescription: Synthetic test fixture\n---\n", encoding="utf-8")


class PrerequisiteTests(unittest.TestCase):
    def test_complete_installation_is_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, checker.REQUIRED_SKILLS)
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}
            result = checker.check([root])
            self.assertTrue(result["prerequisites_present"])
            self.assertEqual(len(result["present"]), len(checker.REQUIRED_SKILLS))
            self.assertEqual(result["missing"], [])
            self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()})

    def test_one_missing_definition_fails_without_installing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, [name for name in checker.REQUIRED_SKILLS if name != "tdd"])
            result = checker.check([root])
            self.assertFalse(result["prerequisites_present"])
            self.assertEqual([item["name"] for item in result["missing"]], ["tdd"])
            self.assertFalse((root / "tdd").exists())

    def test_robustness_skill_is_required_even_when_all_matt_skills_are_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, [name for name in checker.REQUIRED_SKILLS if name != "mkl-uml-robustness-diagram"])
            result = checker.check([root])
            self.assertFalse(result["prerequisites_present"])
            self.assertEqual([item["name"] for item in result["missing"]], ["mkl-uml-robustness-diagram"])
            install(root, ["mkl-uml-robustness-diagram"])
            self.assertTrue(checker.check([root])["prerequisites_present"])

    def test_detailed_design_profile_requires_class_and_sequence_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, checker.REQUIRED_SKILLS)
            self.assertTrue(checker.check([root])["prerequisites_present"])
            result = checker.check([root], profile="detailed-design")
            self.assertFalse(result["prerequisites_present"])
            self.assertEqual(result["required_count"], 14)
            self.assertEqual({item["name"] for item in result["missing"]},
                             {"mkl-uml-design-class-model", "mkl-uml-sequence-diagram"})
            install(root, ["mkl-uml-design-class-model", "mkl-uml-sequence-diagram"])
            self.assertTrue(checker.check([root], profile="detailed-design")["prerequisites_present"])
            self.assertEqual(checker.check([root])["required_count"], 12)

    def test_profile_cli_checks_selected_capabilities_and_rejects_unknown_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, checker.REQUIRED_SKILLS)
            command = [sys.executable, str(ROOT / "scripts/check_prerequisites.py"),
                       "--skills-root", str(root), "--profile", "detailed-design"]
            missing = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertEqual(json.loads(missing.stdout)["profile"], "detailed-design")
            install(root, ["mkl-uml-design-class-model", "mkl-uml-sequence-diagram"])
            present = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(present.returncode, 0)
            self.assertEqual(json.loads(present.stdout)["required_count"], 14)
            with self.assertRaises(ValueError):
                checker.check([root], profile="unknown")

    def test_invalid_definitions_do_not_count_as_installed(self):
        for content in ("", "name: tdd", "---\nname: tdd\n", "---\nname: another-skill\n---\n",
                        "---\nname: tdd\nname: tdd\n---\n"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                install(root, checker.REQUIRED_SKILLS)
                (root / "tdd/SKILL.md").write_text(content)
                self.assertFalse(checker.check([root])["prerequisites_present"])

    def test_actual_yaml_names_and_invalid_yaml_are_not_misreported(self):
        headers = (
            "name: tdd#other-name\ndescription: Fixture\n",
            'name: tdd\ndescription: "unterminated\n',
            'name: tdd\n"name": another-skill\n',
            "name: tdd\ndescription: First\ndescription: Second\n",
            "name: [tdd]\n",
            "- name: tdd\n",
            "name: !!python/object/new:builtins.str []\n",
        )
        for header in headers:
            with self.subTest(header=header), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                install(root, checker.REQUIRED_SKILLS)
                (root / "tdd/SKILL.md").write_text("---\n" + header + "---\n", encoding="utf-8")
                result = checker.check([root])
                self.assertFalse(result["prerequisites_present"])
                self.assertEqual([item["name"] for item in result["missing"]], ["tdd"])

    def test_valid_yaml_string_forms_are_understood(self):
        for header in ('"name": tdd\n', "name: !!str tdd\n", "name: tdd # comment\n",
                       "{name: tdd, description: Fixture}\n", "name: >-\n  tdd\n",
                       "defaults: &defaults\n  name: other\n<<: *defaults\nname: tdd\n"):
            with self.subTest(header=header), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                install(root, checker.REQUIRED_SKILLS)
                (root / "tdd/SKILL.md").write_text("---\n" + header + "---\n", encoding="utf-8")
                self.assertTrue(checker.check([root])["prerequisites_present"])

    def test_excessive_yaml_nesting_is_reported_as_invalid_definition(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            install(root, checker.REQUIRED_SKILLS)
            header = "name: tdd\ndescription: " + "[" * 600 + "0" + "]" * 600 + "\n"
            (root / "tdd/SKILL.md").write_text("---\n" + header + "---\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/check_prerequisites.py"),
                                     "--skills-root", str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(result.stderr, "")
            report = json.loads(result.stdout)
            self.assertFalse(report["prerequisites_present"])
            self.assertEqual([item["name"] for item in report["missing"]], ["tdd"])

    def test_missing_yaml_dependency_is_structured_input_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, "-S", str(ROOT / "scripts/check_prerequisites.py"), "--skills-root", tmp]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("PyYAML", json.loads(result.stderr)["input_error"])
            self.assertEqual(result.stdout, "")

    def test_skills_can_be_split_across_roots_with_quoted_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first", Path(tmp) / "second"
            first.mkdir()
            second.mkdir()
            install(first, checker.REQUIRED_SKILLS[::2])
            install(second, checker.REQUIRED_SKILLS[1::2])
            path = first / checker.REQUIRED_SKILLS[0] / "SKILL.md"
            path.write_text(f"---\nname: '{checker.REQUIRED_SKILLS[0]}' # fixture\n---\n")
            self.assertTrue(checker.check([first, second])["prerequisites_present"])

    def test_valid_second_definition_can_follow_invalid_first_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            first, second = Path(tmp) / "first", Path(tmp) / "second"
            first.mkdir()
            second.mkdir()
            install(first, checker.REQUIRED_SKILLS)
            (first / "tdd/SKILL.md").write_text("broken")
            install(second, ["tdd"])
            result = checker.check([first, second])
            self.assertTrue(result["prerequisites_present"])
            self.assertEqual(next(item["path"] for item in result["present"] if item["name"] == "tdd"),
                             str((second / "tdd/SKILL.md").resolve()))

    def test_empty_or_invalid_roots_are_input_errors(self):
        with self.assertRaises(ValueError):
            checker.check([])
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                checker.check([Path(tmp) / "missing"])

    def test_cli_exit_codes_distinguish_complete_missing_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            command = [sys.executable, str(ROOT / "scripts/check_prerequisites.py"), "--skills-root", str(root)]
            missing = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertFalse(json.loads(missing.stdout)["prerequisites_present"])
            install(root, checker.REQUIRED_SKILLS)
            ready = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(ready.returncode, 0)
            self.assertTrue(json.loads(ready.stdout)["prerequisites_present"])
            invalid = subprocess.run(command[:-1] + [str(root / "missing")], capture_output=True, text=True)
            self.assertEqual(invalid.returncode, 2)
            self.assertIn("input_error", json.loads(invalid.stderr))


if __name__ == "__main__":
    unittest.main()
