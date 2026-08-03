# Review report contract

Write `docs/frontend-ai/reports/<feature-id>-review-report.md` with these sections:

```markdown
# Review: <feature-id>

Outcome: PASS | FAIL | BLOCKED | NEED_HUMAN_REVIEW
Reviewed revision: <commit or worktree description>

## Findings

### [P1] Concise defect title
- Evidence: `src/path/file.ts:42`
- Contract: `REQ-001`, `AC-001`
- Impact: What breaks and for whom
- Required action: Smallest correct remediation

## Acceptance coverage

| Criterion | Evidence | Result |
| --- | --- | --- |
| AC-001 | test or file reference | PASS |

## UI, API, and interaction coverage

## Architecture and decision compliance

## Verification

| Command or check | Result | Notes |
| --- | --- | --- |

## Memory integrity

## Residual risks and next owner
```

Priorities:

- `P0`: active data loss, security compromise, or unusable critical path; stop release immediately.
- `P1`: high-impact correctness or contract failure likely in normal use; block release.
- `P2`: real moderate-impact defect, missing required edge case, or material maintainability risk; fix before release unless explicitly accepted.
- `P3`: low-risk improvement that does not block the contract; track separately.

Every finding must identify a reproducible condition and exact evidence. Do not report personal style preferences as defects. `PASS` requires no open P0-P2 findings and no unsupported acceptance criterion.
