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

    def test_invalid_definitions_do_not_count_as_installed(self):
        for content in ("", "name: tdd", "---\nname: tdd\n", "---\nname: another-skill\n---\n",
                        "---\nname: tdd\nname: tdd\n---\n"):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                install(root, checker.REQUIRED_SKILLS)
                (root / "tdd/SKILL.md").write_text(content)
                self.assertFalse(checker.check([root])["prerequisites_present"])

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
