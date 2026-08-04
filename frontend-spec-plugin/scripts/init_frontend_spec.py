#!/usr/bin/env python3
"""Create a resumable frontend-spec artifact tree without overwriting user work."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


STAGE_NAMES = (
    "requirement-analysis",
    "requirement-clarification",
    "ui-parsing",
    "api-analysis",
    "interaction-design",
    "interaction-review",
    "flow-generation",
    "spec-generation",
)

TEMPLATE_TARGETS = {
    "question-list.md": "requirement/question-list.md",
    "decision-log.md": "requirement/decision-log.md",
    "request-response.md": "api/request-response.md",
    "interaction-review.md": "interaction/interaction-review.md",
    "sequence-diagrams.md": "flow/sequence-diagrams.md",
    "state-models.md": "flow/state-models.md",
    "frontend-development-spec.md": "document/frontend-development-spec.md",
    "manual-override.md": "manual/override.md",
}


def write_json_if_missing(path: Path, value: Any) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def copy_if_missing(source: Path, target: Path) -> bool:
    if target.exists():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return True


def initialize(output: Path, feature_id: str) -> tuple[list[Path], list[Path]]:
    output.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    preserved: list[Path] = []

    stages = {
        name: {"status": "pending", "artifacts": [], "blockers": []}
        for name in STAGE_NAMES
    }
    json_artifacts: dict[str, Any] = {
        "pipeline-state.json": {
            "schema_version": "1.0",
            "feature_id": feature_id,
            "readiness": "in_progress",
            "stages": stages,
        },
        "requirement/requirement-analysis.json": {
            "schema_version": "1.0",
            "feature_id": feature_id,
            "pages": [],
            "features": [],
            "rules": [],
            "non_functional": [],
            "assumptions": [],
            "open_questions": [],
        },
        "api/api-map.json": {
            "schema_version": "1.0",
            "operations": [],
            "models": [],
            "gaps": [],
        },
        "ui/ui-tree.json": {
            "schema_version": "1.0",
            "pages": [],
            "unresolved": [],
        },
        "interaction/interaction-spec.json": {
            "schema_version": "1.0",
            "revision": 1,
            "review_status": "pending_review",
            "approval": None,
            "interactions": [],
            "unmapped_requirements": [],
            "conflicts": [],
        },
        "history/change-log.json": {
            "schema_version": "1.0",
            "changes": [],
        },
    }

    for relative, value in json_artifacts.items():
        target = output / relative
        (created if write_json_if_missing(target, value) else preserved).append(target)

    templates = Path(__file__).resolve().parents[1] / "assets" / "templates"
    for template_name, relative in TEMPLATE_TARGETS.items():
        source = templates / template_name
        if not source.is_file():
            raise FileNotFoundError(f"Missing plugin template: {source}")
        target = output / relative
        (created if copy_if_missing(source, target) else preserved).append(target)

    return created, preserved


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize frontend specification artifacts without overwriting existing files."
    )
    parser.add_argument("--output", type=Path, default=Path("frontend-spec"))
    parser.add_argument("--feature-id", required=True)
    args = parser.parse_args()

    feature_id = args.feature_id.strip()
    if not feature_id:
        parser.error("--feature-id must not be empty")

    created, preserved = initialize(args.output.resolve(), feature_id)
    print(f"Frontend spec directory: {args.output.resolve()}")
    print(f"Created: {len(created)}")
    print(f"Preserved: {len(preserved)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
