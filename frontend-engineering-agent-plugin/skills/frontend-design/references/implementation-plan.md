# Implementation Plan

Write `docs/frontend-ai/runtime/implementation-plan.yaml`:

```yaml
schemaVersion: 2
taskId: TASK-001
status: READY
summary: ""
contractTraceability:
  - contractId: REQ-001
    acceptanceCriteria: [AC-001]
    prototypeRefs: [PROTO-001]
    interactionRefs: [INT-001]
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
  security: []
  performance: []
fileChanges:
  - path: src/example.ts
    operation: modify
    reason: ""
    symbols: []
    preserveUserChanges: []
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
patchStrategy:
  baseRevision: ""
  proposalPath: docs/frontend-ai/runtime/patch-proposal.diff
  conflictChecks: []
  diffReview: []
dependencies: []
risks: []
rollout: []
rollback: []
constitutionCompliance: []
decisionProposals: []
memoryUpdateCandidates: []
openQuestions: []
```

Allowed file operations are `create`, `modify`, `move`, and `delete`. A deletion requires callers, migration, rollback, and explicit scope justification.

For every contract item, preserve the chain `contract -> prototype/interaction evidence -> acceptance -> step -> file -> verification` when the task is user-facing. Mark the plan `READY` only when no open question or design gap can materially alter the patch.
