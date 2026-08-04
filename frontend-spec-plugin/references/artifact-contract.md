# Artifact contract

All stages operate on one selected `<feature-root>`. `frontend-spec/catalog.json` registers isolated feature roots. JSON artifacts use `schema_version: "1.0"`, stable IDs, relative source locators, and UTF-8 encoding. Generated content never outranks confirmed human decisions.

## Directory layout

```text
frontend-spec/
├── catalog.json
└── features/
    └── <feature-id>/              # selected <feature-root>
        ├── pipeline-state.json
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

For backward compatibility, a catalog may register one legacy feature with `path: "."`; its existing root-level artifacts remain in place. New features still use `features/<feature-id>/`.

## Feature isolation

Use a normalized lowercase hyphen-case `feature_id` for every new feature. An adopted legacy feature preserves its existing ID even when it predates that rule. The catalog path is either `features/<feature-id>` or `.` for one adopted legacy feature. Stable IDs, decisions, overrides, history, readiness, and validation are scoped to one feature root. Never resolve references across feature roots or silently reuse an existing root for a different requirement.

Before any feature artifact is changed, list registered features and choose `resume`, `create`, or explicitly approved legacy adoption. If that choice is ambiguous, ask the developer and stop.

## Authority order

When sources conflict, use this order and record the conflict:

1. Latest explicit user instruction
2. Active manual override or confirmed decision
3. Product requirement source for product behavior
4. UI prototype for visible structure and visual states
5. Authoritative machine-readable API contract for backend capability
6. Explicitly supplied frontend code for existing implementation facts only
7. Supported inference

An earlier decision remains in history after it is superseded.

## Stable IDs

Use `PAGE-###`, `RQ-###`, `RULE-###`, `Q-###`, `DEC-###`, `API-###`, `UI-###`, `IX-###`, and `CHG-###`. Preserve IDs across regeneration when the underlying concept remains the same. Never reuse a retired ID for a different concept.

## Pipeline stages

Use these exact keys in `pipeline-state.json`:

1. `requirement-analysis`
2. `requirement-clarification`
3. `ui-parsing`
4. `api-analysis`
5. `interaction-design`
6. `flow-generation`
7. `spec-generation`

Each stage contains `status`, `artifacts`, and `blockers`. Allowed statuses are `pending`, `in_progress`, `blocked`, and `complete`.

## Evidence and assumptions

Evidence locators contain a source path or URL plus a section, heading, line, frame, node, endpoint, or schema name when available. An assumption must contain its reason, owner, validation status, and affected IDs. If a missing answer can materially change user behavior, data integrity, permission, API use, or architecture, treat it as a blocker rather than an assumption.

## Completion contract

`ready_for_implementation` requires all seven stages complete, no blocking question, no unresolved required API/UI mapping, no interaction coverage gap, no unresolved override conflict, and a final document that exposes all non-blocking open items.

## Source boundary

Do not discover project background. The allowed default inputs are requirements, prototypes, and API contracts. Read code only when the user explicitly supplies or names a path, and then only within the named frontend scope plus the minimum direct frontend dependencies needed to understand it. Missing evidence becomes a question or gap, never a reason to scan the repository.

## Input gate

Before reading user workspace files or initializing artifacts, classify requirement, prototype, and API input as `provided`, `explicitly_unavailable`, or `missing`. A feature title or one-line command is not a provided requirement; a project/page name is not a provided prototype; a vague claim of backend support is not a provided API contract. Stop and ask for all `missing` categories in one response. Silence never means unavailable. Continue only when every category is provided or the user explicitly confirms it is unavailable.
