# Review and Memory Sync

## Review report

Write `reports/<task-id>-review.md`:

```markdown
# Review: TASK-001

Outcome: PASS | FAIL | BLOCKED | WAITING_HUMAN
Reviewed revision: <commit and worktree>
Approved patch: docs/frontend-ai/runtime/patch-proposal.diff

## Findings

### [P1] Concise defect title
- Evidence: `src/path/file.ts:42`
- Contract: `REQ-001`, `AC-001`
- Constitution: `RULE-API-001`
- Impact: What breaks and for whom
- Required action: Smallest correct remediation

## Contract and bug coverage
## Regression assessment
## Architecture and Constitution
## Verification
## Memory integrity
## Residual risks and next owner
```

Priorities:

- `P0`: active data loss, security compromise, or unusable critical path.
- `P1`: high-impact correctness or contract failure in normal use.
- `P2`: confirmed moderate-impact defect, missing required edge case, or material maintainability risk.
- `P3`: non-blocking low-risk improvement.

Every finding requires a reproducible condition and exact evidence. `PASS` requires no open P0-P2 finding and no unsupported contract criterion.

## Memory Update Proposal

Write `runtime/memory-update-proposal.yaml`:

```yaml
schemaVersion: 2
taskId: TASK-001
status: PENDING_APPROVAL
reviewOutcome: PASS
changes:
  - action: create
    target: docs/frontend-ai/memory/change/CHG-001/change.yaml
    source: docs/frontend-ai/runtime/change-entity-proposal.yaml
    reason: "Persist the reviewed engineering change"
    confidenceBefore: medium
    confidenceAfter: high
  - action: update
    target: docs/frontend-ai/memory/index/knowledge-index.json
    reason: "Index the new Change relation"
governance:
  requiresHumanApproval: true
  unverifiedClaims: []
  rejectedCandidates: []
generatedAt: 2026-08-04T00:00:00Z
appliedAt: ""
```

Allowed actions are `create`, `update`, and `deprecate`. Never silently delete knowledge. After explicit approval, apply only listed changes, set verified metadata accurately, update the index, set proposal status `APPLIED`, and record `appliedAt`.

Code change does not prove business change. Do not raise confidence or set `verifiedBy` to a human unless that human explicitly confirmed the proposal.
