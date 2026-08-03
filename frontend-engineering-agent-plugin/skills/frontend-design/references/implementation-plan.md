# Implementation plan contract

Write `docs/frontend-ai/features/<feature-id>/implementation.yaml` with this minimum shape:

```yaml
schemaVersion: 1
featureId: customer-import
status: READY
summary: ""
contractTraceability:
  - requirementId: REQ-001
    acceptanceCriteria: [AC-001]
    steps: [STEP-001]
approach:
  selected: ""
  rationale: ""
  alternatives:
    - option: ""
      rejectedBecause: ""
architecture:
  routes: []
  pages: []
  components: []
  api: []
  state: []
  interactions: []
  styling: []
  accessibility: []
fileChanges:
  - path: src/example.ts
    operation: modify
    reason: ""
    symbols: []
steps:
  - id: STEP-001
    description: ""
    dependsOn: []
    files: []
    verification: []
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
```

Allowed operations are `create`, `modify`, `move`, and `delete`. Use `status: READY` only after the design gate passes. A planned deletion must include its callers, migration, and rollback path.

For traceability, each requirement must map to one or more acceptance criteria, steps, files, and verification items. Do not substitute broad prose for these links.
