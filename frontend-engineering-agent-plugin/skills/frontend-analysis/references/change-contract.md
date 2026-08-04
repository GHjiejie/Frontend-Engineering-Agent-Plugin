# Task context and Change Contract

## Prototype and interaction input gate

Classify every task before completing analysis:

- `USER_FACING`: changes anything a user can see or do. A human-provided prototype and complete interaction effects are mandatory.
- `NONE`: changes only internal implementation while UI and interaction behavior remain invariant. Record both the reason and repository evidence.

For `USER_FACING`, require an inspectable prototype that identifies the affected screen, frame, node, or annotated region. Record the source locator and version when available. A link that the agent cannot inspect is not sufficient evidence.

Require human-provided interaction details for every affected click or action:

- trigger and preconditions;
- resulting visual state, navigation, modal, drawer, menu, or message;
- client and server state changes and side effects;
- loading, success, failure, empty, disabled, permission, validation, cancel/back, retry, and repeated-action behavior where applicable;
- responsive or device-specific differences.

Use `DRAFT`, enter `BLOCKED`, and request the missing evidence when the prototype or interaction effects are missing, inaccessible, contradictory, or incomplete. Do not infer them and do not move to analysis approval.

For `NONE`, `prototypeNotRequiredReason` and `uiInvariantEvidence` must both be non-empty. Reclassify the task as `USER_FACING` if the evidence cannot prove that UI and interaction behavior remain unchanged.

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
designEvidence:
  uiImpact: USER_FACING
  prototypeRequired: true
  prototypeStatus: PROVIDED
  prototypeProvidedBy: human
  prototypes:
    - id: PROTO-001
      type: figma
      locator: "Figma file/page/frame-or-node"
      version: ""
      scope: []
  interactionStatus: COMPLETE
  interactionProvidedBy: human
  interactionFlows:
    - id: INT-001
      prototypeRef: PROTO-001
      trigger: ""
      preconditions: []
      action: ""
      result:
        visual: ""
        navigation: ""
        stateChanges: []
        sideEffects: []
      alternateStates:
        loading: ""
        success: ""
        failure: ""
        disabled: ""
        permission: ""
        validation: ""
        cancelOrBack: ""
  uiStates:
    - id: UI-STATE-001
      prototypeRef: PROTO-001
      name: default
      expected: ""
  responsiveRules: []
  unresolvedDesignGaps: []
  prototypeNotRequiredReason: ""
  uiInvariantEvidence: []
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

For `uiImpact: NONE`, use `prototypeRequired: false`, `prototypeStatus: NOT_REQUIRED`, `prototypeProvidedBy: not-required`, `interactionStatus: NOT_REQUIRED`, and `interactionProvidedBy: not-required`; leave prototype/interaction lists empty and provide non-empty `prototypeNotRequiredReason` and `uiInvariantEvidence`.

Use `DRAFT` while blocking ambiguity or any unresolved design gap remains. Use `READY` only after every requested behavior or bug condition has acceptance evidence and the prototype/interaction gate is valid. Approval belongs in `runtime/approvals/analysis.yaml`, never inside the contract.
