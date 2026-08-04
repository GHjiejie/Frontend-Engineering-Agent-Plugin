#!/usr/bin/env python3
"""Operate the Frontend Engineering Knowledge Agent v2 MVP runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ENTITY_PATTERNS = {
    "feature": re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$"),
    "bug": re.compile(r"^BUG-[0-9]{3,}$"),
    "change": re.compile(r"^CHG-[0-9]{3,}$"),
    "decision": re.compile(r"^ADR-[0-9]{3,}$"),
}

STATES = {
    "INIT",
    "MEMORY_SYNC",
    "CONTEXT_BUILD",
    "ANALYSIS",
    "APPROVAL_REQUIRED",
    "DESIGN",
    "IMPLEMENTATION",
    "REVIEW",
    "MEMORY_UPDATE",
    "COMPLETED",
    "BLOCKED",
    "CONFLICT",
    "FAILED",
    "WAITING_HUMAN",
}

TRANSITIONS = {
    "INIT": {"MEMORY_SYNC"},
    "MEMORY_SYNC": {"CONTEXT_BUILD"},
    "CONTEXT_BUILD": {"ANALYSIS"},
    "ANALYSIS": {"APPROVAL_REQUIRED"},
    "APPROVAL_REQUIRED": {"DESIGN"},
    "DESIGN": {"IMPLEMENTATION"},
    "IMPLEMENTATION": {"WAITING_HUMAN", "REVIEW"},
    "WAITING_HUMAN": {"IMPLEMENTATION", "MEMORY_UPDATE"},
    "REVIEW": {"MEMORY_UPDATE"},
    "MEMORY_UPDATE": {"WAITING_HUMAN", "COMPLETED"},
    "BLOCKED": {"MEMORY_SYNC", "ANALYSIS"},
    "CONFLICT": {"MEMORY_SYNC", "ANALYSIS"},
    "FAILED": {"MEMORY_SYNC", "ANALYSIS"},
    "COMPLETED": {"MEMORY_SYNC"},
}

EXCEPTION_STATES = {"BLOCKED", "CONFLICT", "FAILED"}
CONFIDENCE = {"low", "medium", "high"}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def y(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def knowledge_root(root: Path) -> Path:
    return root / "docs" / "frontend-ai"


def metadata_yaml(confidence: str = "low", indent: str = "") -> str:
    return (
        f"{indent}metadata:\n"
        f"{indent}  source: [ai]\n"
        f"{indent}  confidence: {confidence}\n"
        f"{indent}  lastVerified: {today()}\n"
        f"{indent}  verifiedBy: \"\"\n"
    )


def schema_template(entity_type: str, body_key: str) -> str:
    return f"""schemaVersion: 2
entityType: {entity_type}
required: [schemaVersion, metadata, {body_key}]
metadata:
  source:
    type: array
    allowed: [human, ai, git, inferred]
  confidence:
    allowed: [low, medium, high]
  lastVerified:
    type: date
  verifiedBy:
    type: string
body:
  key: {body_key}
  idRequired: true
"""


def initial_templates(timestamp: str) -> dict[str, str]:
    return {
        "memory/project/project-context.yaml": f"""schemaVersion: 2
{metadata_yaml()}project:
  name: ""
  framework: ""
  language: ""
  build: ""
  ui: ""
  state: ""
  packageManager: ""
commands:
  install: ""
  dev: ""
  typecheck: ""
  lint: ""
  test: ""
  build: ""
""",
        "memory/project/architecture-map.yaml": f"""schemaVersion: 2
{metadata_yaml()}layers: {{}}
dependencyRules: []
conventions: []
componentIndex: []
""",
        "memory/project/constitution.yaml": f"""schemaVersion: 2
{metadata_yaml()}rules:
  architecture: []
  api: []
  state: []
  component: []
  styling: []
  testing: []
  accessibility: []
