# Artifact contract

All stages operate on one `frontend-spec/` directory. JSON artifacts use `schema_version: "1.0"`, stable IDs, relative source locators, and UTF-8 encoding. Generated content never outranks confirmed human decisions.

## Directory layout

```text
frontend-spec/
├── pipeline-state.json
├── context/project-context.json
├── requirement/
│   ├── requirement-analysis.json
│   ├── question-list.md
│   └── decision-log.md
├── api/
│   ├── api-map.json
│   └── request-response.md
├── ui/ui-tree.json
├── interaction/interaction-spec.json
├── flow/
│   ├── sequence-diagrams.md
│   └── state-models.md
├── document/frontend-development-spec.md
├── manual/override.md
└── history/change-log.json
```

## Authority order

When sources conflict, use this order and record the conflict:

1. Latest explicit user instruction
2. Active manual override or confirmed decision
3. Authoritative machine-readable API or repository contract
4. Product requirement source
5. UI source
6. Supported inference

An earlier decision remains in history after it is superseded.

## Stable IDs

Use `PAGE-###`, `RQ-###`, `RULE-###`, `Q-###`, `DEC-###`, `API-###`, `UI-###`, `IX-###`, and `CHG-###`. Preserve IDs across regeneration when the underlying concept remains the same. Never reuse a retired ID for a different concept.

## Pipeline stages

Use these exact keys in `pipeline-state.json`:

1. `project-context`
2. `requirement-analysis`
3. `requirement-clarification`
4. `api-analysis`
5. `ui-parsing`
6. `interaction-design`
7. `flow-generation`
8. `spec-generation`

Each stage contains `status`, `artifacts`, and `blockers`. Allowed statuses are `pending`, `in_progress`, `blocked`, and `complete`.

## Evidence and assumptions

Evidence locators contain a source path or URL plus a section, heading, line, frame, node, endpoint, or schema name when available. An assumption must contain its reason, owner, validation status, and affected IDs. If a missing answer can materially change user behavior, data integrity, permission, API use, or architecture, treat it as a blocker rather than an assumption.

## Completion contract

`ready_for_implementation` requires all eight stages complete, no blocking question, no unresolved required API/UI mapping, no interaction coverage gap, no unresolved override conflict, and a final document that exposes all non-blocking open items.
