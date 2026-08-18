#!/usr/bin/env python3
"""Validate a V5 frontend interaction design package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from verify_sync_manifest import validate_manifest


REQUIRED_FILES = (
    "source-manifest.md",
    "clarification.md",
    "user-flow.md",
    "state-machine.md",
    "sequence-diagram.md",
    "frontend-development-plan.md",
    "sync-manifest.json",
)
ID_PATTERNS = {
    "PRD": re.compile(r"\bPRD-\d{2,}\b"),
    "PT": re.compile(r"\bPT-\d{2,}\b"),
    "API": re.compile(r"\bAPI-\d{2,}\b"),
    "CL": re.compile(r"\bCL-\d{2,}\b"),
    "UF": re.compile(r"\bUF-\d{2,}\b"),
    "SM": re.compile(r"\bSM-\d{2,}\b"),
    "SQ": re.compile(r"\bSQ-\d{2,}\b"),
    "FE": re.compile(r"\bFE-\d{2,}\b"),
}
DEFINITION_FILES = {
    "PRD": "source-manifest.md",
    "PT": "source-manifest.md",
    "API": "source-manifest.md",
    "CL": "clarification.md",
    "UF": "user-flow.md",
    "SM": "state-machine.md",
    "SQ": "sequence-diagram.md",
    "FE": "frontend-development-plan.md",
}
PLAN_SECTIONS = (
    "## Review Source",
    "## 1. Review 导读",
    "## 2. 功能背景与问题",
    "## 3. 目标用户与使用场景",
    "## 4. 输入资料与版本",
    "## 5. 原型页面与状态总览",
    "## 6. 本次开发范围与非目标",
    "## 7. 页面与组件职责",
    "## 8. User Flow",
    "## 9. 前端状态设计",
    "## 10. API 使用方案",
    "## 11. API 与交互 Mapping",
    "## 12. 异常与边界状态",
    "## 13. 关键开发决策",
    "## 14. 开发任务拆分",
    "## 15. 验收标准",
    "## 16. 已确认事项",
    "## 17. 未解决问题",
    "## 18. 追踪矩阵",
    "## 19. Technical Review 清单",
    "## 20. Revision 与同步信息",
)
PLAN_DIAGRAM_SECTIONS = {
    "UF": ("## 8. User Flow", "## 9. 前端状态设计", "flowchart"),
    "SM": ("## 9. 前端状态设计", "## 10. API 使用方案", "stateDiagram"),
    "SQ": ("## 11. API 与交互 Mapping", "## 12. 异常与边界状态", "sequenceDiagram"),
}
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\([^\)]+\)|<img\b[^>]*>", re.IGNORECASE)


def _section_body(document: str, start: str, end: str) -> str:
    start_position = document.find(start)
    if start_position < 0:
        return ""
    content_start = start_position + len(start)
    end_position = document.find(end, content_start)
    return document[content_start:] if end_position < 0 else document[content_start:end_position]


def _diagram_block(section: str, identifier: str) -> str | None:
    heading = re.search(
        rf"^(?P<marks>#{{3,6}})\s+{re.escape(identifier)}(?:\s|$).*$",
        section,
        re.MULTILINE,
    )
    if not heading:
        return None
    level = len(heading.group("marks"))
    next_heading = re.search(
        rf"^#{{1,{level}}}\s+.+$", section[heading.end() :], re.MULTILINE
    )
    end = heading.end() + next_heading.start() if next_heading else len(section)
    return section[heading.start() : end]


def _has_diagram_visual(block: str, mermaid_type: str) -> bool:
    mermaid = re.search(
        r"```mermaid\s*(.*?)```", block, re.IGNORECASE | re.DOTALL
    )
    return bool(
        (mermaid and re.search(re.escape(mermaid_type), mermaid.group(1), re.IGNORECASE))
        or MARKDOWN_IMAGE.search(block)
    )


VISUAL_ID_PATTERN = re.compile(r"\b(?:PT|UF|SM|SQ)-\d{2,}\b")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
FENCED_CODE_PATTERN = re.compile(r"(?:^|\n)(?:```|~~~).*?(?:\n```|\n~~~)(?=\n|$)", re.DOTALL)
HEADING_PATTERN = re.compile(r"^\s{0,3}#{1,6}\s+")
EXPIRING_QUERY_KEYS = {
    "expires",
    "signature",
    "x-amz-expires",
    "x-amz-signature",
    "x-oss-signature",
}


def _read(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path.name}: {exc}")
        return ""


def _validate_visual_id_links(plan: str) -> list[str]:
    """Require navigable visual IDs in final-plan prose, lists, and tables."""
    errors: list[str] = []
    without_fences = FENCED_CODE_PATTERN.sub("\n", plan)

    for line_number, line in enumerate(without_fences.splitlines(), start=1):
        if HEADING_PATTERN.match(line):
            continue

        def inspect_link(match: re.Match[str]) -> str:
            label, target = match.groups()
            identifiers = list(dict.fromkeys(VISUAL_ID_PATTERN.findall(label)))
            if len(identifiers) > 1:
                errors.append(
                    f"line {line_number}: visual IDs must be linked individually: "
                    + ", ".join(identifiers)
                )
            if identifiers:
                parsed = urlsplit(target)
                query_keys = {key.lower() for key in parse_qs(parsed.query)}
                if query_keys & EXPIRING_QUERY_KEYS:
                    errors.append(
                        f"line {line_number}: {identifiers[0]} uses an expiring link target"
                    )
                if (
                    parsed.scheme in {"http", "https"}
                    and "/docx/" in parsed.path
                    and not parsed.query
                    and not parsed.fragment
                ):
                    errors.append(
                        f"line {line_number}: {identifiers[0]} points to a document home, "
                        "not an exact block"
                    )
            return ""

        unlinked_text = MARKDOWN_LINK_PATTERN.sub(inspect_link, line)
        for identifier in VISUAL_ID_PATTERN.findall(unlinked_text):
            errors.append(
                f"line {line_number}: {identifier} must link to its exact visual-artifact target"
            )

    return errors


def validate_package(root: Path, require_ready_for_development: bool = False) -> list[str]:
    errors: list[str] = []
    root = root.resolve()
    for name in REQUIRED_FILES:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")
    if errors:
        return errors

    contents = {name: _read(root / name, errors) for name in REQUIRED_FILES if name.endswith(".md")}
    source = contents["source-manifest.md"]
    clarification = contents["clarification.md"]
    plan = contents["frontend-development-plan.md"]

    if not re.search(r"^Source Gate:\s*PASS\s*$", source, re.MULTILINE):
        errors.append("source-manifest.md must contain Source Gate: PASS")
    if not re.search(r"^Clarification Gate:\s*PASS\s*$", clarification, re.MULTILINE):
        errors.append("clarification.md must contain Clarification Gate: PASS")

    status_match = re.search(r"^Status:\s*(.+?)\s*$", plan, re.MULTILINE)
    allowed_statuses = {
        "Ready for Technical Review",
        "Ready for Development",
        "Sync Drift",
        "Blocked",
    }
    if not status_match or status_match.group(1) not in allowed_statuses:
        errors.append(f"final plan Status must be one of {sorted(allowed_statuses)}")
    elif require_ready_for_development and status_match.group(1) != "Ready for Development":
        errors.append("plan is not Ready for Development")

    last_position = -1
    for section in PLAN_SECTIONS:
        position = plan.find(section)
        if position < 0:
            errors.append(f"missing plan section: {section}")
        elif position < last_position:
            errors.append(f"plan section is out of order: {section}")
        else:
            last_position = position

    definitions = {
        prefix: set(pattern.findall(contents[file_name]))
        for prefix, pattern in ID_PATTERNS.items()
        for file_name in (DEFINITION_FILES[prefix],)
    }
    all_markdown = "\n".join(contents.values())
    for prefix, pattern in ID_PATTERNS.items():
        references = set(pattern.findall(all_markdown))
        undefined = references - definitions[prefix]
        for identifier in sorted(undefined):
            errors.append(
                f"{identifier} is referenced but not defined in {DEFINITION_FILES[prefix]}"
            )

    for prefix, (start, end, mermaid_type) in PLAN_DIAGRAM_SECTIONS.items():
        section = _section_body(plan, start, end)
        for identifier in sorted(definitions[prefix]):
            block = _diagram_block(section, identifier)
            if block is None:
                errors.append(
                    f"{identifier} must have its own heading in the Plan section {start}"
                )
            elif not _has_diagram_visual(block, mermaid_type):
                errors.append(
                    f"{identifier} must include an inline {mermaid_type} Mermaid block "
                    "or exported image in the Plan; a local artifact reference is not reviewable"
                )

    errors.extend(_validate_visual_id_links(plan))

    manifest_errors = validate_manifest(root / "sync-manifest.json", strict=True)
    errors.extend(f"sync manifest: {error}" for error in manifest_errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version_directory", type=Path)
    parser.add_argument("--require-ready-for-development", action="store_true")
    args = parser.parse_args()

    errors = validate_package(
        args.version_directory,
        require_ready_for_development=args.require_ready_for_development,
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {args.version_directory}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
