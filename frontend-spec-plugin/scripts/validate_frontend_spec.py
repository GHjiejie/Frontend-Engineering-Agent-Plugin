#!/usr/bin/env python3
"""Validate frontend-spec structure, traceability, and optional readiness gates."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable


EXPECTED_STAGES = {
    "requirement-analysis",
    "requirement-clarification",
    "ui-parsing",
    "api-analysis",
    "interaction-design",
    "flow-generation",
    "spec-generation",
}

REQUIRED_FILES = (
    "pipeline-state.json",
    "requirement/requirement-analysis.json",
    "requirement/question-list.md",
    "requirement/decision-log.md",
    "api/api-map.json",
    "api/request-response.md",
    "ui/ui-tree.json",
    "interaction/interaction-spec.json",
    "flow/sequence-diagrams.md",
    "flow/state-models.md",
    "document/frontend-development-spec.md",
    "manual/override.md",
    "history/change-log.json",
)


def load_json(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level JSON value must be an object")
        return {}
    if value.get("schema_version") != "1.0":
        errors.append(f"{path}: schema_version must be '1.0'")
    return value


def values(items: Iterable[dict[str, Any]], key: str) -> set[str]:
    return {item[key] for item in items if isinstance(item, dict) and isinstance(item.get(key), str)}


def components(pages: Iterable[dict[str, Any]]) -> Iterable[dict[str, Any]]:
    stack: list[dict[str, Any]] = []
    for page in pages:
        if isinstance(page, dict):
            stack.extend(item for item in page.get("components", []) if isinstance(item, dict))
    while stack:
        item = stack.pop()
        yield item
        stack.extend(child for child in item.get("children", []) if isinstance(child, dict))


def check_ids(items: Iterable[dict[str, Any]], prefix: str, label: str, errors: list[str]) -> set[str]:
    ids = [item.get("id") for item in items if isinstance(item, dict)]
    pattern = re.compile(rf"^{re.escape(prefix)}-[0-9]{{3,}}$")
    for item_id in ids:
        if not isinstance(item_id, str) or not pattern.fullmatch(item_id):
            errors.append(f"{label}: invalid ID {item_id!r}; expected {prefix}-###")
    valid = {item_id for item_id in ids if isinstance(item_id, str)}
    if len(valid) != len(ids):
        errors.append(f"{label}: IDs must be unique")
    return valid


def check_refs(
    owner: str,
    refs: Iterable[Any],
    allowed: set[str],
    kind: str,
    errors: list[str],
) -> None:
    for ref in refs:
        if not isinstance(ref, str) or ref not in allowed:
            errors.append(f"{owner}: unknown {kind} reference {ref!r}")


def validate(root: Path, require_complete: bool) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing required artifact: {relative}")
    if errors:
        return errors

    state = load_json(root / "pipeline-state.json", errors)
    requirements = load_json(root / "requirement/requirement-analysis.json", errors)
    api_map = load_json(root / "api/api-map.json", errors)
    ui_tree = load_json(root / "ui/ui-tree.json", errors)
    interactions = load_json(root / "interaction/interaction-spec.json", errors)
    load_json(root / "history/change-log.json", errors)

    stages = state.get("stages", {})
    if not isinstance(stages, dict) or set(stages) != EXPECTED_STAGES:
        errors.append("pipeline-state.json: stages must match the artifact contract")
    else:
        for name, stage in stages.items():
            if not isinstance(stage, dict) or stage.get("status") not in {
                "pending", "in_progress", "blocked", "complete"
            }:
                errors.append(f"pipeline-state.json: invalid status for stage {name}")

    requirement_items = requirements.get("features", [])
    operation_items = api_map.get("operations", [])
    page_items = ui_tree.get("pages", [])
    interaction_items = interactions.get("interactions", [])
    component_items = list(components(page_items if isinstance(page_items, list) else []))

    rq_ids = check_ids(requirement_items, "RQ", "requirements", errors)
    api_ids = check_ids(operation_items, "API", "API operations", errors)
    ui_ids = check_ids(component_items, "UI", "UI components", errors)
    check_ids(interaction_items, "IX", "interactions", errors)

    for operation in operation_items if isinstance(operation_items, list) else []:
        if isinstance(operation, dict):
            check_refs(operation.get("id", "API operation"), operation.get("requirement_ids", []), rq_ids, "requirement", errors)
    for component in component_items:
        check_refs(component.get("id", "UI component"), component.get("requirement_ids", []), rq_ids, "requirement", errors)
    for interaction in interaction_items if isinstance(interaction_items, list) else []:
        if not isinstance(interaction, dict):
            continue
        owner = interaction.get("id", "interaction")
        check_refs(owner, interaction.get("requirement_ids", []), rq_ids, "requirement", errors)
        check_refs(owner, interaction.get("element_ids", []), ui_ids, "UI", errors)
        check_refs(owner, interaction.get("api_ids", []), api_ids, "API", errors)

    if require_complete:
        if state.get("readiness") != "ready_for_implementation":
            errors.append("pipeline-state.json: readiness is not ready_for_implementation")
        if isinstance(stages, dict):
            incomplete = [name for name, stage in stages.items() if not isinstance(stage, dict) or stage.get("status") != "complete"]
            if incomplete:
                errors.append(f"Incomplete pipeline stages: {', '.join(sorted(incomplete))}")
        blocking = [
            item.get("id", "unknown")
            for item in requirements.get("open_questions", [])
            if isinstance(item, dict) and item.get("severity") == "blocking" and item.get("status") != "answered"
        ]
        if blocking:
            errors.append(f"Unanswered blocking questions: {', '.join(blocking)}")
        unmapped = interactions.get("unmapped_requirements", [])
        if unmapped:
            errors.append(f"Unmapped requirements remain: {', '.join(map(str, unmapped))}")
        if interactions.get("conflicts"):
            errors.append("Interaction conflicts remain unresolved")
        document = (root / "document/frontend-development-spec.md").read_text(encoding="utf-8")
        if "Status: `ready_for_implementation`" not in document:
            errors.append("Final document does not declare ready_for_implementation")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a frontend specification artifact tree.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"Not a directory: {root}")

    errors = validate(root, args.require_complete)
    if errors:
        print("Frontend spec validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Frontend spec validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