""",
        "memory/domain/domain-index.yaml": f"""schemaVersion: 2
{metadata_yaml()}domains: []
""",
        "memory/schema/feature.schema.yaml": schema_template("feature", "feature"),
        "memory/schema/bug.schema.yaml": schema_template("bug", "bug"),
        "memory/schema/change.schema.yaml": schema_template("change", "change"),
        "memory/schema/decision.schema.yaml": schema_template("decision", "decision"),
        "memory/index/knowledge-index.json": json.dumps(
            {
                "schemaVersion": 2,
                "updatedAt": timestamp,
                "metadata": {
                    "source": ["ai"],
                    "confidence": "low",
                    "lastVerified": today(),
                    "verifiedBy": "",
                },
                "entities": [],
                "relations": [],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        "runtime/state.yaml": f"""schemaVersion: 2
orchestrator:
  state: INIT
  taskId: ""
  waitingFor: ""
  updatedAt: {y(timestamp)}
  lastTransition:
    from: ""
    to: INIT
    reason: "Knowledge runtime initialized"
""",
        "runtime/task-context.yaml": f"""schemaVersion: 2
status: EMPTY
task:
  id: ""
  type: ""
  goal: ""
generatedAt: {y(timestamp)}
""",
    }


def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def initialize(root: Path) -> int:
    base = knowledge_root(root)
    created: list[Path] = []
    preserved: list[Path] = []
    for relative, content in initial_templates(now()).items():
        target = base / relative
        (created if write_new(target, content) else preserved).append(target)
    for relative in (
        "memory/feature",
        "memory/bug",
        "memory/change",
        "memory/decision",
        "runtime/approvals",
        "runtime/cache",
        "reports",
    ):
        (base / relative).mkdir(parents=True, exist_ok=True)
    legacy = [base / name for name in ("project-memory", "domain-memory", "features") if (base / name).exists()]
    print(f"Initialized Frontend Engineering Knowledge v2 at {base}")
    print(f"Created {len(created)} file(s); preserved {len(preserved)} existing file(s).")
    if legacy:
        print("Legacy v1 paths detected; review and propose migration instead of moving them automatically:")
        for path in legacy:
            print(f"- {path}")
    return 0


def load_index(base: Path) -> dict[str, Any]:
    path = base / "memory" / "index" / "knowledge-index.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError("Knowledge index is missing; run init first.") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Knowledge index is invalid JSON: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("entities"), list):
        raise ValueError("Knowledge index must contain an entities array.")
    if not isinstance(payload.get("relations", []), list):
        raise ValueError("Knowledge index relations must be an array.")
    return payload


def save_index(base: Path, payload: dict[str, Any]) -> None:
    payload["updatedAt"] = now()
    path = base / "memory" / "index" / "knowledge-index.json"
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def entity_templates(kind: str, entity_id: str, title: str, domain: str) -> dict[str, str]:
    timestamp = now()
    if kind == "feature":
        return {
            "feature.yaml": f"""schemaVersion: 2
{metadata_yaml()}feature:
  id: {y(entity_id)}
  title: {y(title)}
  domain: {y(domain)}
  status: proposed
  requirements: []
  ui: []
  api: []
  interaction: []
  files: []
  history: []
""",
            "contract.yaml": f"""schemaVersion: 2
{metadata_yaml()}featureId: {y(entity_id)}
status: DRAFT
requirements: []
acceptanceCriteria: []
""",
            "implementation.yaml": f"""schemaVersion: 2
{metadata_yaml()}featureId: {y(entity_id)}
status: DRAFT
changes: []
verification: []
""",
            "history.yaml": f"""schemaVersion: 2
{metadata_yaml()}featureId: {y(entity_id)}
entries: []
""",
        }
    if kind == "bug":
        return {
            "bug.yaml": f"""schemaVersion: 2
{metadata_yaml()}bug:
  id: {y(entity_id)}
  title: {y(title)}
  domain: {y(domain)}
  status: proposed
  relatedFeature: ""
  observed: []
  expected: []
  files: []
