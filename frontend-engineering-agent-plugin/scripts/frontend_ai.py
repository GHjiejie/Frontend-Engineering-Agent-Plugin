#!/usr/bin/env python3
"""Initialize and validate Frontend Engineering Agent project artifacts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


FEATURE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PHASE_FILES = {
    "analysis": ["feature.yaml", "contract.yaml", "risk-report.md"],
    "design": ["feature.yaml", "contract.yaml", "risk-report.md", "implementation.yaml"],
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def memory_templates(timestamp: str) -> dict[str, str]:
    return {
        "project-memory/project-context.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
sourceRevision: ""
project:
  name: ""
  framework: ""
  language: ""
  ui: ""
  state: ""
  build: ""
  packageManager: ""
commands:
  install: ""
  dev: ""
  typecheck: ""
  lint: ""
  test: ""
  build: ""
rules:
  componentFirst: true
  styleToken: true
""",
        "project-memory/project-index.json": json.dumps(
            {
                "schemaVersion": 1,
                "updatedAt": timestamp,
                "routes": [],
                "views": [],
                "components": [],
                "apis": [],
                "stores": [],
                "composables": [],
                "tests": [],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "project-memory/architecture-map.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
layers: {{}}
dependencyRules: []
conventions: []
""",
        "project-memory/feature-registry.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
features: []
""",
        "project-memory/evolution-log.jsonl": "",
        "project-memory/memory-index.json": json.dumps(
            {"schemaVersion": 1, "updatedAt": timestamp, "sourceRevision": "", "files": {}},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "domain-memory/business-domain.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
domains: {{}}
provenance: []
""",
        "domain-memory/entity-model.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
entities: {{}}
relationships: []
provenance: []
""",
        "domain-memory/business-rule.yaml": f"""schemaVersion: 1
updatedAt: {yaml_string(timestamp)}
rules: []
provenance: []
""",
    }


def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def init_memory(root: Path) -> int:
    memory_root = root / "docs" / "frontend-ai"
    created: list[Path] = []
    skipped: list[Path] = []
    for relative, content in memory_templates(now()).items():
        target = memory_root / relative
        (created if write_new(target, content) else skipped).append(target)
    for directory in ("decisions", "features", "reports"):
        (memory_root / directory).mkdir(parents=True, exist_ok=True)
    print(f"Initialized {memory_root}")
    print(f"Created {len(created)} file(s); preserved {len(skipped)} existing file(s).")
    return 0


def feature_templates(feature_id: str, domain: str, title: str, timestamp: str) -> dict[str, str]:
    return {
        "feature.yaml": f"""schemaVersion: 1
feature:
  id: {yaml_string(feature_id)}
  title: {yaml_string(title)}
  domain: {yaml_string(domain)}
  status: PROPOSED
  orchestratorState: NEW
  contractReady: false
  implementationReady: false
  reviewStatus: NOT_RUN
  createdAt: {yaml_string(timestamp)}
  updatedAt: {yaml_string(timestamp)}
  owners: []
  tags: []
""",
        "contract.yaml": f"""schemaVersion: 1
featureId: {yaml_string(feature_id)}
status: DRAFT
summary: ""
goals: []
actors: []
scope: []
outOfScope: []
requirements: []
ui:
  entryPoints: []
  states: []
  responsive: []
  accessibility: []
api:
  endpoints: []
  dataContracts: []
  errorMapping: []
interactions: []
acceptanceCriteria: []
constraints: []
assumptions: []
openQuestions: []
reuseCandidates: []
affectedAreas: []
""",
        "implementation.yaml": f"""schemaVersion: 1
featureId: {yaml_string(feature_id)}
status: DRAFT
summary: ""
contractTraceability: []
approach:
  selected: ""
  rationale: ""
  alternatives: []
architecture:
  routes: []
  pages: []
  components: []
  api: []
  state: []
  interactions: []
  styling: []
  accessibility: []
fileChanges: []
steps: []
tests:
  unit: []
  component: []
  integration: []
  e2e: []
  manual: []
dependencies: []
risks: []
rollout: []
rollback: []
memoryUpdates: []
decisions: []
openQuestions: []
""",
        "history.yaml": "schemaVersion: 1\nentries: []\n",
        "risk-report.md": f"# Risk report: {feature_id}\n\nNo risks have been assessed yet.\n",
    }


def register_feature(memory_root: Path, feature_id: str, domain: str, timestamp: str) -> None:
    registry = memory_root / "project-memory" / "feature-registry.yaml"
    text = registry.read_text(encoding="utf-8")
    if re.search(rf"^\s*-?\s*id:\s*[\"']?{re.escape(feature_id)}[\"']?\s*$", text, re.MULTILINE):
        return
    entry = (
        f"  - id: {yaml_string(feature_id)}\n"
        f"    status: PROPOSED\n"
        f"    domain: {yaml_string(domain)}\n"
        f"    path: {yaml_string(f'docs/frontend-ai/features/{feature_id}')}\n"
        f"    updatedAt: {yaml_string(timestamp)}\n"
    )
    if re.search(r"^features:\s*\[\]\s*$", text, re.MULTILINE):
        text = re.sub(r"^features:\s*\[\]\s*$", "features:\n" + entry.rstrip(), text, count=1, flags=re.MULTILINE)
    else:
        text = text.rstrip() + "\n" + entry
    registry.write_text(text.rstrip() + "\n", encoding="utf-8")


def new_feature(root: Path, feature_id: str, domain: str, title: str) -> int:
    if not FEATURE_ID.fullmatch(feature_id):
        print("Feature id must be lower-case hyphen-case.", file=sys.stderr)
        return 2
    memory_root = root / "docs" / "frontend-ai"
    registry = memory_root / "project-memory" / "feature-registry.yaml"
    if not registry.exists():
        print("Project memory is missing; run the init command first.", file=sys.stderr)
        return 2
    feature_root = memory_root / "features" / feature_id
    if feature_root.exists():
        print(f"Feature already exists: {feature_root}", file=sys.stderr)
        return 2
    timestamp = now()
    for relative, content in feature_templates(feature_id, domain, title, timestamp).items():
        write_new(feature_root / relative, content)
    register_feature(memory_root, feature_id, domain, timestamp)
    print(f"Created feature: {feature_root}")
    return 0


def require_yaml_keys(path: Path, keys: list[str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for key in keys:
        if not re.search(rf"^\s*{re.escape(key)}:\s*", text, re.MULTILINE):
            errors.append(f"{path}: missing YAML key '{key}'")


def yaml_scalar(path: Path, key: str) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
    if match is None:
        return None
    value = match.group(1)
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return value
        return str(parsed)
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def expect_scalar(path: Path, key: str, expected: str, errors: list[str]) -> None:
    actual = yaml_scalar(path, key)
    if actual != expected:
        errors.append(f"{path}: expected {key}={expected}, found {actual!r}")


def validate(root: Path, feature_id: str | None, phase: str) -> int:
    memory_root = root / "docs" / "frontend-ai"
    errors: list[str] = []
    for relative in memory_templates(now()):
        path = memory_root / relative
        if not path.is_file():
            errors.append(f"Missing required memory file: {path}")
            continue
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"Invalid JSON in {path}: {exc}")
    if not (memory_root / "decisions").is_dir():
        errors.append("Missing decisions directory")
    if feature_id and phase != "memory":
        if not FEATURE_ID.fullmatch(feature_id):
            errors.append("Feature id must be lower-case hyphen-case")
        feature_root = memory_root / "features" / feature_id
        required = list(PHASE_FILES["analysis"])
        if phase in {"design", "implementation", "review"}:
            required = list(PHASE_FILES["design"])
        for relative in required:
            if not (feature_root / relative).is_file():
                errors.append(f"Missing feature artifact: {feature_root / relative}")
        feature_yaml = feature_root / "feature.yaml"
        if feature_yaml.is_file():
            require_yaml_keys(feature_yaml, ["schemaVersion", "feature", "id", "status", "orchestratorState"], errors)
        contract = feature_root / "contract.yaml"
        if contract.is_file():
            require_yaml_keys(contract, ["schemaVersion", "featureId", "status", "requirements", "acceptanceCriteria"], errors)
        implementation = feature_root / "implementation.yaml"
        if phase in {"analysis", "design", "implementation", "review"} and contract.is_file():
            expect_scalar(contract, "status", "READY", errors)
        if phase == "analysis" and feature_yaml.is_file():
            expect_scalar(feature_yaml, "status", "ANALYZING", errors)
            expect_scalar(feature_yaml, "orchestratorState", "FEATURE_CONTRACT_READY", errors)
            expect_scalar(feature_yaml, "contractReady", "true", errors)
        if phase == "design":
            if feature_yaml.is_file():
                expect_scalar(feature_yaml, "status", "DESIGNED", errors)
                expect_scalar(feature_yaml, "orchestratorState", "DESIGN_READY", errors)
                expect_scalar(feature_yaml, "contractReady", "true", errors)
                expect_scalar(feature_yaml, "implementationReady", "true", errors)
            if implementation.is_file():
                expect_scalar(implementation, "status", "READY", errors)
        if phase in {"implementation", "review"}:
            if implementation.is_file():
                expect_scalar(implementation, "status", "READY", errors)
            change_log = memory_root / "reports" / f"{feature_id}-change-log.md"
            if not change_log.is_file():
                errors.append(f"Missing implementation report: {change_log}")
        if phase == "implementation" and feature_yaml.is_file():
            expect_scalar(feature_yaml, "status", "IMPLEMENTING", errors)
            expect_scalar(feature_yaml, "orchestratorState", "VERIFYING", errors)
            expect_scalar(feature_yaml, "contractReady", "true", errors)
            expect_scalar(feature_yaml, "implementationReady", "true", errors)
        if phase == "review":
            review_report = memory_root / "reports" / f"{feature_id}-review-report.md"
            if not review_report.is_file():
                errors.append(f"Missing review report: {review_report}")
            else:
                report_text = review_report.read_text(encoding="utf-8")
                outcome_match = re.search(
                    r"^Outcome:\s*(PASS|FAIL|BLOCKED|NEED_HUMAN_REVIEW)\s*$",
                    report_text,
                    re.MULTILINE,
                )
                if outcome_match is None:
                    errors.append(f"{review_report}: missing a valid Outcome line")
                elif feature_yaml.is_file():
                    outcome = outcome_match.group(1)
                    if outcome == "PASS":
                        expect_scalar(feature_yaml, "status", "RELEASED", errors)
                        expect_scalar(feature_yaml, "orchestratorState", "COMPLETED", errors)
                    else:
                        expected_state = "FAILED" if outcome == "FAIL" else outcome
                        expect_scalar(feature_yaml, "status", "IMPLEMENTING", errors)
                        expect_scalar(feature_yaml, "orchestratorState", expected_state, errors)
                    expect_scalar(feature_yaml, "reviewStatus", outcome, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Frontend AI artifacts are valid for phase '{phase}'.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    init_parser = subparsers.add_parser("init", help="Initialize memory without overwriting files")
    init_parser.add_argument("--root", type=Path, default=Path.cwd())
    feature_parser = subparsers.add_parser("new-feature", help="Create a new Feature Entity")
    feature_parser.add_argument("feature_id")
    feature_parser.add_argument("--root", type=Path, default=Path.cwd())
    feature_parser.add_argument("--domain", required=True)
    feature_parser.add_argument("--title", required=True)
    validate_parser = subparsers.add_parser("validate", help="Validate memory and phase artifacts")
    validate_parser.add_argument("--root", type=Path, default=Path.cwd())
    validate_parser.add_argument("--feature")
    validate_parser.add_argument("--phase", choices=["memory", "analysis", "design", "implementation", "review"], default="memory")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.expanduser().resolve()
    if args.command == "init":
        return init_memory(root)
    if args.command == "new-feature":
        return new_feature(root, args.feature_id, args.domain, args.title)
    return validate(root, args.feature, args.phase)


if __name__ == "__main__":
    raise SystemExit(main())
