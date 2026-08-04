#!/usr/bin/env python3
"""Create, list, select, and adopt isolated frontend specification runs."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from init_frontend_spec import initialize


CATALOG_NAME = "catalog.json"
FEATURE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_object(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def validate_new_feature_id(feature_id: str) -> str:
    if not FEATURE_ID_PATTERN.fullmatch(feature_id):
        raise ValueError("feature ID must use lowercase hyphen-case, for example: wechat-binding")
    return feature_id


def validate_existing_feature_id(feature_id: str) -> str:
    if not feature_id.strip():
        raise ValueError("feature ID must not be empty")
    return feature_id


def normalize_title(title: str | None, feature_id: str) -> str:
    value = (title or feature_id).strip()
    return value or feature_id


def load_catalog(root: Path, required: bool = False) -> dict[str, Any]:
    path = root / CATALOG_NAME
    if not path.exists():
        if required:
            raise ValueError(f"No frontend specification catalog exists at {path}")
        return {"schema_version": "1.0", "features": []}
    catalog = read_object(path)
    if catalog.get("schema_version") != "1.0" or not isinstance(catalog.get("features"), list):
        raise ValueError(f"Invalid frontend specification catalog: {path}")

    ids: set[str] = set()
    paths: set[str] = set()
    for entry in catalog["features"]:
        if not isinstance(entry, dict):
            raise ValueError(f"Invalid feature entry in {path}")
        feature_id = entry.get("feature_id")
        relative_path = entry.get("path")
        if not isinstance(feature_id, str) or not feature_id.strip():
            raise ValueError(f"Invalid feature ID in {path}: {feature_id!r}")
        if not isinstance(relative_path, str) or (
            relative_path != "."
            and (
                not FEATURE_ID_PATTERN.fullmatch(feature_id)
                or relative_path != f"features/{feature_id}"
            )
        ):
            raise ValueError(f"Unsafe feature path in {path}: {relative_path!r}")
        if feature_id in ids or relative_path in paths:
            raise ValueError(f"Duplicate feature ID or path in {path}: {feature_id}")
        ids.add(feature_id)
        paths.add(relative_path)
    return catalog


def find_entry(catalog: dict[str, Any], feature_id: str) -> dict[str, Any] | None:
    return next(
        (entry for entry in catalog["features"] if entry.get("feature_id") == feature_id),
        None,
    )


def resolve_entry(root: Path, entry: dict[str, Any]) -> Path:
    relative_path = entry["path"]
    target = root if relative_path == "." else root / relative_path
    state_path = target / "pipeline-state.json"
    if not state_path.is_file():
        raise ValueError(f"Feature {entry['feature_id']} is missing {state_path}")
    state = read_object(state_path)
    if state.get("feature_id") != entry["feature_id"]:
        raise ValueError(
            f"Feature ID mismatch: catalog has {entry['feature_id']!r}, "
            f"but {state_path} has {state.get('feature_id')!r}"
        )
    return target.resolve()


def list_features(root: Path) -> int:
    catalog_path = root / CATALOG_NAME
    legacy_state = root / "pipeline-state.json"
    if not catalog_path.exists():
        if legacy_state.is_file():
            state = read_object(legacy_state)
            print(f"LEGACY\t{state.get('feature_id', 'unknown')}\t{root.resolve()}")
        else:
            print("No frontend specification features found.")
        return 0

    catalog = load_catalog(root, required=True)
    if legacy_state.is_file() and not any(entry.get("path") == "." for entry in catalog["features"]):
        raise ValueError("Legacy root artifacts are not registered; adopt them before continuing")
    if not catalog["features"]:
        print("No frontend specification features found.")
        return 0
    for entry in catalog["features"]:
        target = resolve_entry(root, entry)
        state = read_object(target / "pipeline-state.json")
        title = entry.get("title") or entry["feature_id"]
        print(f"{entry['feature_id']}\t{title}\t{state.get('readiness', 'unknown')}\t{target}")
    return 0


def create_feature(root: Path, feature_id: str, title: str | None) -> int:
    feature_id = validate_new_feature_id(feature_id)
    catalog = load_catalog(root)
    if (root / "pipeline-state.json").exists() and not any(
        entry.get("path") == "." for entry in catalog["features"]
    ):
        raise ValueError("Legacy frontend-spec layout detected; adopt it before creating another feature")
    if find_entry(catalog, feature_id):
        raise ValueError(f"Feature {feature_id!r} already exists; resume it instead")

    feature_root = root / "features" / feature_id
    if feature_root.exists():
        raise ValueError(f"Feature path already exists but is not cataloged: {feature_root}")
    created, _ = initialize(feature_root, feature_id)
    now = datetime.now(timezone.utc).isoformat()
    catalog["features"].append(
        {
            "feature_id": feature_id,
            "title": normalize_title(title, feature_id),
            "path": f"features/{feature_id}",
            "created_at": now,
        }
    )
    write_object(root / CATALOG_NAME, catalog)
    print(f"Selected feature: {feature_id}")
    print(f"Feature root: {feature_root.resolve()}")
    print(f"Created artifacts: {len(created)}")
    return 0


def resume_feature(root: Path, feature_id: str) -> int:
    feature_id = validate_existing_feature_id(feature_id)
    catalog = load_catalog(root, required=True)
    entry = find_entry(catalog, feature_id)
    if entry is None:
        raise ValueError(f"Feature {feature_id!r} is not registered; create it instead")
    feature_root = resolve_entry(root, entry)
    print(f"Selected feature: {feature_id}")
    print(f"Feature root: {feature_root}")
    return 0


def adopt_legacy(root: Path, feature_id: str, title: str | None) -> int:
    feature_id = validate_existing_feature_id(feature_id)
    state_path = root / "pipeline-state.json"
    if not state_path.is_file():
        raise ValueError(f"No legacy frontend specification exists at {root}")
    state = read_object(state_path)
    if state.get("feature_id") != feature_id:
        raise ValueError(
            f"Legacy feature ID is {state.get('feature_id')!r}; use that exact ID when adopting"
        )

    catalog = load_catalog(root)
    existing = find_entry(catalog, feature_id)
    if existing:
        target = resolve_entry(root, existing)
        print(f"Selected feature: {feature_id}")
        print(f"Feature root: {target}")
        return 0
    if any(entry.get("path") == "." for entry in catalog["features"]):
        raise ValueError("A different legacy feature is already registered at the catalog root")

    catalog["features"].append(
        {
            "feature_id": feature_id,
            "title": normalize_title(title, feature_id),
            "path": ".",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    write_object(root / CATALOG_NAME, catalog)
    print(f"Adopted legacy feature: {feature_id}")
    print(f"Feature root: {root.resolve()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage isolated frontend specification runs.")
    parser.add_argument("--output", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list")
    for command in ("create", "adopt-legacy"):
        child = subparsers.add_parser(command)
        child.add_argument("--feature-id", required=True)
        child.add_argument("--title")
    resume = subparsers.add_parser("resume")
    resume.add_argument("--feature-id", required=True)
    args = parser.parse_args()

    if not args.output.is_absolute():
        parser.error("--output must be the confirmed absolute frontend-spec path")
    if args.output.name != "frontend-spec":
        parser.error("--output must end with the frontend-spec directory name")
    root = args.output.resolve()
    try:
        if args.command == "list":
            return list_features(root)
        if args.command == "create":
            return create_feature(root, args.feature_id, args.title)
        if args.command == "resume":
            return resume_feature(root, args.feature_id)
        return adopt_legacy(root, args.feature_id, args.title)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
