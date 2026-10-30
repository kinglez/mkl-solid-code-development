#!/usr/bin/env python3
"""Check required workflow skill definitions in explicit local skill roots.

Read-only: no installation, overwrite, network access, or skill execution.
Exit: 0 selected definitions present; 1 missing/invalid definitions; 2 invalid input.
This does not prove agent activation, repository setup, or upstream provenance.
Requires PyYAML 6.x to parse the actual frontmatter safely.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    yaml = None


if yaml is not None:
    class UniqueKeysSafeLoader(yaml.SafeLoader):
        """Preserve SafeLoader semantics while rejecting explicit duplicate keys."""

        def construct_mapping(self, node, deep=False):
            if isinstance(node, yaml.MappingNode):
                seen = set()
                for key_node, _ in node.value:
                    if key_node.tag == "tag:yaml.org,2002:merge":
                        continue
                    key = self.construct_object(key_node, deep=deep)
                    try:
                        duplicate = key in seen
                        seen.add(key)
                    except TypeError as exc:
                        raise yaml.constructor.ConstructorError(
                            "while constructing a mapping", node.start_mark,
                            "found an unhashable mapping key", key_node.start_mark) from exc
                    if duplicate:
                        raise yaml.constructor.ConstructorError(
                            "while constructing a mapping", node.start_mark,
                            f"found duplicate key: {key!r}", key_node.start_mark)
            return super().construct_mapping(node, deep=deep)

# Historical public constant retained for explicit core-profile compatibility.
REQUIRED_SKILLS = (
    "setup-matt-pocock-skills",
    "grill-with-docs",
    "grilling",
    "domain-modeling",
    "mkl-uml-robustness-diagram",
    "codebase-design",
    "to-spec",
    "to-tickets",
    "implement",
    "tdd",
    "code-review",
    "improve-codebase-architecture",
)

DETAILED_DESIGN_SKILLS = ("mkl-uml-design-class-model", "mkl-uml-sequence-diagram")

ADDITIONAL_WORKFLOW_SKILLS = (
    "mkl-use-case-specifier",
    "mkl-uml-use-case-diagram",
    "mkl-uml-domain-modeler",
    "mkl-pdr-review",
    "mkl-cdr-review",
)
FULL_WORKFLOW_SKILLS = REQUIRED_SKILLS + DETAILED_DESIGN_SKILLS + ADDITIONAL_WORKFLOW_SKILLS
PROFILES = {
    "full-workflow": FULL_WORKFLOW_SKILLS,
    "core": REQUIRED_SKILLS,
    "detailed-design": REQUIRED_SKILLS + DETAILED_DESIGN_SKILLS,
}


def check(roots: list[Path], profile: str = "full-workflow") -> dict:
    if yaml is None:
        raise ValueError("Prerequisite checking requires PyYAML 6.x; install this skill's requirements.txt.")
    if profile not in PROFILES:
        raise ValueError("Expected profile full-workflow, core, or detailed-design.")
    required = PROFILES[profile]
    if not roots:
        raise ValueError("Provide at least one skill root.")
    for root in roots:
        if not root.is_dir():
            raise ValueError(f"Skill root is not a directory: {root}")
    present, missing = [], []
    for name in required:
        attempts = []
        for root in roots:
            path = root / name / "SKILL.md"
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
                if not lines or lines[0].strip() != "---":
                    raise ValueError("Missing YAML frontmatter.")
                end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
                if end is None:
                    raise ValueError("Unterminated YAML frontmatter.")
                try:
                    frontmatter = yaml.load("\n".join(lines[1:end]), Loader=UniqueKeysSafeLoader)
                except (yaml.YAMLError, RecursionError) as exc:
                    raise ValueError(f"Invalid YAML frontmatter: {exc}") from exc
                if not isinstance(frontmatter, dict) or frontmatter.get("name") != name:
                    raise ValueError(f"Expected a single frontmatter name: {name}")
            except (OSError, UnicodeError, ValueError) as exc:
                attempts.append({"path": str(path), "reason": str(exc)})
                continue
            present.append({"name": name, "path": str(path.resolve())})
            break
        else:
            missing.append({"name": name, "checked": attempts})
    return {
        "profile": profile,
        "prerequisites_present": not missing,
        "required_count": len(required),
        "present": present,
        "missing": missing,
        "scope": "Readable named definitions only; verify agent activation and repository setup separately.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, action="append", required=True,
                        help="Directory containing skill-name/SKILL.md; repeat to search several roots.")
    parser.add_argument("--profile", choices=tuple(PROFILES), default="full-workflow",
                        help="Default full-workflow checks all 19 definitions. Explicit core (12) and "
                             "detailed-design (14) are legacy diagnostic profiles, not full-workflow readiness.")
    args = parser.parse_args(argv)
    try:
        result = check([path.expanduser() for path in args.skills_root], profile=args.profile)
    except (OSError, ValueError) as exc:
        print(json.dumps({"input_error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["prerequisites_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
