# Artifact contract

All stages operate on one selected `<feature-root>` under a developer-confirmed absolute `<spec-root>`. `<spec-root>/catalog.json` registers isolated feature roots. JSON artifacts use `schema_version: "1.0"`, stable IDs, relative source locators, and UTF-8 encoding. Generated content never outranks confirmed human decisions.

## Directory layout

```text
<confirmed-parent>/frontend-spec/       # selected <spec-root>
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
        ├── implementation/                 # implement_and_validate only
        │   ├── restoration-brief.md
        │   └── visual-validation.md
        ├── manual/override.md
        └── history/change-log.json
```

For backward compatibility, a catalog may register one legacy feature with `path: "."`; its existing root-level artifacts remain in place. New features still use `features/<feature-id>/`.

## Feature isolation

Use a normalized lowercase hyphen-case `feature_id` for every new feature. An adopted legacy feature preserves its existing ID even when it predates that rule. The catalog path is either `features/<feature-id>` or `.` for one adopted legacy feature. Stable IDs, decisions, overrides, history, readiness, and validation are scoped to one feature root. Never resolve references across feature roots or silently reuse an existing root for a different requirement.

Before any feature artifact is changed, list registered features and choose `resume`, `create`, or explicitly approved legacy adoption. If that choice is ambiguous, ask the developer and stop.

## Output location gate

Before listing, reading, or creating plugin artifacts, display the exact absolute `<spec-root>` and obtain explicit developer confirmation. The workspace root is only a suggested parent and is never an automatic default. A terminal `cd`, repository selection, existing folder, relative path, or silence does not confirm the location. When the developer names a parent directory, append `frontend-spec`; when they name an exact path ending in `frontend-spec`, preserve it. Confirmation grants access only to plugin artifacts inside `<spec-root>` and does not widen the frontend source boundary.

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

`ready_for_implementation` completes machine validation of the specification pipeline only. For an `implement_and_validate` run, the developer must approve the final specification before the restoration brief is prepared. Delivery additionally requires an approved `implementation/restoration-brief.md`, scoped application changes, and a completed `implementation/visual-validation.md` showing design and regression visual results. A skipped, failed, or blocked visual comparison must remain visible and must not be reported as delivery completion.

## Source boundary

Do not discover project background. The allowed default inputs are requirements, prototypes, and API contracts. Read code only when the user explicitly supplies or names a path, and then only within the named frontend scope plus the minimum direct frontend dependencies needed to understand it. Missing evidence becomes a question or gap, never a reason to scan the repository.

In `implement_and_validate` mode, the exact target page and dashboard frontend root are separate required approvals. The permitted implementation boundary includes the target page, minimum direct frontend imports, relevant semantic token/style files, focused tests, and the selected visual scenario's config and references. It excludes backend code, infrastructure, unrelated frontend pages, and general repository discovery.

## Input gate

Before reading user workspace files or initializing artifacts, classify requirement, prototype, and API input as `provided`, `explicitly_unavailable`, or `missing`, and classify output location as `confirmed`, `proposed`, or `missing`. A feature title or one-line command is not a provided requirement; a project/page name is not a provided prototype; a vague claim of backend support is not a provided API contract. Stop and ask for every missing source plus exact output-location confirmation in one response. Silence never means unavailable or confirmed. Continue only when every source category is provided or explicitly unavailable and the exact absolute `<spec-root>` is confirmed.