""",
            "analysis.yaml": f"""schemaVersion: 2
{metadata_yaml()}bugId: {y(entity_id)}
status: DRAFT
reproduction: []
evidence: []
rootCauseHypotheses: []
""",
            "fix.yaml": f"""schemaVersion: 2
{metadata_yaml()}bugId: {y(entity_id)}
status: DRAFT
rootCause: ""
files: []
verification: []
""",
            "history.yaml": f"""schemaVersion: 2
{metadata_yaml()}bugId: {y(entity_id)}
entries: []
""",
        }
    if kind == "change":
        return {
            "change.yaml": f"""schemaVersion: 2
{metadata_yaml()}change:
  id: {y(entity_id)}
  title: {y(title)}
  status: proposed
  type: ""
  source:
    kind: ""
    revision: ""
  files: []
  related:
    feature: ""
    bug: ""
    decisions: []
  description: ""
  verification: []
"""
        }
    return {
        f"{entity_id}.md": f"""---
schemaVersion: 2
metadata:
  source: [ai]
  confidence: low
  lastVerified: {today()}
  verifiedBy: ""
decision:
  id: {entity_id}
  title: {y(title)}
  status: proposed
  domain: {y(domain)}
---

# {entity_id}: {title}

## Context

## Decision

## Reason

## Consequences
"""
    }


def primary_entity_path(kind: str, entity_id: str) -> str:
    if kind == "decision":
        return f"docs/frontend-ai/memory/decision/{entity_id}.md"
    primary = {"feature": "feature.yaml", "bug": "bug.yaml", "change": "change.yaml"}[kind]
    return f"docs/frontend-ai/memory/{kind}/{entity_id}/{primary}"


def create_entity(root: Path, kind: str, entity_id: str, title: str, domain: str) -> int:
    if ENTITY_PATTERNS[kind].fullmatch(entity_id) is None:
        print(f"Invalid {kind} id: {entity_id}", file=sys.stderr)
        return 2
    base = knowledge_root(root)
    try:
        index = load_index(base)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    if any(item.get("type") == kind and item.get("id") == entity_id for item in index["entities"] if isinstance(item, dict)):
        print(f"Entity is already indexed: {kind}:{entity_id}", file=sys.stderr)
        return 2
    entity_root = base / "memory" / kind
    target_root = entity_root if kind == "decision" else entity_root / entity_id
    paths = {target_root / relative: content for relative, content in entity_templates(kind, entity_id, title, domain).items()}
    if any(path.exists() for path in paths):
        print(f"Entity already exists: {kind}:{entity_id}", file=sys.stderr)
        return 2
    for path, content in paths.items():
        write_new(path, content)
    index["entities"].append(
        {
            "type": kind,
            "id": entity_id,
            "domain": domain,
            "path": primary_entity_path(kind, entity_id),
            "files": [],
            "routes": [],
            "symbols": [],
            "related": [],
            "metadata": {"confidence": "low", "lastVerified": today()},
        }
    )
    save_index(base, index)
    print(f"Created {kind} entity: {entity_id}")
    return 0


def entity_key(entity: dict[str, Any]) -> str:
    return f"{entity.get('type', '')}:{entity.get('id', '')}"


def build_context(
    root: Path,
    task_id: str,
    task_type: str,
    goal: str,
    domain: str,
    targets: list[str],
    feature_id: str,
    bug_id: str,
    constraints: list[str],
    non_goals: list[str],
) -> int:
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", task_id) is None:
        print("Task id must use letters, digits, dot, underscore, or hyphen.", file=sys.stderr)
        return 2
    base = knowledge_root(root)
    try:
        index = load_index(base)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    entities = [item for item in index["entities"] if isinstance(item, dict)]
    target_set = set(targets)
    explicit: list[dict[str, Any]] = []
    for entity in entities:
        values = set(entity.get("files", [])) | set(entity.get("routes", [])) | set(entity.get("symbols", []))
        if (
            (feature_id and entity.get("type") == "feature" and entity.get("id") == feature_id)
            or (bug_id and entity.get("type") == "bug" and entity.get("id") == bug_id)
            or (domain and entity.get("domain") == domain)
            or bool(target_set & values)
        ):
            explicit.append(entity)
    selected = {entity_key(item) for item in explicit}
    related_keys: set[str] = set()
    for item in explicit:
        for related in item.get("related", []):
            if isinstance(related, str):
                related_keys.add(related)
            elif isinstance(related, dict):
                related_keys.add(entity_key(related))
    for relation in index.get("relations", []):
        if not isinstance(relation, dict):
            continue
        left, right = relation.get("from"), relation.get("to")
        if left in selected and isinstance(right, str):
            related_keys.add(right)
        if right in selected and isinstance(left, str):
            related_keys.add(left)
    explicit_files = {path for item in explicit for path in item.get("files", [])}
    structural = [
        item
        for item in entities
        if entity_key(item) not in selected
        and (entity_key(item) in related_keys or bool(explicit_files & set(item.get("files", []))))
    ]

    lines = [
        "schemaVersion: 2",
        "status: READY",
        "task:",
        f"  id: {y(task_id)}",
        f"  type: {task_type}",
        f"  goal: {y(goal)}",
        f"  domain: {y(domain)}",
        f"  targets: {json.dumps(targets, ensure_ascii=False)}",
        f"  featureId: {y(feature_id)}",
        f"  bugId: {y(bug_id)}",
        f"constraints: {json.dumps(constraints, ensure_ascii=False)}",
        f"nonGoals: {json.dumps(non_goals, ensure_ascii=False)}",
        "affectedEntities:",
    ]
    for layer, items in (("explicit", explicit), ("structural", structural)):
        for item in items:
            confidence = item.get("metadata", {}).get("confidence", "low") if isinstance(item.get("metadata"), dict) else "low"
            lines.extend(
                [
                    f"  - type: {item.get('type', '')}",
                    f"    id: {y(str(item.get('id', '')))}",
                    f"    path: {y(str(item.get('path', '')))}",
                    f"    confidence: {confidence}",
                    f"    retrievalLayer: {layer}",
                ]
            )
    if not explicit and not structural:
        lines.append("  []")
    affected_files = sorted(target_set | explicit_files | {path for item in structural for path in item.get("files", [])})
    lines.extend(
        [
            f"files: {json.dumps(affected_files, ensure_ascii=False)}",
            "rules: []",
            "retrieval:",
            f"  explicit: {json.dumps([entity_key(item) for item in explicit], ensure_ascii=False)}",
            f"  structural: {json.dumps([entity_key(item) for item in structural], ensure_ascii=False)}",
            "  semantic:",
            "    enabled: false",
            '    reason: "Semantic retrieval is not implemented in the v2 MVP"',
            f"generatedAt: {y(now())}",
        ]
    )
    path = base / "runtime" / "task-context.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Built task context with {len(explicit)} explicit and {len(structural)} structural entities: {path}")
    return 0


def yaml_scalar(path: Path, key: str) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
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


def approval_path(base: Path, gate: str) -> Path:
    return base / "runtime" / "approvals" / f"{gate}.yaml"


def approval_status(base: Path, gate: str) -> str | None:
    return yaml_scalar(approval_path(base, gate), "status")


def record_approval(root: Path, gate: str, decision: str, actor: str, reason: str, evidence: str) -> int:
    if decision != "PENDING" and not actor.strip():
        print("--by is required for APPROVED or REJECTED decisions.", file=sys.stderr)
        return 2
    base = knowledge_root(root)
    path = approval_path(base, gate)
    timestamp = now()
    content = f"""schemaVersion: 2
