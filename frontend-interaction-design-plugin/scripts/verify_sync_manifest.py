#!/usr/bin/env python3
"""Validate a frontend design sync manifest and optional file digests."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_FIELDS = {
    "feature": str,
    "version": str,
    "feishuDocumentUrl": str,
    "feishuDocumentToken": str,
    "feishuRevisionId": int,
    "syncedAt": str,
    "exportMode": str,
    "syncedFiles": list,
    "prototypeIds": list,
    "status": str,
}
EXPORT_MODES = {"cloud-media", "offline-media"}
STATUSES = {"in-sync", "drift", "blocked"}
PROTOTYPE_ID = re.compile(r"^PT-\d{2,}$")
SHA256 = re.compile(r"^(?:sha256:)?([0-9a-fA-F]{64})$")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_file(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def validate_manifest(manifest_path: Path, strict: bool = False) -> list[str]:
    errors: list[str] = []
    if not manifest_path.is_file():
        return [f"missing sync manifest: {manifest_path}"]

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read valid JSON from {manifest_path}: {exc}"]

    if not isinstance(data, dict):
        return ["sync manifest root must be an object"]

    for field, expected_type in REQUIRED_FIELDS.items():
        value = data.get(field)
        if not isinstance(value, expected_type) or isinstance(value, bool):
            errors.append(f"{field} must be {expected_type.__name__}")

    if errors:
        return errors

    parsed_url = urlparse(data["feishuDocumentUrl"])
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        errors.append("feishuDocumentUrl must be an absolute https URL")
    if not data["feishuDocumentToken"].strip():
        errors.append("feishuDocumentToken must not be empty")
    if data["feishuRevisionId"] < 0:
        errors.append("feishuRevisionId must be non-negative")
    if data["exportMode"] not in EXPORT_MODES:
        errors.append(f"exportMode must be one of {sorted(EXPORT_MODES)}")
    if data["status"] not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    try:
        parsed_time = datetime.fromisoformat(data["syncedAt"].replace("Z", "+00:00"))
        if parsed_time.tzinfo is None:
            errors.append("syncedAt must include a timezone")
    except ValueError:
        errors.append("syncedAt must be ISO-8601")

    synced_files = data["syncedFiles"]
    if not synced_files:
        errors.append("syncedFiles must not be empty")
    elif len(synced_files) != len(set(map(str, synced_files))):
        errors.append("syncedFiles must not contain duplicates")

    root = manifest_path.parent.resolve()
    for item in synced_files:
        if not _safe_relative_file(item):
            errors.append(f"unsafe synced file path: {item!r}")
            continue
        target = root / item
        if not target.is_file():
            errors.append(f"missing synchronized file: {item}")

    prototype_ids = data["prototypeIds"]
    if len(prototype_ids) != len(set(map(str, prototype_ids))):
        errors.append("prototypeIds must not contain duplicates")
    for prototype_id in prototype_ids:
        if not isinstance(prototype_id, str) or not PROTOTYPE_ID.fullmatch(prototype_id):
            errors.append(f"invalid prototype ID: {prototype_id!r}")

    digests = data.get("fileDigests")
    if strict and data["status"] == "in-sync" and not isinstance(digests, dict):
        errors.append("fileDigests is required for strict in-sync validation")
    if digests is not None:
        if not isinstance(digests, dict):
            errors.append("fileDigests must be an object")
        else:
            for relative_path, expected in digests.items():
                if relative_path not in synced_files:
                    errors.append(f"digest path is not listed in syncedFiles: {relative_path}")
                    continue
                match = SHA256.fullmatch(expected) if isinstance(expected, str) else None
                if not match:
                    errors.append(f"invalid SHA-256 digest for {relative_path}")
                    continue
                target = root / relative_path
                if target.is_file() and _sha256(target) != match.group(1).lower():
                    errors.append(f"digest mismatch for {relative_path}")

    plan_path = root / "frontend-development-plan.md"
    if plan_path.is_file():
        plan = plan_path.read_text(encoding="utf-8")
        if data["feishuDocumentUrl"] not in plan:
            errors.append("plan does not contain the Feishu document URL")
        revision_pattern = re.compile(
            rf"Feishu Revision:\s*`?{re.escape(str(data['feishuRevisionId']))}`?"
        )
        if not revision_pattern.search(plan):
            errors.append("plan does not contain the manifest Feishu Revision")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        type=Path,
        help="sync-manifest.json or the version directory containing it",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="require file digests for an in-sync manifest",
    )
    args = parser.parse_args()

    manifest_path = args.path / "sync-manifest.json" if args.path.is_dir() else args.path
    errors = validate_manifest(manifest_path.resolve(), strict=args.strict)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
