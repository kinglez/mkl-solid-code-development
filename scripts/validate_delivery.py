#!/usr/bin/env python3
"""Check a delivery record's structure, references, and declared evidence coverage.

Read-only; never runs recorded commands or interprets source code as SOLID proof.
Exit: 0 valid structure (possibly incomplete); 1 invalid or a readiness gate fails;
2 unreadable/invalid JSON or invalid command usage.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_record(path: Path) -> dict:
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def validate(record: object, project_root: Path, require_handoffs: bool = False) -> dict:
    errors, blockers = [], []
    root = project_root.resolve()

    def issue(target, code, location, message):
        target.append({"code": code, "location": location, "message": message})

    def error(code, location, message):
        issue(errors, code, location, message)

    def block(code, location, message):
        issue(blockers, code, location, message)

    def fields(obj, location, required, optional=()):
        if not isinstance(obj, dict):
            error("OBJECT_REQUIRED", location, "Expected a JSON object.")
            return False
        for key in sorted(set(required) - obj.keys()):
            error("MISSING_FIELD", f"{location}.{key}", "Required field is missing.")
        for key in sorted(obj.keys() - set(required) - set(optional)):
            error("UNKNOWN_FIELD", f"{location}.{key}", "Unknown field; check spelling or schema version.")
        return True

    def text(obj, key, location):
        if not isinstance(obj.get(key), str) or not obj[key].strip():
            error("TEXT_REQUIRED", f"{location}.{key}", "Expected nonempty text.")

    def choice(obj, key, values, location):
        if not isinstance(obj.get(key), str) or obj[key] not in values:
            error("INVALID_VALUE", f"{location}.{key}", f"Expected one of: {', '.join(values)}.")

    def boolean(obj, key, location):
        if type(obj.get(key)) is not bool:
            error("BOOLEAN_REQUIRED", f"{location}.{key}", "Expected true or false.")

    def refs(obj, key, targets, location):
        values = obj.get(key)
        if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
            error("REFERENCE_LIST_REQUIRED", f"{location}.{key}", "Expected a list of IDs.")
            return []
        if len(values) != len(set(values)):
            error("DUPLICATE_REFERENCE", f"{location}.{key}", "Repeated ID in the same reference list.")
        for value in values:
            if value not in targets:
                error("UNKNOWN_REFERENCE", f"{location}.{key}", f"Unknown ID: {value}.")
        return [v for v in values if v in targets]

    required_top = ("schema_version", "task", "rules", "acceptance", "design", "evidence", "review", "limitations")
    if not fields(record, "$", required_top, ("handoffs",)):
        return {"structure_valid": False, "record_ready": False, "errors": errors, "blockers": blockers}
    if type(record.get("schema_version")) is not int or record["schema_version"] != 1:
        error("SCHEMA_VERSION", "schema_version", "Only schema_version 1 is supported.")
    task = record.get("task")
    if fields(task, "task", ("id", "intent", "summary", "status")):
        text(task, "id", "task")
        text(task, "summary", "task")
        choice(task, "intent", ("implement", "design", "review"), "task")
        choice(task, "status", ("in_progress", "partial", "complete"), "task")
    else:
        task = {}
    if task.get("status") != "complete":
        block("TASK_INCOMPLETE", "task.status", "The task is not declared complete.")

    ids = set()

    def entries(name, required, optional=()):
        result = {}
        items = record.get(name)
        if not isinstance(items, list):
            error("ARRAY_REQUIRED", name, "Expected a JSON array.")
            return result
        for index, item in enumerate(items):
            loc = f"{name}[{index}]"
            if not fields(item, loc, required, optional):
                continue
            text(item, "id", loc)
            identifier = item.get("id")
            if isinstance(identifier, str) and identifier.strip():
                if identifier in ids:
                    error("DUPLICATE_ID", loc + ".id", f"ID is not unique: {identifier}.")
                else:
                    ids.add(identifier)
                    result[identifier] = item
        return result

    rules = entries("rules", ("id", "text", "status", "source", "blocks_completion"))
    acceptance = entries("acceptance", ("id", "scenario", "expected", "rule_ids", "evidence_ids"))
    design = entries("design", ("id", "decision", "reason", "tradeoffs", "evidence_ids"))
    evidence = entries("evidence", ("id", "kind", "method", "status", "summary"), ("artifact", "command", "exit_code"))
    limitations = entries("limitations", ("id", "description", "blocks_completion"))

    for identifier, rule in rules.items():
        for key in ("text", "source"):
            text(rule, key, identifier)
        choice(rule, "status", ("confirmed", "proposed", "assumed", "open"), identifier)
        boolean(rule, "blocks_completion", identifier)
        if rule.get("status") != "confirmed" and rule.get("blocks_completion") is True:
            block("UNSETTLED_RULE", identifier, "A completion-blocking business rule is not confirmed.")

    passed = set()
    for identifier, item in evidence.items():
        text(item, "summary", identifier)
        choice(item, "kind", ("behavior", "contract", "structure", "manual_review", "design_review"), identifier)
        choice(item, "method", ("command", "inspection"), identifier)
        choice(item, "status", ("passed", "failed", "not_run"), identifier)
        usable = item.get("status") == "passed"
        if "command" in item:
            text(item, "command", identifier)
        if "exit_code" in item and type(item["exit_code"]) is not int:
            error("EXIT_CODE_REQUIRED", identifier + ".exit_code", "Expected an integer exit code.")
            usable = False
        automated = item.get("method") == "command"
        if item.get("method") == "inspection" and ("command" in item or "exit_code" in item):
            error("INSPECTION_HAS_COMMAND", identifier, "Inspection evidence has no command or exit code.")
            usable = False
        if item.get("status") == "passed" and automated:
            text(item, "command", identifier)
            if type(item.get("exit_code")) is not int or item["exit_code"] != 0:
                error("PASS_EXIT_MISMATCH", identifier, "Passed command evidence must have exit_code 0.")
                usable = False
        if item.get("status") == "failed" and item.get("exit_code") == 0:
            error("FAIL_EXIT_MISMATCH", identifier, "Failed command evidence cannot report exit_code 0.")
        if item.get("status") == "not_run" and "exit_code" in item:
            error("NOT_RUN_EXIT_CODE", identifier, "A command that did not run has no exit code.")
        artifact = item.get("artifact")
        if artifact is not None or item.get("status") == "passed":
            if not isinstance(artifact, str) or not artifact.strip():
                error("ARTIFACT_REQUIRED", identifier, "Passed evidence requires a relative artifact path.")
                usable = False
            else:
                try:
                    relative = Path(artifact)
                    resolved = (root / relative).resolve()
                    if relative.is_absolute() or not resolved.is_relative_to(root):
                        error("ARTIFACT_OUTSIDE_ROOT", identifier, "Evidence must stay inside project_root.")
                        usable = False
                    elif not resolved.is_file():
                        error("ARTIFACT_MISSING", identifier, "Evidence artifact does not exist as a file.")
                        usable = False
                except (OSError, ValueError, RuntimeError) as exc:
                    error("ARTIFACT_INVALID", identifier, str(exc))
                    usable = False
        if usable:
            passed.add(identifier)

    covered_rules = set()
    for identifier, case in acceptance.items():
        text(case, "scenario", identifier)
        text(case, "expected", identifier)
        rule_ids = refs(case, "rule_ids", rules, identifier)
        evidence_ids = refs(case, "evidence_ids", evidence, identifier)
        covered_rules.update(rule_ids)
        if not rule_ids:
            block("CASE_WITHOUT_RULE", identifier, "Acceptance case has no business rule reference.")
        if any(rules[r].get("status") != "confirmed" for r in rule_ids):
            block("CASE_USES_UNSETTLED_RULE", identifier, "Acceptance depends on an unconfirmed rule.")
        if task.get("intent") == "implement" and not any(
            e in passed and evidence[e].get("kind") in ("behavior", "contract") for e in evidence_ids
        ):
            block("CASE_WITHOUT_BEHAVIOR_EVIDENCE", identifier, "No passed behavior or contract evidence is linked.")

    for identifier, item in design.items():
        for key in ("decision", "reason", "tradeoffs"):
            text(item, key, identifier)
        linked = refs(item, "evidence_ids", evidence, identifier)
        if not any(e in passed and evidence[e].get("kind") in ("structure", "manual_review", "design_review") for e in linked):
            block("DESIGN_WITHOUT_REVIEW", identifier, "Design decision lacks passed inspection evidence.")

    review = record.get("review")
    if fields(review, "review", ("status", "evidence_ids", "findings")):
        choice(review, "status", ("not_run", "completed"), "review")
        linked = refs(review, "evidence_ids", evidence, "review")
        if review.get("status") != "completed" or not any(
            e in passed and evidence[e].get("kind") in ("structure", "manual_review", "design_review") for e in linked
        ):
            block("REVIEW_INCOMPLETE", "review", "Review needs a completed status and passed inspection evidence.")
        findings = review.get("findings")
        if not isinstance(findings, list):
            error("ARRAY_REQUIRED", "review.findings", "Expected a JSON array.")
            findings = []
        for index, finding in enumerate(findings):
            loc = f"review.findings[{index}]"
            if not fields(finding, loc, ("id", "detail", "required", "status", "evidence_ids")):
                continue
            text(finding, "id", loc)
            text(finding, "detail", loc)
            fid = finding.get("id")
            if isinstance(fid, str) and fid.strip():
                if fid in ids:
                    error("DUPLICATE_ID", loc + ".id", f"ID is not unique: {fid}.")
                ids.add(fid)
            boolean(finding, "required", loc)
            choice(finding, "status", ("open", "resolved", "deferred"), loc)
            linked = refs(finding, "evidence_ids", evidence, loc)
            if finding.get("status") == "resolved" and not any(e in passed for e in linked):
                block("FIX_WITHOUT_EVIDENCE", loc, "Resolved finding lacks passed verification evidence.")
            if task.get("intent") in ("implement", "design") and finding.get("required") is True and finding.get("status") != "resolved":
                block("REQUIRED_FINDING_OPEN", loc, "A required correction remains unresolved.")

    for identifier, item in limitations.items():
        text(item, "description", identifier)
        boolean(item, "blocks_completion", identifier)
        if item.get("blocks_completion") is True:
            block("BLOCKING_LIMITATION", identifier, "A declared limitation blocks completion.")
    if task.get("intent") == "implement":
        if not rules or not acceptance:
            block("IMPLEMENTATION_COVERAGE_EMPTY", "acceptance", "Implementation needs rules and acceptance cases.")
        for identifier, rule in rules.items():
            if rule.get("status") == "confirmed" and identifier not in covered_rules:
                block("RULE_WITHOUT_ACCEPTANCE", identifier, "Confirmed rule lacks acceptance coverage.")
    if task.get("intent") == "design" and not design:
        block("DESIGN_EMPTY", "design", "Design request needs at least one design decision.")

    if require_handoffs and "handoffs" not in record:
        block("HANDOFFS_MISSING", "handoffs", "Stage handoffs are required for this validation.")
    if "handoffs" in record:
        stages = entries("handoffs", ("id", "stage", "status", "input_ids", "outputs", "notes"))
        usable = ("completed", "reused")
        produced = {}
        stage_outputs = {}
        active = []
        for index, (identifier, stage) in enumerate(stages.items()):
            for key in ("stage", "notes"):
                text(stage, key, identifier)
            choice(stage, "status", (*usable, "pending", "blocked", "invalidated", "skipped"), identifier)
            if stage.get("status") != "skipped":
                active.append(identifier)
                if stage.get("status") not in usable:
                    block("HANDOFF_INCOMPLETE", identifier, "The stage output is not ready for handoff.")
            outputs = stage.get("outputs")
            if not isinstance(outputs, list):
                error("ARRAY_REQUIRED", identifier + ".outputs", "Expected a JSON array.")
                outputs = []
            stage_outputs[identifier] = set()
            if stage.get("status") in usable and not outputs:
                block("HANDOFF_OUTPUT_REQUIRED", identifier, "A completed or reused stage needs a usable output.")
            if stage.get("status") == "skipped" and outputs:
                error("SKIPPED_HANDOFF_HAS_OUTPUT", identifier, "A skipped stage cannot claim produced outputs.")
            for offset, output in enumerate(outputs):
                location = f"{identifier}.outputs[{offset}]"
                if not fields(output, location, ("id", "summary"), ("artifact",)):
                    continue
                text(output, "id", location)
                text(output, "summary", location)
                output_id = output.get("id")
                if isinstance(output_id, str) and output_id.strip():
                    if output_id in ids:
                        error("DUPLICATE_ID", location + ".id", f"ID is not unique: {output_id}.")
                    else:
                        ids.add(output_id)
                        produced[output_id] = (index, stage.get("status"))
                        stage_outputs[identifier].add(output_id)
                if "artifact" in output:
                    artifact = output["artifact"]
                    if not isinstance(artifact, str) or not artifact.strip():
                        error("HANDOFF_ARTIFACT_INVALID", location, "Expected a nonempty relative artifact path.")
                        continue
                    try:
                        relative = Path(artifact)
                        resolved = (root / relative).resolve()
                        if relative.is_absolute() or not resolved.is_relative_to(root):
                            error("HANDOFF_ARTIFACT_OUTSIDE_ROOT", location, "Output artifacts must stay inside project_root.")
                        elif not resolved.is_file():
                            error("HANDOFF_ARTIFACT_MISSING", location, "Output artifact does not exist as a file.")
                    except (OSError, ValueError, RuntimeError) as exc:
                        error("HANDOFF_ARTIFACT_INVALID", location, str(exc))
        if not active:
            block("HANDOFFS_EMPTY", "handoffs", "At least one stage with an actual result is required.")
        consumed = {}
        for index, (identifier, stage) in enumerate(stages.items()):
            linked = refs(stage, "input_ids", produced, identifier)
            consumed[identifier] = set(linked)
            for output_id in linked:
                producer_index, producer_status = produced[output_id]
                if producer_index >= index:
                    error("HANDOFF_FORWARD_REFERENCE", identifier, "Inputs must come from an earlier stage.")
                elif producer_status not in usable:
                    block("HANDOFF_INPUT_NOT_READY", identifier, "An input comes from an unfinished or invalidated stage.")
        for previous, current in zip(active, active[1:]):
            if not stage_outputs[previous].intersection(consumed[current]):
                block("HANDOFF_NOT_CONNECTED", current, "The next active stage must consume a result of the previous stage.")
    return {"structure_valid": not errors, "record_ready": not errors and not blockers,
            "errors": errors, "blockers": blockers}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--project-root", type=Path, help="Evidence root; defaults to the record's directory.")
    parser.add_argument("--require-ready", action="store_true", help="Exit 1 for incomplete evidence records too.")
    parser.add_argument("--require-handoffs", action="store_true",
                        help="Require linked stage handoffs; also implies --require-ready.")
    args = parser.parse_args(argv)
    root = args.project_root or args.record.parent
    try:
        if not root.is_dir():
            raise ValueError("project_root is not a directory")
        result = validate(load_record(args.record), root, require_handoffs=args.require_handoffs)
    except (OSError, ValueError, RuntimeError) as exc:
        print(json.dumps({"input_error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    strict = args.require_ready or args.require_handoffs
    return 0 if result["structure_valid"] and (result["record_ready"] or not strict) else 1


if __name__ == "__main__":
    raise SystemExit(main())
