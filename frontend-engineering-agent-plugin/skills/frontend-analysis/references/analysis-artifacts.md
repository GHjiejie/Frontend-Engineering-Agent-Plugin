# Analysis artifacts

Use YAML block lists for structured items and stable identifiers for requirements and acceptance criteria. Keep evidence paths relative to the repository root.

## `feature.yaml`

Required top-level fields:

```yaml
schemaVersion: 1
feature:
  id: customer-import
  title: Customer import
  domain: customer
  status: ANALYZING
  orchestratorState: FEATURE_CONTRACT_READY
  contractReady: true
  implementationReady: false
  reviewStatus: NOT_RUN
  createdAt: 2026-08-03T00:00:00Z
  updatedAt: 2026-08-03T00:00:00Z
  owners: []
  tags: []
```

Allowed feature lifecycle states: `PROPOSED`, `ANALYZING`, `DESIGNED`, `IMPLEMENTING`, `RELEASED`, `DEPRECATED`.

Allowed orchestrator states: `NEW`, `CONTEXT_LOADING`, `ANALYZING`, `FEATURE_CONTRACT_READY`, `DESIGN_READY`, `IMPLEMENTING`, `VERIFYING`, `MEMORY_UPDATING`, `COMPLETED`, `BLOCKED`, `CONFLICT`, `NEED_HUMAN_REVIEW`, `FAILED`.

Allowed review states: `NOT_RUN`, `PASS`, `FAIL`, `BLOCKED`, `NEED_HUMAN_REVIEW`.

## `contract.yaml`

Required sections:

```yaml
schemaVersion: 1
featureId: customer-import
status: READY
summary: ""
goals: []
actors: []
scope: []
outOfScope: []
requirements:
  - id: REQ-001
    statement: ""
    source: ""
ui:
  entryPoints: []
  states: []
  responsive: []
  accessibility: []
api:
  endpoints: []
  dataContracts: []
  errorMapping: []
interactions:
  - id: INT-001
    trigger: ""
    request: ""
    success: ""
    failure: ""
acceptanceCriteria:
  - id: AC-001
    requirements: [REQ-001]
    given: ""
    when: ""
    then: ""
constraints: []
assumptions: []
openQuestions: []
reuseCandidates: []
affectedAreas: []
```

Use `status: DRAFT` while blocking questions remain and `status: READY` only after the contract gate passes.

## `risk-report.md`

Include evidence, likelihood, impact, mitigation, owner or decision-maker, and blocking status for each risk. Cover at least requirement, API, UI, interaction, architecture, data migration, compatibility, security, accessibility, testing, and delivery risks; state `Not applicable` with a reason when appropriate.

## Memory files

- `project-context.yaml`: framework, language, UI system, state, build, package manager, commands, and non-negotiable rules.
- `project-index.json`: routes, views, components, APIs, stores, composables, tests, and their source paths.
- `architecture-map.yaml`: layer names, allowed paths, dependency direction, and conventions.
- `feature-registry.yaml`: feature id, status, domain, path, and update time.
- `evolution-log.jsonl`: one JSON object per released capability change; do not use it as a raw Git log.
- `decisions/ADR-*.md`: context, decision, alternatives, consequences, and status.
- `memory-index.json`: memory file paths, update times, source revision, and optional hashes.
- `domain-memory/*.yaml`: business entities, statuses, rules, invariants, and provenance.
