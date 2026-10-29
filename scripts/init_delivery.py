#!/usr/bin/env python3
"""Create an optional delivery record from packaged templates; never overwrite files."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[1] / "assets" / "templates"


def initialize(destination: Path, task_id: str, summary: str, intent: str, with_brief=False,
               design_profile: str | None = None):
    if not task_id.strip() or not summary.strip():
        raise ValueError("Task ID and summary must be nonempty.")
    if intent not in ("implement", "design", "review"):
        raise ValueError("Unsupported intent.")
    if design_profile not in (None, "detailed", "lightweight"):
        raise ValueError("Unsupported design profile.")
    record = json.loads((ASSETS / "delivery-record.json").read_text(encoding="utf-8"))
    record["task"].update(id=task_id, summary=summary, intent=intent)
    if design_profile is not None:
        bundle = json.loads((ASSETS / "design-views.json").read_text(encoding="utf-8"))
        bundle["profile"] = design_profile
        record["design_views"] = bundle
    outputs = {"delivery-record.json": json.dumps(record, ensure_ascii=False, indent=2) + "\n"}
    if with_brief:
        outputs["implementation-brief.md"] = (ASSETS / "implementation-brief.md").read_text(encoding="utf-8")
    # Finish encoding before filesystem mutations, so invalid text leaves no output.
    outputs = {name: content.encode("utf-8") for name, content in outputs.items()}
    destination.mkdir(parents=True, exist_ok=True)
    targets = [destination / name for name in outputs]
    if any(path.exists() or path.is_symlink() for path in targets):
        raise FileExistsError("A requested output already exists; choose another directory or edit it in place.")
    created = []
    try:
        for path, content in zip(targets, outputs.values()):
            with path.open("xb") as stream:
                created.append(path)
                stream.write(content)
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise
    return targets


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--id", required=True, dest="task_id")
    parser.add_argument("--summary", required=True)
    parser.add_argument("--intent", choices=("implement", "design", "review"), default="implement")
    parser.add_argument("--with-brief", action="store_true")
    parser.add_argument("--design-profile", choices=("detailed", "lightweight"),
                        help="Add an explicit, unready design-view draft; omitted for legacy records.")
    args = parser.parse_args(argv)
    try:
        for path in initialize(args.destination, args.task_id, args.summary, args.intent,
                               args.with_brief, args.design_profile):
            print(path)
    except (OSError, ValueError) as exc:
        print(f"Cannot initialize: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
