# Patch and Change proposals

## Patch proposal

Write `runtime/patch-proposal.yaml` before changing product files:

```yaml
schemaVersion: 2
taskId: TASK-001
status: PENDING_APPROVAL
baseRevision: "commit plus dirty-worktree description"
contractPath: docs/frontend-ai/runtime/change-contract.yaml
planPath: docs/frontend-ai/runtime/implementation-plan.yaml
diffPath: docs/frontend-ai/runtime/patch-proposal.diff
files:
  - path: src/example.ts
    operation: modify
    purpose: ""
    preservesUserChanges: []
scopeChecks: []
constitutionChecks: []
risks: []
verificationPlanned: []
generatedAt: 2026-08-04T00:00:00Z
appliedAt: ""
```

Write a standard unified diff to `runtime/patch-proposal.diff`. It must be reviewable and apply to the recorded base. Do not hide generated, formatting, or dependency changes outside the proposal.

After explicit approval and successful application, set `status: APPLIED` and record `appliedAt`. Material regeneration invalidates the old approval.

## Change Entity proposal

Write `runtime/change-entity-proposal.yaml` after applying and testing:

```yaml
schemaVersion: 2
metadata:
  source: [ai, git]
  confidence: medium
  lastVerified: 2026-08-04
  verifiedBy: ""
change:
  id: CHG-001
  status: proposed
  type: bug-fix
  taskId: TASK-001
  source:
    kind: worktree
    revision: ""
  files: []
  related:
    feature: ""
    bug: ""
    decisions: []
  description: "Engineering capability change, not raw file churn"
  verification: []
  regressions: []
```

Do not copy this proposal into `memory/change/` before Memory Update approval.

## Change log

Write `reports/<task-id>-change-log.md` with contract coverage, actual file changes, user changes preserved, proposal deviations, commands and results, limitations, rollback, and proposed knowledge changes.