gate: {gate}
decision:
  status: {decision}
  by: {y(actor)}
  at: {y(timestamp)}
  reason: {y(reason)}
  evidence: {y(evidence)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    history = path.parent / "history.jsonl"
    with history.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {"gate": gate, "status": decision, "by": actor, "at": timestamp, "reason": reason, "evidence": evidence},
                ensure_ascii=False,
            )
            + "\n"
        )
    print(f"Recorded {gate} gate as {decision}: {path}")
    return 0


def require_gate(base: Path, gate: str) -> str | None:
    status = approval_status(base, gate)
    return None if status == "APPROVED" else f"Gate '{gate}' must be APPROVED; found {status!r}."


def transition_state(root: Path, target: str, task_id: str, waiting_for: str, reason: str) -> int:
    base = knowledge_root(root)
    path = base / "runtime" / "state.yaml"
    current = yaml_scalar(path, "state")
    if current not in STATES:
        print("Runtime state is missing or invalid; run init first.", file=sys.stderr)
        return 2
    allowed = target in EXCEPTION_STATES or target in TRANSITIONS.get(current, set())
    if not allowed:
        print(f"Invalid orchestrator transition: {current} -> {target}", file=sys.stderr)
        return 2
    gate_error: str | None = None
    if target == "DESIGN":
        gate_error = require_gate(base, "analysis")
    elif current == "WAITING_HUMAN" and target == "IMPLEMENTATION":
        gate_error = require_gate(base, "patch")
    elif current == "WAITING_HUMAN" and target == "MEMORY_UPDATE":
        gate_error = require_gate(base, "memory")
    elif target == "REVIEW" and yaml_scalar(base / "runtime" / "patch-proposal.yaml", "status") != "APPLIED":
        gate_error = "Patch proposal must have status APPLIED before REVIEW."
    elif target == "COMPLETED":
        gate_error = require_gate(base, "memory")
        if gate_error is None and yaml_scalar(base / "runtime" / "memory-update-proposal.yaml", "status") != "APPLIED":
            gate_error = "Memory update proposal must have status APPLIED before COMPLETED."
    if gate_error:
        print(gate_error, file=sys.stderr)
        return 2
    if target == "APPROVAL_REQUIRED":
        waiting_for = "analysis"
    elif target == "WAITING_HUMAN" and waiting_for not in {"patch", "memory"}:
        print("WAITING_HUMAN requires --waiting-for patch or memory.", file=sys.stderr)
        return 2
    elif target != "WAITING_HUMAN":
        waiting_for = ""
    effective_task = task_id or yaml_scalar(path, "taskId") or ""
    timestamp = now()
    path.write_text(
        f"""schemaVersion: 2
orchestrator:
  state: {target}
  taskId: {y(effective_task)}
  waitingFor: {y(waiting_for)}
  updatedAt: {y(timestamp)}
  lastTransition:
    from: {current}
    to: {target}
    reason: {y(reason)}
""",
        encoding="utf-8",
    )
    history = base / "runtime" / "state-history.jsonl"
    with history.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"from": current, "to": target, "taskId": effective_task, "at": timestamp, "reason": reason}) + "\n")
    print(f"Orchestrator: {current} -> {target}")
    return 0


