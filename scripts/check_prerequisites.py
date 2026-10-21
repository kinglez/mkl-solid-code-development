#!/usr/bin/env python3
"""Check required Matt Pocock skill definitions in explicit local skill roots.

Read-only: no installation, overwrite, network access, or skill execution.
Exit: 0 all definitions present; 1 missing/invalid definitions; 2 invalid input.
This does not prove agent activation, repository setup, or upstream provenance.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

REQUIRED_SKILLS = (
    "setup-matt-pocock-skills",
    "grill-with-docs",
    "grilling",
    "domain-modeling",
    "codebase-design",
    "to-spec",
    "to-tickets",
    "implement",
    "tdd",
    "code-review",
    "improve-codebase-architecture",
)


def check(roots: list[Path]) -> dict:
    if not roots:
        raise ValueError("Provide at least one skill root.")
    for root in roots:
        if not root.is_dir():
            raise ValueError(f"Skill root is not a directory: {root}")
    present, missing = [], []
    for name in REQUIRED_SKILLS:
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
                names = []
                for line in lines[1:end]:
                    match = re.fullmatch(r"name:[ \t]*([\"']?)([a-z0-9-]+)\1[ \t]*(?:#.*)?", line)
                    if match:
                        names.append(match.group(2))
                if names != [name]:
                    raise ValueError(f"Expected a single frontmatter name: {name}")
            except (OSError, UnicodeError, ValueError) as exc:
                attempts.append({"path": str(path), "reason": str(exc)})
                continue
            present.append({"name": name, "path": str(path.resolve())})
            break
        else:
            missing.append({"name": name, "checked": attempts})
    return {
        "prerequisites_present": not missing,
        "required_count": len(REQUIRED_SKILLS),
        "present": present,
        "missing": missing,
        "scope": "Readable named definitions only; verify agent activation and repository setup separately.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-root", type=Path, action="append", required=True,
                        help="Directory containing skill-name/SKILL.md; repeat to search several roots.")
    args = parser.parse_args(argv)
    try:
        result = check([path.expanduser() for path in args.skills_root])
    except (OSError, ValueError) as exc:
        print(json.dumps({"input_error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["prerequisites_present"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
