# Task context and Change Contract

## Canonical v2 knowledge layout

Store authoritative knowledge under `docs/frontend-ai/memory/`:

```text
memory/
├── project/
├── domain/
├── feature/
├── bug/
├── change/
├── decision/
├── schema/
└── index/
```

Store current workflow artifacts under `runtime/` and review output under `reports/`. Treat the `features`, `bugs`, `changes`, `decisions`, and `schema` labels in the architecture overview as logical knowledge views; do not duplicate authoritative entities outside `memory/`.

If v1 paths such as `project-memory/`, `domain-memory/`, or top-level `features/` exist, read them as legacy evidence and propose migration. Never move or delete them automatically.

## Governance metadata

Every durable memory entity must contain:

```yaml
metadata:
  source: [human, ai, git, inferred]
  confidence: high
  lastVerified: 2026-08-04
  verifiedBy: human-identifier
```

Use only sources that actually contributed. Allowed confidence values are `low`, `medium`, and `high`. Inferred or unapproved knowledge must not be marked high confidence or human-verified.

## Task context

`runtime/task-context.yaml` must contain:

```yaml
schemaVersion: 2
task:
  id: TASK-001
  type: bug
  goal: "Fix customer list pagination"
  domain: customer
  targets: [src/views/CustomerList.vue]
  featureId: customer-management
  bugId: BUG-003
constraints: []
nonGoals: []
affectedEntities:
  - type: feature
    id: customer-management
    path: docs/frontend-ai/memory/feature/customer-management
    confidence: high
    retrievalLayer: explicit
files: []
rules: []
retrieval:
  explicit: []
  structural: []
  semantic:
    enabled: false
    reason: "Not implemented in the MVP"
generatedAt: 2026-08-04T00:00:00Z
```

Do not pass an unfiltered memory dump into a Skill. Cite retrieval layer and confidence for every affected entity.

## Change Contract

Write `runtime/change-contract.yaml`:

```yaml
schemaVersion: 2
taskId: TASK-001
type: feature
status: READY
summary: ""
facts: []
inferences: []
assumptions: []
unknowns: []
goals: []
nonGoals: []
currentBehavior: []
desiredBehavior: []
requirements:
  - id: REQ-001
    statement: ""
    source: human
bug:
  observed: []
  expected: []
  reproduction: []
  rootCauseHypotheses: []
  relatedFeature: ""
refactor:
  invariants: []
  motivation: []
ui: []
api: []
interactions: []
affectedFiles: []
affectedEntities: []
acceptanceCriteria:
  - id: AC-001
    tracesTo: [REQ-001]
    given: ""
    when: ""
    then: ""
risks: []
constitutionRules: []
memoryEvidence: []
```

Use `DRAFT` while blocking ambiguity remains. Use `READY` only after every requested behavior or bug condition has acceptance evidence. Approval belongs in `runtime/approvals/analysis.yaml`, never inside the contract.