def require_file(path: Path, errors: list[str], nonempty: bool = False) -> None:
    if not path.is_file():
        errors.append(f"Missing required file: {path}")
    elif nonempty and not path.read_text(encoding="utf-8").strip():
        errors.append(f"Required file is empty: {path}")


def require_keys(path: Path, keys: list[str], errors: list[str]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for key in keys:
        if re.search(rf"^\s*{re.escape(key)}:\s*", text, re.MULTILINE) is None:
            errors.append(f"{path}: missing key '{key}'")


def expect(path: Path, key: str, allowed: set[str], errors: list[str]) -> None:
    actual = yaml_scalar(path, key)
    if actual not in allowed:
        errors.append(f"{path}: expected {key} in {sorted(allowed)}, found {actual!r}")


def validate_metadata(path: Path, errors: list[str]) -> None:
    require_keys(path, ["metadata", "source", "confidence", "lastVerified", "verifiedBy"], errors)
    confidence = yaml_scalar(path, "confidence")
    if confidence not in CONFIDENCE:
        errors.append(f"{path}: confidence must be low, medium, or high; found {confidence!r}")


def validate(root: Path, phase: str) -> int:
    base = knowledge_root(root)
    errors: list[str] = []
    templates = initial_templates(now())
    for relative in templates:
        require_file(base / relative, errors)
    index_path = base / "memory" / "index" / "knowledge-index.json"
    if index_path.is_file():
        try:
            index = json.loads(index_path.read_text(encoding="utf-8"))
            if index.get("schemaVersion") != 2 or not isinstance(index.get("entities"), list) or not isinstance(index.get("relations"), list):
                errors.append(f"{index_path}: invalid v2 knowledge index shape")
        except json.JSONDecodeError as exc:
            errors.append(f"{index_path}: invalid JSON: {exc}")
    for path in [
        base / "memory" / "project" / "project-context.yaml",
        base / "memory" / "project" / "architecture-map.yaml",
        base / "memory" / "project" / "constitution.yaml",
        base / "memory" / "domain" / "domain-index.yaml",
    ]:
        if path.is_file():
            validate_metadata(path, errors)
    for kind in ("feature", "bug", "change"):
        entity_root = base / "memory" / kind
        if entity_root.is_dir():
            for path in entity_root.rglob("*.yaml"):
                validate_metadata(path, errors)
    decision_root = base / "memory" / "decision"
    if decision_root.is_dir():
        for path in decision_root.glob("ADR-*.md"):
            validate_metadata(path, errors)

    context = base / "runtime" / "task-context.yaml"
    state = base / "runtime" / "state.yaml"
    task_id = yaml_scalar(context, "id") or ""
    if phase != "memory":
        expect(context, "status", {"READY"}, errors)
        require_keys(context, ["task", "id", "type", "goal", "retrieval", "affectedEntities"], errors)
    if phase == "context":
        expect(state, "state", {"CONTEXT_BUILD", "ANALYSIS"}, errors)
    contract = base / "runtime" / "change-contract.yaml"
    analysis_approval = approval_path(base, "analysis")
    if phase in {"analysis", "design", "patch-proposal", "implementation", "review", "memory-update"}:
        require_file(contract, errors)
        expect(contract, "status", {"READY"}, errors)
    if phase == "analysis":
        require_file(analysis_approval, errors)
        expect(analysis_approval, "status", {"PENDING", "APPROVED"}, errors)
        expect(state, "state", {"APPROVAL_REQUIRED"}, errors)
    plan = base / "runtime" / "implementation-plan.yaml"
    if phase in {"design", "patch-proposal", "implementation", "review", "memory-update"}:
        require_file(analysis_approval, errors)
        expect(analysis_approval, "status", {"APPROVED"}, errors)
        require_file(plan, errors)
        expect(plan, "status", {"READY"}, errors)
    if phase == "design":
        expect(state, "state", {"DESIGN", "IMPLEMENTATION"}, errors)
    patch = base / "runtime" / "patch-proposal.yaml"
    patch_diff = base / "runtime" / "patch-proposal.diff"
    patch_approval = approval_path(base, "patch")
    if phase in {"patch-proposal", "implementation", "review", "memory-update"}:
        require_file(patch, errors)
        require_file(patch_diff, errors, nonempty=True)
        require_file(patch_approval, errors)
    if phase == "patch-proposal":
        expect(patch, "status", {"PENDING_APPROVAL"}, errors)
        expect(patch_approval, "status", {"PENDING", "APPROVED"}, errors)
        expect(state, "state", {"WAITING_HUMAN", "IMPLEMENTATION"}, errors)
    change_proposal = base / "runtime" / "change-entity-proposal.yaml"
    change_log = base / "reports" / f"{task_id}-change-log.md"
    if phase in {"implementation", "review", "memory-update"}:
        expect(patch, "status", {"APPLIED"}, errors)
        expect(patch_approval, "status", {"APPROVED"}, errors)
        require_file(change_proposal, errors)
        if change_proposal.is_file():
            validate_metadata(change_proposal, errors)
        require_file(change_log, errors)
    if phase == "implementation":
        expect(state, "state", {"REVIEW"}, errors)
    review = base / "reports" / f"{task_id}-review.md"
    memory_proposal = base / "runtime" / "memory-update-proposal.yaml"
    memory_approval = approval_path(base, "memory")
    if phase in {"review", "memory-update"}:
        require_file(review, errors)
        if review.is_file() and re.search(r"^Outcome:\s*(PASS|FAIL|BLOCKED|WAITING_HUMAN)\s*$", review.read_text(encoding="utf-8"), re.MULTILINE) is None:
            errors.append(f"{review}: missing valid Outcome line")
        require_file(memory_proposal, errors)
        require_file(memory_approval, errors)
    if phase == "review":
        expect(memory_proposal, "status", {"PENDING_APPROVAL", "APPLIED"}, errors)
        expect(memory_approval, "status", {"PENDING", "APPROVED"}, errors)
        expect(state, "state", {"WAITING_HUMAN", "MEMORY_UPDATE", "COMPLETED"}, errors)
    if phase == "memory-update":
        expect(memory_proposal, "status", {"APPLIED"}, errors)
        expect(memory_approval, "status", {"APPROVED"}, errors)
        expect(state, "state", {"COMPLETED"}, errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Frontend Engineering Knowledge artifacts are valid for phase '{phase}'.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize v2 knowledge storage non-destructively")
    init_parser.add_argument("--root", type=Path, default=Path.cwd())

    entity_parser = subparsers.add_parser("new-entity", help="Create and index a governed engineering entity")
    entity_parser.add_argument("kind", choices=sorted(ENTITY_PATTERNS))
    entity_parser.add_argument("entity_id")
    entity_parser.add_argument("--root", type=Path, default=Path.cwd())
    entity_parser.add_argument("--title", required=True)
    entity_parser.add_argument("--domain", default="")

    context_parser = subparsers.add_parser("context", help="Build task context using explicit and structural retrieval")
    context_parser.add_argument("task_id")
    context_parser.add_argument("--root", type=Path, default=Path.cwd())
    context_parser.add_argument("--type", choices=["feature", "bug", "refactor"], required=True)
    context_parser.add_argument("--goal", required=True)
    context_parser.add_argument("--domain", default="")
    context_parser.add_argument("--target", action="append", default=[])
    context_parser.add_argument("--feature", default="")
    context_parser.add_argument("--bug", default="")
    context_parser.add_argument("--constraint", action="append", default=[])
    context_parser.add_argument("--non-goal", action="append", default=[])

    approval_parser = subparsers.add_parser("approval", help="Record a pending or explicit human gate decision")
    approval_parser.add_argument("--root", type=Path, default=Path.cwd())
    approval_parser.add_argument("--gate", choices=["analysis", "patch", "memory"], required=True)
    approval_parser.add_argument("--decision", choices=["PENDING", "APPROVED", "REJECTED"], required=True)
    approval_parser.add_argument("--by", default="")
    approval_parser.add_argument("--reason", default="")
    approval_parser.add_argument("--evidence", default="")

    state_parser = subparsers.add_parser("state", help="Apply a guarded orchestrator state transition")
    state_parser.add_argument("--root", type=Path, default=Path.cwd())
    state_parser.add_argument("--to", choices=sorted(STATES), required=True)
    state_parser.add_argument("--task-id", default="")
    state_parser.add_argument("--waiting-for", choices=["", "patch", "memory"], default="")
    state_parser.add_argument("--reason", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate v2 memory, gates, and workflow artifacts")
    validate_parser.add_argument("--root", type=Path, default=Path.cwd())
    validate_parser.add_argument(
        "--phase",
        choices=["memory", "context", "analysis", "design", "patch-proposal", "implementation", "review", "memory-update"],
        default="memory",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = args.root.expanduser().resolve()
    if args.command == "init":
        return initialize(root)
    if args.command == "new-entity":
        return create_entity(root, args.kind, args.entity_id, args.title, args.domain)
    if args.command == "context":
        return build_context(
            root,
            args.task_id,
            args.type,
            args.goal,
            args.domain,
            args.target,
            args.feature,
            args.bug,
            args.constraint,
            args.non_goal,
        )
    if args.command == "approval":
        return record_approval(root, args.gate, args.decision, args.by, args.reason, args.evidence)
    if args.command == "state":
        return transition_state(root, args.to, args.task_id, args.waiting_for, args.reason)
    return validate(root, args.phase)


if __name__ == "__main__":
    raise SystemExit(main())
